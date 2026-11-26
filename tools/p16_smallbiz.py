"""Small Business Pricing, Inventory & Profit Spreadsheet (batch 9, lane a, the cheap all-in-one 'Bestseller-style' sheet asked for
on 26 Nov): any maker or reseller. Materials library with cost per unit, product costing (up to 4 materials + packaging + labour +
overheads), suggested price at your target margin AFTER Etsy fees, wholesale price, your own price with profit/margin check,
channel fee table, stock in log + inventory with low-stock flags, sales log with fees by channel, expenses, dashboard with chart.
Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter as gl
from openpyxl.chart import BarChart, Reference

t = Theme("1F2A44", "2F8F8A", "E3F1EF")
wb = Workbook()
NM, NP, NI, NSALE, NE = 155, 105, 406, 1506, 306
USD, USD4 = '"$"#,##0.00', '"$"#,##0.000'
GREY = "6A6F7D"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")
REDF = Font(name=F, bold=True, color="A12A1E"); AMBF = Font(name=F, bold=True, color="8A5A12"); GRNF = Font(name=F, bold=True, color="2E6B3A")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Small Business Pricing, Inventory & Profit", "Know what every product costs, what to charge after fees, what's in stock and what you really made.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly rate, target profit margin, overheads and the fees each place you sell takes (Etsy, your website, markets...).",
         "Materials: add each supply once with the pack size and pack price. The cost per unit (per bead, yard, gram, sheet) is worked out.",
         "Product Pricing: one row per product. Pick up to 4 materials and how much each uses, add packaging and your minutes. "
         "Total cost, a SUGGESTED PRICE that hits your margin after Etsy fees, and a wholesale price appear. Type your own price to see your real profit.",
         "Stock In: log every batch you make or buy in. Inventory shows what's on hand for every product, its value and what to make or reorder.",
         "Sales: one row per sale. Price, fees for that channel, cost and profit fill in. Expenses: tools, ads, subscriptions, market fees.",
         "Dashboard: pick a year to see sales, fees, profit after expenses, margin, a month-by-month chart, best sellers and low stock."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 46 if i == 2 else 34
legend(s, 12, 2)
label(s, "B14", "Profit margin = profit / price. A 40% margin on a $20 item means $8 is left after materials, your time, overheads and fees. "
      "The suggested price includes the fee so the margin is what you really keep.", size=10, color="2E6B6A")
s.row_dimensions[14].height = 44
label(s, "B15", "Works for any handmade or small product business: jewelry, candles, crochet, stickers, prints, soap, bags, baked goods, resale.", size=10)
label(s, "B16", "Example materials, products, stock and sales are included so you can see how it works: type over them or delete them. "
      "Fee rates are estimates: check the current fees for your country. Works in Excel and Google Sheets.", italic=True, size=10)
s.row_dimensions[16].height = 30

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates and fees. Every product and sale uses these.", 5)
widths(st, {"A": 40, "B": 16, "C": 16, "D": 4, "E": 60})
rows = [("Your hourly rate", 18, USD, "What your making, packing and listing time is worth."),
        ("Target profit margin", 0.40, "0%", "Share of the price you want to keep as profit after every cost and fee."),
        ("Overheads (% of materials)", 0.10, "0%", "Electricity, tools wearing out, test pieces, printer ink."),
        ("Wholesale price = cost x", 2, '0.0"x"', "Shops usually pay about half your retail price."),
        ("Round suggested prices to .99?", "Yes", None, "Yes: $18.99. No: rounds up to the nearest 5 cents.")]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"E{5 + i}", n, size=9, color=GREY, italic=True)
dv_list(st, "B9", "Yes,No")
RATE, MARG, OVH, WMUL, R99 = (f"Settings!$B${5 + i}" for i in range(5))
label(st, "A11", "Fees by sales channel", bold=True, size=12)
header(st, 12, ["Channel", "% of order", "Fixed per order"], t)
CH = [("Etsy", 0.095, 0.45, "6.5% transaction + about 3% + $0.25 payment processing + $0.20 listing. Add offsite ads if you pay them."),
      ("Website", 0.029, 0.30, "Card processing on Shopify, Squarespace, Stripe, PayPal."),
      ("Market / craft fair", 0.026, 0.15, "Card reader (Square, SumUp). Booth fees go in Expenses."),
      ("Instagram / Facebook", 0.029, 0.30, "Card or PayPal payments."),
      ("Wholesale", 0, 0, "Invoice paid by bank transfer."),
      ("Other", 0, 0, "")]
for i, (c, p_, fx, n) in enumerate(CH):
    r = 13 + i; inp(st, f"A{r}", c).alignment = Alignment(horizontal="left", indent=1); inp(st, f"B{r}", p_, "0.0%"); inp(st, f"C{r}", fx, USD)
    label(st, f"E{r}", n, size=9, color=GREY, italic=True)
CHN, CHP, CHF = "Settings!$A$13:$A$18", "Settings!$B$13:$B$18", "Settings!$C$13:$C$18"
EPCT, EFIX = "Settings!$B$13", "Settings!$C$13"
label(st, "A20", "Suggested prices use the Etsy row so the margin holds on your highest-fee channel.", italic=True, size=9, color=GREY)
UNITS = "each,yard,metre,gram,ounce,sheet,ml,inch,foot,pack,hour"
CATS = "Material,Component,Packaging,Bought in (resale),Shipping supply,Other"

# ---------- Materials ----------
m = wb.create_sheet("Materials")
banner(m, t, "Materials & supplies", "Add each supply once. Cost per unit is worked out for you.", 10)
header(m, 5, ["Material / supply", "Category", "Unit", "Pack size (units)", "Pack price", "COST PER UNIT", "In stock (units)", "Reorder at", "Status", "Supplier / notes"], t)
m.row_dimensions[5].height = 44
widths(m, {"A": 34, "B": 17, "C": 9, "D": 11, "E": 11, "F": 12, "G": 11, "H": 10, "I": 11, "J": 28}); m.freeze_panes = "B6"
for r in range(6, NM + 1):
    for col in "ABCDEGHJ": inp(m, f"{col}{r}")
    for col in "AJ": m[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    m[f"E{r}"].number_format = USD
    for col in "DGH": m[f"{col}{r}"].number_format = "#,##0.##"
    calc(m, f"F{r}", f'=IF(OR(A{r}="",N(D{r})=0,E{r}=""),"",E{r}/D{r})', USD4, bold=True)
    calc(m, f"I{r}", f'=IF(OR(A{r}="",G{r}=""),"",IF(G{r}<=N(H{r}),"Reorder","OK"))')
ex = [("Soy wax (10 lb bag)", "Material", "ounce", 160, 32.99, 96, 40, ""),
      ("Fragrance oil", "Material", "ounce", 16, 18.50, 30, 8, "1 oz per 10 oz of wax"),
      ("Amber jar 8 oz with lid", "Component", "each", 24, 29.99, 40, 12, ""),
      ("Cotton wick", "Component", "each", 100, 8.99, 120, 30, ""),
      ("Sterling silver chain 18 in", "Component", "each", 10, 24.00, 14, 5, ""),
      ("Gemstone bead 6 mm", "Material", "each", 60, 9.50, 140, 40, "Moonstone strand"),
      ("Jump rings + clasp set", "Component", "each", 50, 7.99, 46, 15, ""),
      ("Gift box with insert", "Packaging", "each", 50, 21.00, 18, 20, ""),
      ("Kraft label 2 in", "Packaging", "each", 250, 11.99, 200, 50, "Printed at home"),
      ("Tote bag blank (canvas)", "Bought in (resale)", "each", 12, 38.00, 9, 6, ""),
      ("Screen print ink", "Material", "ml", 250, 16.00, 180, 60, ""),
      ("Padded mailer 6 x 9", "Shipping supply", "each", 100, 14.99, 64, 25, "")]
for i, row in enumerate(ex):
    for j, v in enumerate(row):
        if v is not None and v != "": m.cell(6 + i, [1, 2, 3, 4, 5, 7, 8, 10][j]).value = v
dv_list(m, f"B6:B{NM}", CATS); dv_list(m, f"C6:C{NM}", UNITS)
m.conditional_formatting.add(f"I6:I{NM}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=red, font=REDF))
MNAME, MCOST = f"Materials!$A$6:$A${NM}", f"Materials!$F$6:$F${NM}"
MLIST = "=" + MNAME
def mc(ref): return f'IF({ref}="",0,IFERROR(INDEX({MCOST},MATCH({ref},{MNAME},0)),0))'

# ---------- Product Pricing ----------
pp = wb.create_sheet("Product Pricing")
banner(pp, t, "Product costing & pricing", "One row per product: what it costs to make, what to charge after fees, and what you keep.", 24)
cols = ["Product", "SKU", "Material 1", "Qty", "Material 2", "Qty", "Material 3", "Qty", "Material 4", "Qty", "Other cost (each)", "Minutes to make + pack",
        "Materials", "Labour", "Overheads", "TOTAL COST", "SUGGESTED PRICE (target margin after Etsy fees)", "Wholesale price", "YOUR PRICE (blank = suggested)",
        "Etsy fees at your price", "PROFIT per sale", "Margin", "Profit per hour", "Price check"]
header(pp, 5, cols, t); pp.row_dimensions[5].height = 70
for i, w in enumerate([30, 9, 26, 6, 26, 6, 22, 6, 22, 6, 10, 10, 11, 10, 10, 11, 14, 11, 12, 10, 11, 8, 10, 13]): pp.column_dimensions[gl(i + 1)].width = w
pp.freeze_panes = "B6"
label(pp, "A4", "Qty = how many units of that material one product uses (ounces of wax, beads, yards). 'Other cost' = anything not in Materials (a print you order, a charm).",
      italic=True, size=9, color=GREY)
for r in range(6, NP + 1):
    for col in "ABCDEFGHIJKLS": inp(pp, f"{col}{r}")
    for col in "ACEGI": pp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    pp[f"K{r}"].number_format = USD; pp[f"S{r}"].number_format = USD
    on = f'A{r}=""'
    mat = "+".join(f"{mc(gl(c) + str(r))}*N({gl(c + 1)}{r})" for c in (3, 5, 7, 9))
    calc(pp, f"M{r}", f'=IF({on},"",{mat}+N(K{r}))', USD)
    calc(pp, f"N{r}", f'=IF({on},"",N(L{r})/60*{RATE})', USD)
    calc(pp, f"O{r}", f'=IF({on},"",M{r}*{OVH})', USD)
    calc(pp, f"P{r}", f'=IF({on},"",M{r}+N{r}+O{r})', USD, bold=True)
    raw = f'(P{r}+{EFIX})/MAX(0.05,1-{EPCT}-{MARG})'
    calc(pp, f"Q{r}", f'=IF({on},"",IF({R99}="Yes",CEILING({raw}+0.01,1)-0.01,CEILING({raw},0.05)))', USD, bold=True)
    calc(pp, f"R{r}", f'=IF({on},"",CEILING(P{r}*{WMUL},0.05))', USD)
    pr_ = f'IF(S{r}="",Q{r},S{r})'
    calc(pp, f"T{r}", f'=IF({on},"",{pr_}*{EPCT}+{EFIX})', USD)
    calc(pp, f"U{r}", f'=IF({on},"",{pr_}-P{r}-T{r})', USD, bold=True)
    calc(pp, f"V{r}", f'=IF({on},"",IF({pr_}=0,"",U{r}/{pr_}))', "0%")
    calc(pp, f"W{r}", f'=IF(OR({on},N(L{r})=0),"",(U{r}+N{r})/(L{r}/60))', USD)
    calc(pp, f"X{r}", f'=IF({on},"",IF(U{r}<0,"Losing money",IF(V{r}<{MARG}-0.05,"Below target","On target")))')
CA, JR, AM, BX, LB, MA = "Soy wax (10 lb bag)", "Amber jar 8 oz with lid", "Fragrance oil", "Gift box with insert", "Kraft label 2 in", "Padded mailer 6 x 9"
prods = [("Amber jar soy candle 8 oz", "CN-08", CA, 7, AM, 0.7, JR, 1, "Cotton wick", 1, None, 12, None),
         ("Candle gift set of 3", "CN-SET", CA, 21, AM, 2.1, JR, 3, BX, 1, 1.20, 40, 64),
         ("Moonstone bead necklace", "JW-01", "Gemstone bead 6 mm", 9, "Sterling silver chain 18 in", 1, "Jump rings + clasp set", 1, BX, 1, None, 25, None),
         ("Moonstone stud earrings", "JW-02", "Gemstone bead 6 mm", 2, "Jump rings + clasp set", 1, BX, 1, None, None, 3.10, 15, 24),
         ("Screen printed tote bag", "TB-01", "Tote bag blank (canvas)", 1, "Screen print ink", 12, LB, 1, MA, 1, None, 14, None),
         ("Wax melts pack of 6", "WM-06", CA, 3, AM, 0.3, LB, 1, None, None, 0.35, 8, 8.5)]
for i, row in enumerate(prods):
    for j, v in enumerate(row):
        if v is not None: pp.cell(6 + i, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19][j]).value = v
for col in "CEGI": dv_list(pp, f"{col}6:{col}{NP}", MLIST)
for val, fill, f_ in (('"Losing money"', red, REDF), ('"Below target"', amb, AMBF), ('"On target"', grn, GRNF)):
    pp.conditional_formatting.add(f"X6:X{NP}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
pp.conditional_formatting.add(f"U6:U{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
legend(pp, NP + 2, 1)
PCOL = lambda c: f"'Product Pricing'!${c}$6:${c}${NP}"
PNAME, PCOST, PPRICE, PSUG, PWH = PCOL("A"), PCOL("P"), PCOL("S"), PCOL("Q"), PCOL("R")
PLIST = "=" + PNAME
def listprice(ref): return f'IFERROR(IF(INDEX({PPRICE},MATCH({ref},{PNAME},0))="",INDEX({PSUG},MATCH({ref},{PNAME},0)),INDEX({PPRICE},MATCH({ref},{PNAME},0))),0)'

# ---------- Stock In ----------
si = wb.create_sheet("Stock In")
banner(si, t, "Stock in", "Log every batch you make or buy in. Inventory adds these up.", 6)
header(si, 5, ["Date", "Product", "Quantity", "Cost of batch", "Month", "Notes"], t)
widths(si, {"A": 13, "B": 32, "C": 10, "D": 13, "E": 8, "F": 32}); si.freeze_panes = "A6"
for r in range(6, NI + 1):
    for col in "ABCF": inp(si, f"{col}{r}")
    for col in "BF": si[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    si[f"A{r}"].number_format = "dd mmm yyyy"
    calc(si, f"D{r}", f'=IF(OR(B{r}="",C{r}=""),"",C{r}*IFERROR(INDEX({PCOST},MATCH(B{r},{PNAME},0)),0))', USD)
    calc(si, f"E{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(si, f"B6:B{NI}", PLIST)
batches = [(-60, "Amber jar soy candle 8 oz", 24, "Autumn scents"), (-55, "Moonstone bead necklace", 10, ""), (-50, "Screen printed tote bag", 12, ""),
           (-41, "Wax melts pack of 6", 30, ""), (-35, "Candle gift set of 3", 8, "Holiday sets"), (-30, "Moonstone stud earrings", 15, ""),
           (-18, "Amber jar soy candle 8 oz", 24, "Restock"), (-9, "Candle gift set of 3", 10, "Restock")]
for i, (dd, p, q, n) in enumerate(batches):
    r = 6 + i; si[f"A{r}"] = f"=TODAY(){dd:+d}"; si[f"B{r}"] = p; si[f"C{r}"] = q; si[f"F{r}"] = n
IP, IQ = (f"'Stock In'!${c}$6:${c}${NI}" for c in "BC")

# ---------- Sales ----------
sa = wb.create_sheet("Sales")
banner(sa, t, "Sales log", "One row per sale. Blank price = your price from Product Pricing. Fees come from the channel table in Settings.", 13)
header(sa, 5, ["Date", "Channel", "Product", "Qty", "Price each (blank = list)", "Shipping charged", "Postage paid", "Discount / ads / other",
               "Sale total", "Fees", "Cost of goods", "PROFIT", "Month"], t)
sa.row_dimensions[5].height = 44
widths(sa, {"A": 13, "B": 18, "C": 30, "D": 6, "E": 11, "F": 10, "G": 10, "H": 11, "I": 11, "J": 9, "K": 11, "L": 11, "M": 7}); sa.freeze_panes = "A6"
for r in range(6, NSALE + 1):
    for col in "ABCDEFGH": inp(sa, f"{col}{r}")
    sa[f"C{r}"].alignment = Alignment(horizontal="left", indent=1); sa[f"B{r}"].alignment = Alignment(horizontal="left", indent=1)
    sa[f"A{r}"].number_format = "dd mmm yyyy"
    for col in "EFGH": sa[f"{col}{r}"].number_format = USD
    on = f'OR(C{r}="",D{r}="")'
    calc(sa, f"I{r}", f'=IF({on},"",D{r}*IF(E{r}="",{listprice(f"C{r}")},E{r}))', USD)
    calc(sa, f"J{r}", f'=IF({on},"",ROUND((I{r}+N(F{r}))*IFERROR(INDEX({CHP},MATCH(B{r},{CHN},0)),0)+IFERROR(INDEX({CHF},MATCH(B{r},{CHN},0)),0),2))', USD)
    calc(sa, f"K{r}", f'=IF({on},"",D{r}*IFERROR(INDEX({PCOST},MATCH(C{r},{PNAME},0)),0))', USD)
    calc(sa, f"L{r}", f'=IF({on},"",I{r}+N(F{r})-N(G{r})-N(H{r})-J{r}-K{r})', USD, bold=True)
    calc(sa, f"M{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(sa, f"B6:B{NSALE}", "=" + CHN); dv_list(sa, f"C6:C{NSALE}", PLIST)
sa.conditional_formatting.add(f"L6:L{NSALE}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
sales = [(52, "Etsy", "Amber jar soy candle 8 oz", 2, None, 5.95, 5.40, None), (47, "Etsy", "Moonstone bead necklace", 1, None, 4.50, 4.10, None),
         (44, "Market / craft fair", "Amber jar soy candle 8 oz", 6, 22, None, None, None), (44, "Market / craft fair", "Wax melts pack of 6", 9, None, None, None, None),
         (44, "Market / craft fair", "Screen printed tote bag", 4, None, None, None, None), (38, "Website", "Moonstone stud earrings", 2, None, 4.00, 3.80, 2.40),
         (31, "Etsy", "Candle gift set of 3", 1, None, 7.95, 7.10, None), (27, "Wholesale", "Amber jar soy candle 8 oz", 12, 11.50, None, 16.00, None),
         (22, "Instagram / Facebook", "Moonstone bead necklace", 1, None, 4.50, 4.10, None), (16, "Etsy", "Candle gift set of 3", 2, None, 7.95, 8.40, 6.30),
         (12, "Market / craft fair", "Candle gift set of 3", 3, None, None, None, None), (12, "Market / craft fair", "Moonstone stud earrings", 5, None, None, None, None),
         (6, "Etsy", "Wax melts pack of 6", 3, None, 4.95, 4.60, None), (2, "Etsy", "Moonstone bead necklace", 1, None, 4.50, 4.10, None)]
for i, (back, ch, p, q, price, shc, post, oth) in enumerate(sales):
    r = 6 + i; sa[f"A{r}"] = f"=TODAY()-{back}"; sa[f"B{r}"] = ch; sa[f"C{r}"] = p; sa[f"D{r}"] = q
    for col, v in zip("EFGH", (price, shc, post, oth)):
        if v is not None: sa[f"{col}{r}"] = v
SD, SCH, SC, SQ, SI, SF, SPF = (f"Sales!${c}$6:${c}${NSALE}" for c in "ABCDIJL")
SSH, SPO, SOT, SK = (f"Sales!${c}$6:${c}${NSALE}" for c in "FGHK")

# ---------- Expenses ----------
ex_ = wb.create_sheet("Expenses")
banner(ex_, t, "Expenses", "Costs that aren't part of one product: tools, booth fees, ads, software, photo props.", 5)
header(ex_, 5, ["Date", "Category", "What for", "Amount", "Month"], t)
widths(ex_, {"A": 13, "B": 20, "C": 40, "D": 12, "E": 8}); ex_.freeze_panes = "A6"
for r in range(6, NE + 1):
    for col in "ABCD": inp(ex_, f"{col}{r}")
    for col in "BC": ex_[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    ex_[f"A{r}"].number_format = "dd mmm yyyy"; ex_[f"D{r}"].number_format = USD
    calc(ex_, f"E{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
ECATS = "Tools & equipment,Booth / market fee,Advertising,Software & subscriptions,Photography,Shipping supplies,Training,Other"
dv_list(ex_, f"B6:B{NE}", ECATS)
for i, (back, c, w, a) in enumerate([(58, "Software & subscriptions", "Canva Pro (monthly)", 14.99), (44, "Booth / market fee", "Autumn craft fair table", 45),
                                      (30, "Advertising", "Etsy Ads", 12.40), (28, "Software & subscriptions", "Canva Pro (monthly)", 14.99),
                                      (12, "Booth / market fee", "Holiday market table", 60), (5, "Tools & equipment", "Pouring pitcher + thermometer", 18.50)]):
    r = 6 + i; ex_[f"A{r}"] = f"=TODAY()-{back}"; ex_[f"B{r}"] = c; ex_[f"C{r}"] = w; ex_[f"D{r}"] = a
ED, EA = f"Expenses!$A$6:$A${NE}", f"Expenses!$D$6:$D${NE}"

# ---------- Inventory ----------
iv = wb.create_sheet("Inventory")
banner(iv, t, "Inventory", "Stock for every product: opening stock + made / bought in - sold - damaged.", 10)
header(iv, 5, ["Product", "Opening stock", "Stock in", "Sold", "Damaged / gifted", "ON HAND", "Make / reorder at", "Status", "Value at cost", "Value at your price"], t)
iv.row_dimensions[5].height = 44
widths(iv, {"A": 32, "B": 10, "C": 10, "D": 9, "E": 10, "F": 10, "G": 11, "H": 13, "I": 12, "J": 13}); iv.freeze_panes = "B6"
for i in range(NP - 5):
    r = 6 + i
    iv[f"A{r}"] = f"=IF('Product Pricing'!A{r}=\"\",\"\",'Product Pricing'!A{r})"; iv[f"A{r}"].font = Font(name=F, size=11)
    iv[f"A{r}"].alignment = Alignment(horizontal="left", indent=1)
    for col in "BEG": inp(iv, f"{col}{r}", None, "0")
    calc(iv, f"C{r}", f'=IF(A{r}="","",SUMIFS({IQ},{IP},A{r}))', "#,##0")
    calc(iv, f"D{r}", f'=IF(A{r}="","",SUMIFS({SQ},{SC},A{r}))', "#,##0")
    calc(iv, f"F{r}", f'=IF(A{r}="","",N(B{r})+C{r}-D{r}-N(E{r}))', "#,##0", bold=True)
    calc(iv, f"H{r}", f'=IF(A{r}="","",IF(F{r}<0,"Check counts",IF(F{r}=0,"Sold out",IF(F{r}<=N(G{r}),"Low stock","In stock"))))')
    calc(iv, f"I{r}", f"=IF(A{r}=\"\",\"\",MAX(0,F{r})*'Product Pricing'!P{r})", USD)
    calc(iv, f"J{r}", f"=IF(A{r}=\"\",\"\",MAX(0,F{r})*IF('Product Pricing'!S{r}=\"\",'Product Pricing'!Q{r},'Product Pricing'!S{r}))", USD)
for i, (o, dmg, at) in enumerate([(6, 1, 8), (0, 0, 12), (2, 0, 4), (0, 0, 3), (0, 1, 8), (4, 2, 10)]):
    iv[f"B{6 + i}"] = o; iv[f"E{6 + i}"] = dmg; iv[f"G{6 + i}"] = at
for val, fill, f_ in (('"Sold out"', red, REDF), ('"Check counts"', red, REDF), ('"Low stock"', amb, AMBF), ('"In stock"', grn, GRNF)):
    iv.conditional_formatting.add(f"H6:H{NP}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
label(iv, f"A{NP + 2}", "Products appear here automatically from Product Pricing. Opening stock = what you had when you started using this sheet.", italic=True, size=9, color=GREY)

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Sales, Expenses, Inventory and Materials.", 10)
widths(d, {"A": 28, "B": 15, "C": 13, "D": 13, "E": 13, "F": 13, "G": 3, "H": 30, "I": 12, "J": 13})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{SD},">="&DATE($B$4,1,1),{SD},"<"&DATE($B$4+1,1,1)'
ey = f'{ED},">="&DATE($B$4,1,1),{ED},"<"&DATE($B$4+1,1,1)'
kpi = [("Sales (incl. shipping)", f"=SUMIFS({SI},{yr})+SUMIFS({SSH},{yr})", USD),
       ("Fees, postage & discounts", f"=SUMIFS({SF},{yr})+SUMIFS({SPO},{yr})+SUMIFS({SOT},{yr})", USD),
       ("Cost of goods", f"=SUMIFS({SK},{yr})", USD),
       ("Profit from sales", f"=SUMIFS({SPF},{yr})", USD),
       ("Expenses", f"=SUMIFS({EA},{ey})", USD),
       ("NET PROFIT", "=B9-B10", USD),
       ("Net margin", '=IF(B6=0,"",B11/B6)', "0%"),
       ("Items sold", f"=SUMIFS({SQ},{yr})", "#,##0"),
       ("Orders", f'=COUNTIFS({SC},"<>",{yr})', "#,##0"),
       ("Average order", '=IF(B14=0,"",B6/B14)', USD),
       ("Stock value at cost", f"=SUM(Inventory!$I$6:$I${NP})", USD),
       ("Products low / sold out", f'=COUNTIF(Inventory!$H$6:$H${NP},"Low stock")+COUNTIF(Inventory!$H$6:$H${NP},"Sold out")', "0"),
       ("Materials to reorder", f'=COUNTIF(Materials!$I$6:$I${NM},"Reorder")', "0")]
for i, (a, f, fmt) in enumerate(kpi):
    r = 6 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 26
d["B11"].fill = PatternFill("solid", fgColor="D6EEE9")
header(d, 20, ["Month", "Sales", "Profit from sales", "Expenses", "Net profit", "Items sold"], t)
for i, mn in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    r = 21 + i; label(d, f"A{r}", mn)
    mr = f'{SD},">="&DATE($B$4,{i + 1},1),{SD},"<"&DATE($B$4,{i + 2},1)'
    me = f'{ED},">="&DATE($B$4,{i + 1},1),{ED},"<"&DATE($B$4,{i + 2},1)'
    calc(d, f"B{r}", f"=SUMIFS({SI},{mr})+SUMIFS({SSH},{mr})", USD); calc(d, f"C{r}", f"=SUMIFS({SPF},{mr})", USD)
    calc(d, f"D{r}", f"=SUMIFS({EA},{me})", USD); calc(d, f"E{r}", f"=C{r}-D{r}", USD, bold=True); calc(d, f"F{r}", f"=SUMIFS({SQ},{mr})", "#,##0")
label(d, "A33", "Total", bold=True)
for col in "BCDEF": calc(d, f"{col}33", f"=SUM({col}21:{col}32)", "#,##0" if col == "F" else USD, bold=True)
header(d, 5, ["Channel", "Sales", "Profit"], t, start=8)
for i in range(6):
    r = 6 + i; d[f"H{r}"] = f"=Settings!A{13 + i}"; d[f"H{r}"].font = Font(name=F, size=11)
    calc(d, f"I{r}", f'=SUMIFS({SI},{SCH},H{r},{yr})', USD); calc(d, f"J{r}", f'=SUMIFS({SPF},{SCH},H{r},{yr})', USD)
header(d, 13, ["Best sellers (first 15 products)", "Items sold", "Profit"], t, start=8)
for i in range(15):
    r = 14 + i
    d[f"H{r}"] = f"=IF('Product Pricing'!A{6 + i}=\"\",\"\",'Product Pricing'!A{6 + i})"; d[f"H{r}"].font = Font(name=F, size=11)
    calc(d, f"I{r}", f'=IF(H{r}="","",SUMIFS({SQ},{SC},H{r},{yr}))', "#,##0")
    calc(d, f"J{r}", f'=IF(H{r}="","",SUMIFS({SPF},{SC},H{r},{yr}))', USD)
d.conditional_formatting.add("J14:J28", CellIsRule(operator="greaterThan", formula=["0"], fill=PatternFill("solid", fgColor="E3F0E1")))
ch = BarChart(); ch.type = "col"; ch.style = 10; ch.title = "Net profit by month"; ch.height = 7.5; ch.width = 17; ch.legend = None
ch.add_data(Reference(d, min_col=5, min_row=20, max_row=32), titles_from_data=True); ch.set_categories(Reference(d, min_col=1, min_row=21, max_row=32))
ch.series[0].graphicalProperties.solidFill = t.accent; ch.series[0].graphicalProperties.line.solidFill = t.accent
d.add_chart(ch, "H31")

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
