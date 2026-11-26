# ---------------- 26 Nov 2026 run 6: FAT QUARTER CALCULATOR + SEAM ALLOWANCE GUIDE + CROCHET PROJECT PLANNER PRINTABLE ----------------
# Executed from build.py after stitchscrap.py (shares page(), top(), href(), e(), SHOP_FOR, more_crafts(), _sb_rows()).
# Demand evidence in DEMAND.md (RADAR 26 Nov run 6). Drawings are our own SVG; wording our own.
# JS lives in assets/app.js (fq-*, sa-* and pjp-* features), CSS in assets/style.css.
import json as _json, math as _math

def _fr8(x):
    """Inches as a whole number plus eighths, e.g. 5.625 -> 5⅝."""
    w = int(x + 1e-9); f = round((x - w) * 8)
    if f == 8: w += 1; f = 0
    F = ["", "⅛", "¼", "⅜", "½", "⅝", "¾", "⅞"][f]
    return (str(w) if w else ("" if F else "0")) + F

# ======== FAT QUARTER CALCULATOR ========
# Precut sizes: a US fat quarter is a half yard (18 in) cut in half across a 42-44 in bolt, so about 18 x 22 in, and most
# quilters plan on 18 x 21 in usable once the selvedge is trimmed and the edge straightened (Missouri Star "fat quarter size",
# Linda's "understanding fat quarter size", Mrs Quilty and Hello Sewing guides, SERP 26 Nov 2026). Fat eighth: 9 x 22 in
# (some shops cut 11 x 18). Long quarter: 9 x 44 in. Metric fat quarter (UK/EU): 50 x 55 cm. 1 yard = 4 fat quarters.
FQ_TYPES = [("fq", "Fat quarter, US (18 x 22 in, plan on 18 x 21)", 18, 21),
            ("fq-full", "Fat quarter, full 18 x 22 in", 18, 22),
            ("fe", "Fat eighth (9 x 22 in, plan on 9 x 21)", 9, 21),
            ("lq", "Long quarter (9 x 44 in, plan on 9 x 42)", 9, 42),
            ("fq-m", "Metric fat quarter (50 x 55 cm)", 19.5, 21.5),
            ("hy", "Half yard (18 x 44 in, plan on 18 x 42)", 18, 42)]

def fq_fit(W, H, w, h):
    """Most w x h pieces from a W x H piece with straight rotary cuts: rows of one way round, then rows turned the other way."""
    a = _sb_rows(W, H, w, h, 0, 0)
    b = _sb_rows(H, W, w, h, 0, 0)
    return max(len(a), len(b))

FQ_SQ = [2.5, 3, 3.5, 4.5, 5, 5.5, 6.5, 10]
fq_sq_rows = "".join(f'<tr><td><strong>{_fr8(s)} in</strong> ({_fr8(s - 0.5)} in finished)</td><td>{fq_fit(18, 21, s, s)}</td><td>{fq_fit(9, 21, s, s)}</td><td>{fq_fit(19.5, 21.5, s, s)}</td></tr>' for s in FQ_SQ)
fq_strip_rows = "".join(f'<tr><td><strong>{_fr8(s)} in</strong></td><td>{int(18 // s)} strips, 21 in long</td><td>{int(9 // s)} strips, 21 in long</td><td>{int(42 // s)} strips across a full width (40-42 in)</td></tr>' for s in (1.5, 2, 2.5, 3, 3.5))
FQ_QUILTS = [("Baby", 36, 48), ("Throw", 50, 65), ("Twin", 70, 90), ("Queen", 90, 100)]

def fq_need(W, H, f, pw=18, ph=21):
    n = _math.ceil(W / f) * _math.ceil(H / f); per = fq_fit(pw, ph, f + 0.5, f + 0.5)
    return n, per, _math.ceil(n / per)

fq_quilt_rows = "".join(f'<tr><td><strong>{n}</strong> ({w} x {h} in)</td>' + "".join(f'<td>{fq_need(w, h, f)[2]}</td>' for f in (4, 5, 6)) + '</tr>' for n, w, h in FQ_QUILTS)
_th = fq_need(50, 65, 5)
fq_opts = "".join(f'<option value="{k}">{e(n)}</option>' for k, n, a, b in FQ_TYPES)
fq_data = _json.dumps({k: [a, b] for k, n, a, b in FQ_TYPES}, separators=(",", ":"))

def _fq_svg9():
    s, out = 16, ""
    for r in range(3):
        for c in range(3):
            out += f'<rect x="{6 + c * 5.5 * s:.0f}" y="{6 + r * 5.5 * s:.0f}" width="{5.5 * s - 3:.0f}" height="{5.5 * s - 3:.0f}" rx="3" fill="{["#2f8f8a", "#b8326a", "#e39a14"][(r + c) % 3]}" opacity=".85"/>'
    out += f'<rect x="6" y="{6 + 16.5 * s:.0f}" width="{18 * s - 3:.0f}" height="{4.5 * s - 3:.0f}" rx="3" fill="#5b6b94" opacity=".35"/>'
    W, H = 18 * s, 21 * s
    return (f'<svg viewBox="0 0 {W + 12:.0f} {H + 40:.0f}" role="img" aria-label="An 18 by 21 inch fat quarter cut into nine 5.5 inch squares with a strip left over">'
            f'<rect x="4" y="4" width="{W + 4:.0f}" height="{H + 4:.0f}" rx="6" fill="#f3ede2" stroke="#1f2a44" stroke-width="2"/>{out}'
            f'<text x="{(W + 12) / 2:.0f}" y="{H + 32:.0f}" text-anchor="middle" font-size="15" fill="#1f2a44" font-family="Georgia,serif">18 x 21 in: nine 5½ in squares + a 4½ in strip</text></svg>')

fqp = top("Fat quarter calculator: how many fat quarters do I need?", "Find how many squares, strips or rectangles you can cut from one fat quarter, and how many fat quarters a whole quilt top takes. US, metric and fat eighth sizes.", "Fat quarter calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> a <strong>fat quarter is 18 x 22 in</strong> (a half yard cut in half), and you can count on about <strong>18 x 21 in</strong> once the selvedge is trimmed. One fat quarter gives <strong>12 five-inch squares</strong>, <strong>9 squares of 5½ in</strong>, <strong>56 squares of 2½ in</strong> or <strong>seven 2½ in strips</strong>. A throw quilt of 50 x 65 in made from 5 in finished squares needs about <strong>{_th[2]} fat quarters</strong>. Four fat quarters make one yard.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="fq-mode">What do you want to know?</label><select id="fq-mode"><option value="pieces">How many pieces from my fat quarters</option><option value="quilt">How many fat quarters for a quilt of squares</option></select></div>
<div class="field"><label for="fq-type">Fabric piece</label><select id="fq-type">{fq_opts}</select></div>
<div id="fq-pieces">
<div class="row2"><div class="field"><label for="fq-w">Cut piece width (in)</label><input type="number" id="fq-w" value="5" min="0.5" max="40" step="0.125" inputmode="decimal"></div>
<div class="field"><label for="fq-h">Cut piece height (in)</label><input type="number" id="fq-h" value="5" min="0.5" max="40" step="0.125" inputmode="decimal"></div></div>
<div class="field"><label for="fq-need">Pieces you need (optional)</label><input type="number" id="fq-need" value="" min="1" max="5000" step="1" inputmode="numeric" placeholder="e.g. 80"></div>
</div>
<div id="fq-quilt" hidden>
<div class="row2"><div class="field"><label for="fq-qw">Quilt top width (in)</label><input type="number" id="fq-qw" value="50" min="6" max="130" step="1" inputmode="decimal"></div>
<div class="field"><label for="fq-qh">Quilt top length (in)</label><input type="number" id="fq-qh" value="65" min="6" max="130" step="1" inputmode="decimal"></div></div>
<div class="field"><label for="fq-f">Finished square size (in)</label><input type="number" id="fq-f" value="5" min="1" max="20" step="0.5" inputmode="decimal"><p class="sub">We add a ¼ in seam allowance all round, so a 5 in finished square is cut 5½ in.</p></div>
</div>
<p class="sub">Saved on this device only. Nothing is uploaded.</p>
</div><div class="result" aria-live="polite" id="fq-out" data-q="{href("quilt-size-calculator.html")}"></div></div></section>
<script type="application/json" id="fq-data">{fq_data}</script>
<section><div class="wrap"><div class="narrow prose">
<h2>What size is a fat quarter?</h2>
<p>Take a half yard of quilting cotton (18 in long, the full 42 to 44 in width of the bolt) and cut it in half along the fold. Each piece is about <strong>18 x 22 in</strong>: that's a fat quarter. A "skinny" or <strong>long quarter</strong> is a quarter yard cut the usual way, 9 x 44 in. Same amount of fabric, but the fat quarter is far more useful for squares and blocks because it's nearly square.</p>
<p>In the UK and Europe fabric is sold by the metre, so a fat quarter is usually <strong>50 x 55 cm</strong>, a little bigger than the US one. A <strong>fat eighth</strong> is half a fat quarter: usually 9 x 22 in, though some shops cut 11 x 18 in, so check the listing.</p>
<figure class="sb-fig"><div>{_fq_svg9()}<figcaption>How a fat quarter cuts into 5½ in squares (5 in finished)</figcaption></div></figure>
<h2>How many squares in a fat quarter?</h2>
<p>Cut sizes, straight rotary cuts only, planning on 18 x 21 in for a US fat quarter (our own cutting maths):</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Square cut size</th><th scope="col">Fat quarter (18 x 21 in)</th><th scope="col">Fat eighth (9 x 21 in)</th><th scope="col">Metric FQ (50 x 55 cm)</th></tr></thead><tbody>{fq_sq_rows}</tbody></table></div>
<h2>How many strips from a fat quarter?</h2>
<p>Strips from a fat quarter are about 21 in long, half the length of a strip cut across the full width of fabric. Most patterns written for jelly roll style strips (2½ in) need two fat quarter strips for every full-width strip.</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Strip width</th><th scope="col">Fat quarter</th><th scope="col">Fat eighth</th><th scope="col">Yardage (for comparison)</th></tr></thead><tbody>{fq_strip_rows}</tbody></table></div>
<h2>How many fat quarters for a quilt?</h2>
<p>For a simple quilt top of squares, with ¼ in seams (not counting borders, binding or backing):</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Quilt top</th><th scope="col">4 in squares</th><th scope="col">5 in squares</th><th scope="col">6 in squares</th></tr></thead><tbody>{fq_quilt_rows}</tbody></table></div>
<p>Sizes are finished squares. The sizes in the first column are typical examples; work out the exact top for your bed with the <a href="{href("quilt-size-calculator.html")}">quilt size calculator</a>, which also gives backing and binding yardage. Buy one or two extra fat quarters so you can move colours around and recut a mistake.</p>
<h2>Fat quarter or yardage?</h2>
<ul><li><strong>Fat quarters</strong> are best for scrappy quilts, lots of colours, and blocks up to about 10 in. A fat quarter bundle is the easiest way to get a set of fabrics that go together.</li>
<li><strong>Yardage</strong> is better for long strips, sashing, borders, binding and backing, which need lengths longer than 21 in.</li>
<li><strong>The maths:</strong> 1 yard = 4 fat quarters = 8 fat eighths. If a pattern asks for ½ yard of one fabric, 2 fat quarters of it will usually do, unless it needs strips longer than 21 in.</li></ul>
<h2>What can you make with one fat quarter?</h2>
<p>A zip pouch, a pair of potholders, a tote bag lining, a cushion front, a set of fabric coasters, a drawstring gift bag, a baby bib or a couple of scrunchies. Half square triangles are a great use for leftovers: the <a href="{href("half-square-triangle-calculator.html")}">HST calculator</a> gives the cut sizes. New to sewing? Our <a href="{href("sewing-seam-allowance.html")}">seam allowance guide</a> explains the ¼ in quilting seam and how to sew it accurately.</p>
<p class="note">Fat quarter, fat eighth and long quarter sizes as described by quilt shops and quilting guides (Missouri Star, Linda's, Mrs Quilty, Hello Sewing; checked 26 Nov 2026). Usable size varies a little with the bolt width and how straight it was cut. The piece counts are our own maths with straight cuts and no waste allowance.</p>
</div></div></section>'''
fq_faq = [
    ("What size is a fat quarter?", "About 18 x 22 inches: a half yard of fabric cut in half across the width. Plan on about 18 x 21 in usable once the selvedge is trimmed. A metric fat quarter is 50 x 55 cm."),
    ("How many 5 inch squares can you cut from a fat quarter?", "12: three across the 18 in side and four down the 21 in side. For 5 in finished squares (cut 5½ in) you get 9."),
    ("How many 2.5 inch squares are in a fat quarter?", "56: seven across and eight down an 18 x 21 in fat quarter."),
    ("How many fat quarters make a yard?", "Four. A yard of 44 in wide fabric is 36 x 44 in, which cuts into four 18 x 22 in fat quarters."),
    ("How many fat quarters do I need for a throw quilt?", f"About {_th[2]} for a 50 x 65 in top of 5 in finished squares ({_th[0]} squares at {_th[1]} per fat quarter), plus yardage for borders, binding and backing."),
    ("What is the difference between a fat quarter and a quarter yard?", "Both are a quarter of a yard. A quarter yard is a long strip, 9 x 44 in; a fat quarter is a squarer 18 x 22 in, which cuts bigger squares and blocks."),
    ("What size is a fat eighth?", "Usually 9 x 22 in, half a fat quarter. Some shops cut fat eighths 11 x 18 in instead."),
]
SHOP_FOR["fat-quarter-calculator.html"] = ["crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "christmas-gift-planner-budget", "christmas-gift-tags"]
page("fat-quarter-calculator.html", "Fat Quarter Calculator: Squares & Quilt Needs | Purl & Paper",
     "A fat quarter is 18 x 22 in (about 18 x 21 usable). Free calculator: how many squares or strips per fat quarter, and how many fat quarters you need for a quilt.",
     fqp, fq_faq, "Fat quarter calculator", app_name="Fat quarter calculator")


# ======== SEAM ALLOWANCE GUIDE + CALCULATOR ========
# Usual allowances: 5/8 in (1.5 cm) on the big commercial garment patterns; 3/8 in (1 cm) or 1/2 in on many independent
# patterns; 1/4 in for quilting; 1/2 in common for home decor; 1/4 to 3/8 in on overlocked knits; many European magazine
# patterns are printed without allowances. Sources: Sew Direct "understanding seam allowance", AllFreeSewing seam allowance
# guide, Oregon State University 4-H sewing guide, University of Kentucky FCS seams guide, Threads "industry seam allowances",
# Wikipedia "Seam allowance" (SERP 26 Nov 2026). Calculator maths is ours.
SA_USES = [("Commercial garment patterns (the big pattern companies)", "⅝ in", "1.5 cm", "The traditional home-sewing standard. Lots of room to fit and to finish the seam."),
           ("Independent garment patterns", "⅜ in or ½ in", "1 cm or 1.2 cm", "Varies by designer. It's printed in the instructions or on the pattern sheet: check before you cut."),
           ("European magazine patterns", "Often none included", "add 1 to 1.5 cm", "Many are traced without allowances. Add your own round every edge (more at hems) before cutting."),
           ("Quilting and patchwork", "¼ in", "6 to 7 mm", "Often a scant ¼ in (a thread or two less) so blocks finish at full size."),
           ("Cushions, curtains and home decor", "½ in", "1.2 to 1.5 cm", "Heavier fabric frays, so a wider allowance is safer."),
           ("Knits on an overlocker (serger)", "¼ to ⅜ in", "6 mm to 1 cm", "The overlocker trims and finishes in one pass."),
           ("Bags and totes", "⅜ to ½ in", "1 to 1.2 cm", "Wide enough to box corners and topstitch."),
           ("Doll clothes and tiny pieces", "¼ in", "6 mm", "Bulk matters at small sizes; trim curves after sewing.")]
sa_use_rows = "".join(f'<tr><td><strong>{e(a)}</strong></td><td>{b}</td><td>{c}</td><td>{e(d)}</td></tr>' for a, b, c, d in SA_USES)
SA_CONV = [(0.125, "⅛", "3 mm"), (0.25, "¼", "6 mm"), (0.375, "⅜", "1 cm"), (0.5, "½", "1.2 to 1.3 cm"), (0.625, "⅝", "1.5 cm"), (0.75, "¾", "2 cm"),
           (1, "1", "2.5 cm"), (1.25, "1¼", "3 cm"), (1.5, "1½", "4 cm"), (2, "2", "5 cm")]
sa_conv_rows = "".join(f'<tr><td>{f} in</td><td>{v * 25.4:.1f} mm</td><td>{r}</td></tr>' for v, f, r in SA_CONV)
SA_PRE = [("0.25", "¼ in (quilting)"), ("0.375", "⅜ in"), ("0.5", "½ in"), ("0.625", "⅝ in (commercial patterns)"), ("0.75", "¾ in"), ("1", "1 in"), ("cm1", "1 cm"), ("cm1.5", "1.5 cm")]
sa_opts = "".join(f'<option value="{v}"{" selected" if v == "0.5" else ""}>{e(n)}</option>' for v, n in SA_PRE)

def _sa_svg():
    return ('<svg viewBox="0 0 360 250" role="img" aria-label="A fabric piece: the solid outer line is the cutting line, the dashed inner line is the stitching line, and the band between them is the seam allowance">'
            '<rect x="20" y="20" width="320" height="190" rx="4" fill="#f3ede2" stroke="#1f2a44" stroke-width="2.5"/>'
            '<rect x="50" y="50" width="260" height="130" fill="#fbf8f1" stroke="#b8326a" stroke-width="2.5" stroke-dasharray="9 6"/>'
            '<path d="M20 115 h30" stroke="#2f8f8a" stroke-width="2"/><path d="M20 109 v12 M50 109 v12" stroke="#2f8f8a" stroke-width="2"/>'
            '<text x="180" y="105" text-anchor="middle" font-size="16" fill="#1f2a44" font-family="Georgia,serif">Finished size</text>'
            '<text x="180" y="128" text-anchor="middle" font-size="13" fill="#5b6b94" font-family="Inter,sans-serif">inside the stitching line</text>'
            '<text x="180" y="40" text-anchor="middle" font-size="13" fill="#2f8f8a" font-family="Inter,sans-serif">seam allowance</text>'
            '<text x="180" y="232" text-anchor="middle" font-size="13" fill="#1f2a44" font-family="Inter,sans-serif">solid line = cut  ·  dashed line = sew</text></svg>')

def _sa_svg2():
    return ('<svg viewBox="0 0 360 200" role="img" aria-label="Two layers of fabric, right sides together, sewn a set distance from the raw edge, then pressed open">'
            '<rect x="30" y="40" width="200" height="22" fill="#2f8f8a" opacity=".85"/><rect x="30" y="64" width="200" height="22" fill="#e39a14" opacity=".9"/>'
            '<path d="M190 34 v58" stroke="#b8326a" stroke-width="3" stroke-dasharray="6 5"/>'
            '<path d="M190 104 h40 M190 98 v12 M230 98 v12" stroke="#1f2a44" stroke-width="2"/>'
            '<text x="210" y="128" text-anchor="middle" font-size="13" fill="#1f2a44" font-family="Inter,sans-serif">allowance</text>'
            '<text x="110" y="128" text-anchor="middle" font-size="13" fill="#5b6b94" font-family="Inter,sans-serif">right sides together</text>'
            '<path d="M40 170 h120 l10 -20 M180 150 l10 20 h120" fill="none" stroke="#2f8f8a" stroke-width="5" stroke-linejoin="round"/>'
            '<path d="M170 150 l5 -10 l5 10" fill="none" stroke="#e39a14" stroke-width="5" stroke-linejoin="round"/>'
            '<text x="180" y="194" text-anchor="middle" font-size="13" fill="#1f2a44" font-family="Inter,sans-serif">then press the seam open (or to one side)</text></svg>')

sap = top("Seam allowance guide: what seam allowance should I use?", "The standard seam allowance for each kind of sewing, an inch and cm converter, and a calculator that adds the right allowance to any finished size so you know what to cut.", "Seam allowance guide") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the seam allowance is the strip of fabric between the cut edge and the stitching line. The usual sizes are <strong>⅝ in (1.5 cm)</strong> for commercial dressmaking patterns, <strong>⅜ in (1 cm) or ½ in</strong> for many independent patterns, <strong>½ in</strong> for cushions and home decor, and <strong>¼ in</strong> for quilting. Always use the one your pattern states. To get the cut size, add the allowance to <strong>every edge that will be sewn</strong>: a 16 in cushion front with ½ in seams is cut 17 x 17 in.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="sa-mode">I know the</label><select id="sa-mode"><option value="add">finished size: tell me what to cut</option><option value="sub">cut size: tell me the finished size</option></select></div>
<div class="row2"><div class="field"><label for="sa-w" id="sa-wl">Finished width</label><input type="number" id="sa-w" value="16" min="0.25" max="200" step="0.125" inputmode="decimal"></div>
<div class="field"><label for="sa-h" id="sa-hl">Finished height</label><input type="number" id="sa-h" value="16" min="0.25" max="200" step="0.125" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="sa-u">Units</label><select id="sa-u"><option value="in">inches</option><option value="cm">cm</option></select></div>
<div class="field"><label for="sa-sa">Seam allowance</label><select id="sa-sa">{sa_opts}<option value="own">My own</option></select></div></div>
<div class="field" id="sa-own-f" hidden><label for="sa-own">My seam allowance (same units)</label><input type="number" id="sa-own" value="0.5" min="0" max="5" step="0.0625" inputmode="decimal"></div>
<div class="row2"><div class="field"><label for="sa-sides">Sewn side edges</label><select id="sa-sides"><option value="2">Both sides</option><option value="1">One side (other on a fold)</option><option value="0">None</option></select></div>
<div class="field"><label for="sa-tb">Sewn top and bottom edges</label><select id="sa-tb"><option value="2">Both</option><option value="1">One (other is a hem or fold)</option><option value="0">None</option></select></div></div>
<div class="field"><label for="sa-hem">Hem allowance on the bottom edge (optional)</label><input type="number" id="sa-hem" value="" min="0" max="20" step="0.125" inputmode="decimal" placeholder="e.g. 1"></div>
<div class="field"><label for="sa-qty">How many pieces (optional)</label><input type="number" id="sa-qty" value="" min="1" max="500" step="1" inputmode="numeric" placeholder="e.g. 2 for a front and back"></div>
<p class="sub">Saved on this device only. Nothing is uploaded.</p>
</div><div class="result" aria-live="polite" id="sa-out"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<figure class="sb-fig"><div>{_sa_svg()}<figcaption>The seam allowance sits between the cutting line and the stitching line</figcaption></div><div>{_sa_svg2()}<figcaption>Sew with right sides together, the allowance away from the needle, then press</figcaption></div></figure>
<h2>Standard seam allowance by type of sewing</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Sewing</th><th scope="col">Usual allowance</th><th scope="col">Metric</th><th scope="col">Why</th></tr></thead><tbody>{sa_use_rows}</tbody></table></div>
<p>These are the usual starting points, not rules. The allowance your pattern prints always wins, because the pattern pieces were drafted for it. If you sew a ½ in seam on a pattern made for ⅝ in, each seam adds ⅛ in, and over a skirt with 4 side and centre seams that's an extra inch round the waist.</p>
<h2>Seam allowance converter: inches to mm and cm</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Inches</th><th scope="col">Exact</th><th scope="col">Rounded, as on metric patterns</th></tr></thead><tbody>{sa_conv_rows}</tbody></table></div>
<h2>How to add seam allowance to a pattern</h2>
<ol><li><strong>Check the pattern.</strong> Look for "seam allowance included" or "add seam allowance" on the sheet or in the instructions.</li>
<li><strong>Measure out from the stitching line</strong> with a ruler or a seam gauge, making small marks every inch or two, then join them. On curves, keep the ruler at a right angle to the line.</li>
<li><strong>Add hems separately.</strong> A hem allowance is usually wider than a seam allowance (often 1 to 2 in on skirts and trousers), so mark it on its own.</li>
<li><strong>Nothing on folds.</strong> Edges placed on the fold of the fabric don't get an allowance.</li>
<li><strong>Cut on the outer line.</strong> Or skip the drawing: two pencils taped together, or a quilting ruler set at your allowance, trace the new line as you go.</li></ol>
<h2>How to sew an accurate seam allowance</h2>
<p>Look at the metal throat plate under your needle: the engraved lines are measured from the needle and are usually marked ⅜, ½, ⅝ and so on. Keep the raw edge of the fabric running along the line you need and watch the line, not the needle. For quilting, a ¼ in presser foot (a foot exactly ¼ in from needle to edge) makes it much easier. Masking tape or a magnetic seam guide on the bed of the machine works too.</p>
<p>Test it: sew two 2½ in strips together and press. The piece should measure exactly 4½ in across. If it's smaller your seam is too wide; try a "scant" ¼ in, a thread or two narrower.</p>
<h2>Trimming, grading and clipping</h2>
<ul><li><strong>Trim</strong> the allowance on necklines, armholes and inside collars to about ¼ in after sewing so the seam turns smoothly.</li>
<li><strong>Grade</strong> bulky seams: cut each layer a different width so there's no ridge on the right side.</li>
<li><strong>Clip</strong> into the allowance on inward curves and <strong>notch</strong> (cut small wedges) on outward curves, without cutting the stitching.</li></ul>
<h2>French seam allowance</h2>
<p>A French seam hides the raw edges inside a neat tube, great for sheer fabric and bags without a lining. On a ⅝ in allowance: sew <strong>wrong sides together at ⅜ in</strong>, trim to about ⅛ in, press, fold right sides together and sew again at <strong>¼ in</strong>. ⅜ + ¼ = ⅝, so the garment still fits. On a 1.5 cm allowance use 1 cm then 0.5 cm.</p>
<p>Quilting? The <a href="{href("fat-quarter-calculator.html")}">fat quarter calculator</a>, <a href="{href("half-square-triangle-calculator.html")}">HST calculator</a> and <a href="{href("quilt-size-calculator.html")}">quilt size calculator</a> all use the ¼ in seam. Making a cushion or bag to sell? Price it with the same method as our <a href="{href("how-to-price-crochet-items.html")}">handmade pricing guide</a> and check the fees in the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>.</p>
<p class="note">Usual allowances from sewing guides and educational sewing resources (Sew Direct, AllFreeSewing, Oregon State University 4-H sewing guide, University of Kentucky FCS seams guide, Threads, Wikipedia's seam allowance article; checked 26 Nov 2026). Metric roundings are the ones commonly printed on metric patterns. The calculator is our own maths.</p>
</div></div></section>'''
sa_faq = [
    ("What is the standard seam allowance?", "⅝ in (1.5 cm) on most commercial dressmaking patterns, ¼ in for quilting and ½ in for most home decor. Many independent patterns use ⅜ in (1 cm) or ½ in, so always check the pattern."),
    ("Is seam allowance included in patterns?", "Usually, on commercial and most independent patterns: the sheet or instructions say so. Many European magazine patterns are printed without it, so you add your own before cutting."),
    ("How do I add seam allowance to a measurement?", "Add the allowance once for every sewn edge: twice across the width if both sides are seamed, and twice down the length if top and bottom are seamed. A 16 in square cushion front with ½ in seams is cut 17 x 17 in. Edges on a fold get nothing."),
    ("What is ⅝ inch in cm?", "⅝ in is 15.9 mm, which metric patterns round to 1.5 cm. ⅜ in is 9.5 mm (about 1 cm), ½ in is 12.7 mm and ¼ in is 6.4 mm."),
    ("Why is quilting seam allowance ¼ inch?", "Patchwork has many small pieces joined together, and a narrow seam keeps the bulk down and wastes less fabric. A scant ¼ in (a thread narrower) makes up for the fabric lost in the fold when you press."),
    ("Is hem allowance the same as seam allowance?", "No. A hem allowance is the extra length folded up at the bottom edge and is usually wider: often 1 to 2 in on skirts and trousers, and about ⅝ to 1 in on tops."),
    ("How do I sew an exact ⅝ inch seam?", "Line the raw edge up with the ⅝ mark on your machine's throat plate and watch that line, not the needle. A strip of masking tape on the bed or a magnetic seam guide makes it easier."),
]
SHOP_FOR["sewing-seam-allowance.html"] = ["crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "christmas-gift-planner-budget", "christmas-gift-tags"]
page("sewing-seam-allowance.html", "Seam Allowance Guide: Standard Sizes + Calculator | Purl & Paper",
     "Standard seam allowance is ⅝ in (1.5 cm) on commercial patterns, ¼ in for quilting, ½ in for home decor. Chart, inch to cm converter and a cut size calculator.",
     sap, sa_faq, "Seam allowance guide", app_name="Seam allowance calculator")


# ======== CROCHET + KNITTING PROJECT PLANNER (free printable, fill in online) ========
# Demand: 'free printable crochet project planner' (SERP 26 Nov 2026: I Like Crochet, Repeat Crafter Me, Daisy Cottage,
# Winding Road Crochet free downloads, Payhip/Etsy/Design Bundles paid planners, Joy of Motion 2026 crochet planner,
# 'crochet planner 2027' listings). Ours: fill it in on screen, print one clean page; four page types. Lead magnet to the 2027 planner.
PJP_SHEETS = [("project", "Project page"), ("tracker", "Row tracker"), ("yarn", "Yarn shopping list"), ("year", "2027 make list (whole year)")]
pjp_opts = "".join(f'<option value="{k}">{e(n)}</option>' for k, n in PJP_SHEETS)

def _pjp_field(i, label, ph="", typ="text"):
    return f'<div class="field"><label for="pjp-{i}">{label}</label><input type="{typ}" id="pjp-{i}" placeholder="{e(ph)}" maxlength="80"></div>'

pjpp = top("Free printable crochet project planner (fill in, then print)", "A crochet and knitting project planner you fill in on screen and print as one clean page: project page, row tracker, yarn shopping list and a whole-year 2027 make list. Leave a box empty and it prints as a blank line to write in.", "Crochet project planner") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> a good crochet project planner page has the <strong>pattern and size</strong>, the <strong>yarn</strong> (brand, weight, colour, dye lot, yards and skeins), the <strong>hook or needle size and gauge</strong>, <strong>start and due dates</strong>, a <strong>row tracker</strong> and space for <strong>notes on what you changed</strong>. Choose a page below, type in what you know, and press print. It's free, there's no sign-up, and the empty boxes print as lines to fill in by hand.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet" id="pjp-form">
<div class="row2"><div class="field"><label for="pjp-sheet">Page</label><select id="pjp-sheet">{pjp_opts}</select></div>
<div class="field"><label for="pjp-craft">Craft</label><select id="pjp-craft"><option value="Crochet">Crochet</option><option value="Knitting">Knitting</option><option value="Crochet and knitting">Both</option></select></div></div>
<div id="pjp-proj">
{_pjp_field("name", "Project name", "e.g. Mum's Christmas blanket")}
<div class="row2">{_pjp_field("pattern", "Pattern and designer", "")}{_pjp_field("size", "Size", "e.g. 50 x 60 in")}</div>
<div class="row2">{_pjp_field("yarn", "Yarn (brand, weight)", "e.g. worsted acrylic")}{_pjp_field("colour", "Colours and dye lot", "")}</div>
<div class="row2">{_pjp_field("yards", "Yards or skeins needed", "")}{_pjp_field("tool", "Hook or needle size", "e.g. 5 mm (H-8)")}</div>
<div class="row2">{_pjp_field("gauge", "Gauge", "e.g. 14 sts x 16 rows = 4 in")}{_pjp_field("for", "Made for", "")}</div>
<div class="row2">{_pjp_field("start", "Start date", "", "date")}{_pjp_field("due", "Due date", "", "date")}</div>
</div>
<div class="field" id="pjp-rows-f"><label for="pjp-rows">Rows or rounds to track</label><input type="number" id="pjp-rows" value="60" min="5" max="300" step="1" inputmode="numeric"></div>
<div class="btns"><button type="button" class="btn" id="pjp-print">Print or save as PDF</button> <button type="button" class="btn ghost" id="pjp-clear">Clear the boxes</button></div>
<p class="sub">Saved on this device only. Nothing is uploaded. In the print window choose "Save as PDF" to keep a copy.</p>
</div><div class="result" aria-live="polite"><h2>Preview</h2><div id="pjp-out" class="pjp-paper"></div></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>What to put on a crochet project planner page</h2>
<ul><li><strong>Pattern, designer and size.</strong> With a link or the book page, so you can find it again for the second sleeve.</li>
<li><strong>Yarn details from the label:</strong> brand, weight, fibre, colour name and <strong>dye lot</strong>. If you run short, the dye lot is what gets you a matching skein. Not sure how much to buy? The <a href="{href("yarn-calculator.html")}">yarn calculator</a> gives yards and skeins.</li>
<li><strong>Hook or needle size and your gauge.</strong> Write down your real gauge, not just the pattern's. The <a href="{href("gauge-converter.html")}">gauge converter</a> shows the size you'll get if they don't match.</li>
<li><strong>Dates.</strong> A due date turns "someday" into a plan. For gifts, check the hours with the <a href="{href("crochet-time-estimator.html")}">crochet time calculator</a> or the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>.</li>
<li><strong>A row tracker</strong> to tick as you go, and <strong>notes on every change</strong>: an extra repeat, a different hook for the border.</li>
<li><strong>Finishing checklist:</strong> weave in ends, block, add a label, photograph it. Our <a href="{href("how-to-weave-in-ends.html")}">weaving in ends guide</a> covers the first one.</li></ul>
<h2>How to use the row tracker</h2>
<p>Print it, clip it to your pattern and strike through a box at the end of each row or round. For patterns with a repeat, colour every 4th or 8th box first so you can see where each repeat starts. Prefer your phone? The online <a href="{href("row-counter.html")}">row counter</a> does the same with big buttons and keeps the screen awake.</p>
<h2>Planning a year of makes for 2027</h2>
<p>The make list page gives each month of 2027 a box. Start with fixed dates (birthdays, Christmas, a craft fair), work back from each one, and leave a few months light: a big blanket rarely fits round other projects. Pair it with the free <a href="{href("2027-calendar-printable.html")}">2027 calendar printable</a> to mark deadlines, and keep every work in progress in the online <a href="{href("projects.html")}">project tracker</a>.</p>
<h2>Tips for a planner you'll keep using</h2>
<ul><li>Keep one page per project in a ring binder or a clear sleeve in your project bag.</li>
<li>Staple a yarn label and a short snip of yarn to the page.</li>
<li>Note the hours and the cost of materials. Those two numbers are most of a fair price if you sell: see <a href="{href("how-to-price-crochet-items.html")}">how to price crochet items</a>.</li>
<li>When it's finished, add a photo and what you'd do differently. Next time you make it, it's all there.</li></ul>
<p class="note">The planner pages are our own layout. Everything you type stays in this browser and prints on your own printer; nothing is sent anywhere.</p>
</div></div></section>'''
pjp_faq = [
    ("What should be in a crochet project planner?", "The pattern and size, yarn details (brand, weight, colour, dye lot, yards and skeins), hook or needle size, your gauge, start and due dates, a row tracker and notes on any changes. A finishing checklist helps too."),
    ("Is this crochet planner printable free?", "Yes. Fill in as much as you like on screen, then print or save it as a PDF. There's no sign-up, and empty boxes print as lines to fill in by hand."),
    ("Can I use it for knitting?", "Yes. Choose Knitting and the page says needle size instead of hook size. The row tracker works for rows or rounds in either craft."),
    ("How do I print the planner as a PDF?", "Press 'Print or save as PDF', then choose 'Save as PDF' as the printer. Use 'Actual size' so the page fits A4 or US letter."),
    ("How do I keep track of rows in crochet?", "Strike through one box on a printed row tracker at the end of each row, use a stitch marker in the first stitch of each round, or use an online row counter on your phone."),
]
SHOP_FOR["crochet-project-planner.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-planner-budget"]
page("crochet-project-planner.html", "Free Printable Crochet Project Planner | Purl & Paper",
     "Free printable crochet and knitting project planner: fill in pattern, yarn, hook, gauge and dates, then print a project page, row tracker or 2027 make list.",
     pjpp, pjp_faq, "Crochet project planner", app_name="Crochet project planner printable")
