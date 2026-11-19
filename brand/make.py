import asyncio, re, sys
sys.path.insert(0, '/home/claude/crafts')
from build import LOGO, GA1
from playwright.async_api import async_playwright

logo = LOGO.replace('aria-hidden="true"', 'class="logo"')
knit = GA1.replace('aria-hidden="true"', 'class="knit"')

BASE = """<style>
*{margin:0;box-sizing:border-box}
body{width:%dpx;height:%dpx;overflow:hidden;font-family:Poppins;color:#1f2a44;background:#eef2ef}
.i{font-style:normal;color:#b8326a}
</style>"""

ICON = BASE % (500, 500) + f"""
<style>
body{{background:#1f2a44;display:grid;place-items:center}}
.disc{{width:500px;height:500px;position:relative;display:grid;place-items:center}}
.ring{{position:absolute;inset:26px;border-radius:50%;border:5px dashed rgba(244,168,35,.75)}}
.logo{{width:250px;height:250px;margin-top:-40px}}
.word{{position:absolute;bottom:92px;font:700 54px Poppins;color:#fbfcfa;letter-spacing:-1.5px}}
.word .i{{color:#f4a823}}
</style>
<div class="disc"><div class="ring"></div>{logo}<div class="word">Purl <span class="i">&amp;</span> Paper</div></div>
"""

BANNER = BASE % (3360, 840) + f"""
<style>
body{{background:#eef2ef;position:relative}}
.band{{position:absolute;left:0;right:0;top:0;bottom:0;display:flex;align-items:center;padding:0 260px;gap:80px}}
.stripe{{position:absolute;left:0;right:0;height:46px;background:#b8326a}}
.stripe.t{{top:0}} .stripe.b{{bottom:0;background:#2f8f8a}}
.logo{{width:330px;height:330px;flex:none}}
h1{{font:700 190px/1 Poppins;letter-spacing:-6px}}
p{{font:400 64px/1.3 Lora;color:#4a5470;margin-top:26px}}
.knit{{position:absolute;right:220px;top:150px;width:540px;height:540px;opacity:.9;border-radius:40px;background:#fbfcfa;padding:40px;transform:rotate(4deg);box-shadow:0 30px 60px -30px rgba(31,42,68,.45)}}
.tape{{position:absolute;right:430px;top:120px;width:160px;height:52px;background:rgba(244,168,35,.8);transform:rotate(-6deg);z-index:2}}
</style>
<div class="stripe t"></div><div class="stripe b"></div>
<div class="band">{logo}<div><h1>Purl <span class="i">&amp;</span> Paper</h1>
<p>Printables and planners for knitters, crocheters and journalers</p></div></div>
<div class="tape"></div>{knit}
"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, html, w, h in [('shop-icon', ICON, 500, 500), ('shop-banner', BANNER, 3360, 840)]:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            await pg.set_content(html)
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'/home/claude/etsy/brand/{name}.png')
        await b.close()

asyncio.run(main())
