import tempfile
import unittest
from pathlib import Path

from astrodb import Database


class DatabaseTest(unittest.TestCase):
    def test_both_engines(self):
        for engine in ("duckdb", "sqlite"):
            with self.subTest(engine=engine), Database(engine=engine) as database:
                database.query("CREATE TABLE missions (name VARCHAR, launched INTEGER)")
                database.query("INSERT INTO missions VALUES ('Voyager', 1977), ('Juno', 2011)")
                columns, rows = database.query("SELECT name FROM missions WHERE launched < 2000")
                self.assertEqual(columns, ["name"])
                self.assertEqual(rows, [("Voyager",)])

    def test_persistence_and_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            for engine in ("duckdb", "sqlite"):
                path = Path(directory) / engine
                with Database(path, engine) as database:
                    database.query("CREATE TABLE sample (answer INTEGER)")
                    database.query("INSERT INTO sample VALUES (42)")
                with Database(path, engine, read_only=True) as database:
                    self.assertEqual(database.query("SELECT answer FROM sample")[1], [(42,)])
                    with self.assertRaises(Exception):
                        database.query("INSERT INTO sample VALUES (43)")

    def test_sqlite_rollback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rollback.sqlite"
            with Database(path, "sqlite") as database:
                database.query("CREATE TABLE sample (answer INTEGER)")
            with self.assertRaises(RuntimeError):
                with Database(path, "sqlite") as database:
                    database.query("INSERT INTO sample VALUES (42)")
                    raise RuntimeError("cancel")
            with Database(path, "sqlite") as database:
                self.assertEqual(database.query("SELECT * FROM sample")[1], [])


if __name__ == "__main__":
    unittest.main()
