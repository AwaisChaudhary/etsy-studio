"""Nail Tech Business Spreadsheet (batch 8, lane a, beauty services): service menu pricing calculator (product cost per service,
overhead per hour, break-even and suggested price, profit per hour), client records (nail shape, length, colours, allergy notes,
next fill / rebalance due, Due / Lapsed status), appointment log with nail art add-ons, tips, no-shows and rebooking, supplies
with cost per use and open-by dates, expenses and a dashboard. Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.utils import get_column_letter as gl
import datetime as _dt

t = Theme("2E3550", "D9677E", "F7EAEE")
wb = Workbook()
NS, NM, NC, NA, NE = 80, 35, 405, 1006, 306
USD, USD4 = '"$"#,##0.00', '"$"#,##0.000'
GREY = "6F6A7A"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Nail Tech Business Spreadsheet", "Price every set, fill and add-on so it really pays you, keep client nail records, and see who is due for a fill.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly pay goal, monthly fixed costs (chair or suite rent, insurance, booking app), hours you work a month, card fees and fill timing.",
         "Supplies: add tips, gels, polishes, acrylic powder and liquid, files, buffers and other disposables with pack price and how many services a pack gives you.",
         "Service Menu: one row per service (Gel-X, acrylic full set and fill, BIAB, gel manicure, pedicure...). Type the minutes, pick the products it uses and your price. Break-even, suggested price and profit per hour appear.",
         "Clients: one row per client with nail shape, length, favourite colours and allergy notes. Visits, total spent, last visit and next fill due fill in.",
         "Appointments: log every appointment. Price comes from your menu (or type a different one), plus nail art and add-ons, tips, no-shows and whether they rebooked.",
         "Expenses and Dashboard: log costs; income, add-on income, profit, average ticket, rebook rate, no-show rate and clients due for a fill update for you."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Client details are personal information: keep this file private (a password-protected drive or a Google account only you use), "
      "and follow the privacy and record-keeping rules where you work. Allergy notes are a record for you, not medical advice.", size=10, color="8A3B2E")
s.row_dimensions[14].height = 44
label(s, "B15", "Example clients, services and appointments are included so you can see how it works: type over them or delete them. "
      "Prices in the examples are illustrations only. Works in Excel and Google Sheets.", italic=True, size=10)
s.row_dimensions[15].height = 30

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your numbers. The menu and dashboard use these.", 4)
widths(st, {"A": 46, "B": 16, "C": 4, "D": 64})
rows = [("Hourly pay goal (what you want to earn)", 30, USD, "Your pay for time with a client, before costs."),
        ("Monthly fixed costs", 600, USD, "Chair or suite rent, insurance, booking app, phone, marketing, education."),
        ("Hours with clients per month", 110, "0", "For example 27 hours a week."),
        ("Card fee (%)", 0.029, "0.0%", "Estimate, check your payment provider."),
        ("Card fee (fixed per payment)", 0.30, USD, None),
        ("Round menu prices up to the nearest", 5, USD, "Use 5 for clean prices like $45 and $65."),
        ("Usual weeks between fills", 3, "0", "Used when a client has no fill timing typed."),
        ("Client counts as lapsed after (weeks)", 8, "0", None),
        ("Set aside for tax (%)", 0.20, "0%", "A reminder figure on the dashboard, not tax advice.")]
for i, (a, v, fmt, n) in enumerate(rows):
    label(st, f"A{5 + i}", a); inp(st, f"B{5 + i}", v, fmt, n)
    if n: label(st, f"D{5 + i}", n, size=9, color=GREY, italic=True)
PAY, FIX, HRS, CPC, CFX, RND, FILLW, LAPSE, TAX = (f"Settings!$B${5 + i}" for i in range(9))
label(st, "A15", "Overhead cost per hour", bold=True); calc(st, "B15", f"=IFERROR({FIX}/{HRS},0)", USD)
OH = "Settings!$B$15"
label(st, "D15", "Fixed costs shared over every hour you work. Every service has to cover this before you earn anything.", size=9, color=GREY, italic=True)
SHAPES = "Almond,Coffin / ballerina,Square,Squoval,Oval,Round,Stiletto,Lipstick,Natural"
LENS = "Natural,Short,Medium,Long,Extra long"

# ---------- Supplies ----------
su = wb.create_sheet("Supplies")
banner(su, t, "Supplies", "Pack price and how many services a pack gives you = cost of each use. Track open dates for gels and liquids.", 12)
header(su, 5, ["Supply", "Type", "Pack price", "Uses per pack", "Cost per use", "On hand (packs)", "Reorder at", "Stock status", "Opened on", "Use within (weeks)", "Replace by", "Notes"], t)
su.row_dimensions[5].height = 44
widths(su, {"A": 34, "B": 13, "C": 11, "D": 11, "E": 11, "F": 11, "G": 10, "H": 12, "I": 12, "J": 11, "K": 14, "L": 30}); su.freeze_panes = "B6"
for r in range(6, NS + 1):
    for col in "ABCDFGIJL": inp(su, f"{col}{r}")
    for col in "AL": su[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    su[f"C{r}"].number_format = USD; su[f"I{r}"].number_format = "dd mmm yyyy"
    calc(su, f"E{r}", f'=IF(OR(A{r}="",N(D{r})=0,C{r}=""),"",C{r}/D{r})', USD4)
    calc(su, f"H{r}", f'=IF(OR(A{r}="",F{r}=""),"",IF(F{r}<=N(G{r}),"Reorder","OK"))')
    calc(su, f"K{r}", f'=IF(OR(I{r}="",J{r}=""),"",IF(TODAY()>I{r}+7*J{r},"REPLACE NOW",TEXT(I{r}+7*J{r},"dd mmm yyyy")))')
ex = [("Soft gel tips (500, 12 sizes)", "Tips", 24.99, 30, 3, 1, None, None, "About 30 full sets a box"),
      ("Tip adhesive gel + primer", "Gel", 19.99, 40, 2, 1, -20, 26, ""),
      ("Builder gel / BIAB 30 g", "Gel", 32.99, 25, 2, 1, -35, 26, ""),
      ("Gel polish colour (average bottle)", "Gel", 9.99, 30, 40, 10, None, None, "Your colour wall: one average"),
      ("Base + top coat set", "Gel", 21.99, 60, 2, 1, -14, 26, ""),
      ("Acrylic powder 4 oz", "Acrylic", 26.99, 30, 3, 1, None, None, ""),
      ("Monomer liquid 16 oz", "Acrylic", 39.99, 40, 1, 1, -40, 52, ""),
      ("Files, buffers + sanding bands (per client)", "Disposables", 22.99, 50, 2, 1, None, None, "Single-use kit"),
      ("Lint-free wipes, cleanser, cuticle oil", "Disposables", 18.99, 80, 1, 1, None, None, ""),
      ("Acetone + foil wraps (soak-off)", "Disposables", 14.99, 30, 1, 1, None, None, ""),
      ("Chrome / foil / decals (per set)", "Nail art", 15.99, 40, 1, 1, None, None, "Nail art add-ons"),
      ("Pedicure liner + kit (per client)", "Pedicure", 39.99, 50, 1, 1, None, None, "")]
for i, (n, ty, pr, uses, oh, ro, opened, wk, note) in enumerate(ex):
    r = 6 + i
    for col, v in zip("ABCDFGL", (n, ty, pr, uses, oh, ro, note)): su[f"{col}{r}"] = v
    if opened is not None: su[f"I{r}"] = f"=TODAY(){opened:+d}"; su[f"J{r}"] = wk
dv_list(su, f"B6:B{NS}", "Tips,Gel,Acrylic,Dip,Polish,Disposables,Nail art,Pedicure,Retail,Other")
su.conditional_formatting.add(f"H6:H{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
su.conditional_formatting.add(f"K6:K{NS}", CellIsRule(operator="equal", formula=['"REPLACE NOW"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
SNAME, SUSE = (f"Supplies!${c}$6:${c}${NS}" for c in "AE")
SLIST = f"=Supplies!$A$6:$A${NS}"

def look(ref):
    return f'IF({ref}="",0,IFERROR(INDEX({SUSE},MATCH({ref},{SNAME},0)),0))'

# ---------- Service Menu ----------
sm = wb.create_sheet("Service Menu")
banner(sm, t, "Service menu & pricing", "Is every service paying you? Type the minutes and your price, pick the products it uses.", 20)
cols = ["Service", "Minutes", "Main product", "Uses", "Second product", "Uses", "Other product 1", "Other product 2", "Your price",
        "Product cost", "Overhead share", "BREAK-EVEN PRICE", "Suggested price", "Card fee", "Your profit", "Profit per hour", "Price check"]
header(sm, 5, cols, t); sm.row_dimensions[5].height = 46
for i, w in enumerate([28, 9, 28, 7, 28, 7, 30, 30, 11, 10, 11, 13, 12, 9, 11, 11, 14]): sm.column_dimensions[gl(i + 1)].width = w
sm.freeze_panes = "B6"
label(sm, "A4", "Uses: 1 = one service from that supply's 'uses per pack'. A fill often uses about half (type 0.5). Suggested price = costs + your hourly pay goal.",
      italic=True, size=9, color=GREY)
for r in range(6, NM + 1):
    for col in "ABCDEFGHI": inp(sm, f"{col}{r}")
    for col in "ACEGH": sm[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sm[f"I{r}"].number_format = USD
    on = f'A{r}=""'
    calc(sm, f"J{r}", f'=IF({on},"",IF(C{r}="",0,IF(D{r}="",1,D{r}))*{look(f"C{r}")}+IF(E{r}="",0,IF(F{r}="",1,F{r}))*{look(f"E{r}")}+{look(f"G{r}")}+{look(f"H{r}")})', USD)
    calc(sm, f"K{r}", f'=IF({on},"",N(B{r})/60*{OH})', USD)
    calc(sm, f"L{r}", f'=IF({on},"",J{r}+K{r})', USD, bold=True)
    calc(sm, f"M{r}", f'=IF({on},"",CEILING((J{r}+K{r}+N(B{r})/60*{PAY}+{CFX})/(1-{CPC}),{RND}))', USD, bold=True)
    calc(sm, f"N{r}", f'=IF(OR({on},I{r}=""),"",I{r}*{CPC}+{CFX})', USD)
    calc(sm, f"O{r}", f'=IF(OR({on},I{r}=""),"",I{r}-J{r}-K{r}-N{r})', USD, bold=True)
    calc(sm, f"P{r}", f'=IF(OR(O{r}="",N(B{r})=0),"",O{r}/(B{r}/60))', USD, bold=True)
    calc(sm, f"Q{r}", f'=IF(O{r}="","",IF(O{r}<0,"Losing money",IF(I{r}<M{r},"Below goal","On target")))')
F1, F2 = "Files, buffers + sanding bands (per client)", "Lint-free wipes, cleanser, cuticle oil"
svc = [("Gel-X full set", 90, "Soft gel tips (500, 12 sizes)", 1, "Tip adhesive gel + primer", 1, F1, F2, 65),
       ("Acrylic full set", 90, "Acrylic powder 4 oz", 1, "Monomer liquid 16 oz", 1, F1, F2, 60),
       ("Acrylic fill (2-3 weeks)", 60, "Acrylic powder 4 oz", 0.5, "Monomer liquid 16 oz", 0.5, F1, F2, 45),
       ("BIAB / builder gel overlay", 75, "Builder gel / BIAB 30 g", 1, "Base + top coat set", 1, F1, F2, 55),
       ("BIAB infill", 60, "Builder gel / BIAB 30 g", 0.5, "Base + top coat set", 1, F1, F2, 45),
       ("Gel manicure", 45, "Gel polish colour (average bottle)", 1, "Base + top coat set", 1, F1, F2, 40),
       ("Soak-off removal", 20, "Acetone + foil wraps (soak-off)", 1, None, None, F2, None, 15),
       ("Gel pedicure", 60, "Pedicure liner + kit (per client)", 1, "Gel polish colour (average bottle)", 1, "Base + top coat set", F2, 55),
       ("Nail art: chrome or French (add-on)", 15, "Chrome / foil / decals (per set)", 1, None, None, None, None, 10)]
for i, row in enumerate(svc):
    for j, v in enumerate(row):
        if v is not None: sm.cell(6 + i, 1 + j).value = v
for rng in (f"C6:C{NM}", f"E6:E{NM}", f"G6:H{NM}"): dv_list(sm, rng, SLIST)
sm.conditional_formatting.add(f"Q6:Q{NM}", CellIsRule(operator="equal", formula=['"Losing money"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
sm.conditional_formatting.add(f"Q6:Q{NM}", CellIsRule(operator="equal", formula=['"Below goal"'], fill=amb, font=Font(name=F, bold=True, color="8A5A12")))
sm.conditional_formatting.add(f"Q6:Q{NM}", CellIsRule(operator="equal", formula=['"On target"'], fill=grn, font=Font(name=F, bold=True, color="2E6B3A")))
legend(sm, NM + 2, 1)
MNAME, MPRICE, MCOST = (f"'Service Menu'!${c}$6:${c}${NM}" for c in "AIJ")

# ---------- Appointments ----------
ap = wb.create_sheet("Appointments")
banner(ap, t, "Appointment log", "One row per appointment. Price comes from your menu unless you type a different one. Add nail art and extras in Add-ons.", 15)
cols = ["Date", "Client", "Service", "Price (blank = menu)", "Nail art / add-ons", "Tip", "Paid by", "Status", "Rebooked?", "Notes",
        "Charged", "Product cost", "Card fee", "Profit (before overheads)", "Month"]
header(ap, 5, cols, t); ap.row_dimensions[5].height = 44
widths(ap, {"A": 13, "B": 20, "C": 26, "D": 12, "E": 11, "F": 8, "G": 10, "H": 11, "I": 10, "J": 24, "K": 11, "L": 11, "M": 9, "N": 13, "O": 8})
ap.freeze_panes = "B6"
for r in range(6, NA + 1):
    for col in "ABCDEFGHIJ": inp(ap, f"{col}{r}")
    for col in "BCJ": ap[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    ap[f"A{r}"].number_format = "dd mmm yyyy"
    for col in "DEF": ap[f"{col}{r}"].number_format = USD
    done = f'OR(C{r}="",H{r}="No-show",H{r}="Cancelled")'
    calc(ap, f"K{r}", f'=IF(C{r}="","",IF(OR(H{r}="No-show",H{r}="Cancelled"),N(D{r}),IF(D{r}="",IFERROR(INDEX({MPRICE},MATCH(C{r},{MNAME},0)),0),D{r})+N(E{r})))', USD)
    calc(ap, f"L{r}", f'=IF({done},"",IFERROR(INDEX({MCOST},MATCH(C{r},{MNAME},0)),0))', USD)
    calc(ap, f"M{r}", f'=IF(OR(C{r}="",G{r}<>"Card",H{r}="Booked"),"",(K{r}+N(F{r}))*{CPC}+{CFX})', USD)
    calc(ap, f"N{r}", f'=IF(OR(C{r}="",H{r}="Booked"),"",K{r}+N(F{r})-N(L{r})-N(M{r}))', USD, bold=True)
    calc(ap, f"O{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(ap, f"C6:C{NA}", "=" + MNAME); dv_list(ap, f"G6:G{NA}", "Card,Cash,Transfer,App,Gift card")
dv_list(ap, f"H6:H{NA}", "Done,No-show,Cancelled,Booked"); dv_list(ap, f"I6:I{NA}", "Yes,No")
dv_list(ap, f"B6:B{NA}", f"=Clients!$A$6:$A${NC}")
ap.conditional_formatting.add(f"H6:H{NA}", CellIsRule(operator="equal", formula=['"No-show"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
ap.conditional_formatting.add(f"H6:H{NA}", CellIsRule(operator="equal", formula=['"Booked"'], fill=amb, font=Font(name=F, color="8A5A12")))
appts = [(-50, "Maya R.", "Gel-X full set", None, 12, 10, "Card", "Done", "Yes", "Almond, medium, nude + chrome"),
         (-29, "Maya R.", "Soak-off removal", None, None, None, "Card", "Done", "Yes", "Before new set"),
         (-29, "Maya R.", "Gel-X full set", None, 20, 12, "Card", "Done", "Yes", "Holiday red + gold foil"),
         (-44, "Chloe B.", "Acrylic full set", None, 0, 10, "Cash", "Done", "Yes", "Coffin, long"),
         (-22, "Chloe B.", "Acrylic fill (2-3 weeks)", None, 8, 8, "Cash", "Done", "Yes", ""),
         (-1, "Chloe B.", "Acrylic fill (2-3 weeks)", None, 0, 8, "Cash", "Done", "Yes", ""),
         (-63, "Grace O.", "BIAB / builder gel overlay", None, 0, 10, "App", "Done", "No", "Short squoval"),
         (-18, "Sofia L.", "Gel manicure", None, 0, 6, "Card", "Done", "No", ""),
         (-11, "Ava T.", "Gel pedicure", None, 0, 10, "Card", "Done", "Yes", ""),
         (-6, "Jade K.", "Gel-X full set", 25, None, None, None, "No-show", "No", "Deposit kept"),
         (4, "Ava T.", "Gel manicure", None, None, None, None, "Booked", None, ""),
         (-55, "Lena P.", "Acrylic full set", None, 15, 10, "Card", "Done", "Yes", "Square, medium"),
         (-34, "Lena P.", "Acrylic fill (2-3 weeks)", None, 10, 8, "Card", "Done", "Yes", ""),
         (-13, "Lena P.", "Acrylic fill (2-3 weeks)", None, 10, 8, "Card", "Done", "Yes", ""),
         (-41, "Hana M.", "Gel-X full set", None, 15, 12, "App", "Done", "Yes", ""),
         (-20, "Hana M.", "Gel-X full set", None, 25, 12, "App", "Done", "Yes", "Birthday set, 3D charms"),
         (-48, "Rosa D.", "BIAB / builder gel overlay", None, 0, 8, "Card", "Done", "Yes", ""),
         (-21, "Rosa D.", "BIAB infill", None, 10, 8, "Card", "Done", "Yes", ""),
         (-3, "Rosa D.", "BIAB infill", None, 0, 8, "Card", "Done", "Yes", ""),
         (-27, "Ivy C.", "Gel pedicure", None, 0, 10, "Cash", "Done", "No", ""),
         (-8, "Ivy C.", "Gel manicure", None, 10, 6, "Cash", "Done", "Yes", "Chrome")]
for i, (dd, cl, sv, pr, add, tip, pb, sta, rb, note) in enumerate(appts):
    r = 6 + i; ap[f"A{r}"] = f"=TODAY(){dd:+d}"
    for col, v in zip("BCDEFGHIJ", (cl, sv, pr, add, tip, pb, sta, rb, note)):
        if v is not None: ap[f"{col}{r}"] = v
AD, AC, AS, AST, ACH, ATIP, APF, ARB, AK, AL, AADD = (f"Appointments!${c}$6:${c}${NA}" for c in "ABCHKFNILME")

# ---------- Clients ----------
cl = wb.create_sheet("Clients")
banner(cl, t, "Client records", "Shape, length, colours and notes for every client. Visits, spend and next fill date fill in from Appointments.", 16)
cols = ["Client name", "Phone", "Email / Instagram", "Birthday", "Usual service", "Nail shape", "Length", "Favourite colours / style",
        "Allergies / sensitivities", "Fill every (weeks)", "Visits", "Total spent (incl. tips)", "Last visit", "Next fill due", "Status", "Notes"]
header(cl, 5, cols, t); cl.row_dimensions[5].height = 44
for i, w in enumerate([18, 13, 22, 10, 24, 14, 10, 26, 22, 9, 7, 12, 13, 13, 11, 24]): cl.column_dimensions[gl(i + 1)].width = w
cl.freeze_panes = "B6"
for r in range(6, NC + 1):
    for col in "ABCDEFGHIJP": inp(cl, f"{col}{r}")
    for col in "ACEHIP": cl[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    cl[f"D{r}"].number_format = "dd mmm"
    on = f'A{r}=""'
    calc(cl, f"K{r}", f'=IF({on},"",COUNTIFS({AC},A{r},{AST},"Done",{AS},"<>Soak-off removal"))', "0")
    calc(cl, f"L{r}", f'=IF({on},"",SUMIFS({ACH},{AC},A{r},{AST},"Done")+SUMIFS({ATIP},{AC},A{r},{AST},"Done"))', USD)
    calc(cl, f"M{r}", f'=IF(OR({on},COUNTIFS({AC},A{r},{AST},"Done")=0),"",_xlfn.MAXIFS({AD},{AC},A{r},{AST},"Done"))', "dd mmm yyyy")
    calc(cl, f"N{r}", f'=IF(M{r}="","",M{r}+7*IF(J{r}="",{FILLW},J{r}))', "ddd dd mmm")
    calc(cl, f"O{r}", f'=IF({on},"",IF(N{r}="","New",IF(COUNTIFS({AC},A{r},{AST},"Booked",{AD},">="&TODAY())>0,"Booked",IF(TODAY()-M{r}>7*{LAPSE},"Lapsed",IF(TODAY()>=N{r},"Due now",IF(N{r}-TODAY()<=5,"Due soon","OK"))))))')
clients = [("Maya R.", "555-0132", "@maya.nails", "1995-04-18", "Gel-X full set", "Almond", "Medium", "Nudes, chrome, seasonal sets", "", 3, ""),
           ("Chloe B.", "555-0158", "chloe.b@example.com", "1999-09-03", "Acrylic fill (2-3 weeks)", "Coffin / ballerina", "Long", "Pinks, ombre, French", "", 3, "Prefers Saturdays"),
           ("Grace O.", "555-0104", "@graceo", "1987-01-26", "BIAB infill", "Squoval", "Short", "Sheer pink", "Gentle on cuticles", 4, ""),
           ("Sofia L.", "555-0171", "@sofial", None, "Gel manicure", "Oval", "Short", "Reds", "HEMA-free gels only", 3, ""),
           ("Ava T.", "555-0189", "@avat", "2001-06-12", "Gel manicure", "Round", "Natural", "Pastels", "", 3, "Pedicure every 6 weeks"),
           ("Jade K.", "555-0117", "@jadek", None, "Gel-X full set", "Stiletto", "Extra long", "Black, jewels", "", 3, ""),
           ("Lena P.", "555-0146", "@lena.p", "1993-08-09", "Acrylic fill (2-3 weeks)", "Square", "Medium", "Milky white, French", "", 3, ""),
           ("Hana M.", "555-0163", "@hanam", "1997-11-20", "Gel-X full set", "Almond", "Long", "Charms, cat eye", "", 3, ""),
           ("Rosa D.", "555-0128", "rosa.d@example.com", "1984-02-02", "BIAB infill", "Oval", "Short", "Nude, sheer", "", 3, ""),
           ("Ivy C.", "555-0192", "@ivyc", None, "Gel manicure", "Round", "Short", "Brights", "", 4, "")]
for i, row in enumerate(clients):
    r = 6 + i
    for col, v in zip("ABCDEFGHIJP", row):
        if v not in ("", None):
            cl[f"{col}{r}"] = _dt.date.fromisoformat(v) if col == "D" else v
dv_list(cl, f"E6:E{NC}", "=" + MNAME); dv_list(cl, f"F6:F{NC}", SHAPES); dv_list(cl, f"G6:G{NC}", LENS)
for val, fill, col in (('"Due now"', red, "A12A1E"), ('"Lapsed"', PatternFill("solid", fgColor="E6E1E8"), "5A4D5E"), ('"Due soon"', amb, "8A5A12"),
                       ('"Booked"', grn, "2E6B3A"), ('"OK"', grn, "2E6B3A"), ('"New"', amb, "8A5A12")):
    cl.conditional_formatting.add(f"O6:O{NC}", CellIsRule(operator="equal", formula=[val], fill=fill, font=Font(name=F, bold=True, color=col)))

# ---------- Expenses ----------
xp = wb.create_sheet("Expenses")
banner(xp, t, "Expenses", "Everything you spend on the business: supplies, rent, insurance, courses, marketing.", 6)
header(xp, 5, ["Date", "Category", "What", "Amount", "Month", "Notes"], t)
widths(xp, {"A": 13, "B": 16, "C": 32, "D": 12, "E": 8, "F": 28}); xp.freeze_panes = "A6"
CAT = "Supplies,Rent / chair,Insurance,Booking app,Marketing,Education,Equipment,Other"
for r in range(6, NE + 1):
    for col in "ABCDF": inp(xp, f"{col}{r}")
    for col in "CF": xp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    xp[f"A{r}"].number_format = "dd mmm yyyy"; xp[f"D{r}"].number_format = USD
    calc(xp, f"E{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(xp, f"B6:B{NE}", CAT)
for i, (dd, c, w, a) in enumerate([(-28, "Rent / chair", "Chair rent", 420), (-24, "Supplies", "Gel + tips restock", 112.46),
                                   (-20, "Booking app", "Monthly plan", 30), (-14, "Insurance", "Monthly premium", 28), (-6, "Equipment", "New e-file bits", 34.99)]):
    r = 6 + i; xp[f"A{r}"] = f"=TODAY(){dd:+d}"; xp[f"B{r}"] = c; xp[f"C{r}"] = w; xp[f"D{r}"] = a
XD, XC, XA = (f"Expenses!${c}$6:${c}${NE}" for c in "ABD")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Appointments, Clients and Expenses.", 9)
widths(d, {"A": 32, "B": 15, "C": 13, "D": 13, "E": 13, "F": 13, "G": 4, "H": 30, "I": 12, "J": 13})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{AD},">="&DATE($B$4,1,1),{AD},"<"&DATE($B$4+1,1,1)'
xyr = f'{XD},">="&DATE($B$4,1,1),{XD},"<"&DATE($B$4+1,1,1)'
kpi = [("Income (services, add-ons, no-show fees)", f'=SUMIFS({ACH},{AST},"<>Booked",{yr})', USD),
       ("of which nail art / add-ons", f'=SUMIFS({AADD},{AST},"Done",{yr})', USD),
       ("Tips", f'=SUMIFS({ATIP},{AST},"Done",{yr})', USD),
       ("Expenses", f"=SUMIFS({XA},{xyr})", USD),
       ("Profit (income + tips - card fees - expenses)", f"=B6+B8-SUMIFS({AL},{yr})-B9", USD),
       ("Appointments done", f'=COUNTIFS({AST},"Done",{yr})', "0"),
       ("Average ticket (incl. tips)", f'=IF(B11=0,"",(SUMIFS({ACH},{AST},"Done",{yr})+B8)/B11)', USD),
       ("Rebook rate", f'=IF(B11=0,"",COUNTIFS({AST},"Done",{ARB},"Yes",{yr})/B11)', "0%"),
       ("No-show rate", f'=IFERROR(COUNTIFS({AST},"No-show",{yr})/(B11+COUNTIFS({AST},"No-show",{yr})),"")', "0%"),
       ("Clients due now", f'=COUNTIF(Clients!$O$6:$O${NC},"Due now")', "0"),
       ("Clients due in 5 days", f'=COUNTIF(Clients!$O$6:$O${NC},"Due soon")', "0"),
       ("Set aside for tax", f"=MAX(0,B10)*{TAX}", USD)]
for i, (a, f, fmt) in enumerate(kpi):
    r = 6 + i; label(d, f"A{r}", a, bold=True, size=11); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 28
label(d, "A18", "Expenses include supplies you buy, so product cost is not taken off twice. No-show and late-cancel fees you keep (type them in Price) count as income.", italic=True, size=9, color=GREY)
d.merge_cells("A18:F18")
header(d, 20, ["Month", "Income", "Tips", "Expenses", "Profit", "Appointments"], t)
for i, mn in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    r = 21 + i; label(d, f"A{r}", mn)
    mr = f'{AD},">="&DATE($B$4,{i + 1},1),{AD},"<"&DATE($B$4,{i + 2},1)'
    xm = f'{XD},">="&DATE($B$4,{i + 1},1),{XD},"<"&DATE($B$4,{i + 2},1)'
    calc(d, f"B{r}", f'=SUMIFS({ACH},{AST},"<>Booked",{mr})', USD)
    calc(d, f"C{r}", f'=SUMIFS({ATIP},{AST},"Done",{mr})', USD)
    calc(d, f"D{r}", f"=SUMIFS({XA},{xm})", USD)
    calc(d, f"E{r}", f"=B{r}+C{r}-D{r}-SUMIFS({AL},{mr})", USD)
    calc(d, f"F{r}", f'=COUNTIFS({AST},"Done",{mr})', "0")
label(d, "A33", "Total", bold=True)
for col in "BCDEF": calc(d, f"{col}33", f"=SUM({col}21:{col}32)", "0" if col == "F" else USD, bold=True)
header(d, 5, ["Service", "Booked (done)", "Income"], t, start=8)
for i in range(12):
    r = 6 + i
    d[f"H{r}"] = f"=IF('Service Menu'!A{6 + i}=\"\",\"\",'Service Menu'!A{6 + i})"; d[f"H{r}"].font = Font(name=F, size=11)
    calc(d, f"I{r}", f'=IF(H{r}="","",COUNTIFS({AS},H{r},{AST},"Done",{yr}))', "0")
    calc(d, f"J{r}", f'=IF(H{r}="","",SUMIFS({ACH},{AS},H{r},{AST},"Done",{yr}))', USD)
header(d, 20, ["Expense category", "This year"], t, start=8)
for i, c in enumerate(CAT.split(",")):
    r = 21 + i; label(d, f"H{r}", c); calc(d, f"I{r}", f'=SUMIFS({XA},{XC},H{r},{xyr})', USD)

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
