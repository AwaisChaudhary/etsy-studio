import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule
t = Theme("7A4A2A", "B5733F", "F6EADF")
wb = Workbook(); N = 120
s = wb.active; s.title = "Start Here"
banner(s, t, "Home Baker Cost & Pricing Calculator", "Know exactly what every bake costs, price it properly, and keep track of orders.", 6)
widths(s, {"A": 6, "B": 90})
steps = ["Enter your hourly rate, overheads, packaging and profit margin on Settings.",
         "Add each ingredient once on the Ingredients tab: the pack size and what you paid. The cost per gram, millilitre or piece is worked out for you.",
         "On Recipe Cost, name the recipe, say how many it makes and how long it takes, then pick ingredients and amounts. You get the cost per item and a suggested price.",
         "Log every order on Orders: deposits, balances and due dates are tracked for you."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color="B5733F"); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 10, 2)
label(s, "B12", "Works in Excel and Google Sheets. Example ingredients, a recipe and an order are included. Ingredient prices are examples; use your own receipts.", italic=True, size=10)
s.row_dimensions[12].height = 30
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates. Every recipe uses these.", 4)
widths(st, {"A": 42, "B": 16, "C": 4, "D": 56})
rows = [("Your hourly rate ($)", 18, '"$"#,##0.00', "Include prep, baking, decorating and clean-up time."),
        ("Overheads (% of ingredient cost)", 0.12, "0%", "Electricity, gas, equipment wear, paper towels and so on."),
        ("Target profit margin", 0.3, "0%", None),
        ("Round prices up to the nearest ($)", 0.5, '"$"#,##0.00', None)]
for i, (a, v, fmt, n) in enumerate(rows): label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
ing = wb.create_sheet("Ingredients")
banner(ing, t, "Ingredients", "Enter each ingredient once with its pack size and price.", 6)
header(ing, 5, ["Ingredient", "Pack size", "Unit", "Pack price", "Cost per unit"], t)
widths(ing, {"A": 30, "B": 12, "C": 10, "D": 12, "E": 15}); ing.freeze_panes = "A6"
ex = [("Plain flour", 2000, "g", 3.49), ("Caster sugar", 1800, "g", 2.99), ("Unsalted butter", 454, "g", 4.99), ("Eggs", 12, "each", 3.99), ("Whole milk", 1890, "ml", 3.49),
      ("Vanilla extract", 59, "ml", 6.99), ("Cocoa powder", 226, "g", 4.49), ("Baking powder", 230, "g", 2.49), ("Cream cheese", 226, "g", 2.79), ("Icing sugar", 907, "g", 2.79),
      ("Chocolate chips", 340, "g", 3.99), ("Cupcake cases", 100, "each", 3.49), ("Cake box", 10, "each", 8.99)]
for r in range(6, N + 1):
    for col in "ABCD": inp(ing, f"{col}{r}"); ing[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    ing[f"D{r}"].number_format = '"$"#,##0.00'
    calc(ing, f"E{r}", f'=IF(OR(B{r}="",D{r}="",B{r}=0),"",D{r}/B{r})', '"$"#,##0.0000')
for i, row in enumerate(ex):
    for j, v in enumerate(row): ing.cell(6 + i, 1 + j).value = v
dv_list(ing, f"C6:C{N}", "g,ml,each,oz,lb,cup")
rc = wb.create_sheet("Recipe Cost")
banner(rc, t, "Recipe cost", "Pick ingredients and amounts. Cost per item and a suggested price appear on the right.", 6)
widths(rc, {"A": 30, "B": 12, "C": 9, "D": 12, "E": 32, "F": 16})
for i, (a, v, fmt) in enumerate([("Recipe", "Vanilla cupcakes", "@"), ("How many it makes", 12, "0"), ("Hours (prep to clean-up)", 1.5, "0.0")]):
    label(rc, f"A{4 + i}", a); inp(rc, f"B{4 + i}", v, fmt)
rc.merge_cells("B4:D4")
header(rc, 8, ["Ingredient", "Amount", "Unit", "Cost"], t)
for r in range(9, 29):
    inp(rc, f"A{r}"); rc[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); inp(rc, f"B{r}", None, "0.##")
    calc(rc, f"C{r}", f'=IF(A{r}="","",IFERROR(INDEX(Ingredients!$C$6:$C${N},MATCH(A{r},Ingredients!$A$6:$A${N},0)),""))')
    calc(rc, f"D{r}", f'=IF(OR(A{r}="",B{r}=""),0,IFERROR(B{r}*INDEX(Ingredients!$E$6:$E${N},MATCH(A{r},Ingredients!$A$6:$A${N},0)),0))', '"$"#,##0.00')
dv_list(rc, "A9:A28", f"=Ingredients!$A$6:$A${N}")
for i, (a, b) in enumerate([("Plain flour", 190), ("Caster sugar", 180), ("Unsalted butter", 170), ("Eggs", 3), ("Whole milk", 120), ("Vanilla extract", 10), ("Baking powder", 8), ("Icing sugar", 300), ("Cupcake cases", 12)]):
    rc[f"A{9 + i}"] = a; rc[f"B{9 + i}"] = b
label(rc, "E4", "Batch cost", bold=True, size=13)
res = [("Ingredients and packaging", "=SUM(D9:D28)"), ("Overheads", "=F5*Settings!B6"), ("Your time", "=B6*Settings!B5"), ("Total for the batch", "=SUM(F5:F7)"), ("Cost per item", "=IFERROR(F8/B5,0)")]
for i, (a, f) in enumerate(res): label(rc, f"E{5 + i}", a); calc(rc, f"F{5 + i}", f, '"$"#,##0.00')
label(rc, "E11", "SUGGESTED PRICE EACH", bold=True, size=13, color="7A4A2A")
calc(rc, "F11", "=CEILING(F9/(1-Settings!B7),Settings!B8)", '"$"#,##0.00', big=True); rc.row_dimensions[11].height = 34
label(rc, "E12", "Price per dozen"); calc(rc, "F12", "=F11*12", '"$"#,##0.00', bold=True)
label(rc, "E13", "Profit per batch (after your wage)"); calc(rc, "F13", "=F11*B5-F8", '"$"#,##0.00', bold=True)
legend(rc, 31, 1)
o = wb.create_sheet("Orders")
banner(o, t, "Orders", "Every order, deposit and balance in one place.", 11)
header(o, 5, ["Order date", "Customer", "Item", "Quantity", "Price each", "Total", "Deposit paid", "Balance due", "Due date", "Status", "Notes"], t)
widths(o, {"A": 13, "B": 20, "C": 24, "D": 10, "E": 11, "F": 11, "G": 13, "H": 13, "I": 13, "J": 13, "K": 30}); o.freeze_panes = "C6"
for r in range(6, 206):
    for col in "ABCDEGIJK": inp(o, f"{col}{r}")
    for col in "BCK": o[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    o[f"A{r}"].number_format = "dd mmm yyyy"; o[f"I{r}"].number_format = "dd mmm yyyy"; o[f"E{r}"].number_format = '"$"#,##0.00'; o[f"G{r}"].number_format = '"$"#,##0.00'
    calc(o, f"F{r}", f'=IF(OR(D{r}="",E{r}=""),"",D{r}*E{r})', '"$"#,##0.00')
    calc(o, f"H{r}", f'=IF(F{r}="","",F{r}-N(G{r}))', '"$"#,##0.00')
for j, v in enumerate(["=TODAY()-2", "Priya S.", "Vanilla cupcakes", 24, 3.5, None, 20, None, "=TODAY()+5", "Ordered", "Pink icing, birthday"]):
    if v is not None: o.cell(6, 1 + j).value = v
dv_list(o, "J6:J205", "Ordered,Baking,Ready,Delivered,Cancelled")
o.conditional_formatting.add("A6:K205", FormulaRule(formula=['$J6="Delivered"'], fill=PatternFill("solid", fgColor="E6F2E4")))
label(o, "E208", "Total sales", bold=True); calc(o, "F208", '=SUMIFS(F6:F205,J6:J205,"<>Cancelled")', '"$"#,##0.00', bold=True)
label(o, "G208", "Still to collect", bold=True); calc(o, "H208", '=SUMIFS(H6:H205,J6:J205,"<>Cancelled")', '"$"#,##0.00', bold=True)
for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.save(sys.argv[1]); print("saved")
