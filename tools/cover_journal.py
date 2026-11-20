"""Knit & Crochet Project Journal: premium wrap cover (v2).
Front: title on cream, knitted fabric panel with a Fair Isle band, yarn ball with a strand running into the stitches.
Back: fanned real interior pages, blurb and contents; knitted band continues round the spine.
Run after book_project_journal.py (needs the interior PDF for page previews and page count)."""
import base64, pathlib, subprocess, tempfile
from kdp import cover

OUT = pathlib.Path("/home/claude/kdp/project-journal")
TW, TH, PAGES = 8.5, 11, 110
INK, BERRY, TEAL, GOLD, CREAM = "#1f2a44", "#b8326a", "#2f8f8a", "#f4a823", "#f4efe6"


def page_png(n, dpi=110):
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), str(OUT / "project-journal-interior.pdf"), str(tmp / "p")], check=True,
                   stderr=subprocess.DEVNULL)
    f = next(tmp.glob("p-*.png"))
    return "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()


# ---------- knitted fabric (SVG): rows of V stitches, colour chart per row ----------
SW, SH = 16, 14  # stitch cell (px in svg units)
MOTIF = [  # Fair Isle band: 0 = ground, 1 = motif colour
    "0001000000010000",
    "0011100000111000",
    "0111110001111100",
    "1111111011111110",
    "0111110001111100",
    "0011100000111000",
    "0001000000010000",
]


def stitch(x, y, c):
    # one knit stitch = two leaning petals forming a V
    return (f'<path d="M{x + 1},{y + 1} Q{x + 2},{y + SH * .75} {x + SW / 2},{y + SH + 3} Q{x + SW / 2 - 1},{y + SH * .3} {x + 1},{y + 1}Z" fill="{c}"/>'
            f'<path d="M{x + SW - 1},{y + 1} Q{x + SW - 2},{y + SH * .75} {x + SW / 2},{y + SH + 3} Q{x + SW / 2 + 1},{y + SH * .3} {x + SW - 1},{y + 1}Z" fill="{c}"/>')


def shade(hexc, f):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * f))) for v in (r, g, b))


def fabric(cols, rows_spec):
    """rows_spec: list of (ground, motif_colour or None, motif_row_index or None) from top to bottom."""
    out = []
    for r, (g, mc, mi) in enumerate(rows_spec):
        for k in range(cols):
            c = g
            if mc is not None:
                c = mc if MOTIF[mi][k % len(MOTIF[mi])] == "1" else g
            c = shade(c, 1.0 + (0.04 if (k + r) % 2 else -0.04))  # subtle yarn variation
            out.append(stitch(k * SW, r * SH, c))
    w, h = cols * SW, len(rows_spec) * SH + 4
    return f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMin slice" width="100%" height="100%" style="display:block;background:{shade(rows_spec[0][0], .8)}">{"".join(out)}</svg>'


rows = []
rows += [(BERRY, None, None)] * 3
rows += [(INK, None, None)] * 1
rows += [(CREAM, BERRY, i) for i in range(7)]
rows += [(INK, None, None)] * 1
rows += [(TEAL, None, None)] * 4
rows += [(GOLD, None, None)] * 2
rows += [(TEAL, None, None)] * 4
rows += [(INK, None, None)] * 1
rows += [(CREAM, TEAL, i) for i in range(7)]
rows += [(INK, None, None)] * 1
rows += [(BERRY, None, None)] * 6
FAB = fabric(130, rows)


def ball(c, size):
    strands = "".join(
        f'<ellipse cx="50" cy="50" rx="{46 - k * 2}" ry="{14 + k * 4}" transform="rotate({k * 23} 50 50)" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="2"/>'
        for k in range(9))
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><defs><clipPath id="cb"><circle cx="50" cy="50" r="46"/></clipPath>'
            f'<radialGradient id="gb" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="{shade(c, 1.18)}"/><stop offset="1" stop-color="{shade(c, .82)}"/></radialGradient></defs>'
            f'<circle cx="50" cy="50" r="46" fill="url(#gb)"/><g clip-path="url(#cb)">{strands}</g></svg>')


NEEDLES = ('<svg width="230" height="230" viewBox="0 0 100 100" style="position:absolute;left:1.35in;bottom:3.75in;transform:rotate(-4deg)">'
           f'<line x1="8" y1="92" x2="88" y2="10" stroke="#c9a46b" stroke-width="3.2" stroke-linecap="round"/><circle cx="7" cy="93" r="4.5" fill="{INK}"/>'
           f'<line x1="22" y1="96" x2="96" y2="22" stroke="#d8b77f" stroke-width="3.2" stroke-linecap="round"/><circle cx="21" cy="97" r="4.5" fill="{INK}"/></svg>')

COVER_CSS = f"""
.wrap {{ background: {CREAM}; color: {INK}; font-family: Poppins, sans-serif; }}
.knit {{ position:absolute; left:0; right:0; bottom:0; height: 3.55in; overflow:hidden; box-shadow: 0 -2px 0 rgba(0,0,0,.08) inset; }}
.knit::before {{ content:""; position:absolute; left:0; right:0; top:0; height:10px; background: linear-gradient(rgba(0,0,0,.18), transparent); z-index:2; }}
.front, .back {{ position:relative; z-index:1; display:flex; flex-direction:column; }}
.eyebrow {{ font-size: 12pt; color: {TEAL}; font-weight: 600; margin-top: .55in; }}
.t {{ font-family: Lora, serif; font-weight: 700; font-size: 60pt; line-height: .95; margin-top: 10pt; letter-spacing: -.01em; }}
.t em {{ font-style: italic; color: {BERRY}; }}
.s {{ font-size: 14pt; margin-top: 16pt; max-width: 5.4in; line-height: 1.45; }}
.badge {{ position:absolute; right: 1.0in; top: 5.05in; width: 1.55in; height: 1.55in; border-radius: 50%; background: {GOLD}; color: {INK};
          display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; transform: rotate(-8deg);
          box-shadow: 0 6px 14px rgba(31,42,68,.18); }}
.badge b {{ font-family: Lora, serif; font-size: 34pt; line-height: 1; }}
.badge span {{ font-size: 9.5pt; font-weight: 600; line-height: 1.2; margin-top: 3pt; }}
.ballwrap {{ position:absolute; left: .55in; bottom: 2.95in; filter: drop-shadow(0 10px 10px rgba(31,42,68,.28)); }}
.strand {{ position:absolute; left: 1.55in; bottom: 2.6in; }}
.brand {{ position:absolute; right: .625in; bottom: 3.85in; font-weight: 600; font-size: 12pt; color: {INK}; }}
.brand i {{ font-style: normal; color: {BERRY}; }}
.blurb {{ font-family: Lora, serif; font-size: 17pt; line-height: 1.3; margin-top: .5in; max-width: 6.6in; }}
.feat {{ margin-top: 14pt; display:grid; grid-template-columns: 1fr 1fr; gap: 6pt 18pt; font-size: 10.5pt; max-width: 7in; }}
.feat div {{ padding-left: 16pt; position:relative; line-height: 1.35; }}
.feat div::before {{ content:""; position:absolute; left:0; top: 4pt; width: 8pt; height: 8pt; border-radius: 50%; background: {BERRY}; }}
.fan {{ position:relative; height: 2.6in; margin-top: 22pt; }}
.fan img {{ position:absolute; width: 1.75in; border: 1px solid #d9d2c5; box-shadow: 0 8px 18px rgba(31,42,68,.22); background:#fff; }}
.spine-t {{ position:absolute; left:0; right:0; top:0; height: 7.45in; display:flex; align-items:center; justify-content:center; writing-mode: vertical-rl;
            font-family: Lora, serif; font-weight: 700; font-size: 11pt; color: {INK}; white-space: nowrap; z-index:1; }}
.small {{ position:absolute; left: .625in; bottom: 3.85in; font-size: 9pt; color: #5b6478; }}
"""

strand = (f'<svg class="strand" width="260" height="90" viewBox="0 0 260 90"><path d="M8 6 C 60 40, 110 10, 150 46 S 230 70, 255 88" '
          f'fill="none" stroke="{BERRY}" stroke-width="5" stroke-linecap="round"/></svg>')
front = ('<div class="eyebrow">For knitters and crocheters</div>'
         '<div class="t">Knit &amp;<br>Crochet<br><em>Project</em> Journal</div>'
         '<div class="s">Plan, track and remember every make: yarn, hooks, gauge, rows and notes, all in one beautiful book.</div>'
         '<div class="badge"><b>40</b><span>project<br>spreads</span></div>'
         '<div class="brand">Purl <i>&amp;</i> Paper</div>'
         f'{NEEDLES}{strand}<div class="ballwrap">{ball(BERRY, 175)}</div>')

imgs = [(22, -9, 0, 18), (23, 3, 1.55, 0), (6, 12, 3.15, 22), (13, -4, 4.75, 6)]
fan = "".join(f'<img src="{page_png(p)}" style="left:{x}in;top:{y}pt;transform:rotate({r}deg)">' for p, r, x, y in imgs)
back = ('<div class="blurb">Which hook was that? How many skeins did it take?<br>Never lose a project detail again.</div>'
        f'<div class="fan">{fan}</div>'
        '<div class="feat"><div>40 two-page project spreads with a 100-row counter</div><div>Yarn weight, needle and hook size charts</div>'
        '<div>UK and US crochet terms and abbreviations</div><div>Gauge maths and yarn substitution worksheet</div>'
        '<div>Yarn stash, needle and pattern wishlist pages</div><div>Care symbols, blocking guide and yarn amounts</div>'
        '<div>Handmade gift tracker and year in review</div><div>Graph paper and dot pages for your designs</div></div>'
        '<div class="small">8.5 x 11 in · 110 pages · Free maker tools at purlandpaperco.com</div>')
spine = '<div class="spine-t">Knit &amp; Crochet Project Journal · Purl &amp; Paper</div>'

# knitted band spans the whole wrap (back, spine, front)
import kdp as _k
_orig = _k._pdf


def _pdf_with_knit(html, *a, **kw):
    html = html.replace('<div class="wrap pg">', f'<div class="wrap pg"><div class="knit">{FAB}</div>', 1)
    return _orig(html, *a, **kw)


_k._pdf = _pdf_with_knit
print(cover(front, back, spine, COVER_CSS, TW, TH, PAGES, OUT / "project-journal-cover.pdf", preview=OUT / "cover.png"))
