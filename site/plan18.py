# ---------------- 28 Nov 2026 run 18: HOW TO KNIT A BLANKET + CROCHET HEADBAND (EAR WARMER) + HOW TO WIND A BALL OF YARN ----------------
# Executed from build.py after plan17.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 28 Nov run 18). Patterns, drawings and wording our own. JS in assets/app.js (kbk-*, chb-*, ywb-*).


# ======== HOW TO KNIT A BLANKET ========
# Demand: S5 'how to knit a blanket for beginners step by step' (SERP 28 Nov: B.Hooked baby blanket, Handy Little Me, Make and Do Crew x3,
# Puffy, Yours.co.uk, Gathered, Udemy chunky blanket, Skillshare; no size-to-cast-on writer). Model: CYC knit gauge by weight (tblanket.kg),
# garter rows = 2 x stitches per inch, stockinette 1.33, seed 1.6 (typical ratios); yardage 0.667 yd per sq in x weight factor; all estimates.

def _kbk_svg(step, label):
    def v(x, y, c=_TEAL):
        return f'<path d="M{x} {y} l7 12 l7 -12" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>'
    def ridge(x, y, c=_TEAL):
        return f'<path d="M{x} {y + 6} q7 -8 14 0" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>'
    if step == 1:
        s = (f'<line x1="30" y1="110" x2="250" y2="110" stroke="{_WOOD}" stroke-width="7" stroke-linecap="round"/><circle cx="250" cy="110" r="7" fill="{_INK}"/>'
             f'<path d="M30 110 q-14 0 -14 -14 q0 -14 14 -14 L60 82" fill="none" stroke="#8a8f99" stroke-width="3"/>'
             + "".join(f'<path d="M{40 + i * 18} 98 q-8 12 0 24 q8 -12 0 -24" fill="none" stroke="{_BERRY}" stroke-width="4"/>' for i in range(11))
             + f'<text x="140" y="160" {_T12} text-anchor="middle">cast on onto a long circular needle</text>')
    elif step == 2:
        s = ("".join(ridge(40 + i * 18, 60 + j * 16, (_TEAL, "#5fb1ac")[j % 2]) for j in range(5) for i in range(11))
             + f'<text x="140" y="168" {_T12} text-anchor="middle">garter: knit every row, ridges both sides</text>')
    elif step == 3:
        s = ("".join(ridge(40 + i * 18, 50 + j * 14) for j in range(2) for i in range(11))
             + "".join(ridge(40 + i * 18, 78 + j * 14) if i < 2 or i > 8 else v(40 + i * 18, 80 + j * 14, _BERRY) for j in range(4) for i in range(11))
             + f'<text x="140" y="168" {_T12} text-anchor="middle">or stockinette inside a garter frame</text>')
    elif step == 4:
        s = (f'<rect x="60" y="34" width="160" height="104" rx="4" fill="{_TEAL}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<line x1="60" y1="{y}" x2="220" y2="{y}" stroke="#fbfcfa" stroke-width="1" opacity=".45"/>' for y in range(44, 138, 8))
             + f'<circle cx="220" cy="64" r="7" fill="{_GOLD}" stroke="{_INK}" stroke-width="1.5"/><path d="M220 64 q24 4 30 30" fill="none" stroke="{_BERRY}" stroke-width="3"/>'
             + f'<text x="140" y="170" {_T12} text-anchor="middle">a marker on the right side, count rows</text>')
    elif step == 5:
        s = (f'<rect x="60" y="34" width="160" height="104" rx="4" fill="{_TEAL}" stroke="{_INK}" stroke-width="2"/>'
             + f'<path d="M220 110 q22 0 26 26" fill="none" stroke="{_BERRY}" stroke-width="4"/><path d="M220 104 q26 -6 30 -32" fill="none" stroke="{_TEAL}" stroke-width="4"/>'
             + f'<text x="140" y="170" {_T12} text-anchor="middle">join a new ball at the start of a row</text>')
    else:
        s = (f'<rect x="56" y="30" width="168" height="120" rx="4" fill="{_TEAL}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{64 + i * 16} 30 q8 -10 16 0" fill="none" stroke="{_INK}" stroke-width="2"/>' for i in range(10))
             + f'<path d="M224 34 l20 -20" stroke="{_INK}" stroke-width="2"/><path d="M244 14 l-4 14 l-10 -10 z" fill="{_INK}"/>'
             + f'<text x="140" y="178" {_T12} text-anchor="middle">bind off loosely, weave in, block</text>')
    return _svg12(s, label)


KBK_STEPS = [(1, "1. Cast on", "Use a long circular needle and work back and forth, as if it were two straight needles: the cable holds the weight of the blanket on your lap. Cast on the number the writer gives you with the long-tail cast on."),
             (2, "2. Knit the first rows", "For garter stitch, knit every stitch of every row. Each two rows make one ridge, and both sides look the same, so it lies flat and never curls."),
             (3, "3. Or add a frame", "Prefer the smooth V stitch? Knit 8 garter rows, then on every row keep the first and last 5 stitches in garter and work stockinette in between. The frame stops the edges rolling."),
             (4, "4. Keep going", "Put a stitch marker on the right side so you know which side you're on. Count your stitches every 10 rows or so, and keep the rows on a row counter."),
             (5, "5. Join a new ball", "When a ball runs out, start the new one at the beginning of a row: drop the old yarn, knit with the new, and leave 6 in tails to weave in later."),
             (6, "6. Bind off and finish", "Bind off loosely (go up a needle size if your bind-off is tight), weave in every end, then wash and lay flat to straighten the edges.")]
kbk_cards = "".join(f'<figure class="gq-fig"><div>{_kbk_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in KBK_STEPS)
_kbk_opts = "".join(f'<option value="{b["id"]}"{" selected" if b["id"] == "stroller" else ""}>{e(b["name"])} ({b["w"]} x {b["l"]} in)</option>' for b in D["blankets"]) + '<option value="custom">My own size</option>'

kbk = top("How to knit a blanket for beginners", "A garter stitch blanket is the friendliest big knitting project there is: one stitch, no shaping and no curling edges. Every step is drawn below, and the writer works out how many stitches to cast on, how many rows to knit, how much yarn to buy and roughly how many hours it'll take, for any size from a lovey to a king.", "How to knit a blanket") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to knit a blanket, <strong>cast on the width you want</strong> on a long circular needle (about 135 stitches for a 30 in baby blanket in worsted), <strong>knit every row</strong> (garter stitch) back and forth until it's as long as you want, then <strong>bind off loosely</strong> and weave in the ends. Garter stitch lies flat without a border. A 30 x 36 in stroller blanket in worsted garter stitch takes roughly 750 to 1,000 yards of yarn and 18 to 30 hours, by our estimates; chunky yarn is far quicker.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Beginner knit blanket pattern writer</h3>
<div class="row2"><div class="field"><label for="kbk-z">Blanket size</label><select id="kbk-z">{_kbk_opts}</select></div>
<div class="field" id="kbk-own" hidden><label for="kbk-w">Width x length (in)</label><div class="row2"><input type="number" id="kbk-w" value="40" min="8" max="120" inputmode="decimal" aria-label="Width in inches"><input type="number" id="kbk-l" value="50" min="8" max="120" inputmode="decimal" aria-label="Length in inches"></div></div></div>
<div class="row2"><div class="field"><label for="kbk-y">Yarn</label><select id="kbk-y"><option value="3">DK / light (3)</option><option value="4" selected>Worsted / aran (4)</option><option value="5">Chunky / bulky (5)</option><option value="6">Super bulky (6)</option><option value="7">Jumbo (7)</option></select></div>
<div class="field"><label for="kbk-s">Stitch</label><select id="kbk-s"><option value="garter" selected>Garter stitch (knit every row; easiest)</option><option value="seed">Seed stitch (k1, p1; textured, flat)</option><option value="st">Stockinette with a garter border (smooth Vs)</option></select></div></div>
<div class="row2"><div class="field"><label for="kbk-k">Yards per ball (from the label)</label><input type="number" id="kbk-k" value="200" min="20" max="2000" inputmode="numeric"></div>
<div class="field"><label for="kbk-g">Your swatch: stitches per 4 in (optional)</label><input type="number" id="kbk-g" placeholder="leave blank for a typical gauge" min="2" max="40" step="0.5" inputmode="decimal"></div></div>
</div><div class="result" aria-live="polite" id="kbk-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to knit a blanket, step by step</h2>
<div class="gq-figs">{kbk_cards}</div>
<h2>What you need to knit your first blanket</h2>
<ul><li><strong>Yarn:</strong> a smooth, light-coloured acrylic or wool blend in worsted (4) or chunky (5). Dark and fluffy yarns hide your stitches, which makes mistakes hard to spot. Buy every ball at once and check they share a dye lot number.</li>
<li><strong>Needles:</strong> a <strong>circular needle</strong> with a long cable, in the size on the yarn label: 32 in (80 cm) for baby blankets, 40 to 47 in (100 to 120 cm) for throws and bigger. You knit flat on it; the cable just holds all the stitches.</li>
<li><strong>Also:</strong> a few stitch markers, a tape measure, scissors and a tapestry needle for weaving in ends.</li></ul>
<p>Never knitted before? Start with <a href="{href("how-to-cast-on-knitting.html")}">how to cast on</a> and <a href="{href("how-to-knit-and-purl.html")}">how to knit and purl</a>, then come back: a blanket is just those stitches, many times over.</p>
<h2>Best stitch for a beginner knit blanket</h2>
<p><strong>Garter stitch</strong> is the easiest: you only ever knit, it's squishy and warm, and the edges stay flat. It does use a bit more yarn and grows slowly in length, because each ridge takes two rows. <strong>Seed stitch</strong> (knit one, purl one, and knit the purls and purl the knits on the next row) also lies flat and has a lovely pebbly look, but switching between knit and purl is slower. <strong>Stockinette</strong> (knit a row, purl a row) gives the classic smooth Vs, but it curls hard at every edge, so it always needs a garter or seed border. For more ideas see our <a href="{href("knit-stitch-patterns.html")}">15 knit stitch patterns for beginners</a>.</p>
<h2>How many stitches to cast on for a blanket?</h2>
<p>Multiply the width you want by your stitches per inch. With worsted yarn at about 18 stitches per 4 in (4.5 per inch), a 30 in baby blanket needs about 135 stitches and a 50 in throw about 225. Chunky yarn at 14 stitches per 4 in needs about 105 and 175. Seed stitch needs an odd number, so the pattern is the same on both sides. Knit a swatch and type your own gauge into the writer for a closer number, or use the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> for scarves, cowls and pattern repeats.</p>
<h2>How to keep the edges neat</h2>
<ul><li><strong>Slip the first stitch</strong> of every row (purlwise, with the yarn in front for garter), then knit the last stitch. This makes a tidy chain-like edge. It's optional, so skip it if it confuses you.</li>
<li>Count your stitches every 10 rows. If you have extra, you've probably knit into the strand between stitches or wrapped the yarn over the needle at the start of a row.</li>
<li>Pull the first two stitches of each row a little snug to avoid a loose, loopy edge.</li>
<li>If you drop a stitch, don't panic: see <a href="{href("how-to-fix-a-dropped-stitch.html")}">how to fix a dropped stitch</a>, even several rows down.</li></ul>
<h2>How long does it take to knit a blanket?</h2>
<p>Much longer than crochet: knit stitches are small, so a blanket is a lot of them. As a rough guide (our estimates for a comfortable knitter), a stroller blanket in worsted garter stitch is about 18 to 30 hours, a throw 50 to 80 and a queen size well over 130. Chunky or super bulky yarn cuts that by half or more, which is why chunky throws are so popular. If you're short on time, <a href="{href("how-to-crochet-a-blanket.html")}">crocheting a blanket</a> is about twice as fast. Check a deadline with the <a href="{href("crochet-time-estimator.html")}">knitting time calculator</a>.</p>
<h2>Finishing your knitted blanket</h2>
<p>Bind off loosely, or the top edge will pull in (our guide to <a href="{href("how-to-bind-off-knitting.html")}">binding off</a> has stretchy options). <a href="{href("how-to-weave-in-ends.html")}">Weave in every end</a> along the edge or through the garter ridges, then wash it and lay it flat to dry (<a href="{href("how-to-block-knitting-crochet.html")}">how to block knitting</a>). Want a picked-up border later? See <a href="{href("how-to-pick-up-stitches-knitting.html")}">how to pick up stitches</a>. Check sizes for beds and sofas on the <a href="{href("blanket-size-calculator.html")}">blanket size chart</a>, and if you'll sell it, work out a fair price with the <a href="{href("how-to-price-a-crochet-blanket.html")}">blanket price calculator</a> (it works for knitting too).</p>
<p class="note">Method is standard knitting technique, checked against Gathered, Make and Do Crew and B.Hooked beginner blanket guides (28 Nov 2026). Gauges use typical Craft Yarn Council ranges for each yarn weight; stitch counts, rows, yardage and hours are our estimates, so knit a swatch and buy a spare ball. Drawings and wording are our own.</p>
</div></div></section>'''
kbk_faq = [
    ("How do you knit a blanket for beginners?", "Cast on the width you want on a long circular needle, knit every row back and forth (garter stitch) until it's long enough, then bind off loosely and weave in the ends. Garter stitch lies flat, so it needs no border."),
    ("How many stitches do I cast on for a blanket?", "Width in inches times your stitches per inch. In worsted yarn (about 4.5 stitches per inch) that's about 135 stitches for a 30 in baby blanket and 225 for a 50 in throw."),
    ("Can you knit a blanket on straight needles?", "Only a small one. A long circular needle (32 to 47 in) is better: you knit back and forth the same way, but the weight rests in your lap instead of on your wrists."),
    ("How much yarn do I need to knit a blanket?", "Roughly 750 to 1,000 yards of worsted for a 30 x 36 in baby blanket and 2,100 to 2,700 yards for a 50 x 60 in throw in garter stitch, by our estimates. Buy one extra ball."),
    ("What is the easiest stitch to knit a blanket?", "Garter stitch: you knit every row, both sides look the same and the edges don't curl."),
    ("Why does my knitted blanket curl?", "Stockinette stitch always curls at the edges. Add a garter or seed border of 5 or more stitches at each side and 8 or more rows top and bottom, or knit the whole blanket in garter or seed stitch."),
    ("How long does it take to knit a blanket?", "About 18 to 30 hours for a baby blanket in worsted garter stitch and 50 to 80 hours for a throw, for a comfortable knitter (our estimates). Chunky yarn halves it."),
]
SHOP_FOR["how-to-knit-a-blanket.html"] = ["2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "yarn-stash-tracker", "christmas-gift-planner-budget"]
page("how-to-knit-a-blanket.html", "How to Knit a Blanket for Beginners (+ Free Pattern Writer)",
     "How to knit a blanket for beginners: six drawn steps, the best stitch, and a writer for cast on, rows, yarn, balls and hours for any size.",
     kbk, kbk_faq, "How to knit a blanket", app_name="Beginner knit blanket pattern writer")


# ======== CROCHET HEADBAND / EAR WARMER PATTERN ========
# Demand: 'crochet ear warmer headband pattern easy' (SERP 28 Nov: Ravelry x12 headband/ear warmer listings incl. Brighton, Simple Steps,
# Easy Ear-Warmers, Back to Basics; B.Hooked step-by-step headband, Handy Little Me, MJ's Off The Hook chunky ribbed headband; no size writer).
# Also: last-minute gift (DEMAND M6) and Christmas crafts to sell ('ear warmers' in /christmas-crafts-to-sell). Our own pattern: a strip of hdc in
# the back loop only (ribbed), worked sideways, with a twist or plain seam. Length ~ 90% of head (rib stretches); gauge = CYC sc gauge x hdc factor.

def _chb_svg(step, label):
    if step == 1:
        s = ("".join(f'<ellipse cx="{50 + i * 20}" cy="100" rx="10" ry="6" fill="none" stroke="{_BERRY}" stroke-width="4"/>' for i in range(10))
             + f'<text x="140" y="150" {_T12} text-anchor="middle">a short chain = the headband width</text>')
    elif step == 2:
        s = ("".join(f'<rect x="{80 + j * 14}" y="40" width="12" height="110" rx="4" fill="{(_BERRY, "#d4577f")[j % 2]}" stroke="{_INK}" stroke-width="1.2"/>' for j in range(8))
             + f'<text x="140" y="176" {_T12} text-anchor="middle">hdc in the back loop: ridges like rib</text>')
    elif step == 3:
        s = (f'<rect x="30" y="74" width="220" height="44" rx="6" fill="{_BERRY}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<line x1="{x}" y1="76" x2="{x}" y2="116" stroke="#fbfcfa" stroke-width="1.4" opacity=".5"/>' for x in range(40, 250, 9))
             + f'<text x="140" y="150" {_T12} text-anchor="middle">rows until it stretches snugly round the head</text>')
    elif step == 4:
        s = (f'<path d="M40 70 h90 v50 h-90 z" fill="{_BERRY}" stroke="{_INK}" stroke-width="2"/><path d="M240 70 h-90 v50 h90 z" fill="#d4577f" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M130 70 q10 25 0 50" fill="none" stroke="{_INK}" stroke-width="1.5" stroke-dasharray="3 3"/><path d="M150 70 q-10 25 0 50" fill="none" stroke="{_INK}" stroke-width="1.5" stroke-dasharray="3 3"/>'
             + f'<text x="140" y="150" {_T12} text-anchor="middle">fold each end in half and hook them together</text>')
    elif step == 5:
        s = (f'<path d="M60 96 q80 -60 160 0" fill="none" stroke="{_BERRY}" stroke-width="28" stroke-linecap="round"/>'
             f'<path d="M126 74 l28 44 M154 74 l-28 44" stroke="{_GOLD}" stroke-width="3"/>'
             + f'<text x="140" y="150" {_T12} text-anchor="middle">sew through all four layers</text>')
    else:
        s = (f'<ellipse cx="140" cy="96" rx="80" ry="54" fill="none" stroke="{_BERRY}" stroke-width="26"/>'
             + f'<path d="M126 34 q14 18 28 0 q-14 26 -28 0" fill="{_GOLD}" stroke="{_INK}" stroke-width="1.5"/>'
             + f'<text x="140" y="182" {_T12} text-anchor="middle">turn right side out: twisted front</text>')
    return _svg12(s, label)


CHB_STEPS = [(1, "1. Chain the width", "Chain the number the writer gives you. This chain becomes the headband's width (it's worked sideways), so it's short."),
             (2, "2. Rows in the back loop", "Row 1: half double crochet in the 3rd chain from the hook and in each chain. From row 2, chain 2, turn and work each hdc in the back loop only. The unused loops make ridges that stretch like ribbing."),
             (3, "3. Work to length", "Keep going until the strip, gently stretched, fits snugly round the head over the ears. The writer gives a row count and a length to check."),
             (4, "4. Fold for the twist", "Lay the strip flat, right side up. Fold each end in half lengthwise, then hook the two folded ends into each other so they hug."),
             (5, "5. Sew the seam", "Pin, then sew straight through all four layers with the long tail, or slip stitch them together with your hook."),
             (6, "6. Turn and wear", "Turn it right side out: the seam hides inside and the front has a neat twist. Prefer it plain? Just sew the two short ends flat.")]
chb_cards = "".join(f'<figure class="gq-fig"><div>{_chb_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CHB_STEPS)
_chb_opts = "".join(f'<option value="{h["id"]}"{" selected" if h["id"] == "adult" else ""}>{e(h["name"])} ({h["head"]:g} in head)</option>' for h in D["hats"] if h["id"] not in ("preemie", "newborn")) + '<option value="custom">Measure my own head</option>'

chb = top("Free crochet headband pattern (easy ear warmer)", "This ribbed ear warmer is a great first wearable and a quick Christmas gift: it's one stretchy strip of half double crochet with a twist at the front. Pick a size, yarn and width and the pattern below works out your chain, rows and yarn.", "Crochet headband pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet an easy ear warmer, <strong>chain the width</strong> (about 12 chains for a 3.5 in adult headband in worsted), work <strong>half double crochet in the back loop only</strong>, row after row, until the strip stretches snugly round the head (about 20 in for an average adult head of 22 in), then <strong>fold the ends and sew them together for a twist</strong>. It takes about 1.5 to 2.5 hours and roughly 60 to 80 yards of worsted yarn (our estimates); chunky yarn is quicker.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Ear warmer pattern writer</h3>
<div class="row2"><div class="field"><label for="chb-z">Size</label><select id="chb-z">{_chb_opts}</select></div>
<div class="field" id="chb-own" hidden><label for="chb-c">Head round the forehead and over the ears (in)</label><input type="number" id="chb-c" value="22" min="14" max="26" step="0.25" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="chb-y">Yarn</label><select id="chb-y"><option value="4" selected>Worsted / aran (4), 5.5 mm hook</option><option value="5">Chunky / bulky (5), 8 mm hook</option><option value="6">Super bulky (6), 10 mm hook</option></select></div>
<div class="field"><label for="chb-w">Width (in)</label><select id="chb-w"><option value="2.5">2.5 in (slim)</option><option value="3">3 in</option><option value="3.5" selected>3.5 in (classic)</option><option value="4">4 in</option><option value="4.5">4.5 in (wide, covers ears well)</option></select></div></div>
<div class="row2"><div class="field"><label for="chb-f">Finish</label><select id="chb-f"><option value="twist" selected>Twisted front</option><option value="seam">Plain seam</option></select></div>
<div class="field"><label for="chb-g">Your swatch: hdc per 4 in (optional)</label><input type="number" id="chb-g" placeholder="leave blank for a typical gauge" min="2" max="30" step="0.5" inputmode="decimal"></div></div>
<div class="field"><span class="label" id="chb-t-l">Terms</span><div class="seg" role="group" aria-labelledby="chb-t-l" id="chb-t"><button type="button" data-v="us" aria-pressed="true">US</button><button type="button" data-v="uk" aria-pressed="false">UK</button></div></div>
</div><div class="result" aria-live="polite" id="chb-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet an ear warmer, step by step</h2>
<div class="gq-figs">{chb_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> about 60 to 80 yards of worsted, or 50 to 70 of chunky, for an adult (the writer works out yours). A soft acrylic, wool blend or anything with a little stretch is ideal; 100% cotton has no bounce and will feel loose.</li>
<li><strong>Hook:</strong> the size on the label: about 5.5 mm (I-9) for worsted, 8 mm (L-11) for chunky, 10 mm (N/P-15) for super bulky.</li>
<li><strong>Also:</strong> scissors, a tapestry needle and a couple of clips or pins for the twist.</li></ul>
<h2>Why work in the back loop?</h2>
<p>Every crochet stitch has two loops on top. Working only into the back one leaves the front loop as a ridge, and row after row those ridges stack up like knitted ribbing. The fabric stretches far more lengthwise, which is exactly what a headband needs: it hugs the head instead of slipping. That's why the strip is made a little shorter than the head (about 90%). New to the stitch? See <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a> for the half double crochet.</p>
<h2>What size should a crochet headband be?</h2>
<p>Measure round the forehead and over the tops of the ears. Typical heads are about 17 in for a baby, 18.5 in for a toddler, 20 in for a child, 21 in for a teen and 22 to 23.5 in for adults (our <a href="{href("hat-size-chart.html")}">hat size chart</a> has the full table from the Craft Yarn Council). Make a ribbed band 1.5 to 2.5 in shorter than the head; less for a non-stretchy stitch. Widths of 2.5 to 3 in suit children and 3.5 to 4.5 in suit adults; wider bands keep ears warmer.</p>
<h2>Ear warmer problems and fixes</h2>
<ul><li><strong>It's too loose:</strong> take off a few rows before you seam. Ribbing relaxes with wear, so snug is right.</li>
<li><strong>The edges wave:</strong> you're adding or skipping a stitch at the ends. Count the stitches on every row for the first few, and remember the chain 2 doesn't count as a stitch.</li>
<li><strong>The twist looks bulky:</strong> use a slimmer width or a lighter yarn, or choose the plain seam and add a button or a <a href="{href("how-to-make-a-pom-pom.html")}">little pom pom</a>.</li>
<li><strong>The seam shows:</strong> sew with the yarn tail through the back loops only, then turn it so the seam sits at the back of the head.</li></ul>
<h2>Gift and selling ideas</h2>
<p>Ear warmers are one of the fastest wearable gifts: see more quick makes in the <a href="{href("crochet-knitting-gift-planner.html")}#last-minute">last-minute gift list</a>. Pair one with a matching <a href="{href("how-to-crochet-a-hat.html")}">crocheted beanie</a> or <a href="{href("how-to-crochet-a-scarf.html")}">scarf</a> for a set. They also sell well at winter craft fairs because they're quick to batch: price them for your time with the <a href="{href("how-to-price-crochet-items.html")}">crochet pricing calculator</a> and see more ideas in <a href="{href("christmas-crafts-to-sell.html")}">Christmas crafts to make and sell</a>.</p>
<p class="note">Pattern, drawings and wording are our own (28 Nov 2026). Head sizes follow the Craft Yarn Council hat and head chart (as on our hat size chart); the twist finish is a standard technique, checked against B.Hooked and Handy Little Me headband tutorials. Gauges are typical CYC ranges; chains, rows, yarn and time are our estimates, so make a small swatch first.</p>
</div></div></section>'''
chb_faq = [
    ("How do you crochet an easy ear warmer?", "Chain the width (about 12 for an adult in worsted), work half double crochet in the back loop only, row after row, until the strip stretches snugly round the head, then fold each end in half, hook them together and sew for a twisted front."),
    ("How long should a crochet headband be?", "About 1.5 to 2.5 in shorter than the head when it's ribbed, because it stretches. For an average adult head of 22 in, make the strip about 20 in long."),
    ("How much yarn do you need for a crochet ear warmer?", "Roughly 60 to 80 yards of worsted or 50 to 70 yards of chunky yarn for an adult, by our estimates. One skein makes two or three."),
    ("How wide should an ear warmer be?", "3.5 to 4.5 in for adults and 2.5 to 3 in for children. Wider bands cover the ears better."),
    ("How long does it take to crochet an ear warmer?", "About 1.5 to 2.5 hours in worsted yarn and 1 to 1.5 hours in chunky for most crocheters, by our estimates."),
    ("What is the best yarn for a crochet headband?", "A soft acrylic, wool or wool blend in worsted or chunky. It needs some stretch, so avoid 100% cotton."),
]
SHOP_FOR["crochet-headband-pattern.html"] = ["crochet-knitting-pricing-calculator", "christmas-gift-tags", "christmas-gift-planner-budget", "yarn-stash-tracker"]
page("crochet-headband-pattern.html", "Free Crochet Headband Pattern: Easy Ear Warmer (Any Size)",
     "Free easy crochet ear warmer pattern: a ribbed headband with a twist, six drawn steps, and a writer for chains, rows and yarn in any size.",
     chb, chb_faq, "Crochet headband pattern", app_name="Crochet ear warmer pattern writer")


# ======== HOW TO WIND A BALL OF YARN ========
# Demand: 'how to wind a ball of yarn by hand center pull' (SERP 28 Nov: Instructables x2, Lion Brand, Purl Soho, AllFreeCrochet, Annie's,
# Sweet Georgia, Jimmy Beans Wool x2, Spin Off nostepinne, Make:, Creativebug, FaveCrafts, String or Nothing, Eye Love Knots scrap ball).
# Plus 'how to split a skein in half' (two-at-a-time socks / sleeves): a kitchen-scale splitter is the tool here.

def _ywb_svg(step, label):
    if step == 1:
        s = (f'<rect x="96" y="40" width="40" height="110" rx="18" fill="#f1d9c4" stroke="{_INK}" stroke-width="2"/><rect x="144" y="50" width="34" height="100" rx="16" fill="#f1d9c4" stroke="{_INK}" stroke-width="2"/>'
             f'<path d="M116 150 q0 20 -20 30" fill="none" stroke="{_BERRY}" stroke-width="4"/>'
             f'<path d="M116 70 C150 50 170 120 160 100 C150 80 110 120 116 70" fill="none" stroke="{_BERRY}" stroke-width="4"/>'
             + f'<text x="140" y="196" {_T12} text-anchor="middle">tail under the thumb, figure 8 round two fingers</text>')
    elif step == 2:
        s = ("".join(f'<path d="M{120 + d} 80 C{170 + d} 60 {170 + d} 120 {140 + d} 110 C{110 + d} 100 {110 + d} 60 {120 + d} 80" fill="none" stroke="{(_BERRY, "#d4577f")[d % 2]}" stroke-width="4"/>' for d in range(0, 12, 3))
             + f'<text x="140" y="170" {_T12} text-anchor="middle">about 20 wraps, then slip them off</text>')
    elif step == 3:
        s = (f'<ellipse cx="140" cy="90" rx="22" ry="34" fill="#d4577f" stroke="{_INK}" stroke-width="1.5"/>'
             + "".join(f'<line x1="112" y1="{78 + i * 6}" x2="168" y2="{78 + i * 6}" stroke="{_BERRY}" stroke-width="4"/>' for i in range(4))
             + f'<path d="M140 56 q-6 -24 -30 -30" fill="none" stroke="{_BERRY}" stroke-width="3"/><text x="140" y="160" {_T12} text-anchor="middle">fold and wrap round the middle</text>')
    elif step == 4:
        s = (f'<circle cx="140" cy="96" r="44" fill="#d4577f" stroke="{_INK}" stroke-width="1.5"/>'
             + "".join(f'<line x1="{100 + i * 8}" y1="{60 + i * 2}" x2="{150 + i * 8}" y2="{140 - i * 2}" stroke="{_BERRY}" stroke-width="3"/>' for i in range(6))
             + f'<rect x="132" y="36" width="16" height="40" rx="8" fill="#f1d9c4" stroke="{_INK}" stroke-width="1.5"/><path d="M140 40 q-10 -26 -36 -28" fill="none" stroke="{_BERRY}" stroke-width="3"/>'
             + f'<text x="140" y="170" {_T12} text-anchor="middle">wrap diagonally over your thumb</text>')
    elif step == 5:
        s = (f'<circle cx="140" cy="96" r="52" fill="#d4577f" stroke="{_INK}" stroke-width="1.5"/>'
             + "".join(f'<path d="M{100 + i * 10} 54 L{150 + i * 6} 142" stroke="{_BERRY}" stroke-width="3"/>' for i in range(5))
             + "".join(f'<path d="M{96 + i * 10} 130 L{168 - i * 4} 52" stroke="{_BERRY}" stroke-width="3" opacity=".7"/>' for i in range(4))
             + f'<path d="M196 70 a30 30 0 0 1 0 50" fill="none" stroke="{_GOLD}" stroke-width="4"/><text x="140" y="172" {_T12} text-anchor="middle">turn the ball a little every few wraps</text>')
    else:
        s = (f'<circle cx="140" cy="96" r="52" fill="#d4577f" stroke="{_INK}" stroke-width="1.5"/>'
             + "".join(f'<path d="M{100 + i * 10} 54 L{150 + i * 6} 142" stroke="{_BERRY}" stroke-width="3"/>' for i in range(5))
             + f'<circle cx="140" cy="60" r="8" fill="#6d1e45"/><path d="M140 60 q10 -40 50 -44" fill="none" stroke="{_BERRY}" stroke-width="4"/>'
             + f'<text x="140" y="172" {_T12} text-anchor="middle">pull from the middle: it sits still</text>')
    return _svg12(s, label)


YWB_STEPS = [(1, "1. Hold the tail", "Leave a 6 in tail hanging and hold it under your thumb against your palm. Keep it there the whole time: it becomes the centre-pull end."),
             (2, "2. Figure 8 round two fingers", "Wrap the yarn in a figure 8 round your index and middle fingers about 20 times, loosely."),
             (3, "3. Make the core", "Slide the bundle off, fold it in half and wrap the yarn round the middle a few times. This little bundle is the core of the ball."),
             (4, "4. Wrap over your thumb", "Hold the core against your thumb (the tail still free) and wrap the yarn diagonally over both. Your thumb keeps a channel open for the tail."),
             (5, "5. Turn as you go", "Every few wraps turn the ball a little, so the wraps criss-cross and it grows evenly round. Don't pull tight: yarn wound under tension loses its spring."),
             (6, "6. Tuck and pull", "Tuck the last end under a few wraps. Pull the tail from the middle: the ball stays put while you knit or crochet, instead of rolling away.")]
ywb_cards = "".join(f'<figure class="gq-fig"><div>{_ywb_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in YWB_STEPS)

ywb = top("How to wind a ball of yarn by hand (centre pull)", "A centre-pull ball sits still in your project bag while the yarn feeds from the middle. You can wind one in about 10 minutes with nothing but your hand. Every step is drawn below, plus how to open a hank without tangles and a calculator for splitting a skein into equal balls on a kitchen scale.", "How to wind a ball of yarn") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to wind a centre-pull ball by hand, <strong>hold a 6 in tail under your thumb</strong>, <strong>wrap the yarn in a figure 8 round two fingers</strong> about 20 times, fold that bundle in half to make a core, then <strong>wrap diagonally over the core and your thumb</strong>, turning the ball a little every few wraps. Keep it loose. When you're done, tuck the end in and <strong>pull the tail from the middle</strong>. A 100 g skein takes about 10 to 15 minutes.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Split a skein into equal balls</h3>
<p class="sub" style="margin-top:0">For two-at-a-time socks or sleeves, or to share a skein between projects. Weigh as you wind.</p>
<div class="row2"><div class="field"><label for="ywb-g">Skein weight now (g)</label><input type="number" id="ywb-g" value="100" min="1" max="2000" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="ywb-lg">Label: grams per skein</label><input type="number" id="ywb-lg" value="100" min="1" max="2000" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="ywb-ly">Label: yards per skein</label><input type="number" id="ywb-ly" value="400" min="1" max="5000" inputmode="numeric"></div>
<div class="field"><label for="ywb-n">Split into</label><select id="ywb-n"><option value="2" selected>2 equal balls</option><option value="3">3 equal balls</option><option value="4">4 equal balls</option><option value="yd">One ball of the yards I need</option></select></div></div>
<div class="field" id="ywb-need-f" hidden><label for="ywb-need">Yards I need in the first ball</label><input type="number" id="ywb-need" value="100" min="1" max="5000" inputmode="numeric"></div>
</div><div class="result" aria-live="polite" id="ywb-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to wind a centre-pull ball, step by step</h2>
<div class="gq-figs">{ywb_cards}</div>
<h2>Do you need to wind yarn into a ball?</h2>
<p>Yarn sold as a <strong>ball</strong> or a <strong>skein</strong> (the long oval shape most acrylic comes in) is ready to use: find the end in the middle and pull. Yarn sold as a <strong>hank</strong>, a big loop twisted into a figure 8, must be wound first, or it will tangle into a nest the moment you start. Winding also lets you check for knots and join a second colour neatly.</p>
<h2>How to open a hank without tangles</h2>
<ol><li>Untwist the hank and shake it out into one big loop. Find the ties (a few pieces of yarn tied loosely round the strands).</li>
<li>Put the loop round the backs of two chairs, your knees, or a helper's hands, so it's gently taut.</li>
<li>Snip only the ties, never the loop. Find the outside end (it's usually tied to one of the ties).</li>
<li>Wind from there, letting the loop turn on the chairs as you go. If it snags, stop and untangle: pulling makes it worse.</li></ol>
<h2>Other ways to wind yarn</h2>
<ul><li><strong>A simple ball:</strong> wrap round your fingers, then round and round in every direction. Quick, but it pulls from the outside and rolls away while you work.</li>
<li><strong>On a tube:</strong> a nostepinne (a smooth wooden stick) or a cardboard kitchen roll tube does the same job as your thumb. Tuck the tail in a slit at one end, wrap diagonally while turning, then slide the ball off.</li>
<li><strong>Ball winder and swift:</strong> a ball winder makes a flat-topped "cake" in a minute or two, and a swift holds the hank. Worth it if you buy a lot of hand-dyed yarn; otherwise chairs and your hand are fine.</li></ul>
<h2>Winding tips</h2>
<ul><li><strong>Wind loosely.</strong> Yarn wound tight stays stretched; your swatch and project then shrink back when washed. Wrap over two fingers or your thumb to keep slack.</li>
<li><strong>Store hand-wound balls loosely</strong> and wind wool close to when you'll use it, rather than months ahead.</li>
<li><strong>Join leftovers</strong> into a scrap ball as you wind: tie or splice them and you've got a ready-made stripe ball. Plan stripes with the <a href="{href("stripe-generator.html")}">random stripe generator</a>.</li>
<li><strong>Not sure how much is left?</strong> Weigh a part-used ball in the <a href="{href("yarn-yardage-calculator.html")}">yarn yardage calculator</a>.</li></ul>
<h2>How to split a skein in half</h2>
<p>Weigh the skein on a kitchen scale and work out half. Wind one ball, putting it on the scale now and then, until it reaches that weight; then cut and wind the rest. The calculator above does the sum, including a split by yards for when a pattern needs a set length. Labels round the weight, and skeins vary by a few grams, so always weigh the real skein rather than trusting the label. Splitting for socks? See the <a href="{href("sock-size-chart.html")}">sock size chart</a> for how much each sock needs.</p>
<p>Want somewhere to keep the ball while you work? Crochet a soft <a href="{href("crochet-basket-pattern.html")}">yarn bowl or basket</a> with our free pattern writer.</p>
<p class="note">Method is standard practice, checked against Lion Brand, Purl Soho and AllFreeCrochet winding tutorials (28 Nov 2026). Drawings and wording are our own. Yards per ball are worked out from the label's yards per gram, so they're close estimates.</p>
</div></div></section>'''
ywb_faq = [
    ("How do you wind a centre-pull ball of yarn by hand?", "Hold a 6 in tail under your thumb, wrap the yarn in a figure 8 round two fingers about 20 times, fold the bundle into a core, then wrap diagonally over the core and your thumb, turning a little every few wraps. Tuck the end in and pull the tail from the middle."),
    ("Do I need to wind yarn before using it?", "Only if it's sold as a hank (a twisted loop). Balls and pull skeins are ready to use; hanks tangle if you knit straight from them."),
    ("Should you wind yarn tightly?", "No. Winding under tension stretches the yarn, so your project can shrink when washed. Wind loosely over your fingers or thumb."),
    ("How do you split a skein of yarn in half?", "Weigh it on a kitchen scale, halve the weight, and wind one ball until it reaches that weight on the scale. Cut, then wind the rest."),
    ("How do I wind yarn without a ball winder?", "By hand with the thumb method, round a cardboard tube or a wooden nostepinne. Put a hank round two chair backs or your knees instead of using a swift."),
    ("How long does it take to wind a ball of yarn by hand?", "About 10 to 15 minutes for a 100 g skein once you have the rhythm."),
]
SHOP_FOR["how-to-wind-a-ball-of-yarn.html"] = ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-planner-budget"]
page("how-to-wind-a-ball-of-yarn.html", "How to Wind a Ball of Yarn by Hand (Centre Pull) + Splitter",
     "How to wind a centre-pull ball of yarn by hand in six drawn steps, open a hank without tangles, and split a skein into equal balls by weight.",
     ywb, ywb_faq, "How to wind a ball of yarn", app_name="Yarn skein splitter")
