"""Machine Embroidery Business Spreadsheet (batch 9, lane a): machine cost per hour, thread cost per 1,000 stitches, run time from
stitch count + speed + colour changes, blanks & stabilizer library, design library (stitch counts, licences), product pricing
(cost-based retail + wholesale AND a stitch-rate price to compare), bulk quote with tiers, digitizing fee, run hours and a finish
date, order tracker, sales log, dashboard. Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter as gl

t = Theme("3A2E4F", "C2557A", "F6E8EE")
wb = Workbook()
NS, ND, NP, NO, NSALE = 105, 105, 65, 205, 1006
USD, USD4 = '"$"#,##0.00', '"$"#,##0.0000'
GREY = "6A6F7D"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")
REDF = Font(name=F, bold=True, color="A12A1E"); AMBF = Font(name=F, bold=True, color="8A5A12"); GRNF = Font(name=F, bold=True, color="2E6B3A")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Machine Embroidery Business Spreadsheet", "Price every hat, hoodie and towel from its stitch count, quote team orders in seconds, and track every order.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly rate, what your machine cost and how long it lasts, stitches per minute, thread cost, colour change and hooping time, mark-ups, fees and bulk tiers.",
         "Blanks & Supplies: add each blank (caps, tees, hoodies, towels, onesies) and stabilizer once. Cost each is worked out from the pack price.",
         "Designs: your design library with stitch count, colours and size, plus where the design came from and its licence.",
         "Product Pricing: pick a blank, up to two designs (left chest + back), stabilizer and any extra stitches for names. "
         "Run time, thread, machine cost, labour, total cost, wholesale and retail prices appear, plus a 'per 1,000 stitches' price to compare.",
         "Bulk Quote: team, school and business orders with discount tiers, digitizing fee, deposit, profit, machine hours and a finish date.",
         "Orders, Sales and Dashboard: track every order from New to Shipped, log sales, and see income, profit and your best sellers."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 46 if i in (0, 3) else 34
legend(s, 12, 2)
label(s, "B14", "Stitches per minute: use your REAL average, not the machine's top speed. Most single-needle and multi-needle home machines average 400-800 "
      "once slow-downs, trims and jumps are included. Time one design and divide its stitch count by the minutes it took.", size=10, color="8A3B5E")
s.row_dimensions[14].height = 44
label(s, "B15", "Only stitch designs you digitized yourself, designs with a commercial licence, or artwork your customer owns. Team, school and brand logos need the owner's permission.",
      size=10, color="8A3B5E")
s.row_dimensions[15].height = 30
label(s, "B16", "Example blanks, designs, products, orders and sales are included so you can see how it works: type over them or delete them. "
      "Prices in the examples are illustrations only. Works in Excel and Google Sheets.", italic=True, size=10)
s.row_dimensions[16].height = 30

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your machine, your rates. Every product and quote uses these.", 4)
widths(st, {"A": 48, "B": 16, "C": 4, "D": 66})
rows = [("Your hourly rate", 20, USD, "Hooping, colour changes, trimming, finishing, packing."),
        ("What your machine cost (incl. hoops, frames)", 1800, USD, None),
        ("Running hours you expect from it", 3000, "#,##0", "Stitching hours before you replace it."),
        ("Upkeep per running hour (needles, oil, service)", 0.50, USD, "Set aside for needles, bobbin cases, servicing."),
        ("Average stitches per minute (real speed)", 600, "#,##0", "Your real average incl. slow-downs and trims. See Start Here."),
        ("Thread cone price", 5.50, USD, "One cone of top thread."),
        ("Yards per cone", 5500, "#,##0", None),
        ("Yards of top thread per 1,000 stitches", 5, "0.0", "About 4-6 for most fill and satin designs."),
        ("Bobbin cost per 1,000 stitches", 0.01, USD4, "Pre-wound bobbins spread over the stitches they give."),
        ("Minutes per colour change", 1, "0.0", "About 1 for single-needle machines, 0.1 for multi-needle."),
        ("Hooping + set-up minutes per piece", 3, "0.0", "Marking, hooping, loading the design, unhooping."),
        ("Count stitching time as your labour?", "Yes", None, "Yes if you watch the machine while it stitches. No if you work on other things."),
        ("Overheads (% of blanks + supplies)", 0.10, "0%", "Test sew-outs, spray adhesive, pens, electricity."),
        ("Wholesale / bulk price = cost x", 1.5, '0.0"x"', "Team, school and business orders start here."),
        ("Retail price = cost x", 2.0, '0.0"x"', "Single and personalised items on Etsy and at markets."),
        ("Round prices up to the nearest", 0.5, USD, None),
        ("Stitch-rate price per 1,000 stitches", 1.00, USD, "The 'per 1,000 stitches' method many shops quote. Shown for comparison."),
        ("Minimum stitching charge per piece", 6, USD, "Stitch-rate method: small designs never go below this."),
        ("Etsy transaction fee", 0.065, "0.0%", "Estimate. Check Etsy's current fees for your country."),
        ("Payment processing (%)", 0.03, "0.0%", "Estimate, varies by country."),
        ("Payment processing (fixed per order)", 0.25, USD, None),
        ("Listing fee per sale", 0.20, USD, None),
        ("Machine hours per working day", 6, "0.0", "For the finish date on bulk quotes."),
        ("Number of machines / heads", 1, "0", "Run time on bulk quotes is shared across them."),
        ("Deposit for custom and bulk orders", 0.5, "0%", None),
        ("Default digitizing fee (new logo)", 35, USD, "One-off, for turning a customer's logo into a stitch file.")]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"D{5 + i}", n, size=9, color=GREY, italic=True)
dv_list(st, "B16", "Yes,No")
(RATE, MPR, MLIFE, UPK, SPM, CONE, YPC, YPK, BOB, CCM, HOOP, LABQ, OVH, WMUL, RMUL, RND, SRATE, SMIN, ETX, PPC, PFX, LST, HPD, HEADS, DEP, DIGI) = \
    (f"Settings!$B${5 + i}" for i in range(26))
label(st, "A32", "MACHINE COST PER RUNNING HOUR", bold=True); calc(st, "B32", f"=IFERROR({MPR}/{MLIFE},0)+{UPK}", USD, bold=True)
label(st, "A33", "THREAD COST PER 1,000 STITCHES", bold=True); calc(st, "B33", f"=IFERROR({CONE}/{YPC}*{YPK},0)+{BOB}", USD4, bold=True)
MCH, THR = "Settings!$B$32", "Settings!$B$33"
label(st, "A35", "Bulk discount tiers", bold=True, size=12); label(st, "B35", "From qty", bold=True, size=10); label(st, "D35", "Discount off the wholesale price", bold=True, size=10)
for i, (q, dsc) in enumerate([(1, 0), (12, 0.05), (24, 0.10), (48, 0.15), (100, 0.20)]):
    label(st, f"A{36 + i}", f"Tier {i + 1}"); inp(st, f"B{36 + i}", q, "0"); inp(st, f"D{36 + i}", dsc, "0%")
TQ, TD = "Settings!$B$36:$B$40", "Settings!$D$36:$D$40"
label(st, "A42", "Keep the 'From qty' numbers going up. A quote for 30 pieces uses the tier that starts at 24.", italic=True, size=9, color=GREY)

# ---------- Blanks & Supplies ----------
su = wb.create_sheet("Blanks & Supplies")
banner(su, t, "Blanks & supplies", "Add each blank and stabilizer once. Cost each is worked out for you.", 10)
header(su, 5, ["Item", "Type", "Pack size (pieces)", "Pack price", "COST EACH", "On hand", "Reorder at", "Status", "Supplier / notes"], t)
su.row_dimensions[5].height = 44
widths(su, {"A": 38, "B": 16, "C": 11, "D": 11, "E": 11, "F": 9, "G": 10, "H": 11, "I": 30}); su.freeze_panes = "B6"
for r in range(6, NS + 1):
    for col in "ABCDFGI": inp(su, f"{col}{r}")
    for col in "AI": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    su[f"D{r}"].number_format = USD
    calc(su, f"E{r}", f'=IF(OR(A{r}="",N(C{r})=0,D{r}=""),"",D{r}/C{r})', USD, bold=True)
    calc(su, f"H{r}", f'=IF(OR(A{r}="",F{r}=""),"",IF(F{r}<=N(G{r}),"Reorder","OK"))')
TYPES = "Blank,Stabilizer,Topping,Patch / applique,Packaging,Other"
ex = [("Structured trucker cap", "Blank", 12, 54.00, 20, 12, "Mixed colours"), ("Unstructured dad cap", "Blank", 12, 42.00, 9, 12, ""),
      ("Cotton tee (adult)", "Blank", 12, 38.00, 30, 12, ""), ("Pullover hoodie (adult)", "Blank", 6, 72.00, 11, 6, ""),
      ("Crewneck sweatshirt (adult)", "Blank", 6, 60.00, 8, 6, ""), ("Waffle hand towel", "Blank", 12, 36.00, 18, 12, ""),
      ("Baby onesie (cotton)", "Blank", 10, 32.00, 14, 10, ""), ("Canvas tote bag", "Blank", 12, 30.00, 24, 12, ""),
      ("Cut-away stabilizer (precut 8 x 8)", "Stabilizer", 100, 22.00, 140, 40, "Knits, sweatshirts"), ("Tear-away stabilizer (precut 8 x 8)", "Stabilizer", 100, 16.00, 90, 40, "Towels, totes, caps"),
      ("Cap backing (tear-away)", "Stabilizer", 100, 14.00, 45, 30, ""), ("Water-soluble topping (8 x 8)", "Topping", 100, 18.00, 60, 30, "Towels, fleece"),
      ("Poly mailer + tissue + thank-you card", "Packaging", 100, 26.00, 70, 25, "")]
for i, row in enumerate(ex):
    for j, v in enumerate(row):
        if v != "": su.cell(6 + i, [1, 2, 3, 4, 6, 7, 9][j]).value = v
dv_list(su, f"B6:B{NS}", TYPES)
su.conditional_formatting.add(f"H6:H{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=red, font=REDF))
SNAME, SEACH = "'Blanks & Supplies'!$A$6:$A$" + str(NS), "'Blanks & Supplies'!$E$6:$E$" + str(NS)
SLIST = "=" + SNAME
def look(ref): return f'IF({ref}="",0,IFERROR(INDEX({SEACH},MATCH({ref},{SNAME},0)),0))'

# ---------- Designs ----------
dz = wb.create_sheet("Designs")
banner(dz, t, "Design library", "Every stitch file you use: stitch count, colours, size and licence. Run time is worked out.", 9)
header(dz, 5, ["Design", "Stitch count", "Colour changes", "Size (in)", "Placement", "Source", "Licence / owner notes", "Run time (min)", "Thread cost"], t)
dz.row_dimensions[5].height = 44
widths(dz, {"A": 32, "B": 11, "C": 10, "D": 10, "E": 15, "F": 20, "G": 32, "H": 10, "I": 10}); dz.freeze_panes = "B6"
for r in range(6, ND + 1):
    for col in "ABCDEFG": inp(dz, f"{col}{r}")
    for col in "AG": dz[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    dz[f"B{r}"].number_format = "#,##0"
    calc(dz, f"H{r}", f'=IF(OR(A{r}="",N(B{r})=0),"",B{r}/{SPM}+N(C{r})*{CCM})', "0.0")
    calc(dz, f"I{r}", f'=IF(OR(A{r}="",N(B{r})=0),"",B{r}/1000*{THR})', USD4)
dv_list(dz, f"E6:E{ND}", "Left chest,Full front,Full back,Cap front,Cap side,Sleeve,Towel border,Bag front,Other")
dv_list(dz, f"F6:F{ND}", "I digitized it,Bought with licence,Customer's artwork,Font / lettering,Other")
designs = [("Floral monogram (3 letters)", 9800, 3, "3.5 x 3.5", "Left chest", "I digitized it", ""),
           ("Mountain line art", 6200, 2, "4 x 2.5", "Cap front", "I digitized it", ""),
           ("Name in script font (per name)", 2800, 1, "4 x 1", "Other", "Font / lettering", "Embroidery font with commercial licence"),
           ("Customer logo: Harbor Coffee", 7400, 4, "3.5 x 2", "Left chest", "Customer's artwork", "Written OK from owner on file"),
           ("Large back wildflowers", 38000, 6, "10 x 10", "Full back", "Bought with licence", "Licence allows up to 500 sales"),
           ("Baby name + date", 5200, 2, "4 x 3", "Full front", "Font / lettering", ""),
           ("Team crest (school)", 11500, 5, "4 x 4", "Left chest", "Customer's artwork", "School approved use for team order")]
for i, row in enumerate(designs):
    for j, v in enumerate(row):
        if v != "": dz.cell(6 + i, 1 + j).value = v
DNAME, DST, DCC = (f"Designs!${c}$6:${c}${ND}" for c in "ABC")
DLIST = "=" + DNAME
def dl(ref, rng): return f'IF({ref}="",0,IFERROR(INDEX({rng},MATCH({ref},{DNAME},0)),0))'

# ---------- Product Pricing ----------
pp = wb.create_sheet("Product Pricing")
banner(pp, t, "Product costing & pricing", "One row per product: blank, designs, stabilizer, run time and every cost, then wholesale and retail prices.", 27)
cols = ["Product", "Blank", "Design 1", "Design 2 (optional)", "Extra stitches (names, text)", "Stabilizer", "Topping / patch", "Packaging", "Extra hands-on minutes",
        "TOTAL STITCHES", "Colour changes", "Stitching time (min)", "Hands-on time (min)",
        "Blank + supplies", "Thread", "Machine", "Labour", "Overheads", "TOTAL COST", "Wholesale / bulk price", "RETAIL PRICE", "Stitch-rate price (compare)",
        "Etsy fees", "PROFIT per retail sale", "Margin", "Profit per machine hour"]
header(pp, 5, cols, t); pp.row_dimensions[5].height = 70
for i, w in enumerate([28, 24, 24, 20, 10, 26, 22, 22, 9, 10, 8, 9, 9, 10, 8, 9, 9, 9, 11, 11, 11, 11, 9, 11, 8, 11]): pp.column_dimensions[gl(i + 1)].width = w
pp.freeze_panes = "B6"
label(pp, "A4", "Two placements (left chest + back)? Pick both designs. Each extra design adds a re-hoop. Personalised names: type their stitch count in 'Extra stitches'.",
      italic=True, size=9, color=GREY)
for r in range(6, NP + 1):
    for col in "ABCDEFGHI": inp(pp, f"{col}{r}")
    for col in "ABCDFGH": pp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    pp[f"E{r}"].number_format = "#,##0"
    on = f'A{r}=""'
    calc(pp, f"J{r}", f'=IF({on},"",{dl(f"C{r}", DST)}+{dl(f"D{r}", DST)}+N(E{r}))', "#,##0", bold=True)
    calc(pp, f"K{r}", f'=IF({on},"",{dl(f"C{r}", DCC)}+{dl(f"D{r}", DCC)}+IF(N(E{r})>0,1,0))', "0")
    calc(pp, f"L{r}", f'=IF({on},"",J{r}/{SPM}+K{r}*{CCM})', "0.0")
    hoops = f'(IF(C{r}="",0,1)+IF(D{r}="",0,1)+IF(AND(C{r}="",D{r}="",N(E{r})>0),1,0))'
    calc(pp, f"M{r}", f'=IF({on},"",{hoops}*{HOOP}+N(I{r})+IF({LABQ}="Yes",L{r},K{r}*{CCM}))', "0.0")
    calc(pp, f"N{r}", f'=IF({on},"",{look(f"B{r}")}+{look(f"F{r}")}*MAX(1,{hoops})+{look(f"G{r}")}+{look(f"H{r}")})', USD)
    calc(pp, f"O{r}", f'=IF({on},"",J{r}/1000*{THR})', USD)
    calc(pp, f"P{r}", f'=IF({on},"",L{r}/60*{MCH})', USD)
    calc(pp, f"Q{r}", f'=IF({on},"",M{r}/60*{RATE})', USD)
    calc(pp, f"R{r}", f'=IF({on},"",N{r}*{OVH})', USD)
    calc(pp, f"S{r}", f'=IF({on},"",N{r}+O{r}+P{r}+Q{r}+R{r})', USD, bold=True)
    calc(pp, f"T{r}", f'=IF({on},"",CEILING(S{r}*{WMUL},{RND}))', USD, bold=True)
    calc(pp, f"U{r}", f'=IF({on},"",CEILING(S{r}*{RMUL},{RND}))', USD, bold=True)
    calc(pp, f"V{r}", f'=IF({on},"",CEILING({look(f"B{r}")}*1.5+MAX({SMIN},J{r}/1000*{SRATE}),{RND}))', USD)
    calc(pp, f"W{r}", f'=IF({on},"",U{r}*({ETX}+{PPC})+{PFX}+{LST})', USD)
    calc(pp, f"X{r}", f'=IF({on},"",U{r}-S{r}-W{r})', USD, bold=True)
    calc(pp, f"Y{r}", f'=IF(OR({on},N(U{r})=0),"",X{r}/U{r})', "0%")
    calc(pp, f"Z{r}", f'=IF(OR({on},N(L{r})=0),"",X{r}/(L{r}/60))', USD)
CT, CU, TEE, HD = "Structured trucker cap", "Cut-away stabilizer (precut 8 x 8)", "Cotton tee (adult)", "Pullover hoodie (adult)"
TA, CB, PK, WT = "Tear-away stabilizer (precut 8 x 8)", "Cap backing (tear-away)", "Poly mailer + tissue + thank-you card", "Water-soluble topping (8 x 8)"
prods = [("Mountain trucker cap", CT, "Mountain line art", None, None, CB, None, PK, 2),
         ("Monogram sweatshirt", "Crewneck sweatshirt (adult)", "Floral monogram (3 letters)", None, None, CU, None, PK, 2),
         ("Wildflower back hoodie + name", HD, "Large back wildflowers", "Name in script font (per name)", None, CU, None, PK, 4),
         ("Personalised hand towel", "Waffle hand towel", None, None, 3400, TA, WT, PK, 3),
         ("Baby name onesie", "Baby onesie (cotton)", "Baby name + date", None, None, CU, None, PK, 3),
         ("Logo tee (left chest)", TEE, "Customer logo: Harbor Coffee", None, None, CU, None, None, 1),
         ("Team crest hoodie", HD, "Team crest (school)", None, None, CU, None, None, 1),
         ("Name tote bag", "Canvas tote bag", None, None, 2800, TA, None, PK, 2)]
for i, row in enumerate(prods):
    for j, v in enumerate(row):
        if v is not None: pp.cell(6 + i, 1 + j).value = v
dv_list(pp, f"B6:B{NP}", SLIST); dv_list(pp, f"F6:H{NP}", SLIST); dv_list(pp, f"C6:D{NP}", DLIST)
pp.conditional_formatting.add(f"X6:X{NP}", CellIsRule(operator="lessThan", formula=["0"], font=Font(name=F, bold=True, color="C00000")))
legend(pp, NP + 2, 1)
PCOL = lambda c: f"'Product Pricing'!${c}$6:${c}${NP}"
PNAME, PCOST, PWH, PRET, PRUN = PCOL("A"), PCOL("S"), PCOL("T"), PCOL("U"), PCOL("L")

# ---------- Bulk Quote ----------
bq = wb.create_sheet("Bulk Quote")
banner(bq, t, "Bulk order quote", "Teams, schools, businesses, bridal parties: price any quantity, see machine hours and a finish date.", 7)
widths(bq, {"A": 30, "B": 28, "C": 2, "D": 30, "E": 14, "F": 16, "G": 16})
qi = [("Customer", "Harbor Coffee (staff tees)", None), ("Product", "Logo tee (left chest)", None), ("Quantity", 30, "0"),
      ("Digitizing fee (blank = default, 0 = none)", None, USD), ("Rush fee (one-off)", 0, USD), ("Shipping charged", 18, USD)]
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
      ("Digitizing fee", f'=IF(B8="",{DIGI},B8)', USD, False),
      ("QUOTE TOTAL", '=IF(E9="","",E9+E10+N(B9)+N(B10))', USD, True),
      ("Deposit to ask for", f'=IF(E11="","",ROUND(E11*{DEP},2))', USD, True),
      ("Your total cost", '=IF(E5="","",E5*B7)', USD, False),
      ("Your profit on this order", '=IF(E11="","",E11-N(B10)-E13)', USD, True),
      ("Machine hours", f'=IFERROR(B7*INDEX({PRUN},{M})/60/MAX(1,{HEADS}),"")', "0.0", False),
      ("Earliest finish date", f'=IFERROR(WORKDAY(TODAY(),MAX(1,ROUNDUP(E15/{HPD},0))),"")', "ddd dd mmm yyyy", True),
      ("Price check", '=IF(E8="","",IF(E8<E5,"Below cost!",IF(E8<E5*1.3,"Thin margin","Healthy")))', None, True)]
for i, (a, f, fmt, b) in enumerate(qo):
    r = 5 + i; label(bq, f"D{r}", a, bold=b); calc(bq, f"E{r}", f, fmt, bold=b)
bq["E11"].font = Font(name=F, size=16, bold=True, color="1F2A44"); bq.row_dimensions[11].height = 28
bq["E8"].font = Font(name=F, size=14, bold=True, color="1F2A44")
bq.column_dimensions["E"].width = 17
for val, fill, f_ in (('"Below cost!"', red, REDF), ('"Thin margin"', amb, AMBF), ('"Healthy"', grn, GRNF)):
    bq.conditional_formatting.add("E17", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
label(bq, "A20", "Price ladder for this product", bold=True, size=12)
header(bq, 21, ["Quantity", "Discount", "", "Price each", "Total (items)", "Your profit"], t)
for i in range(5):
    r = 22 + i
    calc(bq, f"A{r}", f"=INDEX({TQ},{i + 1})", "0"); calc(bq, f"B{r}", f"=INDEX({TD},{i + 1})", "0%")
    calc(bq, f"D{r}", f'=IF($E$6="","",CEILING($E$6*(1-B{r}),0.25))', USD); calc(bq, f"E{r}", f'=IF(D{r}="","",D{r}*A{r})', USD)
    calc(bq, f"F{r}", f'=IF(D{r}="","",(D{r}-$E$5)*A{r})', USD)
label(bq, "A28", "Finish date counts working days from today using your machine hours per day (Settings). Add time for blanks to arrive.", italic=True, size=9, color=GREY)

# ---------- Orders ----------
od = wb.create_sheet("Orders")
banner(od, t, "Order tracker", "Every order from New to Shipped: proofs, sizes, deposits, balance and deadlines.", 16)
cols = ["Order #", "Customer", "Product", "Thread colours / names / sizes", "Qty", "Price each (blank = retail)", "Status", "Deposit paid", "Order date", "Ship by", "Notes",
        "Order total", "Balance due", "Days to ship-by", "Flag"]
header(od, 5, cols, t); od.row_dimensions[5].height = 44
widths(od, {"A": 9, "B": 22, "C": 28, "D": 32, "E": 6, "F": 12, "G": 13, "H": 11, "I": 12, "J": 12, "K": 24, "L": 12, "M": 12, "N": 10, "O": 12})
od.freeze_panes = "C6"
STAT = "New,Proof sent,Approved,Digitizing,Stitching,Finishing,Shipped,Cancelled"
for r in range(6, NO + 1):
    for col in "ABCDEFGHIJK": inp(od, f"{col}{r}")
    for col in "BCDK": od[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    for col in "IJ": od[f"{col}{r}"].number_format = "dd mmm yyyy"
    for col in "FH": od[f"{col}{r}"].number_format = USD
    on = f'C{r}=""'
    calc(od, f"L{r}", f'=IF({on},"",N(E{r})*IF(F{r}="",IFERROR(INDEX({PRET},MATCH(C{r},{PNAME},0)),0),F{r}))', USD)
    calc(od, f"M{r}", f'=IF(OR({on},G{r}="Cancelled"),"",L{r}-N(H{r}))', USD, bold=True)
    calc(od, f"N{r}", f'=IF(OR(J{r}="",G{r}="Shipped",G{r}="Cancelled"),"",J{r}-TODAY())', "0")
    calc(od, f"O{r}", f'=IF(N{r}="","",IF(N{r}<0,"LATE",IF(AND(N{r}<=3,OR(G{r}="New",G{r}="Proof sent")),"Chase proof",IF(N{r}<=2,"Due soon","On track"))))')
dv_list(od, f"G6:G{NO}", STAT); dv_list(od, f"C6:C{NO}", "=" + PNAME)
ords = [("E-201", "Jess M.", "Monogram sweatshirt", "Sage thread, 'AMR', size M", 1, None, "Stitching", "full", -3, 2, "Gift"),
        ("E-202", "Harbor Coffee", "Logo tee (left chest)", "Brown + cream, 10 S / 12 M / 8 L", 30, "q", "Proof sent", 300, -2, 9, "Sew-out photo sent"),
        ("E-203", "Lakeside U12 soccer", "Team crest hoodie", "Navy hoodies, sizes on list", 16, 30, "Approved", 256, -5, 6, "Names on sleeves next order"),
        ("E-204", "Etsy order", "Baby name onesie", "'Theo 03.11.26' pale blue", 1, None, "New", "full", 0, 4, ""),
        ("E-205", "Priya K.", "Wildflower back hoodie + name", "'Priya' on left chest, size L", 1, None, "Finishing", "full", -6, 1, "")]
for i, (n, cu, pr, pers, q, pe, sta, dep, od_, due, note) in enumerate(ords):
    r = 6 + i; od[f"A{r}"] = n; od[f"B{r}"] = cu; od[f"C{r}"] = pr; od[f"D{r}"] = pers; od[f"E{r}"] = q; od[f"G{r}"] = sta; od[f"K{r}"] = note
    if pe == "q": od[f"F{r}"] = "='Bulk Quote'!E8"
    elif pe is not None: od[f"F{r}"] = pe
    if dep == "full": od[f"H{r}"] = f"=L{r}"
    elif dep is not None: od[f"H{r}"] = dep
    od[f"I{r}"] = f"=TODAY(){od_:+d}" if od_ else "=TODAY()"; od[f"J{r}"] = f"=TODAY()+{due}"
for val, fill, f_ in (('"LATE"', red, REDF), ('"Chase proof"', red, REDF), ('"Due soon"', amb, AMBF), ('"On track"', grn, GRNF)):
    od.conditional_formatting.add(f"O6:O{NO}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))

# ---------- Sales ----------
sa = wb.create_sheet("Sales")
banner(sa, t, "Sales log", "One row per sale. Blank price = retail (wholesale for Bulk / team orders). Cost comes from Product Pricing.", 11)
header(sa, 5, ["Date", "Channel", "Product", "Qty", "Price each (blank = list)", "Sale total", "Fees & shipping paid", "Cost of goods", "Profit", "Month", "Notes"], t)
sa.row_dimensions[5].height = 44
widths(sa, {"A": 13, "B": 16, "C": 30, "D": 7, "E": 12, "F": 12, "G": 13, "H": 13, "I": 12, "J": 9, "K": 24}); sa.freeze_panes = "A6"
for r in range(6, NSALE + 1):
    for col in "ABCDEGK": inp(sa, f"{col}{r}")
    for col in "CK": sa[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sa[f"A{r}"].number_format = "dd mmm yyyy"; sa[f"E{r}"].number_format = USD; sa[f"G{r}"].number_format = USD
    lp = f'IFERROR(IF(B{r}="Bulk / team order",INDEX({PWH},MATCH(C{r},{PNAME},0)),INDEX({PRET},MATCH(C{r},{PNAME},0))),0)'
    calc(sa, f"F{r}", f'=IF(OR(C{r}="",D{r}=""),"",D{r}*IF(E{r}="",{lp},E{r}))', USD)
    calc(sa, f"H{r}", f'=IF(OR(C{r}="",D{r}=""),"",D{r}*IFERROR(INDEX({PCOST},MATCH(C{r},{PNAME},0)),0))', USD)
    calc(sa, f"I{r}", f'=IF(F{r}="","",F{r}-N(G{r})-N(H{r}))', USD, bold=True)
    calc(sa, f"J{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
CH = ["Etsy", "Website", "Market", "Bulk / team order", "Local / Instagram", "Other"]
dv_list(sa, f"B6:B{NSALE}", ",".join(CH)); dv_list(sa, f"C6:C{NSALE}", "=" + PNAME)
sales = [(40, "Etsy", "Monogram sweatshirt", 2, None, "etsy", ""), (36, "Bulk / team order", "Team crest hoodie", 14, 30, 0, "Lakeside U10"),
         (33, "Etsy", "Baby name onesie", 3, None, "etsy", ""), (28, "Market", "Mountain trucker cap", 9, None, 0, "Fall festival"),
         (28, "Market", "Name tote bag", 6, None, 0, "Fall festival"), (21, "Local / Instagram", "Personalised hand towel", 8, None, 0, "Housewarming set"),
         (17, "Etsy", "Wildflower back hoodie + name", 1, None, "etsy", ""), (12, "Bulk / team order", "Logo tee (left chest)", 24, None, 0, "Bright Smile Dental"),
         (8, "Etsy", "Monogram sweatshirt", 1, None, "etsy", ""), (5, "Website", "Personalised hand towel", 4, None, 2.1, ""), (2, "Etsy", "Baby name onesie", 2, None, "etsy", "")]
for i, (back, ch, p, q, price, fees, note) in enumerate(sales):
    r = 6 + i; sa[f"A{r}"] = f"=TODAY()-{back}"; sa[f"B{r}"] = ch; sa[f"C{r}"] = p; sa[f"D{r}"] = q; sa[f"K{r}"] = note
    if price is not None: sa[f"E{r}"] = price
    sa[f"G{r}"] = fees if fees != "etsy" else f"=ROUND(F{r}*({ETX}+{PPC})+{PFX}+{LST},2)"
SD, SCH, SC, SQ, ST, SG, SH, SPF = (f"Sales!${c}$6:${c}${NSALE}" for c in "ABCDFGHI")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Sales, Orders and Blanks & Supplies.", 9)
widths(d, {"A": 32, "B": 15, "C": 14, "D": 14, "E": 14, "F": 4, "G": 32, "H": 12, "I": 14})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{SD},">="&DATE($B$4,1,1),{SD},"<"&DATE($B$4+1,1,1)'
OPEN = f'"<>Shipped",Orders!$G$6:$G${NO},"<>Cancelled"'
kpi = [("Sales", f"=SUMIFS({ST},{yr})", USD), ("Profit", f"=SUMIFS({SPF},{yr})", USD), ("Items sold", f"=SUMIFS({SQ},{yr})", "#,##0"),
       ("Profit margin", '=IF(B6=0,"",B7/B6)', "0%"),
       ("Open orders", f'=COUNTIFS(Orders!$C$6:$C${NO},"<>",Orders!$G$6:$G${NO},{OPEN})', "0"),
       ("Pieces still to stitch", f'=SUMIFS(Orders!$E$6:$E${NO},Orders!$G$6:$G${NO},"<>Finishing",Orders!$G$6:$G${NO},{OPEN})', "#,##0"),
       ("Balance still to collect", f'=SUMIFS(Orders!$M$6:$M${NO},Orders!$G$6:$G${NO},{OPEN})', USD),
       ("Orders late / need attention", f'=COUNTIF(Orders!$O$6:$O${NO},"LATE")+COUNTIF(Orders!$O$6:$O${NO},"Chase proof")', "0"),
       ("Blanks & supplies to reorder", f"=COUNTIF('Blanks & Supplies'!$H$6:$H${NS},\"Reorder\")", "0")]
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
header(d, 16, ["Product", "Items sold", "Profit"], t, start=7)
for i in range(12):
    r = 17 + i
    d[f"G{r}"] = f"=IF('Product Pricing'!A{6 + i}=\"\",\"\",'Product Pricing'!A{6 + i})"; d[f"G{r}"].font = Font(name=F, size=11)
    calc(d, f"H{r}", f'=IF(G{r}="","",SUMIFS({SQ},{SC},G{r},{yr}))', "#,##0")
    calc(d, f"I{r}", f'=IF(G{r}="","",SUMIFS({SPF},{SC},G{r},{yr}))', USD)
label(d, "G29", "Shows your first 12 products from Product Pricing.", italic=True, size=9, color=GREY)

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
