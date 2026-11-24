"""Resin Art Business Spreadsheet (batch 7, lane a): resin calculator (how much resin for any shape, Part A / Part B, layers),
supplies & stock with mould cost per use, product costing & pricing (resin from dimensions, pigments, inclusions, mould wear,
hardware, packaging, labour, fees), custom order tracker (deposits, cure/demould dates, deadlines), sales log and dashboard.
Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule

t = Theme("2B3F6B", "9A5BB5", "EEEAF6")
wb = Workbook()
NS, NP, NO, NSALE = 105, 45, 205, 506
USD, USD4 = '"$"#,##0.00', '"$"#,##0.0000'
GREY = "6F6A7F"
SHAPES = "Rectangle / square,Circle / round,Triangle"

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Resin Art Business Spreadsheet", "Know how much resin every piece needs, what it costs, what to charge, and when each order is ready.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly rate, overheads, wholesale and retail mark-ups, Etsy fee estimate, overpour allowance and usual cure time.",
         "Supplies: add each resin kit, pigment, mica, inclusion, mould, hardware and packaging item once. Moulds: type how many pours you expect from them.",
         "Resin Calculator: pick a shape, type the size in inches or cm, how many pieces and your mix ratio. You get total resin, Part A, Part B and the cost.",
         "Product Pricing: one row per product. Type its size (or the resin amount if you know it), pick pigments, mould, hardware and packaging. Cost, wholesale and retail appear.",
         "Orders: track custom orders from quote to delivered: deposits, balance due, pour date, demould date and deadline.",
         "Sales and Dashboard: log every sale; profit, best sellers, open orders and money still to collect update for you."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Resin amounts are by volume (fluid ounces and ml), the way most epoxy kits are mixed. If your resin mixes by weight, follow the maker's "
      "instructions: the volume here is still a good guide to how much to buy. Always follow your resin's safety guidance (gloves, ventilation, respirator).",
      size=10, color="7A2E5C")
s.row_dimensions[14].height = 46
label(s, "B15", "Example supplies, products, orders and sales are included so you can see how it works: type over them or delete them. "
      "Prices in the examples are illustrations only.", italic=True, size=10)
s.row_dimensions[15].height = 30
label(s, "B16", "Works in Excel and Google Sheets.", italic=True, size=10)

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates. Every product uses these.", 4)
widths(st, {"A": 44, "B": 16, "C": 4, "D": 66})
rows = [("Your hourly rate", 20, USD, "Mixing, pouring, demoulding, sanding, finishing and packing time."),
        ("Overheads (% of materials)", 0.10, "0%", "Gloves, cups, sticks, heat gun, sandpaper, respirator filters, electricity."),
        ("Wholesale price = cost x", 2, '0.0"x"', "Common rule: wholesale is about 2x your total cost."),
        ("Retail price = wholesale x", 2, '0.0"x"', "Common rule: retail is about 2x wholesale."),
        ("Round prices up to the nearest", 1, USD, "Use 0.5 or 1 for clean prices."),
        ("Etsy transaction fee", 0.065, "0.0%", "Estimate. Check Etsy's current fees for your country."),
        ("Payment processing (%)", 0.03, "0.0%", "Estimate, varies by country."),
        ("Payment processing (fixed per order)", 0.25, USD, None),
        ("Listing fee per sale", 0.20, USD, None),
        ("Overpour / waste allowance", 0.10, "0%", "Extra resin for what stays in the cup and on the sticks."),
        ("Usual cure time before demoulding (hours)", 48, "0", "Used when an order has no cure time typed."),
        ("Deposit for custom orders", 0.5, "0%", "Suggested deposit shown on the Orders tab.")]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"D{5 + i}", n, size=9, color=GREY, italic=True)
RATE, OVH, WMUL, RMUL, RND, ETX, PPC, PFX, LST, WASTE, CURE, DEP = (f"Settings!$B${5 + i}" for i in range(12))
label(st, "A19", "Unit list (for drop-downs)", bold=True, size=9, color=GREY)
UNITS = [("fl oz", 1), ("ml", 0.033814), ("L", 33.814), ("gal", 128), ("oz", 1), ("g", 0.035274), ("kg", 35.274), ("lb", 16), ("each", 1)]
for i, (u, f) in enumerate(UNITS):
    st[f"A{20 + i}"] = u; st[f"B{20 + i}"] = f
    st[f"A{20 + i}"].font = Font(name=F, size=9, color=GREY); st[f"B{20 + i}"].font = Font(name=F, size=9, color=GREY)
UL = "Settings!$A$20:$B$28"
TYPES = "Resin kit,Pigment,Mica powder,Alcohol ink,Glitter,Inclusions,Dried flowers,Mould,Hardware,Packaging,Other"

# ---------- Supplies ----------
su = wb.create_sheet("Supplies")
banner(su, t, "Supplies & stock", "Add each supply once. Cost per unit, cost per fl oz of resin and mould cost per pour are worked out for you.", 13)
header(su, 5, ["Supply", "Type", "Pack size", "Unit", "Pack price", "Cost per unit", "Resin cost per fl oz", "Mould: expected pours",
               "Cost per pour", "On hand (packs)", "Reorder at", "Stock status", "Supplier / notes", "factor"], t)
su.row_dimensions[5].height = 44
widths(su, {"A": 32, "B": 13, "C": 10, "D": 8, "E": 11, "F": 12, "G": 13, "H": 12, "I": 11, "J": 12, "K": 10, "L": 13, "M": 26, "N": 7}); su.freeze_panes = "B6"
for r in range(6, NS + 1):
    for col in "ABCDEHJKM": inp(su, f"{col}{r}")
    for col in "AM": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    su[f"E{r}"].number_format = USD
    for col in "CHJK": su[f"{col}{r}"].number_format = "#,##0.##"
    su[f"N{r}"] = f'=IF(D{r}="","",IFERROR(VLOOKUP(D{r},{UL},2,FALSE),1))'
    su[f"N{r}"].font = Font(name=F, size=8, color="A9A3B8"); su[f"N{r}"].number_format = "0.####"
    calc(su, f"F{r}", f'=IF(OR(A{r}="",N(C{r})=0,E{r}=""),"",E{r}/C{r})', USD4)
    calc(su, f"G{r}", f'=IF(OR(F{r}="",D{r}="each",D{r}=""),"",E{r}/(C{r}*N{r}))', USD4)
    calc(su, f"I{r}", f'=IF(OR(F{r}="",N(H{r})=0),"",E{r}/H{r})', USD)
    calc(su, f"L{r}", f'=IF(OR(A{r}="",J{r}=""),"",IF(J{r}<=N(K{r}),"Reorder","OK"))')
ex = [("Clear art resin 1 gal kit (A+B)", "Resin kit", 1, "gal", 89.99, None, 1, 1, "1:1 by volume"),
      ("Deep pour resin 1.5 gal kit", "Resin kit", 1.5, "gal", 139.99, None, 1, 0, "Pour up to 2 in deep"),
      ("UV resin 200 g", "Resin kit", 200, "g", 14.99, None, 2, 1, "Small charms, no mixing"),
      ("Mica powder set (24 colours)", "Mica powder", 240, "g", 15.99, None, 1, 0, "About 10 g a colour"),
      ("Alcohol inks (12 x 10 ml)", "Alcohol ink", 120, "ml", 19.99, None, 1, 0, ""),
      ("Gold leaf flakes", "Inclusions", 10, "g", 7.99, None, 2, 1, ""),
      ("Dried pressed flowers mix", "Dried flowers", 120, "each", 12.99, None, 1, 0, ""),
      ("Silicone coaster mould 4 in round", "Mould", 1, "each", 6.99, 60, 4, 0, ""),
      ("Silicone tray mould 12 x 8 in", "Mould", 1, "each", 18.99, 40, 1, 0, ""),
      ("Keychain mould set (12 shapes)", "Mould", 1, "each", 11.99, 50, 1, 0, ""),
      ("Keyring + jump ring", "Hardware", 100, "each", 9.99, None, 1, 0, ""),
      ("Cork backing pads 4 in", "Hardware", 50, "each", 8.99, None, 1, 0, ""),
      ("Tray handles (pair)", "Hardware", 10, "each", 21.99, None, 1, 0, "Gold"),
      ("Kraft gift box (coaster set)", "Packaging", 20, "each", 15.99, None, 1, 1, ""),
      ("Organza bag + thank-you card", "Packaging", 100, "each", 12.99, None, 1, 0, "")]
for i, row in enumerate(ex):
    for j, v in enumerate(row):
        if v is not None: su.cell(6 + i, [1, 2, 3, 4, 5, 8, 10, 11, 13][j]).value = v
dv_list(su, f"B6:B{NS}", TYPES); dv_list(su, f"D6:D{NS}", "=Settings!$A$20:$A$28")
su.conditional_formatting.add(f"L6:L{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=PatternFill("solid", fgColor="F8D7D3"), font=Font(name=F, bold=True, color="A12A1E")))
SNAME, SUNIT, SFLOZ, SPOUR = (f"Supplies!${c}$6:${c}${NS}" for c in "AFGI")
SLIST = f"=Supplies!$A$6:$A${NS}"

def look(rng, ref, default=0):
    return f'IF({ref}="",{default},IFERROR(INDEX({rng},MATCH({ref},{SNAME},0)),{default}))'

def vol_cuin(shape, l, w, d, unit):
    """cubic inches from shape + dims (in or cm)."""
    base = f'IF({shape}="Circle / round",PI()*({w}/2)^2*{d},IF({shape}="Triangle",{l}*{w}/2*{d},{l}*{w}*{d}))'
    return f'({base}/IF({unit}="cm",2.54^3,1))'

# ---------- Resin Calculator ----------
rc = wb.create_sheet("Resin Calculator")
banner(rc, t, "Resin calculator", "How much resin do I need? Pick a shape, type the size and get Part A, Part B and the cost.", 6)
widths(rc, {"A": 34, "B": 20, "C": 4, "D": 40, "E": 18, "F": 18})
inputs = [("Shape", "Rectangle / square", None), ("Length", 12, "#,##0.00"), ("Width (or diameter for round)", 8, "#,##0.00"),
          ("Depth / thickness", 0.25, "#,##0.00"), ("Units", "in", None), ("Number of pieces", 1, "0"),
          ("Mix ratio: Part A", 1, "0.##"), ("Mix ratio: Part B", 1, "0.##"), ("Max pour depth per layer", 0.25, "#,##0.00"),
          ("Resin kit (for cost)", "Clear art resin 1 gal kit (A+B)", None)]
label(rc, "A4", "Your piece", bold=True, size=13)
for i, (a, v, fmt) in enumerate(inputs):
    r = 5 + i; label(rc, f"A{r}", a); c = inp(rc, f"B{r}", v, fmt)
    if i in (0, 9): c.alignment = Alignment(horizontal="left", indent=1)
dv_list(rc, "B5", SHAPES); dv_list(rc, "B9", "in,cm"); dv_list(rc, "B14", SLIST)
label(rc, "A15", "Max pour depth: check your resin's label (coating / art resin is often 1/8 to 1/4 in, deep pour 1-2 in).", italic=True, size=9, color=GREY)
rc.merge_cells("A15:B16"); rc.row_dimensions[15].height = 18
label(rc, "D4", "You need", bold=True, size=13)
vol = vol_cuin("B5", "B6", "B7", "B8", "B9")
res = [("Volume per piece (cubic in)", f"=IFERROR({vol},0)", "#,##0.00", False),
       ("Volume per piece (ml)", "=E5*16.3871", "#,##0", False),
       ("Resin per piece (fl oz)", "=E5/1.80469", "#,##0.00", False),
       ("TOTAL MIXED RESIN (fl oz)", f"=E7*B10*(1+{WASTE})", "#,##0.00", True),
       ("Total mixed resin (ml)", "=E8*29.5735", "#,##0", True),
       ("Part A (fl oz)", "=IFERROR(E8*B11/(B11+B12),\"\")", "#,##0.00", True),
       ("Part B (fl oz)", "=IFERROR(E8*B12/(B11+B12),\"\")", "#,##0.00", True),
       ("Part A (ml)", "=IFERROR(E10*29.5735,\"\")", "#,##0", False),
       ("Part B (ml)", "=IFERROR(E11*29.5735,\"\")", "#,##0", False),
       ("Layers to pour", '=IF(N(B13)=0,1,CEILING(B8/B13,1))', "0", True),
       ("Resin per layer (fl oz)", "=IFERROR(E8/E14,\"\")", "#,##0.00", False),
       ("Resin cost", f'=IFERROR(E8*{look(SFLOZ, "B14")},"")', USD, True)]
for i, (a, f, fmt, b) in enumerate(res):
    r = 5 + i; label(rc, f"D{r}", a, bold=b); calc(rc, f"E{r}", f, fmt, bold=b)
rc["E8"].font = Font(name=F, size=16, bold=True, color="1F2A44"); rc.row_dimensions[8].height = 28
label(rc, "D18", "Totals include the overpour / waste allowance from Settings. Round: width = diameter. Triangle: length x width / 2.", italic=True, size=9, color=GREY)
rc.merge_cells("D18:F19")
label(rc, "A21", "Quick reference: common pieces (1/4 in deep, no waste)", bold=True, size=12)
header(rc, 22, ["Piece", "Size", "", "Resin per piece (fl oz)", "Resin per piece (ml)"], t)
refs = [("Round coaster", "4 in round", "Circle / round", 4, 4, 0.25), ("Square coaster", "4 x 4 in", "Rectangle / square", 4, 4, 0.25),
        ("Small tray", "12 x 8 in", "Rectangle / square", 12, 8, 0.25), ("Serving board coat", "16 x 10 in, 1/8 in", "Rectangle / square", 16, 10, 0.125),
        ("Round wall art coat", "12 in round, 1/8 in", "Circle / round", 12, 12, 0.125), ("Keychain", "2 x 1.5 in, 1/4 in", "Rectangle / square", 2, 1.5, 0.25)]
for i, (n, sz, sh, l, w, d) in enumerate(refs):
    r = 23 + i; label(rc, f"A{r}", n); label(rc, f"B{r}", sz, size=10, color=GREY)
    v = vol_cuin(f'"{sh}"', l, w, d, '"in"')
    calc(rc, f"D{r}", f"={v}/1.80469", "#,##0.00"); calc(rc, f"E{r}", f"={v}*16.3871", "#,##0")

# ---------- Product Pricing ----------
pp = wb.create_sheet("Product Pricing")
banner(pp, t, "Product costing & pricing", "One row per product. Type the size or the resin amount, pick your supplies. Price appears on the right.", 30)
cols = ["Product", "Resin kit", "Shape", "Length", "Width / diam.", "Depth", "in / cm", "Resin fl oz (if known)",
        "Pigment / mica", "Qty used", "Inclusions / extra", "Qty used", "Mould", "Hardware", "Hardware qty", "Packaging", "Labour (min)",
        "Resin per piece (fl oz)", "Resin cost", "Colour & extras", "Mould wear", "Hardware & packaging", "Labour", "Overheads",
        "COST PER PIECE", "Wholesale price", "Retail price", "Etsy fees (est.)", "Profit per retail sale", "Margin"]
header(pp, 5, cols, t); pp.row_dimensions[5].height = 46
W = [30, 26, 15, 8, 9, 7, 7, 10, 24, 7, 22, 7, 26, 20, 8, 24, 8, 10, 10, 10, 9, 11, 9, 9, 12, 11, 11, 10, 12, 8]
from openpyxl.utils import get_column_letter as gl
for i, w in enumerate(W): pp.column_dimensions[gl(i + 1)].width = w
pp.freeze_panes = "B6"
label(pp, "A4", "Qty used = in the unit you bought it in (g of mica, ml of ink, pieces of flowers). Leave size blank and type 'Resin fl oz' if you already know it.",
      italic=True, size=9, color=GREY)
for r in range(6, NP + 1):
    for col in "ABCDEFGHIJKLMNOPQ": inp(pp, f"{col}{r}")
    for col in "ABIKMNP": pp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    on = f'A{r}=""'
    v = vol_cuin(f"C{r}", f"D{r}", f"E{r}", f"F{r}", f"G{r}")
    calc(pp, f"R{r}", f'=IF({on},"",IF(N(H{r})>0,H{r},IF(OR(D{r}="",F{r}=""),0,IFERROR({v}/1.80469,0)))*(1+{WASTE}))', "#,##0.00")
    calc(pp, f"S{r}", f'=IF({on},"",R{r}*{look(SFLOZ, f"B{r}")})', USD)
    calc(pp, f"T{r}", f'=IF({on},"",N(J{r})*{look(SUNIT, f"I{r}")}+N(L{r})*{look(SUNIT, f"K{r}")})', USD)
    calc(pp, f"U{r}", f'=IF({on},"",{look(SPOUR, f"M{r}")})', USD)
    calc(pp, f"V{r}", f'=IF({on},"",IF(N{r}="",0,IF(O{r}="",1,O{r}))*{look(SUNIT, f"N{r}")}+{look(SUNIT, f"P{r}")})', USD)
    calc(pp, f"W{r}", f'=IF({on},"",N(Q{r})/60*{RATE})', USD)
    calc(pp, f"X{r}", f'=IF({on},"",(S{r}+T{r}+U{r}+V{r})*{OVH})', USD)
    calc(pp, f"Y{r}", f'=IF({on},"",S{r}+T{r}+U{r}+V{r}+W{r}+X{r})', USD, bold=True)
    calc(pp, f"Z{r}", f'=IF({on},"",CEILING(Y{r}*{WMUL},{RND}))', USD, bold=True)
    calc(pp, f"AA{r}", f'=IF({on},"",CEILING(Z{r}*{RMUL},{RND}))', USD, bold=True)
    calc(pp, f"AB{r}", f'=IF({on},"",AA{r}*({ETX}+{PPC})+{PFX}+{LST})', USD)
    calc(pp, f"AC{r}", f'=IF({on},"",AA{r}-Y{r}-AB{r})', USD, bold=True)
    calc(pp, f"AD{r}", f'=IF(OR({on},N(AA{r})=0),"",AC{r}/AA{r})', "0%")
prods = [("Ocean wave coaster set (4)", "Clear art resin 1 gal kit (A+B)", None, None, None, None, None, 7, "Mica powder set (24 colours)", 4, "Alcohol inks (12 x 10 ml)", 2, "Silicone coaster mould 4 in round", "Cork backing pads 4 in", 4, "Kraft gift box (coaster set)", 30),
         ("Pressed flower tray", "Clear art resin 1 gal kit (A+B)", "Rectangle / square", 12, 8, 0.25, "in", None, None, None, "Dried pressed flowers mix", 18, "Silicone tray mould 12 x 8 in", "Tray handles (pair)", 1, None, 45),
         ("Gold leaf keychain", "UV resin 200 g", None, None, None, None, None, 0.25, "Mica powder set (24 colours)", 0.3, "Gold leaf flakes", 0.1, "Keychain mould set (12 shapes)", "Keyring + jump ring", 1, "Organza bag + thank-you card", 6),
         ("Geode wall art 12 in round", "Clear art resin 1 gal kit (A+B)", "Circle / round", 12, 12, 0.125, "in", None, "Mica powder set (24 colours)", 6, "Gold leaf flakes", 0.5, None, None, None, None, 75),
         ("River table top 24 x 12 in", "Deep pour resin 1.5 gal kit", "Rectangle / square", 24, 4, 1.5, "in", None, "Mica powder set (24 colours)", 8, None, None, None, None, None, None, 240)]
for i, row in enumerate(prods):
    for j, v in enumerate(row):
        if v is not None: pp.cell(6 + i, 1 + j).value = v
for rng in (f"B6:B{NP}", f"I6:I{NP}", f"K6:K{NP}", f"M6:N{NP}", f"P6:P{NP}"): dv_list(pp, rng, SLIST)
dv_list(pp, f"C6:C{NP}", SHAPES); dv_list(pp, f"G6:G{NP}", "in,cm")
pp.conditional_formatting.add(f"AC6:AC{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
legend(pp, NP + 2, 1)
PNAME, PCOST, PRET, PWH = (f"'Product Pricing'!${c}$6:${c}${NP}" for c in ("A", "Y", "AA", "Z"))

# ---------- Orders ----------
od = wb.create_sheet("Orders")
banner(od, t, "Custom order tracker", "From quote to delivered: deposits, balance, pour and demould dates, deadlines.", 17)
cols = ["Order #", "Customer", "Product", "Qty", "Price each (blank = retail)", "Status", "Deposit paid", "Pour date", "Cure (hours)", "Due date", "Notes",
        "Order total", "Suggested deposit", "Balance due", "Demould date", "Days to due", "Flag"]
header(od, 5, cols, t); od.row_dimensions[5].height = 44
widths(od, {"A": 9, "B": 20, "C": 30, "D": 6, "E": 12, "F": 12, "G": 11, "H": 12, "I": 9, "J": 12, "K": 26, "L": 12, "M": 12, "N": 12, "O": 15, "P": 9, "Q": 15})
od.freeze_panes = "C6"
STAT = "Quote,Confirmed,Poured,Curing,Finishing,Ready,Delivered,Cancelled"
for r in range(6, NO + 1):
    for col in "ABCDEFGHIJK": inp(od, f"{col}{r}")
    for col in "BCK": od[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    for col in "HJ": od[f"{col}{r}"].number_format = "dd mmm yyyy"
    for col in "EG": od[f"{col}{r}"].number_format = USD
    on = f'C{r}=""'
    calc(od, f"L{r}", f'=IF({on},"",N(D{r})*IF(E{r}="",IFERROR(INDEX({PRET},MATCH(C{r},{PNAME},0)),0),E{r}))', USD)
    calc(od, f"M{r}", f'=IF({on},"",ROUND(L{r}*{DEP},2))', USD)
    calc(od, f"N{r}", f'=IF(OR({on},F{r}="Cancelled"),"",L{r}-N(G{r}))', USD, bold=True)
    calc(od, f"O{r}", f'=IF(H{r}="","",H{r}+IF(I{r}="",{CURE},I{r})/24)', "ddd dd mmm")
    calc(od, f"P{r}", f'=IF(OR(J{r}="",F{r}="Delivered",F{r}="Cancelled"),"",J{r}-TODAY())', "0")
    calc(od, f"Q{r}", f'=IF(P{r}="","",IF(P{r}<0,"LATE",IF(AND(O{r}<>"",O{r}>J{r}),"Cure after due!",IF(P{r}<=3,"Due soon","On track"))))')
dv_list(od, f"F6:F{NO}", STAT); dv_list(od, f"C6:C{NO}", "=" + PNAME)
ords = [("R-101", "Hannah P.", "Ocean wave coaster set (4)", 2, None, "Curing", 40, -1, None, 6, "Wedding gift, teal + gold"),
        ("R-102", "Cafe Lumen", "Pressed flower tray", 6, "w", "Confirmed", 100, None, None, 14, "Wholesale, invoice net 14"),
        ("R-103", "Marcus T.", "Geode wall art 12 in round", 1, None, "Quote", None, None, None, 20, "Purple + silver"),
        ("R-104", "Ella J.", "Gold leaf keychain", 10, 9, "Ready", 45, -4, 24, 1, "Bridesmaid initials")]
for i, (n, cu, pr, q, pe, sta, dep, pour, cure, due, note) in enumerate(ords):
    r = 6 + i; od[f"A{r}"] = n; od[f"B{r}"] = cu; od[f"C{r}"] = pr; od[f"D{r}"] = q; od[f"F{r}"] = sta; od[f"K{r}"] = note
    if pe == "w": od[f"E{r}"] = "='Product Pricing'!Z7"
    elif pe is not None: od[f"E{r}"] = pe
    if dep is not None: od[f"G{r}"] = dep
    if pour is not None: od[f"H{r}"] = f"=TODAY(){pour:+d}"
    if cure is not None: od[f"I{r}"] = cure
    od[f"J{r}"] = f"=TODAY()+{due}"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")
od.conditional_formatting.add(f"Q6:Q{NO}", CellIsRule(operator="equal", formula=['"LATE"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
od.conditional_formatting.add(f"Q6:Q{NO}", CellIsRule(operator="equal", formula=['"Cure after due!"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
od.conditional_formatting.add(f"Q6:Q{NO}", CellIsRule(operator="equal", formula=['"Due soon"'], fill=amb, font=Font(name=F, bold=True, color="8A5A12")))
od.conditional_formatting.add(f"Q6:Q{NO}", CellIsRule(operator="equal", formula=['"On track"'], fill=grn, font=Font(name=F, color="2E6B3A")))
od.conditional_formatting.add(f"F6:F{NO}", CellIsRule(operator="equal", formula=['"Ready"'], fill=grn, font=Font(name=F, bold=True, color="2E6B3A")))

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
CH = ["Etsy", "Craft fair", "Custom order", "Wholesale", "Instagram", "Other"]
dv_list(sa, f"B6:B{NSALE}", ",".join(CH)); dv_list(sa, f"C6:C{NSALE}", "=" + PNAME)
for i, (back, ch, pr, q, price, fees, note) in enumerate([(12, "Etsy", "Ocean wave coaster set (4)", 1, "r6", "etsy", ""),
                                                         (8, "Craft fair", "Gold leaf keychain", 6, 10, 0, "Holiday market"),
                                                         (5, "Custom order", "Geode wall art 12 in round", 1, "r9", 0, "Commission"),
                                                         (2, "Etsy", "Pressed flower tray", 1, "r7", "etsy", "")]):
    r = 6 + i; sa[f"A{r}"] = f"=TODAY()-{back}"; sa[f"B{r}"] = ch; sa[f"C{r}"] = pr; sa[f"D{r}"] = q; sa[f"K{r}"] = note
    sa[f"E{r}"] = price if isinstance(price, (int, float)) else f"='Product Pricing'!AA{price[1:]}"
    sa[f"G{r}"] = fees if fees != "etsy" else f"=ROUND(F{r}*({ETX}+{PPC})+{PFX}+{LST},2)"
SD, SCH, SC, SQ, ST, SG, SH, SPF = (f"Sales!${c}$6:${c}${NSALE}" for c in "ABCDFGHI")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Sales, Orders and Supplies.", 9)
widths(d, {"A": 28, "B": 15, "C": 14, "D": 14, "E": 14, "F": 4, "G": 30, "H": 12, "I": 14})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{SD},">="&DATE($B$4,1,1),{SD},"<"&DATE($B$4+1,1,1)'
OPEN = '"<>Delivered",Orders!$F$6:$F$' + str(NO) + ',"<>Cancelled"'
kpi = [("Sales", f"=SUMIFS({ST},{yr})", USD), ("Profit", f"=SUMIFS({SPF},{yr})", USD), ("Pieces sold", f"=SUMIFS({SQ},{yr})", "#,##0"),
       ("Profit margin", '=IF(B6=0,"",B7/B6)', "0%"),
       ("Open custom orders", f'=COUNTIFS(Orders!$C$6:$C${NO},"<>",Orders!$F$6:$F${NO},{OPEN})', "0"),
       ("Balance still to collect", f'=SUMIFS(Orders!$N$6:$N${NO},Orders!$F$6:$F${NO},{OPEN})', USD),
       ("Orders late or due in 3 days", f'=COUNTIF(Orders!$Q$6:$Q${NO},"LATE")+COUNTIF(Orders!$Q$6:$Q${NO},"Due soon")', "0"),
       ("Supplies to reorder", f'=COUNTIF(Supplies!$L$6:$L${NS},"Reorder")', "0")]
for i, (a, f, fmt) in enumerate(kpi):
    r = 6 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 28
header(d, 15, ["Month", "Sales", "Fees & shipping", "Cost", "Profit"], t)
for i, mn in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    r = 16 + i; label(d, f"A{r}", mn)
    mr = f'{SD},">="&DATE($B$4,{i + 1},1),{SD},"<"&DATE($B$4,{i + 2},1)'
    for col, rg in zip("BCDE", (ST, SG, SH, SPF)): calc(d, f"{col}{r}", f"=SUMIFS({rg},{mr})", USD)
label(d, "A28", "Total", bold=True)
for col in "BCDE": calc(d, f"{col}28", f"=SUM({col}16:{col}27)", USD, bold=True)
header(d, 15, ["Channel", "Sales", "Profit"], t, start=7)
for i, ch in enumerate(CH):
    r = 16 + i; label(d, f"G{r}", ch)
    calc(d, f"H{r}", f'=SUMIFS({ST},{SCH},G{r},{yr})', USD); calc(d, f"I{r}", f'=SUMIFS({SPF},{SCH},G{r},{yr})', USD)
header(d, 24, ["Product", "Pieces sold", "Profit"], t, start=7)
for i in range(12):
    r = 25 + i
    d[f"G{r}"] = f"=IF('Product Pricing'!A{6 + i}=\"\",\"\",'Product Pricing'!A{6 + i})"; d[f"G{r}"].font = Font(name=F, size=11)
    calc(d, f"H{r}", f'=IF(G{r}="","",SUMIFS({SQ},{SC},G{r},{yr}))', "#,##0")
    calc(d, f"I{r}", f'=IF(G{r}="","",SUMIFS({SPF},{SC},G{r},{yr}))', USD)
label(d, "G37", "Shows your first 12 products from Product Pricing.", italic=True, size=9, color=GREY)

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
