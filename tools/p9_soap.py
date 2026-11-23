"""Soap Making Business Spreadsheet (batch 6, lane a): supplies & stock, recipe costing by ingredient line (cold process,
hot process or melt & pour), cost per bar + wholesale/retail pricing with Etsy fee estimate, batch planner with stock check,
batch & cure tracker (ready dates), sales log and dashboard. Excel + Google Sheets.
It costs recipes; it does NOT calculate lye (buyers enter the lye and water amounts from their own lye calculator)."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule

t = Theme("2F4F4A", "C2785C", "EEF3EE")
wb = Workbook()
NS, NR, NP, NB, NSALE = 105, 305, 45, 205, 506   # last rows: supplies, recipe lines, soaps, batches, sales (all start at row 6)
USD, USD4 = '"$"#,##0.00', '"$"#,##0.0000'
GREY = "7F7066"

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Soap Making Business Spreadsheet", "Cost every bar to the cent, price for wholesale and retail, plan batches, track cure dates and sales.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly rate, overheads, wholesale and retail mark-ups, Etsy fee estimate and your usual cure time.",
         "Supplies: add each oil, butter, lye, liquid, fragrance, colour, additive, melt & pour base and packaging item once, with pack size and price.",
         "Recipes: one line per ingredient. Type the recipe name on every line, pick the ingredient and type the amount per batch. % of oils and cost appear.",
         "Soap Pricing: one row per soap. Type the recipe name, bars per batch, wrap/label/box and labour. Cost per bar, wholesale and retail prices appear.",
         "Batch Planner: pick a soap and how many bars you want. You get every ingredient to weigh out (oz and g) and whether you have enough stock.",
         "Batches & Cure: log each batch you make. Ready dates and 'Curing / Ready' status work themselves out.",
         "Sales and Dashboard: log every sale; profit, bars in stock and best sellers update for you."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 13, 2)
label(s, "B15", "Important: this spreadsheet costs and prices your recipes. It does not calculate lye. Always work out lye and water with a trusted "
      "soap (lye) calculator and enter those amounts in your recipe. Follow lye safety guidance every time you make soap.", bold=True, size=10, color="A12A1E")
s.row_dimensions[15].height = 46
label(s, "B16", "Amounts can be typed in oz, lb, g or kg: everything is converted to ounces by weight. Example supplies, recipes, batches and sales "
      "are included so you can see how it works: type over them or delete them. Prices in the examples are illustrations only.", italic=True, size=10)
s.row_dimensions[16].height = 44
label(s, "B17", "Works in Excel and Google Sheets.", italic=True, size=10)

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates. Every soap uses these.", 4)
widths(st, {"A": 44, "B": 16, "C": 4, "D": 66})
rows = [("Your hourly rate", 18, USD, "Making, cutting, curing checks, wrapping and clean-up time."),
        ("Overheads (% of materials)", 0.10, "0%", "Electricity, moulds, gloves, goggles, wear on equipment."),
        ("Wholesale price = cost x", 2, '0.0"x"', "Common rule: wholesale is about 2x your total cost."),
        ("Retail price = wholesale x", 2, '0.0"x"', "Common rule: retail is about 2x wholesale."),
        ("Round prices up to the nearest", 0.5, USD, "Use 0.5 or 1 for clean prices."),
        ("Etsy transaction fee", 0.065, "0.0%", "Estimate. Check Etsy's current fees for your country."),
        ("Payment processing (%)", 0.03, "0.0%", "Estimate, varies by country."),
        ("Payment processing (fixed per order)", 0.25, USD, None),
        ("Listing fee per sale", 0.20, USD, None),
        ("Usual cure time (weeks)", 4, "0", "Used when a batch has no cure time typed. Melt & pour: type 0 on the batch."),
        ("Spill allowance for batches", 0.02, "0%", "Extra for what stays in the jug and on the spatula.")]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"D{5 + i}", n, size=9, color=GREY, italic=True)
RATE, OVH, WMUL, RMUL, RND, ETX, PPC, PFX, LST, CURE, SPILL = (f"Settings!$B${5 + i}" for i in range(11))
label(st, "A18", "Unit list (for drop-downs)", bold=True, size=9, color=GREY)
UNITS = [("oz", 1), ("lb", 16), ("g", 0.035274), ("kg", 35.274), ("each", 1)]
for i, (u, f) in enumerate(UNITS):
    st[f"A{19 + i}"] = u; st[f"B{19 + i}"] = f
    st[f"A{19 + i}"].font = Font(name=F, size=9, color=GREY); st[f"B{19 + i}"].font = Font(name=F, size=9, color=GREY)
UL = "Settings!$A$19:$B$23"
TYPES = "Oil,Butter,Lye,Liquid,Fragrance,Essential oil,Colour,Additive,M&P base,Wrap,Label,Box,Other"

# ---------- Supplies ----------
su = wb.create_sheet("Supplies")
banner(su, t, "Supplies & stock", "Add each supply once. Cost per ounce (or per piece) is worked out for you.", 11)
header(su, 5, ["Supply", "Type", "Pack size", "Unit", "Pack price", "Cost per oz / each", "On hand (units)", "Reorder at", "Stock status", "Supplier / notes", "oz per unit"], t)
widths(su, {"A": 30, "B": 13, "C": 11, "D": 9, "E": 12, "F": 15, "G": 14, "H": 12, "I": 14, "J": 26, "K": 9}); su.freeze_panes = "B6"
for r in range(6, NS + 1):
    for col in "ABCDEGHJ": inp(su, f"{col}{r}")
    for col in "AJ": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    su[f"E{r}"].number_format = USD
    for col in "CGH": su[f"{col}{r}"].number_format = "#,##0.##"
    su[f"K{r}"] = f'=IF(D{r}="","",IFERROR(VLOOKUP(D{r},{UL},2,FALSE),1))'
    su[f"K{r}"].font = Font(name=F, size=9, color="9A8F86"); su[f"K{r}"].number_format = "0.####"
    calc(su, f"F{r}", f'=IF(OR(A{r}="",C{r}="",E{r}="",C{r}=0),"",E{r}/(C{r}*K{r}))', USD4)
    calc(su, f"I{r}", f'=IF(OR(A{r}="",G{r}=""),"",IF(G{r}<=N(H{r}),"Reorder","OK"))')
ex = [("Olive oil (pomace)", "Oil", 1, "kg", 9.49, 3, 1, ""),
      ("Coconut oil 76F", "Oil", 7, "lb", 19.99, 5, 2, ""),
      ("Shea butter (unrefined)", "Butter", 2, "lb", 15.99, 1.5, 1, ""),
      ("Castor oil", "Oil", 32, "oz", 12.99, 20, 8, ""),
      ("Sweet almond oil", "Oil", 32, "oz", 15.49, 24, 8, ""),
      ("Sodium hydroxide (lye)", "Lye", 2, "lb", 13.99, 1.5, 1, "Store sealed, away from children"),
      ("Distilled water", "Liquid", 128, "oz", 1.49, 200, 64, ""),
      ("Goat milk (frozen)", "Liquid", 32, "oz", 5.99, 16, 10, ""),
      ("Fragrance: Lavender Fields", "Fragrance", 16, "oz", 21.99, 10, 4, "Skin-safe, check IFRA max"),
      ("Essential oil: Tea tree", "Essential oil", 4, "oz", 12.99, 3, 2, ""),
      ("Colloidal oatmeal", "Additive", 16, "oz", 8.99, 12, 4, ""),
      ("Activated charcoal", "Colour", 4, "oz", 6.99, 3, 1, ""),
      ("Goat milk melt & pour base", "M&P base", 2, "lb", 14.99, 4, 2, ""),
      ("Kraft soap wrap / band", "Wrap", 100, "each", 9.99, 120, 40, ""),
      ("Waterproof label", "Label", 120, "each", 12.99, 180, 50, ""),
      ("Shrink bag", "Wrap", 100, "each", 6.99, 60, 40, "For melt & pour"),
      ("Gift box (single bar)", "Box", 25, "each", 13.99, 15, 25, "")]
for i, row in enumerate(ex):
    for j, v in enumerate(row): su.cell(6 + i, [1, 2, 3, 4, 5, 7, 8, 10][j]).value = v
dv_list(su, f"B6:B{NS}", TYPES); dv_list(su, f"D6:D{NS}", "=Settings!$A$19:$A$23")
su.conditional_formatting.add(f"I6:I{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=PatternFill("solid", fgColor="F8D7D3"), font=Font(name=F, bold=True, color="A12A1E")))
SNAME, STYPE, SCOST, SHAND, SOZ = (f"Supplies!${c}$6:${c}${NS}" for c in "ABFGK")

# ---------- Recipes (ingredient lines) ----------
rc = wb.create_sheet("Recipes")
banner(rc, t, "Recipes", "One line per ingredient. Type the same recipe name on each of its lines. Amounts are per batch.", 11)
header(rc, 5, ["Recipe name", "Ingredient", "Amount per batch", "Unit", "Type", "Amount (oz)", "% of oils", "Cost per oz", "Line cost", "Notes", "planner #"], t)
widths(rc, {"A": 26, "B": 30, "C": 12, "D": 8, "E": 13, "F": 11, "G": 10, "H": 11, "I": 11, "J": 30, "K": 9}); rc.freeze_panes = "C6"
label(rc, "A4", "% of oils = this oil or butter as a share of all oils and butters in the recipe. Lye and water: enter the amounts from your lye calculator.", italic=True, size=9, color=GREY)
for r in range(6, NR + 1):
    for col in "ABCDJ": inp(rc, f"{col}{r}")
    for col in "ABJ": rc[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    rc[f"C{r}"].number_format = "#,##0.00"
    on = f'OR(A{r}="",B{r}="")'
    calc(rc, f"E{r}", f'=IF({on},"",IFERROR(INDEX({STYPE},MATCH(B{r},{SNAME},0)),"not in Supplies"))')
    calc(rc, f"F{r}", f'=IF(OR({on},C{r}=""),"",C{r}*IFERROR(VLOOKUP(IF(D{r}="","oz",D{r}),{UL},2,FALSE),1))', "#,##0.00")
    calc(rc, f"G{r}", f'=IF(OR(F{r}="",AND(E{r}<>"Oil",E{r}<>"Butter")),"",F{r}/(SUMIFS($F$6:$F${NR},$A$6:$A${NR},A{r},$E$6:$E${NR},"Oil")+SUMIFS($F$6:$F${NR},$A$6:$A${NR},A{r},$E$6:$E${NR},"Butter")))', "0.0%")
    calc(rc, f"H{r}", f'=IF({on},"",IFERROR(INDEX({SCOST},MATCH(B{r},{SNAME},0)),""))', USD4)
    calc(rc, f"I{r}", f'=IF(OR(F{r}="",H{r}=""),"",F{r}*H{r})', USD)
    rc[f"K{r}"] = f"=IF(A{r}='Batch Planner'!$B$4,COUNTIF($A$6:A{r},'Batch Planner'!$B$4),\"\")"
    rc[f"K{r}"].font = Font(name=F, size=9, color="9A8F86")
recipes = [("Lavender Fields (cold process)", [("Olive oil (pomace)", 13.6, "oz"), ("Coconut oil 76F", 9.6, "oz"), ("Shea butter (unrefined)", 6.4, "oz"), ("Castor oil", 2.4, "oz"),
            ("Sodium hydroxide (lye)", 4.48, "oz", "From my lye calculator, 5% superfat"), ("Distilled water", 9, "oz", "From my lye calculator"), ("Fragrance: Lavender Fields", 1.5, "oz")]),
           ("Oatmeal Goat Milk (cold process)", [("Olive oil (pomace)", 400, "g"), ("Coconut oil 76F", 270, "g"), ("Shea butter (unrefined)", 135, "g"), ("Sweet almond oil", 90, "g"),
            ("Sodium hydroxide (lye)", 127, "g", "From my lye calculator"), ("Goat milk (frozen)", 255, "g", "Freeze in cubes first"), ("Colloidal oatmeal", 15, "g")]),
           ("Charcoal Tea Tree (cold process)", [("Olive oil (pomace)", 12, "oz"), ("Coconut oil 76F", 10, "oz"), ("Shea butter (unrefined)", 4, "oz"), ("Castor oil", 2, "oz"),
            ("Sodium hydroxide (lye)", 4.2, "oz", "From my lye calculator"), ("Distilled water", 8.4, "oz"), ("Essential oil: Tea tree", 0.9, "oz"), ("Activated charcoal", 0.3, "oz")]),
           ("Goat Milk Melt & Pour", [("Goat milk melt & pour base", 2, "lb"), ("Fragrance: Lavender Fields", 0.8, "oz")])]
r = 6
for name, lines in recipes:
    for ln in lines:
        rc[f"A{r}"] = name; rc[f"B{r}"] = ln[0]; rc[f"C{r}"] = ln[1]; rc[f"D{r}"] = ln[2]
        if len(ln) > 3: rc[f"J{r}"] = ln[3]
        r += 1
dv_list(rc, f"B6:B{NR}", f"=Supplies!$A$6:$A${NS}"); dv_list(rc, f"D6:D{NR}", "=Settings!$A$19:$A$22")
rc.conditional_formatting.add(f"E6:E{NR}", CellIsRule(operator="equal", formula=['"not in Supplies"'], font=Font(name=F, bold=True, color="C00000")))
RNAME, RTYPE, ROZ, RCOST, RNUM, RING = (f"Recipes!${c}$6:${c}${NR}" for c in "AEFIKB")

def cost_of(ref):
    return f'IF({ref}="",0,IFERROR(INDEX({SCOST},MATCH({ref},{SNAME},0)),0))'

# ---------- Soap pricing ----------
sp = wb.create_sheet("Soap Pricing")
banner(sp, t, "Soap costing & pricing", "One row per soap. Type the recipe name exactly as on the Recipes tab.", 20)
cols = ["Soap (recipe name)", "Bars per batch", "Wrap / band", "Label", "Box / extras", "Labour per batch (min)",
        "Batch weight (oz)", "Ingredients per batch", "Ingredients per bar", "Packaging per bar", "Labour per bar", "Overheads per bar",
        "COST PER BAR", "Wholesale price", "Retail price", "Etsy fees (est.)", "Profit per retail sale", "Margin", "Bars made", "Bars in stock"]
header(sp, 5, cols, t); sp.row_dimensions[5].height = 44
for i, w in enumerate([32, 9, 20, 18, 18, 11, 10, 12, 11, 11, 10, 10, 12, 12, 11, 11, 13, 9, 9, 10]):
    sp.column_dimensions[chr(65 + i)].width = w
sp.freeze_panes = "B6"
label(sp, "A4", "Batch weight and ingredient cost come from the Recipes tab. Bars made / in stock come from Batches & Cure and Sales.", italic=True, size=9, color=GREY)
for r in range(6, NP + 1):
    for col in "ABCDEF": inp(sp, f"{col}{r}")
    for col in "ACDE": sp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    on = f'A{r}=""'
    calc(sp, f"G{r}", f'=IF({on},"",SUMIFS({ROZ},{RNAME},A{r}))', "#,##0.0")
    calc(sp, f"H{r}", f'=IF({on},"",SUMIFS({RCOST},{RNAME},A{r}))', USD)
    calc(sp, f"I{r}", f'=IF(OR({on},N(B{r})=0),"",H{r}/B{r})', USD)
    calc(sp, f"J{r}", f'=IF({on},"",{cost_of(f"C{r}")}+{cost_of(f"D{r}")}+{cost_of(f"E{r}")})', USD)
    calc(sp, f"K{r}", f'=IF(OR({on},N(B{r})=0),"",N(F{r})/60*{RATE}/B{r})', USD)
    calc(sp, f"L{r}", f'=IF(I{r}="","",(I{r}+J{r})*{OVH})', USD)
    calc(sp, f"M{r}", f'=IF(I{r}="","",I{r}+J{r}+K{r}+L{r})', USD, bold=True)
    calc(sp, f"N{r}", f'=IF(M{r}="","",CEILING(M{r}*{WMUL},{RND}))', USD, bold=True)
    calc(sp, f"O{r}", f'=IF(M{r}="","",CEILING(N{r}*{RMUL},{RND}))', USD, bold=True)
    calc(sp, f"P{r}", f'=IF(M{r}="","",O{r}*({ETX}+{PPC})+{PFX}+{LST})', USD)
    calc(sp, f"Q{r}", f'=IF(M{r}="","",O{r}-M{r}-P{r})', USD, bold=True)
    calc(sp, f"R{r}", f'=IF(OR(Q{r}="",N(O{r})=0),"",Q{r}/O{r})', "0%")
    calc(sp, f"S{r}", f"=IF({on},\"\",SUMIFS('Batches & Cure'!$D$6:$D${NB},'Batches & Cure'!$B$6:$B${NB},A{r}))", "#,##0")
    calc(sp, f"T{r}", f'=IF({on},"",S{r}-SUMIFS(Sales!$D$6:$D${NSALE},Sales!$C$6:$C${NSALE},A{r}))', "#,##0")
soaps = [("Lavender Fields (cold process)", 10, "Kraft soap wrap / band", "Waterproof label", None, 60),
         ("Oatmeal Goat Milk (cold process)", 10, "Kraft soap wrap / band", "Waterproof label", "Gift box (single bar)", 75),
         ("Charcoal Tea Tree (cold process)", 9, "Kraft soap wrap / band", "Waterproof label", None, 60),
         ("Goat Milk Melt & Pour", 8, "Shrink bag", "Waterproof label", None, 25)]
for i, row in enumerate(soaps):
    for j, v in enumerate(row):
        if v is not None: sp.cell(6 + i, 1 + j).value = v
dv_list(sp, f"C6:E{NP}", f"=Supplies!$A$6:$A${NS}")
sp.conditional_formatting.add(f"Q6:Q{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
sp.conditional_formatting.add(f"T6:T{NP}", CellIsRule(operator="lessThan", formula=["5"], fill=PatternFill("solid", fgColor="FCEBC8")))
legend(sp, NP + 2, 1)
PNAME, PCOST, PBARS = (f"'Soap Pricing'!${c}$6:${c}${NP}" for c in "AMB")

# ---------- Batch planner ----------
bp = wb.create_sheet("Batch Planner")
banner(bp, t, "Batch planner", "Pick a soap and how many bars you want. Weigh out exactly this much.", 7)
widths(bp, {"A": 30, "B": 32, "C": 14, "D": 14, "E": 14, "F": 15, "G": 14})
label(bp, "A4", "Soap", bold=True, size=12); inp(bp, "B4", "Lavender Fields (cold process)"); bp["B4"].alignment = Alignment(horizontal="left", indent=1)
dv_list(bp, "B4", "=" + PNAME)
label(bp, "A5", "Bars wanted", bold=True, size=12); inp(bp, "B5", 30, "0")
label(bp, "A6", "Batch size multiplier", size=11)
calc(bp, "B6", f'=IFERROR(B5/INDEX({PBARS},MATCH(B4,{PNAME},0)),"")', '0.00"x"', bold=True)
header(bp, 8, ["#", "Ingredient", "Per batch (oz)", "Total (oz)", "Total (g)", "On hand (oz)", "Enough?"], t)
for k in range(1, 16):
    r = 8 + k; bp[f"A{r}"] = k; bp[f"A{r}"].font = Font(name=F, size=10, color=GREY); bp[f"A{r}"].alignment = Alignment(horizontal="center")
    bp[f"H{r}"] = f'=IFERROR(MATCH(A{r},{RNUM},0),"")'; bp[f"H{r}"].font = Font(name=F, size=8, color="FFFFFF")
    calc(bp, f"B{r}", f'=IF(H{r}="","",INDEX({RING},H{r}))'); bp[f"B{r}"].alignment = Alignment(horizontal="left", indent=1)
    calc(bp, f"C{r}", f'=IF(H{r}="","",INDEX({ROZ},H{r}))', "#,##0.00")
    calc(bp, f"D{r}", f'=IF(OR(C{r}="",$B$6=""),"",C{r}*$B$6*(1+{SPILL}))', "#,##0.00")
    calc(bp, f"E{r}", f'=IF(D{r}="","",D{r}*28.3495)', "#,##0")
    calc(bp, f"F{r}", f'=IF(B{r}="","",IFERROR(INDEX({SHAND},MATCH(B{r},{SNAME},0))*INDEX({SOZ},MATCH(B{r},{SNAME},0)),""))', "#,##0.0")
    calc(bp, f"G{r}", f'=IF(OR(D{r}="",F{r}=""),"",IF(F{r}>=D{r},"Yes","Short "&TEXT(D{r}-F{r},"0.0")&" oz"))')
bp.conditional_formatting.add("G9:G23", FormulaRule(formula=['LEFT(G9,5)="Short"'], fill=PatternFill("solid", fgColor="F8D7D3"), font=Font(name=F, bold=True, color="A12A1E")))
bp.conditional_formatting.add("G9:G23", CellIsRule(operator="equal", formula=['"Yes"'], fill=PatternFill("solid", fgColor="E3F0E1"), font=Font(name=F, bold=True, color="2E6B3A")))
label(bp, "A25", "Batch summary", bold=True, size=13)
summ = [("Total weight to weigh out (oz)", "=SUM(D9:D23)", "#,##0.0"), ("Total weight (lb)", "=SUM(D9:D23)/16", "0.00"),
        ("Cost of these bars", f'=IFERROR(INDEX({PCOST},MATCH(B4,{PNAME},0))*B5,"")', USD),
        ("Wholesale value", f"=IFERROR(INDEX('Soap Pricing'!$N$6:$N${NP},MATCH(B4,{PNAME},0))*B5,\"\")", USD),
        ("Retail value", f"=IFERROR(INDEX('Soap Pricing'!$O$6:$O${NP},MATCH(B4,{PNAME},0))*B5,\"\")", USD)]
for i, (a, f, fmt) in enumerate(summ):
    label(bp, f"A{26 + i}", a); calc(bp, f"B{26 + i}", f, fmt, bold=True)
label(bp, "A32", "Totals include the spill allowance from Settings. Lists up to 15 ingredients. If you change a recipe, re-check lye and water in your lye calculator.",
      italic=True, size=9, color=GREY)

# ---------- Batches & cure ----------
bc = wb.create_sheet("Batches & Cure")
banner(bc, t, "Batches & cure tracker", "Log every batch. Ready dates and status update every day.", 9)
header(bc, 5, ["Batch #", "Soap", "Date made", "Bars", "Cure (weeks)", "Ready date", "Days left", "Status", "Notes"], t)
widths(bc, {"A": 10, "B": 32, "C": 13, "D": 8, "E": 11, "F": 13, "G": 10, "H": 12, "I": 30}); bc.freeze_panes = "A6"
for r in range(6, NB + 1):
    for col in "ABCDEI": inp(bc, f"{col}{r}")
    for col in "BI": bc[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    bc[f"C{r}"].number_format = "dd mmm yyyy"
    calc(bc, f"F{r}", f'=IF(C{r}="","",C{r}+7*IF(E{r}="",{CURE},E{r}))', "dd mmm yyyy")
    calc(bc, f"G{r}", f'=IF(F{r}="","",MAX(0,F{r}-TODAY()))', "0")
    calc(bc, f"H{r}", f'=IF(F{r}="","",IF(TODAY()>=F{r},"Ready","Curing"))')
for i, (b, soap, back, bars, wk, note) in enumerate([("B-001", "Lavender Fields (cold process)", 40, 10, None, "Gelled, nice purple swirl"),
                                                     ("B-002", "Oatmeal Goat Milk (cold process)", 30, 10, 6, "Goat milk: longer cure"),
                                                     ("B-003", "Charcoal Tea Tree (cold process)", 12, 9, None, ""),
                                                     ("B-004", "Goat Milk Melt & Pour", 2, 8, 0, "Melt & pour: ready next day")]):
    r = 6 + i; bc[f"A{r}"] = b; bc[f"B{r}"] = soap; bc[f"C{r}"] = f"=TODAY()-{back}"; bc[f"D{r}"] = bars; bc[f"I{r}"] = note
    if wk is not None: bc[f"E{r}"] = wk
dv_list(bc, f"B6:B{NB}", "=" + PNAME)
bc.conditional_formatting.add(f"H6:H{NB}", CellIsRule(operator="equal", formula=['"Ready"'], fill=PatternFill("solid", fgColor="E3F0E1"), font=Font(name=F, bold=True, color="2E6B3A")))
bc.conditional_formatting.add(f"H6:H{NB}", CellIsRule(operator="equal", formula=['"Curing"'], fill=PatternFill("solid", fgColor="FCEBC8"), font=Font(name=F, bold=True, color="8A5A12")))

# ---------- Sales ----------
sa = wb.create_sheet("Sales")
banner(sa, t, "Sales log", "One row per sale. Cost comes from Soap Pricing, so profit is real.", 11)
header(sa, 5, ["Date", "Channel", "Soap", "Bars", "Price each", "Sale total", "Fees & shipping paid", "Cost of bars", "Profit", "Month", "Notes"], t)
widths(sa, {"A": 13, "B": 13, "C": 32, "D": 7, "E": 11, "F": 12, "G": 13, "H": 13, "I": 12, "J": 9, "K": 24}); sa.freeze_panes = "A6"
for r in range(6, NSALE + 1):
    for col in "ABCDEGK": inp(sa, f"{col}{r}")
    for col in "CK": sa[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sa[f"A{r}"].number_format = "dd mmm yyyy"; sa[f"E{r}"].number_format = USD; sa[f"G{r}"].number_format = USD
    calc(sa, f"F{r}", f'=IF(OR(D{r}="",E{r}=""),"",D{r}*E{r})', USD)
    calc(sa, f"H{r}", f'=IF(OR(C{r}="",D{r}=""),"",D{r}*IFERROR(INDEX({PCOST},MATCH(C{r},{PNAME},0)),0))', USD)
    calc(sa, f"I{r}", f'=IF(F{r}="","",F{r}-N(G{r})-N(H{r}))', USD)
    calc(sa, f"J{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(sa, f"B6:B{NSALE}", "Etsy,Market,Wholesale,Website,Instagram,Other")
dv_list(sa, f"C6:C{NSALE}", "=" + PNAME)
for i, (back, ch, soap, q, price, fees, note) in enumerate([(9, "Market", "Lavender Fields (cold process)", 3, 12, 0, "Saturday market"),
                                                          (6, "Etsy", "Oatmeal Goat Milk (cold process)", 2, None, "etsy", "Gift box"),
                                                          (3, "Wholesale", "Goat Milk Melt & Pour", 6, "w", 0, "Local gift shop"),
                                                          (1, "Market", "Charcoal Tea Tree (cold process)", 2, 12, 0, "")]):
    r = 6 + i; sa[f"A{r}"] = f"=TODAY()-{back}"; sa[f"B{r}"] = ch; sa[f"C{r}"] = soap; sa[f"D{r}"] = q; sa[f"K{r}"] = note
    sa[f"E{r}"] = price if isinstance(price, (int, float)) else (f"='Soap Pricing'!O7" if price is None else "='Soap Pricing'!N9")
    sa[f"G{r}"] = fees if fees != "etsy" else f"=ROUND(F{r}*({ETX}+{PPC})+{PFX}+{LST},2)"
SD, SCH, SC, SQ, ST, SG, SH, SPF = (f"Sales!${c}$6:${c}${NSALE}" for c in "ABCDFGHI")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Sales, Batches & Cure and Supplies.", 9)
widths(d, {"A": 26, "B": 14, "C": 14, "D": 14, "E": 14, "F": 4, "G": 32, "H": 12, "I": 14})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{SD},">="&DATE($B$4,1,1),{SD},"<"&DATE($B$4+1,1,1)'
kpi = [("Sales", f"=SUMIFS({ST},{yr})", USD), ("Profit", f"=SUMIFS({SPF},{yr})", USD), ("Bars sold", f"=SUMIFS({SQ},{yr})", "#,##0"),
       ("Profit margin", '=IF(B6=0,"",B7/B6)', "0%"),
       ("Bars curing now", f"=SUMIFS('Batches & Cure'!$D$6:$D${NB},'Batches & Cure'!$H$6:$H${NB},\"Curing\")", "#,##0"),
       ("Bars in stock (all soaps)", f"=SUM('Soap Pricing'!$T$6:$T${NP})", "#,##0"),
       ("Supplies to reorder", f'=COUNTIF(Supplies!$I$6:$I${NS},"Reorder")', "0")]
for i, (a, f, fmt) in enumerate(kpi):
    r = 6 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 28
header(d, 14, ["Month", "Sales", "Fees & shipping", "Cost", "Profit"], t)
for i, mn in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    r = 15 + i; label(d, f"A{r}", mn)
    mr = f'{SD},">="&DATE($B$4,{i + 1},1),{SD},"<"&DATE($B$4,{i + 2},1)'
    for col, rg in zip("BCDE", (ST, SG, SH, SPF)): calc(d, f"{col}{r}", f"=SUMIFS({rg},{mr})", USD)
label(d, "A27", "Total", bold=True)
for col in "BCDE": calc(d, f"{col}27", f"=SUM({col}15:{col}26)", USD, bold=True)
header(d, 14, ["Channel", "Sales", "Profit"], t, start=7)
for i, ch in enumerate(["Etsy", "Market", "Wholesale", "Website", "Instagram", "Other"]):
    r = 15 + i; label(d, f"G{r}", ch)
    calc(d, f"H{r}", f'=SUMIFS({ST},{SCH},G{r},{yr})', USD); calc(d, f"I{r}", f'=SUMIFS({SPF},{SCH},G{r},{yr})', USD)
header(d, 23, ["Soap", "Bars sold", "Profit"], t, start=7)
for i in range(12):
    r = 24 + i
    d[f"G{r}"] = f"=IF('Soap Pricing'!A{6 + i}=\"\",\"\",'Soap Pricing'!A{6 + i})"; d[f"G{r}"].font = Font(name=F, size=11)
    calc(d, f"H{r}", f'=IF(G{r}="","",SUMIFS({SQ},{SC},G{r},{yr}))', "#,##0")
    calc(d, f"I{r}", f'=IF(G{r}="","",SUMIFS({SPF},{SC},G{r},{yr}))', USD)
label(d, "G36", "Shows your first 12 soaps from Soap Pricing.", italic=True, size=9, color=GREY)

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
