"""Package the batch 4 clipart into upload-size ZIPs (each < 3.8 MB) with a licence file.
Usage: python3 b4_zip.py <clipart_build_dir> <files_dir>"""
import pathlib, sys, zipfile
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
LIC = """Nordic Folk Christmas Clipart - Purl & Paper
Original artwork designed by Purl & Paper with AI assistance.

YOU MAY: use these designs in things you make and sell (printed cards, gift tags, stickers, mugs, shirts, ornaments,
sublimation, laser and cutting projects, social posts, and digital printables where the clipart is part of your own
larger design). Personal use is unlimited. Commercial use covers up to 5,000 sales per design.

PLEASE DON'T: sell, share or give away the clipart or pattern files themselves (on their own, re-coloured, or inside
another clipart, digital paper or template pack), use them in a logo or trademark, or upload them to print-on-demand
design marketplaces as stand-alone graphics.

Credit is appreciated but not required. Questions about larger use? Send us a message on Etsy or Gumroad.
"""
name = "nordic-folk-christmas-clipart"
for part, folder, pat in (("PNG", "png", "*.png"), ("SVG", "svg", "*.svg"), ("patterns", "patterns", "*.jpg")):
    z = out / f"{name}-{part}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for f in sorted((src / folder).glob(pat)): zf.write(f, f"{name}-{part}/{f.name}")
        zf.writestr(f"{name}-{part}/LICENCE.txt", LIC)
    mb = z.stat().st_size / 1e6; assert mb < 3.8, (z, mb); print(z.name, f"{mb:.2f} MB")
