# ---------------- 26 Nov 2026 run 5: KNIT STITCH PATTERNS LIBRARY + SCRAPBOOK PAGE SIZES (+ photo layout calculator) ----------------
# Executed from build.py after stockread.py (shares page(), top(), href(), e(), SHOP_FOR, more_crafts()).
# Demand evidence in DEMAND.md (RADAR 26 Nov run 5). Drawings are our own SVG, generated from our own charts; wording our own.
# JS lives in assets/app.js (ks-* and sb-* features), CSS in assets/style.css.
import json as _json

# ======== KNIT STITCH PATTERNS (knit and purl only) ========
# Each pattern is a right-side chart: rows bottom-up (row 1 first), "1" = looks knit (a V) on the right side, "0" = looks purl (a bump).
# Written rows are DERIVED from the chart (flat knitting: wrong-side rows are worked from the other end with knit/purl swapped),
# so the words and the drawing can't disagree. Multiples checked against Gathered "17 knit and purl patterns", Yarnspirations
# "repeats and multiples", StudioKnit's beginner stitch list and Vogue Knitting basic stitches (SERP 26 Nov 2026).
KS = [  # key, name, other names, chart rows, multiple, plus, reversible, lies flat, good for, note
    ("stockinette", "Stockinette stitch", "UK: stocking stitch", ["1"], 1, 0, False, False, "Sweaters, hats, socks, colourwork",
     "The smooth fabric most patterns mean by default. It curls at every edge, so add a garter or rib border to a flat piece."),
    ("garter", "Garter stitch", "", ["1", "0"], 1, 0, True, True, "Scarves, dishcloths, borders, first projects",
     "Knit every row. Two rows make one ridge. It's squishy, stretches more in length than width, and looks the same on both sides."),
    ("reverse", "Reverse stockinette", "UK: reverse stocking stitch", ["0"], 1, 0, False, False, "Backgrounds for cables, rolled edges",
     "Stockinette shown bump side out. It curls too, so it usually sits between other stitches."),
    ("rib1", "1x1 rib", "knit 1, purl 1 rib", ["10"], 2, 1, True, True, "Cuffs, neckbands, hat brims",
     "Very stretchy and pulls in sideways, so it hugs. Knit the knits and purl the purls as they face you."),
    ("rib2", "2x2 rib", "knit 2, purl 2 rib", ["1100"], 4, 2, True, True, "Hat brims, sock cuffs, scarves",
     "Bolder columns than 1x1 rib and just as stretchy. Easy to read, so a good first rib."),
    ("seed", "Seed stitch", "UK: moss stitch", ["10", "01"], 2, 1, True, True, "Borders, washcloths, blankets, collars",
     "A pebbly texture. Each stitch is the opposite of the one below it: knit the purls and purl the knits."),
    ("moss", "Moss stitch (US)", "UK: double moss stitch", ["10", "10", "01", "01"], 2, 1, True, True, "Blankets, cushions, scarves",
     "Like seed stitch but the pattern changes every 2 rows, so it looks taller and a little looser."),
    ("box", "Double seed stitch", "box stitch", ["1100", "1100", "0011", "0011"], 4, 2, True, True, "Baby blankets, dishcloths",
     "Little 2-by-2 checks. A good step up from seed stitch that still lies flat."),
    ("check", "Basketweave checks", "checkerboard", ["11110000"] * 4 + ["00001111"] * 4, 8, 4, True, True, "Blankets, cushions, bags",
     "Blocks of 4 knits and 4 purls that swap every 4 rows. Bigger blocks (6 or 8) look bolder; just keep the multiple."),
    ("garter-rib", "Garter rib", "", ["1111", "1100"], 4, 2, False, True, "Scarves, wraps, men's hats",
     "Columns of smooth stockinette between columns of garter ridges. Only one row in two has purls, so it's quick."),
    ("broken-rib", "Broken rib", "", ["11", "10"], 2, 1, False, True, "Sweaters, cowls, beanies",
     "A knit row, then a k1 p1 row. Reads as soft vertical lines and doesn't pull in like true rib."),
    ("mistake-rib", "Mistake rib", "", ["1100", "1001"], 4, 3, True, True, "Scarves, cowls, blankets",
     "Every row is the same: k2, p2 to the last 3 stitches, then k2, p1. The offset gives a thick, ribbed fabric that lies flat."),
    ("andalusian", "Andalusian stitch", "", ["11", "11", "10", "11"], 2, 1, False, False, "Sweaters, socks, dishcloths",
     "Stockinette with a row of tiny purl dots every 4 rows. It curls a little less than plain stockinette."),
    ("welt", "Welt stitch", "ridge stitch, purl ridges", ["1", "1", "1", "1", "0", "0"], 1, 0, False, True, "Hats, cowls, sweater yokes",
     "4 rows of stockinette, then 2 purl rows on the right side. The ridges stand out and help it lie flatter."),
    ("diagonal", "Diagonal rib", "", ["1100", "1001", "0011", "0110"], 4, 0, False, True, "Scarves, cowls, bags",
     "2x2 rib that moves over one stitch every row, so the columns lean. Count carefully: the start of each row shifts."),
]
KS_BY = {k[0]: k for k in KS}

def _ks_bit(rows, r, x): g = rows[r % len(rows)]; return g[x % len(g)] == "1"

def ks_ops(rows, r, n):
    o = []
    for i in range(n):
        xr = i if r % 2 == 0 else n - 1 - i
        k = _ks_bit(rows, r, xr)
        o.append(("k" if k else "p") if r % 2 == 0 else ("p" if k else "k"))
    return o

def _ks_rl(a):
    u, i = [], 0
    while i < len(a):
        j = i
        while j < len(a) and a[j] == a[i]: j += 1
        u.append(a[i] + str(j - i)); i = j
    return u

def ks_say(o):
    n = len(o)
    for p in range(1, min(8, n) + 1):
        best = None
        for a in range(min(p, n)):
            if any(o[i] != o[a + (i - a) % p] for i in range(a, n)): continue
            reps = (n - a) // p
            if reps < 2 and p > 1: continue
            L, U, T = o[:a], o[a:a + p], o[a + reps * p:]
            sc = len(_ks_rl(L)) + len(_ks_rl(T)) + len(_ks_rl(U))
            if best is None or sc < best[3]: best = (L, U, T, sc)
        if not best: continue
        L, U, T, _ = best
        if p == 1 and not L: return "Knit every stitch." if o[0] == "k" else "Purl every stitch."
        t = len(T)
        s = (", ".join(_ks_rl(L)) + ", " if L else "") + "*" + ", ".join(_ks_rl(U)) + "; repeat from * "
        return s + (f"to last {t} sts, " if t > 1 else "to last st, ") + ", ".join(_ks_rl(T)) + "." if t else s + "to end."
    return ", ".join(_ks_rl(o)) + "."

def ks_rows(rows, n):
    H = len(rows) * (2 if len(rows) % 2 else 1)
    txt = [ks_say(ks_ops(rows, r, n)) for r in range(H)]
    for per in range(1, H + 1):
        if H % per == 0 and all(txt[r] == txt[r % per] for r in range(H)): return txt[:per]
    return txt

def ks_cast(m, x, n0=None):
    n = m * max(1, round((20 - x) / m)) + x if n0 is None else n0
    return max(n, m + x if m > 1 else 2)

def ks_swatch(rows, cols=16, nrows=12, cs=13, label=""):
    W, H = cols * cs + 10, nrows * cs + 10
    s = f'<rect width="{W}" height="{H}" rx="8" fill="#fbf8f1"/>'
    for r in range(nrows):
        for x in range(cols):
            cx = W - 5 - (x + 0.5) * cs; cy = H - 5 - (r + 0.5) * cs
            if _ks_bit(rows, r, x):
                s += f'<path d="M{cx-4.5:.1f} {cy-4.5:.1f} l4.5 8 l4.5 -8" fill="none" stroke="#e39a14" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            else:
                s += f'<path d="M{cx-5:.1f} {cy+1.5:.1f} q5 {-6 if (x + r) % 2 else 6} 10 0" fill="none" stroke="#b8326a" stroke-width="2.6" stroke-linecap="round"/>'
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(label)} swatch: Vs are knit stitches, bumps are purl stitches as seen on the right side">{s}</svg>'

def _ks_mult(m, x):
    if m == 1: return "Any number of stitches"
    return f"Multiple of {m}" + (f" + {x}" if x else "")

def _ks_card(k):
    key, n, aka, rows, m, x, rev, flat, uses, note = k
    N = ks_cast(m, x)
    rr = ks_rows(rows, N)
    ol = "".join(f"<li><strong>Row {i + 1}{' (RS)' if len(rr) > 1 and i % 2 == 0 else (' (WS)' if len(rr) > 1 else '')}:</strong> {e(t)}</li>" for i, t in enumerate(rr))
    rep = "Repeat this row." if len(rr) == 1 else f"Repeat rows 1 to {len(rr)}."
    tags = f'<span class="ks-tag">{"Reversible" if rev else "One right side"}</span><span class="ks-tag">{"Lies flat" if flat else "Curls at the edges"}</span>'
    return (f'<article class="ks-card" id="{key}"><div class="ks-sw">{ks_swatch(rows, label=n)}</div><div class="ks-tx">'
            f'<h3>{e(n)}</h3>' + (f'<p class="ks-aka">{e(aka)}</p>' if aka else "") +
            f'<p class="ks-meta"><strong>{_ks_mult(m, x)}</strong> &middot; {len(rr)}-row repeat {tags}</p>'
            f'<ol class="ks-rows">{ol}</ol><p class="ks-rep">{rep} Shown for {N} stitches.</p><p>{e(note)}</p><p class="muted"><strong>Good for:</strong> {e(uses)}</p></div></article>')

ks_cards = "".join(_ks_card(k) for k in KS)
ks_data = _json.dumps([{"k": k[0], "n": k[1], "g": k[3], "m": k[4], "x": k[5]} for k in KS], separators=(",", ":"))
ks_opts = "".join(f'<option value="{k[0]}"{" selected" if k[0] == "seed" else ""}>{e(k[1])}</option>' for k in KS)
ks_tbl = "".join(f'<tr><td><a href="#{k[0]}">{e(k[1])}</a></td><td>{_ks_mult(k[4], k[5])}</td><td>{len(ks_rows(k[3], ks_cast(k[4], k[5])))}</td><td>{"Yes" if k[6] else "No"}</td><td>{"Yes" if k[7] else "No, curls"}</td></tr>' for k in KS)
_seed_rows = ks_rows(KS_BY["seed"][3], 21)

ksp = top("Knit stitch patterns for beginners: 15 knit and purl stitches", "Fifteen textures you can make with nothing but knit and purl: what each looks like, the rows to knit, the stitch multiple, and whether it lies flat. Pick one below and get the rows for your own cast on.", "Knit stitch patterns") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the easiest knit stitch patterns for beginners are <strong>garter stitch</strong> (knit every row), <strong>stockinette</strong> (knit 1 row, purl 1 row), <strong>1x1 and 2x2 rib</strong>, and <strong>seed stitch</strong> (k1, p1, then knit the purls and purl the knits). For a scarf or blanket that lies flat, choose garter, seed, moss, double seed, basketweave checks or mistake rib; plain stockinette curls. Every pattern has a <strong>stitch multiple</strong>: cast on a number that fits it, like 21 for seed stitch (multiple of 2 + 1).</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="field"><label for="ks-pat">Stitch pattern</label><select id="ks-pat">{ks_opts}</select></div>
<div class="row2"><div class="field"><label for="ks-w">Width you want</label><input type="number" id="ks-w" value="8" min="1" max="120" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="ks-u">Units</label><select id="ks-u"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><label for="ks-g">Your gauge: stitches per 4 in / 10 cm</label><input type="number" id="ks-g" value="18" min="4" max="48" step="0.5" inputmode="decimal"><p class="sub">Worsted is about 16 to 20. Textured stitches can knit a little narrower than stockinette, so swatch in the pattern if the width matters.</p></div>
<div class="field"><label for="ks-n">Or type your own cast on (optional)</label><input type="number" id="ks-n" value="" min="2" max="600" step="1" inputmode="numeric" placeholder="e.g. 31"></div>
<p class="sub">Saved on this device only. Nothing is uploaded.</p>
</div><div class="result" aria-live="polite" id="ks-out"></div></div></section>
<script type="application/json" id="ks-data">{ks_data}</script>
<section><div class="wrap"><h2>All 15 stitch patterns, with rows and swatches</h2>
<p class="muted">Each drawing shows the right side: <span style="color:#c07d00;font-weight:700">V = knit stitch</span>, <span style="color:#b8326a;font-weight:700">bump = purl stitch</span>. Rows are for knitting flat, back and forth. RS = right side, WS = wrong side.</p>
<div class="ks-grid">{ks_cards}</div></div></section>
<section><div class="wrap"><div class="narrow prose">
<h2>Stitch multiples at a glance</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Pattern</th><th scope="col">Cast on</th><th scope="col">Rows to repeat</th><th scope="col">Reversible</th><th scope="col">Lies flat</th></tr></thead><tbody>{ks_tbl}</tbody></table></div>
<h2>What does "multiple of 2 + 1" mean?</h2>
<p>It's the number of stitches the pattern repeats across, plus a few extra to balance the edges. "Multiple of 2 + 1" means any even number plus one: 19, 21, 41. "Multiple of 4 + 2" means a number you can split into fours, plus two: 18, 22, 42. Get it wrong and the pattern won't line up from row to row, which is the most common reason seed stitch suddenly looks like rib. The tool above rounds your width to the nearest count that fits.</p>
<h2>How to tell a knit from a purl on your needles</h2>
<p>A knit stitch looks like a little <strong>V</strong>. A purl stitch has a horizontal <strong>bump</strong> at its base, like a collar. When a pattern says "knit the knits and purl the purls", look at the stitch on your left needle: V, knit it; bump, purl it. "Knit the purls and purl the knits" is the opposite, and that's all seed stitch is. If knit and purl are new, start with our step by step guide to <a href="{href("how-to-knit-and-purl.html")}">how to knit and purl</a>.</p>
<h2>Moving the yarn between knits and purls</h2>
<p>Whenever you switch from a knit to a purl, bring the yarn to the front <strong>between</strong> the needle tips, not over the top. When you switch back, take it to the back the same way. Taking the yarn over the needle adds an accidental stitch (a yarn over), which is why a rib can grow wider. Count your stitches at the end of the first few rows.</p>
<h2>Which stitch pattern for which project?</h2>
<ul><li><strong>Scarf:</strong> garter, seed, mistake rib or garter rib. Both sides show, so choose a reversible one. Size it with our <a href="{href("scarf-size-chart.html")}">scarf size chart</a>.</li>
<li><strong>Blanket:</strong> seed, moss, double seed or basketweave checks, which lie flat without a border. Plan the size in the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>.</li>
<li><strong>Hat:</strong> a 2x2 or 1x1 rib brim with a stockinette, welt or broken rib body. The <a href="{href("hat-size-chart.html")}">hat size calculator</a> gives the cast on.</li>
<li><strong>Dishcloth:</strong> garter, seed or double seed in cotton: small, quick and good practice.</li>
<li><strong>Sweater:</strong> stockinette body with rib cuffs; Andalusian or broken rib for texture. See the <a href="{href("sweater-size-calculator.html")}">sweater size calculator</a>.</li></ul>
<h2>Tips for neat textured knitting</h2>
<ul><li>Place a stitch marker every repeat on wide pieces, so a mistake shows up within a few stitches.</li>
<li>Add a 1-stitch garter edge each side (knit the first and last stitch of every row) for tidy edges. Cast on 2 extra stitches.</li>
<li>Keep track of which row you're on with the <a href="{href("row-counter.html")}">row counter</a>, especially for 4- and 8-row repeats.</li>
<li>Textures with lots of purls can come out looser. If yours looks uneven, try a needle half a size smaller for the purl-heavy rows or work your purls a little more snugly.</li>
<li>Binding off? Bind off in pattern (knit the knits, purl the purls) so the edge matches. Our <a href="{href("how-to-bind-off-knitting.html")}">bind off guide</a> shows how.</li></ul>
<p>Need the starting stitches for a whole project? The <a href="{href("cast-on-calculator.html")}">cast on calculator</a> handles multiples and borders, and the <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a> decodes any pattern line.</p>
<p class="note">Stitch multiples and row repeats follow the standard versions in Gathered's knit and purl pattern guide, Yarnspirations' "repeats and multiples", StudioKnit's beginner stitch list and Vogue Knitting's basic stitches (checked 26 Nov 2026). The rows on this page are written from our own charts, and the swatch drawings are our own.</p>
</div></div></section>'''
ks_faq = [
    ("What is the easiest knitting stitch pattern for beginners?", "Garter stitch: knit every row. Next try stockinette (knit a row, purl a row), then 1x1 or 2x2 rib and seed stitch, which only need knit and purl."),
    ("What is the difference between seed stitch and moss stitch?", "In US patterns, seed stitch changes every row (k1, p1, then knit the purls and purl the knits) and moss stitch changes every 2 rows. UK patterns call seed stitch 'moss stitch' and the US moss stitch 'double moss stitch'."),
    ("Which knitting stitches don't curl?", "Garter, seed, moss, double seed, rib, basketweave checks, garter rib, broken rib, welt and mistake rib all lie flat. Stockinette and reverse stockinette curl, so give them a flat border."),
    ("How many stitches do I cast on for seed stitch?", "Any odd number (a multiple of 2 + 1), for example 21 or 31, so every row starts and ends with k1. An even number works too, but then rows alternate between starting k1 and p1."),
    ("What are good reversible knitting stitches for a scarf?", "Garter stitch, seed stitch, moss stitch, 1x1 and 2x2 rib, double seed, basketweave checks and mistake rib look good on both sides."),
    (f"How do I knit seed stitch over 21 stitches?", f"Row 1: {_seed_rows[0]} Repeat that same row every time: with an odd number the k1 always lands on the purl bumps."),
]
SHOP_FOR["knit-stitch-patterns.html"] = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"]
page("knit-stitch-patterns.html", "Knit Stitch Patterns for Beginners: 15 Knit & Purl Stitches | Purl & Paper",
     "15 easy knit stitch patterns for beginners using only knit and purl: garter, seed, moss, rib, basketweave and more, with swatches, rows, stitch multiples and a cast on tool.",
     ksp, ks_faq, "Knit stitch patterns", app_name="Knit stitch pattern row writer")


# ======== SCRAPBOOK PAGE SIZES + PHOTO LAYOUT CALCULATOR ========
# Page sizes: the standard 12x12 in album and paper size, US letter 8.5x11, 8x8 and 6x6 albums, 6x8 and 9x12 albums, A4 in the
# UK/Europe (hometosight "how big are scrapbook pages", Creative Memories album guide 2024, getitscrapped album and page formats,
# Simple Scrapper on 8.5x11). Pocket pages: 12x12 protectors with six 4x6 pockets (Print File refills). Layout maths is ours.
SB_PAGES = [("12x12", "12 x 12 in", 12, 12, "The standard. Most patterned paper and cardstock is sold in 12 x 12 sheets, and most albums take it."),
            ("8.5x11", "8.5 x 11 in (US letter)", 8.5, 11, "Prints on a home printer, fits a binder. Popular for school and family albums."),
            ("a4", "A4 (210 x 297 mm)", 8.27, 11.69, "The UK and European letter size; A4 albums and page protectors are easy to find there."),
            ("9x12", "9 x 12 in", 9, 12, "A slimmer album size that still takes a 12 in sheet trimmed down."),
            ("8x8", "8 x 8 in", 8, 8, "Small and quick to fill. Buy 8 x 8 paper pads, or trim 12 x 12 sheets and keep the strips for borders."),
            ("6x8", "6 x 8 in", 6, 8, "Pocket-page and travel albums; one or two photos per page."),
            ("6x6", "6 x 6 in", 6, 6, "Mini albums and gift books. Four pages come out of one 12 x 12 sheet.")]
SB_PHOTOS = [("4x6", "4 x 6 in (standard print)", 4, 6), ("5x7", "5 x 7 in", 5, 7), ("3.5x5", "3.5 x 5 in", 3.5, 5), ("3x4", "3 x 4 in (pocket card size)", 3, 4),
             ("4x4", "4 x 4 in square", 4, 4), ("3x3", "3 x 3 in square", 3, 3), ("2x3", "2 x 3 in (wallet)", 2, 3), ("8x10", "8 x 10 in", 8, 10)]

def sb_grid(W, H, w, h, m, g):
    c = int((W - 2 * m + g + 1e-9) // (w + g)); r = int((H - 2 * m + g + 1e-9) // (h + g))
    return max(c, 0), max(r, 0)

def _sb_rows(W, H, w, h, m, g):
    """Rows of one orientation on top, rows of the other below. Returns photo rectangles (x, y, w, h)."""
    best = []
    for a, b in ((w, h), (h, w)):
        ca, _ = sb_grid(W, H, a, b, m, g); cb, _ = sb_grid(W, H, b, a, m, g)
        for ra in range(0, 40):
            used = ra * (b + g)
            if ra and 2 * m + used - g > H + 1e-9: break
            rb = max(0, int((H - 2 * m - used + g + 1e-9) // (a + g))) if cb else 0
            if ra * ca + rb * cb > len(best):
                R = [(m + i * (a + g), m + r * (b + g), a, b) for r in range(ra) for i in range(ca)]
                R += [(m + i * (b + g), m + used + r * (a + g), b, a) for r in range(rb) for i in range(cb)]
                best = R
    return best

def sb_rects(W, H, w, h, m=0.5, g=0.25):
    """Most w x h photos on a W x H page: row blocks, column blocks or a pinwheel of 4, whichever fits more."""
    best = _sb_rows(W, H, w, h, m, g)
    cols = [(y, x, hh, ww) for x, y, ww, hh in _sb_rows(H, W, w, h, m, g)]
    if len(cols) > len(best): best = cols
    L, S = max(w, h), min(w, h)
    if L > S and L + S + g <= min(W, H) - 2 * m + 1e-9 and len(best) < 4:
        best = [(m, m, L, S), (m + L + g, m, S, L), (m + S + g, m + L + g, L, S), (m, m + S + g, S, L)]
    return best

def sb_count(W, H, w, h, m=0.5, g=0.25): return len(sb_rects(W, H, w, h, m, g))

def sb_svg(W, H, w, h, m=0.5, g=0.25, s=22):
    R = sb_rects(W, H, w, h, m, g); cols = ["#2f8f8a", "#b8326a", "#e39a14", "#1f2a44"]
    out = f'<rect x="1" y="1" width="{W * s}" height="{H * s}" rx="4" fill="#f3ede2" stroke="#1f2a44" stroke-width="2"/>'
    out += "".join(f'<rect x="{1 + x * s:.1f}" y="{1 + y * s:.1f}" width="{pw * s:.1f}" height="{ph * s:.1f}" rx="2" fill="{cols[k % 4]}" opacity=".85"/>' for k, (x, y, pw, ph) in enumerate(R))
    return f'<svg viewBox="0 0 {W * s + 2:.0f} {H * s + 2:.0f}" role="img" aria-label="{len(R)} photos of {w:g} x {h:g} in on a {W:g} x {H:g} in page">{out}</svg>'

sb_tbl = "".join(f'<tr><td><strong>{e(nm)}</strong></td>' + "".join(f'<td>{sb_count(W, H, pw, ph)}</td>' for _, _, pw, ph in SB_PHOTOS[:5]) + "</tr>" for _, nm, W, H, _ in SB_PAGES)
sb_rows = "".join(f'<tr><td><strong>{e(nm)}</strong></td><td>{W:g} x {H:g} in</td><td>{W * 2.54:.1f} x {H * 2.54:.1f} cm</td><td>{e(u)}</td></tr>' for _, nm, W, H, u in SB_PAGES)
sb_mats = "".join(f'<tr><td>{e(nm.split(" (")[0])}</td>' + "".join(f'<td>{pw + 2 * b:g} x {ph + 2 * b:g} in</td>' for b in (0.125, 0.25, 0.5)) + "</tr>" for _, nm, pw, ph in SB_PHOTOS[:6])
sb_popts = "".join(f'<option value="{k}"{" selected" if k == "12x12" else ""}>{e(n)}</option>' for k, n, W, H, u in SB_PAGES) + '<option value="custom">My own size</option>'
sb_fopts = "".join(f'<option value="{k}"{" selected" if k == "4x6" else ""}>{e(n)}</option>' for k, n, a, b in SB_PHOTOS) + '<option value="custom">My own size</option>'
sb_data = _json.dumps({"p": {k: [W, H] for k, n, W, H, u in SB_PAGES}, "f": {k: [a, b] for k, n, a, b in SB_PHOTOS}}, separators=(",", ":"))
_n12 = sb_count(12, 12, 4, 6); _n85 = sb_count(8.5, 11, 4, 6); _n12m = sb_count(12, 12, 4.5, 6.5)

sbp = top("Scrapbook page sizes and how many photos fit", "Every common scrapbook page size in inches and cm, and a layout calculator: pick the page and photo size and see how many photos fit, how they sit, and how much room is left for journaling.", "Scrapbook page sizes") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> the standard scrapbook page is <strong>12 x 12 inches (30.5 x 30.5 cm)</strong>. Other common sizes are <strong>8.5 x 11 in</strong> (US letter), <strong>A4</strong> in the UK and Europe, <strong>8 x 8 in</strong>, <strong>6 x 8 in</strong> and <strong>6 x 6 in</strong> for mini albums. With a ½ in margin and ¼ in gaps, a 12 x 12 page fits up to <strong>{_n12} standard 4 x 6 photos</strong> (an 8.5 x 11 page fits {_n85}), though most layouts use 1 to 3 photos and leave room for paper, embellishments and journaling.</div></div></section>
<section style="padding-top:0"><div class="wrap tool"><div class="sheet">
<div class="row2"><div class="field"><label for="sb-page">Page size</label><select id="sb-page">{sb_popts}</select></div>
<div class="field"><label for="sb-photo">Photo size</label><select id="sb-photo">{sb_fopts}</select></div></div>
<div class="row2" id="sb-pc" hidden><div class="field"><label for="sb-pw">Page width (in)</label><input type="number" id="sb-pw" value="12" min="2" max="24" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="sb-ph">Page height (in)</label><input type="number" id="sb-ph" value="12" min="2" max="24" step="0.25" inputmode="decimal"></div></div>
<div class="row2" id="sb-fc" hidden><div class="field"><label for="sb-fw">Photo width (in)</label><input type="number" id="sb-fw" value="4" min="0.5" max="20" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="sb-fh">Photo height (in)</label><input type="number" id="sb-fh" value="6" min="0.5" max="20" step="0.25" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="sb-mat">Mat border round each photo</label><select id="sb-mat"><option value="0">No mat</option><option value="0.125">⅛ in</option><option value="0.25">¼ in</option><option value="0.5">½ in</option></select></div>
<div class="field"><label for="sb-m">Page margin (in)</label><input type="number" id="sb-m" value="0.5" min="0" max="3" step="0.125" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="sb-g">Gap between photos (in)</label><input type="number" id="sb-g" value="0.25" min="0" max="2" step="0.125" inputmode="decimal"></div>
<div class="field"><label for="sb-n">Photos for the whole album (optional)</label><input type="number" id="sb-n" value="" min="1" max="5000" step="1" inputmode="numeric" placeholder="e.g. 120"></div></div>
<div class="field"><label for="sb-want">Photos you want on this page</label><input type="number" id="sb-want" value="" min="1" max="40" step="1" inputmode="numeric" placeholder="as many as fit"></div>
<p class="sub">Saved on this device only. Nothing is uploaded.</p>
</div><div class="result" aria-live="polite" id="sb-out"></div></div></section>
<script type="application/json" id="sb-data">{sb_data}</script>
<section><div class="wrap"><div class="narrow prose">
<h2>Scrapbook page sizes chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size</th><th scope="col">Inches</th><th scope="col">Centimetres</th><th scope="col">Good to know</th></tr></thead><tbody>{sb_rows}</tbody></table></div>
<p>Album sizes name the page that goes in, not the outside cover, which is a little bigger. Page protectors (the clear sleeves) are made to match, so a 12 x 12 album takes 12 x 12 protectors.</p>
<h2>How many photos fit on a scrapbook page?</h2>
<p>The most that fit, photos turned whichever way packs best, with a ½ in margin round the page and ¼ in between photos (our own layout maths):</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Page</th>{"".join(f'<th scope="col">{e(n.split(" (")[0])}</th>' for k, n, a, b in SB_PHOTOS[:5])}</tr></thead><tbody>{sb_tbl}</tbody></table></div>
<figure class="sb-fig"><div>{sb_svg(12, 12, 4, 6)}<figcaption>12 x 12 page: {_n12} photos of 4 x 6</figcaption></div><div>{sb_svg(8.5, 11, 4, 6)}<figcaption>8.5 x 11 page: {_n85} photos of 4 x 6</figcaption></div></figure>
<p>That's the maximum. A classic 12 x 12 layout uses <strong>1 to 3 photos</strong> with patterned paper, a title and a journaling spot, and a two-page spread 4 to 6. Matting each photo takes room too: a 12 x 12 page fits {_n12m} matted 4 x 6 photos with a ¼ in mat. Pocket-page albums are the exception: their 12 x 12 protectors often hold six 4 x 6 pockets, or a mix of 4 x 6 and 3 x 4 cards.</p>
<h2>12 x 12 or 8.5 x 11: which should I choose?</h2>
<ul><li><strong>12 x 12</strong> if you buy patterned paper and kits: they're nearly all 12 x 12, so there's no trimming, and you get room for 2 to 4 photos plus embellishments.</li>
<li><strong>8.5 x 11</strong> (or A4) if you print backgrounds, journaling and ephemera at home, want a smaller shelf album, or keep pages in a binder.</li>
<li><strong>8 x 8 and 6 x 6</strong> for quick mini albums: a holiday, a baby's first year, a gift. One photo a page is plenty.</li></ul>
<p>Moving from 12 x 12 paper to an 8.5 x 11 album? Trim the sheet to 8.5 x 11 and keep the 3.5 x 12 in strip for borders and photo mats.</p>
<h2>Photo mat sizes</h2>
<p>A mat is the card behind a photo that shows as a thin frame. Cut the mat the photo size plus twice the border:</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Photo</th><th scope="col">⅛ in border</th><th scope="col">¼ in border</th><th scope="col">½ in border</th></tr></thead><tbody>{sb_mats}</tbody></table></div>
<h2>How to plan a scrapbook layout</h2>
<ol><li><strong>Pick the hero photo</strong> and decide its size. Everything else supports it.</li>
<li><strong>Use a simple grid.</strong> Line photos up with even gaps (the calculator's ¼ in is a good start); one bigger photo plus two smaller ones is a classic.</li>
<li><strong>Leave space for words.</strong> A title and a few lines of journaling make the page a memory, not just a photo display. Our <a href="{href("journal-prompts.html")}">journal prompt generator</a> helps when you're stuck.</li>
<li><strong>Group embellishments in threes</strong> near the hero photo, and repeat a colour from the photo in the paper.</li>
<li><strong>Glue down last.</strong> Lay everything out, take a phone photo of it, then stick it down with acid-free adhesive.</li></ol>
<p>Like a looser, layered look? <a href="{href("junk-journal-beginners.html")}">Junk journaling</a> uses the same skills with found paper, and our <a href="{href("junk-journal-ephemera-ideas.html")}">ephemera ideas</a> and <a href="{href("how-to-tea-stain-paper.html")}">tea-staining guide</a> make backgrounds for scrapbook pages too. Making a card from the offcuts? The <a href="{href("card-making.html")}">card and envelope size calculator</a> has every size.</p>
<p class="note">Sizes from album and paper makers' published sizes and scrapbooking guides (hometosight's standard page sizes, Creative Memories' album guide, Get It Scrapped's album formats, Simple Scrapper on 8.5 x 11 layouts) and the Print File six-pocket 12 x 12 refill (checked 26 Nov 2026). Photo counts and mat sizes are our own maths.</p>
</div></div></section>'''
sb_faq = [
    ("What is the standard scrapbook page size?", "12 x 12 inches (30.5 x 30.5 cm). Most patterned paper, cardstock and albums use it. 8.5 x 11 in, A4, 8 x 8 in and 6 x 6 in are the other common sizes."),
    ("How many 4x6 photos fit on a 12x12 scrapbook page?", f"Up to {_n12} with a ½ in margin and ¼ in gaps, and six in a 12 x 12 pocket page protector. Most designed layouts use 1 to 3 photos so there's room for paper, a title and journaling."),
    ("How many photos fit on an 8.5 x 11 scrapbook page?", f"Up to {_n85} standard 4 x 6 prints with a ½ in margin and ¼ in gaps, or 1 large 8 x 10 print."),
    ("What size are scrapbook pages in cm?", "A 12 x 12 in page is 30.5 x 30.5 cm, 8.5 x 11 in is 21.6 x 27.9 cm, A4 is 21 x 29.7 cm, 8 x 8 in is 20.3 x 20.3 cm and 6 x 6 in is 15.2 x 15.2 cm."),
    ("Is 12x12 or 8.5x11 better for scrapbooking?", "12 x 12 if you use bought patterned paper and kits, which are nearly all that size; 8.5 x 11 if you print pages at home or want a smaller binder album."),
    ("What size mat for a 4x6 photo?", "For a ¼ in border, cut the mat 4.5 x 6.5 in. For ⅛ in, 4.25 x 6.25 in; for ½ in, 5 x 7 in."),
]
SHOP_FOR["scrapbook-page-sizes.html"] = ["journaling-cards-3x4", "vintage-ephemera-pack", "junk-journal-mega-bundle", "december-days-journal-kit"]
page("scrapbook-page-sizes.html", "Scrapbook Page Sizes + How Many Photos Fit (Calculator) | Purl & Paper",
     "Scrapbook page sizes in inches and cm (12x12, 8.5x11, A4, 8x8, 6x6) and a layout calculator: how many 4x6 photos fit on a page, mat sizes, and pages for an album.",
     sbp, sb_faq, "Scrapbook page sizes", app_name="Scrapbook photo layout calculator")
