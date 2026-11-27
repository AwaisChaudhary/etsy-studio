# ---------------- 27 Nov 2026 run 15: HOW TO KNIT CABLES + FREE CROCHET SHEEP PATTERN (+ Christmas junk journal and hoop-finishing merges) ----------------
# Executed from build.py after plan14.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12, colours from plan13).
# Demand evidence in DEMAND.md (RADAR 27 Nov run 15). Drawings our own SVG; wording and the sheep pattern our own. JS in assets/app.js (ckw-*, shp-*).


# ======== HOW TO KNIT CABLES ========
# Demand: 'how to knit cables for beginners', 'how to read a cable chart' (SERP 27 Nov: LoveCrafts x3 regional, Knit Picks tutorial x2,
# B.Hooked, Yarnspirations, Mary Maxim x2, AllFreeKnitting videos x2, Knitting with Chopsticks, WonderHowTo, Dummies; chart SERP: DMC,
# Dummies cable charts, Yarnspirations, LoveCrafts, Gathered cable chart tutorial, Purl Soho, Lion Brand). No cable chart/pattern writer on page 1.
# Facts (standard technique, checked across LoveCrafts, Knit Picks, Dummies): front = crosses to the left, back = crosses to the right; cables
# sit on reverse stocking stitch; charts read RS rows right to left. Extra-yarn and pull-in figures labelled as rough estimates.

def _ck_svg(step, label):
    col = lambda x, c: "".join(f'<path d="M{x} {y} l6 8 l6 -8" fill="none" stroke="{c}" stroke-width="3"/>' for y in range(40, 160, 12))
    bumps = lambda x: "".join(f'<path d="M{x} {y + 4} q6 -6 12 0" fill="none" stroke="{_INK}" stroke-width="3"/>' for y in range(40, 160, 12))
    if step == 1:
        s = (bumps(60) + col(96, _TEAL) + col(112, _TEAL) + col(128, _TEAL) + col(144, _TEAL) + bumps(180) +
             f'<text x="72" y="185" {_T12} text-anchor="middle">purl</text><text x="138" y="185" {_T12} text-anchor="middle">4 knit</text><text x="192" y="185" {_T12} text-anchor="middle">purl</text>')
    elif step == 2:
        s = (f'<rect x="20" y="96" width="240" height="8" rx="4" fill="{_WOOD}"/><rect x="40" y="60" width="90" height="10" rx="5" fill="{_GOLD}" stroke="{_INK}" stroke-width="1.2"/>' +
             "".join(f'<ellipse cx="{x}" cy="100" rx="7" ry="11" fill="none" stroke="{_TEAL}" stroke-width="3"/>' for x in (150, 168)) +
             "".join(f'<ellipse cx="{x}" cy="65" rx="7" ry="11" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for x in (70, 88)) +
             f'<text x="140" y="160" {_T12} text-anchor="middle">slip 2 stitches onto the cable needle</text>')
    elif step == 3:
        s = (f'<rect x="20" y="110" width="240" height="8" rx="4" fill="{_WOOD}"/><path d="M60 60 C100 40 150 40 190 60" fill="none" stroke="{_GOLD}" stroke-width="9" stroke-linecap="round"/>' +
             "".join(f'<ellipse cx="{x}" cy="114" rx="7" ry="11" fill="none" stroke="{_TEAL}" stroke-width="3"/>' for x in (150, 168)) +
             f'<text x="140" y="30" {_T12} text-anchor="middle">held in front: crosses left</text><text x="140" y="165" {_T12} text-anchor="middle">held at the back: crosses right</text>')
    elif step == 4:
        s = (f'<rect x="20" y="110" width="240" height="8" rx="4" fill="{_WOOD}"/><path d="M60 70 C100 54 150 54 190 70" fill="none" stroke="{_GOLD}" stroke-width="9" stroke-linecap="round"/>' +
             "".join(f'<ellipse cx="{x}" cy="114" rx="7" ry="11" fill="{_TEAL}" opacity=".35" stroke="{_TEAL}" stroke-width="3"/>' for x in (80, 98)) +
             f'<path d="M220 150 L150 104" stroke="{_INK}" stroke-width="5" stroke-linecap="round"/><text x="140" y="175" {_T12} text-anchor="middle">knit the next 2 from the left needle</text>')
    elif step == 5:
        s = (f'<rect x="20" y="110" width="240" height="8" rx="4" fill="{_WOOD}"/><path d="M120 70 C140 60 170 60 190 74" fill="none" stroke="{_GOLD}" stroke-width="9" stroke-linecap="round"/>' +
             "".join(f'<ellipse cx="{x}" cy="114" rx="7" ry="11" fill="{_BERRY}" opacity=".35" stroke="{_BERRY}" stroke-width="3"/>' for x in (116, 134)) +
             f'<text x="140" y="165" {_T12} text-anchor="middle">then knit the 2 from the cable needle</text>')
    else:
        rope = "".join(f'<path d="M{118} {y} C{118} {y + 14} {162} {y + 10} {162} {y + 24} M{162} {y} C{162} {y + 6} {150} {y + 10} {144} {y + 12} M{136} {y + 14} C{126} {y + 18} {118} {y + 20} {118} {y + 24}" fill="none" stroke="{_TEAL}" stroke-width="9" stroke-linecap="round"/>' for y in range(28, 160, 30))
        s = bumps(70) + bumps(190) + rope + f'<text x="140" y="190" {_T12} text-anchor="middle">cross every few rows: a rope cable</text>'
    return _svg12(s, label)


CK_STEPS = [(1, "1. Set up the columns", "Cables sit on a column of knit stitches with a few purl stitches either side, so they stand out."),
            (2, "2. Slip to the cable needle", "On the crossing row, slip half the cable stitches (2 for a 4-stitch cable) purlwise onto a cable needle."),
            (3, "3. Front or back", "Hold the cable needle in front of the work for a left-leaning cross, or behind it for a right-leaning cross."),
            (4, "4. Knit from the left needle", "Leave the cable needle hanging and knit the next stitches (2 for C4) from the left needle. Pull the first one snug."),
            (5, "5. Knit from the cable needle", "Now knit the stitches waiting on the cable needle. That's one cross done."),
            (6, "6. Repeat the cross", "Work plain rows between crosses (3 for a C4 crossed every 4th row). The crosses stack into a twisted rope.")]
ck_cards = "".join(f'<figure class="gq-fig"><div>{_ck_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in CK_STEPS)

ckp = top("How to knit cables for beginners", "Cables look hard but they're only knit stitches worked out of order: you park a few on a cable needle, knit the next few, then knit the parked ones. Every step is drawn below, and the writer turns the cable you want into row-by-row instructions, a cast-on number and a chart you can print.", "How to knit cables") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to knit a basic 4-stitch cable (<strong>C4F</strong>), work to the cable, <strong>slip 2 stitches onto a cable needle</strong> and <strong>hold it in front</strong>, <strong>knit the next 2</strong> from the left needle, then <strong>knit the 2 from the cable needle</strong>. Holding the cable needle at the <strong>back</strong> instead (<strong>C4B</strong>) makes it lean the other way. Work the cable on a column of knit stitches with 2 or 3 purl stitches either side, and cross it every 4th row (on the right side) for a classic rope. No cable needle? A double-pointed needle or a spare stitch marker-sized stick works too.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Cable pattern and chart writer</h3>
<div class="row2"><div class="field"><label for="ckw-w">Cable width</label><select id="ckw-w"><option value="4" selected>4 stitches (C4: 2 over 2)</option><option value="6">6 stitches (C6: 3 over 3)</option><option value="8">8 stitches (C8: 4 over 4)</option></select></div>
<div class="field"><label for="ckw-d">Cross</label><select id="ckw-d"><option value="F" selected>Front: leans left (C4F, C6F, C8F)</option><option value="B">Back: leans right (C4B, C6B, C8B)</option><option value="A">Alternate front and back (wavy)</option></select></div></div>
<div class="row2"><div class="field"><label for="ckw-r">Cross every … rows</label><select id="ckw-r"><option value="4">4</option><option value="6">6</option><option value="8">8</option><option value="10">10</option></select></div>
<div class="field"><label for="ckw-p">Purl stitches between cables</label><input type="number" id="ckw-p" value="2" min="1" max="6" step="1" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="ckw-n">Number of cables</label><input type="number" id="ckw-n" value="3" min="1" max="8" step="1" inputmode="numeric"></div>
<div class="field"><span class="label" id="ckw-f-l">Knitting</span><div class="seg" role="group" aria-labelledby="ckw-f-l" id="ckw-f"><button type="button" data-v="flat" aria-pressed="true">Flat, in rows</button><button type="button" data-v="round" aria-pressed="false">In the round</button></div></div></div>
</div><div class="result" aria-live="polite" id="ckw-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to knit a cable, step by step</h2>
<div class="gq-figs">{ck_cards}</div>
<h2>C4F vs C4B: which way does it cross?</h2>
<p>The letter at the end tells you where the cable needle goes. <strong>F (front)</strong> pulls the stitches across to the <strong>left</strong>; <strong>B (back)</strong> pulls them to the <strong>right</strong>. The number is the total stitches in the cross, so C4 moves 2 over 2 and C6 moves 3 over 3. Some patterns write the same thing as <strong>2/2 LC</strong> (left cross) and <strong>2/2 RC</strong> (right cross). Put a left cable on one side of a sweater front and a right cable on the other and they mirror each other. Look up any other abbreviation in our <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a>.</p>
<h2>How to read a cable chart</h2>
<p>A chart is a picture of the right side of the knitting. Each square is a stitch and each line of squares is a row. Read <strong>right-side rows from right to left</strong> and <strong>wrong-side rows from left to right</strong>, starting at the bottom. A blank square is usually knit on the right side, a dot is purl, and the cable symbol stretches across all the stitches in the cross: a line slanting up to the left is a front cross, up to the right a back cross. On the wrong side you knit the purls and purl the knits, unless the key says otherwise. In the round every round is read right to left. The writer above draws the chart for your cable in the same style.</p>
<h2>Best yarn and needles for a first cable project</h2>
<p>Choose a <strong>smooth, light-coloured worsted or DK wool</strong> (or a wool blend): the crosses show clearly and wool's bounce hides small tension wobbles. Avoid dark, fluffy and very slippery yarns for now. Use the needle size on the label. A cable needle is a short double-pointed needle, often bent or with a dip in the middle so stitches don't slide off; pick one a little thinner than your main needles. A cowl, headband or hat brim with one or two cables is a great first project. See the <a href="{href("yarn-weights.html")}">yarn weight chart</a> and <a href="{href("hook-needle-sizes.html")}">needle sizes</a>.</p>
<h2>How to cable without a cable needle</h2>
<p>Once you're comfortable, you can skip the cable needle on small cables. For C4F: slip all 4 stitches to the right needle, pinch the base of the first 2 to hold them, slide the left needle out of all 4, catch the 2 loose stitches with the left needle from the back, put the pinched 2 back on the left needle in their new order, and knit all 4. Work in wool, which grips; slippery yarns can drop. If a stitch does run, here's <a href="{href("how-to-fix-a-dropped-stitch.html")}">how to fix a dropped stitch</a>.</p>
<h2>Cable knitting problems and fixes</h2>
<ul><li><strong>Crossed the wrong way:</strong> drop just the 4 cable stitches down to the bad cross, re-cross them and knit them back up with a crochet hook, row by row.</li>
<li><strong>Loose stitch or hole at the edge of the cable:</strong> pull the first stitch after the cross firmly, and knit the purl stitch next to the cable a little tighter.</li>
<li><strong>Lost count of rows:</strong> keep a <a href="{href("row-counter.html")}">row counter</a> going, or count the plain rows above the last cross: the row with the cable needle has a small hole behind it.</li>
<li><strong>The piece is narrower than the pattern:</strong> cables pull the fabric in. Swatch in the cable pattern, not plain stocking stitch, and use the <a href="{href("gauge-converter.html")}">gauge converter</a>.</li></ul>
<h2>Do cables use more yarn?</h2>
<p>Yes. Each cross folds stitches over each other, so cabled fabric is thicker, narrower and heavier. As a rough rule (our estimate), an all-over cable pattern uses something like 15 to 25% more yarn than plain stocking stitch at the same size, and a single cable panel only a few percent more. Buy an extra skein from the same dye lot and use the <a href="{href("yarn-calculator.html")}">yarn calculator</a> as a starting point. New to knitting? Start with <a href="{href("how-to-knit-and-purl.html")}">knit and purl</a> and a <a href="{href("knit-stitch-patterns.html")}">texture stitch pattern</a> first.</p>
<p class="note">Cable technique and chart conventions are standard and were checked against LoveCrafts, Knit Picks and Dummies cable guides (27 Nov 2026). Drawings, wording and the writer are our own.</p>
</div></div></section>'''
ck_faq = [
    ("How do you knit a cable for beginners?", "Slip 2 stitches onto a cable needle, hold it in front (or behind), knit the next 2 stitches from the left needle, then knit the 2 from the cable needle. That's a 4-stitch cable, C4F (or C4B)."),
    ("What is the difference between C4F and C4B?", "Where the cable needle is held. C4F holds it in front so the cable leans left; C4B holds it at the back so it leans right."),
    ("How often do you cross a cable?", "A common rope cable crosses every 4th row for C4 and every 6th or 8th row for C6 and C8. More rows between crosses give a looser, longer twist."),
    ("Can you knit cables without a cable needle?", "Yes. A double-pointed needle works the same way, and small cables can be crossed by slipping the stitches and rearranging them by hand, which is easiest in grippy wool."),
    ("How do you read a cable knitting chart?", "Start at the bottom right. Read right-side rows right to left and wrong-side rows left to right. Each square is a stitch, and the cable symbol spans all the stitches in the cross."),
    ("Do cables make knitting narrower?", "Yes. Cables pull the fabric in, so swatch in the cable pattern to check your gauge before you cast on."),
    ("What yarn is best for cable knitting?", "A smooth, light-coloured wool or wool-blend in worsted or DK. The stitch definition shows the cables, and wool hides small tension differences."),
]
SHOP_FOR["how-to-knit-cables.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("how-to-knit-cables.html", "How to Knit Cables for Beginners (+ Cable Chart Writer)",
     "How to knit cables for beginners: C4F and C4B drawn step by step, how to read a cable chart, and a free writer for your cable rows, cast-on and chart.",
     ckp, ck_faq, "How to knit cables", app_name="Cable pattern and chart writer")


# ======== FREE CROCHET SHEEP PATTERN ========
# Demand: E1 Google Trends crochet 1-day rising 'crochet sheep' +80% (with a retailer's sheep plush toy trend +130%); SERP 27 Nov 'how to crochet
# a sheep amigurumi easy pattern': almost all Ravelry/Ribblr paid listings + Hobbycraft guide; few free beginner patterns with stitch counts.
# The pattern is our own, built from the standard amigurumi sphere maths (6-stitch increases per round, as on /crochet-circle-calculator).
# Size and yarn figures are estimates (labelled). Safety-eye age advice: standard toy-safety practice (embroider eyes for under-3s).

def _sheep_svg():
    wool = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fbf8f1" stroke="{_INK}" stroke-width="1.6"/>' for x, y, r in
                   ((110, 92, 30), (150, 82, 32), (190, 92, 30), (210, 122, 28), (180, 146, 30), (140, 150, 30), (100, 140, 30), (88, 114, 26))) + '<circle cx="150" cy="116" r="46" fill="#fbf8f1"/>'
    legs = "".join(f'<rect x="{x}" y="166" width="16" height="22" rx="7" fill="#3a3f4b"/>' for x in (108, 130, 162, 184))
    head = (f'<ellipse cx="70" cy="104" rx="30" ry="34" fill="#3a3f4b"/><ellipse cx="42" cy="88" rx="16" ry="7" fill="#3a3f4b" transform="rotate(-25 42 88)"/>'
            f'<ellipse cx="98" cy="84" rx="16" ry="7" fill="#3a3f4b" transform="rotate(25 98 84)"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#fbf8f1" stroke="{_INK}" stroke-width="1.4"/>' for x, y in ((60, 74), (76, 70), (68, 66)))
            + f'<circle cx="60" cy="104" r="3.4" fill="#fbfcfa"/><circle cx="80" cy="104" r="3.4" fill="#fbfcfa"/><path d="M64 120 q6 5 12 0" fill="none" stroke="#fbfcfa" stroke-width="2" stroke-linecap="round"/>'
            f'<ellipse cx="52" cy="116" rx="5" ry="3" fill="{_BERRY}" opacity=".55"/><ellipse cx="88" cy="116" rx="5" ry="3" fill="{_BERRY}" opacity=".55"/>')
    return f'<svg viewBox="0 0 280 200" role="img" aria-label="Finished crochet sheep: fluffy white body, dark grey head, ears and four legs"><rect width="280" height="200" rx="10" fill="#e9f1ef"/>{wool}{legs}{head}<text x="262" y="26" {_T12} text-anchor="end">about 4 in long in worsted</text></svg>'


def _sheep_parts_svg():
    def ball(cx, cy, rx, ry, fill, lab):
        return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{_INK}" stroke-width="1.6"/><text x="{cx}" y="{cy + ry + 16}" {_T12} text-anchor="middle">{lab}</text>'
    s = (ball(60, 80, 42, 40, "#fbf8f1", "body x1") + ball(150, 72, 26, 28, "#3a3f4b", "head x1") + ball(150, 150, 18, 9, "#fbf8f1", "wool tuft x1") +
         "".join(ball(x, 66, 7, 12, "#3a3f4b", "") for x in (212, 232)) + f'<text x="222" y="96" {_T12} text-anchor="middle">ears x2</text>' +
         "".join(f'<rect x="{x}" y="128" width="12" height="22" rx="6" fill="#3a3f4b"/>' for x in (198, 214, 230, 246)) + f'<text x="228" y="168" {_T12} text-anchor="middle">legs x4</text>')
    return _svg12(s, "The crochet sheep pieces: one body, one head, one wool tuft, two ears and four legs")


SHEEP = [
    ("Body", "white", "Make 1. Work in continuous rounds (a spiral); move a stitch marker up each round.", [
        ("1", "6 sc in a magic ring", 6), ("2", "inc in each st around", 12), ("3", "(sc 1, inc) x 6", 18), ("4", "(sc 2, inc) x 6", 24),
        ("5", "(sc 3, inc) x 6", 30), ("6", "(sc 4, inc) x 6", 36), ("7-14", "sc in each st around (8 rounds)", 36),
        ("15", "(sc 4, dec) x 6", 30), ("16", "(sc 3, dec) x 6", 24), ("", "Start stuffing firmly.", None), ("17", "(sc 2, dec) x 6", 18),
        ("18", "(sc 1, dec) x 6", 12), ("", "Finish stuffing.", None), ("19", "dec x 6", 6), ("", "Fasten off, thread the tail through the front loops of the last 6 stitches and pull closed.", None)]),
    ("Head", "dark grey", "Make 1.", [
        ("1", "6 sc in a magic ring", 6), ("2", "inc in each st around", 12), ("3", "(sc 1, inc) x 6", 18), ("4", "(sc 2, inc) x 6", 24),
        ("5-9", "sc in each st around (5 rounds)", 24), ("", "Fit safety eyes between rounds 6 and 7, about 5 stitches apart (or embroider them later for a baby).", None),
        ("10", "(sc 2, dec) x 6", 18), ("11", "(sc 1, dec) x 6", 12), ("", "Stuff firmly.", None), ("12", "dec x 6", 6), ("", "Fasten off and close as for the body. Leave a long tail for sewing.", None)]),
    ("Wool tuft", "white", "Make 1. A little cap of wool for the top of the head.", [
        ("1", "6 sc in a magic ring", 6), ("2", "inc in each st around", 12), ("3", "(sc 1, inc) x 6", 18), ("4", "sc in each st around", 18), ("", "Sl st to join, fasten off with a long tail. Don't stuff.", None)]),
    ("Ears", "dark grey", "Make 2.", [
        ("1", "4 sc in a magic ring", 4), ("2", "inc in each st around", 8), ("3-4", "sc in each st around (2 rounds)", 8), ("", "Don't stuff. Flatten, fasten off with a tail for sewing.", None)]),
    ("Legs", "dark grey", "Make 4.", [
        ("1", "6 sc in a magic ring", 6), ("2", "(sc 1, inc) x 3", 9), ("3-5", "sc in each st around (3 rounds)", 9), ("", "Stuff lightly, fasten off with a long tail.", None)]),
]


def _sheep_rounds():
    out, i = [], 0
    for name, colour, note, rows in SHEEP:
        out.append(f'<h3 id="shp-{name.split()[0].lower()}">{e(name)} <small>({e(colour)})</small></h3><p>{e(note)}</p><ul class="shp-list">')
        for rn, txt, cnt in rows:
            if cnt is None:
                out.append(f'<li class="shp-note">{e(txt)}</li>')
            else:
                out.append(f'<li><label class="chk"><input type="checkbox" data-shp="{i}"> <span><strong>R{e(rn)}:</strong> {e(txt)} <em>({cnt})</em></span></label></li>')
                i += 1
        out.append('</ul>')
    return "".join(out), i


_shp_html, _shp_n = _sheep_rounds()

shp = top("Free crochet sheep pattern (easy amigurumi)", "A chubby little amigurumi sheep you can make in an evening: a round white body, a dark head with floppy ears, four stubby legs and a tuft of wool on top. It's all single crochet in the round, so it's a great first toy. Tick off each round as you go, and the helper works out the size and yarn for the yarn you have.", "Crochet sheep pattern") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to crochet an easy sheep, make a <strong>white ball for the body</strong> (6 sc in a magic ring, increase by 6 each round to 36, work 8 plain rounds, then decrease back to 6), a <strong>smaller dark ball for the head</strong> (up to 24 stitches), <strong>four short tubes for legs</strong>, <strong>two flat ears</strong> and a little <strong>white wool cap</strong>. Sew the head to the front of the body, the legs underneath and the ears to the sides of the head. In worsted yarn with a 3.5 mm hook it's about 4 in (10 cm) long and uses roughly 30 yd of white and 25 yd of dark grey (our estimates).</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="gq-figs"><figure class="gq-fig"><div>{_sheep_svg()}<figcaption><strong>The finished sheep.</strong> Our own drawing of the design on this page.</figcaption></div></figure><figure class="gq-fig"><div>{_sheep_parts_svg()}<figcaption><strong>The pieces.</strong> Five shapes, all single crochet in the round.</figcaption></div></figure></div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Sheep size and yarn helper</h3>
<div class="field"><label for="shp-y">Yarn you have</label><select id="shp-y"><option value="dk">DK / light (3), with a 3 mm hook</option><option value="w" selected>Worsted / aran (4), with a 3.5 mm hook</option><option value="ch">Chunky (5), with a 5 mm hook</option><option value="sb">Super bulky chenille or plush yarn (6), with a 6 mm hook</option></select></div>
<p class="sub">Tick the rounds in the pattern below as you work them: your place is kept on this device.</p>
</div><div class="result" aria-live="polite" id="shp-out" data-n="{_shp_n}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> white (or cream) and dark grey or black, in the same weight. A smooth acrylic or cotton worsted is easiest to see. For an extra fluffy sheep, use a white bouclé or chenille plush yarn for the body and tuft, with a hook to match (see the helper).</li>
<li><strong>Hook:</strong> about 2 sizes smaller than the yarn label says, so the stitches are tight and the stuffing doesn't show. 3.5 mm (E-4) for worsted.</li>
<li><strong>Safety eyes</strong> (8 mm for worsted) or black and white embroidery thread, a <strong>stitch marker</strong>, <strong>polyester toy stuffing</strong>, a <strong>tapestry needle</strong> and scissors. A little pink thread or blusher for cheeks is optional.</li></ul>
<h2>Abbreviations (US terms)</h2>
<p><strong>sc</strong> single crochet (UK double crochet), <strong>inc</strong> 2 sc in the same stitch, <strong>dec</strong> single crochet 2 together (an invisible decrease through the front loops looks neatest), <strong>sl st</strong> slip stitch, <strong>R</strong> round, <strong>(…) x 6</strong> repeat 6 times. The number in brackets at the end is the stitch count. Using UK terms? Swap every sc for dc; the <a href="{href("crochet-terms.html")}">US vs UK crochet terms</a> chart has the rest.</p>
<h2>The pattern, round by round</h2>
{_shp_html}
<h2>How to put your sheep together</h2>
<ol><li><strong>Head:</strong> pin it to the front of the body, slightly tilted up, over about rounds 5 to 11 of the body. Sew all the way round with the head's tail, then go round once more so it doesn't wobble.</li>
<li><strong>Wool tuft:</strong> sew it to the top of the head, slightly towards the back, like a little cap.</li>
<li><strong>Ears:</strong> sew one to each side of the head, just under the tuft, pointing out and a little down.</li>
<li><strong>Legs:</strong> sew the four legs to the underside of the body in a square, about 6 stitches apart, so the sheep stands on them. Push a little more stuffing into each leg before closing the seam.</li>
<li><strong>Face:</strong> if you didn't use safety eyes, embroider them now. Add a small white straight stitch nose or a smile, and a dab of pink for cheeks.</li></ol>
<p>New to this? See <a href="{href("how-to-crochet-magic-ring.html")}">how to crochet a magic ring</a>, <a href="{href("how-to-crochet-increase.html")}">how to increase</a> and <a href="{href("how-to-crochet-decrease.html")}">how to decrease</a> (with the invisible decrease), and <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a> for toys. The <a href="{href("amigurumi.html")}">amigurumi guide</a> explains spiral rounds and stuffing.</p>
<h2>Make it your own</h2>
<ul><li><strong>Bigger sheep:</strong> same pattern, thicker yarn and bigger hook. In chunky chenille it's a squishy cushion-sized friend.</li>
<li><strong>Black sheep:</strong> swap the colours: black body, cream head.</li>
<li><strong>Christmas sheep:</strong> add a tiny scarf (chain 40, one row of sc) or a hanging loop for the tree.</li>
<li><strong>Keyring sheep:</strong> use DK cotton and a 2.5 mm hook, skip rounds 12 to 13 of the body, and sew a key ring to the back.</li>
<li><strong>Want a bigger or flatter body?</strong> The <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a> gives the increase rounds for any size ball.</li></ul>
<h2>Selling your sheep</h2>
<p>You're welcome to sell sheep you make from this pattern; we just ask that you don't sell or share the pattern itself as your own. Price them so your time counts: the <a href="{href("how-to-price-amigurumi.html")}">amigurumi pricing calculator</a> works it out from your hours and materials. If you sell toys for babies and young children, embroider the eyes and check the toy safety rules where you sell.</p>
<p class="note">Pattern, drawings and wording are our own, designed on 27 Nov 2026 using the standard amigurumi round maths. Sizes and yarn amounts are estimates: your tension and yarn will change them, so buy a little extra.</p>
</div></div></section>'''
shp_faq = [
    ("How do you crochet a sheep for beginners?", "Crochet a white ball for the body, a smaller dark ball for the head, four short tubes for legs, two flat ears and a little wool cap, all in single crochet rounds. Stuff the pieces and sew them together."),
    ("How much yarn do I need to crochet a sheep?", "For this pattern in worsted yarn, roughly 30 yards of white and 25 yards of dark grey (our estimate). Chunky yarn needs about half as much again, and super bulky chenille about twice as much."),
    ("What yarn makes a fluffy crochet sheep?", "A white bouclé or chenille plush yarn gives a woolly, fluffy look. Plain acrylic or cotton is easier for beginners because you can see the stitches."),
    ("What size hook for a crochet sheep?", "About two sizes smaller than the yarn label suggests, so the fabric is tight: 3.5 mm (E-4) for worsted, 3 mm for DK."),
    ("How big is a crochet sheep?", "In worsted yarn with a 3.5 mm hook, this sheep is about 4 in (10 cm) long. In super bulky chenille with a 6 mm hook it's closer to 8 or 9 in (an estimate)."),
    ("Are safety eyes safe for babies?", "For children under 3, embroider the eyes instead: safety eyes are small parts and can come loose."),
]
SHOP_FOR["crochet-sheep-pattern.html"] = ["crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-tags"]
page("crochet-sheep-pattern.html", "Free Crochet Sheep Pattern (Easy Amigurumi for Beginners)",
     "Free easy crochet sheep pattern for beginners: round-by-round amigurumi body, head, ears and legs with tick boxes, plus a yarn and size helper.",
     shp, shp_faq, "Crochet sheep pattern", app_name="Crochet sheep pattern tracker and yarn helper")
