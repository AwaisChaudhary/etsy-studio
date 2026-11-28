# Batch 11 — 28 Nov 2026 (BUILT, NOT LISTED)

Status: built and checked in the scheduled cloud run (~19:00-20:30 PKT). Claude in Chrome was not reachable from this cloud run (the scheduled
task does not have "Require this computer" on), so nothing was listed, pinned or deployed, and Etsy Stats / Etsy search pages / Pinterest could not be read.
5 products (27 Nov ramp). Prices follow Awais's 26 Nov launch pricing (business sheet $7.99, planners/printables $3.99-4.99). No Gumroad.
The required $4.99 "Small Business Pricing + Inventory + Profit" sheet already exists (batch 9, live as 4626203317), so it was not rebuilt.

Next run with Chrome: (1) list these 5 on Etsy (listings.json has copy, tags, category, section; fast recipe: copy the small business sheet
4626203317 for bookkeeping, the habit tracker 4626206151 for the workout planner and the cricket scorebook, the Christmas gift tags 4621715645 for
the Santa kit and the Valentine cards), (2) upload the 11 s videos (/home/claude/etsy/batch11/video/<slug>.mp4, rebuild with tools/mkvid.sh),
(3) set listed / etsy_url, (4) post pin-a's (queued after the batch 10 pin-a's, status "queued (needs listing first)"; fill `link` from etsy_url;
pin-b's are at the end of the queue), (5) add the 5 to SHOP in site/build.py and deploy, (6) spreadsheets: add a Google Sheets "make a copy" link
(SALES-PLAN rule 3) once Drive is reachable. Santa kit first: Christmas window is short.
Sections: Christmas items now 3+ (Christmas party games, gift tags, advent cards, December journal, Santa kit) -> create Etsy section "Christmas"
if missing. Kids lane now has 4 (kids Christmas pack, chore chart, advent, Valentine cards) -> "Kids Printables" section.

Double down on winners: not checked (no Etsy Stats this run; as of 27 Nov 20:50: 0 orders, 13 visits/30 days, no listing with 3+ favourites), so no spin-offs.
Etsy search pages could not be checked (no Chrome). Web search (28 Nov): 2027 bookkeeping / income-expense sheets are a large, proven Etsy niche
(many 2027 listings, bundles); workout tracker spreadsheets show "20+ views in the last 24 hours" on several listings (New Year demand);
letter-from-Santa kits are a classic December seller (personalised + printable kits everywhere); cricket scorebooks are mostly physical books
(Gray-Nicolls etc.) with few Etsy printables = low competition (SALES-PLAN item 1); kids classroom Valentines sell Jan-early Feb, listing now builds history.

| Product | Lane | Price | File |
|---|---|---|---|
| Self-Employed Bookkeeping Spreadsheet 2027 (setup: tax year, set-aside %, mileage rate, US quarterly due dates (editable), 8 income + 22 tax-style expense categories; income log with fees -> net; expenses with business-use %, receipt check, tax line; mileage log with round trips -> deduction; invoices with Due soon / Overdue / days late; monthly P&L by category with margin %; quarterly tax set-aside with status; dashboard: net profit, margin, tax to set aside, next due date, unpaid/overdue invoices, missing receipts, bank estimate, top 6 expense categories, income vs expenses chart with profit line) | a | 7.99 | 1 xlsx (9,860 formulas, 0 errors) |
| 2027 Workout Planner & Fitness Tracker Spreadsheet (setup kg/lb, km/miles, weekly target, 3 goals; 71-exercise library; weekly split planner; strength log 3,000 rows with volume, Epley est. 1RM, best so far, automatic NEW PR flag (MAXIFS); cardio log with pace + speed; body & wellbeing; personal records per exercise; 365-day 2027 colour-in calendar; weekly totals; dashboard with streaks, target weeks, top lifts, charts) | b | 4.99 | 1 xlsx (20,583 formulas, 0 errors) |
| Letter from Santa Kit (14 pages: intro, letter to Santa, draw-your-wish letter, wish list, pre-written letter FROM Santa with blanks, blank North Pole letterhead, Nice List certificate, Nice List scroll, envelope labels + 6 stamps, 4 reindeer food toppers + wildlife-friendly recipe, Santa stop here sign, cookie/carrot/milk plate tent cards + 2 notes, thank-you note from Santa, colouring page; undated) | d/h | 3.99 | 2 PDFs (~1 MB) |
| Cricket Scorebook Printable (10 landscape pages: cover + scoring key, batting card with ball-by-ball boxes + fall of wickets, bowling analysis 10 over boxes x 8 bowlers + 50-over tally, long-format bowling 30 overs, one-page T20 card, partnerships + match summary, field placings (labelled RH field + 4 blank), season batting + bowling averages, fixtures & results) | b (sports) | 3.99 | 2 PDFs (~0.9 MB) |
| Kids Valentine Cards for Class (8 pages: cover, 12 original punny critters in colour (2 pages) + colour-it-yourself (2 pages), 4 treat bag toppers, make-your-own page, class checklist) | h/d | 3.99 | 2 PDFs |

Checks (sample values): Bookkeeping: Jan gross $3,690.60 = sum of 6 example payments; Jan expenses $681.90 = $628.84 deductible (phone 60% = $28.80) +
75.8 mi x $0.70 mileage $53.06; Q1 profit $4,949.44, set-aside 25% = $1,237.36, $300 saved -> $937.36 still to set aside; invoice 38 days old on 30-day terms
-> Overdue 8 days, 10 days old on 14 -> Due soon. Workout: bench 60 kg x 8 -> est. 1RM 76.0; later sessions flag NEW PR only when the estimate beats
the previous best; repeated leg curl weight shows no flag; cardio 30 min / 5 km -> 6:00 per km; body weight change -0.5 kg; calendar fills on logged days
(Jan 23 days). Every scene, pin, listing image and centre-square crop viewed; fixed: field-placing labels crowded (slip cordon spread),
Dear Santa page empty bottom (bigger lines + draw box), Valentine card art small, spreadsheet feature panels tiny (xlview tab bar no longer sets window
width: tools/xlview.py + mockups.py `.tabs{contain:inline-size}`), pace shown as 0:06:00.000 in mockups (xlview now formats timedelta as m:ss),
workout dashboard zeros (current streak / this week / this month moved below the screenshot area: they are 0 until 2027 starts).

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch11; mkdir -p $B/{files,demo,images,scenes,upload,pages,video}; cd tools; R=$(ls /root/.claude/skills/synced/*/xlsx/scripts/recalc.py)
python3 p22_bookkeeping.py $B/files/self-employed-bookkeeping-spreadsheet.xlsx; python3 p23_workout.py $B/files/2027-workout-planner-fitness-tracker.xlsx
for f in $B/files/*.xlsx; do python3 $R $f 300; done; cp $B/files/*.xlsx $B/demo/
python3 b11_santa.py $B/files; python3 b11_cricket.py $B/files; python3 b11_valentine.py $B/files
for s in letter-from-santa-kit cricket-scorebook-printable kids-valentine-cards-classroom; do mkdir -p $B/pages/$s; pdftoppm -r 110 -png $B/files/$s-US-Letter.pdf $B/pages/$s/p; done
S="self-employed-bookkeeping-spreadsheet 2027-workout-planner-fitness-tracker letter-from-santa-kit cricket-scorebook-printable kids-valentine-cards-classroom"
PRODUCTS=products_b11 python3 scenes.py $B/pages $B/demo $B/scenes $S; PRODUCTS=products_b11 python3 mockups.py $B/files $B/images $S
python3 listing_b11.py $B ../batch11 ../pins/batch11
for s in $S; do ./mkvid.sh $B/video/$s.mp4 $B/upload/$s-{1,2,3,4,5}.jpg; done
```
Etsy photos = `upload_images` in /home/claude/etsy/batch11/upload (1 = scenes etsy-hero). render.py now also takes "letter-l" / "a4-l" (landscape).
