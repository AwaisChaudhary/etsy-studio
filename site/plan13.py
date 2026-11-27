# ---------------- 27 Nov 2026 run 13: EMBROIDERY HOOP SIZE CALCULATOR + HOW TO PUNCH NEEDLE + HOW TO KNIT A SCARF ----------------
# Executed from build.py after plan12.py (shares page(), top(), href(), e(), SHOP_FOR, _svg12, _T12).
# Demand evidence in DEMAND.md (RADAR 27 Nov run 13). Drawings our own SVG; wording our own. JS in assets/app.js (ehc-*, pnm-*, ksw-*).

_INK, _BERRY, _TEAL, _GOLD, _WOOD = "#1f2a44", "#b8326a", "#2f8f8a", "#e39a14", "#c99a5b"


# ======== EMBROIDERY HOOP SIZE CALCULATOR ========
# Demand: 'embroidery hoop size guide', 'what size embroidery hoop do I need' (SERP 27 Nov: Instructables, Practical Embroidery,
# WeAllSew x2, Ricoma, HC Quilts, Stitcher UK, Missouri Quilt shop, several machine-hoop guides; no hand-embroidery calculator on page 1).
# Facts: hoop about 2-4 cm (1-1.5 in) bigger than the design, 6-7 in hoops most comfortable, re-centre a 6-7 in hoop for big designs,
# don't leave fabric in the hoop between sessions (practicalembroidery.eu); fabric margin is our rule of thumb (labelled).

def _hoop_svg():
    s = (f'<circle cx="140" cy="88" r="68" fill="#fbf8f1" stroke="{_WOOD}" stroke-width="10"/><circle cx="140" cy="88" r="74" fill="none" stroke="{_INK}" stroke-width="1.6"/>'
         f'<rect x="186" y="18" width="22" height="14" rx="3" fill="{_WOOD}" stroke="{_INK}" stroke-width="1.4" transform="rotate(42 197 25)"/>'
         f'<rect x="104" y="52" width="72" height="72" rx="4" fill="none" stroke="{_BERRY}" stroke-width="2.4" stroke-dasharray="6 4"/>'
         f'<path d="M104 52 L176 124" stroke="{_TEAL}" stroke-width="2"/><text x="18" y="190" {_T12}>the design\'s diagonal + a clear margin = hoop</text>')
    return _svg12(s, "A round hoop with a rectangular design inside: the corners of the design must fit inside the ring.")


ehp = top("Embroidery hoop size calculator", "Which hoop does your design need, and how big a piece of fabric should you cut? Enter the design size and whether you'll stitch it and frame it, or show it off in the hoop. The calculator checks the corners fit inside the ring, picks the shop size, and draws it to scale.", "Embroidery hoop size calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> pick a hoop about <strong>1 to 1.5 in (2.5 to 4 cm) bigger than your design</strong>, measured across its widest point, so the whole design sits inside without re-hooping. For a square or rectangle that means the <strong>diagonal</strong>, not the width: a 4 × 4 in design needs a 7 in hoop. Most people find a <strong>6 or 7 in hoop</strong> the most comfortable to hold; for anything bigger than about 10 in, use a scroll frame or move a 7 in hoop around. Cut the fabric at least <strong>2 in (5 cm) bigger than the hoop on every side</strong> (our rule of thumb).</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Your design</h3>
<div class="row2"><div class="field"><label for="ehc-w">Design width</label><input type="number" id="ehc-w" value="4" min="0.5" max="60" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="ehc-h">Design height</label><input type="number" id="ehc-h" value="4" min="0.5" max="60" step="0.25" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="ehc-sh">Design shape</label><select id="ehc-sh"><option value="rect">Square or rectangle (corners matter)</option><option value="round">Round, oval or a loose motif</option></select></div>
<div class="field"><label for="ehc-use">What happens after</label><select id="ehc-use"><option value="stitch">Stitch, then frame or sew it into something</option><option value="display">Display it in the hoop</option></select></div></div>
<div class="field"><span class="label" id="ehc-u-l">Units</span><div class="seg" role="group" aria-labelledby="ehc-u-l" id="ehc-u"><button type="button" data-v="in" aria-pressed="true">inches</button><button type="button" data-v="cm" aria-pressed="false">cm</button></div></div>
</div><div class="result" aria-live="polite" id="ehc-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to choose an embroidery hoop size</h2>
<figure class="gq-fig" style="max-width:420px">{_hoop_svg()}<figcaption>A square design in a round hoop: the corners decide the size.</figcaption></figure>
<ol><li><strong>Measure the design</strong> at its widest and tallest points, including any lettering and loose stitches round the edge.</li>
<li><strong>Square or rectangle?</strong> Use the diagonal (corner to corner), because the corners are what touch the ring first. A round or oval motif only needs its widest measurement.</li>
<li><strong>Add a margin</strong> of about 1 to 1.5 in (2.5 to 4 cm) in total, so there's half an inch or so of clear fabric between the design and the inner ring. Your needle needs room, and stitches pressed under the ring get crushed.</li>
<li><strong>Round up</strong> to the next hoop you can buy. Shops usually stock 3, 4, 5, 6, 7, 8, 9, 10 and 12 in hoops (about 7.5 to 30 cm), with 14 in and up as quilting or specialist hoops.</li></ol>
<h2>Hoop size chart</h2>
<div class="tbl-wrap"><table><thead><tr><th>Hoop</th><th>Round design up to</th><th>Square design up to</th><th>Good for</th></tr></thead><tbody>
{"".join(f'<tr><td>{h} in ({round(h * 2.54, 1):g} cm)</td><td>{h - 1:g} in</td><td>{round((h - 1) / 1.414 * 4) / 4:g} × {round((h - 1) / 1.414 * 4) / 4:g} in</td><td>{u}</td></tr>' for h, u in ((3, "Tiny motifs, brooches, ornaments"), (4, "Ornaments, pocket motifs, initials"), (5, "Small florals, patches"), (6, "The most common beginner size"), (7, "Comfortable all-rounder; most kits"), (8, "Wall hoops, bigger florals"), (9, "Wall hoops"), (10, "Large wall art; heavier to hold"), (12, "Very large wall art; use a stand")))}
</tbody></table></div>
<p>Sizes are inner diameters as sold. Square sizes allow a 1 in total margin round the design's diagonal (our calculation).</p>
<h2>Display in the hoop or stitch and frame?</h2>
<p>If the hoop <strong>is</strong> the frame, the design should fill it nicely: we suggest aiming for the design to take up about 55 to 80% of the hoop's width, so it doesn't look lost in the middle or cramped against the ring. A bamboo or beech hoop with a neat screw is worth it here; cheap hoops are fine for stitching. If you'll frame the work, sew it into a cushion or turn it into a patch, the hoop only has to hold the fabric while you stitch, so comfort wins: a 6 or 7 in hoop that you move around is easier than a huge one.</p>
<h2>What if the design is bigger than my hoop?</h2>
<p>You can stitch one area, loosen the screw, move the hoop and tighten it again. Put tissue paper between the fabric and the outer ring where it sits over finished stitches, and don't leave the fabric clamped between sessions: the ring leaves a crease that can be hard to iron out. For large pieces, a scroll frame, a slate frame or a clip-together plastic frame holds the whole thing flat.</p>
<h2>How much fabric to cut</h2>
<p>Cut fabric big enough to grip in the hoop with plenty to hold on to: we use <strong>at least 2 in (5 cm) beyond the hoop on every side</strong>, and 3 in (7.5 cm) or more if the piece will be framed, so there's enough to lace or tape round the backing board. Hand-stitched fabric should be drum-tight in the hoop; wrapping the inner ring with cotton tape helps slippery fabric grip.</p>
<p>Next: transfer the design with <a href="{href("how-to-transfer-embroidery-pattern.html")}">how to transfer an embroidery pattern</a>, pick stitches from <a href="{href("embroidery-stitches.html")}">12 embroidery stitches for beginners</a>, or browse free <a href="{href("embroidery-patterns.html")}">embroidery patterns</a>. Working with yarn and a frame instead? See <a href="{href("how-to-punch-needle.html")}">how to punch needle</a>. Counted cross stitch? The <a href="{href("cross-stitch-calculator.html")}">cross stitch calculator</a> sizes fabric from the stitch count.</p>
</div></div></section>'''
eh_faq = [
    ("What size embroidery hoop do I need?", "One about 1 to 1.5 in (2.5 to 4 cm) bigger than your design across its widest point. For a square or rectangular design, measure the diagonal, so a 4 × 4 in design needs about a 7 in hoop."),
    ("What is the most common embroidery hoop size?", "6 and 7 in (15 to 18 cm) hoops are the most common and the most comfortable to hold for long sessions; many kits use one of these."),
    ("Should the design be smaller than the hoop?", "Yes. Leave about half an inch (1 to 2 cm) of clear fabric between the design and the inner ring so the stitches don't get crushed and the needle has room."),
    ("How much bigger should the fabric be than the hoop?", "At least 2 in (5 cm) on every side by our rule of thumb, and 3 in or more if you'll frame it, so there's enough to grip and to lace round a board."),
    ("Can I embroider a design bigger than my hoop?", "Yes: stitch one area, then move the hoop. Protect finished stitches with tissue paper under the ring, or use a scroll frame for big pieces."),
    ("Should I leave my embroidery in the hoop?", "Not between sessions. Long clamping leaves a ring-shaped crease. Take it out when you stop, unless the hoop is the finished frame."),
]
SHOP_FOR["embroidery-hoop-size-calculator.html"] = ["machine-embroidery-business-spreadsheet", "small-business-pricing-inventory-spreadsheet", "christmas-gift-tags", "2027-habit-tracker-spreadsheet"]
page("embroidery-hoop-size-calculator.html", "Embroidery Hoop Size Calculator: What Size Hoop Do I Need?",
     "Free embroidery hoop size calculator: enter your design size to find the hoop to buy (corners checked), the fabric to cut, and a hoop size chart.",
     ehp, eh_faq, "Embroidery hoop size calculator", app_name="Embroidery hoop size calculator")


# ======== HOW TO PUNCH NEEDLE ========
# Demand: L4 'how to punch needle for beginners' (SERP 27 Nov: Hobbycraft x3, Crewel Ghoul, Gathered x2, Marching North, We Are Knitters,
# LoveCrafts x3, DMC stitch diagrams + start/finish, Sarah Maker tips, Studio Koekoek). Growth review E4 (punch needle how-to).
# Facts: Oxford #10 Regular = rug/bulky yarn (or finer yarn doubled), #10 Fine = worsted/DK/sport/fingering, both ~1/4 in loops, #8 1/2 in,
# #9 3/8 in (KnitPicks Oxford page, The Stitch Witch blog); no knots, tails pulled to loop side and trimmed, outline then fill (DMC). Wording ours.

def _pn_svg(step, label):
    cloth = f'<rect x="20" y="20" width="240" height="160" rx="6" fill="#efe6d2" stroke="{_INK}" stroke-width="1.6"/>' + "".join(f'<path d="M{x} 22 V178" stroke="#d9cdb3" stroke-width="1"/>' for x in range(32, 260, 12)) + "".join(f'<path d="M22 {y} H258" stroke="#d9cdb3" stroke-width="1"/>' for y in range(32, 180, 12))
    needle = lambda x, y, rot=0: (f'<g transform="rotate({rot} {x} {y})"><rect x="{x - 9}" y="{y - 96}" width="18" height="62" rx="8" fill="{_WOOD}" stroke="{_INK}" stroke-width="1.6"/>'
                                  f'<path d="M{x - 4} {y - 34} L{x - 4} {y - 8} L{x} {y} L{x + 4} {y - 14} L{x + 4} {y - 34} Z" fill="#9aa6c4" stroke="{_INK}" stroke-width="1.4"/>'
                                  f'<path d="M{x + 4} {y - 26} L{x + 4} {y - 12}" stroke="{_BERRY}" stroke-width="3"/></g>')
    if step == 1:
        s = (f'<rect x="12" y="12" width="256" height="176" rx="8" fill="none" stroke="{_WOOD}" stroke-width="12"/>' + cloth +
             "".join(f'<path d="M{x} 12 l4 -6 l4 6" fill="none" stroke="{_INK}" stroke-width="1.2"/>' for x in range(30, 250, 18)) +
             f'<text x="140" y="104" {_T12} text-anchor="middle">drum-tight: tap it and it sounds</text>')
    elif step == 2:
        s = (cloth + f'<text x="-140" y="130" font-family="Georgia,serif" font-size="96" font-weight="700" fill="none" stroke="{_INK}" stroke-width="2.4" text-anchor="middle" transform="scale(-1 1)">R</text>'
             f'<text x="140" y="168" {_T12} text-anchor="middle">draw on the back, mirrored</text>')
    elif step == 3:
        s = (f'<path d="M40 150 C80 120 90 60 140 52" fill="none" stroke="{_BERRY}" stroke-width="4"/>' + needle(170, 150, 0) +
             f'<path d="M140 52 L166 140" stroke="#888" stroke-width="1.6" stroke-dasharray="3 3"/><path d="M174 136 L174 120" stroke="{_BERRY}" stroke-width="3"/>'
             f'<text x="24" y="186" {_T12}>threader in at the tip, out of the handle</text>')
    elif step == 4:
        s = (cloth + needle(140, 112, 0) + f'<path d="M150 96 L210 96" stroke="{_GOLD}" stroke-width="3"/><path d="M200 89 L212 96 L200 103" fill="none" stroke="{_GOLD}" stroke-width="3"/>'
             f'<text x="196" y="84" {_T12} text-anchor="middle">opening faces</text><text x="140" y="168" {_T12} text-anchor="middle">push down to the handle</text>')
    elif step == 5:
        dots = "".join(f'<circle cx="{x}" cy="110" r="3" fill="{_BERRY}"/>' for x in range(50, 140, 12))
        s = (cloth + dots + f'<path d="M50 110 H134" stroke="{_BERRY}" stroke-width="2"/>' + needle(146, 110, 0) +
             f'<text x="140" y="168" {_T12} text-anchor="middle">lift to the surface, slide, punch</text>')
    elif step == 6:
        s = (f'<rect x="20" y="20" width="240" height="160" rx="6" fill="#efe6d2" stroke="{_INK}" stroke-width="1.6"/>' +
             "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{_TEAL if (x + y) % 3 else _BERRY}" stroke="{_INK}" stroke-width="1"/>' for x in range(52, 232, 13) for y in range(40, 136, 12)) +
             f'<text x="140" y="164" {_T12} text-anchor="middle">loops show on the front</text>')
    else:
        s = (cloth + f'<path d="M60 70 C100 60 180 60 220 70 C220 110 220 120 220 130 C180 140 100 140 60 130 Z" fill="none" stroke="{_BERRY}" stroke-width="3"/>'
             f'<path d="M80 86 C120 82 160 82 200 86 M80 100 C120 96 160 96 200 100 M80 114 C120 110 160 110 200 114" fill="none" stroke="{_TEAL}" stroke-width="3"/>'
             f'<text x="140" y="168" {_T12} text-anchor="middle">outline first, then fill in rows</text>')
    return _svg12(s, label)


PN_STEPS = [(1, "1. Stretch the fabric", "Monk's cloth or weaver's cloth, drum-tight in a gripper frame or a no-slip hoop."),
            (2, "2. Draw on the back", "You punch from the back, so trace the design mirrored (like this R) onto the side facing you."),
            (3, "3. Thread the needle", "Push the threader in at the tip, hook the yarn and pull it out through the handle end, then through the eye."),
            (4, "4. Punch to the handle", "Hold it like a pen, opening facing the way you're moving, and push straight down until the handle touches."),
            (5, "5. Slide and repeat", "Lift only to the surface, slide a few threads along, punch again. Never lift the tip right off."),
            (6, "6. Loops on the front", "Turn it over: the loops are the right side. The back shows neat flat stitches."),
            (7, "7. Outline, then fill", "Punch each outline, then fill inside in close rows that follow the shape.")]
pn_cards = "".join(f'<figure class="gq-fig"><div>{_pn_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in PN_STEPS)

pnp = top("How to punch needle for beginners", "Punch needle is the quickest way to make soft, loopy pictures, cushions and little rugs: no knots and no counting, just yarn pushed through stretched fabric. Here's the whole process in seven drawn steps, a helper that matches your yarn to the right needle and fabric, and fixes for the problems every beginner meets.", "How to punch needle") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> stretch <strong>monk's cloth</strong> (or weaver's cloth for fine yarn) <strong>drum-tight</strong> in a frame, draw the design mirrored on the back, and thread the needle. Hold it like a pen with the <strong>opening facing the way you're going</strong>, push it <strong>all the way down to the handle</strong>, lift it only back to the surface, slide a few threads along and punch again. Loops form on the front. Outline each shape first, then fill. To finish a colour, pull the tail through to the loop side and <strong>trim it to loop height</strong>: no knots needed.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Needle, yarn and fabric matcher</h3>
<div class="row2"><div class="field"><label for="pnm-y">Your yarn</label><select id="pnm-y"><option value="floss">Embroidery floss or perle cotton</option><option value="fine">Fingering, sport or DK</option><option value="worsted" selected>Worsted or aran</option><option value="bulky">Chunky, bulky or rug yarn</option><option value="strip">Fabric strips or T-shirt yarn</option></select></div>
<div class="field"><label for="pnm-p">Making</label><select id="pnm-p"><option value="hoop">Hoop art or a patch</option><option value="cushion" selected>Cushion or wall hanging</option><option value="rug">Mug rug or small rug</option></select></div></div>
<div class="field"><label for="pnm-f">Pile you want</label><select id="pnm-f"><option value="flat">Flat, close loops (crisp detail)</option><option value="mid" selected>Medium loops</option><option value="plush">Tall, plush loops</option></select></div>
</div><div class="result" aria-live="polite" id="pnm-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to punch needle, step by step</h2>
<div class="gq-figs">{pn_cards}</div>
<h2>What you need to start</h2>
<ul><li><strong>A punch needle.</strong> A regular (rug) needle for thick yarn, or a fine one for medium and thin yarn. Adjustable needles change the loop height with a gauge or a collar.</li>
<li><strong>Foundation fabric</strong> with a loose, even weave the needle can open without tearing: monk's cloth for regular needles, weaver's cloth or a firm cotton for fine ones. Plain cotton tears; avoid stretchy fabric.</li>
<li><strong>A frame or hoop that grips.</strong> A gripper-strip frame (carpet tacks on a wooden frame) or a no-slip hoop. Ordinary embroidery hoops let the fabric creep, which is the commonest reason loops pull out.</li>
<li><strong>Yarn</strong> that runs freely: unwind a good length into a loose pile first, so it isn't tugging.</li>
<li>Small sharp scissors, a fabric marker, and glue or a needle and thread for finishing.</li></ul>
<h2>Tips that make it work</h2>
<ul><li><strong>Keep the yarn loose.</strong> If anything pulls on it (the ball, the edge of the frame, your hand), the loop you just made comes back out.</li>
<li><strong>Stay close to the surface.</strong> Lift the needle only until the tip reaches the fabric, then drag it to the next spot. Lifting higher pulls the loops back.</li>
<li><strong>Small steps, close rows.</strong> Move about 3 mm (a few threads of the weave) between punches, and keep rows about a needle's width apart, closer for fine needles. Gaps show as bare fabric on the front.</li>
<li><strong>Turning corners:</strong> keep the tip down in the fabric and swivel the handle so the opening faces the new direction.</li>
<li><strong>Change direction for texture.</strong> Rows that follow the shape (round a circle, along a leaf) look smoother than straight rows.</li>
<li><strong>Flat side as a feature:</strong> the back shows a pretty flat stitch. Some designs use both sides: punch the background from the front and the motif from the back.</li></ul>
<h2>Finishing a punch needle piece</h2>
<p>Trim every tail to loop height on the front. For <strong>hoop art</strong>, leave it in the hoop, trim the fabric to about 1 in (2.5 cm) past the ring, then glue it down or run a gathering stitch round it and pull tight. For a <strong>cushion or patch</strong>, fold the margin to the back and stitch or glue it, then back with felt. For a <strong>rug</strong>, leave about 2 in (5 cm) of margin, fold it under, whip stitch or bind the edge and add a non-slip backing. A light coat of fabric glue on the back holds loops in pieces that will be handled a lot. The <a href="{href("punch-needle.html")}">punch needle fabric calculator</a> tells you how much fabric to cut and what frame to use.</p>
<h2>Common punch needle problems</h2>
<ul><li><strong>Loops pull out:</strong> fabric too loose, yarn under tension, or the needle lifted too high. Re-tighten and punch again in the same row.</li>
<li><strong>Uneven loop height:</strong> you're not pushing all the way to the handle every time.</li>
<li><strong>Fabric shows between loops:</strong> rows or stitches are too far apart. Fill the gaps from the back.</li>
<li><strong>Needle sticks or snags:</strong> the yarn is too thick for the needle, or there's a knot in the yarn.</li>
<li><strong>Loops on the wrong side:</strong> the opening is facing backwards. Turn the needle so it faces the way you travel.</li></ul>
<p>Want bigger, faster rugs? See <a href="{href("tufting.html")}">tufting</a>. Planning colours? Try the <a href="{href("stripe-generator.html")}">random stripe generator</a> for a palette, and pick a hoop with the <a href="{href("embroidery-hoop-size-calculator.html")}">embroidery hoop size calculator</a>.</p>
</div></div></section>'''
pn_faq = [
    ("How do you punch needle for beginners?", "Stretch monk's cloth drum-tight in a frame, draw the design mirrored on the back, thread the needle, then punch down to the handle with the opening facing your direction of travel, lifting only to the surface between punches. Outline shapes first, then fill."),
    ("What fabric do you use for punch needle?", "Monk's cloth for regular (rug) needles and weaver's cloth or a firm, even cotton for fine needles. Ordinary cotton can tear and stretchy fabric won't hold the loops."),
    ("What yarn do you use for punch needle?", "Bulky or rug yarn (or finer yarn held double) with a regular needle; worsted, DK, sport or fingering with a fine needle; embroidery floss with a small embroidery punch needle."),
    ("Which side is the front in punch needle?", "You punch from the back. The loops form on the other side, which is usually the front; the side you punch from shows flat stitches."),
    ("Why are my punch needle loops coming out?", "Usually the fabric is too loose, the yarn is being pulled, or you lift the needle too far between punches. Tighten the fabric, unwind loose yarn, and keep the tip at the surface."),
    ("Do you need to knot punch needle?", "No. Fabric tension and close stitches hold the loops. Pull the tails to the loop side and trim them level with the loops."),
]
SHOP_FOR["how-to-punch-needle.html"] = ["small-business-pricing-inventory-spreadsheet", "machine-embroidery-business-spreadsheet", "christmas-gift-tags", "2027-habit-tracker-spreadsheet"]
page("how-to-punch-needle.html", "How to Punch Needle for Beginners (7 Drawn Steps)",
     "How to punch needle for beginners: seven drawn steps, the right needle, yarn and fabric for your project, finishing hoops, cushions and rugs, and fixes.",
     pnp, pn_faq, "How to punch needle", app_name="Punch needle, yarn and fabric matcher")


# ======== HOW TO KNIT A SCARF ========
# Demand: 'how to knit a scarf for beginners' (SERP 27 Nov: LoveCrafts US+UK, Sheep & Stitch x2, Skillshare x3, Lion Brand 3 easy steps,
# Fiskars, Sarah Maker, Knit Picks tutorials, Ravelry beginner patterns, Yours.co.uk). Seasonal: Christmas gift knitting.
# Facts: Craft Yarn Council knit gauge ranges per weight (also in data.json weights). Garter, seed and rib stitch maths standard. Wording ours.

def _ks_svg(step, label):
    if step == 1:
        s = (f'<circle cx="90" cy="110" r="46" fill="{_BERRY}" stroke="{_INK}" stroke-width="2"/>' + "".join(f'<path d="M{50 + i * 14} {80 + (i % 2) * 6} C{70 + i * 10} 110 {60 + i * 12} 140 {74 + i * 10} 150" fill="none" stroke="#e07aa3" stroke-width="2"/>' for i in range(5)) +
             f'<path d="M160 60 L250 160 M176 50 L262 152" stroke="{_INK}" stroke-width="2.4"/><circle cx="160" cy="60" r="6" fill="{_GOLD}" stroke="{_INK}"/><circle cx="176" cy="50" r="6" fill="{_GOLD}" stroke="{_INK}"/>'
             f'<text x="140" y="190" {_T12} text-anchor="middle">worsted yarn + 5 mm (US 8) needles</text>')
    elif step == 2:
        s = (f'<path d="M30 110 L250 110" stroke="{_INK}" stroke-width="3"/>' + "".join(f'<path d="M{x} 102 c-6 8 -6 16 0 22 c6 -6 6 -14 0 -22" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for x in range(50, 230, 16)) +
             f'<text x="140" y="60" {_T12} text-anchor="middle">cast on: one loop per stitch</text><text x="140" y="160" {_T12} text-anchor="middle">e.g. 24 stitches for a 6 in scarf</text>')
    elif step == 3:
        ridges = "".join(f'<path d="M40 {y} q10 -8 20 0 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0" fill="none" stroke="{_TEAL}" stroke-width="3"/>' for y in range(60, 170, 14))
        s = ridges + f'<text x="140" y="190" {_T12} text-anchor="middle">knit every row = garter stitch ridges</text>'
    elif step == 4:
        s = (f'<path d="M30 120 C80 100 120 100 140 110" fill="none" stroke="{_BERRY}" stroke-width="4"/><path d="M140 110 C170 120 210 130 250 110" fill="none" stroke="{_TEAL}" stroke-width="4"/>'
             f'<path d="M120 108 C130 90 150 92 160 116" fill="none" stroke="{_TEAL}" stroke-width="4" stroke-dasharray="5 3"/>'
             f'<text x="140" y="60" {_T12} text-anchor="middle">new ball at the start of a row</text><text x="140" y="160" {_T12} text-anchor="middle">leave 6 in tails to weave in</text>')
    elif step == 5:
        s = (f'<path d="M30 110 L250 110" stroke="{_INK}" stroke-width="3"/>' + "".join(f'<ellipse cx="{x}" cy="110" rx="9" ry="6" fill="none" stroke="{_BERRY}" stroke-width="3"/>' for x in range(50, 170, 18)) +
             f'<path d="M190 104 c-6 8 -6 16 0 22" fill="none" stroke="{_BERRY}" stroke-width="3"/><path d="M206 104 c-6 8 -6 16 0 22" fill="none" stroke="{_BERRY}" stroke-width="3"/>'
             f'<path d="M206 96 C200 80 186 80 190 98" fill="none" stroke="{_GOLD}" stroke-width="2.6"/><text x="140" y="60" {_T12} text-anchor="middle">bind off: lift one stitch over the next</text>')
    else:
        s = (f'<rect x="90" y="20" width="100" height="130" rx="4" fill="{_TEAL}" stroke="{_INK}" stroke-width="2"/>' +
             "".join(f'<path d="M{x} 150 L{x + (i % 3 - 1) * 3} 186" stroke="{_TEAL}" stroke-width="4" stroke-linecap="round"/>' for i, x in enumerate(range(96, 188, 9))) +
             "".join(f'<path d="M94 {y} H186" stroke="#26706c" stroke-width="2"/>' for y in range(34, 150, 10)) + f'<text x="236" y="100" {_T12} text-anchor="middle">fringe</text><text x="236" y="116" {_T12} text-anchor="middle">optional</text>')
    return _svg12(s, label)


KS_STEPS = [(1, "1. Choose yarn and needles", "A smooth, light-coloured worsted yarn and 5 mm (US 8) needles make the stitches easy to see."),
            (2, "2. Cast on", "Make a slip knot and cast on the stitches for your width. The writer below gives the number."),
            (3, "3. Knit every row", "Knit to the end, swap the needles over and knit again. That's garter stitch: flat, squishy and it doesn't curl."),
            (4, "4. Join a new ball", "Start the new ball at the beginning of a row, leaving tails of both yarns to weave in later."),
            (5, "5. Bind off", "At the length you want, knit two, lift the first over the second, and repeat to the end."),
            (6, "6. Finish", "Weave in the ends, block if you like, and add fringe for a classic look.")]
ks_cards = "".join(f'<figure class="gq-fig"><div>{_ks_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in KS_STEPS)

ksp = top("How to knit a scarf for beginners", "A scarf is the classic first knitting project: it's just rows, so you practise the knit stitch over and over and end up with something to wear or give. Here's every step drawn, plus a writer that turns your yarn and size into a full beginner pattern with the stitches to cast on.", "How to knit a scarf") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> with <strong>worsted yarn and 5 mm (US 8) needles</strong>, <strong>cast on about 27 to 32 stitches</strong> for a 6 to 7 in wide scarf. <strong>Knit every row</strong> (garter stitch) until it's about <strong>60 to 70 in (150 to 180 cm)</strong> long, or as long as the wearer is tall. <strong>Bind off</strong>, weave in the ends, and add fringe if you like. An adult 65 × 7 in scarf in worsted takes roughly 270 to 340 yards: about 2 skeins of 200 yd (our estimate; see the <a href="{href("scarf-size-chart.html")}">scarf size calculator</a> for your exact yarn).</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Beginner scarf pattern writer</h3>
<div class="row2"><div class="field"><label for="ksw-y">Yarn weight</label><select id="ksw-y"><option value="3">3 Light (DK)</option><option value="4" selected>4 Medium (Worsted, Aran)</option><option value="5">5 Bulky (Chunky)</option><option value="6">6 Super Bulky</option></select></div>
<div class="field"><label for="ksw-s">Stitch</label><select id="ksw-s"><option value="garter" selected>Garter (knit every row): easiest</option><option value="seed">Seed stitch (knit 1, purl 1)</option><option value="rib">2 × 2 rib (knit 2, purl 2)</option></select></div></div>
<div class="row2"><div class="field"><label for="ksw-w">Width (in)</label><input type="number" id="ksw-w" value="7" min="2" max="24" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="ksw-l">Length (in)</label><input type="number" id="ksw-l" value="65" min="10" max="120" step="1" inputmode="decimal"></div></div>
<div class="field"><label for="ksw-g">My gauge, stitches per 4 in (optional)</label><input type="number" id="ksw-g" value="" min="4" max="40" step="1" inputmode="numeric" placeholder="leave blank to use the yarn label average"></div>
</div><div class="result" aria-live="polite" id="ksw-out" data-scarf="{href("scarf-size-chart.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to knit a scarf, step by step</h2>
<div class="gq-figs">{ks_cards}</div>
<h2>Best yarn and needles for a first scarf</h2>
<p>Choose a <strong>smooth worsted or chunky yarn</strong> in a light, solid colour so you can see every stitch. Wool and wool blends are warm and forgiving; acrylic is cheap and washable. Skip fluffy mohair, eyelash and very dark yarns for now: they hide your stitches and make mistakes hard to fix. Use the needle size on the yarn label, or one size up for a softer, drapier scarf. Straight needles of 10 to 14 in (25 to 35 cm) hold a scarf's width easily. The <a href="{href("yarn-weights.html")}">yarn weight chart</a> lists the needle sizes for every weight.</p>
<h2>How many stitches to cast on for a scarf</h2>
<p>Multiply the width you want by the stitches per inch on the yarn label (the label gives stitches per 4 in, so divide by 4). For worsted at about 18 stitches per 4 in, a 7 in scarf is 7 × 4.5 = about 32 stitches. Garter stitch pulls in a little less than you'd think, so your width will be close. For seed stitch use an odd number; for 2 × 2 rib, a multiple of 4 plus 2, so both edges match. The writer above rounds for you. For any other project, the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> does the same maths.</p>
<h2>Which stitch pattern?</h2>
<ul><li><strong>Garter stitch</strong> (knit every row): the easiest, lies flat, looks the same both sides. Perfect first scarf.</li>
<li><strong>Seed stitch</strong>: knit 1, purl 1 across, and knit the purls and purl the knits on the next row. Bumpy, flat and reversible: a good second project.</li>
<li><strong>Ribbing</strong>: knit 2, purl 2. Stretchy and reversible, it pulls in, so you need more stitches for the same width.</li>
<li><strong>Avoid stockinette</strong> (knit one row, purl one row) for a scarf on its own: the edges roll into a tube. Browse <a href="{href("knit-stitch-patterns.html")}">15 knit stitch patterns for beginners</a> for more flat options.</li></ul>
<h2>Beginner scarf mistakes and fixes</h2>
<ul><li><strong>Scarf getting wider or narrower:</strong> count your stitches every few rows. Extra stitches usually come from wrapping the yarn over the needle by accident or knitting into the first stitch twice; a lost one is a <a href="{href("how-to-fix-a-dropped-stitch.html")}">dropped stitch</a>.</li>
<li><strong>Tight first row:</strong> cast on over two needles held together, or with a needle a size bigger.</li>
<li><strong>Wobbly edges:</strong> slip the first stitch of every row purlwise with the yarn in front, then move the yarn back and carry on. That gives a neat chain edge.</li>
<li><strong>Tight bind off:</strong> bind off with a needle one or two sizes bigger. See <a href="{href("how-to-bind-off-knitting.html")}">how to bind off knitting</a>.</li></ul>
<h2>How long does it take to knit a scarf?</h2>
<p>A beginner knitting an adult garter scarf in worsted usually needs somewhere around 10 to 20 hours; in chunky yarn on big needles it can be half that. Use the <a href="{href("crochet-time-estimator.html")}">knitting time calculator</a> to see if a scarf will be ready for Christmas, and the <a href="{href("row-counter.html")}">row counter</a> to keep your place.</p>
<p>New to knitting? Start with <a href="{href("how-to-cast-on-knitting.html")}">how to cast on</a> and <a href="{href("how-to-knit-and-purl.html")}">how to knit and purl</a>, then <a href="{href("how-to-weave-in-ends.html")}">weave in your ends</a> when you're done.</p>
</div></div></section>'''
ks_faq = [
    ("How many stitches do I cast on for a beginner scarf?", "With worsted yarn and 5 mm (US 8) needles, about 27 to 32 stitches gives a 6 to 7 in wide scarf. Multiply the width by the stitches per inch on your yarn label."),
    ("What is the easiest scarf to knit?", "A garter stitch scarf: knit every row. It lies flat, doesn't curl and looks the same on both sides."),
    ("How long should a knitted scarf be?", "About 60 to 70 in (150 to 180 cm) for an adult, or roughly the wearer's height. Children need about 50 to 60 in."),
    ("How much yarn do I need to knit a scarf?", "Roughly 270 to 340 yards of worsted for an adult 65 × 7 in scarf, about 2 skeins of 200 yd (our estimate). Buy one extra from the same dye lot."),
    ("Why is my knitted scarf curling?", "It's probably in stockinette stitch, which rolls at the edges. Use garter, seed or rib stitch, or add a garter border."),
    ("Why is my scarf getting wider?", "You're adding stitches by accident, usually by wrapping the yarn over the needle at the start of a row. Count your stitches every few rows."),
]
SHOP_FOR["how-to-knit-a-scarf.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-planner-budget", "crochet-knitting-pricing-calculator"]
page("how-to-knit-a-scarf.html", "How to Knit a Scarf for Beginners (+ Pattern Writer)",
     "How to knit a scarf for beginners in six drawn steps: yarn and needles, how many stitches to cast on, garter, seed or rib, and a free pattern writer.",
     ksp, ks_faq, "How to knit a scarf", app_name="Beginner scarf knitting pattern writer")
