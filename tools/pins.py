"""Make Pinterest pins (1000x1500) for a batch.

Usage: python3 tools/pins.py batch1 /home/claude/etsy/batch1/images /home/claude/etsy/batch1/pins
Reads batchN/pins.json: {slug: {"board", "etsy", "gumroad", "designs": [{"img","head","sub","title","desc","link"}]}}
Writes <out>/<slug>-<n>.png
"""
import asyncio, base64, json, sys, pathlib
from playwright.async_api import async_playwright

CSS = """
*{margin:0;box-sizing:border-box}
body{width:1000px;height:1500px;overflow:hidden;font-family:Poppins;background:#eef2ef;color:#1f2a44;position:relative}
.top{height:580px;padding:90px 70px 0;position:relative}
.k{display:inline-block;font:600 30px Poppins;color:#fbfcfa;background:var(--acc);padding:10px 26px;border-radius:999px;margin-bottom:28px}
h1{font:700 92px/1.02 Poppins;letter-spacing:-3px}
.sub{font:400 40px/1.3 Lora;color:#4a5470;margin-top:24px}
.photo{position:absolute;left:50px;right:50px;top:600px;height:720px;border-radius:34px;overflow:hidden;background:#fff;box-shadow:0 30px 60px -30px rgba(31,42,68,.5)}
.photo img{width:100%;height:100%;object-fit:cover}
.tape{position:absolute;top:578px;left:420px;width:170px;height:50px;background:rgba(244,168,35,.85);transform:rotate(-4deg);z-index:2}
.foot{position:absolute;left:0;right:0;bottom:0;height:150px;display:flex;align-items:center;justify-content:space-between;padding:0 70px}
.brand{font:700 40px Poppins;letter-spacing:-1px}
.brand i{font-style:normal;color:#b8326a}
.dl{font:600 30px Poppins;color:#2f8f8a}
"""


def html(d, img_b64, acc):
    return f"""<html><head><style>{CSS}</style></head><body style="--acc:{acc}">
<div class="top"><span class="k">{d['kicker']}</span><h1>{d['head']}</h1><p class="sub">{d['sub']}</p></div>
<div class="tape"></div><div class="photo"><img src="data:image/png;base64,{img_b64}"></div>
<div class="foot"><span class="brand">Purl <i>&amp;</i> Paper</span><span class="dl">Instant download</span></div>
</body></html>"""


async def main(batch, imgdir, out):
    data = json.load(open(f"{batch}/pins.json"))
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    accs = ["#b8326a", "#2f8f8a", "#1f2a44"]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1000, "height": 1500})
        for slug, item in data.items():
            for n, d in enumerate(item["designs"], 1):
                img = pathlib.Path(imgdir) / slug / d["img"]
                b64 = base64.b64encode(img.read_bytes()).decode()
                await pg.set_content(html(d, b64, accs[(n - 1) % 3]))
                await pg.wait_for_timeout(150)
                await pg.screenshot(path=str(out / f"{slug}-{n}.png"), type="png")
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(*sys.argv[1:4]))
