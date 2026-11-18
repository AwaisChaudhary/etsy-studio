import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment
t = Theme("8A2858", "B8326A", "F6E3EC")
wb = Workbook(); N = 80
s = wb.active; s.title = "Start Here"
banner(s, t, "Crochet & Knitting Pricing Calculator", "Price handmade items so every sale pays for your yarn, your time and the selling fees.", 6)
widths(s, {"A": 6, "B": 90})
steps = ["Open Settings and enter your hourly rate, packaging cost and the fees your shop charges (the defaults are typical marketplace fees, so check yours).",
         "List your yarn and supplies on the Materials tab once: pack size and price. The cost per yard, metre, gram or piece is worked out for you.",
         "On Price It, name the item, enter how long it takes, then pick the materials it uses and how much. The recommended price appears on the right.",
         "Thinking of a different price? Type it in 'Try your own price' to see what you'd really earn per hour.",
         "Keep a record of every item you sell on the My Items tab."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color="B8326A"); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 11, 2)
label(s, "B13", "Works in Excel and Google Sheets. Example materials and an example item are filled in so you can see how it works.", italic=True, size=10)
# Settings
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rate, packaging and selling fees.", 4)
widths(st, {"A": 42, "B": 16, "C": 4, "D": 56})
rows = [("Your hourly rate ($)", 15, '"$"#,##0.00', "What your time is worth. Even if you craft for fun, include it so your prices are sustainable."),
        ("Packaging per order ($)", 1.5, '"$"#,##0.00', "Bag, tag, tissue, sticker."),
        ("Marketplace transaction fee", 0.065, "0.0%", "Percentage of the sale the marketplace keeps. Check your own shop's fees."),
        ("Payment processing fee (%)", 0.03, "0.0%", "Varies by country and platform."),
        ("Payment processing fee (fixed, $)", 0.25, '"$"#,##0.00', None),
        ("Listing fee per sale ($)", 0.2, '"$"#,##0.00', None),
        ("Target profit margin", 0.2, "0%", "Extra on top of costs and your wage, for growing the business.")]
for i, (a, v, fmt, n) in enumerate(rows):
    r = 5 + i; label(st, f"A{r}", a); inp(st, f"B{r}", v, fmt, n)
label(st, "D5", "Fees differ by country and platform. Look up your own and type them in.", italic=True, size=10)
# Materials
m = wb.create_sheet("Materials")
banner(m, t, "Materials", "Your yarn and supplies. Enter each once and reuse it in every price.", 6)
header(m, 5, ["Material", "Type", "Unit", "Pack size", "Pack price", "Cost per unit"], t)
widths(m, {"A": 34, "B": 12, "C": 10, "D": 12, "E": 12, "F": 14}); m.freeze_panes = "A6"
ex = [("Worsted acrylic, cream", "Yarn", "yards", 364, 7.49), ("Cotton DK, sage", "Yarn", "yards", 230, 6.99), ("Merino aran, rust", "Yarn", "metres", 150, 9.5),
      ("Safety eyes 12 mm (pair)", "Notion", "each", 10, 4.99), ("Polyester stuffing", "Notion", "grams", 340, 9.99), ("Wooden buttons", "Notion", "each", 20, 3.99)]
for r in range(6, N + 1):
    for col in "ABCDE": inp(m, f"{col}{r}"); m[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    m[f"E{r}"].number_format = '"$"#,##0.00'
    calc(m, f"F{r}", f'=IF(OR(D{r}="",E{r}="",D{r}=0),"",E{r}/D{r})', '"$"#,##0.0000')
for i, row in enumerate(ex):
    for j, v in enumerate(row): m.cell(6 + i, 1 + j).value = v
dv_list(m, f"B6:B{N}", "Yarn,Notion,Packaging,Other"); dv_list(m, f"C6:C{N}", "yards,metres,grams,each")
# Price it
p = wb.create_sheet("Price It")
banner(p, t, "Price it", "Pick materials and enter your time. The recommended price is on the right.", 6)
widths(p, {"A": 34, "B": 14, "C": 10, "D": 13, "E": 34, "F": 16})
label(p, "A4", "Item name"); inp(p, "B4", "Amigurumi bunny", "@"); p.merge_cells("B4:D4")
label(p, "A5", "Hours to make"); inp(p, "B5", 3.5, "0.0")
header(p, 7, ["Material used", "Amount", "Unit", "Cost"], t)
for r in range(8, 18):
    inp(p, f"A{r}"); p[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); inp(p, f"B{r}", None, "0.##")
    calc(p, f"C{r}", f'=IF(A{r}="","",IFERROR(INDEX(Materials!$C$6:$C${N},MATCH(A{r},Materials!$A$6:$A${N},0)),""))')
    calc(p, f"D{r}", f'=IF(OR(A{r}="",B{r}=""),0,IFERROR(B{r}*INDEX(Materials!$F$6:$F${N},MATCH(A{r},Materials!$A$6:$A${N},0)),0))', '"$"#,##0.00')
dv_list(p, "A8:A17", f"=Materials!$A$6:$A${N}")
for r, (a, b) in enumerate([("Worsted acrylic, cream", 180), ("Safety eyes 12 mm (pair)", 1), ("Polyester stuffing", 60)]): p[f"A{8 + r}"] = a; p[f"B{8 + r}"] = b
label(p, "E4", "Your costs", bold=True, size=13)
res = [("Materials", "=SUM(D8:D17)"), ("Your time", "=B5*Settings!B5"), ("Packaging", "=Settings!B6"), ("Total cost", "=SUM(F5:F7)")]
for i, (a, f) in enumerate(res): label(p, f"E{5 + i}", a); calc(p, f"F{5 + i}", f, '"$"#,##0.00')
label(p, "E10", "RECOMMENDED PRICE", bold=True, size=13, color="8A2858")
calc(p, "F10", "=CEILING((F8+Settings!B9+Settings!B10)/(1-Settings!B7-Settings!B8-Settings!B11),1)-0.01", '"$"#,##0.00', big=True); p.row_dimensions[10].height = 34
label(p, "E11", "Selling fees on that price"); calc(p, "F11", "=F10*(Settings!B7+Settings!B8)+Settings!B9+Settings!B10", '"$"#,##0.00')
label(p, "E12", "Profit after costs and your wage"); calc(p, "F12", "=F10-F11-F8", '"$"#,##0.00', bold=True)
label(p, "E13", "You really earn per hour"); calc(p, "F13", "=IFERROR((F10-F11-F5-F7)/B5,0)", '"$"#,##0.00', bold=True)
label(p, "E15", "Try your own price", bold=True, size=13)
label(p, "E16", "Price you're thinking of"); inp(p, "F16", 24, '"$"#,##0.00')
label(p, "E17", "Profit after costs and your wage"); calc(p, "F17", "=F16-(F16*(Settings!B7+Settings!B8)+Settings!B9+Settings!B10)-F8", '"$"#,##0.00', bold=True)
label(p, "E18", "You really earn per hour"); calc(p, "F18", "=IFERROR((F16-(F16*(Settings!B7+Settings!B8)+Settings!B9+Settings!B10)-F5-F7)/B5,0)", '"$"#,##0.00', bold=True)
legend(p, 20, 1)
# My items
it = wb.create_sheet("My Items")
banner(it, t, "My items", "A record of what you make and sell.", 8)
header(it, 5, ["Item", "Hours", "Materials cost", "Price", "Fees", "Profit after your wage", "Sold", "Notes"], t)
widths(it, {"A": 30, "B": 9, "C": 14, "D": 11, "E": 11, "F": 20, "G": 9, "H": 30}); it.freeze_panes = "A6"
for r in range(6, 106):
    for col in "ABCDGH": inp(it, f"{col}{r}")
    it[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); it[f"C{r}"].number_format = '"$"#,##0.00'; it[f"D{r}"].number_format = '"$"#,##0.00'
    calc(it, f"E{r}", f'=IF(D{r}="","",D{r}*(Settings!$B$7+Settings!$B$8)+Settings!$B$9+Settings!$B$10)', '"$"#,##0.00')
    calc(it, f"F{r}", f'=IF(D{r}="","",D{r}-E{r}-C{r}-B{r}*Settings!$B$5-Settings!$B$6)', '"$"#,##0.00')
for j, v in enumerate(["Amigurumi bunny", 3.5, 2.97, 74.99, None, None, 2, "Best seller at craft fair"]):
    if v is not None: it.cell(6, 1 + j).value = v
label(it, "E108", "Total profit (items x sold)", bold=True); calc(it, "F108", '=SUMPRODUCT(--(F6:F105<>""),N(+F6:F105),G6:G105)', '"$"#,##0.00', bold=True)
for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.save(sys.argv[1]); print("saved")
