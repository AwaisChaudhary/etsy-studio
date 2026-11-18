import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import PatternFill
t = Theme("1D5C63", "2F8F8A", "E3F1EF")
wb = Workbook()
# ---------- Start here
s = wb.active; s.title = "Start Here"
banner(s, t, "Cleaning Business Quote & Client Tracker", "Price every job with confidence and keep your regular clients organised.", 6)
widths(s, {"A": 6, "B": 90})
steps = [
  ("1", "Open the Settings tab and type your own numbers in the yellow cells: what you want to earn per hour, your supply and travel costs, your profit margin and minimum price."),
  ("2", "Adjust the time estimates (minutes per bedroom, bathroom and extra task) to match how fast you and your team work."),
  ("3", "Use the Quote tab for each new enquiry. Fill in the yellow cells and the price per visit appears instantly, with the full cost breakdown."),
  ("4", "Add clients who book you to the Clients tab. Next clean dates and monthly value are worked out for you."),
  ("5", "Plan each week on the This Week tab. Pick clients from the drop-down list; their address and price fill in automatically."),
  ("6", "Check the Dashboard for your active clients, monthly recurring income and this week's takings."),
]
label(s, "B4", "How to use it", bold=True, size=14)
for i, (n, txt) in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, n); c.font = Font(name=F, size=14, bold=True, color="2F8F8A"); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Works in Microsoft Excel and Google Sheets (File > Import, or upload to Google Drive and open with Google Sheets). Example rows are included so you can see how each tab works; type over them or delete them.", italic=True, size=10)
s.row_dimensions[14].height = 40
label(s, "B16", "Prices in this file are examples only. Every area and business is different, so always set your own rates.", italic=True, size=10)

# ---------- Settings
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your rates and time estimates. Everything else in the workbook uses these.", 5)
widths(st, {"A": 40, "B": 16, "C": 18, "D": 4, "E": 50})
label(st, "A4", "Your rates", bold=True, size=13)
rows = [("Business name", "Sparkle & Co. Cleaning", "@", None),
        ("Pay per cleaner per hour ($)", 25, '"$"#,##0.00', "What you want to earn for each hour worked, per person."),
        ("Supplies cost per work hour ($)", 2.5, '"$"#,##0.00', "Average spend on products, cloths and bags per hour of cleaning."),
        ("Travel cost per mile or km ($)", 0.7, '"$"#,##0.00', "Fuel and vehicle wear. Use your own figure."),
        ("Target profit margin", 0.25, "0%", "Share of the final price kept as profit after all costs."),
        ("Minimum price per visit ($)", 90, '"$"#,##0', "No visit will be quoted below this."),
        ("Round prices up to the nearest ($)", 5, '"$"#,##0', "For tidy prices, e.g. 5 gives $135 instead of $132.40.")]
for i, (a, v, fmt, note) in enumerate(rows):
    r = 5 + i; label(st, f"A{r}", a); inp(st, f"B{r}", v, fmt, note)
st["B5"].alignment = Alignment(horizontal="left", indent=1)
label(st, "A13", "Time estimates (minutes)", bold=True, size=13)
for i, (a, v) in enumerate([("Base time: kitchen and living areas", 60), ("Per bedroom", 25), ("Per bathroom", 35)]):
    r = 14 + i; label(st, f"A{r}", a); inp(st, f"B{r}", v, "0")
header(st, 19, ["Type of clean", "Time multiplier"], t)
for i, (a, v) in enumerate([("Standard", 1.0), ("Deep clean", 1.6), ("Move-in / move-out", 1.9)]):
    r = 20 + i; inp(st, f"A{r}", a); st[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); inp(st, f"B{r}", v, "0.0x")
header(st, 25, ["How often", "Discount", "Visits per month"], t)
for i, (a, d, v) in enumerate([("One-time", 0, 0), ("Weekly", 0.15, 4.33), ("Every 2 weeks", 0.10, 2.17), ("Monthly", 0.05, 1)]):
    r = 26 + i; inp(st, f"A{r}", a); st[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); inp(st, f"B{r}", d, "0%"); inp(st, f"C{r}", v, "0.00")
header(st, 32, ["Extra task", "Minutes"], t)
extras = [("Inside oven", 30), ("Inside fridge", 30), ("Interior windows", 45), ("Laundry (one load)", 20), ("Inside cabinets", 40), ("Baseboards", 30)]
for i, (a, v) in enumerate(extras):
    r = 33 + i; inp(st, f"A{r}", a); st[f"A{r}"].alignment = Alignment(horizontal="left", indent=1); inp(st, f"B{r}", v, "0")
label(st, "E5", "Tip: if quotes come out too high or low compared with local prices, adjust the pay per hour and the time estimates first.", italic=True, size=10)
st.row_dimensions[5].height = 30

# ---------- Quote
q = wb.create_sheet("Quote")
banner(q, t, "Quote calculator", "Fill in the yellow cells. The price per visit updates instantly.", 6)
widths(q, {"A": 30, "B": 22, "C": 12, "D": 4, "E": 34, "F": 18})
label(q, "A4", "The job", bold=True, size=13)
qi = [("Client name", "Jordan Lee", "@"), ("Date", "=TODAY()", "dd mmm yyyy"), ("Bedrooms", 3, "0"), ("Bathrooms", 2, "0"),
      ("Type of clean", "Standard", "@"), ("How often", "Every 2 weeks", "@"), ("Number of cleaners", 2, "0"), ("Round-trip distance (miles or km)", 12, "0.0")]
for i, (a, v, fmt) in enumerate(qi):
    r = 5 + i; label(q, f"A{r}", a); inp(q, f"B{r}", v, fmt)
dv_list(q, "B9", "=Settings!$A$20:$A$22"); dv_list(q, "B10", "=Settings!$A$26:$A$29")
header(q, 14, ["Extra tasks", "Add it?", "Minutes"], t)
yes = dv_list(q, "B15:B20", "Yes,No")
for i in range(6):
    r = 15 + i
    calc(q, f"A{r}", f"=Settings!A{33 + i}"); q[f"A{r}"].alignment = Alignment(horizontal="left", indent=1)
    inp(q, f"B{r}", "Yes" if i == 1 else "No")
    calc(q, f"C{r}", f'=IF(B{r}="Yes",Settings!B{33 + i},0)', "0")
label(q, "E4", "The numbers", bold=True, size=13)
res = [("Base minutes", "=Settings!B14+B7*Settings!B15+B8*Settings!B16", "0"),
       ("Clean type multiplier", "=IFERROR(INDEX(Settings!$B$20:$B$22,MATCH(B9,Settings!$A$20:$A$22,0)),1)", "0.0x"),
       ("Extra task minutes", "=SUM(C15:C20)", "0"),
       ("Total work hours (all cleaners)", "=(F5*F6+F7)/60", "0.0"),
       ("Hours on site", "=F8/MAX(1,B11)", "0.0"),
       ("Labour cost", "=F8*Settings!B6", '"$"#,##0.00'),
       ("Supplies", "=F8*Settings!B7", '"$"#,##0.00'),
       ("Travel", "=B12*Settings!B8", '"$"#,##0.00'),
       ("Total cost", "=SUM(F10:F12)", '"$"#,##0.00'),
       ("Price before discount", "=F13/(1-Settings!B9)", '"$"#,##0.00'),
       ("Regular-client discount", "=IFERROR(INDEX(Settings!$B$26:$B$29,MATCH(B10,Settings!$A$26:$A$29,0)),0)", "0%")]
for i, (a, f, fmt) in enumerate(res):
    r = 5 + i; label(q, f"E{r}", a); calc(q, f"F{r}", f, fmt)
label(q, "E17", "PRICE PER VISIT", bold=True, size=13, color="1D5C63")
calc(q, "F17", "=MAX(Settings!B10,CEILING(F14*(1-F15),Settings!B11))", '"$"#,##0', big=True); q.row_dimensions[17].height = 34
label(q, "E18", "Your profit per visit"); calc(q, "F18", "=F17-F13", '"$"#,##0.00', bold=True)
label(q, "E19", "Monthly income from this client"); calc(q, "F19", "=F17*IFERROR(INDEX(Settings!$C$26:$C$29,MATCH(B10,Settings!$A$26:$A$29,0)),0)", '"$"#,##0', bold=True)
label(q, "E20", "One-time jobs show $0 monthly income.", italic=True, size=9)
legend(q, 23, 1)

# ---------- Clients
c = wb.create_sheet("Clients")
banner(c, t, "Clients", "One row per client. Next clean and monthly value are calculated.", 11)
cols = ["Client", "Phone", "Address", "How often", "Price per visit", "Usual day", "Last clean", "Next clean", "Monthly value", "Status", "Notes"]
header(c, 5, cols, t)
widths(c, {"A": 22, "B": 16, "C": 30, "D": 16, "E": 14, "F": 12, "G": 14, "H": 14, "I": 15, "J": 12, "K": 34})
c.freeze_panes = "B6"
ex = ["Jordan Lee", "555-0142", "12 Elm Street", "Every 2 weeks", 135, "Tue", "=TODAY()-6", None, None, "Active", "Key under mat. Dog friendly."]
N = 105
for r in range(6, N + 1):
    for col in "ABCDEFGJK":
        inp(c, f"{col}{r}")
        c[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    c[f"E{r}"].number_format = '"$"#,##0'; c[f"G{r}"].number_format = "dd mmm yyyy"
    calc(c, f"H{r}", f'=IF(OR(G{r}="",D{r}="",D{r}="One-time"),"",IF(D{r}="Monthly",EDATE(G{r},1),G{r}+IF(D{r}="Weekly",7,14)))', "dd mmm yyyy")
    calc(c, f"I{r}", f'=IF(OR(E{r}="",J{r}<>"Active"),"",E{r}*IFERROR(INDEX(Settings!$C$26:$C$29,MATCH(D{r},Settings!$A$26:$A$29,0)),0))', '"$"#,##0')
for i, v in enumerate(ex):
    if v is not None: c.cell(6, i + 1).value = v
dv_list(c, f"D6:D{N}", "=Settings!$A$26:$A$29"); dv_list(c, f"F6:F{N}", "Mon,Tue,Wed,Thu,Fri,Sat,Sun"); dv_list(c, f"J6:J{N}", "Active,Paused,Ended")
c.conditional_formatting.add(f"A6:K{N}", FormulaRule(formula=[f'$J6="Ended"'], font=Font(name=F, color="9AA4B8")))

# ---------- This week
w = wb.create_sheet("This Week")
banner(w, t, "This week's schedule", "Pick the week's start date, then add jobs. Address and price fill in from the Clients tab.", 8)
widths(w, {"A": 10, "B": 14, "C": 10, "D": 22, "E": 32, "F": 13, "G": 10, "H": 10})
label(w, "A4", "Week starting (a Monday)", bold=True); w.merge_cells("A4:C4"); inp(w, "D4", "=TODAY()-WEEKDAY(TODAY(),3)", "dddd dd mmm yyyy")
header(w, 6, ["Day", "Date", "Time", "Client", "Address", "Price", "Done?", "Paid?"], t)
w.freeze_panes = "A7"
for r in range(7, 42):
    for col in "ACDGH": inp(w, f"{col}{r}")
    w[f"C{r}"].number_format = "h:mm AM/PM"
    calc(w, f"B{r}", f'=IF(A{r}="","",$D$4+MATCH(A{r},{{"Mon","Tue","Wed","Thu","Fri","Sat","Sun"}},0)-1)', "ddd dd mmm")
    calc(w, f"E{r}", f'=IF(D{r}="","",IFERROR(INDEX(Clients!$C$6:$C${N},MATCH(D{r},Clients!$A$6:$A${N},0)),""))')
    calc(w, f"F{r}", f'=IF(D{r}="","",IFERROR(INDEX(Clients!$E$6:$E${N},MATCH(D{r},Clients!$A$6:$A${N},0)),""))', '"$"#,##0')
    w[f"E{r}"].alignment = Alignment(horizontal="left", indent=1)
w["A7"] = "Tue"; w["C7"] = 0.375; w["D7"] = "Jordan Lee"; w["G7"] = "No"; w["H7"] = "No"
dv_list(w, "A7:A41", "Mon,Tue,Wed,Thu,Fri,Sat,Sun"); dv_list(w, "D7:D41", f"=Clients!$A$6:$A${N}"); dv_list(w, "G7:H41", "Yes,No")
label(w, "E43", "Booked this week", bold=True); calc(w, "F43", "=SUM(F7:F41)", '"$"#,##0', bold=True)
label(w, "E44", "Paid so far", bold=True); calc(w, "F44", '=SUMIFS(F7:F41,H7:H41,"Yes")', '"$"#,##0', bold=True)
w.conditional_formatting.add("A7:H41", FormulaRule(formula=['$H7="Yes"'], fill=PatternFill("solid", fgColor="DFF3E4")))

# ---------- Dashboard
d = wb.create_sheet("Dashboard")
banner(d, t, "Dashboard", "Your business at a glance.", 4)
widths(d, {"A": 40, "B": 20})
kp = [("Active clients", f'=COUNTIF(Clients!J6:J{N},"Active")', "0"),
      ("Monthly recurring income", f"=SUM(Clients!I6:I{N})", '"$"#,##0'),
      ("Yearly recurring income (estimate)", "=B6*12", '"$"#,##0'),
      ("Average price per visit", f'=IFERROR(AVERAGEIF(Clients!E6:E{N},">0"),0)', '"$"#,##0'),
      ("Booked this week", "='This Week'!F43", '"$"#,##0'),
      ("Paid this week", "='This Week'!F44", '"$"#,##0')]
for i, (a, f, fmt) in enumerate(kp):
    r = 5 + i; label(d, f"A{r}", a, bold=True, size=12); calc(d, f"B{r}", f, fmt, big=True); d.row_dimensions[r].height = 30
wb.move_sheet("Dashboard", offset=-4)
for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.save(sys.argv[1])
print("saved")
