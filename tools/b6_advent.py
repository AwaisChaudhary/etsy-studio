"""Family Advent Activity Calendar printable (batch 6, lanes d + h). Original flat festive icons drawn here as SVG.
Usage: python3 b6_advent.py <out_dir> -> family-advent-activity-calendar-US-Letter.pdf / -A4.pdf"""
import math, sys
sys.path.insert(0, ".")
from render import render

INK, CREAM, PINE, RED, GOLD, ROSE, SKY, BARK, SNOW, MOSS = ("#23302a", "#fbf5ea", "#1f5a43", "#c8413b", "#e3a63a", "#e8a29a", "#5c8fb8", "#8a5a3c", "#ffffff", "#7fa66a")
NAME = "family-advent-activity-calendar"
FOOT = "Purl &amp; Paper · Family Advent Activity Calendar"
CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: var(--pw); overflow: hidden; }}
body {{ font-family: Poppins, sans-serif; color: {INK}; }}
.page {{ width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: {CREAM}; contain: strict; }}
.hd {{ position: absolute; left: 0.55in; right: 0.55in; top: 0.5in; text-align: center; }}
.hd h1 {{ font: italic 700 30pt/1.05 Lora, Georgia, serif; color: {PINE}; }}
.hd .k {{ display: inline-block; font: 700 8.5pt Poppins; letter-spacing: .18em; text-transform: uppercase; color: #fff; padding: 0.04in 0.16in; border-radius: 1in; margin-top: 0.08in; }}
.hd p {{ font: 9.5pt/1.45 Poppins; color: #5d665f; margin-top: 0.07in; }}
.body {{ position: absolute; left: 0.55in; right: 0.55in; top: 1.75in; bottom: 0.6in; }}
.foot {{ position: absolute; bottom: 0.3in; left: 0; right: 0; text-align: center; font: 7pt Poppins; color: #a59f90; }}
.cut {{ outline: 1px dashed rgba(0,0,0,.28); outline-offset: -1px; }}
.ln {{ border-bottom: 1.5px solid {INK}35; height: 0.32in; }}
svg {{ display: block; }}
.snow {{ position:absolute; inset:0; background-image: radial-gradient({PINE}12 1.6px, transparent 1.8px), radial-gradient({RED}10 1.2px, transparent 1.4px);
         background-size: 0.36in 0.36in, 0.52in 0.52in; background-position: 0 0, 0.18in 0.22in; }}
"""


def C(cx, cy, r, f, extra=""): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" {extra}/>'
def R(x, y, w, h, f, rx=0, extra=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" {extra}/>'
def P(d, f, extra=""): return f'<path d="{d}" fill="{f}" {extra}/>'
def L(x1, y1, x2, y2, c, w): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
def S(c, w): return f'stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


# ---------- icons (viewBox 0 0 100 100) ----------
def i_tree(): return (R(44, 78, 12, 14, BARK, 2) + P("M50 8 L80 44 L66 44 L86 70 L14 70 L34 44 L20 44 Z", PINE) + C(40, 52, 4, RED) + C(60, 40, 4, GOLD) + C(58, 62, 4, ROSE) + C(36, 64, 3.5, GOLD)
                      + P("M50 2 L53 9 L60 9 L54 13 L56 20 L50 16 L44 20 L46 13 L40 9 L47 9 Z", GOLD))
def i_flake():
    o = ""
    for k in range(6):
        a = k * math.pi / 3; x, y = 50 + 40 * math.cos(a), 50 + 40 * math.sin(a)
        o += L(50, 50, x, y, SKY, 6)
        for t in (.55,):
            bx, by = 50 + 40 * t * math.cos(a), 50 + 40 * t * math.sin(a)
            for s in (-1, 1):
                b = a + s * .7; o += L(bx, by, bx + 13 * math.cos(b), by + 13 * math.sin(b), SKY, 5)
    return o + C(50, 50, 7, SNOW, S(SKY, 4))
def i_cookie(): return (C(50, 22, 15, "#c98a52") + P("M28 40 Q50 32 72 40 L86 52 Q88 60 78 60 L68 56 L70 76 L80 90 Q78 96 70 94 L56 80 L44 80 L30 94 Q22 96 20 90 L30 76 L32 56 L22 60 Q12 60 14 52 Z", "#c98a52")
                        + C(44, 20, 2.5, INK) + C(56, 20, 2.5, INK) + P("M44 28 Q50 32 56 28", "none", S(INK, 2.5)) + C(50, 50, 3.5, RED) + C(50, 62, 3.5, PINE)
                        + P("M22 52 Q26 48 30 52 M70 52 Q74 48 78 52", "none", S(SNOW, 3)))
def i_cocoa(): return (P("M18 34 L74 34 L68 88 L24 88 Z", RED) + P("M74 44 Q92 44 90 60 Q88 74 70 72", "none", S(RED, 7)) + R(18, 30, 56, 8, SNOW, 4)
                       + C(32, 28, 8, SNOW) + C(46, 26, 9, SNOW) + C(60, 28, 7, SNOW) + P("M36 16 Q32 8 38 2 M52 14 Q48 6 54 0", "none", S("#c9b8a6", 3)) + R(26, 54, 40, 6, SNOW, 3, 'opacity=".5"'))
def i_gift(): return R(14, 40, 72, 50, RED, 4) + R(10, 30, 80, 16, "#a8322d", 4) + R(44, 30, 12, 60, GOLD) + P("M50 30 Q30 8 24 22 Q22 32 50 30 Q70 8 76 22 Q78 32 50 30 Z", GOLD)
def i_cane(): return P("M60 92 L60 32 Q60 14 44 14 Q28 14 28 32", "none", S(SNOW, 14)) + P("M60 92 L60 32 Q60 14 44 14 Q28 14 28 32", "none", f'stroke="{RED}" stroke-width="14" stroke-dasharray="9 9" stroke-linecap="butt"') + P("M60 92 L60 32 Q60 14 44 14 Q28 14 28 32", "none", S(INK + "30", 1.5))
def i_mitten(): return P("M30 30 Q30 12 50 12 Q70 12 70 34 L70 74 L30 74 L30 52 Q14 50 16 38 Q20 30 30 38 Z", ROSE) + R(26, 72, 48, 18, SNOW, 6) + C(50, 40, 5, SNOW, 'opacity=".7"') + C(40, 54, 3, SNOW, 'opacity=".7"') + C(60, 56, 3, SNOW, 'opacity=".7"')
def i_stocking(): return P("M34 22 L66 22 L66 62 Q66 74 54 84 L30 92 Q16 92 18 80 Q20 72 34 68 Z", RED) + R(30, 12, 40, 16, SNOW, 6) + C(48, 46, 4, GOLD) + P("M22 82 Q26 76 34 78", "none", S(SNOW, 4))
def i_bauble(): return C(50, 58, 32, SKY) + R(42, 18, 16, 10, GOLD, 2) + P("M50 18 Q44 6 50 4 Q56 6 50 18", "none", S(GOLD, 3)) + P("M20 52 Q50 66 80 52", "none", S(SNOW, 5)) + P("M22 68 Q50 80 78 68", "none", S(GOLD, 4)) + C(38, 44, 5, SNOW, 'opacity=".6"')
def i_book(): return P("M10 26 Q30 18 50 28 Q70 18 90 26 L90 80 Q70 72 50 82 Q30 72 10 80 Z", PINE) + P("M50 28 L50 82", "none", S(SNOW, 3)) + "".join(L(18, 40 + 9 * k, 42, 38 + 9 * k, SNOW, 3) + L(58, 38 + 9 * k, 82, 40 + 9 * k, SNOW, 3) for k in range(4))
def i_film(): return R(10, 30, 80, 52, INK, 8) + "".join(R(16 + 14 * k, 34, 8, 6, SNOW, 1) + R(16 + 14 * k, 72, 8, 6, SNOW, 1) for k in range(5)) + P("M42 46 L62 56 L42 66 Z", GOLD) + P("M20 26 L30 14 M42 26 L52 14 M64 26 L74 14", "none", S(RED, 4))
def i_music(): return P("M38 74 L38 24 L80 14 L80 64", "none", S(PINE, 7)) + C(30, 76, 11, PINE) + C(72, 66, 11, PINE) + L(38, 34, 80, 24, PINE, 7) + C(18, 30, 4, GOLD) + C(88, 84, 4, RED)
def i_pine(): return P("M50 10 Q74 30 72 58 Q70 86 50 92 Q30 86 28 58 Q26 30 50 10 Z", BARK) + "".join(P(f"M{34 + 4 * (k % 2)} {26 + 10 * k} Q50 {34 + 10 * k} {66 - 4 * (k % 2)} {26 + 10 * k}", "none", S("#5e3c26", 4)) for k in range(6)) + P("M46 10 Q50 0 54 10", "none", S(MOSS, 5))
def i_sled(): return R(18, 44, 64, 12, RED, 4) + P("M12 70 L82 70 Q94 70 92 58", "none", S(INK, 6)) + L(30, 56, 30, 70, INK, 5) + L(70, 56, 70, 70, INK, 5) + C(80, 28, 5, SNOW, S(SKY, 3)) + C(20, 26, 4, SNOW, S(SKY, 3))
def i_lights(): return P("M4 30 Q50 60 96 30", "none", S(INK, 3)) + "".join(P(f"M{x - 6} {y} L{x + 6} {y} L{x + 4} {y + 18} Q{x} {y + 24} {x - 4} {y + 18} Z", c) + R(x - 5, y - 6, 10, 7, INK, 2) for x, y, c in [(16, 38, RED), (34, 47, GOLD), (52, 50, PINE), (70, 46, SKY), (86, 37, ROSE)])
def i_heart(): return P("M50 86 Q14 60 14 36 Q14 16 32 16 Q44 16 50 30 Q56 16 68 16 Q86 16 86 36 Q86 60 50 86 Z", RED) + P("M30 30 Q26 38 30 46", "none", S(SNOW, 4) + ' opacity=".6"')
def i_letter(): return R(10, 26, 80, 54, SNOW, 6, S(RED, 4)) + P("M12 30 L50 58 L88 30", "none", S(RED, 4)) + R(66, 32, 16, 18, GOLD, 2) + C(74, 41, 4, RED)
def i_snowman(): return C(50, 68, 24, SNOW, S(SKY, 3)) + C(50, 32, 16, SNOW, S(SKY, 3)) + C(44, 29, 2.5, INK) + C(56, 29, 2.5, INK) + P("M50 33 L64 36 L50 38 Z", "#e0802f") + R(30, 44, 40, 7, RED, 3) + R(56, 46, 8, 18, RED, 3) + C(50, 62, 2.5, INK) + C(50, 72, 2.5, INK) + R(36, 6, 28, 12, INK, 2) + R(30, 16, 40, 5, INK, 2)
def i_house(): return R(20, 44, 60, 46, ROSE) + P("M12 46 L50 14 L88 46 Z", PINE) + P("M12 46 L50 14 L88 46 L78 46 L50 24 L22 46 Z", SNOW) + R(30, 56, 16, 16, GOLD) + R(56, 60, 16, 30, BARK) + "".join(C(16 + 10 * k, 44 - (k if k < 4 else 8 - k) * 7, 2.5, [RED, GOLD, SKY][k % 3]) for k in range(9))
def i_puzzle(): return P("M14 14 L44 14 Q42 4 50 4 Q58 4 56 14 L86 14 L86 44 Q96 42 96 50 Q96 58 86 56 L86 86 L14 86 Z", MOSS) + P("M50 14 L50 86 M14 50 L86 50", "none", S(CREAM, 3))
def i_camera(): return R(10, 30, 80, 54, INK, 10) + R(34, 20, 28, 14, INK, 4) + C(50, 57, 18, SNOW) + C(50, 57, 11, SKY) + C(76, 42, 4, GOLD)
def i_star(col=GOLD):
    pts = " ".join(f"{50 + (44 if k % 2 == 0 else 19) * math.cos(-math.pi / 2 + k * math.pi / 5):.1f},{54 + (44 if k % 2 == 0 else 19) * math.sin(-math.pi / 2 + k * math.pi / 5):.1f}" for k in range(10))
    return f'<polygon points="{pts}" fill="{col}" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>'
def i_skate(): return P("M24 14 L52 14 L54 56 L84 62 Q90 64 88 72 L20 72 Z", SKY) + R(20, 66, 70, 8, INK, 3) + P("M14 84 L92 84 Q98 84 96 78", "none", S("#9aa7b0", 5)) + L(34, 74, 34, 84, "#9aa7b0", 4) + L(78, 74, 78, 84, "#9aa7b0", 4) + "".join(L(40, 24 + 8 * k, 50, 24 + 8 * k, SNOW, 3) for k in range(3))
def i_bird(): return P("M20 60 Q22 34 48 34 Q60 34 66 44 L84 40 L72 52 Q70 76 44 78 Q22 78 20 60 Z", RED) + C(56, 44, 3, INK) + P("M66 44 L78 48 L66 50 Z", GOLD) + P("M30 58 Q42 50 54 60", "none", S("#a8322d", 4)) + L(40, 78, 38, 90, INK, 3) + L(50, 78, 52, 90, INK, 3)

ICONS = dict(tree=i_tree, flake=i_flake, cookie=i_cookie, cocoa=i_cocoa, gift=i_gift, cane=i_cane, mitten=i_mitten, stocking=i_stocking, bauble=i_bauble,
             book=i_book, film=i_film, music=i_music, pine=i_pine, sled=i_sled, lights=i_lights, heart=i_heart, letter=i_letter, snowman=i_snowman,
             house=i_house, puzzle=i_puzzle, camera=i_camera, star=i_star, skate=i_skate, bird=i_bird)


def ic(name, size="0.5in"): return f'<svg viewBox="0 0 100 100" style="width:{size};height:{size};flex:none">{ICONS[name]()}</svg>'


CATS = {"Make": PINE, "Bake & treat": RED, "Cosy at home": SKY, "Kindness": ROSE, "Out & about": GOLD}
ACTS = [("Make", "Cut out paper snowflakes and hang them in the window", "flake"),
        ("Make", "Make a paper chain to count down the days", "lights"),
        ("Make", "Make salt-dough ornaments and paint them", "bauble"),
        ("Make", "Make a pinecone bird feeder for the garden", "bird"),
        ("Make", "Decorate a gingerbread house (or a graham cracker one)", "house"),
        ("Make", "Write and decorate Christmas cards for family", "letter"),
        ("Make", "Build a snowman, or a sock snowman if there's no snow", "snowman"),
        ("Bake & treat", "Bake and decorate Christmas cookies", "cookie"),
        ("Bake & treat", "Hot chocolate night with all the toppings", "cocoa"),
        ("Bake & treat", "Pancakes for dinner in festive shapes", "star"),
        ("Bake & treat", "Make a movie-night snack board together", "film"),
        ("Bake & treat", "Candy cane hunt around the house", "cane"),
        ("Cosy at home", "Christmas movie night in PJs", "film"),
        ("Cosy at home", "Build a blanket fort and read Christmas stories", "book"),
        ("Cosy at home", "Family game night with a festive prize", "puzzle"),
        ("Cosy at home", "Christmas music dance party in the kitchen", "music"),
        ("Cosy at home", "Write letters to Santa", "letter"),
        ("Cosy at home", "Indoor snowball fight with rolled-up socks", "mitten"),
        ("Cosy at home", "Hang the stockings and tell your favourite family Christmas story", "stocking"),
        ("Kindness", "Choose toys you've outgrown to donate", "gift"),
        ("Kindness", "Leave a thank-you note and treat for the delivery driver", "heart"),
        ("Kindness", "Make a card for someone who lives on their own", "letter"),
        ("Kindness", "Do a secret good deed for someone in the family", "heart"),
        ("Kindness", "Pick food together to give to a food bank", "gift"),
        ("Kindness", "Video-call grandparents and sing them a carol", "music"),
        ("Out & about", "Go and see the Christmas lights", "lights"),
        ("Out & about", "Winter nature walk: collect pinecones and twigs", "pine"),
        ("Out & about", "Visit a Christmas market or holiday fair", "bauble"),
        ("Out & about", "Go ice skating or sledging", "skate"),
        ("Out & about", "Family photo in festive sweaters", "camera"),
        ("Out & about", "Choose winter books at the library", "book"),
        ("Out & about", "Look for the brightest star on a clear night", "star")]


def page(title, kicker, kcol, intro, body, top=None, bg=None):
    st = f' style="top:{top}"' if top else ""
    return (f'<div class="page"{f" style=background:{bg}" if bg else ""}><div class="hd"><h1>{title}</h1><div class="k" style="background:{kcol}">{kicker}</div>'
            + (f'<p>{intro}</p>' if intro else "") + f'</div><div class="body"{st}>{body}</div><div class="foot">{FOOT}</div></div>')


def cover():
    ring = ["tree", "cookie", "cocoa", "gift", "flake", "stocking", "bauble", "snowman", "lights", "sled", "cane", "house"]
    tiles = "".join(f'<div style="background:#fff;border-radius:50%;width:1.05in;height:1.05in;display:flex;align-items:center;justify-content:center;box-shadow:0 0.03in 0 {INK}14">{ic(n, "0.68in")}</div>' for n in ring)
    nums = "".join(f'<div style="width:0.42in;height:0.42in;border-radius:50%;background:{[RED, PINE, GOLD][k % 3]};color:#fff;font:700 11pt Poppins;display:flex;align-items:center;justify-content:center">{k + 1}</div>' for k in range(25))
    return (f'<div class="page" style="background:{PINE}"><div class="snow" style="opacity:.6;filter:invert(1)"></div>'
            f'<div style="position:absolute;left:0.5in;right:0.5in;top:0.5in;bottom:0.5in;background:{CREAM};border-radius:0.3in"></div>'
            f'<div style="position:absolute;left:0.85in;right:0.85in;top:0.85in;display:grid;grid-template-columns:repeat(6,1fr);gap:0.14in;justify-items:center">{tiles}</div>'
            f'<div style="position:absolute;left:0.7in;right:0.7in;top:3.55in;text-align:center">'
            f'<div style="font:700 11pt Poppins;letter-spacing:.3em;color:{RED}">FAMILY</div>'
            f'<div style="font:italic 700 50pt/1 Lora,Georgia,serif;color:{PINE};margin-top:0.08in">Advent Activity<br>Calendar</div>'
            f'<div style="display:inline-block;font:700 10.5pt Poppins;letter-spacing:.14em;color:#fff;background:{RED};padding:0.06in 0.24in;border-radius:1in;margin-top:0.2in">25 DAYS OF FAMILY FUN</div>'
            f'<div style="font:10.5pt/1.6 Poppins;color:#5d665f;margin-top:0.2in">32 activity cards + blanks · countdown tree poster · number tags 1 to 25<br>paper chain countdown · planner · bucket list · December memories page</div></div>'
            f'<div style="position:absolute;left:1in;right:1in;bottom:1.3in;display:flex;flex-wrap:wrap;gap:0.07in;justify-content:center">{nums}</div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0.75in;text-align:center;font:8.5pt Poppins;color:#8a8576">Print at home at 100% · US Letter &amp; A4</div></div>')


def howto():
    ways = [("Envelopes or bags", "Number 25 envelopes, paper bags or little boxes with the tags. Pop an activity card inside each one.", "letter"),
            ("Advent jar", "Fold the cards into a jar. Each morning, pick one with the kids (or swap it if the weather says no!).", "cocoa"),
            ("Tree or garland", "Peg the numbered tags to a string of lights or a branch, with the card behind each tag.", "lights"),
            ("Countdown tree", "Colour in one bauble on the countdown tree poster each day once your activity is done.", "tree")]
    w = "".join(f'<div style="background:#fff;border-radius:0.16in;padding:0.16in 0.18in;display:flex;gap:0.14in;align-items:flex-start;border:2px solid {c}">'
                f'{ic(i, "0.62in")}<div><div style="font:700 12pt Poppins;color:{c}">{a}</div><div style="font:9.5pt/1.5 Poppins;color:#5d665f;margin-top:0.03in">{b}</div></div></div>'
                for (a, b, i), c in zip(ways, [RED, PINE, GOLD, SKY]))
    tips = ["Plan the week ahead on the planner page: busy days get quick, cosy activities; weekends get the outings.",
            "Mix the five colours so every week has something to make, bake, give and enjoy.",
            "Use the blank cards for your own family traditions, local events and grandparent visits.",
            "Not every day has to be big. 'Hot chocolate and one story' is a lovely day in the calendar.",
            "Print the cards on cardstock so they survive little hands. Keep them for next year!"]
    t = "".join(f'<div style="display:flex;gap:0.12in;padding:0.08in 0;border-bottom:2px dotted {INK}1f;font:9.8pt/1.5 Poppins">'
                f'<div style="flex:none;width:0.3in;height:0.3in;border-radius:50%;background:{PINE};color:#fff;font:700 9.5pt Poppins;display:flex;align-items:center;justify-content:center">{k + 1}</div><div>{x}</div></div>' for k, x in enumerate(tips))
    key = "".join(f'<span style="display:inline-flex;align-items:center;gap:0.06in;margin:0 0.1in 0.06in 0;font:700 9pt Poppins"><span style="width:0.18in;height:0.18in;border-radius:50%;background:{c}"></span>{n}</span>' for n, c in CATS.items())
    return page("How to use your calendar", "four ways to set it up", RED, "Print, cut and set up in an evening. Then open one little adventure every day from 1 to 25 December.",
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.16in">{w}</div><div style="margin-top:0.3in;font:700 13pt Poppins;color:{PINE}">Tips from our family to yours</div>'
                f'<div style="margin-top:0.05in">{t}</div><div style="margin-top:0.22in;background:#fff;border-radius:0.14in;padding:0.14in 0.18in"><div style="font:700 10pt Poppins;margin-bottom:0.08in">Card colours</div>{key}</div>', top="2.0in")


def tree_poster():
    rows = [1, 2, 3, 4, 5, 6, 4]
    o = ""; k = 1; H = 7.6; top = 0.4
    for ri, n in enumerate(rows):
        y = top + 0.55 + ri * 0.98
        for j in range(n):
            if k > 25: break
            x = 50 + (j - (n - 1) / 2) * 13.2
            o += (f'<div style="position:absolute;left:calc({x}% - 0.34in);top:{y}in;width:0.68in;height:0.68in;border-radius:50%;background:#fff;border:3px solid {[RED, GOLD, SKY, ROSE][k % 4]};'
                  f'display:flex;align-items:center;justify-content:center;font:700 15pt Poppins;color:{INK}">{k}</div>')
            k += 1
    tree = (f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;left:0;top:{top + 0.3}in;width:100%;height:{H - 0.6}in">'
            f'<polygon points="50,0 64,20 58,20 74,42 66,42 84,66 76,66 96,92 4,92 24,66 16,66 34,42 26,42 42,20 36,20" fill="{PINE}"/>'
            f'<rect x="45" y="92" width="10" height="8" fill="{BARK}"/></svg>')
    star = f'<div style="position:absolute;left:calc(50% - 0.45in);top:-0.15in;width:0.9in">{ic("star", "0.9in")}</div>'
    return page("Countdown to Christmas", "colour a bauble every day", PINE, None,
                f'<div style="position:relative;height:{H}in">{tree}{star}{o}</div>', top="1.45in")


def card(cat, text, icon, blank=False):
    c = CATS.get(cat, INK)
    if blank:
        return (f'<div class="cut" style="padding:0.14in;background:#fff"><div style="height:100%;border:2px dashed {INK}35;border-radius:0.12in;padding:0.12in 0.16in;display:flex;flex-direction:column">'
                f'<div style="font:700 7.5pt Poppins;letter-spacing:.18em;color:#9a9486">OUR OWN IDEA</div><div class="ln"></div><div class="ln"></div><div class="ln"></div></div></div>')
    return (f'<div class="cut" style="padding:0.14in;background:#fff"><div style="height:100%;border-radius:0.12in;background:{c}18;border:2px solid {c};padding:0.12in 0.16in;display:flex;gap:0.14in;align-items:center">'
            f'<div style="background:#fff;border-radius:50%;padding:0.07in;flex:none">{ic(icon, "0.72in")}</div>'
            f'<div><div style="font:700 7.5pt Poppins;letter-spacing:.18em;color:{c};text-transform:uppercase">{cat}</div>'
            f'<div style="font:600 12.5pt/1.25 Poppins;margin-top:0.05in">{text}</div></div></div></div>')


def card_pages():
    items = [card(*a) for a in ACTS] + [card(None, None, None, True) for _ in range(8)]
    out = []
    for k in range(5):
        out.append(page("Activity Cards", f"cut out · sheet {k + 1} of 5", [PINE, RED, SKY, ROSE, GOLD][k], None,
                        f'<div style="display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1.95in">{"".join(items[k * 8:(k + 1) * 8])}</div>', top="1.4in"))
    return out


def tag(n):
    c = [RED, PINE, GOLD, SKY, ROSE][n % 5]; icons = ["star", "flake", "bauble", "tree", "heart"]
    return (f'<div class="cut" style="display:flex;align-items:center;justify-content:center;border-radius:50%;background:#fff">'
            f'<div style="width:86%;height:86%;border-radius:50%;background:{c};display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;position:relative">'
            f'<div style="position:absolute;inset:0.07in;border-radius:50%;border:1.5px dashed #ffffff90"></div>'
            f'<div style="font:700 6.5pt Poppins;letter-spacing:.16em">DECEMBER</div><div style="font:italic 700 34pt/1 Lora,Georgia,serif">{n}</div>'
            f'<svg viewBox="0 0 100 100" style="width:0.26in;height:0.26in;opacity:.9">{ICONS[icons[n % 5]]().replace(c, "#fff")}</svg></div></div>')


def tag_pages2():
    nums = list(range(1, 26)); out = []
    for k, chunk in enumerate([nums[:16], nums[16:] + ["*"] * 7]):
        cells = ""
        for n in chunk:
            inner = tag(n) if n != "*" else (f'<div class="cut" style="border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;height:100%">'
                                             f'<div style="width:86%;height:86%;border-radius:50%;border:2px dashed {PINE};display:flex;align-items:center;justify-content:center;font:700 8pt Poppins;color:{PINE};text-align:center">YOUR<br>OWN</div></div>')
            cells += f'<div style="aspect-ratio:1;display:grid">{inner}</div>'
        out.append(page("Number Tags", f"for envelopes, bags or boxes · {k + 1} of 2", RED, "Cut out, punch a hole and tie on with ribbon, or glue to the front of each envelope.",
                        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.2in 0.2in;padding:0 0.25in">{cells}</div>', top="2.0in"))
    return out


def chain_pages():
    out = []
    for k, nums in enumerate([list(range(25, 12, -1)), list(range(12, 0, -1))]):
        strips = ""
        for n in nums:
            c = [RED, PINE, GOLD, SKY, ROSE][n % 5]
            word = "sleep" if n == 1 else "sleeps"
            strips += (f'<div class="cut" style="height:0.62in;background:{c};display:flex;align-items:center;padding:0 0.5in;color:#fff;gap:0.2in">'
                       f'<div style="font:italic 700 22pt Lora,Georgia,serif;width:0.6in;text-align:center">{n}</div>'
                       f'<div style="font:700 10pt Poppins;letter-spacing:.14em;flex:1">{word.upper()} TO CHRISTMAS</div>'
                       f'<svg viewBox="0 0 100 100" style="width:0.34in;height:0.34in">{i_star("#ffffff")}</svg></div>')
        if k == 1:
            strips += (f'<div class="cut" style="height:0.62in;background:#fff;border:2px solid {RED};display:flex;align-items:center;justify-content:center;font:italic 700 18pt Lora,Georgia,serif;color:{RED}">'
                       f'Merry Christmas!</div>')
        out.append(page("Paper Chain Countdown", f"strips {nums[0]} to {nums[-1]}", GOLD, "Cut the strips, loop them together with tape or glue (highest number at the bottom) and tear one off every night.",
                        f'<div style="display:flex;flex-direction:column;gap:0">{strips}</div>', top="1.95in"))
    return out


def planner():
    cells = ""
    for d in range(1, 26):
        cells += (f'<div style="background:#fff;border-radius:0.1in;border:1.5px solid {INK}20;padding:0.06in 0.09in;height:1.5in;display:flex;flex-direction:column">'
                  f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="font:italic 700 15pt Lora,Georgia,serif;color:{[RED, PINE, GOLD][d % 3]}">{d}</div>'
                  f'<div style="width:0.17in;height:0.17in;border:1.5px solid {INK}50;border-radius:0.04in"></div></div>'
                  f'<div style="flex:1;background:repeating-linear-gradient(transparent 0 0.22in,{INK}22 0.22in 0.235in)"></div></div>')
    return page("Our Advent Plan", "for grown-ups", PINE, "Write which activity goes on each day. Tick the box when it's done.",
                f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:0.1in">{cells}</div>', top="1.95in")


def bucket():
    items = ["Watch our favourite Christmas movie", "Bake something to share", "See the Christmas lights", "Make a homemade decoration", "Sing carols",
             "Give to someone in need", "Read 'The Night Before Christmas'", "Have a hot chocolate picnic", "Send cards to family far away", "Take a festive family photo",
             "Make a snowflake (paper or real)", "Do a Christmas jigsaw", "Wear matching PJs", "Play in the snow (or the rain!)", "Write a thank-you note", "Leave a treat for Santa"]
    rows = "".join(f'<div style="display:flex;gap:0.14in;align-items:center;padding:0.075in 0;border-bottom:2px dotted {INK}1f">'
                   f'<div style="width:0.26in;height:0.26in;border-radius:0.06in;border:2px solid {[RED, PINE, GOLD, SKY][k % 4]};flex:none"></div><div style="font:10.5pt Poppins">{x}</div></div>' for k, x in enumerate(items))
    own = "".join(f'<div style="display:flex;gap:0.14in;align-items:flex-end;padding:0.05in 0"><div style="width:0.26in;height:0.26in;border-radius:0.06in;border:2px solid {INK}40;flex:none"></div><div class="ln" style="flex:1"></div></div>' for _ in range(5))
    return page("Christmas Bucket List", "tick them off together", RED, None,
                f'<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:0.35in"><div>{rows}</div><div><div style="background:#fff;border-radius:0.16in;padding:0.18in">'
                f'<div style="font:700 12pt Poppins;color:{PINE}">Our own ideas</div>{own}</div><div style="display:flex;justify-content:center;gap:0.15in;margin-top:0.35in">{ic("snowman", "1.1in")}{ic("tree", "1.1in")}</div></div></div>', top="1.6in")


def memories():
    qs = [("Our favourite day was", "star"), ("The yummiest thing we made", "cookie"), ("The funniest moment", "heart"), ("Someone we helped", "gift"),
          ("Best movie or story", "film"), ("Next year we want to", "tree")]
    boxes = "".join(f'<div style="background:#fff;border-radius:0.16in;padding:0.14in 0.18in;border:2.5px solid {[RED, PINE, GOLD, SKY, ROSE, MOSS][k]}">'
                    f'<div style="display:flex;align-items:center;gap:0.1in">{ic(i, "0.46in")}<div style="font:700 11pt Poppins">{q}...</div></div><div class="ln"></div><div class="ln"></div></div>' for k, (q, i) in enumerate(qs))
    draw = (f'<div style="grid-column:span 2;background:#fff;border-radius:0.16in;border:2.5px dashed {INK}30;height:2.4in;padding:0.14in 0.18in;font:700 11pt Poppins">'
            f'Draw or stick a photo of our December 2026 <span style="font:400 9pt Poppins;color:#5d665f">&nbsp; (or write the year here: ________)</span></div>')
    return page("Our December Memories", "fill in on Christmas Day", PINE, None, f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.16in">{boxes}{draw}</div>', top="1.45in")


def build(out):
    pages = [cover(), howto(), tree_poster()] + card_pages() + tag_pages2() + chain_pages() + [planner(), bucket(), memories()]
    for size in ("letter", "a4"):
        render(CSS, pages, size, f"{out}/{NAME}-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print(len(pages), "pages", len(ACTS), "activities")


if __name__ == "__main__":
    build(sys.argv[1])
