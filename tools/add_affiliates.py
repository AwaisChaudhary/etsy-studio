#!/usr/bin/env python3
"""Adds the affiliate link system to each site build:
- AFF dict of /go/<slug> -> store URL (plain store URLs until each programme approves us; then swap in the tracked URL)
- writes a Cloudflare Pages _redirects file, keeps /go/ out of search via robots.txt
- buying placements on pages where people are choosing what to buy, each with a disclosure line."""
import pathlib, re

H = pathlib.Path("/home/claude")
ATTR = 'rel="sponsored nofollow noopener" target="_blank"'

COMMON = '''
# ---- Affiliate links. Pages link to /go/<slug>; _redirects sends it to the store.
# Until a programme approves us these are plain store URLs; when approved, replace the URL with the tracked link and rebuild.
AFF_ATTR = 'rel="sponsored nofollow noopener" target="_blank"'
AFF_NOTE = '<p class="aff-note">We may earn a commission if you buy through these links, at no extra cost to you.</p>'
def go(slug): return "/go/" + slug
def write_redirects(root):
    lines = "".join(f"/go/{k} {v} 302\\n" for k, v in AFF.items())
    (root / "_redirects").write_text(lines)
'''

AFF_CSS = """
/* ---- Affiliate placements ---- */
.aff-box { margin: 18px 0; padding: 16px 18px; border-radius: 14px; border: 1px dashed currentColor; }
.aff-box h3 { margin: 0 0 8px; }
.aff-links { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 0; padding: 0; list-style: none; }
.aff-links a { display: inline-block; padding: 8px 14px; border-radius: 999px; border: 1px solid currentColor; text-decoration: none; color: inherit; font-weight: 600; }
.aff-note { font-size: .8rem; opacity: .75; margin: 8px 0 0; }
"""


def links_html(items):
    return '<ul class="aff-links">' + "".join(f'<li><a href="/go/{s}" {ATTR}>{n}</a></li>' for s, n in items) + "</ul>"


def patch_build(path, aff_dict_src, root_var):
    b = path.read_text()
    if "AFF_ATTR" in b:
        return b, False
    b = b.replace("\ndef page(", "\n" + aff_dict_src + COMMON + "\n\ndef page(", 1)
    return b, True


def finish(path, b, root_var, robots_marker):
    # write _redirects after robots.txt is written; also keep /go/ out of search
    b = re.sub(r'(\(\w+ / "robots\.txt"\)\.write_text\(f"User-agent: \*\\nAllow: /\\n)', r'\1Disallow: /go/\\n', b, count=1)
    b = b.rstrip() + f"\nwrite_redirects({root_var})\n"
    path.write_text(b)


# ---------------- Padel Glass Box (Padel Market, Awin) ----------------
PADEL_AFF = '''AFF = {
    "padel-round-rackets": "https://padelmarket.com/en/collections/rackets-round-shape",
    "padel-teardrop-rackets": "https://padelmarket.com/en/collections/rackets-teardrop-shape",
    "padel-diamond-rackets": "https://padelmarket.com/en/collections/rackets-diamond-shape",
    "padel-rackets": "https://padelmarket.com/en/collections/rackets",
    "padel-shoes": "https://padelmarket.com/en/collections/shoes",
    "padel-balls": "https://padelmarket.com/en/collections/padel-balls",
    "padel-bags": "https://padelmarket.com/en/collections/padel-bags-1",
    "padel-overgrips": "https://padelmarket.com/en/collections/accessories-overgrips",
}'''


def padel():
    p = H / "padelglassbox/build.py"
    b, new = patch_build(p, PADEL_AFF, "ROOT")
    if not new:
        print("padel already"); return
    gear = ('<section><div class="wrap"><div class="aff-box"><h3>Shop padel gear</h3>'
            '<p>Browse rackets by shape, plus the shoes, balls and grips you need for your first match.</p>'
            + links_html([("padel-round-rackets", "Round rackets"), ("padel-teardrop-rackets", "Teardrop rackets"), ("padel-diamond-rackets", "Diamond rackets"),
                          ("padel-shoes", "Padel shoes"), ("padel-balls", "Balls"), ("padel-bags", "Bags"), ("padel-overgrips", "Overgrips")])
            + '{AFF_NOTE}</div></div></section>')
    # racket finder page: gear box after the body
    b = b.replace('page("racket-finder.html", "Padel Racket Finder: Which Racket Suits You? | Padel Glass Box",\n     "Answer 3 questions and find the padel racket shape, weight, balance, core and face that suit your level and style. Free and instant.", finder,',
                  'page("racket-finder.html", "Padel Racket Finder: Which Racket Suits You? | Padel Glass Box",\n     "Answer 3 questions and find the padel racket shape, weight, balance, core and face that suit your level and style. Free and instant.", finder + f\'\'\'' + gear + '\'\'\',', 1)
    assert "Shop padel gear" in b, "padel finder anchor"
    # beginners page: gear box too
    m = re.search(r'page\("beginners\.html", [^\n]*\n[^\n]*?, (\w+), (\w+)', b)
    if m:
        var = m.group(1)
        b = b[:m.start(1)] + var + " + f'''" + gear + "'''" + b[m.end(1):]
    finish(p, b, "ROOT", None)
    # result card in the finder (JS)
    js = H / "padelglassbox/assets/app.js"
    s = js.read_text()
    old = """'<div class="btns"><button class="btn lime sm" type="button" id="copy-fit">Copy my racket profile</button></div>';"""
    new_js = """'<div class="btns"><button class="btn lime sm" type="button" id="copy-fit">Copy my racket profile</button><a class="btn sm" href="/go/padel-' + shape + '-rackets" rel="sponsored nofollow noopener" target="_blank">Shop ' + shape + ' rackets</a></div><p class="aff-note">We may earn a commission if you buy through this link, at no extra cost to you.</p>';"""
    assert old in s, "padel js anchor"
    js.write_text(s.replace(old, new_js, 1))
    css = H / "padelglassbox/assets/style.css"
    css.write_text(css.read_text() + AFF_CSS)
    print("padel patched")


# ---------------- Purl & Paper (LoveCrafts) ----------------
PURL_AFF = '''AFF = {
    "yarn": "https://www.lovecrafts.com/en-us/collections/yarns",
    "yarn-by-weight": "https://www.lovecrafts.com/en-us/collections/yarn-by-weight",
    "crochet-hooks": "https://www.lovecrafts.com/en-us/collections/crochet-hooks",
    "knitting-needles": "https://www.lovecrafts.com/en-us/collections/knitting-needles",
    "free-patterns": "https://www.lovecrafts.com/en-us/collections/all-free-patterns",
}'''


def purl():
    p = H / "etsy-studio/site/build.py"
    b, new = patch_build(p, PURL_AFF, "ROOT")
    if not new:
        print("purl already"); return
    finish(p, b, "ROOT", None)
    b = p.read_text()
    # hook & needle sizes page: shop box appended to its body via page() call
    box = ('<section><div class="wrap"><div class="aff-box"><h3>Need hooks, needles or yarn?</h3>'
           + links_html([("crochet-hooks", "Crochet hooks"), ("knitting-needles", "Knitting needles"), ("yarn-by-weight", "Yarn by weight"), ("free-patterns", "Free patterns")])
           + '{AFF_NOTE}</div></div></section>')
    for f in ("hook-needle-sizes.html", "yarn-weights.html"):
        m = re.search(r'page\("' + re.escape(f) + r'", "[^"]*",\s*\n?\s*"[^"]*",\s*\n?\s*(\w+)', b)
        if m:
            b = b[:m.start(1)] + m.group(1) + " + f'''" + box + "'''" + b[m.end(1):]
        else:
            print("purl: no page() match for", f)
    p.write_text(b)
    js = H / "etsy-studio/site/assets/app.js"
    s = js.read_text()
    old = '''"<hr><p class=\\"sub\\">Needles: " + esc(w.needle) + "<br>Hook: " + esc(w.hook) + "</p>";'''
    new_js = '''"<hr><p class=\\"sub\\">Needles: " + esc(w.needle) + "<br>Hook: " + esc(w.hook) + "</p>" + '<p class="aff-shop"><a href="/go/yarn-by-weight" rel="sponsored nofollow noopener" target="_blank">Shop ' + esc(w.name.toLowerCase()) + ' yarn</a> · <a href="/go/crochet-hooks" rel="sponsored nofollow noopener" target="_blank">hooks</a> · <a href="/go/knitting-needles" rel="sponsored nofollow noopener" target="_blank">needles</a></p><p class="aff-note">We may earn a commission if you buy through these links, at no extra cost to you.</p>';'''
    assert old in s, "purl js anchor"
    js.write_text(s.replace(old, new_js, 1))
    css = H / "etsy-studio/site/assets/style.css"
    css.write_text(css.read_text() + AFF_CSS)
    print("purl patched")


# ---------------- DayOneDrop (Amazon search for each game) ----------------
def dayonedrop():
    p = H / "dayonedrop/build.py"
    src = '''from urllib.parse import quote_plus as _qp
AFF = {}
def amz_slug(g):
    """Registers /go/amz-<slug> -> Amazon search for the game on its first console platform."""
    plat = next((x for x in g.get("platforms") or [] if x != "PC"), "")
    AFF["amz-" + g["slug"]] = "https://www.amazon.com/s?k=" + _qp((g["title"] + " " + plat).strip()) + "&i=videogames"
    return "amz-" + g["slug"]'''
    b, new = patch_build(p, src, "ROOT")
    if not new:
        print("dod already"); return
    old = '''    acts += f'<button class="btn line sm star" type="button" data-slug="{g["slug"]}"'''
    assert old in b, "dod acts anchor"
    b = b.replace(old, '''    acts += f'<a class="btn sm" href="{go(amz_slug(g))}" {AFF_ATTR}>Pre-order on Amazon</a>'
''' + old, 1)
    old2 = "{cd}<div class=\"acts\">{acts}</div></div>"
    assert old2 in b, "dod ticket anchor"
    b = b.replace(old2, "{cd}<div class=\"acts\">{acts}</div>{AFF_NOTE}</div>", 1)
    finish(p, b, "ROOT", None)
    css = H / "dayonedrop/assets/style.css"
    css.write_text(css.read_text() + AFF_CSS)
    print("dod patched")


# ---------------- NeonCoast (Amazon: GTA 6 + controllers) ----------------
NC_AFF = '''AFF = {
    "gta6-ps5": "https://www.amazon.com/s?k=Grand+Theft+Auto+VI+PS5&i=videogames",
    "gta6-xbox": "https://www.amazon.com/s?k=Grand+Theft+Auto+VI+Xbox+Series+X&i=videogames",
    "ps5-controller": "https://www.amazon.com/s?k=DualSense+wireless+controller&i=videogames",
    "xbox-controller": "https://www.amazon.com/s?k=Xbox+wireless+controller&i=videogames",
    "gaming-headset": "https://www.amazon.com/s?k=gaming+headset+PS5+Xbox&i=videogames",
}'''


def neoncoast():
    p = H / "repo/build.py"
    b, new = patch_build(p, NC_AFF, "OUT")
    if not new:
        print("nc already"); return
    box = ('<section><div class="wrap"><div class="card aff-box"><h2>Get GTA 6 and the gear</h2>'
           '<p class="muted" style="margin:0">Still need the game, a spare controller or a headset for Online?</p>'
           + links_html([("gta6-ps5", "GTA 6 for PS5"), ("gta6-xbox", "GTA 6 for Xbox"), ("ps5-controller", "PS5 controller"), ("xbox-controller", "Xbox controller"), ("gaming-headset", "Gaming headsets")])
           + '{AFF_NOTE}</div></div></section>')
    m = re.search(r'page\("index\.html", "[^"]*",\s*\n?\s*"[^"]*",\s*"[^"]*",\s*(home_body)', b)
    assert m, "nc index anchor"
    b = b[:m.start(1)] + "home_body + f'''" + box + "'''" + b[m.end(1):]
    finish(p, b, "OUT", None)
    css = H / "repo/assets/style.css"
    css.write_text(css.read_text() + AFF_CSS)
    print("nc patched")


if __name__ == "__main__":
    padel(); purl(); dayonedrop(); neoncoast()
