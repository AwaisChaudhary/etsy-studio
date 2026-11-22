"""New Year's Eve Party Games 2027 printable (batch 5, lanes g + d). All artwork drawn here as SVG.
Usage: python3 b5_nye.py <out_dir>  -> new-years-eve-party-games-US-Letter.pdf / -A4.pdf"""
import math, random, sys
sys.path.insert(0, ".")
from render import render

NAVY, NAVY2, GOLD, GOLD2, CHAMP, ROSE, INK, TEAL = "#16203d", "#24315a", "#c9a24a", "#e8cf8a", "#fbf6ea", "#c8607a", "#1c2440", "#3f8f9a"
NAME = "new-years-eve-party-games"
FOOT = "Purl &amp; Paper · New Year's Eve Party Games 2027"
CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: var(--pw); overflow: hidden; }}
body {{ font-family: Poppins, sans-serif; color: {INK}; }}
.page {{ width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: {CHAMP}; contain: strict; }}
.dark {{ background: {NAVY}; color: {CHAMP}; }}
.script {{ font-family: "TeX Gyre Chorus", Lora, serif; font-weight: normal; }}
.frame {{ position: absolute; inset: 0.32in; border: 2px solid {GOLD}; border-radius: 0.14in; }}
.frame::after {{ content: ""; position: absolute; inset: 0.07in; border: 1px solid {GOLD}88; border-radius: 0.09in; }}
.hd {{ position: absolute; left: 0.6in; right: 0.6in; top: 0.58in; text-align: center; }}
.hd h1 {{ font-family: "TeX Gyre Chorus", Lora, serif; font-weight: normal; font-size: 44pt; line-height: 1; color: {NAVY}; }}
.hd .k {{ font: 600 9pt Poppins; letter-spacing: .22em; text-transform: uppercase; color: {ROSE}; margin-top: 0.06in; }}
.hd p {{ font: 9.5pt/1.45 Poppins; margin: 0.08in auto 0; max-width: 6.4in; color: #4a5068; }}
.body {{ position: absolute; left: 0.62in; right: 0.62in; top: 2.0in; bottom: 0.66in; }}
.foot {{ position: absolute; bottom: 0.42in; left: 0; right: 0; text-align: center; font: 7pt Poppins; color: #9a8f78; }}
.cut {{ outline: 1px dashed rgba(0,0,0,.3); outline-offset: -1px; }}
.ln {{ border-bottom: 1px solid {INK}55; height: 0.3in; }}
svg {{ display: block; }}
"""


# ---------- motifs (original SVG) ----------
def star(cx, cy, r, col, pts=5, inner=.45):
    p = []
    for i in range(pts * 2):
        a = -math.pi / 2 + i * math.pi / pts; rr = r if i % 2 == 0 else r * inner
        p.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{col}"/>'


def sparkle(cx, cy, r, col):
    return (f'<path d="M{cx},{cy - r} Q{cx + r * .14},{cy - r * .14} {cx + r},{cy} Q{cx + r * .14},{cy + r * .14} {cx},{cy + r} '
            f'Q{cx - r * .14},{cy + r * .14} {cx - r},{cy} Q{cx - r * .14},{cy - r * .14} {cx},{cy - r}Z" fill="{col}"/>')


def burst(cx, cy, r, col, n=16, seed=1):
    rnd = random.Random(seed); out = []
    for i in range(n):
        a = i * 2 * math.pi / n + rnd.uniform(-.05, .05); l1, l2 = r * .28, r * rnd.uniform(.78, 1)
        x1, y1, x2, y2 = cx + l1 * math.cos(a), cy + l1 * math.sin(a), cx + l2 * math.cos(a), cy + l2 * math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{r * .045:.1f}" stroke-linecap="round"/>')
        out.append(f'<circle cx="{cx + r * 1.08 * math.cos(a):.1f}" cy="{cy + r * 1.08 * math.sin(a):.1f}" r="{r * .035:.1f}" fill="{col}"/>')
    return "".join(out) + f'<circle cx="{cx}" cy="{cy}" r="{r * .08:.1f}" fill="{col}"/>'


def glass(cx, by, s, col, fizz=GOLD2):
    """Coupe glass, base at by."""
    w, h = 46 * s, 150 * s
    return (f'<path d="M{cx - w},{by - h} Q{cx},{by - h + 62 * s} {cx + w},{by - h} Z" fill="{fizz}" stroke="{col}" stroke-width="{3 * s:.1f}"/>'
            f'<line x1="{cx}" y1="{by - h + 31 * s:.1f}" x2="{cx}" y2="{by - 6 * s:.1f}" stroke="{col}" stroke-width="{4 * s:.1f}"/>'
            f'<ellipse cx="{cx}" cy="{by - 4 * s:.1f}" rx="{28 * s:.1f}" ry="{6 * s:.1f}" fill="{col}"/>'
            + "".join(f'<circle cx="{cx + dx * s:.1f}" cy="{by - h - dy * s:.1f}" r="{rr * s:.1f}" fill="none" stroke="{col}" stroke-width="{1.6 * s:.1f}"/>'
                      for dx, dy, rr in ((-10, 14, 4), (6, 28, 3), (-2, 44, 2.4))))


def clock(cx, cy, r, face=CHAMP, rim=GOLD, hand=NAVY, hour=11.9):
    ha = -math.pi / 2 + (hour % 12) * math.pi / 6
    ticks = "".join(f'<line x1="{cx + r * .78 * math.cos(a):.1f}" y1="{cy + r * .78 * math.sin(a):.1f}" x2="{cx + r * .9 * math.cos(a):.1f}" y2="{cy + r * .9 * math.sin(a):.1f}" '
                    f'stroke="{hand}" stroke-width="{r * (.06 if i % 3 == 0 else .03):.1f}" stroke-linecap="round"/>'
                    for i, a in enumerate(-math.pi / 2 + k * math.pi / 6 for k in range(12)))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{face}" stroke="{rim}" stroke-width="{r * .1:.1f}"/>{ticks}'
            f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r * .62:.1f}" stroke="{hand}" stroke-width="{r * .07:.1f}" stroke-linecap="round"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{cx + r * .45 * math.cos(ha):.1f}" y2="{cy + r * .45 * math.sin(ha):.1f}" stroke="{ROSE}" stroke-width="{r * .05:.1f}" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .07:.1f}" fill="{hand}"/>')


def balloon(cx, cy, s, col):
    return (f'<path d="M{cx},{cy + 52 * s:.1f} C{cx + 4 * s},{cy + 80 * s} {cx - 8 * s},{cy + 100 * s} {cx + 2 * s},{cy + 130 * s}" fill="none" stroke="{GOLD}" stroke-width="{1.6 * s:.1f}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{38 * s:.1f}" ry="{48 * s:.1f}" fill="{col}"/>'
            f'<path d="M{cx - 6 * s},{cy + 54 * s} L{cx + 6 * s},{cy + 54 * s} L{cx},{cy + 46 * s}Z" fill="{col}"/>'
            f'<ellipse cx="{cx - 14 * s:.1f}" cy="{cy - 18 * s:.1f}" rx="{7 * s:.1f}" ry="{13 * s:.1f}" fill="#ffffff55" transform="rotate(20 {cx - 14 * s:.1f} {cy - 18 * s:.1f})"/>')


def hat(cx, by, s, col, band=GOLD):
    return (f'<path d="M{cx - 40 * s},{by} L{cx},{by - 110 * s} L{cx + 40 * s},{by}Z" fill="{col}"/>'
            f'<path d="M{cx - 27 * s},{by - 36 * s} L{cx + 27 * s},{by - 36 * s}" stroke="{band}" stroke-width="{7 * s:.1f}"/>'
            f'<path d="M{cx - 14 * s},{by - 72 * s} L{cx + 14 * s},{by - 72 * s}" stroke="{band}" stroke-width="{6 * s:.1f}"/>'
            + "".join(f'<circle cx="{cx + dx * s:.1f}" cy="{by - 116 * s + dy * s:.1f}" r="{7 * s:.1f}" fill="{band}"/>' for dx, dy in ((0, 0), (-8, -6), (8, -6))))


def confetti(w, h, n, seed, cols=(GOLD, ROSE, TEAL, GOLD2)):
    rnd = random.Random(seed); out = []
    for _ in range(n):
        x, y, c, a = rnd.uniform(0, w), rnd.uniform(0, h), rnd.choice(cols), rnd.uniform(0, 180)
        k = rnd.random()
        if k < .4: out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="9" height="4" fill="{c}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>')
        elif k < .7: out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="{c}"/>')
        else: out.append(sparkle(round(x), round(y), 6, c))
    return "".join(out)


def svg(vb, inner, style=""):
    return f'<svg viewBox="{vb}" style="{style}">{inner}</svg>'


def page(title, kicker, intro, body, top=None, dark=False):
    st = f' style="top:{top}"' if top else ""
    return (f'<div class="page"><div class="frame"></div><div class="hd"><h1>{title}</h1><div class="k">{kicker}</div>'
            + (f'<p>{intro}</p>' if intro else "") + f'</div><div class="body"{st}>{body}</div><div class="foot">{FOOT}</div></div>')


# ---------- cover ----------
GAMES = ["New Year's Eve Bingo (24 cards)", "Traditions Around the World Trivia", "Who's Most Likely To… in 2027", "Resolution Would You Rather",
         "Word Scramble", "2027 Predictions Cards", "My 2026 Year in Review", "Countdown to Midnight Bags (6 hours)", "Score Sheet & Answer Keys"]


def cover():
    art = (burst(200, 170, 120, GOLD, 18, 1) + burst(860, 130, 90, ROSE, 14, 2) + burst(560, 90, 60, GOLD2, 12, 3)
           + confetti(1100, 300, 70, 4) + glass(470, 300, 1.2, GOLD) + glass(630, 300, 1.2, GOLD))
    li = "".join(f'<div style="display:flex;gap:0.12in;align-items:center;font:10.5pt Poppins;padding:0.055in 0;border-bottom:1px dotted {GOLD}">'
                 f'{svg("0 0 100 100", sparkle(50, 50, 44, GOLD if i % 2 else ROSE), "width:0.2in")}{g}</div>' for i, g in enumerate(GAMES))
    return (f'<div class="page dark"><div class="frame"></div>'
            f'{svg("0 0 1100 310", art, "position:absolute;left:0.7in;top:0.7in;width:calc(100% - 1.4in)")}'
            f'<div style="position:absolute;left:0;right:0;top:3.55in;text-align:center">'
            f'<div style="font:600 10pt Poppins;letter-spacing:.4em;color:{GOLD2}">HELLO 2027</div>'
            f'<div class="script" style="font-size:62pt;line-height:.98;color:{CHAMP};margin-top:0.06in">New Year\'s Eve<br>Party Games</div>'
            f'<div style="font:600 9.5pt Poppins;letter-spacing:.22em;text-transform:uppercase;color:{GOLD};margin-top:0.14in">9 printable games · families, friends &amp; office parties</div></div>'
            f'<div style="position:absolute;left:1.55in;right:1.55in;top:6.4in;color:{CHAMP}">{li}</div>'
            f'<div style="position:absolute;left:1in;right:1in;bottom:0.7in;text-align:center;font:8.5pt/1.5 Poppins;color:{GOLD2}">Print at 100% (actual size). Print as many copies as your party needs. Answer keys at the back.</div></div>')


# ---------- bingo ----------
WORDS = ["Confetti", "Midnight", "Countdown", "Fireworks", "Sparkler", "Toast", "Cheers", "Resolution", "Balloons", "Party Hat",
         "Noisemaker", "Streamers", "Glitter", "Clock", "Ball Drop", "Auld Lang Syne", "Bubbly", "Mocktail", "Dance", "Calendar",
         "January", "Goals", "Fresh Start", "Disco Ball", "Snacks", "Selfie", "Tiara", "Bow Tie", "Sequins", "Party Popper",
         "Playlist", "Hugs", "Wishes", "Stars", "Celebrate", "2027", "Fizz", "Sparkle", "Midnight Kiss", "Happy New Year"]
ICON = {"Stars": lambda: star(50, 54, 40, GOLD), "Clock": lambda: clock(50, 50, 38), "Balloons": lambda: balloon(50, 38, .62, ROSE),
        "Party Hat": lambda: hat(50, 90, .72, TEAL), "Toast": lambda: glass(38, 96, .6, NAVY) + glass(62, 96, .6, NAVY), "Fireworks": lambda: burst(50, 50, 40, ROSE, 14, 9),
        "Sparkle": lambda: sparkle(50, 50, 40, GOLD), "Bubbly": lambda: glass(50, 96, .62, NAVY)}


def bingo_card(n, words):
    hdr = "".join(f'<div style="background:{[NAVY, ROSE][i % 2]};color:#fff;font:700 20pt Poppins;display:flex;align-items:center;justify-content:center;border-radius:0.05in">{c}</div>' for i, c in enumerate("BINGO"))
    cells = ""
    for k, w in enumerate(words):
        if k == 12:
            cells += (f'<div style="background:{NAVY};border-radius:0.05in;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{GOLD2}">'
                      f'{svg("0 0 100 100", burst(50, 50, 40, GOLD, 12, 5), "width:0.36in")}<div style="font:700 7.5pt Poppins;letter-spacing:.12em">FREE</div></div>')
        else:
            ic = ICON.get(w)
            art = svg("0 0 100 100", ic(), "width:0.28in;margin-bottom:0.02in") if ic else ""
            cells += (f'<div style="border:1.5px solid {INK}30;border-radius:0.05in;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;'
                      f'font:600 8.6pt/1.1 Poppins;padding:0 0.04in;background:#fff">{art}{w}</div>')
    return (f'<div style="display:flex;flex-direction:column;height:100%"><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.05in">'
            f'<div class="script" style="font-size:22pt;color:{NAVY};line-height:1">New Year\'s Eve Bingo</div><div style="font:600 7.5pt Poppins;color:#9a8f78">CARD {n:02d}</div></div>'
            f'<div style="display:grid;grid-template-columns:repeat(5,1fr);grid-template-rows:0.4in repeat(5,1fr);gap:0.045in;flex:1">{hdr}{cells}</div></div>')


def bingo_pages():
    rnd = random.Random(2027); out = []
    for pg in range(12):
        cards = []
        for j in range(2):
            ws = rnd.sample(WORDS, 24); ws.insert(12, "FREE"); cards.append(bingo_card(pg * 2 + j + 1, ws))
        out.append(f'<div class="page"><div style="position:absolute;inset:0.45in 0.6in;display:grid;grid-template-rows:1fr 1fr;gap:0.42in">'
                   + "".join(f'<div>{c}</div>' for c in cards) + f'</div><div style="position:absolute;left:0;right:0;top:50%;border-top:1px dashed #0004"></div>'
                   f'<div class="foot" style="bottom:0.2in">{FOOT}</div></div>')
    return out


def bingo_caller():
    rules = ("Give each player a card and a pen or a pile of confetti, sweets or buttons as markers. The caller cuts out the word squares below, "
             "mixes them in a bowl or party hat and reads them out one at a time. Mark the word if it's on your card. The first player with 5 in a row "
             "(across, down or diagonal) shouts <b>BINGO!</b> For a longer game, play for 4 corners, an X, or a full card at midnight.")
    grid = "".join(f'<div class="cut" style="display:flex;align-items:center;justify-content:center;text-align:center;font:600 9pt Poppins;height:0.52in;background:#fff">{w}</div>' for w in WORDS)
    body = (f'<p style="font:10pt/1.5 Poppins;margin-bottom:0.22in">{rules}</p>'
            f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:0">{grid}</div>')
    return page("Bingo: how to play", "Caller's word squares", None, body, top="1.55in")


# ---------- trivia ----------
TRIVIA = [("In Spain, how many grapes do people eat at the stroke of midnight?", ["7", "12", "21"], 1),
          ("In which city does a famous lit-up ball drop at midnight in Times Square?", ["Chicago", "London", "New York"], 2),
          ("What is the Scottish name for New Year's Eve celebrations?", ["Hogmanay", "Ceilidh", "Burns Night"], 0),
          ("In Scotland, the 'first foot' over the doorstep after midnight traditionally brings what gift?", ["A candle", "A lump of coal", "A loaf of bread and a fish"], 1),
          ("Japanese Buddhist temples ring their bells how many times on New Year's Eve?", ["12", "60", "108"], 2),
          ("In Denmark, what do people traditionally throw at friends' front doors?", ["Old plates", "Rice", "Snowballs"], 0),
          ("In Brazil, many people wear which colour on New Year's Eve for peace?", ["Red", "White", "Gold"], 1),
          ("In the Philippines, families often display how many round fruits for luck?", ["3", "8", "12"], 2),
          ("Which song is traditionally sung at midnight in many English-speaking countries?", ["Auld Lang Syne", "Jingle Bells", "Happy Days"], 0),
          ("Which Scottish poet wrote down the words of 'Auld Lang Syne'?", ["Walter Scott", "Robert Burns", "Robert Louis Stevenson"], 1),
          ("In Colombia, why do some people walk around the block with an empty suitcase?", ["To find lost luck", "For a year of travel", "To carry away bad memories"], 1),
          ("In Greece, what fruit is smashed at the front door for good luck?", ["Pomegranate", "Lemon", "Fig"], 0),
          ("January is named after Janus, a Roman god with how many faces?", ["One", "Two", "Four"], 1),
          ("In Italy, wearing what colour underwear on New Year's Eve is said to bring luck?", ["Green", "Blue", "Red"], 2),
          ("Black-eyed peas eaten for luck in the US South are served in which dish?", ["Hoppin' John", "Gumbo", "Jambalaya"], 0),
          ("What are oliebollen, eaten in the Netherlands on New Year's Eve?", ["Cheese balls", "Fried dough balls", "Herring rolls"], 1),
          ("In Ecuador, people burn life-size figures called 'años viejos'. What does that mean?", ["New hopes", "Fire dolls", "Old years"], 2),
          ("Many Germans watch which short British comedy sketch every New Year's Eve?", ["Dinner for One", "Mr Bean", "The Two Ronnies"], 0),
          ("Which of these Pacific island nations is among the very first to welcome the new year?", ["Hawaii (USA)", "Kiribati", "Samoa (American)"], 1),
          ("Lunar New Year 2027 begins the Year of which animal?", ["Dragon", "Horse", "Goat"], 2)]


def trivia_pages():
    out = []
    for half in range(2):
        qs = ""
        for i in range(10):
            n = half * 10 + i; q, opts, _ = TRIVIA[n]
            o = "".join(f'<span style="margin-right:0.28in">{"ABC"[k]}) {x}</span>' for k, x in enumerate(opts))
            qs += (f'<div style="padding:0.11in 0;border-bottom:1px dotted {GOLD}"><div style="font:10.8pt/1.4 Poppins"><b style="color:{ROSE}">{n + 1}.</b> {q}</div>'
                   f'<div style="font:10pt Poppins;color:#4a5068;margin-top:0.05in;padding-left:0.24in">{o}</div></div>')
        name = '<div style="display:flex;gap:0.2in;font:600 9pt Poppins;margin-bottom:0.06in"><div style="flex:1">Name / team: <span style="display:inline-block;width:3in;border-bottom:1px solid #0006"></span></div><div>Score: ____ / 10</div></div>'
        out.append(page("Around the World", f"New Year traditions trivia · part {half + 1}", "Circle A, B or C. One point for each right answer.", name + qs, top="1.82in"))
    return out


# ---------- cards ----------
LIKELY = ["…run a marathon in 2027", "…still be eating leftovers in February", "…keep their resolution all year", "…be asleep before midnight",
          "…start a new hobby and actually stick with it", "…go viral online", "…travel somewhere new", "…learn a new language",
          "…forget what year it is until March", "…throw the next party", "…cry at midnight", "…make a wish on every candle",
          "…get a new pet", "…read 50 books", "…be first on the dance floor", "…text 'Happy New Year' at 12:01 sharp",
          "…start a business", "…win this game", "…move house", "…learn to cook something fancy",
          "…plan next year's party already", "…join a gym and go twice", "…redecorate their whole home", "…say 'this is my year' and mean it"]
WYR = ["Give up coffee or give up chocolate for all of 2027?", "Wake up early every day or stay up late every night?", "Learn an instrument or learn a language this year?",
       "Travel to a beach or to the mountains in 2027?", "Run a 10K or read 20 books?", "Have a no-spend month or a no-phone weekend?",
       "Cook every meal at home for a month or try 12 new restaurants?", "Keep a daily journal or take a photo every day?",
       "Spend New Year's Eve in a big city or a cosy cabin?", "Know your 2027 highlights now or be totally surprised?",
       "Redo 2026 or skip straight to 2028?", "Have a clean house all year or a perfect wardrobe?",
       "Make one huge resolution or twelve tiny ones?", "Watch fireworks in the cold or watch the countdown on TV in pyjamas?",
       "Go on a road trip or a train trip?", "Get 30 extra minutes of sleep or 30 extra minutes of free time every day?",
       "Learn to dance or learn to sing?", "Have a garden full of vegetables or a garden full of flowers?",
       "Give up social media or give up TV for a month?", "Celebrate your birthday twice or New Year twice in 2027?",
       "Plan every weekend or keep every weekend open?", "Write a book or run a café for a day?",
       "Spend a day with no clocks or a day with no plans?", "Only eat breakfast foods or only eat desserts for a week?"]


def card_grid(items, title, accent, icon):
    cards = "".join(f'<div class="cut" style="position:relative;padding:0.16in 0.18in;display:flex;flex-direction:column;justify-content:center;background:#fff">'
                    f'{svg("0 0 100 100", icon, "position:absolute;right:0.1in;top:0.1in;width:0.26in;opacity:.9")}'
                    f'<div style="font:600 7pt Poppins;letter-spacing:.18em;color:{accent};text-transform:uppercase">{title}</div>'
                    f'<div style="font:12pt/1.38 Lora,serif;margin-top:0.08in">{it}</div></div>' for it in items)
    return f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;grid-auto-rows:1.95in;gap:0">{cards}</div>'


def likely_pages():
    return [page("Who's Most Likely To…", "in 2027 · cut out the cards", "Read a card and on 3, everyone points at the person most likely to. Most fingers keeps the card!",
                 card_grid(LIKELY[i:i + 12], "Most likely to", ROSE, sparkle(50, 50, 40, GOLD)), top="1.95in") for i in (0, 12)]


def wyr_pages():
    return [page("Would You Rather", "resolution edition · cut out the cards", "Take turns reading a card. Everyone picks, then explain your choice in one sentence.",
                 card_grid(WYR[i:i + 12], "Would you rather", TEAL, star(50, 54, 38, GOLD)), top="1.95in") for i in (0, 12)]


# ---------- scramble ----------
SCR = ["CONFETTI", "MIDNIGHT", "COUNTDOWN", "FIREWORKS", "SPARKLER", "RESOLUTION", "CELEBRATE", "BALLOON", "STREAMER", "GLITTER",
       "JANUARY", "CALENDAR", "NOISEMAKER", "CHEERS", "TOAST", "TIARA", "DISCO", "PARTY", "WISHES", "SEQUINS"]


def scramble(w, seed):
    r = random.Random(seed); s = w
    while s == w: l = list(w); r.shuffle(l); s = "".join(l)
    return s


def scramble_page():
    rows = "".join(f'<div style="display:flex;align-items:center;gap:0.18in;padding:0.05in 0;border-bottom:1px dotted {GOLD}"><b style="width:0.3in;color:{ROSE};font:700 10pt Poppins">{i + 1}.</b>'
                   f'<div style="width:2.2in;font:700 12.5pt Poppins;letter-spacing:.2em;color:{NAVY}">{scramble(w, i)}</div><div style="flex:1;border-bottom:1px solid #0005;height:0.26in"></div></div>'
                   for i, w in enumerate(SCR))
    return page("Word Scramble", "unscramble the party words", "Set a timer for 3 minutes. The player with the most correct words wins.", rows, top="1.82in")


# ---------- predictions + year in review ----------
def predictions_page():
    qs = ["The biggest news story of 2027 will be…", "I will finally learn…", "The song of the year will be…", "Something new I'll try…",
          "A place I'll visit…", "The price of a coffee will be…", "My word for 2027 is…"]
    def card(n):
        lines = "".join(f'<div style="font:8.8pt Poppins;margin-top:0.07in">{q}</div><div class="ln" style="height:0.2in"></div>' for q in qs)
        return (f'<div class="cut" style="padding:0.18in 0.24in;background:#fff;position:relative">'
                f'{svg("0 0 200 100", burst(40, 50, 34, GOLD, 12, n) + burst(160, 40, 24, ROSE, 10, n + 3), "position:absolute;right:0.15in;top:0.1in;width:0.9in")}'
                f'<div class="script" style="font-size:24pt;color:{NAVY};line-height:1">My 2027 Predictions</div>'
                f'<div style="font:600 7.5pt Poppins;letter-spacing:.18em;color:{ROSE}">NAME ______________ · SEAL &amp; OPEN NEXT NEW YEAR\'S EVE</div>{lines}</div>')
    return (f'<div class="page"><div style="position:absolute;inset:0.5in 0.6in;display:grid;grid-template-rows:1fr 1fr;gap:0.3in">{card(1)}{card(2)}</div>'
            f'<div class="foot" style="bottom:0.22in">{FOOT}</div></div>')


def review_page():
    qs = ["Best thing that happened in 2026", "Favourite memory with friends or family", "Something I learned", "Best book, film or show",
          "Song I played the most", "Proudest moment", "Something I'm letting go of", "Three words for my 2026"]
    boxes = "".join(f'<div style="border:1.5px solid {GOLD};border-radius:0.08in;padding:0.1in 0.14in;background:#fff">'
                    f'<div style="font:600 8.6pt Poppins;color:{NAVY}">{q}</div>{'<div class="ln" style="height:0.34in"></div>' * 4}</div>' for q in qs)
    return page("My 2026 in Review", "fill in before midnight", "Share one answer each around the table, or keep it for your journal.",
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.16in">{boxes}</div>', top="1.82in")


# ---------- countdown bags ----------
HOURS = [("6:00", "Make party hats", "Decorate hats or crowns with stickers and glitter for the big night."),
         ("7:00", "Game time", "Play a round of New Year's Eve Bingo. Winner picks the next song!"),
         ("8:00", "Dance party", "Five songs, no sitting down. Freeze when the music stops!"),
         ("9:00", "Snack attack", "Open your party snacks and make a toast with your favourite drink."),
         ("10:00", "Time capsule", "Fill in your 2027 Predictions and seal them in an envelope."),
         ("11:00", "Get loud", "Grab the noisemakers and confetti. Practise the countdown: 10, 9, 8…")]


def countdown_page():
    tags = "".join(f'<div class="cut" style="background:{NAVY};color:{CHAMP};padding:0.2in;position:relative;display:flex;flex-direction:column;align-items:center;text-align:center">'
                   f'<div style="width:0.18in;height:0.18in;border-radius:50%;background:{CHAMP};margin-bottom:0.08in;border:2px solid {GOLD}"></div>'
                   f'<div style="font:600 7.5pt Poppins;letter-spacing:.3em;color:{GOLD2}">OPEN AT</div>'
                   f'{svg("0 0 100 100", clock(50, 50, 42, hour=int(h.split(":")[0])), "width:0.85in;margin:0.06in 0")}'
                   f'<div style="font:700 22pt Poppins;color:{GOLD2};line-height:1">{h}<span style="font-size:11pt"> pm</span></div>'
                   f'<div class="script" style="font-size:20pt;line-height:1.05;margin-top:0.06in">{t}</div>'
                   f'<div style="font:8.4pt/1.35 Poppins;margin-top:0.06in;opacity:.9">{d}</div></div>' for h, t, d in HOURS)
    return page("Countdown to Midnight", "6 hourly party bags for kids &amp; families", "Cut out the tags, punch the hole and tie each one to a bag with a small treat or the supplies for that hour.",
                f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;grid-auto-rows:3.4in;gap:0">{tags}</div>', top="2.08in")


def score_page():
    rows = "".join(f'<tr>{"".join(f'<td style="height:0.42in;border:1px solid {GOLD}"></td>' for _ in range(7))}</tr>' for _ in range(15))
    heads = ["Player / team", "Bingo", "Trivia", "Scramble", "Most likely", "Bonus", "Total"]
    th = "".join(f'<th style="background:{NAVY};color:#fff;font:600 8.5pt Poppins;padding:0.08in;border:1px solid {GOLD}">{h}</th>' for h in heads)
    return page("Score Sheet", "keep track all night", "Bonus points for best party hat, best dance move or loudest countdown!",
                f'<table style="width:100%;border-collapse:collapse;background:#fff;table-layout:fixed"><colgroup><col style="width:30%">{"<col>" * 6}</colgroup><tr>{th}</tr>{rows}</table>', top="1.82in")


def keys_page():
    tk = "".join(f'<div style="font:9pt Poppins;padding:0.03in 0"><b style="color:{ROSE}">{i + 1}.</b> {"ABC"[a]}) {o[a]}</div>' for i, (_, o, a) in enumerate(TRIVIA))
    sk = "".join(f'<div style="font:9pt Poppins;padding:0.03in 0"><b style="color:{ROSE}">{i + 1}.</b> {w.title()}</div>' for i, w in enumerate(SCR))
    return page("Answer Keys", "for the host", None,
                f'<div style="display:grid;grid-template-columns:1.6fr 1fr;gap:0.4in"><div><div style="font:700 11pt Poppins;color:{NAVY};margin-bottom:0.08in">Traditions trivia</div>{tk}</div>'
                f'<div><div style="font:700 11pt Poppins;color:{NAVY};margin-bottom:0.08in">Word scramble</div>{sk}</div></div>', top="1.5in")


def build(out):
    pages = [cover(), bingo_caller(), *bingo_pages(), *trivia_pages(), *likely_pages(), *wyr_pages(), scramble_page(), predictions_page(),
             review_page(), countdown_page(), score_page(), keys_page()]
    for size in ("letter", "a4"):
        render(CSS, pages, size, f"{out}/{NAME}-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print(len(pages), "pages")


if __name__ == "__main__":
    build(sys.argv[1])
