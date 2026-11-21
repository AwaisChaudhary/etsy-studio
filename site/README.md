# Purl & Paper (working name)

Static site for knitting, crochet and junk journaling tools. Same setup as the other sites:

- `python3 build.py` builds the live site (clean URLs). `python3 build.py --preview` builds for local file viewing.
- Content data: `assets/data.json` (yarn weights, sizes, crochet terms, yarn amounts, journal prompts).
- Interactivity: `assets/app.js` (tools) and `assets/swatch.js` (home hero swatch). Styles: `assets/style.css`.
- Set `DOMAIN`, `SITE` and `GA_ID` at the top of build.py at launch. Never hand-edit the .html files.
- Log every content change in CONTENT-LOG.md.

## Live (20 Nov 2026)
Deployed to https://purlandpaper.pages.dev (Cloudflare Pages project "purlandpaper", Direct Upload).
Update: `python3 build.py`, zip the site files (all *.html, robots.txt, sitemap.xml, ads.txt, assets/), then Cloudflare dashboard -> Workers & Pages -> purlandpaper -> Create deployment -> upload the zip.
GitHub repo AwaisChaudhary/purlandpaper exists (empty); pushes need the Claude GitHub app to be given access to it, then switch the Pages project to Git deploys.
Domain to buy: purlandpaperco.com (available on Cloudflare Registrar, 20 Nov). After purchase: add it as a custom domain on the Pages project and set DOMAIN in build.py.

## Standing rule: ChatGPT and AI answers (added 21 Nov 2026 at Awais's request)
ChatGPT now sends about 90% of NeonCoast's visitors: it links pages that give a direct, specific, up-to-date answer plus something useful to do next. Every run on this site follows this on each new or refreshed page:
- Open with a 1-2 sentence "Quick answer" that states the specific answer (numbers, sizes, prices, steps), then the detail.
- Use question-style H2s that match how people ask, keep a visible "Last checked/updated" date, and add FAQ JSON-LD for those questions.
- Make facts easy to quote: short lists and tables, one fact per line, units included.
- Keep visitors on the site: end every page and every tool result with 2-3 links to related pages or tools ("what next").
- Keep robots.txt open to all crawlers (Bingbot, OAI-SearchBot, GPTBot included); never add blocks.
