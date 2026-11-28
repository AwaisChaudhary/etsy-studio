# ---------------- 28 Nov 2026 run 22: CROCHET GNOME PATTERN + HOW TO EMBROIDER LETTERS + HOW TO SEW A CHRISTMAS STOCKING ----------------
# Executed from build.py after plan21.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13, STK from stockread.py).
# Demand evidence in DEMAND.md (RADAR 28 Nov run 22). Patterns, drawings and wording our own. JS in assets/app.js (gnm-*, eml-*, sws-*).


# ======== FREE CROCHET GNOME PATTERN (amigurumi, any size) ========
# Demand: 'free crochet gnome pattern easy beginner christmas' (SERP 28 Nov: Hanjan Crochet, Red Ted Art x2, Gathered x2 (Hannah Cross gnomes),
# Love Life Yarn, MJ's Off The Hook mini gnome, Bella Coco gnome decoration, crazypatterns advent gnome, Ribblr, Ravelry x7 listings; no size writer).
# Construction: standard amigurumi. Flat-bottomed body (circle, BLO round, straight rounds, closing decreases), cone hat from the tip, ball nose,
# triangle beard (plain or with fringe). Gauges, round counts, yarn and hours are our estimates for tight amigurumi single crochet.

def _gnm_svg(step, label):
    R, Gy, Bd, Ns = "#b8323f", "#8c93a6", "#f2ede2", "#e8a58a"
    body = f'<path d="M102 160 v-46 q0 -30 38 -30 q38 0 38 30 v46 z" fill="{Gy}" stroke="{_INK}" stroke-width="2"/>'
    hat = f'<path d="M96 112 Q140 98 184 112 L150 30 Q144 20 136 28 Z" fill="{R}" stroke="{_INK}" stroke-width="2"/>'
    beard = f'<path d="M112 116 Q140 124 168 116 Q160 160 140 172 Q120 160 112 116 Z" fill="{Bd}" stroke="{_INK}" stroke-width="2"/>'
    if step == 1:
        s = ("".join(f'<circle cx="140" cy="96" r="{r}" fill="none" stroke="{c}" stroke-width="8"/>' for r, c in ((10, Gy), (20, "#a7adbd"), (30, Gy), (40, "#a7adbd"), (50, Gy)))
             + f'<text x="140" y="172" {_T12} text-anchor="middle">a flat circle for the base</text><text x="140" y="188" {_T12} text-anchor="middle">(6 increases every round)</text>')
    elif step == 2:
        s = (f'<path d="M100 160 v-60 h80 v60 z" fill="{Gy}" stroke="{_INK}" stroke-width="2"/><path d="M100 150 h80" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="5 4"/>'
             + f'<text x="196" y="154" {_T12}>back loops</text><text x="140" y="186" {_T12} text-anchor="middle">1 round in back loops, then straight</text>')
    elif step == 3:
        s = (body + "".join(f'<circle cx="{124 + i * 8}" cy="{98 + (i % 2) * 6}" r="3" fill="#fff"/>' for i in range(5))
             + f'<text x="140" y="186" {_T12} text-anchor="middle">stuff, decrease to close the top</text>')
    elif step == 4:
        s = (f'<path d="M100 150 Q140 136 180 150 L148 40 Q142 28 134 38 Z" fill="{R}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{140 - k * 7} {48 + k * 20} Q140 {52 + k * 21} {140 + k * 7} {48 + k * 20}" fill="none" stroke="#d65561" stroke-width="2"/>' for k in range(1, 5))
             + f'<text x="140" y="180" {_T12} text-anchor="middle">a cone from the tip: the hat</text>')
    elif step == 5:
        s = (f'<path d="M70 70 Q120 82 170 70 Q150 150 120 166 Q90 150 70 70 Z" fill="{Bd}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{80 + i * 9} {78 + (i % 3) * 2} q{-2 + i % 3} 40 {2 + i % 2} 70" fill="none" stroke="#d8d1c1" stroke-width="2"/>' for i in range(10))
             + f'<circle cx="214" cy="96" r="24" fill="{Ns}" stroke="{_INK}" stroke-width="2"/>'
             + f'<text x="120" y="190" {_T12} text-anchor="middle">beard</text><text x="214" y="140" {_T12} text-anchor="middle">nose</text>')
    else:
        s = (body + beard + hat + f'<circle cx="140" cy="116" r="11" fill="{Ns}" stroke="{_INK}" stroke-width="2"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">sew on beard, nose, then the hat</text>')
    return _svg12(s, label)


GNM_STEPS = [(1, "1. Crochet the base", "Make a magic ring with 6 single crochet, then increase 6 stitches every round until the circle is as wide as the writer says. This is the flat bottom that lets the gnome stand."),
             (2, "2. Build the body", "Work one round in the back loops only. It makes a neat edge where the base turns into the sides. Then single crochet round and round with no increases."),
             (3, "3. Stuff and close", "Decrease 6 stitches every round to make a rounded top, stuffing firmly as you go. Close the last few stitches. The hat will cover all of this."),
             (4, "4. Make the hat", "Start at the tip with 4 single crochet and add a few increases each round, spread out, so it grows into a long cone a little wider than the body."),
             (5, "5. Make the nose and beard", "The nose is a small stuffed ball. The beard is a triangle worked in rows. Brush it for fluff or knot strands of yarn into it for a long, shaggy beard."),
             (6, "6. Put it together", "Sew the beard to the front of the body, the nose on top of the beard, then pull the hat down over the head so it rests on the nose. Stitch round the hat edge.")]
gnm_cards = "".join(f'<figure class="gq-fig"><div>{_gnm_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in GNM_STEPS)

gnm = top("Free crochet gnome pattern (easy, any size)", "A crochet gnome is just four simple shapes: a body, a cone hat, a ball nose and a beard. This free beginner pattern shows each step in drawings and writes every round for the size you want, from a 4 in tree ornament to an 11 in shelf gnome, with round tick boxes and yarn amounts.", "Crochet gnome pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet a gnome, make a <strong>flat-bottomed body</strong> in single crochet (a circle, one round in back loops, straight rounds, then decreases to close), a <strong>long cone hat</strong> started from the tip, a small <strong>ball nose</strong> and a <strong>triangle beard</strong>. Sew the beard and nose on, then pull the hat down to the nose. A 6 in gnome takes roughly 70 to 110 yards of worsted yarn in three or four colours and a 3.5 to 4 mm hook, and about 2 to 4 hours, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Gnome pattern writer</h3>
<div class="row2"><div class="field"><label for="gnm-z">Height (to the hat tip)</label><select id="gnm-z"><option value="4">Ornament (4 in)</option><option value="6" selected>Small (6 in)</option><option value="8">Shelf (8 in)</option><option value="11">Large (11 in)</option><option value="m">My own height</option></select></div>
<div class="field" id="gnm-own" hidden><label for="gnm-h">Height (in)</label><input type="number" id="gnm-h" value="7" min="3" max="16" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="gnm-y">Yarn</label><select id="gnm-y"><option value="3">DK (3), 3.5 mm hook</option><option value="4" selected>Worsted (4), 4 mm hook</option><option value="5">Chunky (5), 5 mm hook</option><option value="6">Velvet / chenille (6), 6 mm hook</option></select></div>
<div class="field"><label for="gnm-b">Beard</label><select id="gnm-b"><option value="plain">Crochet triangle (brush it for fluff)</option><option value="fringe" selected>Triangle with knotted fringe (long and shaggy)</option></select></div></div>
<div class="row2"><div class="field"><label for="gnm-x">Extras</label><select id="gnm-x"><option value="none">None</option><option value="loop">Hanging loop (ornament)</option><option value="brim" selected>Folded hat brim</option></select></div>
<div class="field"><label for="gnm-t">Terms</label><select id="gnm-t"><option value="us" selected>US (sc)</option><option value="uk">UK (dc)</option></select></div></div>
</div><div class="result" aria-live="polite" id="gnm-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a gnome, step by step</h2>
<div class="gq-figs">{gnm_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn in 3 or 4 colours:</strong> red (or any colour) for the hat, white, cream or grey for the beard, a skin tone or pink for the nose, and any colour for the body, which hardly shows. Worsted acrylic is easiest to see your stitches in. Leftovers are fine.</li>
<li><strong>Hook:</strong> one or two sizes smaller than the yarn label suggests, so the stuffing doesn't show through: about 3.5 to 4 mm (E-4 to G-6) for worsted.</li>
<li><strong>Also:</strong> toy stuffing (polyester fibrefill), a stitch marker, a tapestry needle and scissors. A pet brush or a stiff comb fluffs up the beard. A pipe cleaner in the hat lets you bend the tip.</li></ul>
<p>New to amigurumi? See the <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>, <a href="{href("how-to-crochet-increase.html")}">how to increase</a>, <a href="{href("how-to-crochet-decrease.html")}">the invisible decrease</a> and our <a href="{href("amigurumi.html")}">amigurumi basics</a>.</p>
<h2>Beard ideas</h2>
<ul><li><strong>Brushed beard:</strong> work the triangle in a fluffy acrylic, then brush it hard with a pet brush. The stitches blur into a soft, fuzzy beard.</li>
<li><strong>Fringe beard:</strong> cut strands twice as long as you want the beard to hang, fold each one, and knot it through a stitch with your hook (a lark's head knot, like a tassel). Trim to a point and untwist the strands for a wavy look.</li>
<li><strong>Loopy beard:</strong> work the triangle in loop stitch (wrap the yarn round a finger before you finish each single crochet) for curls.</li>
<li><strong>Faux fur:</strong> a scrap of faux fur fabric or fur yarn cut to a triangle makes the bushy beard you see on shop gnomes.</li></ul>
<h2>Make a gnome family</h2>
<p>Gnomes look best in groups. Change the hat colour for each one, add a <a href="{href("how-to-make-a-pom-pom.html")}">pom pom</a> to the hat tip, or stripe the hat (see <a href="{href("how-to-change-colors-in-crochet.html")}">how to change colours</a>). The 4 in size with a hanging loop is a quick tree ornament. They sell well at <a href="{href("christmas-crafts-to-sell.html")}">Christmas craft fairs</a>: price them with our <a href="{href("how-to-price-amigurumi.html")}">amigurumi pricing guide</a>. More to make: our <a href="{href("crochet-christmas-tree-pattern.html")}">crochet Christmas tree</a>, <a href="{href("crochet-christmas-ornament-pattern.html")}">bauble ornament</a> and <a href="{href("crochet-sheep-pattern.html")}">sheep</a> patterns.</p>
<p class="note">Pattern and drawings are our own, using standard amigurumi construction (flat circle, back loop round, cone from the tip), checked against gnome patterns from Gathered, Red Ted Art and Love Life Yarn (28 Nov 2026). Gauges, round counts, yardage and hours are estimates for tight amigurumi single crochet; measure as you go. Gnomes with buttons, beads or a bendy wire tip aren't for babies or small children.</p>
</div></div></section>'''
gnm_faq = [
    ("How do you crochet a gnome for beginners?", "Crochet four simple shapes in single crochet: a body with a flat base, a cone hat worked from the tip, a small ball for the nose and a triangle for the beard. Sew the beard and nose to the body, then pull the hat over the top so it rests on the nose."),
    ("How much yarn do I need to crochet a gnome?", "Roughly 70 to 110 yards of worsted in total for a 6 in gnome: most of it for the hat and body, about 5 to 10 yards for the beard triangle and a few yards for the nose. A fringe beard uses more. The writer estimates each colour for your size."),
    ("What yarn is best for crochet gnomes?", "Worsted acrylic is easiest and cheapest. Velvet or chenille yarn makes soft, plush gnomes but is harder to count. For the beard, a fluffy acrylic you can brush, or fur yarn, looks best."),
    ("How do you make a gnome beard with yarn?", "Crochet a small triangle, then knot strands of yarn through its stitches like tassels (a lark's head knot), trim to a point and brush or untwist the strands. Or just brush the crochet triangle itself with a pet brush."),
    ("How long does it take to crochet a gnome?", "A 4 in ornament gnome takes about 1 to 2 hours, a 6 in gnome 2 to 4 hours and an 11 in gnome 6 to 10 hours, depending on your speed and the beard style."),
    ("How do you make a crochet gnome stand up?", "The flat base and the back loop round make it stand. Stuff firmly, and for bigger gnomes put a circle of card or a small bag of pellets in the bottom before you close the body."),
]
SHOP_FOR["crochet-gnome-pattern.html"] = ["crochet-knitting-pricing-calculator", "christmas-gift-tags", "christmas-gift-planner-budget", "2027-crochet-knitting-planner"]
page("crochet-gnome-pattern.html", "Free Crochet Gnome Pattern: Easy, Any Size (Writer)",
     "Free crochet gnome pattern for beginners: six drawn steps and a writer that gives every round for any size, from a gnome ornament to a shelf gnome.",
     gnm, gnm_faq, "Crochet gnome pattern", app_name="Crochet gnome pattern writer")


# ======== HOW TO EMBROIDER LETTERS / NAMES BY HAND (name template maker) ========
# Demand: 'how to embroider a name on fabric by hand' / 'how to embroider letters' (SERP 28 Nov: Crewel Ghoul names on a sweater, Instructables,
# My Modern Met, eHow x4 (blankets, hats, fabric), Needle'nThread x3, Magnetic Hoop, needlework-tips, Gina Michele, Sew Guide, LoveCrafts 5 stitches,
# Gathered, Bob Vila, Skillshare monograms; no template maker that sizes a name and picks the stitch). Stitch advice is standard hand embroidery
# practice (Needle'nThread, LoveCrafts, Gathered). Thread amounts are our estimates.

def _eml_svg(step, label):
    F = "#f6f1e6"
    hoop = f'<circle cx="140" cy="96" r="70" fill="#fff" stroke="{_WOOD}" stroke-width="8"/>'
    word = f'<text x="140" y="108" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="38" fill="none" stroke="#9aa3b5" stroke-width="1" stroke-dasharray="3 3">Ava</text>'
    if step == 1:
        s = (f'<rect x="40" y="40" width="200" height="110" rx="6" fill="#fff" stroke="{_INK}" stroke-width="2"/>'
             + f'<text x="140" y="108" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="46" fill="{_INK}">Ava</text>'
             + f'<text x="140" y="178" {_T12} text-anchor="middle">print the name at the size you want</text>')
    elif step == 2:
        s = (hoop + word + f'<path d="M190 40 l30 -20" stroke="{_TEAL}" stroke-width="6" stroke-linecap="round"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">trace it onto the fabric</text>')
    elif step == 3:
        s = (hoop + word + f'<text x="140" y="190" {_T12} text-anchor="middle">hoop it drum-tight</text>'
             + f'<path d="M84 44 q56 -30 112 0" fill="none" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="5 4"/>')
    elif step == 4:
        s = (f'<path d="M50 110 h180" stroke="#9aa3b5" stroke-width="2" stroke-dasharray="4 4"/>'
             + "".join(f'<path d="M{60 + i * 34} 110 h30" stroke="{_BERRY}" stroke-width="5" stroke-linecap="round"/>' for i in range(4))
             + f'<path d="M196 110 q8 -26 22 0" fill="none" stroke="{_INK}" stroke-width="1.5" stroke-dasharray="3 3"/><circle cx="218" cy="110" r="4" fill="{_INK}"/>'
             + f'<text x="140" y="80" {_T12} text-anchor="middle">small, even stitches along the line</text><text x="140" y="150" {_T12} text-anchor="middle">shorter stitches on tight curves</text>')
    elif step == 5:
        s = (f'<path d="M70 140 C 90 60, 130 60, 150 120 S 200 160, 220 70" fill="none" stroke="{_BERRY}" stroke-width="6" stroke-linecap="round"/>'
             + f'<text x="140" y="178" {_T12} text-anchor="middle">follow the curve, one stroke at a time</text>')
    else:
        s = (hoop + f'<text x="140" y="110" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="38" fill="none" stroke="{_BERRY}" stroke-width="2.2">Ava</text>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">rinse off the lines, press face down</text>')
    return _svg12(s, label)


EML_STEPS = [(1, "1. Size and print the name", "Type the name in the template maker below, pick a lettering style and the height you want, and print it at 100%. Letters at least 1/2 in tall are much easier to stitch."),
             (2, "2. Transfer it to the fabric", "Tape the printout to a window or light box, lay the fabric on top and trace with a water-soluble or heat-erasable pen. On a sweater or dark fabric, trace onto wash-away stabiliser and stick that on."),
             (3, "3. Hoop the fabric", "Put the fabric in a hoop about 2 in wider than the name, and tighten it until it's drum-tight. Loose fabric makes puckered letters."),
             (4, "4. Stitch the straight parts", "Use 2 or 3 strands of floss. Backstitch or split stitch along the lines with small, even stitches, about 1/8 in long. Start each letter with a tiny knot or a waste knot on the back."),
             (5, "5. Take the curves slowly", "On curves, make your stitches shorter so the line stays smooth. Stitch each letter one stroke at a time, the way you would write it, and keep the thread on the back short between letters."),
             (6, "6. Finish and wash", "Weave the thread ends under the stitches on the back. Rinse away the pen lines or stabiliser, let it dry, and press face down on a towel so the stitches don't flatten.")]
eml_cards = "".join(f'<figure class="gq-fig"><div>{_eml_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in EML_STEPS)

EML_STITCH = [("Backstitch", "Small print and script letters, under 1 in", "The easiest outline stitch. Keep the stitches short on curves."),
              ("Split stitch", "Smooth script, any size", "Looks like a fine chain. Great for cursive names on baby blankets."),
              ("Stem stitch", "Curvy script, 1/2 in and up", "Gives a rope-like line that follows curves beautifully."),
              ("Whipped backstitch", "Very smooth lines", "Backstitch first, then wrap a second thread round it. Hides wobbly stitches."),
              ("Chain stitch", "Bold names, 1 in and up", "Thick and textured; the classic stitch on jackets and sweaters."),
              ("Satin stitch", "Block letters and monograms", "Fills the letter with long, side-by-side stitches. Keep each one under 1/4 in, or split the shape.")]
eml_rows = "".join(f'<tr><td><strong>{e(a)}</strong></td><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in EML_STITCH)

eml = top("How to embroider letters and names by hand", "Stitching a name is the most popular first embroidery project: on a baby blanket, a stocking, a sweater or a tote. This guide shows the six steps in drawings, which stitch suits which lettering, and a free template maker that prints your name at actual size with the hoop, stitch and thread to use.", "How to embroider letters") + f'''
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@500&family=Sacramento&display=swap" rel="stylesheet">
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to embroider a name by hand, print the name at the size you want, <strong>trace it onto the fabric</strong> with a water-soluble pen (or onto wash-away stabiliser for sweaters), and put it in a hoop drum-tight. Stitch along the lines with <strong>backstitch, split stitch or stem stitch</strong> using <strong>2 or 3 strands</strong> of embroidery floss, making the stitches shorter on curves. Rinse off the lines and press face down. Letters 1/2 to 2 in tall are the easiest to start with.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Name embroidery template maker</h3>
<div class="row2"><div class="field"><label for="eml-n">Name or word</label><input type="text" id="eml-n" value="Ava" maxlength="24" autocomplete="off"></div>
<div class="field"><label for="eml-f">Lettering</label><select id="eml-f"><option value="script" selected>Flowing script</option><option value="mono">Thin script (monoline)</option><option value="serif">Classic serif</option><option value="print">Simple print</option></select></div></div>
<div class="row2"><div class="field"><label for="eml-h">Letter height (capital), in</label><select id="eml-h"><option value="0.5">1/2 in (small: a hat or cuff)</option><option value="1" selected>1 in (a stocking or bib)</option><option value="1.5">1 1/2 in</option><option value="2">2 in (a blanket or tote)</option><option value="3">3 in (a pillow or wall hoop)</option></select></div>
<div class="field"><label for="eml-o">Fabric</label><select id="eml-o"><option value="woven" selected>Cotton or linen (light colour)</option><option value="dark">Dark fabric</option><option value="knit">Sweater, fleece or towel</option></select></div></div>
<div class="row2"><div class="field"><label for="eml-m">Print it</label><select id="eml-m"><option value="n" selected>Normal (for tracing)</option><option value="r">Mirrored (iron-on transfer pencil)</option></select></div>
<div class="field"><label for="eml-p">Paper</label><select id="eml-p"><option value="letter" selected>US Letter</option><option value="a4">A4</option></select></div></div>
</div><div class="result" aria-live="polite" id="eml-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to embroider a name, step by step</h2>
<div class="gq-figs">{eml_cards}</div>
<h2>Best stitches for embroidering letters</h2>
<div class="tbl"><table class="mt"><thead><tr><th>Stitch</th><th>Best for</th><th>Tip</th></tr></thead><tbody>{eml_rows}</tbody></table></div>
<p>All six are drawn step by step in our <a href="{href("embroidery-stitches.html")}">embroidery stitches for beginners</a> guide. If you're not sure, start with backstitch: it works for every style.</p>
<h2>How many strands of floss for letters?</h2>
<p>Six-strand embroidery floss is pulled apart and used a few strands at a time. Use <strong>1 strand</strong> for tiny letters under 1/4 in, <strong>2 strands</strong> for letters up to about 1 in, and <strong>3 to 4 strands</strong> for bold names 1 1/2 in and up. More strands make a thicker line but are harder to keep smooth on tight curves. Cut pieces about 18 in (45 cm) long so the thread doesn't tangle or wear thin.</p>
<h2>Embroidering a name on a sweater, towel or fleece</h2>
<p>Stretchy and fluffy fabrics swallow pen lines and pull out of shape. Print the name onto <strong>stick-on wash-away stabiliser</strong> (or trace it on), stick it to the front, and stitch through both layers. A piece of iron-on or tear-away stabiliser on the back stops a knit from stretching. Keep a loose tension so the knit can still stretch, then soak the stabiliser away. More methods in <a href="{href("how-to-transfer-embroidery-pattern.html")}">how to transfer an embroidery pattern</a>.</p>
<h2>Ideas for name embroidery</h2>
<ul><li>A baby's name and birth date on a blanket or bib, in split stitch.</li>
<li>Names on Christmas stockings: see our <a href="{href("how-to-sew-a-christmas-stocking.html")}">sew a Christmas stocking</a> guide; stitch the name on the cuff before you sew it on.</li>
<li>A word or initials on a sweater or sweatshirt in chain stitch.</li>
<li>A monogram in satin stitch on a napkin or tote, with a simple vine around it.</li>
<li>A name in a hoop as a nursery sign: use the 3 in size and a 7 or 8 in hoop (see the <a href="{href("embroidery-hoop-size-calculator.html")}">hoop size calculator</a>).</li></ul>
<p class="note">Steps, drawings and the template maker are our own; stitch and strand advice follows standard hand embroidery practice as taught by Needle'nThread, LoveCrafts and Gathered (checked 28 Nov 2026). Script styles use the free Dancing Script and Sacramento fonts (SIL Open Font License). Thread amounts are our estimates.</p>
</div></div></section>'''
eml_faq = [
    ("How do you embroider a name by hand for beginners?", "Print the name at the size you want, trace it onto the fabric with a water-soluble pen, hoop the fabric tightly and stitch over the lines in backstitch or split stitch with 2 or 3 strands of floss. Rinse off the lines when you're done."),
    ("What is the best stitch for embroidering letters?", "Backstitch is the easiest and works for any lettering. Split stitch and stem stitch give smoother curves for script, chain stitch makes bold names, and satin stitch fills block letters and monograms."),
    ("How many strands of embroidery floss should I use for letters?", "Two strands for most letters up to about 1 in tall, one strand for tiny lettering and 3 to 4 strands for big, bold names."),
    ("How do you transfer a name onto fabric for embroidery?", "On light fabric, trace it with a water-soluble or heat-erasable pen over a window or light box. On dark or stretchy fabric, print or trace it onto stick-on wash-away stabiliser and stitch through it."),
    ("How do you embroider a name on a sweater?", "Stick a wash-away stabiliser printed with the name to the front, add a stabiliser on the back so the knit doesn't stretch, and stitch in chain stitch or backstitch with a gentle tension. Soak the stabiliser away afterwards."),
    ("How big should embroidered letters be?", "About 1/2 in tall on a hat or cuff, 1 in on a stocking or bib and 2 to 3 in on a blanket, pillow or nursery hoop. Letters under 1/2 in need tiny stitches and one strand of floss."),
]
SHOP_FOR["how-to-embroider-letters.html"] = ["machine-embroidery-business-spreadsheet", "christmas-gift-tags", "christmas-gift-planner-budget", "small-business-pricing-inventory-spreadsheet"]
page("how-to-embroider-letters.html", "How to Embroider Letters and Names by Hand (Free Template)",
     "How to embroider letters and names by hand: six drawn steps, the best stitches and floss strands, and a free maker that prints your name at actual size.",
     eml, eml_faq, "How to embroider letters", app_name="Name embroidery template maker")


# ======== HOW TO SEW A CHRISTMAS STOCKING (printable template + cutting list) ========
# Demand: 'how to sew a christmas stocking with lining beginner' (SERP 28 Nov: HGTV elf stocking + mini stocking, Bernina blog, Underground Crafter,
# Ideal Home, Woman & Home US+UK, fabrics-store, Polka Dot Chair, Sewing Parts Online, Diary of a Quilter, Sew DIY, Make It Love It, Coral + Co,
# FaveCrafts lined stocking with cuff) + 'christmas stocking template printable'. No page sizes a stocking and prints the tiled template with a
# cutting list. Sizes reuse STK (stockread.py). Bag-lining construction is the standard method used by those tutorials. Yardage is our estimate.

def _sws_svg(step, label):
    R, Rl, Cf = "#b8323f", "#e2c7a0", "#f2ede2"
    sock = lambda dx, fill: f'<path d="M{110 + dx} 30 h50 v80 h30 a22 22 0 0 1 0 44 h-62 a22 22 0 0 1 -22 -22 z" fill="{fill}" stroke="{_INK}" stroke-width="2"/>'
    if step == 1:
        s = (f'<rect x="20" y="18" width="240" height="160" rx="4" fill="#fff" stroke="#9aa3b5" stroke-width="1.5"/>'
             + "".join(f'<path d="M{20 + i * 60} 18 v160" stroke="#9aa3b5" stroke-dasharray="4 4"/>' for i in range(1, 4))
             + sock(-10, "none").replace('fill="none"', 'fill="none" stroke-dasharray="6 3"')
             + f'<text x="140" y="194" {_T12} text-anchor="middle">print the template, tape the pages</text>')
    elif step == 2:
        s = (sock(-50, R) + sock(30, Rl) + f'<text x="70" y="178" {_T12}>outer x 2</text><text x="160" y="178" {_T12}>lining x 2</text>'
             + f'<text x="140" y="196" {_T12} text-anchor="middle">cut each fabric folded, right sides together</text>')
    elif step == 3:
        s = (sock(-10, R) + f'<path d="M100 30 v102 a22 22 0 0 0 22 22 h62 a22 22 0 0 0 0 -44 h-30 v-80" fill="none" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="5 4"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">sew round, leave the top open</text>')
    elif step == 4:
        s = (sock(-10, R) + f'<path d="M100 30 h50 v26 h-50 z" fill="{Cf}" stroke="{_INK}" stroke-width="2"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">sew the cuff into a ring, fold it in half</text>')
    elif step == 5:
        s = (sock(-10, Rl) + f'<path d="M100 30 h50" stroke="{_INK}" stroke-width="2"/><path d="M188 40 l-18 0" stroke="{_TEAL}" stroke-width="3"/>'
             + f'<path d="M140 16 q8 -12 16 0 v14" fill="none" stroke="{_TEAL}" stroke-width="4"/><text x="196" y="44" {_T12}>turning gap</text>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">outer inside the lining, sew the top</text>')
    else:
        s = (sock(-10, R) + f'<path d="M100 30 h50 v26 h-50 z" fill="{Cf}" stroke="{_INK}" stroke-width="2"/><path d="M104 30 q-6 -16 8 -16 q6 0 4 16" fill="none" stroke="{_TEAL}" stroke-width="3"/>'
             + f'<text x="140" y="190" {_T12} text-anchor="middle">turn, stitch the gap, push the lining in</text>')
    return _svg12(s, label)


SWS_STEPS = [(1, "1. Print the template", "Choose a size below and print the tiled template at 100%. Check the 1 in test square, trim the margins on the marked edges and tape the pages together."),
             (2, "2. Cut the pieces", "Fold each fabric in half, right sides together, and cut round the solid line. That gives a front and a back that face opposite ways. Cut the outer fabric and the lining the same way."),
             (3, "3. Sew the outer stocking", "Pin the two outer pieces right sides together and sew round the sides and foot on the dashed line, leaving the top open. Clip the curves and turn it right side out. Sew the lining the same way, but leave a 4 in gap in the straight back seam and don't turn it."),
             (4, "4. Make the cuff and loop", "Sew the cuff piece into a ring, short ends together. Fold it in half, wrong sides together, so it's a double layer. Fold a ribbon into a loop. Stitch a name on the cuff first if you like."),
             (5, "5. Join everything at the top", "Slip the cuff over the outer stocking, raw edges at the top, and pin the loop at the back seam. Push the outer stocking (right side out) into the lining (wrong side out) so right sides face. Sew round the top through all layers."),
             (6, "6. Turn and finish", "Pull everything out through the gap in the lining, stitch the gap closed, push the lining down inside the stocking and fold the cuff down. Press the top edge.")]
sws_cards = "".join(f'<figure class="gq-fig"><div>{_sws_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in SWS_STEPS)

sws_opts = "".join(f'<option value="{k}"{" selected" if k == "standard" else ""}>{e(n)}: {h} in tall ({e(u.split(",")[0])})</option>' for k, n, u, h, w, f, c in STK) + '<option value="m">My own size</option>'
sws_rows = "".join(f'<tr><td>{e(n)}</td><td>{h} in ({round(h * 2.54)} cm)</td><td>{w} in</td><td>{f} in</td><td>{e(u)}</td></tr>' for k, n, u, h, w, f, c in STK)

sws = top("How to sew a Christmas stocking (free printable template)", "A lined Christmas stocking with a cuff is one of the easiest things to sew: two outer pieces, two lining pieces, a cuff and a loop. This beginner guide shows six drawn steps, and the template maker prints a full-size stocking pattern in any size, with the cutting list and how much fabric to buy.", "How to sew a Christmas stocking") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to sew a Christmas stocking, cut <strong>2 outer and 2 lining pieces</strong> from a stocking template (fabric folded, right sides together), sew each pair round the sides and foot, and turn the outer right side out. Slip on a folded cuff and a hanging loop, put the outer stocking inside the lining and <strong>sew round the top</strong>, then turn it through a gap left in the lining and stitch the gap shut. A standard 18 in stocking needs about <strong>1/2 yd of outer fabric and 1/2 yd of lining</strong> with 1/2 in seams, by our estimate.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Stocking template and cutting list</h3>
<div class="row2"><div class="field"><label for="sws-z">Size</label><select id="sws-z">{sws_opts}</select></div>
<div class="field" id="sws-own" hidden><label for="sws-h">Height x leg width x foot length (in)</label><div class="row2"><input type="number" id="sws-h" value="16" min="5" max="32" step="0.5" inputmode="decimal" aria-label="Height in inches"><input type="number" id="sws-w" value="6.5" min="2.5" max="12" step="0.25" inputmode="decimal" aria-label="Leg width in inches"></div><input type="number" id="sws-f" value="9" min="3.5" max="18" step="0.25" inputmode="decimal" aria-label="Foot length in inches" style="margin-top:8px"></div></div>
<div class="row2"><div class="field"><label for="sws-c">Cuff</label><select id="sws-c"><option value="fold" selected>Separate folded cuff (contrast fabric)</option><option value="none">No cuff</option></select></div>
<div class="field"><label for="sws-l">Lining</label><select id="sws-l"><option value="y" selected>Lined (neat inside)</option><option value="n">Not lined (felt or fleece)</option></select></div></div>
<div class="row2"><div class="field"><label for="sws-s">Seam allowance</label><select id="sws-s"><option value="0.25">1/4 in</option><option value="0.375">3/8 in</option><option value="0.5" selected>1/2 in</option><option value="0.625">5/8 in</option></select></div>
<div class="field"><label for="sws-p">Fabric width / paper</label><select id="sws-p"><option value="44|letter" selected>44 in quilting cotton, US Letter</option><option value="58|letter">58 in fabric, US Letter</option><option value="44|a4">112 cm fabric, A4</option><option value="58|a4">150 cm fabric, A4</option></select></div></div>
</div><div class="result" aria-live="polite" id="sws-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to sew a Christmas stocking, step by step</h2>
<div class="gq-figs">{sws_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Outer fabric:</strong> quilting cotton, canvas, velvet, faux fur, wool felt or an old sweater. Quilting cotton is easiest. Add fusible fleece or batting behind the outer pieces for a padded, sturdier stocking.</li>
<li><strong>Lining:</strong> plain or printed cotton. It hides the seams and stops small gifts catching.</li>
<li><strong>Cuff:</strong> a contrast cotton, faux fur, velvet or white felt. Felt and fleece don't fray, so they don't need lining.</li>
<li><strong>Also:</strong> 6 to 8 in of ribbon or a fabric strip for the loop, pins or clips, matching thread, scissors, and a sewing machine or a needle for <a href="{href("hand-sewing-stitches.html")}">backstitch by hand</a>.</li></ul>
<h2>Christmas stocking sizes</h2>
<div class="tbl"><table class="mt"><thead><tr><th>Size</th><th>Height</th><th>Leg width</th><th>Foot length</th><th>Good for</th></tr></thead><tbody>{sws_rows}</tbody></table></div>
<p>These are finished sizes, from the top of the stocking to the bottom of the heel, and across the leg and foot. The template adds the seam allowance you pick. Knitting or crocheting yours instead? Use the <a href="{href("christmas-stocking-calculator.html")}">Christmas stocking calculator</a> or our <a href="{href("how-to-knit-a-christmas-stocking.html")}">knitted stocking guide</a>.</p>
<h2>Sewing tips for a neat stocking</h2>
<ul><li><strong>Clip the curves:</strong> after sewing, snip little notches into the seam allowance round the toe and heel (not through the stitches), so the curves lie smooth when turned.</li>
<li><strong>Directional prints:</strong> folding the fabric makes the front and back face opposite ways, which is right. With a one-way print, check the pattern runs upright on both.</li>
<li><strong>Felt stockings:</strong> skip the lining, sew the two pieces wrong sides together 1/4 in from the edge with blanket stitch or a straight stitch, and leave the edges raw.</li>
<li><strong>Add a name:</strong> stitch it on the cuff before you sew the cuff into a ring. Our <a href="{href("how-to-embroider-letters.html")}">how to embroider letters</a> guide prints the name at the right size.</li>
<li><strong>Selling stockings?</strong> Work out a fair price with the <a href="{href("christmas-crafts-to-sell.html")}">Christmas crafts to sell</a> guide and the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>.</li></ul>
<p>Buying fabric for other projects? The <a href="{href("fabric-yardage-calculator.html")}">fabric yardage calculator</a> and the <a href="{href("sewing-seam-allowance.html")}">seam allowance guide</a> help.</p>
<p class="note">Template, steps and drawings are our own; the lined stocking with a separate cuff is the standard method in tutorials from Bernina, FaveCrafts and Polka Dot Chair (checked 28 Nov 2026). Sizes are typical shop sizes, and fabric amounts are our estimates; buy a little extra for straightening the ends and for directional prints.</p>
</div></div></section>'''
sws_faq = [
    ("How do you sew a Christmas stocking for beginners?", "Cut two outer and two lining pieces from a stocking template, sew each pair round the sides and foot, add a folded cuff and a ribbon loop, put the outer stocking inside the lining and sew round the top. Turn it through a gap in the lining and stitch the gap closed."),
    ("How much fabric do I need for a Christmas stocking?", "About 1/2 yd of outer fabric and 1/2 yd of lining for a standard 18 in stocking from 44 in wide fabric, plus about 1/4 yd for the cuff. Mini stockings fit on a fat quarter. The template maker works it out for your size."),
    ("What size is a standard Christmas stocking?", "About 18 in from the top to the heel, 7 in across the leg and 10 in from heel to toe. Large stockings are 20 to 22 in and mini ones about 7 in."),
    ("What fabric is best for Christmas stockings?", "Quilting cotton is easiest to sew, with fusible fleece behind it for body. Velvet, faux fur and wool felt look cosy; felt and fleece don't fray, so they can be sewn without a lining."),
    ("How do you line a Christmas stocking?", "Sew the lining pieces like the outer stocking, but leave a 4 in gap in the back seam. Put the right-side-out outer stocking inside the wrong-side-out lining, sew round the top, then pull everything through the gap and close it."),
    ("Can I sew a stocking by hand?", "Yes. Use a small backstitch with doubled thread for the seams, 1/4 to 3/8 in from the edge. A felt stocking sewn with blanket stitch round the outside is the easiest hand-sewn version."),
]
SHOP_FOR["how-to-sew-a-christmas-stocking.html"] = ["christmas-gift-tags", "christmas-gift-planner-budget", "december-days-journal-kit", "small-business-pricing-inventory-spreadsheet"]
page("how-to-sew-a-christmas-stocking.html", "How to Sew a Christmas Stocking (Free Printable Template)",
     "How to sew a lined Christmas stocking with a cuff: six drawn steps and a free full-size printable template in any size, with a cutting list and yardage.",
     sws, sws_faq, "How to sew a Christmas stocking", app_name="Christmas stocking template maker")
