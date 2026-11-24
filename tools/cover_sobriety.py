"""Back to Daylight: full-wrap cover (6x9, 130 pages, white paper). Original art: a striped sun rising over a calm horizon.
Back shows a real interior day page and what is inside. Barcode zone (bottom right of back) kept empty for KDP."""
import base64, pathlib, subprocess, tempfile
from kdp import cover

OUT = pathlib.Path("/home/claude/kdp/sobriety")
TW, TH = 6, 9
PAGES = int((OUT / "pages.txt").read_text())
NAVY, NAVY2, SUN, SUN2, CREAM = "#0f2a3d", "#173e57", "#f3b562", "#e9834f", "#f6efe2"


def page_png(n, dpi=120):
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), str(OUT / "interior.pdf"), str(tmp / "p")], check=True, stderr=subprocess.DEVNULL)
    return "data:image/png;base64," + base64.b64encode(next(tmp.glob("p-*.png")).read_bytes()).decode()


def scene_svg(w=600, h=520):
    """Dawn landscape: layered hills, rising sun with soft glow, a winding path to the sun, distant birds. All original vector art."""
    sx, sy, r = 330, 300, 78
    hills = [
        ("#e8a07a", f"M0 300 C120 270 220 285 300 296 C380 307 470 268 600 282 L600 520 L0 520Z", .9),
        ("#b9667a", f"M0 330 C90 300 200 318 290 334 C380 350 470 300 600 318 L600 520 L0 520Z", 1),
        ("#7a3f6e", f"M0 372 C110 342 230 370 330 380 C440 390 520 350 600 362 L600 520 L0 520Z", 1),
        ("#3f2a5c", f"M0 420 C140 396 250 420 360 430 C460 440 540 408 600 414 L600 520 L0 520Z", 1),
        ("#1d1a3a", f"M0 466 C150 448 280 470 400 474 C500 478 560 458 600 462 L600 520 L0 520Z", 1),
    ]
    hill_svg = "".join(f'<path d="{d}" fill="{c}" opacity="{o}"/>' for c, d, o in hills)
    path = ('<path d="M300 520 C280 488 360 474 340 452 C322 432 280 428 300 404 C316 384 352 380 338 362 C328 348 318 340 326 330" '
            'fill="none" stroke="#f6d7a4" stroke-width="10" stroke-linecap="round" opacity=".55"/>'
            '<path d="M300 520 C280 488 360 474 340 452 C322 432 280 428 300 404 C316 384 352 380 338 362 C328 348 318 340 326 330" '
            'fill="none" stroke="#fbe7c2" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 9" opacity=".9"/>')
    birds = "".join(f'<path d="M{x} {y} q6 -6 12 0 q6 -6 12 0" fill="none" stroke="#2a2048" stroke-width="2.2" stroke-linecap="round"/>' for x, y in [(120, 170), (150, 150), (182, 176), (452, 132)])
    rays = "".join(f'<rect x="{sx - 2}" y="{sy - r - 70}" width="4" height="46" rx="2" fill="#fbd9a0" opacity=".35" transform="rotate({a} {sx} {sy})"/>' for a in range(-80, 81, 20))
    return f"""<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax slice">
<defs><radialGradient id="glow" cx="{sx}" cy="{sy}" r="260" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffd59a" stop-opacity=".95"/><stop offset=".35" stop-color="#f7a46f" stop-opacity=".45"/><stop offset="1" stop-color="#f7a46f" stop-opacity="0"/></radialGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1c9"/><stop offset="1" stop-color="#ffc27a"/></linearGradient></defs>
<circle cx="{sx}" cy="{sy}" r="260" fill="url(#glow)"/>{rays}<circle cx="{sx}" cy="{sy}" r="{r}" fill="url(#sun)"/>{birds}{hill_svg}{path}</svg>"""


GRAIN = ("data:image/svg+xml;utf8," + "<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")


CSS = f"""
body {{ font-family: Inter, sans-serif; }}
.wrap {{ background: linear-gradient(180deg, #121a3a 0%, #2b2456 38%, #6b3f6e 62%, #d98a74 86%, #f2b27f 100%); color: {CREAM}; }}
.wrap::after {{ content:""; position:absolute; inset:0; background-image:url("{GRAIN}"); pointer-events:none; }}
.front, .back {{ display:flex; flex-direction:column; position:relative; z-index:1; }}
.front {{ padding-bottom: 0 !important; }}
.kick {{ font-size: 8.6pt; font-weight: 700; letter-spacing: .26em; color: #f6c98d; text-align:center; margin-top: 4pt; }}
.t {{ font-family: 'GFS Baskerville', 'Bitstream Charter', serif; font-size: 52pt; line-height: .98; text-align:center; margin-top: 10pt; color:#fff6e6; text-shadow: 0 2pt 14pt rgba(0,0,0,.25); }}
.s {{ font-family: 'Bitstream Charter', serif; font-style: italic; font-size: 14pt; text-align:center; margin-top: 10pt; color:#f3e3cf; }}
.chips {{ display:flex; justify-content:center; gap: 6pt; margin-top: 12pt; flex-wrap: wrap; }}
.chips span {{ font-size: 7.8pt; font-weight: 600; letter-spacing:.03em; border: .8pt solid rgba(246,201,141,.7); border-radius: 20pt; padding: 3pt 8pt; color:#fbe6c8; }}
.art {{ position:absolute; left:-0.125in; right:-0.125in; bottom: -0.02in; }}
.brand {{ position:absolute; bottom: 0.3in; left:0.5in; text-align:left; font-size: 7.6pt; letter-spacing:.24em; color:#f6dcb6; z-index:2; }}
.spine {{ display:flex; align-items:center; justify-content:center; z-index:1; }}
.spine div {{ transform: rotate(90deg); white-space: nowrap; font-family:'GFS Baskerville', serif; font-size: 11pt; letter-spacing:.04em; color:#fff2dc; }}
.spine div b {{ font-family: Inter, sans-serif; color:#f6c98d; font-weight:700; margin-left: 12pt; font-size: 6.8pt; letter-spacing:.18em; }}
.back h3 {{ font-family: 'GFS Baskerville', serif; font-weight: normal; font-size: 20pt; margin: 0 0 8pt; color: #fff2dc; }}
.back p {{ font-size: 9.4pt; line-height: 1.5; margin: 0 0 8pt; color:#f3e7d7; }}
.back ul {{ margin: 4pt 0 0; padding-left: 13pt; font-size: 8.8pt; line-height: 1.55; color:#f3e7d7; }}
.thumb {{ width: 1.85in; border: 3pt solid #fff6e6; box-shadow: 0 8pt 18pt rgba(0,0,0,.35); transform: rotate(-3deg); margin: 8pt 0 0 6pt; background:#fff; }}
.row {{ display:flex; gap: 16pt; align-items:flex-start; }}
.barcode {{ position:absolute; right: 0.5in; bottom: 0.5in; width: 2in; height: 1.2in; }}
.note {{ font-size: 7.2pt; color:#2a2048; margin-top: auto; max-width: 2.6in; line-height:1.4; font-weight:600; }}
"""

front = ('<div class="kick">A 90-DAY SOBRIETY JOURNAL</div><div class="t">Back to<br>Daylight</div>'
         '<div class="s">One honest page a day</div>'
         '<div class="chips"><span>90 prompts, no repeats</span><span>Craving and HALT check-ins</span><span>Milestones to day 90</span></div>'
         f'<div class="art">{scene_svg()}</div><div class="brand">STEADY GROUND PRESS</div>')

back = ('<h3>Ninety days. One page at a time.</h3>'
        '<p>Back to Daylight walks you through your first ninety days without drinking or using, one page at a time. Every morning takes two minutes. Every evening asks a new question, so the journal grows with you instead of repeating itself.</p>'
        f'<div class="row"><img class="thumb" src="{page_png(14)}"><ul>'
        '<li>90 unique prompts in 13 weekly themes</li><li>Daily mood, craving and HALT check-in</li><li>Trigger map and craving plan</li>'
        '<li>Relapse-prevention plan you fill in</li><li>Milestone pages: 24 hours to 90 days</li><li>13 weekly reviews and a money-saved tracker</li>'
        '<li>Week openers, 30 things to do instead of using, support contacts and meeting log</li><li>6 x 9 in, 144 pages, matte cover</li></ul></div>'
        '<p style="margin-top:12pt">Works for alcohol or any other substance, whether you are on Day 1 or already a few weeks in. A thoughtful gift for someone starting recovery.</p>'
        '<div class="note">A support tool, not a replacement for medical or professional help.</div><div class="barcode"></div>')

spine = '<div>BACK TO DAYLIGHT <b>90-DAY SOBRIETY JOURNAL</b></div>'

if __name__ == "__main__":
    info = cover(front, back, spine, CSS, TW, TH, PAGES, OUT / "cover.pdf", preview=OUT / "cover.png")
    print(info)
