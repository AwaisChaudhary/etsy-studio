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


def sun_svg(w=420, h=250):
    # half sun cut by horizontal gaps, horizon line, a few reflection dashes on the water
    bars = []
    r = 150
    cx, cy = w / 2, 170
    gaps = [(118, 6), (98, 7), (78, 8), (58, 9)]
    clip = "".join(f'<rect x="0" y="{cy - g[0]}" width="{w}" height="{g[1]}" fill="black"/>' for g in gaps)
    refl = "".join(f'<rect x="{cx - L / 2}" y="{cy + 14 + i * 13}" width="{L}" height="4" rx="2" fill="{SUN}" opacity="{0.75 - i * 0.14}"/>'
                   for i, L in enumerate([230, 170, 120, 80, 44]))
    return f"""<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SUN}"/><stop offset="1" stop-color="{SUN2}"/></linearGradient>
<mask id="m"><rect width="{w}" height="{h}" fill="white"/>{clip}</mask></defs>
<path d="M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy} Z" fill="url(#sg)" mask="url(#m)"/>
<rect x="0" y="{cy}" width="{w}" height="2" fill="{CREAM}" opacity=".85"/>{refl}</svg>"""


CSS = f"""
body {{ font-family: Inter, sans-serif; }}
.wrap {{ background: linear-gradient(180deg, {NAVY} 0%, {NAVY2} 100%); color: {CREAM}; }}
.front, .back {{ display:flex; flex-direction:column; }}
.kick {{ font-size: 9.5pt; font-weight: 600; letter-spacing: .14em; color: {SUN}; }}
.t {{ font-family: 'Inter Display', Inter, sans-serif; font-weight: 800; font-size: 54pt; line-height: .95; letter-spacing: -.02em; margin-top: 8pt; }}
.s {{ font-size: 16pt; font-weight: 500; margin-top: 10pt; color: {CREAM}; }}
.art {{ margin: auto 0 0; }}
.chips {{ display:flex; flex-direction:column; gap: 5pt; margin-top: 14pt; }}
.chips span {{ font-size: 10.5pt; font-weight: 600; border-left: 3pt solid {SUN}; padding-left: 8pt; }}
.brand {{ font-size: 8.5pt; letter-spacing:.08em; opacity:.8; margin-top: 14pt; }}
.spine {{ display:flex; align-items:center; justify-content:center; }}
.spine div {{ transform: rotate(90deg); white-space: nowrap; font-weight: 700; font-size: 10pt; letter-spacing:.06em; color:{CREAM}; }}
.spine div b {{ color:{SUN}; font-weight:700; margin-left: 10pt; font-size: 8pt; }}
.back h3 {{ font-size: 15pt; margin: 0 0 8pt; font-weight: 800; color: {SUN}; }}
.back p {{ font-size: 9.6pt; line-height: 1.45; margin: 0 0 8pt; }}
.back ul {{ margin: 4pt 0 0; padding-left: 14pt; font-size: 9pt; line-height: 1.5; }}
.thumb {{ width: 1.9in; border: 3pt solid {CREAM}; box-shadow: 0 6pt 16pt rgba(0,0,0,.35); transform: rotate(-3deg); margin: 10pt 0 0 6pt; background:#fff; }}
.row {{ display:flex; gap: 16pt; align-items:flex-start; }}
.barcode {{ position:absolute; right: 0.5in; bottom: 0.5in; width: 2in; height: 1.2in; }}
.note {{ font-size: 7.4pt; opacity:.75; margin-top: auto; max-width: 2.9in; line-height:1.4; }}
"""

front = (f'<div class="kick">90-DAY SOBRIETY JOURNAL</div><div class="t">Back to<br>Daylight</div>'
         f'<div class="s">A guided recovery journal for the first ninety days</div>'
         f'<div class="chips"><span>90 different daily prompts, no repeats</span><span>Craving log and HALT check every day</span><span>Milestones, weekly reviews and a relapse plan</span></div>'
         f'<div class="art">{sun_svg()}</div><div class="brand">STEADY GROUND PRESS</div>')

back = ('<h3>One honest page a day</h3>'
        '<p>Back to Daylight walks you through your first ninety days without drinking or using, one page at a time. Every morning takes two minutes. Every evening asks a new question, so the journal grows with you instead of repeating itself.</p>'
        f'<div class="row"><img class="thumb" src="{page_png(12)}"><ul>'
        '<li>90 unique prompts in 13 weekly themes</li><li>Daily mood, craving and HALT check-in</li><li>Trigger map and craving plan</li>'
        '<li>Relapse-prevention plan you fill in</li><li>Milestone pages: 24 hours to 90 days</li><li>13 weekly reviews and a money-saved tracker</li>'
        '<li>Support contacts and meeting log</li><li>6 x 9 in, 130 pages, matte cover</li></ul></div>'
        '<p style="margin-top:12pt">Works for alcohol or any other substance, whether you are on Day 1 or already a few weeks in. A thoughtful gift for someone starting recovery.</p>'
        '<div class="note">A support tool, not a replacement for medical or professional help.</div><div class="barcode"></div>')

spine = '<div>BACK TO DAYLIGHT <b>90-DAY SOBRIETY JOURNAL</b></div>'

if __name__ == "__main__":
    info = cover(front, back, spine, CSS, TW, TH, PAGES, OUT / "cover.pdf", preview=OUT / "cover.png")
    print(info)
