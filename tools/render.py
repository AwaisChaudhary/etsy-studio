"""Render a list of HTML page divs to a print-ready PDF (and optional PNG previews) with headless Chrome."""
import pathlib, tempfile
from playwright.sync_api import sync_playwright

SIZES = {"letter": ("8.5in", "11in", "Letter"), "a4": ("210mm", "297mm", "A4"), "letter-l": ("11in", "8.5in", "Letter"), "a4-l": ("297mm", "210mm", "A4")}

def html_doc(css, pages, size):
    pw, ph, _ = SIZES[size]
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page {{ size: {pw} {ph}; margin: 0; }}
:root {{ --pw: {pw}; --ph: {ph}; }}
html, body {{ margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
{css}
</style></head><body>{''.join(pages)}</body></html>"""

def render(css, pages, size, pdf_path, previews=None):
    """previews: list of (page_index, png_path) to screenshot at 150 dpi."""
    doc = html_doc(css, pages, size)
    tmp = pathlib.Path(tempfile.mkdtemp()) / "doc.html"; tmp.write_text(doc, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page()
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(300)
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        if previews:
            pg.emulate_media(media="print")
            pg.set_viewport_size({"width": 816 if size == "letter" else 794, "height": 1056 if size == "letter" else 1123})
            for idx, png in previews:
                el = pg.locator(".page").nth(idx)
                el.screenshot(path=png, scale="device") if False else el.screenshot(path=png)
        b.close()
    return pdf_path
