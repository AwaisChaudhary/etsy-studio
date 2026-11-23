"""Listing images for the Mid-Century Modern wall art set of 6 (batch 6): framed prints on a styled wall drawn in CSS.

Usage: python3 b3_wallscenes.py <wallart_dir> <scenes_out> <images_out>
wallart_dir/preview/{1,2,3}.png come from b3_wallart.py. Writes scenes (pin-a, pin-b, etsy-hero, gumroad-cover, gumroad-thumb)
and listing images (2-sizes, 3-detail, 4-detail, 5-how-it-works) for slug winter-woodland-wall-art-set.
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

SRC, SC, IM = map(pathlib.Path, sys.argv[1:4])
SLUG = "mid-century-modern-wall-art-set-of-6"
ART = [base64.b64encode((SRC / "preview" / f"{i}.png").read_bytes()).decode() for i in range(1, 7)]
NAMES = ["Golden Hour", "Bauhaus Blocks", "Terracotta Hills", "Sage Botanical", "Quarter Arcs", "Balanced Stones"]

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:var(--W);height:var(--H);overflow:hidden;position:relative;font-family:Poppins,sans-serif;color:#2e2a27}
.wall{position:absolute;inset:0;background:
  radial-gradient(ellipse 80% 60% at 30% 10%,rgba(255,250,240,.65),transparent 70%),
  linear-gradient(180deg,#e9e3d8,#dcd3c4)}
.wall::after{content:"";position:absolute;inset:0;opacity:.25;mix-blend-mode:multiply;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .5 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.shadowlight{position:absolute;inset:0;background:repeating-linear-gradient(115deg,transparent 0 22%,rgba(60,40,20,.07) 22% 27%);filter:blur(30px)}
.frame{position:absolute;background:#2b2622;padding:calc(var(--f)*1);box-shadow:0 2px 3px rgba(0,0,0,.35),0 30px 50px -18px rgba(0,0,0,.45)}
.frame.oak{background:linear-gradient(135deg,#c9a77c,#a9845a 60%,#c3a075)}
.mat{background:#fbf8f2;padding:calc(var(--f)*1.6);box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)}
.mat img{display:block;width:100%;box-shadow:inset 0 0 6px rgba(0,0,0,.3)}
.glass{position:absolute;inset:0;background:linear-gradient(120deg,rgba(255,255,255,.22),transparent 35%,transparent 70%,rgba(255,255,255,.08))}
.console{position:absolute;background:linear-gradient(#b48a5e,#8f6a44);box-shadow:0 30px 40px -20px rgba(0,0,0,.5)}
.console::after{content:"";position:absolute;left:0;right:0;bottom:-6%;height:8%;background:#7a5636}
.floor{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(#cdbfa9,#bfae95)}
.label{position:absolute;background:#fbf7ef;padding:calc(var(--u)*3.2) calc(var(--u)*3.6);box-shadow:0 2px 2px rgba(0,0,0,.15),0 24px 40px -18px rgba(0,0,0,.4)}
.label .k{font:600 calc(var(--u)*2.4) Poppins;color:#c8693f}
.label h1{font:italic 600 calc(var(--u)*var(--ts))/1 Lora,serif;margin:calc(var(--u)*1) 0 calc(var(--u)*1.2)}
.label p{font:calc(var(--u)*2.3)/1.35 Poppins;color:#4a5470}
.chips{display:flex;flex-wrap:wrap;gap:calc(var(--u)*.9);margin-top:calc(var(--u)*1.6)}
.chips span{font:600 calc(var(--u)*2) Poppins;padding:calc(var(--u)*.5) calc(var(--u)*1.4);border-radius:99px;background:#2e2a27;color:#fff}
.chips span:nth-child(even){background:transparent;color:#2e2a27;box-shadow:inset 0 0 0 2px #2e2a27}
.brand{position:absolute;font:700 calc(var(--u)*2.5) Poppins;color:#fbf7ef;background:#2e2a27;padding:calc(var(--u)*.8) calc(var(--u)*2);border-radius:99px}
.brand i{font-style:normal;color:#dca449}
.vase{position:absolute}
.cap{font:700 64px Poppins;text-align:center}
"""


def frame(i, x, y, w, oak=False, f=None):
    f = f or w * .035
    return (f'<div class="frame{" oak" if oak else ""}" style="left:{x}px;top:{y}px;width:{w}px;--f:{f:.1f}px"><div class="mat"><img src="data:image/png;base64,{ART[i]}"></div><div class="glass"></div></div>')


def vase(x, y, s):
    """Ceramic vase with pine sprigs, drawn in SVG."""
    sprig = ""
    for ang, ln in [(-30, 260), (-8, 320), (14, 290), (34, 230)]:
        sprig += f'<g transform="translate(150,190) rotate({ang})"><line x1="0" y1="0" x2="0" y2="{-ln}" stroke="#5a3e2b" stroke-width="5"/>'
        for k in range(12):
            yy = -30 - k * (ln - 40) / 12
            sprig += f'<line x1="0" y1="{yy:.0f}" x2="-26" y2="{yy - 22:.0f}" stroke="#2f5d50" stroke-width="5" stroke-linecap="round"/><line x1="0" y1="{yy:.0f}" x2="26" y2="{yy - 22:.0f}" stroke="#24493f" stroke-width="5" stroke-linecap="round"/>'
        sprig += "</g>"
    return (f'<svg class="vase" style="left:{x}px;top:{y}px;width:{300 * s}px" viewBox="0 -170 300 560">{sprig}'
            f'<path d="M105,180 C60,240 60,330 110,380 L190,380 C240,330 240,240 195,180 Z" fill="#f3ead8"/><path d="M105,180 C60,240 60,330 110,380 L130,380 C95,330 90,250 125,180Z" fill="#000" opacity=".06"/>'
            f'<ellipse cx="150" cy="180" rx="46" ry="10" fill="#e3d8c3"/></svg>')




def plant(x, y, s):
    """Terracotta bud vase with dried grass stems and seed heads, drawn in SVG (viewBox 300 x 560, base at y 550)."""
    st = ""
    for ang, ln, col in [(-26, 300, "#b89a6a"), (-10, 360, "#9c7f55"), (6, 330, "#b89a6a"), (20, 280, "#8a6f48"), (32, 240, "#b89a6a")]:
        st += f'<g transform="translate(150,200) rotate({ang})"><path d="M0,0 Q{ang * .6:.0f},{-ln / 2:.0f} 0,{-ln}" stroke="{col}" stroke-width="4" fill="none"/>'
        for k in range(9):
            yy = -ln + 10 + k * 14; w = 10 - k * .5
            st += f'<ellipse cx="{-w:.0f}" cy="{yy}" rx="{w:.0f}" ry="5" fill="{col}" transform="rotate(-25 {-w:.0f} {yy})"/><ellipse cx="{w:.0f}" cy="{yy + 6}" rx="{w:.0f}" ry="5" fill="{col}" transform="rotate(25 {w:.0f} {yy + 6})"/>'
        st += "</g>"
    return (f'<svg class="vase" style="left:{x}px;top:{y}px;width:{300 * s}px" viewBox="0 -170 300 560">{st}'
            f'<path d="M128,200 L172,200 L172,230 C230,260 236,350 200,385 L100,385 C64,350 70,260 128,230 Z" fill="#c8693f"/>'
            f'<path d="M128,230 C70,260 64,350 100,385 L122,385 C96,350 96,270 140,232 Z" fill="#000" opacity=".1"/><ellipse cx="150" cy="200" rx="22" ry="6" fill="#9c4a2e"/></svg>')


def label(x, y, w, ts, chips=True, rot=-1.2):
    ch = '<div class="chips"><span>Set of 6</span><span>6 print ratios</span><span>300 dpi</span><span>Up to 24x36</span></div>' if chips else ""
    return (f'<div class="label" style="left:{x}px;top:{y}px;width:{w}px;--ts:{ts};transform:rotate({rot}deg)"><div class="k">Printable wall art · set of 6</div>'
            f'<h1>Mid-Century Modern</h1><p>Abstract prints in terracotta, mustard &amp; sage</p>{ch}</div>')


def page(W, H, body):
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>:root{{--W:{W}px;--H:{H}px;--u:{min(W, H) / 100}px}}{CSS}'
            f'.wall{{background:radial-gradient(ellipse 80% 60% at 30% 10%,rgba(255,250,240,.6),transparent 70%),linear-gradient(180deg,#ece4d6,#e0d5c3)}}</style></head>'
            f'<body><div class="wall"></div><div class="shadowlight"></div>{body}</body></html>')


def grid(x0, y0, fw, gap, cols=3, order=range(6), oak=False):
    fh = (fw - fw * .035 * 2 - fw * .035 * 3.2) * 1.5 + fw * .035 * 5.2
    return "".join(frame(i, x0 + (k % cols) * (fw + gap), y0 + (k // cols) * (fh + gap), fw, oak) for k, i in enumerate(order))


def console(x, y, w, h): return f'<div class="console" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'


def brand(x, y): return f'<div class="brand" style="left:{x}px;top:{y}px">Purl <i>&amp;</i> Paper</div>'


def scenes():
    out = {}
    body = (grid(500, 50, 300, 50) + console(440, 1000, 1120, 56) + plant(1500, 1000 - 330, .6) + '<div class="floor" style="height:300px"></div>'
            + label(250, 1120, 1020, 4.6, False, -1) + brand(1400, 1440))
    out["etsy-hero"] = (2000, 1600, body)
    body = label(70, 60, 860, 8.6) + grid(95, 520, 250, 30) + console(120, 1290, 760, 40) + brand(70, 1410)
    out["pin-a"] = (1000, 1500, body)
    body = (frame(0, 70, 60, 470, True) + frame(2, 600, 60, 330, True) + frame(4, 600, 560, 330, True)
            + label(60, 1080, 880, 7.8, True, 1) + brand(70, 1420))
    out["pin-b"] = (1000, 1500, body)
    body = grid(650, 70, 150, 24) + label(40, 150, 470, 6.6, True) + brand(40, 620)
    out["gumroad-cover"] = (1280, 720, body)
    body = (grid(89, 50, 130, 16, 3, [0, 2, 4]) + '<div class="label" style="left:40px;top:345px;width:520px;padding:20px 26px;transform:rotate(-1.5deg)">'
            '<h1 style="font:italic 600 44px/1 Lora,serif">Mid-Century Modern</h1><p style="font:19px Poppins;color:#4a5470;margin-top:8px">Printable wall art · set of 6</p></div>')
    out["gumroad-thumb"] = (600, 600, body)
    return out


def listing_images():
    out = {}
    rat = [("2:3", "4x6 · 8x12 · 12x18 · 16x24 · 20x30 · 24x36", 2 / 3), ("3:4", "6x8 · 9x12 · 12x16 · 18x24", 3 / 4), ("4:5", "8x10 · 16x20", 4 / 5),
           ("11x14", "11x14 in", 11 / 14), ("5x7", "5x7 · 10x14", 5 / 7), ("ISO", "A5 · A4 · A3 · A2 · A1", 1 / 1.414)]
    cards = ""
    for i, (r, s, a) in enumerate(rat):
        h = 360; w = h * a
        cards += (f'<div style="display:flex;flex-direction:column;align-items:center;gap:20px"><div style="height:380px;display:flex;align-items:flex-end">'
                  f'<div style="width:{w:.0f}px;height:{h}px;background:url(data:image/png;base64,{ART[i]}) center/cover;box-shadow:0 0 0 14px #fff,0 20px 40px -14px rgba(0,0,0,.4)"></div></div>'
                  f'<div style="font:700 44px Poppins;margin-top:16px">{r}</div><div style="font:26px Poppins;color:#4a5470;text-align:center;max-width:300px">{s}</div></div>')
    out["2-sizes"] = (2000, 1600, f'<div class="cap" style="position:absolute;top:110px;left:0;right:0">6 ratios for standard frames</div>'
                                  f'<div style="position:absolute;left:100px;right:100px;top:330px;display:grid;grid-template-columns:repeat(3,1fr);gap:80px 40px">{cards}</div>')
    six = "".join(f'<div style="display:flex;flex-direction:column;align-items:center"><div style="width:400px;height:600px;background:url(data:image/png;base64,{ART[i]}) center/cover;'
                  f'box-shadow:0 0 0 12px #fff,0 24px 40px -16px rgba(0,0,0,.4)"></div><div style="font:600 38px Poppins;margin-top:30px">{NAMES[i]}</div></div>' for i in range(6))
    out["3-detail"] = (2000, 1600, f'<div class="cap" style="position:absolute;top:60px;left:0;right:0">All 6 prints in every size</div>'
                                   f'<div style="position:absolute;left:0;right:0;top:180px;transform:scale(.84);transform-origin:top center;display:grid;grid-template-columns:repeat(3,400px);justify-content:center;gap:70px 110px">{six}</div>')
    out["4-detail"] = (2000, 1600, frame(4, 1050, 120, 760, True) + f'<div style="position:absolute;left:150px;top:520px;width:780px"><div class="cap" style="text-align:left">Warm, earthy &amp; easy to style</div>'
                       f'<p style="font:36px/1.45 Poppins;color:#4a5470;margin-top:24px">Terracotta, mustard, sage and charcoal on warm cream. Hang all six as a gallery wall, or pick a pair for a hallway, bedroom or office.</p></div>')
    steps = [("1", "Download", "Get 5 ZIP files instantly: all 6 prints in 6 ratios."), ("2", "Print", "At home, at a print shop or with an online photo lab."), ("3", "Frame", "Pick the ratio that matches your frame and hang.")]
    st = "".join(f'<div style="background:#fbf7ef;padding:60px 50px;box-shadow:0 20px 40px -20px rgba(0,0,0,.35)"><div style="font:700 90px Lora;color:#c8693f">{a}</div><div style="font:700 50px Poppins;margin:10px 0 16px">{b}</div><div style="font:32px/1.4 Poppins;color:#4a5470">{c}</div></div>' for a, b, c in steps)
    out["5-how-it-works"] = (2000, 1600, f'<div class="cap" style="position:absolute;top:150px;left:0;right:0">How it works</div><div style="position:absolute;left:120px;right:120px;top:420px;display:grid;grid-template-columns:repeat(3,1fr);gap:50px">{st}</div>'
                                         f'<p style="position:absolute;left:0;right:0;bottom:200px;text-align:center;font:36px Poppins;color:#4a5470">Digital download · nothing is shipped · frames not included</p>')
    return out


def main():
    (SC / SLUG).mkdir(parents=True, exist_ok=True); (IM / SLUG).mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for dest, items in ((SC / SLUG, scenes()), (IM / SLUG, listing_images())):
            for name, (W, H, body) in items.items():
                pg = b.new_page(viewport={"width": W, "height": H}); f = dest / "_s.html"; f.write_text(page(W, H, body), encoding="utf-8")
                pg.goto(f.as_uri()); pg.wait_for_timeout(200); pg.screenshot(path=str(dest / f"{name}.png")); pg.close(); f.unlink()
        b.close()
    print(SLUG, "ok")


if __name__ == "__main__":
    main()
