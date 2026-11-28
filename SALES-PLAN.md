# Why no sales yet (diagnosis 27 Nov 2026, 20:30 PKT) and the plan

## Diagnosis
- The problem is VISIBILITY, not checkout: 13 Etsy visits in 30 days, 0 orders. Etsy's own Search visibility page rates the shop and listings "high-quality".
- Etsy search (checked 27 Nov, first ~36 results): jewelry pricing spreadsheet #3; winter junk journal kit #36; debt snowball, wedding budget, 2027 calendar, candle sheet NOT in the first 36.
- Competitors: about half of the top 24 show "% off" sales; median prices $2-5 for printables/planners. Leaders have huge histories (debt snowball leader 64.3k sales; junk journal leader 114k sales).
- Product value: spreadsheets are at feature parity or better (snowball/avalanche/custom + minimums comparison + colour-in chart + savings). Junk journal kits are THIN vs leaders (17 pages vs "1000+ ephemera" mega bundles).
- Pinterest: 18 impressions / 30 days (new account, pins not distributed yet). Amazon Ads: 4 auto campaigns at $1/day, 0 clicks (too low to win placements).

## Done 27 Nov
- 25% shop-wide sale already running to 2 Dec (Cyber Specials).
- NEW: Interested-shopper targeted offer 15% (code WELCOME15), automatic.

## Approved by Awais (27 Nov): Etsy Ads $3/day once available (4 Dec). "Make sure the content you are uploading is worth buying."
## Not approved (ask first): price cuts below launch pricing, Amazon Ads above $1/day, any other spend.

## Rules for every new batch (quality bar = "worth buying")
1. Before building, open the top 3 Etsy results for the product's main keyword; ours must match or beat them on what's inside (count pages/tabs/features), and the listing must say what's inside in the first 2 lines.
2. Printable kits: at least 30 pages, or bundle; never a thin kit at the leaders' price.
3. Spreadsheets: also deliver a Google Sheets "make a copy" link (buyers search "google sheets"), not only .xlsx.
4. Add a 5-15 s listing video (pan through the real pages/tabs, made with ffmpeg from the listing images); listings with video get more visibility.
5. Volume of Pinterest pins up to 10/day only when there are enough distinct product + site pins (no duplicates within 7 days).

## 27 Nov 20:40 PKT (Awais: 'Yes do it' to the pricing moves)
- Starter items now $1.99 (were $3.99): journaling cards 4620615728, Christmas gift tags 4621715645, 2027 printable calendar 4626878631. With the running 25% sale they show about $1.49.
- 40% sale NOT applied: Etsy can't edit a live sale; it must be ended and recreated, and ending it was blocked by the session's safety check. The 25% shop-wide sale stays until 2 Dec unless Awais ends it (Marketing > Sales and discounts > Shop-wide sale > End sale early) and asks for the 40% one.

## 28 Nov 01:25-01:45 PKT (Awais present, 'Do it')
- Old 25% sale CYBER26 ended (it stopped 28 Nov 01:30). New 40% shop-wide sale CYBER40 scheduled 29 Nov 00:00 - 3 Dec 00:00 (Etsy would not let it start 28 Nov because of the overlap). 28 Nov has only WELCOME15. LAUNCH35 (35%, 3 Dec - 2 Jan) was already scheduled.
- Site moved to Git-connected Cloudflare Pages (see site/DEPLOY.md).

## NEXT BATCHES (revenue push, 28 Nov; each must pass the 'worth buying' rule: beat the top 3 Etsy results)
1. Cricket scorebook printable (Etsy: limited-overs + Test sheets, partnership/bowling/fall-of-wickets, US Letter + A4) AND KDP paperback 'Cricket Scorebook: 100 matches' (8.5x11). Cross-sell from pitchsidecric.com.
2. KDP coloring books (autocomplete: 'coloring pages for adults/kids/christmas' is huge): 'Cozy Winter Coloring Book for Adults' + 'Christmas Coloring Book for Kids', 50 original pages each (no copyrighted characters).
3. Junk Journal Mega Bundle upgrade: merge all kits into 60+ pages.
4. Padel-player gift printables? NO: printables only where Etsy demand is proven; check Etsy search counts first.

## BUSINESS MODE (Awais 28 Nov 02:04: "we have to take pinterest, etsy, kdp very serious... We mean business")
Weekly targets (checked by the Monday scorecard):
- PINTEREST: 10 fresh pins/day from 1 Dec (not 5): every product gets 3 pin designs (pin-a/b/c) + every site page a pin; video pins (5-10 s, ffmpeg) for the top 10 products; group into keyword-named boards; descriptions written for Pinterest search terms. Target: 1,000 impressions/week by mid-Dec, 10,000 by end of Jan; outbound clicks > 1% of impressions.
- ETSY: 5 new products/week that beat the top 3 results; videos on all top listings; Etsy Ads $3/day from 4 Dec; 40% sale 29 Nov-2 Dec then LAUNCH35; renew/refresh titles of listings with 0 views after 14 days using Etsy search autocomplete terms. Target: first sale by 7 Dec, 50 sales in January.
- KDP: 2 new books/week in proven-demand niches (coloring books adults/kids/Christmas, cricket scorebook, crochet/knitting journals, planners), each with a real keyword set (7 backend keywords), 2 categories, A+ content, and author page; Amazon Ads: raise from $1/day ONLY with Awais's OK (ask in the Monday report with numbers). Target: 12 live books by end of December, first royalties in December.

## 28 Nov 13:45 PKT: conversion upgrades
- VIDEOS LIVE on 10 listings (11 s fade + slow zoom from the listing images, 1350x1080, made with tools/mkvid.sh in /home/claude/etsy): jewelry 4626872711, debt 4626884176, wedding 4626885492, habit 4626206151, small business 4626203317, candle 4622481559, Christmas party games 4621829841, crochet pricing 4620610040, junk journal mega bundle 4620610591 (6.8 s, only 3 source images), 2027 budget 4621714773. Each "successfully updated". Etsy needs ~25 s to process a video before "Publish changes" works.
- ETSY SEARCH (logged-in fetch of page 1, first ~12 results; may be personalised for the shop owner, so confirm from a logged-out browser before trusting): jewelry pricing spreadsheet #1 (27 Nov #3); 2027 printable calendar #1 (was not in top 36); wedding budget spreadsheet #3 (was not in top 36); debt snowball spreadsheet #9 (was not in top 36); junk journal kit printable not in top 12; candle business spreadsheet not in top 12.
- JUNK JOURNAL AUDIT vs top results for "junk journal kit printable": #1 whole-shop bundle "thousands of pages" $9.95; #2 mega graphics bundle 11,744 files; #3 vintage mega bundle "1000+ ephemera, 100+ papers & pockets"; also a 160-page single kit. OURS: mega bundle 45 pages, single kits ~17 pages. VERDICT: thin. NEXT BATCH: "Junk Journal Mega Bundle 2.0": merge Tea Room + Night Garden + Winter Cottage + December Days + Vintage Ephemera + journaling cards, add 3 new themed kits (cottagecore village, botanical sage, Christmas cluster) to reach 200+ printable pages / 500+ ephemera pieces, with a page-count contact sheet as image 2 and a flip-through video. Price no lower than current launch price (ask Awais before any cut). Single kits: add 20+ pages each (pockets, envelopes, tags, tuck spots) so each passes 40 pages.
