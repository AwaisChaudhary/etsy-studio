# Purl & Paper website (purlandpaperco.com)
Source of truth: this folder (etsy-studio/site). Cloudflare Pages project "purlandpaper" (Direct Upload; custom domains purlandpaperco.com + www.purlandpaperco.com).
Build: `cd site && python3 build.py` (live, clean URLs) or `--preview` for local file links. GA4: G-CDBWSR0KT3. Search Console: URL-prefix property https://purlandpaperco.com/ verified by google7cb8a0335ce88e7c.html (never delete). Pinterest claim meta p:domain_verify is in the <head> template (keep).
Deploy (needs Chrome on Awais's computer): zip the CONTENTS of: all *.html, robots.txt, sitemap.xml, ads.txt, assets/ ; then dash.cloudflare.com -> Workers & Pages -> purlandpaper -> Create deployment -> Production -> upload the zip via the hidden "file" input -> wait for "29/29 files uploaded" style message -> Save and deploy. Check https://purlandpaperco.com/sitemap.xml afterwards.
Shop boxes: SHOP / SHOP_FOR dicts in build.py (key -> name, price, Etsy listing path, Gumroad slug); thumbnails in assets/shop/<key>.jpg (400x400 from scenes gumroad-thumb).
AdSense: script with ca-pub-1558743317014653 is in the template and ads.txt is set, but the site is NOT yet added in AdSense. Only add it (AdSense -> Sites -> Add site) after neoncoast.org or getdayonedrop.com is approved and the site has 15+ useful pages.
IndexNow key (22 Nov 2026): ALSO include 587793d06442be2254b0454e95cf84ff.txt in every deploy zip (it is a .txt in site/ like robots.txt). A Direct Upload replaces all files, so leaving it out breaks IndexNow.

25 Nov 2026: the Chrome file upload limit is 3.8 MB per file. Zip from site/ with `zip -qr -9 /home/claude/purl-deploy.zip *.html *.txt sitemap.xml _redirects assets -x assets/og/.cache.json` (the zip must be under /home/claude to be uploadable). build.py now resizes OG images to 960x504 q50 after each build (zip ~3.3 MB on 25 Nov with 56 pages). If it nears 3.8 MB again, move to Git-connected Pages deploys.


## RULE (26 Nov): sync before you build, push before you deploy
A run built and committed but did not push; another run then built from an older main. Every run: `git fetch origin main && git rebase FETCH_HEAD` BEFORE building, `git push origin HEAD:main` right after committing, and only deploy a zip built from the pushed main. If the rebase conflicts in generated HTML, resolve the .py sources, rebuild, and commit the rebuild.

27 Nov (evening): the deploy zip hit 4.3 MB with q26 OG. Shrinking OG to 600x315 q28 + shop thumbs to 300px in the copy got it to 3.77 MB. Next deploy will not fit: move purlandpaper to a Git-connected Pages project (or Wrangler) before the next site run.
