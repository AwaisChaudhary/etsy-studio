"""Self-Employed Bookkeeping Spreadsheet 2027 (batch 11, lane a): setup (year, tax set-aside %, mileage rate, quarter due dates);
income log with fees and net; expense log with 20 tax-style categories, business-use % and receipt check; mileage log with
deduction; invoice tracker with Due soon / Overdue; monthly profit & loss by category; quarterly tax set-aside planner; dashboard
with income vs expenses chart. Every total is a formula. Works in Excel and Google Sheets."""
import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule, FormulaRule, DataBarRule
from openpyxl.utils import get_column_letter as gl
from openpyxl.chart import BarChart, LineChart, Reference

t = Theme("1F3B4D", "3E8E7E", "EAF2EF")
wb = Workbook()
NI, NE, NM, NV = 1000, 1500, 600, 300
IE, EE, ME, VE = NI + 5, NE + 5, NM + 5, NV + 5
USD = '"$"#,##0.00'; USD0 = '"$"#,##0'; NEG = '"$"#,##0.00;[Red]-"$"#,##0.00'
GREY = "6A6F7D"
red = PatternFill("solid", fgColor="F8D7D3"); amb = PatternFill("solid", fgColor="FCEBC8"); grn = PatternFill("solid", fgColor="E3F0E1")
REDF = Font(name=F, bold=True, color="A12A1E"); AMBF = Font(name=F, bold=True, color="8A5A12"); GRNF = Font(name=F, bold=True, color="2E6B3A")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "Self-Employed Bookkeeping 2027", "Income, expenses, mileage, invoices, profit and tax set-aside for freelancers, makers and small shops.", 6)
widths(s, {"A": 6, "B": 104})
steps = ["Setup: your business name, the tax year, the % of profit you set aside for tax, your mileage rate and the quarterly tax due dates.",
         "Income: every payment you receive. Add platform or card fees and the net is worked out. Pick a category (sales, services, other).",
         "Expenses: every business cost with a category. Business use % handles things you also use personally (phone, internet, car).",
         "Mileage: business trips. Miles x your rate = a deduction, added to Profit & Loss for you.",
         "Invoices: who owes you what. Due soon and Overdue light up; mark Paid when the money lands (and log it in Income).",
         "Profit & Loss: month by month and by category, all automatic. Quarterly Tax: profit each quarter and what to set aside.",
         "Dashboard: income, expenses, net profit, margin, tax to set aside, unpaid invoices, missing receipts and a monthly chart."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 32
legend(s, 13, 2)
label(s, "B15", "Only rows dated in your tax year (Setup) count in the totals, so you can keep last December's receipts here without breaking anything.", size=10, color="2B5F55")
label(s, "B16", "This is a record-keeping tool, not tax advice. Tax set-aside % and the mileage rate are yours to set: check them with your accountant or tax office.", size=10, color=GREY)
label(s, "B17", "Example rows are included so you can see how it works: type over them or delete them. Works in Excel and Google Sheets.", italic=True, size=10)

# ---------- Setup ----------
su = wb.create_sheet("Setup")
banner(su, t, "Setup", "Fill these in first. Everything else uses them.", 6)
widths(su, {"A": 34, "B": 22, "C": 4, "D": 22, "E": 16, "F": 30})
rows = [("Business name", "Juniper Lane Studio"), ("Tax year", 2027), ("Currency symbol (for labels)", "$"), ("Tax set-aside % of profit", 0.25),
        ("Mileage rate per mile / km", 0.70), ("Opening bank balance", 2400)]
for i, (a, v) in enumerate(rows):
    r = 5 + i; label(su, f"A{r}", a, bold=True); c = inp(su, f"B{r}", v); c.alignment = Alignment(horizontal="left", indent=1)
su["B8"].number_format = "0%"; su["B9"].number_format = USD; su["B10"].number_format = USD
YR, TAX, MR, OB = "Setup!$B$6", "Setup!$B$8", "Setup!$B$9", "Setup!$B$10"
label(su, "A12", "Set-aside % is a planning number: many self-employed people keep 25-30% aside. Ask your accountant what fits you.", italic=True, size=9, color=GREY)
su.merge_cells("A12:B13")
header(su, 4, ["Quarter", "Months", "Tax due date"], t, start=4)
QD = [("Q1", "Jan - Mar", "=DATE($B$6,4,15)"), ("Q2", "Apr - May", "=DATE($B$6,6,15)"), ("Q3", "Jun - Aug", "=DATE($B$6,9,15)"), ("Q4", "Sep - Dec", "=DATE($B$6+1,1,15)")]
for i, (q, m, dd) in enumerate(QD):
    r = 5 + i; su[f"D{r}"] = q; su[f"D{r}"].font = Font(name=F, bold=True); su[f"E{r}"] = m; su[f"E{r}"].font = Font(name=F, size=10)
    inp(su, f"F{r}", dd, "ddd d mmm yyyy")
label(su, "D10", "Quarter months and due dates follow the US estimated tax calendar. Change the dates (and the months in Quarterly Tax) for your country.", italic=True, size=9, color=GREY)
su.merge_cells("D10:F12")
header(su, 15, ["Income categories"], t, start=1); header(su, 15, ["Payment methods"], t, start=2)
ICATS = ["Product sales", "Services / client work", "Commissions", "Wholesale", "Workshops / classes", "Affiliate / ads", "Refunds received", "Other income"]
METH = ["Bank transfer", "Card", "Cash", "PayPal", "Stripe", "Etsy / marketplace", "Cheque", "Other"]
for i, v in enumerate(ICATS): inp(su, f"A{16 + i}", v).alignment = Alignment(horizontal="left", indent=1)
for i, v in enumerate(METH): inp(su, f"B{16 + i}", v).alignment = Alignment(horizontal="left", indent=1)
for i in range(4): inp(su, f"A{16 + len(ICATS) + i}"); inp(su, f"B{16 + len(METH) + i}")
header(su, 15, ["Expense categories (tax-style)", "Typical tax line"], t, start=4)
ECATS = [("Advertising & marketing", "Advertising"), ("Platform & selling fees", "Commissions & fees"), ("Card / payment fees", "Commissions & fees"),
         ("Contract labour", "Contract labour"), ("Materials & supplies", "Supplies / cost of goods"), ("Inventory / stock bought", "Cost of goods sold"),
         ("Packaging & shipping", "Supplies / postage"), ("Equipment & tools", "Depreciation / supplies"), ("Software & subscriptions", "Other expenses"),
         ("Office supplies", "Office expense"), ("Phone & internet", "Utilities"), ("Rent / workspace", "Rent or lease"),
         ("Home office", "Business use of home"), ("Insurance", "Insurance"), ("Legal & professional", "Legal & professional"),
         ("Bank charges", "Other expenses"), ("Training & education", "Other expenses"), ("Travel", "Travel"), ("Meals (business)", "Meals"),
         ("Vehicle (not mileage)", "Car & truck"), ("Repairs & maintenance", "Repairs"), ("Other", "Other expenses")]
for i, (a, b_) in enumerate(ECATS):
    r = 16 + i; inp(su, f"D{r}", a).alignment = Alignment(horizontal="left", indent=1); inp(su, f"E{r}", b_).alignment = Alignment(horizontal="left", indent=1)
su.column_dimensions["D"].width = 28; su.column_dimensions["E"].width = 24
NEC = len(ECATS)
ICL, MTL, ECL = f"=Setup!$A$16:$A${15 + len(ICATS) + 4}", f"=Setup!$B$16:$B${15 + len(METH) + 4}", f"=Setup!$D$16:$D${15 + NEC}"

def ym(sheet_col, r):  # month number if in tax year else ""
    return f'=IF({sheet_col}{r}="","",IF(YEAR({sheet_col}{r})={YR},MONTH({sheet_col}{r}),""))'

# ---------- Income ----------
inc = wb.create_sheet("Income")
banner(inc, t, "Income", "Every payment you receive. Fees = what the platform, card processor or PayPal kept.", 11)
header(inc, 5, ["Date", "Client / source", "Description", "Category", "Method", "Invoice #", "Amount received", "Fees", "NET", "Month", "Notes"], t)
for i, w in enumerate([12, 24, 30, 22, 16, 11, 14, 11, 13, 8, 24]): inc.column_dimensions[gl(i + 1)].width = w
inc.freeze_panes = "B6"
for r in range(6, IE + 1):
    for col in "ABCDEFGHK": inp(inc, f"{col}{r}")
    for col in "BCDEK": inc[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    inc[f"A{r}"].number_format = "dd mmm yyyy"; inc[f"G{r}"].number_format = USD; inc[f"H{r}"].number_format = USD
    calc(inc, f"I{r}", f'=IF(G{r}="","",G{r}-N(H{r}))', USD, bold=True)
    calc(inc, f"J{r}", ym("A", r), "0")
dv_list(inc, f"D6:D{IE}", ICL); dv_list(inc, f"E6:E{IE}", MTL)
ex_inc = [("2027-01-04", "Etsy payout", "Week 1 orders (14)", "Product sales", "Etsy / marketplace", "", 612.40, 71.30),
          ("2027-01-09", "Harbour Cafe", "Menu illustrations", "Services / client work", "Bank transfer", "INV-1001", 850, 0),
          ("2027-01-11", "Etsy payout", "Week 2 orders (9)", "Product sales", "Etsy / marketplace", "", 398.20, 46.10),
          ("2027-01-15", "Craft fair (Winter Market)", "Market day takings", "Product sales", "Card", "", 540, 14.85),
          ("2027-01-22", "Willow & Co (shop)", "Wholesale order 40 pcs", "Wholesale", "Bank transfer", "INV-1002", 960, 0),
          ("2027-01-26", "Linocut workshop", "6 seats", "Workshops / classes", "Stripe", "", 330, 10.47),
          ("2027-02-01", "Etsy payout", "Week 5 orders (11)", "Product sales", "Etsy / marketplace", "", 476.90, 55.60),
          ("2027-02-12", "Harbour Cafe", "Poster set", "Services / client work", "Bank transfer", "INV-1003", 420, 0),
          ("2027-02-20", "Affiliate", "Blog links", "Affiliate / ads", "PayPal", "", 38.12, 1.41),
          ("2027-03-05", "Etsy payout", "Week 9 orders (18)", "Product sales", "Etsy / marketplace", "", 803.70, 93.20),
          ("2027-03-18", "Bloom Florist", "Logo + cards", "Services / client work", "Bank transfer", "INV-1004", 1150, 0)]
import datetime as _dt
for i, row in enumerate(ex_inc):
    r = 6 + i
    for col, val in zip("ABCDEFGH", row):
        if val == "": continue
        inc[f"{col}{r}"] = _dt.date.fromisoformat(val) if col == "A" else val
INC = lambda c: f"Income!${c}$6:${c}${IE}"

# ---------- Expenses ----------
ex = wb.create_sheet("Expenses")
banner(ex, t, "Expenses", "Every business cost. Business use % = the share that's for the business (100% for most things).", 12)
header(ex, 5, ["Date", "Paid to", "What for", "Category", "Method", "Amount", "Business use %", "DEDUCTIBLE", "Receipt saved?", "Month", "Tax line", "Notes"], t)
for i, w in enumerate([12, 22, 28, 24, 16, 12, 10, 13, 10, 8, 20, 22]): ex.column_dimensions[gl(i + 1)].width = w
ex.freeze_panes = "B6"
for r in range(6, EE + 1):
    for col in "ABCDEFGIL": inp(ex, f"{col}{r}")
    for col in "BCDEL": ex[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    ex[f"A{r}"].number_format = "dd mmm yyyy"; ex[f"F{r}"].number_format = USD; ex[f"G{r}"].number_format = "0%"
    calc(ex, f"H{r}", f'=IF(F{r}="","",F{r}*IF(G{r}="",1,G{r}))', USD, bold=True)
    calc(ex, f"J{r}", ym("A", r), "0")
    calc(ex, f"K{r}", f'=IF(D{r}="","",IFERROR(INDEX(Setup!$E$16:$E${15 + NEC},MATCH(D{r},Setup!$D$16:$D${15 + NEC},0)),""))')
    ex[f"K{r}"].font = Font(name=F, size=9, color=GREY)
dv_list(ex, f"D6:D{EE}", ECL); dv_list(ex, f"E6:E{EE}", MTL); dv_list(ex, f"I6:I{EE}", "Yes,No")
ex.conditional_formatting.add(f"I6:I{EE}", CellIsRule(operator="equal", formula=['"No"'], fill=red, font=REDF))
ex.conditional_formatting.add(f"I6:I{EE}", CellIsRule(operator="equal", formula=['"Yes"'], fill=grn, font=GRNF))
ex_exp = [("2027-01-02", "Adobe", "Creative Cloud", "Software & subscriptions", "Card", 59.99, None, "Yes"),
          ("2027-01-03", "Paper Mill Supply", "Card stock + inks", "Materials & supplies", "Card", 186.40, None, "Yes"),
          ("2027-01-05", "Etsy", "Listing + ads fees (Dec)", "Platform & selling fees", "Etsy / marketplace", 42.80, None, "Yes"),
          ("2027-01-08", "BoxCo", "Mailers + tissue", "Packaging & shipping", "Card", 74.25, None, "Yes"),
          ("2027-01-10", "Phone company", "Mobile plan", "Phone & internet", "Card", 48, 0.6, "Yes"),
          ("2027-01-14", "Winter Market", "Stall fee", "Rent / workspace", "Card", 65, None, "No"),
          ("2027-01-20", "Post Office", "Postage (Jan)", "Packaging & shipping", "Card", 131.60, None, "Yes"),
          ("2027-01-28", "Meta", "Instagram ads", "Advertising & marketing", "Card", 40, None, "Yes"),
          ("2027-02-03", "Craft Hardware", "Lino cutter set", "Equipment & tools", "Card", 89.95, None, "Yes"),
          ("2027-02-10", "Insurer", "Liability insurance (year)", "Insurance", "Bank transfer", 210, None, "Yes"),
          ("2027-02-16", "Paper Mill Supply", "Kraft paper", "Materials & supplies", "Card", 64.10, None, "No"),
          ("2027-03-01", "Coworking Hub", "Desk day passes", "Rent / workspace", "Card", 120, None, "Yes"),
          ("2027-03-12", "Bookkeeper", "Year-end help", "Legal & professional", "Bank transfer", 150, None, "Yes")]
for i, row in enumerate(ex_exp):
    r = 6 + i
    for col, val in zip("ABCDEFGI", row):
        if val is None: continue
        ex[f"{col}{r}"] = _dt.date.fromisoformat(val) if col == "A" else val
EXP = lambda c: f"Expenses!${c}$6:${c}${EE}"

# ---------- Mileage ----------
mi = wb.create_sheet("Mileage")
banner(mi, t, "Mileage log", "Business trips only. Miles x your rate (Setup) = your mileage deduction.", 9)
header(mi, 5, ["Date", "From", "To", "Purpose", "Miles / km (one way)", "Round trip?", "TOTAL", "DEDUCTION", "Month"], t)
for i, w in enumerate([12, 20, 20, 30, 12, 10, 10, 13, 8]): mi.column_dimensions[gl(i + 1)].width = w
mi.freeze_panes = "B6"
for r in range(6, ME + 1):
    for col in "ABCDEF": inp(mi, f"{col}{r}")
    for col in "BCD": mi[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    mi[f"A{r}"].number_format = "dd mmm yyyy"; mi[f"E{r}"].number_format = "0.0"
    calc(mi, f"G{r}", f'=IF(E{r}="","",E{r}*IF(F{r}="Yes",2,1))', "0.0")
    calc(mi, f"H{r}", f'=IF(G{r}="","",G{r}*{MR})', USD, bold=True)
    calc(mi, f"I{r}", ym("A", r), "0")
dv_list(mi, f"F6:F{ME}", "Yes,No")
for i, row in enumerate([("2027-01-03", "Studio", "Paper Mill Supply", "Buy card stock", 8.4, "Yes"), ("2027-01-15", "Studio", "Town Hall", "Winter Market stall", 12, "Yes"),
                         ("2027-01-22", "Studio", "Willow & Co", "Deliver wholesale order", 17.5, "Yes"), ("2027-02-12", "Studio", "Harbour Cafe", "Client meeting", 5.2, "Yes"),
                         ("2027-03-18", "Studio", "Bloom Florist", "Logo presentation", 9.8, "Yes")]):
    for col, val in zip("ABCDEF", row): mi[f"{col}{6 + i}"] = _dt.date.fromisoformat(val) if col == "A" else val
MIL = lambda c: f"Mileage!${c}$6:${c}${ME}"

# ---------- Invoices ----------
iv = wb.create_sheet("Invoices")
banner(iv, t, "Invoices", "Who owes you what. Mark Paid = Yes when the money lands, then log it on the Income tab.", 10)
header(iv, 5, ["Invoice #", "Client", "What for", "Issue date", "Terms (days)", "DUE DATE", "Amount", "Paid?", "Date paid", "STATUS", "DAYS LATE"], t)
for i, w in enumerate([12, 24, 28, 12, 9, 13, 12, 8, 12, 12, 9]): iv.column_dimensions[gl(i + 1)].width = w
iv.freeze_panes = "B6"
for r in range(6, VE + 1):
    for col in "ABCDEGHI": inp(iv, f"{col}{r}")
    for col in "BC": iv[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    iv[f"D{r}"].number_format = "dd mmm yyyy"; iv[f"I{r}"].number_format = "dd mmm yyyy"; iv[f"G{r}"].number_format = USD
    calc(iv, f"F{r}", f'=IF(D{r}="","",D{r}+IF(E{r}="",30,E{r}))', "dd mmm yyyy")
    calc(iv, f"J{r}", f'=IF(A{r}="","",IF(H{r}="Yes","Paid",IF(F{r}="","",IF(TODAY()>F{r},"Overdue",IF(F{r}-TODAY()<=7,"Due soon","Not due yet")))))', None, bold=True)
    calc(iv, f"K{r}", f'=IF(J{r}="Overdue",TODAY()-F{r},"")', "0")
dv_list(iv, f"H6:H{VE}", "Yes,No")
for val, fill, f_ in (('"Overdue"', red, REDF), ('"Due soon"', amb, AMBF), ('"Paid"', grn, GRNF)):
    iv.conditional_formatting.add(f"J6:J{VE}", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
for i, (no, cl, wh, dd, terms, amt, pd, pdd) in enumerate([
        ("INV-1001", "Harbour Cafe", "Menu illustrations", "2027-01-02", 14, 850, "Yes", "2027-01-09"),
        ("INV-1002", "Willow & Co (shop)", "Wholesale order 40 pcs", "2027-01-08", 30, 960, "Yes", "2027-01-22"),
        ("INV-1003", "Harbour Cafe", "Poster set", "2027-02-01", 14, 420, "Yes", "2027-02-12"),
        ("INV-1004", "Bloom Florist", "Logo + cards", "2027-03-04", 14, 1150, "Yes", "2027-03-18"),
        ("INV-1005", "Willow & Co (shop)", "Spring wholesale 60 pcs", "=TODAY()-38", 30, 1440, "No", None),
        ("INV-1006", "Oak Street Bakery", "Packaging labels", "=TODAY()-10", 14, 380, "No", None),
        ("INV-1007", "Harbour Cafe", "Summer menu", "=TODAY()-2", 30, 650, "No", None)]):
    r = 6 + i; iv[f"A{r}"] = no; iv[f"B{r}"] = cl; iv[f"C{r}"] = wh
    iv[f"D{r}"] = dd if dd.startswith("=") else _dt.date.fromisoformat(dd); iv[f"E{r}"] = terms; iv[f"G{r}"] = amt; iv[f"H{r}"] = pd
    if pdd: iv[f"I{r}"] = _dt.date.fromisoformat(pdd)
INV = lambda c: f"Invoices!${c}$6:${c}${VE}"

# ---------- Profit & Loss ----------
pl = wb.create_sheet("Profit & Loss")
banner(pl, t, "Profit & loss", "Month by month, all automatic. Only rows dated in your tax year count.", 15)
pl.column_dimensions["A"].width = 30
for k in range(2, 16): pl.column_dimensions[gl(k)].width = 11
pl.column_dimensions["N"].width = 13; pl.column_dimensions["O"].width = 9
header(pl, 5, [""] + MONTHS + ["YEAR", "% of income"], t)
pl["A5"] = '="Tax year "&' + YR; pl["A5"].font = Font(name=F, bold=True, color="FFFFFF")
pl.freeze_panes = "B6"
def sec(r, text):
    c = pl.cell(r, 1, text); c.font = Font(name=F, bold=True, color=t.main, size=11)
    for k in range(1, 16): pl.cell(r, k).fill = t.band
r = 6; sec(r, "INCOME"); r += 1
ICROW = r
for i, cat in enumerate(ICATS):
    pl[f"A{r}"] = f"=Setup!A{16 + i}"; pl[f"A{r}"].font = Font(name=F, size=10)
    for m in range(12):
        calc(pl, f"{gl(m + 2)}{r}", f'=IF($A{r}="",0,SUMIFS({INC("G")},{INC("D")},$A{r},{INC("J")},{m + 1}))', USD0)
    calc(pl, f"N{r}", f"=SUM(B{r}:M{r})", USD0, bold=True); r += 1
ICEND = r - 1
GI = r; label(pl, f"A{r}", "Gross income", bold=True)
for k in range(2, 15): calc(pl, f"{gl(k)}{r}", f"=SUM({gl(k)}{ICROW}:{gl(k)}{ICEND})", USD0, bold=True)
r += 1; FE = r; label(pl, f"A{r}", "Less: fees taken from payments", size=10)
for m in range(12): calc(pl, f"{gl(m + 2)}{r}", f'=SUMIFS({INC("H")},{INC("J")},{m + 1})', USD0)
calc(pl, f"N{r}", f"=SUM(B{r}:M{r})", USD0, bold=True)
r += 1; NI_ = r; label(pl, f"A{r}", "NET INCOME", bold=True)
for k in range(2, 15): calc(pl, f"{gl(k)}{r}", f"={gl(k)}{GI}-{gl(k)}{FE}", USD0, bold=True)
r += 2; sec(r, "EXPENSES (deductible part)"); r += 1
ECROW = r
for i in range(NEC):
    pl[f"A{r}"] = f"=Setup!D{16 + i}"; pl[f"A{r}"].font = Font(name=F, size=10)
    for m in range(12):
        calc(pl, f"{gl(m + 2)}{r}", f'=IF($A{r}="",0,SUMIFS({EXP("H")},{EXP("D")},$A{r},{EXP("J")},{m + 1}))', USD0)
    calc(pl, f"N{r}", f"=SUM(B{r}:M{r})", USD0, bold=True); r += 1
MROW = r; label(pl, f"A{r}", "Mileage deduction", size=10)
for m in range(12): calc(pl, f"{gl(m + 2)}{r}", f'=SUMIFS({MIL("H")},{MIL("I")},{m + 1})', USD0)
calc(pl, f"N{r}", f"=SUM(B{r}:M{r})", USD0, bold=True); r += 1
TE = r; label(pl, f"A{r}", "TOTAL EXPENSES", bold=True)
for k in range(2, 15): calc(pl, f"{gl(k)}{r}", f"=SUM({gl(k)}{ECROW}:{gl(k)}{MROW})", USD0, bold=True)
r += 2; NP = r; label(pl, f"A{r}", "NET PROFIT", bold=True, size=12)
for k in range(2, 15): calc(pl, f"{gl(k)}{r}", f"={gl(k)}{NI_}-{gl(k)}{TE}", '"$"#,##0;[Red]-"$"#,##0', bold=True)
r += 1; SA = r; label(pl, f"A{r}", "Tax to set aside", bold=True)
for k in range(2, 15): calc(pl, f"{gl(k)}{r}", f"=MAX(0,{gl(k)}{NP})*{TAX}", USD0)
r += 1; CUM = r; label(pl, f"A{r}", "Profit so far this year", size=10)
for m in range(12): calc(pl, f"{gl(m + 2)}{r}", f"=SUM($B{NP}:{gl(m + 2)}{NP})", '"$"#,##0;[Red]-"$"#,##0')
for rr in list(range(ICROW, ICEND + 1)) + [GI, FE, NI_] + list(range(ECROW, MROW + 1)) + [TE, NP, SA]:
    calc(pl, f"O{rr}", f'=IF($N${GI}=0,"",N{rr}/$N${GI})', "0.0%")
pl.conditional_formatting.add(f"B{NP}:N{NP}", CellIsRule(operator="lessThan", formula=["0"], fill=red, font=REDF))
pl.conditional_formatting.add(f"B{ECROW}:M{MROW}", FormulaRule(formula=[f"B{ECROW}>0"], font=Font(name=F, color="1F3B4D", bold=True)))

# ---------- Quarterly Tax ----------
q = wb.create_sheet("Quarterly Tax")
banner(q, t, "Quarterly tax set-aside", "Profit each quarter, what to set aside, and whether you've paid or moved it to savings.", 9)
header(q, 5, ["Quarter", "First month", "Last month", "Due date", "Net profit", "SET ASIDE", "Amount paid / saved", "Still to set aside", "STATUS"], t)
for i, w in enumerate([10, 11, 11, 14, 13, 13, 15, 15, 12]): q.column_dimensions[gl(i + 1)].width = w
for i, (qq, a, z) in enumerate([("Q1", 1, 3), ("Q2", 4, 5), ("Q3", 6, 8), ("Q4", 9, 12)]):
    rr = 6 + i; q[f"A{rr}"] = qq; q[f"A{rr}"].font = Font(name=F, bold=True)
    inp(q, f"B{rr}", a, "0"); inp(q, f"C{rr}", z, "0")
    calc(q, f"D{rr}", f"=Setup!F{5 + i}", "dd mmm yyyy")
    calc(q, f"E{rr}", f"=SUMPRODUCT(('Profit & Loss'!$B$4:$M$4>=B{rr})*('Profit & Loss'!$B$4:$M$4<=C{rr})*'Profit & Loss'!$B${NP}:$M${NP})", '"$"#,##0;[Red]-"$"#,##0')
    calc(q, f"F{rr}", f"=MAX(0,E{rr})*{TAX}", USD0, bold=True)
    inp(q, f"G{rr}", None, USD0)
    calc(q, f"H{rr}", f"=MAX(0,F{rr}-N(G{rr}))", USD0)
    calc(q, f"I{rr}", f'=IF(F{rr}=0,"Nothing due",IF(H{rr}=0,"Done",IF(TODAY()>D{rr},"Overdue",IF(D{rr}-TODAY()<=21,"Due soon","Later"))))', None, bold=True)
# month numbers above P&L month columns (hidden helper row 4) for SUMPRODUCT
for m in range(12):
    c = pl.cell(4, m + 2, m + 1); c.font = Font(name=F, size=8, color="FFFFFF"); c.fill = t.head
q["G6"] = 300
label(q, "A11", "TOTAL", bold=True)
for col in "EFGH": calc(q, f"{col}11", f"=SUM({col}6:{col}9)", USD0, bold=True)
for val, fill, f_ in (('"Overdue"', red, REDF), ('"Due soon"', amb, AMBF), ('"Done"', grn, GRNF)):
    q.conditional_formatting.add("I6:I9", CellIsRule(operator="equal", formula=[val], fill=fill, font=f_))
label(q, "A13", "Months are the US estimated-tax quarters by default (Q2 = Apr-May, Q3 = Jun-Aug). Change First / Last month and the due dates in Setup for your country.", italic=True, size=9, color=GREY)
q.merge_cells("A13:I14")
label(q, "A15", "Tip: move each quarter's SET ASIDE amount into a separate savings account the day you see it. Future you will be very grateful.", italic=True, size=10, color="2B5F55")
q.merge_cells("A15:I15")

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Your year at a glance. Everything updates from the other tabs.", 10)
widths(d, {"A": 32, "B": 18, "C": 3, "D": 26, "E": 14, "F": 12})
d.merge_cells("A4:B4"); c = d["A4"]; c.value = '=Setup!B5&"  •  tax year "&Setup!B6'; c.font = Font(name=F, size=14, bold=True, color=t.main)
kpi = [("NET PROFIT (year)", f"='Profit & Loss'!N{NP}", '"$"#,##0;[Red]-"$"#,##0'),
       ("Gross income", f"='Profit & Loss'!N{GI}", USD0), ("Fees taken", f"='Profit & Loss'!N{FE}", USD0),
       ("Total expenses (incl. mileage)", f"='Profit & Loss'!N{TE}", USD0),
       ("Profit margin", f"='Profit & Loss'!O{NP}", "0%"),
       ("Tax to set aside (year)", f"='Profit & Loss'!N{SA}", USD0),
       ("Still to set aside", "='Quarterly Tax'!H11", USD0),
       ("Next tax due date", '=IFERROR(INDEX(\'Quarterly Tax\'!D6:D9,MATCH(TRUE,INDEX(\'Quarterly Tax\'!D6:D9>=TODAY(),0),0)),"")', "ddd d mmm yyyy"),
       ("Unpaid invoices", f'=SUMIFS({INV("G")},{INV("H")},"<>Yes",{INV("A")},"<>")', USD0),
       ("Overdue invoices", f'=COUNTIF({INV("J")},"Overdue")', "0"),
       ("Business miles", f'=SUMIFS({MIL("G")},{MIL("I")},">0")', "#,##0"),
       ("Expenses missing a receipt", f'=COUNTIFS({EXP("I")},"No",{EXP("J")},">0")', "0"),
       ("Bank balance estimate", f"={OB}+'Profit & Loss'!N{NI_}-SUMIFS({EXP('F')},{EXP('J')},\">0\")", USD0)]
for i, (a, f_, fmt) in enumerate(kpi):
    r = 5 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f_, fmt, big=True); d.row_dimensions[r].height = 26
d["B5"].fill = PatternFill("solid", fgColor="D6EBE4"); d["B10"].fill = PatternFill("solid", fgColor="FCEBC8")
label(d, "A18", "Bank balance estimate = opening balance + net income - what you actually paid for expenses (before tax payments and owner draws).", italic=True, size=9, color=GREY)
d.merge_cells("A18:B19")
for c_ in ("B13", "B14"):
    d.conditional_formatting.add(c_, CellIsRule(operator="greaterThan", formula=["0"], fill=red, font=Font(name=F, size=16, bold=True, color="A12A1E")))
header(d, 4, ["Top expense categories", "Year", "Share"], t, start=4)
for i in range(6):
    rr = 5 + i
    calc(d, f"E{rr}", f"=LARGE('Profit & Loss'!$N${ECROW}:$N${MROW},{i + 1})", USD0)
    calc(d, f"D{rr}", f'=IF(E{rr}=0,"",INDEX(\'Profit & Loss\'!$A${ECROW}:$A${MROW},MATCH(E{rr},\'Profit & Loss\'!$N${ECROW}:$N${MROW},0)))')
    d[f"D{rr}"].alignment = Alignment(horizontal="left", indent=1)
    calc(d, f"F{rr}", f"=IF('Profit & Loss'!$N${TE}=0,\"\",E{rr}/'Profit & Loss'!$N${TE})", "0%")
d.conditional_formatting.add("F5:F10", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="3E8E7E"))
# chart data
header(d, 12, ["Month", "Net income", "Expenses", "Profit"], t, start=4)
d.column_dimensions["G"].width = 12
for m in range(12):
    rr = 13 + m; d[f"D{rr}"] = MONTHS[m]; d[f"D{rr}"].font = Font(name=F, size=10)
    calc(d, f"E{rr}", f"='Profit & Loss'!{gl(m + 2)}{NI_}", USD0); calc(d, f"F{rr}", f"='Profit & Loss'!{gl(m + 2)}{TE}", USD0)
    calc(d, f"G{rr}", f"='Profit & Loss'!{gl(m + 2)}{NP}", '"$"#,##0;[Red]-"$"#,##0')
ch = BarChart(); ch.type = "col"; ch.style = 10; ch.title = "Net income vs expenses"; ch.height = 8.5; ch.width = 20
ch.add_data(Reference(d, min_col=5, max_col=6, min_row=12, max_row=24), titles_from_data=True)
ch.set_categories(Reference(d, min_col=4, min_row=13, max_row=24))
ch.series[0].graphicalProperties.solidFill = "3E8E7E"; ch.series[1].graphicalProperties.solidFill = "E8B04B"
ln = LineChart(); ln.add_data(Reference(d, min_col=7, min_row=12, max_row=24), titles_from_data=True)
ln.series[0].graphicalProperties.line.solidFill = "1F3B4D"; ln.series[0].graphicalProperties.line.width = 28000
ch += ln
d.add_chart(ch, "I4")

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.move_sheet("Dashboard", offset=-(len(wb.sheetnames) - 2))
wb.save(sys.argv[1]); print("saved", GI, NI_, TE, NP, SA)
