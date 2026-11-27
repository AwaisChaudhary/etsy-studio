"""Wedding Budget Planner Spreadsheet (batch 10, lane g): set-up with countdown; budget by 12 categories / 50 line items with a
guide %, budget, actual, paid, still to pay and over/under; vendors with quotes, deposits and contracts; payment schedule with
Due soon / Overdue flags; guest list with RSVP, meals, dietary needs, tables and thank-you cards; a 12-month checklist dated from
your wedding day; dashboard with countdown, spend, guest and meal counts, cost per guest and a budget chart. Excel + Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule, FormulaRule, DataBarRule
from openpyxl.utils import get_column_letter as gl
from openpyxl.chart import BarChart, Reference

t = Theme("5B3A4A", "B9826B", "F7EEEA")
wb = Workbook()
NV, NPAY, NG, NC = 80, 200, 406, 120
USD = '"$"#,##0.00'; USD0 = '"$"#,##0'
GREY = "6A6F7D"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1"); blush = PatternFill("solid", fgColor="F3DCD4")
REDF = Font(name=F, bold=True, color="A12A1E"); AMBF = Font(name=F, bold=True, color="8A5A12"); GRNF = Font(name=F, bold=True, color="2E6B3A")

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Wedding Budget Planner", "Budget, vendors, payments, guests and every to-do from 'yes' to 'I do', in one calm place.", 6)
widths(s, {"A": 6, "B": 100})
steps = ["Setup: your names, wedding date, total budget and the guest count you're planning for. The countdown starts.",
         "Budget: every category has a guide % of a typical budget and a starting budget worked out from your total. Type over any budget, then add actual costs.",
         "Vendors: each quote, deposit and contract. Payments: every deposit and balance with its due date: Due soon and Overdue light up.",
         "Guest List: households, RSVPs, adults and kids, meal choices, dietary needs, table numbers, gifts and thank-you cards.",
         "Checklist: 60 tasks from 12+ months out to the week after, each dated from YOUR wedding day. Tick them off.",
         "Dashboard: days to go, budget vs actual, paid and still to pay, guests attending, meal counts and cost per guest."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Guide % are typical shares of a wedding budget to start from, not rules: move money to what matters most to the two of you.", size=10, color="7A4A5A")
label(s, "B15", "Example vendors, payments and guests are included so you can see how it works: type over them or delete them. Works in Excel and Google Sheets.", italic=True, size=10)

# ---------- Setup ----------
su = wb.create_sheet("Setup")
banner(su, t, "Our wedding", "Fill these in first. Everything else uses them.", 5)
widths(su, {"A": 32, "B": 26, "C": 4, "D": 50})
rows = [("Partner 1", "Olivia"), ("Partner 2", "James"), ("Wedding date", "=DATE(YEAR(TODAY())+1,9,18)"), ("Total budget", 30000),
        ("Planned guest count", 110), ("Venue", "The Orchard Barn"), ("Ceremony time", "3:00 PM")]
for i, (a, v) in enumerate(rows):
    r = 5 + i; label(su, f"A{r}", a, bold=True); c = inp(su, f"B{r}", v)
    c.alignment = Alignment(horizontal="left", indent=1)
su["B7"].number_format = "dddd d mmmm yyyy"; su["B8"].number_format = USD0
WD, TB, GC = "Setup!$B$7", "Setup!$B$8", "Setup!$B$9"
label(su, "A13", "Days to go", bold=True, size=14); calc(su, "B13", f'=IF({WD}="","",MAX(0,{WD}-TODAY()))', "#,##0", big=True)
label(su, "A14", "Weeks to go", bold=True); calc(su, "B14", '=IF(B13="","",ROUNDDOWN(B13/7,0))', "0")
label(su, "A15", "Budget per planned guest", bold=True); calc(su, "B15", f'=IF(N({GC})=0,"",{TB}/{GC})', USD)
label(su, "D5", "Tip: write down your top 3 priorities together (food? photos? the band?) and give those categories more of the budget.", italic=True, size=10, color=GREY)
su.merge_cells("D5:D8")

# ---------- Vendors ----------
v = wb.create_sheet("Vendors")
banner(v, t, "Vendors", "Everyone you're booking: quote, deposit, contract and contact details.", 12)
header(v, 5, ["Vendor", "Service", "Contact name", "Phone", "Email / website", "Quote", "Booked?", "Contract signed?", "Paid so far", "STILL TO PAY", "Notes"], t)
for i, w in enumerate([26, 18, 16, 14, 26, 12, 10, 11, 12, 12, 30]): v.column_dimensions[gl(i + 1)].width = w
v.freeze_panes = "B6"
SERV = "Venue,Catering,Photographer,Videographer,Florist,DJ / band,Cake,Hair & makeup,Officiant,Dress / suit,Stationery,Rentals,Transport,Planner,Other"
for r in range(6, NV + 6):
    for col in "ABCDEFGHK": inp(v, f"{col}{r}")
    for col in "ABCEK": v[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    v[f"F{r}"].number_format = USD
    calc(v, f"I{r}", f"=IF(A{r}=\"\",\"\",SUMIFS(Payments!$D$6:$D${NPAY + 5},Payments!$B$6:$B${NPAY + 5},A{r},Payments!$E$6:$E${NPAY + 5},\"Yes\"))", USD)
    calc(v, f"J{r}", f'=IF(A{r}="","",MAX(0,N(F{r})-I{r}))', USD, bold=True)
dv_list(v, f"B6:B{NV + 5}", SERV); dv_list(v, f"G6:H{NV + 5}", "Yes,No,Pending")
vend = [("The Orchard Barn", "Venue", "Sarah", "555-0142", "orchardbarn.example", 5400, "Yes", "Yes", "Includes tables and chairs"),
        ("Fig & Thyme Catering", "Catering", "Marco", "555-0178", "figandthyme.example", 5940, "Yes", "Yes", "$54 x 110, family style"),
        ("Golden Hour Photo", "Photographer", "Ava", "555-0110", "goldenhour.example", 2900, "Yes", "Yes", "8 hours + engagement shoot"),
        ("Wild Stem Florals", "Florist", "Nina", "555-0133", "wildstem.example", 1280, "Yes", "Pending", "Seasonal, dried accents"),
        ("Sound & Soul DJ", "DJ / band", "Theo", "555-0191", "soundsoul.example", 1450, "Pending", "No", "Ceremony mics included?"),
        ("Butter & Bloom Cakes", "Cake", "Ruth", "555-0155", "butterbloom.example", 620, "Yes", "Yes", "3-tier lemon + elderflower")]
for i, row in enumerate(vend):
    for col, val in zip("ABCDEFGHK", row): v[f"{col}{6 + i}"] = val
v.conditional_formatting.add(f"G6:H{NV + 5}", CellIsRule(operator="equal", formula=['"Yes"'], fill=grn, font=GRNF))
v.conditional_formatting.add(f"G6:H{NV + 5}", CellIsRule(operator="equal", formula=['"Pending"'], fill=amb, font=AMBF))
VLIST = f"=Vendors!$A$6:$A${NV + 5}"

# ---------- Budget ----------
b = wb.create_sheet("Budget")
banner(b, t, "Budget", "Guide % = a typical share of the budget. Budget starts from your total: type over it. Actual = what it really costs.", 10)
header(b, 5, ["Category", "Item", "Guide %", "BUDGET", "Actual cost", "Vendor", "Paid", "Still to pay", "Over / under", "Notes"], t)
for i, w in enumerate([20, 30, 9, 12, 12, 24, 11, 12, 12, 26]): b.column_dimensions[gl(i + 1)].width = w
b.freeze_panes = "C6"
CATS = [("Venue & rentals", [("Venue hire", .175), ("Tables, chairs & linens", .015), ("Marquee / lighting", .01)]),
        ("Food & drink", [("Catering (per head)", .205), ("Bar & drinks", .05), ("Wedding cake / desserts", .02), ("Late-night snacks", .005)]),
        ("Photo & video", [("Photographer", .09), ("Videographer", .03)]),
        ("Attire & beauty", [("Dress / outfit 1", .04), ("Suit / outfit 2", .015), ("Alterations", .005), ("Shoes & accessories", .01), ("Hair & makeup", .015)]),
        ("Flowers & decor", [("Bouquets & buttonholes", .02), ("Ceremony flowers", .015), ("Centrepieces", .03), ("Candles, signs & decor", .01)]),
        ("Music & entertainment", [("Ceremony music", .015), ("DJ / band", .04), ("Photo booth / games", .01)]),
        ("Stationery", [("Save the dates", .005), ("Invitations & postage", .01), ("On-the-day stationery", .005)]),
        ("Ceremony", [("Officiant / registrar fee", .01), ("Marriage licence", .002), ("Ceremony extras", .003)]),
        ("Rings", [("Wedding bands", .03)]),
        ("Transport", [("Wedding car", .01), ("Guest shuttle", .01)]),
        ("Favours & gifts", [("Guest favours", .008), ("Wedding party gifts", .01), ("Parents' gifts", .005), ("Welcome bags", .002)]),
        ("Extras", [("Planner / coordinator", .02), ("Wedding night / first nights", .01), ("Tips & gratuities", .015), ("Contingency (just in case)", .02)])]
r = 6; CATROWS = {}
for cat, items in CATS:
    start = r
    for item, pct in items:
        b[f"A{r}"] = cat; b[f"A{r}"].font = Font(name=F, size=11, bold=(r == start), color=t.main if r == start else "8A8F99")
        inp(b, f"B{r}", item).alignment = Alignment(horizontal="left", indent=1)
        inp(b, f"C{r}", pct, "0.0%"); inp(b, f"D{r}", f"=ROUND({TB}*C{r},-1)", USD0); inp(b, f"E{r}", None, USD0); inp(b, f"F{r}").alignment = Alignment(horizontal="left", indent=1)
        inp(b, f"J{r}").alignment = Alignment(horizontal="left", indent=1)
        calc(b, f"G{r}", f"=IF(OR(F{r}=\"\",N(E{r})=0),\"\",SUMIFS(Payments!$D$6:$D${NPAY + 5},Payments!$B$6:$B${NPAY + 5},F{r},Payments!$E$6:$E${NPAY + 5},\"Yes\")*E{r}/SUMIF($F$6:$F$60,F{r},$E$6:$E$60))", USD0)
        calc(b, f"H{r}", f'=IF(E{r}="","",MAX(0,E{r}-N(G{r})))', USD0)
        calc(b, f"I{r}", f'=IF(E{r}="","",D{r}-E{r})', '"$"#,##0;[Red]-"$"#,##0', bold=True)
        r += 1
    CATROWS[cat] = (start, r - 1)
NB = r - 1
for i in range(8):  # spare rows
    for col in "ABCDEFJ": inp(b, f"{col}{r}")
    b[f"D{r}"].number_format = USD0; b[f"E{r}"].number_format = USD0
    calc(b, f"G{r}", f"=IF(OR(F{r}=\"\",N(E{r})=0),\"\",SUMIFS(Payments!$D$6:$D${NPAY + 5},Payments!$B$6:$B${NPAY + 5},F{r},Payments!$E$6:$E${NPAY + 5},\"Yes\")*E{r}/SUMIF($F$6:$F$60,F{r},$E$6:$E$60))", USD0)
    calc(b, f"H{r}", f'=IF(E{r}="","",MAX(0,E{r}-N(G{r})))', USD0)
    calc(b, f"I{r}", f'=IF(E{r}="","",N(D{r})-E{r})', '"$"#,##0;[Red]-"$"#,##0', bold=True)
    r += 1
NBE = r - 1
label(b, f"A{r + 1}", "TOTAL", bold=True, size=12)
calc(b, f"C{r + 1}", f"=SUM(C6:C{NBE})", "0%", bold=True); calc(b, f"D{r + 1}", f"=SUM(D6:D{NBE})", USD0, bold=True); calc(b, f"E{r + 1}", f"=SUM(E6:E{NBE})", USD0, bold=True)
calc(b, f"G{r + 1}", f"=SUM(G6:G{NBE})", USD0, bold=True); calc(b, f"H{r + 1}", f"=SUM(H6:H{NBE})", USD0, bold=True)
calc(b, f"I{r + 1}", f"={TB}-D{r + 1}", '"$"#,##0;[Red]-"$"#,##0', bold=True)
label(b, f"J{r + 1}", "<- left to allocate from your total budget", italic=True, size=9, color=GREY)
BT = r + 1
dv_list(b, f"F6:F{NBE}", VLIST)
b.conditional_formatting.add(f"I6:I{NBE}", CellIsRule(operator="lessThan", formula=["0"], fill=red, font=REDF))
for (item_row, actual, vendor) in [("Venue hire", 5400, "The Orchard Barn"), ("Catering (per head)", 5940, "Fig & Thyme Catering"), ("Photographer", 2900, "Golden Hour Photo"),
                                   ("Centrepieces", 760, "Wild Stem Florals"), ("Bouquets & buttonholes", 520, "Wild Stem Florals"), ("Wedding cake / desserts", 620, "Butter & Bloom Cakes"),
                                   ("Dress / outfit 1", 1100, None), ("Wedding bands", 820, None), ("Save the dates", 95, None)]:
    for rr in range(6, NB + 1):
        if b[f"B{rr}"].value == item_row:
            b[f"E{rr}"] = actual
            if vendor: b[f"F{rr}"] = vendor
# category summary (for chart)
header(b, 5, ["Category", "Budget", "Actual"], t, start=12)
for c, w in (("L", 22), ("M", 11), ("N", 11)): b.column_dimensions[c].width = w
for i, (cat, (a_, z_)) in enumerate(CATROWS.items()):
    rr = 6 + i; b[f"L{rr}"] = cat; b[f"L{rr}"].font = Font(name=F, size=10)
    calc(b, f"M{rr}", f"=SUM(D{a_}:D{z_})", USD0); calc(b, f"N{rr}", f"=SUM(E{a_}:E{z_})", USD0)

# ---------- Payments ----------
pm = wb.create_sheet("Payments")
banner(pm, t, "Payment schedule", "Every deposit and balance with its due date. Mark Paid = Yes when it's done.", 9)
header(pm, 5, ["Due date", "Vendor", "What for", "Amount", "Paid?", "Date paid", "Method", "DAYS LEFT", "Flag"], t)
for i, w in enumerate([13, 26, 22, 12, 8, 13, 13, 10, 12]): pm.column_dimensions[gl(i + 1)].width = w
pm.freeze_panes = "A6"
for r in range(6, NPAY + 6):
    for col in "ABCDEFG": inp(pm, f"{col}{r}")
    for col in "BC": pm[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    for col in "AF": pm[f"{col}{r}"].number_format = "dd mmm yyyy"
    pm[f"D{r}"].number_format = USD
    calc(pm, f"H{r}", f'=IF(OR(A{r}="",E{r}="Yes"),"",A{r}-TODAY())', "0")
    calc(pm, f"I{r}", f'=IF(B{r}="","",IF(E{r}="Yes","Paid",IF(A{r}="","",IF(H{r}<0,"Overdue",IF(H{r}<=14,"Due soon","Upcoming")))))')
dv_list(pm, f"B6:B{NPAY + 5}", VLIST); dv_list(pm, f"E6:E{NPAY + 5}", "Yes,No"); dv_list(pm, f"G6:G{NPAY + 5}", "Card,Bank transfer,Cash,Cheque,PayPal,Other")
for val, fill, f_ in (('"Overdue"', red, REDF), ('"Due soon"', amb, AMBF), ('"Paid"', grn, GRNF)):
    pm.conditional_formatting.add(f"I6:I{NPAY + 5}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
pays = [(-120, "The Orchard Barn", "Deposit", 1350, "Yes", "Bank transfer"), (-90, "Golden Hour Photo", "Retainer", 1000, "Yes", "Card"),
        (-60, "Fig & Thyme Catering", "Deposit", 1500, "Yes", "Bank transfer"), (-30, "Butter & Bloom Cakes", "Deposit", 150, "Yes", "Card"),
        (-20, "Wild Stem Florals", "Deposit", 500, "Yes", "Card"), (-4, "Sound & Soul DJ", "Booking fee", 300, "No", ""),
        (9, "The Orchard Barn", "2nd payment", 2025, "No", ""), (60, "Golden Hour Photo", "Balance", 1900, "No", ""),
        (200, "Fig & Thyme Catering", "Final balance", 4440, "No", ""), (230, "The Orchard Barn", "Final balance", 2025, "No", "")]
for i, (dd, vn, what, amt, pd, meth) in enumerate(pays):
    r = 6 + i; pm[f"A{r}"] = f"=TODAY(){dd:+d}"; pm[f"B{r}"] = vn; pm[f"C{r}"] = what; pm[f"D{r}"] = amt; pm[f"E{r}"] = pd
    if pd == "Yes": pm[f"F{r}"] = f"=TODAY(){dd - 1:+d}"; pm[f"G{r}"] = meth

# ---------- Guest List ----------
g = wb.create_sheet("Guest List")
banner(g, t, "Guest list & RSVPs", "One row per household (or person). Counts, meals and tables add up on the Dashboard.", 16)
header(g, 5, ["Guest / household", "Side", "Group", "Address", "Save the date sent", "Invite sent", "RSVP", "Adults", "Kids", "Meal choice", "Dietary needs",
              "Table", "Gift", "Thank-you sent", "ATTENDING", "Notes"], t)
g.row_dimensions[5].height = 44
for i, w in enumerate([28, 11, 13, 30, 10, 9, 10, 8, 7, 13, 18, 7, 18, 10, 11, 22]): g.column_dimensions[gl(i + 1)].width = w
g.freeze_panes = "B6"
for r in range(6, NG + 1):
    for col in "ABCDEFGHIJKLMNP": inp(g, f"{col}{r}")
    for col in "ADKMP": g[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    calc(g, f"O{r}", f'=IF(A{r}="","",IF(G{r}="Yes",N(H{r})+N(I{r}),0))', "0", bold=True)
dv_list(g, f"B6:B{NG}", "Partner 1,Partner 2,Both"); dv_list(g, f"C6:C{NG}", "Family,Friends,Work,Wedding party,Plus one,Other")
dv_list(g, f"E6:F{NG}", "Yes,No"); dv_list(g, f"G6:G{NG}", "Yes,No,Pending"); dv_list(g, f"N6:N{NG}", "Yes,No")
dv_list(g, f"J6:J{NG}", "Chicken,Beef,Fish,Vegetarian,Vegan,Kids meal,Mixed")
g.conditional_formatting.add(f"G6:G{NG}", CellIsRule(operator="equal", formula=['"Yes"'], fill=grn, font=GRNF))
g.conditional_formatting.add(f"G6:G{NG}", CellIsRule(operator="equal", formula=['"No"'], fill=red, font=REDF))
g.conditional_formatting.add(f"G6:G{NG}", CellIsRule(operator="equal", formula=['"Pending"'], fill=amb, font=AMBF))
guests = [("Mum & Dad (Hughes)", "Partner 1", "Family", "Yes", "Yes", "Yes", 2, 0, "Mixed", "", 1, "", ""),
          ("Grandma Rose", "Partner 1", "Family", "Yes", "Yes", "Yes", 1, 0, "Fish", "Soft foods", 1, "", ""),
          ("The Bennetts", "Partner 2", "Family", "Yes", "Yes", "Yes", 2, 2, "Mixed", "1 nut allergy (kid)", 3, "", ""),
          ("Priya & Sam", "Both", "Friends", "Yes", "Yes", "Yes", 2, 0, "Vegetarian", "", 5, "Stand mixer", "Yes"),
          ("Uncle Ray", "Partner 2", "Family", "Yes", "Yes", "Pending", 1, 0, "", "", None, "", ""),
          ("Chloe (+1)", "Partner 1", "Wedding party", "Yes", "Yes", "Yes", 2, 0, "Vegan", "Vegan", 2, "", ""),
          ("Dan & Lucy", "Partner 2", "Work", "Yes", "Yes", "No", 2, 0, "", "", None, "Card + gift voucher", "Yes"),
          ("The Okafors", "Both", "Friends", "Yes", "Yes", "Yes", 2, 1, "Chicken", "", 4, "", ""),
          ("Marcus", "Partner 2", "Wedding party", "Yes", "Yes", "Yes", 1, 0, "Beef", "", 2, "", ""),
          ("Auntie Jo & Pete", "Partner 1", "Family", "Yes", "No", "Pending", 2, 0, "", "", None, "", "")]
for i, row in enumerate(guests):
    for col, val in zip("ABCEFGHIJKLMN", row):
        if val not in ("", None): g[f"{col}{6 + i}"] = val
GR = lambda c: f"'Guest List'!${c}$6:${c}${NG}"

# ---------- Checklist ----------
ck = wb.create_sheet("Checklist")
banner(ck, t, "Wedding checklist", "Every task is dated from your wedding day. Type Done when it's done.", 7)
header(ck, 5, ["When", "Task", "Months before", "DUE BY", "Done?", "Who", "Status"], t)
for i, w in enumerate([18, 52, 9, 13, 8, 12, 12]): ck.column_dimensions[gl(i + 1)].width = w
ck.freeze_panes = "A6"
TASKS = [(12, ["Set your total budget together", "Pick 3 top priorities", "Draft a rough guest list", "Choose a season and date range", "Book the venue",
               "Start a wedding email + shared folder"]),
         (10, ["Book the photographer", "Book the caterer (if not with venue)", "Choose the wedding party", "Book the officiant / registrar", "Book a planner or coordinator"]),
         (9, ["Start outfit shopping", "Book videographer", "Book band / DJ", "Plan the engagement shoot", "Set up a gift list"]),
         (8, ["Send save the dates", "Book the florist", "Reserve guest hotel rooms", "Start the wedding website"]),
         (6, ["Order invitations", "Book hair and makeup", "Order the cake", "Book transport", "Plan the honeymoon", "Book rentals (tables, linens, lighting)"]),
         (4, ["Wedding bands", "Plan the ceremony order and readings", "Menu tasting", "Buy shoes and accessories", "First outfit fitting"]),
         (3, ["Send invitations", "Order favours and gifts", "Hair and makeup trial", "Plan the reception timeline", "Confirm vendor arrival times"]),
         (2, ["Chase missing RSVPs", "Write vows", "Order on-the-day stationery", "Give music must-play / do-not-play lists", "Get the marriage licence"]),
         (1, ["Final guest count to caterer", "Seating plan", "Final fitting", "Pay final balances", "Pack an emergency kit", "Break in your shoes"]),
         (0.25, ["Confirm every vendor one last time", "Give the timeline to the wedding party", "Prepare tip envelopes", "Pack for the honeymoon"]),
         (0, ["Rehearsal", "Rest, hydrate, enjoy it!"]),
         (-1, ["Return rentals and outfits", "Send thank-you cards", "Review your vendors", "Change your name (if you're changing it)"])]
r = 6
for mb, tasks in TASKS:
    for tk in tasks:
        when = {0: "Wedding week", 0.25: "1 week before", -1: "After the wedding"}.get(mb, f"{mb:g} month{'s' if mb != 1 else ''} before")
        ck[f"A{r}"] = when; ck[f"A{r}"].font = Font(name=F, size=10, color=t.main, bold=True)
        inp(ck, f"B{r}", tk).alignment = Alignment(horizontal="left", indent=1); inp(ck, f"C{r}", mb, "0.##")
        calc(ck, f"D{r}", f'=IF(OR(B{r}="",C{r}=""),"",IF(C{r}<0,{WD}+30,IF(C{r}<1,{WD}-ROUND(C{r}*28,0),EDATE({WD},-C{r}))))', "dd mmm yyyy")
        inp(ck, f"E{r}"); inp(ck, f"F{r}")
        calc(ck, f"G{r}", f'=IF(B{r}="","",IF(E{r}="Done","Done",IF(D{r}<TODAY(),"Overdue",IF(D{r}-TODAY()<=30,"This month","Later"))))')
        r += 1
NCK = r - 1
for i in range(NC + 6 - r if NC + 6 > r else 0):
    rr = r + i
    for col in "ABCEF": inp(ck, f"{col}{rr}")
    ck[f"B{rr}"].alignment = Alignment(horizontal="left", indent=1)
    calc(ck, f"D{rr}", f'=IF(OR(B{rr}="",C{rr}=""),"",IF(C{rr}<0,{WD}+30,IF(C{rr}<1,{WD}-ROUND(C{rr}*28,0),EDATE({WD},-C{rr}))))', "dd mmm yyyy")
    calc(ck, f"G{rr}", f'=IF(B{rr}="","",IF(E{rr}="Done","Done",IF(D{rr}<TODAY(),"Overdue",IF(D{rr}-TODAY()<=30,"This month","Later"))))')
CKE = max(NCK, NC + 5)
dv_list(ck, f"E6:E{CKE}", "Done"); dv_list(ck, f"F6:F{CKE}", "Both,Partner 1,Partner 2,Family,Planner")
for val, fill, f_ in (('"Overdue"', red, REDF), ('"This month"', amb, AMBF), ('"Done"', grn, GRNF)):
    ck.conditional_formatting.add(f"G6:G{CKE}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
ck.conditional_formatting.add(f"B6:B{CKE}", FormulaRule(formula=['$E6="Done"'], font=Font(name=F, color="8A8F99", strike=True)))
for rr in range(6, 6 + 16): ck[f"E{rr}"] = "Done"  # example progress (first tasks done)
for rr in range(6, 6 + 16): ck[f"F{rr}"] = "Both"

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Wedding dashboard", "Everything at a glance. It all updates from the other tabs.", 10)
widths(d, {"A": 30, "B": 18, "C": 3, "D": 22, "E": 12, "F": 12, "G": 12})
d.merge_cells("A4:B4"); c = d["A4"]; c.value = '=Setup!B5&" & "&Setup!B6&"  •  "&TEXT(Setup!B7,"d mmmm yyyy")'
c.font = Font(name=F, size=14, bold=True, color=t.main)
kpi = [("DAYS TO GO", "=Setup!B13", "#,##0"), ("Total budget", f"={TB}", USD0), ("Budgeted so far", f"=Budget!D{BT}", USD0),
       ("Actual costs so far", f"=Budget!E{BT}", USD0), ("Paid", f"=SUMIFS(Payments!$D$6:$D${NPAY + 5},Payments!$E$6:$E${NPAY + 5},\"Yes\")", USD0),
       ("Still to pay (scheduled)", f"=SUMIFS(Payments!$D$6:$D${NPAY + 5},Payments!$E$6:$E${NPAY + 5},\"<>Yes\")", USD0),
       ("Payments due soon / overdue", f'=COUNTIF(Payments!$I$6:$I${NPAY + 5},"Due soon")+COUNTIF(Payments!$I$6:$I${NPAY + 5},"Overdue")', "0"),
       ("Guests invited (people)", f"=SUMIFS({GR('H')},{GR('F')},\"Yes\")+SUMIFS({GR('I')},{GR('F')},\"Yes\")", "0"),
       ("ATTENDING", f"=SUM({GR('O')})", "0"),
       ("RSVPs still pending (households)", f'=COUNTIF({GR("G")},"Pending")', "0"),
       ("Cost per guest (planned count)", f'=IF(N({GC})=0,"",B8/{GC})', USD0),
       ("Thank-you cards to send", f'=COUNTIFS({GR("M")},"<>",{GR("N")},"<>Yes")', "0"),
       ("Checklist done", f'=IF(COUNTA(Checklist!$B$6:$B${CKE})=0,"",COUNTIF(Checklist!$E$6:$E${CKE},"Done")/COUNTA(Checklist!$B$6:$B${CKE}))', "0%"),
       ("Checklist overdue", f'=COUNTIF(Checklist!$G$6:$G${CKE},"Overdue")', "0")]
for i, (a, f_, fmt) in enumerate(kpi):
    r = 5 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f_, fmt, big=True); d.row_dimensions[r].height = 26
d["B5"].fill = blush; d["B13"].fill = blush
d.conditional_formatting.add("B17", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="B9826B"))
header(d, 4, ["Meals (attending)", "Count"], t, start=4)
for i, ml in enumerate(["Chicken", "Beef", "Fish", "Vegetarian", "Vegan", "Kids meal", "Mixed"]):
    r = 5 + i; d[f"D{r}"] = ml; d[f"D{r}"].font = Font(name=F, size=11)
    calc(d, f"E{r}", f"=SUMIFS({GR('O')},{GR('J')},D{r},{GR('G')},\"Yes\")", "0")
label(d, "D12", "'Mixed' = a household with different choices: note them in Dietary needs.", italic=True, size=9, color=GREY)
header(d, 14, ["Side", "Attending"], t, start=4)
for i, sd in enumerate(["Partner 1", "Partner 2", "Both"]):
    r = 15 + i; d[f"D{r}"] = sd; d[f"D{r}"].font = Font(name=F, size=11); calc(d, f"E{r}", f"=SUMIFS({GR('O')},{GR('B')},D{r})", "0")
ch = BarChart(); ch.type = "bar"; ch.style = 10; ch.title = "Budget vs actual by category"; ch.height = 9; ch.width = 18
ch.add_data(Reference(b, min_col=13, max_col=14, min_row=5, max_row=5 + len(CATS)), titles_from_data=True)
ch.set_categories(Reference(b, min_col=12, min_row=6, max_row=5 + len(CATS)))
ch.series[0].graphicalProperties.solidFill = "E6CFC6"; ch.series[1].graphicalProperties.solidFill = "5B3A4A"
d.add_chart(ch, "D20")

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved", NB, NBE, BT, NCK)
