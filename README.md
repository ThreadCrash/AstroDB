# AstroDB

AstroDB is a local SQL database distribution with a native command-line shell and desktop application.

The analytical engine is built from our DuckDB fork. The desktop application is built from our DB Browser for SQLite fork, with an AstroDB SQL window linked directly to the native engine.

## Command line

```sh
astrodb example.astrodb
astrodb example.astrodb -c "CREATE TABLE numbers AS SELECT * FROM range(10);"
astrodb example.astrodb -c "SELECT SUM(range) FROM numbers;"
astrodb -c "SELECT * FROM read_csv('sales.csv');"
astrodb -c "SELECT * FROM 'data.parquet';"
```

The shell uses `.astrodbrc` and `.astrodb_history` in your home directory. `ASTRODB_HISTORY` overrides the history path. Use `astrodb -help` for options.

## Desktop

Launch **AstroDB Desktop.exe**. The main window opens and edits SQLite databases, including tables, indexes, CSV imports, and SQL queries.

Choose **Tools > AstroDB SQL** for analytical queries. This window opens or creates `.astrodb` databases and queries CSV and Parquet files. SQL runs on a worker thread and can be cancelled. Results show up to 1,000 rows. Transactions and temporary tables persist between queries in the same window.

AstroDB files use the DuckDB database format. SQLite files remain SQLite files. The two query windows use their respective SQL dialects; opening a file does not convert its format.

## Build on Windows

Prerequisites:

- Visual Studio with the C++ desktop workload and Windows SDK.
- CMake on PATH.
- Qt 6 with Core5Compat and Qt tools. This build uses Qt 6.8.3 for MSVC 2022.
- Python 3 for downloading and verifying the SQLite source archive during the build.

```powershell
git clone --recurse-submodules https://github.com/ThreadCrash/AstroDB.git
cd AstroDB
./scripts/build_windows.ps1 -QtRoot "C:/Qt/6.8.3/msvc2022_64"
```

The default generator is Visual Studio 2026. Pass `-Generator "Visual Studio 17 2022"` for Visual Studio 2022. `-Jobs` controls parallel compilation.

The script builds the engine, SQLite, and the desktop application, runs native tests, and places the portable application in `releases/AstroDB/`.

The engine source is a development snapshot, pinned by the engine submodule. Its reported engine version is v2.0.0; the AstroDB distribution version is 0.1.0. This is a development build.

## Website

The static website is in `website/`. Run `python scripts/update_website.py` to write a self-contained HTML copy to `../Website/AstroDB.html`.

## Optional Python interface

```sh
python -m pip install -e .
astrodb-python query "SELECT 42;"
astrodb-python studio
python -m unittest discover -s tests -v
```

The Python interface uses the installed DuckDB Python package and Python's SQLite module. It is separate from the native engine build.

## Licensing

Licenses apply per component. AstroDB's original Python and website code use MIT. The native engine retains DuckDB's MIT license. The desktop code retains its existing MPL 2.0 and GPL 3.0 licensing and third-party notices. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
