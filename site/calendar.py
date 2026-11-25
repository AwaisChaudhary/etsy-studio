# ---------------- 2027 CALENDAR PRINTABLE (DEMAND C8; "2027 calendar printable" 10k-100k worldwide, +900% YoY) ----------------
# Executed at the end of crafts.py (shares page(), top(), href(), more_crafts(), shop_box()).
CAL_JS = r'''<script>
(function(){
var MN=["January","February","March","April","May","June","July","August","September","October","November","December"];
var DN=["S","M","T","W","T","F","S"],DL=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
function g(i){return document.getElementById(i)}
function nth(y,m,dow,n){var d=new Date(y,m,1),c=0;while(true){if(d.getDay()==dow){c++;if(c==n)return d.getDate()}d.setDate(d.getDate()+1)}}
function last(y,m,dow){var d=new Date(y,m+1,0);while(d.getDay()!=dow)d.setDate(d.getDate()-1);return d.getDate()}
function easter(y){var a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),gg=Math.floor((b-f+1)/3),h=(19*a+b-d-gg+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*m+114)/31),da=((h+l-7*m+114)%31)+1;return new Date(y,mo-1,da)}
function hol(y,set){var H={};function add(m,d,n){H[m+"-"+d]=n}
 if(set=="us"){add(0,1,"New Year's Day");add(0,nth(y,0,1,3),"MLK Day");add(1,nth(y,1,1,3),"Presidents' Day");add(4,last(y,4,1),"Memorial Day");add(5,19,"Juneteenth");add(6,4,"Independence Day");add(8,nth(y,8,1,1),"Labor Day");add(9,nth(y,9,1,2),"Columbus Day");add(10,11,"Veterans Day");add(10,nth(y,10,4,4),"Thanksgiving");add(11,25,"Christmas Day")}
 if(set=="uk"){var e=easter(y),gf=new Date(e),em=new Date(e);gf.setDate(e.getDate()-2);em.setDate(e.getDate()+1);add(0,1,"New Year's Day");add(gf.getMonth(),gf.getDate(),"Good Friday");add(em.getMonth(),em.getDate(),"Easter Monday");add(4,nth(y,4,1,1),"Early May bank holiday");add(4,last(y,4,1),"Spring bank holiday");add(7,last(y,7,1),"Summer bank holiday");add(11,25,"Christmas Day");add(11,26,"Boxing Day")}
 return H}
function month(y,m,ws,H,big){var first=(new Date(y,m,1).getDay()-ws+7)%7,n=new Date(y,m+1,0).getDate(),h='<table class="cm'+(big?' big':'')+'"><caption>'+MN[m]+(big?' '+y:'')+'</caption><thead><tr>';
 for(var i=0;i<7;i++)h+='<th>'+(big?DL:DN)[(i+ws)%7]+'</th>';h+='</tr></thead><tbody><tr>';
 for(i=0;i<first;i++)h+='<td></td>';
 for(var d=1;d<=n;d++){var k=m+"-"+d,cls=H[k]?' class="hd"':'';h+='<td'+cls+(H[k]?' title="'+H[k]+'"':'')+'><span>'+d+'</span>'+(big&&H[k]?'<small>'+H[k]+'</small>':'')+'</td>';if((first+d)%7==0&&d<n)h+='</tr><tr>'}
 var rem=(7-(first+n)%7)%7;for(i=0;i<rem;i++)h+='<td></td>';
 return h+'</tr></tbody></table>'}
function build(){var y=+g("cl-year").value,ws=+g("cl-ws").value,lay=g("cl-lay").value,H=hol(y,g("cl-hol").value),out='';
 if(lay=="year"){out='<div class="cy"><h2 class="cy-h">'+y+'</h2><div class="cy-grid">';for(var m=0;m<12;m++)out+=month(y,m,ws,H,false);out+='</div>';
  var L=Object.keys(H).map(function(k){var p=k.split("-");return [+p[0],+p[1],H[k]]}).sort(function(a,b){return a[0]-b[0]||a[1]-b[1]});
  if(L.length)out+='<p class="cy-hl">'+L.map(function(x){return MN[x[0]].slice(0,3)+' '+x[1]+': '+x[2]}).join(' &nbsp;|&nbsp; ')+'</p>';out+='</div>'}
 else{for(var m2=0;m2<12;m2++)out+='<div class="cpage">'+month(y,m2,ws,H,true)+'<div class="cnotes">Notes</div></div>'}
 g("cl-prev").innerHTML=out;g("cl-prev").className="cl-prev "+lay}
window.CLprint=function(){var css=document.getElementById("cl-css").textContent,paper=g("cl-paper").value=="a4"?"A4":"letter",lay=g("cl-lay").value;
 var w=window.open("","_blank");if(!w){window.print();return}
 w.document.write('<!doctype html><html><head><title>'+g("cl-year").value+' calendar | Purl & Paper</title><style>'+css+'@page{size:'+paper+(lay=="month"?' landscape':' portrait')+';margin:10mm}body{margin:0;font-family:Georgia,serif}.cpage{page-break-after:always;height:180mm}.cpage:last-child{page-break-after:auto}.cl-prev{max-width:none}</style></head><body><div class="cl-prev '+lay+'">'+g("cl-prev").innerHTML+'</div><p style="font:9px sans-serif;color:#777;text-align:center">purlandpaperco.com</p></body></html>');
 w.document.close();setTimeout(function(){w.focus();w.print()},300)};
["cl-year","cl-ws","cl-lay","cl-hol","cl-paper"].forEach(function(i){g(i).addEventListener("input",build)});build();
})();</script>'''
CAL_CSS = '''<style id="cl-css">
.cl-prev{background:#fff;color:#222;border-radius:10px;padding:14px;max-width:100%;overflow:auto}
.cy-h{font-family:Georgia,serif;text-align:center;font-size:2rem;margin:0 0 8px}
.cy-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 14px}
@media(min-width:700px){.cl-prev.year .cy-grid{grid-template-columns:repeat(4,1fr)}}
table.cm{width:100%;border-collapse:collapse;font:12px/1.3 system-ui,sans-serif}
table.cm caption{font:700 14px Georgia,serif;text-align:left;padding:2px 0 4px;color:#b8326a}
table.cm th{font-weight:600;color:#666;background:none;font-size:10px;padding:2px 0;border:0}
table.cm td{text-align:center;padding:2px 0;border:0;background:none}
table.cm td.hd span{background:#f4a823;border-radius:50%;padding:1px 4px}
.cy-hl{font:10px/1.5 system-ui,sans-serif;color:#555;margin:10px 0 0}
.cpage{margin-bottom:22px}
table.cm.big{table-layout:fixed;font-size:13px}
table.cm.big caption{font-size:24px;text-align:center;padding-bottom:8px}
table.cm.big td{border:1px solid #ccc;height:62px;vertical-align:top;text-align:left;padding:4px}
table.cm.big td small{display:block;font-size:9px;color:#b8326a;margin-top:2px}
table.cm.big td.hd span{background:none;color:#b8326a;font-weight:700}
.cnotes{border:1px solid #ccc;border-top:0;height:50px;padding:4px;font:11px system-ui,sans-serif;color:#999}
</style>'''

calp = top("2027 calendar printable (free)", "A whole year on one page, or twelve monthly pages with room to write. Start weeks on Sunday or Monday, add US or UK holidays, and print on Letter or A4.", "2027 calendar") + CAL_CSS + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> 2027 starts on a <strong>Friday</strong> and ends on a Friday. It is not a leap year (365 days). Easter Sunday is <strong>28 March 2027</strong>, Thanksgiving (US) is <strong>25 November</strong>, and Christmas Day falls on a <strong>Saturday</strong>.</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sheet" style="max-width:760px">
<div class="row2"><div class="field"><label for="cl-year">Year</label><select id="cl-year"><option>2026</option><option selected>2027</option><option>2028</option></select></div>
<div class="field"><label for="cl-lay">Layout</label><select id="cl-lay"><option value="year">Whole year on one page</option><option value="month">12 monthly pages</option></select></div></div>
<div class="row2"><div class="field"><label for="cl-ws">Week starts on</label><select id="cl-ws"><option value="0">Sunday</option><option value="1">Monday</option></select></div>
<div class="field"><label for="cl-hol">Holidays</label><select id="cl-hol"><option value="none">None</option><option value="us">US federal holidays</option><option value="uk">UK bank holidays (England and Wales)</option></select></div></div>
<div class="field"><label for="cl-paper">Paper</label><select id="cl-paper"><option value="letter">US Letter</option><option value="a4">A4</option></select></div>
<div class="btns"><button type="button" class="btn" onclick="CLprint()">Print or save as PDF</button></div>
<p class="note">To save a PDF, choose "Save as PDF" as the printer. Monthly pages print landscape, the year page prints portrait.</p>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><div id="cl-prev" class="cl-prev"></div></div></section>
{CAL_JS}
<section><div class="wrap"><div class="narrow prose">
<h2>2027 at a glance</h2>
<ul><li>1 January 2027 is a Friday; 31 December 2027 is a Friday.</li>
<li>2027 has 365 days and 52 full weeks plus one day. The next leap year is 2028.</li>
<li>Good Friday is 26 March and Easter Monday is 29 March 2027.</li>
<li>US: Memorial Day 31 May, Independence Day 4 July (a Sunday), Labor Day 6 September, Thanksgiving 25 November.</li>
<li>UK (England and Wales): Early May bank holiday 3 May, Spring bank holiday 31 May, Summer bank holiday 30 August. Christmas Day is a Saturday and Boxing Day a Sunday, so the substitute bank holidays are Monday 27 and Tuesday 28 December.</li></ul>
<p class="muted">The tool marks each holiday on its calendar date. When a holiday falls at a weekend, the day off is usually moved to the next weekday; check gov.uk or opm.gov for official observed dates.</p>
<h2>Ways to use a printable calendar</h2>
<ul><li><strong>Make it into a planner:</strong> print the 12 monthly pages double-sided, fold and stitch them into a booklet. The <a href="{href("junk-journal-signature-calculator.html")}">signature calculator</a> tells you how many sheets to fold.</li>
<li><strong>Craft and project planning:</strong> mark deadlines for handmade gifts with the <a href="{href("crochet-knitting-gift-planner.html")}">gift planner</a>, or plan a year-long <a href="{href("temperature-blanket-planner.html")}">temperature blanket</a> for 2027.</li>
<li><strong>Bullet journal future log:</strong> paste the one-page year into your journal, then build monthly spreads on <a href="{href("dot-grid-paper.html")}">dot grid paper</a>.</li>
<li><strong>Shop sellers:</strong> mark sale events and busy seasons, then plan stock in our <a href="{href("seller-tools.html")}">seller tools</a>.</li></ul>
</div></div></section>{more_crafts("2027-calendar-printable.html")}'''
cal_faq = [
 ("What day does 2027 start on?", "1 January 2027 is a Friday, and 31 December 2027 is also a Friday."),
 ("Is 2027 a leap year?", "No. 2027 has 365 days. The next leap year is 2028."),
 ("When is Easter 2027?", "Easter Sunday is 28 March 2027. Good Friday is 26 March and Easter Monday is 29 March."),
 ("How do I print a 2027 calendar for free?", "Choose a layout, week start and holidays above, then press Print. Pick 'Save as PDF' as the printer to keep a PDF copy."),
 ("Can I print a 2027 calendar starting on Monday?", "Yes. Set 'Week starts on' to Monday before printing."),
]
page("2027-calendar-printable.html", "2027 Calendar Printable (Free): Yearly + Monthly, US/UK Holidays, Letter or A4 | Purl & Paper",
     "Free printable 2027 calendar: one-page year or 12 monthly pages with room for notes, Sunday or Monday start, US or UK holidays, Letter or A4. Print or save as PDF.",
     calp, cal_faq, "2027 calendar", app_name="2027 printable calendar maker")
