"""2027 Habit Tracker Spreadsheet (batch 9, lane b): Setup (year, up to 15 habits with a monthly goal), 12 monthly tabs with a
tick grid (dates and weekdays fill in for any year), done count, goal days, %, best streak and days left to goal per habit,
daily completion %, mood (1-5) and sleep rows, Year Overview (habit x month heat map, yearly totals, mood/sleep averages, chart)
and a 2027 Goals page with progress bars. Excel + Google Sheets.
Usage: python3 p18_habits.py out.xlsx [--demo]   (--demo ticks Jan-Mar with example data for screenshots)"""
import sys, random; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule, FormulaRule, ColorScaleRule, DataBarRule
from openpyxl.utils import get_column_letter as gl
from openpyxl.chart import BarChart, Reference

DEMO = "--demo" in sys.argv
t = Theme("2E4A3F", "C9774A", "F3EEE6")
wb = Workbook()
NH = 15
GREY = "6A6F7D"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
TICK = "✓"
DONEF = PatternFill("solid", fgColor="9CC5A8"); MISSF = PatternFill("solid", fgColor="F3D3C6"); OUTF = PatternFill("solid", fgColor="E4E4E4")
WKND = PatternFill("solid", fgColor="F7F3EC")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "2027 Habit Tracker", "Build the habits you want this year: tick them off each day and watch your streaks, goals and year fill in.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Setup: check the year (2027) and type up to 15 habits, each with a monthly goal (for example 80% = about 24 days in a 30-day month).",
         f"Each month has its own tab. Tick a habit with {TICK} from the drop-down (or just type x). Use ✗ for a missed day if you like. Dates and weekdays fill in for you.",
         "Each habit shows days done, your goal, % done, your best streak that month and how many more days you need to hit the goal.",
         "Optional: rate your mood 1-5 and type your hours of sleep each day. The colours show your good and hard days at a glance.",
         "Year Overview: a heat map of every habit by month, your yearly totals, average mood and sleep, and a chart of your year.",
         "2027 Goals: write your big goals with your why, first step and deadline, and drag the progress up as you go."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Tip: start with 3-5 habits. Small and daily beats big and occasional. You can add more habits in Setup at any time and they appear in every month.",
      size=10, color="7A4A2E")
s.row_dimensions[14].height = 30
label(s, "B15", "Change the year in Setup and every month redraws its dates, so you can reuse it in 2028. Works in Excel and Google Sheets (File > Import).",
      italic=True, size=10)
s.row_dimensions[15].height = 30

# ---------- Setup ----------
su = wb.create_sheet("Setup")
banner(su, t, "Setup", "Your year and your habits. Every month uses this list.", 5)
widths(su, {"A": 6, "B": 34, "C": 18, "D": 14, "E": 50})
label(su, "B4", "Year", bold=True, size=12); inp(su, "C4", 2027, "0")
YEAR = "Setup!$C$4"
header(su, 6, ["#", "Habit", "Area", "Monthly goal", "Why it matters to me"], t)
CATS = "Health,Fitness,Mind,Learning,Money,Home,Creative,Relationships,Work,Other"
habits = [("Drink 8 glasses of water", "Health", 0.9, "More energy, fewer headaches"), ("Walk 8,000 steps", "Fitness", 0.8, "Feel strong for summer hikes"),
          ("Read 20 pages", "Learning", 0.8, "24 books this year"), ("No phone first hour", "Mind", 0.7, "Calmer mornings"),
          ("Stretch or yoga 10 min", "Fitness", 0.6, "Back feels better"), ("Make my bed", "Home", 0.9, "Small win to start the day"),
          ("Journal 3 lines", "Mind", 0.7, "Notice the good things"), ("No spend day", "Money", 0.5, "Save for the trip"),
          ("Craft 30 minutes", "Creative", 0.5, "Finish the blanket"), ("In bed by 10:30", "Health", 0.7, "")]
for i in range(NH):
    r = 7 + i; c = su.cell(r, 1, i + 1); c.font = Font(name=F, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center")
    for col in "BCDE": inp(su, f"{col}{r}")
    su[f"D{r}"].number_format = "0%"
    for col in "BCE": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    if i < len(habits):
        h = habits[i]; su[f"B{r}"] = h[0]; su[f"C{r}"] = h[1]; su[f"D{r}"] = h[2]; su[f"E{r}"] = h[3] or None
dv_list(su, f"C7:C{6 + NH}", CATS)
label(su, f"B{8 + NH}", "Monthly goal: the share of days you want to tick. 100% = every day, 70% = about 5 days a week. Blank = no goal.", italic=True, size=9, color=GREY)

# ---------- months ----------
D0 = 2  # column B = day 1
DC = [gl(D0 + i) for i in range(31)]
C_DONE, C_GOAL, C_PCT, C_STREAK, C_LEFT = (gl(D0 + 31 + i) for i in range(5))
HR0 = 7; HR1 = HR0 + NH - 1
R_DAY, R_MOOD, R_SLEEP = HR1 + 1, HR1 + 2, HR1 + 3
HELP0 = R_SLEEP + 3

def done(ref): return f'OR({ref}="{TICK}",{ref}="x",{ref}="X")'

random.seed(7)
for mi, mname in enumerate(MONTHS):
    m = mi + 1
    ws = wb.create_sheet(mname[:3])
    banner(ws, t, f"{mname}", "Tick each habit you did. Your goals, streaks and daily score update as you go.", 2 + 31 + 4)
    ws["A1"] = f'="{mname} "&{YEAR}'
    ws.column_dimensions["A"].width = 28
    for c in DC: ws.column_dimensions[c].width = 3.9
    for c, w in zip((C_DONE, C_GOAL, C_PCT, C_STREAK, C_LEFT), (7, 7, 7, 8, 8)): ws.column_dimensions[c].width = w
    ws.freeze_panes = f"{DC[0]}{HR0}"
    ND = f"DAY(EOMONTH(DATE({YEAR},{m},1),0))"
    label(ws, "A5", "", bold=True)
    # weekday + day rows
    for i, c in enumerate(DC):
        d = i + 1
        w = ws[f"{c}5"]; w.value = f'=IF({d}>{ND},"",LEFT(TEXT(DATE({YEAR},{m},{d}),"ddd"),2))'
        w.font = Font(name=F, size=8, color=GREY); w.alignment = Alignment(horizontal="center")
        h = ws[f"{c}6"]; h.value = f'=IF({d}>{ND},"",{d})'
        h.font = Font(name=F, size=10, bold=True, color="FFFFFF"); h.fill = t.acc; h.alignment = Alignment(horizontal="center", vertical="center"); h.border = BOX
    hc = ws["A6"]; hc.value = "Habit"; hc.font = Font(name=F, size=11, bold=True, color="FFFFFF"); hc.fill = t.acc; hc.border = BOX; hc.alignment = Alignment(indent=1, vertical="center")
    for c, n in zip((C_DONE, C_GOAL, C_PCT, C_STREAK, C_LEFT), ("Done", "Goal", "%", "Best streak", "Days to goal")):
        x = ws[f"{c}6"]; x.value = n; x.font = Font(name=F, size=9, bold=True, color="FFFFFF"); x.fill = t.head; x.border = BOX
        x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[6].height = 30
    LASTD = f"{DC[-1]}"
    for k in range(NH):
        r = HR0 + k; hr = HELP0 + k
        a = ws[f"A{r}"]; a.value = f'=IF(Setup!B{7 + k}="","",Setup!B{7 + k})'; a.font = Font(name=F, size=10, color="1F2A44")
        a.alignment = Alignment(indent=1, vertical="center"); a.border = BOX
        for i, c in enumerate(DC):
            cell = ws[f"{c}{r}"]; cell.border = BOX; cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = Font(name=F, size=11, bold=True, color="1F4F3A"); cell.fill = INPUT
            prev = f"{DC[i - 1]}{hr}" if i else "0"
            ws[f"{c}{hr}"] = f"=IF({done(f'{c}{r}')},{prev}+1,0)"
        rng = f"{DC[0]}{r}:{LASTD}{r}"
        on = f'$A{r}=""'
        calc(ws, f"{C_DONE}{r}", f'=IF({on},"",COUNTIF({rng},"{TICK}")+COUNTIF({rng},"x"))', "0", bold=True)
        calc(ws, f"{C_GOAL}{r}", f'=IF(OR({on},Setup!D{7 + k}=""),"",ROUND(Setup!D{7 + k}*{ND},0))', "0")
        calc(ws, f"{C_PCT}{r}", f'=IF({on},"",{C_DONE}{r}/{ND})', "0%")
        calc(ws, f"{C_STREAK}{r}", f'=IF({on},"",MAX({DC[0]}{hr}:{LASTD}{hr}))', "0")
        calc(ws, f"{C_LEFT}{r}", f'=IF(OR({on},{C_GOAL}{r}=""),"",IF({C_DONE}{r}>={C_GOAL}{r},"Goal hit!",{C_GOAL}{r}-{C_DONE}{r}))', "0")
        ws.row_dimensions[r].height = 19
    dv = DataValidation(type="list", formula1=f'"{TICK},✗"', allow_blank=True); dv.showErrorMessage = False
    dv.add(f"{DC[0]}{HR0}:{LASTD}{HR1}"); ws.add_data_validation(dv)
    grid = f"{DC[0]}{HR0}:{LASTD}{HR1}"
    tl = f"{DC[0]}{HR0}"
    ws.conditional_formatting.add(grid, FormulaRule(formula=[f'COLUMN({tl})-1>{ND}'], fill=OUTF, stopIfTrue=True))
    ws.conditional_formatting.add(grid, FormulaRule(formula=[f'OR({tl}="{TICK}",{tl}="x",{tl}="X")'], fill=DONEF, font=Font(name=F, bold=True, color="1F4F3A")))
    ws.conditional_formatting.add(grid, FormulaRule(formula=[f'{tl}="✗"'], fill=MISSF, font=Font(name=F, color="A0522D")))
    ws.conditional_formatting.add(grid, FormulaRule(formula=[f'$A{HR0}=""'], fill=PatternFill("solid", fgColor="FAFAF7")))
    ws.conditional_formatting.add(grid, FormulaRule(formula=[f'WEEKDAY(DATE({YEAR},{m},MIN(COLUMN({tl})-1,28)),2)>5', ], fill=WKND))
    ws.conditional_formatting.add(f"{C_LEFT}{HR0}:{C_LEFT}{HR1}", CellIsRule(operator="equal", formula=['"Goal hit!"'], fill=PatternFill("solid", fgColor="D6EAD9"), font=Font(name=F, bold=True, color="2E6B3A")))
    ws.conditional_formatting.add(f"{C_PCT}{HR0}:{C_PCT}{HR1}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="9CC5A8"))
    # daily score, mood, sleep
    for r, name in ((R_DAY, "Daily score"), (R_MOOD, "Mood (1-5)"), (R_SLEEP, "Sleep (hours)")):
        a = ws[f"A{r}"]; a.value = name; a.font = Font(name=F, size=10, bold=True, color="FFFFFF" if r == R_DAY else "1F2A44")
        a.fill = t.head if r == R_DAY else t.band; a.border = BOX; a.alignment = Alignment(indent=1, vertical="center")
        ws.row_dimensions[r].height = 20
    for i, c in enumerate(DC):
        d = i + 1
        calc(ws, f"{c}{R_DAY}", f'=IF(OR({d}>{ND},COUNTIF($A${HR0}:$A${HR1},"?*")=0),"",'
                               f'(COUNTIF({c}{HR0}:{c}{HR1},"{TICK}")+COUNTIF({c}{HR0}:{c}{HR1},"x"))/COUNTIF($A${HR0}:$A${HR1},"?*"))', "0%")
        ws[f"{c}{R_DAY}"].font = Font(name=F, size=7, color="1F2A44")
        for r in (R_MOOD, R_SLEEP):
            inp(ws, f"{c}{r}"); ws[f"{c}{r}"].font = Font(name=F, size=9, color="0000FF")
    ws.conditional_formatting.add(f"{DC[0]}{R_DAY}:{LASTD}{R_DAY}", ColorScaleRule(start_type="num", start_value=0, start_color="FFFFFF", end_type="num", end_value=1, end_color="6FA883"))
    ws.conditional_formatting.add(f"{DC[0]}{R_MOOD}:{LASTD}{R_MOOD}", ColorScaleRule(start_type="num", start_value=1, start_color="F2B8A2", mid_type="num", mid_value=3,
                                                                                    mid_color="FBF0D0", end_type="num", end_value=5, end_color="9CC5A8"))
    dvm = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True); dvm.add(f"{DC[0]}{R_MOOD}:{LASTD}{R_MOOD}"); ws.add_data_validation(dvm)
    calc(ws, f"{C_DONE}{R_DAY}", f'=IF(SUM({C_DONE}{HR0}:{C_DONE}{HR1})=0,"",IFERROR(AVERAGE({DC[0]}{R_DAY}:{LASTD}{R_DAY}),""))', "0%", bold=True)
    calc(ws, f"{C_DONE}{R_MOOD}", f'=IFERROR(AVERAGE({DC[0]}{R_MOOD}:{LASTD}{R_MOOD}),"")', "0.0", bold=True)
    calc(ws, f"{C_DONE}{R_SLEEP}", f'=IFERROR(AVERAGE({DC[0]}{R_SLEEP}:{LASTD}{R_SLEEP}),"")', "0.0", bold=True)
    for r, n in ((R_DAY, "avg"), (R_MOOD, "avg"), (R_SLEEP, "avg h")): label(ws, f"{C_GOAL}{r}", n, size=8, color=GREY)
    # month notes
    nr = R_SLEEP + 1
    label(ws, f"A{nr}", "Wins this month:", bold=True, size=10); ws.merge_cells(f"{DC[0]}{nr}:{C_LEFT}{nr}"); inp(ws, f"{DC[0]}{nr}"); ws[f"{DC[0]}{nr}"].alignment = Alignment(horizontal="left", indent=1)
    ws.row_dimensions[nr].height = 22
    for k in range(NH): ws.row_dimensions[HELP0 + k].hidden = True
    label(ws, f"A{HELP0 - 1}", "", size=8)
    if DEMO and m <= 3:
        rate = [0.92, 0.8, 0.83, 0.68, 0.55, 0.9, 0.66, 0.5, 0.48, 0.66]
        nd = [31, 28, 31][mi]
        for k in range(len(habits)):
            p_ = min(0.97, rate[k] + 0.04 * mi)
            for i in range(nd):
                ws[f"{DC[i]}{HR0 + k}"] = TICK if random.random() < p_ else ("✗" if random.random() < 0.25 else None)
        for i in range(nd):
            ws[f"{DC[i]}{R_MOOD}"] = random.choice([3, 4, 4, 4, 5, 5, 3, 2]); ws[f"{DC[i]}{R_SLEEP}"] = random.choice([6.5, 7, 7, 7.5, 8, 8, 6])
        ws[f"{DC[0]}{R_SLEEP + 1}"] = ["Walked every day of week 2. Finished 2 books!", "Water habit on autopilot now. 12-day reading streak.", "Best month yet: 4 goals hit."][mi]
    ws.sheet_properties.tabColor = t.accent

# ---------- Year Overview ----------
yo = wb.create_sheet("Year Overview")
banner(yo, t, "Year overview", "Every habit, every month: the greener, the better. Updates as you tick.", 16)
yo["A1"] = f'="Your "&{YEAR}&" at a glance"'
widths(yo, {"A": 28});
for i in range(12): yo.column_dimensions[gl(2 + i)].width = 7
yo.column_dimensions["N"].width = 10; yo.column_dimensions["O"].width = 10; yo.column_dimensions["P"].width = 11
header(yo, 5, ["Habit"] + [mn[:3] for mn in MONTHS] + ["Days done", "Year %", "Best streak"], t)
for k in range(NH):
    r = 6 + k
    a = yo[f"A{r}"]; a.value = f'=IF(Setup!B{7 + k}="","",Setup!B{7 + k})'; a.font = Font(name=F, size=10); a.border = BOX; a.alignment = Alignment(indent=1)
    for i, mn in enumerate(MONTHS):
        calc(yo, f"{gl(2 + i)}{r}", f"=IF(OR($A{r}=\"\",SUM({mn[:3]}!{C_DONE}{HR0}:{C_DONE}{HR1})=0),\"\",{mn[:3]}!{C_PCT}{HR0 + k})", "0%")
    calc(yo, f"N{r}", f'=IF($A{r}="","",' + "+".join(f"{mn[:3]}!{C_DONE}{HR0 + k}" for mn in MONTHS) + ")", "0", bold=True)
    calc(yo, f"O{r}", f'=IF($A{r}="","",N{r}/(DATE({YEAR}+1,1,1)-DATE({YEAR},1,1)))', "0%", bold=True)
    calc(yo, f"P{r}", f'=IF($A{r}="","",MAX(' + ",".join(f"{mn[:3]}!{C_STREAK}{HR0 + k}" for mn in MONTHS) + "))", "0")
RS = 6 + NH
for rr, (name, src, fmt) in enumerate((("Daily score (avg)", R_DAY, "0%"), ("Mood (avg)", R_MOOD, "0.0"), ("Sleep (avg hours)", R_SLEEP, "0.0"))):
    r = RS + rr
    a = yo[f"A{r}"]; a.value = name; a.font = Font(name=F, size=10, bold=True, color="FFFFFF"); a.fill = t.head; a.border = BOX; a.alignment = Alignment(indent=1)
    for i, mn in enumerate(MONTHS):
        calc(yo, f"{gl(2 + i)}{r}", f"={mn[:3]}!{C_DONE}{src}", fmt)
yo.conditional_formatting.add(f"B6:M{5 + NH}", ColorScaleRule(start_type="num", start_value=0, start_color="FFFFFF", mid_type="num", mid_value=0.5, mid_color="D8EAD9",
                                                             end_type="num", end_value=1, end_color="5E9C74"))
yo.conditional_formatting.add(f"B{RS}:M{RS}", ColorScaleRule(start_type="num", start_value=0, start_color="FFFFFF", end_type="num", end_value=1, end_color="C9774A"))
yo.conditional_formatting.add(f"O6:O{5 + NH}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="9CC5A8"))
ch = BarChart(); ch.type = "col"; ch.style = 10; ch.title = "Daily score by month"; ch.height = 7.5; ch.width = 20; ch.legend = None
ch.add_data(Reference(yo, min_col=2, max_col=13, min_row=RS), from_rows=True, titles_from_data=False)
ch.set_categories(Reference(yo, min_col=2, max_col=13, min_row=5))
ch.series[0].graphicalProperties.solidFill = "5E9C74"; ch.series[0].graphicalProperties.line.solidFill = "5E9C74"
ch.y_axis.number_format = "0%"; ch.y_axis.scaling.min = 0; ch.y_axis.scaling.max = 1
yo.add_chart(ch, f"A{RS + 5}")

# ---------- Goals ----------
g = wb.create_sheet("2027 Goals")
banner(g, t, "My goals", "Big goals for the year: your why, your first step and how far you've come.", 8)
g["A1"] = f'="My "&{YEAR}&" goals"'
header(g, 5, ["Goal", "Area", "Why", "First step", "Deadline", "Progress", "Status", "Days left"], t)
widths(g, {"A": 34, "B": 14, "C": 32, "D": 32, "E": 13, "F": 11, "G": 13, "H": 10})
for r in range(6, 18):
    for col in "ABCDEFG": inp(g, f"{col}{r}")
    for col in "ABCD": g[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1, wrap_text=True)
    g[f"E{r}"].number_format = "dd mmm yyyy"; g[f"F{r}"].number_format = "0%"
    calc(g, f"H{r}", f'=IF(OR(E{r}="",G{r}="Done"),"",E{r}-TODAY())', "0")
    g.row_dimensions[r].height = 30
dv_list(g, "B6:B17", CATS); dv_list(g, "G6:G17", "Not started,In progress,Done,Paused")
dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True); dvp.add("F6:F17"); g.add_data_validation(dvp)
g.conditional_formatting.add("F6:F17", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="C9774A"))
g.conditional_formatting.add("G6:G17", CellIsRule(operator="equal", formula=['"Done"'], fill=PatternFill("solid", fgColor="D6EAD9"), font=Font(name=F, bold=True, color="2E6B3A")))
goals = [("Read 24 books", "Learning", "Read more than I scroll", "Pick January's 2 books", "2027-12-31", 0.25, "In progress"),
         ("Save $3,000 for a trip", "Money", "Visit my sister in the spring", "Auto-transfer $60 every payday", "2027-04-30", 0.4, "In progress"),
         ("Walk a 10K", "Fitness", "Feel strong and proud", "8,000 steps a day", "2027-06-12", 0.1, "In progress"),
         ("Finish the granny square blanket", "Creative", "Gift for Mum's birthday", "3 squares a week", "2027-08-20", 0, "Not started")]
import datetime as _dt
for i, row in enumerate(goals):
    for j, v in enumerate(row):
        g.cell(6 + i, 1 + j).value = _dt.date.fromisoformat(v) if j == 4 else v
label(g, "A19", "Progress: type a % (25%) or 0.25. Tie each goal to a habit in Setup, so your daily ticks move it forward.", italic=True, size=9, color=GREY)

for ws in (s, su, yo, g): ws.sheet_properties.tabColor = t.main
order = ["Start Here", "Setup", "Year Overview", "2027 Goals"] + [mn[:3] for mn in MONTHS]
wb._sheets = [wb[n] for n in order]; wb.active = 0
wb.save(sys.argv[1]); print("saved", wb.sheetnames)
