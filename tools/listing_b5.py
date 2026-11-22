"""Write batch5/listings.json (Etsy + Gumroad copy) and upload-ready JPGs.
Usage: python3 listing_b4.py <build_dir> <repo_batch_dir>"""
import json, pathlib, sys
from PIL import Image
from products import AI_NOTE, DIGITAL
from products_b5 import P
B, R = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
up = B / "upload"; up.mkdir(exist_ok=True)
CLIP_LIC = ("Small business commercial use included (up to 5,000 sales per design): use the clipart in cards, tags, stickers, mugs, shirts and printables you make and sell. "
            "Please don't resell or share the clipart or pattern files themselves, or use them in logos. Full licence in every ZIP.")
out = []
for p in P:
    s = p["slug"]; f = B / "files"
    if p["kind"] == "xlsx":
        files = [f"{s}.xlsx"]
        what = "1 Excel file (.xlsx) that also works in Google Sheets (File > Import, or upload to Google Drive and open with Google Sheets). Works with Numbers on Mac with basic formatting."
        steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Open in Excel, or upload to Google Drive and open with Google Sheets.",
                 "3. Type your numbers in the yellow cells. Everything in green is calculated for you."]
        lic = "For use in your own business. Please don't share or resell the file."
    elif p["kind"] == "clipart":
        files = [f"{s}-PNG.zip", f"{s}-SVG.zip", f"{s}-patterns.zip", f"{s}-catalog.pdf"]
        what = "3 ZIP files (45 transparent PNGs at 3000 x 3000 px, 45 SVGs, 6 seamless 3600 x 3600 px JPG patterns) and a PDF catalog of every element with the colour palette."
        steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Unzip the files on a computer (phones and tablets may need a free unzip app).",
                 "3. Use them in Canva, Cricut Design Space, Silhouette, Procreate, Photoshop, Illustrator, Inkscape or Word."]
        lic = CLIP_LIC
    else:
        files = [f"{s}-US-Letter.pdf", f"{s}-A4.pdf"]
        npg = {"new-years-eve-party-games": 26, "kids-routine-chore-chart-pack": 15}[s]
        what = f"2 PDF files ({npg} pages each): US Letter (8.5 x 11 in) and A4."
        if s == "new-years-eve-party-games":
            steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Print at 100% / actual size on paper or cardstock. Print only the games you want, as many copies as you need.",
                     "3. Cut out the cards and tags on the dashed lines, and keep the answer keys for the host."]
        else:
            steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Print at 100% / actual size on paper or cardstock.",
                     "3. Laminate or slip into sheet protectors and use a dry-erase marker, so you can reuse the charts every week."]
        lic = "For personal use (classroom use in your own class is fine too). Please don't share or resell the files."
    for x in files: assert (f / x).exists() and (f / x).stat().st_size < 3.8e6, x
    imgs = [B / "scenes" / s / "etsy-hero.png"] + [B / "images" / s / n for n in ("2-features.png", "3-detail.png", "4-detail.png", "5-how-it-works.png")]
    body = [p["hook"], "", "WHAT YOU GET", *[f"• {b}" for b in p["bullets"]], "", "INSIDE", ", ".join(p["inside"]) + ".", "", "FILES", what, "",
            "HOW IT WORKS", *steps, "", "PLEASE NOTE", DIGITAL, lic, AI_NOTE, "", "Questions? Send us a message, we're happy to help."]
    desc = "\n".join(body)
    gdesc = "\n".join([l.replace("from your Etsy Purchases page", "right after checkout").replace("1. ", "Step 1: ").replace("2. ", "Step 2: ").replace("3. ", "Step 3: ") for l in body] + ["", "Free crafting tools: purlandpaperco.com"])
    jp = []
    for i, im in enumerate(imgs):
        t = up / f"{s}-{i + 1}.jpg"; Image.open(im).convert("RGB").save(t, "JPEG", quality=90); jp.append(t.name)
    for n in ("gumroad-cover", "gumroad-thumb"):
        Image.open(B / "scenes" / s / f"{n}.png").convert("RGB").save(up / f"{s}-{n}.jpg", "JPEG", quality=90)
    et = p["etsy_title"]
    assert len(et) <= 140 and all(et.count(c) <= 1 for c in "%&:"), et
    assert len(p["tags"]) == 13 and all(len(t) <= 20 for t in p["tags"]) and len(set(p["tags"])) == 13, p["tags"]
    out.append(dict(slug=s, lane=p["lane"], name=p["name"], price=p["price"], title=p["title"], etsy_title=et, tags=p["tags"], description=desc, gumroad_desc=gdesc,
                    files=files, upload_images=jp, gumroad_cover=[jp[0], f"{s}-gumroad-cover.jpg"] + jp[1:], gumroad_thumb=f"{s}-gumroad-thumb.jpg",
                    listed=False, etsy_url=None, gumroad_url=None))
    print(s, len(et), "chars")
(R / "listings.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
