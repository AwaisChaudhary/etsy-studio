import json, pathlib, sys
from PIL import Image
from products import P, AI_NOTE, DIGITAL, LICENSE
B = pathlib.Path(sys.argv[1]); out = []
for p in P:
    files = sorted(x.name for x in (B / "files").iterdir() if x.name.startswith(p["slug"]) or (p["kind"] == "bundle" and x.name.startswith("junk-journal-mega-bundle")))
    if p["kind"] == "xlsx": what = "1 Excel file (.xlsx). Opens in Microsoft Excel and Google Sheets (upload to Google Drive, then open with Google Sheets). Also works in Apple Numbers and LibreOffice, though drop-down lists may look different."
    elif p["kind"] == "bundle": what = "2 ZIP files: one with every PDF in US Letter (8.5 × 11 in), one in A4."
    else: what = "2 PDF files: US Letter (8.5 × 11 in) and A4."
    desc = "\n".join([p["hook"], "", "WHAT YOU GET", *[f"• {b}" for b in p["bullets"]], "", "INSIDE", ", ".join(p["inside"]) + ".", "", "FILES", what, "",
                      "HOW IT WORKS", "1. Buy and download instantly from your Etsy Purchases page.", "2. " + ("Open the file and type your numbers in the yellow cells." if p["kind"] == "xlsx" else "Print at 100% / actual size on paper or cardstock."),
                      "3. " + ("Everything else is calculated for you." if p["kind"] == "xlsx" else "Cut, layer, write and enjoy. Print again any time."), "",
                      "PLEASE NOTE", DIGITAL, ("For use in your own business. Please don't share or resell the file." if p["kind"] == "xlsx" else LICENSE), AI_NOTE, "", "Questions? Send us a message, we're happy to help."])
    imgs = sorted(str(x.relative_to(B)) for x in (B / "images" / p["slug"]).glob("*.png"))
    thumbs = []
    for i in imgs:
        t = B / "preview" / "img" / (p["slug"] + "-" + pathlib.Path(i).stem + ".jpg")
        Image.open(B / i).convert("RGB").resize((1000, 800)).save(t, "JPEG", quality=82); thumbs.append("img/" + t.name)
    out.append(dict(slug=p["slug"], name=p["name"], price=p["price"], title=p["title"], tags=p["tags"], description=desc, files=files, images=imgs, thumbs=thumbs))
(B / "listings.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(out), "listings")
