"""Listing images for the Winter Woodland wall art set: framed prints on a styled wall drawn in CSS.

Usage: python3 b3_wallscenes.py <wallart_dir> <scenes_out> <images_out>
wallart_dir/preview/{1,2,3}.png come from b3_wallart.py. Writes scenes (pin-a, pin-b, etsy-hero, gumroad-cover, gumroad-thumb)
and listing images (2-sizes, 3-detail, 4-detail, 5-how-it-works) for slug winter-woodland-wall-art-set.
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

SRC, SC, IM = map(pathlib.Path, sys.argv[1:4])
SLUG = "winter-woodland-wall-art-set"
ART = [base64.b64encode((SRC / "preview" / f"{i}.png").read_bytes()).decode() for i in (1, 2, 3)]
NAMES = ["Moonlit Pines", "Winter Mountains", "Winter Berries"]

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:var(--W);height:var(--H);overflow:hidden;position:relative;font-family:Poppins,sans-serif;color:#1f2a44}
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
.label .k{font:600 calc(var(--u)*2.4) Poppins;color:#3f6f73}
.label h1{font:italic 600 calc(var(--u)*var(--ts))/1 Lora,serif;margin:calc(var(--u)*1) 0 calc(var(--u)*1.2)}
.label p{font:calc(var(--u)*2.3)/1.35 Poppins;color:#4a5470}
.chips{display:flex;flex-wrap:wrap;gap:calc(var(--u)*.9);margin-top:calc(var(--u)*1.6)}
.chips span{font:600 calc(var(--u)*2) Poppins;padding:calc(var(--u)*.5) calc(var(--u)*1.4);border-radius:99px;background:#1f2a44;color:#fff}
.chips span:nth-child(even){background:transparent;color:#1f2a44;box-shadow:inset 0 0 0 2px #1f2a44}
.brand{position:absolute;font:700 calc(var(--u)*2.5) Poppins;color:#fbf7ef;background:#1f2a44;padding:calc(var(--u)*.8) calc(var(--u)*2);border-radius:99px}
.brand i{font-style:normal;color:#e2b04a}
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


def label(x, y, w, ts, chips=True):
    ch = '<div class="chips"><span>Set of 3</span><span>6 print ratios</span><span>300 dpi</span><span>Up to 24x36</span></div>' if chips else ""
    return (f'<div class="label" style="left:{x}px;top:{y}px;width:{w}px;--ts:{ts};transform:rotate(-1.2deg)"><div class="k">Printable wall art · set of 3</div>'
            f'<h1>Winter Woodland</h1><p>Moonlit Pines, Winter Mountains &amp; Winter Berries</p>{ch}</div>')


def page(W, H, body):
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>:root{{--W:{W}px;--H:{H}px;--u:{min(W, H) / 100}px}}{CSS}</style></head>'
            f'<body><div class="wall"></div><div class="shadowlight"></div>{body}</body></html>')


def trio(cx, top, fw, gap, oak=False):
    x0 = cx - (3 * fw + 2 * gap) / 2
    return "".join(frame(i, x0 + i * (fw + gap), top + (0 if i != 1 else 0), fw, oak) for i in range(3))


def scenes():
    out = {}
    # Etsy hero 2000x1600: three frames over a console, label kept inside the centre square
    fw = 400
    body = (trio(1000, 150, fw, 70) + f'<div class="console" style="left:520px;top:1000px;width:960px;height:56px"></div>'
            + vase(1290, 670, .6) + f'<div class="floor" style="height:300px"></div>'
            + label(230, 1235, 820, 5.2, False).replace("rotate(-1.2deg)", "rotate(-1deg)")
            + '<div class="brand" style="left:1340px;top:1420px">Purl <i>&amp;</i> Paper</div>')
    out["etsy-hero"] = (2000, 1600, body)
    # Pin A 1000x1500: frames stacked as a gallery wall
    body = (label(70, 70, 860, 9) + trio(500, 560, 270, 30)
            + f'<div class="console" style="left:150px;top:1240px;width:700px;height:40px"></div>' + vase(420, 1240 - 330, .6)
            + '<div class="brand" style="left:70px;top:1400px">Purl <i>&amp;</i> Paper</div>')
    out["pin-a"] = (1000, 1500, body)
    # Pin B: big single frame + two small, label bottom
    body = (frame(0, 120, 60, 340, True) + frame(1, 540, 60, 340, True) + frame(2, 330, 580, 340, True)
            + label(60, 1100, 880, 8.4).replace("rotate(-1.2deg)", "rotate(1deg)") + '<div class="brand" style="left:70px;top:1410px">Purl <i>&amp;</i> Paper</div>')
    out["pin-b"] = (1000, 1500, body)
    # Gumroad cover 1280x720
    body = trio(820, 90, 220, 36) + label(40, 120, 440, 7.2, True) + '<div class="brand" style="left:40px;top:620px">Purl <i>&amp;</i> Paper</div>'
    out["gumroad-cover"] = (1280, 720, body)
    body = trio(300, 60, 160, 22) + '<div class="label" style="left:40px;top:420px;width:520px;padding:18px 26px;transform:rotate(-1.5deg)"><h1 style="font:italic 600 46px/1 Lora,serif">Winter Woodland</h1><p style="font:18px Poppins;color:#4a5470;margin-top:6px">Printable wall art · set of 3</p></div>'
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
                  f'<div style="width:{w:.0f}px;height:{h}px;background:url(data:image/png;base64,{ART[i % 3]}) center/cover;box-shadow:0 0 0 14px #fff,0 20px 40px -14px rgba(0,0,0,.4)"></div></div>'
                  f'<div style="font:700 44px Poppins;margin-top:16px">{r}</div><div style="font:26px Poppins;color:#4a5470;text-align:center;max-width:300px">{s}</div></div>')
    out["2-sizes"] = (2000, 1600, f'<div class="cap" style="position:absolute;top:110px;left:0;right:0">6 ratios for standard frames</div>'
                                  f'<div style="position:absolute;left:100px;right:100px;top:330px;display:grid;grid-template-columns:repeat(3,1fr);gap:80px 40px">{cards}</div>')
    for k, idx in ((3, 0), (4, 2)):
        out[f"{k}-detail"] = (2000, 1600, frame(idx, 1050, 120, 760, True) + f'<div style="position:absolute;left:150px;top:560px;width:780px"><div class="cap" style="text-align:left">{NAMES[idx]}</div>'
                                           f'<p style="font:36px/1.45 Poppins;color:#4a5470;margin-top:24px">{["A glowing moon over snowy pines and a little pink cabin.", "", "A minimal botanical branch with winter berries on warm cream."][idx]}</p></div>')
    steps = [("1", "Download", "Get 5 ZIP files instantly: every print in 6 ratios."), ("2", "Print", "At home, at a print shop or with an online photo lab."), ("3", "Frame", "Pick the ratio that matches your frame and hang.")]
    st = "".join(f'<div style="background:#fbf7ef;padding:60px 50px;box-shadow:0 20px 40px -20px rgba(0,0,0,.35)"><div style="font:700 90px Lora;color:#3f6f73">{a}</div><div style="font:700 50px Poppins;margin:10px 0 16px">{b}</div><div style="font:32px/1.4 Poppins;color:#4a5470">{c}</div></div>' for a, b, c in steps)
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
