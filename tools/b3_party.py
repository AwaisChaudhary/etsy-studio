"""Christmas Party Games Bundle printable (batch 3). 8 games, all artwork drawn here as SVG (shared motifs from kits2.py)."""
import random, sys
sys.path.insert(0, ".")
from render import render
from kits2 import pine, bauble, star, snowflake, holly, tree, mitten, gift, RED, GREEN, GOLD, CREAM, BERRY

INK = "#3a1d1d"
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Poppins, sans-serif; color: #3a1d1d; }
.page { width: var(--pw); height: var(--ph); position: relative; overflow: hidden; page-break-after: always; background: #fffdf8; }
.script { font-family: "TeX Gyre Chorus", Lora, serif; }
.serif { font-family: Lora, serif; }
.frame { position: absolute; inset: 0.32in; border: 2px solid #c9a24a; border-radius: 0.16in; }
.frame::after { content: ""; position: absolute; inset: 0.07in; border: 1px solid #c9a24a88; border-radius: 0.11in; }
.hd { position: absolute; left: 0.55in; right: 0.55in; top: 0.55in; text-align: center; }
.hd h1 { font-family: "TeX Gyre Chorus", Lora, serif; font-weight: normal; font-size: 46pt; line-height: 1; color: #8c2430; }
.hd .k { font: 600 9pt Poppins; letter-spacing: .22em; text-transform: uppercase; color: #1f5d45; margin-top: 0.06in; }
.hd p { font: 9.5pt/1.45 Poppins; margin: 0.08in auto 0; max-width: 6.4in; color: #5a3a3a; }
.body { position: absolute; left: 0.62in; right: 0.62in; top: 2.05in; bottom: 0.62in; }
.foot { position: absolute; bottom: 0.4in; left: 0; right: 0; text-align: center; font: 7pt Poppins; color: #a08f80; }
.cut { outline: 1px dashed rgba(0,0,0,.28); outline-offset: -1px; }
.line { border-bottom: 1px solid #3a1d1d66; height: 0.3in; }
svg { display: block; }
.q { font: 10pt/1.35 Poppins; }
.q b { color: #8c2430; }
.opt { font: 9.5pt Poppins; color: #5a3a3a; }
"""


def deco(w=7.0, kind=0):
    """A small row of motifs used under page titles."""
    sets = [[bauble(60, 70, 34, RED, GOLD), star(170, 66, 30, GOLD), holly(250, 70, 1.1, GREEN, BERRY), star(350, 66, 30, GOLD), bauble(460, 70, 34, GREEN, GOLD)],
            [snowflake(70, 66, 38, "#4c7a99"), tree(200, 118, 90, GREEN), gift(330, 72, 1.0, RED, GOLD), tree(460, 118, 90, GREEN), snowflake(590, 66, 38, "#4c7a99")]]
    return sets[kind % 2]


def head(title, kicker, intro, kind=0):
    art = "".join(deco(kind=kind))
    return (f'<div class="frame"></div><div class="hd"><h1>{title}</h1><div class="k">{kicker}</div>'
            + (f'<p>{intro}</p>' if intro else "") + '</div>')


def page(title, kicker, intro, body, foot="Purl &amp; Paper · Christmas Party Games", kind=0, top=None):
    st = f' style="top:{top}"' if top else ""
    return f'<div class="page">{head(title, kicker, intro, kind)}<div class="body"{st}>{body}</div><div class="foot">{foot}</div></div>'


# ---------- cover ----------
def cover():
    art = (bauble(130, 150, 62, RED, GOLD) + star(300, 110, 46, GOLD) + holly(420, 150, 1.7, GREEN, BERRY) + tree(620, 250, 170, GREEN)
           + gift(810, 170, 1.6, RED, GOLD) + snowflake(960, 140, 58, "#4c7a99"))
    games = ["Christmas Bingo (30 cards)", "Christmas Trivia (30 questions)", "Would You Rather (24 cards)", "Who's Most Likely To (24 cards)",
             "Word Scramble", "This or That", "Indoor Scavenger Hunt", "Gift Swap Dice Game"]
    li = "".join(f'<div style="display:flex;gap:0.12in;align-items:center;font:11pt Poppins;padding:0.06in 0;border-bottom:1px dotted #c9a24a"><svg viewBox="0 0 100 100" style="width:0.22in">{star(50, 52, 44, RED if i % 2 else GREEN)}</svg>{g}</div>' for i, g in enumerate(games))
    return (f'<div class="page" style="background:#fbf3e6"><div class="frame"></div>'
            f'<svg viewBox="0 0 1100 290" style="position:absolute;left:0.8in;top:0.85in;width:calc(100% - 1.6in)">{art}</svg>'
            f'<div style="position:absolute;left:0;right:0;top:3.7in;text-align:center">'
            f'<div class="script" style="font-size:64pt;line-height:.95;color:#8c2430">Christmas<br>Party Games</div>'
            f'<div style="font:600 10.5pt Poppins;letter-spacing:.24em;text-transform:uppercase;color:#1f5d45;margin-top:0.16in">8 printable games · kids, families &amp; adults</div></div>'
            f'<div style="position:absolute;left:1.6in;right:1.6in;top:6.55in">{li}</div>'
            f'<div style="position:absolute;left:1in;right:1in;bottom:0.75in;text-align:center;font:9pt/1.5 Poppins;color:#5a3a3a">Print at 100% (actual size) on paper or cardstock. Print as many copies as your party needs.<br>Answer keys are at the back.</div></div>')


# ---------- bingo ----------
WORDS = ["Snowman", "Reindeer", "Candy Cane", "Stocking", "Mistletoe", "Sleigh", "Gingerbread", "Ornament", "Wreath", "Elf",
         "Snowflake", "Hot Cocoa", "Mittens", "Presents", "Star", "Bells", "Holly", "Fireplace", "Carols", "Cookies",
         "Tinsel", "North Pole", "Scarf", "Pine Cone", "Lights", "Angel", "Snow Globe", "Ribbon", "Candle", "Penguin",
         "Polar Bear", "Igloo", "Sweater", "Nutcracker", "Eggnog", "Chimney", "Sledding", "Icicle", "Bow", "Toy Train"]
ICON = {"Star": lambda: star(50, 52, 40, GOLD), "Snowflake": lambda: snowflake(50, 50, 40, "#4c7a99"), "Ornament": lambda: bauble(50, 60, 28, RED, GOLD),
        "Presents": lambda: gift(50, 52, .9, RED, GOLD), "Holly": lambda: holly(36, 54, .95, GREEN, BERRY), "Mittens": lambda: mitten(50, 46, .95, RED, "#f3e6d6")}


def bingo_card(n, words):
    hdr = "".join(f'<div style="background:{[RED, GREEN][i % 2]};color:#fff;font:700 22pt Poppins;display:flex;align-items:center;justify-content:center;border-radius:0.06in">{c}</div>' for i, c in enumerate("BINGO"))
    cells = ""
    for k, w in enumerate(words):
        if k == 12:
            cells += (f'<div style="background:#fbf3e6;border:1.5px solid #c9a24a;border-radius:0.06in;display:flex;flex-direction:column;align-items:center;justify-content:center">'
                      f'<svg viewBox="0 0 100 100" style="width:0.42in">{star(50, 52, 44, GOLD)}</svg><div style="font:700 8pt Poppins;color:#8c2430;letter-spacing:.1em">FREE</div></div>')
        else:
            ic = ICON.get(w)
            art = f'<svg viewBox="0 0 100 100" style="width:0.3in;margin-bottom:0.02in">{ic()}</svg>' if ic else ""
            cells += (f'<div style="border:1.5px solid #3a1d1d33;border-radius:0.06in;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;'
                      f'font:600 9.5pt/1.1 Poppins;padding:0 0.04in">{art}{w}</div>')
    return (f'<div style="display:flex;flex-direction:column;height:100%"><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.06in">'
            f'<div class="script" style="font-size:24pt;color:#8c2430;line-height:1">Christmas Bingo</div><div style="font:600 8pt Poppins;color:#a08f80">CARD {n:02d}</div></div>'
            f'<div style="display:grid;grid-template-columns:repeat(5,1fr);grid-template-rows:0.48in repeat(5,1fr);gap:0.05in;flex:1">{hdr}{cells}</div></div>')


def bingo_pages():
    rnd = random.Random(2026); seen = set(); cards = []
    while len(cards) < 30:
        ws = rnd.sample(WORDS, 24)
        key = frozenset(ws)
        if key in seen: continue
        seen.add(key); ws.insert(12, "FREE"); cards.append(ws)
    out = []
    for i in range(0, 30, 2):
        out.append(f'<div class="page"><div class="frame"></div><div style="position:absolute;left:0.65in;right:0.65in;top:0.6in;bottom:0.6in;display:grid;grid-template-rows:1fr 1fr;gap:0.45in">'
                   f'<div>{bingo_card(i + 1, cards[i])}</div><div>{bingo_card(i + 2, cards[i + 1])}</div></div>'
                   f'<div style="position:absolute;left:0.6in;right:0.6in;top:50%;border-top:1px dashed #0004"></div><div class="foot">Cut along the dashed line · 30 different cards</div></div>')
    return out


def bingo_rules_and_caller():
    rules = ("Give every player a card and a pencil (or use sweets, buttons or mini marshmallows as markers). The caller cuts out the 40 calling cards below, "
             "shuffles them in a bowl and reads them out one at a time. Players mark the word if it is on their card. The centre star is free. "
             "The first player to complete a row (across, down or diagonal) shouts \"BINGO!\" and wins. For a longer game, play for four corners or a full card.")
    cells = "".join(f'<div class="cut" style="display:flex;align-items:center;justify-content:center;text-align:center;font:600 9pt Poppins;background:{["#fbf3e6", "#eef3ee"][i % 2]}">{w}</div>' for i, w in enumerate(WORDS))
    body = f'<div style="display:grid;grid-template-columns:repeat(5,1fr);grid-template-rows:repeat(8,1fr);height:100%;gap:0">{cells}</div>'
    return page("Christmas Bingo", "How to play · calling cards", rules, body, top="2.45in")


# ---------- trivia ----------
TRIVIA = [
 ("In which country did the tradition of decorating Christmas trees begin?", ["Germany", "France", "Canada"], 0),
 ("The red \"petals\" of a poinsettia are actually...", ["Berries", "Leaves (bracts)", "Seeds"], 1),
 ("How many gifts are given in total in the song \"The Twelve Days of Christmas\"?", ["78", "144", "364"], 2),
 ("What bird is given on the first day in \"The Twelve Days of Christmas\"?", ["A partridge", "A swan", "A goose"], 0),
 ("In what year was the first commercial Christmas card sent in England?", ["1743", "1843", "1943"], 1),
 ("What is traditionally hidden inside a British Christmas pudding for luck?", ["A ring", "A bean", "A coin"], 2),
 ("What colour are mistletoe berries?", ["Red", "White", "Purple"], 1),
 ("\"Feliz Navidad\" means Merry Christmas in which language?", ["Spanish", "Italian", "Portuguese"], 0),
 ("Which country sends a giant Christmas tree to London's Trafalgar Square every year?", ["Sweden", "Norway", "Finland"], 1),
 ("What is the name of the four-week season before Christmas?", ["Lent", "Epiphany", "Advent"], 2),
 ("Saint Nicholas was born in what is now which country?", ["Turkey", "Greece", "Italy"], 0),
 ("Who wrote \"A Christmas Carol\" (1843)?", ["Jane Austen", "Charles Dickens", "Mark Twain"], 1),
 ("What does Ebenezer Scrooge famously say about Christmas?", ["\"Fiddlesticks!\"", "\"Poppycock!\"", "\"Bah! Humbug!\""], 2),
 ("In the 1823 poem \"A Visit from St. Nicholas\", how many reindeer pull the sleigh?", ["Six", "Eight", "Ten"], 1),
 ("Which song was the first ever played in space, in December 1965?", ["Jingle Bells", "Silent Night", "Deck the Halls"], 0),
 ("How many points does a snowflake usually have?", ["Four", "Five", "Six"], 2),
 ("Frankincense, one of the gifts of the Wise Men, is...", ["A tree resin", "A spice", "A type of gold"], 0),
 ("Which creamy drink made with milk, sugar and eggs is a Christmas favourite?", ["Mulled wine", "Eggnog", "Cider"], 1),
 ("In Iceland, how many mischievous \"Yule Lads\" visit children before Christmas?", ["3", "7", "13"], 2),
 ("What season is it in Australia at Christmas time?", ["Summer", "Winter", "Autumn"], 0),
 ("In Italy, which kind old woman brings gifts to children on 5-6 January?", ["La Nonna", "La Befana", "La Strega"], 1),
 ("Christmas Island is in which ocean?", ["Pacific", "Atlantic", "Indian"], 2),
 ("What is the day after Christmas called in the UK, Canada and Australia?", ["Boxing Day", "Gift Day", "Ribbon Day"], 0),
 ("Which popular Christmas dinner became a tradition in Japan in the 1970s?", ["Roast turkey", "Fried chicken", "Grilled fish"], 1),
 ("A traditional Yule log was originally...", ["A sweet cake", "A wooden sled", "A large log burned in the fireplace"], 2),
 ("Gingerbread houses became popular in Germany after which fairy tale?", ["Hansel and Gretel", "Snow White", "Cinderella"], 0),
 ("What are the traditional colours of a candy cane?", ["Green and white", "Red and white", "Red and green"], 1),
 ("Which Christmas plant is traditionally hung so people can kiss beneath it?", ["Ivy", "Holly", "Mistletoe"], 2),
 ("Where does Santa Claus traditionally live?", ["The North Pole", "Greenland", "The South Pole"], 0),
 ("The name \"Santa Claus\" comes from the Dutch name...", ["Sankt Klaus", "Sinterklaas", "Saint Nick"], 1),
]


def trivia_pages():
    out = []
    for part in range(2):
        qs = ""
        for i in range(15):
            n = part * 15 + i; q, opts, _ = TRIVIA[n]
            o = "".join(f'<span style="margin-right:0.28in">{"ABC"[j]}) {x}</span>' for j, x in enumerate(opts))
            qs += f'<div style="padding:0.07in 0;border-bottom:1px dotted #c9a24a"><div class="q"><b>{n + 1}.</b> {q}</div><div class="opt" style="margin:0.03in 0 0 0.24in">{o}</div></div>'
        intro = "Circle one answer for each question. One point per correct answer. Answers are at the back." if part == 0 else ""
        out.append(page("Christmas Trivia", f"Part {part + 1} of 2 · questions {part * 15 + 1} to {part * 15 + 15}", intro, qs, kind=part,
                        top="2.05in" if part == 0 else "1.75in"))
    return out


# ---------- card games ----------
WYR = ["Would you rather build a snowman or have a snowball fight?", "Would you rather wear an ugly Christmas sweater all day or reindeer antlers all day?",
       "Would you rather only eat Christmas cookies or only eat candy canes for a week?", "Would you rather be one of Santa's elves or one of his reindeer?",
       "Would you rather open one present a day in December or all of them on Christmas morning?", "Would you rather live in a snow globe or a gingerbread house?",
       "Would you rather sing a carol solo or dance in front of everyone?", "Would you rather have Christmas on a beach or in a snowy cabin?",
       "Would you rather wrap every present in the house or untangle every string of lights?", "Would you rather drink hot cocoa or eggnog forever?",
       "Would you rather get socks every Christmas or a surprise you might not like?", "Would you rather ride a sleigh or go ice skating?",
       "Would you rather have a talking snowman or a flying reindeer as a pet?", "Would you rather decorate the tree or bake the cookies?",
       "Would you rather never see snow again or never have Christmas dinner again?", "Would you rather give the gifts or receive the gifts?",
       "Would you rather have a white Christmas or a sunny Christmas?", "Would you rather wear mittens on your feet or socks on your hands?",
       "Would you rather watch a Christmas film every night or hear carols all day?", "Would you rather be the star on top of the tree or a present under it?",
       "Would you rather have a chocolate advent calendar or a toy advent calendar?", "Would you rather sleep in an igloo or a treehouse in the snow?",
       "Would you rather lose your voice on Christmas Day or lose your appetite?", "Would you rather go sledding at night or build a giant snow fort?"]
MLT = ["...peek at their presents early?", "...fall asleep before midnight on New Year's Eve?", "...eat the most cookies?", "...wear the ugliest Christmas sweater?",
       "...start playing carols in November?", "...wrap a gift in newspaper?", "...lose the TV remote under the wrapping paper?", "...cry at a Christmas film?",
       "...re-gift a present?", "...buy gifts on Christmas Eve?", "...get tangled in the Christmas lights?", "...win this game?",
       "...sing the loudest?", "...burn the Christmas dinner?", "...still believe in Santa?", "...put the tree up first?",
       "...take a nap after dinner?", "...forget someone's gift?", "...build the biggest snowman?", "...shake every present to guess what's inside?",
       "...hide the last chocolate?", "...wear pyjamas all day?", "...get the most presents?", "...make a New Year's resolution and keep it?"]


def cards_page(title, kicker, items, pal, prefix=""):
    cells = ""
    for i, t in enumerate(items):
        bg, ac = pal[i % len(pal)]
        art = [star(50, 52, 34, GOLD), snowflake(50, 50, 34, ac), holly(36, 54, .8, GREEN, BERRY), bauble(50, 60, 24, ac, GOLD)][i % 4]
        cells += (f'<div class="cut" style="background:{bg};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0.12in 0.18in;position:relative">'
                  f'<svg viewBox="0 0 100 100" style="width:0.36in;margin-bottom:0.06in">{art}</svg>'
                  + (f'<div style="font:700 7.5pt Poppins;letter-spacing:.16em;color:{ac};margin-bottom:0.04in">{prefix}</div>' if prefix else "")
                  + f'<div style="font:500 10pt/1.35 Poppins">{t}</div></div>')
    return (f'<div class="page"><div class="frame"></div><div style="position:absolute;left:0;right:0;top:0.5in;text-align:center"><div class="script" style="font-size:34pt;color:#8c2430;line-height:1">{title}</div>'
            f'<div style="font:600 8pt Poppins;letter-spacing:.2em;color:#1f5d45;text-transform:uppercase">{kicker}</div></div>'
            f'<div style="position:absolute;left:0.6in;right:0.6in;top:1.45in;bottom:0.65in;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(4,1fr)">{cells}</div>'
            f'<div class="foot">Cut along the dashed lines · shuffle and take turns</div></div>')


# ---------- word scramble / this or that / hunt / dice ----------
SCR = ["REINDEER", "SNOWMAN", "MISTLETOE", "STOCKING", "GINGERBREAD", "ORNAMENT", "SLEIGH", "TINSEL", "WREATH", "CANDLE",
       "PRESENTS", "CHIMNEY", "SNOWFLAKE", "MITTENS", "CAROLS", "COOKIES", "ICICLE", "NUTCRACKER", "POINSETTIA", "FIREPLACE"]


def scramble(w, seed):
    r = random.Random(seed); s = list(w)
    while "".join(s) == w: r.shuffle(s)
    return "".join(s)


def scramble_page():
    rows = "".join(f'<div style="display:flex;align-items:flex-end;gap:0.15in;padding:0.055in 0"><b style="font:700 10pt Poppins;color:#8c2430;width:0.3in">{i + 1}.</b>'
                   f'<span style="font:600 13pt Lora;letter-spacing:.18em;width:2.4in">{scramble(w, i)}</span><span class="line" style="flex:1"></span></div>' for i, w in enumerate(SCR))
    return page("Word Scramble", "Unscramble the Christmas words", "Fastest player to unscramble all 20 words wins. Set a timer for 5 minutes for an extra challenge.",
                f'<div style="columns:1">{rows}</div>', kind=1)


TOT = [("Hot cocoa", "Eggnog"), ("Snowman", "Snow angel"), ("Real tree", "Artificial tree"), ("Gingerbread", "Sugar cookies"), ("Wrapping paper", "Gift bags"),
       ("Sledding", "Ice skating"), ("White lights", "Coloured lights"), ("Christmas Eve", "Christmas Day"), ("Stockings", "Advent calendar"), ("Carols", "Christmas films"),
       ("Pyjamas", "Christmas sweater"), ("Elf", "Reindeer"), ("Candy cane", "Chocolate coins"), ("Fireplace", "Snowy window"), ("Giving", "Receiving"),
       ("Mittens", "Gloves"), ("Turkey", "Ham"), ("Tinsel", "Garland"), ("Snow day", "Sunny day"), ("Early riser", "Sleep in")]


def tot_page():
    rows = ""
    for i, (a, b) in enumerate(TOT):
        rows += (f'<div style="display:grid;grid-template-columns:1fr 0.5in 1fr;align-items:center;padding:0.06in 0;border-bottom:1px dotted #c9a24a">'
                 f'<span style="text-align:right;font:500 11pt Poppins">{a} &nbsp;○</span><span class="script" style="text-align:center;font-size:16pt;color:#1f5d45">or</span>'
                 f'<span style="font:500 11pt Poppins">○&nbsp; {b}</span></div>')
    return page("This or That", "Christmas edition", "Fill in the circle for your pick, then compare with everyone else. Score a point each time you match the host!", rows)


HUNT = ["Something red", "A candy cane", "Something that sparkles", "A bow or ribbon", "Something that jingles", "A pine cone", "Something soft and fuzzy",
        "A Christmas card", "A star", "Something green", "A sock", "Something that smells nice", "A snowflake (paper counts!)", "A spoon for hot cocoa",
        "Something gold", "A present", "A book with a winter picture", "Something round like a bauble", "A pair of mittens or gloves", "Something with Santa on it"]


def hunt_page():
    cells = "".join(f'<div style="display:flex;align-items:center;gap:0.12in;padding:0.08in 0.1in;border:1.5px solid #3a1d1d22;border-radius:0.08in;background:{["#fffdf8", "#fbf3e6"][i % 2]}">'
                    f'<span style="width:0.24in;height:0.24in;border:2px solid {[RED, GREEN][i % 2]};border-radius:0.05in;flex:none"></span><span style="font:500 10.5pt Poppins">{h}</span></div>' for i, h in enumerate(HUNT))
    return page("Scavenger Hunt", "Indoor Christmas hunt", "Find each thing around the house and tick it off. First to find all 20 (or the most in 10 minutes) wins. Grown-ups: hide a few extras to make it fun!",
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.1in 0.18in">{cells}</div>', kind=1)


def die(n, col):
    pos = {1: [(50, 50)], 2: [(28, 28), (72, 72)], 3: [(26, 26), (50, 50), (74, 74)], 4: [(28, 28), (72, 28), (28, 72), (72, 72)],
           5: [(26, 26), (74, 26), (50, 50), (26, 74), (74, 74)], 6: [(28, 24), (72, 24), (28, 50), (72, 50), (28, 76), (72, 76)]}[n]
    return f'<rect x="6" y="6" width="88" height="88" rx="16" fill="{col}"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="#fff"/>' for x, y in pos)


def dice_page():
    acts = [("Swap left", "Swap your gift with the person on your left."), ("Swap right", "Swap your gift with the person on your right."),
            ("Steal!", "Take any gift you like and give them yours."), ("Keep it", "Hold on tight: you keep your gift this round."),
            ("Unwrap", "Open your gift now. It can still be stolen!"), ("Everyone pass", "Everyone passes their gift one place to the left.")]
    rows = "".join(f'<div style="display:flex;align-items:center;gap:0.22in;padding:0.1in 0.15in;border-radius:0.1in;background:{["#fbf3e6", "#eef3ee"][i % 2]}">'
                   f'<svg viewBox="0 0 100 100" style="width:0.62in;flex:none">{die(i + 1, [RED, GREEN][i % 2])}</svg>'
                   f'<div><div style="font:700 13pt Poppins;color:{[RED, GREEN][i % 2]}">{a}</div><div style="font:10.5pt Poppins">{b}</div></div></div>' for i, (a, b) in enumerate(acts))
    how = ('<div style="margin-top:0.2in;font:9.5pt/1.5 Poppins;color:#5a3a3a"><b style="color:#8c2430">How to play:</b> everyone brings one wrapped gift (agree a budget first) and sits in a circle. '
           'Take turns rolling one die and do what it says. Set a timer for 10 to 15 minutes; when it rings, the game stops and everyone keeps the gift in their hands.</div>')
    return page("Gift Swap Dice Game", "A white elephant game for any group", "", f'<div style="display:grid;gap:0.12in">{rows}</div>{how}', top="1.75in")


def score_page():
    rows = "".join(f'<tr><td style="height:0.36in;border-bottom:1px solid #3a1d1d33"></td>' + "".join('<td style="border-bottom:1px solid #3a1d1d33;border-left:1px solid #3a1d1d22"></td>' for _ in range(6)) + "</tr>" for _ in range(14))
    games = ["Bingo", "Trivia", "Scramble", "This or That", "Hunt", "Total"]
    th = "".join(f'<th style="font:600 8.5pt Poppins;color:#fff;background:{[RED, GREEN][i % 2]};padding:0.06in 0">{g}</th>' for i, g in enumerate(games))
    tbl = f'<table style="width:100%;border-collapse:collapse"><tr><th style="font:600 8.5pt Poppins;color:#fff;background:#3a1d1d;width:30%">Player</th>{th}</tr>{rows}</table>'
    return page("Score Sheet", "Keep track of the winners", "", tbl, top="1.75in", kind=1)


def awards_page():
    aw = ["Trivia Champion", "Bingo Winner", "Best Christmas Sweater", "Scavenger Hunt Hero", "Word Scramble Whiz", "Holiday Spirit Award"]
    cells = "".join(f'<div class="cut" style="background:#fbf3e6;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0.15in;box-shadow:inset 0 0 0 0.08in #fbf3e6, inset 0 0 0 0.1in {GOLD}">'
                    f'<svg viewBox="0 0 100 100" style="width:0.6in">{star(50, 52, 46, GOLD)}</svg><div style="font:600 7.5pt Poppins;letter-spacing:.18em;color:#1f5d45;margin-top:0.06in">THIS AWARD GOES TO</div>'
                    f'<div style="width:80%;border-bottom:1px solid #3a1d1d66;height:0.38in"></div><div class="script" style="font-size:22pt;color:#8c2430;margin-top:0.08in;line-height:1">{a}</div></div>' for a in aw)
    return (f'<div class="page"><div class="frame"></div><div style="position:absolute;left:0;right:0;top:0.5in;text-align:center"><div class="script" style="font-size:34pt;color:#8c2430;line-height:1">Prize Awards</div></div>'
            f'<div style="position:absolute;left:0.6in;right:0.6in;top:1.3in;bottom:0.65in;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr)">{cells}</div><div class="foot">Cut along the dashed lines</div></div>')


def keys_page():
    tk = "".join(f'<div style="font:10pt Poppins;padding:0.035in 0"><b style="color:#8c2430">{i + 1}.</b> {"ABC"[a]}) {o[a]}</div>' for i, (_, o, a) in enumerate(TRIVIA))
    sk = "".join(f'<div style="font:10pt Poppins;padding:0.035in 0"><b style="color:#1f5d45">{i + 1}.</b> {w.title()}</div>' for i, w in enumerate(SCR))
    body = (f'<div style="display:grid;grid-template-columns:1.7fr 1fr;gap:0.35in"><div><div style="font:700 11pt Poppins;color:#8c2430;margin-bottom:0.08in">Christmas Trivia</div>'
            f'<div style="columns:2;column-gap:0.25in">{tk}</div></div><div><div style="font:700 11pt Poppins;color:#1f5d45;margin-bottom:0.08in">Word Scramble</div>{sk}</div></div>')
    return page("Answer Keys", "For the host only", "", body, top="1.75in")


def build():
    return CSS, ([cover(), bingo_rules_and_caller()] + bingo_pages() + trivia_pages()
                 + [cards_page("Would You Rather", "Christmas edition · 24 cards", WYR[:12], [("#fbf3e6", RED), ("#eef3ee", GREEN)]),
                    cards_page("Would You Rather", "Christmas edition · 24 cards", WYR[12:], [("#eef3ee", GREEN), ("#fbf3e6", RED)]),
                    cards_page("Who's Most Likely To", "Point at your answer on the count of three", MLT[:12], [("#fbf3e6", RED), ("#eaf1f6", "#4c7a99")], "WHO'S MOST LIKELY TO"),
                    cards_page("Who's Most Likely To", "Point at your answer on the count of three", MLT[12:], [("#eaf1f6", "#4c7a99"), ("#fbf3e6", RED)], "WHO'S MOST LIKELY TO"),
                    scramble_page(), tot_page(), hunt_page(), dice_page(), score_page(), awards_page(), keys_page()])


if __name__ == "__main__":
    out = sys.argv[1]; name = "christmas-party-games-bundle"
    css, pages = build()
    for size in ("letter", "a4"):
        render(css, pages, size, f"{out}/{name}-{'US-Letter' if size == 'letter' else 'A4'}.pdf")
    print(name, len(pages), "pages")
