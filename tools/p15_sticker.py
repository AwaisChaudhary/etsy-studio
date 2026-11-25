"""Sticker Shop Business Spreadsheet (batch 8, lane a): sticker paper, laminate and packaging library with cost each, ink cost
per sheet by coverage, cutting-machine wear, product costing & pricing for sticker sheets, die-cut singles and packs (cost per
item and per sticker, wholesale, retail, Etsy fees, profit), print run planner with a supply check, finished-stock tracker
(made - sold - damaged), sales log by channel and dashboard. Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.utils import get_column_letter as gl

t = Theme("2F3E64", "E86A5C", "FBEEE9")
wb = Workbook()
NS, NP, NR, NSALE = 105, 65, 306, 1006
USD, USD4 = '"$"#,##0.00', '"$"#,##0.000'
GREY = "6A6F7D"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Sticker Shop Business Spreadsheet", "Cost every sticker sheet, die-cut and pack to the cent, plan print runs, and always know what's in stock.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly rate, ink cost per full-coverage sheet, cutting blade and mat wear, misprint allowance, mark-ups and fees.",
         "Supplies: add each sticker paper, laminate, backing card, sleeve, mailer and extra once with pack size and price. Cost each is worked out.",
         "Product Pricing: one row per product (sticker sheet, die-cut single, pack). Pick paper, laminate and packaging, type how many fit on a sheet and your minutes. Cost per item, cost per sticker, wholesale and retail prices appear.",
         "Print Run Planner: pick a product and how many to make. Sheets, laminate and sleeves needed (with a stock check), print and cut time and the cost of the run appear.",
         "Print Runs and Sales: log what you make and what you sell. The Stock tab shows what's on hand for every design and what to make more of.",
         "Dashboard: sales, profit, margin, best sellers, sales by channel (Etsy, markets, wholesale), stock value and supplies to reorder."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Ink cost: divide what a full set of cartridges or ink bottles costs by roughly how many full-coverage letter or A4 prints it gives you. "
      "Light, medium, heavy and full-bleed designs then use 25%, 50%, 75% and 100% of that.", size=10, color="8A3B2E")
s.row_dimensions[14].height = 44
label(s, "B15", "Only sell designs you made yourself or have a commercial licence for. Fan art of characters, logos and brands can get your shop closed.", size=10, color="8A3B2E")
s.row_dimensions[15].height = 30
label(s, "B16", "Example supplies, products, print runs and sales are included so you can see how it works: type over them or delete them. "
      "Prices in the examples are illustrations only. Works in Excel and Google Sheets.", italic=True, size=10)
s.row_dimensions[16].height = 30

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates. Every product and print run uses these.", 4)
widths(st, {"A": 44, "B": 16, "C": 4, "D": 66})
rows = [("Your hourly rate", 20, USD, "Printing, laminating, cutting, weeding, packing and listing time."),
        ("Overheads (% of materials)", 0.10, "0%", "Electricity, test prints, printer and laminator wear."),
        ("Ink set price (all colours)", 64.99, USD, "Cartridges or ink bottles for a full set."),
        ("Full-coverage sheets per ink set", 180, "#,##0", "Rough yield. Light designs use far less."),
        ("Cutting blade + mat wear per sheet", 0.06, USD, "A blade and mat spread over the sheets they cut."),
        ("Misprint / failed cut allowance", 0.08, "0%", "Banding, misaligned cuts, a jam. Added to sheet cost."),
        ("Wholesale price = cost x", 1.8, '0.0"x"', "What shops pay. Many stores expect about half your retail price."),
        ("Retail price = wholesale x", 1.8, '0.0"x"', "Etsy, website and market price."),
        ("Round prices up to the nearest", 0.25, USD, "Use 0.25 or 0.5 for clean prices like $4.50."),
        ("Etsy transaction fee", 0.065, "0.0%", "Estimate. Check Etsy's current fees for your country."),
        ("Payment processing (%)", 0.03, "0.0%", "Estimate, varies by country."),
        ("Payment processing (fixed per order)", 0.25, USD, None),
        ("Listing fee per sale", 0.20, USD, None)]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"D{5 + i}", n, size=9, color=GREY, italic=True)
RATE, OVH, INK, YIELD, WEAR, MIS, WMUL, RMUL, RND, ETX, PPC, PFX, LST = (f"Settings!$B${5 + i}" for i in range(13))
label(st, "A19", "Ink cost per full-coverage sheet", bold=True); calc(st, "B19", f"=IFERROR({INK}/{YIELD},0)", USD4)
INKS = "Settings!$B$19"
label(st, "A21", "Ink coverage", bold=True, size=12); label(st, "B21", "Share of a full print", bold=True, size=10)
for i, (c, v) in enumerate([("Light", 0.25), ("Medium", 0.5), ("Heavy", 0.75), ("Full bleed", 1)]):
    label(st, f"A{22 + i}", c); inp(st, f"B{22 + i}", v, "0%")
COV = "Settings!$A$22:$B$25"
TYPES = "Sticker paper,Laminate,Backing card,Sleeve / bag,Mailer,Extra,Pre-made (bought in),Other"
FORMATS = "Sticker sheet,Kiss-cut sheet,Die-cut single,Sticker pack,Mini sheet,Bookmark / other"

# ---------- Supplies ----------
su = wb.create_sheet("Supplies")
banner(su, t, "Supplies", "Add each supply once. Cost each (per sheet, per sleeve, per card) is worked out for you.", 10)
header(su, 5, ["Supply", "Type", "Pack size", "Pack price", "Cost each", "On hand (pieces)", "Reorder at", "Stock status", "Supplier / notes"], t)
su.row_dimensions[5].height = 44
widths(su, {"A": 36, "B": 18, "C": 10, "D": 11, "E": 11, "F": 12, "G": 10, "H": 13, "I": 30}); su.freeze_panes = "B6"
for r in range(6, NS + 1):
    for col in "ABCDFGI": inp(su, f"{col}{r}")
    for col in "AI": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    su[f"D{r}"].number_format = USD
    for col in "CFG": su[f"{col}{r}"].number_format = "#,##0"
    calc(su, f"E{r}", f'=IF(OR(A{r}="",N(C{r})=0,D{r}=""),"",D{r}/C{r})', USD4)
    calc(su, f"H{r}", f'=IF(OR(A{r}="",F{r}=""),"",IF(F{r}<=N(G{r}),"Reorder","OK"))')
ex = [("Matte vinyl sticker paper (letter)", "Sticker paper", 50, 24.99, 64, 30, "Waterproof, inkjet"),
      ("Glossy vinyl sticker paper (letter)", "Sticker paper", 50, 22.99, 38, 30, ""),
      ("Clear vinyl sticker paper (letter)", "Sticker paper", 25, 19.99, 12, 15, "For window / bottle decals"),
      ("Holographic laminate sheets (letter)", "Laminate", 50, 21.99, 41, 20, "Cold laminate, stars"),
      ("Matte laminate sheets (letter)", "Laminate", 50, 17.99, 55, 20, ""),
      ("Kraft backing card 4 x 6", "Backing card", 100, 12.99, 140, 40, "For packs and singles"),
      ("Cello sleeve 4 x 6 (self-seal)", "Sleeve / bag", 200, 9.99, 260, 60, ""),
      ("Cello sleeve 5 x 7 (self-seal)", "Sleeve / bag", 200, 11.99, 150, 60, "Fits letter half sheets"),
      ("Rigid mailer 6 x 9", "Mailer", 50, 21.99, 30, 20, "Stops bending in the post"),
      ("Thank-you card + freebie sticker", "Extra", 100, 14.99, 90, 30, ""),
      ("Die-cut stickers 3 in (printed for you)", "Pre-made (bought in)", 100, 59.00, 120, 50, "Bulk order from a print shop")]
for i, row in enumerate(ex):
    for j, v in enumerate(row):
        if v is not None: su.cell(6 + i, [1, 2, 3, 4, 6, 7, 9][j]).value = v
dv_list(su, f"B6:B{NS}", TYPES)
su.conditional_formatting.add(f"H6:H{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
SNAME, SEACH, SHAND = (f"Supplies!${c}$6:${c}${NS}" for c in "AEF")
SLIST = f"=Supplies!$A$6:$A${NS}"

def look(ref, rng=SEACH):
    return f'IF({ref}="",0,IFERROR(INDEX({rng},MATCH({ref},{SNAME},0)),0))'

# ---------- Product Pricing ----------
pp = wb.create_sheet("Product Pricing")
banner(pp, t, "Product costing & pricing", "One row per product. Paper, ink, laminate and cutting are shared across the items on a sheet.", 25)
cols = ["Product / design", "Format", "Sticker paper", "Items per sheet", "Ink coverage", "Laminate", "Backing card", "Sleeve / bag", "Extra",
        "Minutes per sheet", "Packing min per item", "Stickers in item",
        "Sheet cost (paper, ink, laminate, cut)", "Sheet share per item", "Packaging", "Labour", "Overheads",
        "COST PER ITEM", "Cost per sticker", "Wholesale price", "Retail price", "Etsy fees (est.)", "Profit per retail sale", "Margin"]
header(pp, 5, cols, t); pp.row_dimensions[5].height = 58
for i, w in enumerate([28, 15, 30, 8, 11, 28, 22, 24, 22, 9, 9, 9, 13, 11, 10, 9, 10, 12, 10, 11, 10, 10, 12, 8]): pp.column_dimensions[gl(i + 1)].width = w
pp.freeze_panes = "B6"
label(pp, "A4", "Items per sheet: 1 for a full sticker sheet, 2 for half sheets, 12 if 12 die-cut singles fit on one sheet. Bought-in stickers: pick them as the 'paper' and type 1.",
      italic=True, size=9, color=GREY)
for r in range(6, NP + 1):
    for col in "ABCDEFGHIJKL": inp(pp, f"{col}{r}")
    for col in "ACFGHI": pp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    on = f'A{r}=""'
    paper_bought = f'IFERROR(INDEX(Supplies!$B$6:$B${NS},MATCH(C{r},{SNAME},0))="Pre-made (bought in)",FALSE)'
    calc(pp, f"M{r}", f'=IF({on},"",{look(f"C{r}")}+IF({paper_bought},0,{INKS}*IFERROR(VLOOKUP(E{r},{COV},2,FALSE),0)+{look(f"F{r}")}+{WEAR}))', USD)
    calc(pp, f"N{r}", f'=IF({on},"",M{r}/IF(N(D{r})=0,1,D{r})*(1+{MIS}))', USD4)
    calc(pp, f"O{r}", f'=IF({on},"",{look(f"G{r}")}+{look(f"H{r}")}+{look(f"I{r}")})', USD)
    calc(pp, f"P{r}", f'=IF({on},"",(N(J{r})/IF(N(D{r})=0,1,D{r})+N(K{r}))/60*{RATE})', USD)
    calc(pp, f"Q{r}", f'=IF({on},"",(N{r}+O{r})*{OVH})', USD)
    calc(pp, f"R{r}", f'=IF({on},"",N{r}+O{r}+P{r}+Q{r})', USD, bold=True)
    calc(pp, f"S{r}", f'=IF(OR({on},N(L{r})=0),"",R{r}/L{r})', USD4)
    calc(pp, f"T{r}", f'=IF({on},"",CEILING(R{r}*{WMUL},{RND}))', USD, bold=True)
    calc(pp, f"U{r}", f'=IF({on},"",CEILING(T{r}*{RMUL},{RND}))', USD, bold=True)
    calc(pp, f"V{r}", f'=IF({on},"",U{r}*({ETX}+{PPC})+{PFX}+{LST})', USD)
    calc(pp, f"W{r}", f'=IF({on},"",U{r}-R{r}-V{r})', USD, bold=True)
    calc(pp, f"X{r}", f'=IF(OR({on},N(U{r})=0),"",W{r}/U{r})', "0%")
MV, GV, HL, ML = "Matte vinyl sticker paper (letter)", "Glossy vinyl sticker paper (letter)", "Holographic laminate sheets (letter)", "Matte laminate sheets (letter)"
prods = [("Mushroom forest sticker sheet", "Sticker sheet", MV, 2, "Heavy", ML, "Kraft backing card 4 x 6", "Cello sleeve 5 x 7 (self-seal)", None, 4, 0.5, 14),
         ("Planner icons kiss-cut sheet", "Kiss-cut sheet", MV, 2, "Medium", None, None, "Cello sleeve 5 x 7 (self-seal)", None, 4, 0.5, 60),
         ("Frog with umbrella die-cut 3 in", "Die-cut single", GV, 9, "Heavy", HL, "Kraft backing card 4 x 6", "Cello sleeve 4 x 6 (self-seal)", None, 8, 0.5, 1),
         ("Cozy reading pack of 10", "Sticker pack", MV, 1.2, "Heavy", ML, "Kraft backing card 4 x 6", "Cello sleeve 4 x 6 (self-seal)", None, 9, 2, 10),
         ("Holographic moon phases sheet", "Sticker sheet", GV, 2, "Medium", HL, "Kraft backing card 4 x 6", "Cello sleeve 5 x 7 (self-seal)", None, 4, 0.5, 9),
         ("Water bottle decal (clear) 3 in", "Die-cut single", "Clear vinyl sticker paper (letter)", 9, "Medium", None, None, "Cello sleeve 4 x 6 (self-seal)", None, 7, 0.5, 1),
         ("Bulk die-cut 3 in (bought in)", "Die-cut single", "Die-cut stickers 3 in (printed for you)", 1, None, None, "Kraft backing card 4 x 6", "Cello sleeve 4 x 6 (self-seal)", None, None, 0.5, 1)]
for i, row in enumerate(prods):
    for j, v in enumerate(row):
        if v is not None: pp.cell(6 + i, 1 + j).value = v
dv_list(pp, f"B6:B{NP}", FORMATS); dv_list(pp, f"C6:C{NP}", SLIST); dv_list(pp, f"F6:I{NP}", SLIST)
dv_list(pp, f"E6:E{NP}", "=Settings!$A$22:$A$25")
pp.conditional_formatting.add(f"W6:W{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
legend(pp, NP + 2, 1)
PNAME, PPS, PCOST, PWH, PRET = (f"'Product Pricing'!${c}$6:${c}${NP}" for c in "ADRTU")
PCOL = lambda c: f"'Product Pricing'!${c}$6:${c}${NP}"

# ---------- Print Run Planner ----------
pr = wb.create_sheet("Print Run Planner")
banner(pr, t, "Print run planner", "Pick a product and how many to make: sheets, supplies, time and cost of the run, with a stock check.", 7)
widths(pr, {"A": 30, "B": 32, "C": 2, "D": 30, "E": 14, "F": 14, "G": 14})
label(pr, "A4", "The run", bold=True, size=13)
label(pr, "A5", "Product"); c = inp(pr, "B5", "Mushroom forest sticker sheet"); c.alignment = Alignment(horizontal="left", indent=1)
label(pr, "A6", "How many to make"); inp(pr, "B6", 40, "0")
dv_list(pr, "B5", "=" + PNAME)
M = f"MATCH($B$5,{PNAME},0)"
def P_(col): return f"INDEX({PCOL(col)},{M})"
label(pr, "D4", "What you need", bold=True, size=13)
po = [("Items per sheet", f"=IFERROR({P_('D')},\"\")", "0.##", False),
      ("SHEETS TO PRINT", f'=IFERROR(CEILING(B6/IF(N(E5)=0,1,E5)*(1+{MIS}),1),"")', "0", True),
      ("Print & cut time (hours)", f'=IFERROR(E6*N({P_("J")})/60,"")', "0.0", False),
      ("Packing time (hours)", f'=IFERROR(B6*N({P_("K")})/60,"")', "0.0", False),
      ("COST OF THE RUN", f'=IFERROR(B6*{P_("R")},"")', USD, True),
      ("Worth at wholesale", f'=IFERROR(B6*{P_("T")},"")', USD, False),
      ("Worth at retail", f'=IFERROR(B6*{P_("U")},"")', USD, False),
      ("Profit if all sell retail", f'=IFERROR(B6*{P_("W")},"")', USD, True)]
for i, (a, f, fmt, b) in enumerate(po):
    r = 5 + i; label(pr, f"D{r}", a, bold=b); calc(pr, f"E{r}", f, fmt, bold=b)
pr["E6"].font = Font(name=F, size=16, bold=True, color="1F2A44"); pr["E9"].font = Font(name=F, size=14, bold=True, color="1F2A44")
pr.row_dimensions[6].height = 28
label(pr, "A15", "Supply check", bold=True, size=12)
header(pr, 16, ["Supply", "Needed", "", "On hand", "Short by", "Check"], t)
checks = [("C", "E6"), ("F", "E6"), ("G", "B6"), ("H", "B6"), ("I", "B6")]
for i, (col, need) in enumerate(checks):
    r = 17 + i
    calc(pr, f"A{r}", f'=IFERROR(IF({P_(col)}="","",{P_(col)}),"")'); pr[f"A{r}"].alignment = Alignment(horizontal="left", indent=1)
    calc(pr, f"B{r}", f'=IF(A{r}="","",{need})', "0")
    calc(pr, f"D{r}", f'=IF(A{r}="","",IFERROR(INDEX({SHAND},MATCH(A{r},{SNAME},0)),0))', "#,##0")
    calc(pr, f"E{r}", f'=IF(A{r}="","",MAX(0,B{r}-N(D{r})))', "#,##0")
    calc(pr, f"F{r}", f'=IF(A{r}="","",IF(E{r}>0,"Order more","Enough"))')
pr.conditional_formatting.add("F17:F21", CellIsRule(operator="equal", formula=['"Order more"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
pr.conditional_formatting.add("F17:F21", CellIsRule(operator="equal", formula=['"Enough"'], fill=grn, font=Font(name=F, bold=True, color="2E6B3A")))
label(pr, "A23", "Sheets to print includes your misprint allowance. Sticker paper and laminate are counted in sheets; card, sleeves and extras in items.",
      italic=True, size=9, color=GREY)

# ---------- Print Runs ----------
rn = wb.create_sheet("Print Runs")
banner(rn, t, "Print runs", "Log every batch you make. The Stock tab adds these up.", 7)
header(rn, 5, ["Date", "Product", "Quantity made", "Sheets used", "Cost of run", "Month", "Notes"], t)
widths(rn, {"A": 13, "B": 32, "C": 11, "D": 11, "E": 12, "F": 8, "G": 30}); rn.freeze_panes = "A6"
for r in range(6, NR + 1):
    for col in "ABCG": inp(rn, f"{col}{r}")
    for col in "BG": rn[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    rn[f"A{r}"].number_format = "dd mmm yyyy"
    calc(rn, f"D{r}", f'=IF(OR(B{r}="",C{r}=""),"",IFERROR(CEILING(C{r}/IF(N(INDEX({PPS},MATCH(B{r},{PNAME},0)))=0,1,INDEX({PPS},MATCH(B{r},{PNAME},0))),1),""))', "0")
    calc(rn, f"E{r}", f'=IF(OR(B{r}="",C{r}=""),"",C{r}*IFERROR(INDEX({PCOST},MATCH(B{r},{PNAME},0)),0))', USD)
    calc(rn, f"F{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(rn, f"B6:B{NR}", "=" + PNAME)
runs = [(-40, "Mushroom forest sticker sheet", 60, ""), (-38, "Frog with umbrella die-cut 3 in", 90, ""), (-30, "Cozy reading pack of 10", 30, ""),
        (-26, "Planner icons kiss-cut sheet", 40, ""), (-21, "Holographic moon phases sheet", 50, "Holiday market prep"),
        (-20, "Water bottle decal (clear) 3 in", 45, ""), (-12, "Bulk die-cut 3 in (bought in)", 100, "Print shop order"),
        (-5, "Frog with umbrella die-cut 3 in", 54, "Restock")]
for i, (dd, p, q, note) in enumerate(runs):
    r = 6 + i; rn[f"A{r}"] = f"=TODAY(){dd:+d}"; rn[f"B{r}"] = p; rn[f"C{r}"] = q; rn[f"G{r}"] = note
RP, RQ = (f"'Print Runs'!${c}$6:${c}${NR}" for c in "BC")

# ---------- Sales ----------
sa = wb.create_sheet("Sales")
banner(sa, t, "Sales log", "One row per sale. Blank price = retail (wholesale for the Wholesale channel). Cost comes from Product Pricing.", 11)
header(sa, 5, ["Date", "Channel", "Product", "Qty", "Price each (blank = list)", "Sale total", "Fees & shipping paid", "Cost of goods", "Profit", "Month", "Notes"], t)
sa.row_dimensions[5].height = 44
widths(sa, {"A": 13, "B": 13, "C": 32, "D": 7, "E": 12, "F": 12, "G": 13, "H": 13, "I": 12, "J": 9, "K": 24}); sa.freeze_panes = "A6"
for r in range(6, NSALE + 1):
    for col in "ABCDEGK": inp(sa, f"{col}{r}")
    for col in "CK": sa[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sa[f"A{r}"].number_format = "dd mmm yyyy"; sa[f"E{r}"].number_format = USD; sa[f"G{r}"].number_format = USD
    lp = f'IFERROR(IF(B{r}="Wholesale",INDEX({PWH},MATCH(C{r},{PNAME},0)),INDEX({PRET},MATCH(C{r},{PNAME},0))),0)'
    calc(sa, f"F{r}", f'=IF(OR(C{r}="",D{r}=""),"",D{r}*IF(E{r}="",{lp},E{r}))', USD)
    calc(sa, f"H{r}", f'=IF(OR(C{r}="",D{r}=""),"",D{r}*IFERROR(INDEX({PCOST},MATCH(C{r},{PNAME},0)),0))', USD)
    calc(sa, f"I{r}", f'=IF(F{r}="","",F{r}-N(G{r})-N(H{r}))', USD)
    calc(sa, f"J{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
CH = ["Etsy", "Website", "Market", "Wholesale", "Instagram", "Other"]
dv_list(sa, f"B6:B{NSALE}", ",".join(CH)); dv_list(sa, f"C6:C{NSALE}", "=" + PNAME)
sales = [(33, "Etsy", "Mushroom forest sticker sheet", 3, None, "etsy", ""), (29, "Etsy", "Frog with umbrella die-cut 3 in", 5, None, "etsy", ""),
         (25, "Wholesale", "Frog with umbrella die-cut 3 in", 48, None, 12, "Paper & Pine gift shop"),
         (24, "Wholesale", "Mushroom forest sticker sheet", 24, None, 9, "Paper & Pine gift shop"),
         (19, "Market", "Holographic moon phases sheet", 22, None, 0, "Winter craft fair"), (19, "Market", "Cozy reading pack of 10", 14, None, 0, "Winter craft fair"),
         (19, "Market", "Frog with umbrella die-cut 3 in", 31, 3, 0, "3 for $8 deal"), (12, "Website", "Planner icons kiss-cut sheet", 6, None, 4.5, ""),
         (8, "Instagram", "Water bottle decal (clear) 3 in", 7, None, 1.2, ""), (4, "Etsy", "Cozy reading pack of 10", 4, None, "etsy", ""),
         (2, "Market", "Bulk die-cut 3 in (bought in)", 26, None, 0, "Library market"), (1, "Etsy", "Holographic moon phases sheet", 3, None, "etsy", "")]
for i, (back, ch, p, q, price, fees, note) in enumerate(sales):
    r = 6 + i; sa[f"A{r}"] = f"=TODAY()-{back}"; sa[f"B{r}"] = ch; sa[f"C{r}"] = p; sa[f"D{r}"] = q; sa[f"K{r}"] = note
    if price is not None: sa[f"E{r}"] = price
    sa[f"G{r}"] = fees if fees != "etsy" else f"=ROUND(F{r}*({ETX}+{PPC})+{PFX}+{LST},2)"
SD, SCH, SC, SQ, ST, SG, SH, SPF = (f"Sales!${c}$6:${c}${NSALE}" for c in "ABCDFGHI")

# ---------- Stock ----------
sk = wb.create_sheet("Stock")
banner(sk, t, "Finished stock", "What's on hand for every design: made (Print Runs) - sold (Sales) - damaged or given away.", 9)
header(sk, 5, ["Product / design", "Made", "Sold", "Damaged / freebies", "ON HAND", "Make more at", "Status", "Stock value at cost", "Stock value at retail"], t)
sk.row_dimensions[5].height = 44
widths(sk, {"A": 32, "B": 9, "C": 9, "D": 11, "E": 10, "F": 10, "G": 13, "H": 13, "I": 13}); sk.freeze_panes = "B6"
for i in range(NP - 5):
    r = 6 + i; pr_ = 6 + i
    sk[f"A{r}"] = f"=IF('Product Pricing'!A{pr_}=\"\",\"\",'Product Pricing'!A{pr_})"; sk[f"A{r}"].font = Font(name=F, size=11)
    sk[f"A{r}"].alignment = Alignment(horizontal="left", indent=1)
    inp(sk, f"D{r}", None, "0"); inp(sk, f"F{r}", None, "0")
    calc(sk, f"B{r}", f'=IF(A{r}="","",SUMIFS({RQ},{RP},A{r}))', "#,##0")
    calc(sk, f"C{r}", f'=IF(A{r}="","",SUMIFS({SQ},{SC},A{r}))', "#,##0")
    calc(sk, f"E{r}", f'=IF(A{r}="","",B{r}-C{r}-N(D{r}))', "#,##0", bold=True)
    calc(sk, f"G{r}", f'=IF(A{r}="","",IF(E{r}<0,"Check counts",IF(E{r}<=N(F{r}),"Make more","OK")))')
    calc(sk, f"H{r}", f"=IF(A{r}=\"\",\"\",MAX(0,E{r})*'Product Pricing'!R{pr_})", USD)
    calc(sk, f"I{r}", f"=IF(A{r}=\"\",\"\",MAX(0,E{r})*'Product Pricing'!U{pr_})", USD)
for i, (dmg, at) in enumerate([(2, 15), (1, 10), (6, 20), (2, 10), (3, 10), (0, 10), (4, 25)]):
    sk[f"D{6 + i}"] = dmg; sk[f"F{6 + i}"] = at
NK = NP
for val, fill, col in (('"Make more"', red, "A12A1E"), ('"Check counts"', amb, "8A5A12"), ('"OK"', grn, "2E6B3A")):
    sk.conditional_formatting.add(f"G6:G{NK}", CellIsRule(operator="equal", formula=[val], fill=fill, font=Font(name=F, bold=True, color=col)))
label(sk, f"A{NK + 2}", "Damaged / freebies: misprints you found later, stickers added to orders as a thank-you, samples for shops.", italic=True, size=9, color=GREY)

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Sales, Print Runs, Stock and Supplies.", 9)
widths(d, {"A": 30, "B": 15, "C": 14, "D": 14, "E": 14, "F": 4, "G": 32, "H": 12, "I": 14})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{SD},">="&DATE($B$4,1,1),{SD},"<"&DATE($B$4+1,1,1)'
kpi = [("Sales", f"=SUMIFS({ST},{yr})", USD), ("Profit", f"=SUMIFS({SPF},{yr})", USD), ("Items sold", f"=SUMIFS({SQ},{yr})", "#,##0"),
       ("Profit margin", '=IF(B6=0,"",B7/B6)', "0%"),
       ("Average order", f'=IFERROR(B6/COUNTIFS({SC},"<>",{yr}),"")', USD),
       ("Stock on hand (items)", f"=SUM(Stock!$E$6:$E${NK})", "#,##0"),
       ("Stock value at cost", f"=SUM(Stock!$H$6:$H${NK})", USD),
       ("Designs to make more of", f'=COUNTIF(Stock!$G$6:$G${NK},"Make more")', "0"),
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
header(d, 5, ["Channel", "Sales", "Profit"], t, start=7)
for i, ch in enumerate(CH):
    r = 6 + i; label(d, f"G{r}", ch)
    calc(d, f"H{r}", f'=SUMIFS({ST},{SCH},G{r},{yr})', USD); calc(d, f"I{r}", f'=SUMIFS({SPF},{SCH},G{r},{yr})', USD)
header(d, 16, ["Product / design", "Items sold", "Profit"], t, start=7)
for i in range(12):
    r = 17 + i
    d[f"G{r}"] = f"=IF('Product Pricing'!A{6 + i}=\"\",\"\",'Product Pricing'!A{6 + i})"; d[f"G{r}"].font = Font(name=F, size=11)
    calc(d, f"H{r}", f'=IF(G{r}="","",SUMIFS({SQ},{SC},G{r},{yr}))', "#,##0")
    calc(d, f"I{r}", f'=IF(G{r}="","",SUMIFS({SPF},{SC},G{r},{yr}))', USD)
label(d, "G29", "Shows your first 12 products from Product Pricing.", italic=True, size=9, color=GREY)

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
