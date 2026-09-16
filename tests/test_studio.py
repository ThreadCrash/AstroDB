import json
import socket
import subprocess
import sys
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class StudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
        cls.url = f"http://127.0.0.1:{port}"
        code = f"from unittest.mock import patch; from astrodb.studio import serve; patch('webbrowser.open').start(); serve(port={port})"
        cls.process = subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                with urlopen(cls.url, timeout=1):
                    return
            except (URLError, TimeoutError):
                time.sleep(0.1)
        cls.process.terminate()
        cls.process.wait()
        raise RuntimeError("Studio did not start")

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait(timeout=10)

    def request(self, engine, sql, origin=None):
        body = json.dumps({"engine": engine, "sql": sql}).encode()
        return Request(self.url + "/query", data=body, headers={"Content-Type": "application/json", "Origin": origin or self.url})

    def test_queries_across_requests(self):
        for engine in ("duckdb", "sqlite"):
            with self.subTest(engine=engine):
                for sql in ("CREATE TABLE sample (answer INTEGER)", "INSERT INTO sample VALUES (42)"):
                    with urlopen(self.request(engine, sql), timeout=5):
                        pass
                with urlopen(self.request(engine, "SELECT * FROM sample"), timeout=5) as response:
                    self.assertEqual(json.load(response)["rows"], [[42]])

    def test_rejects_external_origin(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(self.request("sqlite", "SELECT 1", "https://example.com"), timeout=5)
        self.assertEqual(error.exception.code, 403)

    def test_sql_error_returns_message(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(self.request("sqlite", "SELECT * FROM missing_table"), timeout=5)
        self.assertEqual(error.exception.code, 400)
        self.assertIn("error", json.load(error.exception))
