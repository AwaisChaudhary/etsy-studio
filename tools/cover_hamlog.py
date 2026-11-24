"""Good Copy: full-wrap cover (8.5x11, white paper). Original art: a receiver panadapter. Amber spectrum trace with signal peaks
over a waterfall of signal streaks on a night-blue ground. No organisation logos (a competitor got 1-star reviews for an ARRL look-alike)."""
import base64, math, pathlib, random, subprocess, tempfile
from kdp import cover

OUT = pathlib.Path("/home/claude/kdp/hamlog")
PAGES = int((OUT / "pages.txt").read_text())
NAVY, DEEP, AMBER, CREAM, CYAN = "#0f2340", "#0a1830", "#f2a93b", "#f6efe1", "#6fc3d6"


def page_png(n, dpi=110):
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), str(OUT / "interior.pdf"), str(tmp / "p")], check=True, stderr=subprocess.DEVNULL)
    return "data:image/png;base64," + base64.b64encode(next(tmp.glob("p-*.png")).read_bytes()).decode()


def panadapter(w=600, h=430):
    rnd = random.Random(7)
    peaks = [(80, 46, 7), (148, 70, 5), (205, 30, 6), (290, 120, 9), (352, 52, 5), (430, 88, 7), (500, 38, 5), (548, 60, 6)]
    top = 150
    pts = []
    for x in range(0, w + 1, 3):
        y = top - 12 - rnd.random() * 9
        for px, ph, pw in peaks:
            y -= ph * math.exp(-((x - px) / pw) ** 2)
        pts.append(f"{x},{y:.1f}")
    trace = " ".join(pts)
    fill = f"0,{top} " + trace + f" {w},{top}"
    grid = "".join(f'<line x1="{x}" y1="10" x2="{x}" y2="{top}" stroke="{CYAN}" stroke-opacity=".14"/>' for x in range(0, w + 1, 60))
    grid += "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{CYAN}" stroke-opacity=".14"/>' for y in range(10, top + 1, 35))
    fall = []
    for px, ph, pw in peaks:
        y = top + 6
        while y < h:
            seg = rnd.randint(8, 34)
            if rnd.random() < .78:
                op = .35 + .6 * (ph / 120) * rnd.random() + .1
                fall.append(f'<rect x="{px - pw * .8:.1f}" y="{y}" width="{pw * 1.6:.1f}" height="{seg}" fill="{AMBER}" opacity="{min(op, .95):.2f}"/>')
            y += seg + rnd.randint(2, 14)
    noise = "".join(f'<rect x="{rnd.randint(0, w)}" y="{rnd.randint(top + 6, h)}" width="2" height="{rnd.randint(2, 7)}" fill="{CYAN}" opacity="{rnd.random() * .35:.2f}"/>' for _ in range(420))
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity=".55"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{DEEP}" stop-opacity="0"/><stop offset="1" stop-color="{NAVY}" stop-opacity="1"/></linearGradient></defs>'
            f'<rect x="0" y="{top + 4}" width="{w}" height="{h - top}" fill="{DEEP}"/>{noise}{"".join(fall)}<rect x="0" y="{top + 4}" width="{w}" height="{h - top}" fill="url(#f)"/>'
            f'{grid}<polygon points="{fill}" fill="url(#g)"/><polyline points="{trace}" fill="none" stroke="{AMBER}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<line x1="290" y1="6" x2="290" y2="{h}" stroke="{CREAM}" stroke-width="1.2" stroke-dasharray="4 4" opacity=".7"/>'
            f'<text x="298" y="22" font-family="Inter" font-size="13" font-weight="700" fill="{CREAM}">14.074</text></svg>')


CSS = f"""
body {{ font-family: Inter, sans-serif; }}
.wrap {{ background: {NAVY}; color: {CREAM}; }}
.front, .back {{ display:flex; flex-direction:column; }}
.kick {{ font-size: 10pt; font-weight:700; letter-spacing:.26em; color:{AMBER}; }}
.t {{ font-family:'GFS Baskerville', serif; font-size: 84pt; line-height:.95; margin-top: 10pt; }}
.s {{ font-family:'Bitstream Charter', serif; font-style:italic; font-size: 19pt; margin-top: 8pt; color:{CREAM}; opacity:.9; }}
.art {{ margin: 26pt -0.1in 0; }}
.facts {{ display:flex; gap: 0; margin-top: 18pt; border-top: 1pt solid rgba(246,239,225,.35); }}
.facts div {{ flex:1; padding: 9pt 10pt 0 0; font-size: 9pt; line-height:1.35; }}
.facts b {{ display:block; font-family:'GFS Baskerville', serif; font-size: 25pt; font-weight:normal; color:{AMBER}; line-height:1; }}
.brand {{ margin-top:auto; font-size: 8pt; letter-spacing:.26em; opacity:.75; }}
.spine {{ background:{DEEP}; display:flex; align-items:center; justify-content:center; }}
.spine div {{ transform: rotate(90deg); white-space:nowrap; font-family:'GFS Baskerville', serif; font-size: 9pt; color:{CREAM}; }}
.spine div b {{ font-family: Inter, sans-serif; color:{AMBER}; font-size: 6pt; letter-spacing:.14em; margin-left: 9pt; }}
.back h3 {{ font-family:'GFS Baskerville', serif; font-weight:normal; font-size: 26pt; margin:0 0 10pt; }}
.back p {{ font-size: 10.5pt; line-height:1.55; margin:0 0 9pt; opacity:.95; }}
.back ul {{ font-size: 10pt; line-height:1.6; padding-left: 14pt; margin: 0; }}
.back li::marker {{ color:{AMBER}; }}
.thumb {{ width: 2.6in; border: 4pt solid #fff; transform: rotate(-2.5deg); box-shadow: 0 8pt 22pt rgba(0,0,0,.45); background:#fff; }}
.row {{ display:flex; gap: 20pt; align-items:flex-start; margin-top: 6pt; }}
.barcode {{ position:absolute; right:.5in; bottom:.5in; width:2in; height:1.2in; }}
.note {{ margin-top:auto; font-size: 8pt; opacity:.7; max-width: 3.6in; }}
"""

front = ('<div class="kick">AMATEUR RADIO LOGBOOK</div><div class="t">Good Copy</div><div class="s">The roomy logbook for hams who write things down</div>'
         f'<div class="art">{panadapter()}</div>'
         '<div class="facts"><div><b>1,320</b>contacts on tall, easy-to-write rows</div><div><b>Wide</b>Name and QTH/grid columns, one RST each way</div><div><b>POTA</b>SOTA, contest and net logs, WAS and DXCC</div></div>'
         '<div class="brand">STEADY GROUND PRESS</div>')
back = ('<h3>A log with room to write</h3>'
        '<p>Most logbooks squeeze tiny rows and waste space on columns you never fill. Good Copy gives every contact a tall row, puts the width where you need it, Name and QTH/grid, and writes rig, power and antenna once per page instead of on every line.</p>'
        f'<div class="row"><img class="thumb" src="{page_png(7)}"><ul>'
        '<li>60 log pages, 1,320 contacts</li><li>UTC, frequency/band, mode, call, RST sent and rcvd</li><li>QSL sent / received tick boxes</li><li>Extra-wide inner margin: no writing into the spine</li>'
        '<li>6 POTA/SOTA activation logs</li><li>Contest and net logs</li><li>Worked All States, DXCC and grid-square trackers</li><li>QSL card log, station and antenna records</li><li>Band edges, FT8 and calling frequencies, phonetics, Q-codes, RST, UTC</li></ul></div>'
        f'<p style="margin-top:12pt">8.5 x 11 in, {PAGES} pages.</p>'
        '<div class="note">Not affiliated with the ARRL, POTA or SOTA. Band information is a US quick reference; always check current rules.</div><div class="barcode"></div>')
spine = '<div>Good Copy <b>AMATEUR RADIO LOGBOOK</b></div>'

if __name__ == "__main__":
    print(cover(front, back, spine, CSS, 8.5, 11, PAGES, OUT / "cover.pdf", preview=OUT / "cover.png"))
