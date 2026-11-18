"""Demo copies of the spreadsheets with more example rows, used only for listing screenshots."""
import shutil, sys, subprocess, glob, datetime as dt
from openpyxl import load_workbook
src, dst = sys.argv[1], sys.argv[2]
R = glob.glob("/root/.claude/skills/synced/*/xlsx/scripts/recalc.py")[0]
today = dt.date(2026, 11, 19)
def fill(ws, row, vals):
    for j, v in enumerate(vals):
        if v is not None: ws.cell(row, j + 1).value = v
f = f"{dst}/cleaning-business-quote-client-tracker.xlsx"; shutil.copy(f"{src}/cleaning-business-quote-client-tracker.xlsx", f)
wb = load_workbook(f); c = wb["Clients"]
for i, row in enumerate([("Maria Gomez", "555-0187", "48 Oak Avenue", "Weekly", 110, "Mon", today - dt.timedelta(days=3), None, None, "Active", "Pet hair: extra vacuum"),
                         ("The Patels", "555-0133", "7 Birch Lane", "Every 2 weeks", 165, "Wed", today - dt.timedelta(days=8), None, None, "Active", "Deep clean kitchen monthly"),
                         ("Sam Carter", "555-0110", "201 River Road, Apt 4", "Monthly", 120, "Fri", today - dt.timedelta(days=20), None, None, "Active", ""),
                         ("Olivia Brown", "555-0164", "15 Maple Court", "Weekly", 95, "Thu", today - dt.timedelta(days=1), None, None, "Active", "Code 2468"),
                         ("Ben & Jo Hughes", "555-0179", "3 Station Road", "Every 2 weeks", 145, "Tue", today - dt.timedelta(days=12), None, None, "Paused", "Away until Jan"),
                         ("Lena Fischer", "555-0121", "92 Hill Street", "One-time", 280, "Sat", today - dt.timedelta(days=30), None, None, "Ended", "Move-out clean")]):
    fill(c, 7 + i, row)
w = wb["This Week"]
for i, row in enumerate([("Mon", None, 0.375, "Maria Gomez", None, None, "Yes", "Yes"), ("Wed", None, 0.4167, "The Patels", None, None, "No", "No"), ("Thu", None, 0.375, "Olivia Brown", None, None, "No", "No"), ("Fri", None, 0.5, "Sam Carter", None, None, "No", "No")]):
    fill(w, 8 + i, row)
wb.save(f)
f = f"{dst}/crochet-knitting-pricing-calculator.xlsx"; shutil.copy(f"{src}/crochet-knitting-pricing-calculator.xlsx", f)
wb = load_workbook(f); it = wb["My Items"]
for i, row in enumerate([("Chunky beanie", 2, 6.5, 44.99, None, None, 5, "Sells well in winter"), ("Baby blanket", 12, 21, 229.99, None, None, 1, "Custom order"), ("Market tote", 4, 7.2, 79.99, None, None, 3, ""), ("Coaster set", 1, 1.8, 22.99, None, None, 8, "Great add-on")]):
    fill(it, 7 + i, row)
wb.save(f)
f = f"{dst}/home-baker-cost-pricing-calculator.xlsx"; shutil.copy(f"{src}/home-baker-cost-pricing-calculator.xlsx", f)
wb = load_workbook(f); o = wb["Orders"]
for i, row in enumerate([(today - dt.timedelta(days=1), "Tom R.", "Chocolate cake", 1, 45, None, 15, None, today + dt.timedelta(days=3), "Baking", "Happy 40th"),
                         (today - dt.timedelta(days=4), "Ana M.", "Cookie box", 2, 18, None, 36, None, today, "Ready", ""),
                         (today - dt.timedelta(days=6), "Westside Cafe", "Scones", 30, 2.5, None, 75, None, today - dt.timedelta(days=1), "Delivered", "Weekly order")]):
    fill(o, 7 + i, row)
wb.save(f)
f = f"{dst}/yarn-stash-tracker.xlsx"; shutil.copy(f"{src}/yarn-stash-tracker.xlsx", f)
wb = load_workbook(f); m = wb["My Stash"]
for i, row in enumerate([("Highland Mill", "Aran Tweed", "Heather", "Wool", "4 Medium (Worsted)", 180, 5, None, "T7", 8.5, None, "Bin 1", "Winter sweater"),
                         ("Cloudsoft", "Alpaca Lace", "Mist", "Alpaca", "0 Lace", 437, 2, None, "", 14, None, "Drawer", "Shawl"),
                         ("Hearthside", "Big Chunky", "Rust", "Acrylic", "6 Super Bulky", 87, 6, None, "B3", 6.99, None, "Bin 3", ""),
                         ("Sock Club", "Speckle Sock", "Confetti", "Blend", "1 Super Fine", 463, 2, None, "S09", 22, None, "Bin 2", "Socks")]):
    fill(m, 9 + i, row)
wb.save(f)
for f in glob.glob(f"{dst}/*.xlsx"): subprocess.run(["python3", R, f], capture_output=True)
print("demo ready")
