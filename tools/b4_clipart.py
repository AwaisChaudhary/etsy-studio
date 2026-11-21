"""Nordic Folk Christmas clipart (batch 4, lane f). Every element is original vector art drawn here as SVG
(1000 x 1000 viewBox). Exports transparent PNG (3000 px), SVG, 6 seamless 12x12 in patterns and a catalog PDF.
Usage: python3 b4_clipart.py <out_dir>"""
import math, pathlib, random, sys, zipfile, io
sys.path.insert(0, str(pathlib.Path(__file__).parent))

R, DR, G, LG, C, M, P, N, BR, W = "#B8323A", "#8E2430", "#2E5E4E", "#7FA68C", "#F4EAD5", "#E0A43A", "#EBA9A2", "#1F3047", "#8A5A3B", "#FFFDF8"
SK = "#3A2A26"  # soft outline for details


def poly(pts, fill, extra=""):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" {extra}/>'


def circ(x, y, r, fill, extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" {extra}/>'


def starpts(cx, cy, r1, r2, n, rot=-90):
    return [(cx + (r1 if i % 2 == 0 else r2) * math.cos(math.radians(rot + i * 180 / n)),
             cy + (r1 if i % 2 == 0 else r2) * math.sin(math.radians(rot + i * 180 / n))) for i in range(2 * n)]


def heart_path(cx, cy, s):
    # heart centred at cx,cy, width about 2s
    return (f"M{cx},{cy + s * .95} C{cx - s * 1.25},{cy + s * .15} {cx - s * 1.05},{cy - s * .95} {cx},{cy - s * .45} "
            f"C{cx + s * 1.05},{cy - s * .95} {cx + s * 1.25},{cy + s * .15} {cx},{cy + s * .95}Z")


def heart(cx, cy, s, fill, extra=""):
    return f'<path d="{heart_path(cx, cy, s)}" fill="{fill}" {extra}/>'


def leaf(x, y, l, w, ang, fill):
    return (f'<path d="M0,0 C{l * .3},{-w} {l * .7},{-w} {l},0 C{l * .7},{w} {l * .3},{w} 0,0Z" fill="{fill}" '
            f'transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})"/>')


def dots_ring(cx, cy, r, n, dr, fill):
    return "".join(circ(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n), dr, fill) for i in range(n))


def zig(x1, x2, y, h, n, col, sw=10):
    step = (x2 - x1) / n
    pts = " ".join(f"{x1 + i * step:.1f},{y + (h if i % 2 else -h):.1f}" for i in range(n + 1))
    return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'


def stitch(d, col, sw=7):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="18 14" stroke-linecap="round"/>'


def folk_flower(cx, cy, s, petal, centre, inner=None):
    out = ""
    for k in range(8):
        a = k * 45
        out += f'<ellipse cx="0" cy="{-s * .55:.1f}" rx="{s * .22:.1f}" ry="{s * .42:.1f}" fill="{petal}" transform="translate({cx},{cy}) rotate({a})"/>'
    out += circ(cx, cy, s * .32, centre)
    if inner: out += dots_ring(cx, cy, s * .17, 6, s * .05, inner)
    return out


def snowflake_folk(cx, cy, r, col, variant=0):
    out = ""
    for k in range(6):
        a = k * 60
        g = f'<g transform="translate({cx},{cy}) rotate({a})">'
        g += f'<rect x="{-r * .035:.1f}" y="{-r:.1f}" width="{r * .07:.1f}" height="{r:.1f}" rx="{r * .03:.1f}" fill="{col}"/>'
        if variant == 0:
            for f in (.45, .7):
                g += f'<path d="M0,{-r * f:.1f} l{-r * .2:.1f},{-r * .2:.1f} M0,{-r * f:.1f} l{r * .2:.1f},{-r * .2:.1f}" stroke="{col}" stroke-width="{r * .06:.1f}" stroke-linecap="round" fill="none"/>'
            g += poly([(0, -r * 1.08), (r * .09, -r * .96), (0, -r * .84), (-r * .09, -r * .96)], col)
        elif variant == 1:
            g += poly([(0, -r * .62), (r * .16, -r * .44), (0, -r * .26), (-r * .16, -r * .44)], col)
            g += circ(0, -r * 1.02, r * .08, col)
            g += f'<path d="M0,{-r * .8:.1f} l{-r * .16:.1f},{-r * .12:.1f} M0,{-r * .8:.1f} l{r * .16:.1f},{-r * .12:.1f}" stroke="{col}" stroke-width="{r * .055:.1f}" stroke-linecap="round" fill="none"/>'
        else:
            g += heart(0, -r * .82, r * .16, col)
            g += f'<path d="M0,{-r * .45:.1f} l{-r * .22:.1f},{-r * .1:.1f} M0,{-r * .45:.1f} l{r * .22:.1f},{-r * .1:.1f}" stroke="{col}" stroke-width="{r * .06:.1f}" stroke-linecap="round" fill="none"/>'
        out += g + "</g>"
    hole = circ(cx, cy, r * .12, col) if variant != 1 else poly(starpts(cx, cy, r * .2, r * .1, 6), col)
    return out + hole


# ---------------- elements ----------------
def e_tree_tiered(a=G, b=LG, orn=R):
    out = f'<rect x="465" y="800" width="70" height="110" rx="10" fill="{BR}"/>'
    tiers = [(430, 820, 380), (290, 640, 300), (180, 470, 220)]
    for i, (top, base, hw) in enumerate(tiers):
        sc = ""
        n = 7
        for k in range(n):
            x0 = 500 - hw + k * 2 * hw / n
            sc += f" Q{x0 + hw / n:.1f},{base + 50:.1f} {x0 + 2 * hw / n:.1f},{base:.1f}"
        out += f'<path d="M500,{top - 60 - i * 10} L{500 + hw},{base} {sc.replace("Q", "Q", 1)} Z" fill="{a if i % 2 == 0 else b}"/>' if False else ""
        pts = f"M500,{top} L{500 + hw},{base}"
        x = 500 + hw
        for k in range(n):
            x1 = x - 2 * hw / n
            pts += f" Q{(x + x1) / 2:.1f},{base + 46:.1f} {x1:.1f},{base:.1f}"
            x = x1
        out += f'<path d="{pts} Z" fill="{a if i != 1 else "#3B7360"}"/>'
        out += zig(500 - hw * .62, 500 + hw * .62, base - 70, 14, 10, C, 9)
    for (x, y, c) in [(400, 700, orn), (610, 735, M), (520, 560, orn), (420, 470, M), (580, 420, orn), (470, 330, C)]:
        out += circ(x, y, 22, c) + circ(x - 7, y - 7, 6, "#ffffff", 'opacity=".6"')
    out += poly(starpts(500, 150, 74, 32, 5), M)
    return out


def e_tree_folk():
    out = f'<path d="M500,140 L500,880" stroke="{BR}" stroke-width="26" stroke-linecap="round"/>'
    out += f'<path d="M380,880 Q500,840 620,880" stroke="{BR}" stroke-width="22" fill="none" stroke-linecap="round"/>'
    for i in range(6):
        y = 250 + i * 105
        l = 120 + i * 38
        for side in (-1, 1):
            ang = -25 if side == 1 else 205
            out += f'<path d="M500,{y + 30} Q{500 + side * l * .5:.0f},{y - 10} {500 + side * l:.0f},{y - 40}" stroke="{G}" stroke-width="14" fill="none" stroke-linecap="round"/>'
            for k in range(3):
                t = .35 + k * .3
                bx, by = 500 + side * l * t, y + 30 - 70 * t
                out += leaf(bx, by, 70, 22, -70 if side == 1 else -110, LG if (k + i) % 2 else G)
            out += heart(500 + side * l, y - 52, 26, R if i % 2 == 0 else M)
    out += heart(500, 120, 52, R) + heart(500, 124, 24, C)
    return out


def e_tree_cone():
    out = f'<rect x="470" y="820" width="60" height="90" rx="8" fill="{BR}"/>'
    out += f'<path d="M500,110 C540,300 690,640 760,830 L240,830 C310,640 460,300 500,110Z" fill="{G}"/>'
    clip = "M500,110 C540,300 690,640 760,830 L240,830 C310,640 460,300 500,110Z"
    out += f'<clipPath id="cone"><path d="{clip}"/></clipPath><g clip-path="url(#cone)">'
    for i, y in enumerate([330, 470, 610, 750]):
        out += f'<path d="M150,{y + 60} Q500,{y - 40} 850,{y + 60}" stroke="{[C, R, M, C][i]}" stroke-width="20" fill="none"/>'
        out += "".join(circ(240 + k * 80, y + 40 - 70 * math.sin(math.pi * (240 + k * 80 - 150) / 700) + 26, 9, C if i % 2 else R) for k in range(8))
    out += "</g>"
    out += poly(starpts(500, 100, 62, 26, 5), M)
    return out


def e_star8(a=R, b=C):
    out = poly(starpts(500, 500, 400, 230, 8, -90), a)
    out += poly(starpts(500, 500, 300, 175, 8, -90), b)
    out += poly(starpts(500, 500, 210, 120, 8, -67.5), a)
    out += circ(500, 500, 70, b) + circ(500, 500, 30, a)
    for k in range(8):
        ang = math.radians(-90 + k * 45)
        out += circ(500 + 345 * math.cos(ang), 500 + 345 * math.sin(ang), 13, b)
    return out


def e_star_straw():
    out = ""
    for k in range(16):
        l = 420 if k % 2 == 0 else 300
        out += f'<rect x="-14" y="{-l}" width="28" height="{2 * l}" rx="12" fill="{M if k % 4 else "#C98E2A"}" transform="translate(500,500) rotate({k * 22.5})"/>'
    for k in range(8):
        ang = math.radians(k * 45 - 90); x, y = 500 + 175 * math.cos(ang), 500 + 175 * math.sin(ang)
        out += f'<rect x="{x - 26:.1f}" y="{y - 8:.1f}" width="52" height="16" rx="6" fill="{R}" transform="rotate({k * 45} {x:.1f} {y:.1f})"/>'
    out += circ(500, 500, 64, R) + circ(500, 500, 26, C)
    return out


def e_heart_folk():
    out = heart(500, 520, 410, R)
    out += f'<path d="{heart_path(500, 520, 330)}" fill="none" stroke="{C}" stroke-width="10" stroke-dasharray="20 16"/>'
    out += folk_flower(500, 470, 150, C, M, R)
    for side in (-1, 1):
        out += leaf(500 + side * 40, 640, 170, 40, 90 - side * 55, G)
        out += circ(500 + side * 230, 330, 22, C) + circ(500 + side * 180, 640, 16, C)
    return out


def e_heart_woven():
    """Danish woven heart: a square with two half-circle lobes, turned 45 degrees, red and cream strips woven in a checker."""
    x0, y0, L = 330, 350, 340; r = L / 2; s4 = L / 4
    shape = (f"M{x0},{y0} A{r},{r} 0 0 1 {x0 + L},{y0} L{x0 + L},{y0 + L} L{x0},{y0 + L} A{r},{r} 0 0 1 {x0},{y0}Z")
    out = f'<g transform="rotate(45 {x0 + r} {y0 + r})"><clipPath id="wvh"><path d="{shape}"/></clipPath><g clip-path="url(#wvh)">'
    out += f'<rect x="{x0 - L}" y="{y0 - L}" width="{3 * L}" height="{3 * L}" fill="{C}"/>'
    out += f'<rect x="{x0}" y="{y0 - L}" width="{L}" height="{L}" fill="{R}"/>'
    for i in range(4):
        for j in range(4):
            if (i + j) % 2 == 0:
                out += f'<rect x="{x0 + i * s4:.1f}" y="{y0 + j * s4:.1f}" width="{s4:.1f}" height="{s4:.1f}" fill="{R}"/>'
    for i in range(1, 4):
        out += f'<line x1="{x0 + i * s4:.1f}" y1="{y0 - L}" x2="{x0 + i * s4:.1f}" y2="{y0}" stroke="{DR}" stroke-width="6"/>'
        out += f'<line x1="{x0 - L}" y1="{y0 + i * s4:.1f}" x2="{x0}" y2="{y0 + i * s4:.1f}" stroke="#E2D4B8" stroke-width="6"/>'
    out += f'</g><path d="{shape}" fill="none" stroke="{DR}" stroke-width="10"/></g>'
    out += f'<path d="M500,{y0 - 10 - 0} C420,90 580,90 500,{y0 - 10}" fill="none" stroke="{R}" stroke-width="16" stroke-linecap="round" transform="translate(0,-150)"/>'
    return out


def e_bird(body=R, wing=C, accent=M):
    out = f'<path d="M640,520 C720,430 820,380 900,330 C880,430 840,520 760,600Z" fill="{G}"/>'
    out += f'<path d="M650,560 C740,520 830,520 900,500 C850,580 780,640 700,650Z" fill="{LG}"/>'
    out += f'<path d="M300,420 C300,280 460,230 540,300 C620,360 700,470 690,600 C680,720 560,780 430,770 C300,760 220,660 240,560 C250,500 280,460 300,420Z" fill="{body}"/>'
    out += f'<path d="M400,500 C470,450 600,470 640,560 C600,660 480,690 400,640 C430,600 430,550 400,500Z" fill="{wing}"/>'
    out += f'<path d="M430,540 C500,520 570,540 600,580" stroke="{body}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    out += f'<path d="M440,600 C500,590 560,600 590,620" stroke="{accent}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    out += poly([(300, 380), (215, 405), (300, 430)], accent)
    out += circ(355, 385, 18, SK) + circ(361, 379, 6, "#fff")
    out += circ(330, 460, 22, P, 'opacity=".8"')
    out += f'<path d="M430,770 L415,850 M520,770 L535,850" stroke="{BR}" stroke-width="12" stroke-linecap="round"/>'
    out += f'<path d="M300,860 Q500,830 700,860" stroke="{BR}" stroke-width="18" fill="none" stroke-linecap="round"/>'
    out += leaf(660, 850, 90, 26, -30, G) + leaf(280, 860, 80, 24, 200, LG) + circ(720, 820, 16, R) + circ(745, 840, 14, R)
    return out


def gnome(hat=R, beard=C, coat=G, extra=""):
    out = f'<ellipse cx="500" cy="900" rx="250" ry="28" fill="{SK}" opacity=".12"/>'
    out += f'<path d="M300,880 C290,760 330,640 380,600 L620,600 C670,640 710,760 700,880Z" fill="{coat}"/>'
    out += f'<ellipse cx="410" cy="885" rx="80" ry="38" fill="{BR}"/><ellipse cx="590" cy="885" rx="80" ry="38" fill="{BR}"/>'
    out += f'<path d="M330,520 C320,700 420,800 500,830 C580,800 680,700 670,520Z" fill="{beard}"/>'
    for k in range(5):
        out += f'<path d="M{380 + k * 60},{560 + (k % 2) * 30} q30,90 0,170" stroke="#E2D4B8" stroke-width="9" fill="none" stroke-linecap="round"/>'
    out += f'<path d="M500,90 C560,150 640,300 700,520 L300,520 C330,360 420,200 500,90Z" fill="{hat}"/>'
    out += f'<path d="M500,90 C440,80 380,110 360,170" stroke="{hat}" stroke-width="34" fill="none" stroke-linecap="round"/>'
    out += circ(355, 182, 30, beard)
    out += f'<rect x="280" y="490" width="440" height="70" rx="35" fill="{beard}"/>'
    out += f'<path d="M300,525 L700,525" stroke="#E2D4B8" stroke-width="8" stroke-dasharray="14 18" stroke-linecap="round"/>'
    out += f'<ellipse cx="500" cy="600" rx="70" ry="62" fill="#E79A86"/><ellipse cx="478" cy="580" rx="20" ry="14" fill="#fff" opacity=".5"/>'
    return out + extra


def e_gnome1(): return gnome(R, C, G, "".join(circ(x, y, 14, C) for x, y in [(470, 260), (540, 330), (450, 400), (600, 440), (520, 200)]))


def e_gnome2():
    ex = "".join(poly(starpts(x, y, 26, 11, 5), M) for x, y in [(500, 250), (440, 380), (590, 400)])
    return gnome(N, C, R, ex)


def e_gnome3():
    ex = zig(380, 640, 420, 20, 8, C, 12) + zig(410, 610, 330, 18, 6, M, 10)
    ex += heart(500, 720, 80, R) + heart(500, 722, 34, C)
    return gnome(G, C, "#C46A5A", ex)


def e_mushroom(cap=R):
    out = f'<path d="M420,560 C410,700 400,800 380,860 L620,860 C600,800 590,700 580,560Z" fill="{C}"/>'
    out += f'<path d="M405,650 C450,690 550,690 595,650 L600,690 C550,730 450,730 400,690Z" fill="#E2D4B8"/>'
    out += f'<path d="M150,560 C160,330 330,190 500,190 C670,190 840,330 850,560 C700,600 300,600 150,560Z" fill="{cap}"/>'
    for x, y, r in [(300, 420, 34), (420, 300, 30), (560, 280, 26), (680, 380, 36), (500, 450, 40), (360, 520, 22), (640, 510, 24), (760, 500, 18), (240, 520, 18)]:
        out += circ(x, y, r, W)
    out += f'<path d="M260,870 Q500,840 740,870" stroke="{LG}" stroke-width="16" fill="none" stroke-linecap="round"/>'
    out += leaf(300, 865, 80, 22, 210, G) + leaf(690, 862, 80, 22, -40, G)
    return out


def e_mushrooms_pair():
    out = '<g transform="translate(-20,90) scale(.8)">' + e_mushroom(R) + "</g>"
    out += '<g transform="translate(470,360) scale(.52)">' + e_mushroom("#D2563D") + "</g>"
    return out


def e_ginger_house():
    out = f'<rect x="250" y="470" width="500" height="400" fill="#B8743F"/>'
    out += poly([(190, 500), (500, 190), (810, 500)], "#9C5A2D")
    sc = "M190,500"
    for k in range(10):
        sc += f" q31,40 62,0"
    out += f'<path d="{sc} L810,500 L500,190Z" fill="none"/>'
    out += f'<path d="M190,500 L500,190 L810,500" stroke="{W}" stroke-width="34" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
    out += "".join(f'<path d="M{200 + k * 60},{512} q30,48 60,0" stroke="{W}" stroke-width="16" fill="none" stroke-linecap="round"/>' for k in range(10))
    out += f'<rect x="620" y="250" width="80" height="150" fill="#9C5A2D"/><rect x="606" y="236" width="108" height="34" rx="12" fill="{W}"/>'
    out += f'<path d="M430,870 L430,700 A70,70 0 0 1 570,700 L570,870Z" fill="{R}"/>' + circ(548, 790, 9, M)
    for x in (290, 620):
        out += f'<rect x="{x}" y="590" width="90" height="90" rx="10" fill="{M}"/><path d="M{x + 45},590 v90 M{x},635 h90" stroke="#9C5A2D" stroke-width="8"/>'
        out += f'<path d="M{x - 8},690 h106" stroke="{W}" stroke-width="12" stroke-linecap="round"/>'
    out += circ(500, 380, 52, W) + circ(500, 380, 34, R)
    out += "".join(circ(x, 880, 22, c) for x, c in [(260, R), (330, G), (670, R), (740, G)])
    out += f'<path d="M240,880 H760" stroke="{W}" stroke-width="12" stroke-linecap="round" opacity=".0"/>'
    for x, c in [(300, R), (360, G), (640, G), (700, R)]:
        out += circ(x, 520 + 18, 12, c)
    return out


def e_ginger_man():
    col = "#B8743F"
    out = f'<path d="M500,140 a120,120 0 1 1 -0.1,0Z" fill="{col}"/>'
    out += f'<path d="M500,330 C600,330 640,370 640,430 L800,430 C860,430 860,540 800,540 L650,540 L690,780 C700,850 610,870 590,810 L520,650 L480,650 L410,810 C390,870 300,850 310,780 L350,540 L200,540 C140,540 140,430 200,430 L360,430 C360,370 400,330 500,330Z" fill="{col}"/>'
    out += circ(460, 240, 16, SK) + circ(540, 240, 16, SK)
    out += f'<path d="M455,300 Q500,335 545,300" stroke="{SK}" stroke-width="12" fill="none" stroke-linecap="round"/>'
    out += circ(440, 285, 18, P, 'opacity=".9"') + circ(560, 285, 18, P, 'opacity=".9"')
    for path in ["M190,470 q20,30 40,0 q20,30 40,0", "M730,470 q20,30 40,0 q20,30 40,0", "M330,790 q20,30 40,0", "M630,790 q20,30 40,0"]:
        out += f'<path d="{path}" stroke="{W}" stroke-width="13" fill="none" stroke-linecap="round"/>'
    out += circ(500, 450, 20, R) + circ(500, 520, 20, G) + circ(500, 590, 20, R)
    out += f'<path d="M430,375 L500,410 L570,375 L570,435 L500,400 L430,435Z" fill="{R}"/>' + circ(500, 405, 16, DR)
    return out


def e_cottage():
    out = f'<rect x="250" y="480" width="500" height="380" fill="{R}"/>'
    out += poly([(200, 500), (500, 230), (800, 500)], "#5B3A2E")
    out += f'<path d="M180,510 C260,500 300,420 500,215 C700,420 740,500 820,510 C780,540 740,500 700,530 C660,500 620,540 580,515 C540,545 470,500 430,530 C390,500 340,545 300,515 C260,540 220,530 180,510Z" fill="{W}"/>'
    out += f'<rect x="610" y="270" width="70" height="140" fill="#5B3A2E"/><path d="M600,275 h90 q-10,-26 -45,-26 q-35,0 -45,26Z" fill="{W}"/>'
    out += "".join(circ(650 + k * 30, 220 - k * 55, 18 + k * 6, "#D9D2C5", 'opacity=".8"') for k in range(3))
    out += f'<rect x="440" y="690" width="120" height="170" rx="8" fill="{G}"/>' + circ(535, 780, 9, M)
    for x in (300, 600):
        out += f'<rect x="{x}" y="580" width="100" height="90" fill="{M}"/><path d="M{x + 50},580 v90 M{x},625 h100" stroke="{R}" stroke-width="9"/>'
        out += f'<rect x="{x - 10}" y="668" width="120" height="16" rx="6" fill="{W}"/>'
    out += f'<path d="M150,870 C300,840 700,840 850,870 L850,900 L150,900Z" fill="{W}"/>'
    out += heart(500, 400, 34, W)
    return out


def nordic_band(x1, x2, y, col, motif="star"):
    out = ""
    n = int((x2 - x1) // 70)
    for k in range(n):
        cx = x1 + 35 + k * (x2 - x1) / n
        if motif == "star": out += poly(starpts(cx, y, 24, 10, 4, -90), col)
        elif motif == "heart": out += heart(cx, y, 20, col)
        else: out += poly([(cx, y - 22), (cx + 22, y), (cx, y + 22), (cx - 22, y)], col)
    return out


def e_mitten(body=R, band=C, motif="star"):
    d = "M330,250 C330,170 380,130 470,130 C570,130 620,180 620,260 L630,470 C670,430 740,420 770,470 C800,520 760,580 700,640 L640,700 L360,700 C340,560 330,400 330,250Z"
    out = f'<path d="{d}" fill="{body}"/>'
    out += f'<clipPath id="mt{motif}"><path d="{d}"/></clipPath><g clip-path="url(#mt{motif})">'
    out += f'<rect x="300" y="340" width="500" height="110" fill="{band}"/>' + nordic_band(310, 650, 395, body, motif)
    out += zig(300, 800, 300, 12, 14, band, 8) + zig(300, 800, 490, 12, 14, band, 8)
    out += "</g>"
    out += f'<rect x="330" y="680" width="330" height="190" rx="30" fill="{band}"/>'
    for k in range(7):
        out += f'<rect x="{350 + k * 44}" y="700" width="20" height="150" rx="10" fill="{body}" opacity=".35"/>'
    out += f'<path d="M495,870 C495,920 560,930 600,900" stroke="{M}" stroke-width="14" fill="none" stroke-linecap="round"/>'
    return out


def e_mitten2(): return e_mitten(G, C, "heart")


def e_stocking(body=R, cuff=W, motif="star"):
    d = "M380,250 L620,250 L620,600 C620,700 560,780 440,820 C330,860 230,820 220,740 C210,660 280,620 380,580Z"
    out = f'<path d="{d}" fill="{body}"/>'
    out += f'<clipPath id="st{motif}"><path d="{d}"/></clipPath><g clip-path="url(#st{motif})">'
    out += f'<rect x="200" y="420" width="450" height="100" fill="{C}"/>' + nordic_band(390, 620, 470, body, motif)
    out += f'<path d="M200,700 C300,640 400,700 400,840 L200,860Z" fill="{C}"/>'
    out += f'<path d="M540,250 L640,250 L640,330 L540,330Z" fill="none"/>'
    out += zig(200, 650, 380, 10, 12, C, 8) + zig(200, 650, 560, 10, 12, C, 8) + "</g>"
    out += f'<rect x="350" y="130" width="300" height="140" rx="26" fill="{cuff}"/>'
    out += "".join(circ(390 + k * 55, 200, 10, P if body == R else LG) for k in range(5))
    out += f'<path d="M620,150 C700,90 760,150 700,190" stroke="{M}" stroke-width="14" fill="none" stroke-linecap="round"/>'
    return out


def e_stocking2(): return e_stocking(G, C, "heart")


def e_sweater():
    d = "M380,180 L620,180 L800,260 L880,560 L780,590 L730,430 L720,860 L280,860 L270,430 L220,590 L120,560 L200,260Z"
    out = f'<path d="{d}" fill="{R}"/>'
    out += f'<clipPath id="sw"><path d="{d}"/></clipPath><g clip-path="url(#sw)">'
    out += f'<path d="M200,260 C320,420 680,420 800,260 L800,180 L200,180Z" fill="{C}"/>'
    out += nordic_band(300, 700, 300, R, "star") + zig(230, 770, 360, 14, 16, G, 10)
    out += f'<rect x="100" y="500" width="800" height="40" fill="{C}"/>' + nordic_band(280, 720, 520, G, "diamond")
    out += f'<rect x="260" y="800" width="480" height="60" fill="{DR}"/>'
    for k in range(10): out += f'<rect x="{275 + k * 47}" y="805" width="18" height="50" rx="8" fill="{R}"/>'
    out += "</g>"
    out += f'<path d="M420,180 Q500,250 580,180" fill="none" stroke="{DR}" stroke-width="26" stroke-linecap="round"/>'
    out += heart(500, 680, 70, C) + heart(500, 682, 30, R)
    return out


def bauble_base(col, band_fn, cap=M):
    out = f'<path d="M500,60 C460,60 450,110 500,130 C550,110 540,60 500,60Z" fill="none" stroke="{cap}" stroke-width="14"/>'
    out += f'<rect x="440" y="125" width="120" height="80" rx="14" fill="{cap}"/>'
    out += "".join(f'<rect x="{452 + k * 26}" y="135" width="10" height="60" rx="5" fill="#C98E2A"/>' for k in range(4))
    out += circ(500, 530, 340, col)
    out += f'<clipPath id="bb{col[1:]}{id(band_fn) % 999}"><circle cx="500" cy="530" r="340"/></clipPath><g clip-path="url(#bb{col[1:]}{id(band_fn) % 999})">' + band_fn() + "</g>"
    out += f'<ellipse cx="380" cy="380" rx="70" ry="40" fill="#fff" opacity=".22" transform="rotate(-35 380 380)"/>'
    return out


def e_bauble1(): return bauble_base(R, lambda: f'<rect x="100" y="450" width="800" height="160" fill="{C}"/>' + nordic_band(170, 830, 530, R, "star") + zig(150, 850, 400, 16, 16, C, 12) + zig(150, 850, 660, 16, 16, C, 12))
def e_bauble2(): return bauble_base(G, lambda: "".join(f'<path d="M100,{y} Q500,{y + 80} 900,{y}" stroke="{c}" stroke-width="34" fill="none"/>' for y, c in [(330, C), (430, R), (530, C), (630, M), (730, C)]))
def e_bauble3(): return bauble_base(N, lambda: snowflake_folk(500, 530, 230, C, 1) + "".join(circ(500 + 300 * math.cos(a), 530 + 300 * math.sin(a), 14, M) for a in [k * math.pi / 6 for k in range(12)]))
def e_bauble4(): return bauble_base(P, lambda: "".join(heart(300 + (k % 4) * 140 + (70 if (k // 4) % 2 else 0), 280 + (k // 4) * 130, 40, [R, W][k % 2]) for k in range(20)))


def e_snow1(): return snowflake_folk(500, 500, 420, N, 0)
def e_snow2(): return snowflake_folk(500, 500, 420, LG, 1)
def e_snow3(): return snowflake_folk(500, 500, 420, R, 2)


def e_wreath():
    out = f'<circle cx="500" cy="520" r="300" fill="none" stroke="{BR}" stroke-width="26" opacity=".5"/>'
    rnd = random.Random(4)
    for ring, rr in enumerate((330, 270, 300)):
        for k in range(30):
            a = 2 * math.pi * (k + ring * .33) / 30
            x, y = 500 + rr * math.cos(a), 520 + rr * math.sin(a)
            ang = math.degrees(a) + 90 + (35 if (k + ring) % 2 else -35) + rnd.uniform(-10, 10)
            out += leaf(x, y, 115, 30, ang, [G, LG, "#3B7360"][(k + ring) % 3])
    for k in range(12):
        a = 2 * math.pi * k / 12 + .2
        out += circ(500 + 300 * math.cos(a), 520 + 300 * math.sin(a), 22, R)
    for k in range(6):
        a = 2 * math.pi * k / 6 + .5
        out += poly(starpts(500 + 330 * math.cos(a), 520 + 330 * math.sin(a), 28, 12, 5), M)
    # bow
    out += f'<path d="M500,200 C400,110 300,170 360,240 C400,280 470,240 500,210Z" fill="{R}"/><path d="M500,200 C600,110 700,170 640,240 C600,280 530,240 500,210Z" fill="{R}"/>'
    out += f'<path d="M490,215 C450,300 420,360 380,400 L430,410 L500,240Z" fill="{DR}"/><path d="M510,215 C550,300 580,360 620,400 L570,410 L500,240Z" fill="{DR}"/>'
    out += circ(500, 210, 36, DR)
    return out


def e_candle():
    out = f'<ellipse cx="500" cy="850" rx="260" ry="50" fill="{M}"/><ellipse cx="500" cy="835" rx="200" ry="34" fill="#C98E2A"/>'
    out += f'<rect x="410" y="360" width="180" height="480" rx="20" fill="{C}"/>'
    out += f'<path d="M410,400 C440,430 450,470 440,520 C460,480 480,440 470,400Z" fill="#E2D4B8"/>'
    out += zig(410, 590, 600, 16, 4, R, 12) + zig(410, 590, 660, 16, 4, G, 12)
    out += f'<path d="M500,360 L500,320" stroke="{SK}" stroke-width="8"/>'
    out += f'<path d="M500,140 C560,220 570,290 500,330 C430,290 440,220 500,140Z" fill="{M}"/><path d="M500,210 C530,250 530,290 500,310 C470,290 470,250 500,210Z" fill="#FFF0C2"/>'
    for side in (-1, 1):
        out += leaf(500 + side * 170, 820, 160, 40, 180 if side < 0 else 0, G) + leaf(500 + side * 230, 800, 120, 32, -160 if side < 0 else -20, LG)
    out += circ(310, 790, 20, R) + circ(690, 790, 20, R) + circ(340, 815, 16, R)
    return out


def e_bells():
    def bell(cx, cy, rot, col):
        return (f'<g transform="rotate({rot} {cx} {cy})"><path d="M{cx - 150},{cy + 220} C{cx - 120},{cy + 150} {cx - 120},{cy - 40} {cx - 80},{cy - 120} C{cx - 40},{cy - 190} {cx + 40},{cy - 190} {cx + 80},{cy - 120} '
                f'C{cx + 120},{cy - 40} {cx + 120},{cy + 150} {cx + 150},{cy + 220}Z" fill="{col}"/>'
                f'<rect x="{cx - 170}" y="{cy + 200}" width="340" height="44" rx="22" fill="#C98E2A"/>' + circ(cx, cy + 260, 34, "#C98E2A")
                + zig(cx - 110, cx + 110, cy + 120, 14, 8, C, 10) + f'</g>')
    out = bell(380, 520, -14, M) + bell(620, 520, 14, M)
    out += f'<path d="M500,240 C380,130 280,200 350,270 C400,320 470,270 500,250Z" fill="{R}"/><path d="M500,240 C620,130 720,200 650,270 C600,320 530,270 500,250Z" fill="{R}"/>'
    out += circ(500, 250, 40, DR) + leaf(470, 280, 150, 40, 120, G) + leaf(530, 280, 150, 40, 60, LG)
    return out


def e_present(box=R, rib=M, pat=C):
    out = f'<rect x="220" y="400" width="560" height="460" rx="12" fill="{box}"/>'
    out += "".join(circ(280 + (k % 5) * 110 + (55 if (k // 5) % 2 else 0), 460 + (k // 5) * 100, 14, pat) for k in range(25))
    out += f'<rect x="190" y="330" width="620" height="110" rx="12" fill="{box}"/><rect x="190" y="420" width="620" height="20" fill="#000" opacity=".12"/>'
    out += f'<rect x="460" y="330" width="80" height="530" fill="{rib}"/>'
    out += f'<path d="M500,330 C380,180 260,260 330,320 C380,360 460,340 500,330Z" fill="{rib}"/><path d="M500,330 C620,180 740,260 670,320 C620,360 540,340 500,330Z" fill="{rib}"/>'
    out += circ(500, 330, 40, "#C98E2A")
    return out


def e_present2(): return e_present(G, R, C)


def e_candy_cane():
    d = "M600,880 L600,330 C600,200 400,200 400,330"
    out = f'<path d="{d}" stroke="{W}" stroke-width="120" fill="none" stroke-linecap="round"/>'
    out += f'<path d="{d}" stroke="{R}" stroke-width="120" fill="none" stroke-linecap="round" stroke-dasharray="60 60"/>'
    out += f'<path d="{d}" stroke="#fff" stroke-width="20" fill="none" stroke-linecap="round" opacity=".35" transform="translate(-24,0)"/>'
    out += f'<path d="M520,700 C440,640 360,700 430,760 C470,790 510,740 520,710Z" fill="{G}"/><path d="M520,700 C600,640 680,700 610,760 C570,790 530,740 520,710Z" fill="{G}"/>'
    out += circ(520, 710, 30, DR)
    return out


def e_sprig():
    out = f'<path d="M200,820 C350,700 500,500 780,180" stroke="{BR}" stroke-width="18" fill="none" stroke-linecap="round"/>'
    for k in range(18):
        t = .08 + k * .05
        x = 200 + (780 - 200) * t; y = 820 - (820 - 180) * (t ** .9)
        for side in (-1, 1):
            out += f'<path d="M{x:.0f},{y:.0f} l{side * 110 * math.cos(math.radians(30)):.0f},{-60 + side * 30:.0f}" stroke="{G if k % 2 else "#3B7360"}" stroke-width="16" stroke-linecap="round"/>'
    out += "".join(circ(x, y, 18, "#7B5B3E") for x, y in [(430, 650), (600, 450)])
    return out


def e_holly():
    out = ""
    for ang, col in [(-150, G), (-30, "#3B7360"), (-95, LG), (60, G)]:
        out += (f'<g transform="translate(500,520) rotate({ang})"><path d="M0,0 C40,-50 80,-30 110,-80 C130,-40 170,-50 200,-90 C210,-40 250,-40 290,-60 C270,0 300,40 260,70 '
                f'C220,60 200,80 180,120 C150,80 120,90 80,120 C80,60 40,40 0,0Z" fill="{col}"/><path d="M10,4 L260,6" stroke="#fff" stroke-width="7" opacity=".35"/></g>')
    for dx, dy in ((-40, -10), (40, -30), (10, 50)):
        out += circ(500 + dx, 520 + dy, 50, R) + circ(500 + dx - 16, 520 + dy - 16, 12, "#fff", 'opacity=".55"')
    return out


def e_flower1(): return folk_flower(500, 500, 400, R, M, C) + "".join(leaf(500, 500, 460, 70, a, G) for a in (225, 315))[:0] + circ(500, 500, 60, R)


def e_flower2():
    out = ""
    for a in (200, 340):
        out += leaf(500, 620, 330, 80, a, G)
    out += f'<path d="M500,900 L500,560" stroke="{G}" stroke-width="18"/>'
    out += leaf(500, 780, 180, 50, 210, LG) + leaf(500, 760, 180, 50, -30, LG)
    for k in range(5):
        a = -90 + (k - 2) * 32
        out += f'<path d="M0,0 C-60,-120 -40,-280 0,-330 C40,-280 60,-120 0,0Z" fill="{[R, P, R, P, R][k]}" transform="translate(500,520) rotate({a + 90})"/>'
    out += f'<path d="M380,500 Q500,600 620,500 Q600,600 500,620 Q400,600 380,500Z" fill="{M}"/>'
    out += dots_ring(500, 330, 70, 6, 14, C)
    return out


def e_sled():
    out = f'<path d="M150,700 L830,700 C900,700 900,610 840,600" stroke="{SK}" stroke-width="22" fill="none" stroke-linecap="round"/>'
    for x in (300, 650):
        out += f'<path d="M{x},700 L{x + 20},580" stroke="{SK}" stroke-width="18"/>'
    out += f'<rect x="200" y="510" width="580" height="80" rx="20" fill="{R}"/>' + zig(220, 760, 550, 14, 14, C, 10)
    out += f'<path d="M760,520 C820,480 840,420 800,380" stroke="{R}" stroke-width="40" fill="none" stroke-linecap="round"/>'
    out += '<g transform="translate(170,80) scale(.5)">' + e_present(G, M, C) + "</g>"
    out += '<g transform="translate(440,149) scale(.42)">' + e_present(R, C, M) + "</g>"
    return out


def e_mug():
    out = f'<path d="M680,430 C820,430 830,650 680,660" stroke="{R}" stroke-width="50" fill="none"/>'
    out += f'<path d="M240,360 L720,360 L690,780 C685,840 640,870 580,870 L380,870 C320,870 275,840 270,780Z" fill="{R}"/>'
    out += f'<rect x="250" y="500" width="460" height="110" fill="{C}"/>' + nordic_band(280, 700, 555, R, "star")
    out += f'<ellipse cx="480" cy="360" rx="240" ry="40" fill="#6B3E26"/>'
    out += "".join(f'<rect x="{x}" y="{y}" width="80" height="70" rx="18" fill="{W}" transform="rotate({r} {x + 40} {y + 35})"/>' for x, y, r in [(340, 300, -10), (440, 290, 8), (530, 305, -4)])
    for k, x in enumerate((400, 500, 600)):
        out += f'<path d="M{x},250 C{x - 40},200 {x + 40},160 {x},100" stroke="#CFC6B8" stroke-width="16" fill="none" stroke-linecap="round" opacity=".8"/>'
    out += heart(480, 740, 50, C)
    return out


def e_garland():
    out = f'<path d="M40,330 Q500,620 960,330" stroke="{BR}" stroke-width="8" fill="none"/>'
    for k in range(9):
        t = (k + .5) / 9; x = 40 + 920 * t; y = 330 + 4 * 290 * t * (1 - t) * .5 * 2
        y = (1 - t) ** 2 * 330 + 2 * (1 - t) * t * 620 + t ** 2 * 330
        if k % 3 == 0: out += poly(starpts(x, y + 50, 52, 22, 5), M)
        elif k % 3 == 1: out += heart(x, y + 50, 46, R)
        else: out += circ(x, y + 55, 42, G) + circ(x - 12, y + 42, 10, "#fff", 'opacity=".5"')
    return out


def e_border():
    out = f'<rect x="20" y="430" width="960" height="140" rx="10" fill="{R}"/>'
    out += nordic_band(40, 960, 500, C, "star")
    out += zig(30, 970, 450, 10, 30, C, 7) + zig(30, 970, 550, 10, 30, C, 7)
    return out


def e_reindeer_head():
    # simple folk reindeer face (front), original shapes
    out = ""
    for side in (-1, 1):
        out += (f'<path d="M{500 + side * 90},360 C{500 + side * 140},260 {500 + side * 170},190 {500 + side * 250},120" stroke="{BR}" stroke-width="30" fill="none" stroke-linecap="round"/>'
                f'<path d="M{500 + side * 145},250 L{500 + side * 260},240" stroke="{BR}" stroke-width="26" stroke-linecap="round"/>'
                f'<path d="M{500 + side * 175},180 L{500 + side * 170},90" stroke="{BR}" stroke-width="24" stroke-linecap="round"/>'
                f'<ellipse cx="{500 + side * 200}" cy="420" rx="90" ry="40" fill="#A56E48" transform="rotate({side * -25} {500 + side * 200} 420)"/>')
    out += f'<path d="M500,330 C620,330 670,420 650,560 C630,690 580,800 500,820 C420,800 370,690 350,560 C330,420 380,330 500,330Z" fill="#A56E48"/>'
    out += f'<path d="M500,600 C580,600 610,700 580,780 C560,820 440,820 420,780 C390,700 420,600 500,600Z" fill="#E7CBA6"/>'
    out += circ(500, 760, 58, R) + circ(484, 745, 16, "#fff", 'opacity=".6"')
    out += circ(440, 500, 20, SK) + circ(560, 500, 20, SK) + circ(446, 494, 6, "#fff") + circ(566, 494, 6, "#fff")
    out += circ(410, 570, 22, P, 'opacity=".8"') + circ(590, 570, 22, P, 'opacity=".8"')
    out += f'<rect x="380" y="840" width="240" height="44" rx="22" fill="{G}"/>' + poly(starpts(500, 862, 28, 12, 5), M)
    return out


EL = [  # (file name, display name, function)
    ("tree-tiered", "Tiered tree", e_tree_tiered), ("tree-folk", "Folk heart tree", e_tree_folk), ("tree-cone", "Garland tree", e_tree_cone),
    ("star-nordic", "Nordic star", e_star8), ("star-nordic-green", "Nordic star, green", lambda: e_star8(G, C)), ("star-straw", "Straw star", e_star_straw),
    ("heart-folk", "Folk heart", e_heart_folk), ("heart-woven", "Woven heart", e_heart_woven), ("bird-red", "Red folk bird", e_bird),
    ("bird-blue", "Blue folk bird", lambda: e_bird(N, C, M)), ("gnome-red", "Gnome, red hat", e_gnome1), ("gnome-navy", "Gnome, starry hat", e_gnome2),
    ("gnome-heart", "Gnome with heart", e_gnome3), ("mushroom", "Toadstool", e_mushroom), ("mushrooms-pair", "Toadstool pair", e_mushrooms_pair),
    ("gingerbread-house", "Gingerbread house", e_ginger_house), ("gingerbread-man", "Gingerbread friend", e_ginger_man), ("cottage", "Snowy cottage", e_cottage),
    ("mitten-red", "Mitten, stars", e_mitten), ("mitten-green", "Mitten, hearts", e_mitten2), ("stocking-red", "Stocking, stars", e_stocking),
    ("stocking-green", "Stocking, hearts", e_stocking2), ("sweater", "Christmas sweater", e_sweater), ("bauble-band", "Bauble, star band", e_bauble1),
    ("bauble-stripes", "Bauble, stripes", e_bauble2), ("bauble-snowflake", "Bauble, snowflake", e_bauble3), ("bauble-hearts", "Bauble, hearts", e_bauble4),
    ("snowflake-navy", "Snowflake 1", e_snow1), ("snowflake-sage", "Snowflake 2", e_snow2), ("snowflake-red", "Snowflake 3", e_snow3),
    ("wreath", "Wreath with bow", e_wreath), ("candle", "Advent candle", e_candle), ("bells", "Bells", e_bells), ("present-red", "Present, red", e_present),
    ("present-green", "Present, green", e_present2), ("candy-cane", "Candy cane", e_candy_cane), ("pine-sprig", "Pine sprig", e_sprig), ("holly", "Holly", e_holly),
    ("folk-flower", "Folk flower", e_flower1), ("folk-tulip", "Folk tulip", e_flower2), ("sled", "Sled with gifts", e_sled), ("cocoa-mug", "Cocoa mug", e_mug),
    ("garland", "Star garland", e_garland), ("border", "Nordic border", e_border), ("reindeer", "Reindeer", e_reindeer_head),
]


def svg_of(fn, size=None):
    sz = f'width="{size}" height="{size}" ' if size else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" {sz}viewBox="0 0 1000 1000">{fn()}</svg>'


# ---------------- seamless patterns ----------------
def pattern(bg, motifs, tile=1000, n=6):
    """motifs: list of (fn, scale). Half-drop grid; each motif sits fully inside its cell so the tile repeats seamlessly."""
    cell = tile / n
    body = f'<rect width="{tile}" height="{tile}" fill="{bg}"/>'
    k = 0
    for i in range(n):
        for j in range(n):
            m = motifs[(i * 2 + j + (i // 2)) % len(motifs)]; fn, sc = m[0], m[1]; k += 1
            cx = i * cell + cell / 2; cy = j * cell + cell / 2 + (cell / 2 if i % 2 else 0)
            s = cell * sc / 1000
            for dy in (0, -tile, tile):
                body += f'<g transform="translate({cx - 500 * s:.1f},{cy + dy - 500 * s:.1f}) scale({s:.4f})">{fn()}</g>'
                body += circ(cx, cy - cell / 2 + dy, cell * .022, m[2] if len(m) > 2 else "#ffffff")
    return body


def dot(col):
    return lambda: circ(500, 500, 120, col)


PATTERNS = [
    ("pattern-trees-cream", C, [(e_tree_tiered, .8, R), (lambda: e_star8(R, C), .45, R), (e_tree_cone, .8, R), (lambda: heart(500, 520, 300, R), .35, R)]),
    ("pattern-gnomes-red", "#9E2B33", [(e_gnome2, .78, C), (lambda: snowflake_folk(500, 500, 420, C, 0), .38, C), (e_gnome1, .78, C), (lambda: snowflake_folk(500, 500, 420, C, 1), .38, C)]),
    ("pattern-snowflakes-navy", N, [(lambda: snowflake_folk(500, 500, 420, C, 0), .7, C), (lambda: snowflake_folk(500, 500, 420, LG, 1), .5, C), (lambda: snowflake_folk(500, 500, 420, P, 2), .62, C)]),
    ("pattern-hearts-pink", "#F6DCD5", [(e_heart_folk, .62, R), (lambda: e_heart_woven(), .5, R), (lambda: folk_flower(500, 500, 400, R, M, C), .4, R)]),
    ("pattern-mushrooms-sage", "#DCE6DA", [(e_mushroom, .7, G), (e_holly, .5, G), (e_mushrooms_pair, .74, G), (e_sprig, .55, G)]),
    ("pattern-baubles-green", G, [(e_bauble1, .66, C), (e_bauble4, .6, C), (e_bauble3, .66, C), (lambda: poly(starpts(500, 500, 420, 180, 5), M), .3, C)]),
]


def pattern_svg(bg, motifs, px=None):
    sz = f'width="{px}" height="{px}" ' if px else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" {sz}viewBox="0 0 1000 1000">{pattern(bg, motifs)}</svg>'


# ---------------- catalog PDF ----------------
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Poppins, sans-serif; color: #3A2A26; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #FBF6EC; contain: strict; }
html, body { width: var(--pw); overflow: hidden; }
h1 { font: italic 600 40pt/1 Lora, serif; color: #8E2430; }
h2 { font: italic 600 22pt/1.1 Lora, serif; color: #8E2430; }
.grid { position: absolute; left: 0.5in; right: 0.5in; top: 1.25in; bottom: 0.6in; display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.14in; }
.cell { background: #fff; border-radius: 0.12in; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0.08in;
  box-shadow: 0 0 0 1px #eadfcd inset; }
.cell svg { width: auto; height: 1.3in; }
.cell span { font: 600 7.5pt Poppins; color: #7a6a60; margin-top: 0.02in; text-align: center; }
.hd { position: absolute; left: 0.5in; right: 0.5in; top: 0.45in; display: flex; justify-content: space-between; align-items: baseline; }
.hd small { font: 600 9pt Poppins; letter-spacing: .14em; text-transform: uppercase; color: #2E5E4E; }
.foot { position: absolute; bottom: 0.25in; left: 0; right: 0; text-align: center; font: 7pt Poppins; color: #a09488; }
"""


def catalog(pattern_pngs):
    pages = []
    hero = [e_gnome1, e_tree_tiered, e_star8, e_heart_woven, e_bird, e_mushroom, e_ginger_house, e_wreath]
    pos = [(0.6, 1.0, 1.9), (2.6, 0.7, 2.2), (4.9, 0.9, 1.9), (6.4, 1.6, 1.5), (0.8, 7.2, 1.7), (2.8, 7.6, 1.5), (4.4, 7.1, 1.9), (6.2, 7.4, 1.7), (0.3, 3.5, 1.2)]
    art = "".join(f'<div style="position:absolute;left:{x}in;top:{y}in;width:{w}in">{svg_of(fn)}</div>' for fn, (x, y, w) in zip(hero, pos))
    pages.append(f'<div class="page">{art}<div style="position:absolute;left:0;right:0;top:3.7in;text-align:center">'
                 f'<div style="font:600 11pt Poppins;letter-spacing:.24em;text-transform:uppercase;color:#2E5E4E">Clipart · PNG + SVG · Commercial use</div>'
                 f'<h1 style="font-size:54pt;margin-top:0.18in">Nordic Folk Christmas</h1>'
                 f'<div style="font:400 13pt/1.5 Poppins;margin:0.2in auto 0;max-width:5.6in">{len(EL)} hand-drawn style vector elements, 6 seamless patterns and a matching palette. '
                 f'Transparent PNGs at 3000 px and editable SVGs.</div>'
                 f'<div style="display:flex;gap:0.12in;justify-content:center;margin-top:0.3in">'
                 + "".join(f'<div style="width:0.42in;height:0.42in;border-radius:50%;background:{c};box-shadow:0 0 0 2px #fff,0 0 0 3px #e2d6c4"></div>' for c in (R, DR, G, LG, C, M, P, N, BR))
                 + '</div></div><div class="foot">Purl &amp; Paper · original artwork · see the licence page</div></div>')
    per = 20
    for pi in range(0, len(EL), per):
        cells = "".join(f'<div class="cell">{svg_of(fn)}<span>{nm} · {fname}</span></div>' for fname, nm, fn in EL[pi:pi + per])
        pages.append(f'<div class="page"><div class="hd"><h2>The elements</h2><small>Page {pi // per + 1} · PNG + SVG</small></div>'
                     f'<div class="grid" style="grid-template-rows:repeat(5,1fr)">{cells}</div><div class="foot">Every element is a separate transparent PNG (3000 x 3000 px) and SVG file</div></div>')
    pc = "".join(f'<div class="cell" style="padding:0;overflow:hidden"><img src="{u}" style="width:100%;display:block"><span style="padding:0.05in">{n.replace("pattern-", "").replace("-", " ")}</span></div>'
                 for n, u in pattern_pngs)
    pages.append(f'<div class="page"><div class="hd"><h2>Seamless patterns</h2><small>12 x 12 in · 300 dpi JPG</small></div>'
                 f'<div class="grid" style="grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);top:1.3in;bottom:3.4in">{pc}</div>'
                 f'<div style="position:absolute;left:0.6in;right:0.6in;bottom:0.8in;font:10pt/1.55 Poppins">'
                 f'<h2 style="font-size:16pt;margin-bottom:0.08in">Colour palette</h2>'
                 + "".join(f'<div style="display:inline-flex;align-items:center;gap:0.06in;width:2.3in;margin-bottom:0.05in"><span style="display:inline-block;width:0.3in;height:0.3in;border-radius:50%;background:{c}"></span>{nm} {c}</div>'
                           for c, nm in [(R, "Berry red"), (DR, "Deep red"), (G, "Pine"), (LG, "Sage"), (C, "Cream"), (M, "Mustard"), (P, "Blush"), (N, "Navy"), (BR, "Bark")])
                 + '</div><div class="foot">Patterns tile seamlessly: use them as backgrounds, gift wrap, digital paper or fabric mock-ups</div></div>')
    lic = ("<b>You may</b> use these designs in things you make and sell: printed cards, gift tags, stickers, mugs, shirts, ornaments, sublimation, laser and cutting projects, "
           "social posts, and digital printables where the clipart is part of your own larger design. Personal use is unlimited. Commercial use covers up to 5,000 sales per design.<br><br>"
           "<b>Please don't</b> sell, share or give away the clipart or pattern files themselves (on their own, re-coloured or in another clipart, digital paper or template pack), "
           "use them in a logo or trademark, or upload them to print-on-demand design marketplaces as stand-alone graphics.<br><br>"
           "<b>Credit</b> is appreciated but not required. Questions about larger use? Send us a message.")
    pages.append(f'<div class="page"><div class="hd"><h2>How to use · licence</h2><small>Purl &amp; Paper</small></div>'
                 f'<div style="position:absolute;left:0.8in;right:0.8in;top:1.4in;font:11pt/1.65 Poppins">'
                 f'<h2 style="font-size:16pt;margin-bottom:0.1in">Files</h2>PNG folder: transparent PNGs, 3000 x 3000 px (10 in at 300 dpi). Drop them into Canva, Procreate, Photoshop, Word, Cricut Design Space or Silhouette Studio.<br>'
                 f'SVG folder: vector files that scale to any size and can be re-coloured in Illustrator, Inkscape, Affinity Designer or Cricut.<br>Patterns folder: 6 seamless 3600 x 3600 px JPGs.<br><br>'
                 f'<h2 style="font-size:16pt;margin-bottom:0.1in">Licence (small business commercial use)</h2>{lic}</div>'
                 f'<div style="position:absolute;left:0;right:0;bottom:1in;display:flex;justify-content:center;gap:0.3in">'
                 + "".join(f'<div style="width:1.2in">{svg_of(fn)}</div>' for fn in (e_gnome3, e_heart_folk, e_star_straw))
                 + '</div><div class="foot">Original artwork designed by Purl &amp; Paper with AI assistance</div></div>')
    return pages


def main(out):
    from playwright.sync_api import sync_playwright
    from render import render
    import base64
    out = pathlib.Path(out); png = out / "png"; svgd = out / "svg"; pat = out / "patterns"
    for d in (png, svgd, pat): d.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1000, "height": 1000}, device_scale_factor=3)
        for fname, nm, fn in EL:
            s = svg_of(fn)
            (svgd / f"{fname}.svg").write_text(s)
            pg.set_content(f'<html><body style="margin:0;background:transparent">{svg_of(fn, 1000)}</body></html>')
            pg.screenshot(path=str(png / f"{fname}.png"), omit_background=True, clip={"x": 0, "y": 0, "width": 1000, "height": 1000})
            from PIL import Image
            im = Image.open(png / f"{fname}.png").convert("RGBA")
            im.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(png / f"{fname}.png", optimize=True, dpi=(300, 300))
        pg.close()
        pg = b.new_page(viewport={"width": 1200, "height": 1200}, device_scale_factor=3)
        thumbs = []
        for name, bg, motifs in PATTERNS:
            pg.set_content(f'<html><body style="margin:0">{pattern_svg(bg, motifs, 1200)}</body></html>')
            p = pat / f"{name}.jpg"
            pg.screenshot(path=str(p), type="jpeg", quality=88, clip={"x": 0, "y": 0, "width": 1200, "height": 1200})
            from PIL import Image
            im = Image.open(p); im.info["dpi"] = (300, 300); im.save(p, "JPEG", quality=88, dpi=(300, 300))
            th = im.resize((500, 500)); bio = io.BytesIO(); th.save(bio, "JPEG", quality=85)
            thumbs.append((name, "data:image/jpeg;base64," + base64.b64encode(bio.getvalue()).decode()))
        b.close()
    render(CSS, catalog(thumbs), "letter", str(out / "nordic-folk-christmas-clipart-US-Letter.pdf"))
    print(len(EL), "elements,", len(PATTERNS), "patterns")


if __name__ == "__main__":
    main(sys.argv[1])
