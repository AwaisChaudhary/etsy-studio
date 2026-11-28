"""Spreadsheet window rendered as HTML (shared by mockups and scenes)."""
import datetime, html, pathlib
from openpyxl import load_workbook
from openpyxl.utils import range_boundaries, get_column_letter
e = html.escape

# ---------- spreadsheet screenshot as HTML ----------
def fmt(v, nf):
    if v is None: return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        if "dddd" in nf: return v.strftime("%A %d %b %Y")
        if "ddd" in nf: return v.strftime("%a %d %b")
        return v.strftime("%d %b %Y")
    if isinstance(v, datetime.time): return v.strftime("%I:%M %p").lstrip("0")
    if isinstance(v, datetime.timedelta):
        t = round(v.total_seconds()); return f"{t // 60}:{t % 60:02d}"
    if isinstance(v, (int, float)):
        if "%" in nf: return f"{v * 100:.0f}%" if "0%" == nf else f"{v * 100:.1f}%"
        if "$" in nf:
            dec = 4 if ".0000" in nf else 2 if ".00" in nf else 0
            return ("-$" if v < 0 else "$") + f"{abs(v):,.{dec}f}"
        if nf.endswith("x"): return f"{v:.1f}x"
        if "0.00" in nf: return f"{v:,.2f}"
        if "0.0" in nf: return f"{v:,.1f}"
        if nf == "0": return f"{v:.0f}"
        if nf == "#,##0": return f"{v:,.0f}"
        if isinstance(v, float) and not v.is_integer(): return f"{v:,.2f}"
        return f"{v:,.0f}"
    return str(v)


# ---------- light conditional-formatting emulation (cellIs equal/less/greater, colour scales, data bars, tick formulas) ----------
def _rgb(c):
    try:
        v = c.rgb
        if isinstance(v, str) and v not in ("00000000",): return v[-6:]
    except Exception: pass
    return None

def _dxf_css(rule):
    st = []
    d = rule.dxf
    if d is not None:
        if d.fill is not None:
            col = _rgb(d.fill.bgColor) or _rgb(d.fill.fgColor)
            if col: st.append(f"background:#{col}")
        if d.font is not None:
            if d.font.b: st.append("font-weight:700")
            if d.font.color is not None and _rgb(d.font.color): st.append(f"color:#{_rgb(d.font.color)}")
    return st

def _mix(a, b, t):
    a = [int(a[i:i + 2], 16) for i in (0, 2, 4)]; b = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))

def _num(v):
    try: return float(v)
    except Exception: return None

def cf_rules(ws):
    out = []
    for cf in ws.conditional_formatting:
        cells = set()
        for cr in cf.sqref.ranges:
            out_rng = (cr.min_col, cr.min_row, cr.max_col, cr.max_row)
            cells.add(out_rng)
        for rule in sorted(cf.rules, key=lambda r: r.priority or 0):
            out.append((cells, rule))
    return out

def cf_css(rules, r, c, val):
    """Returns (css list, stop) for the first matching rule(s)."""
    css = []
    for cells, rule in rules:
        if not any(a <= c <= cc and b <= r <= d for a, b, cc, d in cells): continue
        t = rule.type
        if t == "cellIs" and rule.formula:
            f = rule.formula[0]; op = rule.operator
            if f.startswith('"'):
                if op == "equal" and val == f.strip('"'): return css + _dxf_css(rule)
            else:
                n, x = _num(val), _num(f)
                if n is not None and x is not None and isinstance(val, (int, float)):
                    if (op == "lessThan" and n < x) or (op == "greaterThan" and n > x): css += _dxf_css(rule)
        elif t == "expression" and rule.formula:
            f = rule.formula[0]
            if '="\u2713"' in f or '="✓"' in f:
                if val in ("✓", "x", "X"): return css + _dxf_css(rule)
            elif '="\u2717"' in f or '="✗"' in f:
                if val == "✗": return css + _dxf_css(rule)
        elif t == "colorScale" and isinstance(val, (int, float)) and not isinstance(val, bool):
            cs = rule.colorScale; vals = [_num(v.val) for v in cs.cfvo]; cols = [_rgb(c_) for c_ in cs.color]
            if None in vals or None in cols: continue
            if len(vals) == 2: vals = [vals[0], (vals[0] + vals[1]) / 2, vals[1]]; cols = [cols[0], _mix(cols[0], cols[1], .5), cols[1]]
            v = min(max(val, vals[0]), vals[2])
            col = _mix(cols[0], cols[1], (v - vals[0]) / ((vals[1] - vals[0]) or 1)) if v <= vals[1] else _mix(cols[1], cols[2], (v - vals[1]) / ((vals[2] - vals[1]) or 1))
            css.append(f"background:#{col}")
        elif t == "dataBar" and isinstance(val, (int, float)) and not isinstance(val, bool):
            db = rule.dataBar; lo, hi = _num(db.cfvo[0].val) or 0, _num(db.cfvo[1].val) or 1
            pct = max(0, min(1, (val - lo) / ((hi - lo) or 1))) * 100; col = _rgb(db.color) or "9CC5A8"
            css.append(f"background:linear-gradient(90deg,#{col} {pct:.0f}%,transparent {pct:.0f}%)")
    return css

def xl_html(path, sheet, rng, tabs, active):
    wf = load_workbook(path); wv = load_workbook(path, data_only=True)
    ws, vs = wf[sheet], wv[sheet]
    hide = set()
    if ";" in rng:  # "A1:AD12;B-X,Z" hides columns B..X and Z (for wide sheets)
        rng, spec = rng.split(";")
        from openpyxl.utils import column_index_from_string as ci
        for part in spec.split(","):
            a, _, b = part.partition("-"); hide.update(range(ci(a), ci(b or a) + 1))
    c1, r1, c2, r2 = range_boundaries(rng)
    rules = cf_rules(ws)
    merged = {}
    skip = set()
    for m in ws.merged_cells.ranges:
        a, b, c, d = m.min_col, m.min_row, m.max_col, m.max_row
        if b >= r1 and b <= r2:
            merged[(b, a)] = (min(d, r2) - b + 1, sum(1 for k in range(a, min(c, c2) + 1) if k not in hide) or 1)
            for rr in range(b, d + 1):
                for cc in range(a, c + 1):
                    if (rr, cc) != (b, a): skip.add((rr, cc))
    cols = "".join(f'<th style="width:{int((ws.column_dimensions[get_column_letter(c)].width or 9) * 7.2)}px">{get_column_letter(c)}</th>' for c in range(c1, c2 + 1) if c not in hide)
    rows = ""
    for r in range(r1, r2 + 1):
        h = ws.row_dimensions[r].height or 18
        tds = ""
        for c in range(c1, c2 + 1):
            if (r, c) in skip or (c in hide and (r, c) not in merged): continue
            cell, val = ws.cell(r, c), vs.cell(r, c).value
            st = []
            if cell.fill and cell.fill.fgColor and cell.fill.fill_type == "solid" and cell.fill.fgColor.rgb not in (None, "00000000"):
                st.append(f"background:#{str(cell.fill.fgColor.rgb)[-6:]}")
            f = cell.font
            if f:
                if f.b: st.append("font-weight:700")
                if f.i: st.append("font-style:italic")
                if f.sz: st.append(f"font-size:{float(f.sz) * 1.35:.0f}px")
                if f.color is not None and f.color.rgb and isinstance(f.color.rgb, str): st.append(f"color:#{f.color.rgb[-6:]}")
            al = cell.alignment
            if al and al.horizontal == "center": st.append("text-align:center")
            if al and al.wrap_text: st.append("white-space:normal")
            if cell.border and cell.border.left and cell.border.left.style: st.append("box-shadow:inset 0 0 0 1px #d5dce3")
            st += cf_css(rules, r, c, val)
            span = ""
            if (r, c) in merged: rs, cs = merged[(r, c)]; span = f' rowspan="{rs}" colspan="{cs}"'
            tds += f'<td{span} style="{";".join(st)}">{e(fmt(val, cell.number_format or ""))}</td>'
        rows += f'<tr style="height:{h * 1.35:.0f}px"><th class="rn">{r}</th>{tds}</tr>'
    tabbar = "".join(f'<span class="{"on" if t == active else ""}">{e(t)}</span>' for t in tabs)
    return (f'<div class="win"><div class="bar"><i></i><i></i><i></i><b>{e(pathlib.Path(path).name)}</b></div>'
            f'<div class="sheet"><table><tr><th class="rn"></th>{cols}</tr>{rows}</table></div><div class="tabs">{tabbar}</div></div>')


XL_CSS = """
.win { background: #fff; border-radius: 18px; box-shadow: 0 40px 90px -30px rgba(0,0,0,.55); overflow: hidden; display: inline-block; }
.bar { height: 46px; background: #eef1f4; display: flex; align-items: center; gap: 10px; padding: 0 18px; }
.bar i { width: 14px; height: 14px; border-radius: 50%; background: #e05d5d; } .bar i:nth-child(2) { background: #e9b949; } .bar i:nth-child(3) { background: #5cc06a; }
.bar b { margin-left: 18px; font-size: 18px; font-weight: 500; color: #5b6478; }
.sheet table { border-collapse: collapse; font-family: Arial, sans-serif; font-size: 17px; table-layout: fixed; }
.sheet td { padding: 2px 8px; white-space: nowrap; overflow: hidden; border-right: 1px solid #edf0f2; border-bottom: 1px solid #edf0f2; vertical-align: middle; }
.sheet th { background: #f3f5f7; color: #7a8394; font-weight: 500; font-size: 13px; border: 1px solid #e2e6ea; height: 26px; }
.sheet th.rn { width: 40px; }
.tabs { display: flex; gap: 2px; contain: inline-size; overflow: hidden; white-space: nowrap; background: #f3f5f7; padding: 8px 12px 0; border-top: 1px solid #e2e6ea; }
.tabs span { font-family: Arial; font-size: 15px; padding: 8px 16px; color: #5b6478; }
.tabs span.on { background: #fff; color: var(--xl); font-weight: 700; border-bottom: 3px solid var(--xl); }
"""
