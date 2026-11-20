#!/usr/bin/env python3
"""KDP book 2: Purl & Paper Knit & Crochet Project Journal (8.5 x 11 in, black & white, white paper, ~120 pages)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kdp import interior, cover

OUT = pathlib.Path("/home/claude/kdp/project-journal")
OUT.mkdir(parents=True, exist_ok=True)
TW, TH = 8.5, 11
D = json.load(open("/home/claude/etsy-studio/site/assets/data.json"))

CSS = """
* { box-sizing: border-box; }
body { font-family: Poppins, sans-serif; color: #1a1a1a; font-size: 9pt; }
.blank { flex: 1; }
.hd { display:flex; align-items:baseline; justify-content:space-between; margin-bottom: 4pt; }
.hd h2 { font-family: Lora, serif; font-weight: 700; font-size: 22pt; margin: 0; }
.hd span { font-size: 8pt; color: #666; letter-spacing: .08em; text-transform: uppercase; }
.yarn { height: 9pt; margin: 2pt 0 12pt; background: radial-gradient(circle at 4.5pt 4.5pt, #333 2.4pt, transparent 2.9pt) 0 0 / 12pt 9pt space no-repeat; background-repeat: space no-repeat; opacity: .55; }
h3 { font-family: Lora, serif; font-size: 12pt; margin: 10pt 0 5pt; }
p { margin: 0 0 7pt; line-height: 1.5; }
.lab { font-size: 7pt; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #555; }
.f { border-bottom: .8pt solid #999; height: .32in; display:flex; align-items:flex-end; padding-bottom: 2pt; font-size: 7.5pt; color: #555; }
.g2 { display:grid; grid-template-columns: 1fr 1fr; gap: 4pt 16pt; }
.g3 { display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 4pt 14pt; }
.box { border: 1pt solid #333; border-radius: 6pt; padding: 7pt 9pt; }
.lines { flex:1; background: repeating-linear-gradient(transparent 0 .28in, #bbb .28in calc(.28in + .8pt)); }
.dots { flex:1; background: radial-gradient(#999 .8pt, transparent 1pt) 0 0 / .2in .2in; }
.grid { flex:1; background-image: linear-gradient(#bbb .5pt, transparent .5pt), linear-gradient(90deg, #bbb .5pt, transparent .5pt); background-size: .15in .15in; border: .8pt solid #888; }
table { width:100%; border-collapse: collapse; }
th { font-size: 7.5pt; font-weight: 600; text-align:left; padding: 4pt 5pt; border-bottom: 1.5pt solid #1a1a1a; }
td { border-bottom: .8pt solid #ccc; padding: 2pt 5pt; height: .3in; font-size: 8pt; }
.cb { display:inline-flex; align-items:center; gap:4pt; margin-right: 10pt; font-size: 8pt; }
.cb i { width: 9pt; height: 9pt; border: 1.1pt solid #1a1a1a; border-radius: 2pt; }
.counter { display:grid; grid-template-columns: repeat(20, 1fr); gap: 3pt; }
.counter span { aspect-ratio: 1; border: .8pt solid #999; border-radius: 50%; font-size: 5.5pt; display:flex; align-items:center; justify-content:center; color:#888; }
.pn { position:absolute; bottom: .32in; font-size: 7pt; color: #888; }
.swatch { width: 2.2in; height: 2.2in; border: 1pt dashed #555; border-radius: 4pt; }
"""


def hd(t, s=""):
    return f'<div class="hd"><h2>{t}</h2><span>{s}</span></div><div class="yarn"></div>'


def f(t):
    return f'<div class="f">{t}</div>'


def cbs(xs):
    return "".join(f'<span class="cb"><i></i>{x}</span>' for x in xs)


pages = []
pages.append('<div style="flex:1;display:flex;flex-direction:column;justify-content:center;text-align:center">'
             '<div class="yarn" style="width:60%;margin:0 auto 18pt"></div><div style="font-family:Lora;font-size:40pt;font-weight:700;line-height:1">Knit &amp; Crochet<br>Project Journal</div>'
             '<p style="margin-top:14pt;font-size:12pt">Plan it. Track it. Remember every stitch.</p><p style="color:#666">Purl &amp; Paper</p></div>')
pages.append('<div style="margin-top:auto;font-size:7.5pt;color:#444;line-height:1.5"><p><b>Knit &amp; Crochet Project Journal</b> by Purl &amp; Paper</p>'
             '<p>Copyright &copy; 2026 Purl &amp; Paper. All rights reserved. You may copy the log pages for your own personal use.</p>'
             '<p>Yarn weight, needle and hook sizes follow common industry standards and are guides only. Always check your pattern and knit or crochet a gauge swatch.</p>'
             '<p>Free tools: row counter, yarn calculator and gauge converter at purlandpaperco.com</p></div>')
pages.append(hd("This journal belongs to") + f("Name") + f("I started knitting / crocheting in") + f("Favourite yarn") + f("Favourite stitch") +
             '<h3>Projects I dream of making</h3><div class="lines"></div>')
pages.append(hd("How to use this journal") +
             '<p><b>Project pages.</b> Each project gets a two-page spread: the plan, yarn and tools on the left, and progress, notes and a finished-project photo spot on the right. There is room for 40 projects.</p>'
             '<p><b>Reference charts.</b> Yarn weights, needle and hook sizes, and UK/US terms are at the front so the numbers are always to hand.</p>'
             '<p><b>Inventories.</b> Track your yarn stash, your needles and hooks, and patterns you want to try, so you stop buying duplicates.</p>'
             '<p><b>Graph and dot pages.</b> Sketch colourwork, chart a motif or plan a blanket layout at the back.</p>'
             '<h3>Project index</h3><table><tr><th style="width:10%">#</th><th>Project</th><th style="width:22%">Started</th><th style="width:22%">Finished</th></tr>' +
             "".join(f"<tr><td>{i}</td><td></td><td></td><td></td></tr>" for i in range(1, 21)) + "</table>")
pages.append(hd("Project index", "continued") + '<table><tr><th style="width:10%">#</th><th>Project</th><th style="width:22%">Started</th><th style="width:22%">Finished</th></tr>' +
             "".join(f"<tr><td>{i}</td><td></td><td></td><td></td></tr>" for i in range(21, 41)) + "</table>")
# reference: yarn weights
pages.append(hd("Yarn weights", "Reference") + '<table><tr><th>#</th><th>Weight</th><th>Also called</th><th>UK</th><th>Knit gauge (sts/4 in)</th><th>Needles</th><th>Hook</th></tr>' +
             "".join(f"<tr><td>{w['n']}</td><td>{w['name']}</td><td>{w['also']}</td><td>{w['uk']}</td><td>{w['knit']}</td><td>{w['needle']}</td><td>{w['hook']}</td></tr>" for w in D["weights"]) +
             '</table><h3>Good for</h3><table>' + "".join(f"<tr><td style='width:22%'>{w['n']} {w['name']}</td><td>{w['use']}</td></tr>" for w in D["weights"]) + '</table>')
pages.append(hd("Needle &amp; hook sizes", "Reference") + '<table><tr><th>Metric</th><th>US needle</th><th>Old UK / Canada</th><th>US hook</th></tr>' +
             "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in D["sizes"]) + "</table>")
pages.append(hd("UK and US crochet terms", "Reference") + '<table><tr><th>US term</th><th>US abbr.</th><th>UK term</th><th>UK abbr.</th><th>Note</th></tr>' +
             "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in D["terms"]) + "</table>"
             '<p style="margin-top:8pt;font-size:8pt;color:#555">The same name can mean different stitches: a UK double crochet is a US single crochet. Check which terms your pattern uses before you start.</p>'
             '<h3>Notes</h3><div class="lines"></div>')
# ---- extra reference pages (added 20 Nov) ----
KN = [("BO", "bind off"), ("CO", "cast on"), ("k", "knit"), ("p", "purl"), ("k2tog", "knit 2 together (right-leaning decrease)"), ("ssk", "slip, slip, knit (left-leaning decrease)"),
      ("kfb", "knit front and back (increase)"), ("M1L / M1R", "make 1 left / right (increase)"), ("yo", "yarn over"), ("sl", "slip"), ("pm / sm", "place marker / slip marker"),
      ("RS / WS", "right side / wrong side"), ("tbl", "through the back loop"), ("st st", "stockinette stitch"), ("rnd", "round"), ("rep", "repeat"), ("w&amp;t", "wrap and turn (short rows)")]
CR = [("ch", "chain"), ("sl st", "slip stitch"), ("sc", "single crochet (UK dc)"), ("hdc", "half double crochet (UK htr)"), ("dc", "double crochet (UK tr)"), ("tr", "treble crochet (UK dtr)"),
      ("sk", "skip"), ("sp", "space"), ("inc", "increase (2 sts in one)"), ("sc2tog", "single crochet 2 together (decrease)"), ("BLO / FLO", "back loop / front loop only"),
      ("MR", "magic ring"), ("FPdc / BPdc", "front / back post double crochet"), ("yo", "yarn over"), ("st(s)", "stitch(es)"), ("tch", "turning chain"), ("rnd", "round")]
def abbr(rows):
    return '<table><tr><th style="width:28%">Abbr.</th><th>Meaning</th></tr>' + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in rows) + '</table>'
pages.append(hd("Abbreviations", "Reference") + '<div class="g2" style="align-items:start"><div><h3 style="margin-top:0">Knitting</h3>' + abbr(KN) +
             '</div><div><h3 style="margin-top:0">Crochet (US terms)</h3>' + abbr(CR) + '</div></div>'
             '<p style="margin-top:8pt;font-size:8pt;color:#555">Patterns usually list their own abbreviations near the start. When they differ from this page, follow the pattern.</p>')
pages.append(hd("Gauge maths &amp; yarn swaps", "Worksheet") +
             '<h3>From a swatch to stitches per inch</h3><p>Measure 4 in (10 cm) across the middle of your washed swatch and count the stitches. Stitches per inch = stitches in 4 in ÷ 4.</p>'
             '<div class="g3">' + f("Stitches in 4 in") + f("Stitches per inch") + f("Rows per inch") + '</div>'
             '<h3>How many stitches to cast on or chain</h3><p>Stitches = finished width (in) × stitches per inch. Then round to fit the pattern repeat.</p>'
             '<p style="font-size:8.5pt;color:#444"><b>Example:</b> 20 in wide × 4.5 sts per inch = 90 stitches.</p>'
             '<div class="g3">' + f("Width wanted (in)") + f("× stitches per inch") + f("= stitches") + '</div>'
             '<h3>Swapping to a different yarn</h3><p>1. Choose the same weight category and similar fibre. 2. Total yards needed = yards per ball × balls in the pattern. '
             '3. New balls = total yards ÷ yards per ball of your yarn, rounded up. 4. Knit or crochet a swatch: if your gauge matches, the size will match.</p>'
             '<p style="font-size:8.5pt;color:#444"><b>Example:</b> pattern uses 6 balls × 220 yd = 1,320 yd. Your yarn has 190 yd per ball: 1,320 ÷ 190 = 6.95, so buy 7, plus 1 spare.</p>'
             '<table><tr><th>Pattern yarn</th><th>Yd per ball</th><th>Balls</th><th>Total yd</th><th>My yarn</th><th>Yd per ball</th><th>Balls to buy</th></tr>' + ("<tr>" + "<td></td>" * 7 + "</tr>") * 5 + '</table>')
def tub(dots="", hand=False, cross=False):
    inner = (f'<text x="20" y="22" text-anchor="middle" font-size="9" font-family="Poppins">{dots}</text>' if dots else "") + ('<path d="M14,8 q6,-6 12,0" stroke="#111" fill="none" stroke-width="1.6"/>' if hand else "")
    x = '<path d="M4,2 L36,30 M36,2 L4,30" stroke="#111" stroke-width="1.8"/>' if cross else ""
    return f'<svg viewBox="0 0 40 32" width="40" height="32"><path d="M4,8 L8,28 L32,28 L36,8" stroke="#111" fill="none" stroke-width="1.8"/><path d="M4,8 q4,-4 8,0 q4,4 8,0 q4,-4 8,0 q4,4 8,0" stroke="#111" fill="none" stroke-width="1.5"/>{inner}{x}</svg>'
def sq(inner="", cross=False):
    x = '<path d="M4,4 L36,28 M36,4 L4,28" stroke="#111" stroke-width="1.8"/>' if cross else ""
    return f'<svg viewBox="0 0 40 32" width="40" height="32"><rect x="6" y="2" width="28" height="28" fill="none" stroke="#111" stroke-width="1.8"/>{inner}{x}</svg>'
def tri(cross=False):
    x = '<path d="M6,4 L34,30 M34,4 L6,30" stroke="#111" stroke-width="1.8"/>' if cross else ""
    return f'<svg viewBox="0 0 40 32" width="40" height="32"><path d="M20,3 L36,29 L4,29 Z" fill="none" stroke="#111" stroke-width="1.8"/>{x}</svg>'
def iron(dots, cross=False):
    x = '<path d="M4,6 L36,30 M36,6 L4,30" stroke="#111" stroke-width="1.8"/>' if cross else ""
    return f'<svg viewBox="0 0 40 32" width="40" height="32"><path d="M6,26 L34,26 L34,18 Q30,8 16,8 L12,8 Q6,14 6,26 Z" fill="none" stroke="#111" stroke-width="1.8"/><text x="22" y="22" text-anchor="middle" font-size="8">{dots}</text>{x}</svg>'
CARE = [(tub("•"), "Machine wash cold, up to 30 °C"), (tub("••"), "Machine wash warm, up to 40 °C"), (tub(hand=True), "Hand wash only"), (tub(cross=True), "Do not wash"),
        (tri(), "Any bleach allowed"), (tri(True), "Do not bleach"), (sq('<circle cx="20" cy="16" r="10" fill="none" stroke="#111" stroke-width="1.6"/>'), "Tumble dry"),
        (sq('<circle cx="20" cy="16" r="10" fill="none" stroke="#111" stroke-width="1.6"/>', True), "Do not tumble dry"), (sq('<path d="M12,16 L28,16" stroke="#111" stroke-width="1.8"/>'), "Dry flat"),
        (iron("•"), "Iron on low heat"), (iron("", True), "Do not iron"), ('<svg viewBox="0 0 40 32" width="40" height="32"><circle cx="20" cy="16" r="12" fill="none" stroke="#111" stroke-width="1.8"/></svg>', "Dry clean")]
pages.append(hd("Yarn care symbols", "Reference") + '<p>Most ball bands show care symbols. Wool and other animal fibres usually need a hand wash or a wool cycle and drying flat; many acrylics and cottons can go in the machine.</p>'
             '<table><tr><th style="width:16%">Symbol</th><th>Meaning</th><th style="width:16%">Symbol</th><th>Meaning</th></tr>' +
             "".join(f"<tr><td style='height:.55in'>{CARE[i][0]}</td><td>{CARE[i][1]}</td><td>{CARE[i + 1][0]}</td><td>{CARE[i + 1][1]}</td></tr>" for i in range(0, 12, 2)) + '</table>'
             '<p style="margin-top:8pt;font-size:8pt;color:#555">More dots mean a higher temperature. A line under a symbol means a gentler cycle. Always follow the ball band of your yarn.</p>'
             '<h3>Care cards for gifts</h3><p>When you give something handmade, copy its care symbols onto a small card. Keep the ball band in your project pages.</p><div class="lines"></div>')
pages.append(hd("Blocking guide", "Reference") +
             '<p>Blocking evens out stitches, opens up lace and sets the final size. Always test on your swatch first.</p>'
             '<table><tr><th>Method</th><th>How</th><th>Best for</th></tr>'
             '<tr><td><b>Wet blocking</b></td><td>Soak in cool water with a little wool wash for 20 min, press out water in a towel (do not wring), pin to size, dry flat.</td><td>Wool, alpaca, most natural fibres, lace</td></tr>'
             '<tr><td><b>Steam blocking</b></td><td>Pin to size, hold a steam iron just above the fabric without pressing, let it cool and dry before unpinning.</td><td>Wool and blends, quick touch-ups</td></tr>'
             '<tr><td><b>Spray blocking</b></td><td>Pin to size dry, mist with water until damp, leave to dry.</td><td>Delicate fibres, textured stitches, cotton</td></tr></table>'
             '<p style="margin-top:6pt"><b>Acrylic:</b> it will not hold a new shape from water alone. Use gentle steam, keep the iron off the fabric, and test first: too much heat makes acrylic go flat and shiny for good.</p>'
             '<h3>You will need</h3><p>Blocking mats or a folded towel, rust-proof pins, a tape measure, blocking wires for straight edges (optional).</p>'
             '<h3>My blocking notes</h3><table><tr><th>Project</th><th>Fibre</th><th>Method</th><th>Size before → after</th></tr>' + ("<tr>" + "<td></td>" * 4 + "</tr>") * 6 + '</table>')
pages.append(hd("How much yarn?", "Typical ranges") +
             '<p>Rough ranges for planning and shopping. Your pattern, size, stitch and gauge change the real amount, so always check the pattern and buy one extra ball from the same dye lot. Crochet usually uses about a quarter to a third more yarn than knitting.</p>'
             '<table><tr><th>Project</th><th>Yarn weight</th><th>Typical yardage</th></tr>' +
             "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in [
                 ("Adult hat", "Worsted", "150-250 yd"), ("Pair of mittens", "Worsted", "150-250 yd"), ("Pair of adult socks", "Fingering", "350-450 yd"),
                 ("Scarf, 60 in", "Worsted", "300-500 yd"), ("Cowl", "Bulky", "100-200 yd"), ("Shawl", "Fingering", "400-800 yd"),
                 ("Baby blanket", "Worsted", "700-1,000 yd"), ("Throw blanket", "Worsted", "1,200-1,800 yd"), ("Adult sweater (size M)", "Worsted", "1,000-1,500 yd"),
                 ("Baby cardigan", "DK", "300-500 yd"), ("Amigurumi toy, small", "Worsted", "50-150 yd")]) + '</table>'
             '<p style="margin-top:6pt;font-size:8pt;color:#555">These are typical ranges collected from common patterns, not exact figures.</p><h3>My notes</h3><div class="lines"></div>')
pages.append(hd("Handmade gift tracker") + '<table><tr><th>For</th><th>Project</th><th>Occasion</th><th>Start by</th><th>Given</th><th>Care card?</th></tr>' + ("<tr>" + "<td></td>" * 6 + "</tr>") * 24 + '</table>')
pages.append(hd("Ideas for next year") + '<div class="lines"></div>')
pages.append(hd("Year in review") + '<div class="g2">' + f("Projects finished") + f("Yards / metres used") + f("Favourite make") + f("Biggest challenge") + f("New technique learned") + f("Gifts given") + '</div><h3>What I want to make next year</h3><div class="lines"></div>')
# inventories
for t, cols, n in (("Yarn stash", ["Brand &amp; yarn", "Weight", "Colour / dye lot", "Yardage", "Skeins", "Where kept"], 3),
                   ("Needles &amp; hooks", ["Size", "Type (straight / circ / DPN / hook)", "Length", "Material", "Have"], 1),
                   ("Pattern wishlist", ["Pattern", "Designer / source", "Yarn needed", "Priority"], 1)):
    for k in range(n):
        pages.append(hd(t, "Inventory") + '<table><tr>' + "".join(f"<th>{c}</th>" for c in cols) + '</tr>' + ("<tr>" + "<td></td>" * len(cols) + "</tr>") * 26 + '</table>')
# projects
for i in range(1, 41):
    pages.append(hd(f"Project {i}", "Plan") + '<div class="g2">' + f("Project name") + f("For (gift / me / sale)") + f("Pattern &amp; designer") + f("Size I'm making") + '</div>'
                 f'<div style="margin:8pt 0">{cbs(["Knit", "Crochet", "Other"])}</div>'
                 '<div class="g2" style="flex:1"><div class="box"><span class="lab">Yarn</span>' + f("Brand &amp; name") + f("Weight") + f("Colour &amp; dye lot") + f("Amount needed") + f("Amount bought / cost") + f("Second yarn / colour") + f("Where I bought it") + f("Care / washing") +
                 '</div><div class="box"><span class="lab">Tools &amp; gauge</span>' + f("Needle / hook size") + f("Gauge (sts x rows / 4 in)") + f("My swatch gauge") + f("Notions") + f("Start date") + f("Pattern link / book page") + f("Stitches to learn") + f("Deadline") + '</div></div>'
                 '<h3>Modifications</h3><div class="lines" style="flex:.8"></div>')
    pages.append(hd(f"Project {i}", "Progress") + '<span class="lab">Row counter</span><div class="counter" style="margin:4pt 0 10pt">' + "".join(f"<span>{k}</span>" for k in range(1, 101)) + '</div>'
                 '<h3>Notes as I go</h3><div class="lines"></div>'
                 '<div style="display:flex;gap:14pt;margin-top:10pt"><div class="swatch" style="display:flex;align-items:center;justify-content:center"><span class="lab">Yarn snip / photo</span></div>'
                 '<div style="flex:1">' + f("Finished on") + f("Total time") + f("What I'd do differently") + f("Rating: ☆ ☆ ☆ ☆ ☆") + '</div></div>')
for k in range(4):
    pages.append(hd("Graph paper", "Colourwork &amp; charts") + '<div class="grid"></div>')
for k in range(4):
    pages.append(hd("Sketches &amp; ideas") + '<div class="dots"></div>')
while len(pages) % 2:
    pages.append(hd("Notes") + '<div class="lines"></div>')

pages = [p + (f'<span class="pn" style="{"right" if i % 2 == 0 else "left"}:.5in">{i + 1}</span>' if i > 1 else "") for i, p in enumerate(pages)]
n = interior(pages, CSS, TW, TH, OUT / "project-journal-interior.pdf", inside=0.6, outside=0.5, top=0.55, bottom=0.6,
             previews=[(i, OUT / f"int-{i + 1:03d}.png") for i in (13, 14, 96)])
print("interior pages", n)

COVER_CSS = """
.wrap { background: #f4efe6; color: #1f2a44; font-family: Poppins, sans-serif; }
.front, .back { display:flex; flex-direction:column; }
.t { font-family: Lora, serif; font-weight: 700; font-size: 54pt; line-height: .98; margin-top: .9in; }
.t em { font-style: italic; color: #b8326a; }
.s { font-size: 15pt; margin-top: 16pt; max-width: 6in; }
.brand { margin-top: auto; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; font-size: 11pt; color: #2f8f8a; }
.balls { position:absolute; right:.6in; bottom: 1.3in; display:flex; gap: 10pt; }
.blurb { font-size: 11.5pt; line-height: 1.55; margin-top: .7in; }
.feat { margin-top: 14pt; display:grid; gap: 7pt; font-size: 11pt; }
.feat div::before { content:""; display:inline-block; width: 9pt; height: 9pt; border-radius: 50%; background: #b8326a; margin-right: 9pt; }
.spine-t { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; writing-mode: vertical-rl; font-family: Lora, serif; font-weight: 700; font-size: 11pt; color: #1f2a44; white-space: nowrap; }
"""


def ball(c, size, rot):
    strands = "".join(f'<ellipse cx="50" cy="50" rx="{46 - k * 2}" ry="{14 + k * 4}" transform="rotate({k * 23} 50 50)" fill="none" stroke="rgba(255,255,255,.38)" stroke-width="2.2"/>' for k in range(8))
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" style="transform:rotate({rot}deg)"><defs><clipPath id="c{size}"><circle cx="50" cy="50" r="46"/></clipPath></defs>'
            f'<circle cx="50" cy="50" r="46" fill="{c}"/><g clip-path="url(#c{size})">{strands}</g>'
            f'<path d="M50 96 C 60 110, 85 104, 98 118" stroke="{c}" stroke-width="3" fill="none"/></svg>')


front = ('<div class="t">Knit &amp;<br>Crochet<br><em>Project</em><br>Journal</div>'
         '<div class="s">40 project spreads, yarn &amp; hook charts, stash and needle inventories, row counters and graph pages.</div>'
         '<div class="brand">Purl &amp; Paper</div>'
         f'<div class="balls">{ball("#b8326a", 150, -10)}{ball("#2f8f8a", 120, 20)}{ball("#f4a823", 95, 50)}</div>')
back = ('<div class="blurb">Every maker has a pile of half-remembered projects: which hook was that? How many skeins did it take? This journal keeps it all in one place, so your next project goes even better.</div>'
        '<div class="feat"><div>40 two-page project spreads: plan, yarn, gauge, progress and notes</div><div>Row counters on every progress page</div>'
        '<div>Yarn weight, needle and hook size charts, plus UK/US crochet terms</div><div>Yarn stash, needle &amp; hook and pattern wishlist inventories</div>'
        '<div>Graph paper for colourwork and dot pages for sketches</div></div>'
        '<p style="margin-top:auto;font-size:9pt;color:#5b6478">8.5 x 11 in · Free maker tools at purlandpaperco.com</p>')
spine = '<div class="spine-t">Knit &amp; Crochet Project Journal · Purl &amp; Paper</div>'
print(cover(front, back, spine, COVER_CSS, TW, TH, n, OUT / "project-journal-cover.pdf", preview=OUT / "cover.png"))
