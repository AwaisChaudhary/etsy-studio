# Batch 5 — 22 Nov 2026 (BUILT, NOT LISTED)

Status: built and checked in the cloud run at 18:54 PKT. Claude in Chrome was not reachable (the scheduled task does not have
"Require this computer" on), so nothing was listed, pinned or deployed, and Etsy Stats / Gumroad sales could not be read this run.
Next run with Chrome: list these 3 (listings.json has all copy), post their pin-a (queued just before the other queued pins), deploy the site (23 pages build fine).

| Product | Lane | Price | Files (each < 3.8 MB) |
|---|---|---|---|
| 2027 Reading Tracker Spreadsheet (book log 399 rows, dashboard with goal bars + monthly/genre/format stats + top-10 rated, 36-prompt reading challenge that ticks itself off, TBR list) | b planners & trackers | 7.99 | 1 xlsx (2,408 formulas, 0 errors after LibreOffice recalc) |
| New Year's Eve Party Games 2027 (24 bingo cards + caller, 20-question traditions trivia, most likely to x24, would you rather x24, scramble, 2027 predictions, 2026 in review, 6 countdown-to-midnight bag tags, score sheet, keys; 26 pp) | g/d party + seasonal | 6.99 | 2 PDFs (Letter, A4), ~1.2 MB each |
| Kids Routine & Chore Chart Pack (morning/after-school/bedtime picture charts, chores for 3-5/6-9/10-12 + blank, 20 and 30 sticker reward charts, 28 picture cards + blanks, 8 reward coupons, My 2027 Goals; 28 original icons; 15 pp) | h kids & education | 5.99 | 2 PDFs (Letter, A4), ~1.4 MB each |

Why these: reading trackers and New Year resets peak Dec-Jan (2027 reading goal / reading challenge searches); NYE party games sell from early
December and complement the Christmas party games bundle (bundle candidate later); lane h only had the Christmas activity pack, and chore /
routine charts are evergreen with a New Year bump. Lane b now has 4 products (crochet planner, budget, gift planner, reading tracker):
create Etsy section + Pinterest board "Planners & Trackers" (batch-5 pins use that board name).

Checks: reading tracker tested with sample books (4 finished = 1,498 pages, avg 4.25, monthly counts, genre averages, top-rated list in order,
challenge ticks only Finished books, TBR "In log" flag). Trivia answers double-checked. Every scene image and centre-square crop viewed.
Fixed during build: score sheet rows missing (unquoted style), chore-chart icons stacked above text, countdown intro overlapping tags.

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch5; mkdir -p $B/{files,pages,images,scenes,demo,upload}; cd tools
python3 p8_reading.py $B/files/2027-reading-tracker-spreadsheet.xlsx && python3 <recalc.py> $B/files/2027-reading-tracker-spreadsheet.xlsx 90
python3 demo_b5.py $B/files $B/demo
python3 b5_nye.py $B/files; python3 b5_kids.py $B/files   # then qpdf --object-streams=generate --recompress-flate --compression-level=9
for s in new-years-eve-party-games kids-routine-chore-chart-pack; do mkdir -p $B/pages/$s; pdftoppm -r 110 -png $B/files/$s-US-Letter.pdf $B/pages/$s/p; done
PRODUCTS=products_b5 python3 scenes.py $B/pages $B/demo $B/scenes 2027-reading-tracker-spreadsheet new-years-eve-party-games kids-routine-chore-chart-pack
PRODUCTS=products_b5 python3 mockups.py $B/files $B/images 2027-reading-tracker-spreadsheet new-years-eve-party-games kids-routine-chore-chart-pack
python3 listing_b5.py $B ../batch5
```

Listing notes
- Etsy categories: reading tracker -> Planner Templates; NYE games -> Party Games; kids pack -> Planner Templates (or closest "Chore Chart"/kids printable).
  How it's made: "I did", "A finished product", "With an AI generator". Digital, quantity 999, auto-renew.
- Shop sections: reading tracker + kids pack -> new "Planners & Trackers"; NYE games -> "Christmas Printables" (rename to "Holiday Printables" later if wanted).
- Gumroad slugs planned: 2027-reading-tracker, new-years-eve-party-games, kids-routine-chore-charts.
- After listing: set listed / etsy_url / gumroad_url in batch5/listings.json and fill `link` on the 6 batch-5 pins in pins/queue.json.

## Listed 23 Nov 2026 02:20-02:33 PKT (main chat)
- Etsy: reading tracker 4623371099 (Planner Templates, section Planners), NYE games 4623381612 (Party Games, Celebration New Year's, section Christmas Printables), kids pack 4623374247 (Chore Chart Templates, section Planners). Used existing "Planners" section instead of creating "Planners & Trackers".
- A duplicate kids listing (4623384240) was created because the first publish took ~1 min to appear; deactivated (not deleted). Lesson: after Publish, wait 60 s and re-check the listing grid before retrying.
- Pinterest: created board "Planners & Trackers"; pin-a of all 3 published now (AI-modified on).
- Gumroad: not yet.
