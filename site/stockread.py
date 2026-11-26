# ---------------- 26 Nov 2026 run 4: CHRISTMAS STOCKING CALCULATOR + HOW TO READ CROCHET PATTERNS ----------------
# Executed from build.py after fairstitch.py (shares page(), top(), href(), e(), SHOP_FOR, more_crafts()).
# Demand evidence in DEMAND.md (RADAR 26 Nov run 4). Drawings are our own SVG; wording our own. JS in assets/app.js.

# ======== CHRISTMAS STOCKING SIZE + YARN CALCULATOR ========
# Sizes: typical shop stockings (Northlight and New Traditions 20 in, Coolmade 26 in "extra long", Pottery Barn Kids / L.L.Bean
# heirloom knit stockings around 19-20 in) and pattern size ranges (Dora Does chunky stocking in 3 sizes, Ravelry "mini" and
# "extra-large" stockings). Gauge defaults: Craft Yarn Council standard gauge ranges (mid values). Yardage = our own area model,
# the same yd-per-square-inch figures as the blanket and C2C calculators (0.667 yd/sq in plain worsted knitting, crochet x1.27).
STK = [  # key, name, use, height in (cuff top to heel), flat width in, foot length in (heel to toe), cuff depth in
    ("mini", "Mini", "Tree ornament, advent calendar, gift card holder", 7, 3.5, 4.5, 1.5),
    ("small", "Small", "Child, pet or a row of stockings on a narrow mantel", 12, 5, 7, 2.5),
    ("standard", "Standard", "The classic family stocking", 18, 7, 10, 3.5),
    ("large", "Large", "Room for bigger gifts", 22, 8, 12, 4),
    ("xl", "Extra long", "Statement stocking, the 26 in shop size", 26, 9, 14, 5),
]
STK_KG = {3: 22, 4: 18, 5: 14, 6: 9}    # knit stockinette st per 4 in (CYC mid values)
STK_CG = {3: 15, 4: 13, 5: 10, 6: 8}    # crochet sc per 4 in (CYC mid values)
STK_M = {3: 1.18, 4: 1.0, 5: 0.72, 6: 0.52}
STK_NM = {3: "DK", 4: "worsted", 5: "bulky", 6: "super bulky"}

def stk_area(h, w, f, c, folded=True):
    flat = w * max(h - w, 0) + f * w          # leg + foot, one side
    return 2 * flat + (2 * w * c if folded else 0)

def stk_yd(h, w, f, c, wt=4, craft="knit", folded=True):
    return stk_area(h, w, f, c, folded) * 0.667 * STK_M[wt] * (1.27 if craft == "crochet" else 1) * 1.1

def stk_rng(y):
    lo, hi = y * 0.85, y * 1.15
    r = 5 if y < 120 else 10
    return f"{int(round(lo / r) * r):,}–{int(round(hi / r) * r):,}"

def stk_co(w, wt):
    return int(round(2 * w * STK_KG[wt] / 4 / 4) * 4)

_std = next(s for s in STK if s[0] == "standard")
_std_k = stk_yd(*_std[3:7], 4, "knit"); _std_c = stk_yd(*_std[3:7], 4, "crochet"); _std_b = stk_yd(*_std[3:7], 5, "knit")
stk_rows = "".join(
    f'<tr><td><strong>{n}</strong><br><span class="muted">{e(u)}</span></td><td>{h} in ({round(h * 2.54)} cm)</td><td>{w} in</td><td>{f} in</td>'
    f'<td>{stk_rng(stk_yd(h, w, f, c, 4, "knit"))} yd</td><td>{stk_rng(stk_yd(h, w, f, c, 4, "crochet"))} yd</td><td>{stk_rng(stk_yd(h, w, f, c, 5, "knit"))} yd</td></tr>'
    for k, n, u, h, w, f, c in STK)
stk_co_rows = "".join(f'<tr><td>{n}</td>' + "".join(f'<td>{stk_co(w, wt)}</td>' for wt in (3, 4, 5, 6)) + "</tr>" for k, n, u, h, w, f, c in STK)

def stk_svg():
    # our own drawing: a stocking outline with the three measurements
    s = '<rect width="320" height="300" rx="14" fill="#f3ede2"/>'
    s += '<path d="M96 70 L96 178 Q96 214 128 226 L236 252 Q266 258 270 232 Q274 206 246 196 L176 176 L176 70 Z" fill="#b8326a"/>'
    s += '<path d="M150 200 Q160 228 128 226" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="4 4" opacity=".7"/>'
    s += '<path d="M236 252 Q266 258 270 232 Q274 206 246 196 L232 192 Q244 222 236 252Z" fill="#2f8f8a"/>'
    s += '<path d="M118 226 Q100 214 98 196 Q120 204 134 228Z" fill="#2f8f8a"/>'
    s += '<rect x="88" y="34" width="96" height="40" rx="6" fill="#f7f3ea" stroke="#1f2a44" stroke-width="2"/>'
    for i in range(7):
        s += f'<path d="M{96 + i * 13} 40 v28" stroke="#d6cbb6" stroke-width="2"/>'
    s += '<path d="M178 40 q14 -14 6 -28" fill="none" stroke="#1f2a44" stroke-width="2.4"/>'
    s += '<g stroke="#1f2a44" stroke-width="1.6" fill="none"><path d="M60 34 V226"/><path d="M54 34 H66 M54 226 H66"/>'
    s += '<path d="M96 22 H184"/><path d="M96 16 V28 M184 16 V28"/><path d="M128 272 L270 272"/><path d="M128 266 V278 M270 266 V278"/>'
    s += '<path d="M200 56 H232"/><path d="M200 40 V72"/></g>'
    s += '<g font-family="system-ui,sans-serif" font-size="12" fill="#1f2a44" font-weight="700"><text x="30" y="134" transform="rotate(-90 30 134)" text-anchor="middle">Height (cuff to heel)</text>'
    s += '<text x="140" y="14" text-anchor="middle">Flat width</text><text x="200" y="292" text-anchor="middle">Foot (heel to toe)</text>'
    s += '<text x="238" y="52">Cuff</text><text x="238" y="66" font-weight="400" font-size="11">depth</text></g>'
    return f'<svg viewBox="0 0 320 300" role="img" aria-label="Christmas stocking measurements: height from cuff top to heel, flat width, foot length from heel to toe, and cuff depth" xmlns="http://www.w3.org/2000/svg">{s}</svg>'

_opts = "".join(f'<option value="{k}"{" selected" if k == "standard" else ""}>{n}: {h} in tall</option>' for k, n, u, h, w, f, c in STK) + '<option value="custom">My own size</option>'
stk = top("Christmas stocking size and yarn calculator", "Pick a stocking size, your yarn and knitting or crochet: see how much yarn to buy, how many stitches to start with, and whether a name fits on the cuff.", "Christmas stocking calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> a standard Christmas stocking is about <strong>18 to 20 in (46–51 cm) tall</strong> from the top of the cuff to the heel and 7 to 8 in wide; minis are about 7 in and "extra long" shop stockings 26 in. By our estimate a standard stocking takes roughly <strong>{stk_rng(_std_k)} yd of worsted to knit</strong>, {stk_rng(_std_c)} yd to crochet, or {stk_rng(_std_b)} yd of bulky yarn, folded cuff included. Knit it in the round on about <strong>{stk_co(7, 4)} stitches</strong> in worsted.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="xs-size">Stocking size</label><select id="xs-size">{_opts}</select></div>
<div class="row2" id="xs-custom" hidden><div class="field"><label for="xs-h">Height, cuff top to heel (in)</label><input type="number" id="xs-h" value="18" min="4" max="40" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="xs-w">Flat width (in)</label><input type="number" id="xs-w" value="7" min="2" max="14" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="xs-f">Foot, heel to toe (in)</label><input type="number" id="xs-f" value="10" min="3" max="20" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="xs-c">Cuff depth (in)</label><input type="number" id="xs-c" value="3.5" min="0" max="10" step="0.5" inputmode="decimal"></div></div>
<div class="field"><span class="label" id="xs-craft-l">Knitting or crochet?</span><div class="seg" role="group" aria-labelledby="xs-craft-l" id="xs-craft"><button type="button" data-v="knit" aria-pressed="true">Knitting</button><button type="button" data-v="crochet" aria-pressed="false">Crochet</button></div></div>
<div class="row2"><div class="field"><label for="xs-wt">Yarn weight</label><select id="xs-wt"><option value="3">DK (3)</option><option value="4" selected>Worsted or aran (4)</option><option value="5">Bulky or chunky (5)</option><option value="6">Super bulky (6)</option></select></div>
<div class="field"><label for="xs-g">Your gauge: stitches per 4 in</label><input type="number" id="xs-g" value="18" min="4" max="40" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="xs-sk">Yards in one skein</label><input type="number" id="xs-sk" value="200" min="10" max="2000" step="1" inputmode="numeric"></div>
<div class="field"><label for="xs-cuff">Cuff</label><select id="xs-cuff"><option value="fold">Folded over (double)</option><option value="flat">Plain, not folded</option></select></div></div>
<div class="field"><label for="xs-name">Name for the cuff (optional)</label><input type="text" id="xs-name" value="" maxlength="20" placeholder="e.g. Amelia" autocomplete="off"></div>
<p class="sub">Saved on this device only. Nothing is uploaded.</p>
</div><div class="result" aria-live="polite" id="xs-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Christmas stocking size chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size</th><th scope="col">Height</th><th scope="col">Flat width</th><th scope="col">Foot</th><th scope="col">Knit, worsted</th><th scope="col">Crochet, worsted</th><th scope="col">Knit, bulky</th></tr></thead><tbody>{stk_rows}</tbody></table></div>
<p class="note">Height runs from the top of the cuff to the bottom of the heel; foot runs from the back of the heel to the tip of the toe. Sizes are typical of shop-bought and pattern stockings, not a fixed standard. Yarn amounts are our estimates for plain stitches with a folded cuff, a hanging loop and ends; colourwork, cables and furry yarn use more.</p>
<figure style="margin:20px auto;max-width:360px">{stk_svg()}<figcaption class="note" style="text-align:center">How to measure a stocking, or the one you want to match.</figcaption></figure>
<h2>How many stitches to cast on for a stocking</h2>
<p>A stocking knit in the round is a tube twice the flat width around. Multiply that by your stitches per inch and round to a multiple of 4, so the heel can use exactly half the stitches. Our numbers, at the Craft Yarn Council's middle gauge for each weight:</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size</th><th scope="col">DK</th><th scope="col">Worsted</th><th scope="col">Bulky</th><th scope="col">Super bulky</th></tr></thead><tbody>{stk_co_rows}</tbody></table></div>
<p>Knitting it flat in two pieces instead? Cast on half the number plus 2 for the seam on each piece. Your own gauge matters more than the label, so knit a small swatch and use the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> or the <a href="{href("gauge-converter.html")}">gauge converter</a> if your numbers differ. To start on circular needles without twisting, see <a href="{href("how-to-knit-in-the-round.html")}">how to knit in the round</a>.</p>
<h2>Crocheting a stocking</h2>
<p>Crochet stockings are usually made as two flat panels joined around the edge, or worked in rounds from the cuff down. For two panels, chain the flat width at your gauge plus 1. For rounds, chain twice the flat width and join, then work single crochet or half double crochet in rounds. Crochet uses about a quarter more yarn than knitting for the same size, which the calculator allows for. New to the stitches? Start with <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>, and use the <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a> for the starting chain.</p>
<h2>Which yarn is best for a Christmas stocking?</h2>
<ul><li><strong>Worsted or aran acrylic</strong> is the classic: cheap, washable, holds its shape when it's full of gifts.</li>
<li><strong>Bulky or chunky</strong> is the fastest. A standard stocking in bulky is a weekend make for most knitters and crocheters.</li>
<li><strong>Wool</strong> gives the crisp stitches you want for Fair Isle names and motifs, and it doesn't stretch as much when filled.</li>
<li><strong>Furry or eyelash yarn</strong> makes a Santa-style cuff. It hides stitches, so use it only for the cuff and allow extra yarn.</li></ul>
<h2>Putting a name on the cuff</h2>
<p>The easiest way to add a name is <strong>duplicate stitch</strong>: knit the cuff plain, then embroider the letters over the stitches with a needle afterwards. You can plan it on squared paper or with the <a href="{href("cross-stitch-calculator.html")}">cross stitch calculator</a>'s grid thinking. A simple blocky alphabet is about 5 stitches wide and 7 rows tall, plus a 1-stitch gap between letters. The calculator tells you how many letters fit across the front. Long name? Use a bigger stocking, a finer yarn, or initials. In crochet, tapestry crochet or surface slip stitch works the same way; embroidery stitches like <a href="{href("embroidery-stitches.html")}">backstitch and chain stitch</a> work on felt cuffs too.</p>
<h2>Will it be ready by Christmas?</h2>
<p>A standard worsted stocking is roughly 8 to 14 hours of knitting for most people, less in bulky or for a mini. Check your own pace with the <a href="{href("crochet-time-estimator.html")}">crochet and knitting time calculator</a>, and line it up with your other gifts in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Making a set for the family? Minis make lovely <a href="{href("advent-calendar-ideas.html")}">advent calendars</a>, and our <a href="{href("christmas-crafts.html")}">Christmas crafts</a> page has more quick makes.</p>
<div class="callout"><strong>Selling stockings at a market?</strong> Personalised stockings sell well in November and December. Price them from your yarn and hours with our <a href="{href("how-to-price-crochet-items.html")}">pricing guide</a>, and check a stall pays with the <a href="{href("craft-fair-profit-calculator.html")}">craft fair profit calculator</a>.</div>
</div></div></section>'''
stk_faq = [
    ("What size is a standard Christmas stocking?", "Most are about 18 to 20 inches (46 to 51 cm) from the top of the cuff to the heel and 7 to 8 inches wide. Minis for trees and advent calendars are about 7 inches, and extra long stockings about 26 inches."),
    ("How much yarn do I need to knit a Christmas stocking?", f"By our estimate a standard 18 inch stocking takes about {stk_rng(_std_k)} yards of worsted yarn, or {stk_rng(_std_b)} yards of bulky, with a folded cuff. Plan the cuff, heel and toe colours separately and buy a little extra."),
    ("How much yarn do I need to crochet a Christmas stocking?", f"About a quarter more than knitting: roughly {stk_rng(_std_c)} yards of worsted for a standard 18 inch stocking, by our estimate."),
    ("How many stitches do I cast on for a Christmas stocking?", f"Twice the flat width times your stitches per inch, rounded to a multiple of 4. For a 7 inch wide stocking in worsted at 18 stitches per 4 inches that's {stk_co(7, 4)} stitches in the round."),
    ("How long does it take to make a Christmas stocking?", "A standard worsted stocking takes most people roughly 8 to 14 hours to knit or crochet, a bulky one less, and a mini 1 to 2 hours. Colourwork names add time."),
    ("How do I add a name to a knitted stocking?", "Knit the cuff plain and add the name afterwards in duplicate stitch, embroidering over the stitches. Each letter is about 5 stitches wide and 7 rows tall plus a 1 stitch gap; the calculator shows how many letters fit."),
]
SHOP_FOR["christmas-stocking-calculator.html"] = ["christmas-gift-tags", "christmas-gift-planner-budget", "yarn-stash-tracker", "2027-crochet-knitting-planner"]
page("christmas-stocking-calculator.html", "Christmas Stocking Size Chart & Yarn Calculator | Purl & Paper",
     "Christmas stocking calculator: sizes from mini to 26 in, yarn to knit or crochet one in DK, worsted or bulky, stitches to cast on, and if a name fits the cuff.",
     stk, stk_faq, "Christmas stocking calculator", app_name="Christmas stocking size and yarn calculator")


# ======== HOW TO READ CROCHET PATTERNS ========
# Checked against Craft Yarn Council "How to read a crochet pattern" and its standard chart symbols, Yarnspirations and Annie's
# pattern-reading guides, Gathered "how to read a crochet pattern" (SERP 26 Nov 2026). Own words, own drawings.
def rp_line_svg():
    s = '<rect width="640" height="200" rx="14" fill="#f3ede2"/>'
    parts = [(20, "Rnd 3:", "#2f8f8a"), (86, "*sc in next st,", "#1f2a44"), (222, "2 sc in next st;", "#b8326a"), (368, "rep from * around.", "#1f2a44"), (540, "(18)", "#c07d00")]
    for x, t, c in parts:
        s += f'<text x="{x}" y="96" font-family="ui-monospace,Menlo,monospace" font-size="17" font-weight="700" fill="{c}">{e(t)}</text>'
    s += '<path d="M86 110 H520" stroke="#1f2a44" stroke-width="2" stroke-dasharray="5 4"/><path d="M86 104 V116 M520 104 V116" stroke="#1f2a44" stroke-width="2"/>'
    notes = [(40, 50, "Which round", "#2f8f8a", 40, 78), (150, 40, "1 stitch into 1 stitch", "#1f2a44", 140, 78), (290, 50, "increase: 2 into 1", "#b8326a", 290, 78), (560, 44, "stitches when done", "#c07d00", 556, 78)]
    for x, y, t, c, lx, ly in notes:
        s += f'<text x="{x}" y="{y}" font-family="system-ui,sans-serif" font-size="12.5" text-anchor="middle" fill="{c}" font-weight="700">{t}</text><path d="M{x} {y + 6} L{lx} {ly}" stroke="{c}" stroke-width="1.5"/>'
    s += '<text x="303" y="140" font-family="system-ui,sans-serif" font-size="13" text-anchor="middle" fill="#1f2a44" font-weight="700">The repeat: work everything from the * again and again until the round ends</text>'
    s += '<text x="320" y="178" font-family="system-ui,sans-serif" font-size="12.5" text-anchor="middle" fill="#1f2a44">Last round had 12 stitches, so the repeat (2 stitches used) is worked 6 times: 6 × 3 = 18</text>'
    return f'<svg viewBox="0 0 640 200" role="img" aria-label="A crochet pattern line taken apart: the round number, a single crochet, an increase, the repeat and the stitch count in brackets" xmlns="http://www.w3.org/2000/svg">{s}</svg>'

def rp_sym(k):
    s = '<rect width="64" height="64" rx="8" fill="#f3ede2"/>'
    c = 'stroke="#1f2a44" stroke-width="3" fill="none" stroke-linecap="round"'
    if k == "ch": s += f'<ellipse cx="32" cy="32" rx="14" ry="8" {c}/>'
    elif k == "sl": s += '<circle cx="32" cy="32" r="6" fill="#1f2a44"/>'
    elif k == "sc": s += f'<path d="M22 22 L42 42 M42 22 L22 42" {c}/>'
    elif k == "hdc": s += f'<path d="M32 14 V52 M22 14 H42" {c}/>'
    elif k == "dc": s += f'<path d="M32 12 V54 M22 12 H42 M26 36 L38 28" {c}/>'
    elif k == "tr": s += f'<path d="M32 8 V58 M22 8 H42 M26 32 L38 24 M26 42 L38 34" {c}/>'
    elif k == "inc": s += f'<path d="M24 20 L40 36 M40 20 L24 36 M40 26 L54 40 M54 26 L40 40" {c}/><path d="M32 52 L32 46" {c}/>'
    elif k == "dec": s += f'<path d="M18 50 L32 22 L46 50" {c}/><path d="M24 30 L40 30" {c}/>'
    return f'<svg viewBox="0 0 64 64" width="56" height="56" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">{s}</svg>'

RP_SYMS = [("ch", "Chain (ch)", "An oval"), ("sl", "Slip stitch (sl st)", "A small filled dot"), ("sc", "Single crochet (sc)", "An X or a plus sign"),
           ("hdc", "Half double crochet (hdc)", "A T"), ("dc", "Double crochet (dc)", "A T with one slash"), ("tr", "Treble crochet (tr)", "A T with two slashes"),
           ("inc", "Increase (inc)", "Two symbols that share one base"), ("dec", "Decrease (sc2tog)", "Two symbols that join at the top")]
RP_EX = [("Increase round", "Rnd 2: inc in each st around. (12)", "6"), ("Amigurumi", "Rnd 3: [sc, inc] x 6 (18)", "12"),
         ("Star repeat", "Rnd 4: *sc in next 2 sts, 2 sc in next st; rep from * around. (24 sts)", "18"),
         ("Decrease round", "Rnd 9: (sc 3, dec) x 6 (24)", "30"), ("Row with turn", "Row 2: ch 1, turn, sc in each st across. (20)", "20"),
         ("Magic ring", "Rnd 1: 6 sc in magic ring. (6)", "0")]
rp_syms = "".join(f'<li>{rp_sym(k)}<span><strong>{n}</strong><br>{d}</span></li>' for k, n, d in RP_SYMS)
rp = top("How to read crochet patterns", "What every part of a crochet pattern means, from the abbreviations to the stars, brackets and numbers at the end of each row, with a pattern line explainer that checks your stitch count.", "How to read crochet patterns") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> read a crochet pattern one row or round at a time, left to right. Each instruction usually means one stitch into the next stitch of the last row. Abbreviations like <strong>sc</strong> (single crochet) and <strong>inc</strong> (2 stitches in one) say which stitch to make; anything after a <strong>*</strong> or inside <strong>[ ]</strong> or <strong>( )</strong> is repeated as many times as it says; and the number in brackets at the end, like <strong>(18)</strong>, is how many stitches you should have when the row is done.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="rp-in">Paste one row or round from your pattern</label><textarea id="rp-in" spellcheck="false">Rnd 4: *sc in next 2 sts, 2 sc in next st; rep from * around. (24 sts)</textarea></div>
<div class="field"><label for="rp-prev">Stitches in the row or round before (optional)</label><input type="number" id="rp-prev" value="18" min="0" max="2000" step="1" inputmode="numeric"></div>
<div class="field"><span class="label">Try an example</span><div class="ka-ex">{"".join(f'<button type="button" class="lock" data-ex="{e(x)}" data-prev="{p}">{e(n)}</button>' for n, x, p in RP_EX)}</div></div>
<p class="sub">Works with US terms (sc, hdc, dc, tr, inc, dec, sc2tog, ch, sk, sl st), stars, brackets, "x 6", "6 times" and "around". Nothing leaves your device.</p>
</div><div class="result" id="rp-out" aria-live="polite"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>One pattern line, taken apart</h2>
<figure style="margin:16px 0">{rp_line_svg()}</figure>
<p>Most lines in a crochet pattern have the same four parts: which row or round you're on, the stitches in order, what to repeat, and the stitch count at the end. Once you can spot those four, any pattern becomes readable. If you have a line that confuses you, paste it into the explainer above: it spells out each step and adds up the stitches for you.</p>
<h2>The parts of a crochet pattern</h2>
<ol><li><strong>Skill level.</strong> Beginner, easy, intermediate or experienced. The Craft Yarn Council's skill levels are used by most yarn companies.</li>
<li><strong>Materials.</strong> Yarn weight, how many yards or skeins, hook size, and notions like stitch markers or stuffing. Swapping yarn? See the <a href="{href("yarn-substitution-calculator.html")}">yarn substitution calculator</a> and the <a href="{href("yarn-weights.html")}">yarn weight chart</a>.</li>
<li><strong>Gauge.</strong> How many stitches and rows fit in 4 in (10 cm). It matters for anything that has to fit, like hats and sweaters; the <a href="{href("gauge-converter.html")}">gauge converter</a> helps when yours is different.</li>
<li><strong>Finished size.</strong> What you'll end up with, sometimes in several sizes. Pattern numbers for sizes are often written like <em>36 (40, 44)</em>: follow the number in the same position all the way through. Highlighting yours helps.</li>
<li><strong>Abbreviations and special stitches.</strong> The pattern's own key. Read it before you start, because designers don't always use the same short forms.</li>
<li><strong>Notes.</strong> Whether the turning chain counts as a stitch, whether you join rounds or work in a spiral, and which side is the right side.</li>
<li><strong>Instructions</strong>, row by row, then <strong>finishing</strong>: fasten off, <a href="{href("how-to-weave-in-ends.html")}">weave in ends</a>, block, assemble.</li></ol>
<h2>Rows and rounds</h2>
<p><strong>Row</strong> means you're working back and forth, turning at the end of each row. <strong>Round</strong> (Rnd) means you're working in a circle, either joining each round with a slip stitch or going round in a continuous spiral, as most amigurumi do. In a spiral, put a stitch marker in the first stitch of each round so you know where it starts. "Rows 4–10: repeat Row 3" means work the same row again for each of rows 4 to 10, which is 7 more rows. Keep your place with the <a href="{href("row-counter.html")}">row counter</a>.</p>
<h2>Stars, brackets and repeats</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">You see</th><th scope="col">It means</th></tr></thead><tbody>
<tr><td><code>*sc, inc; rep from * around</code></td><td>Work from the star to the semicolon, then go back to the star and keep going until you reach the end of the round.</td></tr>
<tr><td><code>*sc, inc; rep from * 4 more times</code></td><td>Work the part once, then 4 more times: 5 times in total. "More" is the word to watch.</td></tr>
<tr><td><code>[sc, inc] x 6</code> or <code>(sc, inc) 6 times</code></td><td>Work what's inside the brackets 6 times in total.</td></tr>
<tr><td><code>(dc, ch 2, dc) in next st</code></td><td>Make everything inside the brackets into one single stitch: a V stitch or shell.</td></tr>
<tr><td><code>**</code> inside a <code>*</code> repeat</td><td>A repeat inside a repeat: finish the inner one first, as many times as it says.</td></tr>
<tr><td><code>(18)</code>, <code>[18 sts]</code> or <code>— 18 sts</code> at the end</td><td>The stitch count when the row or round is finished. Count yours before moving on.</td></tr>
</tbody></table></div>
<h2>Phrases you'll meet in crochet patterns</h2>
<ul><li><strong>In next st</strong>: into the next stitch of the last row. <strong>In same st</strong>: into the stitch you just used.</li>
<li><strong>Sc in next 3 sts</strong> or <strong>sc 3</strong>: one single crochet in each of the next 3 stitches (3 stitches, not 3 in one).</li>
<li><strong>3 sc in next st</strong>: all 3 into one stitch, which makes a corner or increase.</li>
<li><strong>Inc</strong>: 2 stitches in one stitch. <strong>Dec</strong> or <strong>sc2tog</strong>: 2 stitches worked together into 1. See <a href="{href("how-to-crochet-decrease.html")}">how to decrease in crochet</a>.</li>
<li><strong>Sk</strong>: skip. <strong>Ch-sp</strong>: the space under a chain from the last row; you work into the gap, not into the chain.</li>
<li><strong>Across</strong> and <strong>around</strong>: to the end of the row or round. <strong>Turn</strong>: flip your work to start the next row.</li>
<li><strong>FLO</strong> and <strong>BLO</strong>: front loop only, back loop only. <strong>FPdc</strong> and <strong>BPdc</strong>: front and back post double crochet, worked around the stitch's post.</li>
<li><strong>RS</strong> and <strong>WS</strong>: right side and wrong side. <strong>MR</strong>: magic ring; see <a href="{href("how-to-crochet-magic-ring.html")}">how to crochet a magic ring</a>.</li>
<li><strong>Ch 3 (counts as dc)</strong>: the turning chain stands in for the first stitch, so skip the first stitch and remember to work into the top of the chain at the end of the next row.</li></ul>
<p>Every stitch name is drawn step by step in <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>.</p>
<h2>Is my pattern in US or UK terms?</h2>
<p>US and UK patterns use the same names for different stitches: a UK double crochet is a US single crochet. Look for <strong>sc</strong> (only in US patterns) or <strong>htr</strong> (only in UK patterns). The full side-by-side list is on our <a href="{href("crochet-terms.html")}">US vs UK crochet terms</a> page. The explainer above reads US terms.</p>
<h2>How to read a crochet chart</h2>
<p>Charts draw the stitches instead of writing them. Each symbol is one stitch, and the symbols sit where the stitches sit in the fabric. Read rounds from the centre out, usually anticlockwise if you're right-handed, and rows from the bottom up, right to left on right-side rows and left to right on wrong-side rows. The height of the symbol matches the height of the stitch. These are the common ones, as the Craft Yarn Council standardises them:</p>
<ul class="rp-syms">{rp_syms}</ul>
<p>Most charts come with their own key, so check it, especially for clusters, puffs and popcorns.</p>
<h2>Tips for your first pattern</h2>
<ul><li>Read the whole pattern once before you start, and look up anything new.</li>
<li>Print it or copy it and tick off rows as you go. Mark your size.</li>
<li>Count your stitches at the end of every row for the first few rows. Most mistakes show up as a wrong count.</li>
<li>Use a stitch marker in the first and last stitch of each row so you don't miss or add one.</li>
<li>Stuck on one line? Paste it in the explainer, then try it stitch by stitch.</li></ul>
<p>Knitting instead? Our <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a> has a decoder for knitting patterns.</p>
</div></div></section>
<style>.rp-syms{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}}.rp-syms li{{display:flex;gap:10px;align-items:center;font-size:.95rem}}.rp-syms svg{{flex:none}}
.rp-steps{{margin:8px 0 0;padding-left:20px;color:#fff}}.rp-steps li{{margin:4px 0}}.rp-seq{{font:600 .9rem/1.6 ui-monospace,Menlo,monospace;color:#fff;background:rgba(255,255,255,.08);border-radius:8px;padding:8px 10px;overflow-wrap:anywhere}}</style>'''
rp_faq = [
    ("What do the numbers in brackets at the end of a crochet row mean?", "They are the stitch count: how many stitches you should have when that row or round is finished. (18) means 18 stitches. Chains and slip stitches are usually not counted unless the pattern says so."),
    ("What does * mean in a crochet pattern?", "The star marks the start of a repeat. Work the instructions after it, then 'rep from *' tells you to go back to the star and work them again, either a set number of times or around to the end of the round."),
    ("What does 'rep from * 3 more times' mean?", "Work the starred part once, then 3 more times, so 4 times in total. Without the word 'more', '3 times' usually means 3 times in total."),
    ("What is the difference between ( ) and [ ] in crochet patterns?", "Both group stitches to repeat or to work into one stitch. Many patterns use brackets inside parentheses for a repeat inside a repeat; the pattern's notes say which it uses."),
    ("What does 'sc 3' mean in a crochet pattern?", "One single crochet in each of the next 3 stitches. '3 sc in next st' is different: all 3 go into the same stitch, which increases."),
    ("Does the turning chain count as a stitch?", "It depends on the pattern. A chain 1 before single crochet usually doesn't count; a chain 2 or 3 before double crochet often does, written 'ch 3 (counts as dc)'. Check the pattern notes."),
    ("How do I know if a crochet pattern is in US or UK terms?", "Look for 'sc', which only US patterns use, or 'htr', which only UK patterns use. A UK double crochet is a US single crochet."),
]
SHOP_FOR["how-to-read-crochet-patterns.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("how-to-read-crochet-patterns.html", "How to Read Crochet Patterns (+ Line Explainer) | Purl & Paper",
     "How to read a crochet pattern: abbreviations, rows vs rounds, * repeats, brackets and stitch counts. Paste any line to see it step by step and check the count.",
     rp, rp_faq, "How to read crochet patterns", app_name="Crochet pattern line explainer")
