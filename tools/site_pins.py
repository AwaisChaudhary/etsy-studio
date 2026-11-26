"""Pinterest pins (1000x1500) for Purl & Paper site pages, in the house style: title on a paper label, the tool in a card.
Usage: python3 tools/site_pins.py spec.json   spec = [{"page","kicker","title","sub","card" (HTML), "badge"}]
Writes pins/site/<page>.jpg. Own design only."""
import json, sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = """*{margin:0;box-sizing:border-box}body{width:1000px;height:1500px;overflow:hidden;font-family:Inter,system-ui,sans-serif;color:#1f2a44;
background:#e6e7e2 radial-gradient(#b9bcb3 1.2px,transparent 1.3px) 0 0/28px 28px;position:relative}
.tape{position:absolute;left:105px;top:28px;width:165px;height:78px;background:repeating-linear-gradient(-60deg,#2f8f8a 0 14px,transparent 14px 26px);z-index:2}
.label{position:absolute;left:44px;top:100px;width:990px;padding:58px 60px 70px;background:#f2eee2;transform:rotate(-1deg);box-shadow:0 6px 14px rgba(0,0,0,.12)}
.k{font:700 36px Georgia,serif;color:#2f8f8a}h1{font:700 76px/1.08 Georgia,serif;margin:14px 0 22px;color:#1f2a44;max-width:820px}.sub{font-size:34px}
.card{position:absolute;left:62px;top:var(--ct,560px);width:640px;background:#1f2a44;color:#fff;border-radius:18px;padding:34px;box-shadow:0 20px 40px -20px rgba(0,0,0,.5)}
.card h3{color:#f4a823;font-size:28px;margin-bottom:14px}.card p{font-size:24px;line-height:1.45;margin:8px 0}.card .big{font:800 72px/1 Inter,sans-serif;margin:8px 0}
.card svg{width:100%;height:auto;display:block;background:#fbf8f1;border-radius:10px;margin-top:10px}
.badge{position:absolute;right:34px;bottom:80px;width:240px;height:240px;border-radius:50%;background:#2f8f8a;border:8px solid #fff;outline:4px solid #2f8f8a;display:flex;align-items:center;justify-content:center;text-align:center;font:700 46px/1.1 Georgia,serif;color:#fff;transform:rotate(-8deg)}
.brand{position:absolute;left:70px;bottom:62px;background:#1f2a44;color:#fff;border-radius:999px;padding:16px 34px;font:700 40px Georgia,serif}.brand i{font-style:normal;color:#e07aa3}"""
def html(d):
    return f"""<html><head><style>{CSS}</style></head><body style="--ct:{d.get('ct','560px')}"><div class="tape"></div><div class="label"><p class="k">{d['kicker']}</p><h1>{d['title']}</h1><p class="sub">{d['sub']}</p></div>
<div class="card">{d['card']}</div><div class="badge">{d.get('badge','Free<br>tool')}</div><div class="brand">Purl <i>&amp;</i> Paper</div></body></html>"""
if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); out = ROOT / "pins" / "site"; out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1000, "height": 1500})
        for d in spec:
            pg.set_content(html(d)); pg.wait_for_timeout(200)
            pg.screenshot(path=str(out / f"{d['page']}.jpg"), type="jpeg", quality=86)
            print("pin", d["page"])
        b.close()
