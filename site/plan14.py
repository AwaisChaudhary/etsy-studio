# ---------------- 27 Nov 2026 run 14: HOW TO CROCHET A SCARF + HAND SEWING STITCHES (+ Offsite Ads and slip knot merges in build.py) ----------------
# Executed from build.py after plan13.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 27 Nov run 14). Drawings our own SVG; wording our own. JS in assets/app.js (csw-*, hss-*).


# ======== HOW TO CROCHET A SCARF ========
# Demand: M4 'how to crochet a scarf for beginners' (SERP 27 Nov: LoveCrafts US+UK, LoveCrochet 10 steps, eHow x2, Instructables,
# Nicki's Homemade Crafts x2, B.Hooked, Petals to Picots, Almanac, Annie's, Ravelry, EasyCrochet scarf guide, Jo to the World).
# Facts: CYC crochet gauge per weight (sc per 4 in) from data.json; turning chains (also on /basic-crochet-stitches). Wording ours.

def _cs_svg(step, label):
    if step == 1:
        s = (f'<circle cx="90" cy="110" r="46" fill="{_TEAL}" stroke="{_INK}" stroke-width="2"/>' + "".join(f'<path d="M{50 + i * 14} {80 + (i % 2) * 6} C{70 + i * 10} 110 {60 + i * 12} 140 {74 + i * 10} 150" fill="none" stroke="#7cc4bf" stroke-width="2"/>' for i in range(5)) +
             f'<path d="M170 40 L230 160" stroke="{_GOLD}" stroke-width="7" stroke-linecap="round"/><path d="M170 40 c-8 -2 -10 8 -3 10" fill="none" stroke="{_INK}" stroke-width="2"/>'
             f'<text x="140" y="190" {_T12} text-anchor="middle">worsted yarn + 6 mm (J-10) hook</text>')
    elif step == 2:
        s = ("".join(f'<ellipse cx="{x}" cy="100" rx="9" ry="6" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for x in range(40, 240, 16)) +
             f'<text x="140" y="60" {_T12} text-anchor="middle">chain the foundation</text><text x="140" y="150" {_T12} text-anchor="middle">stitches + turning chain</text>')
    elif step == 3:
        s = ("".join(f'<ellipse cx="{x}" cy="140" rx="9" ry="6" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for x in range(40, 240, 16)) +
             "".join(f'<path d="M{x} 132 V96 M{x - 6} 96 h12" stroke="{_TEAL}" stroke-width="3"/>' for x in range(56, 240, 16)) +
             f'<text x="140" y="60" {_T12} text-anchor="middle">row 1: a stitch in each chain</text><text x="140" y="180" {_T12} text-anchor="middle">skip the turning chain</text>')
    elif step == 4:
        s = (f'<path d="M60 150 H220" stroke="{_TEAL}" stroke-width="10"/><path d="M220 150 C250 150 250 100 220 100" fill="none" stroke="{_INK}" stroke-width="2" stroke-dasharray="5 4"/>'
             f'<path d="M226 94 l-8 6 l8 6" fill="none" stroke="{_INK}" stroke-width="2"/>' + "".join(f'<ellipse cx="60" cy="{y}" rx="5" ry="7" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for y in (136, 122, 108)) +
             f'<text x="140" y="60" {_T12} text-anchor="middle">turn, chain for the height</text><text x="140" y="185" {_T12} text-anchor="middle">then a stitch in each stitch</text>')
    elif step == 5:
        s = "".join(f'<path d="M60 {y} H220" stroke="{c}" stroke-width="12"/>' for y, c in ((60, _TEAL), (76, "#3aa49e"), (92, _TEAL), (108, "#3aa49e"), (124, _TEAL), (140, "#3aa49e"))) + f'<text x="140" y="180" {_T12} text-anchor="middle">repeat the rows to the length</text>'
    else:
        s = (f'<rect x="90" y="20" width="100" height="130" rx="4" fill="{_BERRY}" stroke="{_INK}" stroke-width="2"/>' +
             "".join(f'<path d="M{x} 150 L{x + (i % 3 - 1) * 3} 186" stroke="{_BERRY}" stroke-width="4" stroke-linecap="round"/>' for i, x in enumerate(range(96, 188, 9))) +
             "".join(f'<path d="M94 {y} H186" stroke="#93234f" stroke-width="2"/>' for y in range(32, 150, 9)) + f'<text x="236" y="100" {_T12} text-anchor="middle">fasten off</text><text x="236" y="116" {_T12} text-anchor="middle">+ fringe</text>')
    return _svg12(s, label)


CS_STEPS = [(1, "1. Choose yarn and hook", "A smooth, light-coloured worsted (medium) yarn and a 5.5 to 6.5 mm hook (I-9 to K-10½) make the stitches easy to see."),
            (2, "2. Chain the foundation", "Make a slip knot and chain the stitches for your width, plus the turning chain. The writer below gives the number."),
            (3, "3. Work row 1", "Work one stitch into each chain, starting in the 2nd, 3rd or 4th chain from the hook depending on the stitch."),
            (4, "4. Turn and repeat", "Turn the work, chain 1, 2 or 3 for the height of the stitch, and work one stitch in each stitch across."),
            (5, "5. Keep going", "Repeat that row until the scarf is long enough. Count the stitches every few rows so the edges stay straight."),
            (6, "6. Fasten off and finish", "Cut the yarn, pull it through the last loop, weave in the ends and add fringe if you like.")]
cs_cards = "".join(f'<figure class="gq-fig"><div>{_cs_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CS_STEPS)

csp = top("How to crochet a scarf for beginners", "A scarf is the friendliest first crochet project: straight rows of one stitch, no shaping, and a finished gift at the end. Every step is drawn below, and the writer turns your yarn, stitch and size into a full beginner pattern with the chain to start.", "How to crochet a scarf") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> with <strong>worsted yarn and a 6 mm (J-10) hook</strong>, <strong>chain about 22 to 25</strong> for a 7 to 8 in wide scarf. Work <strong>half double crochet</strong> (or single crochet) into each chain, then <strong>turn, chain and work a stitch into every stitch</strong> on each row until it's about <strong>60 to 70 in (150 to 180 cm)</strong> long. <strong>Fasten off</strong>, weave in the ends, and add fringe if you like. An adult scarf in worsted takes roughly 300 to 450 yards, or 2 to 3 skeins of 200 yd: crochet uses more yarn than knitting (our estimate; get the figure for your yarn in the <a href="{href("scarf-size-chart.html")}">scarf size calculator</a>).</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Beginner crochet scarf pattern writer</h3>
<div class="row2"><div class="field"><label for="csw-y">Yarn weight</label><select id="csw-y"><option value="3">3 Light (DK)</option><option value="4" selected>4 Medium (Worsted, Aran)</option><option value="5">5 Bulky (Chunky)</option><option value="6">6 Super Bulky</option></select></div>
<div class="field"><label for="csw-s">Stitch</label><select id="csw-s"><option value="sc">Single crochet: dense and warm</option><option value="hdc" selected>Half double crochet: quick and soft</option><option value="dc">Double crochet: fastest, more drape</option><option value="moss">Moss (linen) stitch: woven look</option></select></div></div>
<div class="row2"><div class="field"><label for="csw-w">Width (in)</label><input type="number" id="csw-w" value="7" min="2" max="24" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="csw-l">Length (in)</label><input type="number" id="csw-l" value="65" min="10" max="120" step="1" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="csw-g">My gauge, stitches per 4 in (optional)</label><input type="number" id="csw-g" value="" min="4" max="40" step="1" inputmode="numeric" placeholder="blank = yarn label average"></div>
<div class="field"><span class="label" id="csw-t-l">Terms</span><div class="seg" role="group" aria-labelledby="csw-t-l" id="csw-t"><button type="button" data-v="us" aria-pressed="true">US</button><button type="button" data-v="uk" aria-pressed="false">UK</button></div></div></div>
</div><div class="result" aria-live="polite" id="csw-out" data-scarf="{href("scarf-size-chart.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a scarf, step by step</h2>
<div class="gq-figs">{cs_cards}</div>
<h2>Best yarn and hook for a first crochet scarf</h2>
<p>Pick a <strong>smooth worsted (medium, weight 4) or chunky yarn</strong> in a light, solid colour, so you can see where each stitch goes. Acrylic is cheap, soft and machine washable; wool and wool blends are warmer. Leave fluffy, eyelash, velvet and very dark yarns for later: they hide the stitches. Use the hook on the label, or half a size bigger, because a scarf should drape rather than feel stiff. The Craft Yarn Council range for worsted is a 5.5 to 6.5 mm hook (I-9 to K-10½). The <a href="{href("yarn-weights.html")}">yarn weight chart</a> lists every weight, and <a href="{href("hook-needle-sizes.html")}">hook sizes</a> converts US letters to mm.</p>
<h2>How many chains to start a crochet scarf</h2>
<p>Multiply the width you want by your stitches per inch, then add the turning chain: <strong>1 for single crochet, 2 for half double, 2 for double</strong> (when the first chain 3 counts as a stitch). With worsted yarn at about 12 single crochet per 4 in, a 7 in scarf needs about 21 stitches, so chain 22. Taller stitches spread a little wider, so the writer uses slightly fewer of them (our estimate). Moss stitch needs an even number of stitches. The <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a> does the same maths for any project.</p>
<p>Want a long, skinny scarf with fewer rows? Turn the idea round: chain the <strong>length</strong> (say 65 in) and work rows until it's wide enough. It's quicker to finish but the first row takes a while, and the long chain is easy to twist, so it's a better second scarf.</p>
<h2>Which stitch for a crochet scarf?</h2>
<ul><li><strong>Single crochet</strong>: the tightest and warmest, but slow and a bit stiff. Go up a hook size.</li>
<li><strong>Half double crochet</strong>: our pick for a first scarf. Quick, soft and the same on both sides.</li>
<li><strong>Double crochet</strong>: the fastest to grow, with more holes and drape. Good in chunky yarn.</li>
<li><strong>Moss stitch</strong> (also called linen or granite stitch): single crochet and chain 1, worked into the chain spaces. It looks woven, lies flat and doesn't stretch out of shape.</li></ul>
<p>Learn the stitches themselves in <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>, with a drawing of each step and the US and UK names. Want stripes? Plan the colours with the <a href="{href("stripe-generator.html")}">stripe generator</a> and see <a href="{href("how-to-change-colors-in-crochet.html")}">how to change colours in crochet</a>.</p>
<h2>Beginner crochet scarf mistakes and fixes</h2>
<ul><li><strong>Scarf getting wider or narrower:</strong> a stitch gained or lost at the edges. Put a stitch marker in the first and last stitch of every row and count after each row for a while.</li>
<li><strong>Tight first row:</strong> make the chain with a hook one or two sizes bigger, then switch back.</li>
<li><strong>Wavy, stiff edges:</strong> your turning chain may be too tight or too loose. Chain loosely, and check whether your pattern counts the turning chain as a stitch.</li>
<li><strong>Scarf curling:</strong> crochet rows rarely curl; if yours does, the tension is tight. Go up a hook size, and <a href="{href("how-to-block-knitting-crochet.html")}">block it</a> flat when it's done.</li></ul>
<h2>How long does it take to crochet a scarf?</h2>
<p>An adult scarf in worsted half double crochet usually takes a beginner somewhere around 8 to 15 hours, and chunky yarn on a big hook can be done in a weekend. Crochet is usually quicker than knitting the same scarf. Check whether it'll be ready for Christmas with the <a href="{href("crochet-time-estimator.html")}">crochet time calculator</a>, and keep your place with the <a href="{href("row-counter.html")}">row counter</a>. Prefer needles? See <a href="{href("how-to-knit-a-scarf.html")}">how to knit a scarf</a>. Next: a <a href="{href("how-to-crochet-a-hat.html")}">matching crochet hat</a>.</p>
<p>Finishing: <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a> shows how to hide the tails so they don't pop out in the wash. Making scarves to sell? Price them with the <a href="{href("how-to-price-crochet-items.html")}">crochet pricing calculator</a>.</p>
</div></div></section>'''
cs_faq = [
    ("How many chains do I need for a crochet scarf?", "With worsted yarn and a 6 mm (J-10) hook, about 22 to 25 chains gives a 7 to 8 in wide scarf. Multiply the width by your stitches per inch and add the turning chain (1 for single crochet, 2 for half double or double)."),
    ("What is the easiest crochet stitch for a scarf?", "Half double crochet is quick, soft and simple; single crochet is easier to learn but slower and stiffer. Both look the same on both sides."),
    ("How long should a crochet scarf be?", "About 60 to 70 in (150 to 180 cm) for an adult, or roughly the wearer's height. Children need about 50 to 60 in. See the scarf size chart for every age."),
    ("How many skeins of yarn do I need to crochet a scarf?", "Roughly 300 to 450 yards of worsted for an adult scarf, so 2 to 3 skeins of about 200 yd (our estimate). Crochet uses more yarn than knitting. Buy from one dye lot."),
    ("What size crochet hook for a scarf?", "Use the hook on the yarn label, or half a size bigger for drape. For worsted that's about 5.5 to 6.5 mm (I-9 to K-10½); for chunky, 6.5 to 9 mm."),
    ("Is it faster to crochet or knit a scarf?", "Crochet is usually faster, especially with half double or double crochet, but it uses more yarn for the same size."),
]
SHOP_FOR["how-to-crochet-a-scarf.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-planner-budget", "crochet-knitting-pricing-calculator"]
page("how-to-crochet-a-scarf.html", "How to Crochet a Scarf for Beginners (+ Pattern Writer)",
     "How to crochet a scarf for beginners in six drawn steps: yarn and hook, how many chains to start, which stitch, and a free pattern writer in US or UK terms.",
     csp, cs_faq, "How to crochet a scarf", app_name="Beginner crochet scarf pattern writer")


# ======== HAND SEWING STITCHES ========
# Demand: 'hand sewing stitches for beginners', 'basic hand stitches' (SERP 27 Nov: Bob Vila, Wayfair, Red Ted Art, Skillshare, Homedit
# seven stitches, MasterClass, LoveCrafts 6 essential, Melly Sews, I Heart Naptime, Apartment Therapy, iFixit wiki, Westport Library,
# several SlideShare decks). We only had /how-to-sew-a-button and /sewing-seam-allowance. Stitch uses are standard sewing knowledge,
# checked across 2+ of those guides; stitch lengths are typical ranges (labelled). Wording ours.

def _hs_svg(kind, label):
    cloth = f'<rect x="20" y="70" width="240" height="70" rx="4" fill="#efe6d2" stroke="{_INK}" stroke-width="1.4"/>'
    if kind == "running":
        s = cloth + "".join(f'<path d="M{x} 105 h14" stroke="{_BERRY}" stroke-width="3.4" stroke-linecap="round"/>' for x in range(36, 236, 26)) + f'<path d="M230 105 C250 95 256 70 262 50" fill="none" stroke="{_BERRY}" stroke-width="2"/><text x="140" y="170" {_T12} text-anchor="middle">even stitches and gaps, in and out</text>'
    elif kind == "baste":
        s = cloth + "".join(f'<path d="M{x} 105 h26" stroke="{_GOLD}" stroke-width="3.4" stroke-linecap="round"/>' for x in range(34, 236, 44)) + f'<text x="140" y="170" {_T12} text-anchor="middle">long, loose: pulled out later</text>'
    elif kind == "back":
        s = cloth + f'<path d="M36 105 H200" stroke="{_BERRY}" stroke-width="3.4"/>' + "".join(f'<path d="M{x} 99 v12" stroke="#efe6d2" stroke-width="2"/>' for x in range(54, 200, 18)) + f'<path d="M218 105 C210 85 196 85 200 105" fill="none" stroke="{_BERRY}" stroke-width="2" stroke-dasharray="4 3"/><text x="140" y="170" {_T12} text-anchor="middle">each stitch goes back to meet the last</text>'
    elif kind == "whip":
        s = (f'<rect x="20" y="80" width="240" height="26" fill="#efe6d2" stroke="{_INK}" stroke-width="1.4"/><rect x="20" y="106" width="240" height="26" fill="#e3d6bb" stroke="{_INK}" stroke-width="1.4"/>' +
             "".join(f'<path d="M{x} 88 L{x + 14} 124" stroke="{_TEAL}" stroke-width="3.2" stroke-linecap="round"/>' for x in range(34, 236, 18)) + f'<text x="140" y="170" {_T12} text-anchor="middle">over and over the edge</text>')
    elif kind == "ladder":
        s = (f'<path d="M20 80 H260 M20 130 H260" stroke="{_INK}" stroke-width="1.4"/><rect x="20" y="40" width="240" height="40" fill="#efe6d2"/><rect x="20" y="130" width="240" height="40" fill="#efe6d2"/>' +
             "".join(f'<path d="M{x} 86 h16 M{x + 16} 86 L{x + 16} 124 M{x + 16} 124 h16 M{x + 32} 124 L{x + 32} 86" fill="none" stroke="{_BERRY}" stroke-width="2.6"/>' for x in range(30, 220, 32)) +
             f'<text x="140" y="192" {_T12} text-anchor="middle">rungs across the gap, then pull closed</text>')
    elif kind == "slip":
        s = (f'<rect x="20" y="60" width="240" height="80" fill="#efe6d2" stroke="{_INK}" stroke-width="1.4"/><path d="M20 112 H260" stroke="{_INK}" stroke-width="1.4" stroke-dasharray="6 4"/>' +
             "".join(f'<path d="M{x} 112 L{x + 14} 104" stroke="{_TEAL}" stroke-width="2.4"/><circle cx="{x + 14}" cy="103" r="1.6" fill="{_TEAL}"/>' for x in range(30, 240, 24)) + f'<text x="140" y="170" {_T12} text-anchor="middle">tiny catches: barely shows on the front</text>')
    elif kind == "blanket":
        s = (f'<rect x="20" y="60" width="240" height="60" fill="#efe6d2" stroke="{_INK}" stroke-width="1.4"/>' +
             f'<path d="M30 120 H246" stroke="{_BERRY}" stroke-width="3"/>' + "".join(f'<path d="M{x} 120 V92" stroke="{_BERRY}" stroke-width="3"/>' for x in range(42, 250, 20)) + f'<text x="140" y="170" {_T12} text-anchor="middle">loops that sit along the edge</text>')
    else:  # catch
        s = cloth + "".join(f'<path d="M{x} 86 L{x + 16} 124 L{x + 32} 86" fill="none" stroke="{_TEAL}" stroke-width="2.8"/>' for x in range(30, 220, 32)) + f'<path d="M20 106 H260" stroke="{_INK}" stroke-width="1" stroke-dasharray="4 4"/><text x="140" y="170" {_T12} text-anchor="middle">criss-cross zig-zag over a hem</text>'
    return _svg12(s, label)


HS = [("running", "Running stitch", "Gathering, quick seams that won't take strain, sewing by hand like a machine.", "Push the needle in and out along the line, keeping stitches and gaps the same size. Load several stitches on the needle before pulling through."),
      ("baste", "Basting (tacking) stitch", "Holding layers in place before the real stitching; you pull it out afterwards.", "A long running stitch, about 1/4 to 1/2 in (6 to 12 mm). Use a contrasting thread and don't knot the end tightly, so it's easy to remove."),
      ("back", "Backstitch", "The strongest hand seam: mending split seams, crotches, bags and toys.", "Bring the needle up one stitch length ahead, go back down at the end of the last stitch, come up one stitch ahead again. The front looks like a solid machine line."),
      ("whip", "Whip stitch (overcast)", "Joining two edges: felt, appliqué, patches, closing pillow seams, stopping fraying.", "Take the needle through both layers from the same side every time, so the thread wraps over the edge in neat slanted stitches."),
      ("ladder", "Ladder stitch (invisible stitch)", "Closing a turning gap in a cushion, stuffed toy or lining so no stitches show.", "Take a small stitch along the fold on one side, cross straight over, take a stitch along the other fold, and repeat. Every few rungs, pull the thread and the gap closes."),
      ("slip", "Slip stitch (blind hem)", "Hems on trousers, skirts and curtains where the stitches shouldn't show on the front.", "Run the needle inside the folded hem for about 1/4 in, come out and pick up just one or two threads of the main fabric, then go back into the fold."),
      ("blanket", "Blanket stitch", "Decorative edges on blankets and felt, and appliqué; also stops raw edges fraying.", "Push the needle in from the front a little way in from the edge, keep the thread under the needle point and pull up, so a loop sits along the edge."),
      ("catch", "Catch stitch (herringbone)", "Hems on stretchy or heavy fabric, holding facings and interfacing flat.", "Work from left to right (if right-handed), taking a tiny stitch in the hem, then a tiny stitch in the main fabric above it, so the thread criss-crosses.")]
hs_cards = "".join(f'<figure class="gq-fig" id="hs-{k}"><div>{_hs_svg(k, n)}<figcaption><strong>{e(n)}.</strong> <em>Use it for:</em> {e(u)} <em>How:</em> {e(h)}</figcaption></div></figure>' for k, n, u, h in HS)

hsp = top("Basic hand sewing stitches for beginners", "Eight stitches cover almost every hand-sewing job: mending a seam, hemming trousers, closing a stuffed toy, sewing felt. Each one is drawn below. Not sure which you need? Pick the job and the chooser gives you the stitch, the needle, the thread and how long to make each stitch.", "Hand sewing stitches") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the basic hand stitches are <strong>running stitch</strong> (fast, light seams and gathering), <strong>backstitch</strong> (the strongest, for seams and mending), <strong>whip stitch</strong> (joining edges and felt), <strong>ladder stitch</strong> (invisible closing of a gap), <strong>slip stitch</strong> (invisible hems), <strong>basting</strong> (temporary), <strong>blanket stitch</strong> (decorative edges) and <strong>catch stitch</strong> (stretchy hems). For most jobs use an 18 in (45 cm) length of polyester all-purpose thread, a sharp needle and stitches about 1/8 in (3 mm) long.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Which hand stitch do I need?</h3>
<div class="field"><label for="hss-job">What are you sewing?</label><select id="hss-job">
<option value="seam">Mending a split seam</option><option value="hem">Hemming trousers, a skirt or curtains</option><option value="stretch">Hemming stretchy or knit fabric</option><option value="gap">Closing the gap in a cushion or stuffed toy</option><option value="felt">Sewing felt or a patch on</option><option value="edge">Finishing a blanket or fabric edge nicely</option><option value="hole">Mending a small hole or tear</option><option value="gather">Gathering a ruffle or easing a sleeve</option><option value="hold">Holding layers before sewing properly</option></select></div>
<div class="field"><label for="hss-fab">Fabric</label><select id="hss-fab"><option value="light">Light: cotton shirting, voile, silk</option><option value="medium" selected>Medium: quilting cotton, linen, polycotton</option><option value="heavy">Heavy: denim, canvas, upholstery, wool coat</option><option value="knit">Stretchy knit: jersey, fleece, T-shirt</option><option value="felt">Felt</option></select></div>
</div><div class="result" aria-live="polite" id="hss-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>The 8 basic hand sewing stitches</h2>
<div class="gq-figs">{hs_cards}</div>
<h2>Before you start: thread, needle and knot</h2>
<ol><li><strong>Cut about 18 in (45 cm) of thread</strong>, roughly from your fingertips to your elbow. Longer thread tangles and frays as it's pulled through again and again.</li>
<li><strong>Thread the needle</strong>: cut the end at an angle with sharp scissors and push it through the eye. A needle threader helps with fine needles.</li>
<li><strong>Single or double thread?</strong> Single for hems and anything that should be invisible; double (both ends knotted together) for buttons and strong repairs.</li>
<li><strong>Knot the end</strong>: wrap the thread twice round your fingertip, roll it off with your thumb and pull the twist down into a knot. Or start with two small stitches on the spot on the wrong side, which is flatter.</li></ol>
<h2>How to finish hand sewing (tie off)</h2>
<p>On the wrong side, take a tiny stitch through just a few threads of fabric, but don't pull it tight: pass the needle through the loop it leaves, then pull. Do this twice, then run the needle under the fabric for about 1 in (2.5 cm), come out and snip the thread close. The buried tail stops the knot working loose.</p>
<h2>Which needle and thread for hand sewing?</h2>
<div class="tbl-wrap"><table><thead><tr><th>Fabric</th><th>Needle</th><th>Thread</th><th>Typical stitch length</th></tr></thead><tbody>
<tr><td>Light (shirting, voile, silk)</td><td>Sharps size 9 to 10, or a fine between</td><td>Fine polyester or silk</td><td>1/16 to 1/8 in (2 to 3 mm)</td></tr>
<tr><td>Medium (cotton, linen)</td><td>Sharps size 7 to 9</td><td>All-purpose polyester or cotton</td><td>About 1/8 in (3 mm)</td></tr>
<tr><td>Heavy (denim, canvas, coat wool)</td><td>Sharps 5 to 6, or a heavy-duty needle</td><td>Heavy-duty or upholstery thread</td><td>1/8 to 1/4 in (3 to 6 mm)</td></tr>
<tr><td>Knit (jersey, fleece)</td><td>Ballpoint hand needle</td><td>All-purpose polyester (it has a little stretch)</td><td>About 1/8 in; catch stitch for give</td></tr>
<tr><td>Felt</td><td>Sharps or embroidery needle</td><td>Embroidery floss (2 to 3 strands) or all-purpose</td><td>1/8 in, even and close to the edge</td></tr>
</tbody></table></div>
<p>Higher needle numbers are finer. Stitch lengths are typical ranges, not rules: shorter stitches are stronger and neater. Match the thread colour to the fabric for invisible stitches; when in doubt, go one shade darker.</p>
<h2>Hand sewing tips for beginners</h2>
<ul><li><strong>Thread tangling?</strong> Run it over a beeswax block or press it with an iron, and let the needle dangle now and then so the twist drops out.</li>
<li><strong>Uneven stitches:</strong> draw the line with chalk or a washable pen, and use the fabric's weave as a guide.</li>
<li><strong>Puckered seam:</strong> you're pulling too tight. Snug the thread so it lies flat, not so it gathers.</li>
<li><strong>Sore finger:</strong> a thimble on your middle finger pushes the needle through thick layers.</li></ul>
<p>More sewing: <a href="{href("how-to-sew-a-button.html")}">how to sew on a button</a> (with a spacing calculator), the <a href="{href("sewing-seam-allowance.html")}">seam allowance guide</a>, the <a href="{href("fabric-yardage-calculator.html")}">fabric yardage calculator</a> and <a href="{href("embroidery-stitches.html")}">12 embroidery stitches for beginners</a>, which share several of these stitches. Making soft toys? Ladder stitch is how you close <a href="{href("amigurumi.html")}">amigurumi</a> pieces too.</p>
</div></div></section>'''
hs_faq = [
    ("What are the basic hand sewing stitches?", "Running stitch, basting, backstitch, whip stitch, ladder stitch, slip stitch (blind hem), blanket stitch and catch stitch. Running stitch and backstitch cover most seams."),
    ("What is the strongest hand sewing stitch?", "Backstitch. Each stitch overlaps the last, so it holds like a machine seam. Use it for mending seams and anything that takes strain."),
    ("What stitch do you use to close a stuffed toy or cushion?", "Ladder stitch, also called invisible or blind stitch. Take small stitches along each folded edge in turn, then pull the thread and the gap closes with no stitches showing."),
    ("How do you hem trousers by hand?", "Fold and press the hem, then use slip stitch (blind hem stitch): pick up one or two threads of the trouser fabric, then slide the needle along inside the fold, so almost nothing shows on the front."),
    ("How long should the thread be for hand sewing?", "About 18 in (45 cm), roughly fingertip to elbow. Longer thread tangles and wears thin."),
    ("Should I double the thread for hand sewing?", "For buttons and strong repairs, yes. For hems and invisible stitches, use a single thread so the stitches stay fine."),
]
SHOP_FOR["hand-sewing-stitches.html"] = ["small-business-pricing-inventory-spreadsheet", "machine-embroidery-business-spreadsheet", "2027-crochet-knitting-planner", "christmas-gift-tags"]
page("hand-sewing-stitches.html", "Basic Hand Sewing Stitches for Beginners (+ Stitch Chooser)",
     "8 basic hand sewing stitches drawn step by step: running, backstitch, whip, ladder, slip, basting, blanket and catch stitch, with a chooser for your job.",
     hsp, hs_faq, "Hand sewing stitches", app_name="Hand sewing stitch chooser")
