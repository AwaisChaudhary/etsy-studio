# Batch 3 — 20 Nov 2026 (LIVE on Etsy + Gumroad, listed 21:20 PKT)

Status: built and checked in the cloud run at 18:54 PKT. Chrome on Awais's computer was not reachable (scheduled task does not
have "Require this computer" on), so nothing was listed, pinned or deployed this run. Next run with Chrome: list these 3 first.

| Product | Lane | Price | Files |
|---|---|---|---|
| Christmas Party Games Bundle (30 pp: bingo x30 cards, trivia x30, would you rather, most likely to, scramble, this or that, hunt, dice swap, scores, awards, keys) | g/d party + seasonal | 7.99 | 2 PDFs (Letter, A4), 0.9 MB each |
| Kids Christmas Activity Pack (24 pp: 6 colouring, 2 word searches, 2 mazes, letter to Santa, countdown, Nice List, keys) | h kids | 5.99 | 2 PDFs, 0.4 MB each |
| Winter Woodland Wall Art, set of 3 (Moonlit Pines, Winter Mountains, Winter Berries; 6 ratios, 300 dpi, up to 24x36 / A2) | e wall art | 7.99 | 5 ZIPs, 1.6-2.0 MB each |

Rebuild (built files are not committed):
```
B=/home/claude/etsy/batch3; mkdir -p $B/{files,pages,images,scenes,demo,upload}; cd tools
python3 b3_party.py $B/files; python3 b3_kids.py $B/files; python3 b3_wallart.py $B/wallart   # then zip step (see listing note below)
for s in christmas-party-games-bundle kids-christmas-activity-pack; do mkdir -p $B/pages/$s; pdftoppm -r 110 -png $B/files/$s-US-Letter.pdf $B/pages/$s/p; done
PRODUCTS=products_b3 python3 scenes.py $B/pages $B/demo $B/scenes christmas-party-games-bundle kids-christmas-activity-pack
PRODUCTS=products_b3 python3 mockups.py $B/files $B/images christmas-party-games-bundle kids-christmas-activity-pack
python3 b3_wallscenes.py $B/wallart $B/scenes $B/images
python3 listing_b3.py $B ../batch3      # writes listings.json + $B/upload/*.jpg (Etsy photos 1-5, Gumroad cover/thumb)
```
Wall art ZIPs: one per ratio (2x3, 3x4, 4x5, ISO-A) + 11x14-and-5x7 together, each with PRINTING-GUIDE.txt (JPG q90, 300 dpi tag).

Listing notes
- Etsy categories: party games -> Party Games (Paper & Party Supplies > Party Supplies > Party Games); kids pack -> Coloring Books / Kids activity
  (Paper & Party Supplies > Paper > ... pick the closest "Coloring" category); wall art -> Art & Collectibles > Prints > Digital Prints.
  How it's made: "I did", "A finished product", "With an AI generator".
- New Etsy shop section + Pinterest board: "Christmas Printables" (gift tags, party games, kids pack = 3+ products). Wall art: section "Wall Art";
  board "Printable Wall Art" once 3 products exist (pin to Christmas Printables until then).
- Gumroad slugs planned: christmas-party-games, kids-christmas-activity-pack, winter-woodland-wall-art.
- After listing: set listed/etsy_url/gumroad_url in batch3/listings.json, fill `link` on the 6 batch-3 pins in pins/queue.json.

Double-down check: not possible this run (Etsy Stats / Gumroad need Chrome). batch1/batch2 listings.json now carry their live Etsy/Gumroad URLs (backfilled from the pin queue).

## Listed 20 Nov, 21:20 PKT (evening follow-up from Awais's Chrome)
- Etsy: party games 4621829841, kids pack 4621831051, wall art 4621832807. New shop sections: "Christmas Printables", "Wall Art".
- Gumroad: /l/christmas-party-games, /l/kids-christmas-activity-pack, /l/winter-woodland-wall-art (wall-art ZIPs in 2 named folders).
- Wall-art copy corrected: files are 300 dpi at 16x24 in / A2 (200 dpi at 24x36 / A1); tools/b3_zip.py added for the ZIP step.
- Pinterest: new board "Christmas Printables"; pin-a x3 scheduled 21 Nov 12:00, 14:00, 17:00.
- To do: move the Christmas gift tags listing into the "Christmas Printables" Etsy section.
