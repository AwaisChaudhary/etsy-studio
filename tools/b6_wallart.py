"""Mid-Century Modern abstract printable wall art, set of 6 (batch 6, lane e). Original geometric art drawn here as SVG.
Each design is composed around the canvas centre so every print ratio is laid out properly (not just cropped).

Usage: python3 b6_wallart.py <out_dir>   -> <out>/<ratio>/<n>-<name>.png + previews <out>/preview/<n>.png (2:3, 1000x1500)
"""
import math, pathlib, random, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from b3_wallart import RATIOS

H = 3000
CREAM, SAND, TERRA, RUST, MUSTARD, SAGE, OLIVE, BLUSH, CHAR, TEAL = (
    "#f2e8d8", "#e4d3b8", "#c8693f", "#9c4a2e", "#dca449", "#9fae8c", "#5f6e4c", "#e6b8a2", "#2e2a27", "#3d6b6a")


def arch(cx, by, r, w, col):
    """Thick rainbow arch band: outer radius r, band width w, standing on baseline by."""
    ri = r - w
    return (f'<path d="M{cx - r},{by} L{cx - r},{by - 0} A{r},{r} 0 0 1 {cx + r},{by} L{cx + ri},{by} A{ri},{ri} 0 0 0 {cx - ri},{by} Z" fill="{col}"/>')


def specks(W, seed, n, col, op=.18):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, H):.0f}" r="{r.choice([2, 3, 3, 4])}" fill="{col}" opacity="{op}"/>' for _ in range(n))


def d_sun_arches(W):
    cx = W / 2; by = 2050
    o = f'<rect width="{W}" height="{H}" fill="{CREAM}"/>'
    o += f'<circle cx="{cx}" cy="820" r="300" fill="{MUSTARD}"/>'
    for k, col in enumerate([TERRA, BLUSH, SAGE, RUST, SAND]):
        o += arch(cx, by, 820 - k * 150, 150, col)
    o += f'<rect x="{cx - 820}" y="{by}" width="1640" height="18" fill="{CHAR}"/>'
    o += f'<text x="{cx}" y="2420" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="70" letter-spacing="28" fill="{CHAR}">GOLDEN HOUR</text>'
    return o + specks(W, 1, 260, CHAR)


def d_bauhaus(W):
    cx = W / 2; x0 = cx - 760
    o = f'<rect width="{W}" height="{H}" fill="{CREAM}"/>'
    o += f'<rect x="{x0}" y="420" width="760" height="760" fill="{TERRA}"/><path d="M{x0},1180 A760,760 0 0 1 {x0 + 760},420 L{x0 + 760},1180 Z" fill="{MUSTARD}"/>'
    o += f'<rect x="{cx}" y="420" width="760" height="760" fill="{SAGE}"/><circle cx="{cx + 380}" cy="800" r="250" fill="{CREAM}"/>'
    o += f'<rect x="{x0}" y="1180" width="760" height="760" fill="{CHAR}"/><path d="M{x0 + 760},1180 A760,760 0 0 1 {x0},1940 L{x0 + 760},1940 Z" fill="{BLUSH}"/>'
    o += f'<rect x="{cx}" y="1180" width="760" height="380" fill="{RUST}"/><rect x="{cx}" y="1560" width="760" height="380" fill="{SAND}"/>'
    o += f'<path d="M{cx},1560 A380,380 0 0 1 {cx + 760},1560 Z" fill="{MUSTARD}"/><path d="M{cx},1560 A380,380 0 0 0 {cx + 760},1560 Z" fill="{TEAL}"/>'
    o += f'<rect x="{x0}" y="1940" width="1520" height="760" fill="{SAND}"/><circle cx="{cx - 380}" cy="2320" r="270" fill="{TERRA}"/>'
    o += f'<path d="M{cx},2700 A380,380 0 0 1 {cx + 760},2700 Z" fill="{OLIVE}"/><circle cx="{cx + 380}" cy="2120" r="90" fill="{RUST}"/>'
    return o + specks(W, 2, 260, CHAR)


def d_hills(W):
    cx = W / 2
    o = f'<rect width="{W}" height="{H}" fill="{BLUSH}"/>'
    o += f'<circle cx="{cx + 200}" cy="980" r="330" fill="{CREAM}"/>'
    o += f'<circle cx="{cx + 200}" cy="980" r="230" fill="{TERRA}"/>'
    layers = [(1500, SAND, 480, 1), (1760, TERRA, 380, 2), (2020, RUST, 420, 3), (2300, OLIVE, 330, 4), (2560, CHAR, 300, 5)]
    for y, col, amp, sd in layers:
        r = random.Random(sd); ph, ph2 = r.uniform(0, math.pi * 2), r.uniform(0, math.pi * 2); f1, f2 = r.uniform(1.2, 1.9), r.uniform(2.6, 3.6)
        pts = []
        for i in range(81):
            u = i / 80; x = -100 + (W + 200) * u
            pts.append((x, y - amp * (.55 + .32 * math.sin(ph + u * math.pi * f1) + .13 * math.sin(ph2 + u * math.pi * f2))))
        d = f"M-100,{H} L" + " L".join(f"{x:.0f},{yy:.0f}" for x, yy in pts) + f" L{W + 100},{H} Z"
        o += f'<path d="{d}" fill="{col}"/>'
    for k in range(5):
        o += f'<path d="M{cx - 640 + k * 42},{560 + k * 40} q30,-28 60,0 q30,-28 60,0" fill="none" stroke="{CHAR}" stroke-width="12" stroke-linecap="round"/>'
    return o + specks(W, 3, 200, CHAR, .12)


def d_leaves(W):
    cx = W / 2
    o = f'<rect width="{W}" height="{H}" fill="{SAND}"/>'
    o += f'<rect x="{cx - 640}" y="420" width="1280" height="2160" rx="640" fill="{CREAM}"/>'
    o += f'<path d="M{cx},2620 C{cx - 30},2000 {cx + 40},1400 {cx - 10},760" stroke="{CHAR}" stroke-width="16" fill="none" stroke-linecap="round"/>'

    def leaf(x, y, ang, s, col):
        return (f'<g transform="translate({x},{y}) rotate({ang}) scale({s})"><path d="M0,0 C60,-110 260,-120 380,0 C260,120 60,110 0,0Z" fill="{col}"/>'
                f'<path d="M30,0 L340,0" stroke="{CREAM}" stroke-width="7" opacity=".5"/></g>')
    spots = [(860, -150, 1.1, SAGE), (860, -30, 1.0, OLIVE), (1080, -160, 1.05, TERRA), (1080, -20, .95, SAGE), (1320, -150, 1.0, OLIVE),
             (1320, -30, .95, RUST), (1560, -155, .95, SAGE), (1560, -25, .9, TERRA), (1800, -150, .85, OLIVE), (1800, -30, .85, SAGE), (2040, -140, .75, MUSTARD), (2040, -40, .75, OLIVE)]
    for y, ang, s, col in spots:
        side = -1 if ang < -90 else 1
        o += leaf(cx + (-6 if side < 0 else 6), y, ang, s, col)
    o += f'<path d="M{cx - 10},760 C{cx - 60},640 {cx + 60},560 {cx + 20},470" stroke="{CHAR}" stroke-width="12" fill="none" stroke-linecap="round"/>'
    o += leaf(cx + 20, 600, -70, .7, SAGE) + leaf(cx + 10, 650, -115, .65, TERRA)
    return o + specks(W, 4, 220, CHAR, .14)


def d_arcs(W):
    cx = W / 2; s = 500; x0 = cx - 1.5 * s; y0 = 600
    cols = [[TERRA, CREAM, MUSTARD], [SAGE, RUST, CREAM], [CREAM, OLIVE, BLUSH], [MUSTARD, TERRA, SAGE]]
    o = f'<rect width="{W}" height="{H}" fill="{CREAM}"/>'
    corners = ["bl", "br", "tl", "tr"]
    for row in range(4):
        for c in range(3):
            x, y = x0 + c * s, y0 + row * s; col = cols[row][c]; corner = corners[(row + c) % 4]
            bg = CHAR if col == CREAM else CREAM
            o += f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{bg}"/>'
            ox = x if "l" in corner else x + s; oy = y + s if "b" in corner else y
            for k, rad in enumerate([s, s * .72, s * .44]):
                fill = col if k % 2 == 0 else bg
                o += f'<clipPath id="c{row}{c}{k}"><rect x="{x}" y="{y}" width="{s}" height="{s}"/></clipPath><circle cx="{ox}" cy="{oy}" r="{rad}" fill="{fill}" clip-path="url(#c{row}{c}{k})"/>'
    o += f'<text x="{cx}" y="2760" text-anchor="middle" font-family="Poppins" font-weight="600" font-size="58" letter-spacing="26" fill="{CHAR}">MID CENTURY · NO. 05</text>'
    return o + specks(W, 5, 200, CHAR, .14)


def d_pebbles(W):
    cx = W / 2
    o = f'<rect width="{W}" height="{H}" fill="{CREAM}"/>'
    blobs = [(cx - 120, 2240, 560, 300, TERRA, -4), (cx + 60, 1850, 400, 230, SAGE, 6), (cx - 60, 1520, 300, 190, CHAR, -8),
             (cx + 30, 1250, 210, 150, MUSTARD, 5), (cx - 10, 1040, 120, 100, BLUSH, -3)]
    for x, y, rx, ry, col, rot in blobs:
        o += (f'<g transform="translate({x},{y}) rotate({rot})"><path d="M{-rx},0 C{-rx},{-ry * 1.2} {rx},{-ry * 1.25} {rx},{-ry * .1} C{rx},{ry * .95} {-rx * .9},{ry * 1.05} {-rx},0 Z" fill="{col}"/></g>')
    o += f'<circle cx="{cx + 470}" cy="640" r="150" fill="{TERRA}"/><circle cx="{cx - 520}" cy="760" r="60" fill="{SAGE}"/>'
    o += f'<rect x="{cx - 700}" y="2560" width="1400" height="14" fill="{CHAR}"/>'
    return o + specks(W, 6, 220, CHAR, .14)


DESIGNS = [("golden-hour", "Golden Hour", d_sun_arches), ("bauhaus-blocks", "Bauhaus Blocks", d_bauhaus), ("terracotta-hills", "Terracotta Hills", d_hills),
           ("sage-botanical", "Sage Botanical", d_leaves), ("quarter-arcs", "Quarter Arcs", d_arcs), ("balanced-stones", "Balanced Stones", d_pebbles)]


def svg(fn, W): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H}" width="{W:.0f}" height="{H}">{fn(W)}</svg>'


def main(out, only_preview=False):
    from PIL import Image
    out = pathlib.Path(out); (out / "preview").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for ratio, (W, pw, ph) in RATIOS.items():
            if only_preview and ratio != "2x3": continue
            d = out / ratio; d.mkdir(exist_ok=True)
            vw = 1000; vh = round(vw * ph / pw); scale = pw / vw
            pg = b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=(1.5 if only_preview else scale))
            for i, (slug, name, fn) in enumerate(DESIGNS):
                html = (f'<html>'
                        f'<body style="margin:0;overflow:hidden"><div style="width:{vw}px;height:{vh}px">'
                        f'{svg(fn, W).replace("<svg ", "<svg preserveAspectRatio=\"xMidYMid slice\" style=\"width:100%;height:100%;display:block\" ", 1)}</div></body></html>')
                pg.set_content(html); pg.wait_for_timeout(150)
                png = d / f"{i + 1}-{slug}.png"; pg.screenshot(path=str(png))
                if ratio == "2x3":
                    Image.open(png).resize((1000, 1500), Image.LANCZOS).save(out / "preview" / f"{i + 1}.png")
            pg.close(); print(ratio, "done")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1], "--preview" in sys.argv)
