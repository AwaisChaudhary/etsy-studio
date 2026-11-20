"""Winter Woodland printable wall art, set of 3 (batch 3). Original flat mid-century style vector art drawn here as SVG.
Each design is laid out for the canvas width so every print ratio is composed properly (not just cropped).

Usage: python3 b3_wallart.py <out_dir>   -> <out>/<ratio>/<n>-<name>.jpg + previews <out>/preview/<n>.png (2:3, 1000x1500)
"""
import math, pathlib, random, sys
from playwright.sync_api import sync_playwright

NAVY, NIGHT, TEAL, SAGE, CREAM, SNOW, ROSE, GOLD, PINE, PINE2, BERRY, BARK = (
    "#1f2a44", "#27365a", "#3f6f73", "#8fb3a6", "#f3ead8", "#fbf7ef", "#c98b86", "#e2b04a", "#2f5d50", "#24493f", "#b23a3a", "#6b4a35")
H = 3000
# ratio name -> (canvas width at H=3000, export px w, h)
RATIOS = {"2x3": (2000, 4800, 7200), "3x4": (2250, 5400, 7200), "4x5": (2400, 4800, 6000), "11x14": (2357, 3300, 4200),
          "5x7": (2143, 3000, 4200), "ISO-A": (2121, 4961, 7016)}


def pine(x, base, h, col, snow=True, tiers=4):
    """Stylised layered pine with optional snow caps."""
    out = f'<rect x="{x - h * .025:.0f}" y="{base - h * .1:.0f}" width="{h * .05:.0f}" height="{h * .1:.0f}" fill="{BARK}"/>'
    for i in range(tiers):
        t0 = base - h * .08 - i * h * .22
        w = h * (.34 - i * .065); top = t0 - h * .36
        out += f'<polygon points="{x - w:.0f},{t0:.0f} {x + w:.0f},{t0:.0f} {x:.0f},{top:.0f}" fill="{col}"/>'
        if snow:
            sw = w * .45; sy = top + (t0 - top) * .45
            out += (f'<path d="M{x:.0f},{top:.0f} L{x - sw:.0f},{sy:.0f} Q{x - sw * .5:.0f},{sy + h * .025:.0f} {x - sw * .15:.0f},{sy - h * .005:.0f} '
                    f'Q{x + sw * .2:.0f},{sy + h * .03:.0f} {x + sw * .55:.0f},{sy:.0f} L{x + sw:.0f},{sy:.0f} Z" fill="{SNOW}" opacity=".92"/>')
    return out


def stars(W, seed, y0, y1, n, avoid=None):
    r = random.Random(seed); out = ""
    for _ in range(n):
        x, y = r.uniform(40, W - 40), r.uniform(y0, y1)
        if avoid and (x - avoid[0]) ** 2 + (y - avoid[1]) ** 2 < avoid[2] ** 2: continue
        s = r.choice([4, 5, 6, 8, 12])
        if s >= 8:
            out += f'<path d="M{x},{y - s * 2} L{x + s * .4},{y - s * .4} L{x + s * 2},{y} L{x + s * .4},{y + s * .4} L{x},{y + s * 2} L{x - s * .4},{y + s * .4} L{x - s * 2},{y} L{x - s * .4},{y - s * .4} Z" fill="{CREAM}" opacity=".9"/>'
        else:
            out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s}" fill="{CREAM}" opacity="{r.uniform(.5, .95):.2f}"/>'
    return out


def hill(W, y, amp, col, seed, steps=8):
    r = random.Random(seed); pts = [(0, y + r.uniform(-amp, amp))]
    for i in range(1, steps + 1):
        pts.append((W * i / steps, y + r.uniform(-amp, amp)))
    d = f"M0,{H} L0,{pts[0][1]:.0f} "
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d += f"C{x0 + (x1 - x0) / 2:.0f},{y0:.0f} {x0 + (x1 - x0) / 2:.0f},{y1:.0f} {x1:.0f},{y1:.0f} "
    return f'<path d="{d}L{W},{H} Z" fill="{col}"/>'


def moonlit_pines(W):
    cx = W / 2
    o = f'<rect width="{W}" height="{H}" fill="{NAVY}"/>'
    o += f'<circle cx="{cx}" cy="900" r="620" fill="{NIGHT}"/><circle cx="{cx}" cy="900" r="470" fill="#2f416a"/>'
    o += stars(W, 3, 80, 1700, 90, (cx, 900, 680))
    o += f'<circle cx="{cx}" cy="900" r="330" fill="{CREAM}"/>'
    o += "".join(f'<circle cx="{cx + dx}" cy="{900 + dy}" r="{r}" fill="#e9dcc2"/>' for dx, dy, r in [(-110, -60, 60), (90, 80, 42), (40, -150, 28), (-40, 150, 34)])
    o += hill(W, 1900, 60, "#33476f", 1) + hill(W, 2120, 50, TEAL, 2)
    r = random.Random(8)
    for i in range(int(W / 150) + 2):
        x = i * 150 + r.uniform(-30, 30); o += pine(x, 2250 + r.uniform(-30, 30), r.uniform(420, 600), "#2d5458")
    o += hill(W, 2380, 40, SAGE, 3)
    o += hill(W, 2520, 30, SNOW, 4)
    for x, h in [(cx - 720, 1150), (cx + 700, 1050), (cx - 470, 640), (cx + 450, 700)]:
        o += pine(x, 2760, h, PINE if h > 1000 else PINE2)
    # cabin
    bx = cx - 30
    o += (f'<rect x="{bx - 150}" y="2470" width="300" height="230" fill="{ROSE}"/><polygon points="{bx - 200},2480 {bx + 200},2480 {bx},2290" fill="{BARK}"/>'
          f'<path d="M{bx - 200},2480 L{bx},2290 L{bx + 200},2480 L{bx + 150},2480 L{bx},2345 L{bx - 150},2480 Z" fill="{SNOW}"/>'
          f'<rect x="{bx + 60}" y="2280" width="50" height="110" fill="{BARK}"/><rect x="{bx + 52}" y="2268" width="66" height="22" fill="{SNOW}"/>'
          f'<rect x="{bx - 110}" y="2540" width="80" height="80" fill="{GOLD}"/><path d="M{bx - 70},2540 v80 M{bx - 110},2580 h80" stroke="{BARK}" stroke-width="8"/>'
          f'<rect x="{bx + 20}" y="2540" width="80" height="160" fill="{BARK}"/>')
    o += hill(W, 2700, 25, SNOW, 5) + f'<rect y="2780" width="{W}" height="220" fill="{SNOW}"/>'
    o += "".join(f'<circle cx="{x}" cy="{y}" r="{s}" fill="{SNOW}" opacity=".85"/>' for x, y, s in
                 [(random.Random(i).uniform(0, W), random.Random(i + 99).uniform(100, 2300), random.Random(i + 7).choice([5, 7, 9])) for i in range(140)])
    return o


def mountains(W):
    cx = W / 2
    o = f'<rect width="{W}" height="{H}" fill="#eadfcc"/>'
    o += f'<circle cx="{cx + 260}" cy="1020" r="300" fill="{ROSE}"/>'
    for x, y in [(cx - 520, 640), (cx - 430, 700), (cx - 360, 620)]:
        o += f'<path d="M{x - 34},{y} q17,-20 34,0 q17,-20 34,0" fill="none" stroke="{NAVY}" stroke-width="9" stroke-linecap="round"/>'

    def mtn(px, py, w, col, cap):
        sx = w * .26; sy = py + w * .32
        return (f'<polygon points="{px - w},1900 {px},{py} {px + w},1900" fill="{col}"/>'
                f'<path d="M{px},{py} L{px - sx:.0f},{sy:.0f} L{px - sx * .45:.0f},{sy - 40:.0f} L{px - sx * .1:.0f},{sy + 20:.0f} L{px + sx * .35:.0f},{sy - 30:.0f} L{px + sx:.0f},{sy:.0f} Z" fill="{cap}"/>')
    o += mtn(cx - 560, 1000, 900, "#9fb3ad", SNOW) + mtn(cx + 520, 860, 1000, SAGE, SNOW) + mtn(cx - 40, 1150, 760, TEAL, "#e9f0ec")
    o += f'<rect y="1880" width="{W}" height="40" fill="{SNOW}"/>'
    r = random.Random(4)
    for i in range(int(W / 95) + 2):
        x = i * 95 + r.uniform(-20, 20); o += pine(x, 1960 + r.uniform(-15, 15), r.uniform(260, 380), PINE2, True, 3)
    # lake with reflection stripes
    o += f'<rect y="1960" width="{W}" height="520" fill="#9fc0c0"/>'
    for i in range(14):
        y = 2000 + i * 34; w = W * (.25 + random.Random(i).random() * .5); x = random.Random(i + 40).uniform(0, W - w)
        o += f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="8" rx="4" fill="{SNOW}" opacity=".55"/>'
    o += f'<ellipse cx="{cx + 260}" cy="2060" rx="240" ry="26" fill="{ROSE}" opacity=".55"/>'
    o += hill(W, 2480, 20, SNOW, 9, 5) + f'<rect y="2560" width="{W}" height="440" fill="{SNOW}"/>'
    for x, h in [(cx - 760, 720), (cx + 720, 780), (cx - 540, 520), (cx + 520, 560)]:
        o += pine(x, 2780, h, PINE)
    return o


def berries(W):
    cx = W / 2
    o = f'<rect width="{W}" height="{H}" fill="{CREAM}"/>'
    o += f'<rect x="{cx - 760}" y="260" width="1520" height="2480" rx="760" fill="#e6dcc6"/>'
    r = random.Random(12)
    o += "".join(f'<circle cx="{r.uniform(cx - 700, cx + 700):.0f}" cy="{r.uniform(380, 2600):.0f}" r="{r.choice([6, 8, 10])}" fill="{SNOW}"/>' for _ in range(90))

    def branch(x0, y0, x1, y1, w):
        return f'<path d="M{x0},{y0} Q{(x0 + x1) / 2 + 60},{(y0 + y1) / 2} {x1},{y1}" stroke="{BARK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'

    def needles(x, y, ang, n, L, col):
        out = ""
        for k in range(n):
            t = k / (n - 1); px = x + math.cos(ang) * L * t; py = y + math.sin(ang) * L * t
            for s in (-1, 1):
                a = ang + s * math.radians(50); l = 110 * (1 - t * .5)
                out += f'<path d="M{px:.0f},{py:.0f} q{math.cos(a) * l * .5 + s * 10:.0f},{math.sin(a) * l * .5:.0f} {math.cos(a) * l:.0f},{math.sin(a) * l:.0f}" stroke="{col}" stroke-width="16" fill="none" stroke-linecap="round"/>'
        return out

    def leaf(x, y, ang, s, col):
        return (f'<g transform="translate({x},{y}) rotate({ang}) scale({s})"><path d="M0,0 C40,-50 120,-50 170,0 C120,50 40,50 0,0Z" fill="{col}"/>'
                f'<path d="M10,0 L160,0" stroke="#ffffff55" stroke-width="5"/></g>')

    def cluster(x, y, n, seed):
        rr = random.Random(seed); out = ""
        for _ in range(n):
            bx, by = x + rr.uniform(-70, 70), y + rr.uniform(-60, 60); rad = rr.uniform(26, 38)
            out += f'<path d="M{x},{y - 90} Q{(x + bx) / 2 + 10},{(y - 90 + by) / 2} {bx:.0f},{by - rad * .8:.0f}" stroke="{BARK}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            out += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{rad:.0f}" fill="{BERRY}"/><circle cx="{bx - rad * .35:.0f}" cy="{by - rad * .35:.0f}" r="{rad * .22:.0f}" fill="#ffffff" opacity=".45"/>'
        return out
    o += branch(cx + 120, 2650, cx - 40, 520, 30)
    o += branch(cx + 40, 1700, cx - 420, 1150, 18) + branch(cx + 20, 1300, cx + 430, 880, 18) + branch(cx + 80, 2100, cx + 470, 1700, 16) + branch(cx + 60, 2300, cx - 380, 2050, 14)
    o += leaf(cx - 40, 530, -95, 1.2, SAGE) + leaf(cx - 40, 560, -60, 1.0, TEAL)
    o += leaf(cx - 420, 1150, -150, 1.4, SAGE) + leaf(cx - 300, 1250, 160, 1.2, TEAL) + leaf(cx + 430, 880, -40, 1.4, SAGE) + leaf(cx + 300, 1000, 20, 1.1, TEAL)
    o += leaf(cx + 470, 1700, -20, 1.3, TEAL) + leaf(cx + 360, 1820, 30, 1.1, SAGE) + leaf(cx - 380, 2050, 200, 1.3, SAGE) + leaf(cx - 250, 2140, 150, 1.0, TEAL)
    o += leaf(cx + 6, 900, -60, 1.0, TEAL) + leaf(cx + 35, 1180, 200, 1.1, SAGE) + leaf(cx + 91, 1900, -150, 1.0, TEAL) + leaf(cx + 71, 1600, -70, .9, TEAL) + leaf(cx + 68, 1550, 30, 1.0, SAGE) + leaf(cx + 115, 2450, -30, 1.1, TEAL)
    o += cluster(cx - 330, 1330, 7, 1) + cluster(cx + 320, 1050, 6, 2) + cluster(cx + 380, 1880, 7, 3) + cluster(cx - 300, 2220, 6, 4) + cluster(cx - 60, 760, 5, 5) + cluster(cx + 100, 1420, 4, 6) + cluster(cx + 130, 2010, 5, 7)
    return o


DESIGNS = [("moonlit-pines", "Moonlit Pines", moonlit_pines), ("winter-mountains", "Winter Mountains", mountains), ("winter-berries", "Winter Berries", berries)]


def svg(fn, W): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H}" width="{W:.0f}" height="{H}">{fn(W)}</svg>'


def main(out):
    out = pathlib.Path(out); (out / "preview").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for ratio, (W, pw, ph) in RATIOS.items():
            d = out / ratio; d.mkdir(exist_ok=True)
            vw = 1000; vh = round(vw * ph / pw); scale = pw / vw
            pg = b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=scale)
            for i, (slug, name, fn) in enumerate(DESIGNS):
                html = f'<html><body style="margin:0;overflow:hidden"><div style="width:{vw}px;height:{vh}px">{svg(fn, W).replace("<svg ", "<svg preserveAspectRatio=\"xMidYMid slice\" style=\"width:100%;height:100%;display:block\" ", 1)}</div></body></html>'
                pg.set_content(html); pg.wait_for_timeout(100)
                png = d / f"{i + 1}-{slug}.png"; pg.screenshot(path=str(png))
                if ratio == "2x3":
                    from PIL import Image
                    Image.open(png).resize((1000, 1500)).save(out / "preview" / f"{i + 1}.png")
            pg.close()
            print(ratio, "done")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1])
