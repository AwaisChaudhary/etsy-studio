"""Christmas Gift Planner & Budget: Excel / Google Sheets template."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment
t = Theme("8C1C2B", "1F6B4A", "F7E9E6")
GROUPS = ["Family", "Partner", "Kids", "Friends", "Work", "Teachers", "Neighbours", "Other"]
STATUS = ["Idea", "Ordered", "Bought", "Wrapped", "Given"]
CATS = ["Gifts", "Food & drinks", "Decorations", "Cards & postage", "Wrapping", "Travel", "Parties & outings", "Charity", "Other"]
N = 155   # gift rows 6..155 (150 people)
M = 105   # other spending rows 6..105
wb = Workbook()
s = wb.active; s.title = "Start Here"
banner(s, t, "Christmas Gift Planner & Budget", "Plan every gift, stay on budget and see what's left at a glance.", 6)
widths(s, {"A": 6, "B": 92})
steps = ["Budget: type your total Christmas budget and how you want to split it (gifts, food, decorations and more).",
         "Gift List: one row per person. Add a gift idea, your budget for them and, once bought, the actual cost. Track each gift from idea to given.",
         "Other Spending: log food, decorations, cards, travel and anything else as you spend.",
         "Dashboard: see total spent, what's left, gifts still to buy, spending by group and the countdown to Christmas.",
         "Cards: keep your Christmas card list with addresses and who has been sent one."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 11, 2)
label(s, "B13", "Works in Excel and Google Sheets. The example rows show the format; type over them or delete them.", italic=True, size=10)

# Budget
b = wb.create_sheet("Budget")
banner(b, t, "Budget", "Set your total and split it. Spent and remaining update as you fill in the other tabs.", 5)
widths(b, {"A": 26, "B": 16, "C": 16, "D": 16, "E": 14})
label(b, "A4", "Total Christmas budget", bold=True, size=12); inp(b, "B4", 1500, '"$"#,##0')
b.row_dimensions[4].height = 26
header(b, 6, ["Category", "Budget", "Spent", "Remaining", "% used"], t)
for i, cat in enumerate(CATS):
    r = 7 + i; label(b, f"A{r}", cat)
    inp(b, f"B{r}", [900, 220, 80, 60, 40, 100, 60, 40, 0][i], '"$"#,##0')
    spent = f"SUM('Gift List'!G6:G{N})" if cat == "Gifts" else f"SUMIFS('Other Spending'!D6:D{M},'Other Spending'!B6:B{M},A{r})"
    calc(b, f"C{r}", "=" + spent, '"$"#,##0.00')
    calc(b, f"D{r}", f"=B{r}-C{r}", '"$"#,##0.00;[Red]-"$"#,##0.00')
    calc(b, f"E{r}", f'=IF(B{r}=0,"",C{r}/B{r})', "0%")
tr = 7 + len(CATS)
label(b, f"A{tr}", "Total", bold=True)
calc(b, f"B{tr}", f"=SUM(B7:B{tr - 1})", '"$"#,##0', bold=True)
calc(b, f"C{tr}", f"=SUM(C7:C{tr - 1})", '"$"#,##0.00', bold=True)
calc(b, f"D{tr}", f"=B{tr}-C{tr}", '"$"#,##0.00;[Red]-"$"#,##0.00', bold=True)
calc(b, f"E{tr}", f'=IF(B{tr}=0,"",C{tr}/B{tr})', "0%", bold=True)
label(b, f"A{tr + 2}", "Split vs total budget", bold=True)
calc(b, f"B{tr + 2}", f'=IF(B{tr}=B4,"Matches your total",IF(B{tr}>B4,"Over by "&TEXT(B{tr}-B4,"$#,##0"),"Unassigned: "&TEXT(B4-B{tr},"$#,##0")))')
b.merge_cells(f"B{tr + 2}:D{tr + 2}")
b.conditional_formatting.add(f"E7:E{tr}", CellIsRule(operator="greaterThan", formula=["1"], font=Font(name=F, color="C00000", bold=True)))

# Gift List
g = wb.create_sheet("Gift List")
banner(g, t, "Gift list", "One row per person. Budget vs actual and status are tracked for you.", 11)
cols = ["Name", "Group", "Gift idea", "Where to buy", "Link or notes", "Budget", "Actual cost", "Difference", "Status", "Arrives by", "Wrapped?"]
header(g, 5, cols, t)
widths(g, {"A": 18, "B": 12, "C": 24, "D": 16, "E": 22, "F": 11, "G": 12, "H": 12, "I": 11, "J": 12, "K": 10}); g.freeze_panes = "B6"
for r in range(6, N + 1):
    for col in "ABCDEFGIJK": inp(g, f"{col}{r}")
    for col in "ACDE": g[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    g[f"F{r}"].number_format = '"$"#,##0.00'; g[f"G{r}"].number_format = '"$"#,##0.00'; g[f"J{r}"].number_format = "dd mmm"
    calc(g, f"H{r}", f'=IF(OR(F{r}="",G{r}=""),"",F{r}-G{r})', '"$"#,##0.00;[Red]-"$"#,##0.00')
ex = [("Mum", "Family", "Cashmere scarf", "Department store", "Grey or navy", 80, 72, None, "Bought", None, "No"),
      ("Sam", "Partner", "Weekend away", "Online", "Book by 15 Dec", 250, None, None, "Idea", None, ""),
      ("Leo (8)", "Kids", "Building set", "Toy shop", "Space theme", 45, 39.99, None, "Wrapped", None, "Yes")]
for i, row in enumerate(ex):
    for j, v in enumerate(row):
        if v is not None and v != "": g.cell(6 + i, 1 + j).value = v
dv_list(g, f"B6:B{N}", ",".join(GROUPS)); dv_list(g, f"I6:I{N}", ",".join(STATUS)); dv_list(g, f"K6:K{N}", "Yes,No")
g.conditional_formatting.add(f"I6:I{N}", FormulaRule(formula=['$I6="Given"'], fill=PatternFill("solid", fgColor="D9EAD3")))
g.conditional_formatting.add(f"I6:I{N}", FormulaRule(formula=['$I6="Idea"'], fill=PatternFill("solid", fgColor="FCE4D6")))

# Other Spending
o = wb.create_sheet("Other Spending")
banner(o, t, "Other spending", "Food, decorations, cards, travel and everything that isn't a gift.", 5)
header(o, 5, ["Date", "Category", "What", "Amount", "Paid with"], t)
widths(o, {"A": 13, "B": 20, "C": 30, "D": 13, "E": 16}); o.freeze_panes = "A6"
for r in range(6, M + 1):
    for col in "ABCDE": inp(o, f"{col}{r}")
    o[f"A{r}"].number_format = "dd mmm yyyy"; o[f"D{r}"].number_format = '"$"#,##0.00'; o[f"C{r}"].alignment = Alignment(horizontal="left", indent=1)
import datetime as dt
for i, row in enumerate([(dt.date(2026, 11, 28), "Decorations", "Tree and lights", 64.5, "Card"), (dt.date(2026, 12, 2), "Cards & postage", "Cards and stamps", 23.8, "Cash")]):
    for j, v in enumerate(row): o.cell(6 + i, 1 + j).value = v
dv_list(o, f"B6:B{M}", ",".join(c for c in CATS if c != "Gifts"))

# Dashboard
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Your Christmas at a glance.", 6)
widths(d, {"A": 28, "B": 16, "C": 4, "D": 18, "E": 12, "F": 14})
items = [("Days until Christmas", '=MAX(0,DATE(YEAR(TODAY())+IF(TODAY()>DATE(YEAR(TODAY()),12,25),1,0),12,25)-TODAY())', "0"),
         ("Total budget", "=Budget!B4", '"$"#,##0'),
         ("Spent so far", f"=Budget!C{tr}", '"$"#,##0.00'),
         ("Left to spend", "=B5-B6", '"$"#,##0.00;[Red]-"$"#,##0.00'),
         ("Budget used", '=IF(B5=0,"",B6/B5)', "0%"),
         ("People on the list", f"=COUNTA('Gift List'!A6:A{N})", "0"),
         ("Gifts still to buy", f"=COUNTIFS('Gift List'!A6:A{N},\"<>\",'Gift List'!I6:I{N},\"Idea\")+COUNTIFS('Gift List'!A6:A{N},\"<>\",'Gift List'!I6:I{N},\"\")", "0"),
         ("Bought, not wrapped", f"=COUNTIFS('Gift List'!I6:I{N},\"Bought\")+COUNTIFS('Gift List'!I6:I{N},\"Ordered\")", "0")]
for i, (a, f, fmt) in enumerate(items):
    r = 4 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 28
header(d, 3, ["Group", "People", "Spent"], t, start=4)
for i, gr in enumerate(GROUPS):
    r = 4 + i; label(d, f"D{r}", gr)
    calc(d, f"E{r}", f"=COUNTIFS('Gift List'!$B$6:$B${N},D{r})", "0")
    calc(d, f"F{r}", f"=SUMIFS('Gift List'!$G$6:$G${N},'Gift List'!$B$6:$B${N},D{r})", '"$"#,##0.00')
header(d, 14, ["Status", "Gifts"], t, start=4)
for i, st in enumerate(STATUS):
    r = 15 + i; label(d, f"D{r}", st); calc(d, f"E{r}", f"=COUNTIFS('Gift List'!$I$6:$I${N},D{r})", "0")
d.conditional_formatting.add("B7", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, size=16, bold=True, color="C00000")))

# Cards
c = wb.create_sheet("Cards")
banner(c, t, "Christmas card list", "Who to send cards to, their address, and who has sent you one.", 5)
header(c, 5, ["Name", "Address", "Sent?", "Received?", "Notes"], t)
widths(c, {"A": 22, "B": 44, "C": 10, "D": 11, "E": 24})
for r in range(6, 106):
    for col in "ABCDE": inp(c, f"{col}{r}")
    for col in "ABE": c[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
dv_list(c, "C6:D105", "Yes,No")
c["A6"] = "The Millers"; c["B6"] = "12 Holly Lane, Springfield"; c["C6"] = "Yes"
for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.save(sys.argv[1]); print("saved")
