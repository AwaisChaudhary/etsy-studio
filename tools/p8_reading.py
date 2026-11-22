"""2027 Reading Tracker Spreadsheet (batch 5, lane b): book log with ratings, reading goal, 2027 reading challenge (36 prompts),
TBR list with priority, monthly & genre stats dashboard. Excel + Google Sheets."""
import sys, datetime as dt; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule, CellIsRule, DataBarRule

t = Theme("2B3A55", "B8546A", "F3E7E4")
YEAR = 2027
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
GENRES = ["Fantasy", "Romance", "Mystery & Thriller", "Literary Fiction", "Historical Fiction", "Science Fiction", "Horror",
          "Contemporary", "Young Adult", "Non-fiction", "Memoir", "Self-help", "Classics", "Poetry", "Graphic Novel", "Other"]
FORMATS = ["Paperback", "Hardback", "Ebook", "Audiobook", "Library", "Kindle Unlimited"]
STATUS = ["Finished", "Reading", "DNF", "Paused"]
NB = 405     # book log rows 7..405 (399 books)
NT = 206     # TBR rows 6..206
wb = Workbook()

# ---------- Start Here ----------
s = wb.active; s.title = "Start Here"
banner(s, t, "2027 Reading Tracker", "Log every book, rate it, chase your reading goal and finish the 2027 reading challenge.", 6)
widths(s, {"A": 6, "B": 98})
steps = ["Settings: type your 2027 goal (books and pages). Rename genres or formats if you like; the drop-downs update.",
         "Book Log: one row per book. Pick the genre, format and status, type the pages, dates and your star rating (1 to 5, halves allowed).",
         "Dashboard: books and pages read, goal progress, average rating, books per month, favourite genres, formats and your top-rated reads.",
         "Reading Challenge: 36 prompts for 2027. Type the title of the book you read for each prompt; it ticks itself off when that book is Finished in your log.",
         "TBR List: your to-be-read pile with priority, where it's from, and whether you already own it.",
         "Tip: leave a cell blank rather than typing 0. Dates can be typed like 3/1/2027 or 1 Mar 2027."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color=t.accent); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 12, 2)
label(s, "B14", "Works in Excel and Google Sheets. Example books are included to show the format: type over them or delete them.", italic=True, size=10)

# ---------- Settings ----------
st = wb.create_sheet("Settings")
banner(st, t, "Settings", "Your goals and the lists used by the drop-downs.", 6)
widths(st, {"A": 30, "B": 14, "C": 4, "D": 24, "E": 4, "F": 20, "G": 4, "H": 16})
label(st, "A4", "Books to read in 2027", bold=True); inp(st, "B4", 36, "0")
label(st, "A5", "Pages to read in 2027", bold=True); inp(st, "B5", 12000, "#,##0")
label(st, "A6", "Year", bold=True); inp(st, "B6", YEAR, "0", "Change to track another year.")
header(st, 8, ["Genres"], t, 4); header(st, 8, ["Formats"], t, 6); header(st, 8, ["Status"], t, 8)
for i in range(20):
    inp(st, f"D{9 + i}", GENRES[i] if i < len(GENRES) else None); st[f"D{9 + i}"].alignment = Alignment(horizontal="left", indent=1)
for i in range(10):
    inp(st, f"F{9 + i}", FORMATS[i] if i < len(FORMATS) else None); st[f"F{9 + i}"].alignment = Alignment(horizontal="left", indent=1)
for i, v in enumerate(STATUS):
    c = st.cell(9 + i, 8, v); c.font = Font(name=F, size=11); c.border = BOX
G_RNG, F_RNG = "Settings!$D$9:$D$28", "Settings!$F$9:$F$18"

# ---------- Book Log ----------
b = wb.create_sheet("Book Log")
banner(b, t, "Book Log", "One row per book. Yellow = you type, green = worked out.", 14)
cols = ["Title", "Author", "Genre", "Format", "Pages", "Started", "Finished", "Status", "Rating (1-5)", "Fave?", "Notes / favourite quote",
        "Days to read", "Pages / day", "Month", "Stars"]
header(b, 6, cols, t)
widths(b, {"A": 30, "B": 22, "C": 19, "D": 15, "E": 8, "F": 12, "G": 12, "H": 11, "I": 10, "J": 7, "K": 36, "L": 9, "M": 9, "N": 8, "O": 12, "P": 3})
b.freeze_panes = "B7"
label(b, "A4", "Status 'Finished' + a Finished date counts a book toward your goal. Rating: 1 to 5 (e.g. 4.5).", italic=True, size=10)
for r in range(7, NB + 1):
    for col in "ABCDEFGHIJK": inp(b, f"{col}{r}")
    for col in "ABK": b[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    b[f"F{r}"].number_format = b[f"G{r}"].number_format = "d mmm yy"; b[f"E{r}"].number_format = "#,##0"; b[f"I{r}"].number_format = "0.0"
    calc(b, f"L{r}", f'=IF(OR(F{r}="",G{r}=""),"",G{r}-F{r}+1)', "0")
    calc(b, f"M{r}", f'=IF(OR(L{r}="",E{r}="",L{r}<=0),"",E{r}/L{r})', "0")
    calc(b, f"N{r}", f'=IF(G{r}="","",TEXT(G{r},"mmm"))')
    calc(b, f"O{r}", f'=IF(I{r}="","",REPT("★",INT(I{r}))&REPT("☆",5-INT(I{r})))')
    b[f"O{r}"].font = Font(name=F, size=11, color="C98A1B")
    b[f"P{r}"] = (f'=IF(AND(H{r}="Finished",ISNUMBER(G{r}),ISNUMBER(I{r})),IF(YEAR(G{r})=Settings!$B$6,I{r}+({NB + 1}-ROW())/1000000,""),"")')
    b[f"P{r}"].font = Font(name=F, size=8, color="FFFFFF")
dv_list(b, f"C7:C{NB}", "=" + G_RNG); dv_list(b, f"D7:D{NB}", "=" + F_RNG); dv_list(b, f"H7:H{NB}", "=Settings!$H$9:$H$12"); dv_list(b, f"J7:J{NB}", "Yes")
dv = DataValidation(type="decimal", operator="between", formula1="1", formula2="5", allow_blank=True); dv.add(f"I7:I{NB}"); b.add_data_validation(dv)
EX = [("The Lantern House", "M. Ashby", "Mystery & Thriller", "Paperback", 352, (1, 2), (1, 9), "Finished", 4.5, "Yes", "Couldn't put it down after chapter 12."),
      ("Salt and Starlight", "R. Okafor", "Fantasy", "Audiobook", 480, (1, 10), (1, 24), "Finished", 5, "Yes", "New favourite series."),
      ("A Quiet Year in Kyoto", "H. Mori", "Memoir", "Library", 256, (1, 25), (2, 3), "Finished", 4, None, None),
      ("The Orchard Letters", "E. Byrne", "Historical Fiction", "Ebook", 410, (2, 4), (2, 20), "Finished", 3.5, None, "Slow start, lovely ending."),
      ("Tiny Habits, Big Year", "J. Lane", "Self-help", "Hardback", 288, (2, 21), None, "Reading", None, None, None)]
for i, row in enumerate(EX):
    r = 7 + i
    for j, v in enumerate(row):
        if v is None: continue
        if j in (5, 6): v = dt.date(YEAR, *v)
        b.cell(r, 1 + j).value = v
b.conditional_formatting.add(f"A7:K{NB}", FormulaRule(formula=[f'$H7="Finished"'], fill=PatternFill("solid", fgColor="EAF3EE")))
b.conditional_formatting.add(f"A7:K{NB}", FormulaRule(formula=[f'$H7="DNF"'], font=Font(name=F, color="9A8F8F", italic=True)))
BA, BC, BD, BE, BG, BH, BI, BJ, BP = (f"'Book Log'!${c}$7:${c}${NB}" for c in "ACDEGHIJP")
DONE = f'{BH},"Finished",{BG},">="&DATE(Settings!$B$6,1,1),{BG},"<"&DATE(Settings!$B$6+1,1,1)'

# ---------- Dashboard ----------
d = wb.create_sheet("Dashboard", 1)
banner(d, t, "2027 Reading Dashboard", "Everything updates as you log books.", 10)
widths(d, {"A": 24, "B": 13, "C": 13, "D": 4, "E": 22, "F": 11, "G": 11, "H": 4, "I": 30, "J": 10})
kp = [("Books finished", f"=COUNTIFS({DONE})", "0"), ("Reading goal", "=Settings!B4", "0"),
      ("Goal progress", '=IF(B5=0,"",B4/B5)', "0%"), ("Books to go", "=MAX(0,B5-B4)", "0"),
      ("Pages read", f"=SUMIFS({BE},{DONE})", "#,##0"), ("Page goal progress", '=IF(Settings!B5=0,"",B8/Settings!B5)', "0%"),
      ("Average rating", f'=IFERROR(AVERAGEIFS({BI},{DONE},{BI},">0"),"")', "0.0"),
      ("Currently reading", f'=COUNTIF({BH},"Reading")', "0"), ("Did not finish", f'=COUNTIF({BH},"DNF")', "0"),
      ("On track? (books)", '=IF(B5=0,"",IF(B4>=B5*MAX(0,MIN(1,(TODAY()-DATE(Settings!B6,1,1))/365)),"On track","Catch up time"))', None),
      ("Avg pages / book", '=IF(B4=0,"",B8/B4)', "0")]
for i, (a, f, fmt) in enumerate(kp):
    r = 4 + i; label(d, f"A{r}", a, bold=True); calc(d, f"B{r}", f, fmt, bold=True); d.row_dimensions[r].height = 22
d.merge_cells("B4:C4"); d["B4"].font = Font(name=F, size=16, bold=True, color="1F2A44")
d.conditional_formatting.add("B6", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="B8546A"))
d.conditional_formatting.add("B9", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="2B3A55"))
d.conditional_formatting.add("B13", FormulaRule(formula=['B13="On track"'], font=Font(name=F, bold=True, color="2E7D4F")))
d.conditional_formatting.add("B13", FormulaRule(formula=['B13="Catch up time"'], font=Font(name=F, bold=True, color="B8546A")))
header(d, 16, ["Month", "Books", "Pages"], t)
for i, mn in enumerate(MONTHS):
    r = 17 + i; label(d, f"A{r}", mn)
    rng = f'{BH},"Finished",{BG},">="&DATE(Settings!$B$6,{i + 1},1),{BG},"<"&DATE(Settings!$B$6,{i + 2},1)'
    calc(d, f"B{r}", f"=COUNTIFS({rng})", "0"); calc(d, f"C{r}", f"=SUMIFS({BE},{rng})", "#,##0")
label(d, "A29", "Total", bold=True); calc(d, "B29", "=SUM(B17:B28)", "0", bold=True); calc(d, "C29", "=SUM(C17:C28)", "#,##0", bold=True)
d.conditional_formatting.add("B17:B28", DataBarRule(start_type="num", start_value=0, end_type="max", color="E7A9B5"))
header(d, 3, ["Genre", "Books", "Avg ★"], t, 5)
for i in range(20):
    r = 4 + i; d[f"E{r}"] = f'=IF(Settings!D{9 + i}="","",Settings!D{9 + i})'; d[f"E{r}"].font = Font(name=F, size=11)
    calc(d, f"F{r}", f'=IF(E{r}="","",COUNTIFS({DONE},{BC},E{r}))', "0")
    calc(d, f"G{r}", f'=IF(OR(E{r}="",F{r}=0),"",IFERROR(AVERAGEIFS({BI},{DONE},{BC},E{r},{BI},">0"),""))', "0.0")
d.conditional_formatting.add("F4:F23", DataBarRule(start_type="num", start_value=0, end_type="max", color="9FB3D1"))
header(d, 25, ["Format", "Books"], t, 5)
for i in range(10):
    r = 26 + i; d[f"E{r}"] = f'=IF(Settings!F{9 + i}="","",Settings!F{9 + i})'; d[f"E{r}"].font = Font(name=F, size=11)
    calc(d, f"F{r}", f'=IF(E{r}="","",COUNTIFS({DONE},{BD},E{r}))', "0")
header(d, 3, ["Top rated this year", "Rating"], t, 9)
for k in range(10):
    r = 4 + k
    calc(d, f"J{r}", f'=IFERROR(LARGE({BP},{k + 1}),"")', "0.0")
    calc(d, f"I{r}", f'=IF(J{r}="","",INDEX({BA},MATCH(J{r},{BP},0)))')
    d[f"I{r}"].alignment = Alignment(horizontal="left", indent=1); d[f"J{r}"].number_format = "0.0"
label(d, "I15", "Favourites marked 'Yes'", bold=True); calc(d, "J15", f'=COUNTIFS({DONE},{BJ},"Yes")', "0")

# ---------- Reading Challenge ----------
PROMPTS = ["A book published in 2027", "A book you've owned for over a year", "A debut novel", "A book set in winter", "A book under 200 pages",
           "A book over 500 pages", "A book a friend recommended", "A book with a map inside", "A book by an author from another country",
           "A book translated from another language", "A book set by the sea", "A book from the library", "A book with a one-word title",
           "A memoir or biography", "A book you can finish in a weekend", "A classic you've never read", "A book with a colour in the title",
           "An audiobook", "A book set in a place you want to visit", "A book with a cosy vibe", "A book that makes you cry",
           "A mystery you solve before the end", "A book picked by its cover", "A book about food or cooking", "A book of poetry or short stories",
           "A book with a non-human narrator", "A book from your TBR's oldest pile", "A retelling of a myth or fairy tale", "A book set in the past",
           "A book set in the future", "A book you'd gift someone", "A book with a friendship at its heart", "A banned or challenged book",
           "A book by an author with the same initial as you", "A re-read of an old favourite", "The last book of a series"]
c = wb.create_sheet("Reading Challenge")
banner(c, t, "2027 Reading Challenge", "36 prompts. Type the title of the book you read; it ticks off when that book is Finished in your log.", 5)
widths(c, {"A": 6, "B": 48, "C": 34, "D": 12, "E": 10})
label(c, "B4", "Challenge progress", bold=True, size=12)
calc(c, "C4", '=COUNTIF(D7:D42,"✔ Done")&" of 36 done"', None, bold=True); calc(c, "D4", '=COUNTIF(D7:D42,"✔ Done")/36', "0%", bold=True)
c.conditional_formatting.add("D4", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="B8546A"))
header(c, 6, ["#", "Prompt", "Book title (type it)", "Status", "Rating"], t)
for i, p in enumerate(PROMPTS):
    r = 7 + i; n = c.cell(r, 1, i + 1); n.font = Font(name=F, size=11, bold=True, color=t.accent); n.alignment = Alignment(horizontal="center")
    inp(c, f"B{r}", p); c[f"B{r}"].alignment = Alignment(horizontal="left", indent=1)
    inp(c, f"C{r}"); c[f"C{r}"].alignment = Alignment(horizontal="left", indent=1)
    calc(c, f"D{r}", f'=IF(C{r}="","",IF(COUNTIFS({BA},C{r},{BH},"Finished")>0,"✔ Done",IF(COUNTIF({BA},C{r})>0,"Reading","Planned")))')
    calc(c, f"E{r}", f'=IF(C{r}="","",IFERROR(INDEX({BI},MATCH(C{r},{BA},0))&"",""))')
c["C8"] = "A Quiet Year in Kyoto"; c["C10"] = "The Lantern House"; c["C14"] = "Tiny Habits, Big Year"
c.conditional_formatting.add("D7:D42", CellIsRule(operator="equal", formula=['"✔ Done"'], fill=PatternFill("solid", fgColor="DDEFE3"), font=Font(name=F, bold=True, color="2E7D4F")))

# ---------- TBR ----------
tb = wb.create_sheet("TBR List")
banner(tb, t, "To Be Read", "Your TBR pile. Sort by priority when you need your next book.", 8)
header(tb, 5, ["Title", "Author", "Genre", "Priority", "Own it?", "Where I heard of it", "Added", "Moved to log?"], t)
widths(tb, {"A": 30, "B": 22, "C": 19, "D": 11, "E": 9, "F": 26, "G": 12, "H": 14}); tb.freeze_panes = "A6"
for r in range(6, NT + 1):
    for col in "ABCDEFG": inp(tb, f"{col}{r}")
    for col in "ABF": tb[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    tb[f"G{r}"].number_format = "d mmm yy"
    calc(tb, f"H{r}", f'=IF(A{r}="","",IF(COUNTIF({BA},A{r})>0,"In log ✔",""))')
dv_list(tb, f"C6:C{NT}", "=" + G_RNG); dv_list(tb, f"D6:D{NT}", "High,Medium,Low"); dv_list(tb, f"E6:E{NT}", "Yes,No,Wishlist")
for i, row in enumerate([("Salt and Starlight", "R. Okafor", "Fantasy", "High", "No", "Book club pick", dt.date(2026, 12, 28)),
                         ("The Winter Cartographer", "L. Varga", "Historical Fiction", "Medium", "Yes", "Gift from Mum", dt.date(2026, 12, 25))]):
    for j, v in enumerate(row): tb.cell(6 + i, 1 + j).value = v
tb.conditional_formatting.add(f"D6:D{NT}", CellIsRule(operator="equal", formula=['"High"'], font=Font(name=F, bold=True, color="B8546A")))

for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.save(sys.argv[1]); print("saved")
