# ---------------- NEW CRAFT CATEGORIES (Awais 25 Nov 2026: "add new categories, based on data and demand") ----------------
# Executed from build.py (shares page(), top(), href(), shop_box(), e()). Keyword Planner US volumes in DEMAND.md C1-C7.
# JS lives in plain strings; "{H:file}" placeholders are swapped for real links by L().
import re as _re
def L(s): return _re.sub(r"\{H:([a-z0-9-]+\.html)\}", lambda m: href(m.group(1)), s)

CRAFTS = [
 ("crafts.html", "All crafts", "Every craft we cover, with its free tools."),
 ("calligraphy-practice-sheets.html", "Calligraphy practice sheets", "Make printable guideline sheets for any pen: x-height, slant and spacing."),
 ("2027-calendar-printable.html", "2027 calendar printable", "Free 2027 calendar, yearly or monthly, with US or UK holidays, Letter or A4."),
 ("dot-grid-paper.html", "Dot grid paper (bullet journal)", "Printable dot grid, graph and lined paper in any spacing, A4 or Letter."),
 ("diamond-painting-calculator.html", "Diamond painting calculator", "How many drills fit your canvas, round or square, and how long it will take."),
 ("cross-stitch-calculator.html", "Cross stitch calculator", "Finished size on any fabric count, how much fabric to cut and how many skeins."),
 ("quilt-size-calculator.html", "Quilt size calculator", "Quilt size for any bed, plus backing and binding yardage."),
 ("candle-making-calculator.html", "Candle wax calculator", "Wax and fragrance oil for any jar and batch, with cost per candle."),
 ("resin-calculator.html", "Resin calculator", "How much epoxy resin and hardener to mix for a mould, tray or table."),
 ("macrame-cord-calculator.html", "Macrame cord calculator", "How many cords to cut, how long, and how much cord to buy."),
 ("half-square-triangle-calculator.html", "Half square triangle calculator", "What size squares to cut for HSTs, 2, 4 or 8 at a time, and how much fabric."),
 ("polymer-clay-baking-calculator.html", "Polymer clay baking calculator", "Oven temperature and bake time for your clay brand and thickness."),
]
exec((ROOT / "newcrafts_list.py").read_text())
CRAFT_LINKS = '<ul class="craft-links">' + "".join(f'<li><a href="{href(f)}">{n}</a> <span class="muted">{d}</span></li>' for f, n, d in CRAFTS[1:]) + "</ul>"
def more_crafts(file):
    return '<section><div class="wrap"><div class="narrow prose"><h2>More free craft tools</h2><ul>' + "".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n, _ in CRAFTS if f != file) + "</ul></div></div></section>"

# ---- Crafts hub ----
hub = top("Free craft tools and calculators", "Knitting, crochet and junk journals are where we started. These are the other crafts our readers asked about, each with a free tool that does the maths for you.", "All crafts") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="narrow prose">
<h2>Paper and lettering</h2>
<ul><li><a href="{href("calligraphy-practice-sheets.html")}">Calligraphy practice sheets</a>: guideline sheets for brush pens and pointed pens, set to your x-height and slant.</li>
<li><a href="{href("2027-calendar-printable.html")}">2027 calendar printable</a>: the whole year on one page or a month per page, with US or UK holidays.</li>
<li><a href="{href("dot-grid-paper.html")}">Dot grid paper</a>: the bullet journal standard, plus graph and lined paper, ready to print.</li>
<li><a href="{href("junk-journal-beginners.html")}">Junk journaling for beginners</a> and the <a href="{href("journal-prompts.html")}">journal prompt generator</a>.</li></ul>
<h2>Needlework</h2>
<ul><li><a href="{href("cross-stitch-calculator.html")}">Cross stitch calculator</a>: finished size on Aida or evenweave, fabric to cut and floss to buy.</li>
<li><a href="{href("how-to-cross-stitch.html")}">How to cross stitch for beginners</a>: supplies, the stitch in five drawn steps, and which needle and strands to use.</li>
<li><a href="{href("quilt-size-calculator.html")}">Quilt size calculator</a>: finished size for any bed, backing and binding yardage.</li>
<li><a href="{href("half-square-triangle-calculator.html")}">Half square triangle calculator</a>: cut sizes for HSTs made 2, 4 or 8 at a time.</li>
<li><a href="{href("fat-quarter-calculator.html")}">Fat quarter calculator</a>: squares and strips per fat quarter, and how many a quilt needs.</li>
<li><a href="{href("sewing-seam-allowance.html")}">Seam allowance guide</a>: standard allowances for dressmaking, quilting and home decor, with a cut size calculator.</li>
<li><a href="{href("diamond-painting-calculator.html")}">Diamond painting calculator</a>: drills per canvas and time to finish.</li></ul>
<h2>Clay</h2>
<ul><li><a href="{href("polymer-clay-baking-calculator.html")}">Polymer clay baking calculator</a>: oven temperature and time for Sculpey, Premo, Fimo, Kato and Cernit by thickness.</li></ul>
<h2>Fibre and cord</h2>
<ul><li><a href="{href("macrame-cord-calculator.html")}">Macrame cord calculator</a>: how many cords and how long to cut them.</li>
<li>Knitting and crochet: the <a href="{href("yarn-calculator.html")}">yarn calculator</a>, <a href="{href("row-counter.html")}">row counter</a> and <a href="{href("gauge-converter.html")}">gauge converter</a>.</li></ul>
<h2>Making to sell: candles and resin</h2>
<ul><li><a href="{href("candle-making-calculator.html")}">Candle wax and fragrance calculator</a>: wax for any jar, fragrance load and cost per candle.</li>
<li><a href="{href("resin-calculator.html")}">Resin calculator</a>: resin and hardener for moulds, trays and river tables.</li>
<li><a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>: what Etsy takes and what to charge.</li></ul>
<p class="muted">Every tool runs in your browser. Nothing you type is uploaded.</p>
</div></div></section>'''
hub = hub.replace("<h2>Clay</h2>", L(NEW_HUB) + "<h2>Clay</h2>", 1)
page("crafts.html", "Free Craft Calculators and Printables | Purl & Paper",
     "Free craft tools: calligraphy practice sheets, dot grid paper, cross stitch, quilt size, diamond painting, candle wax, resin and macrame cord calculators.",
     hub, None, "All crafts")

# ---- Shared printable sheet generator (calligraphy + dot grid) ----
SHEET_JS = r'''<script>(function(){var P={a4:[210,297],letter:[215.9,279.4]};
function g(i){return document.getElementById(i)}
window.PPsheet=function(kind){var p=P[g("ps-paper").value],W=p[0],Hh=p[1],m=12,s="";
if(kind=="cal"){var x=+g("ps-x").value||5,asc=+g("ps-asc").value||3,des=+g("ps-des").value||3,ang=+g("ps-ang").value||55,gap=+g("ps-gap").value||3,line=x*(1+asc/2+des/2),y=m+x*asc/2;
 while(y+x+x*des/2<=Hh-m){var base=y+x,top=y,a=y-x*asc/2,d=base+x*des/2;
  s+='<line x1="'+m+'" x2="'+(W-m)+'" y1="'+a+'" y2="'+a+'" stroke="#bbb" stroke-width=".2"/>';
  s+='<rect x="'+m+'" y="'+top+'" width="'+(W-2*m)+'" height="'+x+'" fill="#f3eef8"/>';
  s+='<line x1="'+m+'" x2="'+(W-m)+'" y1="'+top+'" y2="'+top+'" stroke="#8a7aa8" stroke-width=".3"/>';
  s+='<line x1="'+m+'" x2="'+(W-m)+'" y1="'+base+'" y2="'+base+'" stroke="#333" stroke-width=".45"/>';
  s+='<line x1="'+m+'" x2="'+(W-m)+'" y1="'+d+'" y2="'+d+'" stroke="#bbb" stroke-width=".2"/>';
  if(ang<90){var dx=(d-a)/Math.tan(ang*Math.PI/180),st=gap*x;for(var X=m;X+dx<=W-m;X+=st){s+='<line x1="'+(X)+'" y1="'+d+'" x2="'+(X+dx)+'" y2="'+a+'" stroke="#ccc" stroke-width=".15"/>'}}
  y=d+x*0.8+x*asc/2}}
else{var sp=+g("ps-sp").value||5,t=g("ps-type").value,cols=Math.floor((W-2*m)/sp),rows=Math.floor((Hh-2*m)/sp),ox=(W-cols*sp)/2,oy=(Hh-rows*sp)/2;
 if(t=="dot"){for(var i=0;i<=rows;i++)for(var j=0;j<=cols;j++)s+='<circle cx="'+(ox+j*sp)+'" cy="'+(oy+i*sp)+'" r=".28" fill="#777"/>'}
 else if(t=="grid"){for(var i=0;i<=rows;i++)s+='<line x1="'+ox+'" x2="'+(ox+cols*sp)+'" y1="'+(oy+i*sp)+'" y2="'+(oy+i*sp)+'" stroke="#bbb" stroke-width=".18"/>';for(var j=0;j<=cols;j++)s+='<line y1="'+oy+'" y2="'+(oy+rows*sp)+'" x1="'+(ox+j*sp)+'" x2="'+(ox+j*sp)+'" stroke="#bbb" stroke-width=".18"/>'}
 else{for(var i=0;i<=rows;i++)s+='<line x1="'+ox+'" x2="'+(ox+cols*sp)+'" y1="'+(oy+i*sp)+'" y2="'+(oy+i*sp)+'" stroke="#bbb" stroke-width=".2"/>'}}
var svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+Hh+'" width="'+W+'mm" height="'+Hh+'mm"><rect width="'+W+'" height="'+Hh+'" fill="#fff"/>'+s+'</svg>';
g("ps-prev").innerHTML=svg;window.PPsvg=svg;window.PPsize=[W,Hh]};
window.PPprint=function(){var w=window.open("","_blank");if(!w)return;w.document.write('<!DOCTYPE html><html><head><title>Printable sheet</title><style>@page{size:'+window.PPsize[0]+'mm '+window.PPsize[1]+'mm;margin:0}body{margin:0}svg{display:block}</style></head><body>'+window.PPsvg+'<scr'+'ipt>setTimeout(function(){print()},300)</scr'+'ipt></body></html>');w.document.close()};
window.PPdl=function(name){var b=new Blob([window.PPsvg],{type:"image/svg+xml"}),a=document.createElement("a");a.href=URL.createObjectURL(b);a.download=name+".svg";a.click()};
})();</script>'''
PREV_CSS = '<style>#ps-prev{background:#fff;border:1px solid #ddd;border-radius:8px;padding:6px;max-width:420px}#ps-prev svg{width:100%;height:auto;display:block}.craft-links li{margin-bottom:6px}</style>'

cal = top("Calligraphy practice sheets (printable, free)", "Set your pen's x-height, ascenders, descenders and slant. Print as many guideline sheets as you like, or save them as an image for your iPad.", "Calligraphy practice sheets") + PREV_CSS + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> for a <strong>small brush pen</strong> (Tombow Fudenosuke size) start with a <strong>5 mm x-height</strong>; for a <strong>large brush pen</strong> use <strong>7 to 9 mm</strong>; for a <strong>pointed pen</strong> 4 to 6 mm. Modern brush calligraphy uses a <strong>slant of about 55°</strong>; leave it at 90° for upright lettering.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="ps-pen">Your pen (sets the sizes)</label><select id="ps-pen"><option value="5,3,3">Small brush pen (5 mm)</option><option value="8,3,3">Large brush pen (8 mm)</option><option value="5,3,3,1">Pointed pen, copperplate style (5 mm)</option><option value="7,2,2">Broad edge / italic (7 mm)</option></select></div>
<div class="row2"><div class="field"><label for="ps-x">x-height (mm)</label><input type="number" id="ps-x" value="5" min="2" max="30" step="0.5"></div>
<div class="field"><label for="ps-ang">Slant angle (°)</label><input type="number" id="ps-ang" value="55" min="45" max="90" step="1"></div></div>
<div class="row2"><div class="field"><label for="ps-asc">Ascender (× x-height)</label><input type="number" id="ps-asc" value="3" min="1" max="4" step="0.5"></div>
<div class="field"><label for="ps-des">Descender (× x-height)</label><input type="number" id="ps-des" value="3" min="1" max="4" step="0.5"></div></div>
<div class="row2"><div class="field"><label for="ps-gap">Slant line spacing (× x-height)</label><input type="number" id="ps-gap" value="3" min="1" max="8" step="0.5"></div>
<div class="field"><label for="ps-paper">Paper</label><select id="ps-paper"><option value="letter">US Letter</option><option value="a4">A4</option></select></div></div>
<div class="btns"><button type="button" class="btn" onclick="PPprint()">Print sheet</button> <button type="button" class="btn" onclick="PPdl('calligraphy-practice-sheet')">Save as image (SVG)</button></div>
</div><div class="result"><h2>Preview</h2><div id="ps-prev"></div><p class="note">Shaded band = x-height. Dark line = baseline. Light lines = ascender and descender limits. Diagonals = your slant.</p></div></div></section>
{SHEET_JS}<script>(function(){{var ids=["ps-x","ps-ang","ps-asc","ps-des","ps-gap","ps-paper"];function r(){{PPsheet("cal")}}ids.forEach(function(i){{document.getElementById(i).addEventListener("input",r)}});
document.getElementById("ps-pen").addEventListener("change",function(){{var v=this.value.split(",");document.getElementById("ps-x").value=v[0];document.getElementById("ps-asc").value=v[1];document.getElementById("ps-des").value=v[2];document.getElementById("ps-ang").value=v[0]=="7"?"85":"55";r()}});r()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>How to use calligraphy guidelines</h2>
<p>Every letter sits on the <strong>baseline</strong>. Small letters (a, c, e, o) fill the shaded <strong>x-height</strong> band. Tall strokes (b, d, h, k, l) reach up to the ascender line, and tails (g, j, p, y) drop to the descender line. The diagonal lines keep every downstroke at the same angle, which is most of what makes lettering look neat.</p>
<h2>The basic rule: thin up, thick down</h2>
<p>In brush and pointed-pen calligraphy you press on every <strong>downstroke</strong> to get a thick line and ease off on every <strong>upstroke</strong> to get a hairline. Practise the basic strokes before whole letters: the upstroke, downstroke, overturn, underturn, compound curve, oval, ascending loop and descending loop. Fill a sheet with each one, slowly. Speed comes later.</p>
<h2>Which pen should a beginner use?</h2>
<p>A <strong>small, firm-tip brush pen</strong> is the easiest start: it's forgiving, needs no ink pot and works on smooth printer paper. Move to a large brush pen for bigger, bolder letters, and to a pointed pen (nib, holder and ink) for copperplate and modern pointed-pen scripts. Broad-edge pens are a different family: the thick and thin come from the angle of the nib, not pressure, and the letters are usually more upright.</p>
<h2>Which paper won't fray brush pens?</h2>
<p>Very smooth paper. Ordinary copy paper is rough enough to fray felt brush tips over time, so many letterers use smooth laser paper or marker paper (around 90 to 120 gsm). Print the sheet, or slip it under a sheet of tracing or marker paper and letter on top so one printout lasts for weeks.</p>
<h2>Practising on an iPad</h2>
<p>Choose "Save as image", open the file in Procreate or GoodNotes and put it on its own layer underneath your writing. Set the x-height to match the brush size you use there.</p>
<p>Planning a journal spread? Print <a href="{href("dot-grid-paper.html")}">dot grid paper</a> for your bullet journal, or try a <a href="{href("junk-journal-beginners.html")}">junk journal</a>.</p>
</div></div></section>{more_crafts("calligraphy-practice-sheets.html")}'''
cal_faq = [
 ("What x-height should I use for calligraphy practice?", "About 5 mm for a small brush pen or a pointed pen, and 7 to 9 mm for a large brush pen. Bigger guidelines are easier while you learn the strokes."),
 ("What slant is used in modern calligraphy?", "Most modern brush and pointed-pen styles slant at about 55 degrees from the baseline. Copperplate is usually written at about 55 degrees too. For upright lettering set the angle to 90."),
 ("Are these calligraphy practice sheets free?", "Yes. Make as many as you like, print them on US Letter or A4, or save them as an SVG image for an iPad."),
 ("How do I stop my brush pen fraying?", "Use smooth paper such as laser or marker paper, hold the pen at a low angle and don't scrub back and forth. Rough copy paper wears felt tips quickly."),
]
page("calligraphy-practice-sheets.html", "Free Calligraphy Practice Sheets (Printable) | Purl & Paper",
     "Make free printable calligraphy practice sheets: set the x-height, slant and spacing for your brush pen or pointed pen, print on Letter or A4, or save for iPad.",
     cal, cal_faq, "Calligraphy practice sheets", app_name="Calligraphy practice sheet generator")

dot = top("Printable dot grid paper (and graph and lined)", "The bullet journal standard. Choose dot grid, square grid or lines, any spacing, US Letter or A4, then print or save it.", "Dot grid paper") + PREV_CSS + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> bullet journals use <strong>5 mm dot grid</strong> almost everywhere: it's the spacing in the popular journals and fits one line of handwriting in each row. Choose <strong>4 mm</strong> for small writing or more boxes per page, <strong>6 to 7 mm</strong> for large handwriting or children.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="ps-type">Paper type</label><select id="ps-type"><option value="dot">Dot grid</option><option value="grid">Square grid (graph)</option><option value="lined">Lined</option></select></div>
<div class="row2"><div class="field"><label for="ps-sp">Spacing (mm)</label><input type="number" id="ps-sp" value="5" min="3" max="15" step="0.5"></div>
<div class="field"><label for="ps-paper">Paper</label><select id="ps-paper"><option value="letter">US Letter</option><option value="a4">A4</option></select></div></div>
<div class="btns"><button type="button" class="btn" onclick="PPprint()">Print sheet</button> <button type="button" class="btn" onclick="PPdl('dot-grid-paper')">Save as image (SVG)</button></div>
<p class="note">Printing tip: choose "Actual size" (not "Fit to page") so the spacing prints exactly.</p>
</div><div class="result"><h2>Preview</h2><div id="ps-prev"></div></div></div></section>
{SHEET_JS}<script>(function(){{["ps-type","ps-sp","ps-paper"].forEach(function(i){{document.getElementById(i).addEventListener("input",function(){{PPsheet("dot")}})}});PPsheet("dot")}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>Bullet journal spreads to start with</h2>
<ul><li><strong>Future log:</strong> six months on one spread, two or three boxes per page.</li>
<li><strong>Monthly log:</strong> dates down the left, events beside them, a task list opposite.</li>
<li><strong>Weekly spread:</strong> seven boxes plus a to-do column. With 5 mm dots a Letter page is about 40 squares across, so each day gets roughly 10 by 12 squares.</li>
<li><strong>Habit tracker:</strong> one row per habit, one column per day. A full month needs 31 columns, so turn the page sideways or use 4 mm spacing.</li>
<li><strong>Trackers for makers:</strong> a yarn or project log, a pattern wishlist, a craft fair plan.</li></ul>
<h2>Dot grid vs graph paper vs lined</h2>
<p>Dot grid gives you the structure of graph paper without the lines showing through your drawings, which is why bullet journalers love it. Graph paper is better for charts, knitting and cross stitch planning. Lined is best for long writing.</p>
<h2>Making a printable journal</h2>
<p>Print double-sided, fold the sheets in half and stitch them into a signature. Our <a href="{href("junk-journal-signature-calculator.html")}">signature calculator</a> works out how many sheets to fold, and the <a href="{href("journal-prompts.html")}">journal prompt generator</a> gives you something to write about.</p>
<p>Lettering your headers? Print <a href="{href("calligraphy-practice-sheets.html")}">calligraphy practice sheets</a> first.</p>
<p>Need the dates too? Print a free <a href="{href("2027-calendar-printable.html")}">2027 calendar</a>, a whole year or a page a month. Setting goals? Fill in the free <a href="{href("2027-goal-planner-printable.html")}">2027 goal planner</a>.</p>
</div></div></section>{more_crafts("dot-grid-paper.html")}'''
dot_faq = [
 ("What size dot grid is best for a bullet journal?", "5 mm is the standard and suits most handwriting. 4 mm fits more on a page; 6 to 7 mm suits large writing."),
 ("How do I print dot grid paper at the right size?", "Print at Actual size or 100%, not Fit to page, so the spacing stays exact."),
 ("Is this dot grid paper free?", "Yes. Print as many sheets as you like on US Letter or A4, or save them as an SVG image."),
]
page("dot-grid-paper.html", "Free Printable Dot Grid Paper (5 mm, A4 + Letter) | Purl & Paper",
     "Free printable dot grid paper for bullet journals, plus graph and lined paper: choose 4, 5 or 6 mm spacing, US Letter or A4, then print or save as an image.",
     dot, dot_faq, "Dot grid paper", app_name="Dot grid paper generator")

# ---- Diamond painting ----
DP_ROWS = [(20, 30), (25, 30), (30, 30), (30, 40), (40, 40), (40, 50), (50, 60), (60, 80)]
def dp_n(w, h, s): return int(w * 10 // s) * int(h * 10 // s)
dp = top("Diamond painting calculator", "How many drills fit your canvas, round or square, how many hours it will take, and how big to make a custom kit.", "Diamond painting calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> a full-drill <strong>30 × 40 cm</strong> canvas holds about <strong>{dp_n(30,40,2.5):,} square drills</strong> (2.5 mm) or <strong>{dp_n(30,40,2.8):,} round drills</strong> (2.8 mm). Square drills sit edge to edge, 4 per cm; round drills are slightly bigger, about 3.6 per cm.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="dp-w">Canvas width</label><input type="number" id="dp-w" value="30" min="5" step="1"></div>
<div class="field"><label for="dp-h">Canvas height</label><input type="number" id="dp-h" value="40" min="5" step="1"></div></div>
<div class="row2"><div class="field"><label for="dp-u">Units</label><select id="dp-u"><option value="cm">cm</option><option value="in">inches</option></select></div>
<div class="field"><label for="dp-d">Drills</label><select id="dp-d"><option value="2.5">Square (2.5 mm)</option><option value="2.8">Round (2.8 mm)</option></select></div></div>
<div class="row2"><div class="field"><label for="dp-c">Coverage</label><select id="dp-c"><option value="1">Full drill</option><option value="0.6">Partial drill (about 60%)</option></select></div>
<div class="field"><label for="dp-r">Your pace (drills per hour)</label><input type="number" id="dp-r" value="800" min="100" step="50"></div></div>
</div><div class="result" aria-live="polite" id="dp-out"></div></div></section>
<script>(function(){{function v(i){{return parseFloat(document.getElementById(i).value)||0}}function run(){{var k=document.getElementById("dp-u").value=="in"?25.4:10,s=v("dp-d"),a=Math.floor(v("dp-w")*k/s),d=Math.floor(v("dp-h")*k/s),n=Math.round(a*d*v("dp-c")),h=n/Math.max(1,v("dp-r"));
document.getElementById("dp-out").innerHTML="<h2>"+n.toLocaleString()+" drills</h2><p>"+a+" across × "+d+" down"+(v("dp-c")<1?", about 60% covered":"")+".</p><p>At "+v("dp-r")+" drills an hour that's about <strong>"+Math.round(h)+" hours</strong>: "+Math.ceil(h/1)+" one-hour sessions, or about "+Math.ceil(h/7)+" weeks at an hour a day.</p><p class=\\"muted\\">Kits usually include spare drills, so keep the extras for repairs.</p>"}}
["dp-w","dp-h","dp-u","dp-d","dp-c","dp-r"].forEach(function(i){{document.getElementById(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>Diamond painting size chart: drills per canvas</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Canvas (cm)</th><th scope="col">Inches (approx.)</th><th scope="col">Square drills (2.5 mm)</th><th scope="col">Round drills (2.8 mm)</th></tr></thead><tbody>
{"".join(f"<tr><td>{w} × {h}</td><td>{round(w/2.54)} × {round(h/2.54)}</td><td>{dp_n(w,h,2.5):,}</td><td>{dp_n(w,h,2.8):,}</td></tr>" for w, h in DP_ROWS)}
</tbody></table></div>
<p class="note">Full drill counts, worked out from the drill size (canvas ÷ drill size, across and down). Real kits vary a little because the printed area is often slightly smaller than the canvas.</p>
<h2>Round or square drills?</h2>
<p><strong>Round drills</strong> (2.8 mm) don't need lining up, so they're quicker and easier for beginners and give more sparkle, with small gaps between them. <strong>Square drills</strong> (2.5 mm) click together edge to edge for a smoother, more detailed picture, but they take longer because each one has to sit straight.</p>
<h2>How long does a diamond painting take?</h2>
<p>It depends almost entirely on your pace. A beginner might place a few hundred drills an hour; an experienced painter with a multi-placer can manage well over a thousand. Time yourself for 15 minutes, multiply by four and put that in the calculator. A 30 × 40 cm full drill is a few weeks of evenings for most people.</p>
<h2>Beginner tips</h2>
<ul><li>Peel back only a strip of the film at a time so the glue stays sticky.</li>
<li>Work one colour at a time, or in small blocks, checking the symbol on the canvas against the legend.</li>
<li>Roll the drills into a tray and give it a gentle shake so they land facet side up.</li>
<li>When you finish, press the whole canvas flat with a rolling pin or a heavy book under a cloth, then seal it if you want to frame it.</li></ul>
<p>Selling finished pieces or custom kits? Work out what Etsy takes with the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>.</p>
</div></div></section>{more_crafts("diamond-painting-calculator.html")}'''
dp_faq = [
 ("How many drills are in a 30x40 diamond painting?", f"About {dp_n(30,40,2.5):,} square drills (2.5 mm) or {dp_n(30,40,2.8):,} round drills (2.8 mm) for a full drill canvas."),
 ("What size are diamond painting drills?", "Square drills are usually 2.5 mm and round drills 2.8 mm. Some brands differ slightly."),
 ("Are round or square drills better for beginners?", "Round drills are easier because they don't need lining up. Square drills give a sharper, more detailed picture but take longer."),
 ("How long does it take to finish a diamond painting?", "Divide the number of drills by how many you place in an hour. At 800 an hour a 30 x 40 cm square-drill canvas takes about 24 hours."),
]
page("diamond-painting-calculator.html", "Diamond Painting Calculator: How Many Drills? | Purl & Paper",
     "Free diamond painting calculator: how many round or square drills fit any canvas size, how many hours it will take, and a drills-per-canvas size chart.",
     dp, dp_faq, "Diamond painting calculator", app_name="Diamond painting drill calculator")

# ---- Cross stitch ----
XS_SK = {11: 1400, 14: 1750, 16: 1950, 18: 2250, 22: 2750}   # full crosses per 8 m DMC skein, 2 strands (lordlibidan.com experiment, average stitching)
def xs_in(st, ct): return st / ct
XS_LOOP_SVG = ('<svg viewBox="0 0 320 120" role="img" aria-label="Loop start: one strand folded in half, cut ends in the needle, needle passes through the loop at the back" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:420px;height:auto">'
  '<rect width="320" height="120" rx="10" fill="#f3ede2"/>' + "".join(f'<rect x="{x}" y="{y}" width="12" height="12" fill="none" stroke="#d6cbb6"/>' for x in range(170, 306, 14) for y in range(20, 104, 14)) +
  '<path d="M20 60 C 60 30, 100 30, 130 60" fill="none" stroke="#b8326a" stroke-width="3"/><path d="M20 66 C 60 96, 100 96, 130 66" fill="none" stroke="#e59ab9" stroke-width="3"/>'
  '<ellipse cx="18" cy="63" rx="8" ry="6" fill="none" stroke="#b8326a" stroke-width="3"/><line x1="128" y1="63" x2="160" y2="63" stroke="#8a8a8a" stroke-width="3"/>'
  '<text x="18" y="100" font-size="11" text-anchor="middle" fill="#1f2a44">loop</text><text x="140" y="44" font-size="11" text-anchor="middle" fill="#1f2a44">cut ends</text>'
  '<line x1="198" y1="76" x2="210" y2="64" stroke="#b8326a" stroke-width="4" stroke-linecap="round"/>'
  '<path d="M210 64 C 230 92, 190 104, 184 86" fill="none" stroke="#1f2a44" stroke-width="1.6" stroke-dasharray="3 3"/><ellipse cx="190" cy="84" rx="7" ry="4" fill="none" stroke="#e59ab9" stroke-width="2.4"/>'
  '<text x="238" y="114" font-size="10.5" text-anchor="middle" fill="#1f2a44">through the loop, at the back</text></svg>')
xs = top("Cross stitch calculator: size, fabric and floss", "Enter your pattern's stitch count. See the finished size on any Aida or evenweave, how much fabric to cut, and roughly how many skeins to buy.", "Cross stitch calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> divide the stitches by the fabric count. <strong>100 × 100 stitches on 14-count Aida is {xs_in(100,14):.1f} × {xs_in(100,14):.1f} in</strong> ({xs_in(100,14)*2.54:.1f} cm). Add <strong>3 in (7.5 cm) on every side</strong> for framing, so cut {xs_in(100,14)+6:.1f} × {xs_in(100,14)+6:.1f} in. On 28-count evenweave stitched over two, the size is the same as 14-count.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="xs-w">Stitches wide</label><input type="number" id="xs-w" value="100" min="1"></div>
<div class="field"><label for="xs-h">Stitches high</label><input type="number" id="xs-h" value="100" min="1"></div></div>
<div class="row2"><div class="field"><label for="xs-c">Fabric</label><select id="xs-c"><option value="11">11-count Aida</option><option value="14" selected>14-count Aida</option><option value="16">16-count Aida</option><option value="18">18-count Aida</option><option value="14o2">28-count evenweave, over 2</option><option value="16o2">32-count linen, over 2</option><option value="22">22-count Hardanger</option></select></div>
<div class="field"><label for="xs-m">Margin each side (in)</label><input type="number" id="xs-m" value="3" min="0" step="0.5"></div></div>
<div class="row2"><div class="field"><label for="xs-p">Stitched area (%)</label><input type="number" id="xs-p" value="100" min="1" max="100"></div>
<div class="field"><label for="xs-s">Strands</label><select id="xs-s"><option value="2">2 strands</option><option value="3">3 strands</option><option value="1">1 strand</option></select></div></div>
<div class="field"><label for="xs-n">Number of colours</label><input type="number" id="xs-n" value="12" min="1"></div>
</div><div class="result" aria-live="polite" id="xs-out"></div></div></section>
<script>(function(){{var SK={json.dumps(XS_SK)};function v(i){{return parseFloat(document.getElementById(i).value)||0}}
function run(){{var c=document.getElementById("xs-c").value,ct=parseInt(c),W=v("xs-w"),H=v("xs-h"),M=v("xs-m"),w=W/ct,h=H/ct,st=Math.round(W*H*v("xs-p")/100),s=+document.getElementById("xs-s").value,per=(SK[ct]||1750)*(2/s),sk=st/per,n=Math.max(1,v("xs-n"));
document.getElementById("xs-out").innerHTML="<h2>"+w.toFixed(1)+" × "+h.toFixed(1)+" in</h2><p>("+(w*2.54).toFixed(1)+" × "+(h*2.54).toFixed(1)+" cm) finished design.</p><p><strong>Cut your fabric "+(w+2*M).toFixed(1)+" × "+(h+2*M).toFixed(1)+" in</strong> ("+((w+2*M)*2.54).toFixed(0)+" × "+((h+2*M)*2.54).toFixed(0)+" cm) with "+M+" in on every side.</p><p>About <strong>"+st.toLocaleString()+" stitches</strong>, roughly <strong>"+sk.toFixed(1)+" skeins</strong> of floss in total. With "+n+" colours, buy at least 1 skein of each, and "+Math.ceil(sk/n*1.2)+" of your main colours.</p><p class=\\"muted\\">Floss is an estimate from about "+Math.round(per).toLocaleString()+" full crosses per standard 8 m skein at this count. Backstitch and fractional stitches add more. The pattern's key is always the best guide.</p>"}}
["xs-w","xs-h","xs-c","xs-m","xs-p","xs-s","xs-n"].forEach(function(i){{document.getElementById(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>Cross stitch size chart</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Stitches</th><th scope="col">11-count</th><th scope="col">14-count</th><th scope="col">16-count</th><th scope="col">18-count</th></tr></thead><tbody>
{"".join(f"<tr><td>{n}</td>" + "".join(f"<td>{n/c:.1f} in</td>" for c in (11, 14, 16, 18)) + "</tr>" for n in (50, 80, 100, 120, 150, 200, 250, 300))}
</tbody></table></div>
<h2>What does fabric count mean?</h2>
<p>The count is how many stitches fit in one inch. 14-count Aida has 14 squares per inch, so it's the usual beginner's fabric: big enough to see the holes, small enough for detail. Higher counts make a smaller, finer picture from the same pattern. Evenweave and linen are counted by threads, and you usually stitch over two threads, so 28-count over two gives the same size as 14-count.</p>
<h2>How many strands of floss?</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Fabric</th><th scope="col">Cross stitch</th><th scope="col">Backstitch</th></tr></thead><tbody>
<tr><td>11-count Aida</td><td>3 strands</td><td>1 or 2</td></tr><tr><td>14-count Aida</td><td>2 (or 3 for full coverage)</td><td>1</td></tr><tr><td>16-count Aida</td><td>2</td><td>1</td></tr><tr><td>18-count Aida</td><td>1 or 2</td><td>1</td></tr><tr><td>28-count evenweave over 2</td><td>2</td><td>1</td></tr></tbody></table></div>
<p class="note">Common starting points used by most stitching guides. Your pattern's own instructions come first.</p>
<h2>How much fabric to allow</h2>
<p>Allow about 3 in (7.5 cm) on every side if you'll frame the piece, so there's room to stretch it and for the mat. For a hoop display, 2 in is usually enough; allow the hoop size plus about 2 in. Small finishes such as ornaments and cards need only 1 to 1.5 in.</p>
<h2>How to start cross stitch without a knot (the loop method)</h2>
<p>Knots make lumps under a framed piece and can pull through Aida. When you stitch with an even number of strands, the loop start is the neatest way in:</p>
<div class="xs-loop">{XS_LOOP_SVG}</div>
<ol><li>Pull <strong>one</strong> strand from the floss, about twice your usual length, and fold it in half.</li>
<li>Thread the two cut ends through the needle, so the fold hangs as a loop. Now you're stitching with 2 strands.</li>
<li>Come up from the back at the bottom-left of your first stitch. Stop before the loop reaches the fabric.</li>
<li>Go down at the top-right to make the first half stitch, then pass the needle through the loop at the back and pull gently. The thread is locked, with no knot.</li></ol>
<p>For 1 or 3 strands, use a <strong>waste knot</strong> instead: knot the end, go down from the front about 2 in (5 cm) along the row you're about to stitch, and work over the tail at the back; snip the knot when the tail is covered. To finish any thread, slide the needle under 3 or 4 stitches at the back and trim close. More hand stitches, with diagrams, are in <a href="{href("embroidery-stitches.html")}">embroidery stitches for beginners</a>.</p>
<p>Planning a big piece? Chart and count it on <a href="{href("dot-grid-paper.html")}">printable graph paper</a>. Quilting too? Try the <a href="{href("quilt-size-calculator.html")}">quilt size calculator</a>.</p>
<p>First time? Follow <a href="{href("how-to-cross-stitch.html")}">how to cross stitch for beginners</a>: the stitch in five drawn steps, reading a chart, and the right needle and strands.</p></div></div></section>{more_crafts("cross-stitch-calculator.html")}'''
xs_faq = [
 ("How do I work out the size of a cross stitch?", "Divide the number of stitches by the fabric count. 140 stitches on 14-count Aida is 10 inches."),
 ("How much fabric do I need for cross stitch?", "The design size plus 3 inches on every side for framing, or about 2 inches for a hoop."),
 ("How many stitches does one skein of floss make?", "Roughly 1,700 to 1,800 full cross stitches on 14-count Aida with 2 strands, from one standard 8 m skein. Finer fabric makes more stitches per skein."),
 ("How do I start cross stitch without a knot?", "Use the loop method: fold one strand in half, thread the cut ends, come up for your first half stitch, go down, and pass the needle through the loop at the back. For an odd number of strands, use a waste knot on the front that your stitches cover."),
 ("Is 28-count evenweave the same as 14-count Aida?", "When you stitch over two threads, yes: the finished size is the same."),
]
page("cross-stitch-calculator.html", "Cross Stitch Calculator: Size, Fabric and Floss | Purl & Paper",
     "Free cross stitch calculator: finished size on any Aida or evenweave count, how much fabric to cut, skeins of floss to buy, plus a size chart and strands guide.",
     xs, xs_faq, "Cross stitch calculator", app_name="Cross stitch size and floss calculator")

# ---- Quilt size ----
QB = [("crib", "Crib", 28, 52), ("twin", "Twin", 38, 75), ("twinxl", "Twin XL", 38, 80), ("full", "Full / double", 54, 75), ("queen", "Queen", 60, 80), ("king", "King", 76, 80), ("calking", "California king", 72, 84)]
def q_sz(w, l, drop, tuck): return (w + 2 * drop, l + drop + tuck)
qs = top("Quilt size calculator (with backing and binding)", "Pick the bed and how far you want the quilt to hang. Get the finished size, plus how much backing and binding fabric to buy.", "Quilt size calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> quilt size = mattress + the drop on both sides (and at the foot) + about 10 in to tuck under pillows. With a 12 in drop, a <strong>queen quilt is about {q_sz(60,80,12,10)[0]} × {q_sz(60,80,12,10)[1]} in</strong>, a <strong>twin {q_sz(38,75,12,10)[0]} × {q_sz(38,75,12,10)[1]} in</strong> and a <strong>king {q_sz(76,80,12,10)[0]} × {q_sz(76,80,12,10)[1]} in</strong>. A sofa throw is usually about 50 × 65 in.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="qs-b">Bed</label><select id="qs-b">{"".join(f'<option value="{w},{l}"{" selected" if k=="queen" else ""}>{n} ({w} × {l} in mattress)</option>' for k, n, w, l in QB)}<option value="50,65,t">Throw / sofa quilt</option></select></div>
<div class="row2"><div class="field"><label for="qs-d">Drop each side (in)</label><input type="number" id="qs-d" value="12" min="0" step="1"></div>
<div class="field"><label for="qs-t">Pillow tuck (in)</label><input type="number" id="qs-t" value="10" min="0" step="1"></div></div>
<div class="row2"><div class="field"><label for="qs-fw">Backing fabric width (in)</label><select id="qs-fw"><option value="40">42–44 in quilting cotton</option><option value="104">108 in wide backing</option></select></div>
<div class="field"><label for="qs-bw">Binding strip width (in)</label><input type="number" id="qs-bw" value="2.5" min="1.5" step="0.25"></div></div>
</div><div class="result" aria-live="polite" id="qs-out"></div></div></section>
<script>(function(){{function v(i){{return parseFloat(document.getElementById(i).value)||0}}function yd(x){{return Math.ceil(x/36*8)/8}}
function run(){{var b=document.getElementById("qs-b").value.split(","),t=b[2]=="t",W=t?+b[0]:+b[0]+2*v("qs-d"),L=t?+b[1]:+b[1]+v("qs-d")+v("qs-t"),fw=+document.getElementById("qs-fw").value;
var bw=W+8,bl=L+8,pan,len;if(fw>100){{pan=1;len=Math.min(bw,bl)>fw?Math.max(bw,bl)*2:Math.min(bw,bl);}}else{{var a=Math.ceil(bw/fw),c=Math.ceil(bl/fw);if(a*bl<=c*bw){{pan=a;len=pan*bl}}else{{pan=c;len=pan*bw}}}}
var per=2*(W+L)+12,strips=Math.ceil(per/40);
document.getElementById("qs-out").innerHTML="<h2>"+W+" × "+L+" in quilt</h2><p>("+Math.round(W*2.54)+" × "+Math.round(L*2.54)+" cm) finished size.</p><p><strong>Backing:</strong> "+yd(len)+" yd"+(fw>100?" of 108 in wide backing":" of 42–44 in fabric, as "+pan+" panels sewn together")+". The backing is cut "+bw+" × "+bl+" in, 4 in bigger on every side for quilting.</p><p><strong>Binding:</strong> "+strips+" strips of "+v("qs-bw")+" in, about "+yd(strips*v("qs-bw"))+" yd of fabric, for "+per+" in of binding.</p><p><strong>Batting:</strong> at least "+bw+" × "+bl+" in.</p>"}}
["qs-b","qs-d","qs-t","qs-fw","qs-bw"].forEach(function(i){{document.getElementById(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>Quilt size chart</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Bed</th><th scope="col">Mattress</th><th scope="col">Coverlet (8 in drop)</th><th scope="col">Standard (12 in drop + tuck)</th></tr></thead><tbody>
{"".join(f"<tr><td>{n}</td><td>{w} × {l} in</td><td>{q_sz(w,l,8,0)[0]} × {q_sz(w,l,8,0)[1]} in</td><td>{q_sz(w,l,12,10)[0]} × {q_sz(w,l,12,10)[1]} in</td></tr>" for k, n, w, l in QB)}
<tr><td>Throw</td><td>n/a</td><td colspan="2">About 50 × 65 in (lap quilts 36 × 48 to 50 × 60 in)</td></tr></tbody></table></div>
<p class="note">Standard US mattress sizes. Measure your own mattress, especially pillow-tops and deep mattresses, which need more drop.</p>
<p>Making the top from a fat quarter bundle? The <a href="{href("fat-quarter-calculator.html")}">fat quarter calculator</a> counts the squares per fat quarter and how many you need. New to the ¼ in seam? See the <a href="{href("sewing-seam-allowance.html")}">seam allowance guide</a>. Sewing something else? The <a href="{href("fabric-yardage-calculator.html")}">fabric yardage calculator</a> covers cushions, bags and more.</p>
<h2>How to measure for a quilt</h2>
<p>Measure the top of the mattress, then the drop: from the top edge down to where you want the quilt to stop. About 8 in just covers the mattress (a coverlet), 12 in or more hides the box spring, and a bedspread reaches the floor, usually 20 in or more. Add about 10 in at the head if the quilt tucks under the pillows.</p>
<h2>Backing and batting</h2>
<p>Cut both about 4 in bigger than the quilt top on every side (8 in in total), because quilting draws the layers in and longarm quilters need room to clamp. Ordinary quilting cotton is about 42 in wide with around 40 in usable, so most bed quilts need two or three panels seamed together; wide backing (108 in) avoids the seams.</p>
<h2>Binding</h2>
<p>Add up the four sides and about 12 in for joining and corners. Most quilters cut 2.25 to 2.5 in strips across the fabric width (about 40 in usable per strip) and fold them in half for a double-fold binding.</p>
<p>Prefer yarn? See the <a href="{href("blanket-size-calculator.html")}">knit and crochet blanket size calculator</a>. Stitching a label? Plan it with the <a href="{href("cross-stitch-calculator.html")}">cross stitch calculator</a>.</p>
</div></div></section>{more_crafts("quilt-size-calculator.html")}'''
qs_faq = [
 ("What size is a queen quilt?", f"About {q_sz(60,80,12,10)[0]} × {q_sz(60,80,12,10)[1]} in with a 12 in drop and a pillow tuck, or {q_sz(60,80,8,0)[0]} × {q_sz(60,80,8,0)[1]} in as a coverlet. A queen mattress is 60 × 80 in."),
 ("How do I calculate quilt size?", "Width = mattress width + 2 × drop. Length = mattress length + drop at the foot + about 10 in for a pillow tuck."),
 ("How much bigger should the backing be than the quilt top?", "About 4 in on every side, 8 in bigger in total, for the quilting to draw in and for longarm clamps."),
 ("How much binding do I need for a quilt?", "The perimeter plus about 12 in. Divide by 40 for the number of strips cut across 42 in fabric."),
 ("What size is a throw quilt?", "Usually around 50 × 65 in, though anything from about 50 × 60 to 60 × 70 in is common."),
]
page("quilt-size-calculator.html", "Quilt Size Calculator + Chart (Twin, Queen, King) | Purl & Paper",
     "Free quilt size calculator and chart: finished quilt size for crib, twin, full, queen and king beds, plus how much backing, batting and binding fabric to buy.",
     qs, qs_faq, "Quilt size calculator", app_name="Quilt size and yardage calculator")

# ---- Candle making ----
CW = [("soy", "Soy wax", 0.86), ("coco", "Coconut / coconut-soy blend", 0.89), ("para", "Paraffin", 0.92), ("bees", "Beeswax", 0.96)]
cm = top("Candle wax and fragrance calculator", "How much wax and fragrance oil for any jar and any batch, and what each candle costs to make.", "Candle wax calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> weigh the water your jar holds and multiply by <strong>0.86 for soy wax</strong>. An <strong>8 oz jar takes about 6.9 oz of soy wax</strong> in total. At a <strong>6 to 10% fragrance load</strong> (check your wax's maximum), that's 6.3 oz wax + 0.55 oz fragrance at 8%.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="cm-v">Water the jar holds</label><input type="number" id="cm-v" value="8" min="0.5" step="0.5"></div>
<div class="field"><label for="cm-u">Units</label><select id="cm-u"><option value="oz">oz / fl oz</option><option value="g">grams / ml</option></select></div></div>
<div class="row2"><div class="field"><label for="cm-w">Wax</label><select id="cm-w">{"".join(f'<option value="{d}">{n} ({d})</option>' for k, n, d in CW)}</select></div>
<div class="field"><label for="cm-f">Fragrance load (%)</label><input type="number" id="cm-f" value="8" min="0" max="15" step="0.5"></div></div>
<div class="row2"><div class="field"><label for="cm-n">Number of candles</label><input type="number" id="cm-n" value="12" min="1"></div>
<div class="field"><label for="cm-fill">Fill (% of the water line you weighed)</label><input type="number" id="cm-fill" value="100" min="50" max="100"></div></div>
<div class="row2"><div class="field"><label for="cm-pw">Wax price per lb / kg</label><input type="number" id="cm-pw" value="4" min="0" step="0.1"></div>
<div class="field"><label for="cm-pf">Fragrance price per oz / 100 g</label><input type="number" id="cm-pf" value="2.5" min="0" step="0.1"></div></div>
<div class="field"><label for="cm-px">Jar + wick + label, each</label><input type="number" id="cm-px" value="1.6" min="0" step="0.05"></div>
</div><div class="result" aria-live="polite" id="cm-out"></div></div></section>
<script>(function(){{function v(i){{return parseFloat(document.getElementById(i).value)||0}}
function run(){{var g=document.getElementById("cm-u").value=="g",u=g?"g":"oz",tot=v("cm-v")*v("cm-w")*v("cm-fill")/100,f=v("cm-f")/100,fo=tot*f,wx=tot-fo,n=v("cm-n"),W=wx*n,F=fo*n;
var cw=g?W/1000*v("cm-pw"):W/16*v("cm-pw"),cf=g?F/100*v("cm-pf"):F*v("cm-pf"),each=(cw+cf)/n+v("cm-px");function r(x){{return g?Math.round(x):Math.round(x*100)/100}}
document.getElementById("cm-out").innerHTML="<h2>Per candle: "+r(wx)+" "+u+" wax + "+r(fo)+" "+u+" fragrance</h2><p>("+r(tot)+" "+u+" in total, "+v("cm-f")+"% fragrance by weight.)</p><p><strong>For "+n+" candles:</strong> "+r(W)+" "+u+" of wax"+(g?" ("+(W/1000).toFixed(2)+" kg)":" ("+(W/16).toFixed(2)+" lb)")+" and "+r(F)+" "+u+" of fragrance oil.</p><p><strong>Cost to make:</strong> about "+each.toFixed(2)+" per candle. Many makers price at 3 to 4 times their cost for retail.</p>"}}
["cm-v","cm-u","cm-w","cm-f","cm-n","cm-fill","cm-pw","cm-pf","cm-px"].forEach(function(i){{document.getElementById(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>Wax per jar size (soy wax)</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Jar (water it holds)</th><th scope="col">Total fill</th><th scope="col">Wax at 8%</th><th scope="col">Fragrance at 8%</th></tr></thead><tbody>
{"".join(f"<tr><td>{j} oz</td><td>{j*0.86:.1f} oz</td><td>{j*0.86*0.92:.1f} oz</td><td>{j*0.86*0.08:.2f} oz</td></tr>" for j in (4, 6, 8, 10, 12, 16))}
</tbody></table></div>
<p class="note">Soy wax weighs about 0.86 times as much as the same volume of water, the figure most candle suppliers use. Paraffin is about 0.92 and beeswax about 0.96.</p>
<h2>How to measure a jar</h2>
<p>Put the empty jar on a kitchen scale, zero it, then fill it with water to where you want the wax to stop (usually about half an inch below the rim). That weight is the number to enter. It's more accurate than the volume printed on the jar.</p>
<h2>What fragrance load should I use?</h2>
<p>Most container waxes are made for a fragrance load of about 6 to 10%, and many list a maximum of 10 or 12%. More oil doesn't always mean a stronger throw and can make the candle sweat or burn badly, so start at the wax maker's recommendation and test-burn. The calculator works the percentage out of the total weight, so the wax and the oil together fill the jar.</p>
<h2>Safety</h2>
<ul><li>Melt wax in a double boiler or a pouring pot over water, never directly on a burner, and never leave it.</li>
<li>Check the fragrance oil's flash point and the wax maker's temperatures for adding fragrance and pouring.</li>
<li>Choose the wick from the wick maker's chart for your jar diameter and wax, then test-burn for several hours before selling.</li>
<li>Selling? Add warning labels as required where you sell; in the US many makers follow ASTM candle labelling guidance, and in the UK and EU, CLP labelling applies to fragrance.</li></ul>
<p>Selling your candles online? See what Etsy takes with the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>. Making resin pieces too? Try the <a href="{href("resin-calculator.html")}">resin calculator</a>.</p>
</div></div></section>{more_crafts("candle-making-calculator.html")}'''
cm_faq = [
 ("How much wax do I need for an 8 oz candle?", "About 6.9 oz of soy wax in total for a jar that holds 8 oz of water. At an 8% fragrance load that's about 6.3 oz of wax and 0.55 oz of fragrance oil."),
 ("How do I calculate candle wax?", "Weigh the water your jar holds and multiply by the wax density: 0.86 for soy, about 0.92 for paraffin."),
 ("How much fragrance oil per pound of wax?", "At 6% about 1 oz per pound, at 10% about 1.6 oz. Check your wax's maximum fragrance load."),
 ("What is fragrance load?", "The fragrance oil as a percentage of the candle's weight. Most container waxes suit 6 to 10%."),
]
page("candle-making-calculator.html", "Candle Wax Calculator: Wax and Fragrance per Jar | Purl & Paper",
     "Free candle making calculator: how much soy, coconut or paraffin wax and fragrance oil for any jar size and batch, fragrance load, and cost per candle.",
     cm, cm_faq, "Candle wax calculator", app_name="Candle wax and fragrance calculator")

# ---- Resin ----
rs = top("Epoxy resin calculator", "How much resin and hardener to mix for a mould, tray, coaster set, tumbler or river table, by volume or by weight.", "Resin calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> volume = length × width × depth. In centimetres that's millilitres: a <strong>30 × 20 cm tray poured 0.5 cm deep needs 300 ml</strong> of mixed resin. Add about 10% for waste, then split it by your kit's ratio: for a <strong>1:1</strong> kit that's 165 ml resin + 165 ml hardener; for <strong>2:1</strong>, 220 ml + 110 ml.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="rs-sh">Shape</label><select id="rs-sh"><option value="r">Rectangle</option><option value="c">Circle (coaster, round mould)</option></select></div>
<div class="field"><label for="rs-u">Units</label><select id="rs-u"><option value="cm">cm</option><option value="in">inches</option></select></div></div>
<div class="row2"><div class="field"><label for="rs-l" id="rs-ll">Length</label><input type="number" id="rs-l" value="30" min="0" step="0.1"></div>
<div class="field" id="rs-wf"><label for="rs-w">Width</label><input type="number" id="rs-w" value="20" min="0" step="0.1"></div></div>
<div class="row2"><div class="field"><label for="rs-d">Depth</label><input type="number" id="rs-d" value="0.5" min="0" step="0.05"></div>
<div class="field"><label for="rs-q">How many</label><input type="number" id="rs-q" value="1" min="1"></div></div>
<div class="row2"><div class="field"><label for="rs-r">Mix ratio (resin : hardener)</label><select id="rs-r"><option value="1,1">1 : 1</option><option value="2,1">2 : 1</option><option value="3,1">3 : 1</option><option value="100,45">100 : 45 (by weight)</option></select></div>
<div class="field"><label for="rs-x">Extra for waste (%)</label><input type="number" id="rs-x" value="10" min="0" max="50"></div></div>
</div><div class="result" aria-live="polite" id="rs-out"></div></div></section>
<script>(function(){{function v(i){{return parseFloat(document.getElementById(i).value)||0}}
function run(){{var c=document.getElementById("rs-sh").value=="c",k=document.getElementById("rs-u").value=="in"?2.54:1,L=v("rs-l")*k,W=v("rs-w")*k,D=v("rs-d")*k;document.getElementById("rs-wf").style.display=c?"none":"";document.getElementById("rs-ll").textContent=c?"Diameter":"Length";
var ml=(c?Math.PI*L*L/4*D:L*W*D)*v("rs-q"),tot=ml*(1+v("rs-x")/100),r=document.getElementById("rs-r").value.split(","),a=+r[0],b=+r[1],A=tot*a/(a+b),B=tot*b/(a+b),g=tot*1.1,oz=tot/29.574;
document.getElementById("rs-out").innerHTML="<h2>"+Math.round(tot)+" ml mixed resin</h2><p>("+oz.toFixed(1)+" fl oz, about "+Math.round(g)+" g). That's "+Math.round(ml)+" ml for the piece plus "+v("rs-x")+"%.</p><p><strong>Mix "+Math.round(A)+" "+(a==100?"g":"ml")+" resin + "+Math.round(B)+" "+(a==100?"g":"ml")+" hardener</strong> ("+a+":"+b+").</p>"+(D>(1.3)?"<p><strong>Check the pour depth.</strong> Most coating and art resins are poured in layers of about 3 to 6 mm; pours deeper than about 1 cm usually need a deep-pour casting resin, or several layers. Follow your product's maximum.</p>":"")+"<p class=\\"muted\\">Grams use a typical epoxy density of about 1.1 g per ml. Check your kit's data sheet, and measure by volume or weight exactly as its instructions say.</p>"}}
["rs-sh","rs-u","rs-l","rs-w","rs-d","rs-q","rs-r","rs-x"].forEach(function(i){{document.getElementById(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>How much resin for common projects</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Project</th><th scope="col">Size</th><th scope="col">Mixed resin (+10%)</th></tr></thead><tbody>
<tr><td>4 round coasters</td><td>10 cm across, 0.6 cm deep</td><td>{round(3.14159*25*0.6*4*1.1)} ml</td></tr>
<tr><td>Serving tray coat</td><td>40 × 25 cm, 0.3 cm</td><td>{round(40*25*0.3*1.1)} ml</td></tr>
<tr><td>Charcuterie board coat</td><td>45 × 20 cm, 0.2 cm</td><td>{round(45*20*0.2*1.1)} ml</td></tr>
<tr><td>Small river table</td><td>100 × 10 cm river, 4 cm deep</td><td>{round(100*10*4*1.1/1000,1)} litres (deep-pour resin)</td></tr></tbody></table></div>
<h2>Volume or weight?</h2>
<p>Use whatever your kit says. Many art resins are 1:1 by volume; many casting and deep-pour resins give the ratio by weight (for example 100:45). Getting the ratio wrong is the most common reason resin stays sticky, so measure carefully and mix for the full time on the label, scraping the sides and bottom.</p>
<h2>Resin safety</h2>
<ul><li>Work in a well-ventilated room and follow the product's safety data sheet.</li>
<li>Wear nitrile gloves and eye protection; uncured resin can cause skin sensitisation.</li>
<li>Mix only what you can pour in the working time; large batches can heat up fast.</li>
<li>Food contact: only use a resin rated food safe once fully cured, and follow its cure times.</li></ul>
<p>Selling resin art? Our resin calculator and pricing spreadsheet tracks material cost per piece, and the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a> shows what you'll keep.</p>
</div></div></section>{more_crafts("resin-calculator.html")}'''
rs_faq = [
 ("How do I calculate how much resin I need?", "Length × width × depth in centimetres gives millilitres. Add about 10% for waste, then split by your kit's mix ratio."),
 ("How much resin for 4 coasters?", f"Four 10 cm coasters 6 mm deep take about {round(3.14159*25*0.6*4*1.1)} ml of mixed resin, including 10% extra."),
 ("How deep can I pour epoxy resin?", "Coating and art resins are usually poured in layers of about 3 to 6 mm. Deeper pours need a deep-pour casting resin; follow the product's maximum depth."),
 ("How many grams is 100 ml of resin?", "About 110 g, as most epoxy resins weigh about 1.1 g per ml. Check your kit's data sheet."),
]
page("resin-calculator.html", "Resin Calculator: How Much Epoxy Resin Do I Need? | Purl & Paper",
     "Free epoxy resin calculator: how much resin and hardener to mix for moulds, coasters, trays and river tables, by volume or weight, with 1:1 and 2:1 ratios.",
     rs, rs_faq, "Resin calculator", app_name="Epoxy resin calculator")

# ---- Macrame ----
mc = top("Macrame cord calculator", "How many cords to cut, how long each one should be, and how much cord to buy for a wall hanging, plant hanger or keychain.", "Macrame cord calculator") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> cut each cord about <strong>4 times the finished length</strong>, or <strong>8 times</strong> if you fold it in half over the dowel with a lark's head knot (most wall hangings). Dense knotting such as half hitches uses more, so allow up to 5 times; add the fringe on top.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="mc-l">Finished length (without fringe)</label><input type="number" id="mc-l" value="24" min="1"></div>
<div class="field"><label for="mc-fr">Fringe length</label><input type="number" id="mc-fr" value="6" min="0"></div></div>
<div class="row2"><div class="field"><label for="mc-u">Units</label><select id="mc-u"><option value="in">inches</option><option value="cm">cm</option></select></div>
<div class="field"><label for="mc-fold">Cords</label><select id="mc-fold"><option value="2">Folded in half (lark's head)</option><option value="1">Single</option></select></div></div>
<div class="row2"><div class="field"><label for="mc-k">Knotting</label><select id="mc-k"><option value="4">Average (square knots, some open space)</option><option value="3.5">Open, lacy</option><option value="5">Dense (half hitches, solid panels)</option></select></div>
<div class="field"><label for="mc-w">Dowel width used</label><input type="number" id="mc-w" value="16" min="1"></div></div>
<div class="field"><label for="mc-cw">Cord thickness</label><select id="mc-cw"><option value="0.12">3 mm</option><option value="0.16" selected>4 mm</option><option value="0.2">5 mm</option><option value="0.24">6 mm</option></select></div>
</div><div class="result" aria-live="polite" id="mc-out"></div></div></section>
<script>(function(){{function v(i){{return parseFloat(document.getElementById(i).value)||0}}
function run(){{var cm=document.getElementById("mc-u").value=="cm",u=cm?"cm":"in",f=v("mc-fold"),k=v("mc-k"),per=(v("mc-l")*k+v("mc-fr"))*f,cw=v("mc-cw")*(cm?2.54:1),n=Math.max(1,Math.floor(v("mc-w")/(cw*(f==2?4:1.5)))),tot=per*n,yd=cm?tot/100:tot/36;
document.getElementById("mc-out").innerHTML="<h2>Cut "+n+" cords of "+Math.round(per)+" "+u+"</h2><p>That's "+n*f+" working ends across "+v("mc-w")+" "+u+" of dowel"+(f==2?", each cord folded in half":"")+".</p><p><strong>Buy at least "+(Math.ceil(yd*1.1*10)/10)+(cm?" m":" yd")+"</strong> of cord ("+Math.round(tot)+" "+u+" plus 10% spare), plus a short piece to hang it.</p><p class=\\"muted\\">The number of cords assumes the lark's head knots sit side by side, touching, on the dowel (about 4 cord widths each). Leave gaps and you'll need fewer.</p>"}}
["mc-l","mc-fr","mc-u","mc-fold","mc-k","mc-w","mc-cw"].forEach(function(i){{document.getElementById(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>Why 8 times?</h2>
<p>The usual rule is that every working strand needs about four times the finished length, because each knot takes up cord. When a cord is folded in half over the dowel, it becomes two strands, so the cord you cut must be about eight times the finished length. Projects with lots of open space need less; solid rows of half hitches need more. If you run short, you can add in a new length behind a knot.</p>
<h2>Cord lengths for common projects</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Project</th><th scope="col">Finished length</th><th scope="col">Cut each cord (folded)</th></tr></thead><tbody>
<tr><td>Keychain</td><td>4 in (10 cm)</td><td>about 36 in (90 cm)</td></tr><tr><td>Small plant hanger</td><td>30 in (75 cm)</td><td>about 20 ft (6 m), as a plant hanger is mostly long sinnets</td></tr>
<tr><td>Small wall hanging</td><td>18 in (45 cm)</td><td>about 12 ft (3.7 m)</td></tr><tr><td>Medium wall hanging</td><td>30 in (75 cm)</td><td>about 20 ft (6 m)</td></tr></tbody></table></div>
<p class="note">Rule-of-thumb lengths using 8× for folded cords. Follow your pattern if it gives lengths.</p>
<h2>Beginner knots to learn first</h2>
<p>The lark's head (to mount cords), the square knot, the spiral (a half knot repeated), the half hitch and double half hitch, and the gathering knot (to finish plant hangers). Practise each on a short piece of cord before a project. See all ten drawn step by step in <a href="{href("macrame-knots.html")}">macrame knots for beginners</a>.</p>
<p>Love fibre crafts? Try the <a href="{href("yarn-calculator.html")}">yarn calculator</a> for knitting and crochet.</p>
</div></div></section>{more_crafts("macrame-cord-calculator.html")}'''
mc_faq = [
 ("How much macrame cord do I need?", "Cut each cord about 4 times the finished length, or 8 times if it's folded in half with a lark's head knot. Add the fringe length on top."),
 ("How many cords for a macrame wall hanging?", "Divide the width of the dowel you'll cover by the cord thickness. Each folded cord mounted with a lark's head takes about 4 cord widths, so a 16 in dowel holds about 25 folded 4 mm cords (50 working ends)."),
 ("What thickness of macrame cord for beginners?", "4 to 5 mm single-strand cotton is easy to knot, undo and comb into fringe."),
]
page("macrame-cord-calculator.html", "Macrame Cord Calculator: How Much Cord Do I Need? | Purl & Paper",
     "Free macrame cord calculator: how many cords to cut, how long (the 4x and 8x rules) and how much cord to buy for wall hangings, plant hangers and keychains.",
     mc, mc_faq, "Macrame cord calculator", app_name="Macrame cord calculator")

# ---- Polymer clay (Sources: sculpey.com baking chart + FAQ; Cool Tools curing guide (Fimo 110 C 30 min); Wikipedia Kato Polyclay; Earth Guild (Cernit); Blue Bottle Tree (350 F breakdown, bake longer)) ----
PC = [("s3", "Sculpey III, Original Sculpey, Super Sculpey", 275, 130, 15, True), ("premo", "Sculpey Premo", 275, 130, 30, True), ("souffle", "Sculpey Souffle", 275, 130, 30, True),
      ("bendy", "Sculpey Bake Shop Bendy", 285, 140, 20, True), ("fimo", "Fimo Soft, Fimo Professional, Fimo Effect", 230, 110, 30, False), ("kato", "Kato Polyclay", 300, 150, 30, True), ("cernit", "Cernit", 250, 120, 30, False)]
pc_js = "{" + ",".join(f'"{k}":[{f},{c},{m},{1 if per else 0}]' for k, n, f, c, m, per in PC) + "}"
pcb = top("Polymer clay baking calculator", "Pick your clay and how thick your piece is. Get the oven temperature and how long to bake it, plus how to stop it burning or breaking.", "Polymer clay baking calculator") + f"""
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> most <strong>Sculpey</strong> clays bake at <strong>275 °F (130 °C) for 15 to 30 minutes per ¼ inch (6 mm)</strong> of thickness: 15 for Sculpey III, 30 for Premo and Souffle. <strong>Fimo</strong> bakes lower, at <strong>230 °F (110 °C) for 30 minutes</strong>. Use an oven thermometer: oven dials are often 25 °F out, and too hot scorches the clay.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="pc-b">Clay</label><select id="pc-b">{"".join(f'<option value="{k}">{n}</option>' for k, n, *_ in PC)}</select></div>
<div class="row2"><div class="field"><label for="pc-t">Thickest part</label><input type="number" id="pc-t" value="6" min="1" step="0.5"></div>
<div class="field"><label for="pc-u">Units</label><select id="pc-u"><option value="mm">mm</option><option value="in">inches</option></select></div></div>
</div><div class="result" aria-live="polite" id="pc-out"></div></div></section>
<script>(function(){{var P={pc_js};function g(i){{return document.getElementById(i)}}
function run(){{var p=P[g("pc-b").value],t=+g("pc-t").value||0,mm=g("pc-u").value=="in"?t*25.4:t,q=Math.max(1,mm/6.35),min=p[3]?Math.round(p[2]*q):Math.max(p[2],Math.round(p[2]*q));
g("pc-out").innerHTML="<h2>"+p[0]+" °F ("+p[1]+" °C)</h2><p>Bake for at least <strong>"+min+" minutes</strong> for a piece "+(mm).toFixed(1)+" mm thick.</p>"+(p[3]?"":"<p class=\\"muted\\">The pack gives 30 minutes; for pieces thicker than about 6 mm many makers add time per ¼ inch, as here.</p>")+"<p class=\\"muted\\">Preheat, check the temperature with an oven thermometer, and let it cool before you test it: clay is still soft when hot.</p>"}}
["pc-b","pc-t","pc-u"].forEach(function(i){{g(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>Polymer clay baking chart</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Clay</th><th scope="col">Temperature</th><th scope="col">Time</th></tr></thead><tbody>
{"".join(f"<tr><td>{n}</td><td>{f} °F ({c} °C)</td><td>{m} min{' per ¼ in (6 mm)' if per else ''}</td></tr>" for k, n, f, c, m, per in PC)}
</tbody></table></div>
<p class="note">From the makers' own guidance (Sculpey's baking chart; Fimo's 110 °C, 30 minutes). Kato can be cured between about 275 and 325 °F; Cernit's packs give a range of about 110 to 130 °C. Always follow the pack in your hand if it differs.</p>
<h2>How to bake polymer clay without burning it</h2>
<ul><li>Use an oven thermometer: home ovens swing above and below the dial.</li>
<li>Bake on a ceramic tile or card, and tent the piece with foil or a second tray to stop browning.</li>
<li>Pale colours and translucent clay darken first; tent them and don't go hotter than the pack says.</li>
<li>Polymer clay doesn't break down until about 350 °F (177 °C), so a correct temperature for longer is safer than a higher one.</li></ul>
<h2>Why is my baked clay brittle?</h2>
<p>Almost always underbaking: too short, or an oven running cool. Many experienced clayers bake for longer than the pack's minimum, often 45 to 60 minutes, at the correct temperature. Thin pieces of Sculpey III and Original Sculpey stay fragile even when fully baked; for jewellery and thin pieces, a stronger clay such as Premo, Souffle, Fimo or Kato is a better choice.</p>
<h2>Can I bake polymer clay in my kitchen oven?</h2>
<p>Yes, at these temperatures, as the makers say, but keep it separate from food: use dedicated tools and trays, tent or cover the piece, ventilate the kitchen, and wipe the oven afterwards. Many makers use a small toaster oven kept only for clay.</p>
<p>Selling clay earrings? Work out your prices with the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>. Making resin pieces too? Try the <a href="{href("resin-calculator.html")}">resin calculator</a>.</p>
</div></div></section>{more_crafts("polymer-clay-baking-calculator.html")}"""
pcb_faq = [("What temperature do you bake polymer clay?", "275 °F (130 °C) for most Sculpey clays, 230 °F (110 °C) for Fimo, and up to 300 °F (150 °C) for Kato. Check your pack."),
           ("How long do you bake polymer clay?", "Sculpey III: 15 minutes per ¼ inch (6 mm). Premo and Souffle: 30 minutes per ¼ inch. Fimo: 30 minutes. Longer at the correct temperature makes stronger pieces."),
           ("Can you overbake polymer clay?", "At the right temperature, extra time is usually fine. Too high a temperature is what scorches and darkens it."),
           ("Why did my polymer clay crack or break?", "Usually underbaking, or a thin piece of a brittle clay. Bake longer at the correct temperature with an oven thermometer.")]
page("polymer-clay-baking-calculator.html", "Polymer Clay Baking Temperature and Time Calculator | Purl & Paper",
     "Polymer clay baking chart and calculator: oven temperature and bake time for Sculpey, Premo, Fimo, Kato and Cernit by thickness, and how to stop burning.",
     pcb, pcb_faq, "Polymer clay baking calculator", app_name="Polymer clay baking calculator")

# ---- Half square triangles (standard quilting maths: 2-at-a-time finished + 7/8 in; 8-at-a-time (finished + 7/8) x 2; 4-at-a-time (finished + 7/8) x 1.414; unfinished = finished + 1/2) ----
def _fr(x):
    w = int(x); e8 = round((x - w) * 8)
    if e8 == 8: w, e8 = w + 1, 0
    from math import gcd
    if not e8: return f"{w} in"
    g = gcd(e8, 8); return f"{w} {e8 // g}/{8 // g} in" if w else f"{e8 // g}/{8 // g} in"
import math as _m
hst_rows = "".join(f"<tr><td>{_fr(f)}</td><td>{_fr(f + .5)}</td><td>{_fr(f + .875)}</td><td>{_fr(_m.ceil((f + .875) * 1.414 * 8) / 8)}</td><td>{_fr((f + .875) * 2)}</td></tr>" for f in (1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6))
hst = top("Half square triangle calculator", "Enter the finished size of your HSTs and how many you need. Get the size to cut your squares for the 2, 4 and 8 at a time methods, and how much fabric to buy.", "Half square triangle calculator") + f"""
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> for the classic <strong>2 at a time</strong> method, cut squares <strong>⅞ in bigger than the finished size</strong>: a 3 in finished HST starts from 3⅞ in squares. Many quilters cut 1 in bigger instead and trim to the unfinished size (finished + ½ in, so 3½ in). For <strong>8 at a time</strong>, cut squares (finished + ⅞ in) × 2: 7¾ in for 3 in HSTs.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="hs-f">Finished HST size (in)</label><input type="number" id="hs-f" value="3" min="0.5" step="0.25"></div>
<div class="field"><label for="hs-n">How many HSTs</label><input type="number" id="hs-n" value="48" min="1"></div></div>
<div class="row2"><div class="field"><label for="hs-m">Method</label><select id="hs-m"><option value="2">2 at a time (draw a diagonal, sew both sides)</option><option value="4">4 at a time (sew round the edge, cut both diagonals)</option><option value="8">8 at a time (sew both diagonals)</option></select></div>
<div class="field"><label for="hs-t">Trim allowance</label><select id="hs-t"><option value="0">Exact (no trimming)</option><option value="0.125">Add ⅛ in, then trim</option></select></div></div>
</div><div class="result" aria-live="polite" id="hs-out"></div></div></section>
<script>(function(){{function g(i){{return document.getElementById(i)}}function fr(x){{x=Math.ceil(x*8-1e-9)/8;var w=Math.floor(x),e=Math.round((x-w)*8),n=[0,"⅛","¼","⅜","½","⅝","¾","⅞"][e];return (w?w:"")+(e?n:"")+" in"}}
function run(){{var f=+g("hs-f").value||0,n=+g("hs-n").value||0,m=+g("hs-m").value,t=+g("hs-t").value,c=m==2?f+.875:m==8?(f+.875)*2:(f+.875)*1.414;c+=t;var per=m,pairs=Math.ceil(n/per),across=Math.floor(40/c),strips=Math.ceil(pairs/Math.max(1,across)),yd=Math.ceil(strips*c/36*8)/8;
g("hs-out").innerHTML="<h2>Cut squares "+fr(c)+"</h2><p>You need <strong>"+pairs+" light and "+pairs+" dark squares</strong> to make "+(pairs*per)+" HSTs ("+n+" needed).</p><p>From 42 in quilting cotton you get "+across+" squares per strip: cut <strong>"+strips+" strips "+fr(c)+" wide</strong> of each fabric, about <strong>"+yd+" yd</strong> of each.</p><p>Each HST should then measure <strong>"+fr(f+.5)+"</strong> unfinished"+(t||m!=2?", so trim to that.":".")+"</p>"+(m==4?"<p class=\\"muted\\">4 at a time leaves bias edges on the outside, so press gently and starch before cutting.</p>":"")}}
["hs-f","hs-n","hs-m","hs-t"].forEach(function(i){{g(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose">
<h2>HST cut size chart</h2>
<div class="tbl-wrap"><table class="mt"><thead><tr><th scope="col">Finished</th><th scope="col">Unfinished (trim to)</th><th scope="col">2 at a time</th><th scope="col">4 at a time</th><th scope="col">8 at a time</th></tr></thead><tbody>{hst_rows}</tbody></table></div>
<p class="note">Exact cut sizes with a ¼ in seam allowance; 4 at a time is rounded up to the next ⅛ in. Add ⅛ to ½ in if you like to trim your HSTs square.</p>
<p>Cutting your squares from fat quarters? The <a href="{href("fat-quarter-calculator.html")}">fat quarter calculator</a> shows how many fit. Why ¼ in, and how to sew it accurately: our <a href="{href("sewing-seam-allowance.html")}">seam allowance guide</a>.</p>
<h2>Which HST method should I use?</h2>
<ul><li><strong>2 at a time:</strong> the most accurate and easiest for beginners. Pair a light and a dark square, draw one diagonal, sew ¼ in either side, cut on the line, press.</li>
<li><strong>4 at a time:</strong> sew all round the edge of two squares, then cut both diagonals. Fast, but the outer edges are on the bias and stretch.</li>
<li><strong>8 at a time:</strong> draw both diagonals, sew ¼ in either side of both, then cut across, down and on both diagonals. Fastest for big quilts; best with starch and a trim.</li></ul>
<h2>Why ⅞ in?</h2>
<p>A triangle's seam takes up more fabric along its diagonal than a straight seam does. Half an inch covers the two ¼ in seam allowances; the extra ⅜ in covers the diagonal, giving ⅞ in in total.</p>
<p>Planning the whole quilt? Work out its size, backing and binding with the <a href="{href("quilt-size-calculator.html")}">quilt size calculator</a>.</p>
</div></div></section>{more_crafts("half-square-triangle-calculator.html")}"""
hst_faq = [("What size do I cut squares for half square triangles?", "For 2 at a time, the finished size plus ⅞ in. For 3 in finished HSTs, cut 3⅞ in squares. Many quilters add 1 in and trim instead."),
           ("How do I make 8 half square triangles at once?", "Cut two squares (finished + ⅞ in) × 2, draw both diagonals, sew ¼ in either side of each, then cut horizontally, vertically and on both diagonals."),
           ("What size should a 3 inch HST measure before sewing into the quilt?", "3½ in unfinished. It finishes at 3 in once it's sewn in."),
           ("Why are my half square triangles too small?", "Usually a seam wider than ¼ in, or stretching the bias when pressing. Cut a little bigger and trim to the unfinished size.")]
page("half-square-triangle-calculator.html", "Half Square Triangle Calculator: HST Cut Sizes | Purl & Paper",
     "Free half square triangle calculator: what size squares to cut for HSTs made 2, 4 or 8 at a time, how many squares and strips you need, and a cut size chart.",
     hst, hst_faq, "Half square triangle calculator", app_name="Half square triangle calculator")


# ---------------- 2027 CALENDAR PRINTABLE (DEMAND C8: "2027 calendar printable" 10k-100k, +900% YoY, peaks Dec) ----------------
# Holidays computed in the browser. US: federal holidays (5 U.S.C. 6103) with OPM's Saturday->Friday / Sunday->Monday observed rule.
# UK: England & Wales bank holidays; 2027 dates match the Privy Council proclamation of 8 July 2026 (1 Jan, 3 May, 28 Dec) plus the usual rules.
CAL_JS = r'''<script>(function(){
var MN=["January","February","March","April","May","June","July","August","September","October","November","December"],DN=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],
P={a4:[210,297],letter:[215.9,279.4]},AC={ink:"#1f2a44",berry:"#b8326a",teal:"#2a8a86",gold:"#c98a12"};
function g(i){return document.getElementById(i)}
function nth(y,m,dow,n){var d=new Date(y,m,1),off=(dow-d.getDay()+7)%7;return 1+off+(n-1)*7}
function last(y,m,dow){var L=new Date(y,m+1,0),off=(L.getDay()-dow+7)%7;return L.getDate()-off}
function easter(y){var a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),gg=Math.floor((b-f+1)/3),h=(19*a+b-d-gg+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*m+114)/31),da=((h+l-7*m+114)%31)+1;return new Date(y,mo-1,da)}
function dow(y,m,d){return new Date(y,m,d).getDay()}
window.PPhol=function(y,mode){var H={};function add(m,d,n){var k=m+"-"+d;H[k]=H[k]?H[k]+" / "+n:n}
 if(mode=="us"){var fx=[[0,1,"New Year's Day"],[5,19,"Juneteenth"],[6,4,"Independence Day"],[10,11,"Veterans Day"],[11,25,"Christmas Day"]];
  fx.forEach(function(h){add(h[0],h[1],h[2]);var w=dow(y,h[0],h[1]);if(w==6&&!(h[0]==0&&h[1]==1))add(h[0],h[1]-1,h[2]+" (obs.)");if(w==0)add(h[0],h[1]+1,h[2]+" (obs.)")});
  if(dow(y+1,0,1)==6)add(11,31,"New Year's observed");
  add(0,nth(y,0,1,3),"MLK Day");add(1,nth(y,1,1,3),"Presidents' Day");add(4,last(y,4,1),"Memorial Day");add(8,nth(y,8,1,1),"Labor Day");add(9,nth(y,9,1,2),"Columbus Day");add(10,nth(y,10,4,4),"Thanksgiving")}
 else if(mode=="uk"){var w=dow(y,0,1);add(0,w==6?3:(w==0?2:1),"New Year's Day"+(w==6||w==0?" (sub)":""));
  var E=easter(y),gf=new Date(E);gf.setDate(E.getDate()-2);var em=new Date(E);em.setDate(E.getDate()+1);add(gf.getMonth(),gf.getDate(),"Good Friday");add(em.getMonth(),em.getDate(),"Easter Monday");
  add(4,nth(y,4,1,1),"Early May bank hol");add(4,last(y,4,1),"Spring bank hol");add(7,last(y,7,1),"Summer bank hol");
  var c=dow(y,11,25);if(c==6){add(11,25,"Christmas Day");add(11,26,"Boxing Day");add(11,27,"Christmas (sub)");add(11,28,"Boxing Day (sub)")}else if(c==0){add(11,25,"Christmas Day");add(11,26,"Boxing Day");add(11,27,"Christmas (sub)")}else if(c==5){add(11,25,"Christmas Day");add(11,26,"Boxing Day");add(11,28,"Boxing Day (sub)")}else{add(11,25,"Christmas Day");add(11,26,"Boxing Day")}}
 return H};
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/'/g,"&#39;")}
function T(x,y,s,sz,col,wt,anc){return '<text x="'+x+'" y="'+y+'" font-family="Helvetica,Arial,sans-serif" font-size="'+sz+'" fill="'+col+'"'+(wt?' font-weight="'+wt+'"':'')+(anc?' text-anchor="'+anc+'"':'')+'>'+esc(s)+'</text>'}
function opts(){return{y:+g("cl-year").value,lay:g("cl-lay").value,st:g("cl-start").value=="mon"?1:0,hol:g("cl-hol").value,pp:P[g("cl-paper").value],ac:AC[g("cl-ac").value],m:+g("cl-mon").value}}
function weeks(y,m,st){var f=(dow(y,m,1)-st+7)%7,n=new Date(y,m+1,0).getDate();return Math.ceil((f+n)/7)}
function yearSvg(o){var W=o.pp[0],H=o.pp[1],mg=12,s="",HL=PPhol(o.y,o.hol),cw=(W-2*mg)/3,top=34,listH=o.hol=="none"?0:34,ch=(H-top-mg-listH)/4;
 s+=T(W/2,24,String(o.y),16,o.ac,"700","middle");
 for(var m=0;m<12;m++){var cx=mg+(m%3)*cw,cy=top+Math.floor(m/3)*ch,cel=(cw-6)/7,rh=(ch-14)/7,f=(dow(o.y,m,1)-o.st+7)%7,n=new Date(o.y,m+1,0).getDate();
  s+=T(cx+3,cy+5,MN[m],4.2,o.ac,"700");
  for(var j=0;j<7;j++)s+=T(cx+3+cel*j+cel/2,cy+11,DN[(j+o.st)%7].charAt(0),2.6,"#777","700","middle");
  for(var d=1;d<=n;d++){var p=f+d-1,r=Math.floor(p/7),c=p%7,x=cx+3+cel*c+cel/2,yy=cy+11+rh*(r+1),wk=(c+o.st)%7,h=HL[m+"-"+d];
   if(h)s+='<circle cx="'+x+'" cy="'+(yy-1.1)+'" r="2.4" fill="'+o.ac+'" opacity=".16"/>';
   s+=T(x,yy,d,3,h?o.ac:(wk==0||wk==6?"#888":"#222"),h?"700":"","middle")}}
 if(listH){var ks=Object.keys(HL).sort(function(a,b){var A=a.split("-"),B=b.split("-");return(A[0]-B[0])||(A[1]-B[1])}),y0=H-mg-listH+6,per=Math.ceil(ks.length/3);
  s+=T(mg,y0,o.hol=="us"?"US federal holidays":"UK bank holidays (England and Wales)",3,o.ac,"700");
  ks.forEach(function(k,i){var A=k.split("-");s+=T(mg+Math.floor(i/per)*cw,y0+4.5+(i%per)*3.6,MN[+A[0]].slice(0,3)+" "+A[1]+"  "+HL[k],2.6,"#333")})}
 s+=T(W-mg,H-5,"purlandpaperco.com",2.4,"#aaa","","end");
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'mm" height="'+H+'mm"><rect width="'+W+'" height="'+H+'" fill="#fff"/>'+s+'</svg>'}
function monthSvg(o,m){var W=o.pp[1],H=o.pp[0],mg=11,s="",HL=PPhol(o.y,o.hol),side=o.lay=="planner"?64:0,gw=W-2*mg-side,top=30,nw=weeks(o.y,m,o.st),gh=H-top-mg-8,cw=gw/7,rh=gh/nw,f=(dow(o.y,m,1)-o.st+7)%7,n=new Date(o.y,m+1,0).getDate();
 s+=T(mg,20,MN[m],13,o.ac,"700")+T(mg+gw,20,String(o.y),13,"#bbb","700","end");
 for(var j=0;j<7;j++){s+='<rect x="'+(mg+cw*j)+'" y="'+(top-7)+'" width="'+cw+'" height="7" fill="'+o.ac+'"/>';s+=T(mg+cw*j+cw/2,top-2.2,DN[(j+o.st)%7],3.2,"#fff","700","middle")}
 for(var r=0;r<nw;r++)for(var c=0;c<7;c++){var p=r*7+c,d=p-f+1,x=mg+cw*c,yy=top+rh*r,wk=(c+o.st)%7,h=HL[m+"-"+d];
  s+='<rect x="'+x+'" y="'+yy+'" width="'+cw+'" height="'+rh+'" fill="'+(d<1||d>n?"#f6f6f4":(h?"#fbf3f7":"#fff"))+'" stroke="#c9c9c9" stroke-width=".25"/>';
  if(d>=1&&d<=n){s+=T(x+2,yy+5.2,d,4.2,h?o.ac:(wk==0||wk==6?"#888":"#222"),"700");if(h)s+=T(x+2,yy+rh-2.2,h.length>24?h.slice(0,23)+"…":h,2.5,o.ac)}}
 if(side){var sx=W-mg-side+6,sw=side-6;s+=T(sx,top-2,"Projects this month",3.4,o.ac,"700");
  for(var i=0;i<5;i++){var by=top+4+i*9;s+='<rect x="'+sx+'" y="'+by+'" width="3.4" height="3.4" fill="none" stroke="#888" stroke-width=".3"/><line x1="'+(sx+5)+'" x2="'+(sx+sw)+'" y1="'+(by+3.4)+'" y2="'+(by+3.4)+'" stroke="#ccc" stroke-width=".25"/>'}
  var ny=top+54;s+=T(sx,ny,"Yarn, supplies and to-buy",3.4,o.ac,"700");for(var i=1;i<=5;i++)s+='<line x1="'+sx+'" x2="'+(sx+sw)+'" y1="'+(ny+i*7)+'" y2="'+(ny+i*7)+'" stroke="#ccc" stroke-width=".25"/>';
  var ty=ny+46;s+=T(sx,ty,"Notes",3.4,o.ac,"700");for(var i=1;i*7+ty<=H-mg-6;i++)s+='<line x1="'+sx+'" x2="'+(sx+sw)+'" y1="'+(ty+i*7)+'" y2="'+(ty+i*7)+'" stroke="#ccc" stroke-width=".25"/>'}
 s+=T(W-mg,H-4,"purlandpaperco.com",2.4,"#aaa","","end");
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'mm" height="'+H+'mm"><rect width="'+W+'" height="'+H+'" fill="#fff"/>'+s+'</svg>'}
function draw(){var o=opts(),mb=g("cl-mon-f");mb.hidden=o.lay=="year";var svg=o.lay=="year"?yearSvg(o):monthSvg(o,o.m);g("cl-prev").innerHTML=svg;window.PPsvg=svg;
 var HL=PPhol(o.y,o.hol),k=Object.keys(HL).length,f=new Date(o.y,0,1);
 g("cl-info").innerHTML="<strong>"+o.y+"</strong> starts on a "+["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][f.getDay()]+" and has "+((o.y%4==0&&o.y%100!=0)||o.y%400==0?"366 days (leap year)":"365 days")+"."+(k?" "+k+" holiday dates marked.":"")+" "+(o.lay=="year"?"One page, portrait.":"12 pages when you print, landscape.");
 try{localStorage.setItem("pp-cal",JSON.stringify(["cl-year","cl-lay","cl-start","cl-hol","cl-paper","cl-ac"].map(function(i){return g(i).value})))}catch(e){}}
window.PPcalPrint=function(){var o=opts(),pages=o.lay=="year"?[yearSvg(o)]:MN.map(function(_,m){return monthSvg(o,m)}),W=o.lay=="year"?o.pp[0]:o.pp[1],H=o.lay=="year"?o.pp[1]:o.pp[0],w=window.open("","_blank");if(!w)return;
 w.document.write('<!DOCTYPE html><html><head><title>'+o.y+' calendar</title><style>@page{size:'+W+'mm '+H+'mm;margin:0}body{margin:0}svg{display:block;page-break-after:always;break-after:page}</style></head><body>'+pages.join("")+'<scr'+'ipt>setTimeout(function(){print()},400)</scr'+'ipt></body></html>');w.document.close()};
window.PPcalDl=function(){var o=opts(),b=new Blob([window.PPsvg],{type:"image/svg+xml"}),a=document.createElement("a");a.href=URL.createObjectURL(b);a.download=o.y+"-calendar"+(o.lay=="year"?"":"-"+MN[o.m].toLowerCase())+".svg";a.click()};
if(!g("cl-prev"))return;
try{var sv=JSON.parse(localStorage.getItem("pp-cal")||"null");if(sv)["cl-year","cl-lay","cl-start","cl-hol","cl-paper","cl-ac"].forEach(function(i,n){if(sv[n]&&g(i).querySelector('option[value="'+sv[n]+'"]'))g(i).value=sv[n]})}catch(e){}
["cl-year","cl-lay","cl-start","cl-hol","cl-paper","cl-ac","cl-mon"].forEach(function(i){g(i).addEventListener("input",draw)});draw()})();</script>'''
CAL_CSS = '<style>#cl-prev{background:#fff;border:1px solid #ddd;border-radius:8px;padding:6px}#cl-prev svg{width:100%;height:auto;display:block}#cl-info{color:rgba(255,255,255,.85);font-size:.95rem}</style>'
def _cl_sel(i, lab, opts, sel=None): return f'<div class="field"><label for="{i}">{lab}</label><select id="{i}">' + "".join(f'<option value="{v}"{" selected" if v == sel else ""}>{t}</option>' for v, t in opts) + '</select></div>'
CL_US = [("Fri 1 Jan", "New Year's Day"), ("Mon 18 Jan", "Martin Luther King Jr. Day"), ("Mon 15 Feb", "Presidents' Day (Washington's Birthday)"), ("Mon 31 May", "Memorial Day"),
         ("Sat 19 Jun", "Juneteenth (observed Fri 18 Jun)"), ("Sun 4 Jul", "Independence Day (observed Mon 5 Jul)"), ("Mon 6 Sep", "Labor Day"), ("Mon 11 Oct", "Columbus Day"),
         ("Thu 11 Nov", "Veterans Day"), ("Thu 25 Nov", "Thanksgiving"), ("Sat 25 Dec", "Christmas Day (observed Fri 24 Dec)"), ("Fri 31 Dec", "New Year's Day 2028 (observed)")]
CL_UK = [("Fri 1 Jan", "New Year's Day"), ("Fri 26 Mar", "Good Friday"), ("Mon 29 Mar", "Easter Monday"), ("Mon 3 May", "Early May bank holiday"), ("Mon 31 May", "Spring bank holiday"),
         ("Mon 30 Aug", "Summer bank holiday"), ("Mon 27 Dec", "Christmas Day (substitute day)"), ("Tue 28 Dec", "Boxing Day (substitute day)")]
def _cl_tbl(rows): return '<div class="tbl-wrap"><table><thead><tr><th scope="col">Date (2027)</th><th scope="col">Holiday</th></tr></thead><tbody>' + "".join(f"<tr><td><strong>{d}</strong></td><td>{n}</td></tr>" for d, n in rows) + "</tbody></table></div>"
cl = top("Free 2027 calendar printable", "Make your own 2027 calendar: one page for the whole year, or a page a month, with US or UK holidays, Sunday or Monday start, on US Letter or A4. Print it or save it.", "2027 calendar printable") + CAL_CSS + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> <strong>2027 starts on a Friday</strong> (1 January) and ends on a Friday (31 December). It is <strong>not a leap year</strong>, so it has <strong>365 days</strong> and 52 ISO weeks. Easter Sunday is <strong>28 March 2027</strong>, Thanksgiving is <strong>Thursday 25 November</strong>, and Christmas Day falls on a <strong>Saturday</strong>. A 2027 calendar has the same layout as 2021, so a 2021 wall calendar lines up day for day.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<h2 style="margin-top:0">Make your calendar</h2>
<div class="row2">{_cl_sel("cl-lay", "Layout", [("year", "Whole year on one page"), ("month", "A month per page (12 pages)"), ("planner", "Monthly planner with project notes")])}
{_cl_sel("cl-year", "Year", [("2026", "2026"), ("2027", "2027"), ("2028", "2028")], "2027")}</div>
<div class="row2">{_cl_sel("cl-hol", "Holidays", [("us", "US federal holidays"), ("uk", "UK bank holidays"), ("none", "No holidays")])}
{_cl_sel("cl-start", "Week starts on", [("sun", "Sunday"), ("mon", "Monday")])}</div>
<div class="row2">{_cl_sel("cl-paper", "Paper", [("letter", "US Letter"), ("a4", "A4")])}
{_cl_sel("cl-ac", "Colour", [("ink", "Navy"), ("berry", "Berry"), ("teal", "Teal"), ("gold", "Marigold")])}</div>
<div class="field" id="cl-mon-f">{_cl_sel("cl-mon", "Preview month", [(str(i), m) for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])])}</div>
<div class="btns"><button type="button" class="btn" onclick="PPcalPrint()">Print or save as PDF</button> <button type="button" class="btn ghost" onclick="PPcalDl()">Save this page (SVG)</button></div>
<p class="note">To make a PDF, choose "Save as PDF" in the print window. Print at "Actual size". The monthly layouts print all 12 months at once. Planning your makes? Print the free <a href="{href("crochet-project-planner.html")}">crochet project planner</a> with a 2027 make list.</p>
</div><div class="result" aria-live="polite"><h2>Preview</h2><div id="cl-prev"></div><p id="cl-info"></p></div></div></section>
{CAL_JS}
<section><div class="wrap"><div class="narrow prose">
<h2>2027 US federal holidays</h2>
{_cl_tbl(CL_US)}
<p class="note">When a federal holiday falls on a Saturday it's usually observed on the Friday before, and on a Sunday the Monday after (the US Office of Personnel Management rule). That's why New Year's Day 2028, a Saturday, is observed on Friday 31 December 2027. Other days people plan around: Valentine's Day (Sun 14 Feb), Mother's Day (Sun 9 May), Father's Day (Sun 20 Jun) and Halloween (Sun 31 Oct).</p>
<h2>2027 UK bank holidays (England and Wales)</h2>
{_cl_tbl(CL_UK)}
<p class="note">Christmas Day and Boxing Day 2027 fall on a weekend, so the bank holidays move to Monday 27 and Tuesday 28 December. 1 January, 3 May and 28 December were set by royal proclamation in July 2026. Scotland and Northern Ireland have some different days.</p>
<h2>Which 2027 calendar layout should I print?</h2>
<ul><li><strong>Whole year on one page</strong>: for the fridge, a planner cover, or counting weeks to a deadline. Holidays are listed along the bottom.</li>
<li><strong>A month per page</strong>: big boxes to write appointments in. Pin it up or punch it for a binder.</li>
<li><strong>Monthly planner</strong>: the month grid plus a "Projects this month" checklist, a supplies list and notes. Made for makers: plan which blanket rows, gifts or market stock you'll finish each month.</li></ul>
<h2>Sunday or Monday start?</h2>
<p>US calendars usually start the week on Sunday; UK, European and ISO week calendars start on Monday. Pick whichever matches your diary so the days line up.</p>
<h2>Making it into a journal or planner</h2>
<p>Print the monthly pages double-sided, fold and stitch them into a booklet: the <a href="{href("junk-journal-signature-calculator.html")}">signature calculator</a> works out how many sheets per section. Add <a href="{href("dot-grid-paper.html")}">dot grid pages</a> between the months for notes and trackers, and letter the month names with <a href="{href("calligraphy-practice-sheets.html")}">calligraphy practice</a> first.</p>
<div class="callout"><strong>Setting goals for 2027?</strong> Fill in and print the free <a href="{href("2027-goal-planner-printable.html")}">2027 goal planner</a>: four goals, quarterly milestones and a monthly check-in.</div>
<div class="callout"><strong>Planning a year of making?</strong> The <a href="{href("temperature-blanket-planner.html")}">2027 temperature blanket planner</a> gives you a colour for every day of the year, and the <a href="{href("crochet-time-estimator.html")}">crochet time calculator</a> tells you which month a big project will be done.</div>
</div></div></section>{more_crafts("2027-calendar-printable.html")}'''
cl_faq = [
 ("What day does 2027 start on?", "Friday 1 January 2027. It also ends on a Friday, 31 December 2027."),
 ("Is 2027 a leap year?", "No. 2027 has 365 days. The next leap year is 2028, which has 29 February."),
 ("Which year has the same calendar as 2027?", "2021 and 2010. Both started on a Friday and weren't leap years, so every date falls on the same weekday. The next repeat is 2038."),
 ("When is Easter 2027?", "Sunday 28 March 2027. Good Friday is 26 March and Easter Monday is 29 March."),
 ("How many weeks are in 2027?", "52 ISO weeks. Week 1 starts on Monday 4 January 2027, and week 52 ends on Sunday 2 January 2028."),
 ("Is this 2027 calendar printable free?", "Yes. Print as many as you like, on US Letter or A4, or save them as a PDF or SVG image. Nothing to sign up for."),
]
SHOP_FOR["2027-calendar-printable.html"] = ["2027-habit-tracker-spreadsheet", "2027-crochet-knitting-planner", "december-days-journal-kit", "christmas-gift-planner-budget"]
page("2027-calendar-printable.html", "Free 2027 Calendar Printable: Yearly and Monthly | Purl & Paper",
     "Free printable 2027 calendar maker: whole year or a month per page, US or UK holidays, Sunday or Monday start, US Letter or A4. Print or save as PDF.",
     cl, cl_faq, "2027 calendar printable", app_name="2027 calendar printable maker")

exec((ROOT / "newcrafts.py").read_text())
