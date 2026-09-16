"""Local database connections for the AstroDB workspace."""
import sqlite3


class Database:
    def __init__(self, path=":memory:", engine="duckdb", read_only=False):
        self.engine = engine
        if engine == "duckdb":
            import duckdb
            self.connection = duckdb.connect(str(path), read_only=read_only)
        elif engine == "sqlite":
            if read_only:
                from pathlib import Path
                if str(path) == ":memory:":
                    raise ValueError("Read-only mode requires a database file")
                self.connection = sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True)
            else:
                self.connection = sqlite3.connect(str(path))
        else:
            raise ValueError(f"Unknown database engine: {engine}")

    def query(self, sql):
        cursor = self.connection.execute(sql)
        columns = [column[0] for column in cursor.description] if cursor.description else []
        rows = cursor.fetchall() if columns else []
        return columns, rows

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        if self.engine == "sqlite":
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        self.close()
