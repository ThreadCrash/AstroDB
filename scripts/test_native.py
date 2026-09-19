from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys

shell = str(Path(sys.argv[1]).resolve())

def query(database, sql, cwd):
    run = subprocess.run([shell, str(database), "-csv", "-c", sql], cwd=cwd,
                         capture_output=True, text=True)
    if run.returncode:
        raise RuntimeError(run.stderr)
    return run.stdout.strip()

with TemporaryDirectory() as folder:
    root = Path(folder)
    database = root / "sample.astrodb"
    query(database, "CREATE TABLE numbers AS SELECT * FROM range(10);", root)
    assert query(database, "SELECT SUM(range) AS total FROM numbers;", root) == "total\n45"
    (root / "sales.csv").write_text("category,amount\nTools,12\nBooks,7\nTools,8\n")
    assert query(database, "SELECT category, SUM(amount) AS total FROM read_csv('sales.csv') GROUP BY category ORDER BY category;", root) == "category,total\nBooks,7\nTools,20"
    query(database, "COPY numbers TO 'numbers.parquet' (FORMAT PARQUET);", root)
    assert query(database, "SELECT COUNT(*) AS count FROM 'numbers.parquet';", root) == "count\n10"
    invalid = subprocess.run([shell, str(database), "-c", "SELECT * FROM absent_table;"],
                             cwd=root, capture_output=True, text=True)
    assert invalid.returncode != 0 and "absent_table" in invalid.stderr
    version = subprocess.check_output([shell, "-version"], text=True)
    assert version.startswith("AstroDB 0.1.0")
    print("Native SQL: persistence, CSV, Parquet, error status, and version passed.")
