"""Write batchN/listings.json for batch 3 (Etsy + Gumroad copy) and upload-ready JPGs.
Usage: python3 listing_b3.py <build_dir> <repo_batch_dir>"""
import json, pathlib, sys
from PIL import Image
from products import AI_NOTE, DIGITAL, LICENSE
from products_b3 import P
B, R = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
ART_LICENSE = "For personal use only: print as many copies as you like for your own home or as a gift. Please don't share, sell or print the files for sale."
out = []
up = B / "upload"; up.mkdir(exist_ok=True)
for p in P:
    s = p["slug"]
    if p["kind"] == "wallart":
        files = sorted(x.name for x in (B / "files").glob("winter-woodland-wall-art-*.zip"))
        what = "5 ZIP files of high-resolution JPGs (300 dpi): 2:3, 3:4, 4:5, ISO A-sizes, and 11x14 + 5x7 together. Sizes: " + p["ratios"] + ". A printing guide is included."
        steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Unzip the ratio that matches your frame and print at home, at a print shop or with an online photo lab.", "3. Frame, hang and enjoy. Frames are not included."]
        lic = ART_LICENSE
        imgs = [B / "scenes" / s / "etsy-hero.png"] + [B / "images" / s / n for n in ("2-sizes.png", "3-detail.png", "4-detail.png", "5-how-it-works.png")]
    else:
        files = sorted(x.name for x in (B / "files").glob(s + "-*.pdf"))
        what = "2 PDF files: US Letter (8.5 × 11 in) and A4."
        steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Print at 100% / actual size on paper or cardstock.", "3. Cut, play and enjoy. Print again any time."]
        lic = "For personal, family and classroom use. Please don't share or resell the files."
        imgs = [B / "scenes" / s / "etsy-hero.png"] + [B / "images" / s / n for n in ("2-features.png", "3-detail.png", "4-detail.png", "5-how-it-works.png")]
    body = [p["hook"], "", "WHAT YOU GET", *[f"• {b}" for b in p["bullets"]], "", "INSIDE", ", ".join(p["inside"]) + ".", "", "FILES", what, "",
            "HOW IT WORKS", *steps, "", "PLEASE NOTE", DIGITAL, lic, AI_NOTE, "", "Questions? Send us a message, we're happy to help."]
    desc = "\n".join(body)
    gdesc = "\n".join([l.replace("from your Etsy Purchases page", "right after checkout") for l in body] + ["", "Free crafting tools: purlandpaperco.com"])
    jp = []
    for i, im in enumerate(imgs):
        t = up / f"{s}-{i + 1}.jpg"; Image.open(im).convert("RGB").save(t, "JPEG", quality=90); jp.append(t.name)
    for n in ("gumroad-cover", "gumroad-thumb"):
        Image.open(B / "scenes" / s / f"{n}.png").convert("RGB").save(up / f"{s}-{n}.jpg", "JPEG", quality=90)
    et = p["etsy_title"]
    assert len(et) <= 140 and sum(et.count(c) for c in "%&:") <= 3 and all(et.count(c) <= 1 for c in "%&:"), et
    assert len(p["tags"]) == 13 and all(len(t) <= 20 for t in p["tags"]), p["tags"]
    out.append(dict(slug=s, lane=p["lane"], name=p["name"], price=p["price"], title=p["title"], etsy_title=et, tags=p["tags"], description=desc, gumroad_desc=gdesc,
                    files=files, upload_images=jp, gumroad_cover=[jp[0], f"{s}-gumroad-cover.jpg"] + jp[1:], gumroad_thumb=f"{s}-gumroad-thumb.jpg",
                    listed=False, etsy_url=None, gumroad_url=None))
    print(s, len(et), "chars")
(R / "listings.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
