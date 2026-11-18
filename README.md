# etsy-studio

Product factory for the PurlAndPaperCo Etsy shop and karamat4 Gumroad store.

- `tools/` generators: `xl.py` + `p1..p4_*.py` (spreadsheets), `planner.py`, `kits.py` + `textures.py` (printables), `render.py` (HTML to PDF via headless Chrome),
  `products.py` (listing data), `demo.py` (demo data for screenshots), `mockups.py` (listing images 2000x1600), `listing.py` (descriptions), `preview.py` (preview page).
- Batches live in `batchN/`; built files are not committed (rebuild with the tools). `batchN/listings.json` holds titles, tags, prices and descriptions.
- Rules: original artwork only (no copied images, characters or brands); disclose AI help; spreadsheets must recalculate with zero errors; PDFs in US Letter + A4;
  Etsy tags max 13 x 20 chars, titles max 140; keep each upload file under 3.8 MB.
- Workflow: build batch, publish preview, wait for Awais's "go", then list on Gumroad and Etsy through Chrome.

## Listed
Batch 1 (19 Nov 2026): 10 products, see batch1/listings.json.
