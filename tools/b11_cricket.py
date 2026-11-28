"""Cricket Scorebook Printable (batch 11, lane b, sports): 11 landscape pages: cover + scoring key, limited-overs batting
scorecard (ball-by-ball run boxes, how out, R/B/4s/6s/SR, extras, total, fall of wickets), bowling analysis with 10 over boxes
per bowler + over-by-over run tally to 50 overs, long-format (Test / multi-day) bowling with 30 overs, a one-page T20 scorecard
(both innings), partnerships + match summary, field placement page (labelled reference field + 4 blank fields), season batting
averages, season bowling averages, fixtures & results. All drawn here (HTML/SVG). US Letter + A4, landscape."""
import math, sys
sys.path.insert(0, ".")
from render import render

G, DG, RED, CREAM, INK, LINE, TINT = "#1f5b3f", "#123b29", "#a8322c", "#fbf8f1", "#22281f", "#9aa69c", "#eef4ef"
CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Inter, "Liberation Sans", sans-serif; color: {INK}; }}
.page {{ width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #fff; contain: strict; }}
.serif {{ font-family: Lora, serif; }}
.in {{ position: absolute; inset: 0.35in 0.4in 0.38in; display: flex; flex-direction: column; gap: 0.08in; }}
table {{ border-collapse: collapse; width: 100%; table-layout: fixed; }}
td, th {{ border: 0.9px solid {LINE}; font-size: 7.5pt; padding: 0 3px; }}
th {{ background: {G}; color: #fff; font-weight: 600; font-size: 7pt; letter-spacing: .04em; text-transform: uppercase; height: 0.24in; }}
td.k {{ background: {TINT}; font-weight: 600; color: {DG}; }}
.title {{ display: flex; align-items: baseline; justify-content: space-between; border-bottom: 2.5px solid {G}; padding-bottom: 3pt; }}
.title .t {{ font-family: Lora, serif; font-size: 18pt; font-weight: 600; color: {DG}; }}
.title .s {{ font-size: 7.5pt; letter-spacing: .25em; color: {RED}; font-weight: 600; text-transform: uppercase; }}
.hd {{ display: grid; gap: 4px 12px; font-size: 8pt; }}
.f {{ display: flex; gap: 5px; align-items: flex-end; }} .f b {{ font-weight: 600; color: {DG}; white-space: nowrap; font-size: 7.5pt; }}
.f span {{ flex: 1; border-bottom: 0.9px solid {INK}; height: 0.2in; }}
.foot {{ position: absolute; bottom: 0.14in; left: 0; right: 0; text-align: center; font-size: 6.5pt; color: #a3aaa2; letter-spacing: .14em; }}
.balls {{ background: repeating-linear-gradient(90deg, transparent 0 calc(0.19in - 0.6px), #d5dcd6 calc(0.19in - 0.6px) 0.19in); }}
"""
def foot(): return '<div class="foot">PURL &amp; PAPER · CRICKET SCOREBOOK</div>'
def f(lbl, flex=1): return f'<div class="f" style="flex:{flex}"><b>{lbl}</b><span></span></div>'
def row(*items): return '<div style="display:flex;gap:12px">' + "".join(f(a, b) for a, b in items) + '</div>'
def title(t, s): return f'<div class="title"><div class="t">{t}</div><div class="s">{s}</div></div>'

def match_head(extra=True):
    r = row(("Match", 3), ("Date", 1.4), ("Venue", 2.2))
    r += row(("Batting team", 2.6), ("v", 2.2), ("Toss won by", 1.8), ("elected to", 1.2))
    if extra: r += row(("Innings", 0.9), ("Overs per side", 1.1), ("Umpires", 2.2), ("Scorer", 1.6))
    return f'<div class="hd" style="display:flex;flex-direction:column;gap:5px">{r}</div>'

def cricket_ball(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{RED}"/><path d="M{cx - r * .35} {cy - r * .94} Q{cx + r * .25} {cy} {cx - r * .35} {cy + r * .94}" stroke="#f4e3c9" stroke-width="{r * .08:.1f}" fill="none"/>'
            f'<path d="M{cx - r * .22} {cy - r * .97} Q{cx + r * .38} {cy} {cx - r * .22} {cy + r * .97}" stroke="#f4e3c9" stroke-width="{r * .06:.1f}" fill="none" stroke-dasharray="{r * .07:.1f} {r * .06:.1f}"/>'
            f'<circle cx="{cx - r * .4}" cy="{cy - r * .4}" r="{r * .18:.1f}" fill="#fff" opacity=".25"/>')

def stumps(x, y, h):
    return "".join(f'<rect x="{x + k * h * .14}" y="{y}" width="{h * .07:.1f}" height="{h}" rx="{h * .03:.1f}" fill="#e9d9b8" stroke="#8a6a3c" stroke-width="2"/>' for k in range(3)) + \
           f'<rect x="{x - h * .02:.1f}" y="{y - h * .05:.1f}" width="{h * .14:.1f}" height="{h * .04:.1f}" rx="2" fill="#c8a868"/><rect x="{x + h * .14:.1f}" y="{y - h * .05:.1f}" width="{h * .14:.1f}" height="{h * .04:.1f}" rx="2" fill="#c8a868"/>'

# ---------------- pages ----------------
def cover():
    key = [("•", "dot ball (no run)"), ("1 2 3", "runs off the bat"), ("4 / 6", "boundary four / six (circle them)"), ("W", "wicket (write how out in the batting card)"),
           ("+", "wide (add runs: +2 = wide + 1 run)"), ("○", "no ball (write runs inside: ⓸)"), ("b / lb", "byes / leg byes (write the number below the dot)"),
           ("M", "maiden over (no runs off the bowler)"), ("│", "draw a line after the last ball of each over"), ("Σ", "carry the running total down every over")]
    keyrows = "".join(f'<tr><td class="k" style="text-align:center;font-size:11pt;width:0.9in;height:0.31in">{a}</td><td style="font-size:9pt;padding-left:8px">{b}</td></tr>' for a, b in key)
    contents = ["Scoring key (this page)", "Limited-overs batting scorecard", "Bowling analysis + over-by-over tally (50 overs)", "Long-format bowling (Test / multi-day, 30 overs)",
                "One-page T20 scorecard (both innings)", "Partnerships + match summary", "Field placings (reference field + 4 blank fields)", "Season batting averages",
                "Season bowling averages", "Fixtures & results"]
    art = (f'<svg viewBox="0 0 520 520" style="width:3.1in"><circle cx="260" cy="260" r="250" fill="{G}"/><circle cx="260" cy="260" r="250" fill="none" stroke="#fff" stroke-width="5" opacity=".35"/>'
           f'<ellipse cx="260" cy="260" rx="150" ry="140" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="10 9" opacity=".45"/>'
           f'<rect x="240" y="150" width="40" height="220" fill="#d9c38f"/>'
           f'<line x1="232" y1="180" x2="288" y2="180" stroke="#fff" stroke-width="3"/><line x1="232" y1="340" x2="288" y2="340" stroke="#fff" stroke-width="3"/>'
           f'{stumps(250, 150, 34)}{stumps(250, 336, 34)}{cricket_ball(380, 360, 46)}</svg>')
    li = "".join(f'<li>{c}</li>' for c in contents)
    return (f'<div class="page" style="background:{CREAM}"><div style="position:absolute;inset:0.35in;border:2px solid {G};border-radius:10px"></div>'
            f'<div style="position:absolute;left:0.75in;top:0.7in;width:4.3in"><div style="font-size:8pt;letter-spacing:.35em;color:{RED};font-weight:600">PRINTABLE · CLUB · SCHOOL · BACKYARD</div>'
            f'<div class="serif" style="font-size:44pt;font-weight:600;line-height:1.02;color:{DG};margin-top:6pt">Cricket<br>Scorebook</div>'
            f'<div style="font-size:10pt;line-height:1.5;margin-top:8pt;color:#4a5248">Ball-by-ball batting cards, bowling analysis, a one-page T20 card, partnerships, field placings and season averages. '
            f'Print as many as you need.</div><div style="margin-top:14pt;display:flex;gap:0.3in;align-items:center">{art}</div></div>'
            f'<div style="position:absolute;left:5.45in;right:0.75in;top:0.75in"><div class="serif" style="font-size:15pt;font-weight:600;color:{DG};margin-bottom:5pt">Scoring key</div>'
            f'<table>{keyrows}</table><div class="serif" style="font-size:13pt;font-weight:600;color:{DG};margin:12pt 0 3pt">Inside</div>'
            f'<ol style="margin-left:16pt;font-size:8.6pt;line-height:1.6">{li}</ol>'
            f'<div style="font-size:7.8pt;line-height:1.45;color:#6a7268;margin-top:8pt">Print at 100% / actual size, landscape. Works for any format: change the overs per side in the header. '
            f'Strike rate = runs ÷ balls × 100. Economy = runs ÷ overs. Average = runs ÷ (innings − not outs).</div></div>{foot()}</div>')

def batting():
    cols = ('<colgroup><col style="width:0.3in"><col style="width:1.45in"><col><col style="width:1.15in"><col style="width:1.0in">'
            '<col style="width:0.42in"><col style="width:0.4in"><col style="width:0.3in"><col style="width:0.3in"><col style="width:0.45in"></colgroup>')
    th = '<tr><th>#</th><th>Batter</th><th>Runs scored (ball by ball)</th><th>How out</th><th>Bowler</th><th>Runs</th><th>Balls</th><th>4s</th><th>6s</th><th>SR</th></tr>'
    trs = "".join(f'<tr style="height:var(--rh)"><td class="k" style="text-align:center">{i}</td><td></td><td class="balls"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 12))
    ex = (f'<tr style="height:var(--rh)"><td class="k" colspan="2">Extras</td><td style="font-size:7.5pt;color:#5a6358">byes ____ &nbsp; leg byes ____ &nbsp; wides ____ &nbsp; no balls ____ &nbsp; penalty ____</td>'
          f'<td colspan="2" class="k" style="text-align:right">Extras total</td><td></td><td colspan="4"></td></tr>'
          f'<tr style="height:var(--rh)"><td class="k" colspan="2" style="font-size:9pt">TOTAL</td><td style="font-size:8pt">for ______ wickets &nbsp;·&nbsp; ______ overs &nbsp;·&nbsp; run rate ______</td>'
          f'<td colspan="2" class="k" style="text-align:right;font-size:9pt">TOTAL</td><td colspan="5"></td></tr>')
    fow = ('<table style="margin-top:2px"><tr><th style="width:1.2in">Fall of wickets</th>' + "".join(f'<th>{k}</th>' for k in range(1, 11)) + '</tr>'
           + "".join(f'<tr style="height:0.24in"><td class="k">{lab}</td>' + '<td></td>' * 10 + '</tr>' for lab in ("Score", "Batter out (#)", "Over")) + '</table>')
    return (f'<div class="page"><div class="in" style="--rh:0.38in">{title("Batting scorecard", "Limited overs · innings")}{match_head()}'
            f'<table>{cols}{th}{trs}{ex}</table>{fow}</div>{foot()}</div>')

def over_boxes(n, w):
    return "".join(f'<td style="padding:0;position:relative"><div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr 1fr;grid-template-rows:1fr 1fr">'
                   + "".join('<div style="border-right:0.5px dotted #c3cbc4;border-bottom:0.5px dotted #c3cbc4"></div>' for _ in range(6)) + '</div></td>' for _ in range(n))

def bowling():
    n = 10
    cols = '<colgroup><col style="width:1.35in">' + '<col>' * n + ''.join(f'<col style="width:{w}">' for w in ("0.32in", "0.3in", "0.36in", "0.3in", "0.3in", "0.3in", "0.42in")) + '</colgroup>'
    th = '<tr><th>Bowler</th>' + "".join(f'<th>{k}</th>' for k in range(1, n + 1)) + '<th>O</th><th>M</th><th>R</th><th>W</th><th>Wd</th><th>Nb</th><th>Econ</th></tr>'
    trs = "".join(f'<tr style="height:0.42in"><td></td>{over_boxes(n, 1)}' + '<td></td>' * 7 + '</tr>' for _ in range(8))
    tally_th = '<tr><th style="width:0.8in">Over</th>' + "".join(f'<th>{k}</th>' for k in range(1, 26)) + '</tr>'
    tally = ""
    for start in (1, 26):
        tally += '<tr><th>Over</th>' + "".join(f'<th style="background:{DG}">{k}</th>' for k in range(start, start + 25)) + '</tr>'
        tally += "".join(f'<tr style="height:0.22in"><td class="k">{lab}</td>' + '<td></td>' * 25 + '</tr>' for lab in ("Runs", "Total", "Wkts"))
    return (f'<div class="page"><div class="in">{title("Bowling analysis", "Limited overs · each box = one over (6 balls)")}{match_head(False)}'
            f'<table>{cols}{th}{trs}</table><div style="font-size:7pt;color:#6a7268">Write each ball in the small boxes (• 1 2 4 6 W + ○). Circle the over number when it\'s a maiden. Total = running team score at the end of the over.</div>'
            f'<table>{tally}</table></div>{foot()}</div>')

def bowling_long():
    n = 15
    cols = '<colgroup><col style="width:1.2in">' + '<col>' * n + ''.join(f'<col style="width:{w}">' for w in ("0.32in", "0.28in", "0.34in", "0.28in", "0.4in")) + '</colgroup>'
    out = ""
    for part, a in (("Overs 1-15", 1), ("Overs 16-30", 16)):
        th = f'<tr><th>{part}</th>' + "".join(f'<th>{k}</th>' for k in range(a, a + n)) + '<th>O</th><th>M</th><th>R</th><th>W</th><th>Econ</th></tr>'
        trs = "".join(f'<tr style="height:0.36in"><td></td>{over_boxes(n, 1)}' + '<td></td>' * 5 + '</tr>' for _ in range(6))
        out += f'<table>{cols}{th}{trs}</table>'
    return (f'<div class="page"><div class="in">{title("Bowling analysis", "Test · multi-day · long format")}'
            f'<div class="hd" style="display:flex;flex-direction:column;gap:5px">{row(("Match", 3), ("Day", 0.7), ("Innings", 0.8), ("Session", 1), ("Date", 1.3))}</div>'
            f'{out}<div style="font-size:7pt;color:#6a7268">Bowlers keep the same row in both tables. Carry overs, runs and wickets across: O / M / R / W in the second table are the bowler\'s totals.</div></div>{foot()}</div>')

def t20():
    def side(name):
        th = '<tr><th style="width:0.22in">#</th><th style="width:1.05in">Batter</th><th>Ball by ball</th><th style="width:0.7in">How out</th><th style="width:0.32in">R</th><th style="width:0.3in">B</th></tr>'
        trs = "".join(f'<tr style="height:0.235in"><td class="k" style="text-align:center">{i}</td><td></td><td class="balls"></td><td></td><td></td><td></td></tr>' for i in range(1, 12))
        bth = '<tr><th style="width:1.05in" colspan="2">Bowler</th>' + "".join(f'<th>{k}</th>' for k in range(1, 5)) + '<th>O</th><th>R</th><th>W</th></tr>'
        btr = "".join('<tr style="height:0.3in"><td colspan="2"></td>' + over_boxes(4, 1) + '<td></td><td></td><td></td></tr>' for _ in range(6))
        tot = (f'<div style="display:flex;gap:10px;font-size:8pt;margin:3px 0"><div class="f" style="flex:1"><b>Extras</b><span></span></div><div class="f" style="flex:1.3"><b>TOTAL</b><span></span></div>'
               f'<div class="f" style="flex:.8"><b>Wkts</b><span></span></div><div class="f" style="flex:.8"><b>Overs</b><span></span></div></div>')
        return (f'<div style="flex:1;display:flex;flex-direction:column;gap:3px"><div class="f"><b style="font-size:9pt;color:{RED}">{name}</b><span></span></div>'
                f'<table>{th}{trs}</table>{tot}<table>{bth}{btr}</table></div>')
    return (f'<div class="page"><div class="in">{title("T20 scorecard", "Both innings · one page")}'
            f'<div class="hd" style="display:flex;flex-direction:column;gap:5px">{row(("Match", 3), ("Date", 1.3), ("Venue", 2), ("Toss", 1.6))}</div>'
            f'<div style="display:flex;gap:0.25in;flex:1">{side("1st innings")}{side("2nd innings")}</div>'
            f'<div class="hd" style="display:flex;flex-direction:column;gap:5px">{row(("Result", 3), ("Player of the match", 2))}</div></div>{foot()}</div>')

def partnerships():
    th = '<tr><th style="width:0.5in">Wkt</th><th>Batter</th><th>Batter</th><th style="width:0.6in">Runs</th><th style="width:0.6in">Balls</th><th style="width:0.8in">Score at fall</th></tr>'
    trs = "".join(f'<tr style="height:0.3in"><td class="k" style="text-align:center">{w}</td><td></td><td></td><td></td><td></td><td></td></tr>' for w in ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"])
    summ = "".join(f'<div class="f" style="height:0.34in"><b>{k}</b><span></span></div>' for k in
                   ["Team 1 total", "Team 2 total", "Result", "Won by", "Player of the match", "Top scorer", "Best bowling", "Best catch / fielding moment", "Weather & pitch"])
    notes = '<div style="flex:1;margin-top:6px;background:repeating-linear-gradient(transparent 0 0.27in, #c9d1ca 0.27in calc(0.27in + 1px))"></div>'
    return (f'<div class="page"><div class="in">{title("Partnerships & match summary", "One sheet per match")}'
            f'<div style="display:flex;gap:0.35in;flex:1"><div style="flex:1.25;display:flex;flex-direction:column;gap:6px">'
            f'<div class="serif" style="font-size:11pt;font-weight:600;color:{DG}">Partnerships: innings 1</div><table>{th}{trs}</table>'
            f'<div class="serif" style="font-size:11pt;font-weight:600;color:{DG};margin-top:4px">Partnerships: innings 2</div><table>{th}{trs}</table></div>'
            f'<div style="flex:1;display:flex;flex-direction:column"><div class="serif" style="font-size:11pt;font-weight:600;color:{DG};margin-bottom:4px">Match summary</div>{summ}'
            f'<div class="serif" style="font-size:11pt;font-weight:600;color:{DG};margin-top:8px">Notes</div>{notes}</div></div></div>{foot()}</div>')

def field(labels=True, w=440):
    """Oval field for a right-handed batter (batter at the top end, bowler running in from the bottom)."""
    cx, cy = 250, 250
    s = (f'<svg viewBox="0 0 500 500" style="width:100%;height:100%"><ellipse cx="{cx}" cy="{cy}" rx="240" ry="240" fill="#e4efe5" stroke="{G}" stroke-width="4"/>'
         f'<ellipse cx="{cx}" cy="{cy}" rx="135" ry="135" fill="none" stroke="{G}" stroke-width="2" stroke-dasharray="7 6"/>'
         f'<rect x="{cx - 10}" y="{cy - 50}" width="20" height="100" fill="#d9c38f"/><line x1="{cx - 16}" y1="{cy - 40}" x2="{cx + 16}" y2="{cy - 40}" stroke="#fff" stroke-width="2"/>'
         f'<line x1="{cx - 16}" y1="{cy + 40}" x2="{cx + 16}" y2="{cy + 40}" stroke="#fff" stroke-width="2"/>')
    if labels:
        # angle 0 = straight behind the bowler (down the ground), measured clockwise as seen on the page; off side = left of page for a RH batter at the top facing down
        P = [("Keeper", 0, -88, 1, -12), ("Bowler", 0, 72, 1, 18), ("1st slip", -26, -98, 1, -12), ("2nd slip", -68, -100, 1, -12), ("Gully", -104, -84, 1, 18),
             ("Point", -112, -30, 0, 18), ("Cover", -112, 40, 0, 18), ("Mid-off", -48, 108, 0, 18), ("Mid-on", 48, 108, 0, 18), ("Midwicket", 112, 40, 0, 18),
             ("Square leg", 112, -30, 0, 18), ("Short leg", 40, -52, 1, 18), ("Third man", -150, -170, 0, 18), ("Fine leg", 140, -180, 0, 18),
             ("Deep point", -205, -50, 0, 18), ("Deep cover", -190, 95, 0, 18), ("Long-off", -70, 205, 0, 18), ("Long-on", 70, 205, 0, 18),
             ("Deep midwicket", 180, 100, 0, 18), ("Deep sq. leg", 196, -50, 0, 18)]
        for name, dx, dy, small, ly in P:
            x, y = cx + dx, cy + dy
            s += f'<circle cx="{x}" cy="{y}" r="6" fill="{RED}"/><text x="{x}" y="{y + ly}" text-anchor="middle" font-family="Inter, sans-serif" font-size="{10.5 if small else 11.5}" fill="{INK}">{name}</text>'
        s += (f'<text x="60" y="255" font-family="Lora, serif" font-size="15" font-weight="600" fill="{DG}" text-anchor="middle">OFF</text>'
              f'<text x="440" y="255" font-family="Lora, serif" font-size="15" font-weight="600" fill="{DG}" text-anchor="middle">LEG</text>')
    return s + '</svg>'

def fields():
    blank = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px"><div style="width:100%;flex:1">{field(False)}</div>'
                    f'<div class="f" style="width:100%"><b>Bowler / plan</b><span></span></div></div>' for _ in range(4))
    return (f'<div class="page"><div class="in">{title("Field placings", "Right-handed batter · mirror for left-handers")}'
            f'<div style="display:flex;gap:0.3in;flex:1;min-height:0"><div style="flex:1.05;display:flex;flex-direction:column;min-height:0">'
            f'<div style="flex:1;min-height:0">{field(True)}</div><div style="font-size:7pt;color:#6a7268;text-align:center">Batter at the top end. Dashed ring = the 30-yard circle.</div></div>'
            f'<div style="flex:1.25;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0.15in 0.2in">{blank}</div></div></div>{foot()}</div>')

def season_table(kind):
    if kind == "bat":
        heads = ["Player", "M", "Inn", "NO", "Runs", "HS", "Avg", "Balls", "SR", "100s", "50s", "4s", "6s", "Ct", "St"]
        widths = ["1.9in"] + ["auto"] * 14; ttl = ("Season batting averages", "Average = runs ÷ (innings − not outs)")
    else:
        heads = ["Player", "M", "Overs", "Mdns", "Runs", "Wkts", "Best", "Avg", "Econ", "SR", "4w", "5w", "Wd", "Nb"]
        widths = ["1.9in"] + ["auto"] * 13; ttl = ("Season bowling averages", "Avg = runs ÷ wkts · Econ = runs ÷ overs · SR = balls ÷ wkts")
    cols = "<colgroup>" + "".join(f'<col style="width:{w}">' if w != "auto" else "<col>" for w in widths) + "</colgroup>"
    th = "<tr>" + "".join(f"<th>{h}</th>" for h in heads) + "</tr>"
    trs = "".join('<tr style="height:0.315in">' + "<td></td>" * len(heads) + "</tr>" for _ in range(18))
    return (f'<div class="page"><div class="in">{title(*ttl)}<div class="hd" style="display:flex;flex-direction:column;gap:5px">{row(("Team", 3), ("Season", 1.2), ("Competition", 2.2))}</div>'
            f'<table>{cols}{th}{trs}</table></div>{foot()}</div>')

def fixtures():
    heads = [("Date", "0.8in"), ("Opponent", "1.7in"), ("Home / away", "0.7in"), ("Format", "0.65in"), ("Our score", "0.85in"), ("Their score", "0.85in"),
             ("Result", "0.75in"), ("Top scorer", "auto"), ("Best bowler", "auto"), ("Pts", "0.4in")]
    cols = "<colgroup>" + "".join(f'<col style="width:{w}">' if w != "auto" else "<col>" for _, w in heads) + "</colgroup>"
    th = "<tr>" + "".join(f"<th>{h}</th>" for h, _ in heads) + "</tr>"
    trs = "".join('<tr style="height:0.31in">' + "<td></td>" * len(heads) + "</tr>" for _ in range(17))
    tot = (f'<div style="display:flex;gap:12px">' + "".join(f'<div class="f" style="flex:1"><b>{k}</b><span></span></div>' for k in ("Played", "Won", "Lost", "Tied / no result", "Points", "League position")) + '</div>')
    return (f'<div class="page"><div class="in">{title("Fixtures & results", "Season record")}<div class="hd" style="display:flex;flex-direction:column;gap:5px">{row(("Team", 3), ("Season", 1.2), ("Captain", 2.2))}</div>'
            f'<table>{cols}{th}{trs}</table>{tot}</div>{foot()}</div>')

def build():
    return CSS, [cover(), batting(), bowling(), bowling_long(), t20(), partnerships(), fields(), season_table("bat"), season_table("bowl"), fixtures()]

if __name__ == "__main__":
    out = sys.argv[1]
    for size, nm in (("letter-l", "US-Letter"), ("a4-l", "A4")):
        css, pages = build()
        render(css, pages, size, f"{out}/cricket-scorebook-printable-{nm}.pdf")
    print("pages", len(pages))
