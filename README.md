# AstroDB

A local SQL workspace powered by DuckDB and SQLite.

AstroDB provides a branded command-line interface, a local visual query workspace, and a website. It uses the existing engines without changing their SQL dialects or file formats. This is an early implementation, not a new database engine.

## Install

Requires Python 3.10 or newer.

```sh
git clone https://github.com/ThreadCrash/AstroDB.git
cd AstroDB
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate
python -m pip install -e .
```

## Visual workspace

```sh
astrodb studio
```

Open http://127.0.0.1:8042. Select DuckDB or SQLite, enter SQL, and run it. Each engine uses a separate in-memory database that lasts until Studio stops. SQLite transactions in Studio remain open until you explicitly run `COMMIT` or `ROLLBACK`.

Studio is a local development tool with access to files available to your account through SQL. It is bound to localhost and is not intended to be exposed as a network service.

## Query a database

```sh
astrodb query "SELECT 42 AS answer;"
astrodb query "SELECT * FROM read_csv('data.csv');" --format json
astrodb query "SELECT * FROM read_parquet('data.parquet');" --format csv
astrodb query "CREATE TABLE sample (answer INTEGER);" --database demo.astrodb
astrodb query "INSERT INTO sample VALUES (42);" --database demo.astrodb
astrodb query "SELECT * FROM sample;" --database demo.astrodb --read-only
astrodb query "SELECT sqlite_version();" --engine sqlite
astrodb query "SELECT * FROM sample;" --engine sqlite --database demo.sqlite
astrodb query --file query.sql --database demo.astrodb
```

SQLite accepts one statement per query. DuckDB and SQLite have different dialects and database formats; selecting another engine does not convert a database. JSON output represents date/time and other non-JSON values as strings.

## Python

```python
from astrodb import Database

with Database("demo.astrodb") as db:
    columns, rows = db.query("SELECT 42 AS answer")
```

SQLite changes commit on a successful context exit and roll back on an exception.

## Website

Serve `website/` with any static server:

```sh
python -m http.server 8765 --directory website
```

The landing page's interactive example is a predefined browser preview. Studio executes real SQL.

## Development

```sh
python -m unittest discover -s tests -v
```

The supplied DuckDB fork and DB Browser for SQLite fork are not vendored or rebranded in this release. The latter is a desktop browser, not a SQL engine. Integrating that Qt codebase and producing native installers remain future work.

AstroDB branding and interface are independent of DuckDB and DB Browser for SQLite. See [third-party notices](THIRD_PARTY_NOTICES.md) for origins and licensing.
