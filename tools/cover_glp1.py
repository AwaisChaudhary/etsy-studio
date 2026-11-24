"""Dose by Dose: full-wrap cover (6x9, white paper). Original art: a 26-segment progress ring (one segment per week)
that fills from coral to deep teal, with a sprouting leaf in the middle. Light, clean, 'wellness' look. Barcode zone kept empty."""
import base64, math, pathlib, subprocess, tempfile
from kdp import cover

OUT = pathlib.Path("/home/claude/kdp/glp1")
TW, TH = 6, 9
PAGES = int((OUT / "pages.txt").read_text())
INK, TEAL, SAGE, CORAL, CREAM = "#163a3a", "#1f6f6b", "#9cc5b4", "#ef8f6b", "#fbf6ee"


def page_png(n, dpi=120):
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), str(OUT / "interior.pdf"), str(tmp / "p")], check=True, stderr=subprocess.DEVNULL)
    return "data:image/png;base64," + base64.b64encode(next(tmp.glob("p-*.png")).read_bytes()).decode()


def mix(a, b, t):
    a = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def ring_svg(size=420, filled=19):
    cx = cy = size / 2
    R, r = 190, 150
    segs = []
    n = 26
    for i in range(n):
        a0 = -math.pi / 2 + i * 2 * math.pi / n + 0.035
        a1 = -math.pi / 2 + (i + 1) * 2 * math.pi / n - 0.035
        p = [(cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1)),
             (cx + r * math.cos(a1), cy + r * math.sin(a1)), (cx + r * math.cos(a0), cy + r * math.sin(a0))]
        d = f"M{p[0][0]:.1f} {p[0][1]:.1f} A{R} {R} 0 0 1 {p[1][0]:.1f} {p[1][1]:.1f} L{p[2][0]:.1f} {p[2][1]:.1f} A{r} {r} 0 0 0 {p[3][0]:.1f} {p[3][1]:.1f}Z"
        fill = mix(CORAL, TEAL, i / (filled - 1)) if i < filled else "none"
        stroke = "none" if i < filled else SAGE
        segs.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    leaf = (f'<g transform="translate({cx} {cy + 70})" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M0 0 C0 -60 0 -110 0 -150"/>'
            f'<path d="M0 -60 C-50 -70 -80 -110 -78 -150 C-30 -140 -4 -110 0 -60Z" fill="{SAGE}"/>'
            f'<path d="M0 -95 C44 -100 74 -140 72 -175 C30 -168 4 -140 0 -95Z" fill="{TEAL}" stroke="{INK}"/>'
            '<path d="M-36 0 H36"/></g>')
    return f'<svg viewBox="0 0 {size} {size}" width="100%" xmlns="http://www.w3.org/2000/svg">{"".join(segs)}{leaf}</svg>'


CSS = f"""
body {{ font-family: Inter, sans-serif; }}
.wrap {{ background: {CREAM}; color: {INK}; }}
.front, .back {{ display:flex; flex-direction:column; }}
.kick {{ font-size: 8.6pt; font-weight: 700; letter-spacing: .24em; color: {TEAL}; text-align:center; }}
.t {{ font-family: 'GFS Baskerville', serif; font-size: 56pt; line-height: 1; text-align:center; margin-top: 8pt; color: {INK}; }}
.s {{ font-family: 'Bitstream Charter', serif; font-style: italic; font-size: 14pt; text-align:center; margin-top: 6pt; color: {TEAL}; }}
.art {{ width: 3.7in; margin: 16pt auto 0; }}
.chips {{ display:flex; justify-content:center; gap: 6pt; margin-top: 16pt; flex-wrap: wrap; }}
.chips span {{ font-size: 7.8pt; font-weight: 600; border-radius: 20pt; padding: 3.5pt 9pt; background: {TEAL}; color: #fff; }}
.chips span.o {{ background: {CORAL}; }}
.brand {{ margin-top: auto; text-align:center; font-size: 7.6pt; letter-spacing:.24em; color:{TEAL}; }}
.spine {{ background: {TEAL}; display:flex; align-items:center; justify-content:center; }}
.spine div {{ transform: rotate(90deg); white-space: nowrap; font-family:'GFS Baskerville', serif; font-size: 7.6pt; color:#fff; }}
.spine div b {{ font-family: Inter, sans-serif; color:#ffd9c7; font-weight:700; margin-left: 8pt; font-size: 5.4pt; letter-spacing:.14em; }}
.back h3 {{ font-family: 'GFS Baskerville', serif; font-weight: normal; font-size: 20pt; margin: 0 0 8pt; color: {INK}; }}
.back p {{ font-size: 9.3pt; line-height: 1.5; margin: 0 0 8pt; }}
.back ul {{ margin: 4pt 0 0; padding-left: 13pt; font-size: 8.8pt; line-height: 1.55; }}
.thumb {{ width: 1.85in; border: 3pt solid #fff; box-shadow: 0 6pt 16pt rgba(22,58,58,.25); transform: rotate(-3deg); margin: 8pt 0 0 6pt; background:#fff; }}
.row {{ display:flex; gap: 16pt; align-items:flex-start; }}
.barcode {{ position:absolute; right: 0.5in; bottom: 0.5in; width: 2in; height: 1.2in; }}
.note {{ font-size: 7.2pt; margin-top: auto; max-width: 2.7in; line-height:1.4; color:{TEAL}; }}
.back {{ border-top: 6pt solid {CORAL}; }}
"""

front = ('<div class="kick">GLP-1 WEIGHT LOSS JOURNAL</div><div class="t">Dose by Dose</div><div class="s">Your first six months, week by week</div>'
         f'<div class="art">{ring_svg()}</div>'
         '<div class="chips"><span>Shots or pills</span><span class="o">Side-effect tracker</span><span>Protein, water and food log</span></div>'
         '<div class="brand">STEADY GROUND PRESS</div>')

back = ('<h3>Every dose, every week, one place</h3>'
        '<p>Dose by Dose keeps the first six months of your GLP-1 medication organised: what you took and where, how your body reacted, what you ate, and how far you have come. Bring it to appointments and answer your doctor\'s questions in seconds.</p>'
        f'<div class="row"><img class="thumb" src="{page_png(8)}"><ul>'
        '<li>26 weekly check-ins: dose, site, weigh-in, measurements</li><li>Side-effect grid: rate 10 common symptoms 0-3 each day</li>'
        '<li>Daily protein, water, fibre, movement and sleep</li><li>7-day food log with protein per day</li><li>Monthly progress: weight graph, photos, measurements</li>'
        '<li>Injection site rotation map and titration planner</li><li>Doctor visit pages, symptom log, protein-first food ideas</li><li>Works for weekly shots or daily pills</li></ul></div>'
        f'<p style="margin-top:10pt">6 x 9 in, {PAGES} pages, matte cover.</p>'
        '<div class="note">A tracking journal only, not medical advice. Always follow your care team\'s instructions. Not connected with any drug maker.</div><div class="barcode"></div>')

spine = '<div>Dose by Dose <b>GLP-1 WEIGHT LOSS JOURNAL</b></div>'

if __name__ == "__main__":
    print(cover(front, back, spine, CSS, TW, TH, PAGES, OUT / "cover.pdf", preview=OUT / "cover.png"))
