# Batch 7 — 24 Nov 2026 (BUILT, NOT LISTED)

Status: built and checked in the scheduled cloud run (~19:00-20:00 PKT). Claude in Chrome was not reachable from this cloud run (the scheduled task
does not have "Require this computer" on), so nothing was listed, pinned or deployed, and Etsy Stats / Gumroad / Pinterest could not be read
(latest numbers: STATS.md, 23 Nov 20:20: 25 active Etsy listings, 8 visits in 30 days, 0 favourites/orders, 0 Gumroad sales).

Next run with Chrome: (1) list these 3 on Etsy + Gumroad (listings.json has all copy; Etsy category Bookkeeping Templates, section Business
Spreadsheets; fast recipe = copy the soap sheet listing 4623878110), (2) set listed / etsy_url / gumroad_url, (3) post their pin-a (queued in
pins/queue.json just before the other queued pins; fill `link` from etsy_url), (4) deploy the site.

Double down on winners: none yet (0 orders, no listing with 3+ favourites as of 23 Nov), so no spin-offs this run.

Follows the 23 Nov strategy change: one specific trade per spreadsheet, $11.99-12.99, no generic printables today.

| Product | Lane | Price | File |
|---|---|---|---|
| Resin Art Business Spreadsheet (resin calculator by shape/size in in or cm: total, Part A/B by ratio, fl oz + ml, layers by max pour depth, cost; supplies with cost per fl oz and mould cost per pour; product pricing with resin from dimensions, pigments, inclusions, hardware, packaging, labour, Etsy fees; custom order tracker with deposits, demould dates, LATE / cure-after-due flags; sales; dashboard) | a maker business | 11.99 | 1 xlsx (0 errors after LibreOffice recalc) |
| Sublimation & Tumbler Business Spreadsheet (blanks & supplies cost each; ink cost per print from ink set price/yield x coverage; product pricing with paper, tape, shrink wrap, design licence per use, packaging, misprint allowance, press time; bulk quote with 5 discount tiers, deposit, profit, price check and price ladder; order tracker with proof / ship-by flags; sales; dashboard) | a maker business | 11.99 | 1 xlsx (0 errors) |
| Lash Tech Business Spreadsheet (service menu: product cost per service, overhead per hour from fixed costs, break-even, suggested price at your pay goal, profit per hour, price check; clients with lash map, curl, lengths, thickness, patch test, visits, total spent, last visit (MAXIFS), next fill due, Due now / Due soon / Lapsed / Booked / New; appointments with menu price, tips, card fees, no-shows, rebook; supplies with adhesive replace-by; expenses; dashboard with rebook and no-show rates, average ticket, tax set-aside) | a service business | 12.99 | 1 xlsx (0 errors) |

Why these: the strategy list names resin, sublimation/tumbler and lash tech as target trades. Web search shows only a handful of trade-specific
Etsy listings for "resin pricing calculator spreadsheet" and "sublimation cost calculator spreadsheet" (most competitors are generic handmade
pricing sheets), while lash client records are popular but mostly printable PDFs, not calculators. Etsy search pages could not be checked (no Chrome).

Checks: every main formula tested with sample values. Resin: 12x8x0.25 in tray = 24 cu in = 13.30 fl oz, +10% = 14.63 fl oz, 7.31 A + 7.31 B,
$10.28 at $89.99/gal; 4 in round coaster = 1.74 fl oz. Sublimation: 20 oz tumbler $3.60 blank + $0.58 paper & ink (full wrap); 36 teacher mugs ->
tier 24 (10%), $10.00 each, quote $393, deposit $196.50, profit $167.36. Lash: overhead $6.50/h; classic fill 60 min $65 -> profit $53.07/h;
client next-fill and Lapsed / Booked / New status; no-show fee counted as income. MAXIFS written as _xlfn.MAXIFS so Excel reads it.
All scene images (incl. centre-square crop), pins and listing images viewed. Fixed during build: sublimation hero cut off the quote values
(narrowed Bulk Quote columns), lash hero showed no profit (hid middle columns), feature images showed a tiny dashboard (taller range),
depth 0.25 shown as 0.2 in screenshots (xlview number format fix), example prices that looked too high (labour minutes).

Tool changes: xlview.xl_html accepts "A1:AD12;B-Q,S-X" to hide columns in wide sheets; mockups.py now uses the shared xlview renderer.

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch7; mkdir -p $B/{files,demo,images,scenes,upload,pages}; cd tools; R=$(ls /root/.claude/skills/synced/*/xlsx/scripts/recalc.py)
python3 p10_resin.py $B/files/resin-art-business-spreadsheet.xlsx; python3 p11_sublimation.py $B/files/sublimation-tumbler-business-spreadsheet.xlsx
python3 p12_lash.py $B/files/lash-tech-business-spreadsheet.xlsx; for f in $B/files/*.xlsx; do python3 $R $f 120; done; cp $B/files/*.xlsx $B/demo/
S="resin-art-business-spreadsheet sublimation-tumbler-business-spreadsheet lash-tech-business-spreadsheet"
PRODUCTS=products_b7 python3 scenes.py $B/pages $B/demo $B/scenes $S; PRODUCTS=products_b7 python3 mockups.py $B/files $B/images $S
python3 listing_b7.py $B ../batch7 ../pins/batch7
```
Etsy photos = `upload_images` (1 = scenes etsy-hero); Gumroad = `gumroad_cover` + `gumroad_thumb`. Planned Gumroad slugs: resin-business-spreadsheet,
tumbler-pricing-spreadsheet, lash-tech-spreadsheet.
