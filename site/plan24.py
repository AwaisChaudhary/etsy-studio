# ---------------- 29 Nov 2026 run 24: CROCHET TREE SKIRT PATTERN + HOW TO KNIT A DISHCLOTH + HOW TO CROCHET A DISHCLOTH ----------------
# Executed from build.py after plan23.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13, _m).
# Demand evidence in DEMAND.md (RADAR 29 Nov run 24). Patterns, drawings and wording our own. JS in assets/app.js (cts-*, kdc-*, cdc-*).


# ======== CROCHET TREE SKIRT (flat circle in turned rows, with a slit) ========
# Demand: AC4 'how to crochet a christmas tree skirt free pattern' (SERP 29 Nov: Yarnspirations Bernat/Red Heart/Caron x9, Bella Coco x2,
# Hanjan, Gathered, A Crocheted Simplicity poinsettia, Ravelry x4; fixed-size patterns only, no size writer).
# Maths: flat circle worked in rows. Increase per row = 2 pi x row height x sts/in = 12 for dc, 8 for hdc (the standard circle counts).
# Gauge = CYC crochet ranges (mid values). dc row height 1 / (0.54 x sts/in), hdc 1 / (0.78 x sts/in).

def _cts_svg(step, label):
    R, G, W = _BERRY, "#2f8f5a", "#fbfcfa"
    if step == 1:
        s = ("".join(f'<circle cx="{140 + 40 * _m.cos(_m.radians(a)):.1f}" cy="{96 + 40 * _m.sin(_m.radians(a)):.1f}" r="5" fill="none" stroke="{_INK}" stroke-width="2"/>' for a in range(-80, 260, 20))
             + f'<path d="M140 50 v-22" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="4 3"/><text x="140" y="176" {_T12} text-anchor="middle">a chain as long as the trunk hole is round</text><text x="140" y="192" {_T12} text-anchor="middle">(do not join it)</text>')
    elif step == 2:
        s = (f'<path d="M140 96 m-40 0 a40 40 0 1 0 40 -40" fill="none" stroke="{G}" stroke-width="14"/>'
             f'<path d="M140 40 v30" stroke="{_GOLD}" stroke-width="3"/><text x="150" y="36" {_T12}>the slit</text>'
             f'<text x="140" y="176" {_T12} text-anchor="middle">row 1: a stitch in every chain,</text><text x="140" y="192" {_T12} text-anchor="middle">then turn (rows, not rounds)</text>')
    elif step == 3:
        s = ("".join(f'<rect x="{40 + i * 18}" y="96" width="10" height="34" rx="3" fill="{G}"/>' for i in range(11))
             + "".join(f'<path d="M{40 + i * 18 + 5} 96 l-6 -26 M{40 + i * 18 + 5} 96 l6 -26" stroke="{R}" stroke-width="4" stroke-linecap="round"/>' for i in (2, 6, 10))
             + f'<text x="140" y="160" {_T12} text-anchor="middle">2 stitches in one stitch = an increase</text><text x="140" y="176" {_T12} text-anchor="middle">spread evenly across every row</text>')
    elif step == 4:
        s = ("".join(f'<path d="M140 96 m-{r} 0 a{r} {r} 0 1 0 {r} -{r}" fill="none" stroke="{c}" stroke-width="10"/>' for r, c in ((22, G), (34, R), (46, G), (58, W), (70, G)))
             + f'<path d="M140 96 m-70 0 a70 70 0 1 0 70 -70" fill="none" stroke="{_INK}" stroke-width="1" opacity=".4"/>'
             + f'<text x="66" y="34" {_T12} text-anchor="middle">turn at the</text><text x="66" y="50" {_T12} text-anchor="middle">slit each row</text>')
    elif step == 5:
        s = (f'<path d="M30 120 h220" stroke="{G}" stroke-width="16"/>'
             + "".join(f'<path d="M{48 + i * 40} 112 q-18 -40 20 -40 q38 0 20 40" fill="{W}" stroke="{R}" stroke-width="3"/>' for i in range(5))
             + f'<text x="140" y="170" {_T12} text-anchor="middle">a shell edge round the outside</text>')
    else:
        s = (f'<path d="M140 30 l50 100 h-100 z" fill="{G}"/><rect x="132" y="130" width="16" height="16" fill="{_WOOD}"/>'
             f'<ellipse cx="140" cy="160" rx="110" ry="22" fill="{R}" stroke="{_INK}" stroke-width="2"/><ellipse cx="140" cy="154" rx="16" ry="5" fill="{_WOOD}"/>'
             f'<path d="M140 150 l40 30" stroke="{W}" stroke-width="3"/><path d="M128 150 q-8 10 -2 18 M152 150 q8 10 2 18" stroke="{_GOLD}" stroke-width="3" fill="none"/>'
             f'<text x="140" y="30" {_T12} text-anchor="middle" dx="80">tie the slit closed</text>')
    return _svg12(s, label)


CTS_STEPS = [(1, "1. Chain for the centre", "Chain the number the writer gives you: enough to go round your tree stand's trunk. Don't join it into a ring. The gap between the two ends becomes the slit that lets the skirt go round the tree."),
             (2, "2. Work the first row", "Chain up (3 for double crochet, 2 for half double), turn and work one stitch into every chain. You're crocheting a C shape in rows, turning at each end, not rounds."),
             (3, "3. Increase on every row", "Each row adds the same number of stitches (12 for double crochet, 8 for half double), spread evenly: some plain stitches, then 2 stitches in one, all the way across. That's what keeps the skirt flat."),
             (4, "4. Keep going to the size", "Row after row, the C grows into a big circle with a straight slit. Change colour at the start of a row for stripes. Stop when the skirt reaches the diameter you want, measured across the middle."),
             (5, "5. Add a pretty edge", "Work a shell edging along the outer edge (skip 2, 5 double crochet in the next, skip 2, single crochet), then single crochet up both sides of the slit so they lie straight."),
             (6, "6. Add ties and wrap the tree", "Chain three pairs of ties along the slit (at the centre, the middle and the outer edge), or sew on buttons. Weave in the ends, lay the skirt round the stand and tie it closed.")]
cts_cards = "".join(f'<figure class="gq-fig"><div>{_cts_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CTS_STEPS)
CTS_SIZES = [("Tabletop or mini tree (2 to 4 ft)", "24 in", "about 2 ft round"), ("Small tree (4 to 5 ft)", "30 to 36 in", "a mid-size stand"),
             ("Standard tree (6 to 7 ft)", "42 to 48 in", "the most popular size"), ("Large tree (7.5 ft and up)", "52 to 60 in", "covers a wide stand and branches"),
             ("Centre hole", "5 to 8 in across", "fits most trunks and stands")]
cts_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in CTS_SIZES)

cts = top("Free crochet tree skirt pattern (any size)", "A crochet Christmas tree skirt is just a big flat circle worked in rows, with a slit so it wraps round the trunk. Only chains, double (or half double) crochet and a few increases each row. Every step is drawn below, and the writer turns any diameter, yarn and stitch into a row-by-row pattern in US or UK terms.", "Crochet tree skirt pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet a tree skirt, <strong>chain enough to go round the trunk</strong> (about 60 chains for a 6 in hole in worsted), <strong>don't join</strong>, and work rows of double crochet, <strong>adding 12 stitches evenly every row</strong> so the piece stays flat. Turn at the slit each row until the skirt is 36 to 48 in across, add a shell edge and ties. A 36 in skirt takes roughly 700 to 900 yards of worsted and 6 to 10 hours, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Crochet tree skirt pattern writer</h3>
<div class="row2"><div class="field"><label for="cts-d">Finished diameter</label><select id="cts-d"><option value="24">24 in (tabletop tree)</option><option value="30">30 in</option><option value="36" selected>36 in (small to mid tree)</option><option value="42">42 in</option><option value="48">48 in (standard 6 to 7 ft tree)</option><option value="56">56 in (large tree)</option><option value="own">My own size</option></select></div>
<div class="field" id="cts-own" hidden><label for="cts-od">Diameter (in)</label><input type="number" id="cts-od" value="40" min="16" max="72" step="1" inputmode="decimal"></div>
<div class="field"><label for="cts-h">Centre hole across (in)</label><input type="number" id="cts-h" value="6" min="3" max="12" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="cts-y">Yarn</label><select id="cts-y"><option value="4" selected>Worsted / aran (4)</option><option value="5">Chunky / bulky (5)</option><option value="6">Super bulky (6)</option></select></div>
<div class="field"><label for="cts-s">Main stitch</label><select id="cts-s"><option value="dc" selected>Double crochet (quicker)</option><option value="hdc">Half double crochet (denser)</option></select></div></div>
<div class="row2"><div class="field"><label for="cts-t">Terms</label><select id="cts-t"><option value="us" selected>US terms</option><option value="uk">UK terms</option></select></div>
<div class="field"><label for="cts-g">Your swatch: stitches per 4 in in the main stitch (optional)</label><input type="number" id="cts-g" placeholder="leave blank for a typical gauge" min="5" max="24" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="cts-e">Edge</label><select id="cts-e"><option value="shell" selected>Shell edge</option><option value="plain">Plain single crochet edge</option></select></div>
<div class="field"><label for="cts-c">Stripes</label><select id="cts-c"><option value="0" selected>One colour</option><option value="2">Change colour every 2 rows</option><option value="4">Change colour every 4 rows</option></select></div></div>
</div><div class="result" aria-live="polite" id="cts-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a tree skirt, step by step</h2>
<div class="gq-figs">{cts_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> worsted (4) acrylic is the usual choice: cheap, sturdy, washable and easy to find in Christmas reds, greens and white. Chunky or super bulky yarn makes a thick, cosy skirt much faster. Buy all of each colour from one dye lot.</li>
<li><strong>Hook:</strong> the size on the yarn label, about 5 to 5.5 mm (H-8 or I-9) for worsted, 6.5 mm (K-10.5) for chunky or 9 mm (M/N-13) for super bulky.</li>
<li><strong>Also:</strong> stitch markers, a tapestry needle, scissors and a tape measure. Buttons are optional for closing the slit.</li></ul>
<p>New to these stitches? The <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a> guide shows chain, half double and double crochet, and <a href="{href("how-to-crochet-increase.html")}">how to increase</a> shows working 2 stitches into one.</p>
<h2>What size tree skirt do I need?</h2>
<div class="tbl"><table class="mt"><thead><tr><th>Tree</th><th>Skirt diameter</th><th>Notes</th></tr></thead><tbody>{cts_rows}</tbody></table></div>
<p>These are typical sizes. A skirt should reach a little past the lowest branches so it catches needles and hides the stand. Measure your stand's trunk or pole for the hole: the slit means it doesn't need to fit snugly.</p>
<h2>Why crochet the skirt in rows, not rounds?</h2>
<p>A round circle would be a closed doughnut with no way to get it round a tree that's already up. Working back and forth in rows leaves an open slit, and turning each row also stops the seam line slanting the way joined rounds do. The increases are the same as for any flat circle, so the maths is in our <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a> too.</p>
<h2>Why is my tree skirt wavy or curling up?</h2>
<p><strong>Waves or ruffles</strong> mean too many stitches for your row height: your rows are shorter than typical (tight tension). Go up a hook size or work 2 fewer increases per row. <strong>Cupping like a bowl</strong> means too few: your rows are tall, or you've missed an increase. Count every row, and lay the skirt flat every few rows to check. Moving the increases along a few stitches each row (the writer does this) stops the skirt turning into a hexagon.</p>
<h2>How long does it take to crochet a tree skirt?</h2>
<p>As a rough guide for a comfortable crocheter (our estimates), a 36 in skirt in worsted double crochet takes 6 to 10 hours, and a 48 in one 11 to 18 hours, because the outer rows are long. Super bulky yarn halves the time. To finish before Christmas, plan a few rows a night with the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>, and if you'll sell skirts, price them with the <a href="{href("how-to-price-crochet-items.html")}">crochet pricing guide</a>.</p>
<p>More festive makes: a <a href="{href("crochet-christmas-tree-pattern.html")}">crochet Christmas tree</a>, <a href="{href("crochet-christmas-ornament-pattern.html")}">ornaments</a>, a <a href="{href("crochet-snowflake-pattern.html")}">snowflake</a> and a <a href="{href("how-to-crochet-a-christmas-stocking.html")}">stocking</a> to match.</p>
<p class="note">Pattern, writer and drawings are our own. Construction (a flat circle in turned rows with a slit and ties) checked against Yarnspirations, Gathered and Bella Coco tree skirt patterns (29 Nov 2026); gauge from the Craft Yarn Council ranges. Stitch counts are exact for your gauge; yarn and hours are estimates.</p>
</div></div></section>'''
cts_faq = [
    ("How do you crochet a Christmas tree skirt?", "Chain enough stitches to go round the trunk without joining, then work rows of double crochet back and forth, adding 12 stitches evenly in every row so the piece lies flat. Stop at the diameter you want, add a shell edge and chain ties along the slit."),
    ("How many stitches do you increase in a crochet tree skirt?", "Add the same number every row: 12 for double crochet or 8 for half double crochet, spread evenly. These are the usual flat-circle counts; if your skirt ruffles or cups, adjust by 1 or 2."),
    ("How much yarn do I need to crochet a tree skirt?", "Roughly 700 to 900 yards of worsted yarn for a 36 in skirt and 1,200 to 1,650 yards for 48 in in double crochet, by our estimates. The writer above works it out for your size and yarn."),
    ("What size should a crochet tree skirt be?", "About 24 in for a tabletop tree, 30 to 36 in for a small tree, 42 to 48 in for a standard 6 to 7 ft tree and 52 to 60 in for a large tree, with a centre hole of 5 to 8 in."),
    ("Is a crochet tree skirt worked in rows or rounds?", "Usually in rows. Turning at each end leaves an open slit so the skirt can go round a tree that's already standing."),
    ("How long does it take to crochet a tree skirt?", "About 6 to 10 hours for a 36 in skirt in worsted double crochet, and 11 to 18 hours for 48 in (our estimates). Super bulky yarn is much quicker."),
]
SHOP_FOR["crochet-tree-skirt-pattern.html"] = ["christmas-gift-planner-budget", "crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "yarn-stash-tracker"]
page("crochet-tree-skirt-pattern.html", "Free Crochet Tree Skirt Pattern for Any Size (Step by Step)",
     "Free crochet Christmas tree skirt pattern: six drawn steps and a pattern writer for any diameter, yarn and stitch, with every row, yarn and time, in US or UK terms.",
     cts, cts_faq, "Crochet tree skirt pattern", app_name="Crochet tree skirt pattern writer")


# ======== HOW TO KNIT A DISHCLOTH ========
# Demand: 'how to knit a dishcloth for beginners' (SERP 29 Nov: Instructables, AllFreeKnitting, Skillshare, LoveToKnow, B.Hooked,
# Imperfectly Happy, Crochet Crowd, San Diego library PDF, LoveCrafts/Ravelry beginner dishcloth listings x8; no size/yarn writer).
# Gauge = CYC knit ranges. Diagonal: widest stitch count ~ side x sts/in x 1.15 (calibrated on the classic 44-st, ~8.5 in garter cloth).

def _kdc_svg(step, label):
    C, W = "#f2c8d8", "#fbfcfa"
    if step == 1:
        s = (f'<rect x="60" y="70" width="160" height="12" rx="6" fill="{_WOOD}"/>'
             + "".join(f'<path d="M{110 + i * 16} 82 q8 18 16 0" fill="none" stroke="{_BERRY}" stroke-width="4"/>' for i in range(4))
             + f'<text x="140" y="140" {_T12} text-anchor="middle">cast on 4 stitches, knit 1 row</text>')
    elif step == 2:
        s = (f'<path d="M140 160 l-60 -60 l20 -20 l60 60 z" fill="{C}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<circle cx="{86 + i * 8}" cy="{94 - i * 8}" r="2.6" fill="{W}" stroke="{_INK}"/>' for i in range(3))
             + f'<text x="200" y="70" {_T12} text-anchor="middle">k2, yo, knit to end</text><text x="200" y="86" {_T12} text-anchor="middle">(+1 stitch a row)</text>')
    elif step == 3:
        s = (f'<path d="M140 170 l-80 -80 l80 -80 z" fill="{C}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<circle cx="{64 + i * 9}" cy="{86 - i * 9}" r="2.6" fill="{W}" stroke="{_INK}"/>' for i in range(8))
             + f'<path d="M60 90 L140 170" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="5 4"/><text x="200" y="120" {_T12} text-anchor="middle">widest point:</text><text x="200" y="136" {_T12} text-anchor="middle">edge = side length</text>')
    elif step == 4:
        s = (f'<path d="M140 170 L60 90 L140 10 L180 50 L180 130 Z" fill="{C}" stroke="{_INK}" stroke-width="2"/><path d="M140 10 V170" stroke="{_INK}" stroke-width="1" stroke-dasharray="3 3" opacity=".5"/>'
             + f'<text x="56" y="150" {_T12} text-anchor="middle">k1, k2tog, yo,</text><text x="56" y="166" {_T12} text-anchor="middle">k2tog, knit on</text><text x="56" y="182" {_T12} text-anchor="middle">(-1 st a row)</text>')
    elif step == 5:
        s = (f'<path d="M140 180 l-80 -80 l80 -80 l80 80 z" fill="{C}" stroke="{_INK}" stroke-width="2"/>'
             + f'<text x="140" y="104" {_T12} text-anchor="middle">bind off the</text><text x="140" y="120" {_T12} text-anchor="middle">last 4 stitches</text>')
    else:
        s = (f'<rect x="56" y="40" width="120" height="120" rx="4" fill="{C}" stroke="{_INK}" stroke-width="2" transform="rotate(8 116 100)"/>'
             f'<rect x="170" y="96" width="70" height="44" rx="10" fill="#fff3c9" stroke="{_INK}" stroke-width="2"/><text x="205" y="123" {_T12} text-anchor="middle">soap</text>'
             f'<text x="140" y="188" {_T12} text-anchor="middle">weave in the ends and it is ready</text>')
    return _svg12(s, label)


KDC_STEPS = [(1, "1. Cast on 4 stitches", "With cotton yarn, cast on 4 stitches and knit one row. The classic diagonal dishcloth starts at one corner and grows."),
             (2, "2. Increase every row", "Every row: knit 2, yarn over, knit to the end. The yarn over adds one stitch and makes the little holes along both edges. Every row is the same, and it all comes out as garter stitch."),
             (3, "3. Stop at the widest point", "Keep going until the straight edge (not the eyelet edge) is as long as you want each side of the cloth, about 8 in. The writer tells you roughly how many stitches that is."),
             (4, "4. Decrease every row", "Now every row: knit 1, knit 2 together, yarn over, knit 2 together, knit to the end. That loses one stitch a row, and the cloth closes into a square."),
             (5, "5. Bind off", "When 4 stitches are left, bind them off. You're at the opposite corner from where you started."),
             (6, "6. Finish", "Weave in the two ends, hiding them along the edge. Wash it once and it softens. Tie two together with a bar of soap for a quick gift.")]
kdc_cards = "".join(f'<figure class="gq-fig"><div>{_kdc_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in KDC_STEPS)

kdc = top("How to knit a dishcloth for beginners", "A knitted dishcloth is the best first project there is: small, quick, useful, and you learn everything a scarf would teach you in one evening. Every step of the classic diagonal cloth is drawn below, and the writer turns any size, yarn and style (diagonal, garter or seed stitch) into a pattern with the cast on, rows and yarn.", "How to knit a dishcloth") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the classic beginner dishcloth is knitted <strong>corner to corner</strong>. With worsted cotton and 4.5 mm (US 7) needles, cast on 4, then <strong>knit 2, yarn over, knit to the end</strong> on every row until you have about 44 stitches; then <strong>knit 1, knit 2 together, yarn over, knit 2 together, knit to the end</strong> on every row until 4 stitches are left, and bind off. It makes an 8 to 9 in square from about 45 to 65 yards of cotton in 1 to 3 hours, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Knitted dishcloth pattern writer</h3>
<div class="row2"><div class="field"><label for="kdc-p">Style</label><select id="kdc-p"><option value="diag" selected>Diagonal (corner to corner, eyelet edge)</option><option value="garter">Garter stitch square</option><option value="seed">Seed stitch square</option><option value="border">Stockinette with a garter border</option></select></div>
<div class="field"><label for="kdc-z">Size</label><select id="kdc-z"><option value="7">7 in (small, quick)</option><option value="8" selected>8 in (classic)</option><option value="9">9 in</option><option value="10">10 in (washcloth)</option><option value="12">12 in (large)</option></select></div></div>
<div class="row2"><div class="field"><label for="kdc-y">Yarn</label><select id="kdc-y"><option value="3">DK / light cotton (3)</option><option value="4" selected>Worsted cotton (4)</option><option value="5">Chunky cotton (5)</option></select></div>
<div class="field"><label for="kdc-g">Your swatch: stitches per 4 in (optional)</label><input type="number" id="kdc-g" placeholder="leave blank for a typical gauge" min="8" max="30" step="0.5" inputmode="decimal"></div></div>
</div><div class="result" aria-live="polite" id="kdc-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to knit a dishcloth, step by step</h2>
<div class="gq-figs">{kdc_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> 100 percent cotton in worsted weight (4). Cotton soaks up water, handles hot washes and doesn't melt near a hot pan, which acrylic can. One standard 2 oz (57 g) ball of kitchen cotton usually makes one 8 in cloth with a little left over.</li>
<li><strong>Needles:</strong> 4.5 to 5 mm (US 7 or 8) straight needles for worsted cotton. Cotton has no stretch, so a slightly bigger needle than the label keeps it from feeling tight on your hands.</li>
<li><strong>Also:</strong> a tapestry needle and scissors.</li></ul>
<p>Never knitted before? Start with <a href="{href("how-to-cast-on-knitting.html")}">how to cast on</a> and <a href="{href("how-to-knit-and-purl.html")}">how to knit and purl</a>, then finish with <a href="{href("how-to-bind-off-knitting.html")}">how to bind off</a> and <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>.</p>
<h2>Which dishcloth style should I knit first?</h2>
<ul><li><strong>Diagonal (corner to corner):</strong> the classic, sometimes called Grandmother's Favorite. Only knit stitches, yarn overs and knit 2 together, and you never need to count the width: you just measure the edge.</li>
<li><strong>Garter stitch square:</strong> knit every row. The very easiest, but you need to check it's square before you bind off.</li>
<li><strong>Seed stitch square:</strong> knit 1, purl 1 across an odd number of stitches. Bumpy and scrubby, and good purl practice.</li>
<li><strong>Stockinette with a garter border:</strong> smooth in the middle with a frame that stops the edges curling. Practice for keeping track of a few edge stitches.</li></ul>
<p>Want more textures? Our <a href="{href("knit-stitch-patterns.html")}">15 knit stitch patterns</a> all work as dishcloths: knit a square swatch and you've made one.</p>
<h2>How do I know my dishcloth is square?</h2>
<p>Fold one corner across to the opposite side, making a triangle. If the edges meet neatly, it's square. For a diagonal cloth, measure along the plain edge (not the holey one) at the widest point; once that edge reaches your size, start decreasing. Garter stitch rows are short, so a garter square has about twice as many rows as stitches.</p>
<h2>What can I do with dishcloths?</h2>
<p>Use them for dishes and wiping counters, as face washcloths in a softer cotton, or as gifts: a set of three tied with ribbon round a bar of soap is a favourite at craft fairs. Planning a few as gifts? See the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Selling them? <a href="{href("christmas-crafts-to-sell.html")}">Christmas crafts to make and sell</a> has typical prices. Prefer a hook? Try <a href="{href("how-to-crochet-a-dishcloth.html")}">how to crochet a dishcloth</a>.</p>
<p class="note">Steps, writer and drawings are our own. The diagonal method is the traditional one taught in most beginner guides; construction checked against AllFreeKnitting, Instructables and B.Hooked dishcloth tutorials (29 Nov 2026); gauge from the Craft Yarn Council ranges. Stitch counts are for your gauge; the diagonal stitch count, yarn and hours are estimates.</p>
</div></div></section>'''
kdc_faq = [
    ("How do you knit a dishcloth for beginners?", "Cast on 4 stitches in worsted cotton and knit one row. Then knit 2, yarn over, knit to the end on every row until you have about 44 stitches. Then knit 1, knit 2 together, yarn over, knit 2 together, knit to the end on every row until 4 stitches remain, and bind off."),
    ("How many stitches do I cast on for a knitted dishcloth?", "For a square dishcloth, multiply the width by your stitches per inch: about 36 to 40 stitches for 8 in in worsted cotton. For the diagonal dishcloth you cast on just 4 and increase to about 44."),
    ("What yarn is best for knitting dishcloths?", "100 percent cotton in worsted weight. It's absorbent, takes hot washes and won't melt near a hot pan the way acrylic can."),
    ("How much yarn do I need for a knitted dishcloth?", "About 45 to 65 yards of worsted cotton for an 8 in dishcloth, by our estimates, so one 2 oz ball usually makes one cloth."),
    ("What size needles do I use for a dishcloth?", "4.5 to 5 mm (US 7 or 8) for worsted cotton. A slightly bigger needle than the label keeps the stiff cotton easier to knit."),
    ("How big should a knitted dishcloth be?", "About 8 in square is classic. 7 in is quick and small; 9 to 10 in suits a washcloth."),
]
SHOP_FOR["how-to-knit-a-dishcloth.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-planner-budget"]
page("how-to-knit-a-dishcloth.html", "How to Knit a Dishcloth for Beginners (Free Pattern, Any Size)",
     "How to knit a dishcloth for beginners: the classic diagonal cloth in six drawn steps, plus a pattern writer for any size, yarn and style, with cast on, rows and yarn.",
     kdc, kdc_faq, "How to knit a dishcloth", app_name="Knitted dishcloth pattern writer")


# ======== HOW TO CROCHET A DISHCLOTH ========
# Demand: 'how to crochet a dishcloth for beginners' (SERP 29 Nov: EasyCrochet x2, Skillshare x2, eHow, Sigoni Macaroni dc, Miss Mustard Seed,
# Sweet Georgia Yarns, Handy Little Me, Everyday Farmhouse, Ravelry x3; fixed patterns, no size/yarn writer).
# Gauge = CYC crochet ranges (mid values) as the stocking writer; moss/linen stitch rows ~ sc rows.

def _cdc_svg(step, label):
    C, W = "#cfe7e1", "#fbfcfa"
    if step == 1:
        s = ("".join(f'<circle cx="{46 + i * 14}" cy="96" r="6" fill="none" stroke="{_INK}" stroke-width="2"/>' for i in range(14))
             + f'<text x="140" y="140" {_T12} text-anchor="middle">a foundation chain as wide as the cloth</text>')
    elif step == 2:
        s = ("".join(f'<circle cx="{46 + i * 14}" cy="130" r="6" fill="none" stroke="{_INK}" stroke-width="2"/>' for i in range(14))
             + "".join(f'<path d="M{46 + i * 14} 122 v-26" stroke="{_TEAL}" stroke-width="5" stroke-linecap="round"/>' for i in range(1, 14))
             + f'<text x="140" y="70" {_T12} text-anchor="middle">row 1: a stitch in each chain</text>')
    elif step == 3:
        s = ("".join(f'<rect x="{50 + i * 16}" y="{60 + j * 22}" width="10" height="16" rx="3" fill="{_TEAL}"/>' for i in range(11) for j in range(4))
             + f'<path d="M232 60 q22 10 0 22" fill="none" stroke="{_GOLD}" stroke-width="3"/><text x="140" y="170" {_T12} text-anchor="middle">chain 1, turn, repeat the row</text>')
    elif step == 4:
        s = (f'<rect x="36" y="30" width="140" height="140" fill="{C}" stroke="{_INK}" stroke-width="2"/><path d="M36 170 L176 30" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="5 4"/>'
             f'<text x="230" y="100" {_T12} text-anchor="middle">fold to</text><text x="230" y="116" {_T12} text-anchor="middle">check square</text>')
    elif step == 5:
        s = (f'<rect x="36" y="30" width="140" height="140" fill="{C}" stroke="{_BERRY}" stroke-width="8"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{_GOLD}"/>' for x, y in ((36, 30), (176, 30), (36, 170), (176, 170)))
             + f'<text x="230" y="96" {_T12} text-anchor="middle">3 stitches</text><text x="230" y="112" {_T12} text-anchor="middle">in each corner</text>')
    else:
        s = (f'<rect x="40" y="50" width="110" height="110" rx="3" fill="{C}" stroke="{_BERRY}" stroke-width="6" transform="rotate(-6 95 105)"/>'
             f'<rect x="120" y="44" width="110" height="110" rx="3" fill="#f2c8d8" stroke="{_TEAL}" stroke-width="6" transform="rotate(5 175 100)"/>'
             f'<text x="140" y="190" {_T12} text-anchor="middle">weave in the ends: a gift set</text>')
    return _svg12(s, label)


CDC_STEPS = [(1, "1. Chain", "With cotton yarn, chain the number the writer gives you. The chain sets the width of the cloth, about 8 in for a classic dishcloth."),
             (2, "2. Work the first row", "Work your stitch into the second chain from the hook (third for half double) and into every chain across."),
             (3, "3. Repeat the rows", "Chain 1 (or 2), turn and work one stitch into every stitch of the row below. Count now and then: losing or adding stitches at the ends is the most common beginner slip."),
             (4, "4. Check it's square", "When the cloth is about as tall as it is wide, fold one corner across to the opposite edge. If the edges meet in a neat triangle, it's square. Fasten off, or keep the yarn on for a border."),
             (5, "5. Add a border (optional)", "Work single crochet all round the edge, with 3 stitches in each corner so it lies flat. A contrast colour border makes a simple cloth look finished."),
             (6, "6. Finish", "Weave in the ends securely, since a dishcloth gets scrubbed and washed hot. Make two or three in different colours for a gift set.")]
cdc_cards = "".join(f'<figure class="gq-fig"><div>{_cdc_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CDC_STEPS)

cdc = top("How to crochet a dishcloth for beginners", "A crochet dishcloth is a perfect first project: one square, one stitch, and it's finished in an evening. Every step is drawn below, and the writer turns any size, yarn and stitch (single crochet, half double, moss stitch or double crochet) into a pattern with the starting chain, rows, border and yarn, in US or UK terms.", "How to crochet a dishcloth") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet a dishcloth, <strong>chain about 29</strong> in worsted cotton with a 5 mm (H-8) hook, <strong>single crochet in the 2nd chain from the hook and each chain across</strong> (28 stitches), then <strong>chain 1, turn and single crochet in every stitch</strong> for about 31 rows, until it's square, about 8 in. Add a single crochet border with 3 stitches in each corner (the writer makes the middle a little smaller to allow for it). It takes roughly 50 to 75 yards and 1 to 2 hours, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Crochet dishcloth pattern writer</h3>
<div class="row2"><div class="field"><label for="cdc-s">Stitch</label><select id="cdc-s"><option value="sc" selected>Single crochet (easiest, scrubby)</option><option value="hdc">Half double crochet</option><option value="moss">Moss / linen stitch (sc, ch 1)</option><option value="dc">Double crochet (quickest, softer)</option></select></div>
<div class="field"><label for="cdc-z">Size</label><select id="cdc-z"><option value="7">7 in (small, quick)</option><option value="8" selected>8 in (classic)</option><option value="9">9 in</option><option value="10">10 in (washcloth)</option><option value="12">12 in (large)</option></select></div></div>
<div class="row2"><div class="field"><label for="cdc-y">Yarn</label><select id="cdc-y"><option value="3">DK / light cotton (3)</option><option value="4" selected>Worsted cotton (4)</option><option value="5">Chunky cotton (5)</option></select></div>
<div class="field"><label for="cdc-t">Terms</label><select id="cdc-t"><option value="us" selected>US terms</option><option value="uk">UK terms</option></select></div></div>
<div class="row2"><div class="field"><label for="cdc-b">Border</label><select id="cdc-b"><option value="1" selected>Single crochet border</option><option value="0">No border</option></select></div>
<div class="field"><label for="cdc-g">Your swatch: stitches per 4 in (optional)</label><input type="number" id="cdc-g" placeholder="leave blank for a typical gauge" min="6" max="26" step="0.5" inputmode="decimal"></div></div>
</div><div class="result" aria-live="polite" id="cdc-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a dishcloth, step by step</h2>
<div class="gq-figs">{cdc_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> 100 percent cotton in worsted weight (4). It's absorbent, takes hot washes and won't melt near a hot pan the way acrylic can. One 2 oz (57 g) ball of kitchen cotton makes about one 8 in single crochet cloth.</li>
<li><strong>Hook:</strong> 5 mm (H-8) for worsted cotton. Cotton has no stretch, so if your hands ache, go up half a size.</li>
<li><strong>Also:</strong> a tapestry needle and scissors. A stitch marker in the first and last stitch of each row helps keep the edges straight.</li></ul>
<p>New to crochet? The <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a> guide shows chain, single, half double and double crochet step by step, and <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a> shows a secure finish.</p>
<h2>Which crochet stitch is best for a dishcloth?</h2>
<ul><li><strong>Single crochet:</strong> dense and scrubby, the best all-rounder and the easiest to learn.</li>
<li><strong>Moss stitch (also called linen stitch):</strong> single crochet and chain 1, worked into the spaces. Flat, woven-looking and very pretty in two colours.</li>
<li><strong>Half double crochet:</strong> a little quicker than single, still firm.</li>
<li><strong>Double crochet:</strong> quickest and softest, but with gaps: better for a washcloth than for scrubbing pans.</li></ul>
<h2>Why are the sides of my dishcloth uneven?</h2>
<p>Almost always it's the first or last stitch of the row. Either the turning chain is being counted as a stitch when it shouldn't be, or the last stitch is being missed. Put a marker in the first and last stitch of each row, and count every few rows. If the cloth is getting wider, you're adding a stitch; narrower, you're losing one. A border round the outside hides small wobbles.</p>
<h2>Gift and selling ideas</h2>
<p>A set of three cloths in matching colours, tied with twine round a bar of handmade soap, is one of the most popular craft fair gifts. Working out a price? See <a href="{href("how-to-price-crochet-items.html")}">how to price crochet items</a> and typical prices in <a href="{href("christmas-crafts-to-sell.html")}">Christmas crafts to make and sell</a>. Knitting instead? Try <a href="{href("how-to-knit-a-dishcloth.html")}">how to knit a dishcloth</a>.</p>
<p class="note">Steps, writer and drawings are our own. Construction checked against EasyCrochet, Sigoni Macaroni and Handy Little Me beginner dishcloth patterns (29 Nov 2026); gauge from the Craft Yarn Council ranges. Stitch counts are exact for your gauge; rows, yarn and hours are estimates.</p>
</div></div></section>'''
cdc_faq = [
    ("How do you crochet a dishcloth for beginners?", "Chain about 29 in worsted cotton, single crochet in the second chain from the hook and in each chain across, then chain 1, turn and single crochet in every stitch until the cloth is square (about 8 in). Add a single crochet border with 3 stitches in each corner."),
    ("How many chains do I need for a crochet dishcloth?", "For an 8 in single crochet dishcloth in worsted cotton, about 28 stitches plus 1 turning chain, so chain 29. The writer works it out for any size, stitch and yarn."),
    ("What is the best yarn for crochet dishcloths?", "100 percent cotton in worsted weight. It's absorbent, takes hot washes and won't melt near a hot pan."),
    ("How much yarn does a crochet dishcloth take?", "About 50 to 75 yards of worsted cotton for an 8 in single crochet dishcloth, by our estimates. Double crochet uses a little less; a border adds about 8 yards."),
    ("What size hook do I use for a crochet dishcloth?", "A 5 mm (H-8) hook for worsted cotton, or 4 mm (G-6) for DK cotton."),
    ("What is the best crochet stitch for dishcloths?", "Single crochet for scrubbing, moss (linen) stitch for a flat woven look, and half double or double crochet for a softer, quicker cloth."),
]
SHOP_FOR["how-to-crochet-a-dishcloth.html"] = ["crochet-knitting-pricing-calculator", "small-business-pricing-inventory-spreadsheet", "yarn-stash-tracker", "christmas-gift-planner-budget"]
page("how-to-crochet-a-dishcloth.html", "How to Crochet a Dishcloth for Beginners (Free Pattern, Any Size)",
     "How to crochet a dishcloth for beginners: six drawn steps and a pattern writer for any size, yarn and stitch, with starting chain, rows, border and yarn, US or UK terms.",
     cdc, cdc_faq, "How to crochet a dishcloth", app_name="Crochet dishcloth pattern writer")
