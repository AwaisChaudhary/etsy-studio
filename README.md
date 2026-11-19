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
