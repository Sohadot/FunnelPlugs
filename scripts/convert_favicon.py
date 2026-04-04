from pathlib import Path

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
svg_path = ROOT / "assets" / "icons" / "favicon-master.svg"
png_path = ROOT / "assets" / "icons" / "favicon-temp.png"
ico_path = ROOT / "favicon.ico"

# Convert SVG to PNG first
cairosvg.svg2png(
    url=str(svg_path),
    write_to=str(png_path),
    output_width=256,
    output_height=256,
)

# Convert PNG to ICO
img = Image.open(png_path)
img.save(
    ico_path,
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
)

print(f"Created: {ico_path}")
