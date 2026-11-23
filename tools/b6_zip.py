"""Batch 6 wall art: pack rendered PNGs into customer ZIPs (one per ratio group), each kept under 3.8 MB (split into parts if needed).
Usage: python3 b6_zip.py <wallart_dir> <files_dir>"""
import io, sys, zipfile, pathlib
from PIL import Image

src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
SLUG = "mid-century-modern-wall-art-set-of-6"
GUIDE = """Mid-Century Modern Wall Art - set of 6 (Purl & Paper)
Golden Hour, Bauhaus Blocks, Terracotta Hills, Sage Botanical, Quarter Arcs, Balanced Stones

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
LIMIT = 3.8e6
groups = {"2x3": ["2x3"], "3x4": ["3x4"], "4x5": ["4x5"], "ISO-A": ["ISO-A"], "11x14-and-5x7": ["11x14", "5x7"]}
for name, ratios in groups.items():
    jpgs = []
    for r in ratios:
        for png in sorted((src / r).glob("*.png")):
            buf = io.BytesIO(); Image.open(png).convert("RGB").save(buf, "JPEG", quality=90, dpi=(300, 300), optimize=True)
            jpgs.append((f"{r}/{png.stem}-{r}.jpg", buf.getvalue()))
    parts, cur, size = [], [], len(GUIDE)
    for n, b in jpgs:
        if cur and size + len(b) > LIMIT - 50_000: parts.append(cur); cur, size = [], len(GUIDE)
        cur.append((n, b)); size += len(b)
    parts.append(cur)
    for k, part in enumerate(parts):
        suffix = f"-part{k + 1}" if len(parts) > 1 else ""
        out = dst / f"{SLUG}-{name}{suffix}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
            z.writestr("PRINTING-GUIDE.txt", GUIDE)
            for n, b in part: z.writestr(n, b)
        assert out.stat().st_size < LIMIT, out
        print(out.name, round(out.stat().st_size / 1e6, 2), "MB", len(part), "prints")
