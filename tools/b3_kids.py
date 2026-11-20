"""Kids Christmas Activity Pack printable (batch 3): colouring pages, word searches, mazes, dot-to-dot and more.
All artwork is original line art drawn here as SVG. Mazes and word searches are generated (seeded) with answer keys."""
import math, random, sys
sys.path.insert(0, ".")
from render import render
from kits2 import star as fstar, bauble, holly, gift, snowflake as fsnow, tree as ftree, mitten as fmitten

K = "#222"          # line colour
RED, GREEN, GOLD, BLUE, PINK = "#d64545", "#2e8b57", "#f2b631", "#3d8bd4", "#f08bb0"
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Poppins, sans-serif; color: #222; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #fff; }
.t { position: absolute; left: 0.5in; right: 0.5in; top: 0.45in; text-align: center; }
.t h1 { font: 700 30pt/1.05 Poppins; letter-spacing: -.01em; }
.t p { font: 11pt/1.4 Poppins; color: #555; margin-top: 0.05in; }
.box { position: absolute; left: 0.5in; right: 0.5in; top: 1.55in; bottom: 0.6in; display: flex; align-items: center; justify-content: center; }
.foot { position: absolute; bottom: 0.25in; left: 0; right: 0; text-align: center; font: 7pt Poppins; color: #aaa; }
.name { position: absolute; right: 0.55in; top: 0.2in; font: 9pt Poppins; color: #888; }
svg { display: block; }
.ln { border-bottom: 1.5px solid #bbb; height: 0.42in; }
"""


def U(*shapes):
    """Outlined union: every shape drawn thick in ink, then filled white on top, so overlaps merge into one outline."""
    back = "".join(s.replace("FILL", K).replace("SW", "14") for s in shapes)
    front = "".join(s.replace("FILL", "#fff").replace("SW", "0") for s in shapes)
    return back + front


def circ(cx, cy, r): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="FILL" stroke="FILL" stroke-width="SW"/>'
def rect(x, y, w, h, rx=0): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="FILL" stroke="FILL" stroke-width="SW" stroke-linejoin="round"/>'
def poly(pts): return f'<polygon points="{pts}" fill="FILL" stroke="FILL" stroke-width="SW" stroke-linejoin="round"/>'
def limb(x1, y1, x2, y2, w): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="FILL" stroke-width="{w}" stroke-linecap="round" data-w="{w}"/>'


def U2(*shapes):
    """Like U but limbs (thick lines) need width + 14 in the back layer."""
    back, front = "", ""
    for s in shapes:
        if "data-w" in s:
            w = int(s.split('data-w="')[1].split('"')[0])
            back += s.replace("FILL", K).replace(f'stroke-width="{w}"', f'stroke-width="{w + 14}"'); front += s.replace("FILL", "#fff")
        else:
            back += s.replace("FILL", K).replace("SW", "14"); front += s.replace("FILL", "#fff").replace("SW", "0")
    return back + front


def L(d, w=5): return f'<path d="{d}" fill="none" stroke="{K}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def O(cx, cy, r, w=5, fill="#fff"): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{K}" stroke-width="{w}"/>'
def D(cx, cy, r): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{K}"/>'


def ostar(cx, cy, r, w=5, pts=5, inner=.45):
    p = []
    for i in range(pts * 2):
        rr = r if i % 2 == 0 else r * inner; a = -math.pi / 2 + i * math.pi / pts
        p.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="#fff" stroke="{K}" stroke-width="{w}" stroke-linejoin="round"/>'


def oflake(cx, cy, r, w=4):
    out = ""
    for k in range(6):
        a = math.radians(k * 60 + 30); x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        out += L(f"M{cx},{cy} L{x2:.1f},{y2:.1f}", w)
        bx, by = cx + r * .55 * math.cos(a), cy + r * .55 * math.sin(a)
        for s in (-1, 1):
            b = a + s * math.radians(42)
            out += L(f"M{bx:.1f},{by:.1f} l{r * .3 * math.cos(b):.1f},{r * .3 * math.sin(b):.1f}", w)
    return out


def sky(seed, n, box, avoid):
    r = random.Random(seed); out = ""; x0, y0, x1, y1 = box; placed = []
    tries = 0
    while len(placed) < n and tries < 2000:
        tries += 1; x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        if any(ax0 < x < ax1 and ay0 < y < ay1 for ax0, ay0, ax1, ay1 in avoid): continue
        if any((x - px) ** 2 + (y - py) ** 2 < 75 ** 2 for px, py in placed): continue
        placed.append((x, y)); out += oflake(x, y, r.uniform(16, 26)) if r.random() < .6 else ostar(x, y, r.uniform(12, 18), 4)
    return out


# ---------------- colouring pages (viewBox 0 0 800 1000) ----------------
def c_snowman():
    body = U2(circ(400, 760, 175), circ(400, 520, 125), circ(400, 330, 92), limb(300, 500, 170, 400, 10), limb(500, 500, 640, 390, 10),
              limb(205, 430, 175, 360, 8), limb(605, 418, 650, 350, 8))
    hat = U(rect(330, 175, 140, 105, 8), rect(295, 268, 210, 28, 14)) + L("M330,250 L470,250", 5)
    face = D(368, 318, 10) + D(432, 318, 10) + f'<polygon points="400,336 400,356 470,350" fill="#fff" stroke="{K}" stroke-width="5" stroke-linejoin="round"/>' + "".join(D(400 + dx, 385 + dy, 6) for dx, dy in [(-34, -6), (-18, 4), (0, 8), (18, 4), (34, -6)])
    scarf = U(rect(318, 405, 164, 44, 22), rect(430, 430, 48, 130, 14)) + L("M455,520 L455,560 M440,525 L440,560 M470,525 L470,560", 4) + L("M350,410 L345,445 M390,410 L385,447 M430,410 L425,447", 4)
    btn = O(400, 500, 14) + O(400, 560, 14) + O(400, 700, 16) + O(400, 770, 16)
    ground = L("M40,920 C180,880 300,905 400,915 C520,925 640,880 760,905", 6)
    tree = U(poly("100,880 160,770 220,880"), poly("115,800 160,710 205,800")) + U(poly("600,890 680,720 760,890"), poly("620,780 680,650 740,780"))
    return sky(1, 16, (40, 40, 760, 640), [(240, 130, 560, 950)]) + tree + body + scarf + hat + face + btn + ground


def c_gingerbread():
    man = U2(circ(400, 250, 120), rect(275, 330, 250, 330, 90), limb(300, 410, 150, 330, 92), limb(500, 410, 650, 330, 92),
             limb(330, 620, 270, 860, 100), limb(470, 620, 530, 860, 100))
    icing = (L("M120,300 q10,20 0,40 q-10,20 0,40", 6) + L("M680,300 q-10,20 0,40 q10,20 0,40", 6)
             + L("M215,840 q20,-12 40,0 q20,12 40,0", 6) + L("M505,840 q20,-12 40,0 q20,12 40,0", 6))
    face = D(360, 235, 13) + D(440, 235, 13) + L("M345,290 Q400,335 455,290", 7) + O(320, 280, 12) + O(480, 280, 12)
    bow = U(poly("400,375 330,340 330,410"), poly("400,375 470,340 470,410"), circ(400, 375, 22))
    btn = O(400, 470, 22) + O(400, 545, 22) + O(400, 620, 18)
    candy = "".join(U(rect(x - 30, 900, 60, 50, 25)) + L(f"M{x - 30},925 L{x - 52},905 L{x - 52},945 Z M{x + 30},925 L{x + 52},905 L{x + 52},945 Z", 5) for x in (130, 670))
    hearts = "".join(L(f"M{x},{y} c-20,-30 -60,-10 -30,25 l30,25 l30,-25 c30,-35 -10,-55 -30,-25 Z", 5) for x, y in [(130, 120), (670, 130), (110, 610), (690, 620)])
    return hearts + candy + man + icing + bow + face + btn


def c_tree():
    t = U(poly("400,140 600,420 200,420"), poly("400,280 660,600 140,600"), poly("400,430 720,800 80,800"), rect(355, 795, 90, 85, 6))
    garland = L("M285,380 Q400,440 520,385", 5) + L("M215,560 Q400,640 590,555", 5) + L("M150,760 Q400,850 655,752", 5)
    orn = "".join(O(x, y, r) + L(f"M{x - r * .7:.0f},{y} Q{x},{y + r * .5:.0f} {x + r * .7:.0f},{y}", 4) for x, y, r in [(340, 330, 22), (470, 470, 26), (300, 500, 24), (420, 690, 30), (250, 700, 26), (560, 680, 28), (520, 330, 18)])
    top = ostar(400, 120, 70, 6)
    presents = (U(rect(120, 830, 170, 130, 6)) + L("M205,830 L205,960 M120,890 L290,890", 5) + L("M205,830 C170,780 140,810 205,830 C240,780 270,810 205,830", 5)
                + U(rect(520, 860, 190, 100, 6)) + L("M615,860 L615,960 M520,905 L710,905", 5) + L("M615,860 C580,815 555,840 615,860 C650,815 675,840 615,860", 5)
                + U(rect(330, 900, 140, 60, 6)) + L("M400,900 L400,960", 5))
    return sky(3, 10, (40, 40, 760, 500), [(170, 40, 630, 820)]) + t + garland + orn + top + presents


def c_stocking():
    s = U(rect(260, 260, 220, 470, 10), rect(230, 600, 400, 210, 105), rect(230, 190, 280, 110, 22))
    s = s + U(rect(230, 190, 280, 110, 22))
    pattern = ostar(370, 420, 40) + oflake(330, 560, 34) + ostar(420, 650, 30) + O(530, 715, 30) + O(320, 720, 20)
    heel = L("M275,620 Q300,700 375,705", 5) + L("M560,620 Q610,660 600,740", 5)
    cane = (f'<path d="M560,330 L560,140 A55,55 0 0,0 450,140" fill="none" stroke="{K}" stroke-width="44" stroke-linecap="round"/>'
            f'<path d="M560,330 L560,140 A55,55 0 0,0 450,140" fill="none" stroke="#fff" stroke-width="30" stroke-linecap="round"/>'
            + L("M545,300 L575,280 M545,250 L575,230 M545,200 L575,180 M548,150 L572,128 M520,100 L530,130 M478,97 L495,124", 4))
    holl = "".join(L(f"M{x},{y} c25,-20 50,-10 70,-30 c0,25 15,40 35,40 c-25,15 -45,35 -55,60 c-10,-25 -30,-40 -50,-40 Z", 5) for x, y in [(110, 200), (600, 520)])
    name = '<rect x="290" y="215" width="160" height="60" rx="10" fill="#fff" stroke="#222" stroke-width="4" stroke-dasharray="10 8"/>'
    return sky(4, 18, (40, 40, 760, 960), [(200, 80, 680, 830)]) + cane + s + name + heel + pattern


def c_house():
    h = U(rect(170, 470, 460, 380, 10), poly("120,500 400,200 680,500"), rect(520, 230, 70, 160, 6))
    snowroof = L("M130,495 Q160,540 190,495 Q220,540 250,495 Q280,540 310,495 Q340,540 370,495 Q400,540 430,495 Q460,540 490,495 Q520,540 550,495 Q580,540 610,495 Q640,540 670,495", 6)
    door = (f'<path d="M340,850 L340,700 A60,60 0 0,1 460,700 L460,850" fill="#fff" stroke="{K}" stroke-width="6"/>' + O(440, 780, 8))
    win = "".join(U(rect(x, 600, 100, 100, 8)) + L(f"M{x + 50},600 L{x + 50},700 M{x},650 L{x + 100},650", 5) for x in (205, 495))
    candies = "".join(O(x, 450, 16) for x in range(190, 620, 54)) + "".join(O(x, 340 + (abs(x - 400) * .9), 12) for x in (260, 330, 470, 540))
    roofwin = O(400, 380, 45) + L("M355,380 L445,380 M400,335 L400,425", 5)
    canes = "".join(f'<path d="M{x},850 L{x},600" stroke="{K}" stroke-width="5"/>' for x in ())
    ground = L("M40,880 C200,860 600,860 760,880", 6) + L("M60,940 C260,925 540,925 740,940", 4)
    trees = U(poly("60,860 110,700 160,860"), poly("70,760 110,630 150,760")) + U(poly("650,860 700,690 750,860"), poly("660,750 700,620 740,750"))
    path = L("M330,855 Q300,920 240,960 M470,855 Q500,920 560,960", 5)
    smoke = L("M555,215 C520,180 590,150 550,110 C520,80 580,60 560,30", 5)
    return sky(5, 10, (40, 40, 760, 400), [(110, 190, 690, 900), (500, 0, 620, 240)]) + trees + h + snowroof + roofwin + candies + door + win + ground + path + smoke + canes


def c_mandala():
    cx, cy = 400, 520; out = ""
    out += "".join(f'<g transform="rotate({k * 30} {cx} {cy})">' + L(f"M{cx},{cy - 90} C{cx - 70},{cy - 200} {cx - 40},{cy - 330} {cx},{cy - 360} C{cx + 40},{cy - 330} {cx + 70},{cy - 200} {cx},{cy - 90} Z", 5) + "</g>" for k in range(12))
    out += "".join(f'<g transform="rotate({k * 30 + 15} {cx} {cy})">' + L(f"M{cx},{cy - 120} C{cx - 30},{cy - 180} {cx - 20},{cy - 230} {cx},{cy - 250} C{cx + 20},{cy - 230} {cx + 30},{cy - 180} {cx},{cy - 120} Z", 4) + O(cx, cy - 290, 14, 4) + "</g>" for k in range(12))
    out += O(cx, cy, 120, 5) + O(cx, cy, 80, 5)
    out += "".join(f'<g transform="rotate({k * 45} {cx} {cy})">' + L(f"M{cx},{cy - 78} L{cx - 18},{cy - 30} L{cx},{cy} L{cx + 18},{cy - 30} Z", 4) + "</g>" for k in range(8))
    out += "".join(O(cx + 100 * math.cos(math.radians(a)), cy + 100 * math.sin(math.radians(a)), 9, 4) for a in range(0, 360, 30))
    out += O(cx, cy, 22, 5) + O(cx, cy, 380, 5, "none") + O(cx, cy, 405, 3, "none")
    out += "".join(O(cx + 392 * math.cos(math.radians(a)), cy + 392 * math.sin(math.radians(a)), 8, 3) for a in range(0, 360, 10))
    return out


COLOURING = [("Snowman Fun", c_snowman), ("Gingerbread Friend", c_gingerbread), ("Oh Christmas Tree", c_tree),
             ("Hang Your Stocking", c_stocking), ("Gingerbread House", c_house), ("Snowflake Mandala", c_mandala)]


def colour_page(title, fn):
    return (f'<div class="page"><div class="name">Name: ________________</div><div class="t" style="top:0.45in"><h1>{title}</h1></div>'
            f'<div class="box" style="top:1.15in;bottom:0.45in"><svg viewBox="0 0 800 1000" style="height:100%;max-width:100%">{fn()}</svg></div>'
            f'<div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


# ---------------- word search ----------------
def wordsearch(words, n, seed, diag):
    r = random.Random(seed)
    while True:
        g = [[""] * n for _ in range(n)]; placed = {}
        dirs = [(0, 1), (1, 0)] + ([(1, 1), (-1, 1)] if diag else [])
        ok = True
        for w in sorted(words, key=len, reverse=True):
            for _ in range(500):
                dr, dc = r.choice(dirs); row, col = r.randrange(n), r.randrange(n)
                cells = [(row + dr * i, col + dc * i) for i in range(len(w))]
                if all(0 <= a < n and 0 <= b < n and g[a][b] in ("", w[i]) for i, (a, b) in enumerate(cells)):
                    for i, (a, b) in enumerate(cells): g[a][b] = w[i]
                    placed[w] = cells; break
            else:
                ok = False; break
        if ok: break
        seed += 1; r = random.Random(seed)
    letters = "ABCDEFGHIJKLMNOPRSTUWY"
    for a in range(n):
        for b in range(n):
            if not g[a][b]: g[a][b] = r.choice(letters)
    return g, placed


def ws_svg(g, placed, key=False):
    n = len(g); c = 60; W = n * c
    out = f'<rect x="2" y="2" width="{W - 4}" height="{W - 4}" rx="24" fill="#fff" stroke="{GREEN}" stroke-width="6"/>'
    if key:
        for w, cells in placed.items():
            (a0, b0), (a1, b1) = cells[0], cells[-1]
            out += f'<line x1="{b0 * c + c / 2}" y1="{a0 * c + c / 2}" x2="{b1 * c + c / 2}" y2="{a1 * c + c / 2}" stroke="{GOLD}" stroke-width="44" stroke-linecap="round" opacity=".55"/>'
    for a in range(n):
        for b in range(n):
            out += f'<text x="{b * c + c / 2}" y="{a * c + c / 2 + 12}" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="34" fill="#222">{g[a][b]}</text>'
    return f'<svg viewBox="-10 -10 {W + 20} {W + 20}" style="width:100%">{out}</svg>'


WS = [("Word Search", "Easy · find the words across and down", ["SNOW", "STAR", "ELF", "BELLS", "GIFT", "TREE", "SANTA", "SLEIGH"], 10, 11, False),
      ("Word Search", "Tricky · words go across, down and diagonally", ["REINDEER", "SNOWMAN", "STOCKING", "MITTENS", "COOKIES", "CANDLE", "WREATH",
                                                                       "PRESENTS", "TINSEL", "CAROLS", "ANGEL", "HOLLY", "COCOA", "WINTER"], 13, 22, True)]


def ws_page(i, key=False):
    title, sub, words, n, seed, diag = WS[i]
    g, placed = wordsearch(words, n, seed, diag)
    wl = "".join(f'<span style="display:inline-flex;align-items:center;gap:0.08in;margin:0.05in 0.18in;font:600 12pt Poppins"><span style="width:0.2in;height:0.2in;border:2px solid {RED};border-radius:50%"></span>{w}</span>' for w in words)
    return (f'<div class="page"><div class="name">Name: ________________</div><div class="t"><h1 style="color:{GREEN}">{title}{" · Answers" if key else ""}</h1><p>{sub}</p></div>'
            f'<div style="position:absolute;left:{1.1 if n == 10 else .75}in;right:{1.1 if n == 10 else .75}in;top:1.45in">{ws_svg(g, placed, key)}</div>'
            f'<div style="position:absolute;left:0.6in;right:0.6in;bottom:0.6in;text-align:center">{wl}</div><div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>'), placed


# ---------------- mazes ----------------
def maze(w, h, seed):
    r = random.Random(seed); walls = {(x, y): {"N", "S", "E", "W"} for x in range(w) for y in range(h)}
    seen = {(0, 0)}; stack = [(0, 0)]; D_ = {"N": (0, -1, "S"), "S": (0, 1, "N"), "E": (1, 0, "W"), "W": (-1, 0, "E")}
    while stack:
        x, y = stack[-1]; opts = [(d, x + dx, y + dy, o) for d, (dx, dy, o) in D_.items() if (x + dx, y + dy) in walls and (x + dx, y + dy) not in seen]
        if not opts: stack.pop(); continue
        d, nx, ny, o = r.choice(opts); walls[(x, y)].discard(d); walls[(nx, ny)].discard(o); seen.add((nx, ny)); stack.append((nx, ny))
    # solve
    prev = {(0, 0): None}; q = [(0, 0)]
    while q:
        x, y = q.pop(0)
        for d, (dx, dy, _) in D_.items():
            if d not in walls[(x, y)] and (x + dx, y + dy) not in prev: prev[(x + dx, y + dy)] = (x, y); q.append((x + dx, y + dy))
    path = []; cur = (w - 1, h - 1)
    while cur: path.append(cur); cur = prev[cur]
    return walls, path[::-1]


def maze_svg(w, h, seed, key=False):
    walls, path = maze(w, h, seed); c = 50; out = ""
    for (x, y), ws in walls.items():
        X, Y = x * c, y * c
        if "N" in ws and not (x == 0 and y == 0): out += f"M{X},{Y} h{c} "
        if "W" in ws: out += f"M{X},{Y} v{c} "
        if "S" in ws and not (x == w - 1 and y == h - 1): out += f"M{X},{Y + c} h{c} "
        if "E" in ws: out += f"M{X + c},{Y} v{c} "
    sol = ""
    if key:
        pts = " ".join(f"{x * c + c / 2},{y * c + c / 2}" for x, y in path)
        sol = f'<polyline points="{c / 2},{-c} {pts} {(w - .5) * c},{(h + 1) * c}" fill="none" stroke="{RED}" stroke-width="{c * .32}" stroke-linecap="round" stroke-linejoin="round" opacity=".75"/>'
    W, H = w * c, h * c
    start = f'<g transform="translate({c / 2},{-c * 1.6}) scale({c / 55})">{penguin()}</g>'
    end = f'<g transform="translate({W - c / 2},{H + c * 1.9}) scale({c / 38})">{gift(0, 0, 1, RED, GOLD)}</g>'
    return (f'<svg viewBox="{-c * 1.5} {-c * 3.2} {W + 3 * c} {H + c * 6.6}" style="width:100%;height:100%">{sol}<path d="{out}" stroke="#2a3a5a" stroke-width="{max(3, c * .1):.0f}" stroke-linecap="round" fill="none"/>{start}{end}</svg>')


def penguin():
    return (f'<ellipse cx="0" cy="0" rx="42" ry="55" fill="#2a3a5a"/><ellipse cx="0" cy="10" rx="28" ry="42" fill="#fff"/>'
            f'<circle cx="-11" cy="-22" r="6" fill="#222"/><circle cx="11" cy="-22" r="6" fill="#222"/><polygon points="-9,-10 9,-10 0,2" fill="{GOLD}"/>'
            f'<path d="M-40,-38 Q0,-80 40,-38 Z" fill="{RED}"/><circle cx="0" cy="-66" r="10" fill="#fff"/><rect x="-44" y="-42" width="88" height="12" rx="6" fill="#fff"/>')


MZ = [("Help Pip the Penguin", "Find the way to the present · easy", 9, 11, 7), ("The Great Snow Maze", "Find the way to the present · tricky", 15, 19, 12)]


def maze_page(i, key=False):
    t, sub, w, h, seed = MZ[i]
    return (f'<div class="page"><div class="name">Name: ________________</div><div class="t"><h1 style="color:{BLUE}">{t}{" · Answer" if key else ""}</h1><p>{sub}</p></div>'
            f'<div class="box" style="top:1.45in;bottom:0.5in">{maze_svg(w, h, seed, key)}</div><div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


# ---------------- other pages ----------------
def lines(n, gap=0.42):
    return "".join(f'<div class="ln" style="height:{gap}in"></div>' for _ in range(n))


def santa_letter():
    deco = (f'<svg viewBox="0 0 800 120" style="width:100%">{holly(60, 60, 1.6, GREEN, RED)}{fstar(400, 60, 40, GOLD)}{holly(690, 60, 1.6, GREEN, RED)}'
            f'{bauble(250, 70, 30, RED, GOLD)}{bauble(550, 70, 30, BLUE, GOLD)}</svg>')
    tick = "".join(f'<span style="display:inline-flex;align-items:center;gap:0.08in;margin-right:0.3in;font:600 12pt Poppins"><span style="width:0.24in;height:0.24in;border:2.5px solid {GREEN};border-radius:0.05in"></span>{x}</span>' for x in ("Very good", "Good", "Mostly good!"))
    return (f'<div class="page" style="background:#fffaf2"><div style="position:absolute;inset:0.35in;border:8px solid transparent;border-image:repeating-linear-gradient(45deg,{RED} 0 14px,#fff 14px 28px) 8"></div>'
            f'<div style="position:absolute;left:0.8in;right:0.8in;top:0.6in">{deco}<div style="text-align:center;font:700 34pt Poppins;color:{RED};margin-top:0.08in">Dear Santa,</div>'
            f'<div style="font:12pt/2 Poppins;margin-top:0.15in">My name is ____________________ and I am ______ years old.<br>This year I have been: {tick}</div>'
            f'<div style="font:600 12pt Poppins;margin-top:0.18in;color:{GREEN}">Something kind I did this year:</div>{lines(2)}'
            f'<div style="font:600 12pt Poppins;margin-top:0.18in;color:{GREEN}">For Christmas I would love:</div>{lines(4)}'
            f'<div style="font:600 12pt Poppins;margin-top:0.18in;color:{GREEN}">A question for you, Santa:</div>{lines(2)}'
            f'<div style="font:12pt Poppins;margin-top:0.3in">Love from ______________________ &nbsp; P.S. I will leave you cookies!</div></div>'
            f'<div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def wish_list():
    boxes = "".join(f'<div style="border:3px dashed {[RED, GREEN, BLUE, GOLD][i % 4]};border-radius:0.2in;display:flex;flex-direction:column;padding:0.12in">'
                    f'<div style="flex:1"></div><div class="ln" style="height:0.35in"></div></div>' for i in range(6))
    return (f'<div class="page"><div class="t"><h1 style="color:{GREEN}">My Christmas Wish List</h1><p>Draw the things you wish for, then write their names underneath.</p></div>'
            f'<div style="position:absolute;left:0.6in;right:0.6in;top:1.55in;bottom:0.6in;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:0.22in">{boxes}</div>'
            f'<div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def count_page():
    items = [("baubles", lambda x, y: bauble(x, y + 8, 22, RED, GOLD), 7), ("stars", lambda x, y: fstar(x, y, 26, GOLD), 5), ("snowflakes", lambda x, y: fsnow(x, y, 21, BLUE), 9),
             ("presents", lambda x, y: gift(x, y + 4, .7, GREEN, RED), 4), ("trees", lambda x, y: ftree(x, y + 36, 64, GREEN), 6), ("mittens", lambda x, y: fmitten(x, y, .7, RED, "#f3e6d6"), 8)]
    rows = ""
    for i, (nm, fn, k) in enumerate(items):
        r = random.Random(i); art = "".join(fn(40 + j * 62 + r.uniform(-4, 4), 45 + r.uniform(-5, 5)) for j in range(k))
        rows += (f'<div style="display:flex;align-items:center;gap:0.2in;border-bottom:2px dotted #ddd;padding:0.2in 0"><svg viewBox="0 0 600 95" style="width:5.4in;flex:none">{art}</svg>'
                 f'<div style="font:500 10pt Poppins;color:#666;width:0.9in">How many {nm}?</div><div style="width:0.75in;height:0.6in;flex:none;border:3px solid {GREEN};border-radius:0.14in"></div></div>')
    return (f'<div class="page"><div class="name">Name: ________________</div><div class="t"><h1 style="color:{RED}">Count &amp; Write</h1><p>Count each row and write the number in the box. Then colour the pictures!</p></div>'
            f'<div style="position:absolute;left:0.5in;right:0.5in;top:1.55in">{rows}</div><div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def dots_page():
    def ring(n, cx, cy, ro, ri, start=-90):
        return [(cx + (ro if i % 2 == 0 else ri) * math.cos(math.radians(start + i * 180 / (n / 2))), cy + (ro if i % 2 == 0 else ri) * math.sin(math.radians(start + i * 180 / (n / 2)))) for i in range(n)]
    st = ring(10, 400, 260, 230, 95)
    st2 = []
    for i in range(10):
        a, b = st[i], st[(i + 1) % 10]; st2 += [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)]
    tr = [(400 + (x - 600) * 1.35, 560 + (y - 60) * 1.0) for x, y in [(600, 60), (680, 160), (650, 160), (730, 260), (690, 260), (770, 370), (630, 370), (630, 430), (570, 430), (570, 370), (430, 370), (510, 260), (470, 260), (550, 160), (520, 160)]]
    def dots(pts, start):
        o = ""
        for i, (x, y) in enumerate(pts):
            o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#222"/><text x="{x + 10:.0f}" y="{y - 10:.0f}" font-family="Poppins" font-weight="600" font-size="24" fill="#d64545">{start + i}</text>'
        return o
    return (f'<div class="page"><div class="name">Name: ________________</div><div class="t"><h1 style="color:{GOLD}">Dot to Dot</h1><p>Join the dots in order to finish each picture, then colour them in.</p></div>'
            f'<div class="box" style="top:1.5in;bottom:0.5in"><svg viewBox="0 0 800 1000" style="height:100%">{dots(st2, 1)}{dots(tr, 1)}'
            f'<text x="400" y="525" text-anchor="middle" font-family="Poppins" font-size="20" fill="#aaa">Star: 1 to 20, then back to 1</text><text x="400" y="990" text-anchor="middle" font-family="Poppins" font-size="20" fill="#aaa">Tree: 1 to 15, then back to 1</text></svg></div>'
            f'<div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def decorate_tree():
    t = U(poly("400,120 590,400 210,400"), poly("400,260 650,580 150,580"), poly("400,410 720,800 80,800"), rect(355, 795, 90, 90, 6)) + ostar(400, 105, 60, 6)
    return (f'<div class="page"><div class="name">Name: ________________</div><div class="t"><h1 style="color:{GREEN}">Decorate the Tree</h1><p>Draw baubles, lights, garlands and presents. Make it the best tree ever!</p></div>'
            f'<div class="box" style="top:1.4in"><svg viewBox="0 0 800 1000" style="height:100%">{t}</svg></div><div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def sweater():
    sw = U(poly("250,170 330,140 470,140 550,170 610,240 720,640 630,670 560,400 560,880 240,880 240,400 170,670 80,640 190,240"))
    sw += L("M330,140 Q400,215 470,140", 6) + L("M345,148 Q400,195 455,148", 4) + L("M240,830 L560,830", 5) + L("M100,590 L190,620 M700,590 L610,620", 5)
    sw += "".join(L(f"M{x},835 L{x},878", 3) for x in range(260, 560, 22))
    return (f'<div class="page"><div class="name">Name: ________________</div><div class="t"><h1 style="color:{RED}">Design a Christmas Sweater</h1><p>Add stripes, snowflakes, reindeer or anything you like.</p></div>'
            f'<div class="box" style="top:1.4in"><svg viewBox="40 100 720 820" style="height:100%">{sw}</svg></div><div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def ttt():
    g = "".join(f'<div style="display:flex;flex-direction:column;align-items:center"><svg viewBox="0 0 300 300" style="width:3.0in">'
                f'<path d="M100,10 V290 M200,10 V290 M10,100 H290 M10,200 H290" stroke="{[RED, GREEN, BLUE, GOLD][i]}" stroke-width="10" stroke-linecap="round"/></svg>'
                f'<div style="font:500 10pt Poppins;color:#888;margin-top:0.08in">Player 1 ______ &nbsp; Player 2 ______</div></div>' for i in range(4))
    keys = f'<svg viewBox="0 0 400 90" style="width:3.2in;margin:0 auto">{fstar(80, 45, 38, GOLD)}<text x="135" y="58" font-family="Poppins" font-size="30" font-weight="700">vs</text>{fsnow(250, 45, 36, BLUE)}</svg>'
    return (f'<div class="page"><div class="t"><h1 style="color:{BLUE}">Christmas Tic-Tac-Toe</h1><p>Play with stars and snowflakes instead of X and O. Three in a row wins!</p></div>'
            f'<div style="position:absolute;left:0;right:0;top:1.45in">{keys}</div>'
            f'<div style="position:absolute;left:0.6in;right:0.6in;top:2.6in;display:grid;grid-template-columns:1fr 1fr;gap:0.4in 0.3in">{g}</div><div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def countdown():
    cells = ""
    for d in range(1, 25):
        r = 34
        cells += (f'<div style="display:flex;justify-content:center"><svg viewBox="-50 -70 100 125" style="width:1.25in">'
                  f'<line x1="0" y1="-66" x2="0" y2="-44" stroke="#999" stroke-width="3"/><rect x="-11" y="-48" width="22" height="12" rx="3" fill="#fff" stroke="{K}" stroke-width="4"/>'
                  f'<circle r="{r + 4}" cy="2" fill="#fff" stroke="{K}" stroke-width="5"/><path d="M-34,-8 Q0,8 34,-8 M-34,14 Q0,30 34,14" stroke="{K}" stroke-width="3" fill="none"/>'
                  f'<text y="12" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="30" fill="#222" stroke="#fff" stroke-width="6" paint-order="stroke">{d}</text></svg></div>')
    return (f'<div class="page"><div class="t"><h1 style="color:{RED}">Countdown to Christmas</h1><p>Colour in one bauble every day from 1 December. When they are all done, it is Christmas Eve!</p></div>'
            f'<div style="position:absolute;left:0.5in;right:0.5in;top:1.6in;bottom:0.6in;display:grid;grid-template-columns:repeat(5,1fr);align-content:space-evenly">{cells}'
            f'<div style="display:flex;justify-content:center;align-items:center"><svg viewBox="0 0 100 100" style="width:1.05in">{fstar(50, 50, 44, GOLD)}</svg></div></div>'
            f'<div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def certificate():
    return (f'<div class="page" style="background:#fffaf2"><div style="position:absolute;inset:0.4in;border:6px double {GOLD};border-radius:0.3in"></div>'
            f'<svg viewBox="0 0 800 180" style="position:absolute;left:0.9in;right:0.9in;top:0.75in;width:calc(100% - 1.8in)">{holly(90, 90, 1.8, GREEN, RED)}{fstar(400, 90, 80, GOLD)}{holly(690, 90, 1.8, GREEN, RED)}</svg>'
            f'<div style="position:absolute;left:0.8in;right:0.8in;top:3.0in;text-align:center">'
            f'<div style="font:700 12pt Poppins;letter-spacing:.3em;color:{GREEN}">OFFICIAL</div>'
            f'<div style="font-family:\'TeX Gyre Chorus\',Lora,serif;font-size:60pt;line-height:1;color:{RED}">Nice List</div>'
            f'<div style="font:700 24pt Poppins;margin-top:0.04in">Certificate</div>'
            f'<div style="font:12pt Poppins;color:#555;margin-top:0.45in">This certifies that</div><div style="border-bottom:2px solid #222;height:0.6in;width:5in;margin:0 auto"></div>'
            f'<div style="font:12pt/1.6 Poppins;color:#555;margin-top:0.25in">has been kind, helpful and full of Christmas cheer<br>and is officially on the Nice List this year.</div>'
            f'<div style="display:flex;justify-content:space-between;margin-top:0.8in;font:10pt Poppins;color:#555"><div style="width:2.6in;border-top:1.5px solid #222;padding-top:0.06in">Head Elf</div>'
            f'<div style="width:2.6in;border-top:1.5px solid #222;padding-top:0.06in">Date</div></div></div><div class="foot">Purl &amp; Paper · Kids Christmas Activity Pack</div></div>')


def cover():
    art = (bauble(120, 110, 52, RED, GOLD) + fstar(270, 90, 44, GOLD) + ftree(420, 210, 170, GREEN) + gift(580, 120, 1.4, BLUE, GOLD) + fsnow(720, 100, 50, BLUE))
    thumbs = "".join(f'<div style="background:#fff;border-radius:0.12in;box-shadow:0 3px 10px rgba(0,0,0,.12);padding:0.08in;display:flex;flex-direction:column;align-items:center">'
                     f'<svg viewBox="0 0 800 1000" style="width:100%">{fn()}</svg><div style="font:600 8pt Poppins;margin-top:0.04in">{t}</div></div>' for t, fn in COLOURING[:3])
    inside = ["6 colouring pages", "2 word searches", "2 mazes", "Letter to Santa", "Wish list", "Count & write", "Dot to dot", "Decorate the tree",
              "Sweater design", "Tic-tac-toe", "Countdown", "Nice List certificate"]
    chips = "".join(f'<span style="display:inline-block;margin:0.04in;padding:0.05in 0.14in;border-radius:99px;font:600 9pt Poppins;color:#fff;background:{[RED, GREEN, BLUE, GOLD][i % 4]}">{x}</span>' for i, x in enumerate(inside))
    return (f'<div class="page" style="background:#fff6ec"><svg viewBox="0 0 840 230" style="position:absolute;left:0.6in;right:0.6in;top:0.5in;width:calc(100% - 1.2in)">{art}</svg>'
            f'<div style="position:absolute;left:0;right:0;top:3.0in;text-align:center"><div style="font:700 15pt Poppins;letter-spacing:.25em;color:{GREEN}">KIDS</div>'
            f'<div style="font:700 44pt/1 Poppins;color:{RED}">Christmas<br>Activity Pack</div><div style="font:12pt Poppins;color:#555;margin-top:0.12in">24 printable pages for ages 4 to 9 · answer keys included</div></div>'
            f'<div style="position:absolute;left:1in;right:1in;top:5.55in;display:grid;grid-template-columns:repeat(3,1fr);gap:0.2in">{thumbs}</div>'
            f'<div style="position:absolute;left:0.8in;right:0.8in;bottom:0.6in;text-align:center">{chips}</div></div>')


def answers():
    p1, _ = ws_page(0, True); p2, _ = ws_page(1, True)
    return [p1, p2, maze_page(0, True), maze_page(1, True)]


def build():
    pages = [cover(), santa_letter(), wish_list()] + [colour_page(t, fn) for t, fn in COLOURING]
    pages += [ws_page(0)[0], ws_page(1)[0], maze_page(0), maze_page(1), count_page(), dots_page(), decorate_tree(), sweater(), ttt(), countdown(), certificate()]
    pages += answers()
    return CSS, pages


if __name__ == "__main__":
    out = sys.argv[1]; name = "kids-christmas-activity-pack"
    css, pages = build()
    for size in ("letter", "a4"):
        render(css, pages, size, f"{out}/{name}-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print(name, len(pages), "pages")
