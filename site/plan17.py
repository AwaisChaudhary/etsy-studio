# ---------------- 28 Nov 2026 run 17: CROCHET CHRISTMAS ORNAMENT (BAUBLE) + CROCHET SNOWFLAKE + HOW TO CROCHET A BLANKET ----------------
# Executed from build.py after plan16.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 28 Nov run 17). Patterns, drawings and wording our own. JS in assets/app.js (cxo-*, csf-*, cbk-*).
import math as _m17


# ======== FREE CROCHET CHRISTMAS ORNAMENT (BAUBLE) ========
# Demand: Q4 'crochet christmas ornaments free pattern easy' + 'easy crochet christmas bauble ornament pattern free beginner'
# (SERP 28 Nov: Ravelry x12 bauble listings, Ribblr, Juniper & Oakes granny bauble, Make and Do Crew, EasyCrochet 37 ornaments).
# Method: standard amigurumi sphere (6 sts per increase round, as many even rounds as increase rounds, then decrease back).

def _bauble(cx, cy, r, body="#b8326a", band="#fbfcfa", cap=None):
    cap = cap or _GOLD
    s = (f'<line x1="{cx}" y1="{cy - r - 30}" x2="{cx}" y2="{cy - r - 6}" stroke="{_INK}" stroke-width="1.5"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{body}" stroke="{_INK}" stroke-width="2"/>'
         f'<path d="M{cx - r * 0.98} {cy - r * 0.18} Q{cx} {cy - r * 0.05} {cx + r * 0.98} {cy - r * 0.18} L{cx + r * 0.98} {cy + r * 0.18} Q{cx} {cy + r * 0.31} {cx - r * 0.98} {cy + r * 0.18} Z" fill="{band}" stroke="{_INK}" stroke-width="1.2"/>'
         + "".join(f'<path d="M{cx - r + i * r / 4} {cy - r * 0.02} l4 6 l4 -6" fill="none" stroke="{body}" stroke-width="1.6"/>' for i in range(1, 7))
         + f'<rect x="{cx - r * 0.32}" y="{cy - r - 8}" width="{r * 0.64}" height="12" rx="3" fill="{cap}" stroke="{_INK}" stroke-width="1.6"/>'
         f'<path d="M{cx - 6} {cy - r - 8} q6 -16 12 0" fill="none" stroke="{_INK}" stroke-width="1.6"/>'
         f'<ellipse cx="{cx - r * 0.42}" cy="{cy - r * 0.45}" rx="{r * 0.14}" ry="{r * 0.22}" fill="#fff" opacity=".35"/>')
    return s


def _cxo_svg(step, label):
    if step == 1:
        s = (f'<circle cx="140" cy="92" r="16" fill="none" stroke="{_BERRY}" stroke-width="4"/>' + "".join(
            f'<circle cx="{140 + 26 * _m17.cos(a * _m17.pi / 3)}" cy="{92 + 26 * _m17.sin(a * _m17.pi / 3)}" r="6" fill="{_BERRY}" stroke="{_INK}" stroke-width="1.2"/>' for a in range(6))
             + f'<text x="140" y="180" {_T12} text-anchor="middle">6 sc in a magic ring</text>')
    elif step == 2:
        s = "".join(f'<circle cx="140" cy="92" r="{r}" fill="none" stroke="{c}" stroke-width="8"/>' for r, c in ((12, _BERRY), (24, "#d4577f"), (36, _BERRY), (48, "#d4577f"), (60, _BERRY))) + f'<text x="140" y="184" {_T12} text-anchor="middle">add 6 stitches every round</text>'
    elif step == 3:
        s = (f'<path d="M80 130 L80 70 Q80 40 140 40 Q200 40 200 70 L200 130 Z" fill="{_BERRY}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<line x1="80" y1="{y}" x2="200" y2="{y}" stroke="#fbfcfa" stroke-width="1.5" opacity=".5"/>' for y in range(72, 130, 11))
             + f'<rect x="80" y="92" width="120" height="16" fill="#fbfcfa" stroke="{_INK}" stroke-width="1.2"/><text x="140" y="178" {_T12} text-anchor="middle">plain rounds (change colour for a band)</text>')
    elif step == 4:
        s = (f'<path d="M86 70 Q86 150 140 150 Q194 150 194 70 Z" fill="{_BERRY}" stroke="{_INK}" stroke-width="2"/><ellipse cx="140" cy="70" rx="54" ry="12" fill="#f7efe2" stroke="{_INK}" stroke-width="1.6"/>'
             + "".join(f'<circle cx="{120 + i * 12}" cy="{66 + (i % 2) * 6}" r="7" fill="#fff" stroke="#c9c2b4" stroke-width="1"/>' for i in range(4))
             + f'<text x="140" y="184" {_T12} text-anchor="middle">decrease, stuffing as you go</text>')
    elif step == 5:
        s = (f'<rect x="108" y="56" width="64" height="34" rx="6" fill="{_GOLD}" stroke="{_INK}" stroke-width="2"/>' + "".join(
            f'<line x1="{x}" y1="60" x2="{x}" y2="86" stroke="{_INK}" stroke-width="1" opacity=".35"/>' for x in range(116, 170, 8))
             + f'<path d="M126 56 q14 -34 28 0" fill="none" stroke="{_GOLD}" stroke-width="5"/><path d="M126 56 q14 -34 28 0" fill="none" stroke="{_INK}" stroke-width="1" opacity=".5"/>'
             + f'<text x="140" y="130" {_T12} text-anchor="middle">a small gold cap</text><text x="140" y="148" {_T12} text-anchor="middle">and a chain loop</text>')
    else:
        s = _bauble(140, 110, 52) + f'<text x="140" y="190" {_T12} text-anchor="middle">sew on the cap: ready for the tree</text>'
    return _svg12(s, label)


CXO_STEPS = [(1, "1. Start with a ring", "Make a magic ring and work 6 single crochet into it. Pull the tail to close the hole. Work in a spiral and move a stitch marker up each round."),
             (2, "2. Increase", "Add 6 stitches every round until you reach the widest point (24, 30 or 36 stitches, depending on the size you pick)."),
             (3, "3. Work even", "Crochet one stitch in every stitch for as many rounds as you increased. Switch colour for a few rounds to make a stripe or band."),
             (4, "4. Decrease and stuff", "Decrease 6 stitches every round. Stuff firmly when the opening is about the size of a coin so the ball stays round."),
             (5, "5. Make the cap", "In gold or silver, make a tiny cup (12 stitches) and a chain loop for hanging."),
             (6, "6. Finish", "Close the ball, sew the cap on top, thread the loop through and tie. Add sparkle with a few cross stitches of white yarn.")]
cxo_cards = "".join(f'<figure class="gq-fig"><div>{_cxo_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CXO_STEPS)

cxo = top("Free crochet Christmas ornament pattern (easy bauble)", "A round crochet bauble is the easiest Christmas ornament you can make: it's one stuffed ball in single crochet with a little gold cap and a hanging loop. Pick a size and a stripe style below and the pattern rewrites itself, round by round, with tick boxes so you never lose your place.", "Crochet Christmas ornament pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet an easy Christmas bauble, work <strong>6 sc in a magic ring</strong>, <strong>increase by 6 stitches every round</strong> to 30 (5 rounds), work <strong>5 plain rounds</strong> (switch colour in the middle for a band), then <strong>decrease by 6 every round</strong> back to 6, stuffing as you go. Add a <strong>12-stitch gold cap</strong> and a <strong>20-chain loop</strong>. In worsted yarn with a 3.5 mm hook it's about 2 in (5 cm) across and uses about 15 yd of yarn (our estimate). Most people finish one in 45 to 60 minutes.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Bauble pattern writer</h3>
<div class="row2"><div class="field"><label for="cxo-k">Size</label><select id="cxo-k"><option value="4">Small (24 stitches round the middle)</option><option value="5" selected>Medium (30 stitches)</option><option value="6">Large (36 stitches)</option><option value="7">Extra large (42 stitches)</option></select></div>
<div class="field"><label for="cxo-y">Yarn</label><select id="cxo-y"><option value="dk">DK / light (3), 3 mm hook</option><option value="w" selected>Worsted / aran (4), 3.5 mm hook</option><option value="ch">Chunky (5), 5 mm hook</option></select></div></div>
<div class="row2"><div class="field"><label for="cxo-s">Colours</label><select id="cxo-s"><option value="plain">One colour</option><option value="band" selected>Wide band round the middle</option><option value="stripes">Two thin stripes</option><option value="half">Two-tone (top and bottom)</option></select></div>
<div class="field"><label for="cxo-n">How many baubles</label><input type="number" id="cxo-n" value="6" min="1" max="60" inputmode="numeric"></div></div>
<div class="field"><span class="label" id="cxo-t-l">Terms</span><div class="seg" role="group" aria-labelledby="cxo-t-l" id="cxo-t"><button type="button" data-v="us" aria-pressed="true">US</button><button type="button" data-v="uk" aria-pressed="false">UK</button></div></div>
</div><div class="result" aria-live="polite" id="cxo-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<div class="gq-figs"><figure class="gq-fig"><div>{_svg12(_bauble(80, 110, 44) + _bauble(200, 116, 38, body=_TEAL, band=_GOLD, cap="#c9ced6"), "Two finished crochet baubles: berry with a white band, teal with a gold band")}<figcaption><strong>The finished baubles.</strong> Our own drawing: one with a wide band, one with a gold stripe and a silver cap.</figcaption></div></figure></div>
<h2>How to crochet a Christmas bauble, step by step</h2>
<div class="gq-figs">{cxo_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> a smooth acrylic or cotton in Christmas colours, plus a scrap of gold or silver (a metallic yarn or embroidery thread held together with yarn looks lovely). One ball makes lots: a medium bauble takes about 15 yards.</li>
<li><strong>Hook:</strong> about two sizes smaller than the yarn label suggests, so the stitches are tight and the stuffing doesn't show (3.5 mm for worsted).</li>
<li><strong>Also:</strong> a stitch marker, a little polyester toy stuffing, a tapestry needle and scissors. Ribbon or baker's twine works instead of a chain loop.</li></ul>
<h2>Abbreviations</h2>
<p><strong>sc</strong> single crochet (UK double crochet, dc), <strong>inc</strong> 2 sc in the same stitch, <strong>dec</strong> sc 2 together (the invisible decrease through the front loops looks neatest), <strong>BLO</strong> back loop only, <strong>sl st</strong> slip stitch. The number in brackets is the stitch count at the end of the round. Switch the writer to UK terms and every stitch name changes for you. Colours are called <strong>A</strong> (main) and <strong>B</strong> (contrast); change colour on the last pull-through of the round before, as in our guide to <a href="{href("how-to-change-colors-in-crochet.html")}">changing colours in crochet</a>.</p>
<h2>The cap and hanging loop</h2>
<ol><li>With gold yarn, make a magic ring and work 6 sc into it (6).</li>
<li>Inc in each stitch around (12).</li>
<li>Sc in the back loop only of each stitch around (12). This makes the sides turn up like a cup.</li>
<li>Sc in each stitch around (12). Sl st to the next stitch and fasten off with a long tail.</li>
<li>For the loop, chain 20 in gold (or cut 8 in of ribbon), thread both ends down through the middle of the cap and knot them inside.</li>
<li>Sit the cap on the top of the bauble, over the closing point, and sew round its edge with the long tail.</li></ol>
<h2>Ideas to decorate your bauble</h2>
<ul><li><strong>Snowy band:</strong> in a white band, stitch little Vs or crosses with red yarn to look like a Nordic jumper.</li>
<li><strong>Christmas pudding:</strong> brown ball, a wavy white top (crochet a small circle, then sc-hdc-dc scallops round the edge) and a felt holly leaf.</li>
<li><strong>Snowman bauble:</strong> white ball, two embroidered eyes, an orange French knot or tiny cone for the nose, and a scrap-yarn scarf (chain 30, one row of sc).</li>
<li><strong>Granny-stripe look:</strong> change colour every 2 rounds for a candy stripe.</li>
<li><strong>Name bauble:</strong> make the large size and embroider a short name or year across the band in backstitch (see our <a href="{href("embroidery-stitches.html")}">embroidery stitches</a>).</li></ul>
<h2>How do you keep a crochet ball round?</h2>
<p>Stuff it firmly, a little at a time, and push the stuffing outwards with the end of your hook before the hole gets small. Work the same number of plain rounds as increase rounds (the writer does this), and use the invisible decrease, which doesn't leave gaps. If it looks a bit square, roll it between your hands for a minute.</p>
<h2>Selling crochet ornaments</h2>
<p>Crochet baubles are a good craft fair seller because they're quick, light and use up scraps. You're welcome to sell baubles made from this pattern (please don't share the pattern itself as your own). Sets of 3 or 6 in matching colours sell better than singles. Work out a fair price from your hours and materials with the <a href="{href("how-to-price-amigurumi.html")}">amigurumi price calculator</a>, and see more quick ideas in <a href="{href("christmas-crafts-to-sell.html")}">Christmas crafts to make and sell</a>.</p>
<p>More to make: a <a href="{href("crochet-snowflake-pattern.html")}">free crochet snowflake pattern</a> for the tree, a <a href="{href("crochet-sheep-pattern.html")}">little crochet sheep</a>, a <a href="{href("christmas-stocking-calculator.html")}">Christmas stocking</a> and <a href="{href("how-to-make-a-pom-pom.html")}">pom poms</a> for garlands. Check what you can finish before Christmas with the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>.</p>
<p class="note">Pattern, drawings and wording are our own (28 Nov 2026), using the standard amigurumi ball maths (6 stitches added or taken away per round). Sizes, yarn amounts and times are estimates: tension and yarn change them.</p>
</div></div></section>'''
cxo_faq = [
    ("How do you crochet an easy Christmas ornament?", "Crochet a small stuffed ball: 6 sc in a magic ring, add 6 stitches a round to 30, work 5 plain rounds, then decrease 6 a round back to 6, stuffing as you go. Add a small gold cap and a chain loop to hang it."),
    ("How much yarn does a crochet bauble take?", "About 10 yards for a small bauble and 15 to 25 yards for a medium or large one in worsted yarn (our estimates). A 100 g ball of worsted makes 8 to 12 baubles."),
    ("How long does it take to crochet a Christmas ornament?", "About 30 to 60 minutes for a small or medium bauble once you're used to working in the round."),
    ("What yarn is best for crochet Christmas ornaments?", "A smooth acrylic or cotton in worsted or DK weight. Cotton holds its shape best; add a metallic thread for a bit of sparkle."),
    ("How big is a crochet bauble?", "With worsted yarn and a 3.5 mm hook, roughly 1.7 in for 24 stitches, 2.1 in for 30 and 2.5 in for 36 (our estimates). Chunky yarn makes them about half as big again."),
    ("Can I cover a plastic bauble with crochet?", "Yes: work the same rounds but leave out the stuffing, slip the bauble in when the opening is about a third of the way through the decreases, then finish around it. Match the size by measuring round the bauble and comparing it with the writer's size."),
]
SHOP_FOR["crochet-christmas-ornament-pattern.html"] = ["christmas-gift-tags", "crochet-knitting-pricing-calculator", "christmas-gift-planner-budget", "2027-crochet-knitting-planner"]
page("crochet-christmas-ornament-pattern.html", "Free Crochet Christmas Ornament Pattern (Easy Bauble)",
     "Free easy crochet Christmas bauble pattern: six drawn steps, a gold cap and loop, and a writer for 4 sizes and stripe styles with round tick boxes.",
     cxo, cxo_faq, "Crochet Christmas ornament pattern", app_name="Crochet bauble pattern writer")


# ======== FREE CROCHET SNOWFLAKE PATTERN ========
# Demand: Q5 'how to make a crochet snowflake for beginners' (SERP 27-28 Nov: Skillshare x2, Ravelry x6, Craftaholic Witch, Instructables x2,
# B.Hooked, Bella Coco, AllFreeCrochet) + 'how to stiffen crochet snowflakes starch glue' (Hunker, Crochet Spot, Itchin' for some Stitchin',
# The Purple Poncho, The Crochet Crowd, WonderHowTo, Dummies spray starch, eHow, Mumsnet thread). Pattern is our own 4-round design.

def _snowflake(cx, cy, R, col="#fbfcfa", stroke=_INK):
    s = ""
    for i in range(6):
        a = i * _m17.pi / 3 - _m17.pi / 2
        ca, sa = _m17.cos(a), _m17.sin(a)
        tip = (cx + R * ca, cy + R * sa)
        s += f'<line x1="{cx + R * 0.38 * ca:.1f}" y1="{cy + R * 0.38 * sa:.1f}" x2="{tip[0]:.1f}" y2="{tip[1]:.1f}" stroke="{stroke}" stroke-width="5" stroke-linecap="round"/>'
        s += f'<line x1="{cx + R * 0.38 * ca:.1f}" y1="{cy + R * 0.38 * sa:.1f}" x2="{tip[0]:.1f}" y2="{tip[1]:.1f}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
        for side in (-1, 1):
            b = a + side * 0.55
            px, py = cx + R * 0.72 * ca, cy + R * 0.72 * sa
            s += f'<circle cx="{px + R * 0.17 * _m17.cos(b):.1f}" cy="{py + R * 0.17 * _m17.sin(b):.1f}" r="{R * 0.075:.1f}" fill="none" stroke="{stroke}" stroke-width="3.4"/><circle cx="{px + R * 0.17 * _m17.cos(b):.1f}" cy="{py + R * 0.17 * _m17.sin(b):.1f}" r="{R * 0.075:.1f}" fill="none" stroke="{col}" stroke-width="1.6"/>'
        s += f'<ellipse cx="{cx + R * 0.93 * ca:.1f}" cy="{cy + R * 0.93 * sa:.1f}" rx="{R * 0.07:.1f}" ry="{R * 0.12:.1f}" transform="rotate({a * 180 / _m17.pi + 90:.0f} {cx + R * 0.93 * ca:.1f} {cy + R * 0.93 * sa:.1f})" fill="none" stroke="{stroke}" stroke-width="3.4"/>'
        b2 = a + _m17.pi / 6
        s += f'<path d="M{cx + R * 0.36 * _m17.cos(a):.1f} {cy + R * 0.36 * _m17.sin(a):.1f} Q{cx + R * 0.5 * _m17.cos(b2):.1f} {cy + R * 0.5 * _m17.sin(b2):.1f} {cx + R * 0.36 * _m17.cos(a + _m17.pi / 3):.1f} {cy + R * 0.36 * _m17.sin(a + _m17.pi / 3):.1f}" fill="none" stroke="{stroke}" stroke-width="4"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R * 0.3:.1f}" fill="none" stroke="{stroke}" stroke-width="{R * 0.12 + 2:.1f}"/><circle cx="{cx}" cy="{cy}" r="{R * 0.3:.1f}" fill="none" stroke="{col}" stroke-width="{R * 0.12:.1f}"/>'
    return s


def _csf_svg(step, label):
    if step == 1:
        s = (f'<circle cx="140" cy="90" r="34" fill="none" stroke="{_INK}" stroke-width="14"/><circle cx="140" cy="90" r="34" fill="none" stroke="#fbfcfa" stroke-width="11"/>'
             + "".join(f'<line x1="{140 + 28 * _m17.cos(i * _m17.pi / 6)}" y1="{90 + 28 * _m17.sin(i * _m17.pi / 6)}" x2="{140 + 40 * _m17.cos(i * _m17.pi / 6)}" y2="{90 + 40 * _m17.sin(i * _m17.pi / 6)}" stroke="{_TEAL}" stroke-width="2"/>' for i in range(12))
             + f'<text x="140" y="172" {_T12} text-anchor="middle">Round 1: 12 dc in a magic ring</text>')
    elif step == 2:
        s = (f'<circle cx="140" cy="90" r="30" fill="none" stroke="{_INK}" stroke-width="12"/><circle cx="140" cy="90" r="30" fill="none" stroke="#fbfcfa" stroke-width="9"/>'
             + "".join(f'<path d="M{140 + 36 * _m17.cos(i * _m17.pi / 3)} {90 + 36 * _m17.sin(i * _m17.pi / 3)} Q{140 + 58 * _m17.cos(i * _m17.pi / 3 + 0.52)} {90 + 58 * _m17.sin(i * _m17.pi / 3 + 0.52)} {140 + 36 * _m17.cos((i + 1) * _m17.pi / 3)} {90 + 36 * _m17.sin((i + 1) * _m17.pi / 3)}" fill="none" stroke="{_TEAL}" stroke-width="4"/>' for i in range(6))
             + f'<text x="140" y="172" {_T12} text-anchor="middle">Round 2: 6 chain-3 loops</text>')
    elif step == 3:
        s = (f'<circle cx="140" cy="90" r="26" fill="none" stroke="{_INK}" stroke-width="10"/><circle cx="140" cy="90" r="26" fill="none" stroke="#fbfcfa" stroke-width="7"/>'
             + "".join(f'<path d="M{140 + 34 * _m17.cos(a - 0.3)} {90 + 34 * _m17.sin(a - 0.3)} L{140 + 60 * _m17.cos(a)} {90 + 60 * _m17.sin(a)} L{140 + 34 * _m17.cos(a + 0.3)} {90 + 34 * _m17.sin(a + 0.3)}" fill="none" stroke="{_TEAL}" stroke-width="6" stroke-linejoin="round"/>' for a in [i * _m17.pi / 3 + 0.52 for i in range(6)])
             + f'<text x="140" y="172" {_T12} text-anchor="middle">Round 3: a shell in each loop</text>')
    elif step == 4:
        s = _snowflake(140, 88, 70, col="#fbfcfa") + f'<text x="140" y="188" {_T12} text-anchor="middle">Round 4: picot points</text>'
    elif step == 5:
        s = (f'<rect x="40" y="24" width="200" height="140" rx="6" fill="#e9eef0" stroke="{_INK}" stroke-width="2"/>' + _snowflake(140, 94, 56, col="#fbfcfa")
             + "".join(f'<circle cx="{140 + 60 * _m17.cos(i * _m17.pi / 3 - _m17.pi / 2)}" cy="{94 + 60 * _m17.sin(i * _m17.pi / 3 - _m17.pi / 2)}" r="4" fill="{_BERRY}" stroke="{_INK}" stroke-width="1.2"/>' for i in range(6))
             + f'<text x="140" y="188" {_T12} text-anchor="middle">pin every point on a covered board</text>')
    else:
        s = (f'<line x1="140" y1="10" x2="140" y2="34" stroke="{_INK}" stroke-width="1.5"/>' + _snowflake(140, 96, 60, col="#fbfcfa")
             + f'<text x="140" y="188" {_T12} text-anchor="middle">dry overnight, then hang</text>')
    return _svg12(s, label)


CSF_STEPS = [(1, "1. Round 1", "Magic ring, chain 3 (counts as a dc), 11 dc into the ring. Pull it closed and join to the top of the chain 3 (12 stitches)."),
             (2, "2. Round 2", "Chain 1, sc in the same stitch, chain 3, skip 1, *sc in the next stitch, chain 3, skip 1*; repeat 4 more times and join (6 loops)."),
             (3, "3. Round 3", "Slip stitch into the first loop and work a shell, (2 dc, ch 2, 2 dc), into every loop. Join to the top of the first chain 3."),
             (4, "4. Round 4", "In each shell's chain-2 space make a point: (sc, ch 3, sc, ch 6, sc, ch 3, sc). Between points: ch 3, sc between the shells, ch 3."),
             (5, "5. Stiffen and pin", "Soak the snowflake in stiffener, squeeze it out, then pin it flat on a board covered in cling film, one pin in every point and loop."),
             (6, "6. Dry and hang", "Leave it to dry completely (overnight). Unpin, tie on a thread loop and hang it on the tree or in a window.")]
csf_cards = "".join(f'<figure class="gq-fig"><div>{_csf_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CSF_STEPS)

CSF_ROUNDS = [("1", "Make a magic ring. Ch 3 (counts as dc), 11 dc in the ring. Pull the ring closed. Sl st to the top of the ch 3.", "12 dc"),
              ("2", "Ch 1, sc in the same st, ch 3, sk 1, *sc in the next st, ch 3, sk 1*; repeat from * 4 more times. Sl st to the first sc.", "6 sc, 6 ch-3 loops"),
              ("3", "Sl st into the first ch-3 loop. Ch 3 (counts as dc), (dc, ch 2, 2 dc) in the same loop. *(2 dc, ch 2, 2 dc) in the next loop*; repeat from * 4 more times. Sl st to the top of the ch 3.", "6 shells"),
              ("4", "Sl st in the next dc and into the ch-2 space. Ch 1, (sc, ch 3, sc, ch 6, sc, ch 3, sc) in the same space, ch 3, sc in the gap between this shell and the next, ch 3. *(sc, ch 3, sc, ch 6, sc, ch 3, sc) in the next ch-2 space, ch 3, sc between shells, ch 3*; repeat from * 4 more times. Sl st to the first sc. Fasten off.", "6 points")]
csf_rounds = "".join(f'<li><label class="chk"><input type="checkbox" data-csf="{i}"> <span><strong>R{rn}:</strong> <span data-us="{e(t)}">{e(t)}</span> <em>(<span data-us="{e(c)}">{e(c)}</span>)</em></span></label></li>' for i, (rn, t, c) in enumerate(CSF_ROUNDS))

csf = top("Free crochet snowflake pattern (easy, 4 rounds)", "This little six-point snowflake is only four rounds, so it's a good first snowflake: a ring of double crochet, a round of chain loops, a round of shells, then picot points. Make it in cotton thread for a delicate tree decoration or in yarn for a quick window snowflake, then stiffen it so it stays flat.", "Crochet snowflake pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet an easy snowflake, work <strong>12 dc into a magic ring</strong>, then <strong>6 chain-3 loops</strong>, then a <strong>shell (2 dc, ch 2, 2 dc) in each loop</strong>, and finish with a <strong>picot point (sc, ch 3, sc, ch 6, sc, ch 3, sc) in each shell</strong>. To make it stiff, soak it in <strong>white PVA glue mixed half and half with water</strong> (or liquid starch), squeeze it out, <strong>pin every point flat</strong> on a board covered in cling film and leave it to dry overnight. In size 10 cotton thread with a 1.75 mm hook it's about 3 in (7.5 cm) across; in worsted yarn about 5.5 in (our estimates). Each snowflake takes about 20 to 30 minutes.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Snowflake size and stiffener helper</h3>
<div class="row2"><div class="field"><label for="csf-y">Thread or yarn</label><select id="csf-y"><option value="t10">Size 10 crochet cotton, 1.75 mm hook</option><option value="t3" selected>Size 3 cotton, 2.5 mm hook</option><option value="sp">Sport / 4 ply (2), 3 mm hook</option><option value="dk">DK / light (3), 4 mm hook</option><option value="w">Worsted / aran (4), 5 mm hook</option></select></div>
<div class="field"><label for="csf-n">How many snowflakes</label><input type="number" id="csf-n" value="6" min="1" max="100" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="csf-m">Stiffen with</label><select id="csf-m"><option value="glue" selected>White PVA (school) glue and water</option><option value="starch">Liquid laundry starch</option><option value="corn">Cornflour (cornstarch) paste</option><option value="sugar">Sugar syrup (very stiff)</option><option value="spray">Spray starch (light hold)</option></select></div>
<div class="field"><span class="label" id="csf-t-l">Terms</span><div class="seg" role="group" aria-labelledby="csf-t-l" id="csf-t"><button type="button" data-v="us" aria-pressed="true">US</button><button type="button" data-v="uk" aria-pressed="false">UK</button></div></div></div>
</div><div class="result" aria-live="polite" id="csf-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<div class="gq-figs"><figure class="gq-fig"><div>{_svg12('<rect x="0" y="0" width="280" height="200" rx="10" fill="#1f2a44"/>' + _snowflake(140, 100, 82, col="#fbfcfa", stroke="#9fb4c8"), "The finished crochet snowflake: a ring, six shells and six picot points", "0 0 280 200")}<figcaption><strong>The finished snowflake.</strong> Our own drawing of the pattern on this page.</figcaption></div></figure></div>
<h2>The pattern, round by round</h2>
<p class="sub">Stitch names follow the US / UK switch in the helper above (US by default). Tick each round as you finish it (kept on this device).</p>
<ul class="shp-list" id="csf-rounds">{csf_rounds}</ul>
<h2>How to crochet a snowflake, step by step</h2>
<div class="gq-figs">{csf_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Thread or yarn:</strong> white or ice-blue cotton holds its shape best and takes stiffener well. Size 10 crochet thread gives the classic lacy look; size 3 cotton or a DK cotton is easier for beginners because you can see the stitches. Acrylic works, but it never goes quite as crisp.</li>
<li><strong>Hook:</strong> 1.5 to 1.75 mm for size 10 thread, 2.25 to 2.5 mm for size 3, or the label size for yarn.</li>
<li><strong>To finish:</strong> a stiffener (see below), a bowl, an old towel, a foam board, cork board or folded cardboard covered with cling film or a plastic bag, and rust-proof pins.</li></ul>
<h2>Abbreviations</h2>
<p><strong>ch</strong> chain, <strong>sl st</strong> slip stitch, <strong>sc</strong> single crochet (UK double crochet), <strong>dc</strong> double crochet (UK treble), <strong>sk</strong> skip, <strong>st</strong> stitch, <strong>*…*</strong> repeat the part between the stars. A <strong>ch-3 loop</strong> is the space under a chain 3. New to these? See <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>, <a href="{href("how-to-crochet-magic-ring.html")}">the magic ring</a> and <a href="{href("how-to-slip-stitch-crochet.html")}">joining with a slip stitch</a>.</p>
<h2 id="stiffen">How to stiffen crochet snowflakes</h2>
<p>All the usual methods work the same way: soak, squeeze, pin, dry. The difference is how stiff the snowflake ends up and how it copes with damp.</p>
<table class="mt"><thead><tr><th>Stiffener</th><th>How to mix it</th><th>Result</th></tr></thead><tbody>
<tr><td>White PVA glue</td><td>About equal parts glue and water (more glue for stiffer)</td><td>Firm, lasts for years, dries clear. The easiest choice.</td></tr>
<tr><td>Liquid laundry starch</td><td>Use straight from the bottle</td><td>Medium stiff; washes out, so you can re-shape it next year.</td></tr>
<tr><td>Cornflour paste</td><td>Stir about 1 tablespoon cornflour into a little cold water, add to 1 cup of boiling water, stir until it thickens a little, cool</td><td>Medium; cheap and kitchen-safe. Can soften in damp rooms.</td></tr>
<tr><td>Sugar syrup</td><td>Equal parts sugar and water, warmed until the sugar dissolves, cooled</td><td>Very stiff, but goes sticky in humid air and can attract insects. Store in a dry box.</td></tr>
<tr><td>Spray starch</td><td>Pin the snowflake first, then spray until damp; repeat once dry</td><td>Light hold; good for big yarn snowflakes or a quick touch-up.</td></tr>
<tr><td>Ready-made fabric stiffener</td><td>As the bottle says</td><td>Very firm and reliable; the most expensive.</td></tr></tbody></table>
<ol><li><strong>Soak</strong> the snowflake in the mixture for a minute, working it in with your fingers.</li>
<li><strong>Squeeze</strong> out the extra (don't wring it), then blot it in a towel so the holes aren't filled with glue.</li>
<li><strong>Pin</strong> it face up on your covered board. Put a pin in the centre of the ring first, then one in each of the 6 points, then the side picots. Use a printed hexagon or a ruler so the points are evenly spaced.</li>
<li><strong>Dry</strong> it completely, usually overnight (up to 24 hours for glue in a cool room). Don't use a hair dryer on sugar syrup.</li>
<li><strong>Unpin</strong> and check: if it's still floppy, give it a second, slightly stronger coat.</li></ol>
<p>Our guide to <a href="{href("how-to-block-knitting-crochet.html")}">blocking knitting and crochet</a> covers pinning and spray blocking for larger pieces.</p>
<h2>Snowflake problems and fixes</h2>
<ul><li><strong>It cups or curls:</strong> your chains are tighter than your stitches. Go up a hook size for round 2, or chain more loosely; stiffening also flattens it.</li>
<li><strong>It ruffles:</strong> the shells are too big for the loops. Use 1 dc either side of the ch 2 instead of 2.</li>
<li><strong>Points are uneven:</strong> count the chains in every point (3, 6, 3) and pin them all to the same circle when you stiffen.</li>
<li><strong>White glue left a film in the holes:</strong> poke it out with a pin while it's still wet, and dilute the glue a little more next time.</li></ul>
<h2>Ideas for your snowflakes</h2>
<p>Hang them on the tree with fishing line, string a garland across a window, stitch one onto a <a href="{href("christmas-stocking-calculator.html")}">Christmas stocking</a>, use one as a gift topper with our <a href="{href("christmas-crafts.html")}">printable gift tags</a>, or glue a flat stiffened one into a <a href="{href("junk-journal-page-ideas.html")}#christmas">Christmas junk journal</a> spread. Pair them with our <a href="{href("crochet-christmas-ornament-pattern.html")}">crochet bauble pattern</a> for a matching set. Selling them? Sets of 6 or 12 sell better than singles: price your time with the <a href="{href("how-to-price-crochet-items.html")}">crochet pricing guide</a>.</p>
<p class="note">Pattern, drawings and wording are our own (28 Nov 2026). Stiffening methods are standard craft practice, checked against The Purple Poncho, Crochet Spot, Hunker and Itchin' for some Stitchin' tutorials; mixing amounts vary between sources, so test on a swatch. Sizes, yarn and time are our estimates.</p>
</div></div></section>'''
csf_faq = [
    ("How do you crochet a simple snowflake for beginners?", "Work 12 double crochet in a magic ring, then 6 chain-3 loops, then a shell of (2 dc, ch 2, 2 dc) in each loop, and finish with a point of (sc, ch 3, sc, ch 6, sc, ch 3, sc) in each shell. Stiffen it and pin it flat to dry."),
    ("How do you stiffen crochet snowflakes?", "Soak them in white PVA glue mixed about half and half with water (or liquid starch), squeeze out the extra, pin every point flat on a board covered with cling film and leave them to dry overnight."),
    ("Can you stiffen crochet snowflakes with cornstarch?", "Yes. Cook a thin cornflour paste (about a tablespoon in a cup of water, heated until it thickens slightly), cool it, soak the snowflakes, pin and dry. It gives a medium hold and can soften in damp rooms."),
    ("What thread is best for crochet snowflakes?", "Mercerised cotton crochet thread in size 10 for a classic lacy snowflake, or size 3 cotton for an easier, slightly bigger one. Cotton holds stiffener better than acrylic."),
    ("How big is a crochet snowflake?", "This 4-round pattern is about 3 in across in size 10 thread, 3.75 in in size 3 cotton and 5.5 in in worsted yarn (our estimates)."),
    ("How long does a crochet snowflake take?", "About 20 to 30 minutes for this pattern once you know it, plus overnight drying after stiffening."),
]
SHOP_FOR["crochet-snowflake-pattern.html"] = ["christmas-gift-tags", "december-days-journal-kit", "crochet-knitting-pricing-calculator", "christmas-gift-planner-budget"]
page("crochet-snowflake-pattern.html", "Free Crochet Snowflake Pattern (Easy) + How to Stiffen It",
     "Free easy 4-round crochet snowflake pattern with tick boxes and drawn steps, plus how to stiffen snowflakes with glue, starch, cornflour or sugar.",
     csf, csf_faq, "Crochet snowflake pattern", app_name="Crochet snowflake size and stiffener helper")


# ======== HOW TO CROCHET A BLANKET ========
# Demand: 'how to crochet a blanket for beginners step by step' (SERP 28 Nov: Apartment Therapy, Make and Do Crew, LoveCrafts UK, EasyCrochet,
# Jo to the World baby + throw, Skillshare x3, Stylist, Daily Crochet, B.Hooked, Handy Little Me, eHow, Caydo, Storables). We had size, chain,
# granny, C2C and pricing tools but no step-by-step 'first blanket' guide. Gauges and yardage use the same model as /blanket-size-calculator and
# /temperature-blanket-planner (CYC-based sc gauge by weight x stitch factors); all amounts labelled estimates.

def _cbk_svg(step, label):
    if step == 1:
        s = "".join(f'<ellipse cx="{40 + i * 20}" cy="100" rx="10" ry="6" fill="none" stroke="{_BERRY}" stroke-width="4"/>' for i in range(11)) + f'<text x="140" y="160" {_T12} text-anchor="middle">a long foundation chain</text>'
    elif step == 2:
        s = ("".join(f'<ellipse cx="{40 + i * 20}" cy="120" rx="10" ry="6" fill="none" stroke="{_BERRY}" stroke-width="4"/>' for i in range(11))
             + "".join(f'<rect x="{32 + i * 20}" y="84" width="16" height="30" rx="4" fill="{_TEAL}" stroke="{_INK}" stroke-width="1.4"/>' for i in range(10))
             + f'<text x="140" y="168" {_T12} text-anchor="middle">row 1: a stitch in each chain</text>')
    elif step == 3:
        s = ("".join(f'<rect x="{32 + i * 20}" y="104" width="16" height="30" rx="4" fill="{_TEAL}" stroke="{_INK}" stroke-width="1.4"/>' for i in range(10))
             + f'<path d="M240 104 q22 -10 0 -34" fill="none" stroke="{_GOLD}" stroke-width="4" marker-end="url(#a17)"/><defs><marker id="a17" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{_GOLD}"/></marker></defs>'
             + "".join(f'<ellipse cx="236" cy="{62 - i * 12}" rx="5" ry="7" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for i in range(2))
             + f'<text x="140" y="168" {_T12} text-anchor="middle">turn, chain up, work back</text>')
    elif step == 4:
        s = ("".join(f'<rect x="60" y="{30 + j * 22}" width="160" height="20" rx="3" fill="{(_TEAL, "#5fb1ac")[j % 2]}" stroke="{_INK}" stroke-width="1.2"/>' for j in range(6))
             + f'<text x="140" y="180" {_T12} text-anchor="middle">row after row, count every few rows</text>')
    elif step == 5:
        s = ("".join(f'<rect x="60" y="{30 + j * 22}" width="160" height="20" rx="3" fill="{_TEAL if j < 3 else _BERRY}" stroke="{_INK}" stroke-width="1.2"/>' for j in range(6))
             + f'<path d="M226 96 q20 6 20 30" fill="none" stroke="{_BERRY}" stroke-width="4"/><path d="M226 92 q24 -6 26 -30" fill="none" stroke="{_TEAL}" stroke-width="4"/>'
             + f'<text x="140" y="180" {_T12} text-anchor="middle">join a new skein at the edge</text>')
    else:
        s = (f'<rect x="54" y="24" width="172" height="140" rx="4" fill="{_GOLD}" stroke="{_INK}" stroke-width="2"/><rect x="66" y="36" width="148" height="116" rx="2" fill="{_TEAL}" stroke="{_INK}" stroke-width="1.2"/>'
             + "".join(f'<line x1="66" y1="{y}" x2="214" y2="{y}" stroke="#fbfcfa" stroke-width="1" opacity=".4"/>' for y in range(46, 152, 10))
             + f'<text x="140" y="186" {_T12} text-anchor="middle">a border all round, then weave in ends</text>')
    return _svg12(s, label)


CBK_STEPS = [(1, "1. Chain the width", "Make a slip knot and chain the number the writer gives you. Keep it loose: a tight chain makes the bottom edge pull in. Count twice."),
             (2, "2. Work row 1", "Work your stitch into the right chain from the hook (2nd for sc, 3rd for hdc, 4th for dc), then one stitch in every chain to the end."),
             (3, "3. Turn and chain", "Turn the work, chain 1 (sc), 2 (hdc) or 3 (dc) to climb up to the next row, then work one stitch in each stitch back across."),
             (4, "4. Keep going", "Repeat row after row. Count your stitches every few rows: one missing stitch at the edge is the most common beginner slip."),
             (5, "5. Join new yarn", "When a skein runs out, change at the end of a row: finish the last stitch with the new yarn and leave 6 in tails to weave in."),
             (6, "6. Add a border", "Work 1 to 3 rounds of sc all round, with 3 sc in each corner. It hides the uneven edges. Then weave in every end.")]
cbk_cards = "".join(f'<figure class="gq-fig"><div>{_cbk_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CBK_STEPS)

_bk_opts = "".join(f'<option value="{b["id"]}"{" selected" if b["id"] == "throw" else ""}>{e(b["name"])} ({b["w"]} x {b["l"]} in)</option>' for b in D["blankets"]) + '<option value="custom">My own size</option>'

cbk = top("How to crochet a blanket for beginners", "A plain blanket worked in rows is the classic first big crochet project: you only need one stitch and a lot of rows. Every step is drawn below, and the writer tells you how many chains to start with, how many rows to work, how much yarn to buy and roughly how long it'll take, for any size from a lovey to a king.", "How to crochet a blanket") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet a blanket, <strong>chain the width you want</strong> (about 150 chains for a 50 in throw in worsted half double crochet), work <strong>one stitch in each chain</strong> for the first row, then <strong>turn, chain up and work one stitch in each stitch</strong>, row after row, until it's long enough. Finish with a <strong>border of single crochet all round</strong> (3 sc in each corner) and weave in the ends. A 50 x 60 in throw in worsted hdc takes roughly 2,350 to 3,000 yards, about 12 to 15 skeins of 200 yd, and 20 to 30 hours (our estimates). Half double crochet is the best beginner stitch: quicker than single crochet, less holey than double.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Beginner blanket pattern writer</h3>
<div class="row2"><div class="field"><label for="cbk-z">Blanket size</label><select id="cbk-z">{_bk_opts}</select></div>
<div class="field" id="cbk-own" hidden><label for="cbk-w">Width x length (in)</label><div class="row2"><input type="number" id="cbk-w" value="50" min="8" max="120" inputmode="decimal" aria-label="Width in inches"><input type="number" id="cbk-l" value="60" min="8" max="120" inputmode="decimal" aria-label="Length in inches"></div></div></div>
<div class="row2"><div class="field"><label for="cbk-y">Yarn</label><select id="cbk-y"><option value="3">DK / light (3)</option><option value="4" selected>Worsted / aran (4)</option><option value="5">Chunky / bulky (5)</option><option value="6">Super bulky (6)</option><option value="7">Jumbo (7)</option></select></div>
<div class="field"><label for="cbk-s">Stitch</label><select id="cbk-s"><option value="sc">Single crochet (dense, warm, slowest)</option><option value="hdc" selected>Half double crochet (best for beginners)</option><option value="dc">Double crochet (quickest, more holes)</option></select></div></div>
<div class="row2"><div class="field"><label for="cbk-k">Yards per skein (from the label)</label><input type="number" id="cbk-k" value="200" min="20" max="2000" inputmode="numeric"></div>
<div class="field"><label for="cbk-g">Your swatch: stitches per 4 in (optional)</label><input type="number" id="cbk-g" placeholder="leave blank for a typical gauge" min="2" max="40" step="0.5" inputmode="decimal"></div></div>
<div class="field"><span class="label" id="cbk-t-l">Terms</span><div class="seg" role="group" aria-labelledby="cbk-t-l" id="cbk-t"><button type="button" data-v="us" aria-pressed="true">US</button><button type="button" data-v="uk" aria-pressed="false">UK</button></div></div>
</div><div class="result" aria-live="polite" id="cbk-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a blanket, step by step</h2>
<div class="gq-figs">{cbk_cards}</div>
<h2>What you need for your first blanket</h2>
<ul><li><strong>Yarn:</strong> a smooth, light-coloured acrylic or acrylic blend in worsted (4) or chunky (5). It's soft, machine washable and kind to your budget. Buy all the skeins at once and check they share the same dye lot number, or colours can differ slightly.</li>
<li><strong>Hook:</strong> the size on the yarn label or one bigger for a softer drape: about 5.5 to 6 mm (I-9 to J-10) for worsted, 8 mm (L-11) for chunky. An ergonomic handle saves your wrist on a big project.</li>
<li><strong>Also:</strong> stitch markers (one in the first and last stitch of each row makes edges easy), a tape measure, scissors and a tapestry needle.</li></ul>
<h2>Which crochet stitch is best for a beginner blanket?</h2>
<p><strong>Half double crochet</strong> is the sweet spot: it grows faster than single crochet but stays solid and warm. <strong>Single crochet</strong> is easiest to count but makes a stiffer, heavier blanket and uses more yarn. <strong>Double crochet</strong> is quickest and drapes nicely, but the gaps make it a bit less warm. Once you're happy with rows, try the <a href="{href("how-to-crochet-a-granny-square.html")}">granny square</a> (and <a href="{href("granny-square-blanket-calculator.html")}">how many squares you need</a>), corner to corner with the <a href="{href("c2c-blanket-calculator.html")}">C2C calculator</a>, or stripes with the <a href="{href("stripe-generator.html")}">stripe generator</a>. See all the basics on <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>.</p>
<h2>How many chains for a crochet blanket?</h2>
<p>Multiply the width you want by your stitches per inch, then add the turning chain: 1 extra for sc, 2 for hdc and 2 for dc (with the skipped chains counted as the first dc). The writer does this; if you crocheted a swatch, type your own stitches per 4 in for a more exact number. The <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a> handles pattern multiples and other stitches, and the <a href="{href("blanket-size-calculator.html")}">blanket size chart</a> lists standard sizes.</p>
<h2>How to keep crochet blanket edges straight</h2>
<ul><li>Put a stitch marker in the first and the last stitch of every row, so you never miss or add one.</li>
<li>Know whether your turning chain counts as a stitch (it doesn't for sc and hdc in this writer; it does for dc, so skip the first stitch and work into the top of the turning chain at the end).</li>
<li>Count your stitches every 5 to 10 rows. A <a href="{href("row-counter.html")}">row counter</a> helps keep track of rows too.</li>
<li>If the blanket gets wider or narrower, pull back (frog) to the last good row: it's quicker than fighting it later.</li></ul>
<h2>How long does it take to crochet a blanket?</h2>
<p>For a beginner, a baby blanket in worsted hdc is about 9 to 13 hours, a throw 20 to 30 and a queen 60 or more. Chunky yarn and double crochet are the quickest ways to cut it down. The writer gives a rough time for your size, and the <a href="{href("crochet-time-estimator.html")}">crochet time calculator</a> tells you if it'll be ready for a date.</p>
<h2>Finishing your blanket</h2>
<p>Weave in every end at least 2 in in three directions (see <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>), then wash and lay it flat or block it to straighten the edges (<a href="{href("how-to-block-knitting-crochet.html")}">how to block crochet</a>). Prefer needles? See <a href="{href("how-to-knit-a-blanket.html")}">how to knit a blanket</a>. Making it to sell or gift? Work out a fair price with the <a href="{href("how-to-price-a-crochet-blanket.html")}">crochet blanket price calculator</a>.</p>
<p class="note">Method is standard crochet technique, checked against LoveCrafts, EasyCrochet and Jo to the World beginner blanket guides (28 Nov 2026). Gauges use typical Craft Yarn Council ranges for each yarn weight; chain counts, rows, yardage and hours are our estimates, so make a swatch and buy a spare skein. Drawings and wording are our own.</p>
</div></div></section>'''
cbk_faq = [
    ("How do you crochet a blanket for beginners?", "Chain the width you want, work one stitch in each chain for row 1, then turn, chain 1 to 3 and work one stitch in each stitch, row after row, until it's long enough. Finish with a single crochet border and weave in the ends."),
    ("How many chains do I need for a crochet blanket?", "Width in inches times your stitches per inch, plus the turning chain. For a 50 in throw in worsted half double crochet that's about 150 chains; for a 36 in baby blanket about 110 (our estimates)."),
    ("How much yarn do I need to crochet a blanket?", "Roughly 1,000 to 1,300 yards of worsted for a 36 in baby blanket and 2,350 to 3,000 yards for a 50 x 60 in throw in half double crochet (our estimates). Single crochet uses more."),
    ("What is the easiest crochet stitch for a blanket?", "Half double crochet: it's quick, solid and easy to count. Single crochet is simpler but slower; double crochet is quickest but more open."),
    ("How long does it take to crochet a blanket?", "About 9 to 13 hours for a baby blanket and 20 to 30 hours for a throw in worsted half double crochet, for a beginner. Chunky yarn is much quicker."),
    ("Why is my crochet blanket getting wider?", "You're adding a stitch at the ends of rows, usually by working into the turning chain or the first stitch twice. Mark the first and last stitch of each row and count every few rows."),
]
SHOP_FOR["how-to-crochet-a-blanket.html"] = ["2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "yarn-stash-tracker", "christmas-gift-planner-budget"]
page("how-to-crochet-a-blanket.html", "How to Crochet a Blanket for Beginners (+ Pattern Writer)",
     "How to crochet a blanket for beginners: six drawn steps, the best stitch, and a writer for chains, rows, yarn, skeins and hours for any size.",
     cbk, cbk_faq, "How to crochet a blanket", app_name="Beginner crochet blanket pattern writer")
