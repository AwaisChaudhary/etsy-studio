# ---------------- 27 Nov 2026 run 9: HOW TO JOIN GRANNY SQUARES + HOW TO INCREASE IN KNITTING ----------------
# Executed from build.py after trio.py (shares page(), top(), href(), e(), SHOP_FOR, gq_svg from trio.py).
# Demand evidence in DEMAND.md (RADAR 27 Nov run 9). Drawings our own SVG; wording our own. JS in assets/app.js (gj-*, ki-*).

# ======== HOW TO JOIN GRANNY SQUARES ========
# Demand: 'how to join granny squares' (SERP 27 Nov: Gathered, Make:, We Are Knitters x2, Ravelry, B.Hooked 6 ways + JAYGO,
# Yarnspirations JAYGO guide, Marching North x2 (slip stitch joins, CJAYGO), Petals to Picots, Nana's Crafty Home (sc join),
# Craft Passion 12 ways, Joy of Motion). Methods are standard crochet finishing techniques taught by all of them; wording ours.
# Yarn per inch of seam: our own rough estimates for worsted (see GJ_F in app.js), said so on the page.

def _gj_pair(seam, label):
    """Two small granny squares side by side with the chosen seam drawn between them."""
    sq = gq_svg(3, 120, "")
    inner = sq[sq.index(">") + 1:-6]
    L = f'<g transform="translate(8 20)">{inner}</g>'
    R = f'<g transform="translate(152 20)">{inner}</g>'
    x = 140; y0, y1 = 26, 136
    s = ""
    if seam == "whip":
        for k in range(9):
            y = y0 + 6 + k * 12
            s += f'<path d="M{x - 13} {y} L{x + 13} {y + 8}" stroke="#b8326a" stroke-width="3" stroke-linecap="round"/>'
    elif seam == "slip":
        for k in range(10):
            y = y0 + 4 + k * 11
            s += f'<path d="M{x - 5} {y} L{x} {y + 8} L{x + 5} {y}" fill="none" stroke="#b8326a" stroke-width="2.6" stroke-linejoin="round"/>'
    elif seam == "sc":
        for k in range(9):
            y = y0 + 6 + k * 12
            s += f'<path d="M{x - 6} {y - 4} L{x + 6} {y + 4} M{x + 6} {y - 4} L{x - 6} {y + 4}" stroke="#b8326a" stroke-width="2.8" stroke-linecap="round"/>'
        s += f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="#b8326a" stroke-width="1.2" opacity=".5"/>'
    elif seam == "mattress":
        s += f'<line x1="{x - 12}" y1="{y0}" x2="{x - 12}" y2="{y1}" stroke="#1f2a44" stroke-width="1" opacity=".4"/><line x1="{x + 12}" y1="{y0}" x2="{x + 12}" y2="{y1}" stroke="#1f2a44" stroke-width="1" opacity=".4"/>'
        for k in range(10):
            y = y0 + 5 + k * 11
            s += f'<line x1="{x - 12}" y1="{y}" x2="{x + 12}" y2="{y}" stroke="#b8326a" stroke-width="2.6" stroke-linecap="round"/>'
    else:  # jaygo: slip stitches into the neighbour's spaces on the last round
        for y in (y0 + 2, y0 + 30, y0 + 55, y0 + 80, y1 - 2):
            s += f'<path d="M{x - 13} {y} Q{x} {y - 8} {x + 13} {y}" fill="none" stroke="#b8326a" stroke-width="2.6"/><circle cx="{x}" cy="{y - 3}" r="3.2" fill="#e39a14"/>'
    return (f'<svg viewBox="0 0 280 160" role="img" aria-label="{e(label)}"><rect x="0" y="0" width="280" height="160" rx="10" fill="#f6f1e6"/>'
            f'{L}{R}{s}</svg>')

GJ_METHODS = [
    ("whip", "Whip stitch", "Sewn with a needle. Easy, flat and nearly invisible; the classic choice for beginners."),
    ("mattress", "Mattress stitch", "Sewn, with the squares lying flat side by side. The seam disappears and stays soft."),
    ("slip", "Slip stitch join", "Worked with your hook. Quick and neat, with a small ridge on the back."),
    ("sc", "Single crochet join", "Worked with your hook. Strong, with a raised ridge you can show off on the front."),
    ("jaygo", "Join as you go", "Joined on the last round of each new square. No sewing at the end, and no extra yarn."),
]
gj_cards = "".join(f'<figure class="gq-fig"><div>{_gj_pair(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in GJ_METHODS)
gj_opts = "".join(f'<option value="{k}"{" selected" if k == "whip" else ""}>{e(n)}</option>' for k, n, _ in GJ_METHODS)

gjp = top("How to join granny squares", "Five ways to join granny squares, from a simple whip stitch to join-as-you-go, each with our own diagram. Plus a calculator for how many seams your blanket has and how much yarn the joining takes.", "How to join granny squares") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> block all your squares to the same size, then lay them out. For the easiest join, hold two squares <strong>right sides together</strong>, thread a tapestry needle with matching yarn and <strong>whip stitch</strong> through the back loops of each pair of matching stitches, corner to corner. Prefer to use your hook? A <strong>slip stitch</strong> or <strong>single crochet join</strong> through both edges is quicker and stronger. To skip sewing altogether, <strong>join as you go</strong>: on the last round of each new square, swap the chain spaces for slip stitches into the square next to it. Join in long rows, not one square at a time, and you'll have far fewer ends to weave in.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Joining calculator</h3>
<div class="row2"><div class="field"><label for="gj-a">Squares across</label><input type="number" id="gj-a" value="8" min="1" max="60" step="1" inputmode="numeric"></div>
<div class="field"><label for="gj-b">Squares down</label><input type="number" id="gj-b" value="10" min="1" max="60" step="1" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="gj-s">Size of one square (in)</label><input type="number" id="gj-s" value="6" min="1" max="30" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="gj-m">How you'll join</label><select id="gj-m">{gj_opts}</select></div></div>
<p class="sub">Yarn amounts are our rough estimates for worsted yarn: work 4 in of seam and measure the yarn you used to check your own. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="gj-out" data-bl="{href("granny-square-blanket-calculator.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Ways to join granny squares</h2>
<div class="gq-figs">{gj_cards}</div>
<h2>Before you join: block and lay out</h2>
<ol><li><strong>Weave in the ends</strong> on every square first, or leave one long tail on each to sew with. See <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>.</li>
<li><strong>Block the squares.</strong> Pin each one flat to the same measured size, mist with water and let it dry. Squares that match make straight seams.</li>
<li><strong>Lay them out</strong> on the floor or a bed and take a photo, so you remember the order once you start.</li>
<li><strong>Pick your joining yarn.</strong> Use the same weight as the squares. A matching colour hides the seam; a contrast colour (often the border colour) frames each square.</li></ol>
<h2>How to whip stitch granny squares together</h2>
<ol><li>Hold two squares right sides together, edges lined up, corner stitches matching.</li>
<li>Cut a length of yarn about three times the length of the seam and thread a tapestry needle.</li>
<li>Start in the corner chain space: go through both squares and leave a 6 in tail.</li>
<li>Work along the edge: put the needle through the <strong>back loop</strong> of the stitch on the front square and the back loop of the matching stitch on the back square, always from the same side. Pull snug, not tight.</li>
<li>Keep going stitch by stitch to the far corner. Through back loops only, the front loops stay on top as a neat line; through both loops the seam is stronger but shows a little more.</li>
<li>Carry on to the next pair of squares in the row without cutting the yarn.</li></ol>
<h2>How to join granny squares with a slip stitch</h2>
<ol><li>Hold two squares right sides together (the ridge will be on the back) or wrong sides together (the ridge shows on the front).</li>
<li>Make a slip knot on your hook. Insert the hook through the corner space of both squares, yarn over and pull through everything on the hook.</li>
<li>Insert through the next pair of matching stitches (back loops for a flatter seam, both loops for a firmer one), yarn over and pull through both the squares and the loop on your hook.</li>
<li>Repeat to the corner, then add the next pair of squares and keep going. Keep it loose: a tight slip stitch seam puckers. Going up a hook size helps.</li></ol>
<h2>How to join granny squares with single crochet</h2>
<p>Hold the squares <strong>wrong sides together</strong> for a raised ridge on the front, or right sides together to hide it. Work one single crochet (UK double crochet) through both edges in each pair of stitches, and 1 sc in each corner space. This is the strongest of the hook joins, but it uses the most yarn and adds a little width. It looks great in a contrast colour.</p>
<h2>Mattress stitch for a flat, invisible seam</h2>
<p>Lay the two squares flat, right side up, edges touching. Bring a threaded needle up through the outer loop of the first stitch on one square, then across through the outer loop of the matching stitch on the other square. Zigzag between the two edges like the rungs of a ladder, and every few stitches pull the yarn gently so the edges close. The seam lies completely flat.</p>
<h2>How to join granny squares as you go</h2>
<p>Finish the first square completely. On the <strong>last round of the second square</strong>, work as usual until you reach a side that should touch the first square. Then:</p>
<ol><li><strong>At the corner:</strong> work the first 3 dc, then instead of ch 2, ch 1, slip stitch into the corner space of the finished square, ch 1, and work the next 3 dc into your own corner.</li>
<li><strong>Along the side:</strong> instead of each ch 1 between clusters, slip stitch into the matching ch-1 space of the finished square.</li>
<li><strong>At the next corner</strong> do the same as the first, then finish the round as normal.</li>
<li>Squares that touch two finished squares join on two sides; at a four-way corner, slip stitch into the join that's already there.</li></ol>
<p>This is the method most granny blanket makers end up loving: the blanket grows square by square and there's nothing to sew at the end. New to the square itself? Start with <a href="{href("how-to-crochet-a-granny-square.html")}">how to crochet a granny square</a>.</p>
<h2>Join in strips to save time</h2>
<p>Instead of joining every square to its neighbour separately, join all the squares into rows with one long seam per row, then join the rows with long seams the other way. When you cross a corner, catch both corners and keep going. A blanket 8 squares across and 10 down then has just 16 long seams instead of 142 short ones, and only about 32 ends to weave in.</p>
<h2>Common problems</h2>
<ul><li><strong>Seams pucker:</strong> the join is too tight. Use a hook one size up for slip stitch or sc joins, or pull sewn stitches only until they close.</li>
<li><strong>Squares don't line up:</strong> count stitches from each corner and pin matching corners before you start. Blocking fixes small size differences.</li>
<li><strong>Corners have holes:</strong> work into both corner chain spaces, and at four-way corners go into the join already made.</li>
<li><strong>The seam shows too much:</strong> use matching yarn, join through the back loops, or switch to mattress stitch.</li></ul>
<p>Once it's joined, add a border, and if it's a gift or for sale, see <a href="{href("how-to-price-a-crochet-blanket.html")}">how to price a crochet blanket</a>. Planning the next one? The <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> works out squares and yarn for any size.</p>
<p class="note">These joining methods are standard crochet finishing techniques, taught the same way by established craft publishers and designers (Gathered, Yarnspirations, We Are Knitters, Make:, Marching North; checked 27 Nov 2026). Our wording and diagrams. Yarn amounts are our own estimates.</p>
</div></div></section>'''
gj_faq = [
    ("What is the easiest way to join granny squares?", "Whip stitch. Hold two squares right sides together and sew through the back loops of matching stitches with a tapestry needle. It needs no crochet skill and gives a flat seam."),
    ("What is the best way to join granny squares for a blanket?", "Join as you go saves the most time because there is no sewing at the end. For squares that are already made, a slip stitch or whip stitch join in long strips is quick and neat."),
    ("Should I join granny squares right sides or wrong sides together?", "Right sides together hides the seam ridge on the back. Wrong sides together puts the ridge on the front, which looks good with a single crochet join in a contrast colour."),
    ("How much yarn do I need to join granny squares?", "By our rough estimate for worsted yarn, a sewn seam uses about 2.5 to 3 times its length in yarn, a slip stitch join about 4 times and a single crochet join about 6 times. Join as you go uses no extra yarn."),
    ("Do you block granny squares before joining?", "Yes, if you can. Blocking makes all the squares the same size so the seams line up and the blanket lies flat."),
    ("How do you join granny squares without sewing?", "Use a hook join (slip stitch or single crochet) through both edges, or join as you go on the last round of each new square."),
    ("How many seams does a granny square blanket have?", "If you join in strips, one long seam between each row and column: squares across minus 1, plus squares down minus 1. An 8 by 10 blanket has 16 long seams."),
]
SHOP_FOR["how-to-join-granny-squares.html"] = ["yarn-stash-tracker", "crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "christmas-gift-tags"]
page("how-to-join-granny-squares.html", "How to Join Granny Squares: 5 Easy Ways + Yarn Calculator | Purl & Paper",
     "How to join granny squares: whip stitch, mattress stitch, slip stitch, single crochet and join as you go, with diagrams and a joining yarn calculator.",
     gjp, gj_faq, "How to join granny squares", app_name="Granny square joining calculator")


# ======== HOW TO INCREASE IN KNITTING ========
# Demand: 'knitting how to increase stitches' (SERP 27 Nov: Gathered (m1l, m1r, kfb), Annie's, Yarnspirations, Wikipedia, DMC video,
# Lion Brand '5 ways', Vogue Knitting increasing, We Are Knitters, Knitty, WonderHowTo). KFB, M1L/M1R, yarn over, lifted increases
# and backward-loop are standard techniques; wording and drawings ours.

def _ki_svg(kind, label):
    """Two needles with stitches; the highlighted move shows the increase."""
    st = ""
    for i in range(5):  # stitches on the left needle (right side of picture)
        cx = 168 + i * 18
        st += f'<path d="M{cx - 7} 58 Q{cx} 98 {cx + 7} 58" fill="none" stroke="#5b6b94" stroke-width="5" stroke-linecap="round"/>'
    for i in range(4):  # stitches already on the right needle
        cx = 30 + i * 18
        st += f'<path d="M{cx - 7} 58 Q{cx} 98 {cx + 7} 58" fill="none" stroke="#5b6b94" stroke-width="5" stroke-linecap="round"/>'
    needles = ('<rect x="10" y="52" width="104" height="10" rx="5" fill="#d7c39a" stroke="#1f2a44" stroke-width="1.5"/><path d="M114 52 l18 5 l-18 5z" fill="#d7c39a" stroke="#1f2a44" stroke-width="1.5"/>'
               '<rect x="150" y="52" width="110" height="10" rx="5" fill="#d7c39a" stroke="#1f2a44" stroke-width="1.5"/><path d="M150 52 l-18 5 l18 5z" fill="#d7c39a" stroke="#1f2a44" stroke-width="1.5"/>')
    fabric = "".join(f'<path d="M{x - 7} {y} l7 9 l7 -9" fill="none" stroke="#9aa6c4" stroke-width="3"/>' for x in range(30, 260, 18) if not 100 < x < 160 for y in (108, 122))
    hi = ""
    if kind == "kfb":
        hi = ('<path d="M161 58 Q168 98 175 58" fill="none" stroke="#b8326a" stroke-width="5.5" stroke-linecap="round"/>'
              '<path d="M120 40 C140 20 160 30 166 54" fill="none" stroke="#e39a14" stroke-width="2.5" marker-end="url(#ar)"/><text x="104" y="30" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">1 front</text>'
              '<path d="M200 30 C190 40 178 46 172 60" fill="none" stroke="#e39a14" stroke-width="2.5" stroke-dasharray="4 3" marker-end="url(#ar)"/><text x="196" y="24" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">2 back</text>')
    elif kind in ("m1l", "m1r"):
        hi = '<path d="M106 92 Q133 104 160 92" fill="none" stroke="#b8326a" stroke-width="5" stroke-linecap="round"/><text x="122" y="118" font-size="12" fill="#b8326a" font-family="Inter,sans-serif">bar</text>'
        if kind == "m1l":
            hi += '<path d="M150 40 C140 60 136 80 133 96" fill="none" stroke="#e39a14" stroke-width="2.5" marker-end="url(#ar)"/><text x="135" y="30" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif" text-anchor="middle">bar: front to back, knit tbl</text>'
        else:
            hi += '<path d="M118 130 C128 120 132 108 133 96" fill="none" stroke="#e39a14" stroke-width="2.5" marker-end="url(#ar)"/><text x="135" y="30" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif" text-anchor="middle">bar: back to front, knit it</text>'
    elif kind == "yo":
        hi = '<path d="M112 40 C128 30 140 44 132 60 C126 74 118 70 116 60" fill="none" stroke="#b8326a" stroke-width="5" stroke-linecap="round"/><text x="96" y="26" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">yarn over the needle</text>'
    elif kind == "lifted":
        hi = '<path d="M161 104 Q168 118 175 104" fill="none" stroke="#b8326a" stroke-width="5" stroke-linecap="round"/><path d="M146 40 C150 70 158 90 163 106" fill="none" stroke="#e39a14" stroke-width="2.5" marker-end="url(#ar)"/><text x="120" y="30" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">leg of the stitch below</text>'
    else:  # backward loop
        hi = '<path d="M108 58 Q118 30 124 58 Q118 74 110 64" fill="none" stroke="#b8326a" stroke-width="5" stroke-linecap="round"/><text x="70" y="26" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">twist a loop onto the needle</text>'
    return (f'<svg viewBox="0 0 270 150" role="img" aria-label="{e(label)}"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#e39a14"/></marker></defs>'
            f'<rect x="0" y="0" width="270" height="150" rx="10" fill="#f6f1e6"/>{fabric}{st}{needles}{hi}</svg>')

KI_METHODS = [
    ("kfb", "Knit front and back (kfb)", "Knit into the stitch, don't drop it, then knit into its back loop. Easy; leaves a small bump."),
    ("m1l", "Make 1 left (M1L)", "Lift the bar between stitches from the front and knit it through the back loop. Leans left, nearly invisible."),
    ("m1r", "Make 1 right (M1R)", "Lift the bar from the back and knit it through the front loop. Leans right; the mirror of M1L."),
    ("yo", "Yarn over (yo)", "Wrap the yarn over the right needle before the next stitch. Makes a deliberate hole, as in lace."),
    ("lifted", "Lifted increase (RLI / LLI)", "Knit into a leg of the stitch in the row below. The most invisible increase in stocking stitch."),
    ("bl", "Backward loop (M1)", "Twist a loop of yarn onto the right needle. The quickest, but it can look loose."),
]
ki_cards = "".join(f'<figure class="gq-fig"><div>{_ki_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in KI_METHODS)

kip = top("How to increase in knitting", "Six ways to add a stitch, from knit front and back to make 1 left and right, with our own diagrams, a picker that tells you which increase to use, and how to space increases evenly.", "How to increase in knitting") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the easiest increase is <strong>knit front and back (kfb)</strong>: knit the stitch as normal but leave it on the left needle, then knit into its back loop and slide it off. One stitch becomes two. For a near-invisible increase, use <strong>make 1 (M1L or M1R)</strong>: pick up the horizontal bar between two stitches with the left needle and knit it <em>twisted</em> so no hole forms. A <strong>yarn over</strong> also adds a stitch, but leaves a hole on purpose. If your pattern just says "M1", it usually means M1L.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Which increase should I use?</h3>
<div class="field"><span class="label" id="ki-hole-l">Do you want a hole?</span><div class="seg" role="group" aria-labelledby="ki-hole-l" id="ki-hole"><button type="button" data-v="no" aria-pressed="true">No hole</button><button type="button" data-v="yes" aria-pressed="false">Yes, a lacy hole</button></div></div>
<div class="field"><span class="label" id="ki-where-l">Where is it?</span><div class="seg" role="group" aria-labelledby="ki-where-l" id="ki-where"><button type="button" data-v="edge" aria-pressed="true">At the edges</button><button type="button" data-v="mid" aria-pressed="false">Across the row</button><button type="button" data-v="pair" aria-pressed="false">Raglan or paired</button></div></div>
<div class="field"><span class="label" id="ki-lvl-l">Your level</span><div class="seg" role="group" aria-labelledby="ki-lvl-l" id="ki-lvl"><button type="button" data-v="new" aria-pressed="true">Beginner</button><button type="button" data-v="ok" aria-pressed="false">Comfortable</button></div></div>
<div class="field"><label for="ki-st">Stitch pattern</label><select id="ki-st"><option value="st">Stocking stitch (knit side smooth)</option><option value="gt">Garter stitch</option><option value="rib">Ribbing</option></select></div>
<p class="sub">Our suggestions follow how craft publishers usually teach increases. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="ki-out" data-ev="{href("increase-decrease-calculator.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Knitting increases at a glance</h2>
<div class="gq-figs">{ki_cards}</div>
<h2>How to knit front and back (kfb)</h2>
<ol><li>Insert the right needle into the next stitch knitwise and knit it, but <strong>don't slide the old stitch off</strong> the left needle.</li>
<li>Swing the right needle behind and insert it into the <strong>back loop</strong> of that same stitch, from right to left.</li>
<li>Wrap the yarn and pull the loop through, then slip the old stitch off. You now have two stitches where there was one.</li></ol>
<p>The second stitch has a little horizontal bar at its base, like a purl bump. In garter stitch it hides; in stocking stitch it shows slightly, which is fine at edges. The purl version is pfb.</p>
<h2>How to make 1 left (M1L)</h2>
<ol><li>Look between the last stitch on your right needle and the next one on the left: there's a horizontal strand, the bar.</li>
<li>With the left needle, pick up the bar <strong>from front to back</strong>.</li>
<li>Knit it <strong>through the back loop</strong> (insert the right needle into the back of the lifted strand). The twist closes the hole and the new stitch leans left.</li></ol>
<h2>How to make 1 right (M1R)</h2>
<ol><li>With the left needle, pick up the bar <strong>from back to front</strong>.</li>
<li>Knit it <strong>through the front loop</strong>. This twists it the other way, so the stitch leans right.</li></ol>
<p>M1L and M1R are a mirror pair. Use one on each side of a centre line (a raglan seam, a sleeve edge) and the increases look matched. If the bar feels too tight to knit, you may have picked it up the wrong way round: try the other one.</p>
<h2>How to do a yarn over increase</h2>
<p>Bring the yarn to the front between the needles, then knit the next stitch: the yarn goes over the right needle and makes an extra loop. On the next row, work that loop as a normal stitch and it leaves a neat eyelet hole. That's what lace is built from, and it's a pretty choice for raglan lines or a baby blanket edge. Want no hole? Knit the yarn over through the back loop on the next row to twist it shut.</p>
<h2>Lifted increases (RLI and LLI)</h2>
<p><strong>Right lifted increase (RLI):</strong> with the right needle, lift the right leg of the stitch in the row below the next stitch onto the left needle and knit it, then knit the stitch itself. <strong>Left lifted increase (LLI):</strong> after knitting a stitch, use the left needle to lift the left leg of the stitch two rows below the one you just made, and knit it. Lifted increases pull a little yarn from the row below, so they're nearly invisible in stocking stitch. Don't stack them on top of each other every row, or the fabric puckers.</p>
<h2>Backward loop increase</h2>
<p>Wrap the yarn around your thumb, slip the loop onto the right needle and tighten it. It's the same as a backward loop cast on, worked mid-row. It's fast but can look loose and a little holey; it's handy for adding stitches at the very end of a row, or for underarm stitches on a top-down sweater.</p>
<h2>How to increase evenly across a row</h2>
<p>Divide your stitches by the number of increases to find how often to add one. For 80 stitches and 8 increases, that's one increase every 10 stitches: knit 5, M1, then (knit 10, M1) 7 more times, knit 5. Starting with half a section keeps the increases away from the edges. Our <a href="{href("increase-decrease-calculator.html")}">increase evenly calculator</a> writes this out for any numbers.</p>
<h2>Common increase problems</h2>
<ul><li><strong>A hole where you didn't want one:</strong> an M1 that wasn't twisted, or an accidental yarn over. Lift the bar the right way and knit through the back (M1L) or front (M1R).</li>
<li><strong>Too many stitches:</strong> a stray yarn over is the usual cause, often when the yarn sits in front before a knit stitch. Count after every increase row.</li>
<li><strong>Increase looks lumpy:</strong> try an M1 or lifted increase instead of kfb in stocking stitch.</li>
<li><strong>Dropped one?</strong> See <a href="{href("how-to-fix-a-dropped-stitch.html")}">how to fix a dropped stitch</a>.</li></ul>
<p>New to knitting? Start with <a href="{href("how-to-knit-and-purl.html")}">how to knit and purl</a>, then come back here. Every abbreviation on this page is in the <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a>, and the <a href="{href("row-counter.html")}">row counter</a> keeps track of increase rows.</p>
<p class="note">These are standard knitting techniques, described the same way by established craft publishers (Gathered, Lion Brand, Vogue Knitting, Yarnspirations, We Are Knitters; checked 27 Nov 2026). Our wording and diagrams.</p>
</div></div></section>'''
ki_faq = [
    ("What is the easiest way to increase in knitting?", "Knit front and back (kfb): knit the stitch but leave it on the needle, knit into its back loop as well, then slip it off. One stitch becomes two."),
    ("What does M1 mean in knitting?", "Make 1: pick up the bar between two stitches and knit it twisted to add a stitch. Plain M1 usually means M1L, which leans left. M1R leans right."),
    ("What is the difference between M1L and M1R?", "M1L picks up the bar from front to back and knits it through the back loop, leaning left. M1R picks it up from back to front and knits it through the front loop, leaning right."),
    ("Which knitting increase is invisible?", "Lifted increases and M1 are the least visible in stocking stitch. Kfb leaves a small bump and a yarn over leaves a hole."),
    ("Why does my M1 leave a hole?", "The lifted bar wasn't twisted. Knit an M1L through the back loop and an M1R through the front loop and the hole closes."),
    ("How do you increase evenly across a row in knitting?", "Divide the stitch count by the number of increases to get the spacing, then put half a space at each end. For 80 stitches and 8 increases: k5, M1, (k10, M1) 7 times, k5."),
    ("Does a yarn over add a stitch?", "Yes. A yarn over makes an extra loop on the needle that you work as a stitch on the next row, leaving a decorative hole."),
]
SHOP_FOR["how-to-increase-knitting.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("how-to-increase-knitting.html", "How to Increase in Knitting: KFB, M1L, M1R, Yarn Over | Purl & Paper",
     "How to increase in knitting: kfb, M1L, M1R, yarn over, lifted and backward loop increases, with diagrams, an increase picker and spacing tips.",
     kip, ki_faq, "How to increase in knitting", app_name="Knitting increase picker")
