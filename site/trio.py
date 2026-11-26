# ---------------- 27 Nov 2026 run 8: ETSY SHIPPING CALCULATOR + HOW TO CROSS STITCH + HOW TO CROCHET A GRANNY SQUARE ----------------
# Executed from build.py after sellfab.py (shares page(), top(), href(), e(), SHOP_FOR, SELLER, NEW_CRAFTS via CRAFTS, GUIDES).
# Demand evidence in DEMAND.md (RADAR 26 Nov run 7 D4/D5, RADAR 27 Nov run 8). Drawings our own SVG; wording our own.
# JS in assets/app.js (sh-*, cx-*, gq-* features).
import json as _json

# ======== ETSY SHIPPING CALCULATOR ========
# Facts: Etsy charges the 6.5% transaction fee on the item price PLUS shipping and gift wrap, and the payment processing fee
# (US: 3% + $0.25) on the order total; Offsite Ads (15%, or 12% for shops over $10k/yr) also apply to the total incl. shipping
# (Etsy fees policy etsy.com/legal/fees; Etsy Help "How to Calculate Shipping Costs on Etsy"). US Free Shipping Guarantee: US listings
# that ship free on orders of $35+ get priority in US search (Etsy Help). USPS: Ground Advantage under 1 lb is priced in 4 oz steps
# (4, 8, 12, 15.99 oz); packages over 1 cubic foot (1,728 cu in) are priced by dimensional weight = L x W x H / 166 if that beats
# the scale weight (USPS Notice 123 / DMM). Label prices change: the user types the label cost from Etsy's calculator.
SH_FEE = 0.065 + 0.03

def sh_charge(label, pack, ads=0.0):
    return (label + pack) / (1 - SH_FEE - ads)

_sh_ex = sh_charge(5.20, 0.80)

def _sh_svg():
    return ('<svg viewBox="0 0 360 190" role="img" aria-label="A parcel with a shipping label: the shipping you charge has to cover the label, the packaging and the Etsy fees on shipping">'
            '<path d="M60 70 l90 -36 l110 30 l-90 40 z" fill="#e9dcc0" stroke="#1f2a44" stroke-width="2.5"/>'
            '<path d="M60 70 v76 l110 34 v-76 z" fill="#d7c39a" stroke="#1f2a44" stroke-width="2.5"/><path d="M170 104 l90 -40 v76 l-90 40 z" fill="#c9b385" stroke="#1f2a44" stroke-width="2.5"/>'
            '<path d="M105 52 l110 30 v16" stroke="#b8326a" stroke-width="6" fill="none"/>'
            '<rect x="82" y="102" width="62" height="40" rx="3" fill="#fbf8f1" stroke="#1f2a44" stroke-width="1.5" transform="skewY(17) translate(0 -30)"/>'
            '<path d="M90 92 h40 M90 100 h30 M90 108 h44" stroke="#5b6b94" stroke-width="2" transform="skewY(17) translate(0 -30)"/>'
            '<text x="300" y="40" font-size="13" fill="#1f2a44" font-family="Inter,sans-serif" text-anchor="middle">label</text>'
            '<text x="300" y="58" font-size="13" fill="#1f2a44" font-family="Inter,sans-serif" text-anchor="middle">+ box</text>'
            '<text x="300" y="76" font-size="13" fill="#b8326a" font-family="Inter,sans-serif" text-anchor="middle">+ fees</text></svg>')

SH_TIERS = "".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in [
    ("Up to 4 oz", "Earrings, stitch markers, a pattern booklet, a few cards"),
    ("4.01 to 8 oz", "A beanie, a crochet ornament set, a small amigurumi, a mini junk journal"),
    ("8.01 to 12 oz", "A chunky beanie, a cowl, a skein or two of yarn"),
    ("12.01 to 15.99 oz", "A scarf, a medium plush, a stack of dishcloths"),
    ("1 lb and over (per pound)", "Blankets, sweaters, chunky scarves, candles in jars"),
])

shp = top("Etsy shipping calculator: what to charge for shipping", "Type what the label costs and what your packaging costs, and see the shipping price that still covers Etsy's fees, or how much to add to your item price for free shipping. Includes a package weight and box size check.", "Etsy shipping calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> charge <strong>the label cost plus your packaging</strong>, then allow for Etsy's fees, because Etsy takes the <strong>6.5% transaction fee and the 3% payment processing fee on shipping too</strong> (US shops). Divide the label and packaging by about <strong>0.905</strong>: a $5.20 label and $0.80 of packaging means charging about <strong>${_sh_ex:.2f}</strong> for shipping, or adding that much to the item price if you offer free shipping.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="sh-label">Shipping label cost ($)</label><input type="number" id="sh-label" value="5.20" min="0" max="500" step="0.01" inputmode="decimal"></div>
<div class="field"><label for="sh-pack">Packaging per order ($)</label><input type="number" id="sh-pack" value="0.80" min="0" max="100" step="0.01" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="sh-price">Item price ($)</label><input type="number" id="sh-price" value="28" min="0" max="10000" step="0.01" inputmode="decimal"></div>
<div class="field"><label for="sh-ads">Offsite Ads on this order?</label><select id="sh-ads"><option value="0">No</option><option value="0.15">Yes, 15%</option><option value="0.12">Yes, 12% (shops over $10k a year)</option></select></div></div>
<p class="sub" style="margin:4px 0 6px"><strong>Package check</strong> (optional)</p>
<div class="row2"><div class="field"><label for="sh-wi">Item weight (oz)</label><input type="number" id="sh-wi" value="5" min="0" max="2000" step="0.1" inputmode="decimal"></div>
<div class="field"><label for="sh-wp">Packaging weight (oz)</label><input type="number" id="sh-wp" value="1.5" min="0" max="500" step="0.1" inputmode="decimal"></div></div>
<div class="row3"><div class="field"><label for="sh-l">Box length (in)</label><input type="number" id="sh-l" value="9" min="0" max="130" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="sh-w">Width (in)</label><input type="number" id="sh-w" value="6" min="0" max="130" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="sh-h">Height (in)</label><input type="number" id="sh-h" value="2" min="0" max="130" step="0.25" inputmode="decimal"></div></div>
<p class="sub">US Etsy fees. Find the label cost in your shipping profile with Etsy's calculated shipping, or on the carrier's site. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="sh-out" data-fee="{href("etsy-fee-calculator.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<figure class="sb-fig"><div>{_sh_svg()}<figcaption>Shipping you charge has to pay for three things, not one</figcaption></div></figure>
<h2>How to work out what to charge for shipping on Etsy</h2>
<ol><li><strong>Pack one order for real.</strong> Item, tissue, card, mailer or box. Weigh the whole parcel on a kitchen or postal scale and measure the box.</li>
<li><strong>Find the label price.</strong> In Shop Manager, a shipping profile with calculated shipping shows Etsy's discounted label price for your weight and size, or check the carrier's own calculator.</li>
<li><strong>Add packaging.</strong> Mailers, boxes, tape, tissue, stickers and a thank-you card. Most small shops spend between 50 cents and $2 an order.</li>
<li><strong>Cover the fees.</strong> Divide by 0.905 (or by 0.755 if the sale came from Offsite Ads at 15%), because the fees are a share of everything the buyer pays.</li>
<li><strong>Round up</strong> to a tidy price and set it in a shipping profile so every listing of that size uses it.</li></ol>
<h2>Charge for shipping or offer free shipping?</h2>
<p>Buyers on Etsy like free shipping, and in the US, listings that ship free on orders of <strong>$35 or more</strong> are given priority in Etsy's US search. Free shipping isn't free to you, though: you add the same amount to the item price instead. The calculator shows both. A common middle way is free shipping on bigger items like blankets and sweaters, where the cost hides well in the price, and a small shipping charge on low-priced items like ornaments and cards.</p>
<p>For several items in one order, use <strong>"additional item"</strong> prices in the shipping profile. A second beanie in the same mailer adds a few ounces, not a whole new label.</p>
<h2>Package weight: why ounces matter</h2>
<p>For light parcels, US postage jumps at fixed weights. USPS Ground Advantage, the usual service for small handmade items, is priced in 4 ounce steps under a pound, then by the pound. Shaving the packaging can drop you a step.</p>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Weight with packaging</th><th scope="col">Typical handmade items</th></tr></thead><tbody>{SH_TIERS}</tbody></table></div>
<p>Big, light parcels like a chunky blanket can cost more than their weight suggests. Once a box is over <strong>1 cubic foot</strong> (1,728 cubic inches), USPS charges by <strong>dimensional weight</strong>: length × width × height ÷ 166, in pounds, if that is more than the real weight. A 14 × 12 × 12 in box counts as about 12 lb even if the blanket weighs 3. A soft poly mailer, or vacuum-packing a blanket, often fixes it.</p>
<h2>Ways to keep shipping costs down</h2>
<ul><li><strong>Buy labels through Etsy.</strong> Etsy labels are usually cheaper than the post office counter price.</li>
<li><strong>Use mailers for soft items.</strong> Yarn makes don't break; a padded or poly mailer weighs less and stays small.</li>
<li><strong>Ship digital where you can.</strong> Patterns and printables have no shipping at all: our shop sells only digital files for this reason.</li>
<li><strong>Weigh, don't guess.</strong> An item an ounce over a step costs the difference on every order.</li></ul>
<p>Shipping is one part of the price. For the whole picture use the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>, work out a fair item price with <a href="{href("how-to-price-crochet-items.html")}">how to price crochet items</a>, and see <a href="{href("christmas-crafts-to-sell.html")}">Christmas crafts to make and sell</a> for ideas that ship light.</p>
<p class="note">Fees from Etsy's fees and payments policy and Help Center (US shops: 6.5% transaction fee and 3% + $0.25 payment processing on the order total including shipping; Offsite Ads 15% or 12%; US Free Shipping Guarantee at $35), and USPS weight steps and dimensional weight rules (checked 27 Nov 2026). Label prices change and depend on distance, so type your own. Not tax or legal advice.</p>
</div></div></section>'''
sh_faq = [
    ("How much should I charge for shipping on Etsy?", f"The label cost plus packaging, divided by about 0.905 to cover the 6.5% transaction fee and 3% processing fee Etsy takes on shipping. A $5.20 label and $0.80 of packaging means charging about ${_sh_ex:.2f}."),
    ("Does Etsy charge fees on shipping?", "Yes. In the US the 6.5% transaction fee and the 3% payment processing fee are charged on the whole order, shipping included. Offsite Ads fees apply to shipping too."),
    ("Is it better to offer free shipping on Etsy?", "Often, for items over about $35, because US listings with free shipping on $35+ orders get priority in Etsy's US search. Add the shipping cost to the item price so you don't lose money."),
    ("How do I calculate shipping weight?", "Weigh the item packed exactly as you'll send it: item, tissue, card and mailer. For boxes over 1 cubic foot, USPS uses length x width x height / 166 in pounds if that is more than the real weight."),
    ("How much does it cost to ship a crochet hat?", "A beanie in a poly mailer usually weighs 4 to 8 oz, so it ships in one of the lightest USPS Ground Advantage steps. Check the exact label price in your Etsy shipping profile."),
    ("Should I charge for packaging on Etsy?", "Yes, build it in. Mailers, tissue, tape and cards add up to 50 cents to $2 an order for most small shops."),
]
SHOP_FOR["etsy-shipping-calculator.html"] = ["small-business-pricing-inventory-spreadsheet", "crochet-knitting-pricing-calculator", "sublimation-tumbler-business-spreadsheet", "christmas-gift-tags"]
page("etsy-shipping-calculator.html", "Etsy Shipping Calculator: What to Charge for Shipping | Purl & Paper",
     "Free Etsy shipping calculator: label plus packaging, Etsy's 6.5% and 3% fees on shipping, what to add for free shipping, and a USPS weight and box check.",
     shp + more_seller("etsy-shipping-calculator.html"), sh_faq, "Etsy shipping calculator", app_name="Etsy shipping calculator")


# ======== HOW TO CROSS STITCH FOR BEGINNERS ========
# Demand: D4 'how to cross stitch for beginners' (SERP 26-27 Nov: Gathered x3, LoveCrafts, DMC, MasterClass, Sewing Trip,
# Stitched Modern, Cutesy Crafts, Craft Club Co). Needle/strand guide per fabric count as given by DMC and established
# needlework publishers (11ct 3 strands / tapestry 22; 14ct 2 / 24; 16ct 2 / 24-26; 18ct 1-2 / 26; 28ct evenweave over two 2 / 26;
# 32ct over two 1-2 / 28). Steps and drawings ours.
CX_FAB = [("11", "11-count Aida", 11, "3", "1-2", "22"), ("14", "14-count Aida (the usual beginner fabric)", 14, "2", "1", "24"),
          ("16", "16-count Aida", 16, "2", "1", "24 or 26"), ("18", "18-count Aida", 18, "1 or 2", "1", "26"),
          ("28", "28-count evenweave or linen, over two threads", 14, "2", "1", "26"), ("32", "32-count evenweave or linen, over two threads", 16, "1 or 2", "1", "28")]
cx_rows = "".join(f'<tr><td><strong>{e(n)}</strong></td><td>{spi}</td><td>{s}</td><td>{b}</td><td>{nd}</td></tr>' for k, n, spi, s, b, nd in CX_FAB)
cx_opts = "".join(f'<option value="{k}"{" selected" if k == "14" else ""}>{e(n)}</option>' for k, n, spi, s, b, nd in CX_FAB)
cx_data = _json.dumps({k: [spi, s, b, nd] for k, n, spi, s, b, nd in CX_FAB}, separators=(",", ":"))

def _cx_frame(inner, label, cols=7, rows=4):
    S = 34; W = cols * S + 20; H = rows * S + 40
    g = '<rect x="10" y="10" width="{}" height="{}" fill="#f6f1e6" stroke="#c9bfa6" stroke-width="1"/>'.format(cols * S, rows * S)
    for i in range(cols + 1):
        for j in range(rows + 1):
            g += f'<circle cx="{10 + i * S}" cy="{10 + j * S}" r="2.6" fill="#9b8f74"/>'
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(label)}">{g}{inner}</svg>'

def _leg(x1, y1, x2, y2, c="#b8326a", w=5, op=1):
    S = 34
    return f'<line x1="{10 + x1 * S}" y1="{10 + y1 * S}" x2="{10 + x2 * S}" y2="{10 + y2 * S}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'

def _num(x, y, t, c):
    S = 34
    return f'<circle cx="{10 + x * S}" cy="{10 + y * S}" r="9" fill="{c}"/><text x="{10 + x * S}" y="{10 + y * S + 4}" font-size="11" text-anchor="middle" fill="#fff" font-family="Inter,sans-serif">{t}</text>'

def _cx_cap(t, cols=7, rows=4):
    return f'<text x="{(cols * 34 + 20) / 2:.0f}" y="{rows * 34 + 32}" text-anchor="middle" font-size="13" fill="#1f2a44" font-family="Georgia,serif">{e(t)}</text>'

def cx_svgs():
    up, dn = "#2f8f8a", "#1f2a44"
    a = _leg(1, 3, 2, 2) + _num(1, 3, "1", up) + _num(2, 2, "2", dn) + _num(2, 3, "3", up) + _cx_cap("One half stitch: up at 1, down at 2")
    b = "".join(_leg(i, 3, i + 1, 2) for i in range(1, 6)) + "".join(_leg(i, 2, i + 1, 1, op=.3) for i in range(1, 6)) + _cx_cap("Work a row of half stitches ////")
    c = "".join(_leg(i, 3, i + 1, 2) for i in range(1, 6)) + "".join(_leg(i, 2, i + 1, 3, "#8e2353") for i in range(3, 6)) + _num(3, 2, "up", up) + _cx_cap("Come back \\\\\\ to finish each X")
    d = ('<path d="M44 40 q30 -26 60 0" stroke="#1f2a44" stroke-width="2" fill="none" stroke-dasharray="4 4"/>'
         + _leg(1, 3, 2, 2) + '<path d="M78 112 c-28 6 -40 -20 -34 -38" stroke="#b8326a" stroke-width="3" fill="none"/>'
         + '<ellipse cx="40" cy="70" rx="9" ry="14" fill="none" stroke="#b8326a" stroke-width="3"/>' + _cx_cap("Loop start: catch the loop at the back"))
    e_ = ("".join(_leg(i, 3, i + 1, 2, "#e3a8c1", 4) + _leg(i, 2, i + 1, 3, "#e3a8c1", 4) for i in range(1, 6))
          + '<path d="M44 96 h120 q14 0 14 -10" stroke="#1f2a44" stroke-width="3" fill="none"/>' + _cx_cap("Finish: weave under 4 or 5 stitches on the back"))
    return [(a, "Step 1: one half stitch on Aida, needle up at the bottom left hole and down at the top right"),
            (b, "Step 2: a row of half stitches all slanting the same way"),
            (c, "Step 3: coming back along the row with the other diagonal to make full crosses"),
            (d, "Loop start: a folded strand, the needle goes through the loop at the back so no knot is needed"),
            (e_, "Finishing: the thread is run under the backs of several stitches and trimmed")]

cx_figs = "".join(f'<figure class="gq-fig"><div>{_cx_frame(s, l)}<figcaption>{e(l.split(":")[0])}</figcaption></div></figure>' for s, l in cx_svgs())

cxp = top("How to cross stitch for beginners", "Everything you need for a first cross stitch, how to read the chart, and the stitch itself in five drawn steps, plus a helper that says which needle and how many strands for your fabric and where its centre is.", "How to cross stitch") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> put <strong>14-count Aida</strong> in a hoop and find its centre. Thread a <strong>size 24 tapestry needle</strong> with <strong>2 strands</strong> of embroidery floss, about 18 in (45 cm) long. Come up at the <strong>bottom left</strong> of a square and go down at the <strong>top right</strong>, then come up at the bottom right and go down at the top left to make an X. Start from the centre of the chart, keep every top stitch slanting the same way, and fasten off by weaving under the back of a few stitches. No knots.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="cx-fab">Your fabric</label><select id="cx-fab">{cx_opts}</select></div>
<div class="row2"><div class="field"><label for="cx-w">Pattern width (stitches)</label><input type="number" id="cx-w" value="80" min="1" max="2000" step="1" inputmode="numeric"></div>
<div class="field"><label for="cx-h">Pattern height (stitches)</label><input type="number" id="cx-h" value="60" min="1" max="2000" step="1" inputmode="numeric"></div></div>
<p class="sub">The chart's stitch count is usually printed beside it ("80w x 60h"). Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="cx-out" data-calc="{href("cross-stitch-calculator.html")}"></div></div></section>
<script type="application/json" id="cx-data">{cx_data}</script>
<section><div class="wrap"><div class="narrow prose">
<h2>What you need</h2>
<ul><li><strong>Aida fabric.</strong> A stiff cotton woven into little squares with a hole at each corner, so every stitch is easy to place. 14-count (14 squares to the inch) is the easiest to see.</li>
<li><strong>Embroidery floss.</strong> Six thin strands twisted together. You separate them and use two at a time on 14-count.</li>
<li><strong>A tapestry needle.</strong> Blunt tip and a long eye. It slides through the holes without splitting the fabric.</li>
<li><strong>An embroidery hoop</strong> a little bigger than the design, or a small frame, to keep the fabric tight.</li>
<li><strong>Small sharp scissors</strong> and the <strong>chart</strong>. A kit has all of it in one box, which is the easiest way to begin.</li></ul>
<h2>Needle and strands for every fabric count</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Fabric</th><th scope="col">Stitches per inch</th><th scope="col">Strands for crosses</th><th scope="col">Strands for backstitch</th><th scope="col">Tapestry needle</th></tr></thead><tbody>{cx_rows}</tbody></table></div>
<p>The higher the count, the smaller the stitches, the finer the needle and the fewer strands. Evenweave and linen are stitched over two threads, so 28-count gives 14 stitches to the inch, like 14-count Aida.</p>
<h2>Prepare the fabric</h2>
<ol><li><strong>Cut the fabric</strong> big enough for the design plus about 3 in (7.5 cm) on every side for framing. The <a href="{href("cross-stitch-calculator.html")}">cross stitch calculator</a> works this out.</li>
<li><strong>Stop the edges fraying</strong> with masking tape, a zigzag stitch or a line of fray stopper.</li>
<li><strong>Find the centre.</strong> Fold the fabric in half and in half again, and mark the middle with a pin or a few tacking stitches. Most charts mark their centre with arrows on the edges.</li>
<li><strong>Put it in the hoop</strong> and tighten until the fabric is firm like a drum.</li></ol>
<h2>How to make a cross stitch, step by step</h2>
<div class="gq-figs">{cx_figs}</div>
<ol><li><strong>Start without a knot.</strong> Knots make lumps under a framed piece. Either use a <strong>loop start</strong> (fold one strand in half, thread both ends, make your first half stitch and pass the needle through the loop at the back) or leave a 1 in tail at the back and hold it so your first few stitches cover it.</li>
<li><strong>Make a half stitch.</strong> Come up through the bottom left hole of a square and go down through the top right. That's one diagonal leg: /.</li>
<li><strong>Work a row.</strong> When the chart has several of the same colour side by side, make all the / legs along the row first.</li>
<li><strong>Come back.</strong> Work back along the row from bottom right to top left in each square, finishing every X: \\. This is the English or Danish method; it uses less floss and looks neat.</li>
<li><strong>Keep the top legs the same way.</strong> Every cross on the piece should have its top leg slanting the same direction. It's the single thing that makes work look smooth.</li>
<li><strong>Fasten off.</strong> Run the needle under the backs of 4 or 5 stitches on the wrong side and snip close. Don't carry thread more than about 3 squares across the back, or it will show through.</li></ol>
<h2>How to read a cross stitch chart</h2>
<p>Each square on the chart is one square of fabric. A symbol or colour in the square tells you the floss, and the <strong>key</strong> beside the chart matches each symbol to a thread number. Bold lines every 10 squares make counting easier. Solid lines across the squares are <strong>backstitch</strong>, usually done last with one strand to outline shapes. Half-filled squares are fractional stitches: quarter or three-quarter stitches for curves.</p>
<p>Stitch one colour in an area, then the next, working outwards from the centre so the design stays in the middle. Mark off what you've done with a pencil on a copy of the chart.</p>
<h2>Beginner mistakes to avoid</h2>
<ul><li><strong>Too many strands:</strong> stitches look lumpy and the holes stretch. Two strands on 14-count.</li>
<li><strong>Long threads:</strong> longer than 18 in and the floss twists and frays. Let the needle hang to untwist it now and then.</li>
<li><strong>Pulling tight:</strong> the holes distort. Stitches should sit flat on the fabric.</li>
<li><strong>Miscounting:</strong> count twice before starting a new area, and use the grid lines.</li>
<li><strong>Ironing the front:</strong> press finished work face down on a towel so the stitches stay raised.</li></ul>
<p>Want more stitches? Our <a href="{href("embroidery-stitches.html")}">embroidery stitches for beginners</a> covers backstitch, French knots and ten more, and the <a href="{href("embroidery-patterns.html")}">embroidery pattern generator</a> prints a free design to try. For the fabric and floss for a whole chart, use the <a href="{href("cross-stitch-calculator.html")}">cross stitch calculator</a>. Selling your finished pieces? Start with the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>.</p>
<p class="note">Needle sizes and strand counts follow DMC's beginner guidance and established needlework guides (Gathered, LoveCrafts; checked 27 Nov 2026). They're starting points: try a few stitches and use more or fewer strands for the coverage you like. Steps, wording and drawings are our own.</p>
</div></div></section>'''
cx_faq = [
    ("How do you cross stitch for beginners?", "Hoop 14-count Aida, thread a size 24 tapestry needle with 2 strands of floss, start in the centre without a knot, and make each X by coming up bottom left, down top right, then up bottom right and down top left."),
    ("How many strands do you use for cross stitch?", "2 strands on 14-count Aida, 3 on 11-count, and 1 or 2 on 18-count. Backstitch is usually 1 strand."),
    ("What needle do I use for cross stitch?", "A blunt tapestry needle: size 24 for 14-count Aida, 22 for 11-count, 26 for 18-count and 28-count evenweave."),
    ("Where do you start a cross stitch?", "In the centre. Fold the fabric in quarters to find the middle, find the centre arrows on the chart, and work outwards."),
    ("Do you tie a knot in cross stitch?", "No. Knots make lumps and can pull through. Use a loop start or hold a tail at the back and stitch over it, and finish by weaving under a few stitches."),
    ("Which way should the top stitch go in cross stitch?", "It doesn't matter which way, as long as every top leg on the piece slants the same direction."),
    ("How long should my floss be for cross stitch?", "About 18 in (45 cm). Longer threads twist, knot and wear thin."),
]
SHOP_FOR["how-to-cross-stitch.html"] = ["machine-embroidery-business-spreadsheet", "crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "christmas-gift-tags"]
page("how-to-cross-stitch.html", "How to Cross Stitch for Beginners (Step by Step) | Purl & Paper",
     "How to cross stitch for beginners: 14-count Aida, 2 strands, a size 24 needle, start in the centre with no knot. Five drawn steps, a chart guide and helper.",
     cxp, cx_faq, "How to cross stitch", app_name="Cross stitch needle and centre helper")


# ======== HOW TO CROCHET A GRANNY SQUARE ========
# Demand: 'how to crochet a granny square for beginners' (SERP 27 Nov: LoveCrafts x2, Gathered, Yahoo video tutorial, Skillshare x3,
# Ravelry beginner pattern, eHow, Hobbii, Vogue Knitting basics, Marching North, Yours). The classic granny (3-dc clusters, ch-2
# corners, ch-1 between clusters) is a traditional stitch pattern; wording ours. Size/yarn: our estimate, consistent with
# /granny-square-blanket-calculator (5-round worsted square ~5 in, ~25-30 yd).
def _gq_cluster(cx, cy, ang, col):
    import math as _m
    out = ""
    for k in (-1, 0, 1):
        a = _m.radians(ang + 90)
        ox, oy = cx + _m.cos(a) * k * 5, cy + _m.sin(a) * k * 5
        dx, dy = _m.cos(_m.radians(ang)) * 9, _m.sin(_m.radians(ang)) * 9
        out += f'<line x1="{ox - dx:.1f}" y1="{oy - dy:.1f}" x2="{ox + dx:.1f}" y2="{oy + dy:.1f}" stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>'
    return out

def gq_svg(rounds=4, size=300, label="Diagram of a classic granny square"):
    cols = ["#b8326a", "#2f8f8a", "#e39a14", "#5b6b94", "#8e2353", "#1f2a44"]
    c = size / 2; step = size / (2 * rounds + 1.4); out = f'<circle cx="{c}" cy="{c}" r="{step * .45:.1f}" fill="none" stroke="#1f2a44" stroke-width="2"/>'
    for n in range(1, rounds + 1):
        r = step * (n + .25); col = cols[(n - 1) % len(cols)]
        for i in range(n):
            t = -r + r * (2 * i + 1) / n
            out += _gq_cluster(c + t, c - r, 90, col) + _gq_cluster(c + t, c + r, 90, col) + _gq_cluster(c - r, c + t, 0, col) + _gq_cluster(c + r, c + t, 0, col)
    return f'<svg viewBox="0 0 {size} {size}" role="img" aria-label="{e(label)}"><rect x="2" y="2" width="{size - 4}" height="{size - 4}" rx="10" fill="#f6f1e6"/>{out}</svg>'

def gq_step_svg(kind, label=""):
    if kind == "ring":
        inner = ('<circle cx="120" cy="80" r="26" fill="none" stroke="#1f2a44" stroke-width="3"/>'
                 + "".join(f'<ellipse cx="{120 + 26 * x}" cy="{80 + 26 * y}" rx="7" ry="4" fill="none" stroke="#b8326a" stroke-width="2.5" transform="rotate({r} {120 + 26 * x} {80 + 26 * y})"/>' for x, y, r in [(0, -1, 0), (1, 0, 90), (0, 1, 0), (-1, 0, 90)])
                 + '<text x="120" y="140" text-anchor="middle" font-size="13" fill="#1f2a44" font-family="Georgia,serif">Ch 4, join with a slip stitch</text>')
    elif kind == "r1":
        inner = gq_svg(1, 160, "")[gq_svg(1, 160, "").index(">") + 1:-6].replace('<rect x="2" y="2" width="156" height="156" rx="10" fill="#f6f1e6"/>', "")
        inner = f'<g transform="translate(52 4) scale(.85)">{inner}</g>'
    else:
        inner = gq_svg(2, 160, "")[gq_svg(2, 160, "").index(">") + 1:-6].replace('<rect x="2" y="2" width="156" height="156" rx="10" fill="#f6f1e6"/>', "")
        inner = f'<g transform="translate(52 4) scale(.85)">{inner}</g>'
    return f'<svg viewBox="0 0 240 160" role="img" aria-label="{e(label)}"><rect x="0" y="0" width="240" height="160" rx="10" fill="#f6f1e6"/>{inner}</svg>'

gq_steps = "".join(f'<figure class="gq-fig"><div>{gq_step_svg(k, l)}<figcaption>{e(l)}</figcaption></div></figure>' for k, l in [("ring", "Start: a ring of 4 chains"), ("r1", "Round 1: four clusters"), ("r2", "Round 2: the corners")])

gqp = top("How to crochet a granny square for beginners", "The classic granny square round by round, with our own diagrams and a pattern writer that prints the rounds in US or UK terms for as many rounds as you want, plus the size and yarn to expect.", "How to crochet a granny square") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> chain 4 and join into a ring. <strong>Round 1:</strong> chain 3 (counts as a double crochet), 2 dc in the ring, chain 2, then [3 dc, ch 2] three more times and slip stitch to the top of the ch-3. You have 4 clusters of 3. <strong>Every round after:</strong> work <strong>(3 dc, ch 2, 3 dc) in each corner space</strong> and <strong>3 dc in each side space</strong>, with <strong>ch 1</strong> between clusters. Each round adds one cluster to every side. Five rounds in worsted yarn with a 5 mm hook make a square about 5 in (13 cm) across.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="gq-n">Rounds</label><input type="number" id="gq-n" value="5" min="1" max="20" step="1" inputmode="numeric"></div>
<div class="field"><label for="gq-t">Terms</label><select id="gq-t"><option value="us">US (dc)</option><option value="uk">UK (tr)</option></select></div></div>
<div class="row2"><div class="field"><label for="gq-c">Colours</label><select id="gq-c"><option value="1">One colour</option><option value="2">New colour every round</option></select></div>
<div class="field"><label for="gq-y">Yarn</label><select id="gq-y"><option value="dk">DK with a 4 mm hook</option><option value="w" selected>Worsted / aran with a 5 mm hook</option><option value="b">Bulky with a 6.5 mm hook</option></select></div></div>
<p class="sub">Sizes and yardage are our estimates for a classic granny at average tension. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="gq-out" data-bl="{href("granny-square-blanket-calculator.html")}"></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<div class="gq-figs">{gq_steps}</div>
<h2>What you need</h2>
<ul><li><strong>Yarn:</strong> smooth worsted or aran (medium, 4) in a light colour is easiest to see. Acrylic or cotton both work.</li>
<li><strong>Hook:</strong> the size on the yarn label, usually 5 mm (H-8) for worsted.</li>
<li><strong>Scissors and a tapestry needle</strong> to weave in the ends.</li>
<li><strong>Stitches:</strong> chain (ch), slip stitch (sl st) and double crochet (dc; treble, tr, in UK terms). If you're new to them, see <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>.</li></ul>
<h2>How to crochet a granny square, step by step</h2>
<ol><li><strong>Make the centre ring.</strong> Ch 4 and slip stitch into the first chain to close it. Prefer no hole in the middle? Use a <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a> instead.</li>
<li><strong>Round 1.</strong> Ch 3: this stands in for the first dc. Work 2 dc into the ring, then ch 2. *Work 3 dc into the ring, ch 2.* Repeat from * to * twice more. Slip stitch to the top of the first ch-3. You now have 4 groups of 3 dc (clusters) with 4 ch-2 spaces: those are the corners.</li>
<li><strong>Move to a corner.</strong> Slip stitch into the next 2 dc and into the ch-2 space. (Changing colour? Fasten off and join the new colour in any corner space instead.)</li>
<li><strong>Round 2.</strong> Ch 3, then (2 dc, ch 2, 3 dc) in that same corner space. Ch 1. *(3 dc, ch 2, 3 dc) in the next corner space, ch 1.* Repeat from * twice more and slip stitch to the top of the ch-3. Each corner now has two clusters.</li>
<li><strong>Round 3.</strong> Move to a corner as before. Ch 3, (2 dc, ch 2, 3 dc) in the corner, ch 1, then 3 dc in the ch-1 space along the side, ch 1. Do a corner, ch 1, side cluster, ch 1 the rest of the way round, and join.</li>
<li><strong>Keep going.</strong> Every round: two clusters with ch 2 between them in each corner, one cluster in every ch-1 space along the sides, ch 1 between them all. Round 4 has 2 clusters on each side, round 5 has 3.</li>
<li><strong>Finish.</strong> Cut the yarn leaving 6 in, pull it through the last loop, and <a href="{href("how-to-weave-in-ends.html")}">weave in the ends</a>. Block the square (pin it flat and mist it) so all your squares match before joining.</li></ol>
<h2>Granny square diagram</h2>
<figure class="sb-fig"><div>{gq_svg(4, 300, "Diagram of a classic four-round granny square: each round in a new colour, clusters of three stitches, two clusters at each corner")}<figcaption>Four rounds: each colour is one round. Every round adds one cluster to each side.</figcaption></div></figure>
<h2>Granny square stitch counts by round</h2>
<p>Round <em>n</em> has <strong>4 × n clusters</strong>, so 12 × n double crochets: 12 in round 1, 24 in round 2, 36 in round 3, 48 in round 4 and 60 in round 5. Along each side, between the corners, there are n minus 2 clusters from round 2 onwards. Counting clusters is the quickest way to spot a missed space.</p>
<h2>Common granny square problems</h2>
<ul><li><strong>Square twists or turns into a swirl:</strong> it's normal for granny squares to lean a little because you never turn. Some crocheters turn the work at the end of each round to straighten it. Blocking also fixes most of it.</li>
<li><strong>Corners look rounded:</strong> make sure the corner has ch 2 (some people use ch 3 with thicker yarn) and both clusters go into the same space.</li>
<li><strong>Square ruffles or cups:</strong> ch 1 between clusters is too loose or too tight. Try ch 1 loose, or skip it with a smaller hook.</li>
<li><strong>A gap where the round joins:</strong> join into the top of the ch-3, not the space beside it. Or try a standing double crochet to start rounds.</li>
<li><strong>Wrong number of clusters:</strong> count: 4 corners × 2, plus n minus 2 on each side.</li></ul>
<h2>What to make with granny squares</h2>
<p>Blankets, of course: the <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> says how many squares and how much yarn for any size. When the squares are done, see <a href="{href("how-to-join-granny-squares.html")}">how to join granny squares</a> (five methods, including join as you go). Also cushions (two big squares), tote bags, cardigans from six squares, coasters (a 3-round square) and Christmas ornaments. Want to plan colours? Try the <a href="{href("stripe-generator.html")}">random stripe generator</a> for round colours, and keep count with the <a href="{href("row-counter.html")}">row counter</a>. Selling them? See <a href="{href("how-to-price-a-crochet-blanket.html")}">how to price a crochet blanket</a>.</p>
<p class="note">The classic granny square is a traditional crochet pattern; the steps match how established crochet publishers teach it (LoveCrafts, Gathered, Vogue Knitting, Hobbii; checked 27 Nov 2026). Our wording and diagrams. Sizes and yardage are estimates: your tension, hook and yarn change them, so measure your first square.</p>
</div></div></section>'''
gq_faq = [
    ("How do you crochet a granny square for beginners?", "Ch 4 and join. Round 1: ch 3, 2 dc in the ring, ch 2, then [3 dc, ch 2] three times and join. Every later round: (3 dc, ch 2, 3 dc) in each corner and 3 dc in each side space, with ch 1 between clusters."),
    ("How many chains do you start a granny square with?", "Chain 4 and join into a ring with a slip stitch. Some patterns use ch 5 or a magic ring, which closes the centre hole."),
    ("How big is a 5 round granny square?", "About 5 in (13 cm) in worsted yarn with a 5 mm hook, by our estimate. DK makes it closer to 4 in and bulky yarn about 6.5 in."),
    ("How much yarn does one granny square take?", "Roughly 25 to 30 yards for a 5 in, 5-round worsted square. Weigh one finished square to know exactly."),
    ("Why is my granny square twisting?", "Working in the round without turning makes stitches lean. Turn the work at the end of each round or block the finished squares to straighten them."),
    ("Is a granny square double crochet or treble?", "The same stitch, two names: double crochet (dc) in US terms is treble crochet (tr) in UK terms."),
    ("How many clusters are in each round of a granny square?", "Round n has 4 x n clusters of 3 stitches: 4 in round 1, 8 in round 2, 12 in round 3 and so on."),
]
SHOP_FOR["how-to-crochet-a-granny-square.html"] = ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("how-to-crochet-a-granny-square.html", "How to Crochet a Granny Square for Beginners | Purl & Paper",
     "How to crochet a granny square: ch 4 ring, round 1 of four 3-dc clusters, then (3 dc, ch 2, 3 dc) in each corner. Diagrams, US/UK pattern writer and yarn.",
     gqp, gq_faq, "How to crochet a granny square", app_name="Granny square pattern writer")
