"""Listing images (2000 x 1600) for each product: hero, features, detail shots, how it works."""
import base64, datetime, html, pathlib, subprocess, sys, tempfile
from openpyxl import load_workbook
from openpyxl.utils import range_boundaries, get_column_letter
from playwright.sync_api import sync_playwright
from products import P

FILES = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
TMP = pathlib.Path(tempfile.mkdtemp())
e = html.escape

def b64(path): return "data:image/png;base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()

# ---------- spreadsheet screenshot as HTML ----------
def fmt(v, nf):
    if v is None: return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        if "dddd" in nf: return v.strftime("%A %d %b %Y")
        if "ddd" in nf: return v.strftime("%a %d %b")
        return v.strftime("%d %b %Y")
    if isinstance(v, datetime.time): return v.strftime("%I:%M %p").lstrip("0")
    if isinstance(v, (int, float)):
        if "%" in nf: return f"{v * 100:.0f}%" if "0%" == nf else f"{v * 100:.1f}%"
        if "$" in nf:
            dec = 4 if ".0000" in nf else 2 if ".00" in nf else 0
            return ("-$" if v < 0 else "$") + f"{abs(v):,.{dec}f}"
        if nf.endswith("x"): return f"{v:.1f}x"
        if "0.0" in nf: return f"{v:,.1f}"
        if nf == "0": return f"{v:.0f}"
        if nf == "#,##0": return f"{v:,.0f}"
        if isinstance(v, float) and not v.is_integer(): return f"{v:,.2f}"
        return f"{v:,.0f}"
    return str(v)

def xl_html(path, sheet, rng, tabs, active):
    wf = load_workbook(path); wv = load_workbook(path, data_only=True)
    ws, vs = wf[sheet], wv[sheet]
    c1, r1, c2, r2 = range_boundaries(rng)
    merged = {}
    skip = set()
    for m in ws.merged_cells.ranges:
        a, b, c, d = m.min_col, m.min_row, m.max_col, m.max_row
        if b >= r1 and b <= r2:
            merged[(b, a)] = (min(d, r2) - b + 1, min(c, c2) - a + 1)
            for rr in range(b, d + 1):
                for cc in range(a, c + 1):
                    if (rr, cc) != (b, a): skip.add((rr, cc))
    cols = "".join(f'<th style="width:{int((ws.column_dimensions[get_column_letter(c)].width or 9) * 7.2)}px">{get_column_letter(c)}</th>' for c in range(c1, c2 + 1))
    rows = ""
    for r in range(r1, r2 + 1):
        h = ws.row_dimensions[r].height or 18
        tds = ""
        for c in range(c1, c2 + 1):
            if (r, c) in skip: continue
            cell, val = ws.cell(r, c), vs.cell(r, c).value
            st = []
            if cell.fill and cell.fill.fgColor and cell.fill.fill_type == "solid" and cell.fill.fgColor.rgb not in (None, "00000000"):
                st.append(f"background:#{str(cell.fill.fgColor.rgb)[-6:]}")
            f = cell.font
            if f:
                if f.b: st.append("font-weight:700")
                if f.i: st.append("font-style:italic")
                if f.sz: st.append(f"font-size:{float(f.sz) * 1.35:.0f}px")
                if f.color is not None and f.color.rgb and isinstance(f.color.rgb, str): st.append(f"color:#{f.color.rgb[-6:]}")
            al = cell.alignment
            if al and al.horizontal == "center": st.append("text-align:center")
            if al and al.wrap_text: st.append("white-space:normal")
            if cell.border and cell.border.left and cell.border.left.style: st.append("box-shadow:inset 0 0 0 1px #d5dce3")
            span = ""
            if (r, c) in merged: rs, cs = merged[(r, c)]; span = f' rowspan="{rs}" colspan="{cs}"'
            tds += f'<td{span} style="{";".join(st)}">{e(fmt(val, cell.number_format or ""))}</td>'
        rows += f'<tr style="height:{h * 1.35:.0f}px"><th class="rn">{r}</th>{tds}</tr>'
    tabbar = "".join(f'<span class="{"on" if t == active else ""}">{e(t)}</span>' for t in tabs)
    return (f'<div class="win"><div class="bar"><i></i><i></i><i></i><b>{e(pathlib.Path(path).name)}</b></div>'
            f'<div class="sheet"><table><tr><th class="rn"></th>{cols}</tr>{rows}</table></div><div class="tabs">{tabbar}</div></div>')

# ---------- page images ----------
from xlview import xl_html  # shared renderer (supports hidden columns: 'A1:AD12;B-X')

def page_png(pdf, n, dpi=110):
    out = TMP / f"{pdf.stem}-{n}"
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), "-singlefile", str(pdf), str(out)], check=True)
    return b64(str(out) + ".png")

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { width: 2000px; height: 1600px; overflow: hidden; font-family: Poppins, sans-serif; color: var(--ink); background: var(--bg); position: relative; }
h1 { font-family: Lora, serif; font-weight: 700; font-size: 96px; line-height: 1.02; letter-spacing: -1px; }
.kick { font-size: 30px; font-weight: 600; letter-spacing: 4px; text-transform: uppercase; color: var(--acc); }
.badges { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 40px; }
.badges span { text-align: center; font-size: 30px; font-weight: 600; padding: 14px 28px; border-radius: 999px; background: var(--main); color: #fff; }
.badges span.alt { background: #fff; color: var(--main); box-shadow: inset 0 0 0 3px var(--main); }
.win { background: #fff; border-radius: 18px; box-shadow: 0 40px 90px -30px rgba(0,0,0,.55); overflow: hidden; display: inline-block; }
.bar { height: 46px; background: #eef1f4; display: flex; align-items: center; gap: 10px; padding: 0 18px; }
.bar i { width: 14px; height: 14px; border-radius: 50%; background: #e05d5d; } .bar i:nth-child(2) { background: #e9b949; } .bar i:nth-child(3) { background: #5cc06a; }
.bar b { margin-left: 18px; font-size: 18px; font-weight: 500; color: #5b6478; }
.sheet table { border-collapse: collapse; font-family: Arial, sans-serif; font-size: 17px; table-layout: fixed; }
.sheet td { padding: 2px 8px; white-space: nowrap; overflow: hidden; border-right: 1px solid #edf0f2; border-bottom: 1px solid #edf0f2; vertical-align: middle; }
.sheet th { background: #f3f5f7; color: #7a8394; font-weight: 500; font-size: 13px; border: 1px solid #e2e6ea; height: 26px; }
.sheet th.rn { width: 40px; }
.tabs { display: flex; gap: 2px; contain: inline-size; overflow: hidden; white-space: nowrap; background: #f3f5f7; padding: 8px 12px 0; border-top: 1px solid #e2e6ea; }
.tabs span { font-family: Arial; font-size: 15px; padding: 8px 16px; color: #5b6478; }
.tabs span.on { background: #fff; color: var(--main); font-weight: 700; border-bottom: 3px solid var(--main); }
.pagecard { position: absolute; background: #fff; box-shadow: 0 30px 60px -20px rgba(0,0,0,.5); }
.pagecard img { display: block; width: 100%; }
.panel { position: absolute; background: #fff; border-radius: 32px; padding: 70px 80px; box-shadow: 0 30px 80px -40px rgba(0,0,0,.4); }
ul.ticks { list-style: none; } ul.ticks li { font-size: 40px; line-height: 1.3; padding: 18px 0 18px 76px; position: relative; border-bottom: 2px dashed rgba(0,0,0,.08); }
ul.ticks li::before { content: ""; position: absolute; left: 0; top: 22px; width: 46px; height: 46px; border-radius: 50%; background: var(--acc); }
ul.ticks li::after { content: ""; position: absolute; left: 15px; top: 31px; width: 12px; height: 22px; border: solid #fff; border-width: 0 6px 6px 0; transform: rotate(45deg); }
.cap { font-family: Lora, serif; font-weight: 700; font-size: 72px; }
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 50px; }
.steps div { background: #fff; border-radius: 30px; padding: 80px 50px 90px; text-align: center; box-shadow: 0 30px 70px -40px rgba(0,0,0,.4); }
.steps b { display: grid; place-items: center; width: 110px; height: 110px; margin: 0 auto 30px; border-radius: 50%; background: var(--acc); color: #fff; font-size: 56px; font-family: Lora, serif; }
.steps h3 { font-size: 56px; font-family: Lora, serif; margin-bottom: 14px; } .steps p { font-size: 38px; color: #5b6478; line-height: 1.35; }
.dots { position: absolute; inset: 0; background: radial-gradient(rgba(0,0,0,.07) 2px, transparent 2.5px) 0 0 / 40px 40px; }
"""

def shot(html_body, theme, path):
    main, acc, bg = theme
    ink = "#1f2a44"
    doc = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>:root{{--main:{main};--acc:{acc};--bg:{bg};--ink:{ink}}}{CSS}</style></head><body><div class="dots"></div>{html_body}</body></html>'
    f = TMP / "m.html"; f.write_text(doc, encoding="utf-8")
    PG.goto(f.as_uri()); PG.wait_for_timeout(150); PG.screenshot(path=str(path))

def fit(inner, maxw, maxh, x, y, rot=0):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{maxw}px;height:{maxh}px;display:flex;align-items:center;justify-content:center;transform:rotate({rot}deg)"><div class="fitme" data-w="{maxw}" data-h="{maxh}">{inner}</div></div>'

FIT_JS = """() => { document.querySelectorAll('.fitme').forEach(el => { const W=+el.dataset.w, H=+el.dataset.h; const r=el.getBoundingClientRect(); const s=Math.min(W/r.width, H/r.height, 3); el.style.transform='scale('+s+')'; }); }"""

def shot_fit(body, theme, path):
    main, acc, bg = theme
    doc = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>:root{{--main:{main};--acc:{acc};--bg:{bg};--ink:#1f2a44}}{CSS}</style></head><body><div class="dots"></div>{body}</body></html>'
    f = TMP / "m.html"; f.write_text(doc, encoding="utf-8")
    PG.goto(f.as_uri()); PG.wait_for_timeout(150); PG.evaluate(FIT_JS); PG.wait_for_timeout(50); PG.screenshot(path=str(path))

def sizes_badges(p):
    if p["kind"] == "xlsx": return '<span>Instant download</span><span class="alt">Excel</span><span class="alt">Google Sheets</span>'
    if p["kind"] == "clipart": return '<span>Commercial use</span><span class="alt">PNG</span><span class="alt">SVG</span>'
    return '<span>Instant download</span><span class="alt">US Letter</span><span class="alt">A4</span>'

def how(p):
    if p["kind"] == "xlsx":
        s = [("1", "Download", "Your file is ready the moment you buy."), ("2", "Open", "In Excel, or upload to Google Drive and open with Google Sheets."), ("3", "Type in yellow", "Your numbers go in the yellow cells. Everything else is calculated.")]
    elif p["kind"] == "clipart":
        s = [("1", "Download", "Get the ZIP files instantly after you buy."), ("2", "Unzip", "Transparent PNGs, scalable SVGs and seamless patterns."), ("3", "Create", "Use them in Canva, Cricut, Procreate and more, for gifts or products you sell.")]
    else:
        s = [("1", "Download", "Get the PDF instantly after you buy."), ("2", "Print", "Print at home at 100% on paper or cardstock, US Letter or A4."), ("3", "Make", "Cut, layer, write and create. Print again whenever you like.")]
    return "".join(f"<div><b>{a}</b><h3>{bb}</h3><p>{c}</p></div>" for a, bb, c in s)

def build(p):
    d = OUT / p["slug"]; d.mkdir(exist_ok=True); th = p["theme"]; imgs = []
    if p["kind"] == "xlsx":
        path = FILES.parent / 'demo' / f'{p["slug"]}.xlsx'; tabs = load_workbook(path).sheetnames
        views = [xl_html(path, s, r, tabs, s) for s, r, _ in p["shots"]]
        views[0] = xl_html(path, p['hero'][0], p['hero'][1], tabs, p['hero'][0])
        hero = (f'<div style="position:absolute;left:110px;top:90px;right:110px;display:flex;justify-content:space-between;align-items:flex-end;gap:40px">'
                f'<div><div class="kick">Spreadsheet template</div><h1 style="margin-top:14px;font-size:84px">{e(p["name"])}</h1>'
                f'<p style="font-size:36px;margin-top:16px;color:#3b4560">{e(p["hook"])}</p></div>'
                f'<div class="badges" style="flex-direction:column;align-items:stretch;margin:0;flex:none">{sizes_badges(p)}</div></div>'
                + fit(views[0], 1780, 1050, 110, 470, 0))
        shot_fit(hero, th, d / "1-hero.png")
        feat = (f'<div class="panel" style="left:90px;top:110px;width:1020px;bottom:110px"><div class="cap" style="margin-bottom:24px">What it does</div>'
                f'<ul class="ticks">{"".join(f"<li>{e(b)}</li>" for b in p["bullets"])}</ul></div>' + fit(xl_html(path, p['feat'][0], p['feat'][1], tabs, p['feat'][0]), 760, 1300, 1170, 150))
        shot_fit(feat, th, d / "2-features.png")
        for i, (s, r, cap) in enumerate(p["shots"][1:3]):
            body = f'<div class="cap" style="position:absolute;left:0;right:0;top:80px;text-align:center">{e(cap)}</div>' + fit(views[1 + i], 1800, 1250, 100, 260)
            shot_fit(body, th, d / f"{3 + i}-detail.png")
    else:
        if p["kind"] == "bundle":
            covers = [page_png(FILES / f"{s}-US-Letter.pdf", 1, 80) for s in ("tea-room-junk-journal-kit", "night-garden-junk-journal-kit", "vintage-ephemera-pack", "journaling-cards-3x4")]
            pages = covers
        else:
            pdf = FILES / p.get("pdf", f'{p["slug"]}-US-Letter.pdf'); pages = [page_png(pdf, n) for n in p["pages"]]
        cards = "".join(f'<div class="pagecard" style="left:{1010 + i * 175}px;top:{190 + (i % 2) * 70}px;width:600px;transform:rotate({[-8, -2, 4, 9][i]}deg)"><img src="{pg}"></div>' for i, pg in enumerate(pages[:4]))
        hero = (f'<div style="position:absolute;left:110px;top:170px;width:760px"><div class="kick">{"Printable bundle" if p["kind"] == "bundle" else "Clipart pack" if p["kind"] == "clipart" else "Printable"}</div><h1 style="margin-top:20px">{e(p["name"])}</h1>'
                f'<p style="font-size:40px;margin-top:30px;line-height:1.35;color:#3b4560">{e(p["hook"])}</p><div class="badges">{sizes_badges(p)}</div></div>{cards}')
        shot(hero, th, d / "1-hero.png")
        grid = "".join(f'<div class="pagecard" style="position:relative;width:100%"><img src="{pg}"></div>' for pg in pages[:6])
        feat = (f'<div class="panel" style="left:90px;top:110px;width:980px;bottom:110px"><div class="cap" style="margin-bottom:24px">What\'s inside</div>'
                f'<ul class="ticks">{"".join(f"<li>{e(b)}</li>" for b in p["bullets"])}</ul></div>'
                f'<div style="position:absolute;left:1140px;top:110px;width:770px;display:grid;grid-template-columns:1fr 1fr;gap:34px">{grid}</div>')
        shot(feat, th, d / "2-features.png")
        if p["kind"] != "bundle":
            for i, pg in enumerate(pages[:2]):
                body = (f'<div class="pagecard" style="left:{560}px;top:90px;width:1100px;transform:rotate({[-2, 2][i]}deg)"><img src="{pg}"></div>'
                        f'<div style="position:absolute;left:110px;top:640px;width:420px" class="cap">{["A closer look", "Made to print"][i]}</div>')
                shot(body, th, d / f"{3 + i}-detail.png")
    body = (f'<div class="cap" style="position:absolute;left:0;right:0;top:150px;text-align:center">How it works</div>'
            f'<div class="steps" style="position:absolute;left:110px;right:110px;top:420px">{how(p)}</div>'
            f'<p style="position:absolute;left:0;right:0;bottom:200px;text-align:center;font-size:38px;color:#5b6478">Digital download · nothing is shipped · {"works on Windows, Mac and Google Sheets" if p["kind"] == "xlsx" else "small business commercial use included" if p["kind"] == "clipart" else "print as many copies as you need for personal use"}</p>')
    shot(body, th, d / "5-how-it-works.png")
    print(p["slug"], len(list(d.glob("*.png"))), "images")

with sync_playwright() as pw:
    B = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    PG = B.new_page(viewport={"width": 2000, "height": 1600})
    only = sys.argv[3:]
    for p in P:
        if not only or p["slug"] in only: build(p)
    B.close()
