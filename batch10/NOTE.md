# Batch 10 — 27 Nov 2026 (BUILT, NOT LISTED)

Status: built and checked in the scheduled cloud run (~19:00-19:15 PKT). Claude in Chrome was not reachable from this cloud run (the scheduled task
does not have "Require this computer" on), so nothing was listed, pinned or deployed, and Etsy Stats / Etsy search pages / Pinterest could not be read.
First day of the 5/day ramp. Prices follow Awais's 26 Nov launch pricing (business sheet $7.99, planners/printables $3.99-5.99). No Gumroad.

Next run with Chrome: (1) list these 5 on Etsy (listings.json has copy, tags, category, section; fast recipe: copy the embroidery sheet 4626204819 for
jewelry, the habit tracker 4626206151 for debt + wedding, the Tea Room kit 4620607287 for Winter Cottage, the habit tracker for the calendar but set
category Calendars & Planners), (2) set listed / etsy_url, (3) post their pin-a (queued right before the other queued pins; status
"queued (needs listing first)"; fill `link` from etsy_url; pin-b's are at the end of the queue, same status), (4) add the 5 to SHOP in site/build.py and deploy.
Wedding: when a 3rd wedding/party item exists, create an Etsy section + Pinterest board "Wedding Planning".

Double down on winners: not checked (no Etsy Stats this run; as of 26 Nov 20:20: 0 orders, no listing with 3+ favourites), so no spin-offs.
Etsy search pages could not be checked (no Chrome). Choice is based on Awais's 26 Nov Etsy research (cheap, broad sheets win Bestseller badges) and
seasonality: debt payoff / budget sheets and 2027 calendars peak in Dec-Jan (New Year), December is the biggest engagement month (wedding planners
sell Dec-Feb), winter journal kits sell Nov-Feb, and handmade jewelry is one of the largest Etsy maker groups (web search: plenty of generic
pricing sheets, few that price by metal weight).

| Product | Lane | Price | File |
|---|---|---|---|
| Jewelry Business Spreadsheet (metal price table per troy oz -> per gram + waste %; findings/stones/chain library with cost per unit + reorder flags; design costing: metal weight, 4 materials, other cost, minutes, overheads; THREE prices: classic formula (materials x2 + labour = wholesale, x2 retail), cost x multiplier, margin price after Etsy fees; your price with profit, margin, profit/hour, price check; custom orders with ring size, engraving, deposit, balance, Due soon/Overdue; stock in, inventory, sales by 6 channels, expenses, dashboard + chart) | a | 7.99 | 1 xlsx (11,803 formulas, 0 errors) |
| Debt Payoff Planner Spreadsheet (12 debts; Snowball / Avalanche / Custom order; 360-month plan that pays minimums, sends the extra to order 1 and rolls freed payments on; per-debt months, debt-free date and interest; Minimums Only comparison -> interest + months saved; payment log, % paid with data bars; 100-square colour-in chart via conditional formatting; savings goals with per-month amount + savings log; dashboard with line chart) | b | 4.99 | 1 xlsx (25,361 formulas, 0 errors) |
| Wedding Budget Planner Spreadsheet (setup + countdown; 12 categories / 43 items with guide % summing to 100% and budget prefilled from total; actual, paid (split by vendor share), still to pay, over/under; vendors; payment schedule with Due soon/Overdue; guest list with RSVP, adults/kids, meals, dietary, table, gifts, thank-yous; 60-task checklist dated from the wedding day; dashboard with meal counts and budget vs actual chart) | g | 5.99 | 1 xlsx (1,451 formulas, 0 errors) |
| Winter Cottage Junk Journal Kit (17 pages: intro, 2 frost papers, snowy cottage at dusk plate, plain paper, ledger, winter greenery plate, 4 cottage kitchen recipe cards, Nordic knit pattern, flannel plaid, lined letter, Winter List, 8 tags, 12 labels, 8 tickets, 12 stamps, 4 journaling cards) | c | 4.99 | 2 PDFs (~2.1 MB each) |
| 2027 Printable Calendar (cover, year at a glance, 12 monthly pages each with an original seasonal pattern; Sunday + Monday start; no holidays printed) | b/d | 3.99 | 4 PDFs (~0.43 MB each) |

Checks (sample values): Jewelry: sterling $38/oz = $1.22/g; necklace 1.6 g x 1.08 waste = $2.11 metal + $7.82 findings + 55 min at $22 = $20.17 +
10% overhead $0.99 -> cost $31.09; classic wholesale (2.11 + 7.82 + 0.99) x 2 + 20.17 = $42.05, retail $84.99; x2.5 = $77.99; margin price
(31.09 + 0.45) / (1 - 9.5% - 40%) = $62.46 -> $62.99, profit $25.47 = 40%; brass pendant at $39 flags "Below target". Custom orders: due in 2 days
"Due soon", -1 day "Overdue", shipped blank. Debt: the 6 example debts ($23,920, $1,150/month) were re-simulated in Python: 24 months and
$3,055.66 interest, exactly matching the sheet; avalanche order (store, Visa, Mastercard, personal, car, medical) gives $2,795.20 interest; minimums
only 57 months / $6,872.05 -> saves $3,816.39 and 33 months. Plan avoids circular references (explicit per-debt cells, no row-range SUMIF).
Wedding: guide % = 100%; Wild Stem Florals $500 deposit split 203/297 across its two budget lines; 295 days to 18 Sep 2027.
Every scene, pin, listing image and centre-square crop viewed; fixed: jewelry hero showed cost columns only (now cost + 3 prices), wedding hero
too dense (10 rows, 6 columns), July calendar yellow-on-cream header (per-month dark accents), sparse winter greenery plate (bigger plants).

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch10; mkdir -p $B/{files,demo,images,scenes,upload,pages}; cd tools; R=$(ls /root/.claude/skills/synced/*/xlsx/scripts/recalc.py)
python3 p19_jewelry.py $B/files/jewelry-business-spreadsheet.xlsx; python3 p20_debt.py $B/files/debt-payoff-planner-spreadsheet.xlsx
python3 p21_wedding.py $B/files/wedding-budget-planner-spreadsheet.xlsx; for f in $B/files/*.xlsx; do python3 $R $f 300; done; cp $B/files/*.xlsx $B/demo/
python3 b10_winter.py $B/files; python3 b10_calendar.py $B/files
mkdir -p $B/pages/winter-cottage-junk-journal-kit $B/pages/2027-printable-calendar
pdftoppm -r 110 -png $B/files/winter-cottage-junk-journal-kit-US-Letter.pdf $B/pages/winter-cottage-junk-journal-kit/p
pdftoppm -r 110 -png $B/files/2027-printable-calendar-US-Letter-Sunday-Start.pdf $B/pages/2027-printable-calendar/p
S="jewelry-business-spreadsheet debt-payoff-planner-spreadsheet wedding-budget-planner-spreadsheet winter-cottage-junk-journal-kit 2027-printable-calendar"
PRODUCTS=products_b10 python3 scenes.py $B/pages $B/demo $B/scenes $S; PRODUCTS=products_b10 python3 mockups.py $B/files $B/images $S
python3 listing_b10.py $B ../batch10 ../pins/batch10
```
Etsy photos = `upload_images` in /home/claude/etsy/batch10/upload (1 = scenes etsy-hero).
