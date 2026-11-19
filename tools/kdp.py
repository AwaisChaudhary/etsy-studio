"""KDP paperback helpers: interior PDF with mirrored margins (no bleed) and full-wrap cover PDF.
Specs (KDP help, checked 20 Nov 2026): gutter >= 0.375in for 24-150 pages (0.5in 151-300), outside/top/bottom >= 0.25in without bleed;
spine = pages x 0.002252in (white paper); cover = 0.125 bleed + back + spine + front + 0.125 bleed, height = trim + 0.25in."""
import pathlib, tempfile
from playwright.sync_api import sync_playwright

WHITE_PER_PAGE = 0.002252


def gutter_for(pages):
    return 0.375 if pages <= 150 else 0.5 if pages <= 300 else 0.625


def _pdf(html, path, w_in, h_in, previews=None, sel=".pg"):
    tmp = pathlib.Path(tempfile.mkdtemp()) / "doc.html"
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": int(w_in * 96), "height": int(h_in * 96)})
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(400)
        pg.pdf(path=str(path), width=f"{w_in}in", height=f"{h_in}in", print_background=True, prefer_css_page_size=True)
        for idx, png in previews or []:
            pg.locator(sel).nth(idx).screenshot(path=str(png))
        b.close()
    return path


def interior(pages_html, css, trim_w, trim_h, out, inside=0.6, outside=0.45, top=0.5, bottom=0.55, previews=None):
    """pages_html: list of inner HTML per page. Page 1 is a right-hand (recto) page, so its gutter is on the left."""
    n = len(pages_html)
    if n % 2:
        pages_html = pages_html + ['<div class="blank"></div>']
        n += 1
    assert inside >= gutter_for(n) and min(outside, top, bottom) >= 0.25, "margins below KDP minimum"
    body = []
    for i, h in enumerate(pages_html):
        recto = i % 2 == 0
        l, r = (inside, outside) if recto else (outside, inside)
        body.append(f'<section class="pg" style="padding:{top}in {r}in {bottom}in {l}in" data-n="{i + 1}">{h}</section>')
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page {{ size: {trim_w}in {trim_h}in; margin: 0; }}
html,body {{ margin:0; padding:0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.pg {{ width:{trim_w}in; height:{trim_h}in; box-sizing:border-box; page-break-after: always; overflow:hidden; position:relative; display:flex; flex-direction:column; }}
{css}
</style></head><body>{''.join(body)}</body></html>"""
    _pdf(html, out, trim_w, trim_h, previews)
    return n


def cover(front_html, back_html, spine_html, css, trim_w, trim_h, pages, out, preview=None):
    spine = round(pages * WHITE_PER_PAGE, 4)
    W = round(0.125 + trim_w + spine + trim_w + 0.125, 4)
    H = trim_h + 0.25
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page {{ size: {W}in {H}in; margin: 0; }}
html,body {{ margin:0; padding:0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.wrap {{ width:{W}in; height:{H}in; position:relative; overflow:hidden; display:grid; grid-template-columns: {0.125 + trim_w}in {spine}in {trim_w + 0.125}in; }}
.back {{ padding: 0.5in 0.5in 0.5in 0.625in; box-sizing:border-box; position:relative; }}
.spine {{ position:relative; overflow:hidden; }}
.front {{ padding: 0.5in 0.625in 0.5in 0.5in; box-sizing:border-box; position:relative; }}
{css}
</style></head><body><div class="wrap pg"><div class="back">{back_html}</div><div class="spine">{spine_html}</div><div class="front">{front_html}</div></div></body></html>"""
    _pdf(html, out, W, H, [(0, preview)] if preview else None)
    return {"spine_in": spine, "width_in": W, "height_in": H}
