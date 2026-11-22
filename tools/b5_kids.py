"""Kids Routine & Chore Chart Pack printable (batch 5, lane h). 28 original flat icons drawn here as SVG.
Usage: python3 b5_kids.py <out_dir> -> kids-routine-chore-chart-pack-US-Letter.pdf / -A4.pdf"""
import math, sys
sys.path.insert(0, ".")
from render import render

INK, CREAM, TEAL, CORAL, SUN, SKY, LEAF, PLUM, SKIN = "#27324a", "#fffaf0", "#2f9c95", "#f0705a", "#f6b93b", "#5aa9e6", "#7cb86a", "#8e6bb8", "#f2c9a0"
NAME = "kids-routine-chore-chart-pack"
FOOT = "Purl &amp; Paper · Kids Routine &amp; Chore Charts"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: var(--pw); overflow: hidden; }}
body {{ font-family: Poppins, sans-serif; color: {INK}; }}
.page {{ width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: {CREAM}; contain: strict; }}
.round {{ font-family: Poppins, sans-serif; font-weight: 800; }}
.hd {{ position: absolute; left: 0.55in; right: 0.55in; top: 0.5in; text-align: center; }}
.hd h1 {{ font: 800 30pt/1.05 Poppins; color: {INK}; letter-spacing: -.01em; }}
.hd .k {{ display: inline-block; font: 700 9pt Poppins; letter-spacing: .16em; text-transform: uppercase; color: #fff; padding: 0.04in 0.16in; border-radius: 1in; margin-top: 0.08in; }}
.hd p {{ font: 9.5pt/1.45 Poppins; color: #5b6478; margin-top: 0.07in; }}
.body {{ position: absolute; left: 0.55in; right: 0.55in; top: 1.75in; bottom: 0.6in; }}
.foot {{ position: absolute; bottom: 0.3in; left: 0; right: 0; text-align: center; font: 7pt Poppins; color: #a39c8c; }}
.cut {{ outline: 1px dashed rgba(0,0,0,.3); outline-offset: -1px; }}
.ln {{ border-bottom: 1.5px solid {INK}40; height: 0.36in; }}
table.ch {{ width: 100%; border-collapse: separate; border-spacing: 0.05in; table-layout: fixed; }}
table.ch th {{ font: 700 10pt Poppins; color: #fff; border-radius: 0.08in; padding: 0.06in 0; }}
table.ch td {{ background: #fff; border: 2px solid {INK}18; border-radius: 0.1in; }}
table.ch .task {{ display: flex; align-items: center; gap: 0.1in; padding: 0.05in 0.1in; font: 700 10.5pt/1.15 Poppins; height: 100%; }}
svg {{ display: block; }}
.dots {{ position:absolute; inset:0; background-image: radial-gradient({INK}0f 1.4px, transparent 1.6px); background-size: 0.22in 0.22in; }}
"""


# ---------- icons (viewBox 0 0 100 100) ----------
def C(cx, cy, r, f, extra=""): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" {extra}/>'
def R(x, y, w, h, f, rx=0, extra=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" {extra}/>'
def P(d, f, extra=""): return f'<path d="{d}" fill="{f}" {extra}/>'
def L(x1, y1, x2, y2, c, w): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'


def i_sun():
    rays = "".join(L(50 + 30 * math.cos(a), 50 + 30 * math.sin(a), 50 + 42 * math.cos(a), 50 + 42 * math.sin(a), SUN, 6) for a in [k * math.pi / 4 for k in range(8)])
    return rays + C(50, 50, 22, SUN) + C(43, 47, 2.6, INK) + C(57, 47, 2.6, INK) + P("M42 56 Q50 63 58 56", "none", f'stroke="{INK}" stroke-width="3" stroke-linecap="round"')
def i_bed(): return R(10, 52, 80, 20, SKY, 6) + R(10, 40, 26, 16, "#fff", 6, f'stroke="{INK}" stroke-width="2"') + R(36, 44, 54, 14, CORAL, 6) + R(10, 30, 7, 50, INK, 3) + R(83, 50, 7, 30, INK, 3)
def i_teeth(): return R(18, 44, 64, 12, TEAL, 6, 'transform="rotate(-30 50 50)"') + R(62, 22, 18, 14, "#fff", 4, f'stroke="{INK}" stroke-width="2" transform="rotate(-30 50 50)"') + C(30, 80, 6, SKY, 'opacity=".5"') + C(20, 70, 4, SKY, 'opacity=".5"')
def i_shirt(): return P("M30 20 L42 16 Q50 26 58 16 L70 20 L88 36 L76 48 L70 42 L70 86 L30 86 L30 42 L24 48 L12 36 Z", CORAL) + C(50, 58, 6, "#fff", 'opacity=".6"')
def i_bowl(): return P("M14 46 L86 46 Q84 80 50 82 Q16 80 14 46 Z", SKY) + C(36, 42, 7, SUN) + C(50, 40, 8, "#fff") + C(63, 42, 7, CORAL) + L(64, 38, 84, 16, INK, 4)
def i_brush(): return R(44, 46, 12, 44, PLUM, 6) + R(26, 12, 48, 38, PLUM, 16) + "".join(L(32 + 6 * k, 20, 32 + 6 * k, 42, "#fff", 2) for k in range(7))
def i_backpack(): return R(22, 22, 56, 66, TEAL, 16) + R(32, 54, 36, 26, "#fff", 8, 'opacity=".55"') + P("M36 24 Q36 8 50 8 Q64 8 64 24", "none", f'stroke="{INK}" stroke-width="5"') + R(46, 60, 8, 8, SUN, 2)
def i_shoes(): return P("M8 62 Q10 44 26 46 L36 54 L48 58 Q54 62 54 70 L8 70 Z", CORAL) + R(8, 70, 46, 7, INK, 3) + P("M48 52 Q50 34 66 36 L76 44 L88 48 Q94 52 94 60 L48 60 Z", SKY) + R(48, 60, 46, 7, INK, 3)
def i_wash(): return R(18, 54, 64, 26, SKY, 8) + C(36, 46, 9, "#ffffff", f'stroke="{SKY}" stroke-width="3"') + C(54, 36, 7, "#ffffff", f'stroke="{SKY}" stroke-width="3"') + C(68, 48, 5, "#ffffff", f'stroke="{SKY}" stroke-width="3"') + R(30, 60, 40, 10, "#fff", 5, 'opacity=".6"')
def i_book(): return P("M10 26 Q30 18 50 28 Q70 18 90 26 L90 80 Q70 72 50 82 Q30 72 10 80 Z", SUN) + P("M50 28 L50 82", "none", f'stroke="{INK}" stroke-width="3"') + "".join(L(18, 38 + 9 * k, 42, 36 + 9 * k, "#fff", 3) + L(58, 36 + 9 * k, 82, 38 + 9 * k, "#fff", 3) for k in range(4))
def i_bath(): return R(10, 46, 80, 26, SKY, 12) + R(14, 70, 8, 14, INK, 3) + R(78, 70, 8, 14, INK, 3) + C(34, 42, 9, "#fff", f'stroke="{SKY}" stroke-width="2"') + C(52, 36, 11, "#fff", f'stroke="{SKY}" stroke-width="2"') + C(70, 42, 8, "#fff", f'stroke="{SKY}" stroke-width="2"') + P("M18 46 L18 18 Q18 10 28 12", "none", f'stroke="{INK}" stroke-width="4"')
def i_moon(): return P("M60 14 A38 38 0 1 0 86 64 A30 30 0 1 1 60 14 Z", SUN) + C(30, 24, 3, SUN) + C(20, 44, 2, SUN) + C(84, 24, 3, SUN)
def i_pjs(): return i_shirt().replace(CORAL, PLUM) + C(40, 56, 3, "#fff") + C(60, 70, 3, "#fff") + C(52, 48, 2.5, "#fff")
def i_toys(): return R(12, 52, 30, 30, CORAL, 5) + R(46, 52, 30, 30, SKY, 5) + R(28, 20, 30, 30, SUN, 5) + '<text x="27" y="75" font-family="Poppins" font-weight="800" font-size="22" fill="#fff" text-anchor="middle">A</text><text x="61" y="75" font-family="Poppins" font-weight="800" font-size="22" fill="#fff" text-anchor="middle">B</text><text x="43" y="43" font-family="Poppins" font-weight="800" font-size="22" fill="#fff" text-anchor="middle">C</text>'
def i_plant(): return P("M30 60 L70 60 L64 90 L36 90 Z", CORAL) + P("M50 60 Q48 40 50 24", "none", f'stroke="{LEAF}" stroke-width="4"') + P("M50 40 Q30 40 26 22 Q44 22 50 40 Z", LEAF) + P("M50 34 Q68 34 74 16 Q56 16 50 34 Z", LEAF)
def i_pet(): return P("M14 62 L86 62 L78 84 L22 84 Z", CORAL) + C(36, 58, 6, "#b07a4a") + C(48, 56, 6, "#b07a4a") + C(60, 58, 6, "#b07a4a") + C(50, 26, 8, INK) + C(36, 18, 5, INK) + C(64, 18, 5, INK) + C(38, 30, 4, INK) + C(62, 30, 4, INK)
def i_table(): return C(50, 52, 30, "#fff", f'stroke="{SKY}" stroke-width="5"') + C(50, 52, 18, SKY, 'opacity=".35"') + R(8, 26, 6, 52, INK, 3) + R(86, 26, 6, 52, INK, 3) + P("M6 24 L16 24 L16 40 Q11 44 6 40 Z", INK)
def i_trash(): return R(24, 30, 52, 58, LEAF, 6) + R(18, 22, 64, 10, INK, 4) + R(42, 14, 16, 8, INK, 3) + L(38, 42, 38, 78, "#fff", 4) + L(50, 42, 50, 78, "#fff", 4) + L(62, 42, 62, 78, "#fff", 4)
def i_laundry(): return P("M16 40 L84 40 L76 88 L24 88 Z", SUN) + P("M24 40 Q28 18 44 26 Q52 14 62 26 Q76 20 76 40 Z", SKY) + "".join(L(28 + 12 * k, 50, 26 + 12 * k, 80, "#fff", 3) for k in range(5))
def i_broom(): return L(70, 10, 46, 60, "#b07a4a", 6) + P("M30 54 L56 64 L48 92 L14 80 Z", SUN) + "".join(L(22 + 8 * k, 82 + 3 * k, 28 + 8 * k, 66 + 3 * k, "#c9902a", 2) for k in range(4))
def i_dishes(): return C(44, 56, 30, "#fff", f'stroke="{TEAL}" stroke-width="5"') + C(44, 56, 15, TEAL, 'opacity=".3"') + C(76, 26, 8, "#fff", f'stroke="{SKY}" stroke-width="3"') + C(86, 44, 5, "#fff", f'stroke="{SKY}" stroke-width="3"') + C(70, 12, 4, "#fff", f'stroke="{SKY}" stroke-width="3"')
def i_pencil(): return R(10, 60, 66, 70 - 52, SUN, 2, 'transform="rotate(-35 50 60)"') + P("M76 60 L92 69 L76 78 Z", SKIN, 'transform="rotate(-35 50 60)"') + R(4, 60, 10, 18, CORAL, 3, 'transform="rotate(-35 50 60)"') + L(20, 90, 80, 90, INK, 3)
def i_apple(): return P("M50 30 Q30 18 18 38 Q8 62 28 82 Q40 92 50 84 Q60 92 72 82 Q92 62 82 38 Q70 18 50 30 Z", CORAL) + P("M50 30 Q48 18 54 10", "none", f'stroke="#7a4a2a" stroke-width="4"') + P("M54 20 Q66 8 76 16 Q66 28 54 20 Z", LEAF) + P("M30 44 Q28 54 32 60", "none", 'stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".6"')
def i_water(): return P("M28 14 L72 14 L66 88 L34 88 Z", "#fff", f'stroke="{SKY}" stroke-width="4"') + P("M31 40 L69 40 L66 85 L34 85 Z", SKY, 'opacity=".55"') + C(50, 62, 5, "#fff", 'opacity=".7"')
def i_hug(): return P("M50 86 Q14 60 14 36 Q14 16 32 16 Q44 16 50 30 Q56 16 68 16 Q86 16 86 36 Q86 60 50 86 Z", CORAL) + P("M30 30 Q26 38 30 46", "none", 'stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".6"')
def i_toilet(): return R(26, 10, 40, 26, "#fff", 6, f'stroke="{INK}" stroke-width="3"') + P("M18 40 L82 40 Q80 70 56 74 L60 90 L36 90 L40 74 Q20 70 18 40 Z", "#fff", f'stroke="{INK}" stroke-width="3"') + R(18, 38, 64, 8, SKY, 4)
def i_star(col=SUN):
    pts = " ".join(f"{50 + (44 if k % 2 == 0 else 19) * math.cos(-math.pi / 2 + k * math.pi / 5):.1f},{54 + (44 if k % 2 == 0 else 19) * math.sin(-math.pi / 2 + k * math.pi / 5):.1f}" for k in range(10))
    return f'<polygon points="{pts}" fill="{col}" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>'
def i_tidy(): return R(14, 44, 72, 44, "#c9a27a", 6) + R(10, 36, 80, 12, "#b0865c", 4) + R(26, 26, 18, 22, CORAL, 4) + C(60, 32, 12, SKY)

ICONS = {"Wake up": i_sun, "Make my bed": i_bed, "Brush teeth": i_teeth, "Get dressed": i_shirt, "Eat breakfast": i_bowl, "Brush hair": i_brush,
         "Pack my bag": i_backpack, "Shoes on": i_shoes, "Wash hands": i_wash, "Read a book": i_book, "Bath time": i_bath, "Lights out": i_moon,
         "Pyjamas on": i_pjs, "Tidy toys": i_toys, "Water plants": i_plant, "Feed the pet": i_pet, "Set the table": i_table, "Take out trash": i_trash,
         "Laundry": i_laundry, "Sweep": i_broom, "Do the dishes": i_dishes, "Homework": i_pencil, "Healthy snack": i_apple, "Drink water": i_water,
         "Hugs & kisses": i_hug, "Use the toilet": i_toilet, "Put things away": i_tidy, "Be kind": lambda: i_star(SUN)}


def ic(name, size="0.42in"): return f'<svg viewBox="0 0 100 100" style="width:{size};height:{size};flex:none">{ICONS[name]()}</svg>'


def page(title, kicker, kcol, intro, body, top=None):
    st = f' style="top:{top}"' if top else ""
    return (f'<div class="page"><div class="hd"><h1>{title}</h1><div class="k" style="background:{kcol}">{kicker}</div>'
            + (f'<p>{intro}</p>' if intro else "") + f'</div><div class="body"{st}>{body}</div><div class="foot">{FOOT}</div></div>')


def namebar(col):
    return (f'<div style="display:flex;gap:0.25in;font:700 10pt Poppins;margin-bottom:0.1in"><div style="flex:1">Name: <span style="display:inline-block;width:2.4in;border-bottom:2px solid {col}"></span></div>'
            f'<div>Week of: <span style="display:inline-block;width:1.5in;border-bottom:2px solid {col}"></span></div></div>')


def week_chart(tasks, col, rowh=0.66, blank=0):
    hd = f'<tr><th style="width:2.35in;background:{col}">Task</th>' + "".join(f'<th style="background:{col}">{d}</th>' for d in DAYS) + "</tr>"
    rows = ""
    for t in tasks:
        rows += (f'<tr style="height:{rowh}in"><td><div class="task">{ic(t)}<span>{t}</span></div></td>' + "".join("<td></td>" for _ in DAYS) + "</tr>")
    for _ in range(blank):
        rows += (f'<tr style="height:{rowh}in"><td><div class="task"><div style="width:0.42in;height:0.42in;border:2px dashed {INK}30;border-radius:0.08in;flex:none"></div>'
                 f'<span style="flex:1;border-bottom:1.5px solid {INK}30;height:0.2in"></span></div></td>' + "".join("<td></td>" for _ in DAYS) + "</tr>")
    return f'<table class="ch">{hd}{rows}</table>'


def cover():
    tiles = list(ICONS)[:15]
    grid = "".join(f'<div style="background:#fff;border-radius:0.18in;display:flex;align-items:center;justify-content:center;box-shadow:0 0.03in 0 {INK}14">{ic(n, "0.75in")}</div>' for n in tiles)
    return (f'<div class="page" style="background:{SUN}22"><div class="dots"></div>'
            f'<div style="position:absolute;left:0.8in;right:0.8in;top:0.75in;display:grid;grid-template-columns:repeat(5,1fr);grid-auto-rows:1.05in;gap:0.16in">{grid}</div>'
            f'<div style="position:absolute;left:0.6in;right:0.6in;top:4.95in;text-align:center">'
            f'<div style="font:800 44pt/1 Poppins;color:{INK};letter-spacing:-.02em">Routine &amp;<br>Chore Charts</div>'
            f'<div style="display:inline-block;font:700 11pt Poppins;letter-spacing:.14em;color:#fff;background:{CORAL};padding:0.06in 0.24in;border-radius:1in;margin-top:0.18in">FOR KIDS · AGES 3 TO 12</div>'
            f'<div style="font:10.5pt/1.6 Poppins;color:#5b6478;margin-top:0.2in">Morning, after-school and bedtime routines · chore charts by age<br>reward charts · 28 picture cards + blanks · reward coupons · my 2027 goals</div></div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0.55in;text-align:center;font:8.5pt Poppins;color:#8a8576">Print at home at 100% · US Letter &amp; A4 · laminate and use a dry-erase marker to reuse every week</div></div>')


def tips():
    tip = [("Start small", "Pick 3 to 5 tasks to begin with. Add more once the routine feels easy."),
           ("Make it visible", "Hang charts at child height: the fridge, the bathroom door, by the bed."),
           ("Laminate it", "Slip charts into sheet protectors or laminate them and use a dry-erase marker. Reuse every week."),
           ("Tick together", "Let your child tick, colour or sticker each box. Celebrate a full row!"),
           ("Pick rewards together", "Small and often works best: a sticker, a story, choosing dinner, extra play time."),
           ("Picture cards", "Cut out the cards for a velcro or magnet board. Little ones who can't read yet follow the pictures."),
           ("Ages are a guide", "Every child is different. Use the blank chart to make your own list.")]
    body = "".join(f'<div style="display:flex;gap:0.18in;align-items:flex-start;padding:0.12in 0;border-bottom:2px dotted {INK}20">'
                   f'<div style="flex:none;width:0.46in;height:0.46in;border-radius:50%;background:{[TEAL, CORAL, SUN, SKY, PLUM, LEAF, CORAL][i]};color:#fff;font:800 15pt Poppins;display:flex;align-items:center;justify-content:center">{i + 1}</div>'
                   f'<div><div style="font:700 12pt Poppins">{a}</div><div style="font:10pt/1.5 Poppins;color:#5b6478">{b}</div></div></div>' for i, (a, b) in enumerate(tip))
    contents = ["Morning routine", "After-school routine", "Bedtime routine", "Chore charts: ages 3-5, 6-9, 10+", "Make-your-own chore chart",
                "Reward charts: 20 stars and 30 stickers", "28 picture routine cards", "Reward coupons", "My 2027 goals"]
    side = "".join(f'<div style="font:9.5pt Poppins;padding:0.05in 0;border-bottom:1px solid {INK}15">{c}</div>' for c in contents)
    return page("For grown-ups", "tips for success", TEAL, "Routines give kids a sense of calm and confidence. These charts make them visual and fun.",
                f'<div style="display:grid;grid-template-columns:1.7fr 1fr;gap:0.35in"><div>{body}</div><div style="background:#fff;border-radius:0.16in;padding:0.2in 0.22in;align-self:start">'
                f'<div style="font:800 12pt Poppins;margin-bottom:0.08in">What\'s inside</div>{side}</div></div>', top="1.95in")


ROUTINES = [("Good Morning!", "morning routine", SUN, ["Wake up", "Use the toilet", "Wash hands", "Get dressed", "Eat breakfast", "Brush teeth", "Brush hair", "Shoes on", "Pack my bag"]),
            ("After School", "after-school routine", TEAL, ["Put things away", "Wash hands", "Healthy snack", "Drink water", "Homework", "Read a book", "Tidy toys", "Set the table"]),
            ("Good Night!", "bedtime routine", PLUM, ["Tidy toys", "Bath time", "Pyjamas on", "Brush teeth", "Use the toilet", "Read a book", "Hugs & kisses", "Lights out"])]
CHORES = [("Little Helper", "chores for ages 3 to 5", CORAL, ["Make my bed", "Tidy toys", "Put things away", "Feed the pet", "Water plants", "Set the table", "Laundry", "Be kind"]),
          ("Super Helper", "chores for ages 6 to 9", SKY, ["Make my bed", "Tidy toys", "Set the table", "Feed the pet", "Water plants", "Laundry", "Take out trash", "Do the dishes", "Homework"]),
          ("Team Player", "chores for ages 10 to 12", LEAF, ["Make my bed", "Laundry", "Do the dishes", "Sweep", "Take out trash", "Feed the pet", "Set the table", "Homework", "Water plants"])]


def chart_page(title, kicker, col, tasks):
    rowh = min(0.92, 8.0 / (len(tasks) + 1))
    return page(title, kicker, col, None, namebar(col) + week_chart(tasks, col, rowh), top="1.55in")


def blank_page():
    return page("My Chore Chart", "make your own", CORAL, None, namebar(CORAL) + week_chart([], CORAL, 0.72, blank=10), top="1.55in")


def reward_page(n, title, col, cols):
    cells = "".join(f'<div style="aspect-ratio:1;background:#fff;border:2.5px dashed {col};border-radius:50%;display:flex;align-items:center;justify-content:center">'
                    f'<svg viewBox="0 0 100 100" style="width:55%;opacity:.13">{i_star(col)}</svg></div>' for _ in range(n - 1))
    cells += (f'<div style="aspect-ratio:1;background:{col};border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font:800 10pt/1.05 Poppins;text-align:center">'
              f'PRIZE!</div>')
    top = (f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.25in;margin-bottom:0.25in;font:700 10.5pt Poppins">'
           f'<div>I am working on:<div class="ln"></div></div><div>When I fill my chart I get:<div class="ln"></div></div></div>')
    return page(title, f"{n} stickers to a prize", col, "Add a sticker or colour a star each time you do it. Fill them all to win your prize!",
                top + f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:0.14in">{cells}</div>', top="2.05in")


def cards_pages():
    names = list(ICONS); out = []
    for k in range(2):
        chunk = names[k * 14:(k + 1) * 14]
        cols = [TEAL, CORAL, SUN, SKY, PLUM, LEAF]
        cards = "".join(f'<div class="cut" style="display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff;padding:0.08in">'
                        f'<div style="background:{cols[i % 6]}22;border-radius:0.16in;padding:0.1in">{ic(n, "1.05in")}</div>'
                        f'<div style="font:800 11pt Poppins;margin-top:0.08in;text-align:center">{n}</div></div>' for i, n in enumerate(chunk))
        cards += "".join(f'<div class="cut" style="display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff;padding:0.08in">'
                         f'<div style="width:1.25in;height:1.25in;border:2.5px dashed {INK}30;border-radius:0.16in;display:flex;align-items:center;justify-content:center;font:600 8pt Poppins;color:#a39c8c">draw it</div>'
                         f'<div style="width:1.3in;border-bottom:1.5px solid {INK}40;height:0.26in"></div></div>' for _ in range(2))
        out.append(page("Picture Routine Cards", f"cut out · set {k + 1} of 2", [SKY, CORAL][k], "For velcro, magnet or pocket boards. Laminate them so they last.",
                        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:1.95in;gap:0">{cards}</div>', top="1.95in"))
    return out


def coupons():
    cs = [("Pick what's for dinner", SUN, "Eat breakfast"), ("Stay up 15 minutes later", PLUM, "Lights out"), ("Extra story at bedtime", TEAL, "Read a book"),
          ("Choose a family movie", CORAL, "Be kind"), ("A trip to the park", LEAF, "Water plants"), ("Bake a treat together", SUN, "Healthy snack"),
          ("Skip one chore", SKY, "Sweep"), ("Big bear hug + a surprise", CORAL, "Hugs & kisses")]
    cards = "".join(f'<div class="cut" style="display:flex;align-items:center;gap:0.18in;padding:0.18in 0.22in;background:{c}1f">'
                    f'<div style="background:#fff;border-radius:50%;padding:0.1in;flex:none">{ic(i, "0.7in")}</div>'
                    f'<div><div style="font:700 8pt Poppins;letter-spacing:.2em;color:{c}">REWARD COUPON</div><div style="font:800 14pt/1.15 Poppins;margin-top:0.03in">{t}</div>'
                    f'<div style="font:8.5pt Poppins;color:#5b6478;margin-top:0.05in">For: ____________ &nbsp; Signed: ____________</div></div></div>' for t, c, i in cs)
    return page("Reward Coupons", "cut out &amp; give", CORAL, "Hand one out when a reward chart is full, or as a lovely surprise.",
                f'<div style="display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1.95in;gap:0">{cards}</div>', top="1.95in")


def goals():
    qs = [("Something I want to learn", "Read a book"), ("A new food I'll try", "Healthy snack"), ("A way I can help at home", "Sweep"),
          ("A way I can be kind", "Be kind"), ("A place I want to go", "Shoes on"), ("Something I'll get better at", "Homework")]
    boxes = "".join(f'<div style="background:#fff;border-radius:0.16in;padding:0.14in 0.18in;border:2.5px solid {[TEAL, CORAL, SUN, SKY, PLUM, LEAF][i]}">'
                    f'<div style="display:flex;align-items:center;gap:0.1in">{ic(icn, "0.45in")}<div style="font:800 11pt Poppins">{q}</div></div>'
                    f'<div class="ln"></div><div class="ln"></div></div>' for i, (q, icn) in enumerate(qs))
    draw = (f'<div style="grid-column:span 2;background:#fff;border-radius:0.16in;border:2.5px dashed {INK}30;height:2.05in;padding:0.14in 0.18in;font:800 11pt Poppins">'
            f'Draw me in 2027! <span style="font:400 9pt Poppins;color:#5b6478">&nbsp; I am ____ years old</span></div>')
    return page("My 2027 Goals", "a fresh start for kids", PLUM, None, f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.16in">{boxes}{draw}</div>', top="1.45in")


def build(out):
    pages = [cover(), tips()] + [chart_page(*r) for r in ROUTINES] + [chart_page(*c) for c in CHORES] + [blank_page(),
             reward_page(20, "Star Chart", SUN, 5), reward_page(30, "Super Star Chart", TEAL, 6)] + cards_pages() + [coupons(), goals()]
    for size in ("letter", "a4"):
        render(CSS, pages, size, f"{out}/{NAME}-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print(len(pages), "pages")


if __name__ == "__main__":
    build(sys.argv[1])
