"""Styled product scenes: Pinterest pins, Etsy hero images and Gumroad covers.

Each product is photographed (in code) on its own surface: real pages from the
product PDF fanned out with layered shadows, window light, washi tape, a seal
and a paper title label. Spreadsheets sit on a laptop with a sticky note.

Usage:
  python3 tools/scenes.py <pages_dir> <demo_xlsx_dir> <out_dir> [slug ...]
  pages_dir/<slug>/p-NN.png come from: pdftoppm -r 110 -png <slug>-US-Letter.pdf pages/<slug>/p
Outputs per slug: pin-a.png, pin-b.png (1000x1500), etsy-hero.png (2000x1600),
gumroad-cover.png (1280x720), gumroad-thumb.png (600x600)
"""
import base64, glob, html, pathlib, random, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from products import P
from xlview import xl_html, XL_CSS
from openpyxl import load_workbook

e = html.escape
PAGES, DEMO, OUT = map(pathlib.Path, sys.argv[1:4])
ONLY = sys.argv[4:]

NOISE = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(%23n)'/></svg>\")")

# surface, accent, label paper, ink, tape colours, display title, small line, subtitle, seal text, chips
T = {
 "tea-room-junk-journal-kit": dict(surface="linen", base="#d2ae80", acc="#9c4f2e", paper="#fbf5ea", ink="#3b2a1e",
   tape=("#c98b86", "#f3d9d2"), title="The Tea Room", line="Printable junk journal kit",
   sub="Tea-stained papers, recipe cards, menus & botanicals", seal="16 PAGES • PRINT AT HOME • ",
   chips=["Recipe cards", "Tea menu", "Doilies", "Tags & tickets"]),
 "night-garden-junk-journal-kit": dict(surface="velvet", base="#151d3a", acc="#d4b062", paper="#f3ead2", ink="#1d2a4a",
   tape=("#d4b062", "#f1e2b0"), title="Night Garden", line="Printable junk journal kit",
   sub="Moon phases, moths, ferns & star charts", seal="16 PAGES • PRINT AT HOME • ",
   chips=["Moon phases", "Star chart", "Night moths", "Tags & tickets"]),
 "vintage-ephemera-pack": dict(surface="kraft", base="#b48656", acc="#a63d32", paper="#f6eedf", ink="#2b2b2b",
   tape=("#8fb8a8", "#d9ece4"), title="Vintage Ephemera", line="Printable cut-out pack",
   sub="Tickets, tags, labels, stamps & receipts", seal="50+ PIECES • PRINT AT HOME • ",
   chips=["Tickets", "Tags", "Stamps", "Receipts"]),
 "journaling-cards-3x4": dict(surface="linen", base="#e3c2c9", acc="#b8326a", paper="#fff9fa", ink="#22355a",
   tape=("#22355a", "#7d8fb3"), title="Journaling Cards", line="24 printable 3×4 cards",
   sub="Lined, dot grid, grid & botanical in 6 colourways", seal="24 CARDS • PRINT AT HOME • ",
   chips=["Lined", "Dot grid", "Botanical", "Cut guides"]),
 "2027-crochet-knitting-planner": dict(surface="linen", base="#b4c7bd", acc="#2f8f8a", paper="#ffffff", ink="#1f2a44",
   tape=("#f4a823", "#fbe1a6"), title="2027 Crochet & Knitting Planner", line="Printable maker's planner",
   sub="Projects, row counters, yarn stash & gift list", seal="25 PAGES • PRINT AT HOME • ",
   chips=["Year at a glance", "Monthly pages", "Row tracker", "Yarn log"]),
 "junk-journal-mega-bundle": dict(surface="velvet", base="#3f3150", acc="#f4a823", paper="#f6eedf", ink="#3b2f45",
   tape=("#b8326a", "#f0b9cf"), title="Junk Journal Mega Bundle", line="4 printable kits in one",
   sub="Tea Room + Night Garden + Ephemera + 24 cards", seal="45 PAGES • SAVE 30% • ",
   chips=["2 full kits", "Ephemera pack", "24 cards", "US Letter & A4"]),
 "cleaning-business-quote-client-tracker": dict(surface="desk", base="#d7e6e2", acc="#2f8f8a", paper="#ffffff", ink="#163f44",
   tape=("#f4a823", "#fbe1a6"), title="Cleaning Quote Calculator", line="Excel & Google Sheets template",
   sub="Price every job in seconds and track regular clients", seal="EXCEL • GOOGLE SHEETS • ",
   note="Weekly client: $96 a visit", chips=["Quote calculator", "Client list", "Schedule", "Dashboard"]),
 "crochet-knitting-pricing-calculator": dict(surface="desk", base="#efd6e0", acc="#b8326a", paper="#ffffff", ink="#4d1631",
   tape=("#2f8f8a", "#bfe1dd"), title="What Should I Charge?", line="Crochet & knitting pricing calculator",
   sub="Yarn, time, fees and profit worked out for every make", seal="EXCEL • GOOGLE SHEETS • ",
   note="Granny square blanket: $148", chips=["Materials library", "Your hourly rate", "Etsy fees", "Profit"]),
 "home-baker-cost-pricing-calculator": dict(surface="desk", base="#efdfcf", acc="#b5733f", paper="#ffffff", ink="#4a2c18",
   tape=("#b8326a", "#f0b9cf"), title="Price Your Bakes With Confidence", line="Home bakery cost calculator",
   sub="Cost per cake, cookie and loaf, plus a suggested price", seal="EXCEL • GOOGLE SHEETS • ",
   note="Cupcakes: $4.50 each", chips=["Recipe costing", "Ingredient library", "Orders", "Profit"]),
 "yarn-stash-tracker": dict(surface="desk", base="#d9e3f1", acc="#4a73b0", paper="#ffffff", ink="#1d3357",
   tape=("#f4a823", "#fbe1a6"), title="Yarn Stash Tracker", line="Excel & Google Sheets template",
   sub="Know what yarn you have and if it's enough for the next project", seal="EXCEL • GOOGLE SHEETS • ",
   note="Enough for the cardigan? Yes!", chips=["Stash list", "Yards by weight", "Project check", "Wishlist"]),
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:var(--W);height:var(--H);overflow:hidden;position:relative;font-family:Poppins,sans-serif;color:var(--ink);background:var(--base)}
.surface,.light,.shade,.vig,.grain{position:absolute;inset:0;pointer-events:none}
.grain{background-image:NOISE;opacity:.32;mix-blend-mode:multiply}
.s-linen{background:
  repeating-linear-gradient(0deg,rgba(255,255,255,.07) 0 1px,transparent 1px 3px),
  repeating-linear-gradient(90deg,rgba(0,0,0,.05) 0 1px,transparent 1px 4px),var(--base)}
.s-kraft{background:
  repeating-linear-gradient(8deg,rgba(90,50,20,.06) 0 2px,transparent 2px 9px),
  radial-gradient(ellipse at 70% 80%,rgba(80,40,10,.18),transparent 60%),var(--base)}
.s-velvet{background:
  radial-gradient(rgba(240,214,140,.55) 1px,transparent 1.6px) 0 0/97px 89px,
  radial-gradient(rgba(240,214,140,.35) 1px,transparent 1.4px) 31px 47px/61px 71px,
  radial-gradient(ellipse at 50% 30%,rgba(255,255,255,.10),transparent 60%),var(--base)}
.s-desk{background:
  repeating-linear-gradient(90deg,rgba(255,255,255,.12) 0 2px,transparent 2px 160px),
  linear-gradient(180deg,rgba(255,255,255,.35),transparent 40%),var(--base)}
.light{background:radial-gradient(ellipse 70% 55% at 18% 6%,rgba(255,244,220,.55),transparent 70%)}
.shade{background:repeating-linear-gradient(118deg,transparent 0 calc(var(--W)*.16),rgba(20,10,0,.13) calc(var(--W)*.16) calc(var(--W)*.21));
  filter:blur(22px);-webkit-mask-image:linear-gradient(200deg,#000 0%,transparent 55%);mix-blend-mode:multiply}
.vig{background:radial-gradient(ellipse at 50% 45%,transparent 50%,rgba(0,0,0,.32) 100%)}
.pg{position:absolute;background:#fff;
  box-shadow:0 1px 1px rgba(0,0,0,.28),0 8px 14px -4px rgba(0,0,0,.28),0 40px 60px -16px rgba(0,0,0,.42)}
.pg img{display:block;width:100%}
.pg::after{content:"";position:absolute;inset:0;background:linear-gradient(105deg,rgba(255,255,255,.22),transparent 30%,transparent 70%,rgba(0,0,0,.07))}
.tape{position:absolute;opacity:.88;background:repeating-linear-gradient(45deg,var(--t1) 0 10px,var(--t2) 10px 20px);
  box-shadow:0 2px 4px rgba(0,0,0,.12);z-index:30}
.label{position:absolute;background:var(--paper);z-index:20;
  box-shadow:0 2px 2px rgba(0,0,0,.18),0 24px 40px -18px rgba(0,0,0,.45)}
.label::before{content:"";position:absolute;inset:0;background-image:NOISE;opacity:.18;mix-blend-mode:multiply}
.label .ln{font:600 calc(var(--u)*2.6) Poppins;color:var(--acc);letter-spacing:.02em}
.label h1{font:italic 600 calc(var(--u)*var(--tsize)) /1.0 Lora,serif;letter-spacing:-.01em;margin:calc(var(--u)*1.2) 0 calc(var(--u)*1.4)}
.label p{font:400 calc(var(--u)*2.6)/1.35 Poppins;color:color-mix(in srgb,var(--ink) 75%,transparent)}
.rule{height:2px;background:repeating-linear-gradient(90deg,var(--acc) 0 10px,transparent 10px 18px);margin:calc(var(--u)*1.6) 0;opacity:.7}
.seal{position:absolute;z-index:40;filter:drop-shadow(0 10px 14px rgba(0,0,0,.35))}
.brand{position:absolute;z-index:40;font:700 calc(var(--u)*2.6) Poppins;letter-spacing:-.02em;color:var(--paper);
  background:var(--ink);padding:calc(var(--u)*.9) calc(var(--u)*2);border-radius:999px;box-shadow:0 10px 20px -8px rgba(0,0,0,.5)}
.brand i{font-style:normal;color:var(--acc)}
.chips{display:flex;flex-wrap:wrap;gap:calc(var(--u)*1)}
.chips span{font:600 calc(var(--u)*2.2) Poppins;padding:calc(var(--u)*.6) calc(var(--u)*1.6);border-radius:999px;background:var(--acc);color:#fff}
.chips span:nth-child(even){background:transparent;color:var(--ink);box-shadow:inset 0 0 0 2px var(--ink)}
.laptop{position:absolute;z-index:10}
.lid{background:#20242b;border-radius:28px 28px 6px 6px;padding:22px 22px 30px;box-shadow:0 50px 80px -30px rgba(0,0,0,.6)}
.screen{background:#fff;border-radius:6px;overflow:hidden;position:relative}
.screen .win{box-shadow:none;border-radius:0}
.deck{height:26px;margin:0 -60px;background:linear-gradient(#d9dde3,#9aa1ab);border-radius:0 0 30px 30px;position:relative;box-shadow:0 30px 40px -20px rgba(0,0,0,.6)}
.deck::before{content:"";position:absolute;left:50%;top:0;width:180px;height:10px;margin-left:-90px;background:#b7bdc6;border-radius:0 0 10px 10px}
.sticky{position:absolute;z-index:35;background:#ffe27a;padding:calc(var(--u)*2.2);font:italic 600 calc(var(--u)*3.2)/1.15 Lora,serif;color:#3a2f12;
  box-shadow:0 2px 2px rgba(0,0,0,.15),0 26px 30px -14px rgba(0,0,0,.45)}
.sticky::after{content:"";position:absolute;inset:0;background:linear-gradient(160deg,rgba(255,255,255,.35),transparent 40%,rgba(0,0,0,.06))}
.pencil{position:absolute;z-index:34;height:calc(var(--u)*1.6);border-radius:3px;
  background:linear-gradient(90deg,#2b2b2b 0 3%,#f1c27d 3% 9%,#f4a823 9% 92%,#e8a0a0 92% 100%);box-shadow:0 10px 14px -6px rgba(0,0,0,.45)}
""" + XL_CSS
CSS = CSS.replace("NOISE", NOISE)


def b64(p): return "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()


def tape(x, y, w, h, rot):
    rnd = random.Random(int(x * 7 + y * 13))
    left = " ".join(f"{rnd.uniform(0, 4):.1f}% {i * 100 / 6:.0f}%" for i in range(7))
    right = " ".join(f"{100 - rnd.uniform(0, 4):.1f}% {100 - i * 100 / 6:.0f}%" for i in range(7))
    pts = ",".join(p for p in (left + " " + right).split("% ") if p)
    poly = ", ".join(f"{a}% {b}" for a, b in zip(*[iter((left + " " + right).replace('%', '').split())] * 2))
    poly = ", ".join(f"{a}% {b}%" for a, b in zip(*[iter((left + " " + right).replace('%', '').split())] * 2))
    return f'<div class="tape" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);clip-path:polygon({poly})"></div>'


def seal(x, y, d, text, acc, paper, icon="★"):
    r = d / 2
    return (f'<svg class="seal" style="left:{x}px;top:{y}px" width="{d}" height="{d}" viewBox="0 0 {d} {d}">'
            f'<defs><path id="c{x}{y}" d="M {r},{r} m -{r * .72},0 a {r * .72},{r * .72} 0 1,1 {r * 1.44},0 a {r * .72},{r * .72} 0 1,1 -{r * 1.44},0"/></defs>'
            f'<circle cx="{r}" cy="{r}" r="{r - 2}" fill="{acc}"/>'
            f'<circle cx="{r}" cy="{r}" r="{r * .9}" fill="none" stroke="{paper}" stroke-width="2" stroke-dasharray="4 5" opacity=".8"/>'
            f'<circle cx="{r}" cy="{r}" r="{r * .52}" fill="none" stroke="{paper}" stroke-width="2" opacity=".8"/>'
            f'<text font-family="Poppins" font-weight="700" font-size="{d * .085:.1f}" letter-spacing="{d * .012:.1f}" fill="{paper}">'
            f'<textPath href="#c{x}{y}" textLength="{r * 1.44 * 3.1416 * .97:.0f}">{e(text * 2)}</textPath></text>'
            f'<text x="{r}" y="{r + d * .1:.0f}" text-anchor="middle" font-family="Lora" font-style="italic" font-weight="700" font-size="{d * .28:.0f}" fill="{paper}">{icon}</text></svg>')


def pages_for(p):
    if p["kind"] == "bundle":
        out = []
        for s in ("tea-room-junk-journal-kit", "night-garden-junk-journal-kit", "vintage-ephemera-pack", "journaling-cards-3x4"):
            fs = sorted(glob.glob(str(PAGES / s / "*.png")))
            out.append(fs[0])
        extra = sorted(glob.glob(str(PAGES / "night-garden-junk-journal-kit" / "*.png")))
        tea = sorted(glob.glob(str(PAGES / "tea-room-junk-journal-kit" / "*.png")))
        return out + [extra[4], tea[6]]
    fs = sorted(glob.glob(str(PAGES / p["slug"] / "*.png")))
    return [fs[n - 1] for n in p["pages"] if n - 1 < len(fs)]


def fan(imgs, cx, by, pw, spread, angles):
    out = []
    n = len(imgs)
    for i, (src, a) in enumerate(zip(imgs, angles)):
        x = cx - pw / 2 + (i - (n - 1) / 2) * spread
        out.append(f'<div class="pg" style="left:{x:.0f}px;top:{by:.0f}px;width:{pw}px;transform:rotate({a}deg);transform-origin:50% 130%;z-index:{10 + i}"><img src="{b64(src)}"></div>')
    return "".join(out)


def frame(W, H, t, body):
    u = min(W, H) / 100
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>:root{{--W:{W}px;--H:{H}px;--u:{u}px;--base:{t["base"]};--acc:{t["acc"]};'
            f'--paper:{t["paper"]};--ink:{t["ink"]};--t1:{t["tape"][0]};--t2:{t["tape"][1]};--xl:{t["acc"]};--tsize:{t.get("tsize", 9)}}}{CSS}</style></head>'
            f'<body><div class="surface s-{t["surface"]}"></div><div class="grain"></div>{body}'
            f'<div class="shade"></div><div class="light"></div><div class="vig"></div></body></html>')


def label(x, y, w, t, rot=-1.5, chips=False, tsize=None):
    ch = f'<div class="rule"></div><div class="chips">{"".join(f"<span>{e(c)}</span>" for c in t["chips"])}</div>' if chips else ""
    st = f";--tsize:{tsize}" if tsize else ""
    return (f'<div class="label" style="left:{x}px;top:{y}px;width:{w}px;padding:calc(var(--u)*4) calc(var(--u)*4.4);transform:rotate({rot}deg){st}">'
            f'<div class="ln">{e(t["line"])}</div><h1>{e(t["title"])}</h1><p>{e(t["sub"])}</p>{ch}</div>')


def brand(x, y): return f'<div class="brand" style="left:{x}px;top:{y}px">Purl <i>&amp;</i> Paper</div>'


def laptop(p, t, x, y, w, sheet=None):
    path = DEMO / f'{p["slug"]}.xlsx'
    tabs = load_workbook(path).sheetnames
    s, r = sheet or p["hero"]
    win = xl_html(path, s, r, tabs, s)
    sw = w - 44
    sh = sw * 0.62
    return (f'<div class="laptop" style="left:{x}px;top:{y}px;width:{w}px"><div class="lid"><div class="screen" style="height:{sh:.0f}px">'
            f'<div class="fitme" data-w="{sw}" data-h="{sh:.0f}" style="transform-origin:0 0;display:inline-block">{win}</div></div></div><div class="deck"></div></div>')


FIT = """() => document.querySelectorAll('.fitme').forEach(el => { const W=+el.dataset.w,H=+el.dataset.h;
 const r=el.getBoundingClientRect(); const s=Math.max(W/r.width, H/r.height); el.style.transform='scale('+s+')'; })"""


def scenes(p):
    t = T[p["slug"]]
    xl = p["kind"] == "xlsx"
    out = {}
    random.seed(p["slug"])
    if not xl:
        imgs = pages_for(p)
        # Pin A: fan of pages under a title label
        tl = len(t["title"]) > 18
        body = (label(70, 80, 860, t, -1.2, tsize=8 if tl else 10.5) + tape(120, 60, 170, 46, -8) + tape(730, 66, 160, 46, 6)
                + fan(imgs[:5], 500, 560 if tl else 500, 500, 78, [-12, -6, 0, 6, 12])
                + seal(740, 1190, 210, t["seal"], t["acc"], t["paper"]) + brand(70, 1390))
        out["pin-a"] = (1000, 1500, body)
        # Pin B: pages tossed on the surface + what's inside label at bottom
        pos = [(40, 70, -6), (520, 40, 5), (60, 520, 4), (540, 470, -5)]
        tossed = "".join(f'<div class="pg" style="left:{x}px;top:{y}px;width:430px;transform:rotate({a}deg);z-index:{10 + i}"><img src="{b64(imgs[(i + 1) % len(imgs)])}"></div>'
                         for i, (x, y, a) in enumerate(pos))
        tossed += tape(220, 50, 150, 40, -12) + tape(690, 30, 150, 40, 9)
        body = (tossed + label(60, 980, 880, t, 1.2, chips=True, tsize=7.2 if tl else 9)
                + seal(780, 870, 180, t["seal"], t["acc"], t["paper"]) + brand(70, 1410))
        out["pin-b"] = (1000, 1500, body)
        # Etsy hero 2000x1600: label left, wide fan right
        body = (label(110, 380, 820, t, -1.5, chips=True, tsize=6.4 if tl else 7.6) + tape(160, 360, 170, 46, -8) + tape(760, 365, 150, 46, 7)
                + fan(imgs[:5], 1390, 300, 600, 95, [-12, -6, 0, 6, 12])
                + seal(1680, 1180, 260, t["seal"], t["acc"], t["paper"]) + brand(110, 1420))
        out["etsy-hero"] = (2000, 1600, body)
        # Gumroad cover 1280x720
        body = (label(60, 110, 560, t, -1.5, tsize=6.6 if tl else 8.4) + tape(90, 92, 120, 34, -8)
                + fan(imgs[:5], 920, 120, 340, 80, [-13, -6, 0, 6, 13])
                + seal(1100, 520, 150, t["seal"], t["acc"], t["paper"]) + brand(60, 610))
        out["gumroad-cover"] = (1280, 720, body)
        # Thumb 600x600
        body = (fan(imgs[:3], 300, 150, 270, 90, [-9, 0, 9])
                + f'<div class="label" style="left:40px;top:420px;width:520px;padding:18px 26px;transform:rotate(-1.5deg)"><h1 style="font:italic 600 {40 if tl else 50}px/1 Lora,serif">{e(t["title"])}</h1></div>'
                + tape(70, 405, 100, 28, -8) + seal(440, 40, 130, t["seal"], t["acc"], t["paper"]))
        out["gumroad-thumb"] = (600, 600, body)
    else:
        note = f'<div class="sticky" style="--u:10px;left:{{x}}px;top:{{y}}px;width:{{w}}px;transform:rotate({{r}}deg)">{e(t["note"])}</div>'
        body = (label(70, 70, 860, t, -1.2, tsize=8.5) + tape(130, 50, 170, 46, -8) + tape(720, 56, 160, 46, 6)
                + laptop(p, t, 40, 560, 920) + note.format(x=640, y=1030, w=300, r=6)
                + f'<div class="pencil" style="left:120px;top:1250px;width:480px;transform:rotate(-8deg)"></div>'
                + seal(780, 1220, 190, t["seal"], t["acc"], t["paper"], "✓") + brand(70, 1400))
        out["pin-a"] = (1000, 1500, body)
        s2 = p["shots"][1][:2]
        body = (laptop(p, t, 80, 80, 840, s2) + note.format(x=600, y=520, w=320, r=-5)
                + label(60, 820, 880, t, 1.2, chips=True, tsize=7.6) + seal(790, 740, 170, t["seal"], t["acc"], t["paper"], "✓") + brand(70, 1410))
        out["pin-b"] = (1000, 1500, body)
        body = (label(110, 330, 780, t, -1.5, chips=True, tsize=6.6) + tape(160, 310, 170, 46, -8)
                + laptop(p, t, 930, 380, 1010) + note.format(x=1560, y=1050, w=330, r=5)
                + f'<div class="pencil" style="left:1000px;top:1330px;width:520px;transform:rotate(-6deg)"></div>'
                + seal(1720, 200, 230, t["seal"], t["acc"], t["paper"], "✓") + brand(110, 1420))
        out["etsy-hero"] = (2000, 1600, body)
        body = (label(50, 90, 560, t, -1.5, tsize=6) + laptop(p, t, 660, 90, 560)
                + note.format(x=1010, y=470, w=230, r=5).replace("--u:10px", "--u:7px") + brand(50, 610))
        out["gumroad-cover"] = (1280, 720, body)
        body = (laptop(p, t, 50, 40, 500)
                + f'<div class="label" style="left:40px;top:430px;width:520px;padding:18px 26px;transform:rotate(-1.5deg)"><h1 style="font:italic 600 40px/1.05 Lora,serif">{e(t["title"])}</h1></div>'
                + tape(70, 415, 100, 28, -8))
        out["gumroad-thumb"] = (600, 600, body)
    return t, out


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for p in P:
            if ONLY and p["slug"] not in ONLY:
                continue
            t, sc = scenes(p)
            d = OUT / p["slug"]; d.mkdir(parents=True, exist_ok=True)
            for name, (W, H, body) in sc.items():
                pg = b.new_page(viewport={"width": W, "height": H})
                f = d / "_scene.html"; f.write_text(frame(W, H, t, body), encoding="utf-8")
                pg.goto(f.as_uri()); pg.wait_for_timeout(200); pg.evaluate(FIT); pg.wait_for_timeout(80)
                pg.screenshot(path=str(d / f"{name}.png")); pg.close()
            (d / "_scene.html").unlink()
            print(p["slug"], "ok")
        b.close()


if __name__ == "__main__":
    main()
