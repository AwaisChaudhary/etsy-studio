"""Jewelry Business Spreadsheet (batch 10, lane a): handmade jewelry makers. Metal prices per gram/ounce in one place (update the spot
price once and every product re-prices), metal weight + waste per piece, findings/stones/chain library with cost per unit, product
costing (metal + 4 materials + packaging + labour + overheads), THREE pricing methods side by side (classic jewelry formula, cost x
multiplier, target margin after Etsy fees), your price with profit/margin/per hour, custom order tracker (ring size, engraving, deposit,
due date flags), stock in + inventory, sales by channel, expenses, dashboard. Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter as gl
from openpyxl.chart import BarChart, Reference

t = Theme("33304A", "B07A3C", "F4ECE0")
wb = Workbook()
NM, NP, NI, NSALE, NE, NO = 155, 105, 406, 1506, 306, 206
USD, USD4 = '"$"#,##0.00', '"$"#,##0.000'
GREY = "6A6F7D"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")
REDF = Font(name=F, bold=True, color="A12A1E"); AMBF = Font(name=F, bold=True, color="8A5A12"); GRNF = Font(name=F, bold=True, color="2E6B3A")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Jewelry Business Spreadsheet", "Price every necklace, ring and pair of earrings from its metal weight, findings and time, and track stock, orders and profit.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: today's metal prices (per gram or troy ounce), your hourly rate, target margin, overheads and the fees each sales channel takes.",
         "Materials: add each finding, stone, bead, chain and box once with the pack size and pack price. Cost per unit (per bead, inch, piece) is worked out.",
         "Product Pricing: one row per design. Pick the metal and its weight in grams, up to 4 materials and your minutes. Total cost and THREE prices appear: "
         "the classic jewelry formula, cost x your multiplier and a price that hits your margin after Etsy fees. Type your own price to see your real profit.",
         "Metal price went up? Change it once in Settings and every cost and suggested price updates. The 'Price check' column flags designs that slipped below target.",
         "Custom Orders: ring size, length, engraving, deposit and due date for every commission, with Due soon / Overdue flags.",
         "Stock In, Sales and Expenses: log batches, sales by channel and costs. Inventory and the Dashboard update themselves."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 46 if i == 2 else 34
legend(s, 12, 2)
label(s, "B14", "Classic jewelry formula: (materials x 2 + labour) = wholesale, wholesale x 2 = retail. It suits shops that also sell wholesale. "
      "The margin price includes Etsy fees so the margin is what you really keep. Pick whichever fits your market.", size=10, color="7A5A2A")
s.row_dimensions[14].height = 44
label(s, "B15", "For sterling silver, gold-filled, solid gold, brass, copper, beaded, wire-wrapped, resin, clay and permanent jewelry.", size=10)
label(s, "B16", "Example metals, materials, designs, orders and sales are included so you can see how it works: type over them or delete them. "
      "Metal prices and fee rates are examples: use your supplier's current price and your country's fees. Works in Excel and Google Sheets.", italic=True, size=10)
s.row_dimensions[16].height = 30

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your metal prices, rates and fees. Every design and sale uses these.", 5)
widths(st, {"A": 40, "B": 16, "C": 16, "D": 4, "E": 62})
rows = [("Your hourly rate", 22, USD, "What your design, making, polishing, photo and packing time is worth."),
        ("Target profit margin", 0.40, "0%", "Share of the price you want to keep as profit after every cost and fee."),
        ("Overheads (% of materials + metal)", 0.10, "0%", "Tools, polishing compound, pickle, torch gas, test pieces."),
        ("Your multiplier (cost x)", 2.5, '0.0"x"', "Many makers use 2x-3x total cost for retail."),
        ("Round suggested prices to .99?", "Yes", None, "Yes: $48.99. No: rounds up to the nearest 5 cents.")]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"E{5 + i}", n, size=9, color=GREY, italic=True)
dv_list(st, "B9", "Yes,No")
RATE, MARG, OVH, MULT, R99 = (f"Settings!$B${5 + i}" for i in range(5))
label(st, "A11", "Metal prices (update when the market moves)", bold=True, size=12)
header(st, 12, ["Metal", "Price per troy oz", "PRICE PER GRAM", "", "Waste / loss %"], t)
st["D12"].fill = PatternFill(None); st["D12"].border = Border()
METALS = [("Sterling silver (.925)", 38.00, 0.08), ("Fine silver (.999)", 41.00, 0.08), ("Gold-filled 14/20", 52.00, 0.05),
          ("14k yellow gold", 1560.00, 0.03), ("Brass", 1.20, 0.10), ("Copper", 1.00, 0.10), ("Other metal", 0, 0.05), ("None", 0, 0)]
for i, (mname, oz, w) in enumerate(METALS):
    r = 13 + i; inp(st, f"A{r}", mname).alignment = Alignment(horizontal="left", indent=1); inp(st, f"B{r}", oz, USD)
    calc(st, f"C{r}", f'=IF(B{r}="","",B{r}/31.1035)', USD4, bold=True); inp(st, f"E{r}", w, "0%")
label(st, "A21", "Use your supplier's price for sheet, wire or casting grain (it is higher than the market spot price). 1 troy oz = 31.1 g.",
      italic=True, size=9, color=GREY)
MTN, MTG, MTW = "Settings!$A$13:$A$20", "Settings!$C$13:$C$20", "Settings!$E$13:$E$20"
label(st, "A23", "Fees by sales channel", bold=True, size=12)
header(st, 24, ["Channel", "% of order", "Fixed per order"], t)
CH = [("Etsy", 0.095, 0.45, "6.5% transaction + about 3% + $0.25 payment processing + $0.20 listing. Add offsite ads if you pay them."),
      ("Website", 0.029, 0.30, "Card processing on Shopify, Squarespace, Stripe, PayPal."),
      ("Market / craft fair", 0.026, 0.15, "Card reader (Square, SumUp). Booth fees go in Expenses."),
      ("Instagram / Facebook", 0.029, 0.30, "Card or PayPal payments."),
      ("Wholesale / boutique", 0, 0, "Invoice paid by bank transfer."),
      ("Custom order", 0.029, 0.30, "Commissions paid by card or PayPal.")]
for i, (c, p_, fx, n) in enumerate(CH):
    r = 25 + i; inp(st, f"A{r}", c).alignment = Alignment(horizontal="left", indent=1); inp(st, f"B{r}", p_, "0.0%"); inp(st, f"C{r}", fx, USD)
    label(st, f"E{r}", n, size=9, color=GREY, italic=True)
CHN, CHP, CHF = "Settings!$A$25:$A$30", "Settings!$B$25:$B$30", "Settings!$C$25:$C$30"
EPCT, EFIX = "Settings!$B$25", "Settings!$C$25"
label(st, "A32", "Margin prices use the Etsy row so the margin holds on your highest-fee channel.", italic=True, size=9, color=GREY)
UNITS = "each,inch,cm,foot,gram,pair,strand,pack,ml,hour"
CATS = "Finding,Chain,Stone / crystal,Bead,Wire,Clay / resin,Packaging,Shipping supply,Other"
TYPES = "Necklace,Earrings,Ring,Bracelet,Anklet,Pendant,Charm,Set,Permanent jewelry,Other"

# ---------- Materials ----------
m = wb.create_sheet("Materials")
banner(m, t, "Findings, stones & supplies", "Add each supply once. Cost per unit is worked out for you. (Metal by weight goes in Settings.)", 10)
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
ex = [("Sterling cable chain 1.3 mm (spool)", "Chain", "inch", 300, 59.00, 180, 60, "Cut to length"),
      ("Gold-filled satellite chain", "Chain", "inch", 120, 64.00, 40, 36, ""),
      ("Sterling spring ring clasp", "Finding", "each", 20, 16.80, 34, 10, ""),
      ("Sterling jump ring 4 mm", "Finding", "each", 100, 9.50, 140, 40, ""),
      ("Sterling ear wires (pair)", "Finding", "pair", 25, 21.25, 18, 10, ""),
      ("Moonstone 6 mm cabochon", "Stone / crystal", "each", 10, 28.00, 12, 4, "Rainbow moonstone"),
      ("Freshwater pearl 7 mm", "Bead", "each", 50, 18.00, 66, 20, "Half-drilled"),
      ("Birthstone CZ 3 mm", "Stone / crystal", "each", 100, 14.00, 210, 50, "12 colours"),
      ("Bezel cup 6 mm sterling", "Finding", "each", 10, 12.50, 3, 5, ""),
      ("Jewelry box + card insert", "Packaging", "each", 50, 32.00, 44, 20, "Logo sticker"),
      ("Polishing cloth (mini)", "Packaging", "each", 100, 18.00, 120, 30, "Goes in every order"),
      ("Bubble mailer 4 x 8", "Shipping supply", "each", 100, 12.99, 75, 25, "")]
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
banner(pp, t, "Design costing & pricing", "One row per design: metal by weight, findings and time, three ways to price it, and what you keep.", 31)
cols = ["Design", "SKU", "Type", "Metal", "Metal weight (g)", "Material 1", "Qty", "Material 2", "Qty", "Material 3", "Qty", "Material 4", "Qty",
        "Other cost (each)", "Minutes to make + finish", "Metal cost (incl. waste)", "Findings & materials", "Labour", "Overheads", "TOTAL COST",
        "CLASSIC: wholesale (materials x2 + labour)", "CLASSIC: retail (wholesale x2)", "Cost x multiplier", "MARGIN PRICE (target after Etsy fees)",
        "YOUR PRICE (blank = margin price)", "Etsy fees at your price", "PROFIT per sale", "Margin", "Profit per hour", "Price check", "Notes"]
header(pp, 5, cols, t); pp.row_dimensions[5].height = 70
for i, w in enumerate([30, 9, 12, 20, 9, 28, 6, 24, 6, 22, 6, 20, 6, 9, 10, 11, 11, 10, 10, 11, 13, 12, 11, 14, 12, 10, 11, 8, 10, 13, 24]):
    pp.column_dimensions[gl(i + 1)].width = w
pp.freeze_panes = "B6"
label(pp, "A4", "Metal weight = the finished piece's metal in grams (weigh it, or use your supplier's weight per inch/piece). Qty = units of each material used.",
      italic=True, size=9, color=GREY)
for r in range(6, NP + 1):
    for col in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "Y", "AE"]: inp(pp, f"{col}{r}")
    for col in ["A", "D", "F", "H", "J", "L", "AE"]: pp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    pp[f"N{r}"].number_format = USD; pp[f"Y{r}"].number_format = USD; pp[f"E{r}"].number_format = "0.00"
    on = f'A{r}=""'
    calc(pp, f"P{r}", f'=IF({on},"",IF(D{r}="",0,N(E{r})*IFERROR(INDEX({MTG},MATCH(D{r},{MTN},0))*(1+INDEX({MTW},MATCH(D{r},{MTN},0))),0)))', USD)
    mat = "+".join(f"{mc(gl(c) + str(r))}*N({gl(c + 1)}{r})" for c in (6, 8, 10, 12))
    calc(pp, f"Q{r}", f'=IF({on},"",{mat}+N(N{r}))', USD)
    calc(pp, f"R{r}", f'=IF({on},"",N(O{r})/60*{RATE})', USD)
    calc(pp, f"S{r}", f'=IF({on},"",(P{r}+Q{r})*{OVH})', USD)
    calc(pp, f"T{r}", f'=IF({on},"",P{r}+Q{r}+R{r}+S{r})', USD, bold=True)
    calc(pp, f"U{r}", f'=IF({on},"",CEILING((P{r}+Q{r}+S{r})*2+R{r},0.05))', USD)
    def rnd_(x): return f'IF({R99}="Yes",CEILING({x}+0.01,1)-0.01,CEILING({x},0.05))'
    calc(pp, f"V{r}", f'=IF({on},"",{rnd_(f"U{r}*2")})', USD)
    calc(pp, f"W{r}", f'=IF({on},"",{rnd_(f"T{r}*{MULT}")})', USD)
    raw = f'(T{r}+{EFIX})/MAX(0.05,1-{EPCT}-{MARG})'
    calc(pp, f"X{r}", f'=IF({on},"",{rnd_(raw)})', USD, bold=True)
    pr_ = f'IF(Y{r}="",X{r},Y{r})'
    calc(pp, f"Z{r}", f'=IF({on},"",{pr_}*{EPCT}+{EFIX})', USD)
    calc(pp, f"AA{r}", f'=IF({on},"",{pr_}-T{r}-Z{r})', USD, bold=True)
    calc(pp, f"AB{r}", f'=IF({on},"",IF({pr_}=0,"",AA{r}/{pr_}))', "0%")
    calc(pp, f"AC{r}", f'=IF(OR({on},N(O{r})=0),"",(AA{r}+R{r})/(O{r}/60))', USD)
    calc(pp, f"AD{r}", f'=IF({on},"",IF(AA{r}<0,"Losing money",IF(AB{r}<{MARG}-0.05,"Below target","On target")))')
SC_, CL, JR, BOX_, PC = "Sterling cable chain 1.3 mm (spool)", "Sterling spring ring clasp", "Sterling jump ring 4 mm", "Jewelry box + card insert", "Polishing cloth (mini)"
prods = [("Moonstone bezel necklace", "NK-01", "Necklace", "Sterling silver (.925)", 1.6, SC_, 18, CL, 1, "Moonstone 6 mm cabochon", 1, BOX_, 1, None, 55, None, "Bezel from 6 mm cup"),
         ("Pearl drop earrings", "ER-02", "Earrings", "Sterling silver (.925)", 0.8, "Freshwater pearl 7 mm", 2, "Sterling ear wires (pair)", 1, BOX_, 1, PC, 1, None, 20, 38, ""),
         ("Hammered stacking ring", "RG-03", "Ring", "Sterling silver (.925)", 2.4, BOX_, 1, PC, 1, None, None, None, None, None, 30, None, "Size on order"),
         ("Birthstone charm bracelet", "BR-04", "Bracelet", "Gold-filled 14/20", 1.2, "Gold-filled satellite chain", 7.5, "Birthstone CZ 3 mm", 1, BOX_, 1, PC, 1, 2.10, 25, None, "Charm blank bought in"),
         ("14k gold initial stud", "ER-05", "Earrings", "14k yellow gold", 0.6, BOX_, 1, None, None, None, None, None, None, 1.50, 45, 129, "Cast by supplier"),
         ("Brass leaf pendant", "PD-06", "Pendant", "Brass", 4.5, "Gold-filled satellite chain", 18, JR, 2, BOX_, 1, None, None, None, 35, 39, "")]
for i, row in enumerate(prods):
    for j, v in enumerate(row):
        if v is not None: pp.cell(6 + i, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 25, 31][j]).value = v
for col in "FHJL": dv_list(pp, f"{col}6:{col}{NP}", MLIST)
dv_list(pp, f"D6:D{NP}", "=" + MTN); dv_list(pp, f"C6:C{NP}", TYPES)
for val, fill, f_ in (('"Losing money"', red, REDF), ('"Below target"', amb, AMBF), ('"On target"', grn, GRNF)):
    pp.conditional_formatting.add(f"AD6:AD{NP}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
pp.conditional_formatting.add(f"AA6:AA{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
legend(pp, NP + 2, 1)
PCOL = lambda c: f"'Product Pricing'!${c}$6:${c}${NP}"
PNAME, PCOST, PPRICE, PSUG, PWH = PCOL("A"), PCOL("T"), PCOL("Y"), PCOL("X"), PCOL("U")
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
batches = [(-62, "Moonstone bezel necklace", 6, "First run"), (-58, "Pearl drop earrings", 12, ""), (-51, "Hammered stacking ring", 10, "Sizes 5-9"),
           (-44, "Birthstone charm bracelet", 15, "Holiday stock"), (-37, "Brass leaf pendant", 8, ""), (-30, "14k gold initial stud", 4, "Cast batch"),
           (-19, "Pearl drop earrings", 12, "Restock"), (-8, "Birthstone charm bracelet", 10, "Restock")]
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
sales = [(55, "Etsy", "Pearl drop earrings", 1, None, 4.50, 4.10, None), (49, "Etsy", "Moonstone bezel necklace", 1, None, 4.50, 4.10, None),
         (44, "Market / craft fair", "Pearl drop earrings", 5, 36, None, None, None), (44, "Market / craft fair", "Hammered stacking ring", 4, None, None, None, None),
         (44, "Market / craft fair", "Brass leaf pendant", 3, None, None, None, None), (39, "Website", "Birthstone charm bracelet", 2, None, 4.00, 3.80, 3.00),
         (33, "Etsy", "14k gold initial stud", 1, None, 0, 4.60, None), (28, "Wholesale / boutique", "Pearl drop earrings", 8, 19.00, None, 9.50, None),
         (22, "Instagram / Facebook", "Moonstone bezel necklace", 1, None, 4.50, 4.10, None), (17, "Etsy", "Birthstone charm bracelet", 3, None, 4.50, 4.40, 5.20),
         (11, "Custom order", "Hammered stacking ring", 3, 42, 5.00, 4.60, None), (11, "Market / craft fair", "Birthstone charm bracelet", 4, None, None, None, None),
         (6, "Etsy", "Pearl drop earrings", 2, None, 4.50, 4.10, None), (2, "Etsy", "Moonstone bezel necklace", 1, None, 4.50, 4.10, None)]
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
ECATS = "Tools & equipment,Booth / market fee,Advertising,Software & subscriptions,Photography,Shipping supplies,Hallmarking / casting,Training,Other"
dv_list(ex_, f"B6:B{NE}", ECATS)
for i, (back, c, w, a) in enumerate([(58, "Tools & equipment", "Ring mandrel + rawhide mallet", 34.50), (44, "Booth / market fee", "Autumn craft fair table", 45),
                                      (30, "Advertising", "Etsy Ads", 12.40), (28, "Software & subscriptions", "Canva Pro (monthly)", 14.99),
                                      (12, "Booth / market fee", "Holiday market table", 60), (5, "Photography", "Ring display stand + props", 22.00)]):
    r = 6 + i; ex_[f"A{r}"] = f"=TODAY()-{back}"; ex_[f"B{r}"] = c; ex_[f"C{r}"] = w; ex_[f"D{r}"] = a
ED, EA = f"Expenses!$A$6:$A${NE}", f"Expenses!$D$6:$D${NE}"

# ---------- Custom Orders ----------
co = wb.create_sheet("Custom Orders")
banner(co, t, "Custom orders & commissions", "Every personalised piece: size, metal, engraving, deposit and due date in one place.", 16)
header(co, 5, ["Order date", "Customer", "Channel", "Design / description", "Metal", "Ring size / length", "Stone / birthstone", "Engraving / initials",
               "Quoted price", "Deposit paid", "BALANCE DUE", "Due date", "Status", "DAYS LEFT", "Flag", "Notes"], t)
co.row_dimensions[5].height = 44
for i, w in enumerate([12, 18, 15, 30, 18, 11, 14, 16, 11, 10, 11, 12, 13, 9, 12, 26]): co.column_dimensions[gl(i + 1)].width = w
co.freeze_panes = "C6"
STAT = "Enquiry,Quoted,Deposit paid,Making,Ready to ship,Shipped,Cancelled"
for r in range(6, NO + 1):
    for col in "ABCDEFGHIJLMP": inp(co, f"{col}{r}")
    for col in "BCDEGHP": co[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    for col in "AL": co[f"{col}{r}"].number_format = "dd mmm yyyy"
    for col in "IJ": co[f"{col}{r}"].number_format = USD
    calc(co, f"K{r}", f'=IF(B{r}="","",N(I{r})-N(J{r}))', USD, bold=True)
    calc(co, f"N{r}", f'=IF(OR(B{r}="",L{r}="",M{r}="Shipped",M{r}="Cancelled"),"",L{r}-TODAY())', "0")
    calc(co, f"O{r}", f'=IF(N{r}="","",IF(N{r}<0,"Overdue",IF(N{r}<=3,"Due soon","On track")))')
dv_list(co, f"C6:C{NO}", "=" + CHN); dv_list(co, f"E6:E{NO}", "=" + MTN); dv_list(co, f"M6:M{NO}", STAT)
for val, fill, f_ in (('"Overdue"', red, REDF), ('"Due soon"', amb, AMBF), ('"On track"', grn, GRNF)):
    co.conditional_formatting.add(f"O6:O{NO}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
orders = [(-20, "Hannah P.", "Etsy", "Hammered stacking rings x3", "Sterling silver (.925)", "6, 7, 7.5", "", "", 126, 126, -9, "Shipped", "Anniversary"),
          (-9, "Maya R.", "Instagram / Facebook", "Family birthstone necklace (4 stones)", "Gold-filled 14/20", "18 in", "Mar, Jun, Sep, Dec", "", 88, 44, 2, "Making", "Gift wrap"),
          (-6, "Chloe T.", "Etsy", "Initial stud earrings", "14k yellow gold", "", "", "A + J", 129, 129, 6, "Deposit paid", ""),
          (-4, "Priya S.", "Custom order", "Bridesmaid pearl earrings x6", "Sterling silver (.925)", "", "", "", 204, 100, 12, "Making", "Wedding 20 Dec"),
          (-2, "Leah M.", "Website", "Engraved bar necklace", "Sterling silver (.925)", "16 in", "", "\"Always\"", 58, 0, -1, "Quoted", "Chasing reply"),
          (-1, "Grace W.", "Etsy", "Moonstone ring", "Sterling silver (.925)", "8", "Moonstone", "", 74, 37, 9, "Deposit paid", "")]
for i, row in enumerate(orders):
    r = 6 + i; od, cu, chn, de, me, sz, stn, eng, q, dep, due, stt, nt = row
    co[f"A{r}"] = f"=TODAY(){od:+d}"; co[f"L{r}"] = f"=TODAY(){due:+d}"
    for col, v in zip("BCDEFGHIJMP", (cu, chn, de, me, sz, stn, eng, q, dep, stt, nt)):
        if v != "": co[f"{col}{r}"] = v
COF, COK = f"'Custom Orders'!$O$6:$O${NO}", f"'Custom Orders'!$K$6:$K${NO}"
COM = f"'Custom Orders'!$M$6:$M${NO}"

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
    calc(iv, f"I{r}", f"=IF(A{r}=\"\",\"\",MAX(0,F{r})*'Product Pricing'!T{r})", USD)
    calc(iv, f"J{r}", f"=IF(A{r}=\"\",\"\",MAX(0,F{r})*IF('Product Pricing'!Y{r}=\"\",'Product Pricing'!X{r},'Product Pricing'!Y{r}))", USD)
for i, (o, dmg, at) in enumerate([(2, 0, 3), (4, 1, 8), (0, 0, 4), (0, 1, 6), (1, 0, 2), (0, 0, 3)]):
    iv[f"B{6 + i}"] = o; iv[f"E{6 + i}"] = dmg; iv[f"G{6 + i}"] = at
for val, fill, f_ in (('"Sold out"', red, REDF), ('"Check counts"', red, REDF), ('"Low stock"', amb, AMBF), ('"In stock"', grn, GRNF)):
    iv.conditional_formatting.add(f"H6:H{NP}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
label(iv, f"A{NP + 2}", "Designs appear here automatically from Product Pricing. Opening stock = what you had when you started using this sheet.", italic=True, size=9, color=GREY)

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Sales, Expenses, Inventory, Materials and Custom Orders.", 10)
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
       ("Materials to reorder", f'=COUNTIF(Materials!$I$6:$I${NM},"Reorder")', "0"),
       ("Custom orders open", f'=COUNTIFS({COM},"<>Shipped",{COM},"<>Cancelled",{COM},"<>")', "0"),
       ("Custom orders due soon / overdue", f'=COUNTIF({COF},"Due soon")+COUNTIF({COF},"Overdue")', "0")]
for i, (a, f, fmt) in enumerate(kpi):
    r = 6 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 26
d["B11"].fill = PatternFill("solid", fgColor="D6EEE9")
header(d, 22, ["Month", "Sales", "Profit from sales", "Expenses", "Net profit", "Items sold"], t)
for i, mn in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    r = 23 + i; label(d, f"A{r}", mn)
    mr = f'{SD},">="&DATE($B$4,{i + 1},1),{SD},"<"&DATE($B$4,{i + 2},1)'
    me = f'{ED},">="&DATE($B$4,{i + 1},1),{ED},"<"&DATE($B$4,{i + 2},1)'
    calc(d, f"B{r}", f"=SUMIFS({SI},{mr})+SUMIFS({SSH},{mr})", USD); calc(d, f"C{r}", f"=SUMIFS({SPF},{mr})", USD)
    calc(d, f"D{r}", f"=SUMIFS({EA},{me})", USD); calc(d, f"E{r}", f"=C{r}-D{r}", USD, bold=True); calc(d, f"F{r}", f"=SUMIFS({SQ},{mr})", "#,##0")
label(d, "A35", "Total", bold=True)
for col in "BCDEF": calc(d, f"{col}35", f"=SUM({col}23:{col}34)", "#,##0" if col == "F" else USD, bold=True)
header(d, 5, ["Channel", "Sales", "Profit"], t, start=8)
for i in range(6):
    r = 6 + i; d[f"H{r}"] = f"=Settings!A{25 + i}"; d[f"H{r}"].font = Font(name=F, size=11)
    calc(d, f"I{r}", f'=SUMIFS({SI},{SCH},H{r},{yr})', USD); calc(d, f"J{r}", f'=SUMIFS({SPF},{SCH},H{r},{yr})', USD)
header(d, 13, ["Best sellers (first 15 designs)", "Items sold", "Profit"], t, start=8)
for i in range(15):
    r = 14 + i
    d[f"H{r}"] = f"=IF('Product Pricing'!A{6 + i}=\"\",\"\",'Product Pricing'!A{6 + i})"; d[f"H{r}"].font = Font(name=F, size=11)
    calc(d, f"I{r}", f'=IF(H{r}="","",SUMIFS({SQ},{SC},H{r},{yr}))', "#,##0")
    calc(d, f"J{r}", f'=IF(H{r}="","",SUMIFS({SPF},{SC},H{r},{yr}))', USD)
d.conditional_formatting.add("J14:J28", CellIsRule(operator="greaterThan", formula=["0"], fill=PatternFill("solid", fgColor="E3F0E1")))
ch = BarChart(); ch.type = "col"; ch.style = 10; ch.title = "Net profit by month"; ch.height = 7.5; ch.width = 17; ch.legend = None
ch.add_data(Reference(d, min_col=5, min_row=22, max_row=34), titles_from_data=True); ch.set_categories(Reference(d, min_col=1, min_row=23, max_row=34))
ch.series[0].graphicalProperties.solidFill = t.accent; ch.series[0].graphicalProperties.line.solidFill = t.accent
d.add_chart(ch, "H31")

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
