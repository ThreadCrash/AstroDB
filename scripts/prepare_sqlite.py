from hashlib import sha3_256
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import sys

dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
archive = urlopen("https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip").read()
if sha3_256(archive).hexdigest() != "628a44cfe82c66aed1ccbbe85a562d2e33ebe64b3288981ed76285612227934e":
    raise RuntimeError("SQLite archive checksum mismatch")
ZipFile(BytesIO(archive)).extractall(dest)
(dest / "CMakeLists.txt").write_text("""cmake_minimum_required(VERSION 3.16)
project(AstroSQLite LANGUAGES C)
add_library(sqlite3 STATIC sqlite-amalgamation-3530400/sqlite3.c)
target_compile_definitions(sqlite3 PRIVATE SQLITE_ENABLE_COLUMN_METADATA SQLITE_ENABLE_FTS5 SQLITE_ENABLE_RTREE)
target_include_directories(sqlite3 PUBLIC sqlite-amalgamation-3530400)
""", encoding="utf-8")
