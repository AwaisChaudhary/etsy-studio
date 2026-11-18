import sys; sys.path.insert(0, ".")
from xl import *
from openpyxl.styles import Font, Alignment
t = Theme("2B4C7E", "4A73B0", "E4ECF7")
W = ["0 Lace", "1 Super Fine", "2 Fine", "3 Light (DK)", "4 Medium (Worsted)", "5 Bulky", "6 Super Bulky", "7 Jumbo"]
FIB = ["Wool", "Merino", "Acrylic", "Cotton", "Alpaca", "Mohair", "Silk", "Linen", "Blend", "Other"]
wb = Workbook(); N = 305
s = wb.active; s.title = "Start Here"
banner(s, t, "Yarn Stash Tracker", "Know exactly what yarn you have, where it is, and whether it's enough for your next project.", 6)
widths(s, {"A": 6, "B": 90})
steps = ["Add each yarn to My Stash: brand, colour, fibre, weight, yards per skein and how many skeins. Total yards and value are calculated.",
         "Note where it's stored and whether it's set aside for a project, so you can find it fast.",
         "The Summary tab shows your yards by weight and fibre, and what your stash is worth.",
         "Planning something? Enter it on Project Check to see if your stash has enough yarn of that weight.",
         "Keep a Shopping List so you don't buy duplicates."]
label(s, "B4", "How to use it", bold=True, size=14)
for i, txt in enumerate(steps):
    r = 5 + i; c = s.cell(r, 1, str(i + 1)); c.font = Font(name=F, size=14, bold=True, color="4A73B0"); c.alignment = Alignment(horizontal="center", vertical="top")
    label(s, f"B{r}", txt); s.row_dimensions[r].height = 34
legend(s, 11, 2)
label(s, "B13", "Works in Excel and Google Sheets. Three example yarns are included; type over them.", italic=True, size=10)
m = wb.create_sheet("My Stash")
banner(m, t, "My stash", "One row per yarn. Total yards and value are worked out for you.", 13)
cols = ["Brand", "Yarn", "Colour", "Fibre", "Weight", "Yards per skein", "Skeins", "Total yards", "Dye lot", "Price per skein", "Value", "Stored in", "Set aside for"]
header(m, 5, cols, t)
widths(m, {"A": 18, "B": 20, "C": 16, "D": 11, "E": 20, "F": 12, "G": 9, "H": 12, "I": 11, "J": 12, "K": 11, "L": 16, "M": 20}); m.freeze_panes = "C6"
for r in range(6, N + 1):
    for col in "ABCDEFGIJLM": inp(m, f"{col}{r}")
    for col in "ABCLM": m[f"{col}{r}"].alignment = Alignment(horizontal="left", indent=1)
    m[f"J{r}"].number_format = '"$"#,##0.00'
    calc(m, f"H{r}", f'=IF(OR(F{r}="",G{r}=""),"",F{r}*G{r})', "#,##0")
    calc(m, f"K{r}", f'=IF(OR(J{r}="",G{r}=""),"",J{r}*G{r})', '"$"#,##0.00')
ex = [("Hearthside", "Classic Worsted", "Oatmeal", "Acrylic", W[4], 364, 4, None, "A118", 7.49, None, "Bin 1", "Throw blanket"),
      ("Meadow Fibre Co.", "Merino DK", "Sage", "Merino", W[3], 246, 6, None, "M22", 12.0, None, "Bin 2", ""),
      ("Summer Cotton", "Cotton 8", "Coral", "Cotton", W[3], 180, 3, None, "", 4.5, None, "Drawer", "")]
for i, row in enumerate(ex):
    for j, v in enumerate(row):
        if v is not None and v != "": m.cell(6 + i, 1 + j).value = v
dv_list(m, f"E6:E{N}", ",".join(W)); dv_list(m, f"D6:D{N}", ",".join(FIB))
su = wb.create_sheet("Summary")
banner(su, t, "Summary", "Your stash at a glance.", 5)
widths(su, {"A": 30, "B": 16, "C": 16, "D": 4, "E": 20, "F": 14})
for i, (a, f, fmt) in enumerate([("Different yarns", f'=COUNTA(\'My Stash\'!B6:B{N})', "0"), ("Skeins", f"=SUM('My Stash'!G6:G{N})", "#,##0"),
                                 ("Total yards", f"=SUM('My Stash'!H6:H{N})", "#,##0"), ("Total metres", "=B6*0.9144", "#,##0"), ("Stash value", f"=SUM('My Stash'!K6:K{N})", '"$"#,##0')]):
    label(su, f"A{4 + i}", a, bold=True, size=12); calc(su, f"B{4 + i}", f, fmt, big=True); su.row_dimensions[4 + i].height = 28
header(su, 11, ["Weight", "Skeins", "Yards"], t)
for i, wn in enumerate(W):
    r = 12 + i; label(su, f"A{r}", wn)
    calc(su, f"B{r}", f"=SUMIFS('My Stash'!$G$6:$G${N},'My Stash'!$E$6:$E${N},A{r})", "#,##0")
    calc(su, f"C{r}", f"=SUMIFS('My Stash'!$H$6:$H${N},'My Stash'!$E$6:$E${N},A{r})", "#,##0")
header(su, 11, ["Fibre", "Yards"], t, start=5)
for i, fb in enumerate(FIB):
    r = 12 + i; label(su, f"E{r}", fb); calc(su, f"F{r}", f"=SUMIFS('My Stash'!$H$6:$H${N},'My Stash'!$D$6:$D${N},E{r})", "#,##0")
pc = wb.create_sheet("Project Check")
banner(pc, t, "Project check", "Is there enough in your stash? Enter the project's yarn weight and yards needed.", 6)
header(pc, 5, ["Project", "Weight needed", "Yards needed", "Yards in stash (that weight)", "Enough?"], t)
widths(pc, {"A": 26, "B": 22, "C": 14, "D": 26, "E": 18})
for r in range(6, 31):
    for col in "ABC": inp(pc, f"{col}{r}")
    pc[f"A{r}"].alignment = Alignment(horizontal="left", indent=1)
    calc(pc, f"D{r}", f"=IF(B{r}=\"\",\"\",SUMIFS('My Stash'!$H$6:$H${N},'My Stash'!$E$6:$E${N},B{r}))", "#,##0")
    calc(pc, f"E{r}", f'=IF(OR(B{r}="",C{r}=""),"",IF(D{r}>=C{r},"Yes","Short by "&TEXT(C{r}-D{r},"#,##0")&" yd"))')
dv_list(pc, "B6:B30", ",".join(W))
pc["A6"] = "Sunday cardigan"; pc["B6"] = W[3]; pc["C6"] = 1300
sh = wb.create_sheet("Shopping List")
banner(sh, t, "Shopping list", "Yarn to buy, so you never buy what you already own.", 6)
header(sh, 5, ["Yarn", "Weight", "Yards or skeins", "For project", "Where to buy", "Bought?"], t)
widths(sh, {"A": 26, "B": 20, "C": 16, "D": 22, "E": 22, "F": 10})
for r in range(6, 56):
    for col in "ABCDEF": inp(sh, f"{col}{r}")
dv_list(sh, "B6:B55", ",".join(W)); dv_list(sh, "F6:F55", "Yes,No")
for ws in wb.worksheets: ws.sheet_properties.tabColor = t.main
wb.save(sys.argv[1]); print("saved")
