# Third-party components

AstroDB is an independent distribution derived from existing database projects. Original copyright notices and licenses remain in the source and portable package.

## Native engine

- Source: [ThreadCrash/duckdb](https://github.com/ThreadCrash/duckdb), AstroDB branch.
- Derived from [DuckDB](https://github.com/duckdb/duckdb).
- MIT license. The original Stichting DuckDB Foundation copyright is preserved.
- Public C/C++ identifiers, SQL compatibility functions, extension protocols, and the database file format retain their existing names for compatibility.
- Bundled engine dependencies retain the notices in the engine's `third_party/` directories.

## Desktop

- Source: [ThreadCrash/sqlitebrowser-forked](https://github.com/ThreadCrash/sqlitebrowser-forked), AstroDB branch.
- Derived from [DB Browser for SQLite](https://github.com/sqlitebrowser/sqlitebrowser).
- Existing MPL 2.0 / GPL 3.0 licensing applies to the modified desktop source. The original license files and attribution remain.
- Qt 6, QScintilla, QCustomPlot, QHexEdit, and other bundled libraries retain their own license terms. See the desktop license files, library source directories, and Qt license texts.
- Toolbar icons use the Pastel SVG set by Michael Buckley, under CC BY-SA 4.0. The original icon-set attribution remains in the About dialog.
- AstroDB's orbit logo is original project artwork.

## SQLite

SQLite 3.53.4 is compiled from the official amalgamation archive. SQLite is in the public domain. Source and licensing: [sqlite.org](https://sqlite.org/).

## Python and website

The optional Python package depends on the DuckDB Python package and Python's SQLite module. Their own licenses apply. AstroDB's original Python and website components are MIT licensed.

The website uses the DM Sans font through Google Fonts. DM Sans is licensed under the SIL Open Font License. No DuckDB website assets are bundled.
