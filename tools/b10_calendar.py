"""2027 Printable Calendar (batch 10, lane b/d): cover, year at a glance and 12 monthly pages, each with an original seasonal
pattern panel drawn here as SVG (snowflakes, snowdrops, tulips, rain, blossom, strawberries, lemons, sunflowers, apples, pumpkins,
acorns & mushrooms, holly). Sunday-start and Monday-start, US Letter and A4 (4 PDFs). No holidays printed, so it works anywhere."""
import calendar, math, random, sys
sys.path.insert(0, ".")
from render import render
from kits import leaf
from kits2 import snowflake, holly, pine

YEAR = 2027
INK = "#2d2a32"
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Lora, serif; color: #2d2a32; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #fbf8f3; contain: strict; }
.sans { font-family: Poppins, "Liberation Sans", sans-serif; }
.script { font-family: "TeX Gyre Chorus", Lora, serif; }
svg { display: block; }
"""

# ---------- motifs (each drawn around 0,0 at roughly 100 units tall) ----------
def m_flake(c, r): return snowflake(0, 0, 40, c[1])
def m_snowdrop(c, r):
    return (f'<path d="M0 50 Q4 0 -10 -30" stroke="{c[2]}" stroke-width="4" fill="none"/>{leaf(0, 50, 60, -100, c[2])}'
            f'<path d="M-10 -30 q-14 10 -12 34 q8 6 12 -4 q4 10 12 4 q2 -24 -12 -34z" fill="{c[1]}"/>')
def m_tulip(c, r):
    col = r.choice([c[1], c[3]])
    return (f'<path d="M0 55 L0 -5" stroke="{c[2]}" stroke-width="5"/>{leaf(0, 55, 50, -120, c[2])}{leaf(0, 50, 46, -60, c[2])}'
            f'<path d="M-22 -40 L-12 -24 L0 -42 L12 -24 L22 -40 Q26 -4 0 -2 Q-26 -4 -22 -40z" fill="{col}"/>')
def m_rain(c, r):
    if r.random() < .35:
        return f'<g fill="{c[1]}"><circle cx="-18" cy="0" r="18"/><circle cx="6" cy="-10" r="24"/><circle cx="28" cy="2" r="16"/><rect x="-18" y="0" width="46" height="18"/></g>'
    return f'<path d="M0 -26 Q16 0 14 10 A14 14 0 0 1 -14 10 Q-16 0 0 -26z" fill="{r.choice([c[2], c[3]])}"/>'
def m_blossom(c, r):
    col = r.choice([c[1], c[3]])
    return "".join(f'<circle cx="{18 * math.cos(math.radians(a)):.1f}" cy="{18 * math.sin(math.radians(a)):.1f}" r="15" fill="{col}"/>' for a in range(-90, 270, 72)) + f'<circle r="8" fill="{c[2]}"/>'
def m_straw(c, r):
    seeds = "".join(f'<ellipse cx="{x}" cy="{y}" rx="1.8" ry="3" fill="#f6e3a1"/>' for x, y in [(-10, -2), (6, -6), (-2, 10), (12, 8), (-14, 14), (2, 24)])
    return (f'<path d="M0 36 C-30 20 -34 -14 -14 -18 Q0 -20 14 -18 C34 -14 30 20 0 36z" fill="{c[1]}"/>{seeds}'
            f'{leaf(0, -18, 22, -150, c[2])}{leaf(0, -18, 22, -30, c[2])}{leaf(0, -18, 18, -90, c[2])}')
def m_lemon(c, r):
    return (f'<g transform="rotate({r.uniform(-30, 30):.0f})"><ellipse cx="0" cy="0" rx="34" ry="24" fill="{c[1]}"/><ellipse cx="-36" cy="0" rx="6" ry="5" fill="{c[1]}"/>'
            f'<ellipse cx="36" cy="0" rx="6" ry="5" fill="{c[1]}"/><ellipse cx="-10" cy="-8" rx="10" ry="4" fill="#fff" opacity=".45"/>{leaf(30, -12, 34, -50, c[2])}</g>')
def m_sunflower(c, r):
    pet = "".join(leaf(0, 0, 40, a, c[1], "rgba(0,0,0,.08)") for a in range(0, 360, 24))
    return f'{pet}<circle r="17" fill="{c[2]}"/>' + "".join(f'<circle cx="{8 * math.cos(a):.1f}" cy="{8 * math.sin(a):.1f}" r="2" fill="#2b1d12"/>' for a in [k * 1.3 for k in range(8)])
def m_apple(c, r):
    col = r.choice([c[1], c[3]])
    return (f'<path d="M0 -20 C-22 -34 -42 -16 -36 8 C-30 34 -10 38 0 30 C10 38 30 34 36 8 C42 -16 22 -34 0 -20z" fill="{col}"/>'
            f'<path d="M0 -20 Q2 -34 8 -40" stroke="#5a3b26" stroke-width="4" fill="none"/>{leaf(4, -32, 26, -20, c[2])}<ellipse cx="-16" cy="-8" rx="6" ry="10" fill="#fff" opacity=".35"/>')
def m_pumpkin(c, r):
    col = r.choice([c[1], c[3]])
    return (f'<ellipse cx="-16" cy="4" rx="22" ry="28" fill="{col}"/><ellipse cx="16" cy="4" rx="22" ry="28" fill="{col}"/><ellipse cx="0" cy="4" rx="18" ry="30" fill="{col}" '
            f'stroke="#00000022" stroke-width="2"/><path d="M0 -24 q2 -12 8 -16" stroke="{c[2]}" stroke-width="6" fill="none" stroke-linecap="round"/>')
def m_acorn(c, r):
    if r.random() < .5:
        return (f'<path d="M-30 0 Q0 -40 30 0z" fill="{c[3]}"/><rect x="-8" y="0" width="16" height="30" rx="6" fill="#efe3cf"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" opacity=".8"/>' for x, y in [(-12, -10), (6, -16), (16, -6)]))
    return (f'<ellipse cx="0" cy="10" rx="16" ry="20" fill="{c[1]}"/><path d="M-20 -2 Q0 -26 20 -2 Q0 4 -20 -2z" fill="{c[2]}"/>'
            f'<path d="M0 -14 l0 -10" stroke="{c[2]}" stroke-width="4"/>')
def m_holly(c, r): return holly(-10, 0, 1.3, c[2], c[1]) if r.random() < .6 else pine(0, 45, 90, c[3], r.randint(1, 99))

MONTHS = [("January", m_flake, ("#2f4a6b", "#e8eef5", "#c9d6e3", "#9fb6cc")), ("February", m_snowdrop, ("#46604f", "#ffffff", "#8fae8b", "#dbe7d6")),
          ("March", m_tulip, ("#f2e6d0", "#d9774f", "#6c8f5b", "#e8b33f")), ("April", m_rain, ("#dfe8ee", "#ffffff", "#7aa1c0", "#a9c3d8")),
          ("May", m_blossom, ("#f6e1e3", "#ffffff", "#e8b33f", "#e9a3b0")), ("June", m_straw, ("#eaf0e2", "#d24b4b", "#5f8f4e", "#d24b4b")),
          ("July", m_lemon, ("#2f6b73", "#f2cf4a", "#7fb08a", "#f2cf4a")), ("August", m_sunflower, ("#f3e3c0", "#e8a92b", "#6a4a2a", "#e8a92b")),
          ("September", m_apple, ("#efe7da", "#c2463b", "#6f8f4e", "#d99a3b")), ("October", m_pumpkin, ("#3a3530", "#e07b39", "#7a8f4e", "#e8b05a")),
          ("November", m_acorn, ("#e8ddcc", "#a5713f", "#6b4a2b", "#b54a3a")), ("December", m_holly, ("#1f4a3c", "#c9423d", "#2f6b52", "#e4efe8"))]

def panel(i, w=1000, h=620, step=150, seed=0):
    name, fn, c = MONTHS[i]; r = random.Random(100 + i + seed); out = [f'<rect width="{w}" height="{h}" fill="{c[0]}"/>']
    for row in range(-1, h // step + 2):
        for col in range(-1, w // step + 2):
            x = col * step + (step / 2 if row % 2 else 0) + r.uniform(-18, 18); y = row * step * .9 + r.uniform(-14, 14)
            s = r.uniform(.75, 1.05)
            out.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f}) rotate({r.uniform(-18, 18):.0f})">{fn(c, r)}</g>')
    return f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%">{"".join(out)}</svg>'

def heads(monday): return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] if monday else ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def weeks(m, monday):
    cal = calendar.Calendar(0 if monday else 6)
    return cal.monthdayscalendar(YEAR, m)

def month_page(i, monday):
    name, fn, c = MONTHS[i]
    accent = ["#2f4a6b", "#46604f", "#c8643f", "#4f7a9c", "#c45a72", "#c94040", "#2f6b73", "#a8741c", "#c2463b", "#c8642a", "#8a5a30", "#b83a35"][i]
    wk = weeks(i + 1, monday); n = len(wk)
    hd = "".join(f'<div class="sans" style="text-align:center;font-size:8.5pt;letter-spacing:.18em;text-transform:uppercase;padding:5pt 0;color:{accent};font-weight:600">{d}</div>' for d in heads(monday))
    weekend = {5, 6} if monday else {0, 6}
    cells = ""
    for w in wk:
        for k, d in enumerate(w):
            bg = "#f3eee6" if k in weekend else "#ffffff"
            num = f'<div class="sans" style="font-size:11pt;font-weight:600;padding:4pt 6pt;color:{INK if d else "transparent"}">{d or ""}</div>'
            cells += f'<div style="background:{bg if d else "transparent"};border-radius:4px">{num}</div>'
    grid = (f'<div style="position:absolute;left:0.55in;right:0.55in;top:5.15in;bottom:0.95in;display:grid;grid-template-columns:repeat(7,1fr);'
            f'grid-template-rows:auto repeat({n},1fr);gap:3px">{hd}{cells}</div>')
    title = (f'<div style="position:absolute;left:0.55in;right:0.55in;top:4.15in;display:flex;align-items:baseline;justify-content:space-between">'
             f'<div style="font-size:40pt;font-weight:600;letter-spacing:.01em">{name}</div><div class="sans" style="font-size:20pt;letter-spacing:.3em;color:{accent}">{YEAR}</div></div>')
    notes = (f'<div style="position:absolute;left:0.55in;right:0.55in;bottom:0.35in;height:0.42in;display:flex;gap:10pt;align-items:flex-end">'
             f'<div class="sans" style="font-size:8pt;letter-spacing:.25em;color:{accent};font-weight:600">NOTES</div><div style="flex:1;border-bottom:1px solid #c9c1b5"></div></div>')
    art = f'<div style="position:absolute;left:0.55in;right:0.55in;top:0.5in;height:3.45in;border-radius:14px;overflow:hidden">{panel(i)}</div>'
    return f'<div class="page">{art}{title}{grid}{notes}</div>'

def mini(m, monday):
    name, fn, c = MONTHS[m - 1]
    hd = "".join(f'<div style="text-align:center;font-size:6.5pt;color:#8a8290;font-weight:600">{d[0]}</div>' for d in heads(monday))
    days = "".join(f'<div style="text-align:center;font-size:8pt;padding:1.5pt 0">{d or ""}</div>' for w in weeks(m, monday) for d in w)
    sw = f'<span style="display:inline-block;width:9pt;height:9pt;border-radius:50%;background:{c[1] if c[1] not in ("#ffffff", "#e8eef5") else c[0]};margin-right:5pt;vertical-align:middle"></span>'
    return (f'<div><div style="font-size:12.5pt;font-weight:600;margin-bottom:4pt">{sw}{name}</div>'
            f'<div class="sans" style="display:grid;grid-template-columns:repeat(7,1fr)">{hd}{days}</div></div>')

def year_page(monday):
    g = "".join(mini(m, monday) for m in range(1, 13))
    strip = "".join(f'<div style="flex:1">{panel(i, 300, 300, 120, 7)}</div>' for i in range(12))
    return (f'<div class="page"><div style="position:absolute;left:0;right:0;top:0;height:0.42in;display:flex">{strip}</div>'
            f'<div style="position:absolute;left:0.6in;right:0.6in;top:0.8in;display:flex;justify-content:space-between;align-items:baseline">'
            f'<div style="font-size:34pt;font-weight:600">{YEAR}</div><div class="sans" style="font-size:9pt;letter-spacing:.3em;color:#8a8290">YEAR AT A GLANCE</div></div>'
            f'<div style="position:absolute;left:0.6in;right:0.6in;top:1.7in;bottom:0.6in;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(4,1fr);gap:0.25in 0.4in">{g}</div></div>')

def cover(monday):
    tiles = "".join(f'<div style="border-radius:10px;overflow:hidden">{panel(i, 400, 400, 130, 3)}</div>' for i in range(12))
    return (f'<div class="page"><div style="position:absolute;left:0.55in;right:0.55in;top:0.55in;height:6.7in;display:grid;grid-template-columns:repeat(3,1fr);'
            f'grid-template-rows:repeat(4,1fr);gap:8px">{tiles}</div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0.75in;text-align:center"><div style="font-size:80pt;font-weight:600;line-height:1;letter-spacing:.04em">{YEAR}</div>'
            f'<div class="sans" style="font-size:10pt;letter-spacing:.42em;margin-top:10pt;color:#6f6878">A YEAR OF SEASONS · PRINTABLE CALENDAR</div>'
            f'<div class="sans" style="font-size:8pt;letter-spacing:.2em;margin-top:6pt;color:#9a93a2">{"MONDAY" if monday else "SUNDAY"} START</div></div></div>')

def build(size, monday):
    return CSS, [cover(monday), year_page(monday)] + [month_page(i, monday) for i in range(12)]

if __name__ == "__main__":
    out = sys.argv[1]; slug = "2027-printable-calendar"
    for size in ("letter", "a4"):
        for monday in (False, True):
            css, pages = build(size, monday)
            render(css, pages, size, f"{out}/{slug}-{'US-Letter' if size == 'letter' else 'A4'}-{'Monday' if monday else 'Sunday'}-Start.pdf")
    print("pages", len(pages))
