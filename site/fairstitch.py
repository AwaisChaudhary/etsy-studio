# ---------------- 26 Nov 2026 run 3: CRAFT FAIR PROFIT CALCULATOR + EMBROIDERY STITCHES ----------------
# Executed from build.py after seller.py (shares page(), top(), href(), e(), SHOP_FOR, more_seller(), more_crafts()).
# Demand evidence in DEMAND.md (RADAR 26 Nov run 3). Drawings are our own SVG; wording our own.

# ======== CRAFT FAIR PROFIT CALCULATOR ========
# Sources: TheCraftMap booth fee guide (Feb 2026: small fairs $25-75, regional $75-200, juried $200-500+, holiday markets $100-400,
# electricity $10-50, "gross at least 3x the booth fee"); Made Urban "10 costs of selling at craft fairs" (wages, card fees, travel,
# food, display, marketing, packaging, business set-up, sales tax); Square US in-person rate 2.6% + 15c (Square fee page / NerdWallet 2026).
def cfp_be(fee, other, price, mat, pack, cs=0.7, pct=2.6, fx=0.15):
    m = price - mat - pack - cs * (price * pct / 100 + fx)
    return int(-(-(fee + other) // m))  # ceil
cfp_rows = "".join(f"<tr><td>${fee}</td><td>{cfp_be(fee, 40, 20, 6, 0.4)} items (${cfp_be(fee, 40, 20, 6, 0.4) * 20:,})</td><td>${fee * 3:,}</td><td>{cfp_be(fee, 40 + 15 * 12, 20, 6, 0.4)} items</td></tr>" for fee in (25, 50, 100, 150, 250, 400))
_ex_m = 20 - 6 - 0.4 - 0.7 * (20 * 0.026 + 0.15)
cfp = top("Craft fair profit calculator", "Booth fee, travel, card fees, materials and your time: see what a market day really earns, how many sales you need to break even, and whether a fair is worth the fee.", "Craft fair profit calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> break-even sales = <strong>(booth fee + travel, food and other fair costs) ÷ what you keep per item</strong> after materials, packaging and card fees. With a $100 booth and $40 of other costs, selling $20 items that cost $6 to make, you keep about ${_ex_m:.2f} each, so you need <strong>{cfp_be(100, 40, 20, 6, 0.4)} sales just to cover the fair</strong>. A common rule of thumb is to aim for sales of <strong>at least 3 times the booth fee</strong>.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h3 style="margin-top:0">The fair</h3>
<div class="row2"><div class="field"><label for="cfp-fee">Booth or table fee ($)</label><input type="number" id="cfp-fee" value="100" min="0" step="5" inputmode="decimal"></div>
<div class="field"><label for="cfp-ext">Extras: electricity, table hire, jury fee ($)</label><input type="number" id="cfp-ext" value="0" min="0" step="5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="cfp-trv">Travel and parking ($)</label><input type="number" id="cfp-trv" value="25" min="0" step="1" inputmode="decimal"></div>
<div class="field"><label for="cfp-food">Food and drinks ($)</label><input type="number" id="cfp-food" value="15" min="0" step="1" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="cfp-dsp">Display, signs, cards bought for this fair ($)</label><input type="number" id="cfp-dsp" value="20" min="0" step="1" inputmode="decimal"></div>
<div class="field"><label for="cfp-hrs">Your hours: prep, packing, driving, set-up, selling</label><input type="number" id="cfp-hrs" value="12" min="0" step="0.5" inputmode="decimal"></div></div>
<h3>What you sell</h3>
<div class="row2"><div class="field"><label for="cfp-n">Items you expect to sell</label><input type="number" id="cfp-n" value="25" min="0" step="1" inputmode="numeric"></div>
<div class="field"><label for="cfp-p">Average price ($)</label><input type="number" id="cfp-p" value="20" min="0" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="cfp-m">Materials per item ($)</label><input type="number" id="cfp-m" value="6" min="0" step="0.1" inputmode="decimal"></div>
<div class="field"><label for="cfp-pk">Bag, tag, wrapping per item ($)</label><input type="number" id="cfp-pk" value="0.4" min="0" step="0.05" inputmode="decimal"></div></div>
<h3>Card payments</h3>
<div class="row2"><div class="field"><label for="cfp-cs">Share of sales paid by card (%)</label><input type="number" id="cfp-cs" value="70" min="0" max="100" step="5" inputmode="numeric"></div>
<div class="field"><label for="cfp-pct">Card fee (% + fixed $)</label><div class="row2" style="gap:8px"><input type="number" id="cfp-pct" value="2.6" min="0" max="10" step="0.05" aria-label="Card fee percent" inputmode="decimal"><input type="number" id="cfp-fx" value="0.15" min="0" max="1" step="0.01" aria-label="Card fee fixed amount per payment" inputmode="decimal"></div></div></div>
<div class="field"><label for="cfp-w">Hourly pay you'd like for your time ($)</label><input type="number" id="cfp-w" value="15" min="0" step="1" inputmode="decimal"></div>
<p class="sub">Saved on this device only. Nothing is uploaded.</p>
</div><div class="result" aria-live="polite" id="cfp-out"></div></div></section>
<script>(function(){{var F=["fee","ext","trv","food","dsp","hrs","n","p","m","pk","cs","pct","fx","w"];function g(i){{return document.getElementById("cfp-"+i)}}function v(i){{return Math.max(0,parseFloat(g(i).value)||0)}}
function $(x){{return (x<0?"-$":"$")+Math.abs(x).toLocaleString(undefined,{{minimumFractionDigits:2,maximumFractionDigits:2}})}}
try{{var s=JSON.parse(localStorage.getItem("pp-cfp")||"{{}}");F.forEach(function(k){{if(s[k]!=null)g(k).value=s[k]}})}}catch(e){{}}
function run(){{var fair=v("fee")+v("ext")+v("trv")+v("food")+v("dsp"),n=v("n"),p=v("p"),cs=Math.min(v("cs"),100)/100,sales=n*p,mat=n*v("m"),pack=n*v("pk"),card=cs*(sales*v("pct")/100+n*v("fx")),
prof=sales-mat-pack-card-fair,h=v("hrs"),keep=p-v("m")-v("pk")-cs*(p*v("pct")/100+v("fx")),be=keep>0?Math.ceil(fair/keep):Infinity,wage=keep>0?Math.ceil((fair+v("w")*h)/keep):Infinity,mult=v("fee")>0?sales/v("fee"):0,o=[];
o.push("<h2>"+(prof>=0?"Profit: ":"Loss: ")+$(prof)+"</h2><p>From "+$(sales)+" of sales ("+n+" × "+$(p)+").</p>");
if(h>0)o.push("<p><strong>"+$(prof/h)+" an hour</strong> for your "+h+" hours.</p>");
o.push(keep>0?"<p>You keep <strong>"+$(keep)+"</strong> on each sale after materials, packaging and card fees. <strong>Break even at "+be+" sales</strong> ("+$(be*p)+"). To also pay yourself "+$(v("w"))+" an hour: <strong>"+wage+" sales</strong> ("+$(wage*p)+").</p>":"<p>✘ Each sale costs more than its price. Raise your price or cut costs per item.</p>");
if(v("fee")>0)o.push("<p>Sales are <strong>"+mult.toFixed(1)+"×</strong> the booth fee. "+(mult>=3?"✔ That meets the common 3× rule of thumb.":"✘ Below the common 3× rule of thumb: you'd need "+$(v("fee")*3)+" of sales.")+"</p>");
var parts=[["Materials",mat,"#2f8f8a"],["Packaging",pack,"#c9a37a"],["Card fees",card,"#8a6fb0"],["Fair costs",fair,"#b8326a"],["Profit",Math.max(prof,0),"#f4a823"]],tot=parts.reduce(function(a,b){{return a+b[1]}},0)||1;
o.push("<div class=\\"cfp-bar\\" role=\\"img\\" aria-label=\\"Where your takings go\\">"+parts.map(function(q){{return q[1]>0?"<span style=\\"width:"+(q[1]/tot*100).toFixed(1)+"%;background:"+q[2]+"\\"></span>":""}}).join("")+"</div><ul class=\\"cfp-key\\">"+parts.map(function(q){{return "<li><i style=\\"background:"+q[2]+"\\"></i>"+q[0]+" "+$(q[1])+"</li>"}}).join("")+"</ul>");
o.push("<p class=\\"muted\\">Sales tax isn't included: where you must collect it, add it on top of your prices and set it aside.</p>");g("out").innerHTML=o.join("");
try{{var s={{}};F.forEach(function(k){{s[k]=g(k).value}});localStorage.setItem("pp-cfp",JSON.stringify(s))}}catch(e){{}}}}
F.forEach(function(k){{g(k).addEventListener("input",run)}});run()}})();</script>
<style>.cfp-bar{{display:flex;height:22px;border-radius:6px;overflow:hidden;margin:14px 0 8px;background:rgba(255,255,255,.15)}}.cfp-bar span{{display:block;height:100%}}.cfp-key{{list-style:none;padding:0;margin:0 0 10px;display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.9rem}}.cfp-key i{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:middle}}</style>
<section><div class="wrap"><div class="narrow prose">
<h2>How many sales to cover the booth fee?</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Booth fee</th><th scope="col">Break-even sales</th><th scope="col">3× rule: aim to sell</th><th scope="col">To also earn $15/h for 12 h</th></tr></thead><tbody>{cfp_rows}</tbody></table></div>
<p class="note">Worked out with the calculator's defaults: $20 average price, $6 materials, $0.40 packaging, $40 of travel, food and display costs, 70% of sales by card at 2.6% + 15¢. Change the numbers above for your own stall.</p>
<h2>What does a craft fair booth cost?</h2>
<p>Fees vary a lot. TheCraftMap's 2026 guide puts small community fairs at about <strong>$25 to $75</strong>, regional fairs at <strong>$75 to $200</strong>, juried shows at <strong>$200 to $500 or more</strong>, and holiday markets at <strong>$100 to $400</strong>. Electricity is often $10 to $50 extra. School and church fairs are sometimes free or ask for a raffle prize instead. A higher fee usually means more visitors, but it doesn't promise more sales: Made Urban's sellers' guide makes the same point.</p>
<h2>The costs people forget</h2>
<ul><li><strong>Your time.</strong> Applying, making stock, packing, driving, setting up and selling. A 6-hour fair is easily a 12-hour day.</li>
<li><strong>Card fees.</strong> Phone card readers in the US charge around 2.6% plus 15¢ for each tap or swipe (Square's in-person rate). Check your own reader's rate.</li>
<li><strong>Travel and food.</strong> Fuel, parking, and lunch you'd not otherwise buy. Out-of-town shows add a hotel.</li>
<li><strong>Display and packaging.</strong> A tent, risers, signs, bags, tissue and business cards. Spread big items like a tent over the fairs you'll use them for.</li>
<li><strong>Sales tax and permits.</strong> Many places need a seller's permit for in-person sales and expect you to collect sales tax. Check your state or local rules.</li></ul>
<h2>Is a craft fair worth it?</h2>
<p>Run the numbers before you apply. If you'd need to sell more than you've ever sold in a day just to break even, it's a pass, or a reason to bring more lower-priced items. A fair can still be worth a small profit if it brings custom orders, followers or wholesale contacts, so note those too: a sign-up sheet or a QR code to your shop turns browsers into later buyers. Keep a simple log of each fair (fee, footfall, sales, weather) and after three or four you'll know which ones to rebook.</p>
<h2>How to raise your profit at a fair</h2>
<ul><li><strong>Price from costs, not from the stall next to you.</strong> Our <a href="{href("how-to-price-crochet-items.html")}">pricing guide for handmade items</a> has a calculator with a craft fair option.</li>
<li><strong>Have small add-ons at the till.</strong> Ornaments, bookmarks, stickers or coasters lift the average sale.</li>
<li><strong>Use round prices.</strong> $20, not $19.50: quicker change and a smaller float.</li>
<li><strong>Bring enough stock.</strong> Two to three times what you expect to sell, in a spread of prices. Our <a href="{href("craft-fair-checklist.html")}">craft fair checklist</a> works out the stock and cash float.</li>
<li><strong>Selling online too?</strong> Compare with what Etsy takes in the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>.</li></ul>
<p class="note">Figures from TheCraftMap's craft fair booth fee guide (2026 fee ranges, electricity extras, the 3× rule and a break-even formula), Made Urban's "10 costs of selling at craft fairs" (the hidden-cost list and sales tax), and Square's published US in-person rate. All amounts are typical examples, not quotes: check your fair's and your card reader's own terms. This is general information, not tax or financial advice.</p>
</div></div></section>{more_seller("craft-fair-profit-calculator.html")}'''
cfp_faq = [
    ("How do I calculate break-even at a craft fair?", "Add up the booth fee and every other cost of the day (travel, food, extras), then divide by what you keep per item after materials, packaging and card fees. With $140 of costs and about $13 kept per $20 item, you need 11 sales to break even."),
    ("How much should I sell at a craft fair compared with the booth fee?", "A common rule of thumb is sales of at least three times the booth fee: $450 of sales for a $150 booth. Below that, the fair rarely pays for your time."),
    ("How much do craft fair booths cost?", "Roughly $25 to $75 for small community fairs, $75 to $200 for regional fairs, $100 to $400 for holiday markets and $200 to $500 or more for juried shows, according to TheCraftMap's 2026 guide."),
    ("How much do card readers charge at craft fairs?", "In the US, phone card readers such as Square charge around 2.6% plus 15 cents per in-person payment. On a $20 sale that's about 67 cents."),
    ("Is a craft fair worth it if I only break even?", "Sometimes. Count custom orders, new followers and wholesale contacts too. But if a fair only breaks even, your time has been unpaid, so try a cheaper fair, higher prices or more small add-on items."),
    ("Do I need to charge sales tax at a craft fair?", "In many US states and other countries you do, and you may need a seller's permit for the event. Check your state or local rules; the calculator leaves tax out of your takings."),
]
SHOP_FOR["craft-fair-profit-calculator.html"] = ["crochet-knitting-pricing-calculator", "soap-making-business-spreadsheet", "resin-art-business-spreadsheet", "sublimation-tumbler-business-spreadsheet"]
page("craft-fair-profit-calculator.html", "Craft Fair Profit Calculator: Break-Even Sales vs Booth Fee | Purl & Paper",
     "Free craft fair profit calculator: add your booth fee, travel, card fees, materials and hours to see your profit per hour, how many sales you need to break even, and if you meet the 3x booth fee rule.",
     cfp, cfp_faq, "Craft fair profit calculator", app_name="Craft fair profit and break-even calculator")


# ======== EMBROIDERY STITCHES FOR BEGINNERS ========
# Steps checked against EGA "Top 10 embroidery stitches for beginners", LoveCrafts "Top ten embroidery stitches", Lia Griffith basic stitches,
# Gathered embroidery for beginners and Needle'nThread line stitches (SERP 26 Nov 2026). Our own words and drawings.
_EN, _EB, _ET, _EG, _EL = "#1f2a44", "#b8326a", "#2f8f8a", "#f4a823", "#f3ede2"

def _es_frame(body, k, label, h=130):
    dots = f'<defs><pattern id="esd-{k}" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="1" fill="#d6cbb6"/></pattern></defs><rect width="240" height="{h}" rx="10" fill="url(#esd-{k})"/>'
    return f'<svg viewBox="0 0 240 {h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg"><rect width="240" height="{h}" rx="10" fill="{_EL}"/>{dots}{body}</svg>'

def _pt(x, y, n, up=True):
    c = _ET if up else _EN
    return f'<circle cx="{x}" cy="{y}" r="7.5" fill="#fff" stroke="{c}" stroke-width="1.6"/><text x="{x}" y="{y + 3.6}" font-size="10" font-weight="700" text-anchor="middle" fill="{c}">{n}</text>'

def _st(x1, y1, x2, y2, col=_EB, w=4):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'

def _back(d):
    return f'<path d="{d}" fill="none" stroke="{_EN}" stroke-width="1.4" stroke-dasharray="3 4" opacity=".55"/>'

def es_svg(k, label=""):
    b = ""
    if k == "running":
        for i, x in enumerate((20, 76, 132)):
            b += _st(x, 64, x + 32, 64)
        b += _back("M52 64 Q64 84 76 64 M108 64 Q120 84 132 64") + _st(188, 64, 220, 64, "#e59ab9") + _pt(188, 46, 1) + _pt(220, 46, 2, False)
        b += '<text x="120" y="112" font-size="11" text-anchor="middle" fill="#1f2a44">Up, down, skip a gap, repeat</text>'
    elif k == "back":
        for x in (20, 60, 100, 140):
            b += _st(x, 60, x + 40, 60)
        b += _st(180, 60, 220, 60, "#e59ab9") + _back("M180 60 Q200 84 220 60") + _pt(220, 40, 1) + _pt(180, 40, 2, False) + _pt(220, 82, 3)
        b += '<text x="120" y="114" font-size="11" text-anchor="middle" fill="#1f2a44">Up ahead, back into the last hole</text>'
    elif k == "stem":
        for i in range(5):
            x = 22 + i * 34
            b += _st(x, 70 - i * 4, x + 46, 62 - i * 4)
        b += _pt(212, 48, 1, False) + _pt(184, 62, 2) + _back("M196 50 Q180 66 166 54")
        b += '<path d="M30 90 q90 18 180 -36" fill="none" stroke="#c9a37a" stroke-width="1.4" stroke-dasharray="2 3"/>'
        b += '<text x="120" y="116" font-size="11" text-anchor="middle" fill="#1f2a44">Each stitch overlaps half the last</text>'
    elif k == "split":
        for x in (20, 62, 104, 146):
            b += _st(x, 62, x + 52, 62)
            b += f'<line x1="{x + 46}" y1="58" x2="{x + 46}" y2="66" stroke="{_EL}" stroke-width="2"/>'
        b += _pt(192, 42, 1) + _pt(170, 82, 2, False)
        b += '<text x="120" y="112" font-size="11" text-anchor="middle" fill="#1f2a44">Come up through the last stitch</text>'
    elif k == "satin":
        b += '<path d="M40 66 Q120 6 200 66 Q120 126 40 66Z" fill="none" stroke="#c9a37a" stroke-width="1.4" stroke-dasharray="3 3"/>'
        for i in range(-7, 8):
            x = 120 + i * 9.5
            hh = (1 - (i / 8) ** 2) ** 0.5 * 30
            col = _EB if i < 4 else "#e59ab9"
            b += _st(x - 6, 66 - hh, x + 6, 66 + hh, col, 4.5) if i < 6 else ""
        b += _pt(186, 40, 1) + _pt(186, 94, 2, False)
        b += '<text x="120" y="122" font-size="11" text-anchor="middle" fill="#1f2a44">Edge to edge, side by side</text>'
    elif k == "chain":
        for i in range(4):
            x = 30 + i * 40
            b += f'<path d="M{x} 64 C {x + 6} 44, {x + 40} 46, {x + 40} 64 C {x + 40} 82, {x + 6} 84, {x} 64Z" fill="none" stroke="{_EB}" stroke-width="4"/>'
        b += _st(190, 64, 196, 64, _EB, 4) + _pt(190, 40, 1) + _pt(190, 88, 2, False)
        b += _back("M200 64 Q214 64 214 52")
        b += '<text x="120" y="116" font-size="11" text-anchor="middle" fill="#1f2a44">Come up inside the loop, pull snug</text>'
    elif k == "daisy":
        import math as _mm
        for i in range(6):
            a = i * _mm.pi / 3
            x2, y2 = 120 + 40 * _mm.cos(a), 62 + 40 * _mm.sin(a)
            ang = _mm.degrees(a)
            b += f'<g transform="rotate({ang:.0f} 120 62)"><path d="M126 62 C 140 46, 162 50, 162 62 C 162 74, 140 78, 126 62" fill="none" stroke="{_EB}" stroke-width="3.6"/><line x1="161" y1="56" x2="161" y2="68" stroke="{_EB}" stroke-width="3.6" stroke-linecap="round"/></g>'
        b += f'<circle cx="120" cy="62" r="6" fill="{_EG}"/>'
        b += '<text x="120" y="122" font-size="11" text-anchor="middle" fill="#1f2a44">A loop tied down at the tip</text>'
    elif k == "knot":
        b += '<line x1="40" y1="20" x2="70" y2="100" stroke="#8a8a8a" stroke-width="2.4"/>'
        for i in range(2):
            b += f'<ellipse cx="{58 - i * 3.5}" cy="{66 - i * 9}" rx="10" ry="4" fill="none" stroke="{_EB}" stroke-width="3" transform="rotate(-20 {58 - i * 3.5} {66 - i * 9})"/>'
        b += f'<path d="M66 90 Q90 100 100 76" fill="none" stroke="{_EB}" stroke-width="3"/>'
        b += '<text x="62" y="116" font-size="10.5" text-anchor="middle" fill="#1f2a44">Wrap twice</text>'
        for x, y in ((150, 50), (176, 64), (160, 82), (196, 46), (206, 80)):
            b += f'<circle cx="{x}" cy="{y}" r="6.5" fill="{_EB}"/><circle cx="{x - 2}" cy="{y - 2}" r="2" fill="#e59ab9"/>'
        b += '<text x="176" y="116" font-size="10" text-anchor="middle" fill="#1f2a44">Down beside the hole</text>'
    elif k == "blanket":
        b += '<line x1="14" y1="92" x2="226" y2="92" stroke="#c9a37a" stroke-width="1.4"/>'
        for x in (30, 64, 98, 132, 166):
            b += _st(x, 46, x, 90) + _st(x, 90, x + 34, 90)
        b += _st(200, 46, 200, 90, "#e59ab9") + _pt(200, 30, 2, False) + _pt(220, 104, 3)
        b += '<text x="110" y="122" font-size="11" text-anchor="middle" fill="#1f2a44">Up at the edge, over the loop</text>'
    elif k == "fly":
        for x in (40, 100, 160):
            b += f'<path d="M{x - 22} 40 L{x} 70 L{x + 22} 40" fill="none" stroke="{_EB}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>' + _st(x, 70, x, 84)
        b += _pt(138, 30, 1) + _pt(182, 30, 2, False) + _pt(160, 98, 4, False)
        b += '<text x="120" y="122" font-size="11" text-anchor="middle" fill="#1f2a44">A V held by a small stitch</text>'
    elif k == "cross":
        for x in (24, 60, 96, 132):
            b += _st(x, 46, x + 30, 76, "#e59ab9") + _st(x, 76, x + 30, 46)
        b += _st(168, 76, 198, 46, "#e59ab9") + _pt(168, 92, 1) + _pt(198, 32, 2, False)
        b += '<text x="120" y="114" font-size="11" text-anchor="middle" fill="#1f2a44">Top legs all slope the same way</text>'
    elif k == "seed":
        import random as _r
        rr = _r.Random(7)
        for _ in range(26):
            x, y, a = rr.uniform(24, 216), rr.uniform(22, 92), rr.uniform(0, 180)
            b += f'<g transform="rotate({a:.0f} {x:.0f} {y:.0f})">' + _st(x - 5, y, x + 5, y, _EB, 3.4) + '</g>'
        b += '<text x="120" y="118" font-size="11" text-anchor="middle" fill="#1f2a44">Tiny stitches, every direction</text>'
    return _es_frame(b, k, label)

ES = [
 # key, name, use tags, uses text, strands, steps
 ("running", "Running stitch", "line edge first", "Dashed lines, simple outlines, quilting-style borders and gathering.", "2-3",
  ["Bring the needle up at the start of the line (1).", "Go down a stitch length along the line (2).", "Come up again a gap further on: the gap is usually the same as, or a little shorter than, the stitch.", "Repeat. Keep stitches and gaps even; it helps to load two or three stitches on the needle at once."]),
 ("back", "Backstitch", "line letters first", "Solid, crisp lines: lettering, outlines and fine details. The go-to outline stitch.", "1-2",
  ["Come up one stitch length along the line from the start (1).", "Go back down at the very start of the line (2).", "Come up one stitch length ahead of your first stitch (3).", "Go back down into the end of the previous stitch, sharing its hole. Repeat."]),
 ("stem", "Stem stitch", "line curves", "Smooth curves and flower stems. It looks like a twisted rope.", "2-3",
  ["Come up at the start of the line.", "Go down one stitch length along the line, keeping the working thread below the line.", "Come up halfway back along that stitch, just beside it.", "Go down a full stitch length ahead. Keep the thread on the same side for every stitch."]),
 ("split", "Split stitch", "line curves fill", "Bold lines and soft, filled shapes worked in rows. Great on curves.", "2 (even number)",
  ["Make one straight stitch along the line.", "Come up through the middle of that stitch, splitting its strands.", "Go down a stitch length ahead.", "Come up through the middle of the new stitch. Repeat."]),
 ("satin", "Satin stitch", "fill", "Smooth, solid fills for petals, leaves, hearts and small letters.", "2-3",
  ["Outline the shape with split or backstitch first: it gives a neat raised edge.", "Come up on one edge of the shape (1) and go down straight across on the opposite edge (2).", "Come up right next to where you first came up, and lay the next stitch beside the last.", "Keep stitches parallel and close, with no fabric showing. Start in the middle of the shape to keep the angle steady."]),
 ("chain", "Chain stitch", "line curves edge", "Thick, textured lines, borders and lettering. Fills too, in rows.", "2-4",
  ["Come up at the start of the line.", "Go back down into the same hole, leaving a loop on top.", "Come up a stitch length along the line, inside the loop, and pull until the loop sits snug.", "Go down inside the loop at the same hole you came up through to start the next link. End with a tiny stitch over the last loop."]),
 ("daisy", "Lazy daisy (detached chain)", "flowers leaves", "Petals and little leaves. Five or six make a quick flower.", "2-3",
  ["Come up at the inner end of the petal.", "Go back down in the same hole, leaving a loop.", "Come up at the tip of the petal, inside the loop.", "Go down just outside the loop to hold it with a tiny stitch. Repeat round the centre."]),
 ("knot", "French knot", "dots flowers", "Dots, flower centres, eyes and textured fills.", "2-3",
  ["Come up where you want the knot.", "Hold the thread taut and wrap it twice round the needle.", "Keep holding the thread and put the needle back down just next to where it came up (not in the same hole).", "Pull the needle through slowly while still holding the thread snug, so the knot forms on the surface."]),
 ("blanket", "Blanket stitch", "edge", "Edges of felt and fabric, appliqué, and decorative borders.", "2-6",
  ["Come up on the edge line (or at the fabric edge).", "Go down above it at the stitch height and a stitch width along.", "Come up on the edge line directly below, with the thread under the needle.", "Pull snug so the loop catches along the edge. Repeat, keeping heights and spacing even."]),
 ("fly", "Fly stitch", "leaves flowers", "Leaves, ferns, grass and borders. Stack them for a fern.", "2-3",
  ["Come up at the top left of the V (1).", "Go down at the top right (2), but don't pull tight.", "Come up at the point of the V, below and between, inside the loop (3).", "Go down a little below to hold the V with a small straight stitch (4)."]),
 ("cross", "Cross stitch", "fill first", "Counted designs on Aida or evenweave; samplers and pixel-style pictures.", "2 on 14-count",
  ["Work bottom-left to top-right half stitches along the row.", "Come back along the row, top-left to bottom-right, to finish each X.", "Keep every top leg going the same way so the work looks even.", "Use our cross stitch calculator for the fabric size and floss."]),
 ("seed", "Seed stitch", "fill dots", "Speckled, textured fills and soft shading.", "1-2",
  ["Make a tiny straight stitch.", "Come up a short distance away and make another at a different angle.", "Scatter them evenly; for denser shading, work them closer together.", "Work pairs side by side for a bolder seed."]),
]
ES_USE = [("all", "Show every stitch"), ("first", "My very first sampler"), ("line", "Outlines and straight lines"), ("letters", "Lettering and names"),
          ("curves", "Curves and stems"), ("fill", "Filling a shape"), ("flowers", "Flowers and petals"), ("leaves", "Leaves and ferns"),
          ("dots", "Dots, eyes and flower centres"), ("edge", "Edges, felt and borders")]
es_cards = "".join(f'''<article class="es-card" id="{k}" data-use="{tags}"><div class="es-fig">{es_svg(k, e("How to work " + n.lower() + ": step diagram"))}</div><div><h3>{e(n)}</h3><p>{e(u)} <span class="muted" style="white-space:nowrap">Strands: {s.replace("-", "–")}.</span></p>
<ol>{"".join(f"<li>{e(x)}</li>" for x in steps)}</ol></div></article>''' for k, n, tags, u, s, steps in ES)
es_rows = "".join(f'<tr><td><a href="#{k}">{e(n)}</a></td><td>{e(u.split(".")[0])}</td><td>{s}</td></tr>' for k, n, tags, u, s, steps in ES)
es = top("Embroidery stitches for beginners", "Twelve hand embroidery stitches, each with our own step diagram, what it's for and how many strands to use. Pick what you want to stitch to see the stitches that suit it.", "Embroidery stitches") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> start with <strong>running stitch, backstitch, stem stitch, satin stitch, lazy daisy and French knots</strong>. Backstitch and stem stitch do the lines and curves, satin stitch fills shapes, lazy daisy makes petals and French knots make dots, so these six cover most beginner patterns. Use <strong>2 or 3 of the 6 strands</strong> of embroidery floss and a hoop to keep the fabric tight.</div></div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sheet es-pick"><div class="field"><label for="es-use">What do you want to stitch?</label><select id="es-use">{"".join(f'<option value="{v}">{t}</option>' for v, t in ES_USE)}</select></div><p class="sub" id="es-n" aria-live="polite"></p></div>
<div class="es-grid">{es_cards}</div>
<p class="note">In the diagrams, green numbers are where the needle comes up, navy numbers where it goes down, the dotted line is the thread at the back, and the pale stitch is the one being made.</p>
</div></section>
<script>(function(){{var s=document.getElementById("es-use");if(!s)return;var c=[].slice.call(document.querySelectorAll(".es-card"));
function run(){{var u=s.value,n=0;c.forEach(function(x){{var on=u=="all"||x.getAttribute("data-use").split(" ").indexOf(u)>=0;x.hidden=!on;if(on)n++}});document.getElementById("es-n").textContent=u=="all"?"All "+n+" stitches":n+" stitch"+(n==1?"":"es")+" for this";try{{localStorage.setItem("pp-es",u)}}catch(e){{}}}}
try{{var v=localStorage.getItem("pp-es");if(v&&s.querySelector("option[value=\\""+v+"\\"]"))s.value=v}}catch(e){{}}s.addEventListener("change",run);run()}})();</script>
<style>.es-pick{{max-width:520px;margin:0 0 18px}}.es-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}}.es-card{{background:#fff;border-radius:14px;padding:14px 16px;box-shadow:0 1px 3px rgba(31,42,68,.12)}}.es-card[hidden]{{display:none}}.es-card h3{{margin:10px 0 4px}}.es-card ol{{padding-left:20px;margin:8px 0 0}}.es-card li{{margin:3px 0}}.es-fig svg{{width:100%;height:auto;display:block}}</style>
<section><div class="wrap"><div class="narrow prose">
<h2>Embroidery stitch chart</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Stitch</th><th scope="col">Best for</th><th scope="col">Strands of floss</th></tr></thead><tbody>{es_rows}</tbody></table></div>
<h2>What you need to start</h2>
<ul><li><strong>Fabric:</strong> a tightly woven cotton or linen. Calico or quilting cotton is cheap and fine for practice.</li>
<li><strong>A hoop</strong> a little bigger than your design. 6 in (15 cm) is an easy first size.</li>
<li><strong>Embroidery floss:</strong> six strands twisted together. Cut about 18 in (45 cm) at a time and separate the strands you need.</li>
<li><strong>An embroidery (crewel) needle</strong>, size 5 to 9: it has a long eye for the floss.</li>
<li><strong>Small sharp scissors</strong> and a water-soluble pen or pencil to mark the design.</li></ul>
<h2>How to start and finish without a knot</h2>
<p>Knots are fine for practice, but they can show as lumps and pull through loose weaves. For an even number of strands, use the <strong>loop start</strong>: take one strand, fold it in half, thread the two cut ends, come up from the back, go down for your first stitch and pass the needle through the loop at the back before you pull. For any count, a <strong>waste knot</strong> works too: knot the end and go in from the front a few inches away along the line you'll stitch, so your stitches cover the tail at the back; snip the knot off later. To finish, run the needle under three or four stitches at the back and trim.</p>
<h2>How many strands should I use?</h2>
<p>Most patterns use 2 or 3 strands for lines and 2 to 4 for fills. One strand gives fine detail like whiskers; six gives bold lines and quick fills. Split stitch works best with an even number, so it splits neatly. On 14-count Aida, cross stitch is usually worked with 2 strands.</p>
<h2>Which stitch should I learn first?</h2>
<p>Backstitch. It's the outline stitch most patterns use, it's easy to keep neat, and it's also the base for other stitches. Then add stem stitch for curves, satin stitch for fills, and lazy daisy and French knots for flowers. Stitch each one in a row on scrap fabric as a sampler before you start a pattern.</p>
<h2>Why does my satin stitch look messy?</h2>
<ul><li><strong>Outline first.</strong> A row of split stitch round the edge gives the satin stitches something to sit over.</li>
<li><strong>Keep them short.</strong> Stitches longer than about 1 cm (⅜ in) snag and sag; split a big shape into sections.</li>
<li><strong>Keep the fabric drum tight</strong> in the hoop and don't pull the thread tight, which puckers the fabric.</li></ul>
<h2>Ready for a pattern?</h2>
<p>Our free <a href="{href("embroidery-patterns.html")}">embroidery pattern generator</a> makes floral hoop designs to trace, sized for 4 to 8 in hoops, using these stitches. Counted designs on Aida? The <a href="{href("cross-stitch-calculator.html")}">cross stitch calculator</a> works out the fabric and floss. A finished hoop makes a lovely <a href="{href("christmas-crafts.html")}">Christmas gift</a>, and stitched panels look great in a <a href="{href("junk-journal-beginners.html")}">junk journal</a>.</p>
<p class="note">Steps checked against the Embroiderers' Guild of America's top 10 beginner stitches, LoveCrafts' top ten embroidery stitches, Lia Griffith's basic stitch guide, Gathered's embroidery for beginners and Needle'nThread's line stitch notes. Steps, tips and diagrams are our own.</p>
</div></div></section>{more_crafts("embroidery-stitches.html")}'''
es_faq = [
    ("What are the basic embroidery stitches for beginners?", "Running stitch, backstitch, stem stitch, satin stitch, lazy daisy (detached chain) and French knots. Add split stitch, chain stitch, blanket stitch, fly stitch and seed stitch as you go."),
    ("What is the easiest embroidery stitch?", "Running stitch: up, down, leave a gap, repeat. Backstitch is next, and it's the one most patterns use for outlines."),
    ("What is the difference between backstitch and stem stitch?", "Backstitch makes a flat, crisp line of separate stitches sharing holes, best for letters. Stem stitch overlaps each stitch with the last, making a rope-like line that follows curves smoothly."),
    ("How many strands of embroidery floss should I use?", "Usually 2 or 3 of the 6 strands for lines and 2 to 4 for fills. Use 1 for fine detail and 6 for bold lines."),
    ("How do I start embroidery without a knot?", "Use the loop start for an even number of strands: fold one strand in half, thread the cut ends, make your first stitch and pass the needle through the loop at the back. Or use a waste knot placed on the front where later stitches will cover the tail."),
    ("Why does my French knot pull through the fabric?", "The needle went back down in the same hole it came up from. Go down just beside it, and keep the wraps snug while you pull through."),
]
SHOP_FOR["embroidery-stitches.html"] = ["christmas-gift-tags", "2027-crochet-knitting-planner", "junk-journal-mega-bundle", "december-days-journal-kit"]
page("embroidery-stitches.html", "Embroidery Stitches for Beginners: 12 Basic Stitches with Diagrams | Purl & Paper",
     "Basic embroidery stitches for beginners with our own step diagrams: running, backstitch, stem, split, satin, chain, lazy daisy, French knot, blanket, fly, cross and seed stitch, plus strands and a stitch chooser.",
     es, es_faq, "Embroidery stitches", app_name="Embroidery stitch chooser")
