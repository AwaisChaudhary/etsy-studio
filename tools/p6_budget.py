"""2027 Monthly Budget Planner: Excel / Google Sheets template."""
import sys, datetime as dt; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment
t = Theme("1F2A44", "2F8F8A", "E6EFEC")
YEAR = 2027
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
INC = ["Salary", "Side income", "Benefits", "Gifts received", "Other income"]
EXP = ["Rent / mortgage", "Utilities", "Phone & internet", "Groceries", "Eating out", "Transport", "Insurance", "Health", "Childcare",
       "Subscriptions", "Shopping", "Entertainment", "Gifts", "Debt payments", "Savings", "Other"]
NT = 1006  # transaction rows 7..1006
wb = Workbook()
s = wb.active; s.title = "Start Here"
banner(s, t, "2027 Budget Planner", "Every month of 2027 in one simple workbook. Log what you earn and spend; the rest is worked out.", 6)
widths(s, {"A": 6, "B": 92})
steps = ["Categories & Budget: rename the categories if you like, and type your monthly budget for each one.",
         "Transactions: log each income or expense with its date, type and category. Dates must be in 2027.",
         "Monthly: pick a month to see income, spending, savings and budget vs actual for every category.",
         "Year Overview: all 12 months side by side, with your savings rate and running total.",
         "Savings Goals: set targets (holiday, emergency fund) and track how close you are."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 11, 2)
label(s, "B13", "Works in Excel and Google Sheets. Example rows show the format; type over them or delete them.", italic=True, size=10)

# Categories & Budget
c = wb.create_sheet("Categories")
banner(c, t, "Categories & monthly budget", "Rename any category. Budgets are per month.", 4)
widths(c, {"A": 24, "B": 16, "C": 4, "D": 24})
header(c, 4, ["Income category", "Expected / month"], t)
for i, n in enumerate(INC):
    r = 5 + i; inp(c, f"A{r}", n); c[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); inp(c, f"B{r}", [3200, 400, 0, 0, 0][i], '"$"#,##0')
header(c, 12, ["Expense category", "Budget / month"], t)
budgets = [1200, 180, 70, 420, 120, 160, 90, 40, 0, 35, 120, 80, 40, 150, 400, 50]
for i, n in enumerate(EXP):
    r = 13 + i; inp(c, f"A{r}", n); c[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); inp(c, f"B{r}", budgets[i], '"$"#,##0')
ER1, ER2 = 13, 12 + len(EXP)
label(c, f"A{ER2 + 2}", "Total expense budget", bold=True); calc(c, f"B{ER2 + 2}", f"=SUM(B{ER1}:B{ER2})", '"$"#,##0', bold=True)
label(c, f"A{ER2 + 3}", "Expected income", bold=True); calc(c, f"B{ER2 + 3}", "=SUM(B5:B9)", '"$"#,##0', bold=True)
label(c, f"A{ER2 + 4}", "Left over each month", bold=True); calc(c, f"B{ER2 + 4}", f"=B{ER2 + 3}-B{ER2 + 2}", '"$"#,##0;[Red]-"$"#,##0', bold=True)
# helper list of all categories for drop-down (column D)
label(c, "D4", "All categories (for drop-downs)", bold=True, size=9, color="7F8A99")
for i in range(len(INC)): c[f"D{5 + i}"] = f"=A{5 + i}"
for i in range(len(EXP)): c[f"D{5 + len(INC) + i}"] = f"=A{13 + i}"
ALLN = len(INC) + len(EXP)

# Transactions
tr = wb.create_sheet("Transactions")
banner(tr, t, "Transactions", "One row per income or expense. Use the drop-downs for type and category.", 6)
header(tr, 6, ["Date", "Type", "Category", "Description", "Amount", "Month"], t)
widths(tr, {"A": 13, "B": 11, "C": 22, "D": 32, "E": 13, "F": 12}); tr.freeze_panes = "A7"
label(tr, "A4", "Tip: amounts are always positive; the Type column says if it's money in or out.", italic=True, size=10)
for r in range(7, NT + 1):
    for col in "ABCDE": inp(tr, f"{col}{r}")
    tr[f"A{r}"].number_format = "dd mmm yyyy"; tr[f"E{r}"].number_format = '"$"#,##0.00'; tr[f"D{r}"].alignment = Alignment(horizontal="left", indent=1)
    calc(tr, f"F{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
for i, row in enumerate([(dt.date(YEAR, 1, 1), "Income", "Salary", "January pay", 3200), (dt.date(YEAR, 1, 2), "Expense", "Rent / mortgage", "Rent", 1200),
                         (dt.date(YEAR, 1, 4), "Expense", "Groceries", "Weekly shop", 96.4)]):
    for j, v in enumerate(row): tr.cell(7 + i, 1 + j).value = v
dv_list(tr, f"B7:B{NT}", "Income,Expense"); dv_list(tr, f"C7:C{NT}", f"=Categories!$D$5:$D${4 + ALLN}")
DA, DB, DC, DE = (f"Transactions!$A$7:$A${NT}", f"Transactions!$B$7:$B${NT}", f"Transactions!$C$7:$C${NT}", f"Transactions!$E$7:$E${NT}")

def month_sum(typ, mcell, cat=None):
    start, end = f"DATE({YEAR},{mcell},1)", f"DATE({YEAR},{mcell}+1,1)"
    f = f'SUMIFS({DE},{DB},"{typ}",{DA},">="&{start},{DA},"<"&{end}'
    return f + (f",{DC},{cat})" if cat else ")")

# Monthly
m = wb.create_sheet("Monthly")
banner(m, t, "Monthly view", "Pick a month in the yellow cell.", 6)
widths(m, {"A": 26, "B": 15, "C": 15, "D": 15, "E": 11, "F": 4, "G": 6})
label(m, "A4", "Month", bold=True, size=12); inp(m, "B4", "January"); dv_list(m, "B4", ",".join(MONTHS))
m["G4"] = "=MATCH(B4,{" + ",".join(f'"{x}"' for x in MONTHS) + "},0)"
m["G4"].font = Font(name=F, size=8, color="FFFFFF")
for i, (a, f, fmt) in enumerate([("Money in", "=" + month_sum("Income", "$G$4"), '"$"#,##0.00'), ("Money out", "=" + month_sum("Expense", "$G$4"), '"$"#,##0.00'),
                                 ("Saved this month", "=B6-B7", '"$"#,##0.00;[Red]-"$"#,##0.00'), ("Savings rate", '=IF(B6=0,"",B8/B6)', "0%")]):
    r = 6 + i; label(m, f"A{r}", a, bold=True, size=12); calc(m, f"B{r}", f, fmt, big=True); m.row_dimensions[r].height = 28
header(m, 11, ["Expense category", "Budget", "Spent", "Left", "% used"], t)
for i in range(len(EXP)):
    r = 12 + i; m[f"A{r}"] = f"=Categories!A{13 + i}"; m[f"A{r}"].font = Font(name=F, size=11)
    calc(m, f"B{r}", f"=Categories!B{13 + i}", '"$"#,##0')
    calc(m, f"C{r}", "=" + month_sum("Expense", "$G$4", f"A{r}"), '"$"#,##0.00')
    calc(m, f"D{r}", f"=B{r}-C{r}", '"$"#,##0.00;[Red]-"$"#,##0.00')
    calc(m, f"E{r}", f'=IF(B{r}=0,"",C{r}/B{r})', "0%")
mr = 12 + len(EXP)
label(m, f"A{mr}", "Total", bold=True)
for col, fmt in (("B", '"$"#,##0'), ("C", '"$"#,##0.00')): calc(m, f"{col}{mr}", f"=SUM({col}12:{col}{mr - 1})", fmt, bold=True)
calc(m, f"D{mr}", f"=B{mr}-C{mr}", '"$"#,##0.00;[Red]-"$"#,##0.00', bold=True)
calc(m, f"E{mr}", f'=IF(B{mr}=0,"",C{mr}/B{mr})', "0%", bold=True)
m.conditional_formatting.add(f"E12:E{mr}", CellIsRule(operator="greaterThan", formula=["1"], font=Font(name=F, color="C00000", bold=True)))

# Year overview
y = wb.create_sheet("Year Overview")
banner(y, t, "2027 at a glance", "Income, spending and savings for every month.", 6)
widths(y, {"A": 14, "B": 15, "C": 15, "D": 15, "E": 12, "F": 16})
header(y, 4, ["Month", "Money in", "Money out", "Saved", "Savings rate", "Saved so far"], t)
for i, mn in enumerate(MONTHS):
    r = 5 + i; label(y, f"A{r}", mn)
    calc(y, f"B{r}", "=" + month_sum("Income", str(i + 1)), '"$"#,##0')
    calc(y, f"C{r}", "=" + month_sum("Expense", str(i + 1)), '"$"#,##0')
    calc(y, f"D{r}", f"=B{r}-C{r}", '"$"#,##0;[Red]-"$"#,##0')
    calc(y, f"E{r}", f'=IF(B{r}=0,"",D{r}/B{r})', "0%")
    calc(y, f"F{r}", f"=SUM($D$5:D{r})", '"$"#,##0;[Red]-"$"#,##0')
label(y, "A17", "Year total", bold=True)
for col in "BCD": calc(y, f"{col}17", f"=SUM({col}5:{col}16)", '"$"#,##0;[Red]-"$"#,##0', bold=True)
calc(y, "E17", '=IF(B17=0,"",D17/B17)', "0%", bold=True)

# Savings goals
g = wb.create_sheet("Savings Goals")
banner(g, t, "Savings goals", "Set a target and a date; see how much to save each month.", 6)
header(g, 4, ["Goal", "Target", "Saved so far", "Still needed", "Progress", "Target date", "Save per month"], t)
widths(g, {"A": 24, "B": 13, "C": 14, "D": 14, "E": 11, "F": 13, "G": 15})
for r in range(5, 17):
    for col in "ABCF": inp(g, f"{col}{r}")
    g[f"A{r}"].alignment = Alignment(horizontal="left", indent=1)
    g[f"B{r}"].number_format = '"$"#,##0'; g[f"C{r}"].number_format = '"$"#,##0'; g[f"F{r}"].number_format = "mmm yyyy"
    calc(g, f"D{r}", f'=IF(B{r}="","",MAX(0,B{r}-C{r}))', '"$"#,##0')
    calc(g, f"E{r}", f'=IF(OR(B{r}="",B{r}=0),"",MIN(1,C{r}/B{r}))', "0%")
    calc(g, f"G{r}", f'=IF(OR(D{r}="",F{r}=""),"",IF(F{r}<=TODAY(),D{r},IF(DATEDIF(TODAY(),F{r},"m")<1,D{r},D{r}/DATEDIF(TODAY(),F{r},"m"))))', '"$"#,##0')
for i, row in enumerate([("Emergency fund", 3000, 850, None, None, dt.date(YEAR, 12, 1)), ("Summer holiday", 1800, 300, None, None, dt.date(YEAR, 7, 1))]):
    for j, v in enumerate(row):
        if v is not None: g.cell(5 + i, 1 + j).value = v
for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.save(sys.argv[1]); print("saved")
