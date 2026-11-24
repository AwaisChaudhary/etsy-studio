"""KDP paperback: "Dose by Dose: A GLP-1 Weight Loss Journal" (6x9, B&W, white paper).
Research 24 Nov 2026: 'glp-1 journal' ~1,000 results, top sellers BSR 242k-327k with 1-14 reviews, mostly 6x9, 100-150 pages, ~$8.99-9.99.
Most are weekly-only logbooks; the one critical review said it did not fit the buyer's needs and they moved to a more detailed log.
Autocomplete shows oral GLP-1 ('glp-1 pill tracker') and 'glp 1 for seniors' rising. This book: 26 weeks (the first six months),
works for weekly shots OR daily pills, a site-rotation map, a 0-3 side-effect grid every week, a daily protein/water/fibre/steps
table, a 7-day food log, monthly progress with a weight graph, titration planner and doctor-visit pages.
Tracking only: no doses, targets or medical advice are given; the reader fills in what their care team sets."""
import pathlib, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import kdp

OUT = pathlib.Path("/home/claude/kdp/glp1")
OUT.mkdir(parents=True, exist_ok=True)
TITLE, SUB, BRAND = "Dose by Dose", "A GLP-1 Weight Loss Journal", "Steady Ground Press"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SYMPTOMS = ["Nausea", "Vomiting", "Constipation", "Diarrhoea", "Reflux / burping", "Tired", "Headache", "Dizzy", "Site reaction", "Low appetite"]

CSS = """
body { font-family: 'Bitstream Charter', 'DejaVu Serif', serif; color:#111; }
.lab { font-family: Inter, sans-serif; font-size: 7.2pt; letter-spacing:.03em; color:#222; font-weight:700; }
h2 { font-family: Inter, sans-serif; font-weight: 800; font-size: 13pt; margin: 0 0 5pt; }
h3 { font-family: Inter, sans-serif; font-weight: 700; font-size: 8.2pt; margin: 7pt 0 3pt; }
p { font-size: 9.4pt; line-height: 1.42; margin: 0 0 6pt; }
.line { border-bottom: .6pt solid #777; height: 17pt; }
.line.s { height: 15pt; }
.head { display:flex; justify-content:space-between; align-items:baseline; border-bottom: 1.6pt solid #111; padding-bottom: 3pt; margin-bottom: 6pt; }
.head .d { font-family: Inter, sans-serif; font-weight: 800; font-size: 15pt; }
.head .k { font-family: Inter, sans-serif; font-size: 7pt; color:#444; font-weight:600; letter-spacing:.06em; }
table { border-collapse: collapse; width:100%; font-family: Inter, sans-serif; font-size: 7pt; }
td, th { border: .6pt solid #444; padding: 2pt 3pt; height: 15pt; text-align:left; }
th { font-weight:700; background:#e9e9e9; }
.c { text-align:center; }
.tall td { height: 22pt; }
.sec { border: .7pt solid #222; border-radius: 6pt; padding: 5pt 7pt 6pt; margin-bottom: 6pt; }
.grow { flex:1; }
.row { display:flex; gap: 8pt; }
.row > div { flex:1; }
.cell { font-family: Inter, sans-serif; font-size:7pt; }
.box { display:inline-block; width:8pt; height:8pt; border:.8pt solid #222; margin:0 2pt 0 6pt; vertical-align:-1pt; }
.drops span { display:inline-block; width:7pt; height:9pt; border:.7pt solid #333; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; margin-right:1.5pt; }
.title { flex:1; display:flex; flex-direction:column; justify-content:center; }
.title .big { font-family: 'GFS Baskerville', serif; font-size: 38pt; line-height:1; }
.small { font-size: 7.8pt; line-height:1.4; }
.ideas { columns: 2; column-gap: 14pt; font-size: 8.4pt; line-height: 1.45; }
.ideas div { break-inside: avoid; margin-bottom: 3pt; }
.graph { flex:1; border: .7pt solid #222; background-image: linear-gradient(#bbb .5pt, transparent .5pt), linear-gradient(90deg, #bbb .5pt, transparent .5pt); background-size: 100% 10%, 12.5% 100%; position:relative; min-height: 1.9in; }
.photo { border: .8pt dashed #444; height: 1.55in; display:flex; align-items:flex-end; justify-content:center; padding-bottom:3pt; }
.blank {}
"""


def lines(n, cls=""):
    return "".join(f'<div class="line {cls}"></div>' for _ in range(n))


def esc(s):
    return html.escape(s)


BODY = """<svg viewBox="10 0 180 260" width="100%" height="100%" fill="none" stroke="#111" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round">
<circle cx="100" cy="28" r="18"/><path d="M82 46 L60 58 L46 130 M118 46 L140 58 L154 130 M70 58 L70 140 L76 250 M130 58 L130 140 L124 250 M70 140 L130 140 M100 140 L100 250"/>
<g stroke-dasharray="3 3" stroke-width="1"><rect x="74" y="98" width="22" height="26" rx="4"/><rect x="104" y="98" width="22" height="26" rx="4"/><rect x="72" y="150" width="22" height="34" rx="4"/><rect x="106" y="150" width="22" height="34" rx="4"/>
<rect x="47" y="70" width="17" height="30" rx="4" fill="#fff"/><rect x="136" y="70" width="17" height="30" rx="4" fill="#fff"/><rect x="74" y="127" width="22" height="11" rx="3"/><rect x="104" y="127" width="22" height="11" rx="3"/></g>
<g font-family="Inter" font-size="9" font-weight="700" fill="#111" stroke="none" text-anchor="middle"><text x="85" y="115">1</text><text x="115" y="115">2</text><text x="83" y="171">5</text><text x="117" y="171">6</text><text x="55.5" y="89">7</text><text x="144.5" y="89">8</text><text x="85" y="136">3</text><text x="115" y="136">4</text></g></svg>"""

pages = []
pages.append(f'<div class="title"><div class="big">{TITLE}</div><p style="font-size:14pt;margin-top:8pt">{SUB}</p>'
             '<p>Six months of shots or pills, side effects, protein, water, food, weigh-ins and progress, in one place.</p>'
             '<div class="lab" style="margin-top:34pt">THIS JOURNAL BELONGS TO</div><div class="line" style="width:3.2in"></div>'
             '<div class="lab" style="margin-top:12pt">STARTED ON</div><div class="line" style="width:2in"></div></div>')
pages.append(f'<div style="margin-top:auto" class="small"><p class="small"><b>{TITLE}: {SUB}</b><br>Copyright © 2026 {BRAND}. All rights reserved. No part of this book may be reproduced without permission, except for personal use by the owner of this copy.</p>'
             '<p class="small"><b>Important.</b> This is a tracking journal only. It does not give medical advice, doses, targets or diagnoses. Always follow the instructions of your doctor, nurse or pharmacist about your medication, dose changes, diet and exercise. Write the targets your care team sets for you in the spaces provided.</p>'
             '<p class="small">Contact your doctor or pharmacist if a side effect is severe, does not go away, or worries you. Get urgent medical help for severe stomach pain, signs of an allergic reaction, or if you cannot keep fluids down.</p>'
             '<p class="small">GLP-1 is a general name for a class of medicines. This journal is not connected with any drug maker or brand.</p></div>')
pages.append('<h2>How to use this journal</h2>'
             '<p>The journal covers <b>26 weeks</b>, the first six months. Each week has three pages:</p>'
             '<p><b>1. Weekly check-in.</b> Log your dose (shot or pill), the injection site, your weigh-in and measurements, and rate ten common side effects from 0 to 3 for each day.</p>'
             '<p><b>2. Daily habits.</b> One table for the week: protein, water, fibre, fruit and veg, movement, sleep and bathroom notes.</p>'
             '<p><b>3. Food log.</b> What you ate each day, with space for protein per meal.</p>'
             '<p>Every four weeks there is a <b>monthly progress</b> page with a weight graph, measurements and space for progress photos. At the back are doctor-visit pages, a titration planner, symptom questions and high-protein food ideas.</p>'
             '<p>Bring the journal to your appointments. A written record of doses, side effects and patterns makes those conversations faster and more useful.</p>'
             '<h3>Side-effect scale</h3><table><tr><th class="c">0</th><th class="c">1</th><th class="c">2</th><th class="c">3</th></tr><tr><td class="c">None</td><td class="c">Mild, did not affect my day</td><td class="c">Moderate, changed my plans</td><td class="c">Severe, call my care team</td></tr></table>')
pages.append('<h2>My starting point</h2><table class="tall"><tr><th style="width:40%">Start date</th><td></td></tr><tr><th>Starting weight</th><td></td></tr><tr><th>Height</th><td></td></tr>'
             '<tr><th>Waist</th><td></td></tr><tr><th>Hips</th><td></td></tr><tr><th>Chest</th><td></td></tr><tr><th>Upper arm</th><td></td></tr><tr><th>Thigh</th><td></td></tr><tr><th>Other (blood pressure, A1c, etc.)</th><td></td></tr></table>'
             '<h3>Why I started</h3>' + lines(4) + '<h3>Goals for six months (not just the scale)</h3>' + lines(4) + '<h3>How I will celebrate along the way</h3>' + lines(2))
pages.append('<h2>My medication and care team</h2><table class="tall"><tr><th style="width:40%">Medication</th><td></td></tr><tr><th>Shot or pill</th><td></td></tr><tr><th>Dose day and time</th><td></td></tr><tr><th>How to store it</th><td></td></tr>'
             '<tr><th>Prescriber</th><td></td></tr><tr><th>Phone</th><td></td></tr><tr><th>Pharmacy</th><td></td></tr><tr><th>Dietitian / coach</th><td></td></tr><tr><th>Insurance / refill notes</th><td></td></tr></table>'
             '<h3>Targets my care team set for me</h3><table><tr><th>Protein per day</th><th>Water per day</th><th>Fibre per day</th><th>Movement</th></tr><tr class="tall"><td></td><td></td><td></td><td></td></tr></table>'
             '<h3>Instructions I was given (missed dose, side effects, other)</h3>' + lines(5))
trows = "".join(f"<tr><td class='c'>{a}-{a + 3}</td><td></td><td></td><td></td><td></td></tr>" for a in range(1, 26, 4))
pages.append('<h2>Dose and titration planner</h2><p>Fill in the plan from your prescriber. Change it only as they tell you.</p>'
             f'<table class="tall"><tr><th style="width:14%">Weeks</th><th>Planned dose</th><th>Start date</th><th>Actual dose</th><th>Notes</th></tr>{trows}</table>'
             '<h3>Dose change log</h3>' + "".join('<div class="row"><div class="lab" style="flex:0 0 1in">Date</div><div class="line s"></div></div>' for _ in range(5)))
pages.append('<h2>Injection site map</h2><p>Rotate where you inject each week and write the site number in your weekly check-in. Taking a pill instead? Use the weekly page to log the time you take it and whether you followed the instructions on timing and food.</p>'
             f'<div style="height:4.3in; display:flex; justify-content:center; margin: 4pt 0 8pt">{BODY}</div>'
             '<div class="row"><table><tr><th>Site</th><th>Area</th></tr><tr><td>1</td><td>Belly, left</td></tr><tr><td>2</td><td>Belly, right</td></tr><tr><td>3</td><td>Lower belly, left</td></tr><tr><td>4</td><td>Lower belly, right</td></tr></table>'
             '<table><tr><th>Site</th><th>Area</th></tr><tr><td>5</td><td>Thigh, left</td></tr><tr><td>6</td><td>Thigh, right</td></tr><tr><td>7</td><td>Upper arm, left</td></tr><tr><td>8</td><td>Upper arm, right</td></tr></table></div>'
             '<p class="small" style="margin-top:6pt">Use only the areas your care team showed you.</p>')


def week_page(w):
    sx = "".join(f"<tr><td>{esc(s)}</td>" + "<td></td>" * 7 + "</tr>" for s in SYMPTOMS)
    return (f'<div class="head"><span class="d">Week {w}</span><span class="k">WEEKLY CHECK-IN</span><span class="lab">Dates ______ to ______</span></div>'
            '<div class="sec"><div class="lab">DOSE</div><table><tr><th>Day / date</th><th>Time</th><th>Dose</th><th>Site (1-8) or pill</th><th>Missed or late?</th></tr><tr class="tall"><td></td><td></td><td></td><td></td><td></td></tr></table></div>'
            '<div class="sec"><div class="lab">WEIGH-IN AND MEASUREMENTS</div><table><tr><th>Weight</th><th>Change</th><th>Total lost</th><th>Waist</th><th>Hips</th></tr><tr class="tall"><td></td><td></td><td></td><td></td><td></td></tr></table></div>'
            f'<div class="lab" style="margin:2pt 0 2pt">SIDE EFFECTS (0-3 EACH DAY)</div><table><tr><th></th>{"".join(f"<th class=c>{d}</th>" for d in DAYS)}</tr>{sx}</table>'
            '<div class="row" style="margin-top:6pt"><div><div class="lab">APPETITE THIS WEEK</div><span class="cell"><span class="box"></span>Low<span class="box"></span>Normal<span class="box"></span>High</span></div>'
            '<div><div class="lab">ENERGY</div><span class="cell"><span class="box"></span>Low<span class="box"></span>OK<span class="box"></span>Good</span></div></div>'
            '<div class="lab" style="margin-top:6pt">NON-SCALE WIN</div>' + lines(1, "s") + '<div class="lab" style="margin-top:4pt">NOTE FOR MY CARE TEAM</div>' + lines(2, "s"))


def habits_page(w):
    drops = '<span class="drops">' + "<span></span>" * 8 + "</span>"
    rows = "".join(f"<tr><td><b>{d}</b></td><td></td><td>{drops}</td><td></td><td></td><td></td><td></td><td></td></tr>" for d in DAYS)
    return (f'<div class="head"><span class="d">Week {w}</span><span class="k">DAILY HABITS</span><span class="lab">My targets: protein ____ water ____</span></div>'
            '<table class="tall"><tr><th></th><th>Protein</th><th>Water (glasses)</th><th>Fibre</th><th>Fruit / veg</th><th>Move / steps</th><th>Sleep</th><th>BM</th></tr>' + rows +
            '<tr><td><b>Total</b></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>'
            '<h3>What helped with side effects this week</h3>' + lines(3) + '<h3>Meals that sat well</h3>' + lines(3) + '<h3>Next week I will</h3>' + lines(3))


def food_page(w):
    def f(lbl):
        return f'<div style="display:flex;align-items:flex-end;gap:4pt"><span class="cell" style="flex:0 0 .55in">{lbl}</span><div class="line s" style="flex:1"></div></div>'
    blocks = "".join(f'<div class="sec" style="padding:3pt 7pt 5pt;margin-bottom:4pt"><div class="row" style="align-items:center;margin-bottom:1pt"><div class="lab">{d}</div><div class="lab" style="text-align:right">PROTEIN TODAY ______</div></div>'
                     f'<div class="row"><div>{f("Breakfast")}{f("Lunch")}</div><div>{f("Dinner")}{f("Snacks")}</div></div></div>' for d in DAYS)
    return (f'<div class="head"><span class="d">Week {w}</span><span class="k">FOOD LOG</span><span class="lab">Small plates, protein first</span></div>' + blocks +
            '<h3>Foods that did not agree with me</h3>' + lines(3, "s"))


def month_page(m):
    return (f'<div class="head"><span class="d">Month {m}</span><span class="k">PROGRESS</span><span class="lab">Weeks {4 * m - 3}-{4 * m}</span></div>'
            '<div class="lab">WEIGHT GRAPH (mark each weekly weigh-in)</div><div class="graph"></div>'
            '<div class="row" style="margin-top:6pt"><div class="photo"><span class="lab">PHOTO: FRONT</span></div><div class="photo"><span class="lab">PHOTO: SIDE</span></div></div>'
            '<table style="margin-top:6pt"><tr><th>Weight</th><th>Waist</th><th>Hips</th><th>Chest</th><th>Arm</th><th>Thigh</th></tr><tr class="tall"><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>'
            '<h3>What is working</h3>' + lines(2, "s") + '<h3>Questions for my next appointment</h3>' + lines(2, "s"))


for w in range(1, 27):
    pages += [week_page(w), habits_page(w), food_page(w)]
    if w % 4 == 0 or w == 26:
        pages.append(month_page((w + 3) // 4))
for i in range(1, 7):
    pages.append(f'<h2>Doctor visit notes</h2><table class="tall"><tr><th style="width:30%">Date</th><td></td></tr><tr><th>Who I saw</th><td></td></tr><tr><th>Weight / BP</th><td></td></tr><tr><th>Dose now</th><td></td></tr></table>'
                 '<h3>My questions</h3>' + lines(5) + '<h3>What they said / changes</h3>' + lines(6) + '<h3>Next appointment</h3>' + lines(1))
IDEAS = ["Greek yogurt with berries", "Cottage cheese and fruit", "Eggs: boiled, scrambled or an omelette", "Tuna or salmon pouch", "Chicken breast or thighs", "Turkey slices or meatballs",
         "Lean beef or bison", "Shrimp or white fish", "Tofu, tempeh or edamame", "Lentil or bean soup", "Chickpeas or hummus", "Protein shake or ready-to-drink protein",
         "Cheese sticks or string cheese", "Jerky (check the salt)", "Skyr or kefir", "Bone broth", "Chia pudding", "Peanut or almond butter (small portion)", "Oats made with milk", "Leftover protein from dinner"]
pages.append('<h2>Protein-first food ideas</h2><p>A list to jog your memory on low-appetite days. Choose what fits your plan, allergies and your care team\'s advice.</p><div class="ideas">' +
             "".join(f'<div><span class="box" style="margin-left:0"></span>{esc(x)}</div>' for x in IDEAS) + '</div><h3>My go-to meals</h3>' + lines(8))
srows = "".join("<tr><td></td><td></td><td></td><td></td></tr>" for _ in range(14))
pages.append(f'<h2>Symptom and questions log</h2><table class="tall"><tr><th style="width:18%">Date</th><th>Symptom or question</th><th style="width:14%">0-3</th><th>What I did / was told</th></tr>{srows}</table>')
pages.append('<h2>Six months: looking back</h2>' + "".join(f'<h3>{t}</h3>' + lines(k) for t, k in [("How my body feels now", 4), ("Habits I want to keep", 4), ("What I learned about myself", 4), ("Goals for the next six months", 4)]))
for _ in range(3):
    pages.append('<h2>Notes</h2>' + lines(26))
if len(pages) % 2:
    pages.append('<h2>Notes</h2>' + lines(26))

if __name__ == "__main__":
    prev = [(6, OUT / "p-sites.png"), (7, OUT / "p-week.png"), (8, OUT / "p-habits.png"), (9, OUT / "p-food.png"), (19, OUT / "p-month.png")]
    n = kdp.interior(pages, CSS, 6, 9, OUT / "interior.pdf", inside=0.625, outside=0.5, top=0.5, bottom=0.5, previews=prev)
    (OUT / "pages.txt").write_text(str(n))
    print("pages", n)
