# ---------------- 28 Nov 2026 run 21: HOW TO KNIT MITTENS + CROCHET CHRISTMAS TREE PATTERN + JUNK JOURNAL TAGS ----------------
# Executed from build.py after plan20.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 28 Nov run 21). Patterns, drawings and wording our own. JS in assets/app.js (mkm-*, cct-*, jjt-*).


# ======== HOW TO KNIT MITTENS (pattern writer) ========
# Demand: 'how to knit mittens for beginners' (SERP 28 Nov: Yarnspirations beginner series, Instructables, Skillshare, PopSci, Nimble Needles,
# Marly Bird bootcamp x2, Handy Little Me, Gathered, Simply Knitting, Ravelry x3, leeleeknits; 'mitten size chart cast on' SERP: Ravelry, Knitty,
# Purl Soho, Pacific Knit Co; no size-to-pattern writer). Construction: rib cuff, thumb gusset (2 sts every 3rd round), band top decreases.
# Hand sizes are typical figures (measure the hand); gauge mid values from the Craft Yarn Council ranges, knitted a little firm for mittens.

def _mkm_svg(step, label):
    Y, Y2 = "#2f8f8a", "#5fb3ad"
    hand = (f'<path d="M100 170 v-60 q0 -46 40 -46 q40 0 40 46 v60 z" fill="{Y}" stroke="{_INK}" stroke-width="2"/>')
    cuff = "".join(f'<path d="M{104 + i * 8} 172 v-26" stroke="{Y2}" stroke-width="4"/>' for i in range(10))
    if step == 1:
        s = (f'<rect x="96" y="120" width="88" height="52" rx="4" fill="{Y}" stroke="{_INK}" stroke-width="2"/>' + cuff.replace("v-26", "v-48")
             + f'<path d="M70 120 h140" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="6 4"/><text x="140" y="104" {_T12} text-anchor="middle">cast on, join in the round</text><text x="140" y="190" {_T12} text-anchor="middle">k2, p2 rib for the cuff</text>')
    elif step == 2:
        s = (f'<path d="M100 172 v-70 h80 v70 z" fill="{Y}" stroke="{_INK}" stroke-width="2"/>' + cuff
             + f'<path d="M100 140 l-26 -40 h26 z" fill="{_GOLD}" stroke="{_INK}" stroke-width="2"/>'
             + f'<text x="54" y="92" {_T12}>thumb gusset</text><text x="140" y="190" {_T12} text-anchor="middle">increase 2 sts every 3rd round</text>')
    elif step == 3:
        s = (f'<path d="M100 172 v-80 h80 v80 z" fill="{Y}" stroke="{_INK}" stroke-width="2"/>' + cuff
             + f'<path d="M100 132 q-30 -10 -36 -34" fill="none" stroke="{_BERRY}" stroke-width="5"/><circle cx="62" cy="94" r="5" fill="{_BERRY}"/>'
             + f'<text x="40" y="80" {_T12}>waste yarn</text><text x="140" y="190" {_T12} text-anchor="middle">thumb stitches on hold, carry on</text>')
    elif step == 4:
        s = (hand + cuff + f'<path d="M100 132 q-22 -6 -24 -24" fill="none" stroke="{_BERRY}" stroke-width="5"/>'
             + f'<path d="M190 70 v70" stroke="{_GOLD}" stroke-width="2"/><path d="M186 70 h8 M186 140 h8" stroke="{_GOLD}" stroke-width="2"/>'
             + f'<text x="198" y="108" {_T12}>to the little</text><text x="198" y="122" {_T12}>fingertip</text><text x="140" y="190" {_T12} text-anchor="middle">knit the hand straight</text>')
    elif step == 5:
        s = (hand + cuff + "".join(f'<path d="M{106 + i * 2} {104 - i * 7} l6 -2" stroke="{_GOLD}" stroke-width="3"/><path d="M{174 - i * 2} {104 - i * 7} l-6 -2" stroke="{_GOLD}" stroke-width="3"/>' for i in range(5))
             + f'<text x="140" y="190" {_T12} text-anchor="middle">decrease at both sides, then close the top</text>')
    else:
        s = (hand + cuff + f'<path d="M100 132 q-34 -4 -36 -40 q0 -14 12 -14 q14 0 24 30 z" fill="{Y}" stroke="{_INK}" stroke-width="2"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">pick up the thumb, knit it, weave in</text>')
    return _svg12(s, label)


MKM_STEPS = [(1, "1. Cast on and knit the cuff", "Cast on the number the writer gives onto double-pointed needles or a long circular for magic loop. Join in the round without twisting and work k2, p2 rib (or k1, p1) for the cuff."),
             (2, "2. Grow the thumb gusset", "Place a marker, make 1 stitch, place another marker. Every third round, increase just inside both markers. The triangle of stitches between them makes room for the thumb."),
             (3, "3. Put the thumb on hold", "When the gusset has enough stitches, slip them onto a piece of waste yarn. Cast on 1 stitch over the gap and keep knitting the hand in the round."),
             (4, "4. Knit the hand", "Knit every round until the mitten reaches the tip of your little finger when you try it on. Most of the length is here, so check it on the hand."),
             (5, "5. Shape the top", "Split the stitches into back and palm halves. Decrease 2 stitches at each side (4 a round), every other round and then every round, until a few are left. Draw the yarn through them."),
             (6, "6. Knit the thumb", "Put the held stitches back on needles, pick up 2 stitches from the gap, and knit the thumb to the right length. Decrease twice and draw the yarn through. Weave in the ends.")]
mkm_cards = "".join(f'<figure class="gq-fig"><div>{_mkm_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in MKM_STEPS)

MKM_SIZES = [("0", "Toddler (2 to 4 years)", "5.5", "4.75"), ("1", "Child (4 to 6)", "6", "5.25"), ("2", "Child (6 to 8)", "6.5", "5.75"),
             ("3", "Child 8 to 10 / women's S", "7", "6.5"), ("4", "Women's M", "7.5", "7"), ("5", "Women's L / men's S", "8", "7.25"),
             ("6", "Men's M", "8.5", "7.75"), ("7", "Men's L", "9", "8")]
mkm_opts = "".join(f'<option value="{k}"{" selected" if k == "4" else ""}>{e(n)} ({c} in hand)</option>' for k, n, c, _ in MKM_SIZES) + '<option value="m">My own measurements</option>'
mkm_rows = "".join(f'<tr><td>{e(n)}</td><td>{c} in ({round(float(c) * 2.54, 1)} cm)</td><td>{L} in ({round(float(L) * 2.54, 1)} cm)</td></tr>' for _, n, c, L in MKM_SIZES)

mkm = top("How to knit mittens (easy pattern for any size)", "Mittens are a hat-sized project with one extra trick: the thumb. This beginner guide shows each step in drawings, and the pattern writer gives your cast-on, every gusset increase, the hand length and the top decreases for any size and yarn.", "How to knit mittens") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to knit mittens, cast on about as many stitches as your hand circumference times your gauge (36 stitches for a women's medium in worsted), join in the round and knit a <strong>2.5 in rib cuff</strong>. Then make a <strong>thumb gusset</strong> by increasing 2 stitches every third round, put those stitches on waste yarn, and knit the hand straight until it reaches the tip of your little finger. <strong>Decrease 4 stitches a round</strong> to close the top, then pick up the thumb stitches and knit the thumb. A pair of adult worsted mittens takes roughly 140 to 200 yards.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Mitten pattern writer</h3>
<div class="row2"><div class="field"><label for="mkm-z">Size</label><select id="mkm-z">{mkm_opts}</select></div>
<div class="field" id="mkm-own" hidden><label for="mkm-c">Hand around x wrist to fingertip (in)</label><div class="row2"><input type="number" id="mkm-c" value="7.5" min="4" max="11" step="0.25" inputmode="decimal" aria-label="Hand circumference in inches"><input type="number" id="mkm-l" value="7" min="3.5" max="9.5" step="0.25" inputmode="decimal" aria-label="Wrist to fingertip length in inches"></div></div></div>
<div class="row2"><div class="field"><label for="mkm-y">Yarn</label><select id="mkm-y"><option value="3">DK / light (3)</option><option value="4" selected>Worsted / aran (4)</option><option value="5">Chunky / bulky (5)</option></select></div>
<div class="field"><label for="mkm-g">Your swatch: stitches per 4 in (optional)</label><input type="number" id="mkm-g" placeholder="leave blank for a typical firm gauge" min="8" max="36" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="mkm-r">Cuff</label><select id="mkm-r"><option value="2" selected>k2, p2 rib</option><option value="1">k1, p1 rib</option></select></div>
<div class="field"><label for="mkm-k">Cuff length</label><select id="mkm-k"><option value="std" selected>Standard</option><option value="long">Long (tuck into sleeves)</option></select></div></div>
</div><div class="result" aria-live="polite" id="mkm-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to knit mittens, step by step</h2>
<div class="gq-figs">{mkm_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> wool or a wool blend is warmest and stays warm when damp. Worsted (4) is the easiest to start with. Pick a smooth, light colour so you can see your stitches.</li>
<li><strong>Needles:</strong> a set of double-pointed needles (dpns) or one long circular needle (32 in / 80 cm) for the magic loop, one size smaller than the yarn label suggests so the fabric is dense and windproof. About 4 to 4.5 mm (US 6 to 7) for worsted.</li>
<li><strong>Also:</strong> 2 stitch markers, a piece of smooth waste yarn, scissors and a tapestry needle.</li></ul>
<p>New to knitting in the round? See <a href="{href("how-to-knit-in-the-round.html")}">how to knit in the round</a> and <a href="{href("how-to-increase-knitting.html")}">how to increase</a> (the gusset uses M1L and M1R) before you start. The <a href="{href("how-to-pick-up-stitches-knitting.html")}">pick up stitches</a> guide helps at the thumb.</p>
<h2>Mitten size chart</h2>
<p>Measure round the widest part of the hand, over the knuckles, without the thumb. Then measure from the wrist crease to the tip of the middle finger. These are typical measurements; a quick tape measure beats any chart.</p>
<div class="tbl"><table class="mt"><thead><tr><th>Size</th><th>Hand around</th><th>Wrist to fingertip</th></tr></thead><tbody>{mkm_rows}</tbody></table></div>
<p>Mittens are knitted with little or no ease: the same size as the hand, or a touch bigger. A snug mitten is warmer; too loose and the cold gets in at the cuff.</p>
<h2>How the thumb gusset works</h2>
<p>Your hand is wider across the base of the thumb than at the wrist. A gusset is a little triangle of extra stitches that grows from the cuff to the thumb joint. You make it by increasing 2 stitches every third round between two markers. When it holds about a third of the hand stitches, those stitches go on waste yarn and become the thumb later. A mitten without a gusset (a straight "peasant thumb") is quicker but pulls across the palm.</p>
<h2>Fixing holes at the thumb</h2>
<p>The gap where the thumb meets the hand is the one place mittens get holes. Pick up 2 stitches (or even 3) from the gap instead of 1, and on the next round knit 2 of them together. Pull the first stitch on each needle snug. Any small hole left can be closed with the tail when you weave in the ends: see <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>.</p>
<h2>Flat mittens (two needles)</h2>
<p>If you don't want to knit in the round yet, you can knit mittens flat on two straight needles and sew them up the side. Use the same stitch counts plus 2 for the seam, work the gusset on one side of the piece, and seam with mattress stitch. Round mittens have no seam to rub, which is why most patterns use them.</p>
<h2>Making a pair</h2>
<p>Write the round count when you start the gusset and when you finish the hand on the first mitten. Our <a href="{href("row-counter.html")}">row counter</a> keeps track. The two mittens in this pattern are the same, so you can wear them on either hand. Want matching gifts? Add a <a href="{href("how-to-knit-a-hat.html")}">knitted hat</a> and <a href="{href("how-to-knit-a-scarf.html")}">scarf</a> from the same yarn.</p>
<p class="note">Pattern, drawings and wording are our own, using standard top-down-from-cuff mitten construction (rib cuff, M1 thumb gusset every third round, band decreases), checked against Yarnspirations, Gathered and Handy Little Me beginner mittens (28 Nov 2026). Hand sizes are typical figures. Gauges are firm versions of the Craft Yarn Council ranges; round counts, lengths and yardage are estimates, so try the mitten on as you go.</p>
</div></div></section>'''
mkm_faq = [
    ("Are mittens easy to knit for beginners?", "Yes, if you can knit, purl, knit in the round and make an increase. Mittens are small, so they're quick, and the thumb gusset is the only new skill."),
    ("How many stitches do I cast on for mittens?", "Multiply your hand circumference by your stitches per inch and round to a multiple of 4. A women's medium hand (7.5 in) in worsted at 5 stitches per inch needs about 36 to 40 stitches."),
    ("How much yarn do I need for mittens?", "A pair of adult mittens in worsted takes roughly 140 to 200 yards; children's mittens 70 to 120 yards. Long cuffs and chunky yarn use more. The writer above estimates it for your size."),
    ("What needles are best for knitting mittens?", "Double-pointed needles or a long circular needle used for the magic loop, one size smaller than the yarn label suggests, so the mitten is dense and warm."),
    ("Can you knit mittens on straight needles?", "Yes. Knit the mitten flat with 2 extra stitches for the seam, shape the thumb on one edge, and sew it up the side with mattress stitch."),
    ("How long should a mitten be?", "From the wrist, the hand part should reach the tip of the little finger before the top decreases start. With the decreases, the mitten covers the fingertips with a little room to spare."),
]
SHOP_FOR["how-to-knit-mittens.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-planner-budget", "christmas-gift-tags"]
page("how-to-knit-mittens.html", "How to Knit Mittens for Beginners (Pattern Writer)",
     "How to knit mittens for beginners: six drawn steps, a mitten size chart and a free pattern writer for any size and yarn, from the cuff to the thumb.",
     mkm, mkm_faq, "How to knit mittens", app_name="Mitten pattern writer")


# ======== FREE CROCHET CHRISTMAS TREE PATTERN (amigurumi cone, any height) ========
# Demand: 'how to crochet a christmas tree easy free pattern' (SERP 28 Nov: Ravelry x9 listings, Craftaholic Witch, Craft Passion, Gathered tree
# decoration, FaveCrafts tabletop tree, Pocket Yarnlings ornament, Bella Coco, amigurumi.com; no size writer). Construction: sc cone worked from the
# tip with increases spread evenly, flat sc base circle joined to the cone, stuffed. Gauge, yardage and hours are our estimates (tight amigurumi sc).

def _cct_svg(step, label):
    G, G2 = "#2f7d4f", "#4fa36e"
    cone = f'<path d="M140 30 L86 150 Q140 166 194 150 Z" fill="{G}" stroke="{_INK}" stroke-width="2"/>'
    rings = "".join(f'<path d="M{140 - (k * 9)} {30 + k * 20} Q140 {34 + k * 21} {140 + k * 9} {30 + k * 20}" fill="none" stroke="{G2}" stroke-width="2"/>' for k in range(1, 6))
    if step == 1:
        s = (f'<circle cx="140" cy="90" r="16" fill="none" stroke="{G}" stroke-width="6"/>' + "".join(f'<path d="M{140 + 16 * c:.1f} {90 + 16 * d:.1f} l0 -8" stroke="{_INK}" stroke-width="2"/>' for c, d in ((1, 0), (0, 1), (-1, 0), (0, -1)))
             + f'<text x="140" y="150" {_T12} text-anchor="middle">4 sc in a magic ring: the tip</text>')
    elif step == 2:
        s = (f'<path d="M140 40 L104 130 Q140 140 176 130 Z" fill="{G}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<circle cx="{120 + i * 10}" cy="{100 + (i % 2) * 14}" r="3.5" fill="{_GOLD}"/>' for i in range(5))
             + f'<text x="140" y="166" {_T12} text-anchor="middle">a few increases each round,</text><text x="140" y="182" {_T12} text-anchor="middle">spread out: the cone grows</text>')
    elif step == 3:
        s = (cone + rings + f'<path d="M206 30 v120" stroke="{_GOLD}" stroke-width="2"/><path d="M202 30 h8 M202 150 h8" stroke="{_GOLD}" stroke-width="2"/>'
             + f'<text x="140" y="188" {_T12} text-anchor="middle">keep going to your height</text>')
    elif step == 4:
        s = ("".join(f'<circle cx="140" cy="96" r="{r}" fill="none" stroke="{c}" stroke-width="8"/>' for r, c in ((10, G), (20, G2), (30, G), (40, G2), (50, G)))
             + f'<text x="140" y="172" {_T12} text-anchor="middle">a flat circle with the same</text><text x="140" y="188" {_T12} text-anchor="middle">stitch count for the base</text>')
    elif step == 5:
        s = (cone + rings + f'<ellipse cx="140" cy="156" rx="54" ry="10" fill="{G2}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<circle cx="{120 + i * 10}" cy="{100 + (i % 2) * 8}" r="2" fill="#fff"/>' for i in range(5))
             + f'<text x="140" y="188" {_T12} text-anchor="middle">stuff firmly, sc the base on</text>')
    else:
        s = (cone + rings + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}" stroke="{_INK}" stroke-width="1"/>' for x, y, c in ((122, 80, _BERRY), (156, 96, _GOLD), (110, 120, _GOLD), (148, 132, _BERRY), (170, 140, "#f6f1e6"), (132, 58, "#f6f1e6")))
             + f'<path d="M140 12 l5 10 l11 1 l-8 7 l3 11 l-11 -6 l-11 6 l3 -11 l-8 -7 l11 -1 z" fill="{_GOLD}" stroke="{_INK}" stroke-width="1.5"/>'
             + f'<text x="140" y="188" {_T12} text-anchor="middle">add a star, baubles and a trunk</text>')
    return _svg12(s, label)


CCT_STEPS = [(1, "1. Start at the tip", "Make a magic ring and work 4 single crochet into it. Pull it tight. Mark the first stitch: you'll work in a spiral without joining, moving the marker up each round."),
             (2, "2. Grow the cone slowly", "Increase a few stitches each round, spread around the cone. Fewer increases make a tall, slim tree; more make a short, fat one. The writer spaces them for your size."),
             (3, "3. Work to your height", "Keep following the round list until the cone is as tall as you want. Tick off each round so you don't lose your place on the plain ones."),
             (4, "4. Make the base", "Crochet a flat circle with the same number of stitches as the last round of the cone. Cut a card circle the same size if you want a tree that stands very flat."),
             (5, "5. Stuff and join", "Stuff the cone firmly, right into the tip. Hold the base under it and single crochet through both edges all the way round, adding the last stuffing before you close it."),
             (6, "6. Decorate", "Sew on a star topper, beads, pom poms or French knot baubles. Add a little trunk, or a loop at the tip to hang a small tree as an ornament.")]
cct_cards = "".join(f'<figure class="gq-fig"><div>{_cct_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CCT_STEPS)

cct = top("Free crochet Christmas tree pattern (any size)", "A crochet Christmas tree is a stuffed cone with a flat base: easy single crochet in a spiral, a handful of increases and some decorating. This free beginner pattern writes every round for any height, from a 3 in tree ornament to a 10 in tabletop tree, with a star topper, trunk and yarn amounts.", "Crochet Christmas tree pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet a Christmas tree, start at the tip with <strong>4 single crochet in a magic ring</strong> and work in a spiral, adding a few increases spread round each round so the piece grows into a <strong>cone</strong>. At the height you want, crochet a <strong>flat circle</strong> with the same stitch count, stuff the cone and single crochet the base on. A 5 in tree takes roughly 40 to 60 yards of worsted yarn and a 4 mm hook, and about 1.5 to 3 hours, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Christmas tree pattern writer</h3>
<div class="row2"><div class="field"><label for="cct-z">Height</label><select id="cct-z"><option value="3">Ornament (3 in)</option><option value="5" selected>Small (5 in)</option><option value="7">Medium (7 in)</option><option value="10">Tabletop (10 in)</option><option value="m">My own height</option></select></div>
<div class="field" id="cct-own" hidden><label for="cct-h">Height (in)</label><input type="number" id="cct-h" value="6" min="2" max="16" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="cct-s">Shape</label><select id="cct-s"><option value="0.45">Slim</option><option value="0.6" selected>Classic</option><option value="0.78">Short and round</option></select></div>
<div class="field"><label for="cct-y">Yarn</label><select id="cct-y"><option value="3">DK (3), 3.5 mm hook</option><option value="4" selected>Worsted (4), 4 mm hook</option><option value="5">Chunky (5), 5 mm hook</option><option value="6">Velvet / chenille (6), 6 mm hook</option></select></div></div>
<div class="row2"><div class="field"><label for="cct-x">Extras</label><select id="cct-x"><option value="star" selected>Star topper</option><option value="both">Star topper and trunk</option><option value="loop">Hanging loop (ornament)</option><option value="none">None</option></select></div>
<div class="field"><label for="cct-t">Terms</label><select id="cct-t"><option value="us" selected>US (sc)</option><option value="uk">UK (dc)</option></select></div></div>
</div><div class="result" aria-live="polite" id="cct-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a Christmas tree, step by step</h2>
<div class="gq-figs">{cct_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> green worsted acrylic or cotton is easiest to see your stitches in. Velvet or chenille yarn makes the soft, fuzzy trees that are popular this year, but it's harder to count, so use stitch markers often.</li>
<li><strong>Hook:</strong> one or two sizes smaller than the yarn label suggests, so the stuffing doesn't show through: about 4 mm (G-6) for worsted.</li>
<li><strong>Also:</strong> toy stuffing (polyester fibrefill), a stitch marker, a tapestry needle, and a scrap of yellow or gold yarn for the star. A circle of card or a few flat pebbles in a little bag in the base helps a big tree stand.</li></ul>
<p>Need a refresher? See the <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>, <a href="{href("how-to-crochet-increase.html")}">how to increase</a> and our <a href="{href("amigurumi.html")}">amigurumi basics</a>.</p>
<h2>Star topper</h2>
<p>With yellow yarn, make a magic ring and work 5 sc into it; join with a slip stitch. *Chain 4, slip stitch in the 2nd chain from the hook, sc in the next chain, hdc in the next chain, slip stitch into the next sc of the ring; repeat from * 4 more times. That's 5 points. Fasten off with a long tail and sew the star to the tip of the tree, or use two stars back to back with the tip between them.</p>
<h2>Ways to decorate your tree</h2>
<ul><li><strong>Baubles:</strong> French knots in red and gold, little <a href="{href("how-to-make-a-pom-pom.html")}">pom poms</a>, wooden beads or buttons (not for small children).</li>
<li><strong>Garland:</strong> a long chain in a contrast colour or a strand of metallic yarn, wound in a spiral from top to bottom and tacked in place.</li>
<li><strong>Snowy tips:</strong> work the last 2 rounds of the cone in white, or add a frilly round of 2 dc in each front loop.</li>
<li><strong>Stripes:</strong> change to a second green every few rounds (see <a href="{href("how-to-change-colors-in-crochet.html")}">how to change colours</a>).</li>
<li><strong>Faces:</strong> small <a href="{href("safety-eyes-size-chart.html")}">safety eyes</a> and a stitched smile make a cute amigurumi tree.</li></ul>
<p>Want a companion for your tree? Our <a href="{href("crochet-gnome-pattern.html")}">free crochet gnome pattern</a> writes every round for any size, from a 4 in ornament to an 11 in shelf gnome.</p>
<h2>Make a forest: three sizes from one ball</h2>
<p>Trees look best in groups of three: a 5 in, a 7 in and a 10 in tree in classic shape. Together they take roughly 300 to 400 yards of worsted, about two 100 g balls. They sell well at <a href="{href("christmas-crafts-to-sell.html")}">Christmas craft fairs</a>; price them with our <a href="{href("how-to-price-amigurumi.html")}">amigurumi pricing guide</a>. Our <a href="{href("crochet-christmas-ornament-pattern.html")}">bauble ornament</a> and <a href="{href("crochet-snowflake-pattern.html")}">snowflake</a> patterns go with them.</p>
<p class="note">Pattern, star and drawings are our own, using standard amigurumi cone and flat-circle construction, checked against Craftaholic Witch, Gathered and FaveCrafts' tree patterns (28 Nov 2026). Gauges, round counts, yardage and hours are estimates for tight amigurumi single crochet; measure as you go.</p>
</div></div></section>'''
cct_faq = [
    ("How do you crochet a Christmas tree for beginners?", "Work a cone in single crochet from the tip: 4 sc in a magic ring, then a few increases spread around each round until it's tall enough. Crochet a flat circle with the same stitch count, stuff the cone and sc the base on."),
    ("How much yarn do I need for a crochet Christmas tree?", "Roughly 40 to 60 yards of worsted for a 5 in tree and 170 to 230 yards for a 10 in tree. Velvet yarn trees use fewer yards but a heavier ball. The writer estimates it for your size."),
    ("How do you make a crochet tree stand up?", "Stuff it firmly, put a card circle inside the base before you close it, and for big trees add a small bag of pellets or flat stones at the bottom for weight."),
    ("What yarn is best for crochet Christmas trees?", "Worsted acrylic or cotton is easiest. Velvet or chenille yarn gives a soft, plush look. Use a hook one or two sizes smaller than the label suggests so the stuffing doesn't show."),
    ("How long does it take to crochet a Christmas tree?", "A 3 in ornament takes about an hour, a 5 in tree 1.5 to 3 hours and a 10 in tree 5 to 9 hours, depending on your speed."),
    ("How do I turn a crochet tree into an ornament?", "Make the 3 in size and pull a loop of yarn or ribbon through the tip before you add the star. Leave out beads and buttons if it will hang where small children can reach."),
]
SHOP_FOR["crochet-christmas-tree-pattern.html"] = ["crochet-knitting-pricing-calculator", "christmas-gift-tags", "christmas-gift-planner-budget", "2027-crochet-knitting-planner"]
page("crochet-christmas-tree-pattern.html", "Free Crochet Christmas Tree Pattern: Any Size (Writer)",
     "Free crochet Christmas tree pattern for beginners: a writer gives every round for any height, from a tree ornament to a tabletop tree, with yarn amounts.",
     cct, cct_faq, "Crochet Christmas tree pattern", app_name="Crochet Christmas tree pattern writer")


# ======== JUNK JOURNAL TAGS (how to make + printable tag template maker) ========
# Demand: 'how to make junk journal tags' (SERP 28 Nov: Graphics Fairy x5 (round, autumn, botanical, Christmas tags), Artsy Fartsy Life x2,
# Kim Pepper 35+ ideas + 50 things to turn into tags, brit.co, Book Riot, Artifact Uprising, Sustain My Craft Habit cardboard tags; no template maker).
# Shipping tag sizes #1-#8 are the standard US manila tag sizes (2 3/4 x 1 3/8 in to 6 1/4 x 3 1/8 in).

JJT_SIZES = [("1", "#1", 2.75, 1.375), ("2", "#2", 3.25, 1.625), ("3", "#3", 3.75, 1.875), ("4", "#4", 4.25, 2.125),
             ("5", "#5", 4.75, 2.375), ("6", "#6", 5.25, 2.625), ("7", "#7", 5.75, 2.875), ("8", "#8", 6.25, 3.125)]
jjt_opts = "".join(f'<option value="{k}"{" selected" if k == "5" else ""}>{n} shipping tag ({h} x {w} in)</option>' for k, n, h, w in JJT_SIZES) + '<option value="b">Bookmark tag (6 x 2 in)</option><option value="m">My own size</option>'
jjt_rows = "".join(f'<tr><td>{n}</td><td>{h} x {w} in</td><td>{round(h * 2.54, 1)} x {round(w * 2.54, 1)} cm</td></tr>' for _, n, h, w in JJT_SIZES)


def _jjt_svg(step, label):
    P, K = "#f4dfb8", "#c99a5b"
    tag = f'<path d="M110 40 h60 l16 18 v112 h-92 v-112 z" fill="{P}" stroke="{_INK}" stroke-width="2"/><circle cx="140" cy="60" r="7" fill="#f6f1e6" stroke="{_INK}" stroke-width="1.5"/>'
    if step == 1:
        s = (f'<rect x="60" y="30" width="160" height="140" fill="#fff" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{78 + i * 44} 44 h30 l8 9 v56 h-46 v-56 z" fill="none" stroke="{_BERRY}" stroke-width="1.5" stroke-dasharray="4 3"/>' for i in range(3))
             + f'<text x="140" y="190" {_T12} text-anchor="middle">print the template, or trace a tag</text>')
    elif step == 2:
        s = (tag + f'<path d="M70 150 l60 -100" stroke="{_INK}" stroke-width="3"/><path d="M60 160 l14 -6 l-6 -8 z" fill="{_INK}"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">cut it from card, a cereal box or a file folder</text>')
    elif step == 3:
        s = (tag.replace(P, "#d8b27a") + "".join(f'<circle cx="{120 + (i * 13) % 40}" cy="{90 + (i * 23) % 70}" r="{6 + i % 3 * 3}" fill="#8a5a2b" opacity=".35"/>' for i in range(7))
             + f'<text x="140" y="190" {_T12} text-anchor="middle">age it: tea, coffee or ink</text>')
    elif step == 4:
        s = (tag + f'<rect x="100" y="84" width="80" height="34" fill="#cfe3e0" stroke="{_INK}" stroke-width="1"/><rect x="96" y="128" width="88" height="10" fill="{_BERRY}" opacity=".8"/>'
             + f'<path d="M110 150 h50 M110 158 h40" stroke="{_INK}" stroke-width="1.5"/><text x="140" y="190" {_T12} text-anchor="middle">layer paper, a picture, washi tape</text>')
    elif step == 5:
        s = (tag + f'<circle cx="140" cy="60" r="10" fill="none" stroke="{K}" stroke-width="4"/><path d="M140 60 q-20 -30 -50 -40 M140 60 q16 -34 40 -44" fill="none" stroke="{_BERRY}" stroke-width="3"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">punch the hole, add a reinforcer and ribbon</text>')
    else:
        s = (f'<path d="M60 60 h150 v100 h-150 z" fill="#e9dcc3" stroke="{_INK}" stroke-width="2"/><path d="M60 110 h150" stroke="{_INK}" stroke-width="1" opacity=".4"/>'
             + f'<path d="M150 96 h34 l8 8 v66 h-42 z" fill="{P}" stroke="{_INK}" stroke-width="1.5"/><path d="M140 112 h70 v48 h-70 z" fill="#cfe3e0" stroke="{_INK}" stroke-width="2"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">tuck it in a pocket or tie it to the spine</text>')
    return _svg12(s, label)


JJT_STEPS = [(1, "1. Choose a size and print", "Pick a tag size that fits your pockets (the template maker above checks it). Print the template sheet at 100%, or trace round a shop-bought tag."),
             (2, "2. Cut it out", "Cut the tags from card stock, a cereal box, an old file folder or a manila envelope. Clip the top corners at 45 degrees for the classic shipping tag look."),
             (3, "3. Age it if you like", "Brush with cold tea or coffee, dab with distress ink at the edges, or crumple and flatten for a vintage feel. Let it dry flat under a book."),
             (4, "4. Layer and decorate", "Glue on scrap paper, a picture, a strip of washi tape or lace, a stamp, and a few words. Keep the bottom third plain if you want to journal on it."),
             (5, "5. Punch and tie", "Punch a hole at the top centre, about 1/2 in down. Glue on a reinforcer ring made from a scrap circle, then thread ribbon, twine or seam binding through."),
             (6, "6. Use it in your journal", "Tuck it into a pocket, clip it to a page, tie it to the spine or sew it into a signature. Write on the back: tags make a hidden place for journaling.")]
jjt_cards = "".join(f'<figure class="gq-fig"><div>{_jjt_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in JJT_STEPS)

jjt = top("How to make junk journal tags (free printable template)", "Tags are the easiest junk journal embellishment: a scrap of card, a hole and a ribbon. This guide shows six simple steps, 30 tag ideas, the standard tag sizes, and a free template maker that prints a full sheet of tags in your size and shape.", "Junk journal tags") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to make junk journal tags, <strong>cut a rectangle of card</strong> (a #5 shipping tag is 4 3/4 x 2 3/8 in), <strong>clip the two top corners</strong> at 45 degrees, and <strong>punch a hole</strong> about 1/2 in from the top. Age it with tea or ink if you like, layer on scraps, a picture or washi tape, and tie ribbon or twine through the hole. Make tags about 1/4 to 1/2 in narrower and 1/2 to 1 in taller than the pocket they'll sit in, so the top and ribbon stick out.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Printable tag template maker</h3>
<div class="row2"><div class="field"><label for="jjt-z">Tag size</label><select id="jjt-z">{jjt_opts}</select></div>
<div class="field" id="jjt-own" hidden><label for="jjt-h">Height x width (in)</label><div class="row2"><input type="number" id="jjt-h" value="4" min="1.5" max="10" step="0.125" inputmode="decimal" aria-label="Tag height in inches"><input type="number" id="jjt-w" value="2" min="1" max="7" step="0.125" inputmode="decimal" aria-label="Tag width in inches"></div></div></div>
<div class="row2"><div class="field"><label for="jjt-s">Shape</label><select id="jjt-s"><option value="clip" selected>Classic (clipped corners)</option><option value="round">Rounded corners</option><option value="arch">Arched top</option><option value="flag">Flag bottom (notch)</option><option value="rect">Plain rectangle</option></select></div>
<div class="field"><label for="jjt-p">Paper</label><select id="jjt-p"><option value="letter" selected>US Letter (8.5 x 11 in)</option><option value="a4">A4 (210 x 297 mm)</option></select></div></div>
<div class="row2"><div class="field"><label for="jjt-k">Pocket it goes in (optional, width x height in)</label><div class="row2"><input type="number" id="jjt-pw" placeholder="width" min="1" max="12" step="0.125" inputmode="decimal" aria-label="Pocket width in inches"><input type="number" id="jjt-ph" placeholder="height" min="1" max="14" step="0.125" inputmode="decimal" aria-label="Pocket height in inches"></div></div>
<div class="field"><label for="jjt-l">Inside the tag</label><select id="jjt-l"><option value="none" selected>Blank</option><option value="lines">Journaling lines</option><option value="frame">Inner frame</option></select></div></div>
</div><div class="result" aria-live="polite" id="jjt-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to make junk journal tags, step by step</h2>
<div class="gq-figs">{jjt_cards}</div>
<h2>Standard tag sizes</h2>
<p>Shop-bought manila shipping tags come in numbered sizes. Number 5 is the most popular for journals; number 8 makes a big journaling tag. Our template maker uses the same sizes, so your homemade tags will match bought ones.</p>
<div class="tbl"><table class="mt"><thead><tr><th>Tag</th><th>Size (inches)</th><th>Size (cm)</th></tr></thead><tbody>{jjt_rows}</tbody></table></div>
<h2>30 junk journal tag ideas</h2>
<ul><li><strong>Paper:</strong> book pages, sheet music, old maps, envelopes, receipts, tea bag wrappers, ledger paper, seed packets, paper doilies, gift wrap.</li>
<li><strong>Layers:</strong> a strip of washi tape across the middle, a scrap of lace, a torn edge of patterned paper, a stamped image, a vintage picture from our <a href="{href("junk-journal-ephemera-ideas.html")}">ephemera ideas</a>, a pressed flower under tape.</li>
<li><strong>Finishes:</strong> tea or coffee stain (see <a href="{href("how-to-tea-stain-paper.html")}">how to tea stain paper</a>), inked edges, a sewn zigzag border, a wax seal, a metal eyelet, crinkled seam binding.</li>
<li><strong>Uses:</strong> a pocket insert, a bookmark tied to the spine, a hidden journaling spot, a dated memory tag, a list of the month's favourite things, a quote, a gift tag that becomes a page.</li>
<li><strong>Seasonal:</strong> Christmas tags with gold ink and a sprig of greenery, autumn leaves, Valentine hearts in red tissue, spring botanicals.</li></ul>
<h2>Pockets and tags together</h2>
<p>Most tags live in pockets. Make the tag about 1/4 to 1/2 in narrower than the pocket so it slides in easily, and 1/2 to 1 in taller than the pocket, so the top with the hole and ribbon sticks out where you can grab it. Enter your pocket size above and the maker tells you if the tag fits. For pocket shapes and sizes, see <a href="{href("junk-journal-pockets.html")}">junk journal pockets</a>, and for more page layouts <a href="{href("junk-journal-page-ideas.html")}">junk journal page ideas</a>.</p>
<h2>What card to use</h2>
<p>Use card stock of about 65 to 110 lb (176 to 300 gsm), so tags hold their shape in a pocket. Free options work just as well: cereal and cracker boxes (glue paper over the printed side), file folders, old greeting cards and manila envelopes. Thin paper tags are fine for layers, but back them with card. New to all this? Start with our <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a> guide and <a href="{href("junk-journal-supply-checklist.html")}">supply checklist</a>.</p>
<p class="note">Tag ideas, template maker and drawings are our own. Tag sizes are the standard numbered US manila shipping tag sizes. Methods checked against The Graphics Fairy, Kim Pepper and Artsy Fartsy Life's tag tutorials (28 Nov 2026). Print at 100% and check one tag with a ruler.</p>
</div></div></section>'''
jjt_faq = [
    ("How do you make tags for a junk journal?", "Cut a rectangle of card, clip the two top corners, and punch a hole about 1/2 in from the top. Age or decorate it with paper scraps, pictures and washi tape, then tie ribbon or twine through the hole."),
    ("What size are junk journal tags?", "Most are shipping tag size #3 to #5 (3 3/4 x 1 7/8 in to 4 3/4 x 2 3/8 in). A #8 tag (6 1/4 x 3 1/8 in) makes a large journaling tag. Make tags about 1/4 to 1/2 in narrower and 1/2 to 1 in taller than the pocket they go in."),
    ("What paper is best for junk journal tags?", "Card stock of about 65 to 110 lb (176 to 300 gsm), or free card like cereal boxes, file folders and old greeting cards. Thin paper works for layers on top."),
    ("What do you put on junk journal tags?", "Scraps of book pages, sheet music or patterned paper, a vintage picture, washi tape, lace, stamps and a few handwritten words. The back is a good hidden spot for journaling."),
    ("Can I print junk journal tags?", "Yes. The template maker above prints a full sheet of tags on US Letter or A4 paper in your size and shape. Print at 100% and cut along the lines."),
    ("How do you age junk journal tags?", "Brush them with cold tea or coffee, dab distress ink round the edges, or crumple the card and flatten it again. Let them dry flat under a heavy book."),
]
SHOP_FOR["junk-journal-tags.html"] = ["vintage-ephemera-pack", "journaling-cards-3x4", "winter-cottage-junk-journal-kit", "junk-journal-mega-bundle"]
page("junk-journal-tags.html", "How to Make Junk Journal Tags (Free Printable Template)",
     "How to make junk journal tags: six drawn steps, 30 tag ideas, standard tag sizes and a free template maker that prints a sheet of tags in your size.",
     jjt, jjt_faq, "Junk journal tags", app_name="Junk journal tag template maker")
