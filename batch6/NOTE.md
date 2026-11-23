# Batch 6 — 23 Nov 2026 (BUILT, NOT LISTED)

Status: built and checked in the cloud run at 18:55-19:10 PKT. Claude in Chrome was not reachable from this cloud run (the scheduled task does not have
"Require this computer" on), so nothing was listed, pinned or deployed, and Etsy Stats / Gumroad / Pinterest could not be read this run
(latest numbers are in STATS.md, 23 Nov 18:05: 22 active Etsy listings, 8 visits, 0 favourites/orders, 0 Gumroad sales).
Next run with Chrome: (1) batch 5 on Gumroad (still missing), (2) list these 3 on Etsy + Gumroad (listings.json has all copy),
(3) post their pin-a (queued just before the other queued pins in pins/queue.json; fill `link` from etsy_url), (4) deploy the site.

Double down on winners: none yet (0 orders, no listing with 3+ favourites as of STATS 23 Nov), so no spin-offs this run.

| Product | Lane | Price | Files (each < 3.8 MB) |
|---|---|---|---|
| Soap Making Business Spreadsheet (supplies & stock, recipe costing by ingredient line in oz/lb/g/kg with % of oils, cost per bar + wholesale/retail + Etsy fees, batch planner with stock check, batches & cure tracker, sales log, dashboard; cold process, hot process and melt & pour) | a maker business | 11.99 | 1 xlsx (5,494 formulas, 0 errors after LibreOffice recalc) |
| Family Advent Activity Calendar (32 activity cards in 5 themes + 8 blanks, countdown tree poster, number tags 1-25 + blanks, paper chain 25->1, advent planner, bucket list, December memories; 15 pp) | d seasonal + h kids | 5.99 | 2 PDFs (Letter, A4), ~1.6 MB each |
| Mid-Century Modern Wall Art Set of 6 (Golden Hour, Bauhaus Blocks, Terracotta Hills, Sage Botanical, Quarter Arcs, Balanced Stones; 6 ratios, 36 JPGs, 300 dpi) | e wall art | 9.99 | 5 ZIPs 2.0-2.6 MB |

Why these: advent activity calendars peak in the last week of November (1 Dec is in 8 days), and it complements the kids Christmas pack and
chore charts; soap making is one of the largest maker niches after candles (Craftybase and many Etsy listings target "soap cost calculator"), and it
reuses our candle-sheet structure; lane e had only one (seasonal) product, and evergreen mid-century/terracotta/sage gallery sets are a steady
wall-art seller that doesn't expire after Christmas. Etsy search pages could not be checked (no Chrome); research was web search only.

Checks: soap sheet tested with sample data (Lavender 32 oz oils: olive 42.5% / coconut 30% / shea 20% / castor 7.5%; batch $13.67 -> $1.37 per bar,
cost $3.53, wholesale $7.50, retail $15; 30 bars = 3.0x batch, every ingredient + stock check; g -> oz conversion; cure dates and Curing/Ready;
dashboard KPIs). The sheet does NOT calculate lye (stated in Start Here and the listing). Every scene image, the centre-square crop, the listing
images and all 15 advent pages were viewed. Fixed during build: jagged hills in Terracotta Hills, wall-art hero label overflowing, small
"all 6 prints" image, soap features panel overflowing, soap hero changed to the Batch Planner view.

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch6; mkdir -p $B/{files,pages,images,scenes,demo,upload,wallart}; cd tools
python3 p9_soap.py $B/files/soap-making-business-spreadsheet.xlsx && python3 <recalc.py> $B/files/soap-making-business-spreadsheet.xlsx 120 && cp $B/files/soap-making-business-spreadsheet.xlsx $B/demo/
python3 b6_advent.py $B/files   # then qpdf --object-streams=generate --recompress-flate --compression-level=9 on both PDFs
python3 b6_wallart.py $B/wallart && python3 b6_zip.py $B/wallart $B/files && python3 b6_wallscenes.py $B/wallart $B/scenes $B/images
s=family-advent-activity-calendar; mkdir -p $B/pages/$s; pdftoppm -r 110 -png $B/files/$s-US-Letter.pdf $B/pages/$s/p
PRODUCTS=products_b6 python3 scenes.py $B/pages $B/demo $B/scenes soap-making-business-spreadsheet $s
PRODUCTS=products_b6 python3 mockups.py $B/files $B/images soap-making-business-spreadsheet $s
python3 listing_b6.py $B ../batch6 ../pins/batch6
```

Listing notes
- Etsy categories: soap sheet -> Bookkeeping Templates; advent calendar -> Planner Templates or closest "Calendars & Planners"/"Christmas" printable
  (How it's made "A finished product"); wall art -> Prints > Digital Prints ("A finished product"). All: "I did", "With an AI generator", Digital, quantity 999, auto-renew.
- Shop sections: soap -> Spreadsheets/business section used for candle sheet; advent -> "Christmas Printables"; wall art -> "Christmas Printables" for now
  (create "Wall Art" section + Pinterest board "Printable Wall Art" once lane e has 3 products).
- Gumroad slugs planned: soap-business-spreadsheet, family-advent-calendar, mid-century-wall-art-set.
- Etsy photos = `upload_images` (1 = scenes etsy-hero); Gumroad = `gumroad_cover` + `gumroad_thumb`. After listing set listed / etsy_url / gumroad_url.

## Listed 23 Nov 2026 19:50-20:20 PKT (main chat, Chrome)
- Etsy (copied from similar listings, then photos/files/title/description/tags replaced): soap 4623878110 (from candle sheet: Bookkeeping, section Business Spreadsheets), advent 4623873061 (category changed Colouring Books -> Advent Calendars, section Christmas Printables), wall art 4623882770 (section Wall Art).
- Gumroad: soap-business-spreadsheet, family-advent-calendar, mid-century-wall-art-set; batch 5 too: 2027-reading-tracker, new-years-eve-party-games, kids-routine-chore-charts. All published.
- Pinterest: new board "Printable Wall Art"; batch-6 pin-a scheduled 24 Nov 10:30 / 14:30 / 20:00 PKT (+ 2 book pins = 5 that day).
- Site: soap sheet added to SHOP boxes on craft-fair-checklist + how-to-price-crochet-items; deployed; IndexNow 200.
- Fast listing recipe: Etsy listing-editor/copy/<similar id> -> Delete all photos -> upload 5 -> Remove files -> upload -> set title/description/price via JS native setter -> Tags: "Delete all" then type each tag + Enter with 0.5 s pauses (synthetic Enter is ignored) -> check category -> Publish copy -> confirm $0.20.
- Gumroad recipe: products/new -> name + price -> Next -> paste description as HTML via ClipboardEvent on .ProseMirror -> URL field triple-click + type slug -> Summary -> Cover "Upload images or videos" -> Computer files input (6 images) -> Thumbnail input -> Save and continue -> Content file input -> name folder -> Publish and continue.
