# ---------------- 28 Nov 2026 run 23: HOW TO CROCHET A CHRISTMAS STOCKING + HOW TO MAKE PAPER SNOWFLAKES + HOW TO KNIT A COWL ----------------
# Executed from build.py after plan22.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 28 Nov run 23). Patterns, drawings and wording our own. JS in assets/app.js (ccs-*, psf-*, kcw-*).


# ======== HOW TO CROCHET A CHRISTMAS STOCKING (flat, two pieces) ========
# Demand: AB4 'how to crochet a christmas stocking for beginners' (SERP 28 Nov: LoveCrafts, Instructables intro, Make and Do Crew x2,
# Moogly basic, Bella Coco, Yarnspirations Caron tutorial, Mother Earth News, Ravelry x8 listings; no size-to-pattern writer).
# Sizes = /christmas-stocking-calculator table. Gauge = CYC crochet ranges (hdc/sc mid values); hdc row = 0.78 x sts/in, sc row = 1.1 x sts/in.

def _ccs_svg(step, label):
    R, W = _BERRY, "#fbfcfa"
    boot = 'M70 30 h80 v86 h56 q16 0 16 16 v18 q0 12 -12 12 h-120 q-20 0 -20 -20 z'
    if step == 1:
        s = ("".join(f'<circle cx="{62 + i * 14}" cy="44" r="6" fill="none" stroke="{_INK}" stroke-width="2"/>' for i in range(11))
             + f'<rect x="58" y="58" width="160" height="34" rx="2" fill="{W}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{64 + i * 13} 64 v22" stroke="#c9ccc4" stroke-width="3"/>' for i in range(12))
             + f'<text x="140" y="130" {_T12} text-anchor="middle">chain, then single crochet rows</text><text x="140" y="148" {_T12} text-anchor="middle">for the cuff (white)</text>')
    elif step == 2:
        s = (f'<rect x="70" y="30" width="80" height="22" fill="{W}" stroke="{_INK}" stroke-width="2"/><rect x="70" y="52" width="80" height="92" fill="{R}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M76 {60 + j * 12} h68" stroke="#e47aa3" stroke-width="2" stroke-dasharray="5 3"/>' for j in range(7))
             + f'<text x="212" y="92" {_T12} text-anchor="middle">half double</text><text x="212" y="108" {_T12} text-anchor="middle">crochet rows</text>')
    elif step == 3:
        s = (f'<rect x="40" y="30" width="80" height="20" fill="{W}" stroke="{_INK}" stroke-width="2"/><rect x="40" y="50" width="80" height="80" fill="{R}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<circle cx="{126 + i * 10}" cy="124" r="4.5" fill="none" stroke="{_INK}" stroke-width="2"/>' for i in range(7))
             + f'<path d="M200 112 q20 -20 0 -40" fill="none" stroke="{_GOLD}" stroke-width="3"/><path d="M194 76 l8 -6 l2 10" fill="none" stroke="{_GOLD}" stroke-width="3"/>'
             + f'<text x="150" y="160" {_T12} text-anchor="middle">chain extra for the toe, turn</text><text x="150" y="176" {_T12} text-anchor="middle">and work back across</text>')
    elif step == 4:
        s = (f'<path d="{boot}" fill="{R}" stroke="{_INK}" stroke-width="2"/><rect x="70" y="30" width="80" height="20" fill="{W}" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M50 150 q-6 -4 -2 -12" fill="none" stroke="{_GOLD}" stroke-width="3"/><path d="M226 150 q8 -4 4 -14" fill="none" stroke="{_GOLD}" stroke-width="3"/>'
             f'<text x="140" y="186" {_T12} text-anchor="middle">decrease at both ends to round heel and toe</text>')
    elif step == 5:
        s = (f'<g transform="translate(-22 30) scale(.62)"><path d="{boot}" fill="{R}" stroke="{_INK}" stroke-width="3"/></g>'
             f'<g transform="translate(302 30) scale(-.62 .62)"><path d="{boot}" fill="#d9567f" stroke="{_INK}" stroke-width="3"/></g>'
             f'<text x="140" y="190" {_T12} text-anchor="middle">a mirror piece: one extra leg row</text>')
    else:
        s = (f'<path d="{boot}" fill="{R}" stroke="{_INK}" stroke-width="2"/><rect x="70" y="30" width="80" height="20" fill="{W}" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="{boot}" fill="none" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="2 6"/>'
             f'<path d="M78 30 q-8 -22 10 -22 q14 0 4 22" fill="none" stroke="{_TEAL}" stroke-width="4"/>'
             f'<text x="140" y="186" {_T12} text-anchor="middle">single crochet the pieces together</text>')
    return _svg12(s, label)


CCS_STEPS = [(1, "1. Chain and crochet the cuff", "In white, chain the number the writer gives you, then work rows of single crochet for the cuff. Working in the back loops only gives a ribbed, stretchy look."),
             (2, "2. Crochet the leg", "Join the main colour and work rows of half double crochet (or single crochet for a denser stocking) until the piece reaches the start of the foot."),
             (3, "3. Add the toe", "At the end of the last leg row, chain the extra toe stitches plus a turning chain. Turn, work into the new chains, then carry on across the leg. The piece becomes an L, like a boot."),
             (4, "4. Round the heel and toe", "Work the foot straight, then decrease one stitch at each end of the last few rows. The corners round off into a heel and a toe. Fasten off."),
             (5, "5. Make a mirror piece", "Crochet a second piece the same way, but work one extra leg row before you add the toe chains. That puts the toe on the other side, so the pieces match as a front and back."),
             (6, "6. Join and add a loop", "Hold the pieces wrong sides together and single crochet through both layers all round, leaving the top open. Chain a hanging loop at the heel side and weave in the ends.")]
ccs_cards = "".join(f'<figure class="gq-fig"><div>{_ccs_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CCS_STEPS)

ccs = top("How to crochet a Christmas stocking for beginners", "This stocking is crocheted flat in two boot-shaped pieces, in straight rows: no rounds, no heel turn and no gusset. If you can chain, single crochet and half double crochet, you can make it. Every step is drawn below, and the writer turns any size and yarn into a full row-by-row pattern in US or UK terms.", "How to crochet a Christmas stocking") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the easiest way to crochet a Christmas stocking is <strong>flat, in two boot-shaped pieces</strong>. Chain about 24 in worsted yarn, crochet a single crochet cuff, then the leg in half double crochet rows; <strong>chain extra stitches for the toe</strong>, work the foot, <strong>decrease at both ends</strong> of the last rows to round the heel and toe, and fasten off. Make a mirror piece and single crochet them together. A classic 18 in stocking takes roughly 220 to 300 yards of worsted and 5 to 8 hours, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Crochet Christmas stocking pattern writer</h3>
<div class="row2"><div class="field"><label for="ccs-z">Size</label><select id="ccs-z"><option value="mini">Mini ornament (7 in tall)</option><option value="small">Small or child (12 in)</option><option value="standard" selected>Classic (18 in)</option><option value="large">Large (22 in)</option><option value="xl">Extra large (26 in)</option></select></div>
<div class="field"><label for="ccs-y">Yarn</label><select id="ccs-y"><option value="3">DK / light (3)</option><option value="4" selected>Worsted / aran (4)</option><option value="5">Chunky / bulky (5)</option><option value="6">Super bulky (6)</option></select></div></div>
<div class="row2"><div class="field"><label for="ccs-s">Main stitch</label><select id="ccs-s"><option value="hdc" selected>Half double crochet (quicker)</option><option value="sc">Single crochet (denser)</option></select></div>
<div class="field"><label for="ccs-t">Terms</label><select id="ccs-t"><option value="us" selected>US terms</option><option value="uk">UK terms</option></select></div></div>
<div class="row2"><div class="field"><label for="ccs-g">Your swatch: stitches per 4 in in the main stitch (optional)</label><input type="number" id="ccs-g" placeholder="leave blank for a typical gauge" min="5" max="26" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="ccs-c">Cuff</label><select id="ccs-c"><option value="blo" selected>Ribbed (back loops only)</option><option value="plain">Plain single crochet</option></select></div></div>
</div><div class="result" aria-live="polite" id="ccs-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a Christmas stocking, step by step</h2>
<div class="gq-figs">{ccs_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> worsted (4) acrylic in red or green for the body and white for the cuff. Acrylic is cheap, washable and keeps its shape when the stocking is full. Chunky yarn works up much faster.</li>
<li><strong>Hook:</strong> the size on the yarn label, about 5 mm (H-8) for worsted or 6.5 mm (K-10.5) for chunky. Go down half a size if your fabric looks loose: a stocking should be firm.</li>
<li><strong>Also:</strong> a tapestry needle, stitch markers or safety pins, scissors and a tape measure.</li></ul>
<p>New to crochet? The <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a> guide shows chain, single and half double crochet, and <a href="{href("how-to-crochet-decrease.html")}">how to decrease</a> covers the two-together stitches used for the heel and toe.</p>
<h2>Why crochet a stocking flat?</h2>
<p>Many crochet stockings are worked in the round with a separate heel, like a giant sock. They look neat, but keeping the round count right and shaping the heel is where beginners get stuck. Two flat pieces are just rows, a few extra chains and a few decreases. Joining them with single crochet in a contrast colour also hides any uneven edges, and makes a pretty border. For in-the-round numbers, see the <a href="{href("christmas-stocking-calculator.html")}">Christmas stocking calculator</a>.</p>
<h2>Stripes, a white heel or a name</h2>
<ul><li><strong>Stripes:</strong> change colour on the last yarn-over of the row before the new colour. Our guide to <a href="{href("how-to-change-colors-in-crochet.html")}">changing colours in crochet</a> shows the trick, and the <a href="{href("stripe-generator.html")}">stripe generator</a> picks an order for you.</li>
<li><strong>White heel and toe:</strong> work the whole foot section, from the toe chains down, in white. It's the classic look and needs no colour work.</li>
<li><strong>A name:</strong> crochet the letters as a chain and sew them on, or embroider the name on the cuff with chain stitch. Check the name fits with the stocking calculator.</li></ul>
<h2>Joining the two pieces</h2>
<p>Weave in all ends first. Put the pieces wrong sides together with the cuffs lined up and clip them every couple of inches. Join the yarn at the top of the heel side and single crochet through both layers all the way round, working 1 stitch in each row end of half double crochet rows (2 if the edge puckers) and 3 stitches in one spot at sharp corners. Stop at the top. For the loop, chain 20, slip stitch back into the stocking, and fasten off. Prefer an invisible seam? Place right sides together and whip stitch with a tapestry needle, then turn.</p>
<h2>How long does it take to crochet a Christmas stocking?</h2>
<p>As a rough guide for a comfortable beginner (our estimates), a mini ornament stocking takes 1 to 2 hours, a child's stocking 3 to 4 hours and a classic 18 in stocking 5 to 8 hours in worsted, including an hour to join the pieces. Making several as gifts? Check your deadline with the <a href="{href("crochet-knitting-gift-planner.html")}">handmade Christmas gift planner</a>, and if you'll sell them, use the <a href="{href("how-to-price-crochet-items.html")}">crochet pricing guide</a>. Prefer knitting or sewing? See <a href="{href("how-to-knit-a-christmas-stocking.html")}">how to knit a Christmas stocking</a> and <a href="{href("how-to-sew-a-christmas-stocking.html")}">how to sew a Christmas stocking</a>.</p>
<p class="note">Method is our own two-piece design, checked against common beginner stocking construction (LoveCrafts, Moogly, Make and Do Crew, Yarnspirations; 28 Nov 2026). Sizes match our <a href="{href("christmas-stocking-calculator.html")}">stocking size chart</a>; gauge from the Craft Yarn Council ranges. Yarn and hours are estimates.</p>
</div></div></section>'''
ccs_faq = [
    ("How do you crochet a Christmas stocking for beginners?", "Crochet it flat in two boot-shaped pieces: chain, work a single crochet cuff, crochet the leg in half double crochet rows, chain extra stitches for the toe, work the foot, decrease at both ends of the last rows to round the heel and toe, then make a mirror piece and single crochet the two together."),
    ("How many chains do I need for a crochet Christmas stocking?", "For a classic 18 in stocking crocheted flat in two pieces, about 23 to 25 stitches per piece in worsted half double crochet (13 stitches per 4 in), plus the turning chain. The writer above works it out for any size and yarn."),
    ("How much yarn do I need to crochet a Christmas stocking?", "Roughly 220 to 300 yards of worsted yarn for a classic 18 in stocking in half double crochet, by our estimates. Single crochet uses about 10 percent more."),
    ("What is the best stitch for a crochet stocking?", "Half double crochet is quick and firm enough. Single crochet makes a denser stocking that holds heavier gifts. Avoid lacy stitches: small gifts fall through."),
    ("Can a beginner crochet a Christmas stocking?", "Yes. Worked flat in two pieces it only needs chain, single crochet, half double crochet and a simple decrease, with no rounds or heel turn."),
    ("How long does it take to crochet a Christmas stocking?", "About 5 to 8 hours for a classic 18 in stocking in worsted yarn for a beginner, including an hour to join the pieces (our estimates). Chunky yarn is quicker."),
]
SHOP_FOR["how-to-crochet-a-christmas-stocking.html"] = ["letter-from-santa-kit", "christmas-gift-tags", "christmas-gift-planner-budget", "crochet-knitting-pricing-calculator"]
page("how-to-crochet-a-christmas-stocking.html", "How to Crochet a Christmas Stocking for Beginners (Free Pattern)",
     "How to crochet a Christmas stocking for beginners, flat in two pieces with no heel turn: six drawn steps and a pattern writer for any size, yarn and US or UK terms.",
     ccs, ccs_faq, "How to crochet a Christmas stocking", app_name="Crochet Christmas stocking pattern writer")


# ======== HOW TO MAKE PAPER SNOWFLAKES (6-point fold + printable cutting templates) ========
# Demand: 'how to make a paper snowflake template printable' (SERP 28 Nov: Hallmark PDFs x3, NHM animal snowflakes, Easy Peasy and Fun,
# Homemade Gifts Made Easy, One Little Project, Skip To My Lou templates, Gathered, Printables Fairy, library PDF, slideshare copies; static
# PDFs only, no generator). Fold: square -> triangle -> thirds -> half = 30 degree wedge, 12 layers, 6 points (standard 6-fold method).

def _psf_svg(step, label):
    P, L = "#fbfcfa", "#c9ccc4"
    if step == 1:
        s = (f'<rect x="40" y="40" width="110" height="110" fill="{P}" stroke="{_INK}" stroke-width="2"/><path d="M40 150 L150 40" stroke="{_GOLD}" stroke-width="2" stroke-dasharray="6 4"/>'
             f'<path d="M170 150 L280 150 L170 40 z" transform="translate(-10 0)" fill="{P}" stroke="{_INK}" stroke-width="2"/>'
             f'<text x="140" y="180" {_T12} text-anchor="middle">fold the square corner to corner</text>')
    elif step == 2:
        s = (f'<path d="M30 150 L250 150 L140 40 z" fill="{P}" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M140 150 L60 72" stroke="{_GOLD}" stroke-width="2" stroke-dasharray="6 4"/><path d="M140 150 L220 72" stroke="{_GOLD}" stroke-width="2" stroke-dasharray="6 4"/>'
             f'<circle cx="140" cy="150" r="4" fill="{_BERRY}"/><text x="140" y="180" {_T12} text-anchor="middle">fold into thirds from the middle of the long edge</text>')
    elif step == 3:
        s = (f'<path d="M140 160 L92 40 L188 40 z" fill="{P}" stroke="{_INK}" stroke-width="2"/><path d="M140 160 L140 40" stroke="{_GOLD}" stroke-width="2" stroke-dasharray="6 4"/>'
             f'<path d="M188 40 l20 -14" stroke="{_INK}" stroke-width="2"/><text x="140" y="186" {_T12} text-anchor="middle">fold the cone in half: a thin wedge</text>')
    elif step == 4:
        s = (f'<path d="M140 168 L116 30 L164 30 z" fill="{P}" stroke="{_INK}" stroke-width="2"/><path d="M110 58 L170 44" stroke="{_BERRY}" stroke-width="2.5" stroke-dasharray="5 3"/>'
             f'<path d="M116 30 L164 30 L170 44 L110 58 z" fill="{L}" opacity=".8"/><text x="200" y="110" {_T12} text-anchor="middle">cut off</text><text x="200" y="126" {_T12} text-anchor="middle">the top</text>')
    elif step == 5:
        s = (f'<path d="M140 168 L114 58 L166 46 z" fill="{P}" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M126 110 l12 4 l-8 10 z M122 86 l12 2 l-10 10 z M152 92 l-12 6 l10 8 z M146 130 l-6 4 l7 6 z" fill="{L}" stroke="{_BERRY}" stroke-width="1.6"/>'
             f'<text x="214" y="110" {_T12} text-anchor="middle">cut shapes</text><text x="214" y="126" {_T12} text-anchor="middle">from both edges</text>')
    else:
        arm = "".join(f'<g transform="rotate({a} 140 100)"><path d="M140 100 L140 34" stroke="{_TEAL}" stroke-width="6" stroke-linecap="round"/><path d="M140 56 l-12 -10 M140 56 l12 -10 M140 74 l-9 -8 M140 74 l9 -8" stroke="{_TEAL}" stroke-width="4" stroke-linecap="round"/></g>' for a in range(0, 360, 60))
        s = arm + f'<circle cx="140" cy="100" r="9" fill="#f6f1e6" stroke="{_TEAL}" stroke-width="4"/><text x="140" y="190" {_T12} text-anchor="middle">unfold gently, press under a book</text>'
    return _svg12(s, label)


PSF_STEPS = [(1, "1. Start with a square", "Cut a square of thin paper: printer paper trimmed to 8.5 x 8.5 in, or a sheet of origami paper. Fold it in half from corner to corner to make a triangle."),
             (2, "2. Fold into thirds", "Find the middle of the long folded edge: that's the centre of your snowflake. Fold the left and right sides over so they overlap in three equal parts, like a paper cone. Line the edges up neatly."),
             (3, "3. Fold in half again", "Fold the cone in half lengthwise so you have one thin wedge. This is where the six points come from: the paper is now 12 layers thick."),
             (4, "4. Cut off the top", "Trim the uneven top straight across or at a slant. A slant that leaves the folded edge longest gives pointed arms. The template below shows the line."),
             (5, "5. Cut shapes from the edges", "Snip triangles, slots and curves out of both long edges, and a few small holes in the middle. Leave at least a third of the width uncut or it will fall apart."),
             (6, "6. Unfold and flatten", "Open it slowly so the thin parts don't tear. Press it under a heavy book for an hour to take out the creases, then hang it with thread or stick it to a window.")]
psf_cards = "".join(f'<figure class="gq-fig"><div>{_psf_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in PSF_STEPS)

psf = top("How to make paper snowflakes (with free printable templates)", "Real snowflakes have six points, and so will yours with the right fold: a square folded into a triangle, then thirds, then in half. Every fold is drawn below. Then design a snowflake in the maker, see exactly how it opens up, and print an actual-size cutting template for your paper.", "How to make paper snowflakes") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to make a six-pointed paper snowflake, <strong>fold a square of paper in half into a triangle</strong>, <strong>fold it into thirds</strong> from the middle of the long edge, then <strong>fold it in half</strong> once more. Cut the top off at a slant, snip small shapes out of both folded edges, and unfold. Thin paper (printer paper or origami paper) cuts best.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Paper snowflake maker and template</h3>
<div class="row2"><div class="field"><label for="psf-st">Style</label><select id="psf-st"><option value="simple">Simple (good for kids)</option><option value="classic" selected>Classic</option><option value="lacy">Lacy (lots of cuts)</option></select></div>
<div class="field"><label for="psf-tip">Points</label><select id="psf-tip"><option value="star" selected>Star points</option><option value="sharp">Long, sharp points</option><option value="hex">Hexagon (flat edges)</option></select></div></div>
<div class="row2"><div class="field"><label for="psf-p">Paper square</label><select id="psf-p"><option value="8.5" selected>8.5 in (US Letter trimmed)</option><option value="8.27">21 cm (A4 trimmed)</option><option value="6">6 in / 15 cm (origami paper)</option></select></div>
<div class="field"><label for="psf-c">Centre</label><select id="psf-c"><option value="hole" selected>Small hole in the middle</option><option value="none">Solid middle</option></select></div></div>
<div class="btns"><button type="button" class="btn" id="psf-new">New design</button> <button type="button" class="btn gold" id="psf-print">Print the cutting template</button></div>
<p class="note">Design number <span id="psf-n">1</span>. Every design stays in one piece when cut.</p>
</div><div class="result" aria-live="polite" id="psf-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to fold and cut a paper snowflake, step by step</h2>
<div class="gq-figs">{psf_cards}</div>
<h2>How to use the printable template</h2>
<p>Print the template at 100% (turn off "fit to page") on plain paper, cut it out along the wedge outline, and fold your square as in steps 1 to 3. Lay the template on top of the folded wedge with its point at the centre point of the folds, hold or paper-clip it in place, and cut away the shaded parts through all the layers. Or trace the shaded shapes with a pencil and cut those. Small scissors with sharp tips, or a craft knife on a cutting mat for the holes, give the cleanest edges.</p>
<h2>What paper is best for paper snowflakes?</h2>
<ul><li><strong>Printer paper (20 lb / 75 to 80 gsm):</strong> the best all-rounder. Cheap, crisp and easy to cut through 12 layers.</li>
<li><strong>Origami paper or tissue-thin craft paper:</strong> lovely for lacy designs, as thin layers cut very cleanly.</li>
<li><strong>Coffee filters:</strong> already round and soft, great for small children; they make 8-point flakes if folded in quarters, then in half twice.</li>
<li><strong>Avoid card and construction paper:</strong> too thick to cut once it's 12 layers deep. Glitter or metallic paper is fine if it's thin.</li></ul>
<h2>Why fold in thirds? (Why snowflakes have six points)</h2>
<p>Ice crystals grow in six directions, so real snowflakes have six arms. Folding the triangle into thirds and then in half gives 12 layers, and each cut you make is repeated 12 times, mirrored on each side of six arms. Folding a square in half three times (into eighths) is quicker but gives eight points, which looks more like a flower or a star than a snowflake.</p>
<h2>Ideas for using paper snowflakes</h2>
<ul><li><strong>Window decorations:</strong> stick them on with a dab of water or removable tape.</li>
<li><strong>Garlands and mobiles:</strong> thread them on fishing line or tie them to a branch at different heights.</li>
<li><strong>Gift wrap and cards:</strong> glue a small one on plain kraft paper, or use one as a stencil for paint or glitter. Our <a href="{href("christmas-crafts.html")}">Christmas crafts</a> page has a free gift tag maker to match.</li>
<li><strong>Junk journals:</strong> a snowflake cut from old book pages or tea-dyed paper makes a pretty winter page. See <a href="{href("how-to-tea-stain-paper.html")}">how to tea stain paper</a> and our <a href="{href("junk-journal-page-ideas.html")}#christmas">Christmas junk journal ideas</a>.</li>
<li><strong>A yarn version:</strong> the <a href="{href("crochet-snowflake-pattern.html")}">free crochet snowflake pattern</a> takes under an hour and lasts for years.</li></ul>
<h2>Tips for a crisp snowflake</h2>
<ul><li>Crease every fold hard with a fingernail, and keep the edges lined up: a sloppy third fold makes lopsided arms.</li>
<li>Don't cut all the way across the wedge from one edge to the other, or a piece drops off.</li>
<li>Cut the bigger shapes first and the little holes last, when you can see what's left.</li>
<li>Let children draw the cuts with a pencil, then cut with safety scissors. The "Simple" style above is made for them.</li></ul>
<p class="note">The six-point fold is the standard method shown by The Natural History Museum, Gathered and many craft sites (checked 28 Nov 2026). Our steps, drawings and designs are our own; the maker draws new designs and only keeps ones that stay in one piece.</p>
</div></div></section>'''
psf_faq = [
    ("How do you fold paper to make a snowflake?", "Fold a square of paper in half into a triangle, then fold it into thirds from the middle of the long folded edge, then fold it in half once more. Cut the top off, cut shapes from both edges and unfold. This gives a six-pointed snowflake."),
    ("How do you make a 6-pointed paper snowflake?", "The key is folding in thirds: square to triangle, triangle into thirds like a cone, then in half. That makes 12 layers, so each cut repeats around six arms."),
    ("What is the best paper for paper snowflakes?", "Thin paper: ordinary printer paper, origami paper or coffee filters. Card and construction paper are too thick to cut through 12 layers."),
    ("Where can I get free printable snowflake templates?", "Use the snowflake maker on this page: pick a style, click New design until you like it, and print an actual-size cutting template for 8.5 in, A4 or 6 in paper."),
    ("Why does my paper snowflake fall apart?", "A cut went too far across the folded wedge and met another cut, or ran from one edge to the other. Keep at least a third of the wedge width uncut down the middle."),
    ("How do you flatten paper snowflakes?", "Unfold slowly, then press the snowflake between two sheets of paper under a heavy book for an hour or overnight. A cool iron with no steam works too."),
]
SHOP_FOR["how-to-make-paper-snowflakes.html"] = ["december-days-journal-kit", "winter-cottage-junk-journal-kit", "christmas-gift-tags", "letter-from-santa-kit"]
page("how-to-make-paper-snowflakes.html", "How to Make Paper Snowflakes (Free Printable Templates)",
     "How to make six-pointed paper snowflakes: the fold drawn step by step, plus a snowflake maker that shows the open design and prints an actual-size cutting template.",
     psf, psf_faq, "How to make paper snowflakes", app_name="Paper snowflake template maker")


# ======== HOW TO KNIT A COWL (in the round, any size) ========
# Demand: 'how to knit a cowl for beginners circular needles' (SERP 28 Nov: Skillshare blog, Sheep & Stitch x2, Dummies x2, KnitPro blog,
# Handy Little Me neck warmer, Ravelry beginner cowl listings x8; no size/yarn writer). Sizes typical of beginner patterns (estimates).
# Gauge = CYC knit ranges; stockinette rows 1.35 x sts/in, garter ridges 1.9 x, seed/moss 1.6 x. Yarn model as the stocking writer x stitch factor.

def _kcw_svg(step, label):
    if step == 1:
        s = (f'<path d="M40 120 q100 60 200 0" fill="none" stroke="#8a93a6" stroke-width="3"/><rect x="28" y="70" width="14" height="60" rx="5" fill="{_WOOD}"/><rect x="238" y="70" width="14" height="60" rx="5" fill="{_WOOD}"/>'
             + "".join(f'<path d="M{50 + i * 10} 76 q5 -10 10 0" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for i in range(4)) + "".join(f'<path d="M{190 + i * 10} 76 q5 -10 10 0" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for i in range(4))
             + f'<text x="140" y="180" {_T12} text-anchor="middle">cast on to a circular needle</text>')
    elif step == 2:
        s = (f'<circle cx="140" cy="96" r="58" fill="none" stroke="#8a93a6" stroke-width="3"/>'
             + "".join(f'<path d="M{140 + 58 * _m.cos(a / 57.3):.1f} {96 + 58 * _m.sin(a / 57.3):.1f} l0 -8" stroke="{_BERRY}" stroke-width="3"/>' for a in range(0, 360, 20))
             + f'<circle cx="140" cy="38" r="6" fill="{_GOLD}"/><text x="140" y="186" {_T12} text-anchor="middle">bumps all inside: join without twisting</text>')
    elif step == 3:
        s = (f'<rect x="50" y="60" width="180" height="70" rx="6" fill="#f2c8d8" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<rect x="{56 + i * 14}" y="66" width="7" height="58" fill="{_BERRY}" opacity=".7"/>' for i in range(12))
             + f'<path d="M140 52 v86" stroke="{_GOLD}" stroke-width="3"/><text x="140" y="166" {_T12} text-anchor="middle">marker marks the start of each round</text>')
    elif step == 4:
        s = (f'<rect x="80" y="40" width="80" height="120" rx="6" fill="#f2c8d8" stroke="{_INK}" stroke-width="2"/><rect x="176" y="40" width="20" height="120" fill="#fff3c9" stroke="{_INK}" stroke-width="1.5"/>'
             + "".join(f'<path d="M176 {44 + i * 12} h8" stroke="{_INK}" stroke-width="1.5"/>' for i in range(10))
             + f'<text x="140" y="186" {_T12} text-anchor="middle">measure the height on a flat surface</text>')
    elif step == 5:
        s = ("".join(f'<path d="M{50 + i * 22} 100 q11 -26 22 0" fill="none" stroke="{_BERRY}" stroke-width="4"/>' for i in range(8))
             + f'<path d="M120 70 l18 -18" stroke="{_WOOD}" stroke-width="6" stroke-linecap="round"/><text x="140" y="150" {_T12} text-anchor="middle">bind off loosely, in pattern</text>')
    else:
        s = (f'<ellipse cx="140" cy="70" rx="70" ry="18" fill="none" stroke="{_BERRY}" stroke-width="10"/><path d="M70 70 v60 q70 34 140 0 v-60" fill="#f2c8d8" stroke="{_BERRY}" stroke-width="4" opacity=".9"/>'
             + f'<text x="140" y="186" {_T12} text-anchor="middle">weave in the ends, block if you like</text>')
    return _svg12(s, label)


KCW_STEPS = [(1, "1. Cast on", "Cast on the number of stitches the writer gives you onto a circular needle, with the long-tail cast on. Cast on loosely, or over two needles held together, so the top edge stretches over your head."),
             (2, "2. Join in the round", "Spread the stitches round the cable with every cast-on bump facing the centre and none twisted over the needle. Place a marker and knit the first stitch tightly to close the gap."),
             (3, "3. Work the pattern", "Work round after round in your stitch, slipping the marker each time. Rib and seed stitch alternate knits and purls; garter in the round is a knit round, then a purl round."),
             (4, "4. Check the height", "Lay the cowl flat (still on the needle) and measure from the cast-on edge. Keep going until it's as tall as the writer says, or as tall as you like."),
             (5, "5. Bind off loosely", "Bind off in pattern: knit the knits and purl the purls as you go. Use a needle one or two sizes bigger so the edge stretches like the cast on."),
             (6, "6. Finish", "Weave in both ends, hiding them in the ribbing or purl bumps. Blocking with a little steam or water evens out the stitches and makes ribbing lie flat.")]
kcw_cards = "".join(f'<figure class="gq-fig"><div>{_kcw_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in KCW_STEPS)
KCW_SIZES = [("Child neck warmer", "18 in", "7 in", "Ages about 3 to 10"), ("Snug neck warmer", "22 in", "8 in", "Close round the neck, tucks into a coat"),
             ("Classic cowl", "26 in", "10 in", "Pulls over the head, sits loosely"), ("Tall cowl", "26 in", "14 in", "Can be pulled up over the chin or head"),
             ("Long loop (infinity)", "56 in", "10 in", "Wrapped twice round the neck")]
kcw_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in KCW_SIZES)

kcw = top("How to knit a cowl for beginners", "A cowl is the perfect first project on circular needles: one tube, no seams, no shaping, and it's done in an evening or two in chunky yarn. Every step is drawn below, and the writer turns any size, yarn and stitch into a pattern with the cast-on number, rounds, needle length and yarn.", "How to knit a cowl") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to knit a cowl, <strong>cast on</strong> enough stitches for about 22 to 26 in round (about 76 to 92 stitches in chunky yarn), <strong>join in the round</strong> on a 16 in circular needle without twisting, and <strong>knit in rib, seed or garter stitch</strong> until it's 8 to 10 in tall. Bind off loosely and weave in the ends. A classic chunky cowl takes about 130 to 180 yards and 4 to 6 hours, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Cowl pattern writer</h3>
<div class="row2"><div class="field"><label for="kcw-z">Size</label><select id="kcw-z"><option value="18x7">Child neck warmer (18 x 7 in)</option><option value="22x8">Snug neck warmer (22 x 8 in)</option><option value="26x10" selected>Classic cowl (26 x 10 in)</option><option value="26x14">Tall cowl (26 x 14 in)</option><option value="56x10">Long loop / infinity (56 x 10 in)</option><option value="own">My own size</option></select></div>
<div class="field"><label for="kcw-y">Yarn</label><select id="kcw-y"><option value="3">DK / light (3)</option><option value="4">Worsted / aran (4)</option><option value="5" selected>Chunky / bulky (5)</option><option value="6">Super bulky (6)</option><option value="7">Jumbo (7)</option></select></div></div>
<div class="row2" id="kcw-own" hidden><div class="field"><label for="kcw-cw">Circumference (in)</label><input type="number" id="kcw-cw" value="26" min="14" max="80" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="kcw-ch">Height (in)</label><input type="number" id="kcw-ch" value="10" min="3" max="24" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="kcw-s">Stitch</label><select id="kcw-s"><option value="r11">1x1 rib (k1, p1)</option><option value="r22" selected>2x2 rib (k2, p2)</option><option value="seed">Seed stitch</option><option value="garter">Garter stitch</option><option value="st">Stockinette with rib edges</option></select></div>
<div class="field"><label for="kcw-g">Your swatch: stitches per 4 in (optional)</label><input type="number" id="kcw-g" placeholder="leave blank for a typical gauge" min="4" max="32" step="0.5" inputmode="decimal"></div></div>
</div><div class="result" aria-live="polite" id="kcw-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to knit a cowl, step by step</h2>
<div class="gq-figs">{kcw_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> chunky (5) or super bulky (6) wool or a wool blend is the classic choice: warm, quick and forgiving. A soft acrylic or alpaca blend is good if wool itches.</li>
<li><strong>Needle:</strong> a 16 in (40 cm) circular needle for neck warmers and classic cowls, or 24 to 32 in (60 to 80 cm) for long loops, in the size on the yarn label. The writer picks the length for you.</li>
<li><strong>Also:</strong> a stitch marker, a tapestry needle and scissors.</li></ul>
<p>New to circular needles? Our guide to <a href="{href("how-to-knit-in-the-round.html")}">knitting in the round</a> shows the join without twisting. You'll also need <a href="{href("how-to-cast-on-knitting.html")}">a cast on</a>, <a href="{href("how-to-knit-and-purl.html")}">knit and purl</a> and <a href="{href("how-to-bind-off-knitting.html")}">a stretchy bind off</a>.</p>
<h2>Cowl size chart</h2>
<div class="tbl"><table class="mt"><thead><tr><th>Type</th><th>Circumference</th><th>Height</th><th>How it wears</th></tr></thead><tbody>{kcw_rows}</tbody></table></div>
<p>These are typical finished sizes from beginner cowl patterns. A cowl you pull over your head needs at least 22 in round; snugger neck warmers in very stretchy rib can go a little smaller. For a scarf instead, see the <a href="{href("scarf-size-chart.html")}">scarf size chart</a>.</p>
<h2>Which stitch is best for a cowl?</h2>
<ul><li><strong>2x2 or 1x1 rib:</strong> stretchy, reversible and doesn't curl. The easiest choice for a first cowl.</li>
<li><strong>Seed stitch:</strong> a bumpy, textured fabric that lies flat. In the round on an odd number of stitches, just repeat k1, p1 forever and it makes itself.</li>
<li><strong>Garter stitch:</strong> squishy ridges; in the round it's one knit round, one purl round.</li>
<li><strong>Stockinette:</strong> smooth, but the edges roll, so the writer adds a few rounds of rib at each end.</li></ul>
<p>Want more texture? Browse <a href="{href("knit-stitch-patterns.html")}">15 knit stitch patterns for beginners</a>, or add a cable band with the <a href="{href("how-to-knit-cables.html")}">cable guide</a>.</p>
<h2>Can I knit a cowl on straight needles?</h2>
<p>Yes. Cast on the same number of stitches plus 2 for the seam, knit flat back and forth until the piece is as long as the circumference, then sew the two short ends together with mattress stitch or graft them. Knitting a long, narrow strip this way and seaming it makes a long loop with no circular needle at all. Or knit the height as the long side: cast on for the height and knit a strip as long as the circumference.</p>
<h2>How long does it take to knit a cowl?</h2>
<p>As a rough guide for a comfortable beginner (our estimates), a chunky classic cowl takes 4 to 6 hours, a super bulky one 2 to 3, and a worsted one 6 to 9. Long loops take about twice as long. Knitting cowls as gifts? Check what you can finish in time with the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>, and see how much yarn is left on a part ball with the <a href="{href("yarn-yardage-calculator.html")}">yarn yardage calculator</a>.</p>
<p class="note">Steps, writer and drawings are our own. Typical sizes and construction checked against Dummies, Sheep &amp; Stitch, KnitPro and Handy Little Me (28 Nov 2026); gauge from the Craft Yarn Council ranges. Stitch counts are exact for your gauge; yarn and hours are estimates.</p>
</div></div></section>'''
kcw_faq = [
    ("How do you knit a cowl for beginners?", "Cast on onto a 16 in circular needle, join in the round without twisting the stitches, and work rib, seed or garter stitch until the cowl is 8 to 10 in tall. Bind off loosely in pattern and weave in the ends."),
    ("How many stitches do I cast on for a cowl?", "Multiply the circumference by your stitches per inch. For a 26 in cowl in chunky yarn at 14 stitches per 4 in, that's about 92 stitches, rounded to fit your stitch pattern (a multiple of 4 for 2x2 rib)."),
    ("What size circular needle do I need for a cowl?", "A 16 in (40 cm) cable works for neck warmers and cowls from about 18 to 28 in round. Use 24 in for 28 to 44 in, and 32 in or longer for long loops."),
    ("How much yarn do I need for a cowl?", "Roughly 130 to 180 yards of chunky yarn or 185 to 250 yards of worsted for a classic 26 x 10 in cowl, by our estimates. Rib and textured stitches use a little more than stockinette."),
    ("How big should a cowl be?", "About 22 to 26 in round and 8 to 10 in tall for an adult cowl, 18 in round for a child, and 50 to 60 in round for a long loop that wraps twice."),
    ("Can you knit a cowl without circular needles?", "Yes. Knit a flat rectangle on straight needles and sew the short ends together with mattress stitch."),
]
SHOP_FOR["how-to-knit-a-cowl.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-planner-budget", "crochet-knitting-pricing-calculator"]
page("how-to-knit-a-cowl.html", "How to Knit a Cowl for Beginners (Free Pattern, Any Size)",
     "How to knit a cowl on circular needles for beginners: six drawn steps, a cowl size chart and a pattern writer for any size, yarn and stitch, with cast on and yarn.",
     kcw, kcw_faq, "How to knit a cowl", app_name="Cowl pattern writer")
