"""Demo copy of the batch 5 reading tracker with a half-year of example books (listing screenshots only)."""
import shutil, sys, subprocess, glob, datetime as dt
from openpyxl import load_workbook
src, dst = sys.argv[1], sys.argv[2]
R = glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
f = f"{dst}/2027-reading-tracker-spreadsheet.xlsx"; shutil.copy(f"{src}/2027-reading-tracker-spreadsheet.xlsx", f)
wb = load_workbook(f); b = wb["Book Log"]
rows = [("Paper Moons", "T. Hale", "Romance", "Kindle Unlimited", 320, (2, 22), (2, 27), "Finished", 4),
        ("The Glasshouse Garden", "S. Pryce", "Contemporary", "Paperback", 298, (3, 1), (3, 8), "Finished", 4.5),
        ("Ninth Tide", "K. Adeyemi", "Fantasy", "Hardback", 544, (3, 9), (3, 30), "Finished", 5),
        ("Murder at Marrow Bay", "P. Quill", "Mystery & Thriller", "Ebook", 336, (4, 1), (4, 6), "Finished", 4),
        ("Small Wonders", "A. Iqbal", "Non-fiction", "Audiobook", 240, (4, 7), (4, 15), "Finished", 3.5),
        ("The Clockmaker's Daughter", "V. Lind", "Historical Fiction", "Library", 432, (4, 16), (5, 2), "Finished", 4.5),
        ("Static Bloom", "J. Moreau", "Science Fiction", "Paperback", 388, (5, 3), (5, 14), "Finished", 4),
        ("Hollow Pines", "C. Wren", "Horror", "Ebook", 276, (5, 15), (5, 19), "Finished", 3),
        ("Letters to the Lighthouse", "N. Shah", "Literary Fiction", "Hardback", 304, (5, 20), (6, 4), "Finished", 5),
        ("The Long Way North", "D. Kerr", "Memoir", "Audiobook", 352, (6, 5), (6, 16), "Finished", 4),
        ("Ember & Ash", "R. Okafor", "Fantasy", "Paperback", 512, (6, 17), None, "Reading", None),
        ("The Velvet Hour", "M. Ashby", "Mystery & Thriller", "Library", 290, (6, 1), (6, 10), "DNF", 2)]
for i, row in enumerate(rows):
    r = 12 + i
    for j, v in enumerate(row):
        if v is None: continue
        if j in (5, 6): v = dt.date(2027, *v)
        b.cell(r, 1 + j).value = v
b["J14"] = "Yes"; b["J20"] = "Yes"
c = wb["Reading Challenge"]
for r, v in ((11, "Ninth Tide"), (13, "The Long Way North"), (17, "Paper Moons"), (24, "Small Wonders"), (25, "Letters to the Lighthouse"), (31, "Hollow Pines"), (34, "The Clockmaker's Daughter")):
    c[f"C{r}"] = v
wb.save(f); subprocess.run(["python3", R, f, "90"], check=True, capture_output=True); print("demo ok")
