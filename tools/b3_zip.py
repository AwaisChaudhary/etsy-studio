"""Batch 3 wall art: pack the rendered PNGs into customer ZIPs (one per ratio, 11x14 + 5x7 together).
Usage: python3 b3_zip.py <wallart_dir> <files_dir>"""
import io, sys, zipfile, pathlib
from PIL import Image

src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
GUIDE = """Winter Woodland Wall Art - set of 3 (Purl & Paper)

Thank you for your purchase! Each file is a high-resolution JPG at 300 dpi.

WHICH FILE FITS MY FRAME?
- 2x3 ratio: 4x6, 8x12, 12x18, 16x24, 20x30, 24x36 in
- 3x4 ratio: 6x8, 9x12, 12x16, 18x24 in
- 4x5 ratio: 4x5, 8x10, 16x20 in
- 11x14 in and 5x7 in: exact sizes
- ISO A ratio: A5, A4, A3, A2 (and 50x70 cm close fit)

PRINTING TIPS
- Print at "actual size" or "fit to page" with borderless printing if your printer supports it.
- Matte or lustre photo paper or a heavy matte card (200 gsm+) looks best.
- Print shops and online photo labs give the richest colour for large sizes.
- Colours can look slightly different on paper than on screen.

Personal use only. Frames are not included. Questions? Message us on Etsy.
"""
groups = {"2x3": ["2x3"], "3x4": ["3x4"], "4x5": ["4x5"], "ISO-A": ["ISO-A"], "11x14-and-5x7": ["11x14", "5x7"]}
for name, ratios in groups.items():
    out = dst / f"winter-woodland-wall-art-{name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("PRINTING-GUIDE.txt", GUIDE)
        for r in ratios:
            for png in sorted((src / r).glob("*.png")):
                buf = io.BytesIO()
                Image.open(png).convert("RGB").save(buf, "JPEG", quality=90, dpi=(300, 300), optimize=True)
                z.writestr(f"{r}/{png.stem}-{r}.jpg", buf.getvalue())
    print(out.name, round(out.stat().st_size / 1e6, 2), "MB")
