"""Race Ready: premium wrap cover (v2). Front: big title, a race-profile chart (8 runs + 8 stations with simple
station icons) running to a finish line, '12-week plan' badge, track-lane texture. Back: fanned real interior pages
and contents. Run after book_race_log.py."""
import base64, pathlib, subprocess, tempfile
from kdp import cover

OUT = pathlib.Path("/home/claude/kdp/race-ready")
TW, TH, PAGES = 7, 10, 108
LIME, BG, CARD = "#d4f53c", "#111317", "#23262d"

ICONS = {  # simple original line icons, 24x24
    "SkiErg": '<path d="M7 3v18M17 3v18M7 12h10" /><circle cx="12" cy="7" r="2"/>',
    "Sled push": '<path d="M3 17h14l3-4H6z"/><path d="M8 13l3-6h5"/>',
    "Sled pull": '<path d="M3 17h10l3-4H5z"/><path d="M16 13c2-3 3-6 5-8"/>',
    "Burpee jumps": '<path d="M3 19c3-6 6-6 9 0M12 19c3-6 6-6 9 0"/><circle cx="7" cy="7" r="2"/>',
    "Rowing": '<path d="M3 16h18M6 16l5-7 5 7"/><circle cx="11" cy="6" r="2"/>',
    "Farmers carry": '<path d="M6 8h4v10H6zM14 8h4v10h-4zM8 8V5M16 8V5"/>',
    "Sandbag lunges": '<rect x="4" y="7" width="16" height="9" rx="4"/><path d="M8 7V5h8v2"/>',
    "Wall balls": '<circle cx="12" cy="13" r="7"/><path d="M5 13h14M12 6c3 3 3 11 0 14"/>',
}
EFFORT = [0.62, 0.95, 0.88, 0.8, 0.66, 0.58, 0.78, 1.0]  # visual only: relative bar heights


def icon(name, c="#fff"):
    return f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'


def page_png(n, dpi=110):
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), str(OUT / "race-ready-interior.pdf"), str(tmp / "p")], check=True,
                   stderr=subprocess.DEVNULL)
    return "data:image/png;base64," + base64.b64encode(next(tmp.glob("p-*.png")).read_bytes()).decode()


COVER_CSS = f"""
body {{ font-family: Inter, sans-serif; }}
.wrap {{ background: {BG}; color: #fff;
  background-image: repeating-linear-gradient(118deg, transparent 0 46px, rgba(255,255,255,.035) 46px 48px); }}
.front, .back {{ display:flex; flex-direction:column; position:relative; }}
.kick {{ font-weight: 700; font-size: 10.5pt; letter-spacing: .2em; text-transform: uppercase; color: {LIME}; }}
.big {{ font-family: "Inter Display"; font-weight: 900; font-size: 104pt; line-height: .8; letter-spacing: -.055em; margin: 14pt 0 0 -4pt; }}
.big em {{ font-style: normal; color: {LIME}; }}
.sub {{ font-size: 18pt; font-weight: 700; margin-top: 18pt; line-height: 1.18; }}
.sub span {{ color: #9aa1ad; font-weight: 600; }}
.badge {{ position:absolute; right: .55in; top: 2.95in; width: 1.3in; height: 1.3in; border-radius: 50%; border: 3px solid {LIME};
  display:flex; flex-direction:column; align-items:center; justify-content:center; transform: rotate(-10deg); }}
.badge b {{ font-family:"Inter Display"; font-weight:900; font-size: 34pt; line-height:.9; color:{LIME}; }}
.badge span {{ font-size: 8pt; font-weight: 800; letter-spacing:.14em; text-transform:uppercase; margin-top: 3pt; }}
.profile {{ margin-top: auto; position:relative; }}
.bars {{ display:flex; align-items:flex-end; gap: 3pt; height: 2.55in; }}
.bars .r {{ width: 9pt; height: 38%; background: {LIME}; border-radius: 2pt; }}
.bars .s {{ flex:1; background: {CARD}; border-radius: 4pt 4pt 2pt 2pt; border-top: 3px solid #fff; display:flex; justify-content:center; padding-top: 6pt; box-sizing:border-box; }}
.bars .fin {{ width: 14pt; height: 100%; background: repeating-conic-gradient(#fff 0 25%, #111 0 50%) 0 0/7pt 7pt; border-radius: 2pt; }}
.lbl {{ display:flex; gap: 3pt; margin-top: 6pt; }}
.lbl i {{ width: 9pt; }}
.lbl span {{ flex:1; font-size: 6.3pt; font-weight: 800; letter-spacing:.05em; text-transform: uppercase; color:#aab1bd; text-align:center; line-height:1.15; }}
.lbl .f {{ width:14pt; flex:none; }}
.legend {{ display:flex; gap: 14pt; margin-top: 10pt; font-size: 8pt; color:#aab1bd; font-weight:600; }}
.legend b {{ display:inline-block; width: 9pt; height: 9pt; border-radius:2pt; vertical-align: -1pt; margin-right: 5pt; }}
.blurb {{ font-size: 15pt; font-weight: 700; line-height: 1.3; margin-top: 12pt; max-width: 5.6in; }}
.fan {{ position:relative; height: 2.75in; margin-top: 18pt; }}
.fan img {{ position:absolute; width: 1.55in; border-radius: 2pt; box-shadow: 0 10px 22px rgba(0,0,0,.55); background:#fff; }}
.feat {{ margin-top: 10pt; display:grid; grid-template-columns: 1fr 1fr; gap: 6pt 16pt; font-size: 9.6pt; color:#e6e8ec; }}
.feat div {{ padding-left: 14pt; position:relative; line-height:1.35; }}
.feat div::before {{ content:""; position:absolute; left:0; top: 3.5pt; width:7pt; height:7pt; background:{LIME}; border-radius:2pt; }}
.small {{ font-size: 8.5pt; color:#8b93a0; margin-top: auto; max-width: 3.9in; line-height:1.4; }}
.spine-t {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; writing-mode: vertical-rl; font-family:"Inter Display"; font-weight:900; font-size: 9.5pt; letter-spacing:.12em; color:{LIME}; white-space:nowrap; }}
"""

names = list(ICONS)
bars = "".join(f'<div class="r"></div><div class="s" style="height:{int(e * 100)}%">{icon(n)}</div>' for n, e in zip(names, EFFORT)) + '<div class="fin"></div>'
lbl = "".join(f'<i></i><span>{n}</span>' for n in names) + '<span class="f"></span>'
front = ('<div class="kick" style="margin-top:.3in">Fitness race training log</div>'
         '<div class="big">RACE<br><em>READY</em></div>'
         '<div class="sub">8 runs. 8 stations.<br><span>12 weeks to your best finish.</span></div>'
         '<div class="badge"><b>12</b><span>week plan</span></div>'
         f'<div class="profile"><div class="bars">{bars}</div><div class="lbl">{lbl}</div>'
         f'<div class="legend"><span><b style="background:{LIME}"></b>1 km run</span><span><b style="background:#fff"></b>Station</span><span><b style="background:repeating-conic-gradient(#fff 0 25%,#111 0 50%) 0 0/4pt 4pt"></b>Finish</span></div></div>')

imgs = [(21, -8, 0, 22), (15, 3, 1.35, 0), (5, 10, 2.7, 18), (76, -3, 4.05, 6)]
fan = "".join(f'<img src="{page_png(p)}" style="left:{x}in;top:{y}pt;transform:rotate({r}deg)">' for p, r, x, y in imgs)
back = ('<div class="kick" style="margin-top:.3in">Train smarter for race day</div>'
        '<div class="blurb">Plan every week. Log every session.<br>See exactly where you gain time.</div>'
        f'<div class="fan">{fan}</div>'
        '<div class="feat"><div>12-week plan with planning and review pages</div><div>Session logs: sets, weights, pace, RPE</div>'
        '<div>Benchmark tests at weeks 1, 6 and 12</div><div>Run pace chart and finish-time planner</div>'
        '<div>Technique cues and drills for all 8 stations</div><div>Wall ball set plans and first-race pacing</div>'
        '<div>2026/27 station weights for every division</div><div>6 race logs with full split sheets</div></div>'
        '<div class="small">7 x 10 in · 108 pages<br>Independent publication, not affiliated with any race organiser.</div>')
spine = '<div class="spine-t">RACE READY · TRAINING LOG</div>'
print(cover(front, back, spine, COVER_CSS, TW, TH, PAGES, OUT / "race-ready-cover.pdf", preview=OUT / "cover.png"))
