# ---------------- 28 Nov 2026 run 16: HOW TO CROCHET A HAT + HOW TO KNIT A HAT + HOW TO MAKE A POM POM ----------------
# Executed from build.py after plan15.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 28 Nov run 16). Drawings our own SVG; wording our own. JS in assets/app.js (cht-*, kht-*, ppm-*).
# Hat sizes are the same table as /hat-size-chart (Craft Yarn Council head ranges, hat ~12% smaller than the head). Gauges: CYC ranges.


def _beanie(cx, cy, w, col, pom=True, rib=_TEAL):
    h = w * 0.9
    s = (f'<path d="M{cx - w / 2} {cy} C{cx - w / 2} {cy - h} {cx + w / 2} {cy - h} {cx + w / 2} {cy} Z" fill="{col}" stroke="{_INK}" stroke-width="2"/>'
         f'<rect x="{cx - w / 2 - 4}" y="{cy - 4}" width="{w + 8}" height="{w * 0.22}" rx="6" fill="{rib}" stroke="{_INK}" stroke-width="2"/>'
         + "".join(f'<line x1="{cx - w / 2 + 4 + i * 8}" y1="{cy}" x2="{cx - w / 2 + 4 + i * 8}" y2="{cy + w * 0.22 - 8}" stroke="#fbfcfa" stroke-width="2" opacity=".6"/>' for i in range(int(w / 8))))
    if pom:
        s += f'<circle cx="{cx}" cy="{cy - h * 0.8}" r="{w * 0.16}" fill="{_GOLD}" stroke="{_INK}" stroke-width="2"/>' + "".join(
            f'<line x1="{cx}" y1="{cy - h * 0.8}" x2="{cx + w * 0.14 * __import__("math").cos(a / 6)}" y2="{cy - h * 0.8 + w * 0.14 * __import__("math").sin(a / 6)}" stroke="{_INK}" stroke-width="1" opacity=".35"/>' for a in range(0, 38, 3))
    return s


# ======== HOW TO CROCHET A HAT ========
# Demand: 'how to crochet a beanie for beginners step by step' / 'how to crochet a hat' (SERP 28 Nov: Green Matters, LoveCrafts US+UK,
# Instructables x2, Make and Do Crew 1-hour hat (+ comment pages), Create Whimsy, Ravelry x2, Handy Little Me, Hooked on Homemade Happiness)
# + 'crochet hat crown increase chart how many stitches' (Payhip resize guide, Gathered crown, DROPS, Heart Hook Home master beanie,
# Purl Soho, Ravelry sizing chart, Marly Bird top-down, AllFreeCrochet 3 ways). Nobody writes the rounds for your size and yarn.
# Method: standard top-down flat circle (6 / 8 / 12 increases per round for sc / hdc / dc) until the circle is hat-circumference / pi across.

def _ch_svg(step, label):
    import math
    if step == 1:
        s = (f'<circle cx="140" cy="96" r="18" fill="none" stroke="{_BERRY}" stroke-width="4"/>' + "".join(
            f'<line x1="{140 + 20 * math.cos(a * math.pi / 6)}" y1="{96 + 20 * math.sin(a * math.pi / 6)}" x2="{140 + 46 * math.cos(a * math.pi / 6)}" y2="{96 + 46 * math.sin(a * math.pi / 6)}" stroke="{_TEAL}" stroke-width="5" stroke-linecap="round"/>' for a in range(12))
             + f'<text x="140" y="180" {_T12} text-anchor="middle">12 dc into a magic ring, join</text>')
    elif step == 2:
        s = "".join(f'<circle cx="140" cy="92" r="{r}" fill="none" stroke="{c}" stroke-width="7"/>' for r, c in ((14, _TEAL), (28, _BERRY), (42, _TEAL), (56, _BERRY), (70, _TEAL))) + f'<text x="140" y="188" {_T12} text-anchor="middle">add 12 stitches every round: it stays flat</text>'
    elif step == 3:
        s = ("".join(f'<circle cx="140" cy="88" r="{r}" fill="none" stroke="{c}" stroke-width="7"/>' for r, c in ((14, _TEAL), (28, _BERRY), (42, _TEAL), (56, _BERRY), (70, _TEAL)))
             + f'<line x1="66" y1="88" x2="214" y2="88" stroke="{_GOLD}" stroke-width="4"/><path d="M66 80 v16 M214 80 v16" stroke="{_GOLD}" stroke-width="4"/><text x="140" y="186" {_T12} text-anchor="middle">stop when it is the right width across</text>')
    elif step == 4:
        s = (f'<path d="M80 40 C80 20 200 20 200 40 L200 150 L80 150 Z" fill="#f6dbe6" stroke="{_INK}" stroke-width="2"/>' + "".join(
            f'<line x1="80" y1="{y}" x2="200" y2="{y}" stroke="{_BERRY}" stroke-width="2" opacity=".5"/>' for y in range(60, 150, 14))
             + f'<path d="M214 60 v90" stroke="{_GOLD}" stroke-width="4"/><text x="140" y="180" {_T12} text-anchor="middle">rounds with no increases: the sides grow down</text>')
    elif step == 5:
        s = (f'<path d="M80 40 C80 20 200 20 200 40 L200 120 L80 120 Z" fill="#f6dbe6" stroke="{_INK}" stroke-width="2"/><rect x="76" y="120" width="128" height="36" rx="5" fill="{_TEAL}" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<line x1="{x}" y1="124" x2="{x}" y2="152" stroke="#fbfcfa" stroke-width="3" opacity=".7"/>' for x in range(84, 200, 10)) + f'<text x="140" y="182" {_T12} text-anchor="middle">finish with a brim, then fasten off</text>')
    else:
        s = _beanie(140, 140, 130, "#f6dbe6") + f'<text x="140" y="192" {_T12} text-anchor="middle">add a pom pom if you like</text>'
    return _svg12(s, label)


CH_STEPS = [(1, "1. Start at the top", "Make a magic ring and work the first round into it (12 dc, 8 hdc or 6 sc). Join with a slip stitch."),
            (2, "2. Increase every round", "Each round adds the same number of stitches: 2 in one stitch, then 1, 2, 2 and so on. The circle stays flat."),
            (3, "3. Measure the top", "Stop increasing when the circle is as wide across as the writer says (hat width around ÷ 3.14)."),
            (4, "4. Work even", "Now work one stitch in every stitch, round after round. The sides fold down and the hat takes shape."),
            (5, "5. Add a brim", "Finish with a few rounds of single crochet, or front and back post stitches for a stretchy ribbed look."),
            (6, "6. Finish it", "Fasten off, weave in the ends and add a pom pom or a folded cuff.")]
ch_cards = "".join(f'<figure class="gq-fig"><div>{_ch_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CH_STEPS)

HAT_OPTS = ('<option value="0">Preemie (head 12 in)</option><option value="1">Newborn (head 14 in)</option><option value="2">Baby 3-12 months (head 17 in)</option>'
            '<option value="3">Toddler 1-3 years (head 18.5 in)</option><option value="4">Child 3-10 years (head 20 in)</option><option value="5">Teen (head 21 in)</option>'
            '<option value="6" selected>Adult average (head 22 in)</option><option value="7">Adult large (head 23.5 in)</option><option value="m">My own head measurement</option>')
YARN_OPTS = '<option value="3">DK / light (3)</option><option value="4" selected>Worsted / aran (4)</option><option value="5">Chunky / bulky (5)</option><option value="6">Super bulky (6)</option>'

chp = top("How to crochet a hat for beginners", "A simple beanie is one of the best first crochet projects: you start with a flat circle for the top, then work round and round without increasing until it's long enough. Every step is drawn below, and the writer gives you every round for your size and yarn, in US or UK terms.", "How to crochet a hat") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet a beanie from the top down, <strong>make a magic ring and work 12 double crochet</strong> into it, then <strong>add 12 stitches every round</strong> (2 dc in each stitch, then 1 dc and 2 dc, then 2 dc and 2 dc…) until the flat circle is about <strong>6.2 in (16 cm) across</strong> for an average adult. Then <strong>work 1 dc in each stitch</strong> until the hat is about <strong>8 in (20 cm) from the centre top</strong>, and finish with 2 rounds of sc for the brim. In worsted yarn with a 5.5 to 6 mm hook that's about 5 increase rounds (around 54 to 60 stitches, depending on your tension) and roughly 170 to 220 yd of yarn (our estimate). The writer below does the maths for any size, yarn and stitch.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Crochet hat pattern writer</h3>
<div class="row2"><div class="field"><label for="cht-z">Size</label><select id="cht-z">{HAT_OPTS}</select></div>
<div class="field"><label for="cht-m">Head around (in), if measuring</label><input type="number" id="cht-m" value="22" min="10" max="26" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="cht-y">Yarn</label><select id="cht-y">{YARN_OPTS}</select></div>
<div class="field"><label for="cht-s">Stitch</label><select id="cht-s"><option value="dc" selected>Double crochet (quickest)</option><option value="hdc">Half double crochet (cosy, less holey)</option><option value="sc">Single crochet (dense and warm)</option></select></div></div>
<div class="row2"><div class="field"><span class="label" id="cht-t-l">Terms</span><div class="seg" role="group" aria-labelledby="cht-t-l" id="cht-t"><button type="button" data-v="us" aria-pressed="true">US</button><button type="button" data-v="uk" aria-pressed="false">UK</button></div></div>
<div class="field"><span class="label" id="cht-b-l">Brim</span><div class="seg" role="group" aria-labelledby="cht-b-l" id="cht-b"><button type="button" data-v="sc" aria-pressed="true">Plain sc edge</button><button type="button" data-v="rib" aria-pressed="false">Ribbed (post stitches)</button></div></div></div>
</div><div class="result" aria-live="polite" id="cht-out" data-chart="{href("hat-size-chart.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to crochet a beanie, step by step</h2>
<div class="gq-figs">{ch_cards}</div>
<h2>What you need for your first hat</h2>
<ul><li><strong>Yarn:</strong> a smooth worsted (weight 4) in a light colour so you can see the stitches. Acrylic or a wool blend is soft, warm and easy to wash. An adult beanie takes about 170 to 220 yards; a baby hat 70 to 120 (our estimates, the writer gives yours).</li>
<li><strong>Hook:</strong> one or two sizes bigger than the label is normal for a soft, drapey hat, for example 5.5 or 6 mm (I-9 or J-10) for worsted.</li>
<li><strong>Also:</strong> a stitch marker for the first stitch of each round, a tape measure, scissors and a tapestry needle. Card or a pom pom maker if you want a pom pom.</li></ul>
<h2>How many stitches to start a crochet hat?</h2>
<p>Top-down hats start with a set number in the ring and add that many every round, because that's what keeps a circle flat: <strong>6 for single crochet, 8 (or 10) for half double, 12 for double crochet</strong>. Taller stitches need more because each round is taller and the circle grows faster. If your circle ruffles, you're adding too many (or your hook is too big); if it cups into a bowl, too few. Our <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a> writes a flat circle for any start number.</p>
<h2>How big should the crown of a hat be?</h2>
<p>Divide the hat's width around by 3.14. A finished hat is usually about 10 to 12% smaller around than the head so it stays on, so an average 22 in adult head wants a hat of about 19.5 in, and a flat top of about <strong>6.2 in (16 cm)</strong> across. Measure across the middle of the circle, not round the edge. The full table, preemie to large adult, is on our <a href="{href("hat-size-chart.html")}">hat size chart</a>.</p>
<h2>How long should a crochet beanie be?</h2>
<p>Measure from the centre of the top down to the edge. (The taller hat heights on our size chart are the Craft Yarn Council's full-coverage figures, which suit a folded brim.) A fitted adult beanie is about <strong>8 to 8.5 in (20 to 22 cm)</strong>; add 1.5 to 2 in for a folded brim and 2 to 3 in for a slouchy hat. Children's hats are 6 to 7.5 in and baby hats 5 to 6.5 in. Try it on as you go: crochet stretches a little lengthways when it's worn.</p>
<h2>Crochet hat problems and fixes</h2>
<ul><li><strong>Seam slants or wanders:</strong> that's normal in joined rounds. Keep it at the back, or turn after each round to keep it straighter.</li>
<li><strong>Too tight:</strong> go up a hook size, or add one more increase round before working even.</li>
<li><strong>Too loose or wavy brim:</strong> work the brim with a hook one size smaller, or sc2tog every 10th stitch in the first brim round.</li>
<li><strong>Lost count:</strong> count stitches at the end of every increase round; they should always be a multiple of your start number. A <a href="{href("row-counter.html")}">row counter</a> helps.</li></ul>
<h2>Ribbed brim with post stitches</h2>
<p>For a stretchy, knit-look brim, alternate <strong>front post double crochet (FPdc)</strong> and <strong>back post double crochet (BPdc)</strong>: work the stitch round the post of the stitch below, from the front or from the back. On an even number of stitches, repeat (FPdc, BPdc) all the way round, then line up the same stitches on the next rounds. Working in the round only in the back loop of single crochet also gives a soft ridged edge. Need more stitch help? See <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>, the <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a> and <a href="{href("how-to-slip-stitch-crochet.html")}">how to join a round with a slip stitch</a>.</p>
<h2>Gifting or selling hats</h2>
<p>A beanie takes 2 to 4 hours in worsted double crochet (more in single crochet), so they're ideal last-minute Christmas gifts (even quicker: a ribbed <a href="{href("crochet-headband-pattern.html")}">crochet ear warmer</a>): check timings in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Selling them? Our <a href="{href("how-to-price-crochet-items.html")}">crochet pricing guide</a> works out a fair price from yarn and hours, and every hat looks better with a <a href="{href("how-to-make-a-pom-pom.html")}">pom pom</a> on top. Prefer needles? Try <a href="{href("how-to-knit-a-hat.html")}">how to knit a hat</a>.</p>
<p class="note">Hat sizes follow the Craft Yarn Council head ranges (as on our hat size chart); start numbers and the circle method are standard crochet technique, checked against LoveCrafts, AllFreeCrochet and Marly Bird top-down hat tutorials (28 Nov 2026). Round heights and yarn amounts are our estimates: try the hat on as you go. Drawings, wording and the writer are our own.</p>
</div></div></section>'''
ch_faq = [
    ("How do you crochet a hat for beginners?", "Start with a magic ring, work 12 double crochet into it and add 12 stitches every round until the flat circle is the right width across (6 to 6.5 in for an adult). Then work 1 stitch in each stitch until the hat is about 8 in long, and finish with a brim."),
    ("How many stitches do you start a crochet hat with?", "Usually 12 for double crochet, 8 or 10 for half double crochet and 6 for single crochet, worked into a magic ring. You then add the same number every round."),
    ("How wide should the top of a crochet hat be?", "The hat's width around divided by 3.14. For an average adult that's about 6.2 in (16 cm) across; for a toddler about 5.3 in."),
    ("How long should a crochet beanie be?", "About 8 to 8.5 in from the top for a fitted adult beanie, 10 to 11 in for a slouchy one, 6 to 7.5 in for a child and 5 to 6.5 in for a baby."),
    ("How much yarn do I need to crochet a hat?", "Roughly 170 to 220 yards of worsted for an adult double crochet beanie and 70 to 120 yards for a baby hat (our estimates). Single crochet uses more than double crochet."),
    ("How long does it take to crochet a hat?", "About 2 to 4 hours for an adult beanie in worsted double crochet once you know the stitches; single crochet and thinner yarn take longer."),
    ("What size hook for a crochet hat?", "With worsted yarn, a 5 to 6 mm hook (H-8 to J-10) is typical. Go up a size for a softer, slouchier hat or down for a firmer one."),
]
SHOP_FOR["how-to-crochet-a-hat.html"] = ["2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "yarn-stash-tracker", "christmas-gift-tags"]
page("how-to-crochet-a-hat.html", "How to Crochet a Hat for Beginners (+ Beanie Pattern Writer)",
     "How to crochet a hat for beginners: a top-down beanie in six drawn steps, crown size and length by age, and a free writer for every round in US or UK terms.",
     chp, ch_faq, "How to crochet a hat", app_name="Crochet hat pattern writer")


# ======== HOW TO KNIT A HAT ========
# Demand: 'how to knit a hat for beginners circular needles' (SERP 28 Nov: Yahoo video, Instructables x2 first hat + slouchy, AllFreeKnitting x2,
# Knit Picks tutorial x2, Handy Little Me, B.Hooked baby hat x2, Mary Maxim, Skillshare, Ravelry x2, Dummies adult + child specs, Sheep & Stitch
# chunky, LoveCrafts). Writers on page 1: none. Method: standard bottom-up beanie, rib brim, 8-section crown decreases.
# Gauges: CYC knit ranges (as /how-to-knit-a-scarf); rows per inch estimated from a typical stocking stitch ratio (labelled).

def _kh_svg(step, label):
    import math
    if step == 1:
        s = (f'<path d="M60 150 C60 60 220 60 220 150" fill="none" stroke="{_INK}" stroke-width="3"/><rect x="40" y="140" width="40" height="10" rx="5" fill="{_WOOD}"/><rect x="200" y="140" width="40" height="10" rx="5" fill="{_WOOD}"/>'
             + "".join(f'<ellipse cx="{140 + 72 * math.cos(math.pi + a * math.pi / 14)}" cy="{136 + 62 * math.sin(math.pi + a * math.pi / 14)}" rx="5" ry="8" fill="none" stroke="{_TEAL}" stroke-width="3"/>' for a in range(1, 14))
             + f'<text x="140" y="182" {_T12} text-anchor="middle">cast on onto a 16 in circular needle</text>')
    elif step == 2:
        s = (f'<circle cx="140" cy="92" r="58" fill="none" stroke="{_TEAL}" stroke-width="10" stroke-dasharray="3 5"/><circle cx="140" cy="92" r="46" fill="none" stroke="{_WOOD}" stroke-width="3"/>'
             + f'<circle cx="140" cy="34" r="7" fill="{_BERRY}"/><text x="140" y="182" {_T12} text-anchor="middle">check nothing is twisted, then join</text>')
    elif step == 3:
        s = (f'<rect x="60" y="70" width="160" height="70" rx="6" fill="{_TEAL}" stroke="{_INK}" stroke-width="2"/>' + "".join(
            f'<rect x="{x}" y="74" width="8" height="62" rx="3" fill="#fbfcfa" opacity=".55"/>' for x in range(68, 214, 16)) + f'<text x="140" y="174" {_T12} text-anchor="middle">k1, p1 or k2, p2 rib for the brim</text>')
    elif step == 4:
        s = (f'<rect x="60" y="110" width="160" height="40" rx="6" fill="{_TEAL}" stroke="{_INK}" stroke-width="2"/><rect x="60" y="30" width="160" height="80" fill="#f6dbe6" stroke="{_INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{x} {y} l5 7 l5 -7" fill="none" stroke="{_BERRY}" stroke-width="2"/>' for x in range(66, 214, 12) for y in range(38, 104, 10)) + f'<text x="140" y="176" {_T12} text-anchor="middle">knit every round: stocking stitch</text>')
    elif step == 5:
        s = ("".join(f'<path d="M140 96 L{140 + 70 * math.cos(a * math.pi / 4)} {96 + 70 * math.sin(a * math.pi / 4)} A70 70 0 0 1 {140 + 70 * math.cos((a + 1) * math.pi / 4)} {96 + 70 * math.sin((a + 1) * math.pi / 4)} Z" fill="{"#f6dbe6" if a % 2 else "#fbf8f1"}" stroke="{_BERRY}" stroke-width="2"/>' for a in range(8))
             + f'<circle cx="140" cy="96" r="6" fill="{_INK}"/><text x="140" y="188" {_T12} text-anchor="middle">8 decreases a round: the crown closes</text>')
    else:
        s = _beanie(140, 140, 130, "#f6dbe6") + f'<text x="140" y="192" {_T12} text-anchor="middle">thread the tail through the last stitches</text>'
    return _svg12(s, label)


KH_STEPS = [(1, "1. Cast on", "Cast on the number from the writer onto a 16 in (40 cm) circular needle. The long-tail cast on is stretchy and neat."),
            (2, "2. Join in the round", "Lay the needle flat and make sure the cast-on edge isn't twisted. Place a marker and knit the first stitch to join."),
            (3, "3. Knit the brim", "Work k1, p1 or k2, p2 rib for about 1.5 to 2 in. Ribbing pulls in and keeps the hat snug."),
            (4, "4. Knit the body", "Knit every round. In the round that makes smooth stocking stitch. Keep going until the hat reaches the crown start."),
            (5, "5. Shape the crown", "Decrease 8 stitches a round in 8 even sections. Switch to double-pointed needles or magic loop when it gets tight."),
            (6, "6. Close the top", "Cut the yarn, thread it through the last 8 stitches, pull tight and weave in. Add a pom pom.")]
kh_cards = "".join(f'<figure class="gq-fig"><div>{_kh_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in KH_STEPS)

khp = top("How to knit a hat for beginners", "A plain beanie knit in the round is a great second project after a scarf: a ribbed brim, smooth knit rounds and a neat crown. Every step is drawn below, and the writer gives you the cast-on, the brim, the length and every crown round for your size and yarn.", "How to knit a hat") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to knit a beginner beanie, <strong>cast on 88 stitches</strong> in worsted yarn on a <strong>16 in, 5 mm (US 8) circular needle</strong> for an average adult, <strong>join in the round</strong>, work <strong>k2, p2 rib for 2 in</strong>, then <strong>knit every round</strong> until the hat is about <strong>6 in from the cast-on edge</strong>. Shape the crown with <strong>8 decreases every other round</strong> (k9, k2tog; then k8, k2tog…), switching to every round near the top, until 8 stitches are left. Thread the yarn through them and pull tight. That's roughly 150 to 190 yd of worsted (our estimate). The writer below does it for any size and yarn.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Knit hat pattern writer</h3>
<div class="row2"><div class="field"><label for="kht-z">Size</label><select id="kht-z">{HAT_OPTS}</select></div>
<div class="field"><label for="kht-m">Head around (in), if measuring</label><input type="number" id="kht-m" value="22" min="10" max="26" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="kht-y">Yarn</label><select id="kht-y">{YARN_OPTS}</select></div>
<div class="field"><label for="kht-r">Brim</label><select id="kht-r"><option value="2" selected>k2, p2 rib</option><option value="1">k1, p1 rib</option><option value="0">Rolled edge (no rib)</option></select></div></div>
<div class="row2"><div class="field"><label for="kht-g">My gauge, stitches per 4 in (optional)</label><input type="number" id="kht-g" placeholder="e.g. 18" min="6" max="40" step="0.5" inputmode="decimal"></div>
<div class="field"><span class="label" id="kht-f-l">Style</span><div class="seg" role="group" aria-labelledby="kht-f-l" id="kht-f"><button type="button" data-v="fit" aria-pressed="true">Fitted</button><button type="button" data-v="fold" aria-pressed="false">Fold-up brim</button><button type="button" data-v="slouch" aria-pressed="false">Slouchy</button></div></div></div>
</div><div class="result" aria-live="polite" id="kht-out" data-chart="{href("hat-size-chart.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to knit a beanie, step by step</h2>
<div class="gq-figs">{kh_cards}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> a smooth worsted (weight 4) wool or wool blend in a light or bright colour. An adult beanie takes about 150 to 200 yards, a child's 110 to 150 and a baby's 60 to 100 (our estimates, the writer gives yours).</li>
<li><strong>Needles:</strong> a 16 in (40 cm) circular needle in the size for your yarn (5 mm / US 8 for worsted), and a set of double-pointed needles in the same size for the crown, or a long 32 in circular for the magic loop. Baby and toddler hats are too small for a 16 in circular, so work the whole hat on double-pointed needles or magic loop.</li>
<li><strong>Also:</strong> a stitch marker, a tapestry needle, scissors and a tape measure.</li></ul>
<h2>How many stitches to cast on for a hat?</h2>
<p>Multiply the hat's width around by your stitches per inch. The hat should be about 10 to 12% smaller than the head so it hugs, so for an average 22 in head you knit a hat of about 19.5 in. At worsted gauge (18 stitches per 4 in, or 4.5 per inch) that's 88 stitches. The writer rounds to a multiple of 8, so the crown decreases come out even and the number also works for k1, p1 and k2, p2 rib. Knit a small swatch in the round first if you can: the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> and <a href="{href("gauge-converter.html")}">gauge converter</a> work from your own numbers.</p>
<h2>How long should a knitted hat be before decreasing?</h2>
<p>For a fitted adult beanie, knit until it's about <strong>6 to 6.5 in</strong> from the cast-on edge, then decrease; the crown adds the last 2 inches or so. Add 2 to 3 in before decreasing for a fold-up brim and 2 to 3 in for a slouchy hat. Children's hats start the crown at 4.5 to 5.5 in and baby hats at 3.5 to 4.5 in. The writer works it out from the size and your yarn.</p>
<h2>How to decrease the crown of a hat</h2>
<p>The neatest beginner crown splits the stitches into 8 equal sections and decreases once in each: <strong>*knit to 2 stitches before the end of the section, k2tog*</strong>, 8 times. Knit one plain round between decrease rounds until about 6 stitches are left in each section, then decrease every round. When 8 stitches are left, cut the yarn with a 6 in tail, thread it through all 8 with a tapestry needle and pull tight. More on <a href="{href("increase-decrease-calculator.html")}">spacing decreases evenly</a>.</p>
<h2>Knit hat problems and fixes</h2>
<ul><li><strong>Twisted cast-on:</strong> if the first rounds spiral round the needle, there's no fix but starting again. Check before you join. See <a href="{href("how-to-knit-in-the-round.html")}">how to knit in the round</a>.</li>
<li><strong>Ladder between double-pointed needles:</strong> pull the first two stitches on each needle snug, or shift the stitches along a few each round.</li>
<li><strong>Too big:</strong> ribbing hides a lot, but a hat more than an inch too big will slip. Measure your gauge in the knit section and use the writer with your number.</li>
<li><strong>Dropped a stitch:</strong> catch it with a crochet hook: <a href="{href("how-to-fix-a-dropped-stitch.html")}">how to fix a dropped stitch</a>.</li></ul>
<h2>Gifting or selling hats</h2>
<p>A worsted beanie takes about 4 to 6 hours to knit, a chunky one 2 to 3, so a hat is a realistic last-minute Christmas gift: check timings in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Selling them? The <a href="{href("how-to-price-crochet-items.html")}">pricing guide</a> works for knits too. Top it with a <a href="{href("how-to-make-a-pom-pom.html")}">pom pom</a>, and if you prefer a hook, here's <a href="{href("how-to-crochet-a-hat.html")}">how to crochet a hat</a>.</p>
<p>Keep the set going with <a href="{href("how-to-knit-mittens.html")}">how to knit mittens</a>: the same yarn and a pattern writer for any hand size.</p>
<p class="note">Hat sizes follow the Craft Yarn Council head ranges (as on our hat size chart); gauges are the CYC knit ranges; the 8-section crown is standard technique, checked against Knit Picks, Dummies and AllFreeKnitting hat tutorials (28 Nov 2026). Row gauge and yarn amounts are our estimates: measure as you go. Drawings, wording and the writer are our own.</p>
</div></div></section>'''
kh_faq = [
    ("How do you knit a hat for beginners?", "Cast on in the round on a 16 in circular needle, knit 1.5 to 2 in of rib, knit every round until the hat is about 6 in long, then decrease 8 stitches every other round. Thread the yarn through the last 8 stitches and pull tight."),
    ("How many stitches do I cast on for a hat?", "For an average adult in worsted yarn, about 88 stitches; in chunky about 64 and in DK about 108. Multiply the hat's width around (about 19.5 in for an adult) by your stitches per inch."),
    ("What size circular needle for a hat?", "A 16 in (40 cm) circular in the size for your yarn, usually 5 mm (US 8) for worsted. Baby hats are too small for it, so use double-pointed needles or magic loop."),
    ("How long should a knitted hat be before decreasing?", "About 6 to 6.5 in from the cast-on edge for a fitted adult beanie, 4.5 to 5.5 in for a child and 3.5 to 4.5 in for a baby. Add 2 to 3 in for a fold-up brim or a slouchy hat."),
    ("How much yarn do I need to knit a hat?", "Roughly 150 to 200 yards of worsted for an adult beanie, 110 to 150 for a child and 60 to 100 for a baby (our estimates). Add more for a folded brim or a pom pom."),
    ("Can you knit a hat with straight needles?", "Yes: knit it flat as a rectangle with the crown decreases on right-side rows, then sew the side seam with mattress stitch. Knitting in the round avoids the seam."),
    ("How do you finish the top of a knitted hat?", "When 8 stitches are left, cut the yarn with a 6 in tail, thread it through all the stitches on a tapestry needle, pull tight, push it to the inside and weave it in."),
]
SHOP_FOR["how-to-knit-a-hat.html"] = ["2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "yarn-stash-tracker", "christmas-gift-tags"]
page("how-to-knit-a-hat.html", "How to Knit a Hat for Beginners (+ Beanie Pattern Writer)",
     "How to knit a hat for beginners on circular needles: six drawn steps, how many stitches to cast on, when to decrease, and a free writer for every round.",
     khp, kh_faq, "How to knit a hat", app_name="Knit hat pattern writer")


# ======== HOW TO MAKE A POM POM ========
# Demand: 'how to make a yarn pom pom without a maker' (SERP 28 Nov: Laura Radniecki, Make and Do Crew, Little Red Window x2, 3 ways (Julia
# Nyanyo), Mary Maxim CA, Stitches n Scraps, Crafts by Amanda, Instructables, ABCrafty x2, HGTV, Treasurie 4 methods) + 'how much yarn for a
# pom pom' (thin: Little Yellow Wheelbarrow comparison, Purl Soho, One Little Project; no calculator). Methods are standard craft technique.
# Template ring, wraps and yarn are our own rough model (labelled): wraps ~ 20 x diameter(in)^2 in worsted, scaled for yarn thickness.

def _pp_svg(step, label):
    import math
    ring = lambda cx, cy, ro, ri, f="#efe3cf": f'<circle cx="{cx}" cy="{cy}" r="{ro}" fill="{f}" stroke="{_INK}" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="{ri}" fill="#e9f1ef" stroke="{_INK}" stroke-width="2"/><path d="M{cx} {cy - ri} V{cy - ro}" stroke="#e9f1ef" stroke-width="6"/>'
    if step == 1:
        s = ring(90, 92, 52, 20) + ring(196, 92, 52, 20) + f'<text x="140" y="178" {_T12} text-anchor="middle">two card rings with a slot</text>'
    elif step == 2:
        s = ring(140, 92, 62, 24, _GOLD) + "".join(f'<line x1="{140 + 22 * math.cos(a / 9)}" y1="{92 + 22 * math.sin(a / 9)}" x2="{140 + 64 * math.cos(a / 9)}" y2="{92 + 64 * math.sin(a / 9)}" stroke="#c2810f" stroke-width="1.4"/>' for a in range(0, 57)) + f'<text x="140" y="182" {_T12} text-anchor="middle">wrap until the hole is full</text>'
    elif step == 3:
        s = (ring(140, 92, 62, 24, _GOLD) + f'<path d="M200 60 l26 -26 M200 60 l30 -8" stroke="{_INK}" stroke-width="4" stroke-linecap="round"/><circle cx="231" cy="30" r="7" fill="none" stroke="{_INK}" stroke-width="3"/><circle cx="238" cy="52" r="7" fill="none" stroke="{_INK}" stroke-width="3"/>'
             + f'<text x="140" y="182" {_T12} text-anchor="middle">cut around the edge between the rings</text>')
    elif step == 4:
        s = (f'<line x1="70" y1="92" x2="210" y2="92" stroke="{_BERRY}" stroke-width="4"/>' + "".join(f'<line x1="140" y1="92" x2="{140 + 56 * math.cos(a / 7)}" y2="{92 + 56 * math.sin(a / 7)}" stroke="{_GOLD}" stroke-width="3"/>' for a in range(0, 44))
             + f'<circle cx="140" cy="92" r="6" fill="{_BERRY}"/><text x="140" y="182" {_T12} text-anchor="middle">tie tightly in the middle, double knot</text>')
    elif step == 5:
        s = (f'<circle cx="140" cy="88" r="56" fill="{_GOLD}" stroke="{_INK}" stroke-width="2"/>' + "".join(f'<line x1="140" y1="88" x2="{140 + 52 * math.cos(a / 5)}" y2="{88 + 52 * math.sin(a / 5)}" stroke="#c2810f" stroke-width="1.2"/>' for a in range(0, 32))
             + f'<line x1="140" y1="144" x2="140" y2="168" stroke="{_BERRY}" stroke-width="3"/><text x="140" y="186" {_T12} text-anchor="middle">trim round and fluffy, keep the ties</text>')
    else:
        s = (f'<rect x="118" y="30" width="44" height="80" rx="8" fill="#c9ccd3" stroke="{_INK}" stroke-width="2"/>' + "".join(f'<rect x="{x}" y="6" width="6" height="40" rx="3" fill="#c9ccd3" stroke="{_INK}" stroke-width="1.5"/>' for x in (120, 132, 144, 156))
             + f'<rect x="124" y="104" width="32" height="60" rx="6" fill="#c9ccd3" stroke="{_INK}" stroke-width="2"/><rect x="112" y="24" width="56" height="16" rx="5" fill="{_GOLD}" opacity=".9"/>'
             + f'<text x="140" y="186" {_T12} text-anchor="middle">fork method: wrap the tines, tie through the gap</text>')
    return _svg12(s, label)


PP_STEPS = [(1, "1. Cut two rings", "Cut two card circles with a hole in the middle (the helper gives sizes) and a slot from edge to hole so you can wrap easily."),
            (2, "2. Wrap", "Hold the rings together and wrap yarn round and round through the hole. Keep going until the hole is almost full."),
            (3, "3. Cut the edge", "Slide sharp scissors between the two rings at the outer edge and cut all the way round."),
            (4, "4. Tie the middle", "Slip a long piece of strong yarn between the rings, pull it really tight and double knot it. Keep the long ends for attaching."),
            (5, "5. Trim", "Pull off the card and trim the pom pom into a ball. Roll it in your hands and trim the long bits again."),
            (6, "No card? Use a fork", "For a small pom pom, wrap yarn round a fork's tines, tie through the middle gap, slide off, cut the loops and trim.")]
pp_cards = "".join(f'<figure class="gq-fig"><div>{_pp_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in PP_STEPS)

ppp = top("How to make a pom pom (no maker needed)", "A fluffy yarn pom pom takes about 10 minutes and nothing more than card, scissors and yarn. Every step is drawn below, plus the fork and finger methods, and the helper tells you what size rings to cut, how many wraps and how much yarn for the pom pom you want.", "How to make a pom pom") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to make a pom pom without a maker, <strong>cut two card rings</strong> a little bigger than the pom pom you want (for a 3 in pom pom, about 3.25 in across with a 1.25 in hole), <strong>wrap yarn round them</strong> until the hole is full, <strong>cut round the outer edge</strong> between the rings, <strong>tie a strong piece of yarn tightly round the middle</strong>, remove the card and <strong>trim it round</strong>. No card? Wrap yarn round <strong>a fork</strong> (small pom poms) or <strong>two to four fingers</strong> (2 to 3 in), tie the middle, cut the loops and trim. A 3 in pom pom takes about 10 to 15 yards of worsted (our estimate).</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Pom pom size helper</h3>
<div class="row2"><div class="field"><label for="ppm-d">Finished pom pom size</label><select id="ppm-d"><option value="1">1 in (2.5 cm): garlands, baby booties</option><option value="1.5">1.5 in (4 cm): baby hat, gift tags</option><option value="2">2 in (5 cm): child's hat, keyrings</option><option value="2.5">2.5 in (6.5 cm): teen hat, bag charm</option><option value="3" selected>3 in (7.5 cm): adult beanie</option><option value="4">4 in (10 cm): big bobble hat</option><option value="5">5 in (12.5 cm): extra-large, cushions</option></select></div>
<div class="field"><label for="ppm-y">Yarn</label><select id="ppm-y"><option value="dk">DK / light (3)</option><option value="w" selected>Worsted / aran (4)</option><option value="ch">Chunky (5)</option><option value="sb">Super bulky (6)</option></select></div></div>
<div class="field"><span class="label" id="ppm-u-l">Units</span><div class="seg" role="group" aria-labelledby="ppm-u-l" id="ppm-u"><button type="button" data-v="in" aria-pressed="true">Inches</button><button type="button" data-v="cm" aria-pressed="false">Centimetres</button></div></div>
</div><div class="result" aria-live="polite" id="ppm-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to make a pom pom with cardboard, step by step</h2>
<div class="gq-figs">{pp_cards}</div>
<h2>How to make a pom pom with your fingers</h2>
<p>Hold two fingers together for a 2 in pom pom, three or four for 2.5 to 3 in. Wrap the yarn round them 60 to 120 times (more for a fuller pom pom), not too tight. Slip a 10 in piece of yarn between your middle fingers, round the bundle, and tie it as tight as you can. Slide the loops off, double knot, cut through all the loops on both sides and trim. It's the fastest method but the least even, so trim a little more.</p>
<h2>Which yarn makes the best pom pom?</h2>
<p><strong>Wool and wool blends</strong> make the fluffiest, densest pom poms because the fibres spring apart when cut. Acrylic works well and washes easily; very smooth cotton and silky yarns look stringy, and chenille sheds. Thicker yarn fills the rings faster, so chunky is great for big bobble hats. For a multi-colour pom pom, hold two or three strands together, or wrap one colour on each half of the ring.</p>
<h2>How to attach a pom pom to a hat</h2>
<p>Thread both long ends from the middle tie onto a tapestry needle and push them through the top of the hat, either side of the centre stitch. Tie them firmly on the inside with a double knot, then weave the ends in. For a hat you'll wash often or a removable faux-fur pom pom, sew a small button or press stud to the hat and a loop to the pom pom. For babies, sew it on very securely, or leave it off.</p>
<h2>Pom pom problems and fixes</h2>
<ul><li><strong>Flat or floppy:</strong> not enough wraps. Wrap until the hole is completely full, and use a smaller hole next time.</li>
<li><strong>Falling apart:</strong> the middle tie wasn't tight enough. Use strong yarn or dental floss, pull hard and double knot.</li>
<li><strong>Uneven:</strong> roll it between your hands, then trim the longest strands in small snips, turning it as you go. Steaming it lightly (not touching) fluffs wool.</li>
<li><strong>Too small after trimming:</strong> cut the rings about 1/4 in bigger than the size you want; you always lose a little.</li></ul>
<h2>What to make with pom poms</h2>
<p>Top a <a href="{href("how-to-knit-a-hat.html")}">knitted beanie</a> or <a href="{href("how-to-crochet-a-hat.html")}">crochet hat</a>, finish a <a href="{href("how-to-knit-a-scarf.html")}">scarf</a> or a <a href="{href("christmas-stocking-calculator.html")}">Christmas stocking</a>, string a garland, decorate gift wrapping, or glue tiny ones into a <a href="{href("junk-journal-page-ideas.html")}">junk journal</a> spread. Pom pom garlands and bobble hats also sell well at winter craft fairs: see <a href="{href("christmas-crafts-to-sell.html")}">Christmas crafts to make and sell</a> for prices.</p>
<p class="note">The methods are standard craft technique, checked against Mary Maxim, Purl Soho and Treasurie pom pom tutorials (28 Nov 2026). Ring sizes, wraps and yarn amounts are our own rough guide: tight or loose wrapping changes them, so wrap until the hole is full. Drawings, wording and the helper are our own.</p>
</div></div></section>'''
pp_faq = [
    ("How do you make a pom pom without a pom pom maker?", "Cut two card rings a little bigger than the pom pom you want, wrap yarn round them until the hole is full, cut round the edge, tie the middle tightly, remove the card and trim. A fork or your fingers work for small ones."),
    ("What size cardboard circle for a pom pom?", "About 1/4 in bigger across than the finished pom pom, with a hole about 40% of that width. For a 3 in pom pom, cut rings about 3.25 in across with a 1.25 in hole."),
    ("How much yarn do you need for a pom pom?", "Roughly 10 to 15 yards of worsted for a 3 in pom pom and 20 to 30 yards for a 4 in one (our estimates). Thinner yarn needs more length, chunky yarn less."),
    ("How many times do you wrap yarn for a pom pom?", "Until the centre hole is full. That's very roughly 150 to 200 wraps of worsted for a 3 in pom pom and 80 for a 2 in one."),
    ("What size pom pom for a hat?", "About 3 to 4 in for an adult beanie, 2 to 2.5 in for a child's hat and 1.5 in for a baby hat."),
    ("How do you make a pom pom fluffy?", "Use wool or a wool blend, wrap the ring really full, tie the middle very tight, then roll it in your hands and trim. A puff of steam held above the pom pom fluffs wool even more."),
    ("How do you make a pom pom with a fork?", "Wrap yarn round the tines about 40 to 60 times, thread a piece of yarn through the middle gap of the fork and tie it tightly round the bundle, slide it off, cut the loops on both sides and trim."),
]
SHOP_FOR["how-to-make-a-pom-pom.html"] = ["christmas-gift-tags", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "yarn-stash-tracker"]
page("how-to-make-a-pom-pom.html", "How to Make a Pom Pom Without a Maker (+ Size Helper)",
     "How to make a yarn pom pom with cardboard, a fork or your fingers: five drawn steps, plus a helper for ring size, wraps and yarn for 1 to 5 in pom poms.",
     ppp, pp_faq, "How to make a pom pom", app_name="Pom pom size helper")
