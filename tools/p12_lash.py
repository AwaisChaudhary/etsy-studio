"""Lash Tech Business Spreadsheet (batch 7, lane a, beauty services): service menu pricing calculator (product cost per set,
break-even and suggested price, profit per hour), client records (lash map, curl, length, patch test, next fill due,
Due / Lapsed status), appointment log (tips, no-shows, rebooking), supplies with adhesive open dates and replace-by dates,
expenses and a dashboard (income, rebook rate, no-show rate, average ticket, clients due). Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.utils import get_column_letter as gl

t = Theme("3A2A3F", "C98A7B", "F5ECEA")
wb = Workbook()
NS, NM, NC, NA, NE = 80, 30, 405, 1006, 306
USD, USD4 = '"$"#,##0.00', '"$"#,##0.000'
GREY = "736570"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Lash Tech Business Spreadsheet", "Price every set and fill with confidence, keep client lash records, and see who is due for a fill.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Settings: your hourly pay goal, monthly fixed costs (rent, insurance, booking app), hours you work a month, card fees and fill timing.",
         "Supplies: add lash trays, adhesive, primer, pads, tape and other disposables with pack price. Adhesive: type the date you opened it to see the replace-by date.",
         "Service Menu: one row per service. Type the minutes, pick the products a service uses and your price. Break-even, suggested price and profit per hour appear.",
         "Clients: one row per client with lash map, curl, lengths, thickness, patch test date and notes. Visits, total spent, last visit and next fill due fill in.",
         "Appointments: log every appointment. Price comes from your menu (or type a different one), plus tips, no-shows and whether they rebooked.",
         "Expenses and Dashboard: log costs; income, profit, average ticket, rebook rate, no-show rate and clients due for a fill update for you."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Client details are personal information: keep this file private (a password-protected drive or a Google account only you use), "
      "and follow the privacy and record-keeping rules where you work. Patch test and allergy notes are a record for you, not medical advice.", size=10, color="8A3B2E")
s.row_dimensions[14].height = 44
label(s, "B15", "Example clients, services and appointments are included so you can see how it works: type over them or delete them. "
      "Prices in the examples are illustrations only. Works in Excel and Google Sheets.", italic=True, size=10)
s.row_dimensions[15].height = 30

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your numbers. The menu and dashboard use these.", 4)
widths(st, {"A": 46, "B": 16, "C": 4, "D": 64})
rows = [("Hourly pay goal (what you want to earn)", 35, USD, "Your pay for time with a client, before costs."),
        ("Monthly fixed costs", 650, USD, "Suite or chair rent, insurance, booking app, phone, marketing, education."),
        ("Hours with clients per month", 100, "0", "For example 25 hours a week."),
        ("Card fee (%)", 0.029, "0.0%", "Estimate, check your payment provider."),
        ("Card fee (fixed per payment)", 0.30, USD, None),
        ("Round menu prices up to the nearest", 5, USD, "Use 5 for clean prices like $85 and $120."),
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
CURL = "J,B,C,CC,D,DD,L,M"; STY = "Classic,Hybrid,Volume,Mega volume,Wet look,Wispy,Lash lift,Other"

# ---------- Supplies ----------
su = wb.create_sheet("Supplies")
banner(su, t, "Supplies", "Pack price and pack size give the cost of each use. Adhesive: track open dates.", 12)
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
ex = [("Classic lash tray 0.15 C mix", "Lashes", 18.99, 3, 4, 2, None, None, "About 3 full sets a tray"),
      ("Volume lash tray 0.07 D mix", "Lashes", 21.99, 2, 3, 2, None, None, ""),
      ("Easy-fan lashes 0.05 CC", "Lashes", 24.99, 2.5, 2, 2, None, None, ""),
      ("Lash adhesive 5 ml", "Adhesive", 29.99, 40, 2, 1, -32, 6, "Replace about 6 weeks after opening"),
      ("Primer / cleanser", "Prep", 14.99, 120, 1, 1, None, None, ""),
      ("Gel eye pads (pairs)", "Disposables", 12.99, 100, 2, 1, None, None, ""),
      ("Tape, micro swabs, mascara wands", "Disposables", 16.99, 80, 1, 1, None, None, "Per client"),
      ("Lash lift kit (perm, fix, nourish)", "Lift", 44.99, 25, 1, 1, None, None, ""),
      ("Tint (black)", "Lift", 12.99, 30, 1, 1, None, None, ""),
      ("Aftercare cleanser (retail)", "Retail", 48, 12, 1, 1, None, None, "Sold to clients")]
for i, (n, ty, pr, uses, oh, ro, opened, wk, note) in enumerate(ex):
    r = 6 + i
    for col, v in zip("ABCDFGL", (n, ty, pr, uses, oh, ro, note)): su[f"{col}{r}"] = v
    if opened is not None: su[f"I{r}"] = f"=TODAY(){opened:+d}"; su[f"J{r}"] = wk
dv_list(su, f"B6:B{NS}", "Lashes,Adhesive,Prep,Disposables,Lift,Retail,Other")
su.conditional_formatting.add(f"H6:H{NS}", CellIsRule(operator="equal", formula=['"Reorder"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
su.conditional_formatting.add(f"K6:K{NS}", CellIsRule(operator="equal", formula=['"REPLACE NOW"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
SNAME, SUSE = (f"Supplies!${c}$6:${c}${NS}" for c in "AE")
SLIST = f"=Supplies!$A$6:$A${NS}"

def look(ref):
    return f'IF({ref}="",0,IFERROR(INDEX({SUSE},MATCH({ref},{SNAME},0)),0))'

# ---------- Service Menu ----------
sm = wb.create_sheet("Service Menu")
banner(sm, t, "Service menu & pricing", "Is every service paying you? Type the minutes and your price, pick the products it uses.", 20)
cols = ["Service", "Minutes", "Lashes", "Lash uses", "Adhesive", "Adhesive uses", "Other product 1", "Other product 2", "Your price",
        "Product cost", "Overhead share", "BREAK-EVEN PRICE", "Suggested price", "Card fee", "Your profit", "Profit per hour", "Price check"]
header(sm, 5, cols, t); sm.row_dimensions[5].height = 46
for i, w in enumerate([28, 9, 28, 8, 20, 9, 28, 28, 11, 10, 11, 13, 12, 9, 11, 11, 14]): sm.column_dimensions[gl(i + 1)].width = w
sm.freeze_panes = "B6"
label(sm, "A4", "Lash uses: 1 = one full set from that supply's 'uses'. A fill often uses about half (type 0.5). Suggested price = costs + your hourly pay goal.",
      italic=True, size=9, color=GREY)
for r in range(6, NM + 1):
    for col in "ABCDEFGHI": inp(sm, f"{col}{r}")
    for col in "ACEGH": sm[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    sm[f"I{r}"].number_format = USD
    on = f'A{r}=""'
    calc(sm, f"J{r}", f'=IF({on},"",N(D{r})*{look(f"C{r}")}+IF(E{r}="",0,IF(F{r}="",1,F{r}))*{look(f"E{r}")}+{look(f"G{r}")}+{look(f"H{r}")})', USD)
    calc(sm, f"K{r}", f'=IF({on},"",N(B{r})/60*{OH})', USD)
    calc(sm, f"L{r}", f'=IF({on},"",J{r}+K{r})', USD, bold=True)
    calc(sm, f"M{r}", f'=IF({on},"",CEILING((J{r}+K{r}+N(B{r})/60*{PAY}+{CFX})/(1-{CPC}),{RND}))', USD, bold=True)
    calc(sm, f"N{r}", f'=IF(OR({on},I{r}=""),"",I{r}*{CPC}+{CFX})', USD)
    calc(sm, f"O{r}", f'=IF(OR({on},I{r}=""),"",I{r}-J{r}-K{r}-N{r})', USD, bold=True)
    calc(sm, f"P{r}", f'=IF(OR(O{r}="",N(B{r})=0),"",O{r}/(B{r}/60))', USD, bold=True)
    calc(sm, f"Q{r}", f'=IF(O{r}="","",IF(O{r}<0,"Losing money",IF(I{r}<M{r},"Below goal","On target")))')
svc = [("Classic full set", 120, "Classic lash tray 0.15 C mix", 1, "Lash adhesive 5 ml", 1, "Gel eye pads (pairs)", "Tape, micro swabs, mascara wands", 120),
       ("Classic fill (2-3 weeks)", 60, "Classic lash tray 0.15 C mix", 0.4, "Lash adhesive 5 ml", 0.5, "Gel eye pads (pairs)", "Tape, micro swabs, mascara wands", 65),
       ("Hybrid full set", 150, "Volume lash tray 0.07 D mix", 0.8, "Lash adhesive 5 ml", 1, "Gel eye pads (pairs)", "Tape, micro swabs, mascara wands", 150),
       ("Hybrid fill", 75, "Volume lash tray 0.07 D mix", 0.4, "Lash adhesive 5 ml", 0.5, "Gel eye pads (pairs)", "Tape, micro swabs, mascara wands", 75),
       ("Volume full set", 180, "Easy-fan lashes 0.05 CC", 1, "Lash adhesive 5 ml", 1.2, "Gel eye pads (pairs)", "Tape, micro swabs, mascara wands", 160),
       ("Volume fill", 90, "Easy-fan lashes 0.05 CC", 0.5, "Lash adhesive 5 ml", 0.6, "Gel eye pads (pairs)", "Tape, micro swabs, mascara wands", 85),
       ("Lash lift & tint", 60, None, None, None, None, "Lash lift kit (perm, fix, nourish)", "Tint (black)", 80),
       ("Lash removal", 30, None, None, None, None, "Primer / cleanser", "Gel eye pads (pairs)", 25)]
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
banner(ap, t, "Appointment log", "One row per appointment. Price comes from your menu unless you type a different one.", 15)
cols = ["Date", "Client", "Service", "Price (blank = menu)", "Tip", "Paid by", "Status", "Rebooked?", "Notes", "Charged", "Product cost", "Card fee", "Profit (before overheads)", "Month"]
header(ap, 5, cols, t); ap.row_dimensions[5].height = 44
widths(ap, {"A": 13, "B": 22, "C": 26, "D": 12, "E": 9, "F": 10, "G": 11, "H": 10, "I": 26, "J": 11, "K": 11, "L": 9, "M": 13, "N": 8})
ap.freeze_panes = "B6"
for r in range(6, NA + 1):
    for col in "ABCDEFGHI": inp(ap, f"{col}{r}")
    for col in "BCI": ap[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    ap[f"A{r}"].number_format = "dd mmm yyyy"
    for col in "DE": ap[f"{col}{r}"].number_format = USD
    done = f'OR(C{r}="",G{r}="No-show",G{r}="Cancelled")'
    calc(ap, f"J{r}", f'=IF(C{r}="","",IF(OR(G{r}="No-show",G{r}="Cancelled"),N(D{r}),IF(D{r}="",IFERROR(INDEX({MPRICE},MATCH(C{r},{MNAME},0)),0),D{r})))', USD)
    calc(ap, f"K{r}", f'=IF({done},"",IFERROR(INDEX({MCOST},MATCH(C{r},{MNAME},0)),0))', USD)
    calc(ap, f"L{r}", f'=IF(OR(C{r}="",F{r}<>"Card",G{r}="Booked"),"",(J{r}+N(E{r}))*{CPC}+{CFX})', USD)
    calc(ap, f"M{r}", f'=IF(OR(C{r}="",G{r}="Booked"),"",J{r}+N(E{r})-N(K{r})-N(L{r}))', USD, bold=True)
    calc(ap, f"N{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(ap, f"C6:C{NA}", "=" + MNAME); dv_list(ap, f"F6:F{NA}", "Card,Cash,Transfer,App,Gift card")
dv_list(ap, f"G6:G{NA}", "Done,No-show,Cancelled,Booked"); dv_list(ap, f"H6:H{NA}", "Yes,No")
dv_list(ap, f"B6:B{NA}", f"=Clients!$A$6:$A${NC}")
ap.conditional_formatting.add(f"G6:G{NA}", CellIsRule(operator="equal", formula=['"No-show"'], fill=red, font=Font(name=F, bold=True, color="A12A1E")))
ap.conditional_formatting.add(f"G6:G{NA}", CellIsRule(operator="equal", formula=['"Booked"'], fill=amb, font=Font(name=F, color="8A5A12")))
appts = [(-58, "Amara K.", "Classic full set", None, 15, "Card", "Done", "Yes", "First visit"),
         (-40, "Amara K.", "Classic fill (2-3 weeks)", None, 10, "Card", "Done", "Yes", ""),
         (-19, "Amara K.", "Classic fill (2-3 weeks)", None, 10, "Card", "Done", "Yes", ""),
         (-35, "Jess L.", "Hybrid full set", None, 20, "App", "Done", "Yes", "Wispy map"),
         (-16, "Jess L.", "Hybrid fill", None, 10, "App", "Done", "No", ""),
         (-70, "Priya S.", "Volume full set", None, 25, "Card", "Done", "No", ""),
         (-12, "Nicole B.", "Lash lift & tint", None, 10, "Cash", "Done", "No", ""),
         (-9, "Dani R.", "Volume full set", 140, 0, "Card", "Done", "Yes", "Model discount"),
         (-6, "Tasha W.", "Classic full set", None, 0, None, "No-show", "No", "Deposit kept"),
         (-2, "Dani R.", "Volume fill", None, 15, "Card", "Done", "Yes", ""),
         (5, "Jess L.", "Hybrid fill", None, None, None, "Booked", None, "")]
for i, (dd, cl, sv, pr, tip, pb, sta, rb, note) in enumerate(appts):
    r = 6 + i; ap[f"A{r}"] = f"=TODAY(){dd:+d}"
    for col, v in zip("BCDEFGHI", (cl, sv, pr, tip, pb, sta, rb, note)):
        if v is not None: ap[f"{col}{r}"] = v
ap["D14"] = 20
AD, AC, AS, AST, ACH, ATIP, APF, ARB, AK, AL = (f"Appointments!${c}$6:${c}${NA}" for c in "ABCGJEMHKL")

# ---------- Clients ----------
cl = wb.create_sheet("Clients")
banner(cl, t, "Client records", "Lash map and preferences for every client. Visits, spend and next fill date fill in from Appointments.", 19)
cols = ["Client name", "Phone", "Email / Instagram", "Birthday", "Style", "Lash map / shape", "Curl", "Lengths (mm)", "Thickness", "Patch test date",
        "Sensitivities / notes", "Fill every (weeks)", "Visits", "Total spent (incl. tips)", "Last visit", "Next fill due", "Status"]
header(cl, 5, cols, t); cl.row_dimensions[5].height = 44
for i, w in enumerate([20, 14, 22, 11, 11, 16, 7, 12, 9, 12, 28, 10, 7, 12, 13, 13, 12]): cl.column_dimensions[gl(i + 1)].width = w
cl.freeze_panes = "B6"
for r in range(6, NC + 1):
    for col in "ABCDEFGHIJKL": inp(cl, f"{col}{r}")
    for col in "ACFK": cl[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    for col in "DJ": cl[f"{col}{r}"].number_format = "dd mmm yyyy"
    cl[f"D{r}"].number_format = "dd mmm"
    on = f'A{r}=""'
    calc(cl, f"M{r}", f'=IF({on},"",COUNTIFS({AC},A{r},{AST},"Done"))', "0")
    calc(cl, f"N{r}", f'=IF({on},"",SUMIFS({ACH},{AC},A{r},{AST},"Done")+SUMIFS({ATIP},{AC},A{r},{AST},"Done"))', USD)
    calc(cl, f"O{r}", f'=IF(OR({on},M{r}=0),"",_xlfn.MAXIFS({AD},{AC},A{r},{AST},"Done"))', "dd mmm yyyy")
    calc(cl, f"P{r}", f'=IF(O{r}="","",O{r}+7*IF(L{r}="",{FILLW},L{r}))', "ddd dd mmm")
    calc(cl, f"Q{r}", f'=IF({on},"",IF(P{r}="","New",IF(COUNTIFS({AC},A{r},{AST},"Booked",{AD},">="&TODAY())>0,"Booked",IF(TODAY()-O{r}>7*{LAPSE},"Lapsed",IF(TODAY()>=P{r},"Due now",IF(P{r}-TODAY()<=5,"Due soon","OK"))))))')
clients = [("Amara K.", "555-0141", "@amara.k", "1992-03-14", "Classic", "Cat eye", "C", "9-12", "0.15", -58, "None", 3),
           ("Jess L.", "555-0177", "jess.l@example.com", "1996-07-02", "Hybrid", "Wispy", "CC", "8-13", "0.07", -35, "Watery eyes: low humidity", 3),
           ("Priya S.", "555-0109", "@priya.lashes", "1989-11-30", "Volume", "Doll eye", "D", "10-13", "0.05", -70, "", 3),
           ("Nicole B.", "555-0123", "@nicb", "1994-12-09", "Lash lift", "", "", "", "", -12, "Sensitive skin: patch tested OK", 7),
           ("Dani R.", "555-0186", "@danir", "1998-05-21", "Volume", "Open eye", "D", "9-14", "0.05", -9, "", 2),
           ("Tasha W.", "555-0195", "@tashaw", None, "Classic", "Natural", "C", "8-11", "0.15", -7, "", 3)]
import datetime as _dt
for i, (n, ph, em, bd, sty, mp, cu, ln, th, pt, nt, fw) in enumerate(clients):
    r = 6 + i
    for col, v in zip("ABCEFGHIKL", (n, ph, em, sty, mp, cu, ln, th, nt, fw)):
        if v != "": cl[f"{col}{r}"] = v
    if bd: cl[f"D{r}"] = _dt.date.fromisoformat(bd)
    cl[f"J{r}"] = f"=TODAY(){pt:+d}"
dv_list(cl, f"E6:E{NC}", STY); dv_list(cl, f"G6:G{NC}", CURL)
for val, fill, col in (('"Due now"', red, "A12A1E"), ('"Lapsed"', PatternFill("solid", fgColor="E6E1E8"), "5A4D5E"), ('"Due soon"', amb, "8A5A12"),
                       ('"Booked"', grn, "2E6B3A"), ('"OK"', grn, "2E6B3A"), ('"New"', amb, "8A5A12")):
    cl.conditional_formatting.add(f"Q6:Q{NC}", CellIsRule(operator="equal", formula=[val], fill=fill, font=Font(name=F, bold=True, color=col)))

# ---------- Expenses ----------
xp = wb.create_sheet("Expenses")
banner(xp, t, "Expenses", "Everything you spend on the business: supplies, rent, insurance, courses, marketing.", 6)
header(xp, 5, ["Date", "Category", "What", "Amount", "Month", "Notes"], t)
widths(xp, {"A": 13, "B": 16, "C": 32, "D": 12, "E": 8, "F": 28}); xp.freeze_panes = "A6"
CAT = "Supplies,Rent / suite,Insurance,Booking app,Marketing,Education,Equipment,Other"
for r in range(6, NE + 1):
    for col in "ABCDF": inp(xp, f"{col}{r}")
    for col in "CF": xp[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    xp[f"A{r}"].number_format = "dd mmm yyyy"; xp[f"D{r}"].number_format = USD
    calc(xp, f"E{r}", f'=IF(A{r}="","",TEXT(A{r},"mmm"))')
dv_list(xp, f"B6:B{NE}", CAT)
for i, (dd, c, w, a) in enumerate([(-28, "Rent / suite", "Suite rent", 450), (-25, "Supplies", "Lash trays + adhesive restock", 96.95),
                                   (-20, "Booking app", "Monthly plan", 35), (-14, "Insurance", "Monthly premium", 32), (-5, "Marketing", "Business cards", 24)]):
    r = 6 + i; xp[f"A{r}"] = f"=TODAY(){dd:+d}"; xp[f"B{r}"] = c; xp[f"C{r}"] = w; xp[f"D{r}"] = a
XD, XC, XA = (f"Expenses!${c}$6:${c}${NE}" for c in "ABD")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Pick a year. Everything updates from Appointments, Clients and Expenses.", 9)
widths(d, {"A": 30, "B": 15, "C": 13, "D": 13, "E": 13, "F": 13, "G": 4, "H": 28, "I": 12, "J": 13})
label(d, "A4", "Year", bold=True, size=12); inp(d, "B4", "=YEAR(TODAY())", "0")
yr = f'{AD},">="&DATE($B$4,1,1),{AD},"<"&DATE($B$4+1,1,1)'
xyr = f'{XD},">="&DATE($B$4,1,1),{XD},"<"&DATE($B$4+1,1,1)'
kpi = [("Income (services + no-show fees)", f'=SUMIFS({ACH},{AST},"<>Booked",{yr})', USD), ("Tips", f'=SUMIFS({ATIP},{AST},"Done",{yr})', USD),
       ("Expenses", f"=SUMIFS({XA},{xyr})", USD),
       ("Profit (income + tips - card fees - expenses)", f"=B6+B7-SUMIFS({AL},{yr})-B8", USD),
       ("Appointments done", f'=COUNTIFS({AST},"Done",{yr})', "0"),
       ("Average ticket (incl. tips)", f'=IF(B10=0,"",(SUMIFS({ACH},{AST},"Done",{yr})+B7)/B10)', USD),
       ("Rebook rate", f'=IF(B10=0,"",COUNTIFS({AST},"Done",{ARB},"Yes",{yr})/B10)', "0%"),
       ("No-show rate", f'=IFERROR(COUNTIFS({AST},"No-show",{yr})/(B10+COUNTIFS({AST},"No-show",{yr})),"")', "0%"),
       ("Clients due now", f'=COUNTIF(Clients!$Q$6:$Q${NC},"Due now")', "0"),
       ("Clients due in 5 days", f'=COUNTIF(Clients!$Q$6:$Q${NC},"Due soon")', "0"),
       ("Set aside for tax", f"=MAX(0,B9)*{TAX}", USD)]
for i, (a, f, fmt) in enumerate(kpi):
    r = 6 + i; label(d, f"A{r}", a, bold=True, size=11); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 28
label(d, "A17", "Expenses include supplies you buy, so product cost is not taken off twice. No-show and late-cancel fees you keep (type them in Price) count as income.", italic=True, size=9, color=GREY)
d.merge_cells("A17:F17")
header(d, 19, ["Month", "Income", "Tips", "Expenses", "Profit", "Appointments"], t)
for i, mn in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    r = 20 + i; label(d, f"A{r}", mn)
    mr = f'{AD},">="&DATE($B$4,{i + 1},1),{AD},"<"&DATE($B$4,{i + 2},1)'
    xm = f'{XD},">="&DATE($B$4,{i + 1},1),{XD},"<"&DATE($B$4,{i + 2},1)'
    calc(d, f"B{r}", f'=SUMIFS({ACH},{AST},"<>Booked",{mr})', USD)
    calc(d, f"C{r}", f'=SUMIFS({ATIP},{AST},"Done",{mr})', USD)
    calc(d, f"D{r}", f"=SUMIFS({XA},{xm})", USD)
    calc(d, f"E{r}", f"=B{r}+C{r}-D{r}-SUMIFS({AL},{mr})", USD)
    calc(d, f"F{r}", f'=COUNTIFS({AST},"Done",{mr})', "0")
label(d, "A32", "Total", bold=True)
for col in "BCDEF": calc(d, f"{col}32", f"=SUM({col}20:{col}31)", "0" if col == "F" else USD, bold=True)
header(d, 5, ["Service", "Booked (done)", "Income"], t, start=8)
for i in range(12):
    r = 6 + i
    d[f"H{r}"] = f"=IF('Service Menu'!A{6 + i}=\"\",\"\",'Service Menu'!A{6 + i})"; d[f"H{r}"].font = Font(name=F, size=11)
    calc(d, f"I{r}", f'=IF(H{r}="","",COUNTIFS({AS},H{r},{AST},"Done",{yr}))', "0")
    calc(d, f"J{r}", f'=IF(H{r}="","",SUMIFS({ACH},{AS},H{r},{AST},"Done",{yr}))', USD)
header(d, 19, ["Expense category", "This year"], t, start=8)
for i, c in enumerate(CAT.split(",")):
    r = 20 + i; label(d, f"H{r}", c); calc(d, f"I{r}", f'=SUMIFS({XA},{XC},H{r},{xyr})', USD)

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved")
