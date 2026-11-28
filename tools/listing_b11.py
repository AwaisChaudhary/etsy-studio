"""Write batch11/listings.json (Etsy + Gumroad copy), upload-ready JPGs and pin JPGs.
Usage: python3 listing_b10.py <build_dir> <repo_batch_dir> <repo_pins_dir>"""
import json, pathlib, sys
from PIL import Image
from products import AI_NOTE, DIGITAL
from products_b11 import P
B, R, PIN = (pathlib.Path(a) for a in sys.argv[1:4])
up = B / "upload"; up.mkdir(exist_ok=True); PIN.mkdir(parents=True, exist_ok=True)
ART_LICENSE = "For personal use only: print as many copies as you like for your own home or as a gift. Please don't share, sell or print the files for sale."
RATIOS = "2:3 (4x6, 8x12, 12x18, 16x24, 20x30, 24x36), 3:4 (6x8, 9x12, 12x16, 18x24), 4:5 (8x10, 16x20), 11x14, 5x7 / 10x14, ISO (A5, A4, A3, A2, A1)"
out = []
for p in P:
    s = p["slug"]; f = B / "files"
    if p["kind"] == "xlsx":
        files = [f"{s}.xlsx"]
        what = "1 Excel file (.xlsx) that also works in Google Sheets (File > Import, or upload to Google Drive and open with Google Sheets). Works with Numbers on Mac with basic formatting."
        steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Open in Excel, or upload to Google Drive and open with Google Sheets.",
                 "3. Type your numbers in the yellow cells. Everything in green is calculated for you."]
        lic = "For use in your own business. Please don't share or resell the file. Prices and fee rates in the examples are illustrations: type in your own."
        if "workout" in s: lic = "For your own personal use. Please don't share or resell the file. A tracking tool, not medical advice: check with a doctor before starting a new programme."
        if "bookkeeping" in s: lic += " A record-keeping tool, not tax advice: set your own tax set-aside % and mileage rate with your accountant or tax office."
        imgs = [B / "scenes" / s / "etsy-hero.png"] + [B / "images" / s / n for n in ("2-features.png", "3-detail.png", "4-detail.png", "5-how-it-works.png")]
    elif p["kind"] == "wallart":
        files = sorted(x.name for x in f.glob(s + "-*.zip"))
        what = "5 ZIP files of high-resolution JPGs (300 dpi): 2:3, 3:4, 4:5, ISO A-sizes, and 11x14 + 5x7 together (36 JPGs in all). Sizes: " + RATIOS + ". A printing guide is included."
        steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Unzip the ratio that matches your frame and print at home, at a print shop or with an online photo lab.",
                 "3. Frame, hang and enjoy. Frames are not included."]
        lic = ART_LICENSE
        imgs = [B / "scenes" / s / "etsy-hero.png"] + [B / "images" / s / n for n in ("2-sizes.png", "3-detail.png", "4-detail.png", "5-how-it-works.png")]
    elif "calendar" in s:
        files = [f"{s}-US-Letter-Sunday-Start.pdf", f"{s}-US-Letter-Monday-Start.pdf", f"{s}-A4-Sunday-Start.pdf", f"{s}-A4-Monday-Start.pdf"]
        what = "4 PDF files (14 pages each): US Letter (8.5 x 11 in) and A4, each with a Sunday-start and a Monday-start version."
        steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Print at 100% / actual size at home or at a print shop (matte cardstock looks lovely).",
                 "3. Clip, bind or pin it up, or print one month at a time. Print again whenever you like."]
        lic = "For personal use (and in your own home, office or classroom). Please don't share or resell the files."
        imgs = [B / "scenes" / s / "etsy-hero.png"] + [B / "images" / s / n for n in ("2-features.png", "3-detail.png", "4-detail.png", "5-how-it-works.png")]
    else:
        files = [f"{s}-US-Letter.pdf", f"{s}-A4.pdf"]
        npg = {"letter-from-santa-kit": 14, "cricket-scorebook-printable": 10, "kids-valentine-cards-classroom": 8}[s]
        what = f"2 PDF files ({npg} pages each): US Letter (8.5 x 11 in) and A4." + (" Landscape pages." if "cricket" in s else "")
        if "santa" in s:
            steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Print at 100% / actual size on paper, or cardstock for the certificate, sign, tags and plate cards.",
                     "3. Write the names in the blanks, sign as Santa and let the magic happen. Undated, so you can print it again every Christmas."]
        elif "cricket" in s:
            steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Print the pages you need at 100% / actual size, landscape. Print a fresh set for every match.",
                     "3. Clip them to a board or bind them into a season scorebook."]
        else:
            steps = ["1. Buy and download instantly from your Etsy Purchases page.", "2. Print at 100% / actual size on white cardstock or paper.",
                     "3. Cut on the dashed lines, colour in (if you like), write To and From, and hand them out."]
        lic = "For personal use (and in your own home, classroom, club or school). Please don't share or resell the files."
        imgs = [B / "scenes" / s / "etsy-hero.png"] + [B / "images" / s / n for n in ("2-features.png", "3-detail.png", "4-detail.png", "5-how-it-works.png")]
    for x in files: assert (f / x).exists() and (f / x).stat().st_size < 3.8e6, x
    assert 1 <= len(files) <= 5
    body = [p["hook"], "", "WHAT YOU GET", *[f"• {b}" for b in p["bullets"]], "", "INSIDE", ", ".join(p["inside"]) + ".", "", "FILES", what, "",
            "HOW IT WORKS", *steps, "", "PLEASE NOTE", DIGITAL, lic, AI_NOTE, "", "Questions? Send us a message, we're happy to help."]
    desc = "\n".join(body)
    gdesc = "\n".join([l.replace("from your Etsy Purchases page", "right after checkout").replace("1. ", "Step 1: ").replace("2. ", "Step 2: ").replace("3. ", "Step 3: ")
                       .replace("Message us on Etsy", "Message us") for l in body] + ["", "Free crafting tools: purlandpaperco.com"])
    jp = []
    for i, im in enumerate(imgs):
        t = up / f"{s}-{i + 1}.jpg"; Image.open(im).convert("RGB").save(t, "JPEG", quality=90); jp.append(t.name)
        assert t.stat().st_size < 3.8e6
    for n in ("pin-a", "pin-b"):
        Image.open(B / "scenes" / s / f"{n}.png").convert("RGB").save(PIN / f"{s}-{n}.jpg", "JPEG", quality=88)
    et = p["etsy_title"]
    assert len(et) <= 140 and all(et.count(c) <= 1 for c in "%&:"), et
    assert len(p["tags"]) == 13 and all(len(t) <= 20 for t in p["tags"]) and len(set(p["tags"])) == 13, p["tags"]
    out.append(dict(slug=s, lane=p["lane"], name=p["name"], price=p["price"], title=p["title"], etsy_title=et, tags=p["tags"], description=desc,
                    files=files, upload_images=jp, listed=False, etsy_url=None, etsy_section=p.get("section"), etsy_category=p.get("category")))
    print(s, len(et), "chars", files)
R.mkdir(exist_ok=True)
(R / "listings.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
