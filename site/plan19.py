# ---------------- 28 Nov 2026 run 19: HOW TO KNIT A CHRISTMAS STOCKING + SAFETY EYES SIZE CHART + HOW TO MAKE A JUNK JOURNAL COVER ----------------
# Executed from build.py after plan18.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 28 Nov run 19). Patterns, drawings and wording our own. JS in assets/app.js (xks-*, sey-*, jjc-*).


# ======== HOW TO KNIT A CHRISTMAS STOCKING (flat, two pieces, no heel turn) ========
# Demand: T5 'how to knit a christmas stocking for beginners' (SERP 28 Nov: Hobbycraft how-to, Skillshare flat stocking class x3,
# Mary Maxim KAL weeks x6, Briana K free pattern, Purl Soho, Ravelry listings, Cardigang kit). Sizes = the same table as
# /christmas-stocking-calculator (height, width, foot, cuff). Gauge = CYC knit ranges; rows 1.35 x sts/in; garter rows 1.9 x sts/in.

def _xks_svg(step, label):
    R, W, G = _BERRY, "#fbfcfa", _TEAL
    boot = 'M70 30 h80 v86 h56 q16 0 16 16 v18 q0 12 -12 12 h-120 q-20 0 -20 -20 z'
    if step == 1:
        s = (f'<rect x="70" y="30" width="80" height="26" rx="2" fill="{W}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M74 {36 + j * 6} h72" stroke="#c9ccc4" stroke-width="2"/>' for j in range(4))
             + f'<line x1="60" y1="30" x2="160" y2="30" stroke="{_WOOD}" stroke-width="6" stroke-linecap="round"/>'
             + f'<text x="140" y="90" {_T12} text-anchor="middle">cast on, knit a garter cuff</text>'
             + f'<text x="140" y="108" {_T12} text-anchor="middle">(in white, for a classic look)</text>')
    elif step == 2:
        s = (f'<rect x="70" y="30" width="80" height="20" fill="{W}" stroke="{_INK}" stroke-width="2"/><rect x="70" y="50" width="80" height="90" fill="{R}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{76 + i * 12} {56 + j * 12} l6 9 l6 -9" fill="none" stroke="#e47aa3" stroke-width="2"/>' for i in range(6) for j in range(7))
             + f'<text x="210" y="96" {_T12} text-anchor="middle">knit the leg</text><text x="210" y="112" {_T12} text-anchor="middle">in stockinette</text>')
    elif step == 3:
        s = (f'<rect x="40" y="30" width="80" height="20" fill="{W}" stroke="{_INK}" stroke-width="2"/><rect x="40" y="50" width="80" height="80" fill="{R}" stroke="{_INK}" stroke-width="2"/>'
             f'<rect x="120" y="110" width="70" height="20" fill="none" stroke="{_INK}" stroke-width="2" stroke-dasharray="5 4"/>'
             f'<path d="M190 100 v-20 h40" fill="none" stroke="{_GOLD}" stroke-width="3"/><path d="M196 92 l-6 -12 l-6 12" fill="{_GOLD}"/>'
             f'<text x="150" y="160" {_T12} text-anchor="middle">cast on extra stitches for the toe</text>')
    elif step == 4:
        s = (f'<path d="{boot}" fill="{R}" stroke="{_INK}" stroke-width="2"/><rect x="70" y="30" width="80" height="20" fill="{W}" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M50 150 q-6 -4 -2 -12" fill="none" stroke="{_GOLD}" stroke-width="3"/><path d="M226 150 q8 -4 4 -14" fill="none" stroke="{_GOLD}" stroke-width="3"/>'
             f'<text x="140" y="186" {_T12} text-anchor="middle">decrease both ends to round heel and toe</text>')
    elif step == 5:
        s = (f'<g transform="translate(-22 30) scale(.62)"><path d="{boot}" fill="{R}" stroke="{_INK}" stroke-width="3"/></g>'
             f'<g transform="translate(302 30) scale(-.62 .62)"><path d="{boot}" fill="#d9567f" stroke="{_INK}" stroke-width="3"/></g>'
             f'<text x="140" y="190" {_T12} text-anchor="middle">knit a mirror piece: toe the other way</text>')
    else:
        s = (f'<path d="{boot}" fill="{R}" stroke="{_INK}" stroke-width="2"/><rect x="70" y="30" width="80" height="20" fill="{W}" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="{boot}" fill="none" stroke="{_GOLD}" stroke-width="2" stroke-dasharray="3 5" transform="translate(0 0)"/>'
             f'<path d="M78 30 q-8 -22 10 -22 q14 0 4 22" fill="none" stroke="{_TEAL}" stroke-width="4"/>'
             f'<text x="140" y="186" {_T12} text-anchor="middle">sew round the edge, add a hanging loop</text>')
    return _svg12(s, label)


XKS_STEPS = [(1, "1. Cast on and knit the cuff", "Cast on the number the writer gives you with the long-tail cast on. Knit every row for the cuff (garter stitch), so it lies flat and doesn't curl. White yarn here gives the classic look."),
             (2, "2. Knit the leg", "Join the main colour at the start of a right-side row. Knit one row, purl one row (stockinette) until the piece reaches the start of the foot. Stripes are easy: change colour at the start of a right-side row."),
             (3, "3. Add the toe stitches", "At the start of the next right-side row, cast on the extra toe stitches with the cable or knitted cast on, then knit across all of them. The piece turns into an L, like a boot."),
             (4, "4. Round the heel and toe", "Work the foot straight, then decrease one stitch at each end of every right-side row a few times (k2tog at the start, ssk at the end). This rounds both bottom corners. Bind off."),
             (5, "5. Knit the second piece", "Knit a second piece the same way, but cast on the toe stitches at the start of a wrong-side row instead. Its toe points the other way, so the two pieces match up as a front and a back."),
             (6, "6. Sew it together", "Lay the pieces right sides together, pin, and sew all round the edge except the top with mattress or back stitch. Turn it right side out, add a hanging loop at the heel side and weave in the ends.")]
xks_cards = "".join(f'<figure class="gq-fig"><div>{_xks_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in XKS_STEPS)

xks = top("How to knit a Christmas stocking for beginners", "This stocking is knitted flat in two simple pieces: no double-pointed needles, no heel flap and no heel turn. If you can knit, purl and decrease, you can make it. Every step is drawn below, and the writer turns any size and yarn into a full row-by-row pattern with yarn amounts.", "How to knit a Christmas stocking") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the easiest way to knit a Christmas stocking is <strong>flat, in two boot-shaped pieces</strong>. Cast on about 32 stitches in worsted yarn, knit a garter cuff, then the leg in stockinette; <strong>cast on extra stitches for the toe</strong>, knit the foot, <strong>decrease at both ends</strong> to round the heel and toe, and bind off. Knit a mirror piece, then sew them together. A classic 18 in stocking takes roughly 180 to 250 yards of worsted and 8 to 12 hours, by our estimates.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Flat Christmas stocking pattern writer</h3>
<div class="row2"><div class="field"><label for="xks-z">Size</label><select id="xks-z"><option value="mini">Mini ornament (7 in tall)</option><option value="small">Small or child (12 in)</option><option value="standard" selected>Classic (18 in)</option><option value="large">Large (22 in)</option><option value="xl">Extra large (26 in)</option></select></div>
<div class="field"><label for="xks-y">Yarn</label><select id="xks-y"><option value="3">DK / light (3)</option><option value="4" selected>Worsted / aran (4)</option><option value="5">Chunky / bulky (5)</option><option value="6">Super bulky (6)</option></select></div></div>
<div class="row2"><div class="field"><label for="xks-g">Your swatch: stitches per 4 in (optional)</label><input type="number" id="xks-g" placeholder="leave blank for a typical gauge" min="6" max="32" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="xks-c">Cuff</label><select id="xks-c"><option value="garter" selected>Garter (knit every row)</option><option value="rib">K1, p1 rib</option></select></div></div>
</div><div class="result" aria-live="polite" id="xks-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to knit a Christmas stocking, step by step</h2>
<div class="gq-figs">{xks_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> worsted (4) acrylic or wool blend in red or green for the body, plus white for the cuff, heel or toe if you like. Acrylic is cheap, washable and holds its shape. Chunky yarn knits up twice as fast.</li>
<li><strong>Needles:</strong> straight needles, or a circular needle used flat, in the size on the yarn label: about US 8 (5 mm) for worsted, US 10.5 (6.5 mm) for chunky.</li>
<li><strong>Also:</strong> a tapestry needle to sew it up, a few pins or clips, scissors and a tape measure.</li></ul>
<p>New to knitting? Learn <a href="{href("how-to-cast-on-knitting.html")}">how to cast on</a> and <a href="{href("how-to-knit-and-purl.html")}">how to knit and purl</a> first. Every other skill is explained in the steps.</p>
<h2>Why knit a stocking flat?</h2>
<p>A traditional stocking is knitted in the round with a heel flap, a turned heel and a gusset, just like a big sock. It looks lovely but needs double-pointed needles or magic loop, and the heel is where most beginners get stuck. Knitting two flat pieces avoids all of that: you only work straight rows, cast on a few stitches, and decrease at the edges. The heel and toe come out rounded because of the decreases. Once you've made this one, the <a href="{href("christmas-stocking-calculator.html")}">Christmas stocking calculator</a> gives cast-on and heel numbers for knitting one in the round.</p>
<h2>How to add stripes, a name or a white heel and toe</h2>
<ul><li><strong>Stripes:</strong> change colour at the start of a right-side row. Carry the yarn not in use up the side if the stripes are 4 rows or less; otherwise cut it and weave in. Our <a href="{href("stripe-generator.html")}">stripe generator</a> makes random stripe orders.</li>
<li><strong>White heel and toe:</strong> on the foot rows, knit the first and last 8 to 10 stitches in white and the middle in red, twisting the yarns where they meet so there's no hole. Or keep it simple: knit the whole foot in white.</li>
<li><strong>A name:</strong> it's easiest to embroider the name onto the cuff afterwards with duplicate stitch or chain stitch (see our <a href="{href("embroidery-stitches.html")}">embroidery stitches</a>). The stocking calculator checks if a name fits the cuff.</li></ul>
<h2>Sewing the pieces together</h2>
<p>Weave in all the ends first, except one long tail for sewing. Put the pieces right sides together, line up the cuffs, and pin every inch or so. Back stitch about one stitch in from the edge, all the way round the leg, heel, foot and toe, leaving the top open. Turn it right side out and push the toe out gently. For an invisible seam, lay them right side up and use mattress stitch instead. For the hanging loop, knit a 3-stitch i-cord or crochet a 25-chain loop and sew both ends inside the cuff at the heel side. Need more help? See <a href="{href("hand-sewing-stitches.html")}">hand sewing stitches</a> and <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>.</p>
<h2>How long does it take to knit a Christmas stocking?</h2>
<p>As a rough guide for a comfortable beginner (our estimates), a mini ornament stocking takes 1 to 2 hours, a child's stocking 4 to 6 and a classic 18 in stocking 8 to 12 hours in worsted, plus an hour to sew up. Chunky yarn is about a third quicker. Making several as gifts? Check your deadline in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade Christmas gift planner</a>, and if you'll sell them, price them with the <a href="{href("how-to-price-crochet-items.html")}">pricing guide</a> (it works for knitting too).</p>
<p class="note">Method is our own two-piece design, checked against common beginner stocking construction (Hobbycraft, Skillshare's flat stocking class, Mary Maxim's stocking knit-along; 28 Nov 2026). Sizes match our <a href="{href("christmas-stocking-calculator.html")}">stocking size chart</a>; gauge from the Craft Yarn Council ranges. Yarn and hours are estimates.</p>
</div></div></section>'''
xks_faq = [
    ("How do you knit a Christmas stocking for beginners?", "Knit it flat in two boot-shaped pieces: cast on, knit a garter cuff, knit the leg in stockinette, cast on extra stitches for the toe, knit the foot, decrease at both ends to round the heel and toe, and bind off. Knit a mirror piece and sew them together."),
    ("Can you knit a Christmas stocking on straight needles?", "Yes. The flat two-piece method uses straight needles only: no double-pointed needles, heel flap or heel turn."),
    ("How many stitches do I cast on for a Christmas stocking?", "For a classic 18 in stocking knitted flat in two pieces, about 32 stitches per piece in worsted yarn (18 stitches per 4 in), or 24 in chunky. Knitted in the round it's about 64 in worsted."),
    ("How much yarn do I need to knit a Christmas stocking?", "Roughly 180 to 250 yards of worsted yarn for a classic 18 in stocking, by our estimates: buy two 200-yard balls, one for the body and one for the cuff, heel and toe."),
    ("What is the best yarn for a knitted Christmas stocking?", "Worsted or chunky acrylic, or a wool blend. It's sturdy, keeps its shape when filled, and comes in bright reds, greens and white."),
    ("How long does it take to knit a Christmas stocking?", "About 8 to 12 hours for a classic 18 in stocking in worsted yarn for a beginner, plus an hour to sew it up (our estimates). Chunky yarn is quicker."),
]
SHOP_FOR["how-to-knit-a-christmas-stocking.html"] = ["christmas-gift-tags", "christmas-gift-planner-budget", "crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner"]
page("how-to-knit-a-christmas-stocking.html", "How to Knit a Christmas Stocking for Beginners (Flat Pattern)",
     "How to knit a Christmas stocking for beginners, flat in two pieces with no heel turn: six drawn steps and a pattern writer for any size and yarn.",
     xks, xks_faq, "How to knit a Christmas stocking", app_name="Flat Christmas stocking pattern writer")


# ======== SAFETY EYES SIZE CHART ========
# Demand: R9 'safety eyes size chart' / 'what size safety eyes for amigurumi' (SERP 28 Nov: three spam mirror pages titled 'Safety Eyes Size Chart',
# PlanetJune crocheted-eyes table, Repeat Crafter Me favourites, CrochetKim, Discount Craft how-to, Ribblr forum threads, shop listings; no chart
# by yarn weight + head size). Facts: sizes are the eye diameter; 6-12 mm small toys, 12-30 mm large/bulky (Repeat Crafter Me); 12 mm or less small,
# 18-20 mm bigger toys (Discount Craft); washers snap on, near impossible to remove; not for under 3s or pets: embroider (both). Proportions are ours.

def _sey_svg(step, label):
    head = f'<circle cx="140" cy="92" r="62" fill="#f2e3cf" stroke="{_INK}" stroke-width="2"/>' + "".join(f'<path d="M{86 + i * 9} {60 + (i % 2) * 2} q4 4 8 0" fill="none" stroke="#d9c4a7" stroke-width="1.5"/>' for i in range(12))
    if step == 1:
        s = (head + f'<line x1="78" y1="100" x2="202" y2="100" stroke="{_GOLD}" stroke-width="2" stroke-dasharray="4 4"/>'
             + f'<circle cx="114" cy="100" r="7" fill="{_INK}"/><circle cx="166" cy="100" r="7" fill="{_INK}"/>'
             + f'<text x="140" y="180" {_T12} text-anchor="middle">push the posts in between two stitches</text>')
    elif step == 2:
        s = (head + f'<circle cx="114" cy="100" r="7" fill="{_INK}"/><circle cx="166" cy="100" r="7" fill="{_INK}"/>'
             + f'<path d="M122 100 h22" stroke="{_BERRY}" stroke-width="2"/><path d="M144 96 v8" stroke="{_BERRY}" stroke-width="2"/><path d="M122 96 v8" stroke="{_BERRY}" stroke-width="2"/>'
             + f'<text x="140" y="180" {_T12} text-anchor="middle">check spacing and the look before snapping</text>')
    elif step == 3:
        s = (f'<rect x="40" y="88" width="80" height="12" fill="#f2e3cf" stroke="{_INK}" stroke-width="1.5"/><circle cx="34" cy="94" r="14" fill="{_INK}"/><rect x="46" y="91" width="100" height="6" fill="#6b6f7a"/>'
             + "".join(f'<line x1="{120 + i * 6}" y1="89" x2="{120 + i * 6}" y2="99" stroke="#9ea2ab" stroke-width="1"/>' for i in range(5))
             + f'<path d="M168 72 v44 q-14 -4 -14 -22 q0 -18 14 -22 z" fill="#d7dade" stroke="{_INK}" stroke-width="1.5"/><path d="M190 94 h-18" stroke="{_GOLD}" stroke-width="3"/><path d="M174 88 l-8 6 l8 6" fill="{_GOLD}"/>'
             + f'<text x="140" y="150" {_T12} text-anchor="middle">washer on the inside, flat side to the fabric</text><text x="140" y="168" {_T12} text-anchor="middle">push until it clicks</text>')
    else:
        s = (head + "".join(f'<path d="M{108 + k * 52} 100 m-9 0 l3 -5 l3 5 l3 -5 l3 5 l3 -5" fill="none" stroke="{_INK}" stroke-width="2.5"/>' for k in range(2))
             + f'<path d="M128 122 q12 10 24 0" fill="none" stroke="{_BERRY}" stroke-width="2.5"/>'
             + f'<text x="140" y="180" {_T12} text-anchor="middle">for babies and pets: embroider the eyes</text>')
    return _svg12(s, label)


SEY_STEPS = [(1, "1. Place the eyes", "Before you stuff the head, push the eye posts through from the outside, in the gap between two stitches. Most patterns put them a little below the middle of the head."),
             (2, "2. Check before you snap", "Count the stitches between the eyes so both sides match, and look at the face from a step away. Moving them now is easy; later it isn't."),
             (3, "3. Snap on the washers", "On the inside, slide the washer onto the post with its flat side towards the fabric and press until it clicks. It should hold the eye firm without squashing the stitches."),
             (4, "4. Or embroider instead", "For babies, toddlers under 3 and pets, skip safety eyes. Embroider eyes with black yarn, or sew on felt circles very securely.")]
sey_cards = "".join(f'<figure class="gq-fig"><div>{_sey_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in SEY_STEPS)
SEY_ROWS = [("Fingering / thread (1)", "4 to 6 mm", "6 to 8 mm", "keyrings, tiny animals"), ("Sport / DK (2-3)", "6 to 8 mm", "8 to 12 mm", "small toys, about 4 to 6 in"),
            ("Worsted / aran (4)", "8 to 10 mm", "10 to 15 mm", "most patterns, 6 to 10 in toys"), ("Chunky / bulky (5)", "12 mm", "14 to 20 mm", "bigger toys, 10 to 14 in"),
            ("Super bulky / chenille (6-7)", "15 to 18 mm", "18 to 30 mm", "plush and jumbo toys, 12 in and up")]
sey_table = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>" for a, b, c, d in SEY_ROWS)
_sey_mm = "".join(f'<option value="{m}">{m} mm</option>' for m in (4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24, 30))

sey = top("Safety eyes size chart for amigurumi", "Which size safety eyes should you buy? Start from the chart by yarn weight, then use the helper: give it the stitches in your head's widest round, and it works out the head size and draws the face at actual size with different eyes, so you can see the look before you snap anything in.", "Safety eyes size chart") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> safety eyes are sized by the <strong>diameter of the eye in mm</strong>. As a starting point (our guide, by yarn weight): <strong>6 to 8 mm</strong> for fingering or thread, <strong>8 to 12 mm</strong> for DK, <strong>10 to 15 mm</strong> for worsted, <strong>14 to 20 mm</strong> for chunky and <strong>18 to 30 mm</strong> for super bulky or chenille plush. Bigger eyes look younger and cuter; smaller eyes look more realistic. Don't use safety eyes on toys for children under 3 or pets: embroider the eyes instead.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Safety eye size helper</h3>
<div class="row2"><div class="field"><label for="sey-y">Yarn</label><select id="sey-y"><option value="1">Fingering / thread (1)</option><option value="3">Sport / DK (2-3)</option><option value="4" selected>Worsted / aran (4)</option><option value="5">Chunky / bulky (5)</option><option value="6">Super bulky / chenille (6-7)</option></select></div>
<div class="field"><label for="sey-s">Stitches in the widest round of the head</label><input type="number" id="sey-s" value="42" min="12" max="180" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="sey-l">Look</label><select id="sey-l"><option value="cute" selected>Cute (big eyes, kawaii)</option><option value="classic">Classic</option><option value="real">Realistic (small eyes)</option></select></div>
<div class="field"><label for="sey-m">Try an eye size</label><select id="sey-m"><option value="auto" selected>Suggest for me</option>{_sey_mm}</select></div></div>
</div><div class="result" aria-live="polite" id="sey-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Safety eyes size chart by yarn weight</h2>
<div class="tbl"><table class="mt"><thead><tr><th>Yarn</th><th>Realistic look</th><th>Cute look</th><th>Typical toy</th></tr></thead><tbody>{sey_table}</tbody></table></div>
<p>These are starting points, not rules: our own guide built from what amigurumi makers and suppliers recommend (smaller eyes for small toys, 12 to 30 mm for big or bulky ones). Your hook size and tension change the size of the head, and the head's size matters more than the yarn. If you're between two sizes, the helper above shows both side by side at actual size.</p>
<h2>How to choose the right size</h2>
<ul><li><strong>Head size first.</strong> A head with 36 stitches in its widest round is small; one with 60 or more is big, whatever the yarn. The helper turns stitches into a real diameter using a typical gauge for your yarn.</li>
<li><strong>Cute or realistic?</strong> For a kawaii look, the eye is roughly a fifth of the head's width and set wide and low. For a realistic animal, try about a tenth, set higher and a little closer. These proportions are our own design tips.</li>
<li><strong>Common sizes.</strong> 6, 8, 9, 10, 12, 15, 18 and 24 mm are the easiest to find. Many makers keep 10 to 14 mm in stock because they suit most worsted patterns.</li>
<li><strong>Test before you click.</strong> Push the eyes in without washers, pin them, and look from a few steps away. Take a photo: faces are easier to judge on a screen.</li></ul>
<h2>Where to put safety eyes on amigurumi</h2>
<p>Follow your pattern if it gives a round. If not, start a round or two below the middle of the head for a cute face (the widest rounds are a good guide), with about one and a half eye widths between them. Count the stitches between the eyes so both sides are the same, and check they sit on the same round. Put the eyes in <strong>before</strong> you stuff and close the head: once the washer is on, it's very hard to get off without cutting the post.</p>
<h2>How to put safety eyes in, step by step</h2>
<div class="gq-figs">{sey_cards}</div>
<h2>Are safety eyes safe for babies?</h2>
<p>No: the name is misleading. Safety eyes lock with a washer, but they can still be pulled or chewed out, and a loose eye is a choking hazard. Makers and suppliers advise against them for children under 3 and for pets. Embroider the eyes with black yarn or thread, or use felt sewn on very firmly. If you sell toys, toy safety rules apply where you sell (in the US, the CPSIA; in the UK and EU, the toy safety regulations and CE or UKCA marking), so check them before you list. Our <a href="{href("how-to-price-amigurumi.html")}">amigurumi pricing guide</a> has more on selling toys.</p>
<h2>Safety eye colours and types</h2>
<p>Plain black eyes come in two pieces: the eye and the washer. Coloured eyes often have three: the clear eye, a coloured disc behind it and the washer. Put the disc on with the colour facing the eye. There are also oval eyes, cat-slit eyes, glitter eyes and matching safety noses, which go on the same way. Metal washers hold tighter than plastic but are harder to fit; a washer tool or a cotton reel helps you press evenly.</p>
<p>Making your first toy? Start with our <a href="{href("amigurumi.html")}">amigurumi guide</a>, the <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>, the <a href="{href("crochet-circle-calculator.html")}">crochet circle and ball calculator</a> for the head, and the <a href="{href("how-to-crochet-decrease.html")}">invisible decrease</a> to close it. Or try our <a href="{href("crochet-sheep-pattern.html")}">free crochet sheep pattern</a>.</p>
<p class="note">Sources: Repeat Crafter Me (safety eyes and noses, 2026), Discount Craft (how to use safety eyes, 2024), CrochetKim (amigurumi eyes), PlanetJune (crocheted eyes, 2025), checked 28 Nov 2026. The chart ranges, proportions and head-size maths (typical single crochet gauge for each yarn) are our own estimates; your toy may differ.</p>
</div></div></section>'''
sey_faq = [
    ("What size safety eyes should I use for amigurumi?", "As a starting point: 6 to 8 mm for fingering, 8 to 12 mm for DK, 10 to 15 mm for worsted, 14 to 20 mm for chunky and 18 to 30 mm for super bulky. Smaller for a realistic look, bigger for a cute one."),
    ("What size safety eyes for worsted weight yarn?", "Usually 10 to 15 mm for a cute look on a 6 to 10 in toy, or 8 to 10 mm for a more realistic animal. 12 mm is a popular all-rounder."),
    ("How are safety eyes measured?", "By the diameter of the visible eye in millimetres, not including the post."),
    ("Can you remove safety eyes once they are in?", "Not easily: the washer locks onto the ridges of the post. You usually have to cut the post. Place and check the eyes before you push the washer on."),
    ("Are safety eyes safe for babies?", "No. They can come out if pulled or chewed and are a choking hazard, so they aren't recommended for children under 3 or pets. Embroider the eyes instead."),
    ("Where do you put safety eyes on a crochet head?", "Follow the pattern, or start a round or two below the middle of the head, about one and a half eye widths apart, and put them in before stuffing."),
]
SHOP_FOR["safety-eyes-size-chart.html"] = ["crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-tags"]
page("safety-eyes-size-chart.html", "Safety Eyes Size Chart for Amigurumi (+ Actual-Size Helper)",
     "What size safety eyes for amigurumi? A size chart by yarn weight, a helper that draws your toy's head at actual size, and how to put them in.",
     sey, sey_faq, "Safety eyes size chart", app_name="Safety eye size helper")


# ======== HOW TO MAKE A JUNK JOURNAL COVER ========
# Demand: 'how to make a junk journal cover' / 'junk journal cover from cereal box' (SERP 28 Nov: Instructables recycled journal x2, Make: cereal box
# journal x2, 101 Planners step-by-step + cover ideas, Crafty Chica, Book Riot, Art in Context, Scholastic, WonderHowTo, Udemy Amazon-box course,
# The Long Thread; no cover size calculator). Bookbinding conventions: boards overhang the pages ~1/8 in (3 mm) on 3 sides; spine = text block +
# board thickness allowance; covering turns in 3/4 in (2 cm); hinge gap ~2 board thicknesses. Paper thickness: printer paper ~0.004 in.

def _jjc_svg(step, label):
    B = "#c9a77c"
    if step == 1:
        s = (f'<rect x="30" y="40" width="70" height="100" fill="{B}" stroke="{_INK}" stroke-width="2"/><rect x="108" y="40" width="22" height="100" fill="{B}" stroke="{_INK}" stroke-width="2"/><rect x="138" y="40" width="70" height="100" fill="{B}" stroke="{_INK}" stroke-width="2"/>'
             f'<text x="65" y="94" {_T12} text-anchor="middle">back</text><text x="119" y="94" {_T12} text-anchor="middle" font-size="10">spine</text><text x="173" y="94" {_T12} text-anchor="middle">front</text>'
             f'<path d="M226 40 v100" stroke="{_BERRY}" stroke-width="2"/><path d="M220 40 h12 M220 140 h12" stroke="{_BERRY}" stroke-width="2"/>'
             f'<text x="140" y="172" {_T12} text-anchor="middle">cut two boards and a spine</text>')
    elif step == 2:
        s = (f'<rect x="20" y="26" width="240" height="128" fill="#e9d9e8" stroke="{_INK}" stroke-width="2"/>'
             f'<rect x="38" y="44" width="70" height="92" fill="{B}" stroke="{_INK}" stroke-width="1.5"/><rect x="116" y="44" width="22" height="92" fill="{B}" stroke="{_INK}" stroke-width="1.5"/><rect x="146" y="44" width="70" height="92" fill="{B}" stroke="{_INK}" stroke-width="1.5"/>'
             f'<path d="M108 52 h8 M138 52 h8" stroke="{_BERRY}" stroke-width="2"/>'
             f'<text x="140" y="178" {_T12} text-anchor="middle">glue onto the cover paper, leave hinge gaps</text>')
    elif step == 3:
        s = (f'<path d="M20 26 h240 v128 h-240 z" fill="#e9d9e8" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M20 26 l18 18 M260 26 l-18 18 M20 154 l18 -18 M260 154 l-18 -18" stroke="{_INK}" stroke-width="2"/>'
             f'<rect x="38" y="44" width="204" height="92" fill="{B}" stroke="{_INK}" stroke-width="1.5"/>'
             f'<path d="M38 44 h204 v92 h-204 z" fill="none" stroke="{_GOLD}" stroke-width="3" stroke-dasharray="6 5"/>'
             f'<text x="140" y="178" {_T12} text-anchor="middle">cut the corners, fold and glue the edges</text>')
    elif step == 4:
        s = (f'<rect x="38" y="44" width="204" height="92" fill="#e9d9e8" stroke="{_INK}" stroke-width="2"/>'
             f'<rect x="46" y="52" width="88" height="76" fill="#fbf8f1" stroke="{_INK}" stroke-width="1"/><rect x="146" y="52" width="88" height="76" fill="#fbf8f1" stroke="{_INK}" stroke-width="1"/>'
             f'<text x="140" y="178" {_T12} text-anchor="middle">glue in lining papers to hide the edges</text>')
    elif step == 5:
        s = (f'<rect x="38" y="44" width="204" height="92" fill="#e9d9e8" stroke="{_INK}" stroke-width="2"/><rect x="129" y="44" width="22" height="92" fill="#d7bdd5" stroke="{_INK}" stroke-width="1.5"/>'
             + "".join(f'<circle cx="{134 + k * 12}" cy="{y}" r="2.5" fill="{_INK}"/>' for k in range(2) for y in (60, 90, 120))
             + f'<text x="140" y="178" {_T12} text-anchor="middle">pierce 3 holes per signature in the spine</text>')
    else:
        s = (f'<path d="M60 40 l80 -10 v120 l-80 10 z" fill="#e9d9e8" stroke="{_INK}" stroke-width="2"/><path d="M140 30 l80 10 v120 l-80 -10 z" fill="#d7bdd5" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M140 30 v120" stroke="{_INK}" stroke-width="3"/>'
             + "".join(f'<path d="M{70 + i * 4} {50 + i} l66 -8" stroke="#fbf8f1" stroke-width="2"/>' for i in range(3))
             + f'<path d="M210 96 q22 -4 30 18" fill="none" stroke="{_BERRY}" stroke-width="3"/>'
             + f'<text x="140" y="186" {_T12} text-anchor="middle">sew in the signatures, add a tie</text>')
    return _svg12(s, label)


JJC_STEPS = [(1, "1. Cut the boards", "Cut a front and back board from a cereal box, cardboard or chipboard, each a little bigger than your pages, and a spine strip as wide as your stack of signatures. The calculator gives every size."),
             (2, "2. Glue to the covering", "Lay the cover paper or fabric face down. Glue the back board, the spine and the front board onto it in a row, with a small gap on each side of the spine so the cover can open."),
             (3, "3. Fold the edges in", "Cut each corner off at an angle, leaving a board's thickness of paper at the point. Glue the long edges over the boards first, then tuck and glue the short ones."),
             (4, "4. Line the inside", "Glue a lining sheet (old book page, map, scrapbook paper) inside each board to hide the folded edges. Press it under a heavy book for an hour."),
             (5, "5. Pierce the spine", "Mark three holes for each signature down the spine, in rows spaced evenly across it, and pierce them with an awl or a thick needle from the inside."),
             (6, "6. Sew in and finish", "Sew each signature to the spine with a pamphlet stitch, then add a ribbon tie, a button and elastic, or a belly band to keep it closed.")]
jjc_cards = "".join(f'<figure class="gq-fig"><div>{_jjc_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in JJC_STEPS)

jjc = top("How to make a junk journal cover", "A junk journal cover is just two boards, a spine and something pretty wrapped round them. A cereal box works perfectly. The steps are drawn below, and the cover size calculator works out the boards, spine, cover paper and hinge gaps for your page size and number of signatures, with a cutting diagram.", "How to make a junk journal cover") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to make a junk journal cover, <strong>cut two boards</strong> (cereal box or chipboard) about 1/4 in taller and 1/8 in wider than your pages, and a <strong>spine</strong> as wide as your stack of signatures. Glue them onto cover paper or fabric with a <strong>small gap each side of the spine</strong>, fold and glue the edges in, line the inside, then <strong>sew the signatures to the spine</strong>. For A5 pages and 4 signatures, cut boards about 6 x 8.5 in and a spine about 0.5 in.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Junk journal cover size calculator</h3>
<div class="row2"><div class="field"><label for="jjc-p">Page size (folded)</label><select id="jjc-p"><option value="5.83x8.27">A5 (5.8 x 8.3 in)</option><option value="5.5x8.5" selected>Half letter (5.5 x 8.5 in)</option><option value="4.13x5.83">A6 (4.1 x 5.8 in)</option><option value="4.25x5.5">Quarter letter (4.25 x 5.5 in)</option><option value="8.27x11.69">A4 (8.3 x 11.7 in)</option><option value="6x9">6 x 9 in</option><option value="custom">My own size</option></select></div>
<div class="field" id="jjc-own" hidden><label for="jjc-w">Page width x height (in)</label><div class="row2"><input type="number" id="jjc-w" value="5" min="2" max="14" step="0.05" inputmode="decimal" aria-label="Page width in inches"><input type="number" id="jjc-h" value="7" min="2" max="16" step="0.05" inputmode="decimal" aria-label="Page height in inches"></div></div></div>
<div class="row2"><div class="field"><label for="jjc-n">Signatures</label><input type="number" id="jjc-n" value="4" min="1" max="12" inputmode="numeric"></div>
<div class="field"><label for="jjc-s">Sheets per signature (folded in half)</label><input type="number" id="jjc-s" value="6" min="1" max="20" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="jjc-t">Paper</label><select id="jjc-t"><option value="0.004">Printer paper (20-24 lb, 75-90 gsm)</option><option value="0.006" selected>Mixed: printer, book pages, some card</option><option value="0.009">Cardstock, tea-dyed or watercolour paper</option></select></div>
<div class="field"><label for="jjc-b">Cover board</label><select id="jjc-b"><option value="0.02" selected>Cereal box (thin)</option><option value="0.05">Shipping box cardboard</option><option value="0.07">Chipboard / book board</option></select></div></div>
<div class="field"><label for="jjc-x">Extra bulk from tuck spots, pockets and ephemera</label><select id="jjc-x"><option value="1">None (flat pages)</option><option value="1.5" selected>Some (a few pockets and tags)</option><option value="2">Lots (chunky, stuffed journal)</option></select></div>
</div><div class="result" aria-live="polite" id="jjc-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to make a junk journal cover, step by step</h2>
<div class="gq-figs">{jjc_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Board:</strong> a cereal or cracker box for a soft, bendy cover; a shipping box or chipboard for a stiff, book-like one. Cut away any creases or folds.</li>
<li><strong>Covering:</strong> scrapbook paper, wrapping paper, an old map, a pretty paper bag, cotton fabric or faux leather. Paper should be thin enough to fold round the board edges.</li>
<li><strong>Glue:</strong> PVA (white craft glue) or a glue stick for paper; spray adhesive or fabric glue for fabric. Spread it thin with an old card so it doesn't wrinkle.</li>
<li><strong>Tools:</strong> ruler, pencil, craft knife or scissors, bone folder or the back of a spoon, an awl or thick needle, waxed thread or embroidery floss.</li></ul>
<h2>How big should a junk journal cover be?</h2>
<p>Each board should stick out past the pages by about <strong>1/8 in (3 mm)</strong> at the top, bottom and the outer edge. That little overhang is called the square, and it protects the page edges. So a board is your page width plus 1/8 in, and your page height plus 1/4 in. The spine is the thickness of all your signatures, plus room for whatever you'll tuck in. Junk journals always get fatter as you fill them, so the calculator adds extra for pockets and ephemera.</p>
<h2>Why leave a gap by the spine?</h2>
<p>If the boards touch the spine, the cover can't fold open. Leave a gap, called the hinge, of about twice the board's thickness, and at least 1/8 in, between each board and the spine. With thin cereal box board, a 1/8 in gap is plenty; with chipboard, go to 1/4 in. The cover paper bends along the gap like a hinge.</p>
<h2>Junk journal cover ideas</h2>
<ul><li><strong>An old hardback book:</strong> cut the pages out with a knife along the inside of the spine and keep the cover. Line it and sew new signatures in.</li>
<li><strong>Cereal box flip:</strong> cover the printed side with paper, or use the plain brown inside as a kraft cover and decorate it with stamps and collage.</li>
<li><strong>Fabric or tea-dyed muslin:</strong> glue it on like paper, folding the edges in. Add embroidery or a lace trim first. See <a href="{href("how-to-tea-stain-paper.html")}">how to tea stain paper</a> (it works on cotton too).</li>
<li><strong>Paper bag or envelope:</strong> crumple and flatten a brown paper bag for a soft leather look, then glue it on.</li>
<li><strong>Soft cover:</strong> skip the boards and fold heavy cardstock or a file folder around the signatures for a quick traveller's notebook style.</li>
<li><strong>Closures:</strong> a ribbon glued under the lining, a button with a loop of elastic, a belly band, or a tag on a long string wound round.</li></ul>
<h2>Sewing the signatures to the cover</h2>
<p>For each signature, pierce three holes down the spine: one in the middle and one about 1 in from each end. Use the same spacing in the fold of the signature. Sew with a pamphlet stitch: in through the middle hole, out through the top, back in through the bottom (skipping the middle), out through the middle again, and tie the ends round the long stitch. Space the rows of holes evenly across the spine (the calculator gives the spacing). Our <a href="{href("junk-journal-signature-calculator.html")}">junk journal signature calculator</a> plans how many pages go in each signature and how much thread you need, and <a href="{href("bookbinding.html")}">bookbinding</a> has stronger stitches like the long stitch.</p>
<p>New to junk journals? Start with <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a>, the <a href="{href("junk-journal-supply-checklist.html")}">supply checklist</a>, then fill it with <a href="{href("junk-journal-page-ideas.html")}">page ideas</a> and <a href="{href("junk-journal-pockets.html")}">pockets</a>.</p>
<p class="note">Method is standard book cover making (boards, square overhang, hinge gap, turn-ins), checked against Make: (cereal box journal), Instructables (recycled journal) and 101 Planners' junk journal guides (28 Nov 2026). Paper thicknesses and the bulk allowance are estimates; measure your stack with a ruler if you can.</p>
</div></div></section>'''
jjc_faq = [
    ("How do you make a junk journal cover?", "Cut two boards slightly bigger than your pages and a spine as wide as your signatures, glue them onto cover paper or fabric with a small gap either side of the spine, fold and glue the edges, line the inside and sew the signatures to the spine."),
    ("How big should a junk journal cover be?", "Each board should be about 1/8 in wider and 1/4 in taller than your pages, so they overhang by 1/8 in on three sides. The spine matches the thickness of your signatures plus room for tuck-ins."),
    ("Can you use a cereal box for a junk journal cover?", "Yes. Cereal box board is thin enough to cut with scissors and still stiff enough for a soft-bound journal. Cover the printed side with paper or use the plain inside."),
    ("How wide should the spine of a junk journal be?", "As thick as your stack of signatures plus extra for pockets and ephemera: about 1/2 in for 4 signatures of 6 sheets with a few tuck-ins. Junk journals get fatter as you fill them, so err wide."),
    ("What glue is best for a junk journal cover?", "PVA (white craft glue) spread thinly, or a strong glue stick for paper. Use spray adhesive or fabric glue for fabric covers."),
    ("How much paper do I need to cover a junk journal?", "Enough to cover both boards, the spine and the hinge gaps, plus 3/4 in on every side to fold in. For half letter pages with a 1/2 in spine that's about 13.5 x 10.25 in."),
]
SHOP_FOR["how-to-make-a-junk-journal-cover.html"] = ["tea-room-junk-journal-kit", "winter-cottage-junk-journal-kit", "vintage-ephemera-pack", "junk-journal-mega-bundle"]
page("how-to-make-a-junk-journal-cover.html", "How to Make a Junk Journal Cover (+ Cover Size Calculator)",
     "How to make a junk journal cover from a cereal box or chipboard: six drawn steps and a calculator for boards, spine, cover paper and hinge gaps.",
     jjc, jjc_faq, "How to make a junk journal cover", app_name="Junk journal cover size calculator")
