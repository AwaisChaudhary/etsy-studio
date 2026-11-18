"""2027 Crochet & Knitting Project Planner: printable PDF in US Letter (Sunday start) and A4 (Monday start)."""
import calendar, sys
from render import render

YEAR = 2027
TEAL, BERRY, GOLD, INK, SOFT = "#2f8f8a", "#b8326a", "#e9a227", "#1f2a44", "#e6efec"
MONTHS = list(calendar.month_name)[1:]

CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Poppins, sans-serif; color: {INK}; }}
.page {{ width: var(--pw); height: var(--ph); padding: 0.55in 0.6in; position: relative; page-break-after: always; overflow: hidden; display: flex; flex-direction: column; }}
h1 {{ font-family: Lora, serif; font-weight: 700; font-size: 30pt; line-height: 1.05; }}
h2 {{ font-family: Lora, serif; font-weight: 700; font-size: 24pt; margin-bottom: 4pt; }}
.kick {{ font-size: 9pt; font-weight: 500; letter-spacing: .12em; text-transform: uppercase; color: {TEAL}; }}
.sub {{ font-size: 9.5pt; color: #5b6478; margin-bottom: 12pt; }}
.yarnline {{ height: 10pt; margin: 6pt 0 14pt; background: radial-gradient(circle at 5pt 5pt, {BERRY} 3pt, transparent 3.5pt) 0 0 / 14pt 10pt repeat-x; opacity: .85; }}
.box {{ border: 1.2pt solid #c9d3d0; border-radius: 6pt; padding: 8pt 10pt; }}
.lab {{ font-size: 8pt; font-weight: 600; color: #5b6478; text-transform: uppercase; letter-spacing: .06em; }}
.lines {{ background: repeating-linear-gradient(transparent 0 21pt, #cfd6d4 21pt 22pt); }}
.dots {{ background: radial-gradient(#b9c3c0 0.9pt, transparent 1.1pt) 0 0 / 0.2in 0.2in; }}
.foot {{ position: absolute; bottom: 0.3in; left: 0.6in; right: 0.6in; display: flex; justify-content: space-between; font-size: 7pt; color: #9aa4b8; }}
table.cal {{ width: 100%; border-collapse: collapse; table-layout: fixed; align-self: start; }}
table.cal th {{ height: 20pt; }}
table.cal.w4 td {{ height: 1.85in; }}
table.cal.w5 td {{ height: 1.5in; }}
table.cal.w6 td {{ height: 1.25in; }}
table.cal th {{ font-size: 8.5pt; font-weight: 600; color: #fff; background: {TEAL}; padding: 4pt 0; }}
table.cal td {{ border: 1pt solid #cfd6d4; vertical-align: top; padding: 3pt 4pt; font-size: 9pt; font-weight: 600; }}
table.cal td.off {{ background: #f4f6f5; color: #c0c7c5; }}
.mini {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14pt 18pt; flex: 1; }}
.mini table {{ width: 100%; border-collapse: collapse; font-size: 7.5pt; text-align: center; }}
.mini caption {{ font-family: Lora, serif; font-weight: 700; font-size: 11pt; text-align: left; padding-bottom: 3pt; color: {TEAL}; }}
.mini th {{ color: {BERRY}; font-weight: 600; font-size: 6.5pt; }}
.mini td {{ padding: 1.6pt 0; }}
.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10pt; }}
.field {{ border-bottom: 1pt solid #cfd6d4; padding: 4pt 0 3pt; font-size: 8.5pt; color: #5b6478; }}
table.log {{ width: 100%; border-collapse: collapse; }}
table.log th {{ font-size: 8pt; font-weight: 600; color: #fff; background: {TEAL}; padding: 5pt 4pt; text-align: left; }}
table.log td {{ border-bottom: 1pt solid #d5dcda; height: 0.34in; }}
table.log tr:nth-child(even) td {{ background: #f6f9f8; }}
.counter {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 3pt; flex: 1; align-content: start; }}
.counter span {{ border: 1pt solid #cfd6d4; border-radius: 50%; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; font-size: 7pt; color: #8a93a6; }}
.cover {{ background: {INK}; color: #fff; justify-content: center; }}
.cover .big {{ font-family: Lora, serif; font-size: 96pt; font-weight: 700; line-height: .9; color: {GOLD}; }}
.cover h1 {{ font-size: 40pt; color: #fff; margin-top: 10pt; }}
.cover p {{ font-size: 12pt; opacity: .85; margin-top: 12pt; max-width: 4.6in; }}
.swatch {{ position: absolute; right: -0.4in; bottom: 0.8in; width: 4.6in; opacity: .95; }}
.side {{ display: grid; grid-template-columns: 1fr 2.1in; gap: 12pt; flex: 1; min-height: 0; }}
.side .col {{ display: flex; flex-direction: column; gap: 10pt; }}
.check {{ display: flex; gap: 6pt; align-items: center; font-size: 8.5pt; padding: 3.2pt 0; border-bottom: 1pt solid #e2e7e6; }}
.check i {{ width: 9pt; height: 9pt; border: 1.2pt solid {TEAL}; border-radius: 2pt; flex: none; }}
"""

def foot(n):
    return f'<div class="foot"><span>{YEAR} Crochet &amp; Knitting Planner</span><span>{n}</span></div>'

def knit_svg(cols=12, rows=9):
    out = []
    pal = ["#f3eee6", "#f3eee6", "#2f8f8a", "#b8326a", "#e9a227"]
    for r in range(rows):
        for c in range(cols):
            col = pal[(r // 2) % len(pal)] if (r % 4 in (1, 2) and (c + r) % 3 == 0) or r % 6 == 0 else "#f3eee6"
            x, y = c * 30 + 15, r * 25 + 14
            for s in (-1, 1):
                out.append(f'<ellipse cx="{x + s * 6.5}" cy="{y}" rx="7.2" ry="16" transform="rotate({s * 30} {x + s * 6.5} {y})" fill="{col}" stroke="rgba(0,0,0,.18)" stroke-width="1"/>')
    return f'<svg class="swatch" viewBox="0 0 {cols * 30} {rows * 25 + 10}">{"".join(out)}</svg>'

def month_table(y, m, first):
    cal = calendar.Calendar(firstweekday=first)
    heads = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]; heads = heads[first:] + heads[:first]
    rows = ""
    for wk in cal.monthdatescalendar(y, m):
        rows += "<tr>" + "".join(f'<td class="{"off" if d.month != m else ""}">{d.day}</td>' for d in wk) + "</tr>"
    return heads, rows

def build(size):
    first = 6 if size == "letter" else 0
    P = []
    P.append(f'<div class="page cover"><div class="kick" style="color:#e9a227">Printable planner</div><div class="big">{YEAR}</div><h1>Crochet &amp; Knitting<br>Project Planner</h1><p>Plan your makes, track every row, keep your stash in order and remember what you made for whom.</p>{knit_svg()}</div>')
    P.append(f'<div class="page"><div class="kick">Welcome</div><h2>This planner belongs to</h2><div class="field" style="font-size:14pt;height:.5in"></div><div class="yarnline"></div>'
             '<h2 style="font-size:16pt;margin-top:10pt">How to use it</h2><ul style="font-size:10pt;line-height:1.7;margin:6pt 0 0 14pt">'
             '<li>Start with <b>Year at a glance</b> and <b>Making goals</b> to set your plans.</li><li>Each month has a calendar plus space for projects, yarn to buy and notes.</li>'
             '<li>Print as many <b>Project planner</b> and <b>Row tracker</b> pages as you need, one per project.</li><li>Use the logs for your stash, gauge swatches, patterns, gifts and finished projects.</li>'
             '<li>Print at 100% (actual size). Works in colour or black and white.</li></ul>'
             f'<div class="box dots" style="flex:1;margin-top:16pt"><div class="lab">Notes</div></div>{foot(2)}</div>')
    minis = ""
    heads0 = ["M", "T", "W", "T", "F", "S", "S"]; h = heads0[first:] + heads0[:first]
    for m in range(1, 13):
        _, rows = month_table(YEAR, m, first)
        rows = rows.replace('<td class="off">', '<td style="color:#d0d6d4">').replace('<td class="">', "<td>")
        minis += f'<table><caption>{MONTHS[m - 1]}</caption><tr>{"".join(f"<th>{x}</th>" for x in h)}</tr>{rows}</table>'
    P.append(f'<div class="page"><div class="kick">{YEAR}</div><h2>Year at a glance</h2><div class="yarnline"></div><div class="mini">{minis}</div>{foot(3)}</div>')
    goals = "".join(f'<div class="box" style="margin-bottom:10pt"><div class="lab">{t}</div><div class="lines" style="height:{hh}in;margin-top:4pt"></div></div>' for t, hh in
                    [("Projects I want to make this year", 1.5), ("Skills and techniques to learn", 1.0), ("Gifts to make", 1.0), ("Yarn and tools to get", 0.9), ("How I'll make time to craft", 0.9)])
    P.append(f'<div class="page"><div class="kick">Plan</div><h2>My making goals for {YEAR}</h2><div class="yarnline"></div>{goals}{foot(4)}</div>')
    n = 5
    for m in range(1, 13):
        heads, rows = month_table(YEAR, m, first)
        checks = "".join('<div class="check"><i></i></div>' for _ in range(7))
        P.append(f'<div class="page"><div class="kick">{YEAR}</div><h2>{MONTHS[m - 1]}</h2><div class="yarnline" style="margin-bottom:10pt"></div><div class="side">'
                 f'<table class="cal w{rows.count("<tr>")}"><tr>{"".join(f"<th>{x}</th>" for x in heads)}</tr>{rows}</table>'
                 f'<div class="col"><div class="box"><div class="lab">On my needles &amp; hooks</div>{checks}</div>'
                 f'<div class="box"><div class="lab">Yarn to buy</div><div class="lines" style="height:1.1in;margin-top:4pt"></div></div>'
                 f'<div class="box" style="flex:1"><div class="lab">Notes</div><div class="lines" style="height:100%;margin-top:4pt"></div></div></div></div>{foot(n)}</div>')
        n += 1
    fld = lambda t: f'<div class="field">{t}</div>'
    for k in range(2):
        P.append(f'<div class="page"><div class="kick">Project</div><h2>Project planner</h2><div class="yarnline"></div>'
                 f'<div class="grid2">{fld("Project")}{fld("For")}{fld("Pattern / designer")}{fld("Source or link")}{fld("Start date")}{fld("Finish by")}</div>'
                 f'<div class="grid2" style="margin-top:12pt"><div class="box"><div class="lab">Yarn</div>{fld("Brand &amp; name")}{fld("Weight &amp; fibre")}{fld("Colour &amp; dye lot")}{fld("Yards / skeins needed")}</div>'
                 f'<div class="box"><div class="lab">Tools &amp; gauge</div>{fld("Hook / needle size")}{fld("Gauge (sts × rows)")}{fld("Size I&#39;m making")}{fld("Notions")}</div></div>'
                 f'<div class="grid2" style="margin-top:12pt;flex:1"><div class="box"><div class="lab">Modifications &amp; notes</div><div class="lines" style="height:2.6in;margin-top:4pt"></div></div>'
                 f'<div class="box dots"><div class="lab">Sketch or swatch</div></div></div>{foot(n)}</div>')
        n += 1
    P.append(f'<div class="page"><div class="kick">Track</div><h2>Row &amp; round tracker</h2><div class="sub">Tick a circle every row. Project: ______________________________</div>'
             f'<div class="counter">{"".join(f"<span>{i}</span>" for i in range(1, 181))}</div>{foot(n)}</div>'); n += 1
    def log(title, kick, cols, rows=24, sub=""):
        return (f'<div class="page"><div class="kick">{kick}</div><h2>{title}</h2><div class="sub">{sub}</div><table class="log"><tr>{"".join(f"<th>{c}</th>" for c in cols)}</tr>'
                + "".join("<tr>" + "".join("<td></td>" for _ in cols) + "</tr>" for _ in range(rows)) + "</table>")
    for t, k, cols, sub in [("Gauge swatch log", "Log", ["Yarn", "Hook / needle", "Stitch", "Sts per 4 in", "Rows per 4 in", "Washed?"], "Measure after washing and drying your swatch."),
                            ("Yarn stash inventory", "Log", ["Brand &amp; yarn", "Colour", "Weight", "Yards", "Skeins", "Stored"], ""),
                            ("Pattern wishlist", "Log", ["Pattern", "Designer", "Yarn needed", "Where to find it", "Bought?"], ""),
                            ("Gift making planner", "Log", ["For", "Occasion &amp; date", "Project", "Start by", "Done?"], "Work back from the date so nothing is a last-minute rush."),
                            ("Finished projects", "Log", ["Project", "Yarn used", "Finished", "Hours", "Rating"], "Every finished object deserves a line here.")]:
        P.append(log(t, k, cols, sub=sub) + foot(n) + "</div>"); n += 1
    P.append(f'<div class="page"><div class="kick">Notes</div><h2>Notes &amp; charts</h2><div class="box dots" style="flex:1;margin-top:8pt"></div>{foot(n)}</div>')
    return CSS, P

if __name__ == "__main__":
    out = sys.argv[1]
    for size in ("letter", "a4"):
        css, pages = build(size)
        render(css, pages, size, f"{out}/2027-crochet-knitting-planner-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
