#!/usr/bin/env python3
"""Builds the free email-signup downloads for each site (printable PDFs).
Run: python3 work/freebies.py   (needs /usr/bin/google-chrome and pypdf)"""
import asyncio, html, json, pathlib, subprocess, calendar
from playwright.async_api import async_playwright
from pypdf import PdfReader, PdfWriter

H = pathlib.Path("/home/claude")
E = html.escape


def load_nc():
    out = subprocess.run(["node", "-e", 'global.window={};require("/home/claude/repo/assets/data.js");'
                          'process.stdout.write(JSON.stringify(window.SITE))'], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


BASE_CSS = """
* { box-sizing: border-box; }
body { font-family: "Segoe UI", Arial, sans-serif; color: #1b1b24; font-size: 10pt; margin: 0; }
h1 { font-size: 26pt; margin: 0 0 4px; line-height: 1.05; }
h2 { font-size: 13pt; margin: 18px 0 6px; padding-bottom: 4px; border-bottom: 2px solid var(--acc); break-after: avoid; }
.sub { color: #555; margin: 0 0 12px; }
.cols { columns: 2; column-gap: 18px; }
.row { display: flex; gap: 7px; align-items: flex-start; padding: 3px 0; break-inside: avoid; border-bottom: 1px dotted #ccc; }
.box { width: 11px; height: 11px; border: 1.4px solid #333; border-radius: 2px; flex: none; margin-top: 2px; }
.small { color: #666; font-size: 8.4pt; }
.tag { font-size: 7.6pt; padding: 1px 5px; border-radius: 8px; background: #eee; margin-left: 4px; }
.foot { margin-top: 16px; font-size: 8pt; color: #777; border-top: 1px solid #ddd; padding-top: 6px; }
.band { height: 10px; background: var(--band); margin: 0 0 14px; border-radius: 5px; }
"""


def doc(css_vars, body, extra_css=""):
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>:root{{{css_vars}}}{BASE_CSS}{extra_css}</style></head><body><div class='band'></div>{body}</body></html>"


def neoncoast():
    S = load_nc()
    parts = ["<h1>GTA 6 100% Checklist</h1>",
             f"<p class='sub'>Every story mission, trophy and completion goal from NeonCoast, ready to tick off. Updated {E(S['updated'])}. Live version and map: neoncoast.org</p>"]
    parts.append("<h2>Completion goals</h2><div class='cols'>")
    for sec in S["completion"]:
        parts.append(f"<p style='margin:6px 0 2px;font-weight:700'>{E(sec['section'])}</p>")
        for it in sec["items"]:
            parts.append(f"<div class='row'><span class='box'></span><span>{E(it['name'])} <span class='small'>({E(str(it['need']))} &middot; {E(it['what'])})</span></span></div>")
    parts.append("</div><h2>Story missions</h2><div class='cols'>")
    ch = None
    for m in S["missions"]:
        if m.get("chapter") != ch:
            ch = m.get("chapter")
            parts.append(f"<p style='margin:6px 0 2px;font-weight:700'>Chapter {E(str(ch))}</p>")
        parts.append(f"<div class='row'><span class='box'></span><span>{E(m['name'])}<span class='tag'>{E(m.get('character') or '')}</span></span></div>")
    parts.append("</div><h2>Trophies</h2><div class='cols'>")
    for t in S["trophies"]:
        name = "Hidden trophy (spoiler)" if t.get("spoiler") else t["name"]
        how = "" if t.get("spoiler") else t.get("how", "")
        parts.append(f"<div class='row'><span class='box'></span><span><b>{E(name)}</b> <span class='tag'>{E(t['tier'])}</span><br><span class='small'>{E(how)}</span></span></div>")
    parts.append("</div><p class='foot'>NeonCoast is an unofficial fan site, not linked to Rockstar Games or Take-Two Interactive. Lists grow as facts are confirmed; get the latest at neoncoast.org/completion.</p>")
    return doc("--acc:#ff3d8b;--band:linear-gradient(90deg,#ffe3b3,#ff8a3d,#ff3d8b,#2de2e6)", "".join(parts))


def dayonedrop():
    g = json.load(open(H / "dayonedrop/assets/games.json"))
    games = sorted(g["games"], key=lambda x: (x.get("month") or 13, x.get("date") or "9999"))
    parts = ["<h1>2027 Game Release Calendar</h1>",
             f"<p class='sub'>Every 2027 release DayOneDrop is tracking, month by month. Checked {E(g['updated'])}. Dates move: see the live board at getdayonedrop.com</p><div class='cols'>"]
    cur = None
    for x in games:
        m = x.get("month")
        label = calendar.month_name[m] if m else "Date to be announced"
        if label != cur:
            cur = label
            parts.append(f"<h2 style='column-span:none'>{E(label)} 2027</h2>" if m else f"<h2>{E(label)}</h2>")
        when = x["date"][8:10].lstrip("0") if x.get("status") == "dated" and x.get("date") else (x.get("window") or "TBA")
        status = " &middot; delayed" if x.get("status") == "delayed" else ""
        plats = ", ".join(x.get("platforms") or [])
        parts.append(f"<div class='row'><span class='box'></span><span><b>{E(x['title'])}</b> <span class='tag'>{E(str(when))}{status}</span><br><span class='small'>{E(plats)}</span></span></div>")
    parts.append("</div><p class='foot'>Tick the games you plan to buy. DayOneDrop is an independent release tracker, not linked to any publisher.</p>")
    return doc("--acc:#ffc629;--band:repeating-linear-gradient(90deg,#0c0d10 0 22px,#ffc629 22px 26px)", "".join(parts))


def padel():
    card = lambda t, b: f"<div class='card'><h3>{t}</h3><p>{b}</p></div>"
    body = "<h1>Padel Rules Cheat Sheet</h1><p class='sub'>The rules you need on court, on one page. From padelglassbox.com</p><div class='grid'>" + "".join([
        card("The serve", "Stand behind the service line, bounce the ball and hit it underhand, at or below waist height, into the box diagonally opposite. Two attempts per point."),
        card("Serve faults", "It lands outside the diagonal box, it is hit above the waist, you miss the ball, or after bouncing in the box it hits the metal mesh."),
        card("Receiving", "Let the serve bounce first. After that, volley freely."),
        card("The walls", "On your side the ball may bounce once and then hit the walls; still in play. You can also hit into your own walls to get it back over the net."),
        card("You lose the point if", "The ball bounces twice, your shot hits the opponents' wall or fence before their ground, or the ball touches your body."),
        card("Scoring", "15, 30, 40, game. Sets to six games, tie-break at 6-6: first to 7 points with a two-point lead."),
        card("At 40-40", "<b>Advantage:</b> win two in a row.<br><b>Golden point:</b> one point decides; the receiving pair picks who receives.<br><b>Star Point (pro tours from 2026):</b> advantage twice, then one deciding point at the third deuce."),
        card("Court", "20 m long, 10 m wide. Service lines 6.95 m from the net. Net 88 cm in the middle, 92 cm at the posts."),
    ]) + "</div><p class='foot'>Agree the deuce format before the first serve. Free score keeper, draw maker and level calculator at padelglassbox.com</p>"
    css = ".grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.card{border:1.5px solid #c9d6ee;border-radius:10px;padding:10px 12px;break-inside:avoid}.card h3{margin:0 0 6px;color:#1e46c8;font-size:15pt}.card p{margin:0;line-height:1.5;font-size:12pt}.card{padding:16px 16px}.grid{gap:14px}"
    return doc("--acc:#1e46c8;--band:linear-gradient(90deg,#1e46c8,#e8f84a)", body, css)


async def render(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for html_doc, out in jobs:
            pg = await b.new_page()
            await pg.set_content(html_doc, wait_until="load")
            out.parent.mkdir(parents=True, exist_ok=True)
            await pg.pdf(path=str(out), format="Letter", print_background=True,
                         margin={"top": "14mm", "bottom": "14mm", "left": "13mm", "right": "13mm"})
            print(out, out.stat().st_size // 1024, "KB")
        await b.close()


def purl_sampler(out):
    """Free sampler: a few pages from our own printables (our original artwork) plus a link page."""
    w = PdfWriter()
    picks = [("journaling-cards-3x4", [0, 1]), ("vintage-ephemera-pack", [0]), ("2027-crochet-knitting-planner", [2])]
    for slug, idx in picks:
        r = PdfReader(str(H / f"etsy/batch1/files/{slug}-US-Letter.pdf"))
        for i in idx:
            if i < len(r.pages):
                w.add_page(r.pages[i])
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        w.write(f)
    print(out, out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    asyncio.run(render([
        (neoncoast(), H / "repo/assets/free/gta-6-100-percent-checklist.pdf"),
        (dayonedrop(), H / "dayonedrop/assets/free/2027-game-release-calendar.pdf"),
        (padel(), H / "padelglassbox/assets/free/padel-rules-cheat-sheet.pdf"),
    ]))
    purl_sampler(H / "etsy-studio/site/assets/free/purl-and-paper-free-sampler.pdf")
