# ---------------- SELLER TOOLS (Awais 26 Nov 2026: narrow free tools for Etsy and KDP sellers; later a paid micro-SaaS) ----------------
# Facts: KDP Help "Create a paperback cover" (spine factors 0.002252 white / 0.0025 cream / 0.002347 premium colour / 0.002252 standard colour,
# 0.125 in bleed, spine text only over 79 pages); KDP paperback royalty 60% at $9.99+ and 50% at $9.98 and below (June 2025 change);
# US black-ink printing: 24-110 pages $2.30 regular / $2.84 large trim, above 110 pages $1.00 + $0.012 / $0.017 per page (KDP Paperback Printing Cost page,
# as summarised by Cambric, Inkfluence, bookprinttools Nov 2026). Etsy: titles up to 140 characters, 13 tags of up to 20 characters.
SELLER = [
 ("seller-tools.html", "Free tools for Etsy and KDP sellers", "Every free calculator and checker for people selling on Etsy and Amazon KDP."),
 ("etsy-fee-calculator.html", "Etsy fee calculator", "What Etsy takes from each sale and what to charge."),
 ("etsy-title-tag-checker.html", "Etsy title and tag checker", "Check your title and 13 tags against Etsy's limits and common mistakes."),
 ("eu-rules-checker-etsy-sellers.html", "EU rules checker for Etsy sellers", "Which EU rules apply to your shop: GPSR, packaging (PPWR) and the 2026 guarantee notice."),
 ("kdp-royalty-calculator.html", "KDP royalty calculator", "Printing cost and royalty for any paperback, and the price you need."),
 ("kdp-cover-size-calculator.html", "KDP cover size and spine calculator", "Full-wrap cover size, spine width and pixels for any trim and page count."),
 ("craft-fair-profit-calculator.html", "Craft fair profit calculator", "Break-even sales, profit per hour and the 3x booth fee rule for a market day."),
 ("christmas-crafts-to-sell.html", "Christmas crafts to make and sell", "19 Christmas makes with material cost, time and a price for your hourly rate."),
]
def more_seller(file):
    return '<section><div class="wrap"><div class="narrow prose"><h2>More free seller tools</h2><ul>' + "".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n, _ in SELLER if f != file) + "</ul></div></div></section>"

hub = top("Free tools for Etsy and KDP sellers", "We sell digital products on Etsy and low-content books on Amazon KDP ourselves. These are the small tools we wanted and couldn't find in one place. All free, no sign-up.", "Seller tools") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="narrow prose">
<h2>Etsy</h2><ul>
<li><a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>: listing, transaction, payment processing and Offsite Ads fees, and the price you need for the profit you want.</li>
<li><a href="{href("etsy-title-tag-checker.html")}">Etsy title and tag checker</a>: length limits, repeated words, tags over 20 characters, tags that waste a slot.</li>
<li><a href="{href("eu-rules-checker-etsy-sellers.html")}">EU rules checker</a>: five questions to see which EU rules apply to your shop, with a to-do list.</li></ul>
<h2>Amazon KDP</h2><ul>
<li><a href="{href("kdp-royalty-calculator.html")}">KDP royalty calculator</a>: printing cost and royalty per paperback, and why $9.99 matters.</li>
<li><a href="{href("kdp-cover-size-calculator.html")}">KDP cover size and spine calculator</a>: full-wrap size in inches, millimetres and pixels.</li></ul>
<h2>Running the business</h2><ul>
<li><a href="{href("craft-fair-profit-calculator.html")}">Craft fair profit calculator</a>: booth fee, travel and card fees against your sales, break-even and profit per hour.</li>
<li><a href="{href("craft-fair-checklist.html")}">Craft fair checklist</a> and <a href="{href("how-to-price-crochet-items.html")}">how to price handmade items</a>.</li></ul>
<p class="muted">Figures checked 26 November 2026. Etsy and Amazon change their fees and rules; each tool says where its numbers come from.</p>
</div></div></section>'''
page("seller-tools.html", "Free Tools for Etsy and KDP Sellers: Fee, Royalty, Cover Size and Tag Calculators | Purl & Paper",
     "Free tools for Etsy and Amazon KDP sellers: Etsy fee calculator, Etsy title and tag checker, KDP royalty calculator and KDP cover size and spine calculator.",
     hub, None, "Seller tools")

# ---- Etsy title & tag checker ----
tt = top("Etsy title and tag checker", "Paste your listing title and tags. See what's over Etsy's limits, what's repeated and which tags are wasting a slot.", "Etsy title and tag checker") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> Etsy allows a <strong>title of up to 140 characters</strong> and <strong>13 tags of up to 20 characters each</strong>. Use all 13 tags, make them multi-word phrases buyers would type, and don't spend tags repeating your category or exact title words unless they're part of a phrase. Put the clearest description of the item at the start of the title.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="tc-t">Listing title</label><textarea id="tc-t" rows="3">Nail Tech Spreadsheet, Nail Pricing Calculator, Nail Client Record, Fill Due Tracker, Appointment & Income Log, Excel Google Sheets</textarea></div>
<div class="field"><label for="tc-g">Tags (comma or new line between them)</label><textarea id="tc-g" rows="5">nail tech, nail business, nail pricing, nail price list, nail client record, nail tech planner, client tracker, salon spreadsheet, nail salon, income tracker, appointment log, nail artist, beauty business</textarea></div>
</div><div class="result" aria-live="polite" id="tc-out"></div></div></section>
<script>(function(){{function g(i){{return document.getElementById(i)}}function esc(s){{return s.replace(/[&<>]/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;"}}[c]}})}}
function run(){{var t=g("tc-t").value.trim(),tags=g("tc-g").value.split(/[,\\n]/).map(function(x){{return x.trim().toLowerCase()}}).filter(Boolean),o=[],bad=0;
var tl=t.length;o.push("<h2>Title: "+tl+" / 140</h2>");if(tl>140){{o.push("<p>✘ Over the limit by "+(tl-140)+" characters.</p>");bad++}}else if(tl<40)o.push("<p>Your title is short. You have room to add what the item is, who it's for or the format.</p>");
var words=t.toLowerCase().match(/[a-z0-9']+/g)||[],cnt={{}};words.forEach(function(w){{if(w.length>3)cnt[w]=(cnt[w]||0)+1}});var rep=Object.keys(cnt).filter(function(w){{return cnt[w]>2}});
if(rep.length)o.push("<p>Words used 3+ times in the title: <strong>"+esc(rep.join(", "))+"</strong>. Repeating a word doesn't help it rank, so you could use that space for a different search phrase.</p>");
var first=t.split(/[,|:\\-–]/)[0].trim();o.push("<p>First phrase (what buyers read first): <strong>"+esc(first)+"</strong>. Make sure it says exactly what the item is.</p>");
o.push("<h2>Tags: "+tags.length+" / 13</h2>");if(tags.length<13)o.push("<p>✘ You have "+(13-tags.length)+" empty tag slot"+(13-tags.length>1?"s":"")+". Every unused tag is a search you can't be found for.</p>");if(tags.length>13){{o.push("<p>✘ Etsy only takes 13 tags.</p>");bad++}}
var rows=tags.map(function(x,i){{var p=[];if(x.length>20){{p.push("over 20 characters ("+x.length+")");bad++}}if(tags.indexOf(x)!==i)p.push("duplicate");if(x.indexOf(" ")<0)p.push("single word: a phrase usually matches more searches");if(/[^a-z0-9 '&-]/.test(x))p.push("Etsy only allows letters, numbers, spaces, - ' and &");
return "<tr><td>"+esc(x)+"</td><td>"+x.length+"</td><td>"+(p.length?"✘ "+p.join("; "):"✔")+"</td></tr>"}}).join("");
o.push("<div class=\\"tbl-wrap\\"><table class=\\"mt\\"><thead><tr><th>Tag</th><th>Chars</th><th>Check</th></tr></thead><tbody>"+rows+"</tbody></table></div>");
o.push(bad?"<p><strong>"+bad+" thing"+(bad>1?"s":"")+" to fix before publishing.</strong></p>":"<p><strong>No hard errors.</strong> Now check each tag is a phrase a buyer would really type.</p>");g("tc-out").innerHTML=o.join("")}}
["tc-t","tc-g"].forEach(function(i){{g(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>How to write Etsy tags that get found</h2>
<ul><li><strong>Use all 13.</strong> Each tag is another search your listing can match.</li>
<li><strong>Use phrases, not single words.</strong> "Nail price list" matches a real search; "nail" on its own competes with millions of listings.</li>
<li><strong>Think like the buyer.</strong> Who it's for ("gift for crocheter"), what it does ("pricing calculator"), the format ("google sheets"), the occasion.</li>
<li><strong>Don't waste tags on your category or attributes.</strong> Etsy already uses your category and attributes (colour, occasion) for search, so tags are better spent on other phrases.</li>
<li><strong>Check spelling variants</strong> only when buyers really use them ("colour" and "color" if you sell to both the UK and US).</li></ul>
<h2>How to write an Etsy title in 2026</h2>
<p>Lead with what the item is in plain words, then the most important details. Etsy has encouraged shorter, clearer titles for several years, so a long list of keywords is no longer the advantage it once was: put the extra search phrases in your tags and description instead.</p>
<p>Worked out your title? Check what you'll keep from each sale with the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>.</p>
</div></div></section>{more_seller("etsy-title-tag-checker.html")}'''
tt_faq = [("How many characters can an Etsy title have?", "Up to 140 characters."),
          ("How many tags can you use on Etsy?", "13 tags, each up to 20 characters."),
          ("Should Etsy tags be single words or phrases?", "Phrases usually work better: they match what buyers actually type and face less competition than single words."),
          ("Do Etsy tags need to repeat the title?", "No. Etsy matches searches across your title, tags, category and attributes, so use tags for phrases your title doesn't already cover.")]
page("etsy-title-tag-checker.html", "Etsy Title and Tag Checker: 140 Characters, 13 Tags, 20-Character Limit (Free) | Purl & Paper",
     "Free Etsy title and tag checker: paste your title and tags to check Etsy's 140-character and 20-character limits, empty tag slots, duplicates and repeated words.",
     tt, tt_faq, "Etsy title and tag checker", app_name="Etsy title and tag checker")

# ---- KDP royalty calculator ----
def _pc(pages, large=False):
    if pages <= 110: return 2.84 if large else 2.30
    return 1.00 + pages * (0.017 if large else 0.012)
def _roy(price, pages, large=False):
    return round((0.6 if price >= 9.99 else 0.5) * price - _pc(pages, large), 2)
kr_rows = "".join(f"<tr><td>{p}</td><td>${_pc(p):.2f}</td><td>${_roy(8.99,p):.2f}</td><td>${_roy(9.99,p):.2f}</td><td>${_roy(12.99,p):.2f}</td></tr>" for p in (100, 120, 150, 200, 250, 300))
kr = top("KDP royalty calculator (paperback)", "Enter your page count, trim size and list price. See the printing cost, your royalty per copy and the lowest price that makes sense.", "KDP royalty calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> on Amazon.com a KDP paperback earns <strong>60% of the list price at $9.99 or more</strong> and <strong>50% at $9.98 or less</strong>, minus the printing cost. A black-ink book on a regular trim (6 × 9 in or smaller) costs <strong>$2.30 to print up to 110 pages</strong>, then <strong>$1.00 + $0.012 a page</strong>. So a 120-page journal at $9.99 earns <strong>${_roy(9.99,120):.2f}</strong> a copy; at $9.98 it earns about $1 less.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="kr-p">Page count</label><input type="number" id="kr-p" value="120" min="24" max="828"></div>
<div class="field"><label for="kr-l">List price (USD)</label><input type="number" id="kr-l" value="9.99" min="0" step="0.01"></div></div>
<div class="row2"><div class="field"><label for="kr-t">Trim size</label><select id="kr-t"><option value="0">Regular (6 × 9 in or smaller)</option><option value="1">Large (wider than 6.12 in or taller than 9 in, e.g. 8.5 × 11)</option></select></div>
<div class="field"><label for="kr-n">Copies a month</label><input type="number" id="kr-n" value="10" min="0"></div></div>
</div><div class="result" aria-live="polite" id="kr-out"></div></div></section>
<script>(function(){{function g(i){{return document.getElementById(i)}}function pc(p,L){{return p<=110?(L?2.84:2.30):1+p*(L?0.017:0.012)}}
function run(){{var p=+g("kr-p").value||0,l=+g("kr-l").value||0,L=g("kr-t").value=="1",c=pc(p,L),r=(l>=9.99?0.6:0.5)*l-c,mn=Math.ceil(c/0.5*100)/100,n=+g("kr-n").value||0,o=[];
o.push("<h2>$"+r.toFixed(2)+" per copy</h2><p>Printing cost $"+c.toFixed(2)+". Royalty rate "+(l>=9.99?"60%":"50%")+" of $"+l.toFixed(2)+".</p>");
if(l<9.99&&l>=8){{var r2=0.6*9.99-c;o.push("<p><strong>Price at $9.99 instead</strong> and you'd earn $"+r2.toFixed(2)+": $"+(r2-r).toFixed(2)+" more per copy.</p>")}}
if(r<0)o.push("<p>✘ You'd lose money on every copy. KDP won't let you list below the printing cost, so the lowest price is about $"+mn.toFixed(2)+".</p>");
o.push("<p>At "+n+" copies a month that's about <strong>$"+(r*n).toFixed(2)+" a month</strong>, or $"+(r*n*12).toFixed(0)+" a year, before tax.</p><p class=\\"muted\\">Amazon.com, black ink on white or cream paper, standard distribution. Colour and hardcover cost more; Expanded Distribution pays 40%.</p>");g("kr-out").innerHTML=o.join("")}}
["kr-p","kr-l","kr-t","kr-n"].forEach(function(i){{g(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>KDP paperback royalty table (regular trim, black ink)</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Pages</th><th scope="col">Print cost</th><th scope="col">At $8.99</th><th scope="col">At $9.99</th><th scope="col">At $12.99</th></tr></thead><tbody>{kr_rows}</tbody></table></div>
<p class="note">Amazon.com, standard distribution. Worked out from KDP's published rates; check your title's royalty on KDP's pricing page before publishing.</p>
<h2>Why $9.99 matters</h2>
<p>Since June 2025, KDP paperbacks priced at $9.98 or less earn 50% instead of 60%. Because the rate applies to the whole list price, one cent can make about a dollar's difference per copy. For most journals, planners and logbooks, $9.99 is the lowest price worth choosing.</p>
<h2>What sets the printing cost</h2>
<ul><li><strong>Page count:</strong> up to 110 pages costs a flat fee; above that you pay per page. A 100-page and a 110-page book cost the same to print.</li>
<li><strong>Trim size:</strong> anything wider than 6.12 in or taller than 9 in (like 8.5 × 11) is a large trim and costs more per page.</li>
<li><strong>Ink:</strong> colour interiors cost several times more than black ink, which is why most low-content books are black and white.</li></ul>
<p>Designing the cover? Get the exact size with the <a href="{href("kdp-cover-size-calculator.html")}">KDP cover size and spine calculator</a>.</p>
</div></div></section>{more_seller("kdp-royalty-calculator.html")}'''
kr_faq = [("How much does KDP pay per paperback?", "60% of the list price at $9.99 or more on Amazon.com (50% at $9.98 or less), minus the printing cost."),
          ("How much does KDP charge to print a paperback?", "For black ink on a regular trim: $2.30 for 24 to 110 pages, then $1.00 plus $0.012 per page. Large trims cost $2.84, then $1.00 plus $0.017 per page."),
          ("What is the best price for a KDP journal?", "Usually $9.99 or more, because that's where the royalty rate rises from 50% to 60%."),
          ("How much do I earn on a 120-page journal at $9.99?", f"About ${_roy(9.99,120):.2f} per copy on Amazon.com: 60% of $9.99 minus ${_pc(120):.2f} printing.")]
page("kdp-royalty-calculator.html", "KDP Royalty Calculator 2026: Paperback Printing Cost + Royalty (60% at $9.99) | Purl & Paper",
     "Free KDP royalty calculator for paperbacks: printing cost for any page count and trim, royalty per copy at the 50% and 60% rates, and why $9.99 matters.",
     kr, kr_faq, "KDP royalty calculator", app_name="KDP paperback royalty calculator")

# ---- KDP cover size ----
KS = {"white": 0.002252, "cream": 0.0025, "std": 0.002252, "prem": 0.002347}
def _cv(w, h, p, k="white"): s = p * KS[k]; return s, 0.125 * 2 + w * 2 + s, h + 0.25
_s, _w, _h = _cv(6, 9, 120)
kc = top("KDP cover size and spine width calculator", "Pick your trim size, page count and paper. Get the full-wrap cover size with bleed, the spine width and the canvas size in pixels.", "KDP cover size calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> spine width = pages × <strong>0.002252 in</strong> (white paper) or <strong>0.0025 in</strong> (cream). Cover width = 0.125 in bleed + back + spine + front + 0.125 in bleed; height = trim height + 0.25 in. A <strong>6 × 9 in, 120-page</strong> book on white paper needs a <strong>{_w:.3f} × {_h:.3f} in</strong> cover with a {_s:.3f} in spine ({round(_w*300)} × {round(_h*300)} px at 300 DPI).</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="kc-t">Trim size</label><select id="kc-t"><option value="6,9">6 × 9 in</option><option value="5,8">5 × 8 in</option><option value="5.5,8.5">5.5 × 8.5 in</option><option value="7,10">7 × 10 in</option><option value="8,10">8 × 10 in</option><option value="8.5,11">8.5 × 11 in</option><option value="8.27,11.69">A4 (8.27 × 11.69 in)</option><option value="8.5,8.5">8.5 × 8.5 in</option></select></div>
<div class="row2"><div class="field"><label for="kc-p">Page count</label><input type="number" id="kc-p" value="120" min="24" max="828"></div>
<div class="field"><label for="kc-k">Paper</label><select id="kc-k"><option value="white">Black ink, white paper</option><option value="cream">Black ink, cream paper</option><option value="std">Standard colour</option><option value="prem">Premium colour</option></select></div></div>
</div><div class="result" aria-live="polite" id="kc-out"></div></div></section>
<script>(function(){{var K={json.dumps(KS)};function g(i){{return document.getElementById(i)}}
function run(){{var t=g("kc-t").value.split(","),w=+t[0],h=+t[1],p=+g("kc-p").value||0,s=p*K[g("kc-k").value],W=0.25+2*w+s,H=h+0.25,mm=function(x){{return (x*25.4).toFixed(1)}};
g("kc-out").innerHTML="<h2>"+W.toFixed(3)+" × "+H.toFixed(3)+" in</h2><p>("+mm(W)+" × "+mm(H)+" mm) full-wrap cover with bleed.</p><p><strong>Canvas at 300 DPI: "+Math.round(W*300)+" × "+Math.round(H*300)+" px.</strong></p><p>Spine: <strong>"+s.toFixed(3)+" in</strong> ("+mm(s)+" mm). "+(p>79?"You can put text on the spine; keep it well inside the fold lines.":"✘ Too thin for spine text: KDP only prints spine text on books with more than 79 pages.")+"</p><p>From the left: 0.125 in bleed, back cover "+w+" in, spine "+s.toFixed(3)+" in, front cover "+w+" in, 0.125 in bleed. Keep text and images you don't want trimmed at least 0.25 in from the outer edges.</p>"}}
["kc-t","kc-p","kc-k"].forEach(function(i){{g(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>KDP spine width chart</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Pages</th><th scope="col">White paper</th><th scope="col">Cream paper</th><th scope="col">6 × 9 cover (white)</th></tr></thead><tbody>
{"".join(f"<tr><td>{p}</td><td>{p*0.002252:.3f} in</td><td>{p*0.0025:.3f} in</td><td>{_cv(6,9,p)[1]:.3f} × 9.250 in</td></tr>" for p in (24, 50, 100, 120, 150, 200, 300))}
</tbody></table></div>
<p class="note">Spine factors from KDP's paperback cover guidelines.</p>
<h2>Common cover mistakes</h2>
<ul><li><strong>Designing for the wrong paper.</strong> Cream paper is about 11% thicker than white, so a cover sized for white paper won't fit a cream interior.</li>
<li><strong>Changing the page count after the cover is done.</strong> Even ten pages moves the spine. Finish the interior first.</li>
<li><strong>Spine text on thin books.</strong> KDP only prints spine text on books over 79 pages.</li>
<li><strong>Forgetting the barcode area.</strong> KDP places a barcode on the back cover, near the lower spine-side corner; keep that area clear.</li></ul>
<p>Pricing the book? Work it out with the <a href="{href("kdp-royalty-calculator.html")}">KDP royalty calculator</a>.</p>
</div></div></section>{more_seller("kdp-cover-size-calculator.html")}'''
kc_faq = [("How do I calculate KDP spine width?", "Multiply the page count by 0.002252 in for white paper or 0.0025 in for cream paper (0.002347 in for premium colour)."),
          ("What size should a KDP cover be?", "Width = 0.125 in + back cover + spine + front cover + 0.125 in. Height = trim height + 0.25 in."),
          ("What size is a 6x9 KDP cover with 120 pages?", f"{_w:.3f} × {_h:.3f} in on white paper, with a {_s:.3f} in spine."),
          ("Can I put text on the spine?", "Only if the book has more than 79 pages.")]
page("kdp-cover-size-calculator.html", "KDP Cover Size Calculator + Spine Width (6x9, 8.5x11, Pixels at 300 DPI) | Purl & Paper",
     "Free KDP cover size calculator: spine width for white, cream and colour paper, full-wrap cover size with bleed in inches, mm and pixels, for 6x9, 8.5x11 and more.",
     kc, kc_faq, "KDP cover size calculator", app_name="KDP cover size and spine width calculator")

exec((ROOT / "eu_rules.py").read_text())
