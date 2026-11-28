"""Kids Valentine Cards for Class (batch 11, lane h/d): 12 original critter designs with kid-friendly puns, each in colour AND as a
colour-it-yourself version, 6 cards per page (3.5 x 2.9 in) with To / From lines and cut guides; classroom checklist; a make-your-own
page; treat bag toppers. All artwork drawn here (SVG). US Letter + A4."""
import math, sys
sys.path.insert(0, ".")
from render import render

INK, PINK, RED, CREAM = "#3a2733", "#f4a7b9", "#e0475b", "#fff7f4"
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Poppins, "Liberation Sans", sans-serif; color: #3a2733; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #fff; contain: strict; }
.round { font-family: "Archivo Black", Poppins, sans-serif; }
.script { font-family: "TeX Gyre Chorus", Lora, serif; }
.cut { outline: 1px dashed rgba(0,0,0,.32); outline-offset: 0.04in; }
svg { display: block; }
.foot { position: absolute; bottom: 0.16in; left: 0; right: 0; text-align: center; font-size: 6.5pt; color: #b8a8ae; letter-spacing: .14em; }
"""
BW = False  # set per render pass for outline mode

def C(col):  # colour or white (outline mode)
    return "#ffffff" if BW else col
def S(w=4):
    return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"' if BW else f'stroke="{INK}" stroke-width="{w * .6:.1f}" stroke-linejoin="round"'
def eyes(x1, x2, y, r=6):
    return f'<circle cx="{x1}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x2}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x1 + 2}" cy="{y - 2}" r="{r * .35:.1f}" fill="#fff"/><circle cx="{x2 + 2}" cy="{y - 2}" r="{r * .35:.1f}" fill="#fff"/>'
def cheeks(x1, x2, y): return "" if BW else f'<ellipse cx="{x1}" cy="{y}" rx="9" ry="6" fill="#f7a1a8" opacity=".8"/><ellipse cx="{x2}" cy="{y}" rx="9" ry="6" fill="#f7a1a8" opacity=".8"/>'
def smile(x, y, w=12): return f'<path d="M{x - w} {y} Q{x} {y + w * .9} {x + w} {y}" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
def heart(x, y, s, col):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 12 C-22 -4 -14 -24 0 -12 C14 -24 22 -4 0 12Z" fill="{C(col)}" {S(3)}/>'

# ---- 12 critters, each drawn in a 200 x 160 box ----
def bee():
    stripes = "".join(f'<rect x="{x}" y="50" width="14" height="80" fill="{INK}" clip-path="url(#bb)"/>' for x in (82, 112))
    return (f'<ellipse cx="80" cy="56" rx="26" ry="18" fill="{C("#dff1fb")}" {S()} transform="rotate(-20 80 56)"/><ellipse cx="118" cy="52" rx="26" ry="18" fill="{C("#dff1fb")}" {S()} transform="rotate(20 118 52)"/>'
            f'<defs><clipPath id="bb"><ellipse cx="100" cy="92" rx="52" ry="40"/></clipPath></defs><ellipse cx="100" cy="92" rx="52" ry="40" fill="{C("#ffd34d")}" {S()}/>{stripes}'
            f'<ellipse cx="100" cy="92" rx="52" ry="40" fill="none" {S()}/><path d="M152 92 l14 0" {S(4)}/>{eyes(64, 82, 86)}{cheeks(58, 88, 100)}{smile(72, 102, 8)}'
            f'<path d="M66 54 q-6 -20 -18 -22 M78 52 q2 -22 12 -26" stroke="{INK}" stroke-width="3" fill="none"/>')
def whale():
    return (f'<path d="M30 100 Q30 50 95 50 Q160 50 165 95 Q175 92 185 70 Q192 100 175 112 Q150 135 95 132 Q30 132 30 100Z" fill="{C("#7cc3e8")}" {S()}/>'
            f'<path d="M40 112 Q95 128 150 112 Q120 132 95 132 Q55 132 40 112Z" fill="{C("#d6eef9")}" {S(3)}/>{eyes(62, 86, 90)}{cheeks(56, 94, 104)}{smile(74, 106, 9)}'
            f'<path d="M80 48 q-4 -20 -18 -26 M80 48 q4 -22 20 -26 M80 48 v-24" stroke="{C("#7cc3e8") if not BW else INK}" stroke-width="4" fill="none" stroke-linecap="round"/>{heart(130, 30, .7, RED)}')
def owl():
    return (f'<path d="M50 140 Q40 60 70 40 L76 20 L92 38 Q100 36 108 38 L124 20 L130 40 Q160 60 150 140Z" fill="{C("#b08968")}" {S()}/>'
            f'<ellipse cx="100" cy="110" rx="32" ry="28" fill="{C("#f1dcc3")}" {S(3)}/><circle cx="82" cy="70" r="17" fill="#fff" {S(3)}/><circle cx="118" cy="70" r="17" fill="#fff" {S(3)}/>'
            f'{eyes(82, 118, 72, 7)}<path d="M94 84 L106 84 L100 96Z" fill="{C("#f2a93b")}" {S(3)}/>'
            + "".join(f'<path d="M{x} {y} q6 6 12 0" stroke="{INK}" stroke-width="2.5" fill="none"/>' for x, y in [(86, 104), (100, 112), (114, 104), (92, 122), (106, 122)]))
def dino():
    spikes = "".join(f'<path d="M{x} {62 - (x - 60) * .05} l8 -16 l8 16" fill="{C("#ffb3c1")}" {S(3)}/>' for x in (66, 84, 102, 120))
    return (f'{spikes}<path d="M40 130 Q36 60 100 56 Q150 56 158 110 Q186 112 190 132 Q170 140 150 136 L150 146 L128 146 L128 138 L74 138 L74 146 L52 146 L52 136 Q40 136 40 130Z" fill="{C("#8fd18b")}" {S()}/>'
            f'{eyes(62, 84, 90)}{cheeks(56, 92, 104)}{smile(74, 106, 9)}<path d="M100 120 q10 -8 22 0" stroke="{INK}" stroke-width="2.5" fill="none" opacity=".4"/>')
def cactus():
    return (f'<path d="M70 120 h60 l-8 32 h-44z" fill="{C("#e9876b")}" {S()}/><rect x="64" y="112" width="72" height="14" rx="4" fill="{C("#f0a089")}" {S()}/>'
            f'<path d="M84 112 V50 Q84 28 100 28 Q116 28 116 50 V112Z" fill="{C("#6fbf73")}" {S()}/>'
            f'<path d="M84 86 H70 Q60 86 60 76 V60 Q60 52 67 52 Q74 52 74 60 V72 H84" fill="{C("#6fbf73")}" {S()}/>'
            f'<path d="M116 78 H130 Q140 78 140 68 V54 Q140 46 133 46 Q126 46 126 54 V64 H116" fill="{C("#6fbf73")}" {S()}/>'
            f'{eyes(93, 107, 66, 5)}{cheeks(88, 112, 76)}{smile(100, 78, 6)}{heart(100, 22, .7, RED)}')
def rocket():
    return (f'<path d="M100 18 Q130 40 130 92 L130 120 H70 V92 Q70 40 100 18Z" fill="{C("#ffffff")}" {S()}/><path d="M100 18 Q120 32 126 52 H74 Q80 32 100 18Z" fill="{C(RED)}" {S(3)}/>'
            f'<path d="M70 96 L48 126 L70 120Z M130 96 L152 126 L130 120Z" fill="{C(RED)}" {S(3)}/><circle cx="100" cy="78" r="15" fill="{C("#9fd3f0")}" {S(3)}/>'
            f'<path d="M82 120 Q90 150 100 158 Q110 150 118 120Z" fill="{C("#ffcc4d")}" {S(3)}/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{INK if BW else "#ffcc4d"}"/>' for x, y in [(30, 40), (170, 30), (160, 90), (40, 100), (176, 140)]))
def cat():
    return (f'<path d="M48 70 L56 26 L84 50 Q100 46 116 50 L144 26 L152 70 Q162 130 100 134 Q38 130 48 70Z" fill="{C("#f6b26b")}" {S()}/>'
            f'<path d="M58 40 L62 58 L74 50Z M142 40 L138 58 L126 50Z" fill="{C("#f7c6c9")}"/>{eyes(82, 118, 84, 7)}{cheeks(74, 126, 100)}'
            f'<path d="M96 96 L104 96 L100 102Z" fill="{C("#e0607a")}"/><path d="M100 102 q-6 8 -12 4 M100 102 q6 8 12 4" stroke="{INK}" stroke-width="3" fill="none"/>'
            f'<path d="M60 98 L36 94 M60 104 L36 108 M140 98 L164 94 M140 104 L164 108" stroke="{INK}" stroke-width="2.5"/>{heart(150, 140, .7, RED)}')
def donut():
    sp = "".join(f'<rect x="{x}" y="{y}" width="10" height="4" rx="2" fill="{c if not BW else "#fff"}" {S(1.5) if BW else ""} transform="rotate({a} {x} {y})"/>'
                 for x, y, a, c in [(62, 60, 20, "#7cc3e8"), (90, 48, -30, "#ffd34d"), (124, 54, 40, "#8fd18b"), (140, 82, -10, "#7cc3e8"), (58, 92, 60, "#ffd34d"), (128, 108, 15, "#ffffff")])
    return (f'<circle cx="100" cy="88" r="58" fill="{C("#e0b07a")}" {S()}/><path d="M48 80 Q50 34 100 32 Q152 34 154 82 Q150 110 132 104 Q118 120 100 112 Q80 124 66 108 Q50 112 48 80Z" fill="{C("#f59ab0")}" {S(3)}/>'
            f'<circle cx="100" cy="88" r="16" fill="#fff" {S(3)}/>{sp}{eyes(80, 120, 120, 5)}{smile(100, 128, 7)}')
def taco():
    return (f'<path d="M30 130 Q30 50 100 50 Q170 50 170 130Z" fill="{C("#f6c453")}" {S()}/>'
            f'<path d="M40 104 Q50 80 64 92 Q74 70 90 86 Q102 66 116 84 Q130 70 140 90 Q154 80 160 104" fill="{C("#7cc576")}" {S(3)}/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{C("#e8505b")}" {S(2.5)}/>' for x, y in [(70, 98), (104, 92), (138, 100)])
            + f'{eyes(82, 118, 114, 6)}{cheeks(74, 126, 124)}{smile(100, 122, 8)}')
def octopus():
    legs = "".join(f'<path d="M{x} 100 Q{x + d} 130 {x + d * 2} 146" stroke="{INK}" stroke-width="{"20" if not BW else "22"}" fill="none" stroke-linecap="round"/>'
                   f'<path d="M{x} 100 Q{x + d} 130 {x + d * 2} 146" stroke="{C("#b79cf0")}" stroke-width="{"16" if not BW else "16"}" fill="none" stroke-linecap="round"/>'
                   for x, d in [(66, -12), (88, -5), (112, 5), (134, 12)])
    return (f'{legs}<path d="M50 104 Q46 30 100 30 Q154 30 150 104Z" fill="{C("#b79cf0")}" {S()}/>{eyes(84, 116, 74, 7)}{cheeks(74, 126, 88)}{smile(100, 88, 9)}'
            f'{heart(40, 40, .6, RED)}{heart(166, 52, .5, RED)}')
def sloth():
    return (f'<path d="M10 40 H190" stroke="{INK if BW else "#8a5a3c"}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M64 40 Q60 60 70 70 M136 40 Q140 60 130 70" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<path d="M64 40 Q60 60 70 70 M136 40 Q140 60 130 70" stroke="{C("#b6997d")}" stroke-width="8" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="100" cy="100" rx="46" ry="42" fill="{C("#b6997d")}" {S()}/><ellipse cx="100" cy="102" rx="34" ry="28" fill="{C("#efe0cc")}" {S(3)}/>'
            f'<ellipse cx="86" cy="98" rx="11" ry="8" fill="{C("#6b4f3a")}" transform="rotate(-20 86 98)"/><ellipse cx="114" cy="98" rx="11" ry="8" fill="{C("#6b4f3a")}" transform="rotate(20 114 98)"/>'
            f'{eyes(87, 113, 98, 4)}<ellipse cx="100" cy="108" rx="5" ry="3.5" fill="{INK}"/>{smile(100, 114, 7)}')
def avocado():
    return (f'<path d="M100 22 Q138 22 146 80 Q156 146 100 148 Q44 146 54 80 Q62 22 100 22Z" fill="{C("#5f8f3e")}" {S()}/>'
            f'<path d="M100 32 Q130 32 136 82 Q144 136 100 138 Q56 136 64 82 Q70 32 100 32Z" fill="{C("#d9eaa0")}"/>'
            f'<circle cx="100" cy="106" r="22" fill="{C("#a86c45")}" {S(3)}/>{eyes(86, 114, 70, 5)}{cheeks(78, 122, 80)}{smile(100, 80, 7)}')
CRITTERS = [(bee, "You're bee-utiful!", "#fff4c7"), (whale, "Whale you be my Valentine?", "#e2f3fb"), (owl, "Owl always be your friend", "#f6ebdd"),
            (dino, "You're dino-mite!", "#e7f6e3"), (cactus, "I'm stuck on you", "#fde7e2"), (rocket, "You're out of this world", "#e9e6fb"),
            (cat, "You're purr-fect!", "#fff0e0"), (donut, "Donut forget you're awesome", "#fde6ee"), (taco, "Taco 'bout a great friend!", "#fff6d8"),
            (octopus, "Octo-pals forever", "#efe8fd"), (sloth, "Hanging out with you is the best", "#f3ece4"), (avocado, "We make a great pear... avo-pear!", "#eef6dc")]
CRITTERS[11] = (avocado, "You're guac-tastic!", "#eef6dc")

def card(i):
    fn, txt, bg = CRITTERS[i]
    bgc = "#ffffff" if BW else bg
    border = f'box-shadow:inset 0 0 0 3px {INK if BW else RED}' if True else ""
    hearts = "" if BW else "".join(f'<path transform="translate({x} {y}) scale(.35)" d="M0 12 C-22 -4 -14 -24 0 -12 C14 -24 22 -4 0 12Z" fill="{PINK}" opacity=".6"/>' for x, y in [(14, 14), (186, 18), (12, 150), (188, 146)])
    return (f'<div class="cut" style="background:{bgc};border-radius:12px;{border};position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;padding:0.12in 0.14in 0.1in">'
            f'<svg viewBox="0 0 200 160" style="width:2.5in;height:1.72in;flex:none">{hearts}{fn()}</svg>'
            f'<div class="round" style="font-size:12.5pt;line-height:1.15;text-align:center;margin-top:1pt;color:{INK if BW else RED}">{txt}</div>'
            f'<div style="width:100%;margin-top:auto;font-size:8pt;display:flex;flex-direction:column;gap:3pt">'
            f'<div style="display:flex;gap:4pt;align-items:flex-end"><b>To:</b><span style="flex:1;border-bottom:1.2px solid {INK}"></span></div>'
            f'<div style="display:flex;gap:4pt;align-items:flex-end"><b>From:</b><span style="flex:1;border-bottom:1.2px solid {INK}"></span></div></div></div>')

def cards_page(start, label):
    cells = "".join(card(i) for i in range(start, start + 6))
    return (f'<div class="page"><div style="position:absolute;left:0;right:0;top:0.22in;text-align:center;font-size:7pt;letter-spacing:.25em;color:#b8a8ae">{label}</div>'
            f'<div style="position:absolute;inset:0.5in 0.55in 0.45in;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:0.22in">{cells}</div>'
            f'<div class="foot">PURL &amp; PAPER · CLASSROOM VALENTINES · CUT ON THE DASHED LINES</div></div>')

def cover():
    global BW
    BW = False
    mini = "".join(f'<svg viewBox="0 0 200 160" style="width:100%;background:{bg};border-radius:12px;padding:6px">{fn()}</svg>' for fn, _, bg in CRITTERS)
    return (f'<div class="page" style="background:{CREAM}">'
            f'<div style="position:absolute;left:0.7in;right:0.7in;top:0.6in;text-align:center"><div style="font-size:9pt;letter-spacing:.35em;color:{RED};font-weight:600">PRINTABLE · FOR THE WHOLE CLASS</div>'
            f'<div class="round" style="font-size:40pt;line-height:1.05;color:{INK};margin-top:8pt">Valentine<br>Cards for Kids</div>'
            f'<div style="font-size:11pt;margin-top:8pt;color:#6b5560">12 punny critters · colour version + colour-it-yourself version · To / From on every card</div></div>'
            f'<div style="position:absolute;left:0.8in;right:0.8in;top:3.35in;display:grid;grid-template-columns:repeat(4,1fr);gap:0.14in">{mini}</div>'
            f'<div style="position:absolute;left:0.8in;right:0.8in;bottom:0.65in;font-size:9.5pt;line-height:1.55;color:#5a4650">'
            f'<b>How to use:</b> print at 100% / actual size on white cardstock (or plain paper). Pages 2-3 are colour, pages 4-5 are the same cards to colour in. '
            f'Cut on the dashed lines, write To and From, and tape on a lollipop, pencil or sticker if you like. The class checklist helps you make sure nobody is left out. '
            f'Treat bag toppers fold over a small bag and staple.</div><div class="foot">PURL &amp; PAPER · CLASSROOM VALENTINES</div></div>')

def checklist():
    rows = "".join(f'<div style="display:flex;gap:8pt;align-items:center;height:0.33in;border-bottom:1px solid #e7d6dc"><span style="width:13pt;height:13pt;border:1.8px solid {RED};border-radius:4px"></span>'
                   f'<span style="flex:1"></span><span style="width:13pt;height:13pt;border:1.8px solid {PINK};border-radius:50%"></span></div>' for _ in range(16))
    return (f'<div class="page" style="background:{CREAM}"><div style="position:absolute;left:0.8in;right:0.8in;top:0.6in;text-align:center">'
            f'<div class="round" style="font-size:28pt;color:{INK}">My class Valentine list</div><div style="font-size:10pt;color:#6b5560;margin-top:4pt">Write every name, tick the square when the card is made and the circle when it\'s given</div></div>'
            f'<div style="position:absolute;left:0.8in;right:0.8in;top:1.75in;display:grid;grid-template-columns:1fr 1fr;gap:0 0.45in">{rows}{rows}</div>'
            f'<svg viewBox="0 0 200 160" style="position:absolute;right:0.5in;bottom:0.35in;width:1.5in">{owl()}</svg><div class="foot">PURL &amp; PAPER · CLASSROOM VALENTINES</div></div>')

def make_own():
    cells = "".join(f'<div class="cut" style="border-radius:12px;box-shadow:inset 0 0 0 3px {RED};padding:0.15in;display:flex;flex-direction:column">'
                    f'<div style="flex:1;border:2px dashed #e8c3cd;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:8pt;color:#c9a5b0">draw your own Valentine here</div>'
                    f'<div style="font-size:8pt;display:flex;flex-direction:column;gap:3pt;margin-top:6pt"><div style="display:flex;gap:4pt"><b>To:</b><span style="flex:1;border-bottom:1.2px solid {INK}"></span></div>'
                    f'<div style="display:flex;gap:4pt"><b>From:</b><span style="flex:1;border-bottom:1.2px solid {INK}"></span></div></div></div>' for _ in range(6))
    return (f'<div class="page"><div style="position:absolute;left:0;right:0;top:0.22in;text-align:center;font-size:7pt;letter-spacing:.25em;color:#b8a8ae">MAKE YOUR OWN</div>'
            f'<div style="position:absolute;inset:0.5in 0.55in 0.45in;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:0.22in">{cells}</div>'
            f'<div class="foot">PURL &amp; PAPER · CLASSROOM VALENTINES</div></div>')

def toppers():
    global BW
    BW = False
    cells = ""
    for i in (0, 3, 6, 9):
        fn, txt, bg = CRITTERS[i]
        cells += (f'<div class="cut" style="background:{bg};border-radius:10px;position:relative;text-align:center">'
                  f'<div style="position:absolute;left:0;right:0;top:50%;border-top:1.5px dashed #0004"></div><div style="position:absolute;right:6px;top:calc(50% - 13px);font-size:6pt;color:#0006">fold</div>'
                  f'<div style="position:absolute;left:0;right:0;top:52%;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 0.15in">'
                  f'<svg viewBox="0 0 200 160" style="width:1.5in">{fn()}</svg><div class="round" style="font-size:11pt;color:{RED};line-height:1.15">{txt}</div>'
                  f'<div style="font-size:8pt;margin-top:4pt">From: ____________</div></div></div>')
    return (f'<div class="page"><div style="position:absolute;left:0;right:0;top:0.22in;text-align:center;font-size:7pt;letter-spacing:.25em;color:#b8a8ae">TREAT BAG TOPPERS · FOLD OVER A 4 IN BAG AND STAPLE</div>'
            f'<div style="position:absolute;inset:0.5in 0.55in 0.45in;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0.25in">{cells}</div>'
            f'<div class="foot">PURL &amp; PAPER · CLASSROOM VALENTINES</div></div>')

def build():
    global BW
    pages = [cover()]
    BW = False; pages += [cards_page(0, "COLOUR · 1 OF 2"), cards_page(6, "COLOUR · 2 OF 2")]
    BW = True; pages += [cards_page(0, "COLOUR IT YOURSELF · 1 OF 2"), cards_page(6, "COLOUR IT YOURSELF · 2 OF 2")]
    BW = False; pages += [toppers(), make_own(), checklist()]
    return CSS, pages

if __name__ == "__main__":
    out = sys.argv[1]
    for size in ("letter", "a4"):
        css, pages = build()
        render(css, pages, size, f"{out}/kids-valentine-cards-classroom-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print("pages", len(pages))
