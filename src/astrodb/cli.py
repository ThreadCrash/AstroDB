import argparse
import csv
import json
import sys
from pathlib import Path

from astrodb import Database


def print_result(columns, rows, output):
    if output == "json":
        print(json.dumps([dict(zip(columns, row)) for row in rows], default=str))
    elif output == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(columns)
        writer.writerows(rows)
    elif columns:
        values = [[str(value) if value is not None else "NULL" for value in row] for row in rows]
        widths = [max(len(column), *(len(row[i]) for row in values)) if values else len(column) for i, column in enumerate(columns)]
        print(" | ".join(column.ljust(width) for column, width in zip(columns, widths)))
        print("-+-".join("-" * width for width in widths))
        for row in values:
            print(" | ".join(value.ljust(width) for value, width in zip(row, widths)))
        print(f"({len(rows)} rows)")
    else:
        print("Statement complete")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="astrodb-python", description="AstroDB Python interface for DuckDB and SQLite")
    subcommands = parser.add_subparsers(dest="command", required=True)
    studio = subcommands.add_parser("studio", help="Open the local visual SQL workspace")
    studio.add_argument("--port", type=int, default=8042)
    query = subcommands.add_parser("query", help="Execute a SQL statement")
    query.add_argument("sql", nargs="?", help="SQL statement; omit when using --file")
    query.add_argument("--file", type=Path, help="Read SQL from a UTF-8 file")
    query.add_argument("--database", default=":memory:", help="Database path (default: in memory)")
    query.add_argument("--engine", choices=["duckdb", "sqlite"], default="duckdb")
    query.add_argument("--read-only", action="store_true")
    query.add_argument("--format", choices=["table", "json", "csv"], default="table")
    args = parser.parse_args(argv)
    if args.command == "studio":
        from astrodb.studio import serve
        serve(port=args.port)
        return 0
    if bool(args.sql) == bool(args.file):
        parser.error("Provide either a SQL statement or --file")
    try:
        sql = args.file.read_text(encoding="utf-8") if args.file else args.sql
        with Database(args.database, args.engine, args.read_only) as database:
            columns, rows = database.query(sql)
        print_result(columns, rows, args.format)
        return 0
    except Exception as error:
        print(f"astrodb: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
