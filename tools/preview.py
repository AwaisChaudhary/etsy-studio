import json, html, pathlib, sys
B = pathlib.Path(sys.argv[1]); L = json.loads((B / "listings.json").read_text()); e = html.escape
cards = ""
for i, p in enumerate(L):
    th = "".join(f'<img src="{t}" alt="" loading="lazy">' for t in p["thumbs"][1:])
    cards += f'''<article class="prod"><div class="gal"><img class="hero" src="{p["thumbs"][0]}" alt="{e(p["name"])} listing image"><div class="more">{th}</div></div>
<div class="info"><div class="num">{i + 1:02d}</div><h2>{e(p["name"])}</h2><div class="price">${p["price"]:.2f}</div>
<p class="lbl">Etsy title</p><p class="title">{e(p["title"])}</p>
<p class="lbl">Tags</p><div class="tags">{"".join(f"<span>{e(t)}</span>" for t in p["tags"])}</div>
<p class="lbl">Files the buyer gets</p><p class="files">{" · ".join(e(f) for f in p["files"])}</p>
<details><summary>Full description</summary><pre>{e(p["description"])}</pre></details></div></article>'''
total = sum(p["price"] for p in L)
doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Etsy & Gumroad batch 1 preview</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#1f2a44;background:#f4f1ec}}
header{{background:#1f2a44;color:#fff;padding:44px 24px}} header .w,main{{max-width:1180px;margin:0 auto}}
h1{{font-size:clamp(28px,4vw,44px);margin:0 0 10px}} header p{{margin:6px 0;opacity:.88;font-size:17px;max-width:760px}}
.stats{{display:flex;gap:28px;flex-wrap:wrap;margin-top:22px}} .stats div b{{display:block;font-size:30px;color:#f4a823}} .stats div span{{font-size:14px;opacity:.8}}
.go{{margin-top:24px;background:#f4a823;color:#1f2a44;padding:16px 20px;border-radius:14px;font-weight:700;font-size:17px;max-width:760px}}
main{{padding:30px 18px 60px}} .prod{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:28px;background:#fff;border-radius:20px;padding:22px;margin-bottom:26px;box-shadow:0 12px 30px -20px rgba(0,0,0,.35)}}
.hero{{width:100%;border-radius:12px;display:block}} .more{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}} .more img{{width:100%;border-radius:8px}}
.num{{font-weight:800;color:#b8326a}} h2{{margin:4px 0 2px;font-size:26px}} .price{{font-size:24px;font-weight:800;color:#2f8f8a;margin-bottom:8px}}
.lbl{{margin:14px 0 4px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#6b7489}} .title{{margin:0;line-height:1.45}}
.tags{{display:flex;flex-wrap:wrap;gap:6px}} .tags span{{background:#eef2f0;border-radius:999px;padding:4px 10px;font-size:13px}} .files{{margin:0;font-size:14px;color:#4a5470;word-break:break-word}}
details{{margin-top:14px}} summary{{cursor:pointer;font-weight:700;color:#b8326a}} pre{{white-space:pre-wrap;font-family:inherit;font-size:14px;background:#f7f7f5;padding:14px;border-radius:10px;line-height:1.5}}
@media(max-width:800px){{.prod{{grid-template-columns:1fr}}}}
</style></head><body><header><div class="w"><h1>Etsy &amp; Gumroad: batch 1</h1>
<p>10 products ready to list: 4 business spreadsheets, a 2027 planner, 2 junk journal kits, an ephemera pack, journaling cards and a bundle. Every file was built and checked, and every spreadsheet formula tested.</p>
<div class="stats"><div><b>10</b><span>products</span></div><div><b>48</b><span>listing images</span></div><div><b>${total:.2f}</b><span>if one of each sells</span></div><div><b>$3.99–14.99</b><span>price range</span></div></div>
<div class="go">Happy with these? Reply "go" in chat and I'll list all 10 on Etsy (about $2 in listing fees) and on Gumroad.</div></div></header><main>{cards}</main></body></html>'''
(B / "preview" / "index.html").write_text(doc, encoding="utf-8"); print("ok", len(list((B / "preview" / "img").glob("*.jpg"))))
