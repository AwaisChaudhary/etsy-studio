"""Candle Business Spreadsheet (batch 4, lane a): supplies & inventory, candle costing with fragrance load,
wholesale/retail pricing with Etsy fee estimate, batch pour planner, sales log and dashboard. Excel + Google Sheets."""
import sys, datetime as dt; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule

t = Theme("3E2C23", "C7793B", "F7EBDD")
wb = Workbook()
NS, NP, NSALE = 105, 45, 506          # supplies rows 6..105, product rows 6..45, sales rows 6..506
USD, USD4 = '"$"#,##0.00', '"$"#,##0.0000'

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Candle Business Spreadsheet", "Cost every candle to the cent, price it for wholesale and retail, plan your pours and track sales.", 6)
widths(s, {"A": 6, "B": 96})
steps = ["Settings: your hourly rate, overheads, wholesale and retail mark-ups and the Etsy fee estimate.",
         "Supplies: add each wax, fragrance oil, wick, vessel, lid, label and box once with its pack size and price. Add what you have on hand to track stock.",
         "Candle Costing: one row per candle you sell. Pick the vessel, wax, fragrance and wick, type the fill weight and fragrance load. Cost, wholesale and retail prices appear.",
         "Pour Planner: pick a candle and how many you want to pour. You get the exact wax and fragrance to weigh out, and whether you have enough stock.",
         "Sales: log every sale (Etsy, markets, wholesale, website). Profit is worked out from the candle's real cost.",
         "Dashboard: sales, profit and units by month, by channel and by candle, plus supplies that need reordering."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Fragrance load is a percentage of the wax weight (the common candle-maker method): fragrance = wax x load. "
      "Weights are in ounces; grams are shown too. Example supplies, candles and sales are included: type over them or delete them.", italic=True, size=10)
s.row_dimensions[14].height = 44
label(s, "B15", "Works in Excel and Google Sheets. Prices in the examples are illustrations only; use your own receipts.", italic=True, size=10)

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates. Every candle uses these.", 4)
widths(st, {"A": 44, "B": 16, "C": 4, "D": 62})
rows = [("Your hourly rate", 18, USD, "Pouring, curing checks, labelling, packing and clean-up time."),
        ("Overheads (% of materials)", 0.10, "0%", "Electricity, heat gun, pouring pitchers, wear on equipment."),
        ("Wholesale price = cost x", 2, '0.0"x"', "Common rule: wholesale is about 2x your total cost."),
        ("Retail price = wholesale x", 2, '0.0"x"', "Common rule: retail is about 2x wholesale."),
        ("Round prices up to the nearest", 0.5, USD, "Use 0.5 or 1 for clean prices."),
        ("Etsy transaction fee", 0.065, "0.0%", "Estimate. Check Etsy's current fees for your country."),
        ("Payment processing (%)", 0.03, "0.0%", "Estimate, varies by country."),
        ("Payment processing (fixed per order)", 0.25, USD, None),
        ("Listing fee per sale", 0.20, USD, None),
        ("Spill allowance for pours", 0.03, "0%", "Extra wax and fragrance for what stays in the pitcher.")]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"D{5 + i}", n, size=9, color="7F7066", italic=True)
RATE, OVH, WMUL, RMUL, RND, ETX, PPC, PFX, LST, SPILL = (f"Settings!$B${5 + i}" for i in range(10))
label(st, "A17", "Unit list (for drop-downs)", bold=True, size=9, color="7F7066")
UNITS = [("oz", 1), ("lb", 16), ("g", 0.035274), ("kg", 35.274), ("each", 1)]
for i, (u, f) in enumerate(UNITS):
    st[f"A{18 + i}"] = u; st[f"B{18 + i}"] = f; st[f"A{18 + i}"].font = Font(name=F, size=9, color="7F7066"); st[f"B{18 + i}"].font = Font(name=F, size=9, color="7F7066")
TYPES = "Wax,Fragrance,Wick,Vessel,Lid,Label,Dye,Box,Other"

# ---------- Supplies & stock ----------
su = wb.create_sheet("Supplies")
banner(su, t, "Supplies & stock", "Add each supply once. Cost per ounce (or per piece) is worked out for you.", 11)
header(su, 5, ["Supply", "Type", "Pack size", "Unit", "Pack price", "Cost per oz / each", "On hand (units)", "Reorder at", "Stock status", "Supplier / notes", "oz per unit"], t)
widths(su, {"A": 30, "B": 12, "C": 11, "D": 9, "E": 12, "F": 15, "G": 14, "H": 12, "I": 14, "J": 26, "K": 9}); su.freeze_panes = "B6"
for r in range(6, NS + 1):
    for col in "ABCDEGHJ": inp(su, f"{col}{r}")
    for col in "AJ": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    su[f"E{r}"].number_format = USD; su[f"C{r}"].number_format = "#,##0.##"; su[f"G{r}"].number_format = "#,##0.##"; su[f"H{r}"].number_format = "#,##0.##"
    su[f"K{r}"] = f'=IF(D{r}="","",IFERROR(VLOOKUP(D{r},Settings!$A$18:$B$22,2,FALSE),1))'
    su[f"K{r}"].font = Font(name=F, size=9, color="9A8F86"); su[f"K{r}"].number_format = "0.####"
    calc(su, f"F{r}", f'=IF(OR(A{r}="",C{r}="",E{r}="",C{r}=0),"",E{r}/(C{r}*K{r}))', USD4)
    calc(su, f"I{r}", f'=IF(OR(A{r}="",G{r}=""),"",IF(G{r}<=N(H{r}),"Reorder","OK"))')
ex = [("Soy wax (container blend)", "Wax", 10, "lb", 39.99, 18, 8, "Bulk 10 lb bag"),
      ("Coconut soy wax", "Wax", 10, "lb", 54.99, 6, 5, ""),
      ("Fragrance: Fireside Cedar", "Fragrance", 16, "oz", 24.99, 22, 8, "Max load 10%"),
      ("Fragrance: Vanilla Bean", "Fragrance", 16, "oz", 21.99, 6, 8, ""),
      ("Fragrance: Fresh Linen", "Fragrance", 16, "oz", 22.99, 14, 8, ""),
      ("Fragrance: Sugared Orange", "Fragrance", 8, "oz", 14.99, 8, 4, "Holiday scent"),
      ("Cotton wick, pre-tabbed (medium)", "Wick", 100, "each", 9.99, 140, 50, "For 3 in jars"),
      ("Wooden wick (0.5 in)", "Wick", 50, "each", 14.99, 30, 20, ""),
      ("Amber jar 8 oz", "Vessel", 12, "each", 21.99, 36, 24, "Fill weight about 7 oz"),
      ("Amber jar 16 oz", "Vessel", 12, "each", 32.99, 10, 12, "Fill weight about 13 oz"),
      ("Travel tin 4 oz", "Vessel", 24, "each", 16.99, 40, 24, ""),
      ("Black metal lid", "Lid", 24, "each", 9.99, 60, 24, ""),
      ("Waterproof label (round)", "Label", 120, "each", 17.99, 220, 60, ""),
      ("Warning label", "Label", 500, "each", 11.99, 400, 100, ""),
      ("Kraft gift box", "Box", 25, "each", 18.99, 20, 25, ""),
      ("Liquid candle dye", "Dye", 1, "oz", 4.99, 2, 1, "About 1 drop per lb")]
for i, row in enumerate(ex):
    for j, v in enumerate(row): su.cell(6 + i, [1, 2, 3, 4, 5, 7, 8, 10][j]).value = v
dv_list(su, f"B6:B{NS}", TYPES); dv_list(su, f"D6:D{NS}", "=Settings!$A$18:$A$22")
su.conditional_formatting.add(f"I6:I{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=PatternFill("solid", fgColor="F8D7D3"), font=Font(name=F, bold=True, color="A12A1E")))
SNAME, SCOST, SHAND, SOZ = (f"Supplies!$A$6:$A${NS}", f"Supplies!$F$6:$F${NS}", f"Supplies!$G$6:$G${NS}", f"Supplies!$K$6:$K${NS}")

def cost_of(ref):
    return f'IF({ref}="",0,IFERROR(INDEX({SCOST},MATCH({ref},{SNAME},0)),0))'

# ---------- Candle costing ----------
cc = wb.create_sheet("Candle Costing")
banner(cc, t, "Candle costing & pricing", "One row per candle you sell. Yellow: your recipe. Green: cost and prices.", 23)
cols = ["Candle name", "Vessel", "Fill weight (oz)", "Wax", "Fragrance oil", "Fragrance load", "Wick", "Wicks per candle", "Lid", "Label", "Box / extras",
        "Labour (min each)", "Wax (oz)", "Fragrance (oz)", "Materials", "Labour", "Overheads", "TOTAL COST", "Wholesale price", "Retail price",
        "Etsy fees (est.)", "Profit per retail sale", "Margin"]
header(cc, 5, cols, t)
cc.row_dimensions[5].height = 44
for i, w in enumerate([24, 18, 10, 20, 22, 10, 22, 9, 15, 18, 15, 10, 9, 10, 11, 10, 10, 12, 12, 11, 11, 13, 9]):
    cc.column_dimensions[chr(65 + i)].width = w
cc.freeze_panes = "B6"
label(cc, "A4", "Fill weight = total weight of wax + fragrance in the vessel. Load is % of wax weight (8% to 10% is typical).", italic=True, size=9, color="7F7066")
for r in range(6, NP + 1):
    for col in "ABCDEFGHIJKL": inp(cc, f"{col}{r}")
    for col in "ABDEGIJK": cc[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    cc[f"C{r}"].number_format = "0.0"; cc[f"F{r}"].number_format = "0.0%"
    on = f'A{r}=""'
    calc(cc, f"M{r}", f'=IF(OR({on},C{r}=""),"",C{r}/(1+N(F{r})))', "0.00")
    calc(cc, f"N{r}", f'=IF(M{r}="","",C{r}-M{r})', "0.00")
    calc(cc, f"O{r}", f'=IF({on},"",N(M{r})*{cost_of(f"D{r}")}+N(N{r})*{cost_of(f"E{r}")}+N(H{r})*{cost_of(f"G{r}")}'
                      f'+{cost_of(f"B{r}")}+{cost_of(f"I{r}")}+{cost_of(f"J{r}")}+{cost_of(f"K{r}")})', USD)
    calc(cc, f"P{r}", f'=IF({on},"",N(L{r})/60*{RATE})', USD)
    calc(cc, f"Q{r}", f'=IF({on},"",O{r}*{OVH})', USD)
    calc(cc, f"R{r}", f'=IF({on},"",O{r}+P{r}+Q{r})', USD, bold=True)
    calc(cc, f"S{r}", f'=IF({on},"",CEILING(R{r}*{WMUL},{RND}))', USD, bold=True)
    calc(cc, f"T{r}", f'=IF({on},"",CEILING(S{r}*{RMUL},{RND}))', USD, bold=True)
    calc(cc, f"U{r}", f'=IF({on},"",T{r}*({ETX}+{PPC})+{PFX}+{LST})', USD)
    calc(cc, f"V{r}", f'=IF({on},"",T{r}-R{r}-U{r})', USD, bold=True)
    calc(cc, f"W{r}", f'=IF(OR({on},N(T{r})=0),"",V{r}/T{r})', "0%")
cands = [("Fireside Cedar 8 oz", "Amber jar 8 oz", 7, "Soy wax (container blend)", "Fragrance: Fireside Cedar", 0.09, "Cotton wick, pre-tabbed (medium)", 1, "Black metal lid", "Waterproof label (round)", "Warning label", 6),
         ("Vanilla Bean 16 oz", "Amber jar 16 oz", 13, "Coconut soy wax", "Fragrance: Vanilla Bean", 0.08, "Cotton wick, pre-tabbed (medium)", 2, "Black metal lid", "Waterproof label (round)", "Warning label", 8),
         ("Fresh Linen travel tin", "Travel tin 4 oz", 3.5, "Soy wax (container blend)", "Fragrance: Fresh Linen", 0.08, "Cotton wick, pre-tabbed (medium)", 1, None, "Waterproof label (round)", "Warning label", 8),
         ("Sugared Orange gift box", "Amber jar 8 oz", 7, "Coconut soy wax", "Fragrance: Sugared Orange", 0.10, "Wooden wick (0.5 in)", 1, "Black metal lid", "Waterproof label (round)", "Kraft gift box", 9)]
for i, row in enumerate(cands):
    for j, v in enumerate(row):
        if v is not None: cc.cell(6 + i, 1 + j).value = v
rng = f"6:{NP}"
dv_list(cc, f"B6:B{NP}", f"=Supplies!$A$6:$A${NS}")
for col in "DEGIJK": dv_list(cc, f"{col}6:{col}{NP}", f"=Supplies!$A$6:$A${NS}")
cc.conditional_formatting.add(f"V6:V{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
cc.conditional_formatting.add(f"F6:F{NP}", CellIsRule(operator="greaterThan", formula=["0.12"], fill=PatternFill("solid", fgColor="F8D7D3")))
legend(cc, NP + 2, 1)
CNAME, CCOST = f"'Candle Costing'!$A$6:$A${NP}", f"'Candle Costing'!$R$6:$R${NP}"

# ---------- Pour planner ----------
pp = wb.create_sheet("Pour Planner")
banner(pp, t, "Pour planner", "Pick a candle and how many to pour. Weigh out exactly this much.", 7)
widths(pp, {"A": 30, "B": 30, "C": 14, "D": 14, "E": 14, "F": 14, "G": 12})
label(pp, "A4", "Candle", bold=True, size=12); inp(pp, "B4", "Fireside Cedar 8 oz"); pp["B4"].alignment = Alignment(horizontal="left", indent=1)
dv_list(pp, "B4", "=" + CNAME)
label(pp, "A5", "How many candles", bold=True, size=12); inp(pp, "B5", 24, "0")
pp["H4"] = f'=IFERROR(MATCH(B4,{CNAME},0)+5,"")'; pp["H4"].font = Font(name=F, size=8, color="FFFFFF")
def cc_ref(col): return f'IF($H$4="","",INDEX(\'Candle Costing\'!${col}:${col},$H$4))'
header(pp, 7, ["What", "Supply", "Per candle", "Total (oz / pcs)", "Total in grams", "On hand (oz / pcs)", "Enough?"], t)
lines = [("Wax", "D", "M", True, 1), ("Fragrance oil", "E", "N", True, 1), ("Wicks", "G", "H", False, 0), ("Vessels", "B", None, False, 0),
         ("Lids", "I", None, False, 0), ("Labels", "J", None, False, 0), ("Box / extras", "K", None, False, 0)]
for i, (what, scol, qcol, weight, _) in enumerate(lines):
    r = 8 + i; label(pp, f"A{r}", what, bold=True)
    calc(pp, f"B{r}", "=" + cc_ref(scol)); pp[f"B{r}"].alignment = Alignment(horizontal="left", indent=1)
    per = ("=" + cc_ref(qcol)) if qcol else f'=IF(OR(B{r}="",B{r}=0),"",1)'
    calc(pp, f"C{r}", per, "0.00" if weight else "0")
    if weight:
        calc(pp, f"D{r}", f'=IF(OR(B{r}="",B{r}=0,C{r}=""),"",C{r}*$B$5*(1+{SPILL}))', "#,##0.0")
        calc(pp, f"E{r}", f'=IF(D{r}="","",D{r}*28.3495)', "#,##0")
    else:
        calc(pp, f"D{r}", f'=IF(OR(B{r}="",B{r}=0,C{r}=""),"",C{r}*$B$5)', "#,##0")
        calc(pp, f"E{r}", '=""')
    calc(pp, f"F{r}", f'=IF(OR(B{r}="",B{r}=0),"",IFERROR(INDEX({SHAND},MATCH(B{r},{SNAME},0))*INDEX({SOZ},MATCH(B{r},{SNAME},0)),""))', "#,##0.0" if weight else "#,##0")
    calc(pp, f"G{r}", f'=IF(OR(D{r}="",F{r}=""),"",IF(F{r}>=D{r},"Yes","Short "&TEXT(D{r}-F{r},"0.0")))')
pp.conditional_formatting.add("G8:G14", FormulaRule(formula=['LEFT(G8,5)="Short"'], fill=PatternFill("solid", fgColor="F8D7D3"), font=Font(name=F, bold=True, color="A12A1E")))
pp.conditional_formatting.add("G8:G14", CellIsRule(operator="equal", formula=['"Yes"'], fill=PatternFill("solid", fgColor="E3F0E1"), font=Font(name=F, bold=True, color="2E6B3A")))
label(pp, "A16", "Batch summary", bold=True, size=13)
summ = [("Wax to weigh (lb)", '=IF(D8="","",D8/16)', "0.00"), ("Total pour weight (oz)", '=IF(D8="","",D8+N(D9))', "#,##0.0"),
        ("Cost of this batch", f'=IF($H$4="","",INDEX(\'Candle Costing\'!$R:$R,$H$4)*B5)', USD),
        ("Wholesale value", f'=IF($H$4="","",INDEX(\'Candle Costing\'!$S:$S,$H$4)*B5)', USD),
        ("Retail value", f'=IF($H$4="","",INDEX(\'Candle Costing\'!$T:$T,$H$4)*B5)', USD)]
for i, (a, f, fmt) in enumerate(summ):
    label(pp, f"A{17 + i}", a); calc(pp, f"B{17 + i}", f, fmt, bold=True)
label(pp, "A23", "Totals include the spill allowance from Settings. Add fragrance at the temperature your wax supplier recommends.", italic=True, size=9, color="7F7066")

# ---------- Sales ----------
sa = wb.create_sheet("Sales")
banner(sa, t, "Sales log", "One row per sale. Cost comes from Candle Costing, so profit is real.", 11)
header(sa, 5, ["Date", "Channel", "Candle", "Qty", "Price each", "Sale total", "Fees & shipping paid", "Cost of candles", "Profit", "Month", "Notes"], t)
widths(sa, {"A": 13, "B": 13, "C": 26, "D": 7, "E": 11, "F": 12, "G": 13, "H": 13, "I": 12, "J": 9, "K": 24}); sa.freeze_panes = "A6"
for r in range(6, NSALE + 1):
    for col in "ABCDEGK": inp(sa, f"{col}{r}")
    for col in "CK": sa[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sa[f"A{r}"].number_format = "dd mmm yyyy"; sa[f"E{r}"].number_format = USD; sa[f"G{r}"].number_format = USD
    calc(sa, f"F{r}", f'=IF(OR(D{r}="",E{r}=""),"",D{r}*E{r})', USD)
    calc(sa, f"H{r}", f'=IF(OR(C{r}="",D{r}=""),"",D{r}*IFERROR(INDEX({CCOST},MATCH(C{r},{CNAME},0)),0))', USD)
    calc(sa, f"I{r}", f'=IF(F{r}="","",F{r}-N(G{r})-N(H{r}))', USD)
    calc(sa, f"J{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(sa, f"B6:B{NSALE}", "Etsy,Market,Wholesale,Website,Instagram,Other")
dv_list(sa, f"C6:C{NSALE}", "=" + CNAME)
for j, v in enumerate(["=TODAY()-3", "Etsy", "Fireside Cedar 8 oz", 2, None, None, None, None, None, None, "Gift wrapped"]):
    if v is not None: sa.cell(6, 1 + j).value = v
sa["E6"] = "='Candle Costing'!T6"; sa["G6"] = "=ROUND(F6*(Settings!B10+Settings!B11)+Settings!B12+Settings!B13,2)"
SD, SCH, SC, SQ, ST, SG, SH, SP = (f"Sales!$A$6:$A${NSALE}", f"Sales!$B$6:$B${NSALE}", f"Sales!$C$6:$C${NSALE}", f"Sales!$D$6:$D${NSALE}",
                                   f"Sales!$F$6:$F${NSALE}", f"Sales!$G$6:$G${NSALE}", f"Sales!$H$6:$H${NSALE}", f"Sales!$I$6:$I${NSALE}")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from the Sales log and Supplies.", 9)
widths(d, {"A": 24, "B": 14, "C": 14, "D": 14, "E": 14, "F": 4, "G": 26, "H": 12, "I": 14})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
Y0, Y1 = "DATE($B$4,1,1)", "DATE($B$4+1,1,1)"
yr = f'{SD},">="&{Y0},{SD},"<"&{Y1}'
kpi = [("Sales", f"=SUMIFS({ST},{yr})", USD), ("Profit", f"=SUMIFS({SP},{yr})", USD), ("Candles sold", f"=SUMIFS({SQ},{yr})", "#,##0"),
       ("Profit margin", '=IF(B6=0,"",B7/B6)', "0%"), ("Supplies to reorder", f'=COUNTIF(Supplies!$I$6:$I${NS},"Reorder")', "0")]
for i, (a, f, fmt) in enumerate(kpi):
    r = 6 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 28
header(d, 12, ["Month", "Sales", "Fees & shipping", "Cost", "Profit"], t)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for i, mn in enumerate(MONTHS):
    r = 13 + i; label(d, f"A{r}", mn)
    mr = f'{SD},">="&DATE($B$4,{i + 1},1),{SD},"<"&DATE($B$4,{i + 2},1)'
    for col, rg in zip("BCDE", (ST, SG, SH, SP)): calc(d, f"{col}{r}", f"=SUMIFS({rg},{mr})", USD)
label(d, "A25", "Total", bold=True)
for col in "BCDE": calc(d, f"{col}25", f"=SUM({col}13:{col}24)", USD, bold=True)
header(d, 12, ["Channel", "Sales", "Profit"], t, start=7)
for i, ch in enumerate(["Etsy", "Market", "Wholesale", "Website", "Instagram", "Other"]):
    r = 13 + i; label(d, f"G{r}", ch)
    calc(d, f"H{r}", f'=SUMIFS({ST},{SCH},G{r},{yr})', USD); calc(d, f"I{r}", f'=SUMIFS({SP},{SCH},G{r},{yr})', USD)
header(d, 21, ["Candle", "Sold", "Profit"], t, start=7)
for i in range(12):
    r = 22 + i
    d[f"G{r}"] = f"=IF('Candle Costing'!A{6 + i}=\"\",\"\",'Candle Costing'!A{6 + i})"; d[f"G{r}"].font = Font(name=F, size=11)
    calc(d, f"H{r}", f'=IF(G{r}="","",SUMIFS({SQ},{SC},G{r},{yr}))', "#,##0")
    calc(d, f"I{r}", f'=IF(G{r}="","",SUMIFS({SP},{SC},G{r},{yr}))', USD)
label(d, "G34", "Shows your first 12 candles from Candle Costing.", italic=True, size=9, color="7F7066")

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
