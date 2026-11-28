# ---------------- 28 Nov 2026 competitor watch quick win: SLEEVE DECREASE CALCULATOR (shaping spread over rows) ----------------
# Executed from build.py after plan19.py (shares page(), top(), href(), e(), SHOP_FOR).
# Demand: COMPETITOR WATCH 28 Nov (DEMAND.md): stitchmath, pyknit, kcguild, everycalculators all have a "decrease over rows"
# calculator; ours only spread shaping across one row. Pure arithmetic, wording and examples our own. JS in assets/app.js (sd-*).

sd_faq = [
    ("How do I calculate sleeve decreases?", "Take the stitches you have away from the stitches you need, then divide by 2 (one decrease at each end of a shaping row). That's how many shaping rows you need. Divide the rows you have by that number to get the gap. 80 down to 56 stitches is 12 shaping rows; over 96 rows that's a decrease row every 8th row, 12 times."),
    ("What if the rows don't divide evenly?", "Use two gaps one row apart. 12 shaping rows over 90 rows is 7.5, so work 6 shaping rows every 7th row and 6 every 8th row (42 + 48 = 90 rows)."),
    ("Why should knitting decreases go on right-side rows?", "Decreases like k2tog and ssk are easiest to work and look neatest on knit (right-side) rows, so most patterns keep the gaps to even numbers: every 4th, 6th or 8th row. The calculator does this when 'Right-side rows only' is ticked."),
    ("How many rows do I have for a sleeve?", "Multiply the length you want to shape over by your row gauge. 16 in of sleeve at 28 rows per 4 in is 16 ÷ 4 × 28 = 112 rows. Leave a few plain rows at the cuff and below the underarm so the shaping doesn't start or end right at an edge."),
    ("Does this work for increasing a bottom-up sleeve?", "Yes. The spacing is the same maths: pick Increase, enter the cuff stitches and the upper arm stitches, and the rows between them."),
]

sd = top("Sleeve decrease calculator", "Need to take a sleeve from the upper arm down to the cuff, or shape a side seam? Enter the stitches you start and end with and the rows you have. You get a line like \"decrease every 6th row 8 times, then every 8th row 2 times\" and a row-by-row list to tick off.", "Sleeve decrease calculator") + f'''
<section style="padding-top:10px"><div class="wrap tool">
<div class="sheet">
<div class="field"><span class="label" id="sd-craft-l">Knitting or crochet?</span><div class="seg" role="group" aria-labelledby="sd-craft-l" id="sd-craft"><button type="button" data-v="knit" aria-pressed="true">Knitting</button><button type="button" data-v="crochet" aria-pressed="false">Crochet</button></div></div>
<div class="field"><span class="label" id="sd-dir-l">Shaping</span><div class="seg" role="group" aria-labelledby="sd-dir-l" id="sd-dir"><button type="button" data-v="dec" aria-pressed="true">Decrease (top-down sleeve)</button><button type="button" data-v="inc" aria-pressed="false">Increase (bottom-up sleeve)</button></div></div>
<div class="row2"><div class="field"><label for="sd-s">Stitches you start with</label><input type="number" id="sd-s" value="80" min="2" max="2000" inputmode="numeric"></div>
<div class="field"><label for="sd-e">Stitches you want to end with</label><input type="number" id="sd-e" value="56" min="1" max="2000" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="sd-k">Stitches shaped per shaping row</label><select id="sd-k"><option value="2" selected>2 (one at each end, or each side of a marker)</option><option value="1">1 (one edge only)</option><option value="4">4 (two pairs, e.g. both sides of 2 markers)</option></select></div>
<div class="field"><label for="sd-r">Rows (or rounds) to shape over</label><input type="number" id="sd-r" value="96" min="1" max="3000" inputmode="numeric"><span class="note">Don't know? Fill in the two boxes below.</span></div></div>
<div class="row2"><div class="field"><label for="sd-len">Length to shape over (optional)</label><input type="number" id="sd-len" placeholder="e.g. 14" min="0" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="sd-rg">Rows per 4 in / 10 cm in your swatch</label><input type="number" id="sd-rg" placeholder="e.g. 28" min="1" step="0.5" inputmode="decimal"><span class="note">Length and swatch in the same unit (in with 4 in, cm with 10 cm).</span></div></div>
<div class="field"><span class="label" id="sd-u-l">Length unit</span><div class="seg" role="group" aria-labelledby="sd-u-l" id="sd-u"><button type="button" data-v="in" aria-pressed="true">inches</button><button type="button" data-v="cm" aria-pressed="false">cm</button></div></div>
<label class="switch" id="sd-rs-f"><input type="checkbox" id="sd-rs" checked> Right-side rows only (even gaps: every 2nd, 4th, 6th row...)</label>
</div>
<div class="result" aria-live="polite" id="sd-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<div class="quick"><strong>Quick answer:</strong> shaping rows = (start stitches − end stitches) ÷ stitches shaped per row; gap = rows ÷ shaping rows. For 80 down to 56 stitches with a decrease at each end, that's 24 ÷ 2 = <strong>12 shaping rows</strong>. Over 96 rows the gap is 96 ÷ 12 = 8, so <strong>decrease at each end of every 8th row, 12 times</strong>. If it doesn't divide exactly, split the shaping into two gaps one (or two) rows apart.</div>
<h2>How do you work out sleeve decreases?</h2>
<ol><li><strong>Count the stitches to lose.</strong> Upper arm stitches minus cuff stitches. 80 − 56 = 24.</li>
<li><strong>Count the shaping rows.</strong> A sleeve usually loses one stitch at each edge on a shaping row, so 2 per row: 24 ÷ 2 = 12 shaping rows.</li>
<li><strong>Count the rows you have.</strong> Sleeve length you're shaping over × row gauge. 13.7 in at 28 rows per 4 in is about 96 rows.</li>
<li><strong>Divide.</strong> 96 ÷ 12 = 8: one shaping row every 8th row.</li>
<li><strong>If it isn't a whole number</strong>, use the two nearest gaps. 90 ÷ 12 = 7.5, so 6 shaping rows every 7th row and 6 every 8th row. Working flat in knitting, keep the gaps even (6 and 8) so every decrease falls on a right-side row.</li></ol>
<h2>Which decreases should I use on a sleeve?</h2>
<p>In knitting, a neat pair is <strong>k1, ssk</strong> at the start of the row and <strong>k2tog, k1</strong> at the end: they lean in with the edge and leave a clean stitch for seaming. In crochet, a <strong>sc2tog</strong> or <strong>dc2tog</strong> one stitch in from each end does the same job. See <a href="{href("how-to-crochet-decrease.html")}">how to decrease in crochet</a> for the invisible decrease.</p>
<h2>Faster shaping first, or slower?</h2>
<p>Both are fine for a plain sleeve. Many knitters put the shorter gaps near the upper arm (top-down) so the sleeve narrows quickly below the elbow area and runs straighter into the cuff. Our list puts the shorter gaps first; if you'd rather have them the other way round, work the two parts in reverse order. The total rows stay the same.</p>
<h2>Plain rows at each end</h2>
<p>Most sleeves have a few plain rows below the underarm and above the cuff, so leave those out of the rows you enter. For example, of 110 rows, keep 6 plain at the top and 8 above the ribbing and enter 96.</p>
<p>What next? Spread stitches across one row with the <a href="{href("increase-decrease-calculator.html")}">increase and decrease evenly calculator</a>, find your size with the <a href="{href("sweater-size-calculator.html")}">sweater size calculator</a>, check your row gauge with the <a href="{href("gauge-converter.html")}">gauge converter</a>, and keep track of the shaping rows with the <a href="{href("row-counter.html")}">row counter</a>: the button above adds a counter set to your gap.</p>
</div></section>'''

page("sleeve-decrease-calculator.html", "Sleeve Decrease Calculator: Shaping Over Rows",
     "Free sleeve decrease calculator for knitting and crochet: enter start and end stitches and rows, get 'decrease every 6th row 8 times, then every 8th row 2 times'.",
     sd, sd_faq, "Sleeve decrease calculator", app_name="Sleeve decrease calculator")
