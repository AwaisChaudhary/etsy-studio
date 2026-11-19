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
