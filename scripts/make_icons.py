from pathlib import Path
from math import cos, sin, pi
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2]
source = Path(__file__).resolve().parents[1]
engine = source / "engine" if (source / "engine").exists() else root / "Engine"
desktop = source / "desktop" if (source / "desktop").exists() else root / "Desktop"
image = Image.new("RGBA", (1024, 1024), (16, 19, 13, 255))
draw = ImageDraw.Draw(image)
for tilt in (-pi / 4, pi / 4):
    points = []
    for i in range(361):
        t = i * pi / 180
        x, y = 390 * cos(t), 170 * sin(t)
        points.append((512 + x * cos(tilt) - y * sin(tilt),
                       512 + x * sin(tilt) + y * cos(tilt)))
    draw.line(points, fill="#c6ff69", width=22)
draw.ellipse((458, 458, 566, 566), fill="#c6ff69")
draw.ellipse((205, 735, 287, 817), fill="#c6ff69")
icon = image.resize((256, 256), Image.Resampling.LANCZOS)
icon.save(engine / "logo/AstroDB.ico", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
icon.save(desktop / "src/iconwin.ico", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
for name in ("src/icons/astrodb.png", "src/icons/sqlitebrowser.png", "images/logo.png", "images/logo-nightly.png"):
    icon.save(desktop / name)
for name in ("logo.svg", "logo-nightly.svg"):
    (desktop / "images" / name).write_bytes((source / "website/mark.svg").read_bytes())
