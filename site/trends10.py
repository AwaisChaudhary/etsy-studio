# ---------------- 27 Nov 2026 run 10: CROCHET INCREASE + EMBROIDERY TRANSFER + SEW A BUTTON ----------------
# Executed from build.py after joininc.py (shares page(), top(), href(), e(), SHOP_FOR).
# Demand evidence in DEMAND.md (RADAR 27 Nov run 10). Drawings our own SVG; wording our own. JS in assets/app.js (ci-*, et-*, bs-*).

_AR = '<defs><marker id="ar{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#e39a14"/></marker></defs>'
_T = 'font-family="Inter,sans-serif" font-size="12" fill="#1f2a44"'

# ======== HOW TO INCREASE IN CROCHET ========
# Demand: 'how to increase in crochet' (SERP 27 Nov: Mary Maxim x3, DMC video, Gathered, Yarnspirations, Dummies x2, Hobbii,
# Annie's, EasyCrochet sc inc tutorial, Pocket Yarnlings '15 ways', Nordic Hook, Lion Brand lesson). Standard technique; wording ours.

def _sym(kind, x, y, col):
    """Crochet chart symbol centred on x, y (sc = x, hdc = T, dc = T with a bar)."""
    if kind == "sc":
        return f'<path d="M{x-6} {y-6} L{x+6} {y+6} M{x+6} {y-6} L{x-6} {y+6}" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>'
    s = f'<path d="M{x} {y-12} L{x} {y+12} M{x-7} {y-12} L{x+7} {y-12}" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>'
    if kind == "dc":
        s += f'<path d="M{x-4} {y+2} L{x+4} {y-4}" stroke="{col}" stroke-width="2.4" stroke-linecap="round"/>'
    return s

def _ci_svg(kind, label, n):
    base = "".join(f'<ellipse cx="{x}" cy="118" rx="12" ry="6" fill="none" stroke="#9aa6c4" stroke-width="2.4"/>' for x in range(34, 260, 32))
    st = "sc" if kind in ("sc", "inv", "edge") else kind
    up = ""
    for i, x in enumerate(range(34, 260, 32)):
        if kind == "edge" and i in (0, 7):
            for dx in (-9, 9):
                up += f'<line x1="{x}" y1="110" x2="{x + dx}" y2="80" stroke="#b8326a" stroke-width="1.4" opacity=".6"/>' + _sym(st, x + dx, 72, "#b8326a")
        elif kind != "edge" and i == 3:
            for dx in (-11, 11):
                up += f'<line x1="{x}" y1="110" x2="{x + dx}" y2="80" stroke="#b8326a" stroke-width="1.4" opacity=".6"/>' + _sym(st, x + dx, 66, "#b8326a")
        else:
            up += _sym(st, x, 72, "#1f2a44")
    note = {"sc": "2 sc in one stitch", "hdc": "2 hdc in one stitch", "dc": "2 dc in one stitch",
            "inv": "1st: front loop only, 2nd: both loops", "edge": "inc in first and last stitch"}[kind]
    extra = ""
    if kind == "inv":
        extra = f'<text x="118" y="40" {_T} text-anchor="end">FLO</text><text x="154" y="40" {_T}>BLO+FLO</text>'
    return (f'<svg viewBox="0 0 280 150" role="img" aria-label="{e(label)}"><rect width="280" height="150" rx="10" fill="#f6f1e6"/>'
            f'{base}{up}{extra}<text x="140" y="142" {_T} text-anchor="middle" fill="#b8326a">{e(note)}</text></svg>')

CI_METHODS = [
    ("sc", "Single crochet increase (sc inc)", "Work 2 sc into the same stitch. The one in almost every amigurumi and circle pattern."),
    ("hdc", "Half double increase", "Work 2 hdc into the same stitch. Same move, taller stitch."),
    ("dc", "Double crochet increase", "Work 2 dc into the same stitch. Leaves a small gap between the pair, which is normal."),
    ("inv", "Invisible increase", "First sc in the front loop only, second in both loops. The pair sits flatter, so no lumps on toys."),
    ("edge", "Increase at the edges", "Work 2 sts in the first and last stitch of a row to widen a triangle, shawl or sleeve."),
]
ci_cards = "".join(f'<figure class="gq-fig"><div>{_ci_svg(k, n + ": " + d, i)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for i, (k, n, d) in enumerate(CI_METHODS))

cip = top("How to increase in crochet", "How to add stitches in crochet: the single crochet increase, increases in taller stitches, the invisible increase and edge increases, each with our own chart diagram. Plus a writer that spaces your increases evenly across any round or row.", "How to increase in crochet") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to increase in crochet, work <strong>two stitches into the same stitch</strong>. For a single crochet increase (written <strong>inc</strong> or <strong>2 sc in next st</strong>), work one single crochet, then put your hook back into that same stitch and work another one. One stitch becomes two, so the row grows by one. To increase evenly, divide your stitches by the number of increases: going from 24 to 30 stitches is 6 increases, so <strong>(sc 3, inc) 6 times</strong>. In UK patterns single crochet is called double crochet (dc), but the move is the same.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Crochet increase writer</h3>
<div class="row2"><div class="field"><label for="ci-a">Stitches you have now</label><input type="number" id="ci-a" value="24" min="1" max="500" step="1" inputmode="numeric"></div>
<div class="field"><label for="ci-b">Stitches you want</label><input type="number" id="ci-b" value="30" min="2" max="1000" step="1" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="ci-s">Stitch</label><select id="ci-s"><option value="sc">Single crochet</option><option value="hdc">Half double crochet</option><option value="dc">Double crochet</option></select></div>
<div class="field"><span class="label" id="ci-w-l">Working</span><div class="seg" role="group" aria-labelledby="ci-w-l" id="ci-w"><button type="button" data-v="round" aria-pressed="true">In the round</button><button type="button" data-v="row" aria-pressed="false">In rows</button></div></div></div>
<div class="field"><span class="label" id="ci-t-l">Terms</span><div class="seg" role="group" aria-labelledby="ci-t-l" id="ci-t"><button type="button" data-v="us" aria-pressed="true">US</button><button type="button" data-v="uk" aria-pressed="false">UK</button></div></div>
<p class="sub">It writes the round or row for you and checks the stitch count. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="ci-out" data-dec="{href("how-to-crochet-decrease.html")}" data-circ="{href("crochet-circle-calculator.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Crochet increases at a glance</h2>
<div class="gq-figs">{ci_cards}</div>
<p class="sub">Drawn as crochet chart symbols: × is single crochet, T is half double, T with a bar is double crochet. Pink marks the increase.</p>
<h2>How to do a single crochet increase, step by step</h2>
<ol><li><strong>Work a single crochet</strong> as normal: insert the hook into the stitch, yarn over, pull up a loop, yarn over and pull through both loops.</li>
<li><strong>Go back into the same stitch.</strong> Insert the hook into the exact stitch you just worked, not the next one.</li>
<li><strong>Work a second single crochet</strong> there. You now have two stitches sitting on one stitch of the row below.</li>
<li><strong>Carry on</strong> with the next stitch as the pattern says. Count at the end of the row or round: it should have grown by one for every increase.</li></ol>
<p>Stitch markers help a lot here: put one in the first stitch of each round, and in a tricky pattern clip one onto each increase so you can count them.</p>
<h2>How to increase with taller stitches</h2>
<p>Half double, double and treble crochet increase in exactly the same way: work the stitch, then work another one into the same place. With taller stitches the pair fans out and leaves a small gap at the top, which is normal and blocks out. Some patterns write it as <strong>2 dc in next st</strong>; a <strong>V-stitch</strong> is the same idea with a chain between, (dc, ch 1, dc) in one stitch, for a lacier look.</p>
<h2>The invisible increase</h2>
<p>A normal sc inc can leave a little bump or a hole, which shows on amigurumi. For a neater one, work the <strong>first single crochet into the front loop only</strong>, then the <strong>second into both loops</strong> of the same stitch. The pair sits flatter and the gap closes. It's worth learning if you make toys; for blankets the normal increase is fine.</p>
<h2>How to increase evenly in a round</h2>
<p>Flat circles grow by the same number of stitches every round: 6 for single crochet, about 8 for half double and 12 for double crochet. Round 2 is "inc in every stitch", round 3 is (sc 1, inc), round 4 is (sc 2, inc) and so on. That puts the increases in the same place every round, which slowly turns a circle into a hexagon. To keep it round, <strong>stagger the increases</strong>: on every other round start with half of the plain stitches, for example sc 1, inc, (sc 2, inc) 5 times, sc 1 instead of (sc 2, inc) 6 times. The writer above gives you both versions. For the full chart, see the <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a>.</p>
<h2>How to increase at the end of a row</h2>
<p>Work 2 stitches into the first stitch, 2 into the last, or both, to widen a piece at the edges, as in a triangle shawl or a sleeve. For a neater edge, put the increase one stitch in from the edge instead. To add several stitches at once at the end of a row, chain the number you need (plus the turning chain) and work back along the chains.</p>
<h2>Why is my crochet getting wider (or not)?</h2>
<ul><li><strong>Piece slowly gets wider without meaning to:</strong> you're working 2 stitches into the first or last stitch by accident, often into the turning chain. Count each row.</li>
<li><strong>Circle cups like a bowl:</strong> not enough increases, or your stitches are tight. Check the count, or go up a hook size.</li>
<li><strong>Circle ruffles like a frill:</strong> too many increases. Count the last round and rip back to where it went wrong.</li>
<li><strong>Need to go smaller?</strong> See <a href="{href("how-to-crochet-decrease.html")}">how to decrease in crochet</a>, the mirror of this page.</li></ul>
<p>New to crochet? Start with <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a> and the <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>, check pattern words on the <a href="{href("crochet-terms.html")}">US vs UK crochet terms</a> chart, and keep count of rounds with the <a href="{href("row-counter.html")}">row counter</a>. Knitting too? See <a href="{href("how-to-increase-knitting.html")}">how to increase in knitting</a>.</p>
<p class="note">Increasing is a standard crochet technique, described the same way by established craft publishers (Yarnspirations, Gathered, Mary Maxim, Hobbii, Crocheting For Dummies; checked 27 Nov 2026). Our wording and diagrams.</p>
</div></div></section>'''
ci_faq = [
    ("How do you increase in crochet?", "Work two stitches into the same stitch. For a single crochet increase, work one sc, then insert the hook into the same stitch again and work a second sc."),
    ("What does inc mean in crochet?", "Increase: work 2 stitches in the same stitch, usually single crochet in amigurumi patterns. Some patterns write it as 2 sc in next st."),
    ("How do you increase evenly in crochet?", "Divide the stitches you have by the number of increases. From 24 to 30 is 6 increases, and 24 divided by 6 is 4, so work (sc 3, inc) 6 times."),
    ("What is an invisible increase in crochet?", "Work the first single crochet in the front loop only and the second in both loops of the same stitch. It sits flatter than a normal increase and hides the gap."),
    ("How many stitches do you increase each round in a crochet circle?", "Usually 6 for single crochet, about 8 for half double and 12 for double crochet, spread evenly around the round."),
    ("Why is my crochet circle turning into a hexagon?", "The increases are stacking in the same place every round. Stagger them by starting every other round with half the plain stitches before the first increase."),
    ("Does an increase count as one stitch or two?", "Two. An increase makes two stitches out of one, so each increase adds one stitch to your count."),
]
SHOP_FOR["how-to-crochet-increase.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("how-to-crochet-increase.html", "How to Increase in Crochet (sc inc, Invisible) | Purl & Paper",
     "How to increase in crochet: single crochet increase, taller stitches, the invisible increase and edge increases, plus a writer that spaces increases evenly.",
     cip, ci_faq, "How to increase in crochet", app_name="Crochet increase writer")

# ======== HOW TO TRANSFER AN EMBROIDERY PATTERN ========
# Demand: 'how to transfer embroidery pattern to fabric' (SERP 27 Nov run 9: EGA x2 incl. PDF guide, LoveCrafts 4 ways, Instructables,
# Make:, Twig and Tale, eHow, Gathered, Needle 'n Thread x2, Clever Poppy) and 'to dark fabric' (SERP run 10: Needle 'n Thread x4,
# Sublime Stitching dark fabrics, Cutesy Crafts, PieceWork, practicalembroidery.eu tissue paper, EGA 5 methods). Standard methods.

def _et_svg(kind, label):
    hoop = '<circle cx="200" cy="78" r="48" fill="#fbf8f1" stroke="#c9a46a" stroke-width="6"/>'
    flower = 'M200 52 C214 62 214 74 200 80 C186 74 186 62 200 52 M200 80 C214 86 226 98 214 108 M200 80 C186 86 174 98 186 108 M200 80 L200 118'
    if kind == "light":
        art = ('<rect x="20" y="30" width="110" height="92" rx="6" fill="#bfe3e0" stroke="#1f2a44" stroke-width="2"/><path d="M75 30 V122 M20 76 H130" stroke="#1f2a44" stroke-width="2"/>'
               '<rect x="34" y="42" width="82" height="70" fill="#fff" opacity=".85"/><path d="' + flower.replace("200", "75").replace("214", "89").replace("186", "61").replace("226", "101").replace("174", "49") + '" transform="translate(0 -6)" fill="none" stroke="#1f2a44" stroke-width="2" stroke-dasharray="3 3"/>'
               f'<text x="75" y="140" {_T} text-anchor="middle">trace on a window</text>')
        tail = f'<path d="{flower}" fill="none" stroke="#2f8f8a" stroke-width="2.4"/>'
    elif kind == "wss":
        art = (f'<rect x="22" y="36" width="104" height="80" rx="4" fill="#e8f4f3" stroke="#2f8f8a" stroke-width="2" stroke-dasharray="6 4"/>'
               f'<text x="74" y="80" {_T} text-anchor="middle">stick-on</text><text x="74" y="96" {_T} text-anchor="middle">stabilizer</text>'
               f'<text x="74" y="140" {_T} text-anchor="middle">stitch, then rinse away</text>')
        hoop = '<circle cx="200" cy="78" r="48" fill="#2b3350" stroke="#c9a46a" stroke-width="6"/><rect x="170" y="48" width="60" height="60" fill="#e8f4f3" opacity=".7"/>'
        tail = f'<path d="{flower}" fill="none" stroke="#f4a823" stroke-width="2.6"/>'
    elif kind == "carbon":
        art = ('<rect x="24" y="34" width="100" height="80" fill="#fff" stroke="#1f2a44" stroke-width="1.6"/><rect x="30" y="40" width="100" height="80" fill="#f2f2f2" stroke="#9aa6c4" stroke-width="1.6"/>'
               '<path d="M100 54 L120 30 L126 34 L106 60z" fill="#e39a14" stroke="#1f2a44" stroke-width="1.4"/>'
               f'<text x="76" y="140" {_T} text-anchor="middle">white carbon paper</text>')
        hoop = '<circle cx="200" cy="78" r="48" fill="#2b3350" stroke="#c9a46a" stroke-width="6"/>'
        tail = f'<path d="{flower}" fill="none" stroke="#ffffff" stroke-width="2" stroke-dasharray="4 3"/>'
    elif kind == "tissue":
        art = ('<path d="M24 38 L124 34 L128 116 L28 120z" fill="#fff8e8" stroke="#1f2a44" stroke-width="1.6" opacity=".95"/>'
               '<path d="M30 46 h88 M30 110 h88" stroke="#b8326a" stroke-width="2" stroke-dasharray="6 5"/>'
               f'<text x="76" y="140" {_T} text-anchor="middle">tack on tissue, tear away</text>')
        hoop = '<circle cx="200" cy="78" r="48" fill="#7c8a5c" stroke="#c9a46a" stroke-width="6"/>'
        tail = f'<path d="{flower}" fill="none" stroke="#fbf8f1" stroke-width="2.6"/>'
    else:  # iron-on
        art = ('<path d="M30 96 C30 60 70 46 118 46 L126 46 L126 96z" fill="#d7dbe6" stroke="#1f2a44" stroke-width="2"/><rect x="58" y="34" width="50" height="10" rx="5" fill="#1f2a44"/>'
               '<path d="M40 112 h86" stroke="#b8326a" stroke-width="3"/>'
               f'<text x="76" y="140" {_T} text-anchor="middle">iron-on: mirror image</text>')
        tail = f'<path d="{flower}" fill="none" stroke="#b8326a" stroke-width="2.4"/>'
    return (f'<svg viewBox="0 0 280 150" role="img" aria-label="{e(label)}"><rect width="280" height="150" rx="10" fill="#f6f1e6"/>'
            f'{art}<path d="M140 76 h12" stroke="#e39a14" stroke-width="3"/><path d="M150 70 l8 6 l-8 6z" fill="#e39a14"/>{hoop}{tail}</svg>')

ET_METHODS = [
    ("light", "Trace with light", "Tape the pattern to a sunny window or light pad, fabric on top, and trace with a water-soluble or erasable pen. Best for light, thin fabric."),
    ("wss", "Water-soluble stabilizer", "Print or trace onto a stick-on stabilizer sheet, stick it on, stitch through it, then rinse it away. Works on any colour."),
    ("carbon", "Transfer (carbon) paper", "Lay dressmaker's carbon paper face down on the fabric, the pattern on top, and draw over the lines. White or yellow shows on dark fabric."),
    ("tissue", "Tissue paper", "Trace onto tissue paper, tack it to the fabric, stitch through it and tear the paper away. No marks, good for textured fabric."),
    ("iron", "Iron-on transfer", "Trace the reversed design with a transfer pen or pencil, then iron it onto the fabric. Lines are permanent, so cover them."),
]
et_cards = "".join(f'<figure class="gq-fig"><div>{_et_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in ET_METHODS)
def _etseg(i, lab, opts):
    return f'<div class="field"><span class="label" id="et-{i}-l">{lab}</span><div class="seg" role="group" aria-labelledby="et-{i}-l" id="et-{i}">' + "".join(
        f'<button type="button" data-v="{v}" aria-pressed="{"true" if j == 0 else "false"}">{t}</button>' for j, (v, t) in enumerate(opts)) + '</div></div>'

etp = top("How to transfer an embroidery pattern", "Five ways to get an embroidery design onto fabric, from tracing on a window to stick-on stabilizer for dark fabric, each with our own drawing. Answer three questions and the picker tells you which method to use.", "How to transfer an embroidery pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> on <strong>light, thin fabric</strong> like cotton or linen, tape the pattern to a window or light pad, put the fabric on top and trace the lines with a <strong>water-soluble pen</strong>; the marks rinse out when you're done. On <strong>dark or thick fabric</strong> (denim, felt, a sweatshirt), you can't see through, so print or trace the design onto <strong>water-soluble stick-on stabilizer</strong>, stick it on, stitch through it and rinse it away. If the item can't get wet, trace onto <strong>tissue paper</strong>, tack it on, stitch and tear it off. Always test any pen on a scrap first.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Which transfer method should I use?</h3>
{_etseg("c", "Fabric colour", [("light", "Light"), ("mid", "Medium"), ("dark", "Dark")])}
{_etseg("k", "Fabric", [("thin", "Thin, smooth (cotton, linen)"), ("thick", "Thick or textured (denim, felt, towel, knit)")])}
{_etseg("w", "Can it be washed after?", [("yes", "Yes"), ("no", "No, keep it dry")])}
{_etseg("d", "Design", [("fine", "Fine lines or lettering"), ("bold", "Simple, bold shapes")])}
<p class="sub">Our suggestions follow how embroidery guilds and craft publishers teach transfers. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="et-out" data-pat="{href("embroidery-patterns.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Embroidery transfer methods at a glance</h2>
<div class="gq-figs">{et_cards}</div>
<h2>Method 1: trace it with light</h2>
<ol><li>Iron the fabric smooth. Print the pattern at the size you want, or draw it.</li>
<li>Tape the pattern to a bright window, a light pad or a tablet screen turned to full white brightness. Tape the fabric over it, the grain straight.</li>
<li>Trace the lines with a <strong>water-soluble fabric marker</strong> (rinses out with water), a <strong>heat-erasable pen</strong> (vanishes under an iron) or a sharp, light pencil whose lines your stitches will cover.</li>
<li>Put the fabric in the hoop and stitch. Remove water-soluble marks by soaking in cool water, not by ironing, which can set them.</li></ol>
<p>Heat-erasable lines can come back faintly in the cold, so they're best on things that won't be washed or left in a cold car. Whatever you use, test it on a scrap of the same fabric first.</p>
<h2>Method 2: water-soluble stabilizer for dark fabric</h2>
<ol><li>Print the design straight onto a sheet of stick-on water-soluble stabilizer (most go through a home inkjet printer; check the pack), or trace it on with a pen.</li>
<li>Peel off the backing and stick it where you want the design. Hoop the fabric and stabilizer together.</li>
<li>Stitch through the stabilizer and fabric as normal. A slightly fuller needle helps it glide.</li>
<li>Trim the extra stabilizer, then soak the piece in lukewarm water until it dissolves. Rinse again if it feels sticky, and dry flat.</li></ol>
<p>This is the easiest way onto dark, thick or stretchy fabric, and it works for fine detail too. The piece has to survive a soak, so skip it for things that can't get wet.</p>
<h2>Method 3: transfer paper (dressmaker's carbon)</h2>
<p>Lay the fabric flat on a hard surface, put the transfer paper coloured side down on it and the pattern on top. Pin or tape so nothing slides, then go over every line with a ballpoint pen or a stylus, pressing firmly. Lift one corner to check before you unpin. Use <strong>white or yellow</strong> paper on dark fabric and a light colour on light fabric. Some carbon lines are hard to remove, so pick the wash-out kind.</p>
<h2>Method 4: tissue paper or tear-away</h2>
<p>Trace the design onto tissue paper or a tear-away stabilizer, tack it to the fabric with a few big running stitches around the edge, and stitch the design right through the paper. Then tear the paper away gently, holding the stitches down with a finger, and pick out the little bits with tweezers. It leaves no marks, so it's a good choice for towels, knitwear and things that can't get wet.</p>
<h2>Method 5: iron-on transfer pen or pencil</h2>
<p>Trace the design onto paper with a transfer pen or pencil, flip it face down on the fabric and press (don't slide) with a hot iron. Because you flip it, the design comes out <strong>mirrored</strong>, so reverse lettering first. Iron-on lines are permanent: use thin lines and cover them all with stitches. Many printed patterns and books come with ready-made iron-on transfers that work the same way.</p>
<h2>Tips for a clean transfer</h2>
<ul><li><strong>Mark the centre</strong> of the fabric and the pattern with a small cross so the design sits straight.</li>
<li><strong>Leave a margin</strong> of at least 3 in (8 cm) around the design so it fits your hoop and can be framed.</li>
<li><strong>Trace thin.</strong> A fine line is easier to cover than a thick one.</li>
<li><strong>Keep heat away</strong> from water-soluble marks until they've been rinsed out.</li></ul>
<p>Need a design to transfer? Make one with the free <a href="{href("embroidery-patterns.html")}">embroidery pattern generator</a>, then learn the stitches with <a href="{href("embroidery-stitches.html")}">embroidery stitches for beginners</a>. Counted cross stitch needs no transfer at all: see <a href="{href("how-to-cross-stitch.html")}">how to cross stitch</a>. Punch needle uses the same methods: see <a href="{href("punch-needle.html")}">punch needle</a>.</p>
<p class="note">These transfer methods are standard embroidery practice, described the same way by the Embroiderers' Guild of America, Needle 'n Thread, PieceWork and LoveCrafts (checked 27 Nov 2026). Our wording and drawings. Test any marker on a scrap first.</p>
</div></div></section>'''
et_faq = [
    ("What is the easiest way to transfer an embroidery pattern?", "On light fabric, tape the pattern to a bright window, put the fabric over it and trace the lines with a water-soluble fabric pen. The lines rinse out after stitching."),
    ("How do you transfer an embroidery pattern to dark fabric?", "Print or trace the design onto water-soluble stick-on stabilizer, stick it on, stitch through it and rinse it away. White carbon transfer paper or a white chalk pencil also works for simple designs."),
    ("Can I use a pencil to transfer embroidery?", "Yes, a sharp, light pencil works on light fabric if your stitches will cover the lines. Pencil doesn't always wash out completely, so keep the lines thin."),
    ("How do you transfer embroidery without a light box?", "Use a sunny window or a tablet screen on full brightness as a light source, or use stick-on stabilizer, carbon paper or tissue paper, which need no light at all."),
    ("Do water-soluble pen marks come out?", "Usually yes, with a soak in cool water. Don't iron over them first, as heat can set the marks. Test the pen on a scrap of your fabric."),
    ("Why is my iron-on transfer backwards?", "Iron-on transfers are flipped when you press them, so the design comes out mirrored. Reverse any lettering before you trace it."),
    ("How do you transfer an embroidery pattern onto a sweatshirt or towel?", "Use stick-on water-soluble stabilizer if it can be washed, or tissue paper tacked on and torn away after stitching. Both sit on top of the thick, fuzzy surface."),
]
SHOP_FOR["how-to-transfer-embroidery-pattern.html"] = ["machine-embroidery-business-spreadsheet", "crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "christmas-gift-tags"]
page("how-to-transfer-embroidery-pattern.html", "How to Transfer an Embroidery Pattern to Fabric | Purl & Paper",
     "How to transfer an embroidery pattern to fabric, including dark fabric: tracing, water-soluble stabilizer, carbon paper, tissue paper and iron-on, with a picker.",
     etp, et_faq, "How to transfer an embroidery pattern", app_name="Embroidery transfer method picker")

# ======== HOW TO SEW ON A BUTTON ========
# Demand: 'how to sew a button by hand' (SERP 27 Nov run 10: LoveCrafts x4 regions, Hobbycraft, Bob Vila, MasterClass, Tilly and the
# Buttons x2, Family Handyman, eHow, WonderHowTo, Treasurie, Make:, Gear Patrol). Standard hand-sewing technique; wording and drawings ours.
# Button spacing calculator: simple equal spacing between a top and bottom button (our maths).

def _bs_svg(step, label):
    btn = '<circle cx="140" cy="70" r="34" fill="#f4a823" stroke="#1f2a44" stroke-width="2.4"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4.4" fill="#1f2a44"/>' for x, y in ((128, 58), (152, 58), (128, 82), (152, 82)))
    fab = '<rect x="20" y="112" width="240" height="18" rx="3" fill="#8fb7d9"/><path d="M20 112 h240" stroke="#1f2a44" stroke-width="1"/>'
    s = ""
    if step == 1:
        s = ('<path d="M40 30 L60 30" stroke="#1f2a44" stroke-width="3"/><ellipse cx="66" cy="30" rx="6" ry="3" fill="none" stroke="#1f2a44" stroke-width="2"/>'
             '<path d="M72 30 C120 30 150 50 200 40 M72 32 C120 36 150 56 200 44" fill="none" stroke="#b8326a" stroke-width="2"/><circle cx="204" cy="42" r="5" fill="#b8326a"/>'
             f'<text x="140" y="72" {_T} text-anchor="middle">thread doubled, knot at the end</text>')
        return (f'<svg viewBox="0 0 280 150" role="img" aria-label="{e(label)}"><rect width="280" height="150" rx="10" fill="#f6f1e6"/>{fab}{s}'
                f'<path d="M140 108 v-20" stroke="#b8326a" stroke-width="2"/><text x="140" y="146" {_T} text-anchor="middle">start from the back</text></svg>')
    if step == 2:
        s = '<rect x="96" y="66" width="88" height="6" rx="3" fill="#d7c39a" stroke="#1f2a44" stroke-width="1.4"/>'
        t = "a pin or toothpick on top makes a gap"
    elif step == 3:
        s = '<path d="M128 58 L152 82 M152 58 L128 82" stroke="#b8326a" stroke-width="4"/><path d="M128 58 L128 82 M152 58 L152 82" stroke="#b8326a" stroke-width="2" opacity=".35"/>'
        t = "4 to 6 passes, in a cross or two bars"
    else:
        s = '<path d="M126 108 h28 M126 103 h28 M126 98 h28" stroke="#b8326a" stroke-width="3"/>'
        t = "remove pin, wrap the shank, knot behind"
    by = -14 if step == 4 else 0
    return (f'<svg viewBox="0 0 280 150" role="img" aria-label="{e(label)}"><rect width="280" height="150" rx="10" fill="#f6f1e6"/>{fab}'
            f'<g transform="translate(0 {by})">{btn}{s if step != 4 else ""}</g>{s if step == 4 else ""}'
            f'<path d="M128 {104 + by} v8 M152 {104 + by} v8" stroke="#b8326a" stroke-width="2"/><text x="140" y="146" {_T} text-anchor="middle">{e(t)}</text></svg>')

BS_STEPS = [(1, "Thread and knot", "Cut about 24 in (60 cm) of thread, double it and knot the ends. Come up from the back where the button goes."),
            (2, "Add a spacer", "Lay a pin or toothpick across the top of the button. It leaves room for the thread shank."),
            (3, "Sew through the holes", "Go up and down through the holes 4 to 6 times. On a 4-hole button, make two bars or a cross."),
            (4, "Wrap and finish", "Pull out the spacer, wind the thread round the stitches under the button 3 to 6 times, and knot on the back.")]
bs_cards = "".join(f'<figure class="gq-fig"><div>{_bs_svg(k, n + ": " + d)}<figcaption><strong>{k}. {e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in BS_STEPS)

bsp = top("How to sew on a button", "Sew a button on by hand in four steps, with our own drawings: flat buttons, shank buttons and coat buttons. Plus a button spacing calculator for cardigans, shirts and cushion covers.", "How to sew on a button") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> thread a needle with about 24 in (60 cm) of thread, double it and knot the ends. Come up from the back of the fabric where the button goes, lay a <strong>pin or toothpick across the top</strong> of the button, and sew up and down through the holes <strong>4 to 6 times</strong>, over the pin. Take the pin out, bring the needle up between the button and the fabric, <strong>wrap the thread around the stitches 3 to 6 times</strong> to make a little stem (the shank), then go to the back and knot it. The shank leaves room for the other layer of fabric, so the button closes without pulling.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Button spacing calculator</h3>
<div class="field"><span class="label" id="bs-u-l">Units</span><div class="seg" role="group" aria-labelledby="bs-u-l" id="bs-u"><button type="button" data-v="in" aria-pressed="true">Inches</button><button type="button" data-v="cm" aria-pressed="false">cm</button></div></div>
<div class="row2"><div class="field"><label for="bs-l">Length of the opening (band or placket)</label><input type="number" id="bs-l" value="22" min="1" max="200" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="bs-n">Number of buttons</label><input type="number" id="bs-n" value="6" min="2" max="40" step="1" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="bs-t">Top button, from the top edge</label><input type="number" id="bs-t" value="0.5" min="0" max="50" step="0.125" inputmode="decimal"></div>
<div class="field"><label for="bs-b">Bottom button, from the bottom edge</label><input type="number" id="bs-b" value="1" min="0" max="50" step="0.125" inputmode="decimal"></div></div>
<div class="field"><label for="bs-r">Knitted band? Rows per inch or cm (optional)</label><input type="number" id="bs-r" value="" min="0" max="40" step="0.5" inputmode="decimal" placeholder="e.g. 7 for worsted garter"></div>
<p class="sub">It spaces the buttons evenly between the top and bottom ones and gives each mark from the top. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="bs-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to sew on a button in 4 steps</h2>
<div class="gq-figs">{bs_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Thread</strong> that matches the button or the fabric. All-purpose polyester is fine; use button or upholstery thread for coats and bags.</li>
<li><strong>A hand-sewing needle</strong> thin enough to pass through the holes twice.</li>
<li><strong>A pin or toothpick</strong> as a spacer, a matchstick for thick coats.</li>
<li><strong>Chalk or a fabric pen</strong> to mark the spot, and scissors.</li></ul>
<h2>Where exactly does the button go?</h2>
<p>Close the garment as it should sit, line the edges up, and push a pin through the end of the buttonhole nearest the edge (or the middle of a vertical buttonhole) into the fabric underneath. That pin mark is the centre of your button. On a shirt the buttons usually run down the centre front line; on a cardigan, down the middle of the button band.</p>
<h2>How to sew a shank button</h2>
<p>A shank button has a loop under it instead of holes, so it already has its stem. Sew through the loop and the fabric 6 to 8 times, keeping the loop lined up with the buttonhole direction, then knot on the back. No spacer needed.</p>
<h2>How to sew on a coat button</h2>
<p>Thick fabric needs a longer shank, roughly as long as the fabric is thick, so use a matchstick or two toothpicks as the spacer and strong thread. On heavy coats, sew a small flat button on the inside directly behind it (a <strong>backing button</strong>) and go through both, so the pull of the button doesn't tear the fabric.</p>
<h2>How to space buttons evenly</h2>
<p>Place the top and bottom buttons first, then divide the distance between them by the number of gaps (buttons minus one). For a 22 in band with 6 buttons, the top one 0.5 in down and the bottom one 1 in up, the buttons are 20.5 in apart in total, so 4.1 in (about 4 1/8 in) between each one. The calculator above does it in inches or centimetres. On a fitted top, put one button level with the fullest part of the bust and space the rest from it, which stops the front gaping.</p>
<h2>Buttons on knitted and crocheted things</h2>
<p>Sew with a strand of the same yarn split down to a thinner ply, or with matching sewing thread, going through the centre of a stitch rather than between stitches so the button doesn't pull a hole. For knitted bands, the calculator turns the spacing into rows if you give your rows per inch. Picking up a button band? See <a href="{href("how-to-pick-up-stitches-knitting.html")}">how to pick up stitches</a>.</p>
<h2>Why does my button keep falling off?</h2>
<ul><li><strong>No shank:</strong> sewn flat and tight, the thread rubs through when the button is done up. Use a spacer.</li>
<li><strong>Too few passes or weak thread:</strong> 4 to 6 passes with doubled thread, or button thread for coats.</li>
<li><strong>Knot only on the front:</strong> finish with two or three small stitches and a knot on the back.</li></ul>
<p>Sewing more? See the <a href="{href("sewing-seam-allowance.html")}">seam allowance guide</a> and the <a href="{href("fabric-yardage-calculator.html")}">fabric yardage calculator</a>. More crafts are on the <a href="{href("crafts.html")}">crafts page</a>.</p>
<p class="note">Sewing on a button is a standard hand-sewing technique, taught the same way by LoveCrafts, Hobbycraft, Tilly and the Buttons and MasterClass (checked 27 Nov 2026). Our wording and drawings; the spacing maths is ours.</p>
</div></div></section>'''
bs_faq = [
    ("How do you sew a button on by hand?", "Knot a doubled thread, come up from the back, lay a pin across the button, sew through the holes 4 to 6 times, remove the pin, wrap the thread round the stitches under the button a few times and knot on the back."),
    ("How much thread do you need to sew on a button?", "About 24 in (60 cm), doubled so you sew with 12 in (30 cm). That's plenty for one button with a shank."),
    ("Why do you put a toothpick under a button?", "It leaves a little slack so you can wrap a thread shank. The shank lifts the button so the buttonhole layer fits under it without pulling."),
    ("How many times should you sew through a button?", "4 to 6 times through each pair of holes with doubled thread. Coat buttons can take a few more with strong thread."),
    ("Should I sew a 4-hole button in a cross or two lines?", "Either holds well. Two parallel bars look neater on shirts; a cross is common on casual and children's clothes."),
    ("How do you space buttons evenly?", "Place the top and bottom buttons, then divide the distance between them by the number of buttons minus one. That's the gap between each button."),
    ("How do you sew a button on a knitted cardigan?", "Use matching thread or split yarn and sew through the middle of a stitch on the band, with a short shank so the thick band fits under the button."),
]
SHOP_FOR["how-to-sew-a-button.html"] = ["small-business-pricing-inventory-spreadsheet", "machine-embroidery-business-spreadsheet", "2027-crochet-knitting-planner", "christmas-gift-tags"]
page("how-to-sew-a-button.html", "How to Sew On a Button by Hand + Spacing Calculator | Purl & Paper",
     "How to sew on a button by hand in four steps: flat, shank and coat buttons, with our own drawings and a button spacing calculator for cardigans and shirts.",
     bsp, bs_faq, "How to sew on a button", app_name="Button spacing calculator")
