# Batch 9 — 26 Nov 2026 (BUILT, NOT LISTED)

Status: built and checked in the scheduled cloud run (~19:00-21:00 PKT). Claude in Chrome was not reachable from this cloud run (the scheduled
task does not have "Require this computer" on), so nothing was listed, pinned or deployed, and Etsy Stats / Pinterest could not be read.
Follows Awais's 26 Nov decisions: no Gumroad, new prices ($4.99 all-in-one sheet, $7.99-8.99 trade sheets, $3.99-5.99 planners).

Next run with Chrome: (1) list these 3 on Etsy (listings.json has all copy, category and section; fast recipe = copy the sticker sheet
4625456612 for the small-business and embroidery sheets, copy the 2027 reading tracker listing for the habit tracker), (2) set listed / etsy_url,
(3) post their pin-a (queued in pins/queue.json right after the batch 8 pin-a's, status "queued (needs listing first)"; fill `link` from etsy_url;
pin-b's are at the end of the queue), (4) add the 3 to SHOP in site/build.py and deploy.
Queue change: 28 queued pins that linked to Gumroad are now "skipped: Gumroad dropped (26 Nov)".

Double down on winners: not checked (no Etsy Stats access this run; as of 25 Nov: 0 orders, no listing with 3+ favourites).
Etsy search pages could not be checked (no Chrome); product choice is based on Awais's 26 Nov Etsy research (generic $1-4.99 pricing/inventory
sheets win the Bestseller badges) plus web search: machine embroidery pricing sheets exist but most are generic handmade pricing sheets or free
stitch calculators (Printavo); 2027 habit trackers are a big seasonal search for Dec-Jan (many PDF/Canva versions, fewer spreadsheet ones with streaks).

| Product | Lane | Price | File |
|---|---|---|---|
| Small Business Pricing, Inventory & Profit Spreadsheet (materials cost per unit; product costing with 4 materials + other cost + labour + overheads; SUGGESTED PRICE at target margin AFTER Etsy fees, rounded to .99; wholesale; your own price with profit, margin, profit/hour, price check; channel fee table (Etsy/website/market/IG/wholesale); stock in log; inventory with low-stock / sold-out flags and stock value; sales with fees by channel, shipping, postage, discounts; expenses; dashboard with net profit chart) | a (all-in-one, the required $4.99 product) | 4.99 | 1 xlsx (10,878 formulas, 0 errors) |
| Machine Embroidery Business Spreadsheet (machine cost per running hour; thread cost per 1,000 stitches; run time = stitches / real SPM + colour changes; blanks & stabilizer library; design library with stitch count, colours, licence; product pricing with 2 placements + name stitches, re-hoops, labour option, cost, wholesale, retail, per-1,000-stitch comparison price, profit per machine hour; bulk quote with tiers, digitizing fee, deposit, machine hours, finish date (WORKDAY), price ladder; orders with proof flags; sales; dashboard) | a | 8.99 | 1 xlsx (6,404 formulas, 0 errors) |
| 2027 Habit Tracker Spreadsheet (Setup: year + 15 habits with monthly goal; 12 month tabs with dates/weekdays from the year, tick drop-down (or x), done / goal / % / best streak / days to goal, green tick + red miss colours, weekend shading, daily score, mood 1-5 and sleep rows with colour scales, wins box; Year Overview heat map + totals + chart; 2027 Goals with progress bars) | b | 4.99 | 1 xlsx (8,114 formulas, 0 errors; demo copy with Jan-Mar ticks used only for images) |

Checks (sample values): Small biz: candle 7 oz wax $1.44 + 0.7 oz FO $0.81 + jar $1.25 + wick $0.09 = $3.59, 12 min at $18 = $3.60, overhead $0.36
-> cost $7.55; suggested (7.55 + 0.45) / (1 - 9.5% - 40%) = $15.84 -> $15.99; fees $1.97; profit $6.47 = 40%. Wholesale 12 x $11.50 - $16 postage
- cost $90.62 = $31.38. Inventory 6 + 48 in - 20 sold - 1 damaged = 33. Embroidery: $1,800 / 3,000 h + $0.50 = $1.10/h; thread $5.50/5,500 yd x 5
+ $0.01 = $0.015 per 1,000; cap 6,200 st / 600 + 2 changes = 12.3 min, cost $11.49, retail $23, profit $8.88; bulk 30 logo tees at 24+ tier (10%)
-> $15.00 each, + $35 digitizing + $18 shipping = $503, deposit $251.50, 8.2 machine hours, finish date = 2 working days. Habit: Feb 2027 starts
Monday, 28 days, days 29-31 blank and greyed; goal 90% of 28 = 25; best streak from hidden helper rows; empty months stay blank in the Year Overview.
Also: tools/xlview.py now emulates conditional formatting (cellIs text/number rules, colour scales, data bars, tick rules), so status flags and
heat maps show in all future mockups. Every scene image, pin and listing image viewed; fixed: habit grid too dense (hero shows days 1-15 + stats),
plain uncoloured mockups (CF emulation), all-"In stock" inventory example (two Low stock rows now), embroidery retail too high (x2.0 retail, x1.5 bulk).

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch9; mkdir -p $B/{files,demo,images,scenes,upload,pages}; cd tools; R=$(ls /root/.claude/skills/synced/*/xlsx/scripts/recalc.py)
python3 p16_smallbiz.py $B/files/small-business-pricing-inventory-spreadsheet.xlsx; python3 p17_embroidery.py $B/files/machine-embroidery-business-spreadsheet.xlsx
python3 p18_habits.py $B/files/2027-habit-tracker-spreadsheet.xlsx; python3 p18_habits.py $B/demo/2027-habit-tracker-spreadsheet.xlsx --demo
for f in $B/files/*.xlsx $B/demo/2027*.xlsx; do python3 $R $f 120; done; cp $B/files/small*.xlsx $B/files/machine*.xlsx $B/demo/
S="small-business-pricing-inventory-spreadsheet machine-embroidery-business-spreadsheet 2027-habit-tracker-spreadsheet"
PRODUCTS=products_b9 python3 scenes.py $B/pages $B/demo $B/scenes $S; PRODUCTS=products_b9 python3 mockups.py $B/files $B/images $S
python3 listing_b9.py $B ../batch9 ../pins/batch9
```
Etsy photos = `upload_images` in /home/claude/etsy/batch9/upload (1 = scenes etsy-hero).

## 26 Nov 2026 20:00-20:35 PKT (main chat, Chrome)
- Listed on Etsy with the copy recipe: small business 4626203317 (copy of sticker), embroidery 4626204819 (copy of sticker), habit tracker 4626206151 (copy of reading tracker; Planner Templates / Planners). Image order 1,3,4,5,2 (image 2 has a lot of empty space at right). Tags typed with 1 s pauses (0.5 s garbled 3 tags once; fixed before publishing).
- Pinterest 27 Nov: laser 10:30, small business 12:00, embroidery 15:00, nail 17:30, habit 20:00 PKT (all AI-modified).
