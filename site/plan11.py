# ---------------- 27 Nov 2026 run 11: JUNK JOURNAL POCKETS + 2027 GOAL PLANNER + HOW TO BLOCK ----------------
# Executed from build.py after trends10.py (shares page(), top(), href(), e(), SHOP_FOR).
# Demand evidence in DEMAND.md (RADAR 27 Nov run 11). Drawings our own SVG; wording our own. JS in assets/app.js (jpk-*, gpl-*, blk-*).

_T11 = 'font-family="Inter,sans-serif" font-size="12" fill="#1f2a44"'

# ======== JUNK JOURNAL POCKETS ========
# Demand: 'junk journal pockets', 'how to make a pocket in a junk journal' (SERP 27 Nov: Graphics Fairy x2, Archer & Olive washi pocket,
# Splitcoast triple pocket, 101 Planners storage pocket, Skillshare origami pockets class, JenniferMaker, Crafty Chica). Wording ours.

def _pk_svg(kind, label):
    pg = '<rect x="70" y="14" width="140" height="190" rx="3" fill="#efe6d2" stroke="#9aa6c4" stroke-width="2"/>'
    card = lambda x, y, w, h, c="#fff": f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{c}" stroke="#1f2a44" stroke-width="1.6"/>'
    tag = '<path d="M112 70 L168 70 L168 150 L112 150 Z" fill="#e8d3a6" stroke="#1f2a44" stroke-width="1.6"/><circle cx="140" cy="82" r="4" fill="#efe6d2" stroke="#1f2a44" stroke-width="1.4"/><path d="M140 78 C130 60 150 50 145 36" fill="none" stroke="#b8326a" stroke-width="1.6"/>'
    if kind == "flap":
        s = pg + tag + '<rect x="90" y="118" width="100" height="72" fill="#f4c6d4" stroke="#1f2a44" stroke-width="1.8"/><path d="M90 118 L82 124 L82 186 L90 190 M190 118 L198 124 L198 186 L190 190 M90 190 L96 198 L184 198 L190 190" fill="none" stroke="#b8326a" stroke-width="1.4" stroke-dasharray="4 3"/>'
    elif kind == "fold":
        s = pg + card(104, 64, 72, 96) + '<rect x="70" y="126" width="140" height="78" fill="#d9c7a0" stroke="#1f2a44" stroke-width="1.8"/><line x1="70" y1="204" x2="210" y2="204" stroke="#b8326a" stroke-width="2" stroke-dasharray="5 3"/><path d="M220 196 C232 170 232 150 218 132" fill="none" stroke="#e39a14" stroke-width="2.4"/><path d="M214 138 L218 130 L224 138" fill="none" stroke="#e39a14" stroke-width="2.4"/>'
    elif kind == "env":
        s = pg + card(100, 60, 80, 90) + '<path d="M86 120 L194 120 L194 192 L86 192 Z" fill="#fbf8f1" stroke="#1f2a44" stroke-width="1.8"/><path d="M86 192 L140 150 L194 192" fill="none" stroke="#9aa6c4" stroke-width="1.6"/><line x1="80" y1="120" x2="200" y2="120" stroke="#b8326a" stroke-width="1.6" stroke-dasharray="4 3"/>'
    elif kind == "corner":
        s = pg + '<rect x="92" y="40" width="96" height="120" rx="2" fill="#fff" stroke="#1f2a44" stroke-width="1.6" transform="rotate(-4 140 100)"/><path d="M82 36 L138 36 L82 92 Z M198 168 L198 112 L142 168 Z" fill="#7bb7b2" stroke="#1f2a44" stroke-width="1.8"/>'
    elif kind == "band":
        s = pg + card(96, 40, 88, 116) + '<rect x="70" y="112" width="140" height="34" fill="#e39a14" opacity=".9" stroke="#1f2a44" stroke-width="1.6"/><path d="M210 112 L222 116 L222 150 L210 146" fill="#c98510" stroke="#1f2a44" stroke-width="1.4"/>'
    else:  # washi
        tape = "".join(f'<line x1="{x}" y1="0" x2="{x - 12}" y2="40" stroke="#b8326a" stroke-width="3"/>' for x in range(8, 140, 10))
        s = (pg + card(102, 50, 76, 100) + '<rect x="92" y="118" width="96" height="70" fill="#fbf8f1" stroke="#1f2a44" stroke-width="1.6"/>'
             '<rect x="82" y="182" width="116" height="14" fill="#f4c6d4" opacity=".95"/><rect x="84" y="112" width="14" height="84" fill="#f4c6d4" opacity=".95"/><rect x="182" y="112" width="14" height="84" fill="#f4c6d4" opacity=".95"/>')
    return f'<svg viewBox="0 0 280 218" role="img" aria-label="{e(label)}"><rect width="280" height="218" rx="10" fill="#f6f1e6"/>{s}</svg>'

PK_TYPES = [
    ("flap", "Glue-on pocket with flaps", "A piece of card with folded side and bottom flaps glued to the page. The easiest one to start with."),
    ("fold", "Fold-up page pocket", "Cut the page taller, fold the bottom up and glue or stitch the sides. No extra paper at all."),
    ("env", "Envelope pocket", "Cut the flap end off an envelope and glue it down, or bind it in as a page. Old letters work best."),
    ("corner", "Corner pockets", "Two paper triangles on opposite corners hold a photo or card that slides out from the side."),
    ("band", "Belly band", "A strip wrapped round the page and glued at the back. Tuck cards and tags under it."),
    ("washi", "Washi tape pocket", "A scrap of paper taped down on three sides. Quick, flat and easy to peel off again."),
]
pk_cards = "".join(f'<figure class="gq-fig"><div>{_pk_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in PK_TYPES)

PK_PAGES = [("a5", "A5 (5.8 x 8.3 in)", 5.83, 8.27), ("half", "Half letter (5.5 x 8.5 in)", 5.5, 8.5), ("6x9", "6 x 9 in", 6, 9), ("b6", "B6 (4.9 x 6.9 in)", 4.92, 6.93),
            ("a6", "A6 (4.1 x 5.8 in)", 4.13, 5.83), ("tn", "Traveler's notebook (4.3 x 8.3 in)", 4.33, 8.27), ("8x8", "8 x 8 in", 8, 8), ("custom", "Custom size", 0, 0)]
PK_FILL = [("jc", "3 x 4 in journaling card", 3, 4), ("tag5", "#5 shipping tag (2 3/8 x 4 3/4 in)", 2.375, 4.75), ("atc", "Artist trading card (2.5 x 3.5 in)", 2.5, 3.5),
           ("lib", "Library card (3 x 5 in)", 3, 5), ("photo", "4 x 6 in photo or card", 4, 6), ("tag8", "#8 shipping tag (3 1/8 x 6 1/4 in)", 3.125, 6.25), ("tag3", "#3 tag (1 7/8 x 3 3/4 in)", 1.875, 3.75)]
_pk_po = "".join(f'<option value="{k}" data-w="{w}" data-h="{h}">{e(n)}</option>' for k, n, w, h in PK_PAGES)
_pk_fo = "".join(f'<option value="{k}" data-w="{w}" data-h="{h}">{e(n)}</option>' for k, n, w, h in PK_FILL)
_pk_to = "".join(f'<option value="{k}">{e(n)}</option>' for k, n, _ in PK_TYPES)

jpkp = top("Junk journal pockets", "Six easy pockets for junk journals, each drawn so you can see how it goes together, plus a size helper that works out how big to cut a pocket for your page and the tags or cards going in it, with a template to print at actual size.", "Junk journal pockets") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the easiest junk journal pocket is a piece of card with <strong>folded flaps</strong>. Cut it 1 in (2.5 cm) wider and 1/2 in (1.3 cm) taller than you want the pocket, score 1/2 in in from each side and the bottom, fold the flaps back, trim the corners and glue the flaps (not the middle) to the page. Make the pocket about <strong>1/4 in wider</strong> than the tag or card that goes in it, and about <strong>1 in shorter</strong>, so the top peeks out and is easy to pull. No card? Fold up the bottom of a page, cut the flap end off an envelope, or tape a scrap down on three sides with washi tape.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Pocket size helper</h3>
<div class="row2"><div class="field"><label for="jpk-pg">Journal page</label><select id="jpk-pg">{_pk_po}</select></div>
<div class="field"><label for="jpk-fill">What goes in it</label><select id="jpk-fill">{_pk_fo}</select></div></div>
<div class="row2" id="jpk-cust" hidden><div class="field"><label for="jpk-w">Page width (in)</label><input type="number" id="jpk-w" value="6" min="2" max="14" step="0.125" inputmode="decimal"></div>
<div class="field"><label for="jpk-h">Page height (in)</label><input type="number" id="jpk-h" value="8" min="2" max="14" step="0.125" inputmode="decimal"></div></div>
<div class="field"><label for="jpk-t">Pocket type</label><select id="jpk-t">{_pk_to}</select></div>
<p class="sub">Sizes in inches with centimetres alongside. The template prints at actual size when you print at 100% (turn off "fit to page"). Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="jpk-out" data-env="{href("junk-journal-ephemera-ideas.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Six junk journal pockets at a glance</h2>
<div class="gq-figs">{pk_cards}</div>
<p class="sub">Pink dashed lines are folds or cut lines. Our own drawings.</p>
<h2>How to make a glue-on pocket with flaps</h2>
<ol><li><strong>Pick the size.</strong> Measure what goes in: the pocket should be about 1/4 in wider than it and about 1 in shorter. The helper above does the sums.</li>
<li><strong>Cut the card</strong> 1 in wider and 1/2 in taller than the pocket, so there's a 1/2 in flap on each side and along the bottom.</li>
<li><strong>Score and fold</strong> along the flap lines with a bone folder or the back of a butter knife and a ruler, then fold the flaps back.</li>
<li><strong>Trim the corners</strong> of the flaps at an angle so they don't overlap and make a lump.</li>
<li><strong>Glue only the flaps</strong> to the page. Glue in the middle seals the pocket shut. Press flat under a book for a few minutes.</li>
<li><strong>Decorate the top edge</strong> with a strip of washi tape, lace or a scalloped edge cut with scissors, so it doesn't tear when you pull cards out.</li></ol>
<h2>How to make a fold-up page pocket</h2>
<p>When you make your signatures, cut one page taller than the rest: the extra is the pocket. Fold the extra up against the front of the page and glue or sew down the two sides. A 3 in fold makes a pocket that holds a 3 x 4 in journaling card with a good bit showing. It's the strongest pocket because it's part of the page, so it's good for the front of a signature. If your paper isn't tall enough, glue a strip to the bottom of the page first and fold that. Planning signatures? See the <a href="{href("junk-journal-signature-calculator.html")}">junk journal signature calculator</a>.</p>
<h2>How to make an envelope pocket</h2>
<p>Cut the flap end off an envelope so it's open along the top, then glue the back of it to a page. Or keep the envelope whole and sew it in as a page with its opening at the side, which gives you a hidden pocket. Coloured security envelopes (the ones with patterns inside) and old airmail envelopes look great. A 4 3/8 x 5 3/4 in (A2) envelope fits a 3 x 4 in card either way round.</p>
<h2>How to make corner pockets</h2>
<p>Fold a square of paper in half diagonally to get a triangle, then glue it into a page corner with the fold facing inwards. Do the opposite corner the same way. Slide a photo or card in at an angle. About 2 in squares hold a 4 x 6 in photo well; make them smaller for small cards. Photo corners are the same idea, only tiny.</p>
<h2>How to make a belly band</h2>
<p>Cut a strip of paper or card about 1 1/2 in wide and twice the page width plus 1 in long. Wrap it round the page, overlap the ends at the back and glue them together (not to the page), so the band can slide. Tuck tags, cards and photos under it. Ribbon, lace or a strip of book page work too.</p>
<h2>How to make a washi tape pocket</h2>
<p>Lay a piece of paper on the page and tape down the two sides and the bottom with washi tape, leaving the top open. It takes a minute, adds no bulk, and it's the one to use in a bought notebook or a planner. Use a wide tape so it holds.</p>
<h2>What to put in a junk journal pocket</h2>
<ul><li><strong>Tags</strong> with journaling on the back. A #5 tag (2 3/8 x 4 3/4 in) is the classic size; a #8 tag needs a bigger page.</li>
<li><strong>Journaling cards</strong> (3 x 4 in) and <strong>library cards</strong> (3 x 5 in).</li>
<li><strong>Photos</strong>, tickets, receipts, letters, seed packets and other ephemera. See our list of <a href="{href("junk-journal-ephemera-ideas.html")}">62 ephemera ideas</a>.</li>
<li><strong>Tuck spots</strong> for later: a blank card to write on when you have something to say.</li></ul>
<h2>Tips for pockets that last</h2>
<ul><li><strong>Use thicker paper</strong> for the pocket than for the page: card, cereal box card covered in paper, or a doubled sheet.</li>
<li><strong>Don't fill every page</strong> with pockets: they make the spine bulge. Leave a gap in the binding or use a wider spine.</li>
<li><strong>Strong glue or stitches</strong> on the sides: a glue stick lifts with use. Double-sided tape, PVA or a machine zigzag holds.</li>
<li><strong>Tea-stain</strong> new white card so it matches old pages: see <a href="{href("how-to-tea-stain-paper.html")}">how to tea stain paper</a>.</li></ul>
<p>New to all of this? Start with <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a> and the <a href="{href("junk-journal-supply-checklist.html")}">supply checklist</a> (it has a free pocket and tag template too). Stuck for words? Try the <a href="{href("journal-prompts.html")}">journal prompt generator</a>.</p>
<p>Something to tuck in your pockets: <a href="{href("junk-journal-tags.html")}">how to make junk journal tags</a>, with a free printable tag template maker that checks the tag fits your pocket.</p>
<p class="note">Pocket methods are standard paper-craft techniques, shown in similar ways by The Graphics Fairy, Archer &amp; Olive, Splitcoast Stampers and 101 Planners (checked 27 Nov 2026). Tag and envelope sizes are the usual US stationery sizes. Our wording, drawings and size rules (pocket 1/4 in wider and about 1 in shorter than its contents).</p>
</div></div></section>'''
jpk_faq = [
    ("How do you make a pocket in a junk journal?", "Cut card 1 in wider and 1/2 in taller than the pocket, fold back 1/2 in flaps on the sides and bottom, trim the corners and glue only the flaps to the page."),
    ("How big should a junk journal pocket be?", "About 1/4 in wider than the tag or card going in, and about 1 in shorter so the top peeks out. For a 3 x 4 in journaling card that's a 3 1/4 x 3 in pocket."),
    ("What size tag fits in a junk journal pocket?", "A #5 shipping tag (2 3/8 x 4 3/4 in) suits A5 and half letter pages. Use #3 tags for small journals and #8 tags for 6 x 9 in or larger pages."),
    ("What can I use to make junk journal pockets?", "Card, envelopes, old book covers, paper bags, file folders, cereal box card covered with paper, lace, fabric or a scrap of paper and washi tape."),
    ("How do you make a hidden pocket in a junk journal?", "Glue two pages together along three edges and leave one side open, or sew a whole envelope in as a page with its opening at the side."),
    ("What glue is best for junk journal pockets?", "Double-sided tape or PVA glue on the flaps. Glue sticks are fine for light pockets but can lift when cards go in and out a lot."),
]
SHOP_FOR["junk-journal-pockets.html"] = ["junk-journal-mega-bundle", "journaling-cards-3x4", "vintage-ephemera-pack", "night-garden-junk-journal-kit"]
page("junk-journal-pockets.html", "Junk Journal Pockets: 6 Easy Pockets + Size Helper",
     "How to make junk journal pockets: six easy pockets with our own drawings, plus a size helper and a free template that prints at actual size for your page.",
     jpkp, jpk_faq, "Junk journal pockets", app_name="Junk journal pocket size helper")

# ======== 2027 GOAL PLANNER PRINTABLE ========
# Demand: 'printable year planner 2027', '2027 goal planner printable free', 'new year goal setting worksheet 2027' (SERP 27 Nov: spam mirror
# sites, WeAreTeachers goals tracker, Day Designer blog, paid pages on Stan, Design Bundles, Getly). Seasonal: New Year. Wording ours.

gplp = top("Free 2027 goal planner printable", "Fill in your goals for 2027 on screen, or leave it blank to write by hand, then print it or save it as a PDF. Two pages: your goals with the first steps and quarterly milestones, and a monthly check-in for the whole year.", "2027 goal planner printable") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> this free 2027 goal planner prints on <strong>US Letter or A4</strong>. Page 1 holds a word of the year, up to <strong>4 goals</strong> (each with why it matters, a first step, a deadline and a milestone for every quarter) and 3 habits. Page 2 is a <strong>monthly check-in</strong>: a box for each month with a tick for each goal, a win and next month's focus. Type in the boxes below and press print, or clear it and print a blank copy. Nothing is sent anywhere; it's saved on your device only.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet" id="gpl-form">
<h3 style="margin-top:0">Your 2027 goals</h3>
<div class="row2"><div class="field"><label for="gpl-name">Name (optional)</label><input type="text" id="gpl-name" maxlength="40" autocomplete="off"></div>
<div class="field"><label for="gpl-word">Word of the year</label><input type="text" id="gpl-word" maxlength="24" placeholder="e.g. finish" autocomplete="off"></div></div>
<div class="row2"><div class="field"><label for="gpl-theme">Extra box</label><select id="gpl-theme"><option value="none">None</option><option value="craft">Makes and skills for 2027</option><option value="biz">Shop and sales goals</option><option value="read">Books to read</option></select></div>
<div class="field"><span class="label" id="gpl-paper-l">Paper</span><div class="seg" role="group" aria-labelledby="gpl-paper-l" id="gpl-paper"><button type="button" data-v="letter" aria-pressed="true">US Letter</button><button type="button" data-v="a4" aria-pressed="false">A4</button></div></div></div>
{"".join(f"""<fieldset class="gpl-g"><legend>Goal {i}</legend>
<div class="field"><label for="gpl-g{i}">Goal</label><input type="text" id="gpl-g{i}" maxlength="70" autocomplete="off"></div>
<div class="row2"><div class="field"><label for="gpl-y{i}">Why it matters</label><input type="text" id="gpl-y{i}" maxlength="70" autocomplete="off"></div>
<div class="field"><label for="gpl-s{i}">First step</label><input type="text" id="gpl-s{i}" maxlength="70" autocomplete="off"></div></div>
<div class="field"><label for="gpl-d{i}">Done by</label><select id="gpl-d{i}"><option value="">Leave blank</option>{"".join(f'<option>{m} 2027</option>' for m in ("January","February","March","April","May","June","July","August","September","October","November","December"))}</select></div></fieldset>""" for i in range(1, 5))}
<div class="row2"><div class="field"><label for="gpl-h1">Habit 1</label><input type="text" id="gpl-h1" maxlength="40" autocomplete="off"></div>
<div class="field"><label for="gpl-h2">Habit 2</label><input type="text" id="gpl-h2" maxlength="40" autocomplete="off"></div></div>
<div class="field"><label for="gpl-h3">Habit 3</label><input type="text" id="gpl-h3" maxlength="40" autocomplete="off"></div>
<div class="btns"><button type="button" class="btn" id="gpl-print">Print or save as PDF</button> <button type="button" class="btn ghost" id="gpl-clear">Clear for a blank copy</button></div>
<p class="sub">To save a PDF, choose "Save as PDF" as the printer. Two pages.</p>
</div><div class="result" aria-live="polite"><h2>Preview</h2><div id="gpl-out" class="pjp-paper"></div></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How to use a goal planner so it actually works</h2>
<ol><li><strong>Pick fewer goals.</strong> Three or four is plenty for a year. If you have ten, choose the ones you'd be most pleased to have done by December and park the rest.</li>
<li><strong>Make each one checkable.</strong> "Knit more" is a wish; "knit 4 sweaters" or "finish the granny square blanket by June" is a goal you can tick off. Put a number or a finished thing in it, and a date.</li>
<li><strong>Write why.</strong> A short reason keeps you going in March, when the shine has worn off.</li>
<li><strong>Write the very first step.</strong> Something you could do this week: buy the yarn, book the class, open the shop account.</li>
<li><strong>Split it into quarters.</strong> One milestone for each three months turns a big goal into four small ones. The planner gives each goal a Q1 to Q4 line.</li>
<li><strong>Check in every month.</strong> Ten minutes at the end of each month: tick the goals you moved forward, write one win and choose next month's focus. Page 2 is for that.</li></ol>
<h2>Goal ideas for crafters</h2>
<ul><li>Finish three works in progress before starting anything new.</li>
<li>Learn one new technique each quarter: cables, colourwork, the <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>, <a href="{href("how-to-cross-stitch.html")}">cross stitch</a>.</li>
<li>Make a temperature blanket: plan it with the <a href="{href("temperature-blanket-planner.html")}">temperature blanket planner</a>.</li>
<li>Knit or crochet all your Christmas gifts, planned from January with the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>.</li>
<li>Fill one junk journal: start with <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a>.</li>
<li>Use up your stash before buying more yarn.</li>
<li>Open a shop or do your first craft fair: the <a href="{href("craft-fair-checklist.html")}">craft fair checklist</a> and <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a> help.</li></ul>
<h2>Word of the year ideas</h2>
<p>A word of the year is one word that sums up how you want the year to feel, and it's handy when you're choosing between two things. A few to start from: finish, slow, brave, make, simple, learn, rest, share, grow, focus, enough, begin.</p>
<h2>More printables for 2027</h2>
<p>Print the dates too with the free <a href="{href("2027-calendar-printable.html")}">2027 calendar</a> (whole year or a page a month, with US or UK holidays). For your projects, there's the <a href="{href("crochet-project-planner.html")}">crochet project planner</a>, and <a href="{href("journal-prompts.html")}">journal prompts</a> for New Year reflection.</p>
<p class="note">Our own planner layout and wording. Goal tips are general advice, not a method from any one source.</p>
</div></div></section>'''
gpl_faq = [
    ("Is this 2027 goal planner free?", "Yes. Fill it in on screen or leave it blank, then print it or save it as a PDF. Nothing to sign up for, and your goals stay on your device."),
    ("What size does the goal planner print?", "US Letter or A4, two pages: your goals on page 1 and a monthly check-in on page 2. Pick the paper above before printing."),
    ("How many goals should I set for the year?", "Three or four is a good number. Fewer goals get more attention, and you can add new ones at a mid-year check-in."),
    ("How do I write a goal I'll stick to?", "Make it checkable with a number or finished thing and a date, write why it matters, and write the first step you can take this week."),
    ("What is a word of the year?", "One word that sums up how you want the year to go, like finish, slow or brave. It helps when you're deciding what to say yes to."),
    ("How do I save the planner as a PDF?", "Press Print, then choose Save as PDF (or Microsoft Print to PDF) as the printer."),
]
SHOP_FOR["2027-goal-planner-printable.html"] = ["2027-habit-tracker-spreadsheet", "debt-payoff-planner-spreadsheet", "december-days-journal-kit", "christmas-gift-planner-budget"]
page("2027-goal-planner-printable.html", "Free 2027 Goal Planner Printable (Fill In, Then Print)",
     "Free 2027 goal planner printable: fill in up to 4 goals with first steps and quarterly milestones, plus a monthly check-in. Letter or A4, print or save as PDF.",
     gplp, gpl_faq, "2027 goal planner printable", app_name="2027 goal planner printable")

# ======== HOW TO BLOCK KNITTING AND CROCHET ========
# Demand: 'how to block knitting', 'how to block crochet', 'how to block acrylic yarn' (SERP 27 Nov: DMC, LoveCrafts US+UK, Gathered x2,
# Wool Warehouse, Purl Soho, Annie's x2, Dummies wet blocking, A Crocheted Simplicity acrylic, Mary Maxim acrylic, Herrschners, Yarnspirations video).

def _bk_svg(kind, label):
    if kind == "soak":
        s = ('<path d="M50 70 L230 70 L214 170 L66 170 Z" fill="#dbe9e8" stroke="#1f2a44" stroke-width="2"/>'
             '<path d="M58 96 Q78 88 98 96 T138 96 T178 96 T222 96" fill="none" stroke="#2f8f8a" stroke-width="2"/>'
             '<path d="M96 118 Q140 104 184 122 Q170 150 112 148 Z" fill="#f4c6d4" stroke="#b8326a" stroke-width="1.8"/>'
             f'<text x="140" y="56" {_T11} text-anchor="middle">lukewarm water + wool wash, 15-30 min</text>')
    elif kind == "towel":
        s = ('<rect x="30" y="80" width="220" height="56" rx="28" fill="#f2e2b8" stroke="#1f2a44" stroke-width="2"/>'
             '<path d="M58 80 C58 108 58 108 58 136 M98 80 C98 108 98 108 98 136 M138 80 C138 108 138 108 138 136 M178 80 C178 108 178 108 178 136 M218 80 C218 108 218 108 218 136" stroke="#c9a85c" stroke-width="1.6" fill="none"/>'
             '<path d="M120 40 L120 70 M110 60 L120 72 L130 60 M160 40 L160 70 M150 60 L160 72 L170 60" stroke="#e39a14" stroke-width="2.6" fill="none"/>'
             f'<text x="140" y="164" {_T11} text-anchor="middle">roll in a towel and press: never wring</text>')
    elif kind == "pin":
        grid = "".join(f'<line x1="{x}" y1="30" x2="{x}" y2="170" stroke="#c4cbe0" stroke-width="1"/>' for x in range(40, 250, 20)) + "".join(f'<line x1="30" y1="{y}" x2="250" y2="{y}" stroke="#c4cbe0" stroke-width="1"/>' for y in range(40, 170, 20))
        pins = "".join(f'<g><line x1="{x}" y1="{y}" x2="{x + 6}" y2="{y - 8}" stroke="#1f2a44" stroke-width="1.6"/><circle cx="{x + 7}" cy="{y - 9}" r="3.2" fill="#b8326a"/></g>' for x, y in
                       [(70, 60), (110, 60), (150, 60), (190, 60), (210, 80), (210, 110), (210, 140), (70, 150), (110, 150), (150, 150), (190, 150), (70, 90), (70, 120)])
        s = ('<rect x="30" y="30" width="220" height="140" rx="4" fill="#e7ebf5" stroke="#9aa6c4" stroke-width="2"/>' + grid +
             '<path d="M70 60 Q90 66 110 60 Q130 66 150 60 Q170 66 190 60 Q206 64 210 80 L210 140 Q206 152 190 150 Q170 144 150 150 Q130 144 110 150 Q90 144 70 150 L70 60 Z" fill="#f4c6d4" stroke="#b8326a" stroke-width="1.8"/>' + pins)
    elif kind == "steam":
        s = ('<rect x="30" y="140" width="220" height="24" rx="4" fill="#e7ebf5" stroke="#9aa6c4" stroke-width="2"/><rect x="60" y="128" width="160" height="14" rx="3" fill="#cfe3e1" stroke="#2f8f8a" stroke-width="1.6"/>'
             '<path d="M90 70 Q96 40 150 40 L200 40 Q210 40 206 70 Z" fill="#1f2a44"/><path d="M84 70 L212 70 L212 80 L84 80 Z" fill="#9aa6c4" stroke="#1f2a44" stroke-width="1.6"/>'
             '<path d="M110 86 q6 10 0 20 t0 20 M140 86 q6 10 0 20 t0 20 M170 86 q6 10 0 20 t0 20" fill="none" stroke="#9aa6c4" stroke-width="2" stroke-linecap="round"/>'
             '<line x1="236" y1="80" x2="236" y2="126" stroke="#e39a14" stroke-width="2"/><path d="M231 86 L236 78 L241 86 M231 120 L236 128 L241 120" fill="none" stroke="#e39a14" stroke-width="2"/>'
             f'<text x="140" y="26" {_T11} text-anchor="middle">hover about 1 in above: don\'t touch</text>')
    else:  # spray
        s = ('<rect x="30" y="140" width="220" height="24" rx="4" fill="#e7ebf5" stroke="#9aa6c4" stroke-width="2"/><rect x="40" y="126" width="150" height="16" rx="3" fill="#f4c6d4" stroke="#b8326a" stroke-width="1.6"/>'
             '<rect x="196" y="62" width="34" height="62" rx="8" fill="#2f8f8a" stroke="#1f2a44" stroke-width="1.8"/><path d="M204 62 L204 46 L184 46 L178 52 L204 52" fill="#1f2a44" stroke="#1f2a44" stroke-width="2"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#2f8f8a" opacity=".7"/>' for x, y in [(170, 60), (160, 72), (150, 84), (164, 88), (140, 96), (152, 104), (128, 108), (140, 114), (116, 116), (172, 76)]) +
             f'<text x="110" y="40" {_T11} text-anchor="middle">pin dry, then mist until damp</text>')
    return f'<svg viewBox="0 0 280 180" role="img" aria-label="{e(label)}"><rect width="280" height="180" rx="10" fill="#f6f1e6"/>{s}</svg>'

BK_STEPS = [("soak", "1. Soak", "Wet blocking: soak the piece until the water goes right through it."),
            ("towel", "2. Squeeze out", "Press the water out in a rolled towel. Wringing stretches and felts it."),
            ("pin", "3. Pin to size", "Lay it flat on a mat and pin it to the measurements. Leave it until bone dry."),
            ("steam", "Steam blocking", "Pin dry, then hold a steam iron just above it. Best for acrylic and cotton."),
            ("spray", "Spray blocking", "Pin dry, mist with water until damp and leave to dry. Gentle and quick.")]
bk_cards = "".join(f'<figure class="gq-fig"><div>{_bk_svg(k, n + ": " + d)}<figcaption><strong>{e(n)}.</strong> {e(d)}</figcaption></div></figure>' for k, n, d in BK_STEPS)

bkp = top("How to block knitting and crochet", "Blocking is the last step that makes a finished piece look finished: stitches even out, edges straighten and lace opens up. Here are wet, steam and spray blocking with our own drawings, and a helper that picks the method for your yarn and works out the mats and pins you need.", "How to block knitting and crochet") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to block knitting or crochet, <strong>wet it, shape it and let it dry</strong>. For <strong>wool and most natural fibres</strong>, soak the piece in lukewarm water with a little wool wash for 15 to 30 minutes, press the water out in a towel (don't wring), lay it flat on blocking mats or towels, pin it to the measurements and leave it until completely dry, usually a day or two. <strong>Acrylic</strong> doesn't hold a new shape from water, so pin it dry and <strong>steam block</strong> it: hold a steam iron just above it, never touching. For a light tidy-up, pin it out and <strong>spray</strong> it with water.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">Blocking helper</h3>
<div class="row2"><div class="field"><label for="blk-f">Yarn</label><select id="blk-f"><option value="wool">Wool, alpaca, merino (not superwash)</option><option value="sw">Superwash wool</option><option value="acr">Acrylic</option><option value="blend">Wool and acrylic blend</option><option value="cot">Cotton, linen, bamboo</option><option value="moh">Mohair, silk or lace-weight blends</option></select></div>
<div class="field"><label for="blk-i">What you made</label><select id="blk-i"><option value="lace">Lace shawl or doily</option><option value="sweater">Sweater or cardigan</option><option value="squares">Granny squares or motifs</option><option value="blanket">Blanket</option><option value="scarf">Scarf or wrap</option><option value="hat">Hat, socks or mittens</option><option value="toy">Amigurumi or toy</option><option value="swatch">Gauge swatch</option></select></div></div>
<div class="row2"><div class="field"><label for="blk-w">Finished width</label><input type="number" id="blk-w" value="20" min="1" max="400" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="blk-h">Finished length</label><input type="number" id="blk-h" value="60" min="1" max="400" step="0.5" inputmode="decimal"></div></div>
<div class="field"><span class="label" id="blk-u-l">Units</span><div class="seg" role="group" aria-labelledby="blk-u-l" id="blk-u"><button type="button" data-v="in" aria-pressed="true">Inches</button><button type="button" data-v="cm" aria-pressed="false">Centimetres</button></div></div>
<p class="sub">Enter the size you want it to block to (the pattern's finished measurements). It works out how many 12 in (30 cm) interlocking mat tiles cover it and about how many pins. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="blk-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Blocking methods at a glance</h2>
<div class="gq-figs">{bk_cards}</div>
<h2>What is blocking, and do I need to do it?</h2>
<p>Blocking means getting a finished piece wet (or steamed), shaping it and letting it dry in that shape. It evens out wobbly stitches, flattens curling edges, makes pieces the right size to sew together and opens up lace so the pattern shows. Lace and colourwork really need it. Sweaters, shawls, granny squares and anything you'll seam look much better for it. Toys, dishcloths and chunky hats often don't need it at all.</p>
<h2>What you need</h2>
<ul><li><strong>Something flat to pin into:</strong> interlocking foam blocking mats (often sold as 12 in tiles), a spare bed, or folded towels on a carpet.</li>
<li><strong>Rust-proof pins:</strong> T-pins or blocking pins with combs. Ordinary pins can rust and mark the yarn.</li>
<li><strong>Blocking wires</strong> for lace and long straight edges (optional, but they save a lot of pins).</li>
<li><strong>A tape measure</strong>, the pattern's measurements, a basin and a gentle wool wash (no-rinse kinds are easiest).</li>
<li><strong>A steam iron or steamer</strong> if you're steam blocking.</li></ul>
<h2>How to wet block, step by step</h2>
<ol><li><strong>Soak:</strong> fill a basin with lukewarm water and a little wool wash. Push the piece under and leave it 15 to 30 minutes so the water gets right into the fibres. Don't agitate wool: rubbing plus warm water felts it.</li>
<li><strong>Squeeze out:</strong> lift it out supported in both hands (wet knitting stretches under its own weight), press out the water, then roll it up in a towel and press or stand on it.</li>
<li><strong>Shape:</strong> lay it on the mats and pat it into shape, measuring as you go. Pin the corners and centres first, then fill in, every 1 to 2 in on edges (closer for lace points).</li>
<li><strong>Dry:</strong> leave it until it's completely dry, usually 24 to 48 hours. A fan speeds it up. Unpin too early and it springs back.</li></ol>
<h2>How to steam block</h2>
<p>Pin the piece out dry to its measurements, then hold a steam iron or a garment steamer about 1 in above it and let the steam soak in. <strong>Don't press down or touch the yarn</strong>, especially acrylic, which melts and goes flat and shiny. Pat it into shape with your hand if needed (careful, it's hot) and leave it pinned until it's cool and dry, about half an hour. Steam is quick and suits acrylic, cotton and wool; skip it on mohair halos and textured stitches you don't want flattened, like cables and bobbles, unless you hold the steam well above.</p>
<h2>How to spray block</h2>
<p>Pin the piece out dry, then mist it with a spray bottle until it's evenly damp, and leave it to dry. It's the gentlest method and the one to use for granny squares, a quick tidy-up or delicate yarn you don't want to soak.</p>
<h2>How to block acrylic yarn</h2>
<p>Acrylic is plastic, so water alone doesn't reset it: wet blocking only tidies it until the next wash. Heat does reset it. Steam blocking acrylic softens it and makes it drape, and the change is permanent, which is why it's called <strong>killing acrylic</strong>. A little steam is enough for most projects; a lot makes lace drapey and flat. Always keep the iron off the yarn and try it on your swatch first.</p>
<h2>Blocking superwash wool</h2>
<p>Superwash wool is treated so it won't felt, but it can <strong>grow a lot when wet</strong>. Soak it, squeeze it out well, then lay it flat and push it back to size rather than stretching it. Never hang it to dry. If your swatch grew in blocking, measure gauge on the blocked swatch, not the unblocked one.</p>
<h2>How to block granny squares</h2>
<p>Draw or print a square of the right size on a mat (or use a grid mat), pin each square to it at the corners and middles, spray, and leave to dry. Blocking a batch to the same size makes joining much easier: see <a href="{href("how-to-join-granny-squares.html")}">how to join granny squares</a>. A blanket can also be blocked after joining, in sections on a bed.</p>
<h2>Blocking a gauge swatch</h2>
<p>Always block your swatch the same way you'll block the finished piece, then measure. Many yarns change size when blocked, and a swatch measured before blocking can give you a sweater a size too big or small. Then turn your gauge into stitches with the <a href="{href("gauge-converter.html")}">gauge converter</a>.</p>
<p>Before you block, finish the ends: see <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a> (trim the tails after blocking, so they don't pop out). Knitting a sweater? Get the size right first with the <a href="{href("sweater-size-calculator.html")}">sweater size calculator</a>.</p>
<p class="note">Blocking methods as taught by established craft sources: LoveCrafts, Gathered, DMC, Purl Soho, Annie's, Wool Warehouse and Crocheting For Dummies, with acrylic steam blocking as described by Mary Maxim, Herrschners and Yarnspirations (checked 27 Nov 2026). Our wording and drawings. Pin and mat counts are our estimates.</p>
</div></div></section>'''
bk_faq = [
    ("How do you block knitting?", "Soak it in lukewarm water with wool wash for 15 to 30 minutes, press the water out in a towel, pin it flat to the pattern measurements and leave it until completely dry."),
    ("How do you block crochet?", "The same way as knitting: wet block wool and cotton, steam block acrylic, or pin it out dry and spray it with water for a quick tidy-up."),
    ("Can you block acrylic yarn?", "Yes, with steam. Pin it dry and hold a steam iron just above it without touching. The heat sets the new shape permanently, so test on a swatch first."),
    ("How long does blocking take to dry?", "Wet blocking usually takes 24 to 48 hours, depending on the yarn and the room. Spray blocking dries in a few hours and steam blocking in about half an hour."),
    ("Do I need blocking mats?", "No. A spare bed, a carpet covered with towels, or an ironing board for small pieces all work. Mats just make pinning and measuring easier."),
    ("Should you block before or after seaming?", "Before, for sweaters: blocked pieces are flat and easier to sew. A quick block after seaming then evens out the seams."),
    ("Do you have to block amigurumi?", "No, toys usually aren't blocked. A little steam can smooth a lumpy shape or flatten ears, held well above the toy."),
]
SHOP_FOR["how-to-block-knitting-crochet.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("how-to-block-knitting-crochet.html", "How to Block Knitting and Crochet (Wet, Steam, Spray)",
     "How to block knitting and crochet: wet, steam and spray blocking with our own drawings, acrylic and superwash tips, and a helper for method, mats and pins.",
     bkp, bk_faq, "How to block knitting and crochet", app_name="Blocking method, mats and pins helper")
