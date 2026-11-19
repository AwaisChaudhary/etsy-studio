# etsy-studio

Product factory for the PurlAndPaperCo Etsy shop and karamat4 Gumroad store.

- `tools/` generators: `xl.py` + `p1..p4_*.py` (spreadsheets), `planner.py`, `kits.py` + `textures.py` (printables), `render.py` (HTML to PDF via headless Chrome),
  `products.py` (listing data), `demo.py` (demo data for screenshots), `mockups.py` (listing images 2000x1600), `listing.py` (descriptions), `preview.py` (preview page).
- Batches live in `batchN/`; built files are not committed (rebuild with the tools). `batchN/listings.json` holds titles, tags, prices and descriptions.
- Rules: original artwork only (no copied images, characters or brands); disclose AI help; spreadsheets must recalculate with zero errors; PDFs in US Letter + A4;
  Etsy tags max 13 x 20 chars, titles max 140; keep each upload file under 3.8 MB.
- Workflow: build batch, publish a preview, then list on Gumroad and Etsy through Claude in Chrome (Awais approved listing new batches without waiting, 19 Nov 2026).
- `brand/`: shop icon (500x500) and big banner (3360x840), made by `brand/make.py`. Palette: ink #1f2a44, berry #b8326a, marigold #f4a823, teal #2f8f8a, paper #eef2ef.

## Listed
Batch 1 (19 Nov 2026): 10 products live on both Etsy (etsy.com/shop/PurlAndPaperCo) and Gumroad (karamat4.gumroad.com), see batch1/listings.json.

## Etsy listing playbook (Shop Manager > Add a listing, https://www.etsy.com/your/shops/me/listing-editor/create)
Changing the main photo of a live listing (edit/<id>#media): photos are dnd-kit sortables ([aria-roledescription=sortable], id = photo id). Upload to "Add photos", then focus the new tile via JS, press Space, Up, Left x5, Space (repeat once), check order via JS, delete old tiles by hovering a tile and clicking its trash icon, then "Publish changes". Mouse drag does NOT work. Etsy shows square crops in the shop grid: keep hero text inside the centre square (x 200-1800 of 2000).
1. Photos: upload 5 JPGs to the hidden "Add photos" file input (max 3.8 MB per upload call).
2. Category (combobox): spreadsheets -> Bookkeeping Templates (stash tracker -> Planner Templates); planners -> Planner Templates; kits/ephemera -> Scrapbooking Ephemera; cards -> Journaling Spots.
3. "What type of item is it?" -> Digital. Then set title (#listing-title-input) and description (#listing-description-textarea) via JS native value setter + input/change/blur events.
   Etsy titles may use %, & or : only once.
4. Digital files: hidden file input that appears after choosing Digital (up to 5 files).
5. Tags: type all 13 comma-separated, press Enter. Price: click the field by coordinate and type (ref clicks sometimes lose the value; verify "Estimated earnings" appears). Quantity 999.
6. How it's made: "I did"; spreadsheets/planners "A finished product", kits/cards "A supply or tool to make things"; "With an AI generator" (honest disclosure).
7. Publish -> confirm dialog ($0.20 fee). Renewal automatic.

## Gumroad playbook
gumroad.com/products/new -> name + price -> Next; edit page: square thumbnail, cover images, description (no lines starting "1." - they auto-number), URL slug, summary; Save; Content tab: upload files; Save; Publish.
- Covers: click "Upload images or videos" (or "Add cover" then that button), THEN `find` the file input labelled "Computer files" and upload several JPGs in one call (order is kept: scenes etsy-hero first, then features/details/how-it-works). Remove a cover: hover its small thumbnail, click the red x at its top-right.
- Thumbnail: click the trash icon on the thumbnail, then the "Upload" file input appears; upload scenes gumroad-thumb (600x600).
- Use the 2000x1600 etsy-hero as cover 1 so all covers share one aspect ratio. Profile: name "Purl & Paper", shop icon avatar, bio with Etsy link (set 19 Nov).

## Scenes (v2 design, 19 Nov 2026)
`tools/scenes.py` makes styled product scenes from the real product pages: pins (pin-a fan, pin-b tossed pages, 1000x1500), Etsy hero (2000x1600), Gumroad cover (1280x720) and thumbnail (600x600).
Render pages first: `pdftoppm -r 110 -png files/<slug>-US-Letter.pdf pages/<slug>/p`, then
`python3 tools/scenes.py <pages> <demo_xlsx_dir> <out> [slug...]`. Each new product needs an entry in `T` (surface, colours, title, chips, seal text; spreadsheets also a sticky `note`).
`tools/xlview.py` holds the spreadsheet-window renderer shared with mockups.py. Pins are marked "AI-modified" on Pinterest.

## Pinterest (business account "Purl & Paper", pinterest.com/purlandpaperco)
Boards: Junk Journal Printables, Crochet & Knitting Planners, Small Business Spreadsheets (add a board when a new lane has 3+ products, e.g. Christmas Printables).
`pins/queue.json` = pins to post, in order; set `status` to "published <date>" / "scheduled <date time>" after posting. Daily: post the next 3 queued pins + pin-a of each new product (render with tools/scenes.py, add pin-b to the END of the queue).
Playbook (pinterest.com/pin-creation-tool/): upload the JPG via the hidden file input (find "File Upload"), title, description, link, board dropdown, Tagged topics (type, wait, pick first match; if suggestions look unrelated, delete and retype the last letter), turn ON "Mark as AI-Modified", Publish. "Publish at a later date" shows date/time fields (default tomorrow 12:00 PM) then Schedule -> confirm. Pins link to the Etsy listing (pin-a) or Gumroad product (pin-b). Etsy shop claim is not offered for this account; claim the crafts website once it has a domain.
Rules: max ~5 new pins a day while the account is new; never repost the same image; no follow/comment automation.
