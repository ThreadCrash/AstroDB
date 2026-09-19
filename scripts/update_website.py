from pathlib import Path
from urllib.parse import quote

root = Path(__file__).resolve().parents[1]
site = root / "website"
html = (site / "index.html").read_text(encoding="utf-8")
html = html.replace('<link rel="stylesheet" href="style.css">',
                    '<style>' + (site / "style.css").read_text(encoding="utf-8") + '</style>')
html = html.replace('<script src="app.js" defer></script>',
                    '<script>' + (site / "app.js").read_text(encoding="utf-8") + '</script>')
html = html.replace('"mark.svg"', '"data:image/svg+xml,' +
                    quote((site / "mark.svg").read_text(encoding="utf-8")) + '"')
output = root.parent / "Website"
output.mkdir(exist_ok=True)
(output / "AstroDB.html").write_text(html, encoding="utf-8")
