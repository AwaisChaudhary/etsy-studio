# Batch 4 — 21 Nov 2026 (BUILT, NOT LISTED)

Status: built and checked in the cloud run at 18:54 PKT. Claude in Chrome was not reachable from this cloud run (the scheduled task does not
have "Require this computer" on), so nothing was listed, pinned or deployed, and Etsy Stats / Gumroad sales could not be read.
Next run with Chrome: list these 3 first (listings.json has all copy), post their pin-a (top of pins/queue.json), deploy the site.

| Product | Lane | Price | Files (each < 3.8 MB) |
|---|---|---|---|
| Candle Business Spreadsheet (supplies & stock, candle costing with fragrance load, wholesale/retail + Etsy fees, pour planner in oz and g with stock check, sales log, dashboard) | a maker business | 11.99 | 1 xlsx (2,901 formulas, 0 errors after LibreOffice recalc) |
| Nordic Folk Christmas Clipart (45 original vector elements, 6 seamless 12x12 patterns, catalog + palette, small-business commercial licence) | f clipart (NEW lane) | 6.99 | PNG.zip 1.6 MB, SVG.zip, patterns.zip 2.4 MB, catalog PDF |
| December Days Journal Kit (25 daily prompt cards 4x3 + 5 bonus, number circles, 12 journaling cards 3x4, one-line-a-day page, lists, tickets/tags/labels, Dear Santa letter, 6 papers; 20 pp) | c journal + d seasonal | 6.99 | 2 PDFs (Letter, A4), ~1.9 MB each |

Why these: lane f (clipart) had no products yet; candle-making is the biggest maker-pricing niche we had not covered (only cleaning/crochet/bakery);
"December Daily" journaling peaks in the last week of November. The clipart and the journal kit share one original art set and palette, so
they can be bundled later (and spin-offs: gift tags / wrapping paper / Christmas cards from the same art).

Checks done: candle sheet tested with sample values (8 oz jar: wax 6.42 oz + fragrance 0.58 oz at 9% load, cost $7.33, wholesale $15, retail $30;
pour planner 24 candles = 158.8 oz wax incl. 3% spill; reorder alerts fire). Every scene image and the centre-square crop were viewed.
Fixed during the build: Chrome shrank whole PDFs to ~77% when pages had inline SVG (fix: `contain: strict` on .page + body width); patterns
re-laid so columns don't repeat; mushroom pair / sled art re-positioned.

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch4; mkdir -p $B/{files,pages,images,scenes,demo,upload}; cd tools
python3 p7_candle.py $B/files/candle-business-spreadsheet.xlsx && python3 <recalc.py> $B/files/candle-business-spreadsheet.xlsx 90
python3 b4_clipart.py $B/clipart && cp $B/clipart/nordic-folk-christmas-clipart-US-Letter.pdf $B/files/ && cp $B/files/nordic-folk-christmas-clipart-US-Letter.pdf $B/files/nordic-folk-christmas-clipart-catalog.pdf
python3 b4_zip.py $B/clipart $B/files
python3 b4_december.py $B/files   # then qpdf --object-streams=generate --recompress-flate --compression-level=9
python3 demo_b4.py $B/files $B/demo
for s in december-days-journal-kit nordic-folk-christmas-clipart; do mkdir -p $B/pages/$s; pdftoppm -r 110 -png $B/files/$s-US-Letter.pdf $B/pages/$s/p; done
PRODUCTS=products_b4 python3 scenes.py $B/pages $B/demo $B/scenes candle-business-spreadsheet nordic-folk-christmas-clipart december-days-journal-kit
PRODUCTS=products_b4 python3 mockups.py $B/files $B/images candle-business-spreadsheet nordic-folk-christmas-clipart december-days-journal-kit
python3 listing_b4.py $B ../batch4
```
Upload files per product = listings.json `files`; Etsy photos = `upload_images` (1 = scenes etsy-hero); Gumroad = `gumroad_cover` + `gumroad_thumb`.

Listing notes
- Etsy categories: candle sheet -> Bookkeeping Templates; clipart -> Craft Supplies & Tools > ... > Clip Art / Digital (pick "Clip Art" / "Embellishments"
  closest match; How it's made: "A supply or tool to make things"); journal kit -> Scrapbooking Ephemera or Journaling Spots ("A supply or tool to make things").
  All: "I did", "With an AI generator", Digital, quantity 999, auto-renew.
- Shop sections: candle -> existing spreadsheet section; journal kit -> "Christmas Printables" (or junk journal section); clipart -> new section "Clipart & SVG"
  (create when the lane has 3 products; until then "Christmas Printables").
- Gumroad slugs planned: candle-business-spreadsheet, nordic-folk-christmas-clipart, december-days-journal-kit.
- After listing: set listed / etsy_url / gumroad_url in batch4/listings.json and fill `link` on the 6 batch-4 pins in pins/queue.json.
- Site: built fine (17 pages) but not deployed this run (needs Chrome).
