"""Debt Payoff Planner Spreadsheet (batch 10, lane b): snowball, avalanche or your own order. Up to 12 debts; a 30-year month-by-month
plan in formulas that rolls every freed-up payment into the next debt; debt-free date per debt and overall; interest and months saved
vs minimum payments only; payment log with progress; a 100-square colour-in chart that fills itself; savings goals + log. Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule, FormulaRule, DataBarRule
from openpyxl.utils import get_column_letter as gl
from openpyxl.chart import LineChart, Reference

t = Theme("1E4D3F", "C9962E", "EEF3E8")
wb = Workbook()
ND, NM, NL, NG, NSV = 12, 360, 606, 12, 506
USD = '"$"#,##0.00'; USD0 = '"$"#,##0'
GREY = "6A6F7D"
red = PatternFill("solid", fgColor="F8D7D3"); grn = PatternFill("solid", fgColor="DCEFD9"); gold = PatternFill("solid", fgColor="F3DFA9")
REDF = Font(name=F, bold=True, color="A12A1E"); GRNF = Font(name=F, bold=True, color="2E6B3A")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Debt Payoff Planner", "Snowball, avalanche or your own order: see your debt-free date, the interest you save and colour in your progress.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["My Debts: list each debt with its balance today, interest rate (APR) and minimum payment. Add your total monthly debt budget and pick a method.",
         "Snowball pays the smallest balance first (quick wins). Avalanche pays the highest interest rate first (least interest). Custom uses your own 1, 2, 3 order.",
         "Every month the plan pays every minimum, puts all the extra on the first debt in your order and, when a debt is gone, rolls its payment into the next one.",
         "Dashboard: your debt-free date, total interest, how much and how many months you save compared with minimum payments only, and a balance chart.",
         "Payment Log: record what you actually pay. Paid so far, balance left and the 100-square colour-in chart update by themselves.",
         "Savings Goals: an emergency fund, a holiday, Christmas 2027... how much to put away each month and how close you are."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Tip: try both methods. Change the method on My Debts and watch the debt-free date and the interest on the Dashboard change instantly.", size=10, color="1E4D3F")
label(s, "B15", "The plan is an estimate: it assumes the rates stay the same, no new spending on the cards and interest worked out monthly (APR / 12). "
      "Your lender's statement is always the real number. This is a planning tool, not financial advice.", italic=True, size=10)
s.row_dimensions[15].height = 30
label(s, "B16", "Example debts, payments and goals are included so you can see how it works: type over them or delete them. Works in Excel and Google Sheets.", italic=True, size=10)

# ---------- My Debts ----------
d = wb.create_sheet("My Debts")
banner(d, t, "My debts", "One row per debt. Everything else is worked out from here.", 14)
widths(d, {"A": 26, "B": 15, "C": 13, "D": 9, "E": 12, "F": 10, "G": 8, "H": 9, "I": 14, "J": 12, "K": 12, "L": 13, "M": 9, "N": 3})
label(d, "A4", "Monthly amount for ALL debts", bold=True); inp(d, "B4", 1150, USD, "Everything you can put toward debt each month, minimums included.")
label(d, "C4", "Method", bold=True); inp(d, "D4", "Snowball"); d.merge_cells("D4:E4"); dv_list(d, "D4", "Snowball,Avalanche,Custom")
label(d, "F4", "Start", bold=True); inp(d, "G4", "=DATE(YEAR(TODAY()),MONTH(TODAY())+1,1)", "mmm yyyy"); d.merge_cells("G4:H4")
calc(d, "I4", '=IF(B4<SUM(E8:E19),"Budget is below your minimums!",IF(SUM(C8:C19)=0,"","Extra each month: "&TEXT(B4-SUM(E8:E19),"$#,##0")))')
d.merge_cells("I4:M4")
d.conditional_formatting.add("I4", FormulaRule(formula=['$B$4<SUM($E$8:$E$19)'], fill=red, font=REDF))
label(d, "A5", "Snowball = smallest balance first. Avalanche = highest rate first. Custom = your own order in column F.", italic=True, size=9, color=GREY)
header(d, 7, ["Debt", "Type", "Balance today", "APR %", "Minimum payment", "Custom order", "ORDER", "Months", "DEBT-FREE DATE", "Interest (plan)",
              "Paid so far", "Balance left", "% paid"], t)
d.row_dimensions[7].height = 44
TYPES = "Credit card,Store card,Car loan,Personal loan,Student loan,Medical,Buy now pay later,Family / friend,Overdraft,Other"
for i in range(ND):
    r = 8 + i
    for col in "ABCDEF": inp(d, f"{col}{r}")
    for col in "AB": d[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    d[f"C{r}"].number_format = USD; d[f"D{r}"].number_format = "0.00%"; d[f"E{r}"].number_format = USD
    # sort key: snowball = balance, avalanche = -APR, custom = order number; ties keep row order
    key = f'IF(N(C{r})<=0,"",IF($D$4="Avalanche",-D{r},IF($D$4="Custom",IF(F{r}="",999,F{r}),C{r})))'
    d[f"O{r}"] = f"={key}"; d[f"O{r}"].font = Font(name=F, size=8, color="FFFFFF")
    calc(d, f"G{r}", f'=IF(O{r}="","",COUNTIF($O$8:$O$19,"<"&O{r})+COUNTIF($O$7:O{r - 1},O{r})+1)', "0", bold=True)
dv_list(d, "B8:B19", TYPES)
debts = [("Store card", "Store card", 640, 0.2899, 35), ("Visa card", "Credit card", 4820, 0.2449, 145), ("Medical bill", "Medical", 1150, 0, 50),
         ("Car loan", "Car loan", 9600, 0.069, 289), ("Mastercard", "Credit card", 2310, 0.2199, 70), ("Personal loan", "Personal loan", 5400, 0.1149, 182)]
for i, row in enumerate(debts):
    for col, v in zip("ABCDE", row): d[f"{col}{8 + i}"] = v
d["O7"] = "key"; d["O7"].font = Font(name=F, size=8, color="FFFFFF"); d.column_dimensions["O"].width = 4
for col in "CDE": d[f"{col}20"].font = Font(name=F, bold=True)
label(d, "A20", "Total", bold=True); calc(d, "C20", "=SUM(C8:C19)", USD, bold=True); calc(d, "E20", "=SUM(E8:E19)", USD, bold=True)
calc(d, "J20", "=SUM(J8:J19)", USD, bold=True); calc(d, "K20", "=SUM(K8:K19)", USD, bold=True); calc(d, "L20", "=SUM(L8:L19)", USD, bold=True)
calc(d, "M20", '=IF(C20=0,"",MIN(1,K20/C20))', "0%", bold=True)

# ---------- Plan (month by month) ----------
p = wb.create_sheet("Plan")
banner(p, t, "Month-by-month plan", "Every month: interest added, minimums paid, the extra goes to the first debt in your order, freed payments roll on.", 12)
# columns: A month#, B date, C total interest, D total paid, E total balance, F extra pool, then per debt 4 cols: interest, left-after-min, payment, balance
C0 = 7
def dc(i, k): return gl(C0 + 4 * i + k)   # k: 0 interest, 1 remainder after minimum, 2 payment, 3 balance
p.column_dimensions["A"].width = 7; p.column_dimensions["B"].width = 10
for c in "CDEF": p.column_dimensions[c].width = 12
header(p, 6, ["Month", "Date", "Interest", "Paid", "Total balance", "Extra pool"], t)
p.row_dimensions[6].height = 44
for i in range(ND):
    dr = f"'My Debts'!"
    p.merge_cells(start_row=5, start_column=C0 + 4 * i, end_row=5, end_column=C0 + 4 * i + 3)
    h = p.cell(5, C0 + 4 * i, f"={dr}A{8 + i}&\"\""); h.font = Font(name=F, bold=True, color="FFFFFF"); h.fill = t.head; h.alignment = Alignment(horizontal="center")
    header(p, 6, ["Interest", "Left after min", "Payment", "Balance"], t, start=C0 + 4 * i)
    p[f"{dc(i, 1)}4"] = f"='My Debts'!G{8 + i}"; p[f"{dc(i, 1)}4"].font = Font(name=F, size=8, color="8A8F99")
    for k, w in enumerate([9, 9, 10, 11]): p.column_dimensions[dc(i, k)].width = w
    p.column_dimensions[dc(i, 1)].hidden = True
label(p, "A4", "order ->", size=8, color="8A8F99")
LAST = gl(C0 + 4 * ND - 1)
RANKROW = f"$G$4:${LAST}$4"
p.freeze_panes = "C7"
for m in range(NM):
    r = 7 + m
    p[f"A{r}"] = m + 1; p[f"A{r}"].font = Font(name=F, size=10); p[f"A{r}"].alignment = Alignment(horizontal="center")
    p[f"B{r}"] = f"=EDATE('My Debts'!$G$4,{m})"; p[f"B{r}"].number_format = "mmm yyyy"; p[f"B{r}"].font = Font(name=F, size=10)
    for i in range(ND):
        dr = 8 + i
        prev = f"'My Debts'!$C${dr}" if m == 0 else f"{dc(i, 3)}{r - 1}"
        p[f"{dc(i, 0)}{r}"] = f"=ROUND(N({prev})*N('My Debts'!$D${dr})/12,2)"
        p[f"{dc(i, 1)}{r}"] = f"=MAX(0,N({prev})+{dc(i, 0)}{r}-N('My Debts'!$E${dr}))"
        due = f"(N({prev})+{dc(i, 0)}{r})"
        before = "+".join(f'IF(N({dc(j, 1)}$4)<N({dc(i, 1)}$4),{dc(j, 1)}{r},0)' for j in range(ND) if j != i)
        extra = f'MIN({dc(i, 1)}{r},MAX(0,$F{r}-({before})))'
        p[f"{dc(i, 2)}{r}"] = f'=IF({dc(i, 1)}$4="",0,MIN({due},N(\'My Debts\'!$E${dr}))+{extra})'
        p[f"{dc(i, 3)}{r}"] = f"=MAX(0,ROUND({due}-{dc(i, 2)}{r},2))"
    ints = ",".join(f"{dc(i, 0)}{r}" for i in range(ND)); pays = ",".join(f"{dc(i, 2)}{r}" for i in range(ND)); bals = ",".join(f"{dc(i, 3)}{r}" for i in range(ND))
    prevtot = "'My Debts'!$C$20" if m == 0 else f"E{r - 1}"
    p[f"C{r}"] = f"=SUM({ints})"; p[f"D{r}"] = f"=SUM({pays})"; p[f"E{r}"] = f"=SUM({bals})"
    # extra pool = budget - all minimums actually due this month
    p[f"F{r}"] = f'=MAX(0,\'My Debts\'!$B$4-(N({prevtot})+C{r}-SUM({",".join(dc(i, 1) + str(r) for i in range(ND))})))'
    for c in "CDEF": p[f"{c}{r}"].number_format = USD0; p[f"{c}{r}"].font = Font(name=F, size=10, bold=(c == "E")); p[f"{c}{r}"].fill = CALC
    for i in range(ND):
        for k in range(4):
            cc = p[f"{dc(i, k)}{r}"]; cc.number_format = USD0 if k == 3 else '#,##0'; cc.font = Font(name=F, size=10, bold=(k == 3), color="1F2A44" if k != 0 else "8A5A12")
p.conditional_formatting.add(f"E7:E{6 + NM}", CellIsRule(operator="equal", formula=["0"], fill=grn, font=GRNF))
for i in range(ND):
    rng = f"{dc(i, 3)}7:{dc(i, 3)}{6 + NM}"
    p.conditional_formatting.add(rng, FormulaRule(formula=[f"AND({dc(i, 3)}7=0,'My Debts'!$C${8 + i}>0)"], fill=grn, font=GRNF))
PD, PE, PC_, PP = f"Plan!$B$7:$B${6 + NM}", f"Plan!$E$7:$E${6 + NM}", f"Plan!$C$7:$C${6 + NM}", f"Plan!$D$7:$D${6 + NM}"

# ---------- Minimum payments only (comparison) ----------
mo = wb.create_sheet("Minimums Only")
banner(mo, t, "If you only paid the minimums", "Same debts, minimum payments only, nothing rolled over. Used for 'what you save' on the Dashboard.", 8)
mo.column_dimensions["A"].width = 7; mo.column_dimensions["B"].width = 12; mo.column_dimensions["C"].width = 13; mo.column_dimensions["D"].width = 13
header(mo, 6, ["Month", "Paid", "Total balance", "Interest"], t)
for i in range(ND):
    header(mo, 6, [f"Debt {i + 1} balance"], t, start=5 + i); mo.column_dimensions[gl(5 + i)].width = 11
    mo.cell(5, 5 + i, f"='My Debts'!A{8 + i}&\"\"").font = Font(name=F, size=9, bold=True)
for m in range(NM):
    r = 7 + m; mo[f"A{r}"] = m + 1; mo[f"A{r}"].font = Font(name=F, size=10)
    for i in range(ND):
        dr = 8 + i; prev = f"'My Debts'!$C${dr}" if m == 0 else f"{gl(5 + i)}{r - 1}"
        mo.cell(r, 5 + i, f"=MAX(0,ROUND(N({prev})*(1+N('My Debts'!$D${dr})/12)-N('My Debts'!$E${dr}),2))").number_format = USD0
    prevtot = "'My Debts'!$C$20" if m == 0 else f"C{r - 1}"
    mo[f"C{r}"] = f"=SUM(E{r}:{gl(4 + ND)}{r})"; mo[f"C{r}"].number_format = USD0
    prevs = [("'My Debts'!$C$" + str(8 + i)) if m == 0 else (gl(5 + i) + str(r - 1)) for i in range(ND)]
    ints = "+".join(f"ROUND(N({pv})*N('My Debts'!$D${8 + i})/12,2)" for i, pv in enumerate(prevs))
    mo[f"D{r}"] = f"={ints}"; mo[f"D{r}"].number_format = USD0
    mo[f"B{r}"] = f"=N({prevtot})+D{r}-C{r}"; mo[f"B{r}"].number_format = USD0
MOC, MOD = f"'Minimums Only'!$C$7:$C${6 + NM}", f"'Minimums Only'!$D$7:$D${6 + NM}"

# per-debt results on My Debts
for i in range(ND):
    r = 8 + i; bal = f"Plan!${dc(i, 3)}$7:${dc(i, 3)}${6 + NM}"; it = f"Plan!${dc(i, 0)}$7:${dc(i, 0)}${6 + NM}"
    on = f"N(C{r})<=0"
    calc(d, f"H{r}", f'=IF({on},"",IF(COUNTIF({bal},">0")>={NM},"30+ yrs",COUNTIF({bal},">0")+1))', "0")
    calc(d, f"I{r}", f'=IF({on},"",IF(H{r}="30+ yrs","Not in 30 yrs",EDATE($G$4,H{r}-1)))', "mmm yyyy", bold=True)
    calc(d, f"J{r}", f'=IF({on},"",SUM({it}))', USD)
    calc(d, f"K{r}", f"=IF(A{r}=\"\",\"\",SUMIFS('Payment Log'!$D$6:$D${NL},'Payment Log'!$B$6:$B${NL},A{r}))", USD)
    calc(d, f"L{r}", f'=IF({on},"",MAX(0,C{r}-N(K{r})))', USD, bold=True)
    calc(d, f"M{r}", f'=IF({on},"",MIN(1,N(K{r})/C{r}))', "0%")
d.conditional_formatting.add("M8:M19", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="C9962E"))
d.conditional_formatting.add("G8:G19", CellIsRule(operator="equal", formula=["1"], fill=gold, font=Font(name=F, bold=True, color="6B4E10")))
label(d, "A22", "ORDER 1 gets all the extra money until it is paid off. Months / Debt-free date / Interest come from the Plan tab.", italic=True, size=9, color=GREY)
label(d, "A23", "Balance left = balance today - what you've logged in the Payment Log (a simple tracker; your statement shows interest added).", italic=True, size=9, color=GREY)

# ---------- Payment Log ----------
pl = wb.create_sheet("Payment Log")
banner(pl, t, "Payment log", "Record every payment you make. My Debts and the colour-in chart update.", 6)
header(pl, 5, ["Date", "Debt", "Type", "Amount", "Month", "Note"], t)
widths(pl, {"A": 13, "B": 26, "C": 14, "D": 12, "E": 10, "F": 34}); pl.freeze_panes = "A6"
for r in range(6, NL + 1):
    for col in "ABCDF": inp(pl, f"{col}{r}")
    for col in "BF": pl[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    pl[f"A{r}"].number_format = "dd mmm yyyy"; pl[f"D{r}"].number_format = USD
    calc(pl, f"E{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm yy"))')
dv_list(pl, f"B6:B{NL}", "='My Debts'!$A$8:$A$19"); dv_list(pl, f"C6:C{NL}", "Minimum,Extra,Windfall,Balance transfer,Other")
logs = [(-58, "Store card", "Minimum", 35), (-58, "Visa card", "Minimum", 145), (-58, "Medical bill", "Minimum", 50), (-58, "Car loan", "Minimum", 289),
        (-58, "Mastercard", "Minimum", 70), (-58, "Personal loan", "Minimum", 182), (-55, "Store card", "Extra", 379), (-28, "Store card", "Windfall", 226, "Tax refund: store card PAID OFF!"),
        (-28, "Medical bill", "Extra", 230), (-28, "Visa card", "Minimum", 145), (-28, "Car loan", "Minimum", 289), (-28, "Mastercard", "Minimum", 70),
        (-28, "Personal loan", "Minimum", 182), (-3, "Medical bill", "Extra", 330), (-3, "Visa card", "Minimum", 145), (-3, "Car loan", "Minimum", 289)]
for i, row in enumerate(logs):
    r = 6 + i; pl[f"A{r}"] = f"=TODAY(){row[0]:+d}"; pl[f"B{r}"] = row[1]; pl[f"C{r}"] = row[2]; pl[f"D{r}"] = row[3]
    if len(row) > 4: pl[f"F{r}"] = row[4]
calc(pl, "H5", "=SUM(D6:D%d)" % NL, USD, big=True); label(pl, "H4", "Paid in total", bold=True); pl.column_dimensions["H"].width = 18

# ---------- Savings Goals ----------
sg = wb.create_sheet("Savings Goals")
banner(sg, t, "Savings goals", "What you're saving for, by when, and how much to put away each month.", 10)
header(sg, 5, ["Goal", "Target", "Target date", "Saved so far", "STILL NEEDED", "Months left", "PER MONTH", "Progress", "Status"], t)
widths(sg, {"A": 28, "B": 12, "C": 13, "D": 13, "E": 13, "F": 10, "G": 13, "H": 11, "I": 14})
for i in range(NG):
    r = 6 + i
    for col in "ABC": inp(sg, f"{col}{r}")
    sg[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); sg[f"B{r}"].number_format = USD; sg[f"C{r}"].number_format = "mmm yyyy"
    calc(sg, f"D{r}", f"=IF(A{r}=\"\",\"\",SUMIFS('Savings Log'!$C$6:$C${NSV},'Savings Log'!$B$6:$B${NSV},A{r}))", USD)
    calc(sg, f"E{r}", f'=IF(A{r}="","",MAX(0,N(B{r})-D{r}))', USD, bold=True)
    calc(sg, f"F{r}", f'=IF(OR(A{r}="",C{r}=""),"",MAX(0,(YEAR(C{r})-YEAR(TODAY()))*12+MONTH(C{r})-MONTH(TODAY())))', "0")
    calc(sg, f"G{r}", f'=IF(OR(A{r}="",F{r}=""),"",IF(E{r}=0,0,E{r}/MAX(1,F{r})))', USD, bold=True)
    calc(sg, f"H{r}", f'=IF(OR(A{r}="",N(B{r})=0),"",MIN(1,D{r}/B{r}))', "0%")
    calc(sg, f"I{r}", f'=IF(A{r}="","",IF(H{r}>=1,"Reached!",IF(H{r}>=0.5,"Over halfway","Saving")))')
goals = [("Emergency fund (1 month)", 2500, "=DATE(YEAR(TODAY())+1,6,1)"), ("Christmas 2027", 900, "=DATE(YEAR(TODAY())+1,11,1)"),
         ("Car repairs", 600, "=DATE(YEAR(TODAY())+1,3,1)"), ("Weekend away", 450, "=DATE(YEAR(TODAY())+1,8,1)")]
for i, (g, tg, dt) in enumerate(goals): sg[f"A{6 + i}"] = g; sg[f"B{6 + i}"] = tg; sg[f"C{6 + i}"] = dt
sg.conditional_formatting.add("H6:H17", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="2F8F6A"))
sg.conditional_formatting.add("I6:I17", CellIsRule(operator="equal", formula=['"Reached!"'], fill=grn, font=GRNF))
label(sg, "A19", "Total saved", bold=True); calc(sg, "D19", "=SUM(D6:D17)", USD, bold=True); calc(sg, "G19", "=SUM(G6:G17)", USD, bold=True)
label(sg, "A20", "Per month = still needed / months left, so you know what to set aside each payday.", italic=True, size=9, color=GREY)
sv = wb.create_sheet("Savings Log")
banner(sv, t, "Savings log", "Every deposit (or withdrawal as a minus) toward a goal.", 4)
header(sv, 5, ["Date", "Goal", "Amount", "Note"], t)
widths(sv, {"A": 13, "B": 28, "C": 12, "D": 34}); sv.freeze_panes = "A6"
for r in range(6, NSV + 1):
    for col in "ABCD": inp(sv, f"{col}{r}")
    for col in "BD": sv[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sv[f"A{r}"].number_format = "dd mmm yyyy"; sv[f"C{r}"].number_format = USD
dv_list(sv, f"B6:B{NSV}", "='Savings Goals'!$A$6:$A$17")
for i, (dd, g, a, n) in enumerate([(-60, "Emergency fund (1 month)", 400, "Starter"), (-30, "Emergency fund (1 month)", 250, ""), (-30, "Christmas 2027", 75, ""),
                                   (-30, "Car repairs", 100, ""), (-2, "Emergency fund (1 month)", 250, ""), (-2, "Christmas 2027", 75, ""), (-2, "Weekend away", 60, "")]):
    r = 6 + i; sv[f"A{r}"] = f"=TODAY(){dd:+d}"; sv[f"B{r}"] = g; sv[f"C{r}"] = a; sv[f"D{r}"] = n

# ---------- Dashboard ----------
db = wb.create_sheet("Dashboard")
banner(db, t, "Debt-free dashboard", "Your plan at a glance. Change the method or budget on My Debts and watch it move.", 14)
widths(db, {"A": 34, "B": 18, "C": 3})
for k in range(4, 14): db.column_dimensions[gl(k)].width = 4.2
kpi = [("DEBT-FREE DATE", f'=IF(\'My Debts\'!C20=0,"",IF(COUNTIF({PE},">0")>={NM},"Not in 30 yrs",INDEX({PD},COUNTIF({PE},">0")+1)))', "mmmm yyyy"),
       ("Months to debt-free", f'=IF(\'My Debts\'!C20=0,"",MIN({NM},COUNTIF({PE},">0")+1))', "0"),
       ("Method", "='My Debts'!D4", None),
       ("Total debt today", "='My Debts'!C20", USD),
       ("Total interest on this plan", f"=SUM({PC_})", USD),
       ("Total you'll pay", f"=SUM({PP})", USD),
       ("Minimums only: months", f'=IF(\'My Debts\'!C20=0,"",IF(COUNTIF({MOC},">0")>={NM},"30+ yrs",COUNTIF({MOC},">0")+1))', "0"),
       ("Minimums only: interest", f"=SUM({MOD})", USD),
       ("INTEREST YOU SAVE", '=MAX(0,B12-B9)', USD),
       ("MONTHS YOU SAVE", '=IF(ISNUMBER(B11),B11-B6,"30+ yrs sooner")', "0"),
       ("Paid so far (Payment Log)", "='My Debts'!K20", USD),
       ("Debts paid off", '=COUNTIFS(\'My Debts\'!L8:L19,0,\'My Debts\'!C8:C19,">0")&" of "&COUNTIF(\'My Debts\'!C8:C19,">0")', None),
       ("Saved toward goals", "='Savings Goals'!D19", USD)]
for i, (a, f, fmt) in enumerate(kpi):
    r = 5 + i; label(db, f"A{r}", a, bold=True, size=12); c = calc(db, f"B{r}", f, fmt, big=True); db.row_dimensions[r].height = 26
for ref in ("B5", "B13", "B14"): db[ref].fill = gold
db["B5"].font = Font(name=F, size=16, bold=True, color="1E4D3F")
# 100-square colour-in chart
db.merge_cells("D4:M4"); h = db["D4"]; h.value = '="Colour-in chart: "&TEXT(IF(\'My Debts\'!C20=0,0,\'My Debts\'!M20),"0%")&" paid"'
h.font = Font(name=F, bold=True, size=12, color="1E4D3F"); h.alignment = Alignment(horizontal="center")
for k in range(100):
    rr, cc = 5 + k // 10, 4 + k % 10
    c = db.cell(rr, cc, k + 1); c.font = Font(name=F, size=7, color="9AA79F"); c.alignment = Alignment(horizontal="center", vertical="center"); c.border = BOX
    c.fill = PatternFill("solid", fgColor="F4F6F1")
db.conditional_formatting.add("D5:M14", FormulaRule(formula=["AND('My Debts'!$C$20>0,D5<='My Debts'!$M$20*100)"],
                              fill=PatternFill("solid", fgColor="C9962E"), font=Font(name=F, size=7, color="FFFFFF", bold=True)))
label(db, "D15", "Each square = 1% of your debt. They fill in as you log payments.", italic=True, size=9, color=GREY); db.merge_cells("D15:M16")
header(db, 19, ["Payoff order", "Debt-free"], t)
for i in range(ND):
    r = 20 + i
    db[f"A{r}"] = f"=IFERROR(INDEX('My Debts'!$A$8:$A$19,MATCH({i + 1},'My Debts'!$G$8:$G$19,0)),\"\")"
    db[f"A{r}"].font = Font(name=F, size=11, bold=(i == 0))
    calc(db, f"B{r}", f"=IFERROR(INDEX('My Debts'!$I$8:$I$19,MATCH({i + 1},'My Debts'!$G$8:$G$19,0)),\"\")", "mmm yyyy")
ch = LineChart(); ch.title = "Total debt balance (first 8 years)"; ch.height = 8; ch.width = 18; ch.legend = None; ch.style = 12
ch.add_data(Reference(p, min_col=5, min_row=6, max_row=6 + 96), titles_from_data=True)
ch.set_categories(Reference(p, min_col=2, min_row=7, max_row=6 + 96))
ch.series[0].graphicalProperties.line.solidFill = "C9962E"; ch.series[0].graphicalProperties.line.width = 32000; ch.series[0].smooth = True
ch.x_axis.number_format = "mmm yy"; ch.y_axis.number_format = '"$"#,##0'
db.add_chart(ch, "D19")

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
