"""2027 Workout Planner & Fitness Tracker Spreadsheet (batch 11, lane b): setup (units, goal, weekly target); exercise library
(70 exercises by muscle group + equipment); weekly split planner; strength log with volume, estimated 1-rep max (Epley) and an
automatic NEW PR flag; personal records table; cardio log with pace; body measurements; a 365-day 2027 colour-in calendar that
fills in on workout days; streaks (current + longest), weekly totals and a dashboard with charts. Excel + Google Sheets."""
import sys, datetime as dt; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule, FormulaRule, DataBarRule, ColorScaleRule
from openpyxl.utils import get_column_letter as gl
from openpyxl.chart import BarChart, LineChart, Reference

t = Theme("22304A", "E0603A", "EEF1F6")
wb = Workbook()
NL, NC, NB = 3000, 800, 200
LE, CE, BE = NL + 5, NC + 5, NB + 5
GREY = "6A6F7D"
orng = PatternFill("solid", fgColor="E0603A"); peach = PatternFill("solid", fgColor="FBD9CB"); grn = PatternFill("solid", fgColor="E3F0E1")
GRNF = Font(name=F, bold=True, color="2E6B3A")
YEAR = 2027

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "2027 Workout Planner & Fitness Tracker", "Plan your week, log every set, watch your PRs climb and colour in a whole year of workouts.", 6)
widths(s, {"A": 6, "B": 104})
steps = ["Setup: your name, kg or lb, km or miles, your weekly workout target and up to 3 goals.",
         "Exercises: 70 exercises by muscle group and equipment are ready to use. Add your own at the bottom.",
         "Weekly Plan: your split (Push / Pull / Legs, Upper / Lower, Full body...) with up to 6 exercises per day and target sets x reps.",
         "Strength Log: one row per exercise: sets, reps and weight. Volume and estimated 1-rep max are worked out; NEW PR lights up when you beat your best.",
         "Cardio Log: runs, rides, swims, walks and classes with minutes, distance and pace. Body: weigh-ins and measurements, if you track them.",
         "2027 Calendar: every day you log a workout colours itself in. Dashboard: streaks, workouts this week and month, PRs and charts."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 32
legend(s, 12, 2)
label(s, "B14", "Estimated 1-rep max uses the Epley formula (weight x (1 + reps / 30)). It's an estimate for tracking progress, not a target to test.", size=10, color=GREY)
label(s, "B15", "This is a tracking tool, not medical advice. Start where you are, progress gradually and check with a doctor before starting a new programme.", size=10, color=GREY)
label(s, "B16", "Example workouts are included so you can see how it works: delete them when you start. Works in Excel and Google Sheets.", italic=True, size=10)

# ---------- Setup ----------
su = wb.create_sheet("Setup")
banner(su, t, "Setup", "Fill these in first.", 4)
widths(su, {"A": 30, "B": 40})
rows = [("Name", "Sam"), ("Weight unit", "kg"), ("Distance unit", "km"), ("Workouts per week (target)", 4), ("Year", YEAR),
        ("Goal 1", "Squat 100 kg for 5"), ("Goal 2", "Run 10 km under 55 min"), ("Goal 3", "Train 4x a week all year")]
for i, (a, v) in enumerate(rows):
    r = 5 + i; label(su, f"A{r}", a, bold=True); inp(su, f"B{r}", v).alignment = Alignment(horizontal="left", indent=1)
dv_list(su, "B6", "kg,lb"); dv_list(su, "B7", "km,miles")
WU, DU, WT = "Setup!$B$6", "Setup!$B$7", "Setup!$B$8"
label(su, "A14", "The year is fixed at 2027 for the colour-in calendar; everything else works for any dates.", italic=True, size=9, color=GREY)

# ---------- Exercises ----------
exs = wb.create_sheet("Exercises")
banner(exs, t, "Exercise library", "Pick these from drop-downs in the Weekly Plan and Strength Log. Add your own at the bottom.", 5)
header(exs, 5, ["Exercise", "Muscle group", "Equipment", "Type", "Times logged"], t)
for i, w in enumerate([30, 16, 16, 12, 12]): exs.column_dimensions[gl(i + 1)].width = w
LIB = {"Chest": [("Barbell bench press", "Barbell"), ("Incline dumbbell press", "Dumbbell"), ("Dumbbell bench press", "Dumbbell"), ("Push-up", "Bodyweight"),
                 ("Cable fly", "Cable"), ("Machine chest press", "Machine"), ("Dips", "Bodyweight")],
       "Back": [("Deadlift", "Barbell"), ("Barbell row", "Barbell"), ("Pull-up", "Bodyweight"), ("Chin-up", "Bodyweight"), ("Lat pulldown", "Cable"),
                ("Seated cable row", "Cable"), ("One-arm dumbbell row", "Dumbbell"), ("Face pull", "Cable"), ("Back extension", "Bodyweight")],
       "Legs": [("Back squat", "Barbell"), ("Front squat", "Barbell"), ("Romanian deadlift", "Barbell"), ("Leg press", "Machine"), ("Walking lunge", "Dumbbell"),
                ("Bulgarian split squat", "Dumbbell"), ("Goblet squat", "Kettlebell"), ("Leg extension", "Machine"), ("Leg curl", "Machine"), ("Calf raise", "Machine"),
                ("Step-up", "Dumbbell")],
       "Glutes": [("Hip thrust", "Barbell"), ("Glute bridge", "Bodyweight"), ("Cable kickback", "Cable"), ("Hip abduction", "Machine"), ("Kettlebell swing", "Kettlebell")],
       "Shoulders": [("Overhead press", "Barbell"), ("Seated dumbbell press", "Dumbbell"), ("Lateral raise", "Dumbbell"), ("Rear delt fly", "Dumbbell"),
                     ("Arnold press", "Dumbbell"), ("Upright row", "Cable")],
       "Arms": [("Barbell curl", "Barbell"), ("Dumbbell curl", "Dumbbell"), ("Hammer curl", "Dumbbell"), ("Triceps pushdown", "Cable"),
                ("Overhead triceps extension", "Dumbbell"), ("Skull crusher", "Barbell"), ("Close-grip bench press", "Barbell")],
       "Core": [("Plank", "Bodyweight"), ("Hanging leg raise", "Bodyweight"), ("Cable crunch", "Cable"), ("Russian twist", "Bodyweight"), ("Dead bug", "Bodyweight"),
                ("Ab wheel rollout", "Other"), ("Side plank", "Bodyweight"), ("Pallof press", "Cable")],
       "Full body": [("Clean and press", "Barbell"), ("Thruster", "Dumbbell"), ("Burpee", "Bodyweight"), ("Farmer's carry", "Dumbbell"), ("Turkish get-up", "Kettlebell"),
                     ("Sled push", "Other"), ("Wall ball", "Other")],
       "Cardio": [("Running", "None"), ("Cycling", "Bike"), ("Rowing", "Rower"), ("Swimming", "Pool"), ("Walking", "None"), ("Elliptical", "Machine"),
                  ("Stair climber", "Machine"), ("Jump rope", "Rope"), ("HIIT class", "Other"), ("Yoga", "Mat"), ("Pilates", "Mat")]}
r = 6
for grp, items in LIB.items():
    for name, eq in items:
        inp(exs, f"A{r}", name).alignment = Alignment(horizontal="left", indent=1); inp(exs, f"B{r}", grp); inp(exs, f"C{r}", eq)
        inp(exs, f"D{r}", "Cardio" if grp == "Cardio" else "Strength")
        r += 1
NEX = r - 6
for i in range(30):
    for col in "ABCD": inp(exs, f"{col}{r + i}")
    exs[f"A{r + i}"].alignment = Alignment(horizontal="left", indent=1)
EXE = r + 29
for rr in range(6, EXE + 1):
    calc(exs, f"E{rr}", f'=IF(A{rr}="","",COUNTIF(\'Strength Log\'!$C$6:$C${LE},A{rr})+COUNTIF(\'Cardio Log\'!$B$6:$B${CE},A{rr}))', "0")
dv_list(exs, f"B6:B{EXE}", ",".join(LIB.keys())); dv_list(exs, f"D6:D{EXE}", "Strength,Cardio")
exs.freeze_panes = "A6"
EXL = f"=Exercises!$A$6:$A${EXE}"

# ---------- Weekly Plan ----------
wp = wb.create_sheet("Weekly Plan")
banner(wp, t, "Weekly plan", "Your split. Type a workout name for each day (or Rest), then up to 6 exercises with target sets x reps.", 9)
widths(wp, {"A": 14, "B": 22, "C": 28, "D": 8, "E": 9, "F": 12, "G": 24})
header(wp, 5, ["Day", "Workout", "Exercise", "Sets", "Reps", "Rest (sec)", "Notes"], t)
PLAN = {"Monday": ("Push", [("Barbell bench press", 4, "6-8", 120), ("Overhead press", 3, "8", 90), ("Incline dumbbell press", 3, "10", 90), ("Lateral raise", 3, "12-15", 60), ("Triceps pushdown", 3, "12", 60)]),
        "Tuesday": ("Pull", [("Deadlift", 3, "5", 180), ("Pull-up", 4, "6-10", 120), ("Seated cable row", 3, "10", 90), ("Face pull", 3, "15", 60), ("Hammer curl", 3, "12", 60)]),
        "Wednesday": ("Easy run", [("Running", 1, "30 min", None)]),
        "Thursday": ("Legs", [("Back squat", 4, "5", 180), ("Romanian deadlift", 3, "8", 120), ("Bulgarian split squat", 3, "10", 90), ("Leg curl", 3, "12", 60), ("Calf raise", 4, "12", 60), ("Plank", 3, "45 s", 45)]),
        "Friday": ("Rest", []), "Saturday": ("Full body", [("Hip thrust", 4, "8", 120), ("Clean and press", 3, "5", 120), ("Farmer's carry", 3, "40 m", 90), ("Hanging leg raise", 3, "10", 60)]),
        "Sunday": ("Long walk", [("Walking", 1, "60 min", None)])}
r = 6; DAYROWS = {}
for day, (wk, items) in PLAN.items():
    start = r
    for k in range(6):
        wp[f"A{r}"] = day if k == 0 else None; wp[f"A{r}"].font = Font(name=F, bold=True, color=t.main)
        inp(wp, f"B{r}", wk if k == 0 else None).alignment = Alignment(horizontal="left", indent=1)
        it = items[k] if k < len(items) else (None, None, None, None)
        inp(wp, f"C{r}", it[0]).alignment = Alignment(horizontal="left", indent=1); inp(wp, f"D{r}", it[1]); inp(wp, f"E{r}", it[2]); inp(wp, f"F{r}", it[3]); inp(wp, f"G{r}")
        wp[f"A{r}"].fill = t.band
        r += 1
    DAYROWS[day] = start
    for col in "ABCDEFG": wp[f"{col}{r - 1}"].border = Border(left=thin, right=thin, top=thin, bottom=Side(style="medium", color=t.main))
dv_list(wp, f"C6:C{r - 1}", EXL)
wp.freeze_panes = "A6"
label(wp, "I5", "Tip: progressive overload = add a rep or a little weight when you hit the top of your rep range on every set.", italic=True, size=10, color="9A3B1E")
wp.merge_cells("I5:L8"); widths(wp, {"I": 14, "J": 14, "K": 14, "L": 14})

# ---------- Strength Log ----------
sl = wb.create_sheet("Strength Log")
banner(sl, t, "Strength log", "One row per exercise per session. Type the date, exercise, sets, reps and weight.", 13)
header(sl, 5, ["Date", "Workout", "Exercise", "Sets", "Reps (per set)", "Weight", "VOLUME", "EST. 1RM", "BEST SO FAR", "PR?", "Effort (RPE 1-10)", "Muscle group", "Notes"], t)
for i, w in enumerate([12, 14, 26, 7, 10, 10, 11, 11, 12, 10, 10, 13, 24]): sl.column_dimensions[gl(i + 1)].width = w
sl.freeze_panes = "D6"
for r in range(6, LE + 1):
    for col in "ABCDEFKM": inp(sl, f"{col}{r}")
    for col in "BCM": sl[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sl[f"A{r}"].number_format = "ddd d mmm"; sl[f"F{r}"].number_format = "0.0"
    calc(sl, f"G{r}", f'=IF(OR(D{r}="",E{r}=""),"",D{r}*E{r}*N(F{r}))', "#,##0")
    calc(sl, f"H{r}", f'=IF(OR(E{r}="",N(F{r})=0),"",IF(E{r}=1,F{r},F{r}*(1+E{r}/30)))', "0.0", bold=True)
    if r == 6:
        calc(sl, f"I{r}", f'=IF(H{r}="","",H{r})', "0.0")
        calc(sl, f"J{r}", f'=IF(H{r}="","","First")')
    else:
        # best est. 1RM for this exercise in all rows above, then flag a new best
        calc(sl, f"I{r}", f'=IF(H{r}="","",MAX(H{r},_xlfn.MAXIFS(H$6:H{r - 1},C$6:C{r - 1},C{r})))', "0.0")
        calc(sl, f"J{r}", f'=IF(H{r}="","",IF(COUNTIF(C$6:C{r - 1},C{r})=0,"First",IF(H{r}>_xlfn.MAXIFS(H$6:H{r - 1},C$6:C{r - 1},C{r}),"NEW PR","")))')
    calc(sl, f"L{r}", f'=IF(C{r}="","",IFERROR(INDEX(Exercises!$B$6:$B${EXE},MATCH(C{r},Exercises!$A$6:$A${EXE},0)),""))')
dv_list(sl, f"C6:C{LE}", EXL)
sl.conditional_formatting.add(f"J6:J{LE}", CellIsRule(operator="equal", formula=['"NEW PR"'], fill=orng, font=Font(name=F, bold=True, color="FFFFFF")))
sl.conditional_formatting.add(f"K6:K{LE}", ColorScaleRule(start_type="num", start_value=1, start_color="E3F0E1", end_type="num", end_value=10, end_color="F4B9A3"))
# example log: 6 weeks of a 4-day split, progressing
base = dt.date(2027, 1, 4)
LOG = []
prog = {"Barbell bench press": (60, 2.5, 4, 8), "Overhead press": (37.5, 1.25, 3, 8), "Lateral raise": (8, 0, 3, 14), "Deadlift": (100, 5, 3, 5), "Pull-up": (0, 0, 4, 7),
        "Seated cable row": (50, 2.5, 3, 10), "Back squat": (80, 2.5, 4, 5), "Romanian deadlift": (70, 2.5, 3, 8), "Leg curl": (35, 0, 3, 12), "Hip thrust": (90, 5, 4, 8),
        "Hanging leg raise": (0, 0, 3, 10)}
days = [(0, "Push", ["Barbell bench press", "Overhead press", "Lateral raise"]), (1, "Pull", ["Deadlift", "Seated cable row"]),
        (3, "Legs", ["Back squat", "Romanian deadlift", "Leg curl"]), (5, "Full body", ["Hip thrust", "Hanging leg raise"])]
for wk in range(6):
    for off, wname, exl in days:
        if wk == 3 and off == 5: continue   # a missed day
        for exn in exl:
            w0, inc_, sets, reps = prog[exn]
            w = w0 + inc_ * wk - (inc_ if wk == 4 and exn == "Back squat" else 0)
            LOG.append((base + dt.timedelta(days=7 * wk + off), wname, exn, sets, reps, w if w else None, [7, 7, 8, 8, 9, 8][wk]))
for i, row in enumerate(LOG):
    r = 6 + i
    for col, val in zip("ABCDEFK", row):
        if val is not None: sl[f"{col}{r}"] = val
SL = lambda c: f"'Strength Log'!${c}$6:${c}${LE}"

# ---------- Cardio Log ----------
cl = wb.create_sheet("Cardio Log")
banner(cl, t, "Cardio log", "Runs, rides, swims, walks and classes. Pace is worked out for you.", 10)
header(cl, 5, ["Date", "Activity", "Minutes", "Distance", "PACE (min per unit)", "SPEED (per hour)", "Avg heart rate", "Effort (1-10)", "How it felt", "Notes"], t)
for i, w in enumerate([12, 18, 9, 10, 12, 11, 10, 9, 18, 24]): cl.column_dimensions[gl(i + 1)].width = w
cl.freeze_panes = "B6"
for r in range(6, CE + 1):
    for col in "ABCDGHIJ": inp(cl, f"{col}{r}")
    for col in "BIJ": cl[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    cl[f"A{r}"].number_format = "ddd d mmm"; cl[f"D{r}"].number_format = "0.00"
    calc(cl, f"E{r}", f'=IF(OR(N(C{r})=0,N(D{r})=0),"",C{r}/D{r}/1440)', "[m]:ss")
    calc(cl, f"F{r}", f'=IF(OR(N(C{r})=0,N(D{r})=0),"",D{r}/(C{r}/60))', "0.0")
dv_list(cl, f"B6:B{CE}", EXL); dv_list(cl, f"I6:I{CE}", "Great,Good,OK,Tough,Awful")
for i, (o, act, mins, dist, hr, eff, felt) in enumerate([(2, "Running", 30, 5.0, 148, 5, "Good"), (6, "Walking", 60, 5.4, 102, 2, "Great"), (9, "Running", 32, 5.4, 150, 6, "Good"),
        (13, "Walking", 55, 5.0, 100, 2, "Great"), (16, "Running", 35, 6.0, 151, 6, "OK"), (20, "Cycling", 45, 18.5, 132, 5, "Good"), (23, "Running", 38, 6.6, 149, 6, "Good"),
        (27, "Yoga", 40, None, None, 3, "Great"), (30, "Running", 41, 7.2, 152, 7, "Tough"), (34, "Walking", 60, 5.6, 104, 2, "Great"), (37, "Running", 44, 8.0, 150, 7, "Good")]):
    r = 6 + i; cl[f"A{r}"] = base + dt.timedelta(days=o); cl[f"B{r}"] = act; cl[f"C{r}"] = mins
    if dist: cl[f"D{r}"] = dist
    if hr: cl[f"G{r}"] = hr
    cl[f"H{r}"] = eff; cl[f"I{r}"] = felt
CL = lambda c: f"'Cardio Log'!${c}$6:${c}${CE}"

# ---------- Body ----------
bd = wb.create_sheet("Body")
banner(bd, t, "Body & wellbeing", "Optional: track only what helps you. Sleep and energy matter as much as the scale.", 10)
header(bd, 5, ["Date", "Body weight", "Change", "Waist", "Hips", "Chest", "Arm", "Thigh", "Sleep (hrs avg)", "Energy (1-5)", "Notes"], t)
for i, w in enumerate([12, 11, 9, 9, 9, 9, 9, 9, 10, 10, 26]): bd.column_dimensions[gl(i + 1)].width = w
for r in range(6, BE + 1):
    for col in "ABDEFGHIJK": inp(bd, f"{col}{r}")
    bd[f"A{r}"].number_format = "d mmm yyyy"; bd[f"K{r}"].alignment = Alignment(horizontal="left", indent=1)
    calc(bd, f"C{r}", f'=IF(OR(B{r}="",r_prev),"",B{r}-LOOKUP(2,1/(B$5:B{r - 1}<>""),B$5:B{r - 1}))'.replace("r_prev", f'COUNT(B$5:B{r - 1})=0'), "+0.0;-0.0;0.0")
for i, (o, w, wa, sl_, en) in enumerate([(0, 78.4, 86, 7.0, 3), (14, 78.0, 85.5, 7.2, 4), (28, 77.6, 85, 7.4, 4), (42, 77.9, 84.5, 7.1, 4)]):
    r = 6 + i; bd[f"A{r}"] = base + dt.timedelta(days=o - 1); bd[f"B{r}"] = w; bd[f"D{r}"] = wa; bd[f"I{r}"] = sl_; bd[f"J{r}"] = en

# ---------- Days (helper) ----------
dy = wb.create_sheet("Days")
banner(dy, t, "Days", "Helper for the calendar and streaks. No need to edit.", 6)
header(dy, 5, ["Date", "Strength", "Cardio", "WORKED OUT", "Streak", "Week start"], t)
for i, w in enumerate([13, 10, 10, 12, 9, 13]): dy.column_dimensions[gl(i + 1)].width = w
D0 = 6; ND = 365
for k in range(ND):
    r = D0 + k
    calc(dy, f"A{r}", f"=DATE(Setup!$B$9,1,1)+{k}" if False else f"=DATE({YEAR},1,1)+{k}", "ddd d mmm")
    calc(dy, f"B{r}", f"=COUNTIF({SL('A')},A{r})", "0"); calc(dy, f"C{r}", f"=COUNTIF({CL('A')},A{r})", "0")
    calc(dy, f"D{r}", f"=IF(B{r}+C{r}>0,1,0)", "0")
    calc(dy, f"E{r}", f"=IF(D{r}=1,{'E' + str(r - 1) + '+1' if k else '1'},0)", "0")
    calc(dy, f"F{r}", f"=A{r}-WEEKDAY(A{r},3)", "d mmm")
DE = D0 + ND - 1
DY = lambda c: f"Days!${c}${D0}:${c}${DE}"

# ---------- 2027 Calendar (colour-in) ----------
ca = wb.create_sheet("2027 Calendar")
banner(ca, t, "2027 workout calendar", "Every day you log a workout colours itself in. Fill the whole year!", 33)
ca.column_dimensions["A"].width = 7
for k in range(2, 33): ca.column_dimensions[gl(k)].width = 3.6
ca.column_dimensions["AG"].width = 7
for dnum in range(1, 32):
    c = ca.cell(4, dnum + 1, dnum); c.font = Font(name=F, size=8, color=GREY); c.alignment = Alignment(horizontal="center")
ca.cell(4, 33, "Days").font = Font(name=F, size=8, bold=True, color=GREY)
MN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for m in range(12):
    r = 5 + m; c = ca.cell(r, 1, MN[m]); c.font = Font(name=F, bold=True, color=t.main); ca.row_dimensions[r].height = 20
    ndays = (dt.date(YEAR + (m == 11), (m + 1) % 12 + 1, 1) - dt.date(YEAR, m + 1, 1)).days
    for dnum in range(1, 32):
        cell = ca.cell(r, dnum + 1)
        if dnum <= ndays:
            doy = (dt.date(YEAR, m + 1, dnum) - dt.date(YEAR, 1, 1)).days
            cell.value = f"=Days!D{D0 + doy}"; cell.number_format = ';;;'; cell.border = BOX
            cell.fill = PatternFill("solid", fgColor="F3F4F7")
        else:
            cell.fill = PatternFill("solid", fgColor="FFFFFF")
    calc(ca, f"AG{r}", f"=SUM(B{r}:AF{r})", "0")
ca.conditional_formatting.add("B5:AF16", CellIsRule(operator="equal", formula=["1"], fill=orng))
calc(ca, "AG17", "=SUM(AG5:AG16)", "0", bold=True); label(ca, "AA17", "Total", bold=True); ca.merge_cells("AA17:AF17")
ca["AA17"].alignment = Alignment(horizontal="right")
label(ca, "A19", "Tip: print this tab and stick it on the fridge, or just watch it fill up on screen.", italic=True, size=10, color=GREY); ca.merge_cells("A19:AF19")

# ---------- Weekly totals (helper on Dashboard data) ----------
wk = wb.create_sheet("Weekly Totals")
banner(wk, t, "Weekly totals", "Every week of 2027: workouts, sets, volume and cardio minutes.", 7)
header(wk, 5, ["Week starting", "Workouts", "Target", "Hit?", "Strength sets", "Volume", "Cardio minutes"], t)
for i, w in enumerate([14, 10, 9, 8, 12, 12, 13]): wk.column_dimensions[gl(i + 1)].width = w
first_mon = dt.date(YEAR, 1, 1) - dt.timedelta(days=dt.date(YEAR, 1, 1).weekday())
for k in range(53):
    r = 6 + k
    calc(wk, f"A{r}", f"=DATE({first_mon.year},{first_mon.month},{first_mon.day})+{7 * k}", "d mmm yyyy")
    calc(wk, f"B{r}", f"=SUMIFS({DY('D')},{DY('F')},A{r})", "0")
    calc(wk, f"C{r}", f"={WT}", "0")
    calc(wk, f"D{r}", f'=IF(AND(A{r}>TODAY(),B{r}=0),"",IF(B{r}>=C{r},"Yes","No"))')
    calc(wk, f"E{r}", f'=SUMIFS({SL("D")},{SL("A")},">="&A{r},{SL("A")},"<"&A{r}+7)', "0")
    calc(wk, f"F{r}", f'=SUMIFS({SL("G")},{SL("A")},">="&A{r},{SL("A")},"<"&A{r}+7)', "#,##0")
    calc(wk, f"G{r}", f'=SUMIFS({CL("C")},{CL("A")},">="&A{r},{CL("A")},"<"&A{r}+7)', "0")
wk.conditional_formatting.add("D6:D58", CellIsRule(operator="equal", formula=['"Yes"'], fill=grn, font=GRNF))
wk.conditional_formatting.add("F6:F58", DataBarRule(start_type="num", start_value=0, end_type="max", color="E0603A"))

# ---------- PRs ----------
pr = wb.create_sheet("Personal Records")
banner(pr, t, "Personal records", "Your best for every exercise you've logged. Updates itself.", 7)
header(pr, 5, ["Exercise", "Muscle group", "Heaviest weight", "BEST EST. 1RM", "Best volume (one session)", "Times logged", "Last done"], t)
for i, w in enumerate([28, 14, 12, 13, 14, 10, 12]): pr.column_dimensions[gl(i + 1)].width = w
for k in range(EXE - 5):
    r = 6 + k; er = 6 + k
    pr[f"A{r}"] = f'=IF(Exercises!D{er}="Strength",Exercises!A{er},"")'; pr[f"A{r}"].font = Font(name=F, size=11)
    calc(pr, f"B{r}", f'=IF(A{r}="","",Exercises!B{er})')
    calc(pr, f"C{r}", f'=IF(OR(A{r}="",COUNTIF({SL("C")},A{r})=0),"",_xlfn.MAXIFS({SL("F")},{SL("C")},A{r}))', "0.0")
    calc(pr, f"D{r}", f'=IF(C{r}="","",_xlfn.MAXIFS({SL("H")},{SL("C")},A{r}))', "0.0", bold=True)
    calc(pr, f"E{r}", f'=IF(C{r}="","",_xlfn.MAXIFS({SL("G")},{SL("C")},A{r}))', "#,##0")
    calc(pr, f"F{r}", f'=IF(A{r}="","",COUNTIF({SL("C")},A{r}))', "0")
    calc(pr, f"G{r}", f'=IF(C{r}="","",_xlfn.MAXIFS({SL("A")},{SL("C")},A{r}))', "d mmm yyyy")
PRE = 6 + EXE - 6
pr.conditional_formatting.add(f"D6:D{PRE}", DataBarRule(start_type="num", start_value=0, end_type="max", color="E0603A"))
pr.freeze_panes = "B6"

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Your training at a glance. It all updates from the logs.", 10)
widths(d, {"A": 30, "B": 16, "C": 3, "D": 26, "E": 12, "F": 12})
d.merge_cells("A4:B4"); c = d["A4"]; c.value = '=Setup!B5&"\'s 2027 training"'; c.font = Font(name=F, size=14, bold=True, color=t.main)
TODAYROW = f"MATCH(MIN(TODAY(),DATE({YEAR},12,31)),{DY('A')},1)"
kpi = [("WORKOUTS IN 2027", f"=SUM({DY('D')})", "0"),
       ("Current streak (days)", f'=IF(TODAY()<DATE({YEAR},1,1),0,MAX(INDEX({DY("E")},{TODAYROW}),IF({TODAYROW}>1,INDEX({DY("E")},{TODAYROW}-1),0)))', "0"),
       ("Longest streak (days)", f"=MAX({DY('E')})", "0"),
       ("Workouts this week", f'=SUMIFS({DY("D")},{DY("F")},TODAY()-WEEKDAY(TODAY(),3))', "0"),
       ("Weekly target", f"={WT}", "0"),
       ("Weeks you hit your target", "=COUNTIF('Weekly Totals'!D6:D58,\"Yes\")", "0"),
       ("Workouts this month", f'=SUMPRODUCT(({DY("D")}=1)*(MONTH({DY("A")})=MONTH(TODAY()))*(YEAR({DY("A")})=YEAR(TODAY())))', "0"),
       ("Strength sessions logged", f'=SUMPRODUCT(({DY("B")}>0)*1)', "0"),
       ("Total volume lifted", f"=SUM({SL('G')})", "#,##0"),
       ("New PRs", f'=COUNTIF({SL("J")},"NEW PR")', "0"),
       ("Cardio minutes", f"=SUM({CL('C')})", "#,##0"),
       ("Cardio distance", f"=SUM({CL('D')})", "#,##0.0"),
       ("Body weight change", "=IFERROR(LOOKUP(2,1/(Body!B6:B205<>\"\"),Body!B6:B205)-INDEX(Body!B6:B205,MATCH(TRUE,INDEX(Body!B6:B205<>\"\",0),0)),\"\")", "+0.0;-0.0;0.0")]
kpi = [kpi[i] for i in (0, 2, 5, 7, 8, 9, 10, 11, 4, 1, 3, 6, 12)]
for i, (a, f_, fmt) in enumerate(kpi):
    r = 5 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f_, fmt, big=True); d.row_dimensions[r].height = 26
d["B5"].fill = peach; d["B14"].fill = peach
d["A17"] = f'="Volume in "&{WU}&" (sets x reps x weight). Distance in "&{DU}&"."'; d["A17"].font = Font(name=F, size=9, italic=True, color=GREY)
header(d, 4, ["Top lifts (best est. 1RM)", "Est. 1RM", "Heaviest"], t, start=4)
for i in range(6):
    rr = 5 + i
    calc(d, f"E{rr}", f"=IFERROR(LARGE('Personal Records'!$D$6:$D${PRE},{i + 1}),\"\")", "0.0")
    calc(d, f"D{rr}", f"=IF(E{rr}=\"\",\"\",INDEX('Personal Records'!$A$6:$A${PRE},MATCH(E{rr},'Personal Records'!$D$6:$D${PRE},0)))")
    d[f"D{rr}"].alignment = Alignment(horizontal="left", indent=1)
    calc(d, f"F{rr}", f"=IF(D{rr}=\"\",\"\",INDEX('Personal Records'!$C$6:$C${PRE},MATCH(D{rr},'Personal Records'!$A$6:$A${PRE},0)))", "0.0")
header(d, 12, ["Goals", "Done?"], t, start=4)
for i in range(3):
    rr = 13 + i; d[f"D{rr}"] = f"=Setup!B{10 + i}"; d[f"D{rr}"].font = Font(name=F, size=11); inp(d, f"E{rr}")
dv_list(d, "E13:E15", "Yes,Not yet")
d.conditional_formatting.add("E13:E15", CellIsRule(operator="equal", formula=['"Yes"'], fill=grn, font=GRNF))
ch = BarChart(); ch.type = "col"; ch.style = 10; ch.title = "Workouts per week"; ch.height = 7.5; ch.width = 20; ch.legend = None
ch.add_data(Reference(wk, min_col=2, min_row=5, max_row=18), titles_from_data=True); ch.set_categories(Reference(wk, min_col=1, min_row=6, max_row=18))
ch.series[0].graphicalProperties.solidFill = "E0603A"
d.add_chart(ch, "H4")
ln = LineChart(); ln.title = "Volume per week"; ln.height = 7.5; ln.width = 20; ln.legend = None; ln.style = 12
ln.add_data(Reference(wk, min_col=6, min_row=5, max_row=18), titles_from_data=True); ln.set_categories(Reference(wk, min_col=1, min_row=6, max_row=18))
ln.series[0].graphicalProperties.line.solidFill = "22304A"; ln.series[0].graphicalProperties.line.width = 30000
d.add_chart(ln, "H20")

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb["Days"].sheet_state = "visible"
order = ["Start Here", "Dashboard", "Setup", "Weekly Plan", "Strength Log", "Cardio Log", "Body", "Personal Records", "2027 Calendar", "Weekly Totals", "Exercises", "Days"]
wb._sheets = [wb[n] for n in order]
wb.save(sys.argv[1]); print("saved", NEX, "exercises", len(LOG), "log rows", PRE)
