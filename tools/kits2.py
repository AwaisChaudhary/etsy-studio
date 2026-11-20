"""Christmas gift tags printable (batch 2). All artwork drawn here from scratch as SVG."""
import math, random, sys
sys.path.insert(0, ".")
from render import render

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Lora, serif; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #fff; }
.script { font-family: "TeX Gyre Chorus", Lora, serif; }
.sans { font-family: Poppins, sans-serif; }
.grid { position: absolute; inset: 0.45in 0.4in; display: grid; gap: 0.22in; }
.cut { outline: 1px dashed rgba(0,0,0,.28); outline-offset: 0.05in; }
svg { display: block; }
.foot { position: absolute; bottom: 0.18in; left: 0; right: 0; text-align: center; font: 7pt Poppins, sans-serif; color: #9aa0a6; }
"""
RED, GREEN, GOLD, CREAM, INK, PINE, BERRY, SKY = "#a8323e", "#1f5d45", "#c9a24a", "#f7f1e6", "#2a2a2a", "#2e6b52", "#c0392b", "#d9e7ef"

def pine(x, y, h, col, seed):
    r = random.Random(seed); out = f'<path d="M{x},{y} C{x - 6},{y - h * .4} {x + 4},{y - h * .7} {x},{y - h}" stroke="#6b4a2b" stroke-width="3" fill="none"/>'
    for i in range(16):
        t = i / 16; px = x + math.sin(t * 3) * 3; py = y - h * t
        for side in (-1, 1):
            l = (1 - t) * h * .32 + 8; a = math.radians(-55 * side + r.uniform(-6, 6))
            out += f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px + side * l * math.cos(math.radians(35)):.1f}" y2="{py - l * .55:.1f}" stroke="{col}" stroke-width="2.4" stroke-linecap="round"/>'
    return out

def bauble(cx, cy, r, col, band):
    return (f'<line x1="{cx}" y1="{cy - r - 26}" x2="{cx}" y2="{cy - r - 4}" stroke="{GOLD}" stroke-width="2"/>'
            f'<rect x="{cx - 9}" y="{cy - r - 8}" width="18" height="10" rx="2" fill="{GOLD}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>'
            f'<path d="M{cx - r},{cy} Q{cx},{cy + r * .35} {cx + r},{cy}" stroke="{band}" stroke-width="{r * .16:.1f}" fill="none"/>'
            f'<circle cx="{cx - r * .35}" cy="{cy - r * .38}" r="{r * .16:.1f}" fill="#fff" opacity=".45"/>')

def star(cx, cy, r, col, pts=5):
    p = []
    for i in range(pts * 2):
        rr = r if i % 2 == 0 else r * .45; a = -math.pi / 2 + i * math.pi / pts
        p.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{col}"/>'

def snowflake(cx, cy, r, col):
    out = ""
    for k in range(6):
        a = math.radians(k * 60); x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        out += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
        for f in (.45, .7):
            bx, by = cx + r * f * math.cos(a), cy + r * f * math.sin(a)
            for s in (-1, 1):
                b = a + s * math.radians(40); l = r * .28
                out += f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + l * math.cos(b):.1f}" y2="{by + l * math.sin(b):.1f}" stroke="{col}" stroke-width="2.4" stroke-linecap="round"/>'
    return out + f'<circle cx="{cx}" cy="{cy}" r="{r * .1:.1f}" fill="{col}"/>'

def holly(cx, cy, s, leaf, berry):
    out = ""
    for ang in (-35, 35, 180):
        out += (f'<g transform="translate({cx},{cy}) rotate({ang}) scale({s})"><path d="M0,0 C8,-6 14,-4 18,-12 C22,-6 28,-8 32,-14 C34,-6 40,-6 46,-10 C42,0 46,6 40,10 C34,8 30,12 26,18 C22,12 16,14 10,18 C10,10 4,6 0,0Z" fill="{leaf}"/>'
                f'<path d="M2,1 L40,2" stroke="#ffffff55" stroke-width="1.2"/></g>')
    for dx, dy in ((-6, -2), (5, -5), (2, 6)):
        out += f'<circle cx="{cx + dx * s}" cy="{cy + dy * s}" r="{6 * s:.1f}" fill="{berry}"/><circle cx="{cx + dx * s - 2 * s}" cy="{cy + dy * s - 2 * s}" r="{1.6 * s:.1f}" fill="#fff" opacity=".6"/>'
    return out

def tree(cx, by, h, col):
    out = f'<rect x="{cx - 7}" y="{by - 14}" width="14" height="16" fill="#6b4a2b"/>'
    for i in range(3):
        w = h * (.55 - i * .12); top = by - 14 - h * (.38 + i * .26); base = by - 14 - h * i * .24
        out += f'<polygon points="{cx - w},{base} {cx + w},{base} {cx},{top}" fill="{col}"/>'
    return out + star(cx, by - 14 - h * .95, h * .1, GOLD)

def mitten(cx, cy, s, col, cuff):
    return (f'<g transform="translate({cx},{cy}) scale({s})"><path d="M-22,30 L-24,-14 C-24,-38 18,-40 20,-14 L22,8 C30,2 40,8 34,18 L22,30 Z" fill="{col}"/>'
            f'<rect x="-26" y="28" width="50" height="16" rx="5" fill="{cuff}"/>'
            f'<path d="M-16,-6 L12,-6 M-16,6 L14,6" stroke="{cuff}" stroke-width="3" stroke-dasharray="4 4"/></g>')

def gift(cx, cy, s, box, ribbon):
    return (f'<g transform="translate({cx},{cy}) scale({s})"><rect x="-30" y="-14" width="60" height="44" fill="{box}"/><rect x="-34" y="-26" width="68" height="14" fill="{box}"/>'
            f'<rect x="-5" y="-26" width="10" height="56" fill="{ribbon}"/><path d="M0,-26 C-24,-50 -30,-24 0,-26 C30,-24 24,-50 0,-26Z" fill="none" stroke="{ribbon}" stroke-width="5"/></g>')

ART = [lambda c: pine(100, 150, 120, c[1], 3), lambda c: bauble(100, 92, 42, c[1], c[2]), lambda c: star(100, 88, 50, c[2]) + star(52, 40, 10, c[1]) + star(150, 46, 8, c[1]),
       lambda c: snowflake(100, 88, 52, c[1]), lambda c: holly(80, 92, 1.6, c[1], c[2]), lambda c: tree(100, 150, 110, c[1]),
       lambda c: mitten(100, 92, 1.6, c[1], c[2]), lambda c: gift(100, 96, 1.5, c[1], c[2])]

PAL = [("#f7f1e6", RED, GOLD, "#5a2a2a"), ("#eef3ee", GREEN, BERRY, "#1d3a2c"), ("#1f3b2f", "#e9dfc6", GOLD, "#f7f1e6"), ("#8c2430", "#f3e6d6", GOLD, "#fbf3e6"),
       ("#eaf1f6", "#4c7a99", "#c9a24a", "#22384a"), ("#fbf6ef", "#7a4a2b", RED, "#3a2a20")]
WORDS = ["Merry Christmas", "Happy Holidays", "Season's Greetings", "Joy", "Ho Ho Ho", "With Love", "Noel", "Peace & Joy"]

def tag(i, pal, word, shape):
    bg, a, b, ink = pal
    clip = ["polygon(20% 0,80% 0,100% 13%,100% 100%,0 100%,0 13%)", "inset(0 round 0.18in)", "polygon(50% 0,100% 12%,100% 100%,0 100%,0 12%)"][shape % 3]
    art = ART[i % len(ART)]((bg, a, b))
    band = [f"repeating-linear-gradient(45deg,{a} 0 6px,{bg} 6px 12px)", f"radial-gradient({a} 2px,transparent 2.5px) 0 0/12px 12px", f"repeating-linear-gradient(90deg,{a} 0 5px,{b} 5px 10px)"][i % 3]
    return (f'<div class="cut" style="position:relative;background:{bg};clip-path:{clip};color:{ink};text-align:center;display:flex;flex-direction:column;align-items:center">'
            f'<div style="position:absolute;top:0.2in;left:50%;width:0.22in;height:0.22in;margin-left:-0.11in;border-radius:50%;background:#fff;box-shadow:0 0 0 3px {b}"></div>'
            f'<svg viewBox="0 0 200 170" style="width:92%;margin-top:0.52in;flex:none">{art}</svg>'
            f'<div class="script" style="font-size:21pt;line-height:1;margin:0.1in 0.12in 0;min-height:0.62in;display:flex;align-items:center">{word}</div>'
            f'<div style="flex:1"></div>'
            f'<div class="sans" style="font-size:8.5pt;text-align:left;width:100%;padding:0 0.2in;line-height:2.3">To <span style="display:inline-block;width:72%;border-bottom:1px solid {ink}99"></span><br>From <span style="display:inline-block;width:62%;border-bottom:1px solid {ink}99"></span></div>'
            f'<div style="width:100%;height:0.32in;margin-top:0.12in;background:{band};opacity:.9"></div></div>')

def tags_page(start, pal_ids, shape, n=8):
    cells = "".join(tag(start + k, PAL[pal_ids[k % len(pal_ids)]], WORDS[(start + k) % len(WORDS)], shape) for k in range(n))
    return f'<div class="page"><div class="grid" style="grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1fr">{cells}</div><div class="foot">Print at 100% on cardstock · cut along the dashed lines · punch the hole</div></div>'

def circles_page():
    texts = ["Do not open until Dec 25", "Handmade with love", "Merry Christmas", "Happy Holidays", "Made in Santa's workshop", "Shh... it's a surprise",
             "From our home to yours", "Joy to the world", "Baked with love", "Let it snow", "Peace on earth", "Season's greetings"]
    cells = ""
    for i, tx in enumerate(texts):
        bg, a, b, ink = PAL[i % len(PAL)]
        cells += (f'<div style="display:flex;align-items:center;justify-content:center"><div class="cut" style="width:1.95in;height:1.95in;border-radius:50%;background:{bg};outline-offset:0.04in;'
                  f'box-shadow:inset 0 0 0 0.08in {bg}, inset 0 0 0 0.1in {b};display:flex;flex-direction:column;align-items:center;justify-content:center;color:{ink};text-align:center;padding:0.25in">'
                  f'<svg viewBox="0 0 200 170" style="width:62%">{ART[(i + 3) % len(ART)]((bg, a, b))}</svg><div class="script" style="font-size:14pt;line-height:1.05">{tx}</div></div></div>')
    return f'<div class="page"><div class="grid" style="grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(4,1fr)">{cells}</div><div class="foot">Round labels, 2 in · use as stickers on sticker paper or glue onto wrapping</div></div>'

def labels_page():
    cells = ""
    for i in range(16):
        bg, a, b, ink = PAL[i % len(PAL)]
        cells += (f'<div class="cut" style="background:{bg};color:{ink};border-radius:0.12in;display:flex;align-items:center;gap:0.12in;padding:0 0.18in;box-shadow:inset 0 0 0 3px {bg},inset 0 0 0 4.5px {b}">'
                  f'<svg viewBox="0 0 200 170" style="width:0.75in;flex:none">{ART[i % len(ART)]((bg, a, b))}</svg>'
                  f'<div class="sans" style="font-size:8.5pt;line-height:2.2;flex:1">To <span style="display:inline-block;width:74%;border-bottom:1px solid {ink}88"></span><br>From <span style="display:inline-block;width:66%;border-bottom:1px solid {ink}88"></span></div></div>')
    return f'<div class="page"><div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:repeat(8,1fr);gap:0.16in 0.25in">{cells}</div><div class="foot">To / From labels · 16 per page</div></div>'

def cover():
    art = "".join([bauble(160, 160, 60, RED, GOLD), star(330, 120, 50, GOLD), snowflake(500, 160, 60, "#4c7a99"), holly(640, 150, 1.8, GREEN, BERRY), tree(820, 230, 160, GREEN), gift(980, 170, 1.6, RED, GOLD)])
    return (f'<div class="page" style="background:{CREAM}"><div style="position:absolute;inset:0.5in;border:2px solid {GOLD};border-radius:0.2in"></div>'
            f'<svg viewBox="0 0 1100 280" style="position:absolute;left:0.8in;right:0.8in;top:1.1in;width:calc(100% - 1.6in)">{art}</svg>'
            f'<div style="position:absolute;left:0;right:0;top:4.1in;text-align:center;color:#5a2a2a"><div class="script" style="font-size:58pt;line-height:1">Christmas Gift Tags</div>'
            f'<div class="sans" style="font-size:12pt;letter-spacing:.2em;text-transform:uppercase;margin-top:0.2in;color:{GREEN}">Printable · 48 tags · 12 round labels · 16 To/From labels</div>'
            f'<div style="font-size:12pt;margin:0.5in auto 0;max-width:5.6in;line-height:1.6;color:{INK}">Print on white cardstock (65 to 110 lb / 176 to 300 gsm) at 100% or "actual size". Cut along the dashed lines and punch a hole for ribbon or twine. '
            f'Print the round labels on sticker paper if you want stickers. Print as many as you need for your own gifts.</div></div>'
            f'<div class="foot" style="bottom:0.7in">Purl &amp; Paper · original artwork · for personal use</div></div>')

def build(size):
    pages = [cover(), tags_page(0, [0, 1], 0), tags_page(8, [2, 3], 1), tags_page(16, [4, 5], 2), tags_page(24, [0, 2], 0), tags_page(32, [1, 3], 2), tags_page(40, [5, 4], 1),
             circles_page(), labels_page()]
    return CSS, pages

if __name__ == "__main__":
    out = sys.argv[1]; name = "christmas-gift-tags"
    for size in ("letter", "a4"):
        css, pages = build(size)
        render(css, pages, size, f"{out}/{name}-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print(name, len(pages), "pages")
