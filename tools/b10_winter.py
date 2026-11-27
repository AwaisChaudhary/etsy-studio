"""Winter Cottage junk journal kit (batch 10, lane c). 16 pages, all artwork drawn here from scratch (SVG + generated textures):
frosty papers, a snowy cottage plate, winter botanicals, cocoa recipe cards, a Nordic knit pattern paper, flannel plaid, ledger,
lined letter, tags, labels, tickets, stamps, a winter list page and journaling cards. US Letter + A4."""
import math, random, sys
sys.path.insert(0, ".")
from render import render
import textures as T
from kits import (BASE_CSS, leaf, sprig, fern, tex_page, ledger, lined_letter, pattern_page, tags_sheet, labels_sheet, tickets_sheet,
                  stamps_sheet, cards_sheet, intro_page, SIZES_NOTE)
from kits2 import pine, snowflake, holly, mitten, star

INK, NAVY, RED, PINE_, BERRY, FROST, CREAM, WOOD = "#2c3a4f", "#33476b", "#9e3a3a", "#3f6b5a", "#b23b3b", "#dfe8ef", "#f5f1e8", "#7a5a3e"
CSS = BASE_CSS + ".page{contain:strict}"

def snow_dots(w, h, n, seed, col="#ffffff", rmax=4.5):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.uniform(1, rmax):.1f}" fill="{col}" opacity="{r.uniform(.5, .95):.2f}"/>' for _ in range(n))

def cottage(cx, by, s):
    """A little snowy cottage: walls, snow-heavy roof, chimney smoke, glowing windows, door with wreath."""
    g = (f'<g transform="translate({cx} {by}) scale({s})">'
         f'<rect x="-120" y="-150" width="240" height="150" fill="#c9875d"/>'
         f'<g stroke="#a86c45" stroke-width="2">' + "".join(f'<line x1="-120" y1="{-150 + k * 18}" x2="120" y2="{-150 + k * 18}"/>' for k in range(1, 9)) + '</g>'
         f'<rect x="70" y="-250" width="28" height="70" fill="#8a5a3c"/><path d="M66 -252 h36 q6 -10 -6 -14 h-24 q-12 4 -6 14z" fill="#fff"/>'
         f'<path d="M84 -270 q-18 -24 4 -44 q22 -20 0 -46" stroke="#e9eef3" stroke-width="10" fill="none" stroke-linecap="round" opacity=".85"/>'
         f'<polygon points="-150,-145 0,-265 150,-145" fill="#6d3f37"/>'
         f'<path d="M-162 -140 Q-150 -158 -138 -150 L0 -270 L138 -150 Q152 -160 162 -140 Q150 -128 130 -136 Q110 -124 90 -134 Q60 -122 30 -134 Q0 -122 -30 -134 Q-60 -122 -90 -134 Q-112 -124 -130 -136 Q-150 -128 -162 -140Z" fill="#ffffff"/>'
         f'<rect x="-22" y="-92" width="44" height="92" rx="20" fill="#3d5a76"/><circle cx="12" cy="-46" r="3" fill="#e8c46b"/>'
         f'<circle cx="0" cy="-74" r="14" fill="none" stroke="{PINE_}" stroke-width="7"/><circle cx="-6" cy="-62" r="3" fill="{BERRY}"/><circle cx="6" cy="-62" r="3" fill="{BERRY}"/>'
         + "".join(f'<rect x="{x}" y="-118" width="46" height="46" fill="#f6d37a"/><rect x="{x}" y="-118" width="46" height="46" fill="none" stroke="#fff" stroke-width="5"/>'
                   f'<line x1="{x + 23}" y1="-118" x2="{x + 23}" y2="-72" stroke="#fff" stroke-width="4"/><line x1="{x}" y1="-95" x2="{x + 46}" y2="-95" stroke="#fff" stroke-width="4"/>'
                   f'<path d="M{x - 6} -70 h58 q-6 8 -29 8 q-23 0 -29 -8z" fill="#fff"/>' for x in (-98, 52))
         + '<path d="M-200 0 Q-100 -14 0 -4 Q100 -16 220 0 L220 30 L-200 30Z" fill="#ffffff"/></g>')
    return g

def scene_plate(W, H):
    sky = (f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22324d"/><stop offset=".7" stop-color="#5d7393"/>'
           f'<stop offset="1" stop-color="#c7d4e0"/></linearGradient></defs><rect width="1000" height="1300" fill="url(#sky)"/>')
    hills = ('<path d="M0 900 Q250 820 520 880 T1000 850 V1300 H0Z" fill="#e8eef4"/><path d="M0 1000 Q300 930 600 990 T1000 970 V1300 H0Z" fill="#ffffff"/>')
    trees = "".join(pine(x, y, h, c, i) for i, (x, y, h, c) in enumerate([(90, 960, 330, "#2f5246"), (190, 930, 260, "#3e6656"), (820, 940, 340, "#2f5246"),
                                                                           (920, 975, 280, "#3e6656"), (700, 905, 200, "#46705f"), (330, 900, 180, "#46705f")]))
    snowcaps = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="9" fill="#fff" opacity=".9"/>' for x, y, w in [(90, 800, 40), (190, 830, 32), (820, 790, 44), (920, 860, 34)])
    moon = '<circle cx="770" cy="210" r="70" fill="#f5ecd2"/><circle cx="800" cy="190" r="62" fill="#3a4c6a" opacity=".25"/>'
    stars_ = "".join(star(x, y, r, "#f5ecd2") for x, y, r in [(150, 160, 9), (300, 90, 6), (460, 200, 7), (600, 120, 5), (900, 330, 6), (240, 330, 5)])
    body = (f'{sky}{moon}{stars_}{hills}{trees}{snowcaps}{cottage(500, 1010, 1.25)}'
            f'<path d="M500 1040 Q470 1120 520 1200 Q560 1260 520 1300" stroke="#dfe7ef" stroke-width="40" fill="none"/>{snow_dots(1000, 1300, 260, 7)}')
    return (f'<div class="page" style="background:{CREAM}"><div style="position:absolute;inset:0.55in 0.55in 1.5in;border:10px solid #fffdf8;box-shadow:0 0 0 1.5px {INK}33">'
            f'<svg viewBox="0 0 1000 1300" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%">{body}</svg></div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0.55in;text-align:center;color:{INK}"><div class="script" style="font-size:40pt;line-height:1">Winter Cottage</div>'
            f'<div class="type" style="font-size:8.5pt;letter-spacing:.3em;margin-top:4pt">PLATE I · SNOWFALL AT DUSK</div></div></div>')

def botanicals(uri):
    sp = []
    sp.append(pine(200, 1000, 760, "#3f6b5a", 31))
    sp.append(f'<g>{"".join(leaf(560 + 10 * k, 980 - k * 52, 46, -150 + (k % 2) * 120, "#6f8f7a") for k in range(15))}'
              f'<path d="M560 1000 Q600 640 630 230" stroke="{WOOD}" stroke-width="5" fill="none"/></g>')
    berries = "".join(f'<circle cx="{560 + 10 * k + (14 if k % 2 else -14)}" cy="{965 - k * 52}" r="11" fill="{BERRY}"/>' for k in range(0, 15, 2))
    sp.append(berries)
    sp.append(holly(790, 560, 3.4, "#2f5d48", BERRY)); sp.append(holly(770, 780, 2.6, "#3f6b5a", BERRY))
    sp.append(fern(1030, 1010, 380, "#7c9a86", 5))
    labels = [(200, 1060, "Picea abies"), (590, 1060, "Ilex verticillata"), (840, 1060, "Ilex aquifolium")]
    lab = "".join(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="TeX Gyre Chorus, serif" font-size="40" fill="{INK}">{t}</text>' for x, y, t in labels)
    return tex_page(uri, f'<svg class="layer" viewBox="0 180 1100 920" preserveAspectRatio="xMidYMid meet" style="padding:1.2in 0.3in 0.4in">{"".join(sp)}{lab}</svg>'
                         f'<div class="pad"><div class="script" style="color:{INK};font-size:38pt">Winter greenery</div><div class="type" style="color:{INK};font-size:9pt;letter-spacing:.2em">BOTANICAL STUDY · PLATE II</div></div>')

def nordic_pattern():
    """A Fair Isle style knit pattern paper: rows of little V-stitches forming bands of snowflakes, hearts and pines."""
    cell = 12; cols, rows = 24, 40
    motif = {  # rows of 24 chars per band; x = contrast stitch
        "flake": ["..........x...........x.", ".x...x...xxx...x...x..xx", "..x.x...x.x.x...x.x...x.", "...x...xxxxxxx...x...x..", "..x.x...x.x.x...x.x...x.",
                  ".x...x...xxx...x...x..xx", "..........x...........x."],
        "pine": ["..........x...........x.", ".........xxx.........xxx", "........xxxxx.......xxxx", ".........xxx.........xxx", "........xxxxx.......xxxx", "...........x...........x"],
        "dots": ["x.x.x.x.x.x.x.x.x.x.x.x.", "........................", ".x.x.x.x.x.x.x.x.x.x.x.x"]}
    bands = [("dots", "#f5f1e8", RED), ("flake", "#f5f1e8", NAVY), ("dots", "#f5f1e8", RED), ("pine", NAVY, "#f5f1e8"), ("dots", "#f5f1e8", RED), ("flake", RED, "#f5f1e8")]
    y = 0; out = []
    for name, bg, fg in bands * 2:
        rowsm = motif[name]; hgt = (len(rowsm) + 2) * cell
        out.append(f'<rect x="0" y="{y}" width="{cols * cell}" height="{hgt}" fill="{bg}"/>')
        for ri, row in enumerate(rowsm):
            for ci, ch in enumerate(row):
                if ch == "x":
                    x0, y0 = ci * cell, y + (ri + 1) * cell
                    out.append(f'<path d="M{x0 + 1} {y0} L{x0 + 6} {y0 + 10} L{x0 + 11} {y0}" stroke="{fg}" stroke-width="4" fill="none" stroke-linejoin="round"/>')
        y += hgt
    pat = f'<pattern id="nk" width="{cols * cell}" height="{y}" patternUnits="userSpaceOnUse">{"".join(out)}</pattern>'
    return pattern_page(pat, "nk", "#f5f1e8")

def plaid():
    p = (f'<pattern id="pl" width="160" height="160" patternUnits="userSpaceOnUse"><rect width="160" height="160" fill="#8e3333"/>'
         f'<rect y="50" width="160" height="60" fill="#2c3a4f" opacity=".55"/><rect x="50" width="60" height="160" fill="#2c3a4f" opacity=".55"/>'
         f'<rect y="76" width="160" height="8" fill="#e9dcc0" opacity=".55"/><rect x="76" width="8" height="160" fill="#e9dcc0" opacity=".55"/>'
         f'<rect y="20" width="160" height="4" fill="#1d2636" opacity=".5"/><rect x="20" width="4" height="160" fill="#1d2636" opacity=".5"/>'
         f'<rect y="136" width="160" height="4" fill="#1d2636" opacity=".5"/><rect x="136" width="4" height="160" fill="#1d2636" opacity=".5"/></pattern>')
    return pattern_page(p, "pl", "#8e3333")

def frost_page(uri, seed):
    flakes = "".join(snowflake(x, y, r, "#ffffff") for x, y, r in random.Random(seed).sample([(a, b, c) for a in range(80, 1100, 180) for b in range(80, 1500, 200) for c in (22, 34, 46)], 26))
    return tex_page(uri, f'<svg class="layer" viewBox="0 0 1100 1500" preserveAspectRatio="xMidYMid slice" style="opacity:.7">{flakes}{snow_dots(1100, 1500, 300, seed)}</svg>')

def cocoa_cards(uri):
    recipes = [("Midnight Hot Cocoa", "2 cups milk · 3 tbsp cocoa · 3 tbsp sugar · pinch of salt · splash of vanilla. Whisk over low heat until steaming. Top with cream."),
               ("Cinnamon Snow Buns", "Soft dough, rolled thin, brushed with butter, cinnamon and brown sugar. Roll, slice, rise, bake. Ice while warm."),
               ("Cottage Stew", "Onion, carrots, potatoes, a bay leaf and a good stock. Simmer low for an afternoon while the snow falls."),
               ("Gingerbread Loaf", "Treacle, brown sugar, butter, ginger and a little orange zest. Bake low until the kitchen smells like December.")]
    cards = "".join(f'<div style="background:#fbf8f1;border:2px solid {NAVY};padding:0.2in 0.25in;color:{INK};box-shadow:0 2px 3px rgba(0,0,0,.15);position:relative">'
                    f'<div class="type" style="font-size:7pt;letter-spacing:.25em;color:{RED}">FROM THE COTTAGE KITCHEN OF ____________</div>'
                    f'<div class="script" style="font-size:24pt;margin:6pt 0;border-bottom:1.5px solid {NAVY}">{t}</div>'
                    f'<div class="type" style="font-size:9pt;line-height:0.3in;background:repeating-linear-gradient(transparent 0 calc(0.3in - 1px), {INK}33 calc(0.3in - 1px) 0.3in)">{b}</div>'
                    f'<svg viewBox="-60 -60 120 120" style="position:absolute;right:0.15in;bottom:0.15in;width:0.7in;opacity:.5">{snowflake(0, 0, 50, NAVY)}</svg></div>' for t, b in recipes)
    return tex_page(uri, f'<div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0.3in">{cards}</div>')

def winter_list(uri):
    items = ["Build a snowman", "Bake something warm", "A long walk in the snow", "Read by the fire", "Hot cocoa with marshmallows", "Watch the first snowfall",
             "Knit something cosy", "Make paper snowflakes", "Feed the birds", "Write a letter to someone", "Ice skating", "Stargaze on a clear night"]
    rows = "".join(f'<div style="display:flex;align-items:center;gap:10pt;border-bottom:1px dotted {INK}88;padding:6.5pt 0"><div style="width:14pt;height:14pt;border:1.5px solid {NAVY};border-radius:3px;flex:none"></div>'
                   f'<div style="font-size:13pt">{it}</div></div>' for it in items)
    rows += "".join(f'<div style="display:flex;align-items:center;gap:10pt;border-bottom:1px dotted {INK}88;padding:6.5pt 0;height:26pt"><div style="width:14pt;height:14pt;border:1.5px solid {NAVY};border-radius:3px;flex:none"></div></div>' for _ in range(4))
    return tex_page(uri, f'<div class="pad" style="inset:0.75in 0.95in;color:{INK};border:3px double {NAVY};padding:0.4in 0.55in;background:rgba(251,248,241,.6)">'
                         f'<div style="text-align:center"><div class="type" style="font-size:8pt;letter-spacing:.35em">THE COTTAGE · WINTER</div><div class="script" style="font-size:50pt;line-height:1.1">Winter List</div>'
                         f'<div class="type" style="font-size:8pt;letter-spacing:.3em;margin-bottom:10pt">LITTLE THINGS TO DO WHILE IT SNOWS</div></div>{rows}</div>')

def build(size):
    W, H = (1275, 1650) if size == "letter" else (1240, 1754)
    tA = T.tea(W, H, 41, base=(226, 232, 236), dark=(120, 140, 160), rings=0, strength=.8)
    tB = T.tea(W, H, 42, base=(236, 230, 218), dark=(150, 128, 104), rings=1, strength=.8)
    tC = T.tea(W, H, 43, base=(214, 224, 232), dark=(90, 110, 140), rings=0, strength=.9)
    tD = T.tea(W, H, 44, base=(242, 238, 230), dark=(170, 150, 120), rings=0, strength=.55)
    P = []
    art = (f'<svg viewBox="0 0 400 330" style="position:absolute;right:0.35in;bottom:1.35in;width:3.8in">'
           f'{pine(70, 320, 230, PINE_, 4)}{pine(340, 320, 190, "#4f7a69", 5)}{cottage(205, 300, .62)}{snow_dots(400, 330, 70, 3, NAVY, 3)}</svg>')
    P.append(intro_page(CREAM, INK, RED, "Winter Cottage", "Frosty papers, a snowy cottage at dusk, winter greenery, cocoa recipes and Nordic knits for cosy winter pages.",
                        ["Frosted and snow-speckled papers, a ledger page", "Snowy cottage plate and a winter greenery plate", "Cottage kitchen recipe cards",
                         "Nordic knit and flannel plaid pattern papers", "Lined letter paper and a Winter List page", "Tags, labels, tickets and postage stamps", "Journaling cards (3 × 4 in)"],
                        SIZES_NOTE, art))
    P.append(frost_page(tA, 1)); P.append(scene_plate(W, H)); P.append(tex_page(tB)); P.append(ledger(tD, INK, RED))
    P.append(botanicals(tD)); P.append(cocoa_cards(tB)); P.append(nordic_pattern()); P.append(plaid()); P.append(frost_page(tC, 2))
    P.append(lined_letter(tD, INK, "Dear winter,"))
    P.append(winter_list(tA))
    P.append(tags_sheet("#dfe6ec", "#fbf8f1", INK, NAVY, ["Snow day", "Cosy", "Hygge", "Warm wishes", "Frost", "Fireside", "Hello winter", "Notes"]))
    P.append(labels_sheet("#e9e1d3", "#fbf8f1", INK, RED, [("Cocoa", "Pantry"), ("Cinnamon", "Spice"), ("Pinecones", "Gathered"), ("Firewood", "Dry"), ("Wool", "Pure"),
                                                          ("Marshmallows", "Treats"), ("Peppermint", "Tea"), ("Snowflakes", "No. 1"), ("Clementines", "Fresh"), ("Candles", "Beeswax"),
                                                          ("Mittens", "Lost & found"), ("Gingerbread", "Bakery")]))
    P.append(tickets_sheet("#dfe6ec", ["#f2ece0", "#e4d2cf", "#d8e2e9"], INK, [("Frozen Lake", "SKATING", "Admit one · until dusk"), ("Winter Fair", "ADMIT TWO", "Village green · Saturday"),
                                                                            ("Sleigh Ride", "SEAT 3", "Departs the old mill at four"), ("Mountain Rail", "RETURN", "Snowline express"),
                                                                            ("Candlelight Concert", "ROW B", "St. Bride's · 7 o'clock"), ("Bakery", "RECEIPT", "1 loaf · 4 cinnamon buns"),
                                                                            ("Ski Lodge", "ROOM 12", "Two nights · breakfast"), ("Post Office", "PARCEL", "With care · do not bend")]))
    draw = [lambda i: snowflake(0, 0, 44, NAVY), lambda i: pine(0, 52, 100, PINE_, i), lambda i: cottage(0, 40, .32), lambda i: mitten(0, 0, 1.3, RED, "#f2ece0"),
            lambda i: holly(-6, 0, 1.4, "#2f5d48", BERRY), lambda i: star(0, 0, 40, "#c9a24a")]
    P.append(stamps_sheet("#e9e1d3", ["#f2ece0", "#d8e2e9", "#e4d2cf"], INK, draw, ["1d", "2d", "3d", "½d", "4d", "6d"]))
    jc = []
    for i, (w, bg) in enumerate([("Snow day", "#fbf8f1"), (None, "#22324d"), ("Hello winter", "#f2ece0"), ("Remember", "#e7edf2")]):
        if w: jc.append(f'<div style="position:absolute;inset:0;background:{bg};padding:0.25in;color:{INK}"><div class="script" style="font-size:30pt">{w}</div>'
                        f'<div style="position:absolute;inset:1in 0.25in 0.3in;background:repeating-linear-gradient(transparent 0 0.3in, {INK}44 0.3in calc(0.3in + 1px))"></div></div>')
        else: jc.append(f'<div style="position:absolute;inset:0;background:{bg}"><svg viewBox="0 0 300 400" style="width:100%;height:100%">'
                        f'{pine(70, 400, 220, "#3e6656", 8)}{pine(240, 400, 180, "#2f5246", 9)}{cottage(150, 380, .45)}{snow_dots(300, 400, 80, 4)}{star(230, 60, 10, "#f5ecd2")}</svg></div>')
    P.append(cards_sheet("#dfe6ec", jc))
    return CSS, P

if __name__ == "__main__":
    out = sys.argv[1]
    for size in ("letter", "a4"):
        css, pages = build(size)
        render(css, pages, size, f"{out}/winter-cottage-junk-journal-kit-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print("pages", len(pages))
