"""Junk journal kits, ephemera pack and journaling cards. All artwork is drawn here from scratch (SVG + generated textures)."""
import math, random, sys
from render import render
import textures as T

BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Lora, serif; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; }
.bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.layer { position: absolute; inset: 0; }
.pad { position: absolute; inset: 0.45in; }
.script { font-family: "TeX Gyre Chorus", Lora, serif; }
.type { font-family: "Liberation Mono", monospace; }
.grid { position: absolute; inset: 0.4in; display: grid; gap: 0.18in; }
.cut { outline: 1px dashed rgba(0,0,0,0.25); outline-offset: 0.06in; }
svg { display: block; }
svg.layer { width: 100%; height: 100%; }
"""

def rnd(seed): return random.Random(seed)

# ---------------- drawing helpers ----------------
def leaf(x, y, l, ang, col, vein="rgba(0,0,0,.25)"):
    a = math.radians(ang); ex, ey = x + l * math.cos(a), y + l * math.sin(a)
    nx, ny = -math.sin(a) * l * 0.32, math.cos(a) * l * 0.32
    mx, my = (x + ex) / 2, (y + ey) / 2
    return (f'<path d="M{x:.1f} {y:.1f} Q{mx + nx:.1f} {my + ny:.1f} {ex:.1f} {ey:.1f} Q{mx - nx:.1f} {my - ny:.1f} {x:.1f} {y:.1f}Z" fill="{col}"/>'
            f'<path d="M{x:.1f} {y:.1f} L{ex:.1f} {ey:.1f}" stroke="{vein}" stroke-width="{max(.6, l / 40):.1f}" fill="none"/>')

def sprig(x, y, h, col, leafcol, seed, flower=None):
    r = rnd(seed); out = []; pts = []
    cx = x
    for i in range(9):
        t = i / 8; px = x + math.sin(t * 2.4 + seed) * h * 0.08; py = y - t * h; pts.append((px, py))
    d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
    out.append(f'<path d="{d}" stroke="{col}" stroke-width="{h / 90:.1f}" fill="none" stroke-linecap="round"/>')
    for i in range(1, 8):
        px, py = pts[i]; s = h * (0.2 - i * 0.012)
        out.append(leaf(px, py, s, -150 + r.uniform(-15, 15), leafcol)); out.append(leaf(px, py, s, -30 + r.uniform(-15, 15), leafcol))
    if flower:
        px, py = pts[-1]
        for k in range(6):
            a = k * 60 + r.uniform(-8, 8); out.append(leaf(px, py, h * 0.11, a, flower, "rgba(0,0,0,.15)"))
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{h * 0.025:.1f}" fill="#e9c46a"/>')
    return "".join(out)

def teacup(x, y, s, col, ink):
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{ink}" stroke-width="2.2" fill="{col}">'
            '<path d="M-40 -10 L40 -10 Q38 30 0 34 Q-38 30 -40 -10Z"/><path d="M40 0 Q60 0 56 14 Q52 26 34 22" fill="none"/>'
            '<ellipse cx="0" cy="40" rx="56" ry="8"/><path d="M-12 -22 q6 -10 0 -18 M6 -22 q6 -10 0 -18" fill="none" stroke-linecap="round"/></g>')

def moth(x, y, s, col, ink, seed):
    r = rnd(seed); a = r.uniform(0.85, 1.15)
    w1 = f"M0 -4 C-30 -40 -78 -36 -70 -6 C-66 10 -30 12 0 4Z"
    w2 = f"M0 4 C-24 10 -52 30 -40 48 C-28 60 -8 30 0 10Z"
    spots = f'<circle cx="-42" cy="-14" r="7" fill="{ink}" opacity=".35"/><circle cx="-28" cy="30" r="4" fill="{ink}" opacity=".3"/>'
    wing = f'<path d="{w1}" fill="{col}" stroke="{ink}" stroke-width="1.6"/><path d="{w2}" fill="{col}" stroke="{ink}" stroke-width="1.6" opacity=".9"/>{spots}'
    body = f'<ellipse cx="0" cy="8" rx="5" ry="22" fill="{ink}"/><path d="M-2 -12 q-10 -18 -22 -20 M2 -12 q10 -18 22 -20" stroke="{ink}" stroke-width="1.4" fill="none"/>'
    return f'<g transform="translate({x} {y}) scale({s * a}) rotate({r.uniform(-12, 12):.0f})">{wing}<g transform="scale(-1 1)">{wing}</g>{body}</g>'

def fern(x, y, h, col, seed):
    r = rnd(seed); out = [f'<path d="M{x} {y} Q{x + h * .15} {y - h * .5} {x + h * .05} {y - h}" stroke="{col}" stroke-width="{h / 120:.1f}" fill="none"/>']
    for i in range(1, 22):
        t = i / 22; px = x + h * .15 * (2 * t * (1 - t)) + h * .05 * t * t; py = y - h * t; l = h * .16 * (1 - t) + 4
        out.append(leaf(px, py, l, -160 + r.uniform(-6, 6), col, "rgba(0,0,0,0)")); out.append(leaf(px, py, l, -20 + r.uniform(-6, 6), col, "rgba(0,0,0,0)"))
    return "".join(out)

def stamp_frame(w, h, fill, inner):
    return f'<div style="width:{w};height:{h};padding:9px;background:radial-gradient(circle at 50% 50%, transparent 4.5px, {fill} 5px) -5px -5px / 13px 13px;filter:drop-shadow(0 1px 1px rgba(0,0,0,.25))"><div style="width:100%;height:100%;background:{fill};padding:6px">{inner}</div></div>'

# ---------------- page builders ----------------
def tex_page(uri, extra=""):
    return f'<div class="page"><img class="bg" src="{uri}">{extra}</div>'

def ledger(uri, ink, red):
    lines = (f'<div class="layer" style="background:repeating-linear-gradient(transparent 0 0.3in, {ink}55 0.3in calc(0.3in + 1px)) 0 1.1in / 100% 100% no-repeat;"></div>'
             f'<div class="layer" style="left:1.15in;width:4px;border-left:1px solid {red};border-right:1px solid {red};"></div>'
             f'<div class="layer" style="left:auto;right:1.6in;width:1px;background:{ink}55"></div><div class="layer" style="left:auto;right:0.9in;width:1px;background:{ink}55"></div>')
    return tex_page(uri, lines)

def lined_letter(uri, ink, word):
    return tex_page(uri, f'<div class="pad"><div class="script" style="font-size:38pt;color:{ink};opacity:.85">{word}</div>'
                    f'<div style="position:absolute;top:1in;left:0;right:0;bottom:0;background:repeating-linear-gradient(transparent 0 0.36in, {ink}66 0.36in calc(0.36in + 1px))"></div></div>')

def pattern_page(defs, fill_id, bg):
    return f'<div class="page" style="background:{bg}"><svg width="100%" height="100%"><defs>{defs}</defs><rect width="100%" height="100%" fill="url(#{fill_id})"/></svg></div>'

def tags_sheet(bg, fill, ink, accent, words, title_font="script"):
    cells = ""
    for i, w in enumerate(words[:8]):
        cells += (f'<div style="position:relative;background:{fill};clip-path:polygon(18% 0,82% 0,100% 12%,100% 100%,0 100%,0 12%);padding:0.62in 0.18in 0.2in;text-align:center;color:{ink};box-shadow:inset 0 0 0 2px {accent}33">'
                  f'<div style="position:absolute;top:0.2in;left:50%;width:0.24in;height:0.24in;margin-left:-0.12in;border-radius:50%;background:{bg};box-shadow:0 0 0 4px {accent}"></div>'
                  f'<div class="{title_font}" style="font-size:24pt;line-height:1">{w}</div><div style="margin:0.12in auto 0;width:70%;border-top:1.5px dashed {ink}88"></div>'
                  f'<div style="margin-top:0.14in;height:1.3in;background:repeating-linear-gradient(transparent 0 0.26in, {ink}44 0.26in calc(0.26in + 1px))"></div></div>')
    return f'<div class="page" style="background:{bg}"><div class="grid" style="grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1fr">{cells}</div></div>'

def labels_sheet(bg, fill, ink, accent, items):
    cells = ""
    for i, (a, b) in enumerate(items[:12]):
        shape = ["border-radius:0.15in", "border-radius:50% / 30%", "clip-path:polygon(8% 0,92% 0,100% 50%,92% 100%,8% 100%,0 50%)"][i % 3]
        cells += (f'<div style="background:{fill};{shape};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{ink};padding:0.1in;box-shadow:inset 0 0 0 3px {fill}, inset 0 0 0 4.5px {accent}">'
                  f'<div class="type" style="font-size:7pt;letter-spacing:.2em;text-transform:uppercase;opacity:.75">{b}</div><div class="script" style="font-size:22pt;line-height:1.05">{a}</div>'
                  f'<div class="type" style="font-size:6.5pt;letter-spacing:.15em;margin-top:2pt;opacity:.6">No. {101 + i * 7}</div></div>')
    return f'<div class="page" style="background:{bg}"><div class="grid" style="grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(4,1fr)">{cells}</div></div>'

def tickets_sheet(bg, fills, ink, items):
    cells = ""
    for i, (top, big, small) in enumerate(items[:8]):
        f = fills[i % len(fills)]
        cells += (f'<div style="position:relative;background:{f};color:{ink};display:flex;align-items:stretch;-webkit-mask:radial-gradient(circle 0.11in at 0 50%,transparent 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 0.11in at 100% 50%,transparent 98%,#000) right/51% 100% no-repeat">'
                  f'<div style="flex:1;padding:0.12in 0.22in;display:flex;flex-direction:column;justify-content:center;border-right:2px dashed {ink}66">'
                  f'<div class="type" style="font-size:7pt;letter-spacing:.22em;text-transform:uppercase">{top}</div><div style="font-size:21pt;font-weight:700;line-height:1.05;margin:3pt 0">{big}</div>'
                  f'<div class="type" style="font-size:7pt">{small}</div></div><div class="type" style="width:0.55in;display:flex;align-items:center;justify-content:center;font-size:8pt;writing-mode:vertical-rl;letter-spacing:.15em">No {4021 + i * 113}</div></div>')
    return f'<div class="page" style="background:{bg}"><div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:repeat(4,1fr);gap:0.3in 0.25in">{cells}</div></div>'

def stamps_sheet(bg, fills, ink, drawers, values):
    cells = ""
    for i in range(12):
        f = fills[i % len(fills)]; art = drawers[i % len(drawers)](i)
        inner = (f'<div style="height:100%;border:1.5px solid {ink}55;display:flex;flex-direction:column;justify-content:space-between;align-items:center;padding:4px;color:{ink}">'
                 f'<svg viewBox="-60 -60 120 120" style="width:82%;flex:1">{art}</svg><div class="type" style="font-size:8pt;display:flex;justify-content:space-between;width:100%"><b>{values[i % len(values)]}</b><span>POSTE</span></div></div>')
        cells += f'<div style="display:flex;align-items:center;justify-content:center">{stamp_frame("1.75in", "2.1in", f, inner)}</div>'
    return f'<div class="page" style="background:{bg}"><div class="grid" style="grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(3,1fr)">{cells}</div></div>'

def cards_sheet(bg, cards):
    """4 cards of 3 x 4 in per page with cut guides."""
    cells = "".join(f'<div class="cut" style="width:3in;height:4in;position:relative;overflow:hidden">{c}</div>' for c in cards[:4])
    return (f'<div class="page" style="background:{bg}"><div style="position:absolute;inset:0;display:grid;grid-template-columns:3in 3in;grid-template-rows:4in 4in;gap:0.5in;'
            f'justify-content:center;align-content:center">{cells}</div></div>')

def intro_page(bg, ink, accent, title, sub, contents, sizes_note, art=""):
    li = "".join(f"<li>{c}</li>" for c in contents)
    return (f'<div class="page" style="background:{bg};color:{ink}"><div class="pad" style="display:flex;flex-direction:column">'
            f'<div class="type" style="font-size:9pt;letter-spacing:.3em;text-transform:uppercase;color:{accent}">Printable junk journal kit</div>'
            f'<div class="script" style="font-size:64pt;line-height:1;margin-top:10pt">{title}</div><div style="font-size:13pt;margin-top:8pt;opacity:.85;max-width:5in">{sub}</div>'
            f'<div style="margin-top:22pt;font-weight:700;font-size:12pt">Inside this kit</div><ul style="margin:6pt 0 0 16pt;font-size:10.5pt;line-height:1.65">{li}</ul>'
            f'<div style="margin-top:auto;font-size:9pt;opacity:.75;line-height:1.5">{sizes_note}</div></div>{art}</div>')

SIZES_NOTE = ("How to print: print at 100% / actual size on plain printer paper, or on cardstock for tags and cards. Every page is designed to print edge to edge; "
              "most printers leave a thin white border, which is part of the vintage look. For personal use and for handmade items you sell (journals, cards), not for reselling the files.")

# ---------------- TEA ROOM ----------------
def tea_room(size):
    W, H = (1275, 1650) if size == "letter" else (1240, 1754)
    ink, rust, sage, honey, rose, cream = "#5a3b26", "#9c4f2e", "#7a8f6a", "#d9a066", "#c98a8a", "#f3e7cf"
    tA, tB, tC = T.tea(W, H, 11), T.tea(W, H, 12, rings=1), T.tea(W, H, 13, base=(240, 230, 210), rings=0, strength=.7)
    P = []
    teaart = f'<svg viewBox="0 0 400 300" style="position:absolute;right:0.4in;bottom:1.4in;width:3.6in;opacity:.9">{teacup(200, 170, 1.8, rose, ink)}{sprig(60, 290, 220, sage, sage, 3, rose)}</svg>'
    P.append(intro_page(cream, ink, rust, "The Tea Room", "Soft tea-stained papers, recipe cards, menus and botanical pieces for slow afternoon pages.",
                        ["Tea-stained papers and a ledger page", "Recipe cards and a tea room menu", "Botanical tea sprig artwork", "Floral and gingham pattern papers",
                         "Lined writing paper", "Paper doilies, tags, labels, tickets and postage stamps", "Journaling cards (3 × 4 in)"], SIZES_NOTE, teaart))
    P.append(tex_page(tA)); P.append(ledger(tB, ink, rust)); P.append(tex_page(tC))
    recipes = [("Honey Lavender Scones", "2 cups flour · 1/3 cup cold butter · 1/4 cup honey · 1 tsp dried lavender · 2/3 cup cream. Rub, stir, pat, cut. Bake hot until golden."),
               ("Lemon Drizzle Loaf", "Cream butter and sugar. Beat in eggs and lemon zest. Fold in flour. Bake, then pour lemon syrup over while warm."),
               ("Grandma's Shortbread", "1 part sugar, 2 parts butter, 3 parts flour. Press into a tin, prick with a fork, bake low and slow."),
               ("Spiced Pear Jam", "Ripe pears, a little sugar, a cinnamon stick and one clove. Simmer gently until it sets on a cold plate.")]
    cards = "".join(f'<div style="background:#fbf6ea;border:2px solid {rust};padding:0.2in 0.25in;color:{ink};box-shadow:0 2px 3px rgba(0,0,0,.15)">'
                    f'<div class="type" style="font-size:7pt;letter-spacing:.25em;color:{rust}">RECIPE FROM THE KITCHEN OF ______________</div><div class="script" style="font-size:24pt;margin:6pt 0;border-bottom:1.5px solid {rust}">{t}</div>'
                    f'<div class="type" style="font-size:9pt;line-height:0.3in;background:repeating-linear-gradient(transparent 0 calc(0.3in - 1px), {ink}33 calc(0.3in - 1px) 0.3in)">{b}</div></div>' for t, b in recipes)
    P.append(tex_page(tC, f'<div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0.3in">{cards}</div>'))
    menu = [("Darjeeling", "Light, floral, a summer afternoon"), ("Earl Grey", "Bergamot and a slice of lemon"), ("Chamomile", "For quiet evenings"), ("Rose & Hibiscus", "Pink, tart and pretty"),
            ("Scones with jam", "Clotted cream on the side"), ("Cucumber sandwiches", "Crusts off, of course"), ("Victoria sponge", "A slice, or two"), ("Lemon tart", "Bright and buttery")]
    mi = "".join(f'<div style="display:flex;justify-content:space-between;gap:12pt;border-bottom:1px dotted {ink}88;padding:7pt 0"><div><div style="font-size:15pt;font-weight:600">{a}</div><div style="font-size:9.5pt;font-style:italic;opacity:.8">{b}</div></div><div class="type" style="font-size:11pt;align-self:end">{["1/-", "1/2", "9d", "1/4", "2/-", "1/6", "1/8", "2/2"][i]}</div></div>' for i, (a, b) in enumerate(menu))
    P.append(tex_page(tA, f'<div class="pad" style="inset:0.8in 1in;color:{ink};border:3px double {rust};padding:0.45in 0.6in;background:rgba(251,246,234,.55)"><div style="text-align:center"><div class="type" style="font-size:8pt;letter-spacing:.35em">EST. 1924 · THE LINDEN</div><div class="script" style="font-size:54pt;line-height:1.1">Tea Room</div><div class="type" style="font-size:8pt;letter-spacing:.3em;margin-bottom:12pt">AFTERNOON MENU</div></div>{mi}</div>'))
    bot = "".join(sprig(120 + i * 210, 980 + (i % 2) * 40, 600 + (i % 3) * 120, ink, [sage, "#8aa37a", "#6f8460"][i % 3], 20 + i, [rose, None, honey][i % 3]) for i in range(5))
    P.append(tex_page(tB, f'<svg class="layer" viewBox="0 0 1100 1100" preserveAspectRatio="xMidYMax meet" style="opacity:.92">{bot}</svg><div class="pad"><div class="script" style="color:{ink};font-size:40pt">Camellia sinensis</div><div class="type" style="color:{ink};font-size:9pt;letter-spacing:.2em">BOTANICAL STUDY · PLATE IV</div></div>'))
    flor = (f'<pattern id="fl" width="140" height="140" patternUnits="userSpaceOnUse"><rect width="140" height="140" fill="#f4e9d6"/>'
            f'<g transform="translate(35 35)">{"".join(leaf(0, 0, 22, a, rose, "rgba(0,0,0,.1)") for a in range(0, 360, 72))}<circle r="5" fill="{honey}"/></g>'
            f'<g transform="translate(105 105)">{"".join(leaf(0, 0, 18, a + 36, "#d8a7a0", "rgba(0,0,0,.1)") for a in range(0, 360, 72))}<circle r="4" fill="{honey}"/></g>'
            f'{leaf(70, 55, 22, -30, sage)}{leaf(70, 55, 20, 200, sage)}{leaf(12, 110, 18, 40, sage)}{leaf(128, 20, 18, 220, sage)}</pattern>')
    P.append(pattern_page(flor, "fl", "#f4e9d6"))
    ging = (f'<pattern id="gi" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="#f6eedf"/><rect width="30" height="60" fill="{rust}" opacity=".28"/>'
            f'<rect width="60" height="30" fill="{rust}" opacity=".28"/></pattern>')
    P.append(pattern_page(ging, "gi", "#f6eedf"))
    P.append(lined_letter(tC, ink, "My dearest,"))
    doil = ""
    for k in range(6):
        cx, cy = 260 + (k % 2) * 520, 260 + (k // 2) * 560; rr = 210
        petals = "".join(f'<circle cx="{cx + rr * math.cos(math.radians(a)):.1f}" cy="{cy + rr * math.sin(math.radians(a)):.1f}" r="34" fill="#fffdf8"/>' for a in range(0, 360, 15))
        holes = "".join(f'<circle cx="{cx + r2 * math.cos(math.radians(a + r2)):.1f}" cy="{cy + r2 * math.sin(math.radians(a + r2)):.1f}" r="{6 + r2 / 40:.1f}" fill="{["#e8d9bd", "#d9c3a0"][k % 2]}"/>'
                        for r2 in (70, 120, 170) for a in range(0, 360, int(360 / (r2 / 9))))
        doil += f'{petals}<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#fffdf8"/>{holes}<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="#d9c3a0" stroke-width="3"/>'
    P.append(f'<div class="page" style="background:#d9c3a0"><svg class="layer" viewBox="0 0 1040 1640" preserveAspectRatio="xMidYMid meet">{doil}</svg></div>')
    P.append(tags_sheet("#efe2c8", "#fbf6ea", ink, rust, ["Tea time", "Sweet", "Savour", "Afternoon", "Cosy", "Steep", "Linger", "Notes"]))
    P.append(labels_sheet("#e6d5b8", "#fbf6ea", ink, rust, [("Earl Grey", "Fine tea"), ("Chamomile", "Herbal"), ("Assam", "Strong"), ("Jasmine", "Green tea"), ("Rooibos", "Red bush"),
                                                             ("Peppermint", "Herbal"), ("Lemon Curd", "Preserve"), ("Strawberry", "Jam"), ("Honey", "Wildflower"), ("Shortbread", "Biscuits"), ("Marmalade", "Seville"), ("Sugar", "Lumps")]))
    P.append(tickets_sheet("#e9dcc2", ["#f3e3c3", "#e8c9b5", "#dfe5d3"], ink, [("The Linden Tea Room", "TABLE 4", "Afternoon sitting · 3 o'clock"), ("Garden Party", "ADMIT ONE", "Lawn and rose garden"),
                                                                              ("Village Fete", "RAFFLE", "Draw at four sharp"), ("Tea Dance", "ADMIT TWO", "Assembly Rooms · Saturday"),
                                                                              ("Flower Show", "EXHIBITOR", "Sweet peas, class 12"), ("Bakery", "RECEIPT", "2 iced buns · 1 loaf"), ("Railway", "RETURN", "Third class · valid one day"), ("Lending Library", "DUE BACK", "Fourteen days")]))
    draw = [lambda i: teacup(0, 4, 0.75, rose, ink), lambda i: sprig(0, 50, 100, ink, sage, i, rose), lambda i: f'<circle r="34" fill="{honey}"/>' + "".join(leaf(0, 0, 40, a, rose, "rgba(0,0,0,.1)") for a in range(0, 360, 60))]
    P.append(stamps_sheet("#e6d5b8", ["#f6ecd8", "#e9cfc4", "#dfe6d6"], ink, draw, ["1d", "2d", "3d", "½d", "4d", "6d"]))
    jc = [f'<div style="position:absolute;inset:0;background:#fbf6ea;padding:0.25in;color:{ink}"><div class="script" style="font-size:30pt">{w}</div><div style="position:absolute;inset:1in 0.25in 0.3in;background:repeating-linear-gradient(transparent 0 0.3in, {ink}44 0.3in calc(0.3in + 1px))"></div></div>'
          for w in ["Today", "Remember", "Sweet moments"]]
    jc.insert(1, f'<div style="position:absolute;inset:0;background:url(#) #f1e1c6"><svg viewBox="0 0 300 400" style="width:100%;height:100%">{sprig(150, 380, 340, ink, sage, 9, rose)}</svg></div>')
    P.append(cards_sheet("#efe2c8", jc))
    return BASE_CSS, P

# ---------------- NIGHT GARDEN ----------------
def night_garden(size):
    W, H = (1275, 1650) if size == "letter" else (1240, 1754)
    navy, deep, gold, peri, mauve, parch = "#1d2a4a", "#141d36", "#d4b062", "#8796c4", "#b48ab8", "#efe3c4"
    nA, nB = T.night(W, H, 21), T.night(W, H, 22, base=(30, 26, 52), light=(64, 52, 96), stars=400)
    pd = T.tea(W, H, 23, base=(232, 220, 190), dark=(160, 130, 90), rings=0, strength=.8)
    P = []
    art = f'<svg viewBox="0 0 400 400" style="position:absolute;right:0.5in;bottom:1.5in;width:3.4in">{moth(200, 170, 1.6, mauve, gold, 1)}<circle cx="320" cy="60" r="34" fill="{parch}"/><circle cx="334" cy="52" r="30" fill="{navy}"/></svg>'
    P.append(intro_page(navy, parch, gold, "Night Garden", "Moonlit papers, moths, ferns and star charts for dreamy, moody pages.",
                        ["Starry night papers", "Star chart with original constellations", "Moon phases page", "Moth and fern artwork", "Midnight ledger and parchment page",
                         "Celestial and damask pattern papers", "Tags, labels, tickets and postage stamps", "Journaling cards (3 × 4 in)"], SIZES_NOTE, art))
    P.append(tex_page(nA)); P.append(tex_page(nB))
    r = rnd(5); cons = ""; names = ["The Lantern", "The Heron", "The Key", "The Little Boat", "The Moth", "The Fox"]
    for k, nm in enumerate(names):
        cx, cy = 220 + (k % 2) * 560, 260 + (k // 2) * 480; pts = [(cx + r.uniform(-170, 170), cy + r.uniform(-140, 140)) for _ in range(6)]
        cons += f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="none" stroke="{gold}" stroke-width="2" opacity=".7"/>'
        cons += "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([5, 7, 9])}" fill="{parch}"/>' for x, y in pts)
        cons += f'<text x="{cx - 120}" y="{cy + 190}" fill="{gold}" font-family="TeX Gyre Chorus" font-size="44">{nm}</text>'
    rings = "".join(f'<circle cx="520" cy="820" r="{rr}" fill="none" stroke="{gold}" stroke-width="1" opacity=".25" stroke-dasharray="4 8"/>' for rr in (300, 520, 740))
    P.append(tex_page(nA, f'<svg class="layer" viewBox="0 0 1040 1640" preserveAspectRatio="xMidYMid meet">{rings}{cons}<text x="520" y="1600" text-anchor="middle" fill="{gold}" font-family="Liberation Mono" font-size="22" letter-spacing="10">A CHART OF THE NORTHERN GARDEN SKY</text></svg>'))
    ph = ""
    names = ["NEW", "WAXING CRESCENT", "FIRST QUARTER", "WAXING GIBBOUS", "FULL", "WANING GIBBOUS", "LAST QUARTER", "WANING CRESCENT"]
    for k in range(8):
        x, y = 260 + (k % 2) * 520, 220 + (k // 2) * 380; f = k / 8; R = 120
        ph += f'<circle cx="{x}" cy="{y}" r="{R}" fill="#2c3866" stroke="{parch}" stroke-opacity=".35" stroke-width="2"/>'
        if k == 4: ph += f'<circle cx="{x}" cy="{y}" r="{R}" fill="{parch}"/>'
        elif k != 0:
            rx = abs(math.cos(2 * math.pi * f)) * R; wax = f < 0.5; cres = (f % 0.5) < 0.25 if wax else (f % 0.5) >= 0.25
            side = 1 if wax else 0
            sweep = (0 if cres else 1) if wax else (1 if cres else 0)
            ph += f'<path d="M{x} {y - R} A{R} {R} 0 0 {side} {x} {y + R} A{rx:.1f} {R} 0 0 {sweep} {x} {y - R}Z" fill="{parch}"/>'
        ph += f'<text x="{x}" y="{y + 170}" text-anchor="middle" fill="{gold}" font-family="Liberation Mono" font-size="20" letter-spacing="6">{names[k]}</text>'
    P.append(tex_page(nB, f'<svg class="layer" viewBox="0 0 1040 1640" preserveAspectRatio="xMidYMid meet">{ph}</svg>'))
    moths = "".join(moth(230 + (k % 3) * 290, 260 + (k // 3) * 420, 2.0, [mauve, peri, "#c9a6a0", gold][k % 4], parch if k % 2 else gold, k) for k in range(9))
    P.append(tex_page(pd, f'<svg class="layer" viewBox="0 0 1100 1500" preserveAspectRatio="xMidYMid meet">{moths.replace(parch, "#3b2f45")}</svg><div class="pad"><div class="script" style="font-size:40pt;color:#3b2f45">Night Moths</div><div class="type" style="font-size:9pt;letter-spacing:.2em;color:#3b2f45">FIELD NOTES · PLATE IX</div></div>'))
    fr = "".join(fern(120 + k * 200, 1640, 900 + (k % 3) * 220, [gold, peri, mauve][k % 3] + "cc", k) for k in range(6))
    P.append(tex_page(nA, f'<svg class="layer" viewBox="0 0 1200 1640" preserveAspectRatio="xMidYMax slice">{fr}</svg>'))
    P.append(ledger(nB, parch, gold))
    P.append(lined_letter(pd, "#3b2f45", "Under the moon,"))
    cel = (f'<pattern id="ce" width="160" height="160" patternUnits="userSpaceOnUse"><rect width="160" height="160" fill="{navy}"/>'
           f'<path d="M40 30 l5 15 15 5 -15 5 -5 15 -5 -15 -15 -5 15 -5z" fill="{gold}"/><circle cx="120" cy="110" r="14" fill="{parch}"/><circle cx="127" cy="104" r="12" fill="{navy}"/>'
           f'<circle cx="110" cy="30" r="2.5" fill="{parch}"/><circle cx="20" cy="120" r="2" fill="{parch}"/><circle cx="70" cy="140" r="1.6" fill="{gold}"/></pattern>')
    P.append(pattern_page(cel, "ce", navy))
    def orn(cx, cy, sc, col):
        half = (f'<path d="M0 -70 C-18 -50 -20 -30 0 -12 C-30 -20 -46 -4 -40 16 C-34 34 -14 30 -10 18 C-6 6 -20 2 -24 12" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
                + leaf(0, 10, 34, 125, col, "rgba(0,0,0,0)") + leaf(0, 40, 28, 150, col, "rgba(0,0,0,0)"))
        return (f'<g transform="translate({cx} {cy}) scale({sc})">{half}<g transform="scale(-1 1)">{half}</g>'
                f'<path d="M0 -92 L10 -78 L0 -64 L-10 -78Z" fill="{col}"/><circle cx="0" cy="66" r="8" fill="{col}"/><path d="M0 -12 L0 74" stroke="{col}" stroke-width="4"/></g>')
    dam = (f'<pattern id="da" width="200" height="260" patternUnits="userSpaceOnUse"><rect width="200" height="260" fill="#2a2244"/>'
           f'{orn(100, 120, 1, mauve + "aa")}{orn(0, -10, .55, peri + "88")}{orn(200, -10, .55, peri + "88")}{orn(0, 250, .55, peri + "88")}{orn(200, 250, .55, peri + "88")}</pattern>')
    P.append(pattern_page(dam, "da", "#2a2244"))
    P.append(tags_sheet(deep, navy, parch, gold, ["Dream", "Midnight", "Wish", "Starlight", "Hush", "Bloom", "Wander", "Moonlit"]))
    P.append(labels_sheet(deep, navy, parch, gold, [("Nocturne", "No. 7"), ("Moonflower", "Seeds"), ("Belladonna", "Botanical"), ("Stardust", "Jar"), ("Lunaria", "Honesty"),
                                                     ("Night Jasmine", "Perfume"), ("Comet", "Observed"), ("Fox Glove", "Garden"), ("Owl Feather", "Found"), ("Velvet", "Moth"), ("Dew", "Collected"), ("Orion", "Winter")]))
    P.append(tickets_sheet(deep, ["#2b3866", "#3a2f5c", "#24405a"], parch, [("Old Hill Observatory", "ADMIT ONE", "Viewing from 10 pm"), ("Midnight Garden", "LANTERN WALK", "Gate opens at dusk"),
                                                                             ("Star Party", "TELESCOPE 3", "Bring a blanket"), ("Night Train", "SLEEPER", "Berth 12 · coach C"), ("Moth Survey", "RECORDER", "Light trap no. 4"),
                                                                             ("Planetarium", "ADMIT TWO", "Show: The Long Night"), ("Night Market", "STALL 21", "Candles and honey"), ("Lighthouse", "TOUR", "Keeper's lamp room")]))
    draw = [lambda i: moth(0, 0, 0.6, mauve, gold, i), lambda i: f'<circle r="38" fill="{parch}"/><circle cx="14" cy="-8" r="34" fill="{navy}"/>', lambda i: fern(0, 56, 110, gold, i)]
    P.append(stamps_sheet(deep, ["#2b3866", "#3a2f5c", "#24405a"], parch, draw, ["5c", "10c", "25c", "1 lune", "2c", "50c"]))
    jc = [f'<div style="position:absolute;inset:0;background:{navy};padding:0.25in;color:{parch}"><div class="script" style="font-size:30pt;color:{gold}">{w}</div><div style="position:absolute;inset:1in 0.25in 0.3in;background:repeating-linear-gradient(transparent 0 0.3in, {parch}44 0.3in calc(0.3in + 1px))"></div></div>' for w in ["Tonight", "Dreams", "Wishes"]]
    jc.insert(1, f'<div style="position:absolute;inset:0;background:{navy}"><svg viewBox="0 0 300 400" style="width:100%;height:100%">{moth(150, 190, 1.4, mauve, gold, 5)}</svg></div>')
    P.append(cards_sheet(deep, jc))
    return BASE_CSS, P

# ---------------- EPHEMERA PACK ----------------
def ephemera(size):
    ink, red, kraftc, cream, black = "#2b2b2b", "#a63d32", "#c8a678", "#f2e8d5", "#2b2b2b"
    STAMPART = '<svg viewBox="-60 -60 120 120">' + sprig(0, 50, 100, ink, "#6f7d5c", 2, red) + "</svg>"
    P = [intro_page(cream, ink, red, "Ephemera Pack", "Vintage-style tickets, tags, labels, stamps, receipts and library cards to cut out and layer.",
                    ["8 tickets", "8 tags", "12 labels", "12 postage stamps", "Library cards and receipts", "Index tabs and small notes"], SIZES_NOTE,
                    f'<div style="position:absolute;right:0.6in;bottom:1.5in;width:3.3in;height:3.4in">'
                    f'<div style="position:absolute;right:0;top:0;transform:rotate(6deg)">{stamp_frame("1.6in", "1.95in", "#e3d2b4", STAMPART)}</div>'
                    f'<div class="type" style="position:absolute;left:0;bottom:0;transform:rotate(-5deg);background:#d9c3a0;color:{ink};padding:0.15in 0.3in;font-size:8pt;letter-spacing:.2em;border-left:3px dashed {ink}66">GRAND CINEMA<br><b style="font-size:20pt;font-family:Lora">ADMIT ONE</b><br>ROW F · SEAT 9</div></div>')]
    P.append(tickets_sheet(cream, ["#e8dcc3", "#d9c3a0", "#efe6d2"], ink, [("Grand Cinema", "ADMIT ONE", "Row F · seat 9"), ("Ferry", "SINGLE", "Harbour crossing"), ("Museum", "ENTRY", "Natural history wing"),
                                                                             ("Circus", "RING SIDE", "Two shows daily"), ("Dance Hall", "ADMIT ONE", "Saturday night"), ("Botanical Garden", "SEASON", "Glasshouses included"),
                                                                             ("Funfair", "CAROUSEL", "One ride"), ("Exhibition", "PRIVATE VIEW", "Gallery II")]))
    P.append(tags_sheet("#d9c3a0", cream, ink, red, ["Memories", "Hello", "Adventure", "Collected", "Found", "Treasure", "Keep", "Notes"]))
    P.append(labels_sheet("#c8a678", cream, ink, red, [("Postcards", "Saved"), ("Letters", "Bundle"), ("Receipts", "Kept"), ("Buttons", "Assorted"), ("Ribbons", "Notions"), ("Photos", "Family"),
                                                        ("Maps", "Travels"), ("Stamps", "Collection"), ("Seeds", "Packet"), ("Recipes", "Kitchen"), ("Tickets", "Outings"), ("Pressed", "Flowers")]))
    draw = [lambda i: f'<rect x="-40" y="-32" width="80" height="58" fill="none" stroke="{ink}" stroke-width="3"/><path d="M-40 -32 L0 4 L40 -32" fill="none" stroke="{ink}" stroke-width="3"/>',
            lambda i: sprig(0, 50, 100, ink, "#6f7d5c", i, red), lambda i: f'<path d="M0 -40 L10 -12 L40 -12 L16 6 L26 36 L0 18 L-26 36 L-16 6 L-40 -12 L-10 -12Z" fill="{red}" opacity=".8"/>']
    P.append(stamps_sheet("#d9c3a0", ["#efe6d2", "#e3d2b4", "#f2e8d5"], ink, draw, ["1c", "3c", "5c", "8c", "10c", "2c"]))
    lib = "".join(f'<div style="background:#efe6d2;border:1.5px solid {ink};color:{ink};padding:0.15in"><div class="type" style="text-align:center;font-size:8pt;letter-spacing:.2em;border-bottom:1.5px solid {ink};padding-bottom:4pt">PUBLIC LIBRARY</div>'
                  f'<table style="width:100%;border-collapse:collapse;margin-top:4pt;font-family:Liberation Mono;font-size:7pt">' + "<tr><th style='border:1px solid #2b2b2b'>DATE DUE</th><th style='border:1px solid #2b2b2b'>BORROWER</th></tr>" +
                  "".join("<tr><td style='border:1px solid #2b2b2b;height:0.24in'></td><td style='border:1px solid #2b2b2b'></td></tr>" for _ in range(7)) + "</table></div>" for _ in range(2))
    rec = "".join(f'<div class="type" style="background:#fbf8f0;color:{ink};font-size:8pt;padding:0.15in;line-height:1.6;clip-path:polygon(0 0,100% 0,100% 96%,95% 100%,90% 96%,85% 100%,80% 96%,75% 100%,70% 96%,65% 100%,60% 96%,55% 100%,50% 96%,45% 100%,40% 96%,35% 100%,30% 96%,25% 100%,20% 96%,15% 100%,10% 96%,5% 100%,0 96%)">'
                  f'<div style="text-align:center;font-weight:700">{n}</div><div style="text-align:center">THANK YOU · CALL AGAIN</div>- - - - - - - - - - - - - - -<br>{items}<br>- - - - - - - - - - - - - - -<br><b>TOTAL {tot}</b></div>'
                  for n, items, tot in [("CORNER GROCER", "TEA ........ 0.45<br>BREAD ...... 0.20<br>JAM ........ 0.35", "1.00"), ("HABERDASHERY", "BUTTONS .... 0.15<br>RIBBON ..... 0.30<br>THREAD ..... 0.10", "0.55")])
    P.append(f'<div class="page" style="background:#d9c3a0"><div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0.35in">{lib}{rec}</div></div>')
    tabs = "".join(f'<div style="background:{c};border-radius:0.25in 0.25in 0 0;color:{ink};display:flex;align-items:flex-start;justify-content:center;padding-top:0.12in" class="type"><b style="font-size:9pt;letter-spacing:.2em">{t}</b></div>'
                   for c, t in zip(["#e8dcc3", "#d9c3a0", "#c8a678", "#efe6d2", "#e3c7b8", "#d6dcc8"] * 2, ["JANUARY", "SPRING", "TRAVEL", "HOME", "GARDEN", "FAMILY", "NOTES", "IDEAS", "LISTS", "DREAMS", "RECIPES", "MISC"]))
    notes = "".join(f'<div style="background:#fbf8f0;padding:0.15in;box-shadow:0 1px 2px rgba(0,0,0,.2);background-image:repeating-linear-gradient(transparent 0 0.25in,{ink}33 0.25in calc(0.25in + 1px))"><div class="script" style="font-size:18pt;color:{red}">{w}</div></div>' for w in ["Note to self", "Don't forget", "Today", "List"])
    P.append(f'<div class="page" style="background:{cream}"><div class="grid" style="grid-template-columns:repeat(4,1fr);grid-template-rows:0.8in 0.8in 0.8in 1fr 1fr;gap:0.25in">{tabs}{notes}</div></div>')
    return BASE_CSS, P

# ---------------- JOURNALING CARDS ----------------
def journal_cards(size):
    pal = [("#f3e7cf", "#5a3b26", "#9c4f2e"), ("#1d2a4a", "#efe3c4", "#d4b062"), ("#e3ece6", "#2f4a3e", "#2f8f8a"), ("#f6e3ec", "#5b2440", "#b8326a"), ("#efe6d2", "#2b2b2b", "#a63d32"), ("#e4ecf7", "#22355a", "#4a73b0")]
    words = ["Today", "Grateful", "Remember", "Little things", "Dream big", "Notes", "Adventure", "This week", "Loved", "Wish list", "Hello", "Moments",
             "Make", "Slow down", "Collected", "Look up", "Home", "Plans", "Kindness", "Bloom", "Seasons", "Treasure", "Begin", "Someday"]
    cards = []
    for i, w in enumerate(words):
        bg, ink, acc = pal[i % len(pal)]; style = i % 4
        if style == 0: body = f'<div style="position:absolute;inset:1.05in 0.25in 0.3in;background:repeating-linear-gradient(transparent 0 0.3in,{ink}44 0.3in calc(0.3in + 1px))"></div>'
        elif style == 1: body = f'<div style="position:absolute;inset:1.05in 0.25in 0.3in;background:radial-gradient({ink}55 1px,transparent 1.3px) 0 0/0.2in 0.2in"></div>'
        elif style == 2: body = f'<div style="position:absolute;inset:1.05in 0.25in 0.3in;background:linear-gradient({ink}22 1px,transparent 1px) 0 0/0.2in 0.2in,linear-gradient(90deg,{ink}22 1px,transparent 1px) 0 0/0.2in 0.2in"></div>'
        else: body = f'<svg viewBox="0 0 300 300" style="position:absolute;left:0;right:0;bottom:0;width:100%;height:2.9in">{sprig(150, 300, 260, ink, acc, i, acc)}</svg>'
        cards.append(f'<div style="position:absolute;inset:0;background:{bg};padding:0.25in;color:{ink};border:0.12in solid {bg};box-shadow:inset 0 0 0 1.5px {acc}"><div class="script" style="font-size:30pt;color:{acc}">{w}</div>{body}</div>')
    P = [cards_sheet("#ffffff", cards[k:k + 4]) for k in range(0, 24, 4)]
    return BASE_CSS, P

PRODUCTS = {"tea-room-junk-journal-kit": tea_room, "night-garden-junk-journal-kit": night_garden, "vintage-ephemera-pack": ephemera, "journaling-cards-3x4": journal_cards}

if __name__ == "__main__":
    out = sys.argv[1]; only = sys.argv[2:] or list(PRODUCTS)
    for name in only:
        for size in ("letter", "a4"):
            css, pages = PRODUCTS[name](size)
            render(css, pages, size, f"{out}/{name}-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
        print(name, len(pages), "pages")
