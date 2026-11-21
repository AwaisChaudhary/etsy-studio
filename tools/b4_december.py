"""December Days journal kit (batch 4, lanes c + d): 25 daily prompt cards (4x3), number circles, journaling cards,
seamless papers, tags, tickets, labels and lists. Artwork reuses the original Nordic Folk vector set (b4_clipart.py).
Usage: python3 b4_december.py <out_dir>"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render import render
import b4_clipart as K

R, DR, G, LG, C, M, P, N, BR = K.R, K.DR, K.G, K.LG, K.C, K.M, K.P, K.N, K.BR
INK = "#3A2A26"
PROMPTS = ["How December began", "Bringing out the decorations", "Our tree this year", "A cosy evening in", "Something we baked",
           "Lights around town", "The song on repeat", "Writing Christmas cards", "A favourite ornament and its story", "Out in the cold",
           "Wrapping presents", "A kindness given or received", "Movie night", "A winter walk", "A tradition we keep",
           "Something handmade", "Friends & gatherings", "The smells of the season", "What I'm grateful for", "The view from my window",
           "Shortest day, longest night", "Last-minute errands", "Getting ready", "Christmas Eve", "Christmas Day"]
EXTRA = ["Our wish lists", "The best gift", "Snow day!", "Family recipe", "Looking ahead"]
ICONS = [K.e_cottage, K.e_star_straw, K.e_tree_tiered, K.e_mug, K.e_ginger_man, K.e_candle, K.e_bells, K.e_bird, K.e_bauble1, K.e_mitten,
         K.e_present, K.e_heart_folk, K.e_star8, K.e_tree_folk, K.e_wreath, K.e_sweater, K.e_gnome1, K.e_holly, K.e_heart_woven, K.e_snow1,
         K.e_snow2, K.e_sled, K.e_stocking, K.e_gnome3, K.e_tree_cone]
XICONS = [K.e_stocking2, K.e_present2, K.e_snow3, K.e_ginger_house, K.e_reindeer_head]
SCHEMES = [(C, R, INK), ("#EEF2EA", G, "#1F3A30"), ("#F6E7E2", DR, "#3A2024"), ("#E9EDF3", N, N)]

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Poppins, sans-serif; color: #3A2A26; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #fff; contain: strict; }
html, body { width: var(--pw); overflow: hidden; }
.sheet { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); display: grid; }
.cut { outline: 0.6px dashed rgba(0,0,0,.35); }
.card { position: relative; overflow: hidden; }
.card .inner { position: absolute; inset: 0.14in; border-radius: 0.08in; }
.num { font: italic 600 38pt/0.9 Lora, serif; }
.pr { font: 600 10pt/1.2 Poppins; }
.lines { position: absolute; left: 0.32in; right: 0.32in; }
.lines div { height: 0.3in; border-bottom: 1px solid currentColor; opacity: .35; }
h1 { font: italic 600 44pt/1 Lora, serif; }
.lab { font: 600 8pt Poppins; letter-spacing: .16em; text-transform: uppercase; }
.foot { position: absolute; bottom: 0.2in; left: 0; right: 0; text-align: center; font: 7pt Poppins; color: #a09488; }
svg { display: block; }
"""


def icon(fn, w):
    return f'<div style="width:{w}in">{K.svg_of(fn)}</div>'


def day_card(n, prompt, fn, scheme, label=None):
    bg, acc, ink = scheme
    num = label or f"{n:02d}"
    return (f'<div class="card cut" style="width:4in;height:3in;background:{bg};color:{ink}">'
            f'<div class="inner" style="border:1.5px solid {acc}55"></div>'
            f'<div style="position:absolute;left:0.32in;top:0.3in;color:{acc}" class="num">{num}</div>'
            f'<div class="lab" style="position:absolute;left:0.34in;top:0.98in;color:{acc}">December</div>'
            f'<div class="pr" style="position:absolute;left:0.34in;top:1.2in;width:2.25in">{prompt}</div>'
            f'<div style="position:absolute;right:0.28in;top:0.26in">{icon(fn, 1.25)}</div>'
            f'<div class="lines" style="top:1.72in;color:{ink}"><div></div><div></div><div></div></div>'
            + K.zig(0, 1, 0, 0, 1, acc)[:0] + "</div>")


def day_pages():
    items = [(i + 1, PROMPTS[i], ICONS[i], None) for i in range(25)] + [(0, EXTRA[i], XICONS[i], "★") for i in range(5)]
    pages = []
    for p in range(5):
        cells = "".join(day_card(n, pr, fn, SCHEMES[(n - 1 if n else k) % 4], lab) for k, (n, pr, fn, lab) in enumerate(items[p * 6:(p + 1) * 6]))
        pages.append(f'<div class="page"><div class="sheet" style="grid-template-columns:4in 4in;grid-template-rows:repeat(3,3in)">{cells}</div>'
                     f'<div class="foot">Daily prompt cards · 4 x 3 in · cut on the dashed lines</div></div>')
    return pages


def circles_page():
    cells = ""
    for i in range(1, 26):
        bg, acc, ink = SCHEMES[i % 4]
        fill, txt = (acc, bg) if i % 2 else (bg, acc)
        cells += (f'<div style="display:flex;align-items:center;justify-content:center"><div class="cut" style="width:1.35in;height:1.35in;border-radius:50%;background:{fill};'
                  f'box-shadow:inset 0 0 0 0.07in {fill},inset 0 0 0 0.09in {txt};display:flex;flex-direction:column;align-items:center;justify-content:center;color:{txt}">'
                  f'<div style="font:italic 600 34pt/0.9 Lora,serif">{i}</div><div style="font:600 6pt Poppins;letter-spacing:.2em;margin-top:0.03in">DECEMBER</div></div></div>')
    return (f'<div class="page"><div style="position:absolute;left:0.5in;right:0.5in;top:0.4in;text-align:center"><div class="lab" style="color:{G}">Number circles</div>'
            f'<div style="font:9pt Poppins;color:#7a6a60;margin-top:0.04in">Glue onto photos or pages · 1.35 in</div></div>'
            f'<div class="sheet" style="grid-template-columns:repeat(5,1.5in);grid-template-rows:repeat(5,1.62in);top:54%">{cells}</div>'
            f'<div class="foot">Number circles 1 to 25</div></div>')


def jcard(kind, scheme, fn=None, title=None):
    bg, acc, ink = scheme
    body = ""
    if kind == "lined":
        body = f'<div class="lines" style="top:{0.8 if title else 0.35}in;color:{ink}">' + "<div></div>" * (6 if title else 8) + "</div>"
    elif kind == "grid":
        body = (f'<div style="position:absolute;inset:0.32in;background-image:linear-gradient({ink}22 1px,transparent 1px),linear-gradient(90deg,{ink}22 1px,transparent 1px);'
                f'background-size:0.2in 0.2in"></div>')
    elif kind == "dot":
        body = f'<div style="position:absolute;inset:0.32in;background-image:radial-gradient({ink}55 1.1px,transparent 1.4px);background-size:0.2in 0.2in"></div>'
    elif kind == "art":
        body = f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">{icon(fn, 2.2)}</div>'
    elif kind == "word":
        body = (f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{acc}">'
                f'<div style="width:0.9in">{K.svg_of(fn)}</div><div style="font:italic 600 26pt/1 Lora,serif;margin-top:0.12in">{title}</div></div>')
    t = (f'<div style="position:absolute;left:0.32in;top:0.3in;font:italic 600 18pt Lora,serif;color:{acc}">{title}</div>' if title and kind == "lined" else "")
    return (f'<div class="card cut" style="width:3in;height:4in;background:{bg};color:{ink}"><div class="inner" style="border:1.5px solid {acc}55"></div>{t}{body}</div>')


def jcards_pages():
    a = [jcard("word", SCHEMES[0], K.e_star8, "Merry & Bright"), jcard("lined", SCHEMES[1], title="Today"), jcard("art", SCHEMES[2], K.e_gnome2),
         jcard("grid", SCHEMES[3]), jcard("lined", SCHEMES[0], title="Remember"), jcard("word", SCHEMES[1], K.e_tree_tiered, "Oh Christmas Tree")]
    b = [jcard("art", SCHEMES[3], K.e_bauble3), jcard("dot", SCHEMES[0]), jcard("word", SCHEMES[2], K.e_heart_folk, "Home for the Holidays"),
         jcard("lined", SCHEMES[3], title="Notes"), jcard("art", SCHEMES[1], K.e_mushrooms_pair), jcard("word", SCHEMES[0], K.e_snow1, "Let it Snow")]
    out = []
    for cards in (a, b):
        out.append(f'<div class="page" style="--x:0"><div class="sheet" style="grid-template-columns:repeat(2,3in);grid-template-rows:repeat(2,4in);transform:translate(-50%,-50%)">'
                   f'{"".join(cards[:4])}</div><div class="foot">Journaling cards · 3 x 4 in</div></div>')
    # the 2 extra cards of each set go onto a shared third page
    out.append(f'<div class="page"><div class="sheet" style="grid-template-columns:repeat(2,3in);grid-template-rows:repeat(2,4in)">{a[4]}{a[5]}{b[4]}{b[5]}</div>'
               f'<div class="foot">Journaling cards · 3 x 4 in</div></div>')
    return out


def paper_page(name):
    import base64
    nm, bg, motifs = [x for x in K.PATTERNS if x[0] == name][0]
    uri = "data:image/svg+xml;base64," + base64.b64encode(K.pattern_svg(bg, motifs, 1000).encode()).decode()
    return f'<div class="page" style="background:{bg} url({uri}) center/6in 6in repeat"></div>'


def ticket(t1, t2, scheme, w=3.4, h=1.45):
    bg, acc, ink = scheme
    return (f'<div class="cut" style="width:{w}in;height:{h}in;background:{bg};color:{ink};position:relative;display:flex;align-items:center;'
            f'-webkit-mask:radial-gradient(circle at 0 50%,transparent 0.12in,#000 0.125in) left/51% 100% no-repeat,radial-gradient(circle at 100% 50%,transparent 0.12in,#000 0.125in) right/51% 100% no-repeat">'
            f'<div style="position:absolute;inset:0.08in 0.2in;border:1.2px dashed {acc}99"></div>'
            f'<div style="padding-left:0.32in;flex:1"><div class="lab" style="color:{acc};font-size:7pt">{t1}</div><div style="font:italic 600 17pt/1.05 Lora,serif;margin-top:0.03in">{t2}</div></div>'
            f'<div style="width:0.75in;border-left:1.2px dashed {acc}99;height:70%;display:flex;align-items:center;justify-content:center;writing-mode:vertical-rl;font:600 7pt Poppins;letter-spacing:.15em;color:{acc}">ADMIT ONE</div></div>')


def tag(word, scheme, fn):
    bg, acc, ink = scheme
    return (f'<div class="cut" style="width:1.75in;height:3.4in;background:{bg};color:{ink};position:relative;clip-path:polygon(22% 0,78% 0,100% 12%,100% 100%,0 100%,0 12%);'
            f'display:flex;flex-direction:column;align-items:center">'
            f'<div style="width:0.2in;height:0.2in;border-radius:50%;background:#fff;box-shadow:0 0 0 2.5px {acc};margin-top:0.2in"></div>'
            f'<div style="width:1.35in;margin-top:0.2in">{K.svg_of(fn)}</div>'
            f'<div style="font:italic 600 15pt/1.05 Lora,serif;color:{acc};text-align:center;margin-top:0.12in;padding:0 0.12in">{word}</div>'
            f'<div style="flex:1"></div><div style="width:100%;height:0.28in;background:repeating-linear-gradient(45deg,{acc} 0 6px,{bg} 6px 12px)"></div></div>')


def label(text, scheme, w=2.35, h=0.8):
    bg, acc, ink = scheme
    return (f'<div class="cut" style="width:{w}in;height:{h}in;background:{acc};color:{bg};border-radius:0.4in;display:flex;align-items:center;justify-content:center;'
            f'box-shadow:inset 0 0 0 0.05in {acc},inset 0 0 0 0.065in {bg};font:italic 600 14pt Lora,serif">{text}</div>')


def ephemera_page():
    t = [ticket("Christmas market", "Mulled Cider & Lights", SCHEMES[0]), ticket("Holiday express", "North Pole Line", SCHEMES[3]),
         ticket("Winter concert", "Carols by Candlelight", SCHEMES[1]), ticket("Admit the whole family", "Cocoa & Cookies", SCHEMES[2])]
    tg = [tag("Merry Christmas", SCHEMES[0], K.e_tree_cone), tag("Joy", SCHEMES[1], K.e_star_straw), tag("Made with love", SCHEMES[2], K.e_heart_woven),
          tag("Let it snow", SCHEMES[3], K.e_snow2)]
    lb = [label(x, SCHEMES[i % 4]) for i, x in enumerate(["Our December", "Cosy days", "Best day ever", "Snowed in", "Home sweet home", "Pure magic"])]
    return (f'<div class="page"><div style="position:absolute;left:0.5in;top:0.45in;display:grid;grid-template-columns:3.4in 3.4in;gap:0.18in 0.3in">{"".join(t)}</div>'
            f'<div style="position:absolute;left:0.5in;top:3.75in;display:flex;gap:0.12in">{"".join(tg)}</div>'
            f'<div style="position:absolute;left:0.5in;top:7.45in;display:grid;grid-template-columns:repeat(3,2.35in);gap:0.16in 0.12in">{"".join(lb)}</div>'
            f'<div class="foot">Tickets, tags and labels</div></div>')


def list_card(title, scheme, rows=10, w=3.7, h=4.9, cols=None):
    bg, acc, ink = scheme
    head = ""
    if cols:
        head = f'<div style="display:flex;font:600 7pt Poppins;letter-spacing:.12em;text-transform:uppercase;color:{acc};margin-bottom:0.04in">' + "".join(f'<div style="flex:{f}">{c}</div>' for c, f in cols) + "</div>"
    lines = "".join(f'<div style="height:0.31in;border-bottom:1px solid {ink}44;display:flex;align-items:flex-end"><span style="width:0.14in;height:0.14in;border:1.2px solid {acc};border-radius:3px;margin:0 0.08in 0.05in 0"></span></div>' for _ in range(rows))
    return (f'<div class="cut" style="width:{w}in;height:{h}in;background:{bg};color:{ink};position:relative;padding:0.3in 0.3in">'
            f'<div style="position:absolute;inset:0.12in;border:1.5px solid {acc}55;border-radius:0.08in"></div>'
            f'<div style="font:italic 600 20pt Lora,serif;color:{acc};margin-bottom:0.1in">{title}</div>{head}{lines}</div>')


def lists_page():
    return (f'<div class="page"><div class="sheet" style="grid-template-columns:3.7in 3.7in;grid-template-rows:4.9in 4.9in;gap:0.2in">'
            f'{list_card("Gifts to give", SCHEMES[0], cols=[("For", 1), ("Idea", 2)])}{list_card("Cards sent", SCHEMES[1])}'
            f'{list_card("Christmas bucket list", SCHEMES[3])}{list_card("Things to bake", SCHEMES[2])}</div><div class="foot">List cards · 3.7 x 4.9 in</div></div>')


def letter_page():
    lines = "".join('<div style="height:0.36in;border-bottom:1px solid #3A2A2633"></div>' for _ in range(13))
    return (f'<div class="page" style="background:{C}"><div style="position:absolute;inset:0.45in;border:2px solid {R};border-radius:0.15in"></div>'
            f'<div style="position:absolute;inset:0.6in;border:1px dashed {G}"></div>'
            f'<div style="position:absolute;left:0;right:0;top:0.9in;text-align:center;color:{R}"><div style="width:1.4in;margin:0 auto">{K.svg_of(K.e_star_straw)}</div>'
            f'<h1 style="margin-top:0.15in">Dear Santa</h1><div class="lab" style="color:{G};margin-top:0.08in">A letter for this year\'s pages</div></div>'
            f'<div style="position:absolute;left:1in;right:1in;top:3.6in;font:11pt Poppins">{lines}</div>'
            f'<div style="position:absolute;left:1in;bottom:1in;font:italic 600 14pt Lora,serif;color:{R}">Love from ______________________</div>'
            f'<div style="position:absolute;right:0.9in;bottom:0.8in;width:1.3in">{K.svg_of(K.e_gnome1)}</div></div>')


def tracker_page():
    cells = ""
    for i in range(1, 26):
        bg, acc, ink = SCHEMES[i % 4]
        cells += (f'<div style="background:{bg};border-radius:0.08in;position:relative;box-shadow:inset 0 0 0 1.5px {acc}55">'
                  f'<div style="position:absolute;left:0.1in;top:0.06in;font:italic 600 16pt Lora,serif;color:{acc}">{i}</div>'
                  f'<div style="position:absolute;left:0.1in;right:0.1in;bottom:0.12in;height:0.6in;background-image:linear-gradient({ink}33 1px,transparent 1px);background-size:100% 0.2in"></div></div>')
    return (f'<div class="page"><div style="position:absolute;left:0;right:0;top:0.5in;text-align:center;color:{G}"><h1 style="font-size:34pt">25 Days of December</h1>'
            f'<div class="lab" style="color:{R};margin-top:0.08in">One line a day · a whole month on one page</div></div>'
            f'<div style="position:absolute;left:0.5in;right:0.5in;top:1.75in;bottom:0.6in;display:grid;grid-template-columns:repeat(5,1fr);gap:0.12in">{cells}</div>'
            f'<div class="foot">One-line-a-day tracker</div></div>')


def cover_page():
    art = [(K.e_gnome1, 0.6, 0.7, 1.6), (K.e_tree_tiered, 2.4, 0.5, 1.9), (K.e_star_straw, 4.5, 0.6, 1.6), (K.e_heart_woven, 6.2, 0.9, 1.5),
           (K.e_candle, 0.7, 7.3, 1.6), (K.e_mug, 2.6, 7.6, 1.5), (K.e_wreath, 4.4, 7.3, 1.7), (K.e_stocking, 6.3, 7.4, 1.5)]
    a = "".join(f'<div style="position:absolute;left:{x}in;top:{y}in;width:{w}in">{K.svg_of(fn)}</div>' for fn, x, y, w in art)
    return (f'<div class="page" style="background:{C}">{a}<div style="position:absolute;left:0;right:0;top:3.2in;text-align:center;color:{DR}">'
            f'<div class="lab" style="color:{G};font-size:10pt">Printable December journal kit</div><h1 style="font-size:60pt;margin-top:0.15in">December Days</h1>'
            f'<div style="font:400 12pt/1.6 Poppins;color:{INK};max-width:5.8in;margin:0.25in auto 0">25 daily prompt cards, number circles, journaling cards, '
            f'patterned papers, tickets, tags, lists and a one-line-a-day page. Print what you need for a December journal, scrapbook album or memory planner.</div>'
            f'<div style="font:600 9pt/1.7 Poppins;color:{G};max-width:5.8in;margin:0.2in auto 0">Print at 100% / actual size on matte cardstock or photo paper. Cut on the dashed lines.</div></div>'
            f'<div class="foot">Purl &amp; Paper · original artwork · for personal use</div></div>')


def build():
    return ([cover_page()] + day_pages() + [circles_page()] + jcards_pages() + [tracker_page(), lists_page(), ephemera_page(), letter_page()]
            + [paper_page(n) for n in ("pattern-trees-cream", "pattern-gnomes-red", "pattern-snowflakes-navy", "pattern-hearts-pink", "pattern-mushrooms-sage", "pattern-baubles-green")])


if __name__ == "__main__":
    out = sys.argv[1]; name = "december-days-journal-kit"
    pages = build()
    for size in ("letter", "a4"):
        render(CSS, pages, size, f"{out}/{name}-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print(name, len(pages), "pages")
