# Batch 8 — 25 Nov 2026 (BUILT, NOT LISTED)

Status: built and checked in the scheduled cloud run (~19:00-20:00 PKT). Claude in Chrome was not reachable from this cloud run (the scheduled task
does not have "Require this computer" on), so nothing was listed, pinned or deployed, and Etsy Stats / Gumroad / Pinterest could not be read
(latest numbers: STATS.md 24 Nov 20:40: 28 listed, 9 Etsy visits in 30 days, 0 orders, 0 Gumroad sales, Pinterest 18 impressions).

Next run with Chrome: (1) list these 3 on Etsy + Gumroad (listings.json has all copy; Etsy category Bookkeeping Templates, section Business
Spreadsheets; fast recipe = copy the lash sheet 4624651798 for nails, the resin sheet 4624644331 for laser and sticker), (2) set listed / etsy_url /
gumroad_url, (3) post their pin-a (queued in pins/queue.json just before the other queued pins; fill `link` from etsy_url; status
"queued (needs listing first)"), (4) deploy the site (and add the 3 to SHOP in site/build.py).

Double down on winners: none yet (0 orders, no listing with 3+ favourites as of 24 Nov), so no spin-offs this run.

Follows the 23 Nov strategy change: one specific trade per spreadsheet, $11.99-12.99, no generic printables today.

| Product | Lane | Price | File |
|---|---|---|---|
| Laser Engraving Business Spreadsheet (machine cost per hour from laser price / working hours + power + upkeep; materials by the sheet with cost per sq in, plus blanks and extras; product pricing from part size, pieces, engrave + cut minutes, hands-on time, 15% waste, packaging, overheads; wholesale / retail, Etsy fees, profit, margin, PROFIT PER MACHINE HOUR; bulk quote with 5 tiers + price ladder; orders with proof / ship-by flags; sales; dashboard) | a maker business | 12.99 | 1 xlsx (3,751 formulas, 0 errors) |
| Nail Tech Business Spreadsheet (service menu: product cost per service, overhead per hour, break-even, suggested price at pay goal, profit per hour, price check; Gel-X / acrylic / BIAB / gel / pedicure / nail art examples; clients with shape, length, colours, allergy notes (HEMA-free), visits, spend, last visit (MAXIFS), next fill due, Due now / Due soon / Lapsed / Booked / New; appointments with nail art add-ons, tips, card fees, no-shows, rebook; supplies with open / replace-by dates; expenses; dashboard incl. add-on income) | a service business | 12.99 | 1 xlsx (7,914 formulas, 0 errors) |
| Sticker Shop Business Spreadsheet (supplies cost each; ink per sheet by coverage + blade/mat wear + misprint allowance; product pricing for sheets, kiss-cut, die-cut singles, packs and bought-in stickers: cost per item AND per sticker, wholesale, retail, fees, profit; print run planner: sheets to print, time, cost, value, supply check vs stock; print runs log; finished stock per design = made - sold - damaged with Make more flags and stock value; sales by channel with wholesale price auto-used for the Wholesale channel; dashboard) | a maker business | 11.99 | 1 xlsx (6,415 formulas, 0 errors) |

Why these: the 23 Nov strategy list names laser engraving, nail tech and sticker shop as target trades. Web search for each shows mostly generic
"handmade pricing" sheets and free web calculators (xTool, OMTech, calculator.academy) rather than a full trade-specific business workbook; nail
tech pairs with the lash sheet (same buyers: beauty service pros) and laser/sticker sellers are among the most active Etsy maker niches.
Etsy search pages could not be checked (no Chrome).

Checks (sample values): Laser: machine $2,500 / 3,000 h + $0.40 + $0.60 = $1.83/h; birch 12x20 sheet $2.75 = $0.0115/sq in; keychain 2.5x1.5 in
material $0.05 (+15% waste), 2 machine min $0.06, 4 hands-on min $1.67 -> cost $2.38, retail $8, $132/machine hour; slate set of 4 = 4 x $2.50 +15%
= $11.50 -> cost $17.90, retail $53; bulk 30 boards at tier 25 (10%) -> $22.50 each, quote $722 incl. $25 set-up + $22 shipping, deposit $361,
profit $299.78. Nails: overhead $600/110 h = $5.45/h; Gel-X 90 min $65 -> product $2.03, break-even $10.21, profit $52.60 = $35.07/h; client
next-fill / Lapsed / Booked statuses; removal visits not counted as visits; dashboard profit $625 on example data. Stickers: matte sheet $0.50 + ink
$0.27 (heavy) + laminate $0.36 + wear $0.06 = $1.19 per sheet, 2 per sheet +8% -> $0.64 + card + sleeve + labour -> $1.75, wholesale $3.25,
retail $6; 40 sheets -> 22 sheets to print, supply check "Enough"; stock made 60 - sold 27 - damaged 2 = 31.
Every scene image, centre-square crop, pins, Gumroad cover/thumb and listing image viewed. Fixed during build: feature panels overflowing
(shorter bullets), hero laptops cutting off the key column (hid columns so profit per machine hour / profit per hour show), nail example with a
negative-profit month (more example appointments), sticker retail prices too high for the market (mark-ups 1.8x/1.8x, faster minutes), a
-$1.04 soak-off row.

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch8; mkdir -p $B/{files,demo,images,scenes,upload,pages}; cd tools; R=$(ls /root/.claude/skills/synced/*/xlsx/scripts/recalc.py)
python3 p13_laser.py $B/files/laser-engraving-business-spreadsheet.xlsx; python3 p14_nails.py $B/files/nail-tech-business-spreadsheet.xlsx
python3 p15_sticker.py $B/files/sticker-shop-business-spreadsheet.xlsx; for f in $B/files/*.xlsx; do python3 $R $f 120; done; cp $B/files/*.xlsx $B/demo/
S="laser-engraving-business-spreadsheet nail-tech-business-spreadsheet sticker-shop-business-spreadsheet"
PRODUCTS=products_b8 python3 scenes.py $B/pages $B/demo $B/scenes $S; PRODUCTS=products_b8 python3 mockups.py $B/files $B/images $S
python3 listing_b8.py $B ../batch8 ../pins/batch8
```
Etsy photos = `upload_images` (1 = scenes etsy-hero); Gumroad = `gumroad_cover` + `gumroad_thumb`. Planned Gumroad slugs: laser-engraving-spreadsheet,
nail-tech-spreadsheet, sticker-business-spreadsheet (pin-b links in queue.json already use them).

## 25 Nov 2026 19:50-20:10 PKT (main chat, Chrome)
- Etsy DRAFTS made with the copy recipe (photos, file, title, description, price, 13 tags replaced; category Bookkeeping Templates, section Business Spreadsheets): nail 4625445559 (from lash), laser 4625446969 (from resin), sticker 4625456612 (from resin). Publishing was blocked by the auto-mode safety check ($0.20 fee), so they are drafts until Awais approves; then publish from Listings > Draft.
- Gumroad not done: the new Chrome profile's extension can't act on gumroad.com yet.
- Pins stay 'queued (needs listing first)' until the listings are live.
- 26 Nov 00:50 PKT: Awais approved; all 3 published on Etsy (Active 31). Pins now queued with Etsy links.
