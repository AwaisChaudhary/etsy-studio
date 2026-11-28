# ---------------- HOW TO KNIT AND PURL (DEMAND W3: completes the stitch library) ----------------
# Executed from build.py. Own drawings (English/throwing style, right-handed). Steps checked against Craft Yarn Council
# "Learn to knit", Lion Brand and Purl Soho beginner guides (SERP 26 Nov 2026), written in our own words.
_KN, _KB, _KG, _KT, _KY = "#1f2a44", "#b8326a", "#f4a823", "#2f8f8a", "#c9a37a"

def _kp_loop(x, y, col, front=True, part="all"):
    # a stitch sitting on a needle: back half then front half
    b = f'<path d="M{x-8} {y} q8 -20 16 0" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round" opacity=".55"/>'
    f = f'<path d="M{x-8} {y} q8 24 16 0" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
    return {"back": b, "front": f, "all": b + f}[part]

def kp_fig(kind, step):
    """kind: knit|purl. step: 1 insert, 2 wrap, 3 pull through, 4 slide off."""
    s = '<rect width="260" height="170" fill="#fff"/>'
    ln = 4 if step < 4 else 3                   # stitches left on the left needle
    lx = [118 - i * 22 for i in range(ln)]      # first stitch nearest the tip
    # left needle (holds the stitches to work)
    s += f'<line x1="8" y1="104" x2="138" y2="96" stroke="{_KY}" stroke-width="7" stroke-linecap="round"/><circle cx="8" cy="104" r="7" fill="{_KN}"/>'
    # right needle: back for knit (goes behind left needle), front for purl
    made = [176, 198] if step < 4 else [154, 176, 198]
    rn_back = kind == "knit"
    if step in (1, 2, 3):
        rn = f'<line x1="252" y1="{126 if rn_back else 70}" x2="112" y2="{82 if rn_back else 112}" stroke="{_KT}" stroke-width="7" stroke-linecap="round"/>'
    else:
        rn = f'<line x1="252" y1="100" x2="140" y2="88" stroke="{_KT}" stroke-width="7" stroke-linecap="round"/>'
    loops_back = "".join(_kp_loop(x, 100 + (118 - x) * 0.06, _KG, part="back") for x in lx)
    loops_front = "".join(_kp_loop(x, 100 + (118 - x) * 0.06, _KG, part="front") for x in lx)
    if step == 4:
        rmade = "".join(_kp_loop(x, 95 - (x - 154) * 0.1, _KB if x == 154 else "#d97aa0") for x in made)
    else:
        rmade = ""
    s += loops_back
    s += rn if rn_back or step == 4 else ""
    s += loops_front
    s += rn if (not rn_back and step < 4) else ""
    s += rmade
    # working yarn: from the last made stitch; at the back for knit (dashed = behind), in front for purl
    yx = 200
    if step == 4:
        ytxt = ""
    elif kind == "knit":
        s += f'<path d="M{yx} 108 C {yx+6} 140, {yx-20} 150, {yx-10} 166" fill="none" stroke="{_KB}" stroke-width="3" stroke-dasharray="5 4"/>'
    else:
        s += f'<path d="M{yx} 108 C {yx-4} 130, {yx-30} 140, {yx-24} 166" fill="none" stroke="{_KB}" stroke-width="3"/>'
    # step marks
    tipx, tipy = (124, 88) if rn_back else (124, 106)
    if step == 1:
        if kind == "knit":
            s += f'<path d="M150 50 q-20 2 -30 24" fill="none" stroke="{_KN}" stroke-width="2"/><path d="M116 70 l4 8 l5 -7" fill="none" stroke="{_KN}" stroke-width="2"/>'
            lab = "Into the stitch: front to back"
        else:
            s += f'<path d="M150 140 q-22 -4 -30 -24" fill="none" stroke="{_KN}" stroke-width="2"/><path d="M116 122 l4 -8 l5 7" fill="none" stroke="{_KN}" stroke-width="2"/>'
            lab = "Into the stitch: back to front"
        s += f'<text x="142" y="24" font-size="12" font-weight="700" fill="{_KN}" text-anchor="middle">{lab}</text>'
    elif step == 2:
        s += f'<path d="M{tipx+14} {tipy-14} a12 12 0 1 0 2 22" fill="none" stroke="{_KB}" stroke-width="4"/><path d="M{tipx+12} {tipy+4} l6 4 l-1 -8" fill="none" stroke="{_KN}" stroke-width="2"/>'
        s += f'<text x="142" y="24" font-size="12" font-weight="700" fill="{_KN}" text-anchor="middle">Wrap the yarn round the needle</text>'
    elif step == 3:
        s += f'<ellipse cx="{tipx-6}" cy="{tipy}" rx="9" ry="13" fill="none" stroke="{_KB}" stroke-width="5"/>'
        if kind == "knit":
            s += f'<path d="M100 66 q-6 -16 8 -26" fill="none" stroke="{_KN}" stroke-width="2"/><path d="M102 42 l7 -2 l-1 7" fill="none" stroke="{_KN}" stroke-width="2"/>'
            lab = "Pull the loop through to the front"
        else:
            s += f'<path d="M100 126 q-6 16 8 26" fill="none" stroke="{_KN}" stroke-width="2"/><path d="M102 150 l7 2 l-1 -7" fill="none" stroke="{_KN}" stroke-width="2"/>'
            lab = "Push the loop through to the back"
        s += f'<text x="142" y="24" font-size="12" font-weight="700" fill="{_KN}" text-anchor="middle">{lab}</text>'
    else:
        s += f'<path d="M140 128 q8 10 -4 18" fill="none" stroke="{_KN}" stroke-width="2"/><text x="160" y="150" font-size="11" fill="{_KN}">old stitch slides off</text>'
        s += f'<text x="142" y="24" font-size="12" font-weight="700" fill="{_KN}" text-anchor="middle">Slide the old stitch off</text>'
    yl = "yarn at the back" if kind == "knit" else "yarn in front"
    if step < 4:
        s += f'<text x="246" y="162" font-size="11" fill="{_KB}" text-anchor="end">{yl}</text>'
    s += f'<text x="10" y="136" font-size="10" fill="#777">left needle</text><text x="250" y="60" font-size="10" fill="#777" text-anchor="end">right needle</text>'
    return f'<svg viewBox="0 0 260 170" role="img" aria-label="{kind} stitch, step {step}">{s}</svg>'

KP_KNIT = [("Insert", "Hold the needle with the stitches in your left hand, yarn at the back. Push the tip of the right needle into the first stitch from front to back, going in from left to right, so the right needle sits behind the left one."),
           ("Wrap", "With your right hand, wrap the working yarn around the right needle tip, under and then over it, anticlockwise (towards you, then away)."),
           ("Pull through", "Bring the right needle tip, with the wrapped yarn on it, back through the stitch towards you. You now have a new loop on the right needle."),
           ("Slide off", "Slide the old stitch off the left needle. One knit stitch made. Repeat into the next stitch until the left needle is empty, then swap needles and start the next row.")]
KP_PURL = [("Insert", "Bring the yarn to the front, between the needle tips. Push the right needle into the front of the first stitch from back to front, going in from right to left, so it sits in front of the left needle."),
           ("Wrap", "Wrap the yarn around the right needle tip anticlockwise: over the top and down between the needles."),
           ("Push through", "Push the right needle tip back through the stitch, away from you, taking the new loop with it."),
           ("Slide off", "Slide the old stitch off the left needle. One purl stitch made, with the yarn still in front, ready for the next purl.")]

def kp_steps(kind, rows):
    return '<div class="kp-steps">' + "".join(f'<figure><span class="kp-n">{i + 1}</span>{kp_fig(kind, i + 1)}<figcaption><strong>{e(t)}.</strong> {e(x)}</figcaption></figure>' for i, (t, x) in enumerate(rows)) + '</div>'

KP_FACE = f'''<svg viewBox="0 0 300 120" role="img" aria-label="Knit stitches look like Vs, purl stitches look like bumps"><rect width="300" height="120" fill="#fff"/>
{"".join(f'<path d="M{20+c*22} {18+r*24} l10 18 l10 -18" fill="none" stroke="{_KG}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' for r in range(4) for c in range(5))}
{"".join(f'<path d="M{170+c*22} {26+r*24} q10 {(-12 if (c+r)%2 else 12)} 20 0" fill="none" stroke="{_KB}" stroke-width="5" stroke-linecap="round"/>' for r in range(4) for c in range(5))}
<text x="70" y="116" font-size="12" font-weight="700" fill="{_KN}" text-anchor="middle">knit: little Vs</text><text x="220" y="116" font-size="12" font-weight="700" fill="{_KN}" text-anchor="middle">purl: bumps</text></svg>'''

KP_JS = r'''<script>(function(){var g=function(i){return document.getElementById(i)};if(!g("kp-pat"))return;
var F={st:function(r,x){return 1},ga:function(r,x){return r%2==0?1:0},r1:function(r,x){return x%2==0?1:0},r2:function(r,x){return x%4<2?1:0},seed:function(r,x){return(x+r)%2==0?1:0},
 bw:function(r,x){var b=Math.floor(r/4)%2;return (Math.floor(x/4)%2==b)?1:0}};
function ops(p,r,n){var o=[];for(var i=0;i<n;i++){var xr=(r%2==0)?i:n-1-i,k=F[p](r,xr);o.push(r%2==0?(k?"k":"p"):(k?"p":"k"))}return o}
function rl(a){var u=[],i=0;while(i<a.length){var j=i;while(j<a.length&&a[j]==a[i])j++;u.push(a[i]+(j-i));i=j}return u}
function say(o){var n=o.length;for(var p=1;p<=8&&p<=n;p++){var best=null;for(var a=0;a<p&&a<n;a++){var ok=true;for(var i=a;i<n;i++)if(o[i]!=o[a+((i-a)%p)]){ok=false;break}if(!ok)continue;
  var reps=Math.floor((n-a)/p);if(reps<2&&p>1)continue;var L=o.slice(0,a),U=o.slice(a,a+p),Tl=o.slice(a+reps*p),sc=rl(L).length+rl(Tl).length+rl(U).length;if(!best||sc<best.sc)best={L:L,U:U,T:Tl,sc:sc}}
 if(!best)continue;if(p==1&&!best.L.length)return o[0]=="k"?"Knit every stitch.":"Purl every stitch.";
 var t=best.T.length;return (best.L.length?rl(best.L).join(", ")+", ":"")+"*"+rl(best.U).join(", ")+"; repeat from * "+(t?"to last "+(t>1?t+" sts":"st")+", "+rl(best.T).join(", ")+".":"to end.")}
 return rl(o).join(", ")}
function run(){var p=g("kp-pat").value,n=Math.max(2,Math.min(200,parseInt(g("kp-n").value)||20)),L=[],per=1,txt=[];
 for(var r=0;r<8;r++)txt.push(say(ops(p,r,n)));for(per=1;per<=8;per++){var ok=true;for(var r=0;r<8;r++)if(txt[r]!=txt[r%per]){ok=false;break}if(ok)break}
 var h="<h2>Your rows</h2><p class=\"sub\">"+n+" stitches, worked flat (back and forth).</p><ol class=\"kp-rows\">";
 for(var r=0;r<per;r++)h+="<li><strong>Row "+(r+1)+(per>1?(r%2==0?" (right side)":" (wrong side)"):"")+":</strong> "+txt[r]+"</li>";
 h+="</ol><p>Repeat "+(per==1?"this row":"rows 1 to "+per)+" for the pattern.</p>";
 var cols=Math.min(n,30),rows=12,cs=11,W=cols*cs+8,H=rows*cs+8,s="";
 for(var r=0;r<rows;r++)for(var x=0;x<cols;x++){var k=F[p](r,x),cx=W-4-(x+0.5)*cs,cy=H-4-(r+0.5)*cs;
  s+=k?'<path d="M'+(cx-4)+' '+(cy-4)+' l4 7 l4 -7" fill="none" stroke="#f4a823" stroke-width="2.2" stroke-linecap="round"/>':'<path d="M'+(cx-4.5)+' '+(cy+1)+' q4.5 '+((x+r)%2?-5:5)+' 9 0" fill="none" stroke="#d97aa0" stroke-width="2.4" stroke-linecap="round"/>'}
 h+='<figure style="margin:12px 0 0;background:#fff;border-radius:8px;padding:6px"><svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Preview of the right side">'+s+'</svg><figcaption class="note" style="color:#555;margin:4px 0 0">How the right side looks'+(n>30?" (first 30 stitches)":"")+'. Row 1 at the bottom.</figcaption></figure>';
 g("kp-out").innerHTML=h;try{localStorage.setItem("pp-kp",p+"|"+n)}catch(e){}}
try{var sv=(localStorage.getItem("pp-kp")||"").split("|");if(sv[0]&&g("kp-pat").querySelector('option[value="'+sv[0]+'"]')){g("kp-pat").value=sv[0];g("kp-n").value=sv[1]||20}}catch(e){}
["kp-pat","kp-n"].forEach(function(i){g(i).addEventListener("input",run)});run()})();</script>'''

KP_CSS = '<style>.kp-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:14px 0 24px}.kp-steps figure{margin:0;background:var(--sheet);border-radius:12px;padding:10px;box-shadow:var(--shadow);position:relative}.kp-steps svg{width:100%;height:auto;display:block;border-radius:8px}.kp-steps figcaption{font-size:.95rem;margin-top:8px}.kp-n{position:absolute;top:8px;left:8px;background:var(--ink);color:#fff;border-radius:50%;width:26px;height:26px;display:grid;place-items:center;font-weight:700;font-size:.9rem}.kp-rows li{margin-bottom:6px}#kp-out svg{width:100%;height:auto;display:block}</style>'

KP_TBL = [("Stockinette (stocking stitch)", "Row 1 knit, row 2 purl", "Smooth Vs on the front, bumps on the back", "Curls at the edges", "Sweaters, hats, socks"),
          ("Garter stitch", "Knit every row", "Ridges on both sides, looks the same front and back", "Lies flat", "Scarves, dishcloths, first projects"),
          ("1x1 rib", "Knit 1, purl 1 (knit the knits, purl the purls)", "Narrow columns, very stretchy", "Lies flat, pulls in", "Cuffs, hat brims, necklines"),
          ("2x2 rib", "Knit 2, purl 2", "Wider columns, stretchy", "Lies flat, pulls in", "Hat brims, sock cuffs"),
          ("Seed stitch (UK: moss stitch)", "Knit 1, purl 1, and knit the purls and purl the knits on the next row", "Pebbly texture, same both sides", "Lies flat", "Borders, blankets, washcloths"),
          ("Basketweave", "Blocks of 4 knits and 4 purls, swapped every 4 rows", "Checkerboard squares", "Mostly flat", "Blankets, cushions")]
kp_rows = "".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{f}</td></tr>" for a, b, c, d, f in KP_TBL)

kp = top("How to knit and purl: the two stitches every pattern uses", "Every knitting pattern, from a garter scarf to a cabled sweater, is made of knit and purl stitches. Learn both in four steps each, with our own drawings, then use the pattern maker to write out the rows for stockinette, garter, rib or seed stitch.", "How to knit and purl") + KP_CSS + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> to <strong>knit</strong>, keep the yarn at the back, put the right needle into the stitch <strong>from front to back</strong>, wrap the yarn, pull the new loop through to the front and slide the old stitch off. To <strong>purl</strong>, bring the yarn to the front, go into the stitch <strong>from back to front</strong>, wrap, push the loop through to the back and slide off. Knitting every row makes <strong>garter stitch</strong>; knitting one row and purling the next makes <strong>stockinette</strong> (smooth Vs on the front).</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="narrow prose">
<h2>How to knit stitch: step by step</h2>
<p>Cast on about 20 stitches first (see <a href="{href("how-to-cast-on-knitting.html")}">how to cast on</a>), using a smooth, light-coloured worsted yarn and 5 mm (US 8) needles so you can see each stitch.</p></div>
{kp_steps("knit", KP_KNIT)}
<div class="narrow prose"><p class="note">Our drawings, right-handed, English (throwing) style. The dashed yarn is behind the work. Continental knitters hold the yarn in the left hand and pick it with the needle instead of wrapping, but the needle goes into the stitch the same way.</p>
<h2>How to purl stitch: step by step</h2>
<p>The purl is the knit stitch done from the other side. The two differences: the yarn is <strong>in front</strong>, and the right needle goes in <strong>from the back of the stitch to the front</strong>.</p></div>
{kp_steps("purl", KP_PURL)}
</div></section>
{AD.format("kp-mid")}
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h2 style="margin-top:0">Knit and purl pattern maker</h2>
<p class="note" style="margin-top:0">Pick a stitch pattern and how many stitches you cast on. You get each row in plain words and a preview of the right side.</p>
<div class="row2"><div class="field"><label for="kp-pat">Stitch pattern</label><select id="kp-pat"><option value="st">Stockinette (stocking stitch)</option><option value="ga">Garter stitch</option><option value="r1">1x1 rib</option><option value="r2">2x2 rib</option><option value="seed">Seed stitch (UK moss)</option><option value="bw">Basketweave (4x4 blocks)</option></select></div>
<div class="field"><label for="kp-n">Stitches cast on</label><input type="number" id="kp-n" value="20" min="2" max="200" step="1" inputmode="numeric"></div></div>
<p class="note">Odd or even counts both work: the maker adds the extra stitch at the end so ribs and seed stitch line up. Want a set width? The <a href="{href("cast-on-calculator.html")}">cast on calculator</a> gives you the number.</p>
</div><div class="result" aria-live="polite" id="kp-out"></div></div></section>
{KP_JS}
<section style="padding-top:0"><div class="wrap"><h2>What knit and purl make: the beginner stitch patterns</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Pattern</th><th scope="col">How</th><th scope="col">Looks like</th><th scope="col">Edges</th><th scope="col">Good for</th></tr></thead><tbody>{kp_rows}</tbody></table></div><p>Ready for more textures? The <a href="{href("knit-stitch-patterns.html")}">knit stitch patterns library</a> has 15 knit and purl stitches (moss, double seed, garter rib, mistake rib, welt and more) with swatch drawings, rows and stitch multiples.</p></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>How do I tell a knit stitch from a purl stitch?</h2>
<figure class="co-fig">{KP_FACE}<figcaption class="note">Our drawing. Look at the stitches just below the needle.</figcaption></figure>
<p>A knit stitch looks like a little <strong>V</strong>. A purl stitch looks like a little <strong>bump</strong>, like a bead on a string. They're the same stitch seen from opposite sides: the back of every knit is a purl. That's why "knit the knits and purl the purls" works for ribbing: look at the stitch, and if it's a V, knit it; if it's a bump, purl it.</p>
<h2>Why did I get extra stitches when switching from knit to purl?</h2>
<p>When you change between knit and purl in the same row, the yarn has to move between the needle tips: to the front before a purl, to the back before a knit. If you take it over the needle instead, it wraps the needle and makes an extra loop (a yarn over) and a hole. Count your stitches at the end of each row while you learn, and use a <a href="{href("row-counter.html")}">row counter</a> so you know which row you're on.</p>
<h2>Why is my knitting so tight (or so loose)?</h2>
<p>Usually you're pulling the yarn after every stitch, or working on the very tips of the needles. Make each new stitch on the thick part of the right needle, not the tip, and let the yarn run through your fingers without tugging. Loose, uneven purls are common too (some knitters call it "rowing out"); wrapping the purl a little more snugly usually fixes it. Your stitches even out with practice, so knit a 20-stitch swatch before a project and check your <a href="{href("gauge-converter.html")}">gauge</a>.</p>
<h2>Which is easier, knit or purl?</h2>
<p>Most beginners find the knit stitch easier, which is why a garter stitch scarf (knit every row) is the classic first project. Once you're comfortable, add the purl and try stockinette, then ribbing for a hat brim. Both stitches take the same four moves: in, wrap, through, off.</p>
<h2>What does "right side" and "wrong side" mean?</h2>
<p>The right side (RS) is the side that will show. In stockinette it's the smooth knit side. The wrong side (WS) is the back, with the purl bumps. When you knit flat you turn the work at the end of each row, so you work RS rows and WS rows in turn; when you <a href="{href("how-to-knit-in-the-round.html")}">knit in the round</a> the right side always faces you, so stockinette is just knit every round.</p>
<div class="callout"><strong>First project idea:</strong> a <a href="{href("how-to-knit-a-dishcloth.html")}">dishcloth</a> (done in an evening) or a garter stitch scarf. Pick the size in the <a href="{href("scarf-size-chart.html")}">scarf size chart</a>, then shape things later with <a href="{href("how-to-increase-knitting.html")}">how to increase in knitting</a>, and finish with <a href="{href("how-to-bind-off-knitting.html")}">how to bind off</a> and <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>.</div>
<p>What next? Once knit and purl feel easy, try <a href="{href("how-to-knit-cables.html")}">knitting cables</a>: they are only knit stitches worked out of order. Fix mistakes with <a href="{href("how-to-fix-a-dropped-stitch.html")}">how to fix a dropped stitch</a>, decode patterns with the <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a>, and pick needles in the <a href="{href("hook-needle-sizes.html")}">needle size chart</a>. Prefer a hook? See <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>.</p>
</div></div></section>'''
kp_faq = [
    ("How do you knit a stitch step by step?", "Yarn at the back. Put the right needle into the first stitch from front to back, wrap the yarn around the right needle anticlockwise, pull the new loop through to the front, and slide the old stitch off the left needle."),
    ("How do you purl step by step?", "Yarn in front. Put the right needle into the first stitch from back to front (right to left), wrap the yarn anticlockwise, push the new loop through to the back, and slide the old stitch off."),
    ("What is the difference between knit and purl?", "They're the same stitch from opposite sides. A knit makes a V on the side facing you and a purl makes a bump. Knit goes in front to back with the yarn behind; purl goes in back to front with the yarn in front."),
    ("What happens if you only knit every row?", "You get garter stitch: ridged on both sides, flat and a little stretchy. Knit one row and purl the next for stockinette."),
    ("Why does my stockinette curl?", "Stockinette always curls at the edges because the knit and purl sides pull differently. Add a garter, seed or rib border a few stitches wide, or block it; a border is the reliable fix."),
    ("What does k1, p1 mean?", "Knit 1 stitch, purl 1 stitch, then repeat. Bring the yarn between the needles to the front before each purl and to the back before each knit."),
]
SHOP_FOR["how-to-knit-and-purl.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("how-to-knit-and-purl.html", "How to Knit and Purl for Beginners + Pattern Maker | Purl & Paper",
     "Learn the knit and purl stitches in 4 steps each with drawings, how to tell them apart, and a free pattern maker for stockinette, garter, rib and seed stitch.",
     kp, kp_faq, "How to knit and purl", app_name="Knit and purl stitch pattern maker")
