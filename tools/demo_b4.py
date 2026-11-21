"""Demo copy of the batch 4 candle spreadsheet with more example rows (listing screenshots only)."""
import shutil, sys, subprocess, glob, datetime as dt
from openpyxl import load_workbook
src, dst = sys.argv[1], sys.argv[2]
R = glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
f = f"{dst}/candle-business-spreadsheet.xlsx"; shutil.copy(f"{src}/candle-business-spreadsheet.xlsx", f)
wb = load_workbook(f); s = wb["Sales"]; today = dt.date(2026, 11, 20)
rows = [(-40, "Market", "Vanilla Bean 16 oz", 3, 50, 0), (-33, "Etsy", "Fresh Linen travel tin", 4, 20, 9.4), (-27, "Wholesale", "Fireside Cedar 8 oz", 24, 15, 0),
        (-20, "Etsy", "Sugared Orange gift box", 2, 41, 8.7), (-14, "Website", "Vanilla Bean 16 oz", 1, 50, 2.1), (-9, "Market", "Fireside Cedar 8 oz", 6, 30, 0),
        (-6, "Etsy", "Sugared Orange gift box", 3, 41, 12.6), (-2, "Instagram", "Fresh Linen travel tin", 5, 20, 0)]
for i, (d, ch, c, q, p, fee) in enumerate(rows):
    r = 7 + i
    for col, v in zip("ABCDEG", (today + dt.timedelta(days=d), ch, c, q, p, fee)): s[f"{col}{r}"] = v
wb.save(f); subprocess.run(["python3", R, f, "90"], check=True, capture_output=True); print("demo ok")
