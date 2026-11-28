# ---------------- 28 Nov 2026 run 20: CROCHET BASKET / YARN BOWL PATTERN + HOW TO HEM PANTS BY HAND + SCRAPBOOK LAYOUT IDEAS ----------------
# Executed from build.py after plan19.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 28 Nov run 20). Patterns, drawings and wording our own. JS in assets/app.js (cbb-*, hem-*, sbl-*).


# ======== FREE CROCHET BASKET PATTERN (round, any size, yarn bowl option) ========
# Demand: V5/R2/R6 'yarn bowl' + 'yarn holder for crochet' (Trends +130%), 'how to crochet a basket for beginners step by step'
# (SERP 28 Nov: B.Hooked x3, Sigoni Macaroni, Handy Little Me 17 baskets, Yarnspirations bulky basket, Craftaholics Anonymous, One Little Project,
# We Are Knitters, Envato Tuts+, Ravelry/LoveCrafts/Ribblr bowl listings; no size writer). Construction: flat sc circle (6 increases a round),
# a back-loop-only turning round, straight sc walls. Yardage = area x yd per sq in (firm sc, estimate).

def _cbk_svg(step, label):
    Y, Y2 = "#d9567f", "#e47aa3"
    if step == 1:
        s = (f'<circle cx="140" cy="88" r="30" fill="none" stroke="{Y}" stroke-width="6"/>'
             + "".join(f'<path d="M{140 + 30 * __import__("math").cos(a * 1.047):.1f} {88 + 30 * __import__("math").sin(a * 1.047):.1f} l0 -8" stroke="{_INK}" stroke-width="2"/>' for a in range(6))
             + f'<text x="140" y="160" {_T12} text-anchor="middle">6 sc in a magic ring, pull it tight</text>')
    elif step == 2:
        s = ("".join(f'<circle cx="140" cy="88" r="{r}" fill="none" stroke="{c}" stroke-width="8"/>' for r, c in ((12, Y), (24, Y2), (36, Y), (48, Y2)))
             + f'<circle cx="188" cy="88" r="5" fill="{_GOLD}"/>'
             + f'<text x="140" y="166" {_T12} text-anchor="middle">increase 6 stitches every round</text><text x="140" y="182" {_T12} text-anchor="middle">until the base is wide enough</text>')
    elif step == 3:
        s = (f'<ellipse cx="140" cy="120" rx="90" ry="24" fill="{Y2}" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M50 120 v-14 a90 24 0 0 1 180 0 v14" fill="none" stroke="{Y}" stroke-width="6"/>'
             f'<path d="M188 96 l14 -16" stroke="{_GOLD}" stroke-width="3"/><text x="214" y="74" {_T12} text-anchor="middle">back loop</text>'
             f'<text x="140" y="174" {_T12} text-anchor="middle">1 round in back loops only turns the corner</text>')
    elif step == 4:
        s = (f'<path d="M60 52 v86 a80 20 0 0 0 160 0 v-86" fill="{Y}" stroke="{_INK}" stroke-width="2"/><ellipse cx="140" cy="52" rx="80" ry="20" fill="#f4c6d6" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M60 {66 + j * 14} a80 20 0 0 0 160 0" fill="none" stroke="{Y2}" stroke-width="2"/>' for j in range(5))
             + f'<text x="140" y="188" {_T12} text-anchor="middle">sc every round for the walls, no increases</text>')
    elif step == 5:
        s = (f'<path d="M60 52 v86 a80 20 0 0 0 160 0 v-86" fill="{Y}" stroke="{_INK}" stroke-width="2"/><ellipse cx="140" cy="52" rx="80" ry="20" fill="#f4c6d6" stroke="{_INK}" stroke-width="2"/>'
             f'<rect x="76" y="70" width="26" height="10" rx="5" fill="#f6f1e6" stroke="{_INK}" stroke-width="1.5"/><rect x="178" y="70" width="26" height="10" rx="5" fill="#f6f1e6" stroke="{_INK}" stroke-width="1.5"/>'
             f'<circle cx="140" cy="84" r="5" fill="#f6f1e6" stroke="{_INK}" stroke-width="1.5"/><path d="M140 84 q30 -60 80 -70" fill="none" stroke="{_TEAL}" stroke-width="3"/>'
             f'<text x="140" y="188" {_T12} text-anchor="middle">optional handle slots and a yarn hole</text>')
    else:
        s = (f'<path d="M60 52 v86 a80 20 0 0 0 160 0 v-86" fill="{Y}" stroke="{_INK}" stroke-width="2"/><ellipse cx="140" cy="52" rx="80" ry="20" fill="#f4c6d6" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<circle cx="{66 + i * 15}" cy="{58 + abs(i - 5) * -2 + 8}" r="4" fill="{_GOLD}"/>' for i in range(11))
             + f'<circle cx="140" cy="44" r="14" fill="{_TEAL}"/><path d="M140 44 q40 -10 70 -34" fill="none" stroke="{_TEAL}" stroke-width="3"/>'
             + f'<text x="140" y="188" {_T12} text-anchor="middle">finish the rim with crab stitch, weave in</text>')
    return _svg12(s, label)


CBK_STEPS = [(1, "1. Start with a magic ring", "Make a magic ring and work 6 single crochet into it. Pull the tail to close the hole. Put a stitch marker in the first stitch: you will work in a spiral without joining."),
             (2, "2. Grow the flat base", "Work 2 sc in each stitch (12), then (sc, inc) around (18), then (sc 2, inc) around (24), adding one plain stitch between increases each round. The writer gives every round for your size."),
             (3, "3. Turn the corner", "When the base is the size you want, work one round of sc in the back loops only, with no increases. This leaves a ridge underneath and makes the sides stand up with a crisp edge."),
             (4, "4. Work the walls", "Now sc in both loops in every stitch, round after round, with no increases. The basket grows straight up. Move your marker up each round so you can count."),
             (5, "5. Add handles or a yarn hole", "For handles, chain over a few stitches and skip them on one round, then sc into the chains on the next. For a yarn bowl, chain 3 and skip 3 once, which leaves a hole for your working yarn."),
             (6, "6. Finish the rim", "Slip stitch into the next stitch to even out the spiral, then work a round of crab stitch (reverse sc) or slip stitch for a firm edge. Fasten off and weave the end into the wall.")]
cbk_cards = "".join(f'<figure class="gq-fig"><div>{_cbk_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CBK_STEPS)

cbk = top("Free crochet basket pattern (any size, plus a yarn bowl)", "A round crochet basket is just three parts: a flat circle, one round that turns the corner, and straight walls. This free beginner pattern writes every round for any size, from a little yarn bowl to a big storage basket, with handle slots, a yarn hole and an estimate of how much yarn to buy.", "Crochet basket pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet a basket, work a <strong>flat circle of single crochet</strong> (6 sc in a magic ring, then 6 increases every round) until it is as wide as you want the base. Work <strong>one round in the back loops only</strong> to turn the corner, then <strong>sc every round with no increases</strong> for the walls. Use thick yarn (or two strands held together) and a hook one or two sizes smaller than the label says, so the basket is firm. A 6 in yarn bowl takes roughly 120 to 200 yards of worsted held double, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Crochet basket pattern writer</h3>
<div class="row2"><div class="field"><label for="cbb-z">Size</label><select id="cbb-z"><option value="6x4">Yarn bowl (6 in wide, 4 in tall)</option><option value="5x3">Little catch-all (5 x 3 in)</option><option value="7x6" selected>Small basket (7 x 6 in)</option><option value="9x7">Medium basket (9 x 7 in)</option><option value="11x9">Storage basket (11 x 9 in)</option><option value="13x11">Large basket (13 x 11 in)</option><option value="custom">My own size</option></select></div>
<div class="field" id="cbb-own" hidden><label for="cbb-d">Base width x height (in)</label><div class="row2"><input type="number" id="cbb-d" value="8" min="3" max="20" step="0.5" inputmode="decimal" aria-label="Base width in inches"><input type="number" id="cbb-h" value="6" min="1" max="18" step="0.5" inputmode="decimal" aria-label="Height in inches"></div></div></div>
<div class="row2"><div class="field"><label for="cbb-y">Yarn</label><select id="cbb-y"><option value="w2">Worsted (4) held double</option><option value="w1">Worsted (4), one strand</option><option value="b">Bulky / chunky (5)</option><option value="sb" selected>Super bulky (6)</option><option value="t">T-shirt yarn or cotton cord</option></select></div>
<div class="field"><label for="cbb-g">Your swatch: sc per 4 in (optional)</label><input type="number" id="cbb-g" placeholder="leave blank for a typical firm gauge" min="4" max="24" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="cbb-x">Extras</label><select id="cbb-x"><option value="none">None</option><option value="handles" selected>Two handle slots</option><option value="hole">Yarn hole (yarn bowl)</option><option value="both">Handles and a yarn hole</option></select></div>
<div class="field"><label for="cbb-t">Terms</label><select id="cbb-t"><option value="us" selected>US (sc)</option><option value="uk">UK (dc)</option></select></div></div>
</div><div class="result" aria-live="polite" id="cbb-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a basket, step by step</h2>
<div class="gq-figs">{cbk_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> something thick and not too stretchy. Super bulky (6) yarn, T-shirt yarn or cotton macrame cord makes a basket that stands up on its own. Worsted (4) works too if you hold two strands together. Cotton holds its shape better than acrylic.</li>
<li><strong>Hook:</strong> one or two sizes smaller than the yarn label suggests, so the stitches are tight: about 6 mm (US J) for worsted held double, 8 to 9 mm (US L to M) for super bulky, 10 to 12 mm for T-shirt yarn.</li>
<li><strong>Also:</strong> a stitch marker (a scrap of yarn works), scissors and a large-eye tapestry needle.</li></ul>
<p>New to crochet? Learn the <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a> and <a href="{href("basic-crochet-stitches.html")}">single crochet</a> first; everything else is explained here.</p>
<h2>How to make the base lie flat</h2>
<p>A single crochet circle lies flat when you add <strong>6 stitches every round</strong>. If the edge starts to ripple like a frill, you are adding too many (or your stitches are loose); if it cups up like a bowl, you are adding too few. Count at the end of every round: round 5 should have 30 stitches, round 10 should have 60. If you stack increases in the same place each round, the circle turns into a hexagon, so the writer shifts the increase by half a repeat on every other round. Our <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a> does the same maths for hdc and dc circles.</p>
<h2>How to make a crochet basket stiff</h2>
<ul><li><strong>Tighter stitches:</strong> a smaller hook is the biggest help. The fabric should feel almost hard to push the hook through.</li>
<li><strong>More yarn:</strong> hold two or three strands together, or use cord or T-shirt yarn.</li>
<li><strong>Waistcoat stitch</strong> (sc worked between the legs of the stitch below) is denser than plain sc and makes very firm walls.</li>
<li><strong>Fold-down cuff:</strong> work the walls 2 in taller and fold the top over. The double layer stands up well.</li>
<li><strong>Stiffener:</strong> for a cotton yarn bowl, soak it in fabric stiffener or a 1:1 mix of PVA glue and water, shape it over a bowl and let it dry (see our <a href="{href("crochet-snowflake-pattern.html")}#stiffen">stiffening guide</a>).</li></ul>
<h2>Crochet yarn bowl: how it works</h2>
<p>A yarn bowl stops your ball rolling away while you crochet or knit. Pick the yarn hole option and the writer puts a small hole near the top of the wall: thread your working yarn through it from the inside, drop the ball in, and pull as you work. A crocheted bowl is soft, light and won't break if it falls; a ceramic or wooden one is heavier and holds the ball steadier. A 6 in wide, 4 in tall bowl fits most 100 g balls. To <a href="{href("how-to-wind-a-ball-of-yarn.html")}">wind a centre-pull ball</a> first, the ball will hardly move at all.</p>
<h2>Square and oval baskets</h2>
<p>For an oval basket, start with a chain as long as the difference between the length and the width, and work round both sides of it, increasing at each end. For a square one, start with a granny-style square or work 4 corners of 3 sc. Both use the same back-loop round and straight walls. This page writes round baskets, which are the easiest to get right first time.</p>
<h2>Selling crochet baskets</h2>
<p>Baskets sell well at craft fairs and online as plant pot covers, nursery storage and yarn bowls. Price for materials and your time, not just the yarn: our <a href="{href("how-to-price-crochet-items.html")}">crochet pricing guide</a> and <a href="{href("craft-fair-profit-calculator.html")}">craft fair profit calculator</a> help.</p>
<p class="note">Pattern and drawings are our own, using standard flat-circle and basket construction (6 sc increases a round, back-loop turning round), checked against B.Hooked, Sigoni Macaroni and Yarnspirations' basket tutorials (28 Nov 2026). Gauges, yardage and hours are estimates for firm single crochet; your own swatch makes them more accurate.</p>
</div></div></section>'''
cbk_faq = [
    ("How do you crochet a basket for beginners?", "Crochet a flat circle in single crochet, adding 6 stitches every round, until it is the width of the base. Work one round in the back loops only to turn the corner, then single crochet every round without increasing until the walls are tall enough. Finish with a slip stitch or crab stitch edge."),
    ("What yarn is best for a crochet basket?", "Thick, firm yarn: super bulky (6) yarn, T-shirt yarn or cotton cord. Worsted yarn works if you hold two strands together. Use a hook one or two sizes smaller than the label suggests so the basket is stiff."),
    ("How do I make my crochet basket stand up?", "Use a smaller hook, thicker yarn or two strands together, and make the turning round in the back loops only. A fold-down cuff, waistcoat stitch or fabric stiffener also help."),
    ("How much yarn do I need for a crochet basket?", "A 7 in wide, 6 in tall basket takes roughly 100 to 150 yards of super bulky yarn; a large storage basket can take 300 yards or more. The pattern writer above estimates it for your size and yarn."),
    ("How do you make a crochet yarn bowl?", "Make a small round basket about 6 in wide and 4 in tall, and leave a hole near the top by chaining 3 and skipping 3 stitches on one round. Thread your working yarn through the hole from the inside."),
    ("Why is my crochet basket base curling?", "If it cups upward you are adding too few stitches or crocheting tightly; if it ripples, too many. Add exactly 6 stitches every round and count at the end of each round."),
]
SHOP_FOR["crochet-basket-pattern.html"] = ["crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "yarn-stash-tracker", "small-business-pricing-inventory-spreadsheet"]
page("crochet-basket-pattern.html", "Free Crochet Basket Pattern: Any Size + Yarn Bowl (Writer)",
     "Free crochet basket pattern for beginners: a writer gives every round for any size, from a yarn bowl to a storage basket, with handles and yarn amounts.",
     cbk, cbk_faq, "Crochet basket pattern", app_name="Crochet basket pattern writer")


# ======== HOW TO HEM PANTS BY HAND ========
# Demand: N3 'how to hem pants by hand' (SERP 28 Nov: Skillshare, Make: blind hem, National Sewing Circle, Sew Guide dress pants, Sew Can She,
# One Good Thing (jeans original hem), LoveCrafts invisible hem, sewingtrip x2, wikiHow mirror, Melly Sews machine blind hem; no hem calculator).
# Allowances: dress trousers 1.5-2 in, jeans double fold ~1/2 + 1/2 in, tapered legs ~1 in (standard dressmaking practice; labelled typical).

def _hem_svg(step, label):
    L, D = "#7d8db5", "#5a6a94"
    leg = 'M100 20 h80 l6 130 h-92 z'
    if step == 1:
        s = (f'<path d="{leg}" fill="{L}" stroke="{_INK}" stroke-width="2"/><path d="M80 150 h120" stroke="{_WOOD}" stroke-width="4"/>'
             + "".join(f'<path d="M{96 + i * 18} 132 l4 -4 l4 4" fill="none" stroke="{_GOLD}" stroke-width="2"/>' for i in range(5))
             + f'<text x="140" y="178" {_T12} text-anchor="middle">try on with shoes, pin the new length</text>')
    elif step == 2:
        s = (f'<path d="{leg}" fill="{L}" stroke="{_INK}" stroke-width="2"/><path d="M95 130 h91" stroke="#fff" stroke-width="2" stroke-dasharray="6 4"/>'
             f'<path d="M94 110 h93" stroke="{_BERRY}" stroke-width="2"/>'
             f'<text x="214" y="114" {_T12}>fold line</text><text x="214" y="134" {_T12}>cut line</text>'
             f'<text x="140" y="178" {_T12} text-anchor="middle">mark the fold line, then the cut line below it</text>')
    elif step == 3:
        s = (f'<path d="M100 20 h80 l5 110 h-90 z" fill="{L}" stroke="{_INK}" stroke-width="2"/><path d="M95 130 h91" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M188 136 l20 18 M208 136 l-20 18" stroke="{_INK}" stroke-width="2"/><circle cx="184" cy="132" r="5" fill="none" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{97 + i * 9} 130 l4 6 l4 -6" fill="none" stroke="{_TEAL}" stroke-width="1.5"/>' for i in range(10))
             + f'<text x="140" y="178" {_T12} text-anchor="middle">cut, then overcast or zigzag the raw edge</text>')
    elif step == 4:
        s = (f'<path d="M100 20 h80 l4 90 h-88 z" fill="{L}" stroke="{_INK}" stroke-width="2"/><path d="M96 110 h88 l1 20 h-90 z" fill="{D}" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M140 136 v14 M134 144 l6 6 l6 -6" stroke="{_GOLD}" stroke-width="3" fill="none"/>'
             f'<text x="140" y="178" {_T12} text-anchor="middle">fold up to the inside, press and pin</text>')
    elif step == 5:
        s = (f'<rect x="40" y="40" width="200" height="70" fill="{L}" stroke="{_INK}" stroke-width="2"/><rect x="40" y="90" width="200" height="40" fill="{D}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{50 + i * 24} 90 l6 -6 l6 6" fill="none" stroke="{_BERRY}" stroke-width="2"/>' for i in range(8))
             + f'<text x="140" y="160" {_T12} text-anchor="middle">blind hem: catch 1-2 threads of the leg,</text><text x="140" y="176" {_T12} text-anchor="middle">then slide along inside the fold</text>')
    else:
        s = (f'<path d="M100 20 h80 l6 110 h-92 z" fill="{L}" stroke="{_INK}" stroke-width="2"/><path d="M90 140 h100" stroke="{_INK}" stroke-width="2"/>'
             f'<rect x="150" y="40" width="70" height="30" rx="8" fill="{_WOOD}" stroke="{_INK}" stroke-width="2" transform="rotate(14 185 55)"/>'
             f'<text x="140" y="178" {_T12} text-anchor="middle">press from the inside: no stitches show</text>')
    return _svg12(s, label)


HEM_STEPS = [(1, "1. Measure with shoes on", "Put the trousers on with the shoes you'll wear them with. Fold the leg up to the length you like and pin it. Do both legs: they are often slightly different."),
             (2, "2. Mark fold and cut lines", "Take them off, lay them flat and chalk a line at the pin: that is the fold line. Measure down from it by the hem allowance (the calculator gives it) and draw the cut line."),
             (3, "3. Unpick, cut and neaten", "Unpick the old hem if it's in the way and press it flat. Cut along the cut line. Overcast the raw edge by hand, or fold it under 1/4 in, so it won't fray."),
             (4, "4. Fold and press", "Fold the hem up to the inside along the fold line, matching the side seams. Press it with an iron and pin every few inches, pins pointing up."),
             (5, "5. Sew a blind hem", "Thread a single strand that matches the trousers. Catch one or two threads of the leg fabric, then slide the needle 1/4 to 3/8 in along inside the hem fold and come out. Repeat all round, keeping it loose."),
             (6, "6. Press to finish", "Knot inside the hem, then press from the inside with a cloth over the fabric. From the outside you should see almost nothing: just a few tiny dots.")]
hem_cards = "".join(f'<figure class="gq-fig"><div>{_hem_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in HEM_STEPS)

hem = top("How to hem pants by hand (invisible blind hem)", "You don't need a sewing machine to shorten trousers. A hand-sewn blind hem is what tailors use on good trousers, because it hardly shows. The steps are drawn below, and the hem calculator works out exactly where to fold and cut, how much to take off and how many stitches to expect.", "How to hem pants by hand") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to hem pants by hand, <strong>pin the new length with your shoes on</strong>, mark a fold line, then a cut line <strong>1.5 in below it</strong> for dress trousers (about 1 in for jeans and tapered legs). Cut, neaten the raw edge, fold up and press, then sew with a <strong>blind hem stitch</strong>: catch one or two threads of the leg, slide 1/4 to 3/8 in inside the fold, and repeat. A pair takes about 45 minutes to an hour by hand.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Pants hem calculator</h3>
<div class="row2"><div class="field"><label for="hem-m">How do you know the new length?</label><select id="hem-m"><option value="off" selected>I know how much to take off</option><option value="len">I know the inseam I want</option></select></div>
<div class="field"><label for="hem-u">Units</label><select id="hem-u"><option value="in" selected>inches</option><option value="cm">centimetres</option></select></div></div>
<div class="row2"><div class="field" id="hem-off-f"><label for="hem-off">Take off (shorten by)</label><input type="number" id="hem-off" value="2" min="0.25" max="30" step="0.125" inputmode="decimal"></div>
<div class="field" id="hem-len-f" hidden><label for="hem-c">Inseam now x inseam wanted</label><div class="row2"><input type="number" id="hem-c" value="32" min="10" max="45" step="0.125" inputmode="decimal" aria-label="Current inseam"><input type="number" id="hem-w" value="30" min="5" max="45" step="0.125" inputmode="decimal" aria-label="Inseam wanted"></div></div>
<div class="field"><label for="hem-t">Trousers</label><select id="hem-t"><option value="dress" selected>Dress trousers / chinos (blind hem)</option><option value="tapered">Tapered or slim leg (blind hem)</option><option value="jeans">Jeans (double fold)</option><option value="wide">Wide leg or linen (blind hem, deep)</option><option value="kids">Kids, room to let down later</option></select></div></div>
<div class="field"><label for="hem-o">Leg opening, measured flat across (optional)</label><input type="number" id="hem-o" placeholder="e.g. 8 in or 20 cm" min="2" max="60" step="0.25" inputmode="decimal"></div>
</div><div class="result" aria-live="polite" id="hem-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to hem pants by hand, step by step</h2>
<div class="gq-figs">{hem_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Needle and thread:</strong> a fine hand-sewing needle (sharps or betweens) and polyester all-purpose thread matching the trousers. On dark fabric go one shade darker; it shows less than lighter.</li>
<li><strong>Marking:</strong> tailor's chalk or a washable fabric pen, a ruler or tape measure, and pins or clips.</li>
<li><strong>Iron:</strong> pressing does half the work. A pressing cloth (a cotton tea towel) stops shiny marks on wool and dark fabric.</li>
<li><strong>Sharp scissors</strong> and a seam ripper for the old hem.</li></ul>
<h2>How long should pants be? (the break)</h2>
<p>The break is the little fold where the hem sits on your shoe. <strong>No break:</strong> the hem just touches the top of the shoe, a modern, cropped look for slim trousers. <strong>Slight break:</strong> one soft fold at the front; the safe choice for most suit and work trousers. <strong>Full break:</strong> a deeper fold, more traditional, for wide legs. Ankle trousers end at the ankle bone with no break at all. Whatever you pick, the back of the hem should sit about 1/2 in (1 cm) above where the heel meets the sole.</p>
<h2>The blind hem stitch, close up</h2>
<p>Work from right to left (left to right if you're left-handed) with the hem folded towards you. Hide the knot inside the fold. Take a tiny stitch, just one or two threads, in the trouser leg above the hem edge, then slide the needle inside the folded hem for about 1/4 to 3/8 in (6 to 10 mm) and come out. Repeat. Don't pull tight: tight stitches make dimples you can see from the outside. Every 4 in or so, make a small knot so that if the thread breaks, the whole hem won't drop. Our <a href="{href("hand-sewing-stitches.html")}">hand sewing stitches</a> page draws the slip stitch and catch stitch too.</p>
<h2>How to hem jeans by hand</h2>
<p>Denim is thick, so a double-folded hem is easier than a blind hem. Fold the edge up 1/2 in, then 1/2 in again, press hard, and sew with a small running or back stitch close to the top fold using strong jeans thread. A thimble really helps at the side seams. If you want to <strong>keep the original hem</strong>, fold the old hem up by the amount you're taking off plus 1/4 in, back stitch right next to the old hem edge, trim the extra fabric inside and press the original hem down.</p>
<h2>Hem allowances at a glance</h2>
<table class="mt"><thead><tr><th>Trousers</th><th>Typical hem allowance</th><th>Stitch</th></tr></thead><tbody>
<tr><td>Dress trousers, chinos</td><td>1.5 in (4 cm)</td><td>Blind hem</td></tr><tr><td>Tapered or slim leg</td><td>1 in (2.5 cm)</td><td>Blind hem</td></tr>
<tr><td>Jeans</td><td>1/2 + 1/2 in double fold (1 + 1 cm)</td><td>Back or running stitch</td></tr><tr><td>Wide leg, linen</td><td>2 in (5 cm)</td><td>Blind hem</td></tr>
<tr><td>Kids' trousers</td><td>2 to 3 in, to let down later</td><td>Loose blind hem</td></tr></tbody></table>
<p>On a tapered leg the trousers get narrower towards the ankle, so a deep hem is too tight to lie flat: keep it to about 1 in. See our <a href="{href("sewing-seam-allowance.html")}">seam allowance guide</a> for other garments.</p>
<p class="note">Steps and allowances follow standard dressmaking practice, checked against Sew Guide, Make: (hand-sewn blind hem), LoveCrafts (invisible hem) and Skillshare's pant hemming guide (28 Nov 2026). Allowances are typical figures; check the trousers' existing hem depth too. Drawings and wording our own.</p>
</div></div></section>'''
hem_faq = [
    ("How do you hem pants by hand without a sewing machine?", "Pin the new length with your shoes on, mark the fold line and a cut line about 1.5 in below it, cut and neaten the edge, fold up and press, then sew all round with a blind hem stitch, catching only one or two threads of the leg each time."),
    ("How much should I leave for a hem on pants?", "About 1.5 in (4 cm) for dress trousers, 1 in for tapered or slim legs, 1/2 in folded twice for jeans, and 2 in for wide-leg or linen trousers."),
    ("What is the best stitch to hem pants by hand?", "The blind hem stitch (also called slip hem or invisible hem stitch). It picks up only a thread or two of the outside fabric, so almost nothing shows from the right side."),
    ("How do you hem jeans by hand and keep the original hem?", "Fold the original hem up by the amount you want to take off plus 1/4 in, back stitch close to the edge of the old hem, trim the extra fabric inside and press the original hem back down."),
    ("How long does it take to hem pants by hand?", "About 45 minutes to an hour for a pair, including measuring and pressing. Jeans take a little longer because the fabric is thick."),
    ("Why can I see my hem stitches from the outside?", "You are taking too much of the outside fabric or pulling the thread tight. Pick up just one or two threads, keep the stitches relaxed and use thread one shade darker than the fabric."),
]
SHOP_FOR["how-to-hem-pants-by-hand.html"] = ["small-business-pricing-inventory-spreadsheet", "2027-habit-tracker-spreadsheet", "2027-printable-calendar", "yarn-stash-tracker"]
page("how-to-hem-pants-by-hand.html", "How to Hem Pants by Hand: Invisible Blind Hem (+ Calculator)",
     "How to hem pants by hand with an invisible blind hem: six drawn steps, jeans and original-hem methods, and a calculator for fold and cut lines.",
     hem, hem_faq, "How to hem pants by hand", app_name="Pants hem calculator")


# ======== SCRAPBOOK LAYOUT IDEAS ========
# Demand: 'scrapbook layout ideas for beginners' / 'scrapbook ideas' (SERP 28 Nov: Hobbycraft x2, Altenew x5 beginner posts, The Works 10 layouts,
# Stampin' Up, LoveCrafts beginner guide, CreativeLive, Scary Mommy, FaveCrafts, Adobe Express; no layout/sketch generator on page 1).
# Page sizes as /scrapbook-page-sizes (12x12, 8.5x11, 6x8, 8x8). Sketches are our own geometric layouts.

def _sbl_svg(step, label):
    P1, P2, P3 = "#e9d9e8", "#cfe3e0", "#f4dfb8"
    page_ = f'<rect x="80" y="20" width="120" height="120" fill="#fbf8f1" stroke="{_INK}" stroke-width="2"/>'
    if step == 1:
        s = ("".join(f'<rect x="{60 + i * 38}" y="{40 + (i % 2) * 14}" width="44" height="58" fill="{c}" stroke="{_INK}" stroke-width="2" transform="rotate({(-8, 4, -3, 9)[i]} {82 + i * 38} 70)"/>' for i, c in enumerate((P2, P3, P1, P2)))
             + f'<path d="M150 112 l10 10 l20 -22" fill="none" stroke="{_TEAL}" stroke-width="4"/>'
             + f'<text x="140" y="170" {_T12} text-anchor="middle">pick 1 to 5 photos with one story</text>')
    elif step == 2:
        s = (f'<rect x="60" y="30" width="80" height="100" fill="{P1}" stroke="{_INK}" stroke-width="2"/><rect x="100" y="40" width="80" height="100" fill="{P2}" stroke="{_INK}" stroke-width="2"/><rect x="140" y="50" width="80" height="100" fill="{P3}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<circle cx="{150 + (i % 3) * 22}" cy="{64 + (i // 3) * 22}" r="4" fill="#fff"/>' for i in range(12))
             + f'<text x="140" y="176" {_T12} text-anchor="middle">choose a background and 2-3 papers</text>')
    elif step == 3:
        s = (page_ + f'<rect x="96" y="38" width="66" height="50" fill="{_BERRY}"/><rect x="100" y="42" width="58" height="42" fill="{P2}" stroke="{_INK}" stroke-width="1"/>'
             f'<text x="140" y="170" {_T12} text-anchor="middle">mat photos with a thin border</text>')
    elif step == 4:
        s = (page_ + f'<rect x="90" y="30" width="60" height="44" fill="{P2}" stroke="{_INK}"/><rect x="154" y="30" width="36" height="44" fill="{P3}" stroke="{_INK}"/><rect x="90" y="78" width="40" height="30" fill="{P1}" stroke="{_INK}"/>'
             f'<rect x="134" y="78" width="56" height="12" fill="none" stroke="{_INK}" stroke-dasharray="3 3"/>'
             f'<text x="140" y="170" {_T12} text-anchor="middle">arrange on a sketch before you glue</text>')
    elif step == 5:
        s = (page_ + f'<rect x="90" y="30" width="100" height="56" fill="{P2}" stroke="{_INK}"/><text x="140" y="104" font-family="Georgia,serif" font-size="16" fill="{_BERRY}" text-anchor="middle">Snow day</text>'
             + "".join(f'<path d="M92 {114 + j * 7} h{88 - j * 14}" stroke="{_INK}" stroke-width="1.5"/>' for j in range(3))
             + f'<text x="140" y="170" {_T12} text-anchor="middle">add a title and a few lines of journaling</text>')
    else:
        s = (page_ + f'<rect x="90" y="30" width="100" height="56" fill="{P2}" stroke="{_INK}"/><text x="140" y="104" font-family="Georgia,serif" font-size="16" fill="{_BERRY}" text-anchor="middle">Snow day</text>'
             f'<circle cx="184" cy="34" r="10" fill="{_GOLD}"/><path d="M170 40 l12 12 l10 -18" fill="{_BERRY}"/><rect x="88" y="78" width="26" height="12" fill="{_TEAL}" transform="rotate(-12 101 84)"/>'
             f'<text x="140" y="170" {_T12} text-anchor="middle">cluster embellishments in a triangle</text>')
    return _svg12(s, label)


SBL_STEPS = [(1, "1. Pick the photos", "Choose one story per page: one day, one trip, one person. One great photo, or 3 to 5 that belong together, works better than squeezing in everything. Choose one to be the star."),
             (2, "2. Choose the papers", "Pick a background (plain cardstock is easiest), then two or three patterned papers that share a colour with the photos. A small, medium and large pattern together always looks balanced."),
             (3, "3. Mat the photos", "Glue the star photo onto cardstock and trim it with a thin border, about 1/8 to 1/4 in. A mat makes a photo stand out from busy paper."),
             (4, "4. Arrange on a sketch", "Lay everything out on the page before you stick anything down. Use a sketch (the generator below makes one) so photos, title and journaling each have a place. Snap a phone photo of the layout you like."),
             (5, "5. Add a title and journaling", "Write a short title, then a few lines: who, where, what happened and one small detail you'd otherwise forget. Even a date and three words count."),
             (6, "6. Embellish in threes", "Add stickers, die-cuts, buttons or washi in groups of three, set in a triangle around the star photo. This leads the eye across the page. Stop before the photos get lost.")]
sbl_cards = "".join(f'<figure class="gq-fig"><div>{_sbl_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in SBL_STEPS)

SBL_IDEAS = [
    ("Christmas and winter", ["First snow: one big photo, white cardstock, a few silver snowflakes and the date.", "Christmas morning grid: 6 small photos in a neat 3 x 2 block with a single red title strip.", "Advent memories: 24 tiny squares, one per day, with a word under each.", "The tree year by year: this year's tree photo next to last year's, side by side.", "Christmas card pocket: a pocket page holding the cards you were sent."]),
    ("Travel and days out", ["Map background: a printed map of the place, with photos matted in white on top.", "Ticket strip: train, museum and plane tickets in a row along the bottom.", "One trip, one page: a big landscape photo across the top and 3 small ones beneath.", "Postcard spread: a bought postcard as the 'star', with your own photos around it.", "Day in the life of a trip: times down the side with one photo for each."]),
    ("Family and baby", ["Month by month: 12 small photos in a grid for a baby's first year.", "Hands and feet: an outline trace of a hand next to a photo of the day.", "Then and now: a parent's childhood photo beside their child at the same age.", "Family recipe: a handwritten recipe card tucked beside photos of cooking it.", "Favourite things: a list of this year's favourite food, song and toy with one portrait."]),
    ("School, friends and milestones", ["First day of school: photo, a little interview (age, favourite colour, best friend), and the year.", "Report card or artwork: shrink and print a child's drawing as the background.", "Graduation: tassel colours as the paper scheme, cap photo as the star.", "Best friends: two photos taken years apart, the same pose.", "Birthday: party photo, the invitation and a candle count in stickers."]),
    ("Everyday and home", ["Pets: one photo and a list of the pet's silly habits.", "Our home: a photo of the front door and notes on what you love about it.", "Ordinary Tuesday: a page with photos from one normal day.", "Garden through the year: four photos of the same spot in each season.", "Quote page: a big printed quote with one small photo, lots of white space."]),
    ("Easy layouts for beginners", ["One photo, one paper: a single matted photo, a title and nothing else.", "Grid layout: photos in equal blocks with even gaps; very forgiving.", "Rule of thirds: photos in two thirds, journaling and embellishments in the other third.", "Colour block: three strips of paper across the page, photos sitting over the joins.", "White space: lots of plain background, everything grouped in the middle."]),
]
sbl_ideas = "".join(f'<h3>{e(t)}</h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>" for t, xs in SBL_IDEAS)

sbl = top("Scrapbook layout ideas for beginners", "Thirty easy scrapbook layout ideas, six drawn steps for putting a page together, and a free layout sketch generator: pick your page size and how many photos you have, and it draws a balanced sketch with exact photo and mat sizes you can follow.", "Scrapbook layout ideas") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the easiest scrapbook layouts for beginners are a <strong>single matted photo</strong> with a title, a <strong>grid</strong> of equal photos with even gaps, and the <strong>rule of thirds</strong> (photos in two thirds, words and embellishments in the rest). Pick one story per page, choose a plain background and 2 to 3 papers that match the photos, mat the star photo, then add a title, a few lines of journaling and embellishments in groups of three.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Scrapbook layout sketch generator</h3>
<div class="row2"><div class="field"><label for="sbl-p">Page size</label><select id="sbl-p"><option value="12x12" selected>12 x 12 in</option><option value="8.5x11">8.5 x 11 in</option><option value="8x8">8 x 8 in</option><option value="6x8">6 x 8 in</option><option value="8.27x11.69">A4</option></select></div>
<div class="field"><label for="sbl-n">Photos</label><select id="sbl-n"><option value="1">1</option><option value="2">2</option><option value="3" selected>3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option></select></div></div>
<div class="row2"><div class="field"><label for="sbl-m">Mat border</label><select id="sbl-m"><option value="0">No mats</option><option value="0.125">1/8 in</option><option value="0.25" selected>1/4 in</option></select></div>
<div class="field"><label>&nbsp;</label><button type="button" class="btn sm" id="sbl-go">Show me another sketch</button></div></div>
</div><div class="result" aria-live="polite" id="sbl-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to make a scrapbook layout, step by step</h2>
<div class="gq-figs">{sbl_cards}</div>
<h2>30 scrapbook layout ideas</h2>
{sbl_ideas}
<h2>Design tips that make any page look better</h2>
<ul><li><strong>One star:</strong> make one photo bigger or matted so the eye knows where to land first.</li>
<li><strong>Odd numbers:</strong> groups of 3 or 5 (photos, stickers, flowers) look more natural than pairs.</li>
<li><strong>Visual triangle:</strong> repeat one colour or embellishment in three spots forming a triangle; the eye travels round the page.</li>
<li><strong>Even gaps:</strong> keep the same space (about 1/4 in) between photos. Grids look neat even with mixed photos.</li>
<li><strong>Leave space:</strong> white space isn't wasted. A page with room to breathe looks calmer and more modern.</li>
<li><strong>Photos first:</strong> choose papers to suit the photos, not the other way round, and keep busy patterns away from busy photos.</li></ul>
<h2>What size photos for a scrapbook?</h2>
<p>Standard 4 x 6 in prints suit 12 x 12 pages (you can fit up to 6 with a little trimming). For 8.5 x 11 and 8 x 8 pages, 3 x 4 in and 4 x 4 in prints fit better, and 6 x 8 albums suit 3 x 4 in or wallet prints. Our <a href="{href("scrapbook-page-sizes.html")}">scrapbook page sizes</a> calculator shows exactly how many photos fit each page. The sketch generator above gives the trimmed size of every photo, so you can crop them before printing.</p>
<h2>Scrapbook or junk journal?</h2>
<p>A scrapbook is built around photos, laid out neatly on flat pages in an album. A junk journal is a hand-bound book stuffed with ephemera, pockets and found paper. Many people do both. Our <a href="{href("junk-journal-vs-scrapbook.html")}">junk journal vs scrapbook</a> guide compares them, and <a href="{href("junk-journal-page-ideas.html")}">junk journal page ideas</a> has 42 more layouts if you like the looser style. Journaling stuck? Try our <a href="{href("journal-prompts.html")}">journal prompts</a>.</p>
<p class="note">Ideas, sketches and drawings are our own. Design principles (focal photo, odd-number groupings, visual triangle, white space) are standard scrapbooking practice, checked against Hobbycraft, Altenew and LoveCrafts' beginner guides (28 Nov 2026). Photo sizes are trimmed sizes for the sketch; print a little bigger and crop.</p>
</div></div></section>'''
sbl_faq = [
    ("What is the easiest scrapbook layout for beginners?", "A single matted photo with a title, or a grid of equal photos with even gaps. Both look neat with very little planning."),
    ("How many photos should be on a scrapbook page?", "One to five is easiest. One large photo makes a striking page; 3 to 5 tell a story. A 12 x 12 page fits up to six 4 x 6 in prints with some trimming."),
    ("What do you put on a scrapbook page?", "A background paper, your photos (matted if you like), a title, a few lines of journaling about who, where and what happened, and a few embellishments such as stickers, die-cuts or washi tape."),
    ("What is a scrapbook sketch?", "A simple plan of a page showing where the photos, title, journaling and embellishments go. You follow it with your own photos and papers, so you don't start from a blank page."),
    ("What size photos are best for scrapbooking?", "4 x 6 in prints for 12 x 12 pages; 3 x 4 in or 4 x 4 in prints for 8.5 x 11 and 8 x 8 pages; 3 x 4 in or wallet prints for 6 x 8 albums."),
    ("How do I make my scrapbook pages look good?", "Pick one focal photo, use papers that share a colour with the photos, keep even gaps, group embellishments in threes in a triangle, and leave some white space."),
]
SHOP_FOR["scrapbook-layout-ideas.html"] = ["journaling-cards-3x4", "vintage-ephemera-pack", "december-days-journal-kit", "junk-journal-mega-bundle"]
page("scrapbook-layout-ideas.html", "Scrapbook Layout Ideas for Beginners (+ Sketch Generator)",
     "30 easy scrapbook layout ideas for beginners, six drawn steps and a free sketch generator with exact photo and mat sizes for 12x12 and 8.5x11 pages.",
     sbl, sbl_faq, "Scrapbook layout ideas", app_name="Scrapbook layout sketch generator")
