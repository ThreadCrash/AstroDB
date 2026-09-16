import json
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files

from astrodb import Database


def serve(host="127.0.0.1", port=8042):
    worker = ThreadPoolExecutor(max_workers=1)
    databases = worker.submit(lambda: {engine: Database(engine=engine) for engine in ("duckdb", "sqlite")}).result()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ("/", "/studio"):
                self.send_error(404)
                return
            content = files("astrodb").joinpath("studio.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def do_POST(self):
            if self.path != "/query":
                self.send_error(404)
                return
            expected = f"http://{host}:{port}"
            if self.headers.get("Origin") != expected or self.headers.get("Host") != f"{host}:{port}":
                self.send_error(403)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 1_000_000:
                    raise ValueError("Invalid request size")
                request = json.loads(self.rfile.read(length))
                columns, rows = worker.submit(lambda: databases[request["engine"]].query(request["sql"])).result()
                result = {"columns": columns, "rows": rows}
                status = 200
            except Exception as error:
                result = {"error": str(error)}
                status = 400
            content = json.dumps(result, default=str).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    url = f"http://{host}:{port}"
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"AstroDB Studio: {url}\nIn-memory databases last until you stop Studio. Press Ctrl+C to stop.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        for database in databases.values():
            worker.submit(database.close).result()
        worker.shutdown()
