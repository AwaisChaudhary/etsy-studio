# ---- EU rules checker for Etsy sellers (exec'd at the end of seller.py) ----
# Sources: Etsy Help "What is the GPSR?"; Regulation (EU) 2023/988 (GPSR, applies 13 Dec 2024); Regulation (EU) 2025/40 (PPWR, applies 12 Aug 2026, Art. 45(3));
# Directive (EU) 2024/825 + Implementing Regulation (EU) 2025/1960 (harmonised legal guarantee notice, 27 Sep 2026); verpackungsregister.org (LUCID).
EU_JS = r"""<script>(function(){function g(i){return document.getElementById(i)}
function run(){var out=g("eu-w").value=="out",sell=g("eu-s").value=="y",p=g("eu-p").value,c=g("eu-c").value,gt=g("eu-g").value=="y",phys=p!="dig",o=[],todo=[];
if(!sell){g("eu-out").innerHTML="<h2>Mostly not your concern</h2><p>If no listing is available to EU or Northern Ireland buyers, GPSR, the packaging rules and the EU guarantee notice don't apply to those sales. Check your Etsy shipping profiles really exclude the EU, and remember Northern Ireland follows GPSR too.</p>";return}
o.push("<h2>Rules that apply to you</h2>");
o.push("<h3>1. GPSR (product safety): applies</h3><p>Listings visible in the EU need the <strong>manufacturer's name, postal and electronic address</strong>"+(out?", and because you're outside the EU, an <strong>EU-based responsible person</strong> (name, address, contact)":"")+", plus product identification and any warnings or safety information. "+(p=="dig"?"For digital downloads most of the safety duties hardly apply, but Etsy's guidance says GPSR covers digital items too, so fill in the fields Etsy asks for.":"Keep a simple risk assessment and technical file for each product type.")+"</p>");
if(out)todo.push("Appoint an EU responsible person (Etsy partners with Cert-Rep and International Associates; others exist) and add them in Etsy, where they can be applied shop-wide.");
todo.push("Fill in manufacturer details on every listing visible in the EU, and add warnings or safety information where your product needs them.");
if(phys){o.push("<h3>2. PPWR (packaging): applies</h3><p>When you ship a packaged item straight to a buyer in an EU country, you are usually the <strong>packaging producer</strong> there: you register with that country's packaging register and pay for recycling through a scheme (extended producer responsibility). "+(out?"Since <strong>12 August 2026</strong>, sellers shipping directly to end users in a country where they aren't established must appoint an <strong>authorised representative for EPR in each of those countries</strong>; in Germany you still register in LUCID yourself.":"If you ship to other EU countries, you need an authorised representative in each country where you're not established.")+" There is no small-business exemption from registration.</p>");
todo.push("List the EU countries you actually ship to (Etsy Orders) and start with the biggest, usually Germany, France and the Netherlands.");todo.push("For each one, register as a packaging producer (Germany: LUCID) and appoint an authorised representative or compliance scheme; keep the registration numbers.")}
else o.push("<h3>2. PPWR (packaging): doesn't apply</h3><p>No packaging, no packaging rules.</p>");
if(phys){o.push("<h3>3. Legal guarantee notice: applies</h3><p>Since <strong>27 September 2026</strong>, anyone selling goods to EU consumers must show the EU's <strong>harmonised notice on the 2-year legal guarantee</strong> before the sale, in the buyer's language, with the official wording and design. "+(gt?"Because you offer a guarantee longer than 2 years, you can also use the voluntary <strong>GARAN</strong> durability label. ":"")+"On Etsy the simplest places are your listing images or description and your shop policies; check whether Etsy has added a setting for it in your country.</p>");todo.push("Add the harmonised legal guarantee notice (official design from the European Commission) to your listings and shop policies.")}
else o.push("<h3>3. Legal guarantee notice: probably not</h3><p>The notice is for goods; digital content has separate rules.</p>");
var ex={toy:"Toys: the toy safety rules need CE marking, a declaration of conformity, testing and age warnings. GPSR alone is not enough.",cos:"Cosmetics and soap: the EU Cosmetics Regulation needs a responsible person, a safety assessment and CPNP notification before you sell.",candle:"Candles: standard candle safety warnings and, for scented candles and wax melts, CLP hazard labels for fragrance allergens.",elec:"Batteries and electronics: CE marking, plus WEEE and battery producer registration in each country.",text:"Clothing and textiles: fibre content labelling, and textile EPR rules starting in some countries."};
if(c!="none"&&phys){o.push("<h3>4. Extra rules for your products</h3><p>"+ex[c]+"</p>");todo.push("Check the product-specific rules for your category before your next EU sale.")}
o.push("<h2>Your to-do list</h2><ol>"+todo.map(function(t){return "<li>"+t+"</li>"}).join("")+"</ol><p class=\"muted\">General information, not legal advice. Rules differ between EU countries; a compliance service or your EU representative can confirm what applies to you.</p>");
g("eu-out").innerHTML=o.join("")}
["eu-w","eu-s","eu-p","eu-c","eu-g"].forEach(function(i){g(i).addEventListener("input",run)});run()})();</script>"""
eu = top("EU rules checker for Etsy sellers (2026)", "Answer five questions about your shop. See which EU rules apply to you, what each one asks for, and a to-do list in order.", "EU rules checker") + """
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> if you sell <strong>physical products to buyers in the EU</strong> from outside the EU, three sets of rules matter in 2026: <strong>GPSR</strong> (manufacturer and EU responsible person details on your listings, since 13 December 2024), the <strong>PPWR</strong> packaging rules (producer registration, and since 12 August 2026 an authorised representative in each EU country you ship packaged goods to directly), and the <strong>harmonised legal guarantee notice</strong> (shown where you sell, since 27 September 2026). Digital-only shops have much less to do, but Etsy still asks for GPSR details on listings visible in the EU.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="eu-w">Where is your business based?</label><select id="eu-w"><option value="out">Outside the EU (US, UK, Pakistan, Canada and so on)</option><option value="in">In an EU country</option></select></div>
<div class="field"><label for="eu-s">Do you sell to buyers in the EU or Northern Ireland?</label><select id="eu-s"><option value="y">Yes</option><option value="n">No, I've turned off EU shipping</option></select></div>
<div class="field"><label for="eu-p">What do you sell?</label><select id="eu-p"><option value="phys">Physical items</option><option value="both">Both physical and digital</option><option value="dig">Digital downloads only</option></select></div>
<div class="field"><label for="eu-c">Do you sell any of these? (special rules on top of GPSR)</label><select id="eu-c"><option value="none">None of these</option><option value="toy">Toys or items for children</option><option value="cos">Cosmetics, soap, bath products</option><option value="candle">Candles or wax melts</option><option value="elec">Anything with batteries or electronics</option><option value="text">Clothing or textiles</option></select></div>
<div class="field"><label for="eu-g">Do you offer your own guarantee longer than 2 years?</label><select id="eu-g"><option value="n">No</option><option value="y">Yes</option></select></div>
</div><div class="result" aria-live="polite" id="eu-out"></div></div></section>
""" + EU_JS + f"""
<section><div class="wrap"><div class="narrow prose">
<h2>The three EU rules, in plain words</h2>
<h3>GPSR: General Product Safety Regulation (since 13 December 2024)</h3>
<p>Every consumer product sold in the EU must be safe, and buyers and authorities must be able to see who is responsible for it. For an Etsy seller outside the EU that means naming an EU-based responsible person and showing manufacturer details on your listings. Etsy can apply the responsible person shop-wide, but you still need to check each listing's safety information.</p>
<h3>PPWR: Packaging and Packaging Waste Regulation (since 12 August 2026)</h3>
<p>Whoever first puts packaging into an EU country pays to recycle it. If you post orders straight to EU buyers, that is usually you. You register in each country, report the packaging you send and pay a recycling scheme. Since 12 August 2026, sellers who aren't established in a country must also name an authorised representative there.</p>
<h3>Harmonised guarantee notice (since 27 September 2026)</h3>
<p>Every buyer of goods in the EU already has a 2-year legal guarantee. Sellers must now show the EU's standard notice explaining it, with fixed wording and design, wherever they sell, including online. The GARAN label is an optional extra for sellers who offer a longer durability guarantee.</p>
<h2>What about digital downloads?</h2>
<p>Downloads have no packaging and aren't "goods" for the guarantee notice. Etsy's guidance still says GPSR covers digital items, so complete the fields Etsy shows on digital listings visible in the EU.</p>
<p>Pricing your products after compliance costs? Use the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>.</p>
<div class="nl-card" id="eu-waitlist" style="margin:26px 0">
<div><h2>Get your whole shop checked automatically</h2><p>We're building a low-cost tool that scans every Etsy listing, flags the ones missing EU details, and fills them in bulk from your saved templates. Join the waitlist for early access and a launch discount. No spam: one email when it's ready.</p></div>
<form class="nl-form" action="https://app.kit.com/forms/10243558/subscriptions" method="post">
<label class="nl-sr" for="eu-email">Email address</label>
<input id="eu-email" type="email" name="email_address" required placeholder="Your email address" autocomplete="email">
<button type="submit">Join the waitlist</button>
</form>
</div>
<p class="muted">Sources: Etsy Help Centre (GPSR); Regulation (EU) 2023/988; Regulation (EU) 2025/40 (PPWR), Article 45; Directive (EU) 2024/825 and Implementing Regulation (EU) 2025/1960; German Central Agency Packaging Register (LUCID). Checked 26 November 2026. General information, not legal advice.</p>
</div></div></section>{more_seller("eu-rules-checker-etsy-sellers.html")}"""
eu_faq = [("Do Etsy sellers need an EU responsible person?", "Yes, if you're based outside the EU and sell products to EU buyers: GPSR requires an EU-based responsible person whose details appear on your listings."),
          ("What changed for packaging on 12 August 2026?", "The EU Packaging and Packaging Waste Regulation started applying. Sellers who ship packaged goods directly to buyers in an EU country where they aren't established must register as a packaging producer there and appoint an authorised representative."),
          ("What is the EU legal guarantee notice?", "From 27 September 2026, sellers of goods to EU consumers must show a standard EU notice explaining the 2-year legal guarantee, with fixed wording and design, wherever they sell."),
          ("Do digital downloads need GPSR details on Etsy?", "Etsy's guidance says GPSR applies to physical and digital products, so fill in the details Etsy asks for on digital listings visible in the EU. The packaging rules and the guarantee notice don't apply to downloads.")]
page("eu-rules-checker-etsy-sellers.html", "EU Rules Checker for Etsy Sellers 2026: GPSR, Packaging (PPWR) and Guarantee Notice | Purl & Paper",
     "Free EU rules checker for Etsy sellers: answer five questions to see if GPSR, the 12 August 2026 packaging rules (PPWR) and the 27 September 2026 guarantee notice apply to your shop.",
     eu, eu_faq, "EU rules checker", app_name="EU rules checker for Etsy sellers")

page("eu-waitlist-thanks.html", "You're on the waitlist | Purl & Paper", "Confirm your email to join the EU seller tool waitlist.",
     """<section><div class="wrap nl-done"><h1>Check your inbox</h1>
<p>We've emailed you a confirmation link. Tap it and you're on the waitlist for our EU listing checker for Etsy sellers. We'll email you once when early access opens.</p>
<p>Can't see it after a minute? Look in your spam or promotions folder.</p>
<div class="nl-links"><a href="/eu-rules-checker-etsy-sellers">EU rules checker</a><a href="/etsy-fee-calculator">Etsy fee calculator</a><a href="/seller-tools">All seller tools</a></div></div></section>""")
