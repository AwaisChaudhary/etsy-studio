"""Shared styling helpers for the Etsy spreadsheet products."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.comments import Comment

F = "Arial"
INPUT = PatternFill("solid", fgColor="FFF6D6")      # cells buyers fill in
CALC = PatternFill("solid", fgColor="EEF4F2")       # formula results
thin = Side(style="thin", color="D5DCE3")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

class Theme:
    def __init__(self, main, accent, light):
        self.main, self.accent, self.light = main, accent, light
        self.head = PatternFill("solid", fgColor=main)
        self.band = PatternFill("solid", fgColor=light)
        self.acc = PatternFill("solid", fgColor=accent)

def banner(ws, t, title, sub, width=8):
    ws.sheet_view.showGridLines = False
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=width)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=width)
    c = ws.cell(1, 1, title); c.font = Font(name=F, size=20, bold=True, color="FFFFFF"); c.fill = t.head
    c.alignment = Alignment(vertical="center", indent=1)
    for col in range(1, width + 1):
        ws.cell(1, col).fill = t.head; ws.cell(2, col).fill = t.head
    s = ws.cell(2, 1, sub); s.font = Font(name=F, size=11, color="FFFFFF", italic=True); s.alignment = Alignment(vertical="top", indent=1)
    ws.row_dimensions[1].height = 40; ws.row_dimensions[2].height = 24

def header(ws, row, cols, t, start=1):
    for i, name in enumerate(cols):
        c = ws.cell(row, start + i, name)
        c.font = Font(name=F, size=11, bold=True, color="FFFFFF"); c.fill = t.acc
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = BOX
    ws.row_dimensions[row].height = 32

def label(ws, ref, text, bold=False, size=11, color="1F2A44", italic=False):
    c = ws[ref]; c.value = text; c.font = Font(name=F, size=size, bold=bold, color=color, italic=italic)
    c.alignment = Alignment(vertical="center", wrap_text=True); return c

def inp(ws, ref, value=None, fmt=None, note=None):
    c = ws[ref]
    if value is not None: c.value = value
    c.fill = INPUT; c.border = BOX; c.font = Font(name=F, size=11, color="0000FF")
    c.alignment = Alignment(horizontal="center", vertical="center")
    if fmt: c.number_format = fmt
    if note: c.comment = Comment(note, "Guide")
    return c

def calc(ws, ref, formula, fmt=None, bold=False, big=False):
    c = ws[ref]; c.value = formula; c.fill = CALC; c.border = BOX
    c.font = Font(name=F, size=16 if big else 11, bold=bold or big, color="1F2A44")
    c.alignment = Alignment(horizontal="center", vertical="center")
    if fmt: c.number_format = fmt
    return c

def widths(ws, d):
    for k, v in d.items(): ws.column_dimensions[k].width = v

def body_font(ws, r1, r2, c1, c2):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            cell = ws.cell(r, c)
            if cell.font is None or cell.font.name != F: cell.font = Font(name=F, size=11)

def legend(ws, row, col=1):
    a = ws.cell(row, col, "Yellow"); a.fill = INPUT; a.border = BOX; a.font = Font(name=F, size=10, color="0000FF"); a.alignment = Alignment(horizontal="center")
    ws.cell(row, col + 1, "type here").font = Font(name=F, size=10)
    b = ws.cell(row, col + 2, "Green"); b.fill = CALC; b.border = BOX; b.font = Font(name=F, size=10); b.alignment = Alignment(horizontal="center")
    ws.cell(row, col + 3, "calculated for you").font = Font(name=F, size=10)

def dv_list(ws, rng, options_or_ref):
    f = options_or_ref if options_or_ref.startswith("=") else '"' + options_or_ref + '"'
    dv = DataValidation(type="list", formula1=f, allow_blank=True); dv.add(rng); ws.add_data_validation(dv); return dv
