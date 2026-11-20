#!/usr/bin/env python3
"""KDP book 1: RACE READY - Fitness Race Training Log (7 x 10 in, black & white interior, white paper)."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kdp import interior, cover

OUT = pathlib.Path("/home/claude/kdp/race-ready")
OUT.mkdir(parents=True, exist_ok=True)
TW, TH = 7, 10
TITLE = "Race Ready"
SUB = "Fitness Race Training Log"

STATIONS = [("SkiErg", "1,000 m"), ("Sled push", "50 m"), ("Sled pull", "50 m"), ("Burpee broad jumps", "80 m"),
            ("Rowing", "1,000 m"), ("Farmers carry", "200 m"), ("Sandbag lunges", "100 m"), ("Wall balls", "100 reps")]
# Season 26/27 standard weights (checked against two published summaries of the official rulebooks, Nov 2026)
WEIGHTS = [
    ("Women Open", "102 kg", "78 kg", "2 x 16 kg", "10 kg", "4 kg / 2.70 m"),
    ("Men Open", "152 kg", "103 kg", "2 x 24 kg", "20 kg", "6 kg / 3.00 m"),
    ("Women Pro", "152 kg", "103 kg", "2 x 24 kg", "20 kg", "6 kg / 2.70 m"),
    ("Men Pro", "202 kg", "153 kg", "2 x 32 kg", "30 kg", "9 kg / 3.00 m"),
]

CSS = """
* { box-sizing: border-box; }
body { font-family: Inter, sans-serif; color: #111; font-size: 9pt; }
.blank { flex: 1; }
.hd { display: flex; align-items: flex-end; justify-content: space-between; border-bottom: 3pt solid #111; padding-bottom: 4pt; margin-bottom: 10pt; }
.hd h2 { font-family: "Inter Display"; font-weight: 900; font-size: 20pt; letter-spacing: -.02em; margin: 0; text-transform: none; }
.hd span { font-size: 8pt; color: #555; }
h3 { font-family: "Inter Display"; font-weight: 800; font-size: 11pt; margin: 10pt 0 5pt; }
p { margin: 0 0 7pt; line-height: 1.45; }
table { width: 100%; border-collapse: collapse; }
th { background: #111; color: #fff; font-size: 7.5pt; font-weight: 700; text-align: left; padding: 4pt 5pt; }
td { border-bottom: .8pt solid #bbb; padding: 0 5pt; height: .29in; font-size: 8.5pt; }
tr:nth-child(even) td { background: #f2f2f2; }
.lines { flex: 1; background: repeating-linear-gradient(transparent 0 .27in, #bbb .27in calc(.27in + .8pt)); }
.f { border-bottom: .8pt solid #999; height: .3in; display: flex; align-items: flex-end; padding-bottom: 2pt; font-size: 7.5pt; color: #555; font-weight: 600; }
.row { display: grid; gap: 8pt; }
.box { border: 1.2pt solid #111; border-radius: 4pt; padding: 6pt 8pt; }
.lab { font-size: 7pt; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: #333; }
.cb { display: inline-flex; align-items: center; gap: 4pt; margin-right: 9pt; font-size: 8pt; }
.cb i { width: 9pt; height: 9pt; border: 1.2pt solid #111; border-radius: 2pt; display: inline-block; }
.pn { position: absolute; bottom: .3in; font-size: 7pt; color: #777; }
.scale span { display: inline-flex; width: 14pt; height: 14pt; border: 1pt solid #111; border-radius: 50%; align-items: center; justify-content: center; font-size: 7pt; margin-right: 3pt; }
.track { display: flex; gap: 3pt; margin: 6pt 0 10pt; }
.track b { flex: 1; height: 6pt; background: #111; border-radius: 3pt; }
.track b.st { background: repeating-linear-gradient(90deg, #111 0 3pt, transparent 3pt 5pt); border: 1pt solid #111; }
.title { justify-content: center; text-align: center; }
.title .big { font-family: "Inter Display"; font-weight: 900; font-size: 54pt; letter-spacing: -.04em; line-height: .9; }
"""


def hd(t, s=""):
    return f'<div class="hd"><h2>{t}</h2><span>{s}</span></div>'


def f(label, w="1fr"):
    return f'<div class="f">{label}</div>'


def cbs(items):
    return "".join(f'<span class="cb"><i></i>{x}</span>' for x in items)


def scale(n=10):
    return '<div class="scale">' + "".join(f"<span>{i}</span>" for i in range(1, n + 1)) + "</div>"


def track():
    return '<div class="track">' + "".join("<b></b><b class='st'></b>" for _ in range(8)) + "</div>"


def mmss(sec):
    return f"{sec // 60}:{sec % 60:02d}"


pages = []
# 1 title
pages.append(f'<div class="title" style="flex:1;display:flex;flex-direction:column;justify-content:center">{track()}<div class="big">RACE<br>READY</div>'
             f'<p style="font-size:12pt;margin-top:14pt">{SUB}</p><p style="color:#555">8 runs. 8 stations. 12 weeks to your best finish.</p>{track()}</div>')
# 2 copyright
pages.append('<div style="margin-top:auto;font-size:7.5pt;color:#444;line-height:1.5">'
             '<p><b>Race Ready: Fitness Race Training Log</b></p>'
             '<p>Copyright &copy; 2026. All rights reserved. No part of this book may be reproduced without permission, except for personal use of the log pages.</p>'
             '<p>This log is for the popular fitness race format of eight 1 km runs, each followed by a workout station. It is an independent publication and is not affiliated with, sponsored or endorsed by any race organiser. Event names are trademarks of their owners.</p>'
             '<p>Station weights are the published standards for the 2026/27 season. Organisers can change them, so always check the current rulebook for your race.</p>'
             '<p>Talk to a doctor before starting a new training plan. Stop if you feel pain, dizziness or shortness of breath beyond normal effort.</p></div>')
# 3 athlete
pages.append(hd("This log belongs to") + f('Name') + f('Division (Open / Pro / Doubles / Relay)') + f('Age group') + f('Training partner') +
             '<h3>My race</h3>' + f('Race city and date') + f('Goal finish time') + f('Why this matters to me') +
             '<h3>Starting point</h3><div class="row" style="grid-template-columns:1fr 1fr">' + f('5 km run time') + f('Body weight (optional)') + f('Resting heart rate') + f('Longest run in last month') + '</div>'
             '<h3>12-week goals</h3><div class="lines"></div>')
# 4 how to use
pages.append(hd("How to use this log") +
             '<p><b>1. Test.</b> Fill in the benchmark tests in week 1, week 6 and week 12. They show what is improving and where you lose time.</p>'
             '<p><b>2. Plan the week.</b> Each week starts with a planning page: pick your key sessions, then log them on the daily pages.</p>'
             '<p><b>3. Log every session.</b> Write the main set, how hard it felt (RPE 1 to 10) and one note. Patterns appear after a few weeks.</p>'
             '<p><b>4. Review.</b> Every Sunday, score your week and set one focus for the next.</p>'
             '<p><b>5. Race.</b> Use the race-day checklist, then record your splits on the race log pages so your next race is faster.</p>'
             '<h3>RPE scale</h3><table><tr><th>RPE</th><th>Feels like</th></tr>' +
             "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in [("1-3", "Easy. Full conversation."), ("4-5", "Steady. Short sentences."), ("6-7", "Comfortably hard. A few words."), ("8-9", "Hard. Race effort on stations."), ("10", "All out. Final wall balls.")]) +
             '</table><h3>A typical week</h3><p>Two runs (one easy, one with intervals), two strength or station sessions, one long hybrid session that mixes running and stations, and at least one full rest day.</p>')
# 5 format + weights
pages.append(hd("The race at a glance", "Season 2026/27 standards") +
             '<p>You run 1 km, then complete a station, eight times. The station order never changes. Time spent moving between the track and stations (the transition zone) counts too.</p>'
             '<table><tr><th>#</th><th>Run</th><th>Station</th><th>Distance / reps</th></tr>' +
             "".join(f"<tr><td>{i + 1}</td><td>1 km</td><td>{s}</td><td>{d}</td></tr>" for i, (s, d) in enumerate(STATIONS)) + '</table>'
             '<h3>Weights by division</h3><table><tr><th>Division</th><th>Sled push</th><th>Sled pull</th><th>Farmers</th><th>Lunges</th><th>Wall ball / target</th></tr>' +
             "".join("<tr>" + "".join(f"<td>{c}</td>" for c in w) + "</tr>" for w in WEIGHTS) + '</table>'
             '<p style="margin-top:8pt;font-size:8pt;color:#444">Sled weights include the sled. Mixed doubles use the Men Open column for both partners; other doubles and relays use the weights of their category. Check your event\'s current rulebook before you race.</p>')
# 6 pace chart
rows = "".join(f"<tr><td>{mmss(s)}</td><td>{mmss(s * 8)}</td><td>{mmss(s + 10)}</td><td>{mmss((s + 10) * 8)}</td></tr>" for s in range(210, 481, 15))
pages.append(hd("Run pace chart", "8 x 1 km") + '<p>Your race runs come with tired legs. Most athletes run 10 to 30 seconds per km slower than their fresh pace. Use this chart to set a realistic target.</p>'
             '<table><tr><th>Fresh pace /km</th><th>8 km at that pace</th><th>Race pace (+10 s)</th><th>8 km at race pace</th></tr>' + rows + '</table>')
# 7 finish time planner
pages.append(hd("Finish time planner") + '<p>Split your goal time into runs, stations and transitions. Then train the parts that cost the most.</p>' +
             f('Goal finish time') + '<table style="margin-top:8pt"><tr><th>Segment</th><th>Target</th><th>Segment</th><th>Target</th></tr>' +
             "".join(f"<tr><td>Run {i + 1}</td><td></td><td>{s}</td><td></td></tr>" for i, (s, _) in enumerate(STATIONS)) +
             '<tr><td><b>Transitions total</b></td><td></td><td><b>Total</b></td><td></td></tr></table>'
             '<h3>Where I can gain the most time</h3><div class="lines"></div>')
# ---- coaching content (added 20 Nov) ----
TECH = [
 ("SkiErg", "1,000 m", ["Hinge at the hips and drive the handles down with your lats, not just your arms.", "Finish each pull with hands near your thighs, then let the handles rise as you stand tall.",
   "Find a steady rhythm of about 30 to 40 strokes a minute. Long, strong pulls beat fast, short ones."],
  ["Pulling only with the arms", "Starting too fast after run 1"], "3 x 500 m at race effort, 90 s rest. Note your split per 500 m."),
 ("Sled push", "50 m", ["Arms long or bent, low body angle, drive through the balls of your feet.", "Short, quick steps. Keep pushing: restarting a stopped sled costs the most energy.",
   "Look down a few metres ahead, not up the lane."],
  ["Standing too upright", "Big, slow strides that let the sled stop"], "4 x 25 m heavy push, 2 min rest. Add a 400 m run straight after the last one."),
 ("Sled pull", "50 m", ["Sit back into a low squat and pull the rope hand over hand to your hip.", "Brace your core and keep a slight bend in the arms at the end of each pull.",
   "Keep the rope tidy behind you so it doesn't tangle."],
  ["Pulling with straight legs (back takes the load)", "Long rests between pulls"], "5 x 15 m heavy pulls, 90 s rest. Grip work: 3 x 30 s dead hang."),
 ("Burpee broad jumps", "80 m", ["Step back or jump back into the burpee; choose what you can repeat for 80 m.", "Jump forward a comfortable distance. Steady small jumps beat a few big ones followed by rests.",
   "Land soft and go straight into the next rep."],
  ["Huge first jumps, then walking", "Holding your breath"], "EMOM 10 min: 6 burpee broad jumps. Then 1 km run at race pace."),
 ("Rowing", "1,000 m", ["Push with the legs first, then swing the body, then pull the arms. Return in the opposite order.", "Damper around 5 to 7 suits most people. Higher is not faster.",
   "Use this station to settle your breathing after the burpees."],
  ["Pulling with the arms before the legs", "Rushing the slide forward"], "4 x 500 m, 1 min rest, holding the same split each time."),
 ("Farmers carry", "200 m", ["Stand tall, shoulders back and down, short fast steps.", "Squeeze the handles. Grip, not legs, is what usually fails.",
   "If you must put the weights down, rest for 3 to 5 seconds only and pick them up the same way."],
  ["Shrugging and leaning", "Long rests with the weights down"], "4 x 100 m heavy carry, 90 s rest. Finish with a 3 x 45 s plank."),
 ("Sandbag lunges", "100 m", ["Bag high on the shoulders behind the neck, chest up.", "Back knee touches the floor gently on every rep; full hip extension at the top.",
   "Pick a steady count, for example 10 lunges then 3 breaths."],
  ["Short steps that fail the depth standard", "Letting the bag slide forward"], "4 x 25 m walking lunges with the bag, 1 min rest. Then 2 x 1 km run."),
 ("Wall balls", "100 reps", ["Full squat below parallel, then drive up and throw in one motion.", "Catch the ball high and ride it straight down into the next squat.",
   "Plan your sets before the race (see Wall balls: break them up)."],
  ["Unbroken first set, then long rests", "Ball short of the target line (no rep)"], "5 rounds: 20 wall balls + 200 m run. Note how many reps before your first break."),
]
for k in range(0, 8, 2):
    blocks = ""
    for name, dist, cues, errs, drill in TECH[k:k + 2]:
        blocks += (f'<div class="box" style="flex:1;display:flex;flex-direction:column;gap:2pt"><div style="display:flex;justify-content:space-between;align-items:baseline">'
                   f'<h3 style="margin:2pt 0">{name}</h3><span class="lab">{dist}</span></div>'
                   + "".join(f'<p style="margin:0 0 3pt">&bull; {c}</p>' for c in cues)
                   + f'<p style="margin:3pt 0"><b>Common mistakes:</b> {"; ".join(errs)}.</p><p style="margin:0 0 4pt"><b>Training drill:</b> {drill}</p>'
                   + '<div class="f">My best time</div><span class="lab" style="margin-top:4pt">Technique notes</span><div class="lines" style="flex:1;min-height:.5in"></div></div>')
    pages.append(hd("Station technique", f"{k + 1}-{k + 2} of 8") + f'<div style="flex:1;display:flex;flex-direction:column;gap:8pt">{blocks}</div>')
pages.append(hd("Wall balls: break them up", "100 reps") +
             '<p>Wall balls come last, when your legs are tired. Going unbroken until you fail usually leads to long rests later. Pick a plan before race day and practise it.</p>'
             '<table><tr><th>Plan</th><th>Sets</th><th>Rest between sets</th><th>Good for</th></tr>'
             '<tr><td>A</td><td>25 x 4</td><td>5 to 8 breaths</td><td>Strong legs, wall balls practised often</td></tr>'
             '<tr><td>B</td><td>20 x 5</td><td>5 to 8 breaths</td><td>Most athletes</td></tr>'
             '<tr><td>C</td><td>15, 15, 15, 15, 15, 15, 10</td><td>4 to 6 breaths</td><td>First race, newer to squats</td></tr>'
             '<tr><td>D</td><td>10 x 10</td><td>3 to 5 breaths</td><td>Keeping no-reps low when very tired</td></tr></table>'
             '<h3>How to rest</h3><p>Hold the ball at your chest or set it down right in front of you. Count your breaths, not seconds. Start the next set before you feel ready.</p>'
             '<h3>My plan</h3>' + f('Sets') + f('Rest') + '<h3>Practice log</h3><table><tr><th>Date</th><th>Plan used</th><th>Total time</th><th>No-reps</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>" * 12 + '</table><h3>Notes</h3><div class="lines" style="min-height:1.2in"></div>')
pages.append(hd("Your first race: pacing plan") +
             '<p>Most first-timers start too fast. The first 1 km run feels easy on fresh legs and the crowd is loud, so it is easy to run 30 seconds too quick and pay for it at the sled.</p>'
             '<table><tr><th>Part</th><th>Aim</th><th>Effort (RPE)</th></tr>'
             '<tr><td>Run 1</td><td>Slower than you want. You should be able to talk.</td><td>5 to 6</td></tr>'
             '<tr><td>SkiErg, row</td><td>Steady rhythm, settle your breathing.</td><td>6 to 7</td></tr>'
             '<tr><td>Sled push and pull</td><td>Keep moving. Short steps, short rests.</td><td>8</td></tr>'
             '<tr><td>Runs 2 to 6</td><td>Same pace each time. Use the first 200 m to recover.</td><td>6 to 7</td></tr>'
             '<tr><td>Burpees, farmers, lunges</td><td>Planned rhythm, rests of a few breaths only.</td><td>7 to 8</td></tr>'
             '<tr><td>Runs 7 and 8</td><td>Hold pace. Run 8 is the time to empty the tank.</td><td>8 to 9</td></tr>'
             '<tr><td>Wall balls</td><td>Your planned sets. Finish strong.</td><td>9 to 10</td></tr></table>'
             '<h3>Transitions</h3><p>Walk briskly, breathe and drink a sip of water if you need it. Do not stop in the transition zone; small stops add up to minutes.</p>'
             '<h3>My first-race targets</h3>' + f('Run 1 pace') + f('Average run pace') + f('Wall ball plan') + f('Finish time goal') + '<h3>Notes</h3><div class="lines" style="min-height:2in"></div>')
pages.append(hd("Doubles and relay") +
             '<p>Racing with others is a great first step and a lot of fun. Rules differ by event, so check your race\'s rulebook. The common formats work like this:</p>'
             '<h3>Doubles</h3><p>Both partners run every 1 km together. At each station you share the work however you like, for example switching every 250 m on the SkiErg or every 10 wall balls. Only one partner works at a time.</p>'
             '<h3>Relay</h3><p>A team of four. Each athlete does two of the eight run-plus-station legs, then tags the next team member.</p>'
             '<h3>Our split plan</h3><table><tr><th>Station</th><th>How we split it</th><th>Who starts</th></tr>' +
             "".join(f"<tr><td>{s}</td><td></td><td></td></tr>" for s, _ in STATIONS) + '</table>'
             '<h3>Team notes</h3><div class="lines" style="min-height:2.6in"></div>')
PLAN = [
 ("1", "Base + test", "Benchmark tests. Easy 5 km run.", "40 min easy run + 3 stations at easy effort"),
 ("2", "Base", "6 x 400 m run, 90 s rest", "45 min hybrid: 4 x (1 km run + 1 station)"),
 ("3", "Build", "5 x 800 m at goal race pace", "50 min hybrid: 5 x (1 km + station)"),
 ("4", "Easier week", "Easy runs only, technique work", "30 min easy run"),
 ("5", "Build", "4 x 1 km at race pace + 20 wall balls after each", "Half race simulation (4 runs + 4 stations)"),
 ("6", "Build + retest", "Retest benchmarks", "60 min hybrid, steady effort"),
 ("7", "Strength focus", "Heavy sled push and pull, 5 sets", "6 x (1 km + station) at race pace"),
 ("8", "Easier week", "Easy runs, mobility", "35 min easy run"),
 ("9", "Race practice", "8 x 1 km at race pace, 1 min rest", "Full race simulation at 80% effort"),
 ("10", "Sharpen", "Race-order stations, short rests", "5 x (1 km + 2 stations)"),
 ("11", "Taper", "3 x 1 km at race pace", "30 min easy + 2 stations, light"),
 ("12", "Race week", "Retest only what you need; 2 easy runs", "RACE DAY"),
]
pages.append(hd("Your 12-week plan", "A suggested plan, adjust to you") +
             '<p>A simple plan for most athletes training 4 to 5 times a week. Add one or two strength sessions each week (squats, lunges, deadlifts, pulls). Easier weeks let your body adapt.</p>'
             '<table><tr><th style="width:9%">Wk</th><th style="width:18%">Phase</th><th>Key session</th><th>Long session</th></tr>' +
             "".join(f"<tr style='height:.47in'><td style='height:.47in'>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in PLAN) + '</table>'
             '<p style="margin-top:6pt;font-size:8pt;color:#444">Copy each week\'s key and long session onto that week\'s planning page.</p>')
pages.append(hd("Exercise library", "Strength that carries over") +
             '<table><tr><th>Exercise</th><th>Helps with</th><th>Typical sets</th></tr>' +
             "".join(f"<tr style='height:.34in'><td style='height:.34in'>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in [
                 ("Back or front squat", "Wall balls, lunges, sled push", "4 x 6-8"), ("Walking lunges", "Sandbag lunges", "3 x 20 steps"),
                 ("Romanian deadlift", "Sled pull, rowing, farmers carry", "3 x 8"), ("Sled push / heavy prowler", "Sled push", "5 x 20 m"),
                 ("Bent-over row", "Sled pull, SkiErg, rowing", "3 x 10"), ("Pull-ups or lat pulldown", "SkiErg, sled pull", "3 x 8"),
                 ("Farmers hold", "Farmers carry grip", "3 x 45 s"), ("Thrusters", "Wall balls", "4 x 10"),
                 ("Box step-ups", "Lunges, running", "3 x 10 each leg"), ("Plank / side plank", "Every station", "3 x 45 s"),
                 ("Burpees", "Burpee broad jumps", "EMOM 8-10 min"), ("Calf raises", "Running, sled push", "3 x 15")]) + '</table>'
             '<h3>Notes</h3><div class="lines"></div>')
# 8-9 benchmarks
bench = ["1 km run (fresh)", "5 km run", "1,000 m SkiErg", "1,000 m row", "50 m sled push (race weight)", "50 m sled pull (race weight)",
         "80 m burpee broad jumps", "200 m farmers carry", "100 m sandbag lunges", "100 wall balls", "Half race simulation (4 runs + 4 stations)"]
for part in (bench[:6], bench[6:]):
    pages.append(hd("Benchmark tests", "Week 1 · Week 6 · Week 12") + '<table><tr><th>Test</th><th>Week 1</th><th>Week 6</th><th>Week 12</th></tr>' +
                 "".join(f"<tr style='height:.55in'><td style='height:.55in'>{t}</td><td></td><td></td><td></td></tr>" for t in part) + '</table>'
                 '<h3>Notes</h3><div class="lines"></div>')
# 10 12-week overview
pages.append(hd("12-week overview") + '<table><tr><th>Week</th><th>Focus</th><th>Key session</th><th>Long session</th><th>Done</th></tr>' +
             "".join(f"<tr style='height:.48in'><td style='height:.48in'>{w}</td><td></td><td></td><td></td><td></td></tr>" for w in range(1, 13)) + '</table>'
             '<p style="margin-top:8pt;font-size:8pt;color:#444">Build for three weeks, then ease off in week 4. Repeat twice, then taper in weeks 11 to 12.</p>')


def day_block(label):
    return (f'<div class="box" style="flex:1;display:flex;flex-direction:column;gap:3pt">'
            f'<div style="display:flex;justify-content:space-between"><span class="lab">{label}</span><span class="lab">Date ______</span></div>'
            f'<div>{cbs(["Run", "Strength", "Stations", "Hybrid", "Rest"])}</div>'
            '<table><tr><th style="width:38%">Exercise / run</th><th>Sets x reps</th><th>Weight</th><th>Time / pace</th></tr>' + "<tr><td></td><td></td><td></td><td></td></tr>" * 7 + '</table>'
            f'<div style="display:flex;gap:10pt;align-items:center"><span class="lab">RPE</span>{scale()}</div>'
            '<span class="lab">Note</span><div class="lines" style="min-height:.6in"></div></div>')


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for w in range(1, 13):
    pages.append(hd(f"Week {w}", "Plan") + '<div class="row" style="grid-template-columns:1fr 1fr">' + f('Focus this week') + f('Target km run') + '</div>'
                 '<table style="margin-top:8pt"><tr><th>Day</th><th>Planned session</th><th>Done</th></tr>' +
                 "".join(f"<tr style='height:.42in'><td style='height:.42in'>{d}</td><td></td><td></td></tr>" for d in days) + '</table>'
                 '<h3>Sleep and recovery</h3><table><tr><th></th>' + "".join(f"<th>{d[:3]}</th>" for d in days) + '</tr>' +
                 "".join(f"<tr><td>{r}</td>" + "<td></td>" * 7 + "</tr>" for r in ("Sleep (h)", "Energy 1-5", "Soreness 1-5")) + '</table><h3>Key workout details</h3><div class="lines"></div>')
    for a, b in ((0, 1), (2, 3), (4, 5)):
        pages.append(hd(f"Week {w}", f"{days[a]} · {days[b]}") + '<div style="flex:1;display:flex;flex-direction:column;gap:8pt">' + day_block(days[a]) + day_block(days[b]) + '</div>')
    pages.append(hd(f"Week {w}", "Sunday · Review") + '<div style="flex:1;display:flex;flex-direction:column;gap:8pt">' + day_block("Sunday") +
                 '<div class="box" style="flex:1;display:flex;flex-direction:column;gap:4pt"><span class="lab">Week review</span>'
                 '<div style="display:flex;gap:10pt;align-items:center"><span class="lab">Week score</span>' + scale() + '</div>' +
                 '<div class="f">Best session</div><div class="f">What got in the way</div><div class="f">One focus for next week</div></div></div>')
# race logs
for r in range(1, 7):
    pages.append(hd(f"Race {r}", "Details") + '<div class="row" style="grid-template-columns:1fr 1fr">' + f('Race / city') + f('Date') + f('Division') + f('Start time') +
                 f('Goal time') + f('Finish time') + f('Overall place') + f('Age group place') + '</div>'
                 '<h3>Race plan</h3><div class="lines" style="flex:.6"></div><h3>How it went</h3><div class="lines"></div>')
    pages.append(hd(f"Race {r}", "Splits") + '<table><tr><th>Segment</th><th>Target</th><th>Actual</th><th>+/-</th></tr>' +
                 "".join(f"<tr><td>Run {i + 1}</td><td></td><td></td><td></td></tr><tr><td>{s}</td><td></td><td></td><td></td></tr>" for i, (s, _) in enumerate(STATIONS)) +
                 '<tr><td><b>Transitions</b></td><td></td><td></td><td></td></tr><tr><td><b>Total</b></td><td></td><td></td><td></td></tr></table>'
                 '<h3>Next time I will</h3><div class="lines"></div>')
# PRs + checklists
pages.append(hd("Personal records") + '<table><tr><th>Event</th><th>Best</th><th>Date</th><th>Best</th><th>Date</th></tr>' +
             "".join(f"<tr style='height:.4in'><td style='height:.4in'>{t}</td><td></td><td></td><td></td><td></td></tr>" for t in bench + ["Full race"]) + '</table>')
pack = ["Race ticket / QR code", "Photo ID", "Shoes (tested in training)", "Spare socks", "Gloves for sled and rope (if allowed)", "Chalk (check rules)",
        "Water bottle", "Pre-race snack", "Energy gel", "Warm layer for waiting", "Towel", "Change of clothes", "Recovery drink", "Headphones for warm-up", "Plasters / tape"]
plan = ["Eat a familiar meal 3 hours before", "Arrive 60 minutes early", "Find your start pen and the station order", "Warm up: 10 min easy jog + drills",
        "Start the first run slower than you want to", "Breathe through the transitions", "Break wall balls into planned sets", "Finish strong: smile for the photo"]
pages.append(hd("Race-day checklist") + '<h3>Pack</h3>' + "".join(f'<div style="padding:3pt 0;border-bottom:.8pt solid #ddd">{cbs([x])}</div>' for x in pack) +
             '<h3>On the day</h3>' + "".join(f'<div style="padding:3pt 0;border-bottom:.8pt solid #ddd">{cbs([x])}</div>' for x in plan))
while len(pages) < 108:
    pages.append(hd("Notes") + '<div class="lines"></div>')

# page numbers (skip title + copyright)
pages = [p + (f'<span class="pn" style="{"right" if i % 2 == 0 else "left"}:.45in">{i + 1}</span>' if i > 1 else "") for i, p in enumerate(pages)]
n = interior(pages, CSS, TW, TH, OUT / "race-ready-interior.pdf",
             previews=[(i, OUT / f"int-{i + 1:03d}.png") for i in (0, 12, 75, 90)])
print("interior pages", n)

COVER_CSS = """
body { font-family: Inter, sans-serif; }
.wrap { background: #121418; color: #fff; }
.front, .back { display:flex; flex-direction:column; }
.kick { font-weight: 700; font-size: 11pt; letter-spacing: .22em; text-transform: uppercase; color: #d4f53c; }
.big { font-family: "Inter Display"; font-weight: 900; font-size: 96pt; line-height: .82; letter-spacing: -.05em; margin: 16pt 0 0; }
.big em { font-style: normal; color: #d4f53c; }
.sub { font-size: 17pt; font-weight: 600; margin-top: 18pt; line-height: 1.2; }
.lane { margin-top: auto; display:grid; grid-template-columns: repeat(8, 1fr); gap: 5pt; }
.lane div { display:flex; flex-direction:column; gap:5pt; }
.lane b { height: 1.25in; border-radius: 6pt; background: #2a2e36; position: relative; }
.lane b.run { background: #d4f53c; height: .5in; }
.lane span { font-size: 6.6pt; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: #aab; text-align: center; line-height: 1.15; min-height: 16pt; }
.feat { margin-top: 18pt; display: grid; gap: 6pt; font-size: 10.5pt; }
.feat div::before { content: ""; display:inline-block; width:8pt; height:8pt; background:#d4f53c; border-radius:2pt; margin-right:8pt; }
.blurb { font-size: 11pt; line-height: 1.5; color: #dde; }
.barcode { display:none; }
.spine-t { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; writing-mode: vertical-rl; font-family:"Inter Display"; font-weight:900; font-size: 10pt; letter-spacing:.12em; color:#d4f53c; white-space:nowrap; }
"""
lane = "".join(f'<div><b class="run"></b><b></b><span>{s}</span></div>' for s, _ in STATIONS)
front = (f'<div class="kick" style="margin-top:.35in">Fitness race training log</div><div class="big">RACE<br><em>READY</em></div>'
         f'<div class="sub">8 runs. 8 stations.<br>12 weeks to your best finish.</div><div class="lane">{lane}</div>')
back = ('<div class="kick" style="margin-top:.35in">Train smarter for race day</div>'
        '<p class="blurb" style="margin-top:12pt">Eight 1 km runs. Eight stations. One finish line. Race Ready is the training log built for fitness racing: plan every week, track every session, and see exactly where you are gaining time.</p>'
        '<div class="feat"><div>12-week plan with weekly planning and review pages</div><div>Daily session logs with sets, weights, pace and RPE</div>'
        '<div>Benchmark tests for every station, at week 1, 6 and 12</div><div>Run pace chart and finish-time planner</div>'
        '<div>Season 2026/27 station weights for every division</div><div>6 race logs with full split sheets</div><div>Race-day packing and pacing checklist</div></div>'
        '<p class="blurb" style="margin-top:16pt;font-size:9pt;color:#99a">7 x 10 in · 108 pages · Independent publication, not affiliated with any race organiser.</p>'
        '<div class="barcode"></div>')
spine = '<div class="spine-t">RACE READY · TRAINING LOG</div>'
info = cover(front, back, spine, COVER_CSS, TW, TH, n, OUT / "race-ready-cover.pdf", preview=OUT / "cover.png")
print(info)
