# ---------------- 26 Nov 2026 run 7: FABRIC YARDAGE CALCULATOR + CHRISTMAS CRAFTS TO SELL + JUNK JOURNAL VS SCRAPBOOK ----------------
# Executed from build.py after sewplan.py (shares page(), top(), href(), e(), SHOP_FOR).
# Demand evidence in DEMAND.md (EVENING RADAR R1/R3, RADAR run 6 B5). Drawings our own SVG; wording our own.
# JS in assets/app.js (fy-*, cs-*, jvs-* features), CSS in assets/style.css.
import json as _json, math as _math

# ======== FABRIC YARDAGE CALCULATOR ========
# Bolt widths: quilting cotton 42-45 in (about 42 usable without selvedges), apparel/home decor 54 in, knits and many apparel
# fabrics 58-60 in, wide backing 108 in; metric 112, 140, 150 cm. 1 yd = 36 in = 91.44 cm; fabric is cut in 1/8 yd (4.5 in) steps
# in US shops. Pre-washing cotton shrinks it, so guides add extra. Sources: Melly Sews yardage guide, Cashmerette "how much fabric
# do I need" (2025), Sew Guide fabric measurements, AllFreeSewing yardage charts (SERP 26 Nov 2026). Layout maths is ours.
FY_WIDTHS = [("42", "44/45 in quilting cotton (112 cm): plan on 42 in"), ("52", "54 in home decor (137 cm): plan on 52 in"),
             ("57", "58/60 in apparel and knits (150 cm): plan on 57 in"), ("106", "108 in wide backing (274 cm): plan on 106 in"), ("own", "Other width")]

def fy_len(pieces, FW, rotate=True):
    """Simple straight-grain layout: each piece type in its own rows across the width. Returns total length in the same unit."""
    tot = 0
    for w, h, q in pieces:
        best = None
        for a, b in ([(w, h), (h, w)] if rotate else [(w, h)]):
            if a <= FW + 1e-9:
                per = int(FW // a + 1e-9); L = _math.ceil(q / per) * b
                best = L if best is None else min(best, L)
        if best is None: return None
        tot += best
    return tot

def fy_yd(L, extra=0.05):
    return _math.ceil(L * (1 + extra) / 4.5 - 1e-9) / 8

def _yfr(y):
    w = int(y + 1e-9); f = round((y - w) * 8)
    F = ["", "⅛", "¼", "⅜", "½", "⅝", "¾", "⅞"][f]
    return (str(w) if w else "") + F + " yd"

FY_PROJ = [("cushion", "16 in envelope cushion cover", [(17, 17, 1), (17, 12, 2)]),
           ("pillowcase", "Standard pillowcase with cuff", [(41, 27, 1), (41, 10, 1)]),
           ("tote", "Tote bag, 14 x 16 in (outer only)", [(15, 17, 2), (4, 24, 2)]),
           ("giftbags", "6 drawstring gift bags, 8 x 10 in", [(9, 22, 6)]),
           ("napkins", "4 cloth napkins, 18 in", [(19, 19, 4)]),
           ("placemats", "4 placemats, 13 x 19 in (fronts)", [(14, 20, 4)]),
           ("apron", "Simple adult apron with ties", [(26, 32, 1), (3, 36, 2)])]

def _cutlist(p): return ", ".join(f"{q} x {w} x {h} in" for w, h, q in p)

fy_proj_rows = "".join(f'<tr><td><strong>{e(n)}</strong><br><small>{_cutlist(p)}</small></td><td>{_yfr(fy_yd(fy_len(p, 42)))}</td><td>{_yfr(fy_yd(fy_len(p, 57)))}</td><td>{round(fy_yd(fy_len(p, 42)) * 0.9144 + 0.049, 1)} m</td></tr>' for k, n, p in FY_PROJ)
fy_frac_rows = "".join(f'<tr><td><strong>{_yfr(i / 8)}</strong></td><td>{i * 4.5:g} in</td><td>{i * 4.5 * 2.54:.1f} cm</td></tr>' for i in range(1, 9))
fy_data = _json.dumps({k: {"n": n, "p": p} for k, n, p in FY_PROJ}, separators=(",", ":"))
fy_opts = "".join(f'<option value="{v}"{" selected" if v == "42" else ""}>{e(n)}</option>' for v, n in FY_WIDTHS)
fy_popts = '<option value="">Choose an example (optional)</option>' + "".join(f'<option value="{k}">{e(n)}</option>' for k, n, p in FY_PROJ)
_fy_c = fy_yd(fy_len(FY_PROJ[0][2], 42))

def _fy_row(i, w, h, q):
    return (f'<div class="fy-row"><span class="fy-n">{"ABC"[i]}</span><div class="field"><label for="fy-w{i}">Width</label><input type="number" id="fy-w{i}" value="{w}" min="0" max="400" step="0.25" inputmode="decimal"></div>'
            f'<div class="field"><label for="fy-h{i}">Length</label><input type="number" id="fy-h{i}" value="{h}" min="0" max="400" step="0.25" inputmode="decimal"></div>'
            f'<div class="field"><label for="fy-q{i}">How many</label><input type="number" id="fy-q{i}" value="{q}" min="0" max="200" step="1" inputmode="numeric"></div></div>')

def _fy_svg():
    s = 6; W = 42 * s
    r = [(0, 0, 17, 17, "#2f8f8a"), (17, 0, 17, 17, "#b8326a"), (0, 17, 17, 12, "#e39a14"), (17, 17, 17, 12, "#e39a14")]
    out = "".join(f'<rect x="{10 + x * s + 1}" y="{10 + y * s + 1}" width="{w * s - 2}" height="{h * s - 2}" rx="3" fill="{c}" opacity=".85"/>' for x, y, w, h, c in r)
    return (f'<svg viewBox="0 0 {W + 20} {29 * s + 52}" role="img" aria-label="Layout on 42 inch wide fabric: a 17 inch cushion front and spare space on the top row, two 17 by 12 inch back panels on the next row, 29 inches long in total">'
            f'<rect x="10" y="10" width="{W}" height="{29 * s}" fill="#f3ede2" stroke="#1f2a44" stroke-width="2"/>{out}'
            f'<path d="M{W + 4} 10 v{29 * s}" stroke="#5b6b94" stroke-width="2" stroke-dasharray="4 4"/>'
            f'<text x="{W / 2 + 10:.0f}" y="{29 * s + 36}" text-anchor="middle" font-size="14" fill="#1f2a44" font-family="Georgia,serif">42 in wide · 29 in long: 1 front, 2 backs</text></svg>')

fyp = top("Fabric yardage calculator: how much fabric do I need?", "Type the size of each piece you need to cut and the width of your fabric, and get the yardage to buy, rounded up to the next ⅛ yard, with a to-scale cutting layout. Inches or cm, with extra for shrinkage.", "Fabric yardage calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> work out how many pieces fit <strong>across the usable width</strong> of the fabric (about <strong>42 in</strong> on 44/45 in quilting cotton, 57 in on 60 in fabric), multiply the rows you need by the <strong>length of each piece</strong>, add about <strong>5 to 10% for shrinkage</strong> and straightening, then divide by 36 and round up to the next ⅛ yard. A 16 in envelope cushion cover (one 17 in front and two 17 x 12 in backs) takes about <strong>{_yfr(_fy_c)}</strong> of 44 in fabric.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="fy-proj">Start from an example</label><select id="fy-proj">{fy_popts}</select></div>
<div class="row2"><div class="field"><label for="fy-u">Units</label><select id="fy-u"><option value="in">inches</option><option value="cm">cm</option></select></div>
<div class="field"><label for="fy-fw">Fabric width</label><select id="fy-fw">{fy_opts}</select></div></div>
<div class="field" id="fy-own-f" hidden><label for="fy-own">Usable fabric width (same units, without selvedges)</label><input type="number" id="fy-own" value="42" min="5" max="400" step="0.5" inputmode="decimal"></div>
<p class="sub" style="margin-bottom:6px"><strong>Pieces to cut</strong> (cut sizes, with seam allowance)</p>
{_fy_row(0, 17, 17, 1)}{_fy_row(1, 17, 12, 2)}{_fy_row(2, "", "", "")}
<div class="row2"><div class="field"><label for="fy-sa">Add seam allowance to every edge</label><select id="fy-sa"><option value="0">No, sizes include it</option><option value="0.25">¼ in (6 mm)</option><option value="0.5">½ in (1.2 cm)</option><option value="0.625">⅝ in (1.5 cm)</option></select></div>
<div class="field"><label for="fy-x">Extra for shrinkage and straightening</label><select id="fy-x"><option value="0">None (pre-washed)</option><option value="0.05" selected>5%</option><option value="0.1">10% (cotton, linen, flannel)</option></select></div></div>
<label class="chk"><input type="checkbox" id="fy-dir"> One-way print or nap (don't turn pieces sideways)</label>
<p class="sub">Saved on this device only. Nothing is uploaded.</p>
</div><div class="result" aria-live="polite" id="fy-out" data-sa="{href("sewing-seam-allowance.html")}"></div></div></section>
<script type="application/json" id="fy-data">{fy_data}</script>
<section><div class="wrap"><div class="narrow prose">
<figure class="sb-fig"><div>{_fy_svg()}<figcaption>How the calculator lays out a 16 in cushion cover on 44 in fabric</figcaption></div></figure>
<h2>How to calculate fabric yardage</h2>
<ol><li><strong>List every piece</strong> with its cut size, seam allowance included. If the pattern gives finished sizes, add the allowance on each sewn edge (our <a href="{href("sewing-seam-allowance.html")}">seam allowance guide</a> explains how).</li>
<li><strong>Check the usable width.</strong> The selvedges (the tightly woven edges) aren't used, so 44/45 in quilting cotton gives about 42 in, and 60 in fabric about 57 in.</li>
<li><strong>Count pieces across.</strong> Usable width ÷ piece width, rounded down. A 17 in piece fits twice across 42 in.</li>
<li><strong>Count rows.</strong> Pieces needed ÷ pieces per row, rounded up, times the piece length.</li>
<li><strong>Add the rows together</strong>, add 5 to 10% for shrinkage and a straight first cut, then divide by 36 for yards (or by 100 for metres) and round up to the next ⅛ yard or 10 cm.</li></ol>
<p>Turning a piece sideways often saves fabric, and the calculator tries both ways. Don't turn pieces on <strong>one-way prints</strong> (animals that would end up lying down) or fabrics with a <strong>nap</strong> like velvet and corduroy, where the colour changes with direction. Tick the box and it keeps everything upright.</p>
<h2>How much fabric for common projects</h2>
<p>Our own example cut lists, with ½ in seams included and 5% extra, rounded up to the next ⅛ yard:</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Project and cut list</th><th scope="col">44/45 in fabric</th><th scope="col">58/60 in fabric</th><th scope="col">Metric (112 cm)</th></tr></thead><tbody>{fy_proj_rows}</tbody></table></div>
<p>These are estimates for simple straight-cut shapes. A printed pattern's yardage chart always wins, because curved pieces and sleeves nest together in ways a simple layout can't. Quilt? Use the <a href="{href("quilt-size-calculator.html")}">quilt size calculator</a> for backing and binding, and the <a href="{href("fat-quarter-calculator.html")}">fat quarter calculator</a> for squares from precuts.</p>
<h2>Fabric widths</h2>
<ul><li><strong>44/45 in (112 cm):</strong> quilting cotton and most craft cottons. Plan on 42 in.</li>
<li><strong>54 in (137 cm):</strong> home decor, upholstery and canvas.</li>
<li><strong>58/60 in (150 cm):</strong> knits, fleece, many apparel fabrics and linens.</li>
<li><strong>108 in (274 cm):</strong> wide quilt backing: no seam down the back of a quilt.</li></ul>
<p>The same project can need much less of a wider fabric. The tote above takes less on 60 in fabric because both straps fit side by side across the width.</p>
<h2>Yard fractions in inches and cm</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Cut</th><th scope="col">Inches</th><th scope="col">Centimetres</th></tr></thead><tbody>{fy_frac_rows}</tbody></table></div>
<p>1 yard is 36 in or 91.44 cm, so 1 metre is about 1.09 yards. A fat quarter (18 x 22 in) is a quarter yard cut squarer, not a ¼ yard cut across the bolt.</p>
<h2>Tips before you buy</h2>
<ul><li><strong>Pre-wash</strong> cotton, linen and rayon the way you'll wash the finished item. They can shrink several percent, mostly in length.</li>
<li><strong>Matching stripes, plaids or a big repeat</strong> needs more: add one pattern repeat per piece you want to match.</li>
<li><strong>Buy enough at once.</strong> Dye lots vary, so a second trip for the same print may not match.</li>
<li><strong>Selling what you sew?</strong> Count the fabric cost per piece in your price with the <a href="{href("how-to-price-crochet-items.html")}">handmade pricing method</a> (it works for sewing too), or see our <a href="{href("christmas-crafts-to-sell.html")}">Christmas crafts to make and sell</a>.</li></ul>
<p class="note">Fabric widths and the advice to add extra for shrinkage are as described by sewing guides (Melly Sews, Cashmerette, Sew Guide, AllFreeSewing; checked 26 Nov 2026). The layout and yardage figures are our own maths and are estimates: real layouts, directional prints and pattern matching change them.</p>
</div></div></section>'''
fy_faq = [
    ("How do I calculate how much fabric I need?", "Find how many pieces fit across the usable fabric width, multiply the number of rows by the piece length, add 5 to 10% for shrinkage, divide by 36 and round up to the next ⅛ yard."),
    ("How much fabric do I need for a 16 inch cushion cover?", f"About {_yfr(_fy_c)} of 44 in fabric for an envelope cover: one 17 x 17 in front and two 17 x 12 in back panels with ½ in seams."),
    ("How many inches is ⅛ of a yard?", "4½ inches (11.4 cm). A ¼ yard is 9 in, ½ yard is 18 in and ¾ yard is 27 in."),
    ("What is the usable width of 45 inch fabric?", "About 42 inches once the selvedges are cut off. Quilting patterns usually plan on 40 to 42 in."),
    ("How much extra fabric should I buy for shrinkage?", "About 5% for most fabric and around 10% for cotton, linen and flannel you'll pre-wash. Add one pattern repeat per piece if you need to match a print."),
    ("Is a metre more than a yard?", "Yes. 1 metre is 39.37 in, about 1.09 yards; 1 yard is 91.44 cm."),
    ("How much fabric do I need for a tote bag?", "About ¾ yard of 44 in fabric for a 14 x 16 in tote with two 4 in straps (outer only). Add the same again for a lining."),
]
SHOP_FOR["fabric-yardage-calculator.html"] = ["small-business-pricing-inventory-spreadsheet", "crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "christmas-gift-tags"]
page("fabric-yardage-calculator.html", "Fabric Yardage Calculator: How Much Fabric Do I Need? | Purl & Paper",
     "Free fabric yardage calculator: enter your pieces and fabric width (44, 54, 60 or 108 in) to get the yards or metres to buy, with a cutting layout.",
     fyp, fy_faq, "Fabric yardage calculator", app_name="Fabric yardage calculator")


# ======== CHRISTMAS CRAFTS TO MAKE AND SELL ========
# Demand: 'christmas crafts to make and sell' / 'for adults to make and sell' (Google autocomplete #4/#7, 26 Nov 2026).
# SERP: The Penny Hoarder 15 holiday crafts, Small Business Trends (3 versions), Unexpectedly Domestic 101 crafts to sell,
# Gumtree "easy Christmas crafts to make and sell", MoneyPantry, xTool. All lists; none put a price on each idea for YOUR wage.
# Materials and hours are our own rough estimates (labelled). Price method = our pricing guide: (materials + hours x rate) x 1.1
# overheads, then Etsy fees (6.5% transaction + 3% + $0.25 processing + $0.20 listing, US) or ~3% card fee at a fair.
CS = [("Crochet or knit beanie", "yarn", 6, 2.5, "The classic gift. Chunky yarn halves the time. Offer sizes from baby to adult.", "hat-size-chart.html"),
      ("Crochet Christmas ornaments (set of 3)", "yarn", 2, 1.5, "Baubles, stars and mini stockings. Sell in sets: one ornament is hard to price fairly.", "crochet-circle-calculator.html"),
      ("Mini Christmas stocking", "yarn", 3, 2, "Gift card holders and tree decorations. Add a name for a higher price.", "christmas-stocking-calculator.html"),
      ("Full-size Christmas stocking", "yarn", 9, 6, "A keepsake. Take name orders by early December.", "christmas-stocking-calculator.html"),
      ("Chunky scarf", "yarn", 12, 4, "Super bulky yarn sells well at winter fairs. Price the yarn honestly: it adds up.", "scarf-size-chart.html"),
      ("Ear warmer headband", "yarn", 4, 1.5, "Quick, uses up leftover yarn, easy to make in stacks.", "hat-size-chart.html"),
      ("Amigurumi gnome or small toy", "yarn", 4, 3, "Gnomes, snowmen and reindeer. Use safety eyes or embroider them for babies.", "how-to-price-amigurumi.html"),
      ("Coasters (set of 4)", "yarn", 3, 1.5, "Cotton yarn, festive colours, tied with a ribbon.", "crochet-circle-calculator.html"),
      ("Cotton dishcloths (set of 3)", "yarn", 4, 2, "Useful gifts that sell all year. Pair with a bar of soap.", "how-to-crochet-a-dishcloth.html"),
      ("Drawstring gift bags (set of 3)", "sewing", 4, 1, "Reusable wrapping. Christmas fabric, ribbon drawstring.", "fabric-yardage-calculator.html"),
      ("Mug rugs or potholders (pair)", "sewing", 5, 1.5, "Scrap-friendly quilting. Use insulated batting for potholders.", "fat-quarter-calculator.html"),
      ("Scrunchies (set of 3)", "sewing", 3, 0.75, "Stocking fillers at a low price point; velvet sells well in winter.", "fabric-yardage-calculator.html"),
      ("Embroidery hoop ornament with a name", "sewing", 3, 1.5, "Small hoops, one name or a simple motif. Personalised items earn more.", "embroidery-stitches.html"),
      ("Handmade Christmas cards (pack of 5)", "paper", 4, 1.5, "Matching envelopes make them look shop-bought. Price per pack.", "card-making.html"),
      ("Mini junk journal", "paper", 8, 6, "Christmas or winter themed, with pockets and tags. A slower make for a higher price.", "junk-journal-beginners.html"),
      ("Paper flower bouquet or wreath", "paper", 5, 2.5, "Long-lasting table decorations. Cardstock in reds, whites and greens.", "paper-flowers.html"),
      ("Soy container candle (8 oz)", "other", 5, 0.5, "Pour in batches: the time per candle drops fast. Follow fragrance load limits and add warning labels.", "candle-making-calculator.html"),
      ("Resin ornament", "other", 3, 0.5, "Pressed flowers or glitter in a mould. Allow full cure time before you pack them.", "resin-calculator.html"),
      ("Macrame ornament or mini wall hanging", "other", 5, 1.5, "Natural cord, quick knots, ships flat.", "macrame-cord-calculator.html")]
CS_GROUPS = [("all", "All crafts"), ("yarn", "Crochet and knitting"), ("sewing", "Sewing and embroidery"), ("paper", "Paper crafts"), ("other", "Candles, resin and macrame")]

def cs_price(m, h, rate=15, where="etsy"):
    base = (m + h * rate) * 1.1
    if where == "etsy": return (base + 0.45) / 0.905
    if where == "fair": return base / 0.97
    return base

def _usd(x): return "$" + str(int(_math.ceil(x)))

cs_rows = "".join(f'<tr data-g="{g}"><td><strong><a href="{href(l)}">{e(n)}</a></strong><br><small>{e(t)}</small></td><td>${m}</td><td>{h:g} h</td><td><strong>{_usd(cs_price(m, h))}</strong></td></tr>' for n, g, m, h, t, l in CS)
cs_data = _json.dumps([[n, g, m, h] for n, g, m, h, t, l in CS], separators=(",", ":"))
cs_gopts = "".join(f'<option value="{k}">{e(n)}</option>' for k, n in CS_GROUPS)
_cs_b = cs_price(6, 2.5)

def _cs_svg():
    return ('<svg viewBox="0 0 360 210" role="img" aria-label="A price tag split into materials, your time, overheads and selling fees">'
            '<path d="M40 40 h230 l50 65 l-50 65 h-230 z" fill="#f3ede2" stroke="#1f2a44" stroke-width="2.5"/><circle cx="285" cy="105" r="9" fill="#fbf8f1" stroke="#1f2a44" stroke-width="2"/>'
            '<rect x="55" y="58" width="40" height="94" fill="#2f8f8a"/><rect x="95" y="58" width="120" height="94" fill="#b8326a"/><rect x="215" y="58" width="22" height="94" fill="#e39a14"/><rect x="237" y="58" width="22" height="94" fill="#5b6b94"/>'
            '<text x="75" y="190" text-anchor="middle" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">materials</text>'
            '<text x="155" y="190" text-anchor="middle" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">your time</text>'
            '<text x="226" y="30" text-anchor="middle" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">overheads</text>'
            '<text x="262" y="190" text-anchor="middle" font-size="12" fill="#1f2a44" font-family="Inter,sans-serif">fees</text>'
            '<text x="155" y="111" text-anchor="middle" font-size="16" fill="#fff" font-family="Georgia,serif">the biggest part</text></svg>')

csp = top("Christmas crafts to make and sell (with prices that pay you)", "19 Christmas crafts adults can make and sell, from crochet ornaments and beanies to candles and cards, each with rough material costs, making time and a price worked out for your own hourly rate.", "Christmas crafts to sell") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the Christmas crafts that sell best are <strong>quick, giftable and easy to make in batches</strong>: crochet ornaments, beanies and ear warmers, mini stockings, gift bags, scrunchies, cards, candles and resin ornaments. Personalised makes (a name on a stocking or hoop) earn more. Price each one as <strong>materials + your hours × an hourly rate</strong>, plus about 10% for overheads and the selling fees: a beanie with $6 of yarn and 2½ hours at $15 an hour is about <strong>{_usd(_cs_b)}</strong> on Etsy.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="cs-rate">Your hourly rate ($)</label><input type="number" id="cs-rate" value="15" min="0" max="200" step="1" inputmode="decimal"></div>
<div class="field"><label for="cs-where">Where you sell</label><select id="cs-where"><option value="etsy">Etsy (US fees)</option><option value="fair">Craft fair (card reader ~3%)</option><option value="none">No fees (cash, friends)</option></select></div></div>
<div class="row2"><div class="field"><label for="cs-g">Craft</label><select id="cs-g">{cs_gopts}</select></div>
<div class="field"><label for="cs-max">Most hours per item</label><select id="cs-max"><option value="99">Any</option><option value="1">1 hour or less</option><option value="2">2 hours or less</option><option value="3">3 hours or less</option></select></div></div>
<p class="sub">Materials and hours are rough estimates for a confident beginner. Change your rate and every price updates. Saved on this device only.</p>
</div><div class="result" aria-live="polite" id="cs-out" data-fee="{href("etsy-fee-calculator.html")}"></div></div></section>
<script type="application/json" id="cs-data">{cs_data}</script>
<section><div class="wrap"><div class="narrow prose">
<h2>19 Christmas crafts to sell, with prices</h2>
<p>Prices below are at $15 an hour, sold on Etsy (estimates: your materials and speed will differ). Each idea links to a free tool that helps you make it.</p>
<div class="tbl-wrap"><table id="cs-table"><thead><tr><th scope="col">Craft</th><th scope="col">Materials</th><th scope="col">Time</th><th scope="col">Price</th></tr></thead><tbody>{cs_rows}</tbody></table></div>
<figure class="sb-fig"><div>{_cs_svg()}<figcaption>Your time is the biggest part of a fair handmade price</figcaption></div></figure>
<h2>How to price Christmas crafts</h2>
<ol><li><strong>Materials:</strong> the share of yarn, fabric, wax or paper the item uses, plus labels and packaging.</li>
<li><strong>Time:</strong> your real hours times a rate you'd be happy to earn. Time yourself on the first one.</li>
<li><strong>Overheads:</strong> about 10% for tools, electricity, card fees and photos.</li>
<li><strong>Fees:</strong> on Etsy, the transaction and payment processing fees come out of each sale. The <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a> shows the exact amount, and the <a href="{href("craft-fair-profit-calculator.html")}">craft fair profit calculator</a> checks whether a booth fee is worth it.</li></ol>
<p>If a price feels too high for your market, don't cut your rate: pick a faster make, use cheaper materials, or sell a set. Our full guide to <a href="{href("how-to-price-crochet-items.html")}">pricing crochet items</a> covers wholesale, discounts and the "materials × 3" trap.</p>
<h2>What sells best at Christmas craft fairs</h2>
<ul><li><strong>A spread of price points.</strong> Have something under $10 (ornaments, scrunchies, cards), a middle range ($20 to $40: beanies, sets of coasters, candles) and a few showpieces.</li>
<li><strong>Sets and bundles.</strong> Three ornaments in a box are easier to buy as a gift than one.</li>
<li><strong>Personalisation.</strong> Names on stockings and hoop ornaments. Take orders early and set a last order date.</li>
<li><strong>Gift-ready packaging.</strong> A tag, a ribbon and a card back make a small item look like a present. Free printable <a href="{href("christmas-crafts.html")}">Christmas gift tags</a> help.</li>
<li><strong>Stock planning:</strong> the <a href="{href("craft-fair-checklist.html")}">craft fair checklist</a> works out how many of each item to bring.</li></ul>
<h2>When to start making</h2>
<p>Christmas shopping on Etsy starts early, and craft fairs run from mid November to mid December. Make stock in batches from early autumn, list online by early November, and stop taking custom orders when your making time runs out. Check whether your list fits with the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a> or the <a href="{href("crochet-time-estimator.html")}">crochet time calculator</a>. For gifts you're making for family rather than selling, see our <a href="{href("christmas-crafts.html")}">Christmas crafts</a> ideas.</p>
<h2>Selling safely</h2>
<ul><li><strong>Toys for babies and young children</strong> must meet toy safety rules where you sell (for example in the US, UK and EU): avoid small parts like buttons and loose safety eyes, or label items as decorations.</li>
<li><strong>Candles</strong> need warning labels, and you should test your wax, wick and fragrance before selling.</li>
<li><strong>Selling into the EU from outside it?</strong> Our <a href="{href("eu-rules-checker-etsy-sellers.html")}">EU rules checker</a> explains what applies.</li></ul>
<p class="note">Ideas reflect what popular "crafts to make and sell" guides list (The Penny Hoarder, Small Business Trends, Gumtree, Unexpectedly Domestic; checked 26 Nov 2026). Material costs and hours are our own rough estimates; prices use our pricing method and Etsy's published US fees (6.5% transaction, 3% + $0.25 payment processing, $0.20 listing). Not legal advice on product safety rules.</p>
</div></div></section>'''
cs_faq = [
    ("What are the best Christmas crafts to make and sell?", "Quick, giftable makes that you can batch: crochet ornaments, beanies, ear warmers, mini stockings, gift bags, scrunchies, cards, candles and resin ornaments. Personalised items like name stockings sell for more."),
    ("How do I price handmade Christmas crafts?", "Add materials and your hours times an hourly rate, then about 10% for overheads, then the selling fees. A $6-of-yarn beanie that takes 2.5 hours is about $47 before fees at $15 an hour."),
    ("What crafts can I make quickly to sell?", "Scrunchies, drawstring gift bags, ear warmers, crochet ornaments, soy candles poured in batches and resin ornaments all take an hour or two or less each."),
    ("When should I start making crafts for Christmas sales?", "Early autumn. Etsy Christmas shopping starts early and fairs run from mid November, so aim to have stock listed by early November."),
    ("Do I need to charge sales tax at a craft fair?", "It depends on where you live. Many US states need a seller's permit even for one-day events; check your state or local tax office before the fair."),
    ("Is it worth selling crochet at Christmas?", "Yes, if you price for your time. Choose faster makes (ornaments, ear warmers, chunky beanies) so the price stays one people will pay."),
]
SHOP_FOR["christmas-crafts-to-sell.html"] = ["crochet-knitting-pricing-calculator", "small-business-pricing-inventory-spreadsheet", "christmas-gift-tags", "christmas-gift-planner-budget"]
page("christmas-crafts-to-sell.html", "Christmas Crafts to Make and Sell (With Prices) | Purl & Paper",
     "19 Christmas crafts to make and sell: crochet ornaments, beanies, stockings, gift bags, candles and cards, each with material cost, time and a fair price.",
     csp, cs_faq, "Christmas crafts to sell", app_name="Christmas craft price calculator")


# ======== JUNK JOURNAL VS SCRAPBOOK ========
# Demand: 'junk journal vs scrapbook' (Google autocomplete #7 for 'junk journal', 26 Nov 2026). SERP: Bearly Art "scrapbooking vs
# junk journaling", Artsy Fartsy Life, AOL/Real Simple "how they're different from scrapbooks", Journalsay, My Modern Met
# "what is a junk journal", Red River Catalog, Wikipedia "Junk journal", Happy Planner "scrapbooking reimagined". Wording ours.
JVS = [("What it's for", "Telling the story of events and people through photos", "A place to collect, create and write: memories, art, ideas or just pretty pages"),
       ("Main materials", "Photos, patterned paper, stickers, die cuts, journaling cards", "Found and recycled paper: book pages, envelopes, tickets, tea-stained paper, fabric, ephemera"),
       ("Format", "Albums with page protectors, usually 12 x 12 in or 8.5 x 11 in", "A handmade book: signatures sewn into a cover, any size"),
       ("Look", "Planned, neat layouts built around the photos", "Layered, collaged, vintage or messy on purpose; bulky and full of pockets"),
       ("Photo safety", "Acid-free, lignin-free, photo-safe products so photos last decades", "Mostly not archival; old paper can yellow photos, so use copies or sleeves"),
       ("Cost to start", "Moderate: an album, protectors and papers", "Very low: much of it comes from your recycling bin"),
       ("Writing", "Short captions and journaling cards", "As much or as little as you like: diary pages, prompts, lists")]
jvs_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in JVS)
JVS_Q = [("What do you mostly want to keep?", [("Photos of events and people", "s", 2), ("Writing, art and pretty paper", "j", 2), ("A bit of both", "b", 1)]),
         ("How do you like your pages to look?", [("Neat and planned", "s", 2), ("Layered, messy and vintage", "j", 2), ("Depends on my mood", "b", 1)]),
         ("Should it last for your grandchildren?", [("Yes, the photos must last", "s", 2), ("It's for me, now", "j", 1), ("Not sure", "b", 0)]),
         ("What's your budget to start?", [("Close to nothing", "j", 2), ("Happy to buy an album and papers", "s", 1), ("Somewhere in between", "b", 1)]),
         ("Do you like making things from scratch?", [("Yes: sewing, tearing, dyeing paper", "j", 2), ("I'd rather arrange than build", "s", 2), ("A little", "b", 1)])]
jvs_q = "".join(f'<fieldset class="jvs-q"><legend>{i + 1}. {e(q)}</legend>' + "".join(f'<label class="chk"><input type="radio" name="jvs{i}" value="{k}:{w}"> {e(t)}</label>' for t, k, w in a) + '</fieldset>' for i, (q, a) in enumerate(JVS_Q))

def _jvs_svg():
    sb = ('<rect x="20" y="40" width="140" height="140" rx="4" fill="#f3ede2" stroke="#1f2a44" stroke-width="2.5"/>'
          '<rect x="34" y="54" width="54" height="40" fill="#2f8f8a" opacity=".8"/><rect x="94" y="54" width="54" height="40" fill="#e39a14" opacity=".8"/>'
          '<rect x="34" y="100" width="114" height="44" fill="#b8326a" opacity=".75"/><path d="M38 160 h70 M38 168 h50" stroke="#5b6b94" stroke-width="2"/>')
    jj = ('<path d="M200 50 l130 -8 l6 140 l-132 6 z" fill="#e9dcc0" stroke="#1f2a44" stroke-width="2.5"/>'
          '<path d="M212 62 l60 -6 l4 50 l-58 5 z" fill="#d7c39a" transform="rotate(-4 240 80)"/><rect x="262" y="96" width="58" height="34" fill="#f3ede2" stroke="#5b6b94" stroke-width="1.5" transform="rotate(6 290 112)"/>'
          '<path d="M220 140 h40 v28 h-40 z" fill="#b8326a" opacity=".55"/><circle cx="300" cy="66" r="12" fill="#e39a14" opacity=".8"/>'
          '<path d="M236 120 l18 -2" stroke="#2f8f8a" stroke-width="5"/><path d="M276 150 q14 -6 30 2" stroke="#1f2a44" stroke-width="1.5" fill="none"/>'
          '<path d="M203 70 h-6 M203 110 h-6 M204 150 h-6" stroke="#1f2a44" stroke-width="2"/>')
    return ('<svg viewBox="0 0 360 230" role="img" aria-label="Left: a scrapbook page with photos in neat blocks and a caption. Right: a junk journal page with layered torn paper, a tag, a pocket and stitching">'
            + sb + jj + '<text x="90" y="210" text-anchor="middle" font-size="15" fill="#1f2a44" font-family="Georgia,serif">Scrapbook</text>'
            '<text x="268" y="210" text-anchor="middle" font-size="15" fill="#1f2a44" font-family="Georgia,serif">Junk journal</text></svg>')

jvsp = top("Junk journal vs scrapbook: what's the difference?", "A scrapbook tells a story with photos on neat, photo-safe album pages. A junk journal is a handmade book of found paper, collage and writing. Here's how they differ, a 5-question quiz to see which suits you, and how to combine them.", "Junk journal vs scrapbook") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> a <strong>scrapbook</strong> is built around <strong>photos</strong>: planned layouts on acid-free pages in an album, made to preserve memories for years. A <strong>junk journal</strong> is a <strong>handmade book of recycled and found paper</strong> (book pages, envelopes, tickets, tea-stained paper) for collage, keepsakes and writing, with a layered, vintage look. Scrapbooks focus on the story in the photos; junk journals on the making, the textures and your own words. Many people do both.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet" id="jvs-form">
<h2 style="margin-top:0">Which one suits you?</h2>
{jvs_q}
<p class="sub">Answer all five. Nothing is saved or sent.</p>
</div><div class="result" aria-live="polite" id="jvs-out" data-jj="{href("junk-journal-beginners.html")}" data-sb="{href("scrapbook-page-sizes.html")}"><p>Pick an answer for each question to see your match.</p></div></div></section>
<section><div class="wrap"><div class="narrow prose">
<figure class="sb-fig"><div>{_jvs_svg()}<figcaption>Same memories, two different styles</figcaption></div></figure>
<h2>Junk journal vs scrapbook at a glance</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col"></th><th scope="col">Scrapbook</th><th scope="col">Junk journal</th></tr></thead><tbody>{jvs_rows}</tbody></table></div>
<h2>What is a scrapbook?</h2>
<p>A scrapbook is an album of decorated pages that tell the story of something: a holiday, a baby's first year, a wedding. The photos are the stars. Pages are usually 12 x 12 in or 8.5 x 11 in in clear page protectors, and the papers, stickers and adhesives are labelled <strong>acid-free and lignin-free</strong> so the photos don't yellow. Layouts tend to be planned: a background paper, photos on mats, a title and a short caption. See every album size and how many photos fit with our <a href="{href("scrapbook-page-sizes.html")}">scrapbook page size calculator</a>.</p>
<h2>What is a junk journal?</h2>
<p>A junk journal is a book you make yourself from paper that would otherwise be thrown away: old book pages, envelopes, receipts, packaging, maps, sewing patterns and wrapping paper, often stained with tea or coffee. Pages are folded into signatures and sewn into a cover. Inside you add pockets, tags, flip-outs and bits of ephemera, and use it as a diary, an art journal or a memory book. Start with our <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a> guide and the <a href="{href("junk-journal-supply-checklist.html")}">supply checklist</a>.</p>
<h2>The main differences</h2>
<ul><li><strong>Purpose:</strong> scrapbooks document events; junk journals are as much about the making and writing as the memory.</li>
<li><strong>Materials:</strong> scrapbooks use bought papers made for the job; junk journals use found and recycled paper.</li>
<li><strong>Structure:</strong> scrapbook pages sit in an album and can be moved; a junk journal is a bound book.</li>
<li><strong>Longevity:</strong> scrapbook products are made to protect photos; junk journal paper often isn't archival.</li>
<li><strong>Style:</strong> clean and planned versus layered, textured and imperfect.</li></ul>
<h2>Can you use a junk journal as a scrapbook?</h2>
<p>Yes, and lots of people do: a travel junk journal with tickets, maps and photos from the trip is both. To keep photos safe, use <strong>prints or copies</strong> rather than one-off originals, slip them into tuck spots or photo corners instead of gluing them flat, and keep acidic paper (old book pages, newspaper) from touching the photo face. The <a href="{href("junk-journal-signature-calculator.html")}">signature calculator</a> helps you plan a thicker book with room for bulky pages.</p>
<h2>Supplies you can share between the two</h2>
<ul><li>Patterned paper, cardstock and journaling cards</li>
<li>A paper trimmer, scissors, a bone folder and a corner rounder</li>
<li>Glue sticks and double-sided tape (acid-free for anything near photos)</li>
<li>Washi tape, stamps, stickers and die cuts</li>
<li>Ephemera: see <a href="{href("junk-journal-ephemera-ideas.html")}">62 junk journal ephemera ideas</a></li></ul>
<h2>Which is cheaper?</h2>
<p>Junk journaling is cheaper to start: a needle, thread, glue and your recycling bin are enough for a first book, and our <a href="{href("how-to-tea-stain-paper.html")}">tea staining guide</a> turns plain paper into vintage pages for pennies. Scrapbooking needs an album, protectors and photo-safe papers, but those last for many projects. Either way, printable kits save time: print a sheet of tags or cards whenever you need them.</p>
<p class="note">Comparison drawn from established craft and scrapbooking sources (Bearly Art, Red River Catalog, My Modern Met, Wikipedia's junk journal article, The Happy Planner; checked 26 Nov 2026). Wording, table and drawing are our own.</p>
</div></div></section>'''
jvs_faq = [
    ("What is the difference between a junk journal and a scrapbook?", "A scrapbook is a photo-focused album with planned layouts on acid-free pages. A junk journal is a handmade book of found and recycled paper used for collage, keepsakes and writing, with a layered, vintage look."),
    ("Is junk journaling the same as scrapbooking?", "No, though they overlap. Both use paper and memories, but scrapbooking is built around photos and preservation, while junk journaling is about making a book from scraps and filling it however you like."),
    ("Can I put photos in a junk journal?", "Yes. Use prints or copies, tuck them into pockets or photo corners, and keep acidic paper like old book pages from touching the photo face so they don't yellow."),
    ("Which is better for beginners, junk journal or scrapbook?", "Junk journaling costs less to start because much of the paper is free. Scrapbooking is easier if you want quick, neat pages around your photos. Try the quiz above to see which suits you."),
    ("Is a junk journal archival?", "Usually not. Recycled paper, book pages and tea-stained paper are often acidic and can yellow over time. Scrapbook products are labelled acid-free and lignin-free for long life."),
    ("What size is a junk journal?", "Any size. Popular sizes are about 5.5 x 8.5 in (half letter) and A5, because a letter or A4 sheet folds in half to make the pages."),
]
SHOP_FOR["junk-journal-vs-scrapbook.html"] = ["junk-journal-mega-bundle", "tea-room-junk-journal-kit", "journaling-cards-3x4", "vintage-ephemera-pack"]
page("junk-journal-vs-scrapbook.html", "Junk Journal vs Scrapbook: What's the Difference? | Purl & Paper",
     "Junk journal vs scrapbook: a scrapbook tells a photo story on acid-free pages; a junk journal is a handmade book of found paper. Compare and take the quiz.",
     jvsp, jvs_faq, "Junk journal vs scrapbook")
