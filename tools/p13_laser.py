"""Laser Engraving Business Spreadsheet (batch 8, lane a): machine cost per hour (machine price over its working life, power,
air assist, lens/tube upkeep), materials library with cost per sheet and per square inch, product costing & pricing from part
size, engrave and cut minutes, extras, packaging, labour, waste and fees, profit per machine hour, bulk order quote with
discount tiers, order tracker (proofs, deposits, deadlines), sales log and dashboard. Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.utils import get_column_letter as gl

t = Theme("33302B", "C8692E", "F3ECE4")
wb = Workbook()
NS, NP, NO, NSALE = 105, 45, 205, 506
USD, USD4 = '"$"#,##0.00', '"$"#,##0.0000'
GREY = "6E675E"

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Laser Engraving Business Spreadsheet", "Know what every engraved and laser-cut piece really costs, what to charge, and what your machine earns per hour.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly rate, what your laser cost and how many hours you expect from it, power and upkeep per hour, mark-ups, fees and discount tiers.",
         "Materials: add each sheet (plywood, acrylic, leatherette) with its size and pack price, and each blank (slate, tumbler, board) or extra. Cost per square inch is worked out.",
         "Product Pricing: one row per product. Pick the material, type the part size, engrave and cut minutes and your hands-on time. Cost, prices, profit and profit per machine hour appear.",
         "Bulk Quote: pick a product and a quantity (a wedding, a company gift order, a school). The discount tier, price each, total, deposit and your profit appear.",
         "Orders: track every order from New to Proof sent, Approved, Engraving, Finishing and Shipped, with deposits, balance due and deadline flags.",
         "Sales and Dashboard: log every sale; profit, best sellers, open orders and money still to collect update for you."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Machine time: your laser wears out while it runs, so every minute of engraving and cutting is charged at your machine cost per hour "
      "(machine price spread over its working life, plus power, air assist and lens/tube upkeep). Your own time is charged separately at your hourly rate.", size=10, color="7A3B16")
s.row_dimensions[14].height = 44
label(s, "B15", "Engrave and cut minutes: use the time estimate from your laser software (LightBurn, xTool Creative Space, Glowforge app) or time a test piece. "
      "Only engrave designs you have the rights to sell.", size=10, color="7A3B16")
s.row_dimensions[15].height = 44
label(s, "B16", "Example materials, products, orders and sales are included so you can see how it works: type over them or delete them. "
      "Prices in the examples are illustrations only. Works in Excel and Google Sheets. Always follow your laser maker's safety instructions.", italic=True, size=10)
s.row_dimensions[16].height = 30

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates. Every product and quote uses these.", 4)
widths(st, {"A": 46, "B": 16, "C": 4, "D": 66})
rows = [("Your hourly rate", 25, USD, "Design, set-up, masking, sanding, finishing and packing time."),
        ("What your laser cost (incl. rotary, air assist, extractor)", 2500, USD, None),
        ("Working hours you expect from it", 3000, "#,##0", "Hours of actual running time before you replace it. 2,000-5,000 is a common guess for diode and CO2 lasers."),
        ("Power, air assist and extraction per hour", 0.40, USD, "Electricity for the laser, compressor and fan."),
        ("Lens, mirrors, tube / module upkeep per hour", 0.60, USD, "Set aside for parts that wear out (a CO2 tube, a diode module, lenses)."),
        ("Overheads (% of materials)", 0.10, "0%", "Test cuts, masking tape, wipes, honeycomb bed, software subscription."),
        ("Wholesale price = cost x", 1.8, '0.0"x"', "Bulk and wholesale orders start from this price."),
        ("Retail price = wholesale x", 1.6, '0.0"x"', "Single orders on Etsy and at markets."),
        ("Round prices up to the nearest", 1, USD, "Use 0.5 or 1 for clean prices."),
        ("Etsy transaction fee", 0.065, "0.0%", "Estimate. Check Etsy's current fees for your country."),
        ("Payment processing (%)", 0.03, "0.0%", "Estimate, varies by country."),
        ("Payment processing (fixed per order)", 0.25, USD, None),
        ("Listing fee per sale", 0.20, USD, None),
        ("Material waste allowance", 0.15, "0%", "Kerf, spacing between parts, offcuts and the odd failed piece."),
        ("Deposit for custom and bulk orders", 0.5, "0%", None)]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"D{5 + i}", n, size=9, color=GREY, italic=True)
RATE, MPR, MLIFE, PWR, UPK, OVH, WMUL, RMUL, RND, ETX, PPC, PFX, LST, WASTE, DEP = (f"Settings!$B${5 + i}" for i in range(15))
label(st, "A21", "MACHINE COST PER HOUR", bold=True); calc(st, "B21", f"=IFERROR({MPR}/{MLIFE},0)+{PWR}+{UPK}", USD, bold=True)
label(st, "D21", "Charged for every minute the laser runs (engrave + cut).", size=9, color=GREY, italic=True)
MCH = "Settings!$B$21"
label(st, "A23", "Bulk discount tiers", bold=True, size=12); label(st, "B23", "From qty", bold=True, size=10); label(st, "D23", "Discount off the wholesale price", bold=True, size=10)
for i, (q, dsc) in enumerate([(1, 0), (10, 0.05), (25, 0.10), (50, 0.15), (100, 0.20)]):
    label(st, f"A{24 + i}", f"Tier {i + 1}"); inp(st, f"B{24 + i}", q, "0"); inp(st, f"D{24 + i}", dsc, "0%")
TQ, TD = "Settings!$B$24:$B$28", "Settings!$D$24:$D$28"
label(st, "A30", "Keep the 'From qty' numbers going up. A quote for 30 pieces uses the tier that starts at 25.", italic=True, size=9, color=GREY)
TYPES = "Wood sheet,Acrylic sheet,Leather / leatherette,Other sheet,Blank (each),Hardware / extra,Finish,Packaging,Other"

# ---------- Materials ----------
su = wb.create_sheet("Materials")
banner(su, t, "Materials & supplies", "Sheets: type width and height to get cost per square inch. Blanks and extras: leave the size blank.", 12)
header(su, 5, ["Material / supply", "Type", "Sheet width (in)", "Sheet height (in)", "Pack size (sheets / pieces / uses)", "Pack price",
               "Cost per sheet / each", "Cost per sq in", "On hand", "Reorder at", "Stock status", "Supplier / notes"], t)
su.row_dimensions[5].height = 46
widths(su, {"A": 36, "B": 18, "C": 10, "D": 10, "E": 13, "F": 11, "G": 12, "H": 11, "I": 9, "J": 9, "K": 12, "L": 30}); su.freeze_panes = "B6"
for r in range(6, NS + 1):
    for col in "ABCDEFIJL": inp(su, f"{col}{r}")
    for col in "AL": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    su[f"F{r}"].number_format = USD
    for col in "EIJ": su[f"{col}{r}"].number_format = "#,##0"
    for col in "CD": su[f"{col}{r}"].number_format = "0.##"
    calc(su, f"G{r}", f'=IF(OR(A{r}="",N(E{r})=0,F{r}=""),"",F{r}/E{r})', USD4)
    calc(su, f"H{r}", f'=IF(OR(G{r}="",N(C{r})=0,N(D{r})=0),"",G{r}/(C{r}*D{r}))', USD4)
    calc(su, f"K{r}", f'=IF(OR(A{r}="",I{r}=""),"",IF(I{r}<=N(J{r}),"Reorder","OK"))')
ex = [("3 mm (1/8 in) Baltic birch plywood", "Wood sheet", 12, 20, 20, 54.99, 14, 5, "Laser-grade, low-void"),
      ("3 mm clear cast acrylic", "Acrylic sheet", 12, 12, 10, 39.99, 6, 3, "Cast engraves frosty white"),
      ("3 mm black mirror acrylic", "Acrylic sheet", 12, 12, 5, 29.99, 4, 2, ""),
      ("Leatherette sheet (black/gold)", "Leather / leatherette", 12, 24, 10, 28.99, 7, 3, "Laserable, for patches and tags"),
      ("Round slate coaster blank 4 in", "Blank (each)", None, None, 12, 29.99, 20, 8, ""),
      ("20 oz stainless steel tumbler blank", "Blank (each)", None, None, 25, 124.99, 11, 10, "Powder-coated, for rotary"),
      ("Bamboo cutting board 11 x 8 in", "Blank (each)", None, None, 10, 69.99, 6, 4, ""),
      ("Keyring + jump ring", "Hardware / extra", None, None, 100, 9.99, 70, 25, ""),
      ("Ornament ribbon (cut lengths)", "Hardware / extra", None, None, 100, 7.99, 80, 25, ""),
      ("Wood finish / sealant (uses)", "Finish", None, None, 250, 15.99, None, None, "About 250 small pieces a can"),
      ("Transfer / masking tape (uses)", "Finish", None, None, 300, 22.99, None, None, "Stops smoke marks on wood"),
      ("Kraft gift box", "Packaging", None, None, 50, 32.99, 40, 15, ""),
      ("Poly mailer + tissue + card", "Packaging", None, None, 50, 18.99, 35, 15, "")]
for i, row in enumerate(ex):
    for j, v in enumerate(row):
        if v is not None: su.cell(6 + i, [1, 2, 3, 4, 5, 6, 9, 10, 12][j]).value = v
dv_list(su, f"B6:B{NS}", TYPES)
su.conditional_formatting.add(f"K6:K{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=PatternFill("solid", fgColor="F8D7D3"), font=Font(name=F, bold=True, color="A12A1E")))
SNAME, SEACH, SSQ = (f"Materials!${c}$6:${c}${NS}" for c in "AGH")
SLIST = f"=Materials!$A$6:$A${NS}"

def look(ref, rng=SEACH):
    return f'IF({ref}="",0,IFERROR(INDEX({rng},MATCH({ref},{SNAME},0))*1,0))'

# ---------- Product Pricing ----------
pp = wb.create_sheet("Product Pricing")
banner(pp, t, "Product costing & pricing", "One row per product. Material from the part size, machine time from your minutes, then cost, prices and profit.", 23)
cols = ["Product", "Material / blank", "Part width (in)", "Part height (in)", "Pieces per item", "Extra 1", "Extra 2", "Packaging",
        "Engrave (min)", "Cut (min)", "Hands-on (min)",
        "Material cost", "Extras & packaging", "Machine time", "Labour", "Overheads",
        "COST PER ITEM", "Wholesale price", "Retail price", "Etsy fees (est.)", "Profit per retail sale", "Margin", "Profit per machine hour"]
header(pp, 5, cols, t); pp.row_dimensions[5].height = 46
for i, w in enumerate([30, 32, 9, 9, 8, 24, 24, 24, 9, 8, 9, 10, 11, 10, 9, 10, 12, 11, 11, 10, 12, 8, 12]): pp.column_dimensions[gl(i + 1)].width = w
pp.freeze_panes = "B6"
label(pp, "A4", "Sheet materials: material cost = width x height x pieces x cost per sq in + waste. Blanks (no size on Materials): cost each x pieces + waste.",
      italic=True, size=9, color=GREY)
for r in range(6, NP + 1):
    for col in "ABCDEFGHIJK": inp(pp, f"{col}{r}")
    for col in "ABFGH": pp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    for col in "CD": pp[f"{col}{r}"].number_format = "0.##"
    on = f'A{r}=""'
    sq = look(f"B{r}", SSQ)
    calc(pp, f"L{r}", f'=IF({on},"",IF(E{r}="",1,E{r})*IF(AND(N(C{r})>0,N(D{r})>0,{sq}>0),C{r}*D{r}*{sq},{look(f"B{r}")})*(1+{WASTE}))', USD)
    calc(pp, f"M{r}", f'=IF({on},"",IF(E{r}="",1,E{r})*({look(f"F{r}")}+{look(f"G{r}")})+{look(f"H{r}")})', USD)
    calc(pp, f"N{r}", f'=IF({on},"",(N(I{r})+N(J{r}))/60*{MCH})', USD)
    calc(pp, f"O{r}", f'=IF({on},"",N(K{r})/60*{RATE})', USD)
    calc(pp, f"P{r}", f'=IF({on},"",(L{r}+M{r})*{OVH})', USD)
    calc(pp, f"Q{r}", f'=IF({on},"",L{r}+M{r}+N{r}+O{r}+P{r})', USD, bold=True)
    calc(pp, f"R{r}", f'=IF({on},"",CEILING(Q{r}*{WMUL},{RND}))', USD, bold=True)
    calc(pp, f"S{r}", f'=IF({on},"",CEILING(R{r}*{RMUL},{RND}))', USD, bold=True)
    calc(pp, f"T{r}", f'=IF({on},"",S{r}*({ETX}+{PPC})+{PFX}+{LST})', USD)
    calc(pp, f"U{r}", f'=IF({on},"",S{r}-Q{r}-T{r})', USD, bold=True)
    calc(pp, f"V{r}", f'=IF(OR({on},N(S{r})=0),"",U{r}/S{r})', "0%")
    calc(pp, f"W{r}", f'=IF(OR({on},N(I{r})+N(J{r})=0),"",U{r}/((N(I{r})+N(J{r}))/60))', USD, bold=True)
prods = [("Personalised wood keychain", "3 mm (1/8 in) Baltic birch plywood", 2.5, 1.5, 1, "Keyring + jump ring", "Wood finish / sealant (uses)", "Poly mailer + tissue + card", 1.5, 0.5, 4),
         ("Engraved slate coaster set of 4", "Round slate coaster blank 4 in", None, None, 4, None, None, "Kraft gift box", 12, None, 10),
         ("Custom acrylic name sign 10 in", "3 mm clear cast acrylic", 10, 3.5, 1, "Transfer / masking tape (uses)", None, "Poly mailer + tissue + card", 3, 2.5, 8),
         ("Engraved bamboo cutting board", "Bamboo cutting board 11 x 8 in", None, None, 1, None, None, "Kraft gift box", 14, None, 8),
         ("Laser-cut wood ornament", "3 mm (1/8 in) Baltic birch plywood", 3.5, 3.5, 1, "Ornament ribbon (cut lengths)", "Wood finish / sealant (uses)", "Poly mailer + tissue + card", 2, 1, 3),
         ("Engraved 20 oz tumbler (rotary)", "20 oz stainless steel tumbler blank", None, None, 1, None, None, "Kraft gift box", 9, None, 6),
         ("Leatherette hat patch", "Leatherette sheet (black/gold)", 3, 2, 1, None, None, None, 1, 0.5, 2)]
for i, row in enumerate(prods):
    for j, v in enumerate(row):
        if v is not None: pp.cell(6 + i, 1 + j).value = v
for rng in (f"B6:B{NP}", f"F6:H{NP}"): dv_list(pp, rng, SLIST)
pp.conditional_formatting.add(f"U6:U{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
legend(pp, NP + 2, 1)
PNAME, PCOST, PWH, PRET = (f"'Product Pricing'!${c}$6:${c}${NP}" for c in "AQRS")

# ---------- Bulk Quote ----------
bq = wb.create_sheet("Bulk Quote")
banner(bq, t, "Bulk order quote", "Wedding favours, company gifts, school orders: price any quantity in seconds.", 7)
widths(bq, {"A": 28, "B": 26, "C": 2, "D": 28, "E": 14, "F": 16, "G": 16})
qi = [("Customer", "Harbor Realty (closing gifts)", None), ("Product", "Engraved bamboo cutting board", None), ("Quantity", 30, "0"),
      ("Set-up / design fee (one-off)", 25, USD), ("Rush fee (one-off)", 0, USD), ("Shipping charged", 22, USD)]
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
STAT = "New,Proof sent,Approved,Engraving,Finishing,Shipped,Cancelled"
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
ords = [("L-101", "Megan T.", "Custom acrylic name sign 10 in", "'Olivia' script, white paint fill", 1, None, "Finishing", "full", -3, 1, "Nursery sign"),
        ("L-102", "Harbor Realty", "Engraved bamboo cutting board", "Logo + 'Welcome home, [family]' x 30", 30, "q", "Proof sent", 400, -2, 2, "Names list by email"),
        ("L-103", "Rivera wedding", "Laser-cut wood ornament", "Names + date, 80 favours", 80, 6, "Approved", 240, -6, 12, "Pick-up"),
        ("L-104", "Etsy order", "Engraved slate coaster set of 4", "Family initial + est. 2019", 1, None, "New", None, 0, 4, "")]
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
for i, (back, ch, pr, q, price, fees, note) in enumerate([(15, "Etsy", "Engraved slate coaster set of 4", 1, "r7", "etsy", ""),
                                                         (11, "Bulk order", "Personalised wood keychain", 40, 6, 0, "Gym team"),
                                                         (7, "Facebook", "Engraved 20 oz tumbler (rotary)", 2, "r11", 0, "Local pickup"),
                                                         (4, "Market", "Laser-cut wood ornament", 14, 12, 0, "Holiday market"),
                                                         (1, "Etsy", "Custom acrylic name sign 10 in", 1, "r8", "etsy", "")]):
    r = 6 + i; sa[f"A{r}"] = f"=TODAY()-{back}"; sa[f"B{r}"] = ch; sa[f"C{r}"] = pr; sa[f"D{r}"] = q; sa[f"K{r}"] = note
    sa[f"E{r}"] = price if isinstance(price, (int, float)) else f"='Product Pricing'!S{price[1:]}"
    sa[f"G{r}"] = fees if fees != "etsy" else f"=ROUND(F{r}*({ETX}+{PPC})+{PFX}+{LST},2)"
SD, SCH, SC, SQ, ST, SG, SH, SPF = (f"Sales!${c}$6:${c}${NSALE}" for c in "ABCDFGHI")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Sales, Orders and Materials.", 9)
widths(d, {"A": 28, "B": 15, "C": 14, "D": 14, "E": 14, "F": 4, "G": 30, "H": 12, "I": 14})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{SD},">="&DATE($B$4,1,1),{SD},"<"&DATE($B$4+1,1,1)'
OPEN = f'"<>Shipped",Orders!$G$6:$G${NO},"<>Cancelled"'
kpi = [("Sales", f"=SUMIFS({ST},{yr})", USD), ("Profit", f"=SUMIFS({SPF},{yr})", USD), ("Items sold", f"=SUMIFS({SQ},{yr})", "#,##0"),
       ("Profit margin", '=IF(B6=0,"",B7/B6)', "0%"),
       ("Open orders", f'=COUNTIFS(Orders!$C$6:$C${NO},"<>",Orders!$G$6:$G${NO},{OPEN})', "0"),
       ("Items to make", f'=SUMIFS(Orders!$E$6:$E${NO},Orders!$G$6:$G${NO},"<>Finishing",Orders!$G$6:$G${NO},{OPEN})', "#,##0"),
       ("Balance still to collect", f'=SUMIFS(Orders!$M$6:$M${NO},Orders!$G$6:$G${NO},{OPEN})', USD),
       ("Orders late / need attention", f'=COUNTIF(Orders!$O$6:$O${NO},"LATE")+COUNTIF(Orders!$O$6:$O${NO},"Chase proof")', "0"),
       ("Materials to reorder", f'=COUNTIF(Materials!$K$6:$K${NS},"Reorder")', "0")]
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
