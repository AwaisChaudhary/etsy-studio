"""KDP paperback: "Good Copy: The Roomy Amateur Radio Logbook" (8.5x11, B&W, white paper).
Research 24 Nov 2026 (Amazon stripbooks): the sellers are 8.5x11. ARRL logbook BSR 40k (brand); indie #135k (120pp), #226k (108pp);
POTA/SOTA pocket log #351k. 1-3 star complaints: line spacing too small; space wasted on power and doubled RST columns while
Name/QTH get no room; pages don't lie flat so you write into the spine; a cover logo that copies ARRL's.
This book: 22 tall rows (0.36in) per page, wide Name and QTH/Grid columns, power/rig written once per page header,
one RST sent + one RST rcvd, QSL sent/rcvd tick boxes, extra-wide inner margin. 60 log pages = 1,320 contacts.
Plus POTA/SOTA activation logs, contest + net logs, WAS, DXCC and grid trackers, station/antenna pages, references."""
import pathlib, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import kdp

OUT = pathlib.Path("/home/claude/kdp/hamlog")
OUT.mkdir(parents=True, exist_ok=True)
TITLE, SUB, BRAND = "Good Copy", "The Roomy Amateur Radio Logbook", "Steady Ground Press"
LOG_PAGES, ROWS = 60, 22

CSS = """
body { font-family: 'Bitstream Charter', 'DejaVu Serif', serif; color:#111; }
h2 { font-family: Inter, sans-serif; font-weight: 800; font-size: 15pt; margin: 0 0 6pt; }
h3 { font-family: Inter, sans-serif; font-weight: 700; font-size: 9pt; margin: 8pt 0 3pt; }
p { font-size: 9.6pt; line-height: 1.45; margin: 0 0 6pt; }
.lab { font-family: Inter, sans-serif; font-size: 7.4pt; font-weight:700; letter-spacing:.03em; }
.line { border-bottom: .6pt solid #777; height: 21pt; }
table { border-collapse: collapse; width:100%; font-family: Inter, sans-serif; font-size: 7.4pt; }
td, th { border: .6pt solid #333; padding: 1.5pt 3pt; text-align:left; }
th { background:#e6e6e6; font-weight:700; font-size: 6.9pt; height: 15pt; }
.log td { height: 25.9pt; }
.log td.z { background:#f4f4f4; }
.c { text-align:center; }
.qb { font-size: 6.4pt; color:#333; white-space:nowrap; }
.qb span { display:inline-block; width:7pt; height:7pt; border:.7pt solid #222; vertical-align:-1pt; margin:0 1pt 0 2pt; }
.ph { display:flex; gap:10pt; font-family: Inter, sans-serif; font-size:7.6pt; margin-bottom:5pt; align-items:flex-end; }
.ph div { flex:1; border-bottom: .6pt solid #555; padding-bottom:2pt; }
.ph b { font-weight:800; font-size: 12pt; flex:0 0 auto; border:0; }
.small { font-size: 8pt; line-height:1.45; }
.tall td { height: 22pt; }
.cols2 { display:flex; gap: 14pt; } .cols2 > * { flex:1; }
.title { flex:1; display:flex; flex-direction:column; justify-content:center; }
.title .big { font-family:'GFS Baskerville', serif; font-size: 52pt; line-height:1; }
.states { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 12pt; font-family: Inter, sans-serif; font-size: 8pt; }
.states div { border-bottom: .5pt solid #999; padding: 3.6pt 0; display:flex; justify-content:space-between; }
.grid { display:grid; grid-template-columns: repeat(10, 1fr); border-left:.6pt solid #333; border-top:.6pt solid #333; }
.grid div { border-right:.6pt solid #333; border-bottom:.6pt solid #333; height: 26pt; font-family:Inter,sans-serif; font-size:6pt; color:#666; padding:1pt 2pt; }
"""


def lines(n):
    return "".join('<div class="line"></div>' for _ in range(n))


QSL = '<span class="qb">S<span></span> R<span></span></span>'


def log_page(i):
    rows = "".join(f'<tr><td></td><td></td><td></td><td></td><td></td><td class="c"></td><td class="c"></td><td></td><td></td><td>{QSL}</td><td></td></tr>' for _ in range(ROWS))
    return (f'<div class="ph"><b>Log {i}</b><div>Station / rig</div><div>Power</div><div>Antenna</div><div style="flex:.7">Location / grid</div></div>'
            '<table class="log"><colgroup><col style="width:8%"><col style="width:6.5%"><col style="width:8%"><col style="width:6%"><col style="width:12%">'
            '<col style="width:5%"><col style="width:5%"><col style="width:12%"><col style="width:14%"><col style="width:8.5%"><col></colgroup>'
            '<tr><th>Date</th><th>UTC</th><th>Freq / band</th><th>Mode</th><th>Call</th><th class="c">RST sent</th><th class="c">RST rcvd</th><th>Name</th><th>QTH / grid</th><th>QSL</th><th>Notes</th></tr>' + rows + '</table>')


pages = []
pages.append(f'<div class="title"><div class="big">{TITLE}</div><p style="font-size:15pt;margin-top:10pt">{SUB}</p>'
             '<p>1,320 contacts with room to write, plus POTA/SOTA, contest and net logs, award trackers and an operating reference.</p>'
             '<table class="tall" style="margin-top:30pt;width:4.6in"><tr><th style="width:35%">Call sign</th><td></td></tr><tr><th>Name</th><td></td></tr><tr><th>Grid / QTH</th><td></td></tr><tr><th>Log started</th><td></td></tr><tr><th>Log ended</th><td></td></tr></table>'
             '<p class="small" style="margin-top:14pt">If found, please return to the owner. QSL via the call sign above.</p></div>')
pages.append(f'<div style="margin-top:auto" class="small"><p class="small"><b>{TITLE}: {SUB}</b><br>Copyright © 2026 {BRAND}. All rights reserved.</p>'
             '<p class="small">Band edges and frequencies in this book are a quick reference for the United States (ITU Region 2) as of 2026. Your privileges depend on your licence class. Always check the current rules from the FCC or your own national regulator before transmitting.</p>'
             '<p class="small">This logbook is not affiliated with or endorsed by the ARRL, POTA, SOTA or any other organisation.</p></div>')
pages.append('<h2>How this log works</h2>'
             '<p><b>Written for real logging.</b> Every row is tall enough to write in comfortably, Name and QTH/grid get the widest columns, and power, rig and antenna go once at the top of each page instead of on every line.</p>'
             '<p><b>One RST each way.</b> RST sent and RST rcvd sit side by side. The QSL column has two tick boxes: S when you send a card or upload, R when it is confirmed.</p>'
             '<p><b>Times in UTC.</b> Log in UTC so your records match the other station and online confirmations.</p>'
             '<p><b>Wide inner margin.</b> The columns stop well short of the spine, so you never have to write into the fold. Press the book open firmly once and it will stay open better.</p>'
             '<h3>Inside</h3><p>Station and antenna records · 60 log pages (1,320 contacts) · 6 POTA/SOTA activation logs · 4 contest logs · 4 net logs · Worked All States tracker · DXCC tracker · grid-square tracker · QSL card log · reference pages: band plan, FT8 and calling frequencies, phonetic alphabet, Q-codes, RST scale, time zones.</p>'
             '<h3>Example row</h3><table><tr><th>Date</th><th>UTC</th><th>Freq / band</th><th>Mode</th><th>Call</th><th>RST S</th><th>RST R</th><th>Name</th><th>QTH / grid</th><th>QSL</th><th>Notes</th></tr>'
             '<tr style="font-family:\'Bitstream Charter\',serif;font-style:italic;font-size:8.5pt"><td>2026-12-03</td><td>1412</td><td>14.074</td><td>FT8</td><td>K1ABC</td><td>-08</td><td>-12</td><td>Ann</td><td>FN42</td><td>S ✓</td><td>first CT</td></tr></table>')
for n in (1, 2):
    pages.append(f'<h2>Station record {n}</h2><table class="tall"><tr><th style="width:32%">Radio (make / model)</th><td></td></tr><tr><th>Serial number</th><td></td></tr><tr><th>Purchased / from</th><td></td></tr>'
                 '<tr><th>Power supply</th><td></td></tr><tr><th>Tuner / amplifier</th><td></td></tr><tr><th>Microphone / key</th><td></td></tr><tr><th>Computer / interface</th><td></td></tr><tr><th>Software</th><td></td></tr></table>'
                 '<h3>Antennas</h3><table class="tall"><tr><th>Antenna</th><th>Bands</th><th>Height / direction</th><th>Feed line</th><th>SWR notes</th></tr>' + "<tr><td></td><td></td><td></td><td></td><td></td></tr>" * 5 + '</table>'
                 '<h3>Memory channels and repeaters</h3><table class="tall"><tr><th>Ch</th><th>Name</th><th>Output</th><th>Offset</th><th>Tone</th><th>Notes</th></tr>' + "<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>" * 7 + '</table>')
pages.append('<h2>Licence and equipment changes</h2><table class="tall"><tr><th style="width:30%">Licence class</th><td></td></tr><tr><th>Granted</th><td></td></tr><tr><th>Expires</th><td></td></tr><tr><th>FRN / ID</th><td></td></tr></table>'
             '<h3>Changes, repairs and upgrades</h3><table class="tall"><tr><th style="width:16%">Date</th><th>What changed</th></tr>' + "<tr><td></td><td></td></tr>" * 16 + '</table>')
for i in range(1, LOG_PAGES + 1):
    pages.append(log_page(i))


def act_page(kind, i):
    rows = "".join("<tr><td class='c'>" + str(k) + "</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" for k in range(1, 23))
    return (f'<h2>{kind} activation log {i}</h2><div class="ph"><div>Park / summit ref</div><div>Name</div><div>Date (UTC)</div><div style="flex:.6">Grid</div></div>'
            '<div class="ph"><div>Rig and power</div><div>Antenna</div><div style="flex:.6">Start UTC</div><div style="flex:.6">End UTC</div></div>'
            '<table class="log" style="font-size:7pt"><tr><th class="c" style="width:4%">#</th><th style="width:9%">UTC</th><th style="width:11%">Band / freq</th><th style="width:7%">Mode</th><th style="width:15%">Call</th><th style="width:7%">Sent</th><th style="width:7%">Rcvd</th><th>Their park / summit (P2P, S2S) / notes</th></tr>' + rows.replace('<td', '<td style="height:21.4pt"', 0) + '</table>')


for i in range(1, 7):
    pages.append(act_page("POTA / SOTA", i).replace('class="log"', 'class="log" ').replace('<td></td>', '<td style="height:20.8pt"></td>'))
for i in range(1, 5):
    rows = "".join(f"<tr><td class='c'>{k}</td>" + "<td></td>" * 8 + "</tr>" for k in range(1, 24))
    pages.append(f'<h2>Contest log {i}</h2><div class="ph"><div>Contest</div><div>Date</div><div>Category</div><div style="flex:.6">My exchange</div></div>'
                 '<table class="log"><tr><th class="c" style="width:4%">#</th><th style="width:8%">UTC</th><th style="width:8%">Band</th><th style="width:7%">Mode</th><th style="width:15%">Call</th><th style="width:12%">Sent</th><th style="width:16%">Rcvd</th><th style="width:7%">Mult</th><th>Pts</th></tr>' + rows.replace('<td></td>', '<td style="height:21pt"></td>') + '</table>')
for i in range(1, 5):
    rows = "".join(f"<tr><td class='c'>{k}</td>" + "<td></td>" * 5 + "</tr>" for k in range(1, 23))
    pages.append(f'<h2>Net log {i}</h2><div class="ph"><div>Net name</div><div>Frequency / repeater</div><div>Date</div><div style="flex:.6">Net control</div></div>'
                 '<table class="log"><tr><th class="c" style="width:4%">#</th><th style="width:9%">UTC in</th><th style="width:16%">Call</th><th style="width:16%">Name</th><th style="width:18%">Location</th><th>Traffic / comments</th></tr>' + rows.replace('<td></td>', '<td style="height:22.6pt"></td>') + '</table>')
STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
          "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
          "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
          "Washington", "West Virginia", "Wisconsin", "Wyoming"]
assert len(STATES) == 50
st = "".join(f'<div><span>{s}</span><span class="qb">W<span></span> C<span></span> ____</span></div>' for s in STATES)
pages.append(f'<h2>Worked All States tracker</h2><p>Tick W when worked and C when confirmed. Write the band or call on the line.</p><div class="states">{st}</div>')
for i in range(1, 7):
    rows = "".join(f"<tr><td class='c'>{(i - 1) * 27 + k}</td>" + "<td></td>" * 7 + "</tr>" for k in range(1, 28))
    pages.append(f'<h2>DXCC tracker {i}</h2><table><tr><th class="c" style="width:5%">#</th><th style="width:24%">Entity</th><th style="width:9%">Prefix</th><th style="width:14%">Call</th><th style="width:12%">Date</th><th style="width:9%">Band</th><th style="width:8%">Mode</th><th>Confirmed</th></tr>' + rows.replace('<td></td>', '<td style="height:19pt"></td>') + '</table>')
for i in range(1, 3):
    pages.append(f'<h2>Grid square tracker {i}</h2><p>Write each new grid (for example FN42) in a box, with the band and date.</p><div class="grid">' + "<div></div>" * 220 + '</div>')
rows = "".join("<tr>" + "<td></td>" * 6 + "</tr>" for _ in range(26))
for i in range(1, 3):
    pages.append(f'<h2>QSL card log {i}</h2><table><tr><th style="width:16%">Call</th><th style="width:13%">QSO date</th><th style="width:13%">Sent</th><th style="width:12%">Via</th><th style="width:13%">Received</th><th>Notes</th></tr>' + rows.replace('<td></td>', '<td style="height:20pt"></td>') + '</table>')
BANDS = [("160 m", "1.800-2.000", "1.840"), ("80 m", "3.500-4.000", "3.573"), ("60 m", "5 MHz channels (check rules)", "5.357"), ("40 m", "7.000-7.300", "7.074"), ("30 m", "10.100-10.150", "10.136"),
         ("20 m", "14.000-14.350", "14.074"), ("17 m", "18.068-18.168", "18.100"), ("15 m", "21.000-21.450", "21.074"), ("12 m", "24.890-24.990", "24.915"), ("10 m", "28.000-29.700", "28.074"),
         ("6 m", "50.0-54.0", "50.313"), ("2 m", "144-148", "144.174"), ("1.25 m", "222-225", ""), ("70 cm", "420-450", "")]
br = "".join(f"<tr><td>{b}</td><td>{r}</td><td>{f}</td><td></td></tr>" for b, r, f in BANDS)
pages.append('<h2>Quick reference: bands</h2><p class="small">US (Region 2) band edges in MHz. Privileges inside each band depend on licence class and mode. Check the current FCC chart before you transmit.</p>'
             f'<table class="tall"><tr><th>Band</th><th>Range (MHz)</th><th>Common FT8</th><th>My notes / favourite frequencies</th></tr>{br}</table>'
             '<h3>Common calling frequencies</h3><table><tr><th>2 m FM simplex</th><th>70 cm FM simplex</th><th>6 m SSB</th><th>2 m SSB</th></tr><tr><td>146.520</td><td>446.000</td><td>50.125</td><td>144.200</td></tr></table>')
PH = "Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima Mike November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey X-ray Yankee Zulu".split()
QC = [("QRL", "Is this frequency in use?"), ("QRM", "Interference from other stations"), ("QRN", "Static / natural noise"), ("QRO", "Increase power"), ("QRP", "Decrease power / low power"),
      ("QRQ", "Send faster"), ("QRS", "Send slower"), ("QRT", "Stop sending / closing down"), ("QRU", "Nothing more for you"), ("QRV", "I am ready"), ("QRX", "Wait / stand by"),
      ("QRZ", "Who is calling me?"), ("QSB", "Signals are fading"), ("QSL", "I confirm / acknowledge"), ("QSO", "A contact"), ("QSY", "Change frequency"), ("QTH", "My location is")]
ph = "".join(f"<tr><td><b>{w[0]}</b></td><td>{w}</td></tr>" for w in PH)
qc = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in QC)
pages.append(f'<h2>Quick reference: phonetics and Q-codes</h2><div class="cols2"><table>{ph}</table><table>{qc}</table></div>')
pages.append('<h2>Quick reference: RST and UTC</h2><div class="cols2"><div><h3>R: readability</h3><table><tr><td>1</td><td>Unreadable</td></tr><tr><td>2</td><td>Barely readable</td></tr><tr><td>3</td><td>Readable with difficulty</td></tr><tr><td>4</td><td>Readable, almost no difficulty</td></tr><tr><td>5</td><td>Perfectly readable</td></tr></table>'
             '<h3>T: tone (CW only)</h3><table><tr><td>1</td><td>Very rough, broad</td></tr><tr><td>5</td><td>Rough, musical modulation</td></tr><tr><td>9</td><td>Perfect tone</td></tr></table></div>'
             '<div><h3>S: signal strength</h3><table><tr><td>1</td><td>Faint, barely perceptible</td></tr><tr><td>3</td><td>Weak</td></tr><tr><td>5</td><td>Fairly good</td></tr><tr><td>7</td><td>Moderately strong</td></tr><tr><td>9</td><td>Extremely strong</td></tr></table>'
             '<h3>UTC from US time zones</h3><table><tr><th>Zone</th><th>Standard</th><th>Daylight</th></tr><tr><td>Eastern</td><td>+5 h</td><td>+4 h</td></tr><tr><td>Central</td><td>+6 h</td><td>+5 h</td></tr><tr><td>Mountain</td><td>+7 h</td><td>+6 h</td></tr><tr><td>Pacific</td><td>+8 h</td><td>+7 h</td></tr><tr><td>Alaska</td><td>+9 h</td><td>+8 h</td></tr><tr><td>Hawaii</td><td>+10 h</td><td>n/a</td></tr></table>'
             '<p class="small" style="margin-top:4pt">Add the hours to local time to get UTC.</p></div></div>')
while len(pages) % 2 or len(pages) < 100:
    pages.append('<h2>Notes</h2>' + lines(28))

if __name__ == "__main__":
    prev = [(2, OUT / "p-how.png"), (6, OUT / "p-log.png"), (66, OUT / "p-pota.png"), (76, OUT / "p-net.png"), (80, OUT / "p-was.png"), (81, OUT / "p-dxcc.png"), (87, OUT / "p-grid.png"), (91, OUT / "p-ref.png"), (93, OUT / "p-rst.png")]
    n = kdp.interior(pages, CSS, 8.5, 11, OUT / "interior.pdf", inside=0.75, outside=0.4, top=0.45, bottom=0.45, previews=prev)
    (OUT / "pages.txt").write_text(str(n))
    print("pages", n)
