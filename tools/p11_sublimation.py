"""Sublimation & Tumbler Business Spreadsheet (batch 7, lane a): blanks & supplies with cost per piece, ink cost per print by
coverage, product costing & pricing (blank, paper, ink, tape, shrink wrap, design licence per use, packaging, misprints,
labour, fees), bulk order quote calculator with quantity discount tiers, order tracker (proofs, deposits, deadlines),
sales log and dashboard. Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.utils import get_column_letter as gl

t = Theme("1E5D73", "E0567A", "E6F1F4")
wb = Workbook()
NS, NP, NO, NSALE = 105, 45, 205, 506
USD, USD4 = '"$"#,##0.00', '"$"#,##0.000'
GREY = "62727A"

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Sublimation & Tumbler Business Spreadsheet", "Cost every tumbler, mug and shirt to the cent, quote bulk orders in seconds and track every order.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly rate, overheads, mark-ups, Etsy fee estimate, ink set price and prints per set, misprint allowance and bulk discount tiers.",
         "Supplies: add each blank, paper, tape, shrink wrap, packaging and design licence once, with the pack size and price. Cost per piece is worked out.",
         "Product Pricing: one row per product. Pick the blank, paper, ink coverage, extras and press time. Cost, wholesale and retail prices appear.",
         "Bulk Quote: pick a product and a quantity (a team order, a wedding, a school). The discount tier, price each, total, deposit and your profit appear.",
         "Orders: track every order from New to Proof sent, Approved, Pressed and Shipped, with deposits, balance due and deadline flags.",
         "Sales and Dashboard: log every sale; profit, best sellers, open orders and money still to collect update for you."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Ink cost: divide what you pay for a full ink set by roughly how many full-coverage letter-size prints it gives you (check your printer's "
      "yield, or count your own). Light, medium, heavy and full coverage then use 25%, 50%, 75% and 100% of that.", size=10, color="7A2E45")
s.row_dimensions[14].height = 44
label(s, "B15", "Design licences: if you buy designs with a commercial licence that allows a set number of uses, add them as a supply with the number of "
      "uses as the pack size, and the cost per use is added to each item. Only use designs you have the rights to sell.", size=10, color="7A2E45")
s.row_dimensions[15].height = 44
label(s, "B16", "Example supplies, products, orders and sales are included so you can see how it works: type over them or delete them. "
      "Prices in the examples are illustrations only. Works in Excel and Google Sheets.", italic=True, size=10)
s.row_dimensions[16].height = 30

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates. Every product and quote uses these.", 4)
widths(st, {"A": 44, "B": 16, "C": 4, "D": 66})
rows = [("Your hourly rate", 20, USD, "Design set-up, printing, taping, pressing, wrapping and packing time."),
        ("Overheads (% of materials)", 0.10, "0%", "Electricity, press and printer wear, gloves, butcher paper, teflon sheets."),
        ("Wholesale price = cost x", 1.8, '0.0"x"', "Bulk and wholesale orders start from this price."),
        ("Retail price = wholesale x", 1.8, '0.0"x"', "Single orders on Etsy and at markets."),
        ("Round prices up to the nearest", 1, USD, "Use 0.5 or 1 for clean prices."),
        ("Etsy transaction fee", 0.065, "0.0%", "Estimate. Check Etsy's current fees for your country."),
        ("Payment processing (%)", 0.03, "0.0%", "Estimate, varies by country."),
        ("Payment processing (fixed per order)", 0.25, USD, None),
        ("Listing fee per sale", 0.20, USD, None),
        ("Ink set price (all colours)", 129.99, USD, "What you pay for a full set of sublimation ink."),
        ("Full-coverage letter prints per ink set", 300, "#,##0", "Rough yield. Light prints use far less."),
        ("Misprint / reject allowance", 0.05, "0%", "Ghosting, blowouts, a blank with a dent. Added to material cost."),
        ("Deposit for custom and bulk orders", 0.5, "0%", None)]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"D{5 + i}", n, size=9, color=GREY, italic=True)
RATE, OVH, WMUL, RMUL, RND, ETX, PPC, PFX, LST, INK, YIELD, MIS, DEP = (f"Settings!$B${5 + i}" for i in range(13))
label(st, "A18", "Ink cost per full-coverage letter sheet", bold=True); calc(st, "B18", f"=IFERROR({INK}/{YIELD},0)", USD4)
INKS = "Settings!$B$18"
label(st, "A20", "Ink coverage", bold=True, size=12); label(st, "B20", "Share of a full print", bold=True, size=10)
for i, (c, v) in enumerate([("Light", 0.25), ("Medium", 0.5), ("Heavy", 0.75), ("Full wrap", 1)]):
    label(st, f"A{21 + i}", c); inp(st, f"B{21 + i}", v, "0%")
COV = "Settings!$A$21:$B$24"
label(st, "A26", "Bulk discount tiers", bold=True, size=12); label(st, "B26", "From qty", bold=True, size=10); label(st, "D26", "Discount off the wholesale price", bold=True, size=10)
for i, (q, dsc) in enumerate([(1, 0), (12, 0.05), (24, 0.10), (50, 0.15), (100, 0.20)]):
    label(st, f"A{27 + i}", f"Tier {i + 1}"); inp(st, f"B{27 + i}", q, "0"); inp(st, f"D{27 + i}", dsc, "0%")
TQ, TD = "Settings!$B$27:$B$31", "Settings!$D$27:$D$31"
label(st, "A33", "Keep the 'From qty' numbers going up. A quote for 30 pieces uses the tier that starts at 24.", italic=True, size=9, color=GREY)
TYPES = "Tumbler blank,Mug blank,Shirt / apparel,Other blank,Sublimation paper,Tape,Shrink wrap,Packaging,Design licence,Other"

# ---------- Supplies ----------
su = wb.create_sheet("Supplies")
banner(su, t, "Blanks & supplies", "Add each supply once. Cost per piece (or per use) is worked out for you.", 10)
header(su, 5, ["Supply", "Type", "Pack size (pieces / uses)", "Pack price", "Cost each", "On hand (pieces)", "Reorder at", "Stock status", "Supplier / notes"], t)
su.row_dimensions[5].height = 44
widths(su, {"A": 36, "B": 16, "C": 13, "D": 11, "E": 11, "F": 12, "G": 10, "H": 13, "I": 30}); su.freeze_panes = "B6"
for r in range(6, NS + 1):
    for col in "ABCDFGI": inp(su, f"{col}{r}")
    for col in "AI": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    su[f"D{r}"].number_format = USD
    for col in "CFG": su[f"{col}{r}"].number_format = "#,##0"
    calc(su, f"E{r}", f'=IF(OR(A{r}="",N(C{r})=0,D{r}=""),"",D{r}/C{r})', USD4)
    calc(su, f"H{r}", f'=IF(OR(A{r}="",F{r}=""),"",IF(F{r}<=N(G{r}),"Reorder","OK"))')
ex = [("20 oz skinny tumbler blank (white)", "Tumbler blank", 25, 89.99, 18, 10, "Straight, with lid + straw"),
      ("30 oz tumbler blank (white)", "Tumbler blank", 25, 112.99, 9, 10, ""),
      ("15 oz ceramic mug blank", "Mug blank", 36, 79.99, 40, 12, "AAA coating"),
      ("Polyester tee (white, mixed sizes)", "Shirt / apparel", 12, 47.99, 14, 6, "95% polyester"),
      ("MDF keychain blank + ring", "Other blank", 50, 14.99, 60, 20, ""),
      ("Sublimation paper 8.5 x 11", "Sublimation paper", 110, 15.99, 160, 50, ""),
      ("Sublimation paper 11 x 17", "Sublimation paper", 100, 24.99, 45, 30, "For 30 oz wraps"),
      ("Heat-resistant tape (uses)", "Tape", 200, 7.99, 300, 50, "One roll = about 100 items"),
      ("Shrink wrap sleeve", "Shrink wrap", 100, 11.99, 70, 25, "For convection oven"),
      ("Tumbler gift box", "Packaging", 25, 27.99, 20, 10, ""),
      ("Mug box (white)", "Packaging", 36, 29.99, 30, 12, ""),
      ("Poly mailer + tissue + card", "Packaging", 50, 18.99, 35, 15, ""),
      ("Floral wrap design (licence, 200 uses)", "Design licence", 200, 6.00, None, None, "Commercial licence, check terms"),
      ("Teacher quote design (licence, 100 uses)", "Design licence", 100, 4.00, None, None, "Commercial licence, check terms")]
for i, row in enumerate(ex):
    for j, v in enumerate(row):
        if v is not None: su.cell(6 + i, [1, 2, 3, 4, 6, 7, 9][j]).value = v
dv_list(su, f"B6:B{NS}", TYPES)
su.conditional_formatting.add(f"H6:H{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=PatternFill("solid", fgColor="F8D7D3"), font=Font(name=F, bold=True, color="A12A1E")))
SNAME, SEACH = (f"Supplies!${c}$6:${c}${NS}" for c in "AE")
SLIST = f"=Supplies!$A$6:$A${NS}"

def look(ref):
    return f'IF({ref}="",0,IFERROR(INDEX({SEACH},MATCH({ref},{SNAME},0)),0))'

# ---------- Product Pricing ----------
pp = wb.create_sheet("Product Pricing")
banner(pp, t, "Product costing & pricing", "One row per product. Pick your blank and supplies: cost, wholesale and retail prices appear.", 22)
cols = ["Product", "Blank", "Paper", "Sheets per item", "Ink coverage", "Tape", "Shrink wrap / extra", "Design licence", "Packaging", "Labour (min)",
        "Blank cost", "Paper & ink", "Tape, wrap, design & box", "Misprint allowance", "Labour", "Overheads",
        "COST PER ITEM", "Wholesale price", "Retail price", "Etsy fees (est.)", "Profit per retail sale", "Margin"]
header(pp, 5, cols, t); pp.row_dimensions[5].height = 46
for i, w in enumerate([30, 30, 24, 9, 12, 22, 20, 30, 24, 9, 10, 10, 13, 10, 9, 10, 12, 11, 11, 10, 12, 8]): pp.column_dimensions[gl(i + 1)].width = w
pp.freeze_panes = "B6"
label(pp, "A4", "Sheets per item: a 20 oz wrap fits one letter sheet; two mug wraps often fit one sheet (type 0.5).", italic=True, size=9, color=GREY)
for r in range(6, NP + 1):
    for col in "ABCDEFGHIJ": inp(pp, f"{col}{r}")
    for col in "ABCFGHI": pp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    on = f'A{r}=""'
    calc(pp, f"K{r}", f'=IF({on},"",{look(f"B{r}")})', USD)
    calc(pp, f"L{r}", f'=IF({on},"",N(D{r})*({look(f"C{r}")}+{INKS}*IFERROR(VLOOKUP(E{r},{COV},2,FALSE),0)))', USD)
    calc(pp, f"M{r}", f'=IF({on},"",{look(f"F{r}")}+{look(f"G{r}")}+{look(f"H{r}")}+{look(f"I{r}")})', USD)
    calc(pp, f"N{r}", f'=IF({on},"",(K{r}+L{r})*{MIS})', USD)
    calc(pp, f"O{r}", f'=IF({on},"",N(J{r})/60*{RATE})', USD)
    calc(pp, f"P{r}", f'=IF({on},"",(K{r}+L{r}+M{r})*{OVH})', USD)
    calc(pp, f"Q{r}", f'=IF({on},"",K{r}+L{r}+M{r}+N{r}+O{r}+P{r})', USD, bold=True)
    calc(pp, f"R{r}", f'=IF({on},"",CEILING(Q{r}*{WMUL},{RND}))', USD, bold=True)
    calc(pp, f"S{r}", f'=IF({on},"",CEILING(R{r}*{RMUL},{RND}))', USD, bold=True)
    calc(pp, f"T{r}", f'=IF({on},"",S{r}*({ETX}+{PPC})+{PFX}+{LST})', USD)
    calc(pp, f"U{r}", f'=IF({on},"",S{r}-Q{r}-T{r})', USD, bold=True)
    calc(pp, f"V{r}", f'=IF(OR({on},N(S{r})=0),"",U{r}/S{r})', "0%")
prods = [("20 oz floral skinny tumbler", "20 oz skinny tumbler blank (white)", "Sublimation paper 8.5 x 11", 1, "Full wrap", "Heat-resistant tape (uses)", "Shrink wrap sleeve", "Floral wrap design (licence, 200 uses)", "Tumbler gift box", 15),
         ("Custom name 30 oz tumbler", "30 oz tumbler blank (white)", "Sublimation paper 11 x 17", 1, "Full wrap", "Heat-resistant tape (uses)", "Shrink wrap sleeve", None, "Tumbler gift box", 20),
         ("Photo mug 15 oz", "15 oz ceramic mug blank", "Sublimation paper 8.5 x 11", 0.5, "Heavy", "Heat-resistant tape (uses)", None, None, "Mug box (white)", 8),
         ("Teacher appreciation mug", "15 oz ceramic mug blank", "Sublimation paper 8.5 x 11", 0.5, "Medium", "Heat-resistant tape (uses)", None, "Teacher quote design (licence, 100 uses)", "Mug box (white)", 6),
         ("Family reunion tee", "Polyester tee (white, mixed sizes)", "Sublimation paper 8.5 x 11", 1, "Medium", "Heat-resistant tape (uses)", None, None, "Poly mailer + tissue + card", 7),
         ("Photo keychain", "MDF keychain blank + ring", "Sublimation paper 8.5 x 11", 0.1, "Heavy", "Heat-resistant tape (uses)", None, None, None, 3)]
for i, row in enumerate(prods):
    for j, v in enumerate(row):
        if v is not None: pp.cell(6 + i, 1 + j).value = v
for rng in (f"B6:C{NP}", f"F6:I{NP}"): dv_list(pp, rng, SLIST)
dv_list(pp, f"E6:E{NP}", "=Settings!$A$21:$A$24")
pp.conditional_formatting.add(f"U6:U{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
legend(pp, NP + 2, 1)
PNAME, PCOST, PWH, PRET = (f"'Product Pricing'!${c}$6:${c}${NP}" for c in "AQRS")

# ---------- Bulk Quote ----------
bq = wb.create_sheet("Bulk Quote")
banner(bq, t, "Bulk order quote", "Team shirts, wedding tumblers, teacher gifts: price any quantity in seconds.", 7)
widths(bq, {"A": 28, "B": 26, "C": 2, "D": 28, "E": 14, "F": 16, "G": 16})
qi = [("Customer", "Lincoln School PTA", None), ("Product", "Teacher appreciation mug", None), ("Quantity", 36, "0"),
      ("Set-up / design fee (one-off)", 15, USD), ("Rush fee (one-off)", 0, USD), ("Shipping charged", 18, USD)]
label(bq, "A4", "The order", bold=True, size=13)
for i, (a, v, fmt) in enumerate(qi):
    r = 5 + i; label(bq, f"A{r}", a); c = inp(bq, f"B{r}", v, fmt)
    if i < 2: c.alignment = Alignment(horizontal="left", indent=1)
dv_list(bq, "B6", "=" + PNAME)
M = f"MATCH($B$6,{PNAME},0)"
label(bq, "D4", "Your quote", bold=True, size=13)
qo = [("Cost per item", f"=IFERROR(INDEX({PCOST},{M}),\"\")", USD, False),
      ("Wholesale price each", f"=IFERROR(INDEX({PWH},{M}),\"\")", USD, False),
      ("Bulk discount", f"=IFERROR(LOOKUP(B7,{TQ},{TD}),0)", "0%", True),
      ("PRICE EACH", f'=IF(E6="","",CEILING(E6*(1-E7),0.25))', USD, True),
      ("Items subtotal", '=IF(E8="","",E8*B7)', USD, False),
      ("QUOTE TOTAL", '=IF(E9="","",E9+N(B8)+N(B9)+N(B10))', USD, True),
      ("Deposit to ask for", f'=IF(E10="","",ROUND(E10*{DEP},2))', USD, True),
      ("Your total cost", '=IF(E5="","",E5*B7)', USD, False),
      ("Your profit on this order", '=IF(E10="","",E10-N(B10)-E12)', USD, True),
      ("Profit per item", '=IF(OR(E13="",N(B7)=0),"",E13/B7)', USD, False),
      ("Price check", '=IF(E8="","",IF(E8<E5,"Below cost!",IF(E8<E5*1.3,"Thin margin","Healthy")))', None, True)]
for i, (a, f, fmt, b) in enumerate(qo):
    r = 5 + i; label(bq, f"D{r}", a, bold=b); calc(bq, f"E{r}", f, fmt, bold=b)
bq["E10"].font = Font(name=F, size=16, bold=True, color="1F2A44"); bq.row_dimensions[10].height = 28
bq["E8"].font = Font(name=F, size=14, bold=True, color="1F2A44")
bq.conditional_formatting.add("E15", CellIsRule(operator="equal", formula=['"Below cost!"'], fill=PatternFill("solid", fgColor="F8D7D3"), font=Font(name=F, bold=True, color="A12A1E")))
bq.conditional_formatting.add("E15", CellIsRule(operator="equal", formula=['"Thin margin"'], fill=PatternFill("solid", fgColor="FCEBC8"), font=Font(name=F, bold=True, color="8A5A12")))
bq.conditional_formatting.add("E15", CellIsRule(operator="equal", formula=['"Healthy"'], fill=PatternFill("solid", fgColor="E3F0E1"), font=Font(name=F, bold=True, color="2E6B3A")))
label(bq, "A18", "Price ladder for this product", bold=True, size=12)
header(bq, 19, ["Quantity", "Discount", "", "Price each", "Total (items)", "Your profit"], t)
for i in range(5):
    r = 20 + i
    calc(bq, f"A{r}", f"=INDEX({TQ},{i + 1})", "0"); calc(bq, f"B{r}", f"=INDEX({TD},{i + 1})", "0%")
    calc(bq, f"D{r}", f'=IF($E$6="","",CEILING($E$6*(1-B{r}),0.25))', USD); calc(bq, f"E{r}", f'=IF(D{r}="","",D{r}*A{r})', USD)
    calc(bq, f"F{r}", f'=IF(D{r}="","",(D{r}-$E$5)*A{r})', USD)
label(bq, "A26", "Send customers the ladder so they can see the saving for ordering more. Tiers and discounts are on the Settings tab.", italic=True, size=9, color=GREY)

# ---------- Orders ----------
od = wb.create_sheet("Orders")
banner(od, t, "Order tracker", "Every order from New to Shipped: proofs, deposits, balance and deadlines.", 16)
cols = ["Order #", "Customer", "Product", "Personalisation / design", "Qty", "Price each (blank = retail)", "Status", "Deposit paid", "Order date", "Ship by", "Notes",
        "Order total", "Balance due", "Days to ship-by", "Flag"]
header(od, 5, cols, t); od.row_dimensions[5].height = 44
widths(od, {"A": 9, "B": 20, "C": 28, "D": 28, "E": 6, "F": 12, "G": 13, "H": 11, "I": 12, "J": 12, "K": 24, "L": 12, "M": 12, "N": 10, "O": 12})
od.freeze_panes = "C6"
STAT = "New,Proof sent,Approved,Printing,Pressed,Shipped,Cancelled"
for r in range(6, NO + 1):
    for col in "ABCDEFGHIJK": inp(od, f"{col}{r}")
    for col in "BCDK": od[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    for col in "IJ": od[f"{col}{r}"].number_format = "dd mmm yyyy"
    for col in "FH": od[f"{col}{r}"].number_format = USD
    on = f'C{r}=""'
    calc(od, f"L{r}", f'=IF({on},"",N(E{r})*IF(F{r}="",IFERROR(INDEX({PRET},MATCH(C{r},{PNAME},0)),0),F{r}))', USD)
    calc(od, f"M{r}", f'=IF(OR({on},G{r}="Cancelled"),"",L{r}-N(H{r}))', USD, bold=True)
    calc(od, f"N{r}", f'=IF(OR(J{r}="",G{r}="Shipped",G{r}="Cancelled"),"",J{r}-TODAY())', "0")
    calc(od, f"O{r}", f'=IF(N{r}="","",IF(N{r}<0,"LATE",IF(AND(N{r}<=2,OR(G{r}="New",G{r}="Proof sent")),"Chase proof",IF(N{r}<=2,"Due soon","On track"))))')
dv_list(od, f"G6:G{NO}", STAT); dv_list(od, f"C6:C{NO}", "=" + PNAME)
ords = [("S-201", "Kayla M.", "Custom name 30 oz tumbler", "'Kayla' in pink script, leopard", 1, None, "Pressed", "full", -3, 1, "Gift wrap"),
        ("S-202", "Lincoln School PTA", "Teacher appreciation mug", "School logo + teacher names", 36, "q", "Proof sent", 300, -2, 2, "Invoice sent"),
        ("S-203", "Ruiz family", "Family reunion tee", "Ruiz Reunion 2027, sizes list", 24, 14, "Approved", 168, -5, 9, "Sizes: 6S 8M 6L 4XL"),
        ("S-204", "Etsy order", "20 oz floral skinny tumbler", "", 2, None, "New", None, 0, 4, "")]
for i, (n, cu, pr, pers, q, pe, sta, dep, od_, due, note) in enumerate(ords):
    r = 6 + i; od[f"A{r}"] = n; od[f"B{r}"] = cu; od[f"C{r}"] = pr; od[f"D{r}"] = pers; od[f"E{r}"] = q; od[f"G{r}"] = sta; od[f"K{r}"] = note
    if pe == "q": od[f"F{r}"] = "='Bulk Quote'!E8"
    elif pe is not None: od[f"F{r}"] = pe
    if dep == "full": od[f"H{r}"] = f"=L{r}"
    elif dep is not None: od[f"H{r}"] = dep
    od[f"I{r}"] = f"=TODAY(){od_:+d}" if od_ else "=TODAY()"; od[f"J{r}"] = f"=TODAY()+{due}"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")
for val, fill, col in (('"LATE"', red, "A12A1E"), ('"Chase proof"', red, "A12A1E"), ('"Due soon"', amb, "8A5A12"), ('"On track"', grn, "2E6B3A")):
    od.conditional_formatting.add(f"O6:O{NO}", CellIsRule(operator="equal", formula=[val], fill=fill, font=Font(name=F, bold=True, color=col)))

# ---------- Sales ----------
sa = wb.create_sheet("Sales")
banner(sa, t, "Sales log", "One row per sale. Cost comes from Product Pricing, so profit is real.", 11)
header(sa, 5, ["Date", "Channel", "Product", "Qty", "Price each", "Sale total", "Fees & shipping paid", "Cost of goods", "Profit", "Month", "Notes"], t)
widths(sa, {"A": 13, "B": 13, "C": 30, "D": 7, "E": 11, "F": 12, "G": 13, "H": 13, "I": 12, "J": 9, "K": 24}); sa.freeze_panes = "A6"
for r in range(6, NSALE + 1):
    for col in "ABCDEGK": inp(sa, f"{col}{r}")
    for col in "CK": sa[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sa[f"A{r}"].number_format = "dd mmm yyyy"; sa[f"E{r}"].number_format = USD; sa[f"G{r}"].number_format = USD
    calc(sa, f"F{r}", f'=IF(OR(D{r}="",E{r}=""),"",D{r}*E{r})', USD)
    calc(sa, f"H{r}", f'=IF(OR(C{r}="",D{r}=""),"",D{r}*IFERROR(INDEX({PCOST},MATCH(C{r},{PNAME},0)),0))', USD)
    calc(sa, f"I{r}", f'=IF(F{r}="","",F{r}-N(G{r})-N(H{r}))', USD)
    calc(sa, f"J{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
CH = ["Etsy", "Facebook", "Market", "Bulk order", "Wholesale", "Other"]
dv_list(sa, f"B6:B{NSALE}", ",".join(CH)); dv_list(sa, f"C6:C{NSALE}", "=" + PNAME)
for i, (back, ch, pr, q, price, fees, note) in enumerate([(14, "Etsy", "20 oz floral skinny tumbler", 1, "r6", "etsy", ""),
                                                         (10, "Bulk order", "Teacher appreciation mug", 24, 7.75, 0, "Church group"),
                                                         (6, "Facebook", "Custom name 30 oz tumbler", 2, "r7", 0, "Local pickup"),
                                                         (3, "Market", "Photo keychain", 9, 8, 0, "Holiday market"),
                                                         (1, "Etsy", "Photo mug 15 oz", 2, "r8", "etsy", "")]):
    r = 6 + i; sa[f"A{r}"] = f"=TODAY()-{back}"; sa[f"B{r}"] = ch; sa[f"C{r}"] = pr; sa[f"D{r}"] = q; sa[f"K{r}"] = note
    sa[f"E{r}"] = price if isinstance(price, (int, float)) else f"='Product Pricing'!S{price[1:]}"
    sa[f"G{r}"] = fees if fees != "etsy" else f"=ROUND(F{r}*({ETX}+{PPC})+{PFX}+{LST},2)"
SD, SCH, SC, SQ, ST, SG, SH, SPF = (f"Sales!${c}$6:${c}${NSALE}" for c in "ABCDFGHI")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Sales, Orders and Supplies.", 9)
widths(d, {"A": 28, "B": 15, "C": 14, "D": 14, "E": 14, "F": 4, "G": 30, "H": 12, "I": 14})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{SD},">="&DATE($B$4,1,1),{SD},"<"&DATE($B$4+1,1,1)'
OPEN = f'"<>Shipped",Orders!$G$6:$G${NO},"<>Cancelled"'
kpi = [("Sales", f"=SUMIFS({ST},{yr})", USD), ("Profit", f"=SUMIFS({SPF},{yr})", USD), ("Items sold", f"=SUMIFS({SQ},{yr})", "#,##0"),
       ("Profit margin", '=IF(B6=0,"",B7/B6)', "0%"),
       ("Open orders", f'=COUNTIFS(Orders!$C$6:$C${NO},"<>",Orders!$G$6:$G${NO},{OPEN})', "0"),
       ("Items to press", f'=SUMIFS(Orders!$E$6:$E${NO},Orders!$G$6:$G${NO},"<>Pressed",Orders!$G$6:$G${NO},{OPEN})', "#,##0"),
       ("Balance still to collect", f'=SUMIFS(Orders!$M$6:$M${NO},Orders!$G$6:$G${NO},{OPEN})', USD),
       ("Orders late / need attention", f'=COUNTIF(Orders!$O$6:$O${NO},"LATE")+COUNTIF(Orders!$O$6:$O${NO},"Chase proof")', "0"),
       ("Supplies to reorder", f'=COUNTIF(Supplies!$H$6:$H${NS},"Reorder")', "0")]
for i, (a, f, fmt) in enumerate(kpi):
    r = 6 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 28
header(d, 16, ["Month", "Sales", "Fees & shipping", "Cost", "Profit"], t)
for i, mn in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    r = 17 + i; label(d, f"A{r}", mn)
    mr = f'{SD},">="&DATE($B$4,{i + 1},1),{SD},"<"&DATE($B$4,{i + 2},1)'
    for col, rg in zip("BCDE", (ST, SG, SH, SPF)): calc(d, f"{col}{r}", f"=SUMIFS({rg},{mr})", USD)
label(d, "A29", "Total", bold=True)
for col in "BCDE": calc(d, f"{col}29", f"=SUM({col}17:{col}28)", USD, bold=True)
header(d, 16, ["Channel", "Sales", "Profit"], t, start=7)
for i, ch in enumerate(CH):
    r = 17 + i; label(d, f"G{r}", ch)
    calc(d, f"H{r}", f'=SUMIFS({ST},{SCH},G{r},{yr})', USD); calc(d, f"I{r}", f'=SUMIFS({SPF},{SCH},G{r},{yr})', USD)
header(d, 25, ["Product", "Items sold", "Profit"], t, start=7)
for i in range(12):
    r = 26 + i
    d[f"G{r}"] = f"=IF('Product Pricing'!A{6 + i}=\"\",\"\",'Product Pricing'!A{6 + i})"; d[f"G{r}"].font = Font(name=F, size=11)
    calc(d, f"H{r}", f'=IF(G{r}="","",SUMIFS({SQ},{SC},G{r},{yr}))', "#,##0")
    calc(d, f"I{r}", f'=IF(G{r}="","",SUMIFS({SPF},{SC},G{r},{yr}))', USD)
label(d, "G38", "Shows your first 12 products from Product Pricing.", italic=True, size=9, color=GREY)

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
