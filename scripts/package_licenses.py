from pathlib import Path
from urllib.request import urlopen
import shutil
import sys

engine, desktop, dest = map(Path, sys.argv[1:])
for name, root in (("engine", engine), ("desktop", desktop)):
    for source in root.rglob("*"):
        if not source.is_file() or any(part in (".git", "build") for part in source.relative_to(root).parts):
            continue
        if not source.name.upper().startswith(("LICENSE", "COPYING", "NOTICE")):
            continue
        target = dest / name / source.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
qt = dest / "Qt"
qt.mkdir(parents=True, exist_ok=True)
for name in ("LGPL-3.0-only.txt", "GPL-3.0-only.txt", "GPL-2.0-only.txt", "Qt-GPL-exception-1.0.txt"):
    text = urlopen("https://raw.githubusercontent.com/qt/qtbase/v6.8.3/LICENSES/" + name).read()
    (qt / name).write_bytes(text)
