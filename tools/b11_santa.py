"""Letter from Santa Kit (batch 11, lane d/h): 14 printable pages, all artwork drawn here from scratch (SVG).
Letter TO Santa (2 designs: writers + little ones who draw), wish list, a warm pre-written letter FROM Santa with blanks, a blank
North Pole letterhead, Official Nice List certificate, the Nice List scroll, North Pole envelope labels + stamps, reindeer food
bag toppers + recipe card, "Santa stop here" sign, cookie + carrot plate tent cards, a thank-you note from Santa and a colouring page.
Undated, so it works every year. US Letter + A4."""
import math, random, sys
sys.path.insert(0, ".")
from render import render
from kits2 import pine, star, snowflake, holly, gift, bauble, tree

RED, DRED, GREEN, GOLD, CREAM, INK, SKY, NIGHT = "#b3262e", "#7d1b22", "#1f5b45", "#c9a24a", "#fbf6ec", "#2b2a2a", "#dbe8ef", "#1d2f4a"
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Lora, serif; color: #2b2a2a; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #fbf6ec; contain: strict; }
.script { font-family: "TeX Gyre Chorus", Lora, serif; }
.sans { font-family: Poppins, "Liberation Sans", sans-serif; }
.cut { outline: 1px dashed rgba(0,0,0,.3); outline-offset: 0.05in; }
svg { display: block; }
.lines { background: repeating-linear-gradient(transparent 0 calc(var(--lh) - 1px), rgba(43,42,42,.35) calc(var(--lh) - 1px) var(--lh)); }
.foot { position: absolute; bottom: 0.22in; left: 0; right: 0; text-align: center; font: 7pt Poppins, sans-serif; color: #a39b8f; letter-spacing: .12em; }
"""

def santa(cx, cy, s, outline=False):
    """An original, simple Santa: round face, rosy cheeks, big curly beard, red hat with a pom-pom."""
    if outline:
        f = lambda c: 'fill="#fff" stroke="#2b2a2a" stroke-width="4"'
        g = lambda c: 'fill="none" stroke="#2b2a2a" stroke-width="4"'
        cheek = eye = ""
    else:
        f = lambda c: f'fill="{c}"'; g = lambda c: f'fill="{c}"'
        cheek = '<circle cx="-30" cy="6" r="11" fill="#f2a39b" opacity=".8"/><circle cx="30" cy="6" r="11" fill="#f2a39b" opacity=".8"/>'
    eye = '<circle cx="-18" cy="-8" r="5" fill="#2b2a2a"/><circle cx="18" cy="-8" r="5" fill="#2b2a2a"/>'
    curls = "".join(f'<circle cx="{58 * math.cos(math.radians(a)):.1f}" cy="{20 + 62 * math.sin(math.radians(a)):.1f}" r="22" {f("#ffffff")}/>' for a in range(10, 171, 20))
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M-62 -38 Q-40 -130 30 -120 Q80 -112 96 -40 Z" {f(RED)}/>'
            f'<circle cx="100" cy="-34" r="18" {f("#ffffff")}/>'
            f'{curls}<ellipse cx="0" cy="40" rx="58" ry="62" {f("#ffffff")}/>'
            f'<ellipse cx="0" cy="-2" rx="48" ry="42" {f("#f6d4bf")}/>{cheek}{eye}'
            f'<path d="M-30 22 Q-14 8 0 20 Q14 8 30 22 Q14 30 0 24 Q-14 30 -30 22Z" {f("#ffffff")}/>'
            f'<circle cx="0" cy="10" r="9" {f("#e98a7e")}/>'
            f'<rect x="-70" y="-50" width="140" height="28" rx="14" {f("#ffffff")}/></g>')

def reindeer(cx, cy, s, body="#8a5a3c", outline=False):
    st = 'fill="#fff" stroke="#2b2a2a" stroke-width="4"' if outline else f'fill="{body}"'
    ant = "#2b2a2a" if outline else "#6b4430"
    antlers = (f'<path d="M-24 -46 Q-40 -90 -70 -100 M-38 -76 Q-58 -74 -66 -60 M-50 -92 Q-46 -114 -30 -122" stroke="{ant}" stroke-width="7" fill="none" stroke-linecap="round"/>'
               f'<path d="M24 -46 Q40 -90 70 -100 M38 -76 Q58 -74 66 -60 M50 -92 Q46 -114 30 -122" stroke="{ant}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    return (f'<g transform="translate({cx} {cy}) scale({s})">{antlers}'
            f'<ellipse cx="-46" cy="-36" rx="20" ry="10" transform="rotate(-25 -46 -36)" {st}/><ellipse cx="46" cy="-36" rx="20" ry="10" transform="rotate(25 46 -36)" {st}/>'
            f'<path d="M-34 -50 Q0 -70 34 -50 Q44 0 22 40 Q0 56 -22 40 Q-44 0 -34 -50Z" {st}/>'
            f'<ellipse cx="0" cy="34" rx="24" ry="18" {"fill=\"#fff\" stroke=\"#2b2a2a\" stroke-width=\"4\"" if outline else "fill=\"#c89a72\""}/>'
            f'<ellipse cx="0" cy="24" rx="11" ry="8" fill="#3b2a22"/>'
            f'<circle cx="-14" cy="-14" r="5" fill="#2b2a2a"/><circle cx="14" cy="-14" r="5" fill="#2b2a2a"/></g>')

def seal(cx, cy, r, col=RED, text="OFFICIAL · NORTH POLE · POST OFFICE · "):
    pid = f"sp{int(cx)}{int(cy)}{int(r)}"
    return (f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/><circle cx="{cx}" cy="{cy}" r="{r * .9:.1f}" fill="none" stroke="#fff" stroke-width="{r * .03:.1f}" opacity=".7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .6:.1f}" fill="none" stroke="#fff" stroke-width="{r * .025:.1f}" opacity=".7"/>'
            f'<defs><path id="{pid}" d="M{cx - r * .75},{cy} a{r * .75},{r * .75} 0 1,1 {r * 1.5},0 a{r * .75},{r * .75} 0 1,1 -{r * 1.5},0"/></defs>'
            f'<text font-family="Poppins, sans-serif" font-size="{r * .16:.1f}" letter-spacing="{r * .02:.1f}" fill="#fff" font-weight="600"><textPath href="#{pid}">{text}</textPath></text>'
            f'{star(cx, cy, r * .38, "#fff")}</g>')

def flakes(w, h, n, seed, col="#ffffff", op=.7):
    r = random.Random(seed)
    return "".join(f'<g opacity="{op}">{snowflake(r.uniform(0, w), r.uniform(0, h), r.uniform(8, 20), col)}</g>' for _ in range(n))

def border_holly(col_leaf=GREEN, col_berry=RED, top_only=False):
    pts = [(60, 60, 0), (790, 60, 90)] + ([] if top_only else [(60, 1040, -90), (790, 1040, 180)])
    corners = "".join(f'<g transform="translate({x} {y}) rotate({a})">{holly(0, 0, 2.4, col_leaf, col_berry)}</g>' for x, y, a in pts)
    return f'<svg viewBox="0 0 850 1100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">{corners}</svg>'

def candy_frame(inset="0.32in", w="0.16in"):
    return (f'<div style="position:absolute;inset:{inset};border:{w} solid transparent;border-image:repeating-linear-gradient(45deg,{RED} 0 14px,#fff 14px 28px) 30;'
            f'pointer-events:none"></div>')

def foot(txt="PURL & PAPER · LETTER FROM SANTA KIT"): return f'<div class="foot">{txt}</div>'

# ---------------- pages ----------------
def intro():
    li = "".join(f"<li>{x}</li>" for x in [
        "Letter to Santa, 2 designs (writers + little ones who draw)", "Christmas wish list", "Letter FROM Santa, ready to personalise", "Blank North Pole letterhead",
        "Official Nice List certificate", "The Nice List scroll", "North Pole envelope labels + postage stamps", "Magic reindeer food toppers + recipe",
        "\"Santa, please stop here\" sign", "Cookie + carrot plate cards", "A thank-you note from Santa", "A Christmas colouring page"])
    art = f'<svg viewBox="-150 -150 300 300" style="position:absolute;right:0.4in;top:0.55in;width:2.6in">{santa(0, 0, 1.05)}</svg>'
    return (f'<div class="page" style="background:{CREAM}">{candy_frame()}{art}'
            f'<div style="position:absolute;left:0.85in;right:0.85in;top:0.85in">'
            f'<div class="sans" style="font-size:9pt;letter-spacing:.32em;color:{RED};font-weight:600">PRINTABLE CHRISTMAS KIT</div>'
            f'<div class="script" style="font-size:58pt;line-height:1;margin-top:8pt;color:{DRED}">Letter from<br>Santa</div>'
            f'<div style="font-size:12.5pt;margin-top:10pt;max-width:4.1in;line-height:1.45">Everything for a little North Pole magic: letters to and from Santa, a Nice List certificate, reindeer food and treats for Christmas Eve.</div>'
            f'<div style="margin-top:22pt;font-weight:700;font-size:12pt;color:{GREEN}">Inside this kit</div><ul style="margin:6pt 0 0 16pt;font-size:10.5pt;line-height:1.7">{li}</ul>'
            f'<div style="margin-top:18pt;font-size:9.5pt;line-height:1.55;max-width:6.4in;color:#5a554e"><b>How to use:</b> print at 100% / actual size on plain paper, or cardstock for the certificate, '
            f'sign, tags and plate cards. Write the child\'s name in the blanks (a gold or red pen looks lovely), sign as Santa, and let the magic happen. Undated, so you can print it again every Christmas.</div></div>'
            f'{foot()}</div>')

def letter_to_santa():
    fields = [("My name is", 3.2), ("I am", 1.0, "years old"), ("I live in", 3.6)]
    rows = (f'<div style="display:flex;gap:6pt;align-items:flex-end;margin:6pt 0"><span>My name is</span><span style="flex:1;border-bottom:1.5px solid {INK}"></span>'
            f'<span>and I am</span><span style="width:0.7in;border-bottom:1.5px solid {INK}"></span><span>years old.</span></div>'
            f'<div style="display:flex;gap:6pt;align-items:flex-end;margin:10pt 0"><span>This year I have been</span>'
            + "".join(f'<span style="display:inline-flex;align-items:center;gap:4pt;margin-left:8pt"><span style="width:12pt;height:12pt;border:1.5px solid {INK};border-radius:3px"></span>{w}</span>' for w in ("very good", "good", "mostly good"))
            + '</div>')
    did = f'<div style="margin-top:10pt">Something kind I did this year:</div><div class="lines" style="--lh:0.42in;height:1.26in"></div>'
    wish = (f'<div style="margin-top:12pt">For Christmas I would love:</div>'
            + "".join(f'<div style="display:flex;gap:8pt;align-items:flex-end;height:0.46in"><b style="color:{RED};width:14pt">{i}.</b><span style="flex:1;border-bottom:1px solid {INK}66"></span></div>' for i in range(1, 7)))
    sign = (f'<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:14pt"><div><div>Love from,</div><div style="width:2.6in;border-bottom:1.5px solid {INK};height:0.45in"></div></div>'
            f'<div style="text-align:center"><div style="width:2.1in;height:1.6in;border:2px dashed {RED};border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:8.5pt;color:{RED}" class="sans">draw yourself!</div></div></div>')
    head = (f'<div style="text-align:center;position:relative"><div class="sans" style="font-size:8pt;letter-spacing:.35em;color:{GREEN};font-weight:600">TO: SANTA CLAUS · THE NORTH POLE</div>'
            f'<div class="script" style="font-size:54pt;color:{DRED};line-height:1.05">Dear Santa,</div></div>')
    art = (f'<svg viewBox="0 0 850 200" style="position:absolute;left:0;right:0;bottom:0;width:100%">'
           f'{pine(60, 200, 150, GREEN, 3)}{pine(790, 200, 170, GREEN, 4)}{gift(150, 170, .9, RED, GOLD)}{gift(700, 172, .8, GREEN, RED)}</svg>')
    return (f'<div class="page">{border_holly(top_only=True)}{art}<div style="position:absolute;left:0.85in;right:0.85in;top:0.7in;font-size:13.5pt">{head}{rows}{did}{wish}{sign}</div>{foot()}</div>')

def letter_draw():
    """For little ones: big name line and a frame to draw the present they'd like."""
    return (f'<div class="page" style="background:#fff">{candy_frame()}'
            f'<div style="position:absolute;left:0.75in;right:0.75in;top:0.72in;text-align:center">'
            f'<div class="script" style="font-size:52pt;color:{DRED};line-height:1">Dear Santa,</div>'
            f'<div class="sans" style="font-size:14pt;margin-top:10pt;font-weight:600;color:{GREEN}">this is what I would like for Christmas!</div></div>'
            f'<div style="position:absolute;left:0.9in;right:0.9in;top:2.1in;bottom:3.0in;border:3px solid {INK};border-radius:22px;background:'
            f'radial-gradient(circle at 20px 20px, {SKY} 3px, transparent 4px) 0 0 / 40px 40px"></div>'
            f'<svg viewBox="-150 -150 300 300" style="position:absolute;left:0.6in;bottom:1.55in;width:1.6in">{santa(0, 0, 1, outline=True)}</svg>'
            f'<svg viewBox="-110 -140 220 220" style="position:absolute;right:0.6in;bottom:1.45in;width:1.5in">{reindeer(0, 0, 1, outline=True)}</svg>'
            f'<div class="sans" style="position:absolute;left:2.4in;right:2.3in;bottom:1.55in;font-size:13pt;text-align:center">'
            f'<div style="height:0.5in;border-bottom:2px solid {INK}"></div><div style="font-size:9pt;margin-top:4pt;color:#7a746b">MY NAME</div></div>{foot()}</div>')

def wish_list():
    cols = ""
    for title, n in (("My wish list", 10), ("Gifts I'll give", 6)):
        items = "".join(f'<div style="display:flex;gap:9pt;align-items:center;height:0.4in;border-bottom:1px dotted {INK}88"><span style="width:13pt;height:13pt;border:1.6px solid {RED};border-radius:50%;flex:none"></span></div>' for _ in range(n))
        cols += f'<div><div class="script" style="font-size:30pt;color:{GREEN}">{title}</div>{items}</div>'
    art = (f'<svg viewBox="0 0 400 520" style="position:absolute;right:0.5in;bottom:0.6in;width:2.6in">{tree(200, 510, 420, GREEN)}'
           + "".join(bauble(x, y, 16, c, GOLD) for x, y, c in [(160, 300, RED), (240, 260, GOLD), (200, 380, RED), (130, 420, GOLD), (270, 410, RED), (205, 200, RED)]) + '</svg>')
    return (f'<div class="page">{flakes(850, 1100, 0, 1)}<div style="position:absolute;inset:0.6in;border:3px double {RED};border-radius:16px"></div>{art}'
            f'<div style="position:absolute;left:1in;right:1in;top:0.9in;text-align:center"><div class="sans" style="font-size:9pt;letter-spacing:.35em;color:{RED};font-weight:600">CHRISTMAS</div>'
            f'<div class="script" style="font-size:60pt;line-height:1;color:{DRED}">Wish List</div><div style="font-size:12pt;margin-top:4pt">Name: <span style="display:inline-block;width:3in;border-bottom:1.5px solid {INK}"></span></div></div>'
            f'<div style="position:absolute;left:1in;width:3.9in;top:2.55in;display:flex;flex-direction:column;gap:0.25in">{cols}</div>{foot()}</div>')

def letterhead(body):
    head = (f'<div style="position:absolute;left:0;right:0;top:0;height:1.55in;background:{DRED};overflow:hidden">'
            f'<svg viewBox="0 0 850 160" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%">{flakes(850, 160, 22, 5, "#ffffff", .35)}</svg>'
            f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">'
            f'<div class="sans" style="font-size:8.5pt;letter-spacing:.42em;opacity:.85">FROM THE DESK OF</div><div class="script" style="font-size:46pt;line-height:1.05">Santa Claus</div>'
            f'<div class="sans" style="font-size:8pt;letter-spacing:.38em;opacity:.85">THE NORTH POLE · WORKSHOP NO. 1</div></div></div>'
            f'<div style="position:absolute;left:0;right:0;top:1.55in;height:0.12in;background:repeating-linear-gradient(90deg,{GOLD} 0 30px,{GREEN} 30px 60px)"></div>')
    sealsvg = f'<svg viewBox="0 0 200 200" style="position:absolute;right:0.7in;bottom:0.75in;width:1.35in;transform:rotate(-12deg)">{seal(100, 100, 92)}</svg>'
    return f'<div class="page">{head}{body}{sealsvg}{foot()}</div>'

def letter_from_santa():
    b = lambda w: f'<span style="display:inline-block;width:{w};border-bottom:1.3px solid {INK};height:1em;vertical-align:baseline"></span>'
    txt = (f'<p>Dear {b("2.4in")},</p>'
           f'<p>Ho ho ho! Your letter arrived at the North Pole post office this morning, and the elves brought it straight to my desk with a mug of cocoa.</p>'
           f'<p>I have been checking my list very carefully, and I am delighted to tell you that you are on the <b style="color:{RED}">Nice List</b> this year. '
           f'I was especially proud when you {b("3.1in")} {b("6.3in")}.</p>'
           f'<p>The reindeer are practising their rooftop landings, Mrs. Claus is baking enough gingerbread for the whole sleigh team, and the workshop is busy, busy, busy.</p>'
           f'<p>Keep being kind, keep helping at home, and don\'t forget to go to sleep early on Christmas Eve. I\'ll be keeping an eye out for {b("1.6in")}!</p>'
           f'<p>Merry Christmas, and lots of love,</p>')
    sign = f'<div class="script" style="font-size:44pt;color:{DRED};margin-top:2pt;line-height:1">Santa Claus</div><div class="sans" style="font-size:8pt;letter-spacing:.2em;color:#7a746b">P.S. The elves say hello, and so do the reindeer!</div>'
    body = f'<div style="position:absolute;left:0.95in;right:0.95in;top:2.2in;font-size:13.6pt;line-height:2.0">{txt.replace("<p>", "<p style=\"margin-bottom:8pt\">")}{sign}</div>'
    return letterhead(body)

def letter_blank():
    body = f'<div class="lines" style="--lh:0.4in;position:absolute;left:0.95in;right:0.95in;top:2.3in;bottom:2.3in"></div><div class="script" style="position:absolute;left:0.95in;top:1.92in;font-size:28pt;color:{DRED}">Dear</div>'
    return letterhead(body)

def certificate():
    line = lambda w: f'<span style="display:inline-block;width:{w};border-bottom:1.5px solid {INK}"></span>'
    orn = f'<svg viewBox="0 0 400 60" style="width:3.4in;margin:6pt auto"><path d="M10 30 H170 M230 30 H390" stroke="{GOLD}" stroke-width="3"/>{star(200, 30, 22, GOLD)}{star(150, 30, 8, RED)}{star(250, 30, 8, RED)}</svg>'
    return (f'<div class="page" style="background:{CREAM}"><div style="position:absolute;inset:0.42in;border:0.1in solid {DRED};border-radius:6px"></div>'
            f'<div style="position:absolute;inset:0.62in;border:2px solid {GOLD};border-radius:4px"></div>{border_holly()}'
            f'<div style="position:absolute;left:0.9in;right:0.9in;top:1.25in;text-align:center">'
            f'<div class="sans" style="font-size:9.5pt;letter-spacing:.45em;color:{GREEN};font-weight:600">OFFICIAL CERTIFICATE</div>'
            f'<div class="script" style="font-size:72pt;line-height:1;color:{DRED};margin-top:10pt">Nice List</div>{orn}'
            f'<div style="font-size:13pt;margin-top:8pt">This certifies that</div>'
            f'<div style="margin:16pt auto 0;width:5.2in;border-bottom:2px solid {INK};height:0.55in"></div>'
            f'<div style="font-size:13pt;line-height:1.7;margin-top:16pt">has been kind, thoughtful and helpful all year long<br>and is officially on Santa\'s <b style="color:{RED}">Nice List</b> for Christmas {line("0.8in")}.</div>'
            f'<div style="font-size:11pt;line-height:1.6;margin-top:12pt;color:#5a554e">Checked twice by the elves, approved by the reindeer,<br>and stamped by the North Pole Post Office.</div></div>'
            f'<div style="position:absolute;left:1.15in;right:1.15in;bottom:1.45in;display:flex;justify-content:space-between;align-items:flex-end">'
            f'<div style="text-align:center"><div class="script" style="font-size:34pt;color:{DRED};border-bottom:1.5px solid {INK};width:2.3in;line-height:1.2">Santa Claus</div>'
            f'<div class="sans" style="font-size:8pt;letter-spacing:.25em;margin-top:4pt">SANTA CLAUS</div></div>'
            f'<svg viewBox="0 0 200 200" style="width:1.4in">{seal(100, 100, 92, GREEN)}</svg>'
            f'<div style="text-align:center"><div style="border-bottom:1.5px solid {INK};width:2.1in;height:0.55in"></div><div class="sans" style="font-size:8pt;letter-spacing:.25em;margin-top:4pt">HEAD ELF</div></div></div>'
            f'{foot()}</div>')

def nice_list():
    rows = "".join(f'<div style="display:flex;align-items:flex-end;gap:8pt;height:0.4in;border-bottom:1px solid {INK}55"><span style="flex:1"></span>'
                   f'<span class="sans" style="font-size:8pt;color:{GREEN};font-weight:600;width:0.5in;text-align:center">NICE</span><span style="width:14pt;height:14pt;border:1.6px solid {GREEN};border-radius:3px;margin-bottom:4pt"></span>'
                   f'<span class="sans" style="font-size:8pt;color:{RED};font-weight:600;width:0.75in;text-align:center">CHECKED</span><span style="width:14pt;height:14pt;border:1.6px solid {RED};border-radius:3px;margin-bottom:4pt"></span></div>' for _ in range(14))
    scroll = (f'<div style="position:absolute;left:1.15in;right:1.15in;top:1.05in;bottom:0.9in;background:#fffaf0;box-shadow:0 0 0 2px {GOLD}88, 0 8px 18px rgba(0,0,0,.18);border-radius:6px">'
              f'<div style="position:absolute;left:-0.25in;right:-0.25in;top:-0.22in;height:0.44in;border-radius:0.22in;background:linear-gradient({GOLD},#9c7a2f)"></div>'
              f'<div style="position:absolute;left:-0.25in;right:-0.25in;bottom:-0.22in;height:0.44in;border-radius:0.22in;background:linear-gradient({GOLD},#9c7a2f)"></div>'
              f'<div style="position:absolute;left:0.5in;right:0.5in;top:0.45in;text-align:center"><div class="sans" style="font-size:8.5pt;letter-spacing:.35em;color:{RED};font-weight:600">SANTA\'S OFFICIAL</div>'
              f'<div class="script" style="font-size:56pt;color:{DRED};line-height:1">The Nice List</div><div style="font-size:10pt;color:#6b655c;margin-top:2pt">made a list · checked it twice</div></div>'
              f'<div style="position:absolute;left:0.5in;right:0.5in;top:2.05in">{rows}</div></div>')
    return f'<div class="page" style="background:{NIGHT}"><svg viewBox="0 0 850 1100" style="position:absolute;inset:0;width:100%;height:100%">{flakes(850, 1100, 40, 9, "#fff", .5)}</svg>{scroll}{foot()}</div>'

def envelope_labels():
    to = "".join(f'<div class="cut" style="background:#fff;border-radius:10px;padding:0.18in 0.25in;position:relative;box-shadow:inset 0 0 0 3px {c}">'
                 f'<div class="sans" style="font-size:8pt;letter-spacing:.3em;color:{c};font-weight:600">{top}</div><div class="script" style="font-size:30pt;line-height:1.05;color:{INK}">{name}</div>'
                 f'<div style="font-size:10pt;line-height:1.45">{addr}</div><svg viewBox="0 0 200 200" style="position:absolute;right:0.15in;top:0.15in;width:0.85in">{seal(100, 100, 92, c)}</svg></div>'
                 for top, name, addr, c in [("SPECIAL DELIVERY TO", "Santa Claus", "Toy Workshop, Candy Cane Lane<br>The North Pole · 0001", RED),
                                            ("AIR MAIL · BY REINDEER", "Santa Claus", "Toy Workshop, Candy Cane Lane<br>The North Pole · 0001", GREEN),
                                            ("SPECIAL DELIVERY FROM", "The North Pole", "Santa's Workshop<br>Please deliver by Christmas Eve", RED),
                                            ("PRIORITY · ELF POST", "The North Pole", "Santa's Workshop<br>Handle with Christmas cheer", GREEN)])
    addr = "".join(f'<div class="cut" style="background:#fff;border-radius:10px;padding:0.2in 0.25in;box-shadow:inset 0 0 0 3px {GOLD}">'
                   f'<div class="sans" style="font-size:8pt;letter-spacing:.3em;color:{GOLD};font-weight:700">TO</div>'
                   + "".join(f'<div style="border-bottom:1.2px solid {INK}66;height:0.34in"></div>' for _ in range(3)) + '</div>' for _ in range(2))
    stamps = ""
    art = [lambda: santa(0, 0, .42), lambda: reindeer(0, 14, .42), lambda: tree(0, 46, 90, GREEN), lambda: gift(0, 4, 1, RED, GOLD), lambda: snowflake(0, 0, 40, "#4c7a99"), lambda: star(0, 0, 40, GOLD)]
    for i in range(6):
        bg = ["#fdf3e7", "#e7f0ea", "#eef3f7"][i % 3]
        stamps += (f'<div style="display:flex;align-items:center;justify-content:center"><div style="width:1.05in;height:1.25in;padding:6px;background:radial-gradient(circle,transparent 4px,{bg} 4.5px) -4px -4px / 11px 11px;filter:drop-shadow(0 1px 1px rgba(0,0,0,.3))">'
                   f'<div style="width:100%;height:100%;background:{bg};border:1.2px solid {INK}55;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:3px">'
                   f'<svg viewBox="-60 -60 120 120" style="width:85%;flex:1">{art[i]()}</svg><div class="sans" style="font-size:6pt;letter-spacing:.12em;font-weight:600">NORTH POLE · {["5", "10", "25", "50", "1", "2"][i]}{"c" if i < 4 else " ★"}</div></div></div></div>')
    return (f'<div class="page" style="background:#f1e9dc"><div style="position:absolute;left:0.5in;right:0.5in;top:0.4in;text-align:center" class="script"><span style="font-size:30pt;color:{DRED}">North Pole Post</span></div>'
            f'<div style="position:absolute;left:0.5in;right:0.5in;top:1.05in;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1.85in);gap:0.28in">{to}{addr}</div>'
            f'<div style="position:absolute;left:0.5in;right:0.5in;bottom:0.6in;display:grid;grid-template-columns:repeat(6,1fr)">{stamps}</div>{foot()}</div>')

def reindeer_food():
    tops = ""
    for i in range(4):
        bg, ink_ = [(RED, "#fff"), (GREEN, "#fff"), ("#fff", DRED), (NIGHT, "#fff")][i]
        tops += (f'<div class="cut" style="background:{bg};color:{ink_};border-radius:8px;position:relative;overflow:hidden;text-align:center;padding:0.18in 0.2in">'
                 f'<div style="position:absolute;left:0;right:0;top:50%;border-top:1.5px dashed {ink_}66"></div>'
                 f'<div class="sans" style="position:absolute;right:6px;top:calc(50% - 12px);font-size:6pt;opacity:.7">fold</div>'
                 f'<div style="height:50%"></div>'
                 f'<svg viewBox="-110 -130 220 200" style="width:1.1in;margin:2pt auto 0">{reindeer(0, 0, .9, "#9a6a48")}</svg>'
                 f'<div class="sans" style="font-size:7.5pt;letter-spacing:.32em;font-weight:600;margin-top:2pt">MAGIC</div>'
                 f'<div class="script" style="font-size:28pt;line-height:1">Reindeer Food</div>'
                 f'<div style="font-size:8.5pt;line-height:1.35;margin-top:3pt;opacity:.9">Sprinkle on the lawn on Christmas Eve.<br>The moonlight makes it sparkle and<br>helps the reindeer find your home!</div></div>')
    recipe = (f'<div class="cut" style="grid-column:span 2;background:#fff;border-radius:10px;padding:0.2in 0.3in;display:flex;gap:0.3in;align-items:center;box-shadow:inset 0 0 0 3px {GREEN}">'
              f'<svg viewBox="-110 -130 220 200" style="width:1.2in;flex:none">{reindeer(0, 0, .95)}</svg><div style="font-size:10pt;line-height:1.5">'
              f'<div class="script" style="font-size:28pt;color:{GREEN};line-height:1">Reindeer food recipe</div>'
              f'Mix 1 cup of rolled oats with 2 spoonfuls of coloured sugar sprinkles (or a little birdseed). Spoon into a small clear bag, fold the topper over the top and staple. '
              f'<b>Wildlife friendly:</b> skip glitter and plastic sprinkles, so the birds can enjoy the leftovers too.</div></div>')
    return (f'<div class="page" style="background:#f6f0e6"><div style="position:absolute;left:0.5in;right:0.5in;top:0.42in;bottom:0.55in;display:grid;grid-template-columns:1fr 1fr;'
            f'grid-template-rows:3.55in 3.55in 1fr;gap:0.25in">{tops}{recipe}</div>{foot()}</div>')

def stop_sign():
    scene = (f'<svg viewBox="0 0 700 520" style="width:100%"><rect width="700" height="520" rx="30" fill="{NIGHT}"/>'
             f'{flakes(700, 520, 26, 3, "#fff", .55)}<circle cx="560" cy="110" r="55" fill="#f6edd2"/>'
             f'<path d="M0 420 Q350 360 700 420 V520 H0Z" fill="#fff"/>'
             f'<g transform="translate(120 300) scale(.8)"><path d="M0 0 h250 q40 0 30 30 l-20 40 h-260 z" fill="{RED}"/><path d="M-10 70 h300" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
             f'<path d="M260 0 q40 -10 40 -40" stroke="{GOLD}" stroke-width="8" fill="none"/>{gift(60, -18, .9, GREEN, GOLD)}{gift(140, -30, 1.1, GOLD, RED)}</g>'
             + "".join(reindeer(x, 330, .45, "#8a5a3c") for x in (420, 520, 620)) + '</svg>')
    return (f'<div class="page" style="background:{CREAM}">{candy_frame("0.4in", "0.2in")}'
            f'<div style="position:absolute;left:0.9in;right:0.9in;top:1in;text-align:center">'
            f'<div class="sans" style="font-size:10pt;letter-spacing:.45em;color:{GREEN};font-weight:600">ATTENTION, SLEIGH PILOT</div>'
            f'<div class="script" style="font-size:80pt;line-height:.95;color:{DRED};margin-top:8pt">Santa,<br>please stop here!</div>'
            f'<div style="margin:22pt auto 0;width:5.3in">{scene}</div>'
            f'<div style="font-size:13pt;margin-top:18pt">The children who live here have been <b style="color:{RED}">very good</b> this year.</div>'
            f'<div class="sans" style="font-size:9pt;letter-spacing:.25em;margin-top:8pt;color:#7a746b">COOKIES INSIDE · CARROTS BY THE DOOR</div></div>{foot()}</div>')

def plate_cards():
    def tent(title, sub, art, bg, ink_):
        return (f'<div class="cut" style="background:{bg};color:{ink_};border-radius:6px;position:relative;text-align:center">'
                f'<div style="position:absolute;left:0;right:0;top:50%;border-top:1.5px dashed {ink_}66"></div>'
                f'<div class="sans" style="position:absolute;left:8px;top:calc(50% - 13px);font-size:6pt;opacity:.6">fold</div>'
                f'<div style="position:absolute;left:0;right:0;top:52%;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 0.2in">'
                f'<svg viewBox="-80 -80 160 160" style="width:0.95in">{art}</svg><div class="script" style="font-size:30pt;line-height:1">{title}</div>'
                f'<div style="font-size:9pt;opacity:.85">{sub}</div></div></div>')
    cookie = ('<circle r="56" fill="#c98a4e"/><circle r="56" fill="none" stroke="#a96d36" stroke-width="5"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#4b2e1e"/>' for x, y in [(-24, -18), (14, -30), (24, 10), (-8, 22), (-30, 18), (6, -4)]))
    carrot = (f'<g transform="rotate(35)"><path d="M-16 -50 L16 -50 L0 60 Z" fill="#e8822f"/><path d="M-8 -30 h10 M-4 -4 h10 M-2 22 h8" stroke="#c4621c" stroke-width="3"/>'
              f'<path d="M0 -50 q-24 -24 -14 -36 M0 -50 q0 -30 10 -38 M0 -50 q20 -22 30 -18" stroke="{GREEN}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
    milk = (f'<path d="M-30 -50 h60 l-6 106 h-48 z" fill="#ffffff" stroke="#9fb6cc" stroke-width="5"/><path d="M-27 -20 h54 l-4 74 h-46 z" fill="#f2f6fa"/>')
    note = lambda t, s: (f'<div class="cut" style="background:#fff;border-radius:10px;padding:0.22in 0.3in;box-shadow:inset 0 0 0 3px {RED}">'
                         f'<div class="script" style="font-size:28pt;color:{DRED};line-height:1">{t}</div><div style="font-size:10pt;margin-top:4pt">{s}</div>'
                         f'<div class="lines" style="--lh:0.32in;height:0.96in;margin-top:4pt"></div><div style="font-size:10pt;margin-top:6pt">Love, <span style="display:inline-block;width:2in;border-bottom:1px solid {INK}"></span></div></div>')
    return (f'<div class="page" style="background:#f3ece1"><div style="position:absolute;left:0.5in;right:0.5in;top:0.45in;height:6.3in;display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.22in">'
            f'{tent("For Santa", "cookies + milk, with love", cookie, "#fff", DRED)}{tent("For the reindeer", "crunchy carrots for the journey", carrot, GREEN, "#fff")}'
            f'{tent("Santa\'s milk", "a little something to drink", milk, RED, "#fff")}</div>'
            f'<div style="position:absolute;left:0.5in;right:0.5in;bottom:0.6in;display:grid;grid-template-columns:1fr 1fr;gap:0.25in">'
            f'{note("Dear Santa,", "We left you a little treat:")}{note("Dear Santa,", "Our reindeer questions:")}</div>{foot()}</div>')

def thank_you():
    def half(bg):
        return (f'<div style="position:relative;height:50%;background:{bg};overflow:hidden">'
                f'<div style="position:absolute;inset:0.45in 0.6in;border:2px solid {GOLD};border-radius:10px;background:#fffdf8;padding:0.3in 0.45in">'
                f'<div class="sans" style="font-size:8pt;letter-spacing:.35em;color:{GREEN};font-weight:600">CHRISTMAS MORNING · NORTH POLE</div>'
                f'<div class="script" style="font-size:36pt;color:{DRED};line-height:1.1">Thank you!</div>'
                f'<div style="font-size:11.5pt;line-height:1.6;margin-top:4pt">Dear <span style="display:inline-block;width:2.2in;border-bottom:1.2px solid {INK}"></span>,<br>'
                f'Thank you for the delicious treats! The reindeer loved their carrots and I ate every crumb. '
                f'Your home was one of the cosiest stops on my whole journey. Have a very merry Christmas!</div>'
                f'<div class="script" style="font-size:30pt;color:{DRED};margin-top:4pt">Santa</div></div>'
                f'<svg viewBox="-150 -150 300 300" style="position:absolute;right:0.9in;bottom:0.65in;width:1.75in">{santa(0, 0, 1)}</svg></div>')
    return f'<div class="page" style="background:#fff">{half("#f2e8db")}<div style="position:absolute;left:0;right:0;top:50%;border-top:1.5px dashed #0005"></div>{half("#e6efe9")}{foot()}</div>'

def colouring():
    o = 'fill="none" stroke="#2b2a2a" stroke-width="4" stroke-linejoin="round"'
    trunk = '<rect x="380" y="900" width="70" height="80" fill="#fff" stroke="#2b2a2a" stroke-width="4"/>'
    layers = "".join(f'<path d="M{415 - w} {b} Q{415} {b + 30} {415 + w} {b} L415 {tp} Z" fill="#fff" stroke="#2b2a2a" stroke-width="4" stroke-linejoin="round"/>'
                     for w, b, tp in [(300, 910, 520), (250, 720, 360), (190, 540, 220)])
    garl = "".join(f'<path d="M{415 - w} {y} Q415 {y + 50} {415 + w} {y - 20}" {o}/>' for w, y in [(230, 820), (180, 640), (120, 470)])
    balls = "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="#fff" stroke="#2b2a2a" stroke-width="4"/><path d="M{x - 22} {y} Q{x} {y + 10} {x + 22} {y}" {o}/>'
                    for x, y in [(300, 860), (520, 840), (420, 700), (330, 620), (500, 600), (400, 450), (560, 760), (260, 760)])
    star_ = f'<g transform="translate(415 200)"><polygon points="0,-70 18,-22 68,-22 28,8 44,56 0,28 -44,56 -28,8 -68,-22 -18,-22" {o.replace("none", "#fff")}/></g>'
    gifts = "".join(f'<g transform="translate({x} {y}) scale({s})"><rect x="-60" y="-40" width="120" height="90" fill="#fff" stroke="#2b2a2a" stroke-width="4"/>'
                    f'<rect x="-68" y="-62" width="136" height="26" fill="#fff" stroke="#2b2a2a" stroke-width="4"/><rect x="-10" y="-62" width="20" height="112" fill="#fff" stroke="#2b2a2a" stroke-width="4"/>'
                    f'<path d="M0 -62 C-40 -110 -60 -60 0 -62 C60 -60 40 -110 0 -62Z" {o}/></g>' for x, y, s in [(140, 950, 1.0), (690, 940, 1.1), (250, 990, .7)])
    flk = "".join(f'<g transform="translate({x} {y})">{snowflake(0, 0, 26, "#2b2a2a")}</g>' for x, y in [(90, 120), (740, 160), (120, 420), (760, 480), (80, 700), (780, 700)])
    return (f'<div class="page" style="background:#fff"><div style="position:absolute;left:0.6in;right:0.6in;top:0.45in;text-align:center">'
            f'<div class="script" style="font-size:44pt;line-height:1">Colour in the Christmas tree!</div></div>'
            f'<svg viewBox="0 0 850 1050" style="position:absolute;left:0.5in;right:0.5in;top:1.25in;bottom:0.5in;width:calc(100% - 1in);height:calc(100% - 1.75in)">'
            f'{flk}{trunk}{layers}{garl}{balls}{star_}{gifts}</svg>{foot()}</div>')

def build(size):
    P = [intro(), letter_to_santa(), letter_draw(), wish_list(), letter_from_santa(), letter_blank(), certificate(), nice_list(),
         envelope_labels(), reindeer_food(), stop_sign(), plate_cards(), thank_you(), colouring()]
    return CSS, P

if __name__ == "__main__":
    out = sys.argv[1]
    for size in ("letter", "a4"):
        css, pages = build(size)
        render(css, pages, size, f"{out}/letter-from-santa-kit-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print("pages", len(pages))
