#!/usr/bin/env python3
"""Builds the crafts site. `python3 build.py` = live (clean URLs). `python3 build.py --preview` = local files.
Change SITE / DOMAIN / GA_ID here once the domain is bought. Content data lives in assets/data.json."""
import json, html, pathlib, sys, hashlib
import pathlib as _pl, sys as _sy
_sy.path.insert(0, str(_pl.Path(__file__).resolve().parent / "tools"))
from og import og_image

ROOT = pathlib.Path(__file__).resolve().parent
DOMAIN = "https://purlandpaperco.com"
SITE = "Purl & Paper"
ADSENSE_CLIENT = "ca-pub-1558743317014653"
GA_ID = "G-CDBWSR0KT3"                # GA4 property "Purl & Paper (purlandpaperco.com)"
PREVIEW = "--preview" in sys.argv
D = json.loads((ROOT / "assets" / "data.json").read_text())
UPDATED = D["updated"]
e = html.escape


def v(n): return hashlib.md5((ROOT / "assets" / n).read_bytes()).hexdigest()[:8]
def href(p): return p if PREVIEW else ("/" if p == "index.html" else "/" + p[:-5])
def canon(p): return DOMAIN + ("/" if p == "index.html" else "/" + p[:-5])
def asset(n): return ("" if PREVIEW else "/") + "assets/" + n + "?v=" + v(n)


NAV = [("row-counter.html", "Row counter"), ("yarn-calculator.html", "Yarn calculator"), ("gauge-converter.html", "Gauge"),
       ("projects.html", "Projects"), ("journal-prompts.html", "Journal prompts")]
TOOLS_MORE = [("blanket-size-calculator.html", "Blanket size calculator"), ("crochet-knitting-gift-planner.html", "Handmade gift planner"), ("hat-size-chart.html", "Hat size calculator"), ("granny-square-blanket-calculator.html", "Granny square calculator"), ("increase-decrease-calculator.html", "Increase evenly calculator"), ("sock-size-chart.html", "Sock size calculator"), ("yarn-substitution-calculator.html", "Yarn substitution calculator"), ("cast-on-calculator.html", "Cast on calculator"), ("crochet-circle-calculator.html", "Crochet circle calculator"), ("temperature-blanket-planner.html", "Temperature blanket planner"), ("yarn-yardage-calculator.html", "Yarn yardage calculator"), ("foundation-chain-calculator.html", "Foundation chain calculator"), ("junk-journal-signature-calculator.html", "Junk journal signature calculator"), ("c2c-blanket-calculator.html", "C2C blanket calculator"), ("scarf-size-chart.html", "Scarf size chart"), ("crochet-time-estimator.html", "Crochet time calculator"), ("stripe-generator.html", "Random stripe generator"), ("sweater-size-calculator.html", "Sweater size calculator")]
GUIDES = [("crafts.html", "More crafts: calligraphy, cross stitch, quilting, candles, resin"), ("yarn-weights.html", "Yarn weight chart"), ("hook-needle-sizes.html", "Hook and needle sizes"),
          ("crochet-terms.html", "US vs UK crochet terms"), ("junk-journal-beginners.html", "Junk journaling for beginners"), ("how-to-price-crochet-items.html", "How to price crochet items"), ("how-to-tea-stain-paper.html", "How to tea stain paper"), ("knitting-abbreviations.html", "Knitting abbreviations"), ("junk-journal-ephemera-ideas.html", "Junk journal ephemera ideas"), ("craft-fair-checklist.html", "Craft fair checklist"), ("how-to-crochet-magic-ring.html", "How to crochet a magic ring"), ("how-to-change-colors-in-crochet.html", "How to change colours in crochet"), ("how-to-bind-off-knitting.html", "How to bind off knitting"), ("how-to-weave-in-ends.html", "How to weave in ends"), ("how-to-cast-on-knitting.html", "How to cast on knitting"), ("how-to-crochet-decrease.html", "How to decrease in crochet"), ("how-to-fix-a-dropped-stitch.html", "How to fix a dropped stitch"), ("how-to-price-a-crochet-blanket.html", "How to price a crochet blanket"), ("etsy-fee-calculator.html", "Etsy fee calculator"), ("how-to-knit-in-the-round.html", "How to knit in the round"), ("junk-journal-supply-checklist.html", "Junk journal supply checklist"), ("how-to-pick-up-stitches-knitting.html", "How to pick up stitches"), ("how-to-price-amigurumi.html", "How to price amigurumi"), ("basic-crochet-stitches.html", "Basic crochet stitches")]
LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="17" cy="20" r="13" fill="#b8326a"/>'
        '<path d="M6 15c7 3 15 3 22-2M5 22c8 4 17 4 24-3M9 29c6 2 13 1 18-4M12 8c-1 8 0 17 5 25M20 7c3 7 4 16 1 26" fill="none" stroke="#fbfcfa" stroke-width="1.6" stroke-linecap="round" opacity=".75"/>'
        '<path d="M29 28c4 1 7 4 8 8" fill="none" stroke="#b8326a" stroke-width="2" stroke-linecap="round"/>'
        '<rect x="25" y="2" width="13" height="10" rx="2" fill="#f4a823" transform="rotate(14 31 7)"/><circle cx="28.5" cy="5.6" r="1.3" fill="#fbfcfa"/></svg>')
GA1 = '<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M0.6 0.5L6.0 8.8L11.4 0.5M12.6 0.5L18.0 8.8L23.4 0.5M24.6 0.5L30.0 8.8L35.4 0.5M36.6 0.5L42.0 8.8L47.4 0.5M48.6 0.5L54.0 8.8L59.4 0.5M60.6 0.5L66.0 8.8L71.4 0.5M72.6 0.5L78.0 8.8L83.4 0.5M84.6 0.5L90.0 8.8L95.4 0.5M96.6 0.5L102.0 8.8L107.4 0.5M108.6 0.5L114.0 8.8L119.4 0.5M0.6 9.7L6.0 18.1L11.4 9.7M12.6 9.7L18.0 18.1L23.4 9.7M24.6 9.7L30.0 18.1L35.4 9.7M36.6 9.7L42.0 18.1L47.4 9.7M48.6 9.7L54.0 18.1L59.4 9.7M60.6 9.7L66.0 18.1L71.4 9.7M72.6 9.7L78.0 18.1L83.4 9.7M84.6 9.7L90.0 18.1L95.4 9.7M96.6 9.7L102.0 18.1L107.4 9.7M108.6 9.7L114.0 18.1L119.4 9.7M0.6 19.0L6.0 27.3L11.4 19.0M12.6 19.0L18.0 27.3L23.4 19.0M24.6 19.0L30.0 27.3L35.4 19.0M36.6 19.0L42.0 27.3L47.4 19.0M48.6 19.0L54.0 27.3L59.4 19.0M60.6 19.0L66.0 27.3L71.4 19.0M72.6 19.0L78.0 27.3L83.4 19.0M84.6 19.0L90.0 27.3L95.4 19.0M96.6 19.0L102.0 27.3L107.4 19.0M108.6 19.0L114.0 27.3L119.4 19.0M0.6 28.2L6.0 36.5L11.4 28.2M12.6 28.2L18.0 36.5L23.4 28.2M24.6 28.2L30.0 36.5L35.4 28.2M36.6 28.2L42.0 36.5L47.4 28.2M48.6 28.2L54.0 36.5L59.4 28.2M60.6 28.2L66.0 36.5L71.4 28.2M72.6 28.2L78.0 36.5L83.4 28.2M84.6 28.2L90.0 36.5L95.4 28.2M96.6 28.2L102.0 36.5L107.4 28.2M108.6 28.2L114.0 36.5L119.4 28.2M0.6 37.4L6.0 45.8L11.4 37.4M12.6 37.4L18.0 45.8L23.4 37.4M24.6 37.4L30.0 45.8L35.4 37.4M36.6 37.4L42.0 45.8L47.4 37.4M48.6 37.4L54.0 45.8L59.4 37.4M60.6 37.4L66.0 45.8L71.4 37.4M72.6 37.4L78.0 45.8L83.4 37.4M84.6 37.4L90.0 45.8L95.4 37.4M96.6 37.4L102.0 45.8L107.4 37.4M108.6 37.4L114.0 45.8L119.4 37.4M0.6 46.7L6.0 55.0L11.4 46.7M12.6 46.7L18.0 55.0L23.4 46.7M24.6 46.7L30.0 55.0L35.4 46.7M36.6 46.7L42.0 55.0L47.4 46.7M48.6 46.7L54.0 55.0L59.4 46.7M60.6 46.7L66.0 55.0L71.4 46.7M72.6 46.7L78.0 55.0L83.4 46.7M84.6 46.7L90.0 55.0L95.4 46.7M96.6 46.7L102.0 55.0L107.4 46.7M108.6 46.7L114.0 55.0L119.4 46.7M0.6 55.9L6.0 64.2L11.4 55.9M12.6 55.9L18.0 64.2L23.4 55.9M24.6 55.9L30.0 64.2L35.4 55.9M36.6 55.9L42.0 64.2L47.4 55.9M48.6 55.9L54.0 64.2L59.4 55.9M60.6 55.9L66.0 64.2L71.4 55.9M72.6 55.9L78.0 64.2L83.4 55.9M84.6 55.9L90.0 64.2L95.4 55.9M96.6 55.9L102.0 64.2L107.4 55.9M108.6 55.9L114.0 64.2L119.4 55.9M0.6 65.1L6.0 73.4L11.4 65.1M12.6 65.1L18.0 73.4L23.4 65.1M24.6 65.1L30.0 73.4L35.4 65.1M36.6 65.1L42.0 73.4L47.4 65.1M48.6 65.1L54.0 73.4L59.4 65.1M60.6 65.1L66.0 73.4L71.4 65.1M72.6 65.1L78.0 73.4L83.4 65.1M84.6 65.1L90.0 73.4L95.4 65.1M96.6 65.1L102.0 73.4L107.4 65.1M108.6 65.1L114.0 73.4L119.4 65.1M0.6 74.3L6.0 82.7L11.4 74.3M12.6 74.3L18.0 82.7L23.4 74.3M24.6 74.3L30.0 82.7L35.4 74.3M36.6 74.3L42.0 82.7L47.4 74.3M48.6 74.3L54.0 82.7L59.4 74.3M60.6 74.3L66.0 82.7L71.4 74.3M72.6 74.3L78.0 82.7L83.4 74.3M84.6 74.3L90.0 82.7L95.4 74.3M96.6 74.3L102.0 82.7L107.4 74.3M108.6 74.3L114.0 82.7L119.4 74.3M0.6 83.6L6.0 91.9L11.4 83.6M12.6 83.6L18.0 91.9L23.4 83.6M24.6 83.6L30.0 91.9L35.4 83.6M36.6 83.6L42.0 91.9L47.4 83.6M48.6 83.6L54.0 91.9L59.4 83.6M60.6 83.6L66.0 91.9L71.4 83.6M72.6 83.6L78.0 91.9L83.4 83.6M84.6 83.6L90.0 91.9L95.4 83.6M96.6 83.6L102.0 91.9L107.4 83.6M108.6 83.6L114.0 91.9L119.4 83.6M0.6 92.8L6.0 101.1L11.4 92.8M12.6 92.8L18.0 101.1L23.4 92.8M24.6 92.8L30.0 101.1L35.4 92.8M36.6 92.8L42.0 101.1L47.4 92.8M48.6 92.8L54.0 101.1L59.4 92.8M60.6 92.8L66.0 101.1L71.4 92.8M72.6 92.8L78.0 101.1L83.4 92.8M84.6 92.8L90.0 101.1L95.4 92.8M96.6 92.8L102.0 101.1L107.4 92.8M108.6 92.8L114.0 101.1L119.4 92.8M0.6 102.0L6.0 110.4L11.4 102.0M12.6 102.0L18.0 110.4L23.4 102.0M24.6 102.0L30.0 110.4L35.4 102.0M36.6 102.0L42.0 110.4L47.4 102.0M48.6 102.0L54.0 110.4L59.4 102.0M60.6 102.0L66.0 110.4L71.4 102.0M72.6 102.0L78.0 110.4L83.4 102.0M84.6 102.0L90.0 110.4L95.4 102.0M96.6 102.0L102.0 110.4L107.4 102.0M108.6 102.0L114.0 110.4L119.4 102.0M0.6 111.3L6.0 119.6L11.4 111.3M12.6 111.3L18.0 119.6L23.4 111.3M24.6 111.3L30.0 119.6L35.4 111.3M36.6 111.3L42.0 119.6L47.4 111.3M48.6 111.3L54.0 119.6L59.4 111.3M60.6 111.3L66.0 119.6L71.4 111.3M72.6 111.3L78.0 119.6L83.4 111.3M84.6 111.3L90.0 119.6L95.4 111.3M96.6 111.3L102.0 119.6L107.4 111.3M108.6 111.3L114.0 119.6L119.4 111.3" fill="none" stroke="#b8326a" stroke-width="1.4" stroke-linejoin="round"/></svg>'
GA2 = '<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M0.6 0.5L4.3 6.3L8.0 0.5M9.2 0.5L12.9 6.3L16.5 0.5M17.7 0.5L21.4 6.3L25.1 0.5M26.3 0.5L30.0 6.3L33.7 0.5M34.9 0.5L38.6 6.3L42.3 0.5M43.5 0.5L47.1 6.3L50.8 0.5M52.0 0.5L55.7 6.3L59.4 0.5M60.6 0.5L64.3 6.3L68.0 0.5M69.2 0.5L72.9 6.3L76.5 0.5M77.7 0.5L81.4 6.3L85.1 0.5M86.3 0.5L90.0 6.3L93.7 0.5M94.9 0.5L98.6 6.3L102.3 0.5M103.5 0.5L107.1 6.3L110.8 0.5M112.0 0.5L115.7 6.3L119.4 0.5M0.6 7.2L4.3 12.9L8.0 7.2M9.2 7.2L12.9 12.9L16.5 7.2M17.7 7.2L21.4 12.9L25.1 7.2M26.3 7.2L30.0 12.9L33.7 7.2M34.9 7.2L38.6 12.9L42.3 7.2M43.5 7.2L47.1 12.9L50.8 7.2M52.0 7.2L55.7 12.9L59.4 7.2M60.6 7.2L64.3 12.9L68.0 7.2M69.2 7.2L72.9 12.9L76.5 7.2M77.7 7.2L81.4 12.9L85.1 7.2M86.3 7.2L90.0 12.9L93.7 7.2M94.9 7.2L98.6 12.9L102.3 7.2M103.5 7.2L107.1 12.9L110.8 7.2M112.0 7.2L115.7 12.9L119.4 7.2M0.6 13.8L4.3 19.6L8.0 13.8M9.2 13.8L12.9 19.6L16.5 13.8M17.7 13.8L21.4 19.6L25.1 13.8M26.3 13.8L30.0 19.6L33.7 13.8M34.9 13.8L38.6 19.6L42.3 13.8M43.5 13.8L47.1 19.6L50.8 13.8M52.0 13.8L55.7 19.6L59.4 13.8M60.6 13.8L64.3 19.6L68.0 13.8M69.2 13.8L72.9 19.6L76.5 13.8M77.7 13.8L81.4 19.6L85.1 13.8M86.3 13.8L90.0 19.6L93.7 13.8M94.9 13.8L98.6 19.6L102.3 13.8M103.5 13.8L107.1 19.6L110.8 13.8M112.0 13.8L115.7 19.6L119.4 13.8M0.6 20.5L4.3 26.3L8.0 20.5M9.2 20.5L12.9 26.3L16.5 20.5M17.7 20.5L21.4 26.3L25.1 20.5M26.3 20.5L30.0 26.3L33.7 20.5M34.9 20.5L38.6 26.3L42.3 20.5M43.5 20.5L47.1 26.3L50.8 20.5M52.0 20.5L55.7 26.3L59.4 20.5M60.6 20.5L64.3 26.3L68.0 20.5M69.2 20.5L72.9 26.3L76.5 20.5M77.7 20.5L81.4 26.3L85.1 20.5M86.3 20.5L90.0 26.3L93.7 20.5M94.9 20.5L98.6 26.3L102.3 20.5M103.5 20.5L107.1 26.3L110.8 20.5M112.0 20.5L115.7 26.3L119.4 20.5M0.6 27.2L4.3 32.9L8.0 27.2M9.2 27.2L12.9 32.9L16.5 27.2M17.7 27.2L21.4 32.9L25.1 27.2M26.3 27.2L30.0 32.9L33.7 27.2M34.9 27.2L38.6 32.9L42.3 27.2M43.5 27.2L47.1 32.9L50.8 27.2M52.0 27.2L55.7 32.9L59.4 27.2M60.6 27.2L64.3 32.9L68.0 27.2M69.2 27.2L72.9 32.9L76.5 27.2M77.7 27.2L81.4 32.9L85.1 27.2M86.3 27.2L90.0 32.9L93.7 27.2M94.9 27.2L98.6 32.9L102.3 27.2M103.5 27.2L107.1 32.9L110.8 27.2M112.0 27.2L115.7 32.9L119.4 27.2M0.6 33.8L4.3 39.6L8.0 33.8M9.2 33.8L12.9 39.6L16.5 33.8M17.7 33.8L21.4 39.6L25.1 33.8M26.3 33.8L30.0 39.6L33.7 33.8M34.9 33.8L38.6 39.6L42.3 33.8M43.5 33.8L47.1 39.6L50.8 33.8M52.0 33.8L55.7 39.6L59.4 33.8M60.6 33.8L64.3 39.6L68.0 33.8M69.2 33.8L72.9 39.6L76.5 33.8M77.7 33.8L81.4 39.6L85.1 33.8M86.3 33.8L90.0 39.6L93.7 33.8M94.9 33.8L98.6 39.6L102.3 33.8M103.5 33.8L107.1 39.6L110.8 33.8M112.0 33.8L115.7 39.6L119.4 33.8M0.6 40.5L4.3 46.3L8.0 40.5M9.2 40.5L12.9 46.3L16.5 40.5M17.7 40.5L21.4 46.3L25.1 40.5M26.3 40.5L30.0 46.3L33.7 40.5M34.9 40.5L38.6 46.3L42.3 40.5M43.5 40.5L47.1 46.3L50.8 40.5M52.0 40.5L55.7 46.3L59.4 40.5M60.6 40.5L64.3 46.3L68.0 40.5M69.2 40.5L72.9 46.3L76.5 40.5M77.7 40.5L81.4 46.3L85.1 40.5M86.3 40.5L90.0 46.3L93.7 40.5M94.9 40.5L98.6 46.3L102.3 40.5M103.5 40.5L107.1 46.3L110.8 40.5M112.0 40.5L115.7 46.3L119.4 40.5M0.6 47.2L4.3 52.9L8.0 47.2M9.2 47.2L12.9 52.9L16.5 47.2M17.7 47.2L21.4 52.9L25.1 47.2M26.3 47.2L30.0 52.9L33.7 47.2M34.9 47.2L38.6 52.9L42.3 47.2M43.5 47.2L47.1 52.9L50.8 47.2M52.0 47.2L55.7 52.9L59.4 47.2M60.6 47.2L64.3 52.9L68.0 47.2M69.2 47.2L72.9 52.9L76.5 47.2M77.7 47.2L81.4 52.9L85.1 47.2M86.3 47.2L90.0 52.9L93.7 47.2M94.9 47.2L98.6 52.9L102.3 47.2M103.5 47.2L107.1 52.9L110.8 47.2M112.0 47.2L115.7 52.9L119.4 47.2M0.6 53.8L4.3 59.6L8.0 53.8M9.2 53.8L12.9 59.6L16.5 53.8M17.7 53.8L21.4 59.6L25.1 53.8M26.3 53.8L30.0 59.6L33.7 53.8M34.9 53.8L38.6 59.6L42.3 53.8M43.5 53.8L47.1 59.6L50.8 53.8M52.0 53.8L55.7 59.6L59.4 53.8M60.6 53.8L64.3 59.6L68.0 53.8M69.2 53.8L72.9 59.6L76.5 53.8M77.7 53.8L81.4 59.6L85.1 53.8M86.3 53.8L90.0 59.6L93.7 53.8M94.9 53.8L98.6 59.6L102.3 53.8M103.5 53.8L107.1 59.6L110.8 53.8M112.0 53.8L115.7 59.6L119.4 53.8M0.6 60.5L4.3 66.3L8.0 60.5M9.2 60.5L12.9 66.3L16.5 60.5M17.7 60.5L21.4 66.3L25.1 60.5M26.3 60.5L30.0 66.3L33.7 60.5M34.9 60.5L38.6 66.3L42.3 60.5M43.5 60.5L47.1 66.3L50.8 60.5M52.0 60.5L55.7 66.3L59.4 60.5M60.6 60.5L64.3 66.3L68.0 60.5M69.2 60.5L72.9 66.3L76.5 60.5M77.7 60.5L81.4 66.3L85.1 60.5M86.3 60.5L90.0 66.3L93.7 60.5M94.9 60.5L98.6 66.3L102.3 60.5M103.5 60.5L107.1 66.3L110.8 60.5M112.0 60.5L115.7 66.3L119.4 60.5M0.6 67.2L4.3 72.9L8.0 67.2M9.2 67.2L12.9 72.9L16.5 67.2M17.7 67.2L21.4 72.9L25.1 67.2M26.3 67.2L30.0 72.9L33.7 67.2M34.9 67.2L38.6 72.9L42.3 67.2M43.5 67.2L47.1 72.9L50.8 67.2M52.0 67.2L55.7 72.9L59.4 67.2M60.6 67.2L64.3 72.9L68.0 67.2M69.2 67.2L72.9 72.9L76.5 67.2M77.7 67.2L81.4 72.9L85.1 67.2M86.3 67.2L90.0 72.9L93.7 67.2M94.9 67.2L98.6 72.9L102.3 67.2M103.5 67.2L107.1 72.9L110.8 67.2M112.0 67.2L115.7 72.9L119.4 67.2M0.6 73.8L4.3 79.6L8.0 73.8M9.2 73.8L12.9 79.6L16.5 73.8M17.7 73.8L21.4 79.6L25.1 73.8M26.3 73.8L30.0 79.6L33.7 73.8M34.9 73.8L38.6 79.6L42.3 73.8M43.5 73.8L47.1 79.6L50.8 73.8M52.0 73.8L55.7 79.6L59.4 73.8M60.6 73.8L64.3 79.6L68.0 73.8M69.2 73.8L72.9 79.6L76.5 73.8M77.7 73.8L81.4 79.6L85.1 73.8M86.3 73.8L90.0 79.6L93.7 73.8M94.9 73.8L98.6 79.6L102.3 73.8M103.5 73.8L107.1 79.6L110.8 73.8M112.0 73.8L115.7 79.6L119.4 73.8M0.6 80.5L4.3 86.3L8.0 80.5M9.2 80.5L12.9 86.3L16.5 80.5M17.7 80.5L21.4 86.3L25.1 80.5M26.3 80.5L30.0 86.3L33.7 80.5M34.9 80.5L38.6 86.3L42.3 80.5M43.5 80.5L47.1 86.3L50.8 80.5M52.0 80.5L55.7 86.3L59.4 80.5M60.6 80.5L64.3 86.3L68.0 80.5M69.2 80.5L72.9 86.3L76.5 80.5M77.7 80.5L81.4 86.3L85.1 80.5M86.3 80.5L90.0 86.3L93.7 80.5M94.9 80.5L98.6 86.3L102.3 80.5M103.5 80.5L107.1 86.3L110.8 80.5M112.0 80.5L115.7 86.3L119.4 80.5M0.6 87.2L4.3 92.9L8.0 87.2M9.2 87.2L12.9 92.9L16.5 87.2M17.7 87.2L21.4 92.9L25.1 87.2M26.3 87.2L30.0 92.9L33.7 87.2M34.9 87.2L38.6 92.9L42.3 87.2M43.5 87.2L47.1 92.9L50.8 87.2M52.0 87.2L55.7 92.9L59.4 87.2M60.6 87.2L64.3 92.9L68.0 87.2M69.2 87.2L72.9 92.9L76.5 87.2M77.7 87.2L81.4 92.9L85.1 87.2M86.3 87.2L90.0 92.9L93.7 87.2M94.9 87.2L98.6 92.9L102.3 87.2M103.5 87.2L107.1 92.9L110.8 87.2M112.0 87.2L115.7 92.9L119.4 87.2M0.6 93.8L4.3 99.6L8.0 93.8M9.2 93.8L12.9 99.6L16.5 93.8M17.7 93.8L21.4 99.6L25.1 93.8M26.3 93.8L30.0 99.6L33.7 93.8M34.9 93.8L38.6 99.6L42.3 93.8M43.5 93.8L47.1 99.6L50.8 93.8M52.0 93.8L55.7 99.6L59.4 93.8M60.6 93.8L64.3 99.6L68.0 93.8M69.2 93.8L72.9 99.6L76.5 93.8M77.7 93.8L81.4 99.6L85.1 93.8M86.3 93.8L90.0 99.6L93.7 93.8M94.9 93.8L98.6 99.6L102.3 93.8M103.5 93.8L107.1 99.6L110.8 93.8M112.0 93.8L115.7 99.6L119.4 93.8M0.6 100.5L4.3 106.3L8.0 100.5M9.2 100.5L12.9 106.3L16.5 100.5M17.7 100.5L21.4 106.3L25.1 100.5M26.3 100.5L30.0 106.3L33.7 100.5M34.9 100.5L38.6 106.3L42.3 100.5M43.5 100.5L47.1 106.3L50.8 100.5M52.0 100.5L55.7 106.3L59.4 100.5M60.6 100.5L64.3 106.3L68.0 100.5M69.2 100.5L72.9 106.3L76.5 100.5M77.7 100.5L81.4 106.3L85.1 100.5M86.3 100.5L90.0 106.3L93.7 100.5M94.9 100.5L98.6 106.3L102.3 100.5M103.5 100.5L107.1 106.3L110.8 100.5M112.0 100.5L115.7 106.3L119.4 100.5M0.6 107.2L4.3 112.9L8.0 107.2M9.2 107.2L12.9 112.9L16.5 107.2M17.7 107.2L21.4 112.9L25.1 107.2M26.3 107.2L30.0 112.9L33.7 107.2M34.9 107.2L38.6 112.9L42.3 107.2M43.5 107.2L47.1 112.9L50.8 107.2M52.0 107.2L55.7 112.9L59.4 107.2M60.6 107.2L64.3 112.9L68.0 107.2M69.2 107.2L72.9 112.9L76.5 107.2M77.7 107.2L81.4 112.9L85.1 107.2M86.3 107.2L90.0 112.9L93.7 107.2M94.9 107.2L98.6 112.9L102.3 107.2M103.5 107.2L107.1 112.9L110.8 107.2M112.0 107.2L115.7 112.9L119.4 107.2M0.6 113.8L4.3 119.6L8.0 113.8M9.2 113.8L12.9 119.6L16.5 113.8M17.7 113.8L21.4 119.6L25.1 113.8M26.3 113.8L30.0 119.6L33.7 113.8M34.9 113.8L38.6 119.6L42.3 113.8M43.5 113.8L47.1 119.6L50.8 113.8M52.0 113.8L55.7 119.6L59.4 113.8M60.6 113.8L64.3 119.6L68.0 113.8M69.2 113.8L72.9 119.6L76.5 113.8M77.7 113.8L81.4 119.6L85.1 113.8M86.3 113.8L90.0 119.6L93.7 113.8M94.9 113.8L98.6 119.6L102.3 113.8M103.5 113.8L107.1 119.6L110.8 113.8M112.0 113.8L115.7 119.6L119.4 113.8" fill="none" stroke="#2f8f8a" stroke-width="1.4" stroke-linejoin="round"/></svg>'
AD = '<div class="ad-slot" data-ad="{}"><!-- AdSense ad unit goes here --></div>'


def mini_gauge():
    return '<div class="mini-gauge">' + GA1 + '<span>vs</span>' + GA2 + '</div>'


def faq_html(faqs):
    if not faqs: return ""
    return '<section class="faq"><div class="narrow"><h2>Questions crafters ask</h2>' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs) + "</div></section>"


def top(title_html, lead, crumb):
    return f'<div class="page-top"><div class="wrap"><p class="crumbs"><a href="{href("index.html")}">Home</a> / {e(crumb)}</p><h1>{title_html}</h1><p class="lead">{lead}</p></div></div>'

ETSY = "https://www.etsy.com/shop/PurlAndPaperCo"
GUM = "https://karamat4.gumroad.com"
# Our own products (Etsy + Gumroad). key: (name, price, etsy listing, gumroad slug)
SHOP = {
 "tea-room-junk-journal-kit": ("Tea Room junk journal kit", "6.99", "4620607287/tea-room-junk-journal-kit-printable", "tea-room-junk-journal-kit"),
 "night-garden-junk-journal-kit": ("Night Garden junk journal kit", "6.99", "4620614320/night-garden-junk-journal-kit-printable", "night-garden-junk-journal-kit"),
 "vintage-ephemera-pack": ("Vintage ephemera pack", "4.99", "4620615058/vintage-ephemera-printable-pack-junk", "vintage-ephemera-pack"),
 "journaling-cards-3x4": ("24 journaling cards (3x4)", "3.99", "4620615728/printable-journaling-cards-3x4-pocket", "journaling-cards"),
 "junk-journal-mega-bundle": ("Junk journal mega bundle", "14.99", "4620610591/junk-journal-mega-bundle-printable-tea", "junk-journal-mega-bundle"),
 "2027-crochet-knitting-planner": ("2027 crochet and knitting planner", "7.99", "4620606347/2027-crochet-planner-printable-knitting", "2027-crochet-knitting-planner"),
 "yarn-stash-tracker": ("Yarn stash tracker spreadsheet", "5.99", "4620611752/yarn-stash-tracker-spreadsheet-yarn", "yarn-stash-tracker"),
 "crochet-knitting-pricing-calculator": ("Crochet pricing calculator", "9.99", "4620610040/crochet-pricing-calculator-knitting", "crochet-pricing-calculator"),
 "christmas-gift-planner-budget": ("Christmas gift planner and budget", "6.99", "4621713425/christmas-gift-planner-spreadsheet", "christmas-gift-planner"),
 "december-days-journal-kit": ("December Days journal kit", "6.99", "4622484083/december-daily-journal-kit-printable-25", "december-days-journal-kit"),
 "christmas-gift-tags": ("Printable Christmas gift tags", "3.99", "4621715645/printable-christmas-gift-tags-holiday", "christmas-gift-tags"),
 "soap-making-business-spreadsheet": ("Soap making business spreadsheet", "11.99", "4623878110", "soap-business-spreadsheet"),
 "resin-art-business-spreadsheet": ("Resin calculator and pricing spreadsheet", "11.99", "4624644331", "resin-business-spreadsheet"),
 "sublimation-tumbler-business-spreadsheet": ("Tumbler and sublimation pricing spreadsheet", "11.99", "4624645405", "tumbler-pricing-spreadsheet"),
}
KNIT = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator"]
JJ = ["december-days-journal-kit", "junk-journal-mega-bundle", "tea-room-junk-journal-kit", "night-garden-junk-journal-kit"]
SHOP_FOR = {"index.html": ["junk-journal-mega-bundle", "2027-crochet-knitting-planner", "night-garden-junk-journal-kit", "yarn-stash-tracker"],
            "row-counter.html": KNIT, "yarn-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator"],
            "gauge-converter.html": KNIT, "projects.html": KNIT, "yarn-weights.html": KNIT, "hook-needle-sizes.html": KNIT, "crochet-terms.html": KNIT,
            "journal-prompts.html": ["december-days-journal-kit", "journaling-cards-3x4", "vintage-ephemera-pack", "junk-journal-mega-bundle"], "junk-journal-beginners.html": JJ,
            "blanket-size-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "hat-size-chart.html": ["2027-crochet-knitting-planner", "christmas-gift-tags", "yarn-stash-tracker", "crochet-knitting-pricing-calculator"],
            "granny-square-blanket-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "increase-decrease-calculator.html": KNIT,
            "sock-size-chart.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-tags", "crochet-knitting-pricing-calculator"],
            "how-to-price-crochet-items.html": ["crochet-knitting-pricing-calculator", "yarn-stash-tracker", "2027-crochet-knitting-planner", "soap-making-business-spreadsheet"],
            "yarn-substitution-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "crochet-circle-calculator.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "cast-on-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-tea-stain-paper.html": ["tea-room-junk-journal-kit", "vintage-ephemera-pack", "junk-journal-mega-bundle", "december-days-journal-kit"],
            "knitting-abbreviations.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "junk-journal-ephemera-ideas.html": ["vintage-ephemera-pack", "journaling-cards-3x4", "junk-journal-mega-bundle", "tea-room-junk-journal-kit"],
            "yarn-yardage-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "etsy-fee-calculator.html": ["crochet-knitting-pricing-calculator", "soap-making-business-spreadsheet", "resin-art-business-spreadsheet", "sublimation-tumbler-business-spreadsheet"],
            "craft-fair-checklist.html": ["crochet-knitting-pricing-calculator", "soap-making-business-spreadsheet", "resin-art-business-spreadsheet", "sublimation-tumbler-business-spreadsheet"],
            "temperature-blanket-planner.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "c2c-blanket-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "scarf-size-chart.html": ["christmas-gift-tags", "2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator"],
            "foundation-chain-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "junk-journal-signature-calculator.html": ["junk-journal-mega-bundle", "tea-room-junk-journal-kit", "night-garden-junk-journal-kit", "journaling-cards-3x4"],
            "how-to-crochet-magic-ring.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-change-colors-in-crochet.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-bind-off-knitting.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-cast-on-knitting.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-crochet-decrease.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-weave-in-ends.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-fix-a-dropped-stitch.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-price-a-crochet-blanket.html": ["crochet-knitting-pricing-calculator", "yarn-stash-tracker", "2027-crochet-knitting-planner", "christmas-gift-tags"],
            "how-to-knit-in-the-round.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-tags", "crochet-knitting-pricing-calculator"],
            "junk-journal-supply-checklist.html": ["junk-journal-mega-bundle", "vintage-ephemera-pack", "journaling-cards-3x4", "tea-room-junk-journal-kit"],
            "how-to-pick-up-stitches-knitting.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-price-amigurumi.html": ["crochet-knitting-pricing-calculator", "yarn-stash-tracker", "2027-crochet-knitting-planner", "christmas-gift-tags"],
            "crochet-time-estimator.html": ["crochet-knitting-pricing-calculator", "2027-crochet-knitting-planner", "christmas-gift-planner-budget", "yarn-stash-tracker"],
            "basic-crochet-stitches.html": ["2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "yarn-stash-tracker", "christmas-gift-tags"],
            "sweater-size-calculator.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-planner-budget"],
            "stripe-generator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "crochet-knitting-gift-planner.html": ["christmas-gift-planner-budget", "christmas-gift-tags", "2027-crochet-knitting-planner", "yarn-stash-tracker"]}


def shop_box(file):
    keys = SHOP_FOR.get(file)
    if not keys:
        return ""
    cards = "".join(
        f'<li class="shop-card"><a href="https://www.etsy.com/listing/{SHOP[k][2]}" rel="noopener"><img src="{asset("shop/" + k + ".jpg")}" alt="{e(SHOP[k][0])} preview" width="400" height="400" loading="lazy">'
        f'<span class="shop-name">{e(SHOP[k][0])}</span></a><span class="shop-meta">${SHOP[k][1]} &middot; <a href="https://www.etsy.com/listing/{SHOP[k][2]}" rel="noopener">Etsy</a> or <a href="{GUM}/l/{SHOP[k][3]}" rel="noopener">Gumroad</a></span></li>'
        for k in keys)
    return (f'<section class="shop-strip" aria-labelledby="shop-h"><div class="wrap"><h2 id="shop-h">Made by us, for your next project</h2>'
            f'<p class="muted">These tools are free. If you\'d like printables or planners to go with them, our shop helps keep the site free.</p>'
            f'<ul class="shop-grid">{cards}</ul><p><a class="btn ghost" href="{ETSY}" rel="noopener">See the whole shop on Etsy</a></p></div></section>')


# ---- Our own KDP paperback (Amazon affiliate link via /go/knit-journal) ----
def book_box(file):
    keys = SHOP_FOR.get(file) or []
    if file != "index.html" and "2027-crochet-knitting-planner" not in keys:
        return ""
    return (f'<section class="book-strip" aria-labelledby="book-h"><div class="wrap"><div class="book-card">'
            f'<img src="{asset("shop/knit-crochet-project-journal.jpg")}" alt="Knit and Crochet Project Journal paperback cover" width="400" height="400" loading="lazy">'
            f'<div><p class="muted" style="margin:0">Our paperback</p><h2 id="book-h">Knit &amp; Crochet Project Journal</h2>'
            f'<p>Which hook was that? How many skeins did it take? 40 two-page project spreads with 100-row counters, yarn weight and hook size charts, a stash inventory, abbreviations and graph paper. 8.5 x 11 in, 110 pages.</p>'
            f'<p><a class="btn" href="{go("knit-journal")}" {AFF_ATTR}>See it on Amazon ($9.99)</a></p>'
            f'<p class="aff-note">This is our own book. The Amazon link is an affiliate link, so we may also earn a small commission, at no extra cost to you.</p></div></div></div></section>')


# ---- Email signup (Kit form 10215409). Sign-ups go to Kit; Kit redirects to /thanks, then /welcome after confirming. ----
NL_SKIP = ("thanks.html", "welcome.html", "404.html", "privacy.html")
NOINDEX = ("thanks.html", "welcome.html", "404.html")
def signup(file):
    if file in NL_SKIP:
        return ""
    return """<section class="nl" id="newsletter"><div class="wrap"><div class="nl-card">
<div><h2>Free printable sampler</h2><p>Journaling cards, a vintage ephemera sheet and a planner page from our shop, free to print. Plus new freebies and pattern ideas now and then.</p></div>
<form class="nl-form" action="https://app.kit.com/forms/10215409/subscriptions" method="post">
<label class="nl-sr" for="nl-email">Email address</label>
<input id="nl-email" type="email" name="email_address" required placeholder="Your email address" autocomplete="email">
<button type="submit">Send my printables</button>
</form>
<p class="nl-fine">Free. No spam, unsubscribe in one click. See our <a href="/privacy.html">privacy policy</a>.</p>
</div></div></section>"""
NL_THANKS = """<section><div class="wrap nl-done"><h1>Check your inbox</h1>
<p>We've just emailed you a confirmation link. Tap the button in that email and your free printable sampler opens straight away.</p>
<p>Can't see it after a minute? Look in your spam or promotions folder.</p>
<div class="nl-links"><a href="/row-counter">Row counter</a><a href="/yarn-calculator">Yarn calculator</a><a href="/journal-prompts">Journal prompts</a></div></div></section>"""
NL_WELCOME = """<section><div class="wrap nl-done"><h1>You're in!</h1>
<p>Thanks for confirming. Here's your free printable sampler:</p>
<a class="nl-btn" href="/assets/free/purl-and-paper-free-sampler.pdf" download>Download the PDF</a>
<p>We'll email you when there's something worth knowing, never more than once a week.</p>
<div class="nl-links"><a href="/row-counter">Row counter</a><a href="/yarn-calculator">Yarn calculator</a><a href="/journal-prompts">Journal prompts</a></div></div></section>"""


AFF = {
    "yarn": "https://www.lovecrafts.com/en-us/collections/yarns",
    "yarn-by-weight": "https://www.lovecrafts.com/en-us/collections/yarn-by-weight",
    "crochet-hooks": "https://www.lovecrafts.com/en-us/collections/crochet-hooks",
    "knitting-needles": "https://www.lovecrafts.com/en-us/collections/knitting-needles",
    "free-patterns": "https://www.lovecrafts.com/en-us/collections/all-free-patterns",
    "knit-journal": "https://www.amazon.com/dp/B0HSMCC4S9?tag=purlandpaper-20",
}
# ---- Affiliate links. Pages link to /go/<slug>; _redirects sends it to the store.
# Until a programme approves us these are plain store URLs; when approved, replace the URL with the tracked link and rebuild.
AFF_ATTR = 'rel="sponsored nofollow noopener" target="_blank"'
AFF_NOTE = '<p class="aff-note">We may earn a commission if you buy through these links, at no extra cost to you.</p>'
def go(slug): return "/go/" + slug
def write_redirects(root):
    lines = "".join(f"/go/{k} {v} 302\n" for k, v in AFF.items())
    (root / "_redirects").write_text(lines)


def page(file, title, desc, body, faqs=None, crumb=None, scripts="", app_name=None):
    _og = og_image(file, title, DOMAIN)
    url = canon(file)
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": url, "dateModified": UPDATED,
           "isPartOf": {"@type": "WebSite", "name": SITE, "url": DOMAIN + "/"}}]
    if app_name:
        ld.append({"@context": "https://schema.org", "@type": "WebApplication", "name": app_name, "url": url, "applicationCategory": "LifestyleApplication",
                   "operatingSystem": "Any (web browser)", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}})
    if crumb:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}, {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]})
    if faqs:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");</script>' if GA_ID else "")
    nav = "".join(f'<li><a href="{href(f)}"{" aria-current=\"page\"" if f == file else ""}>{n}</a></li>' for f, n in NAV)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="p:domain_verify" content="745e513870bb39b37db2c4334a6fa032">
{ga}
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="msvalidate.01" content="215145BE38DEE30C2985F40FB4D4041F">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{"noindex, follow" if file in NOINDEX else "index, follow, max-image-preview:large"}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(SITE)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{_og}"><meta property="og:image:width" content="960"><meta property="og:image:height" content="504"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{_og}"><meta name="theme-color" content="#1f2a44">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='15' cy='17' r='12' fill='%23b8326a'/%3E%3Crect x='19' y='2' width='11' height='8' rx='2' fill='%23f4a823'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&display=swap" rel="stylesheet" media="print" onload="this.media='all'"><noscript><link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&display=swap" rel="stylesheet"></noscript>
<link rel="stylesheet" href="{asset("style.css")}">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body data-page="{file[:-5]}">
<header class="head"><div class="wrap">
<a class="brand" href="{href("index.html")}">{LOGO}<span>Purl <i>&amp;</i> Paper</span></a>
<button class="burger" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<ul class="nav" id="nav">{nav}</ul>
</div></header>
<main id="main">
{body}
{faq_html(faqs)}
{signup(file)}
{AD.format(file)}
</main>
{book_box(file)}{shop_box(file)}
<footer><div class="wrap"><div class="fgrid">
<div><a class="brand" href="{href("index.html")}">{LOGO}<span>Purl <i>&amp;</i> Paper</span></a><p style="margin-top:12px" class="muted">Free tools for knitters, crocheters and junk journalers. Count your rows, plan your yarn, and never run out of ideas for the next page.</p></div>
<div><strong>Tools</strong><ul>{"".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in NAV + TOOLS_MORE)}</ul></div>
<div><strong>Shop</strong><ul><li><a href="{ETSY}" rel="noopener">Purl &amp; Paper on Etsy</a></li><li><a href="{GUM}" rel="noopener">Purl &amp; Paper on Gumroad</a></li><li><a href="https://www.pinterest.com/purlandpaperco/" rel="noopener">Pinterest</a></li></ul></div>
<div><strong>Guides</strong><ul>{"".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in GUIDES)}<li><a href="{href("about.html")}">About and contact</a></li><li><a href="{href("privacy.html")}">Privacy policy</a></li></ul></div>
</div>
<p class="legal">{e(SITE)} is an independent site. Your counters, projects and saved prompts stay on your own device; nothing is uploaded. Yarn amounts are estimates, so always check your pattern. Last checked {e(UPDATED)}.</p>
</div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>window.PP={json.dumps({k: D[k] for k in ("prompts", "projects", "weights", "blankets", "gifts", "hats", "socks", "tblanket")}, ensure_ascii=False)};</script>
{scripts}<script src="{asset("app.js")}"></script>
</body>
</html>
'''
    (ROOT / file).write_text(doc, encoding="utf-8")


# ---------------- HOME ----------------
home = f'''<section class="hero" aria-label="Introduction">
<canvas id="swatch" class="fabric" role="img" aria-label="Knitted fabric that knits itself row by row, with the colour chart still to knit above it. Pick a yarn colour and draw on it to add colourwork."></canvas>
<div class="wrap hero-in">
<div class="ballband">
<div class="bb-top"><span>Free tools · No sign-up</span><span class="bb-wt" aria-hidden="true"><svg viewBox="0 0 40 46"><path d="M20 2c9 0 17 6 17 14v14c0 8-8 14-17 14S3 38 3 30V16C3 8 11 2 20 2z" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M6 12c9 4 19 4 28 0M5 34c9-4 21-4 30 0" fill="none" stroke="currentColor" stroke-width="1.6"/><text x="20" y="28.5" text-anchor="middle" font-size="15" font-weight="800" fill="currentColor" font-family="sans-serif">4</text></svg></span></div>
<h1>Count rows. <span class="l2">Plan yarn.</span> <span class="l3">Fill the journal.</span></h1>
<p class="lead">Free tools for knitters, crocheters and junk journalers: a row counter that keeps your screen awake, a yarn calculator, a gauge fixer and prompts for your next page.</p>
<div class="btns"><a class="btn gold" href="{href("row-counter.html")}">Open the row counter</a><a class="btn ghost" href="{href("yarn-calculator.html")}">How much yarn do I need?</a></div>
<dl class="bb-specs"><div><dt>Tools</dt><dd>6</dd></div><div><dt>Price</dt><dd>Free</dd></div><div><dt>Saves to</dt><dd>Your device</dd></div><div><dt>Account</dt><dd>None</dd></div></dl>
</div>
<div class="knit-ctl"><span class="kc-l">Knit in colour</span><div class="yarns" role="group" aria-label="Yarn colour">
<button type="button" class="yarn-btn" style="--c:#b8326a" data-c="#b8326a" aria-pressed="true" aria-label="Berry yarn"></button><button type="button" class="yarn-btn" style="--c:#f4a823" data-c="#f4a823" aria-pressed="false" aria-label="Marigold yarn"></button><button type="button" class="yarn-btn" style="--c:#2f8f8a" data-c="#2f8f8a" aria-pressed="false" aria-label="Teal yarn"></button><button type="button" class="yarn-btn" style="--c:#1f2a44" data-c="#1f2a44" aria-pressed="false" aria-label="Navy yarn"></button><button type="button" class="yarn-btn" style="--c:#f3eee6" data-c="#f3eee6" aria-pressed="false" aria-label="Cream yarn"></button></div>
<span class="row-chip">Row <span id="sw-row">0</span></span><button type="button" class="kc-reset" id="sw-reset" aria-label="Unravel and start again" title="Unravel and start again">↺</button></div>
</div></section>
<hr class="stitch">
<section><div class="wrap"><div class="sh"><h2>On the work table</h2><p class="muted">Every tool saves on your phone. Nothing to install.</p></div>
<div class="table">
<a class="piece big tape t1" href="{href("row-counter.html")}"><h3>Row counter that stays awake</h3><div class="mini-count"><b>48</b><span>+</span><small>of 60 rows<br>4 repeats done</small></div><p>Big buttons you can tap with yarn in your hands. Set a target, count pattern repeats, run several counters at once, and keep the screen from going dark.</p><span class="go">Start counting</span></a>
<a class="piece mid tape t2" href="{href("yarn-calculator.html")}"><h3>How much yarn do I need?</h3><div class="skeins"><i></i><i></i><i></i><i></i></div><p>Pick the project, size and yarn weight. You get yards, metres and how many skeins to buy, with a little spare.</p><span class="go">Plan my yarn</span></a>
<a class="piece tape t3" href="{href("gauge-converter.html")}"><h3>Gauge converter</h3>{mini_gauge()}<p>Your swatch doesn't match the pattern? Find out how big the finished piece will be, and how many stitches to cast on instead.</p><span class="go">Fix my gauge</span></a>
<a class="piece tape t4" href="{href("projects.html")}"><h3>Project tracker</h3><ul class="mini-proj" aria-hidden="true"><li>Sunday cardigan<i style="--p:70%;--c:#2f8f8a"></i></li><li>Baby blanket<i style="--p:35%;--c:#b8326a"></i></li><li>Travel journal<i style="--p:90%;--c:#f4a823"></i></li></ul><p>Every work in progress in one place: the yarn, the hook or needles, where you got to, and notes for next time.</p><span class="go">Track my projects</span></a>
<a class="piece tape t1" href="{href("journal-prompts.html")}"><h3>Junk journal prompts</h3><div class="prompt-peek" id="peek">A walk you took this week + a ticket stub</div><p>Shuffle a theme, a piece of ephemera, a technique and a colour palette for your next spread.</p><span class="go">Shuffle a spread</span></a>
</div></div></section>
{AD.format("home-mid")}
<section class="band"><div class="wrap"><div class="sh"><h2>Guides worth keeping open</h2><p class="muted">Charts and plain-English answers for the things patterns assume you know.</p></div>
<div class="guides">
<a class="guide" href="{href("yarn-weights.html")}"><div class="gi">0–7</div><h3>Yarn weight chart</h3><p>Lace to jumbo, with the needle and hook size, gauge and UK names for each.</p></a>
<a class="guide" href="{href("hook-needle-sizes.html")}"><div class="gi">mm ↔ US</div><h3>Hook and needle sizes</h3><p>Metric, US and old UK sizes side by side, with a quick finder.</p></a>
<a class="guide" href="{href("crochet-terms.html")}"><div class="gi">sc = dc?</div><h3>US vs UK crochet terms</h3><p>Why a UK double crochet is a US single, and a full conversion table.</p></a>
<a class="guide" href="{href("junk-journal-beginners.html")}"><div class="gi">Page 1</div><h3>Junk journaling for beginners</h3><p>What it is, what you need (mostly free), and how to bind your first signature.</p></a>
</div><p class="guides-more"><strong>New crafts:</strong> <a href="{href("calligraphy-practice-sheets.html")}">calligraphy practice sheets</a>, <a href="{href("dot-grid-paper.html")}">dot grid paper</a> for bullet journals, and calculators for <a href="{href("cross-stitch-calculator.html")}">cross stitch</a>, <a href="{href("quilt-size-calculator.html")}">quilt size</a>, <a href="{href("diamond-painting-calculator.html")}">diamond painting</a>, <a href="{href("candle-making-calculator.html")}">candle wax</a>, <a href="{href("resin-calculator.html")}">epoxy resin</a> and <a href="{href("macrame-cord-calculator.html")}">macrame cord</a>. See <a href="{href("crafts.html")}">all crafts</a>.</p><p class="guides-more">New on the work table: <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a> (step through chain, single, half double, double and treble crochet with US/UK names), the <a href="{href("sweater-size-calculator.html")}">sweater size calculator</a> (which size to knit or crochet, with ease and yarn), the <a href="{href("crochet-time-estimator.html")}">crochet and knitting time calculator</a> (how long a blanket, scarf or gift will take, and whether it will be ready in time), a <a href="{href("stripe-generator.html")}">random stripe generator</a> (pick your colours, shuffle, print the row list), the <a href="{href("c2c-blanket-calculator.html")}">C2C blanket calculator</a> (how many corner to corner tiles, when to decrease, and how much yarn), a <a href="{href("scarf-size-chart.html")}">scarf size chart</a> (how long and wide for kids, women and men, with a yarn calculator), <a href="{href("how-to-pick-up-stitches-knitting.html")}">how to pick up stitches</a> (with a calculator for how many and how to space them), <a href="{href("how-to-price-amigurumi.html")}">how to price amigurumi</a> (a crochet toy price calculator from keyring to large plush), <a href="{href("how-to-knit-in-the-round.html")}">how to knit in the round</a> (join without twisting, with a circular needle length finder), a <a href="{href("junk-journal-supply-checklist.html")}">junk journal supply checklist</a> (what you need, what's free at home, and a free pocket and tag template), <a href="{href("how-to-fix-a-dropped-stitch.html")}">how to fix a dropped stitch</a> (even several rows down, with a helper for garter and rib), <a href="{href("how-to-price-a-crochet-blanket.html")}">how to price a crochet blanket</a> (a calculator for yarn, hours and a fair price by size), <a href="{href("how-to-cast-on-knitting.html")}">how to cast on knitting</a> (with a long-tail tail calculator and a cast on chooser), <a href="{href("how-to-crochet-decrease.html")}">how to decrease in crochet</a> (sc2tog, the invisible decrease, and a helper that writes your amigurumi closing rounds), <a href="{href("how-to-bind-off-knitting.html")}">how to bind off knitting</a> (with a chooser for stretchy bind offs and how much yarn to keep), <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a> in crochet and knitting (with a helper for your yarn), step-by-step guides to <a href="{href("how-to-crochet-magic-ring.html")}">the crochet magic ring</a> (with a helper that writes your first rounds) and <a href="{href("how-to-change-colors-in-crochet.html")}">changing colours in crochet</a> (with a stripe planner that says when to carry and when to cut), the <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a> (how many chains to start a crochet blanket or scarf), a <a href="{href("junk-journal-signature-calculator.html")}">junk journal signature calculator</a> (pages, spine, sewing holes and thread), the <a href="{href("yarn-yardage-calculator.html")}">yarn yardage calculator</a> (weigh a leftover ball to see how many yards are left), a printable <a href="{href("craft-fair-checklist.html")}">craft fair checklist</a> with a stock and cash float planner, the <a href="{href("temperature-blanket-planner.html")}">temperature blanket planner</a> (colour key, ranges and yarn per colour for 2027), a <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list with a pattern decoder</a> (paste a line, get plain English), 62 <a href="{href("junk-journal-ephemera-ideas.html")}">junk journal ephemera ideas</a> with a checklist, the <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a> (stitches per round and an amigurumi ball pattern), the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> (how many stitches for a scarf, blanket or cowl), seasonal <a href="{href("journal-prompts.html")}">winter and Christmas journal prompts</a>, the <a href="{href("yarn-substitution-calculator.html")}">yarn substitution calculator</a> (how many balls of a different yarn), a guide to <a href="{href("how-to-tea-stain-paper.html")}">tea staining paper</a> for junk journals with a shade tester, the <a href="{href("sock-size-chart.html")}">sock size chart and cast-on calculator</a> (heel, gusset and toe numbers for your gauge), the <a href="{href("increase-decrease-calculator.html")}">increase and decrease evenly calculator</a> (it writes the row out for you), a guide to <a href="{href("how-to-price-crochet-items.html")}">pricing crochet items to sell</a> with a fee calculator, the <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> (how many squares and how much yarn), the <a href="{href("hat-size-chart.html")}">hat size chart and cast-on calculator</a> (preemie to adult, knit or crochet), the <a href="{href("crochet-knitting-gift-planner.html")}">handmade Christmas gift planner</a> (will your knitted and crocheted gifts be ready in time?) and the <a href="{href("blanket-size-calculator.html")}">blanket size chart and yarn calculator</a>, from lovey to king size.</p></div></section>'''
home_faq = [
    ("Are these tools really free?", "Yes. Every tool is free and works in your browser without an account. The site is supported by ads."),
    ("Will my row count be saved if I close the page?", "Yes. Counters, projects and saved prompts are stored on your own device, so they're still there when you come back on the same phone or computer and browser."),
    ("Do the tools work on a phone?", "Yes. Everything is built for a phone at the craft table first, with big buttons and a keep-screen-on option on the row counter."),
]
page("index.html", "Free Row Counter, Yarn Calculator and Junk Journal Prompts | Purl & Paper",
     "Free tools for knitting, crochet and junk journaling: a row counter that keeps your screen on, a yarn calculator, a gauge converter, a project tracker and journal prompts.",
     home, home_faq, scripts=f'<script src="{asset("knit.js")}"></script><script src="{asset("swatch.js")}"></script>')

# ---------------- ROW COUNTER ----------------
rc = top("Row counter", "Tap the big button each time you finish a row. Add a target, count pattern repeats, and run as many counters as your project needs. Everything saves on this device.", "Row counter") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="toolbar"><button type="button" class="btn sm" id="rc-add">+ Add a counter</button>
<label class="switch"><input type="checkbox" id="rc-wake"> Keep screen on</label>
<label class="switch"><input type="checkbox" id="rc-buzz" checked> Buzz on tap</label>
<span class="spacer"></span><button type="button" class="btn ghost sm" id="rc-undo" disabled>Undo last tap</button></div>
<div class="counters" id="counters"></div>
<p class="note" style="margin-top:20px">Keyboard: press <strong>Space</strong> or <strong>+</strong> to add a row on the first counter, <strong>−</strong> to take one away.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><div class="quick"><strong>Quick answer:</strong> tap the big + button after every row (or press Space on a keyboard). Set "Repeat every" to the length of your pattern repeat, add a target if you know the total, and tick "Keep screen on" so the phone doesn't lock mid-row. Counts save on this device automatically.</div>
<h2>How many rows do I need to reach a length?</h2>
<p>Count the rows in 4 in (10 cm) of your swatch, then multiply. 28 rows in 4 in is 7 rows per inch, so a 10 in sleeve needs 70 rows. Type your numbers here and set the answer as the target on your first counter.</p>
<div class="sheet rc-need"><div class="row2"><div class="field"><label for="rc-nl">Length to work</label><input type="number" id="rc-nl" value="10" min="0.5" max="400" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="rc-nu">Unit</label><select id="rc-nu"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="row2"><div class="field"><label for="rc-nr">Rows in your swatch</label><input type="number" id="rc-nr" value="28" min="1" max="200" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="rc-no">Measured over</label><select id="rc-no"><option value="4">4 in</option><option value="10">10 cm</option></select></div></div>
<p id="rc-need" aria-live="polite"><strong>70 rows</strong></p><p><button type="button" class="btn sm" id="rc-nset">Set as target on my first counter</button></p></div>
<p class="note">Rows stretch and squash more than stitches, so measure the piece as you go too. Row gauge on the ball band is a guide, not a promise; our <a href="{href("gauge-converter.html")}">gauge converter</a> explains why it matters.</p>
<h2>How do I use the repeat counter?</h2>
<p>Many patterns repeat a set of rows, like "repeat rows 1 to 8 six times". Put <strong>8</strong> in "Repeat every". The counter then shows which row of the repeat you're on and adds one to your repeat count each time you finish the set.</p>
<p>Use a second counter for something separate, like decreases on a sleeve or rounds on a hat crown, so you never have to keep two numbers in your head.</p>
<h2>How do I keep track of increase and decrease rows?</h2>
<p>Patterns often say something like "decrease at each end every 6th row, 8 times". Make a second counter called "Decreases", set its repeat to <strong>6</strong>, and give it a target of <strong>48</strong> (6 × 8). It tells you which row of the six you're on, and adds one to the repeat count each time you reach a decrease row. Your main counter keeps the total rows.</p>
<p>Need to work out the spacing first, like "increase 14 stitches evenly across the row"? The <a href="{href("increase-decrease-calculator.html")}">increase and decrease evenly calculator</a> writes the row out for you.</p>
<h2>How do I count rows I've already knitted?</h2>
<ul><li><strong>Knitting:</strong> each V in a column of stockinette is one row. Count the Vs from just above the cast-on edge up to the needle; the loops on the needle are the current row, not yet counted.</li>
<li><strong>Garter stitch:</strong> each ridge is two rows.</li>
<li><strong>Crochet:</strong> count the tall stitch posts in one column; for single crochet, each little ridge of loops is one row.</li></ul>
<p>Tap "Set number" on the counter, type the rows you counted, then carry on tapping.</p>
<h2>What next?</h2>
<p>Log the project, its yarn and where you got to in the <a href="{href("projects.html")}">project tracker</a>, check you've got enough yarn with the <a href="{href("yarn-calculator.html")}">yarn calculator</a>, or plan a hat with the <a href="{href("hat-size-chart.html")}">hat size calculator</a>.</p></div></section>'''
rc_faq = [
    ("How do I stop my phone screen turning off while I knit?", "Tick 'Keep screen on'. It uses your browser's screen wake feature, which works in most up-to-date browsers on Android, iPhone and computers. It switches off when you leave the page."),
    ("Does the row counter work offline?", "Once the page has loaded it keeps working without a connection, and your counts are saved on your device."),
    ("Can I count rounds instead of rows?", "Yes. Rename the counter to 'Rounds' by tapping its name. It counts the same way."),
    ("How do I count decrease rows like every 6th row?", "Add a second counter, set its repeat to 6 and its target to 6 times the number of decreases. It shows which row of the six you're on and counts each completed repeat, while your first counter keeps the total."),
    ("How many rows do I need for 10 inches?", "Multiply 10 by your rows per inch. With 28 rows in 4 in (7 per inch) that is 70 rows; with 20 rows in 4 in it is 50. The helper on this page works it out and sets it as your target."),
    ("How do I count rows in knitting?", "In stockinette, count the Vs in one column from above the cast-on edge; each V is one row. In garter stitch each ridge is two rows. Don't count the loops on your needle."),
]
page("row-counter.html", "Free Online Row Counter for Knitting and Crochet | Purl & Paper",
     "A free row counter for knitting and crochet with big tap buttons, repeat counting, targets, multiple counters and a keep-screen-on switch. Saves automatically.",
     rc, rc_faq, "Row counter", app_name="Row counter")

# ---------------- YARN CALCULATOR ----------------
wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"])})</option>' for w in D["weights"])
popts = "".join(f'<option value="{p["id"]}">{e(p["name"])}</option>' for p in D["projects"])
YC_M = {w["n"]: w["m"] for w in D["weights"]}
def yc_yd(pid, wn, craft=1.0): pr = [x for x in D["projects"] if x["id"] == pid][0]; return int(pr["yd"] * YC_M[wn] * craft / 10 + 0.5) * 10
YC_COLS = [(3, 1.0, "Knit, DK"), (4, 1.0, "Knit, worsted"), (5, 1.0, "Knit, bulky"), (4, 1.27, "Crochet, worsted")]
yc_rows = "".join(f'<tr><td><strong>{e(x["name"])}</strong>{" <span class=\"muted\">(size M)</span>" if x["sizes"] else ""}</td>' + "".join(f"<td>{yc_yd(x['id'], wn, cf):,}</td>" for wn, cf, _ in YC_COLS) + "</tr>" for x in D["projects"])
yc = top("How much yarn do I need?", "Choose what you're making, the size and your yarn weight. You get an estimate in yards and metres, and how many skeins to buy.", "Yarn calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> in worsted yarn, a knitted adult beanie takes about <strong>{yc_yd("hat", 4)} yards</strong>, a scarf about <strong>{yc_yd("scarf", 4)}</strong>, a baby blanket about <strong>{yc_yd("babyb", 4):,}</strong> and an adult sweater about <strong>{yc_yd("sweater", 4):,}</strong>. Thinner yarn needs more length, thicker yarn less, and crochet uses roughly a quarter more. These are estimates: your pattern's amount always wins.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="yc-proj">What are you making?</label><select id="yc-proj">{popts}</select></div>
<div class="field" id="yc-size-f" hidden><label for="yc-size">Size</label><select id="yc-size"></select></div>
<div class="field"><span class="label" id="yc-craft-l">Knitting or crochet?</span><div class="seg" role="group" aria-labelledby="yc-craft-l" id="yc-craft"><button type="button" data-v="knit" aria-pressed="true">Knitting</button><button type="button" data-v="crochet" aria-pressed="false">Crochet</button></div></div>
<div class="field"><label for="yc-weight">Yarn weight (number on the label)</label><select id="yc-weight">{wopts}</select></div>
<div class="row2"><div class="field"><label for="yc-skein">Length per skein</label><input type="number" id="yc-skein" value="200" min="1" inputmode="decimal"></div>
<div class="field"><label for="yc-unit">Unit on the label</label><select id="yc-unit"><option value="yd">yards</option><option value="m">metres</option></select></div></div>
<div class="field"><span class="label" id="yc-col-l">Yarn colour (just for fun)</span><div class="yarns" role="group" aria-labelledby="yc-col-l" id="yc-col"><button type="button" class="yarn-btn" style="--c:#2f8f8a" data-c="#2f8f8a" aria-pressed="true" aria-label="Teal"></button><button type="button" class="yarn-btn" style="--c:#b8326a" data-c="#b8326a" aria-pressed="false" aria-label="Berry"></button><button type="button" class="yarn-btn" style="--c:#f4a823" data-c="#f4a823" aria-pressed="false" aria-label="Marigold"></button><button type="button" class="yarn-btn" style="--c:#8a5a44" data-c="#8a5a44" aria-pressed="false" aria-label="Rust"></button><button type="button" class="yarn-btn" style="--c:#9aa4b8" data-c="#9aa4b8" aria-pressed="false" aria-label="Grey"></button><button type="button" class="yarn-btn" style="--c:#efe6d6" data-c="#efe6d6" aria-pressed="false" aria-label="Oatmeal"></button></div></div>
<div class="field"><span class="label" id="yc-dense-l">Stitch pattern</span><div class="seg" role="group" aria-labelledby="yc-dense-l" id="yc-dense"><button type="button" data-v="1" aria-pressed="true">Plain</button><button type="button" data-v="1.15" aria-pressed="false">Textured or cables</button><button type="button" data-v="0.85" aria-pressed="false">Lacy or open</button></div></div>
</div>
<div class="result" aria-live="polite" id="yc-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How the estimate works</h2>
<p>We start from typical amounts for each project in worsted (weight 4) yarn, then adjust for your yarn's thickness: thinner yarn needs more length, thicker yarn less. Crochet usually uses around a quarter more yarn than knitting for the same piece, and cables or bobbles use more again.</p>
<div class="callout"><strong>Buy from the same dye lot.</strong> Skeins dyed in different batches can look slightly different side by side. The dye lot number is on the label, so buy everything you need at once, plus one spare if you can return it.</div>
<p>Your pattern's yarn amount always wins. Use this when you're designing your own piece, swapping yarn, or the pattern doesn't say.</p>
<h2>Making a blanket?</h2>
<p>Blankets vary so much in size that a single number isn't much help. Our <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a> lists the usual sizes from lovey to king, draws your blanket next to a bed, and works out the yarn from the exact width and length you want.</p>
<h2>Using a different yarn from the pattern?</h2>
<p>If your pattern already gives an amount but you're swapping brands, don't start from scratch: the <a href="{href("yarn-substitution-calculator.html")}">yarn substitution calculator</a> turns the pattern's balls into balls of your yarn and checks the thickness.</p></div></section>
<section style="padding-top:0"><div class="wrap"><h2>How much yarn for a hat, scarf, blanket or sweater?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Project</th>{"".join(f'<th scope="col">{n}</th>' for _, _, n in YC_COLS)}</tr></thead><tbody>{yc_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Yards, rounded to the nearest 10, from the same estimate the calculator uses: a typical worsted amount for each project, scaled for yarn thickness, with crochet about 27% more. Plain stitch patterns; add 10 to 15% for cables or texture. Divide by the length on your yarn label to get skeins, and round up.</p></div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How do I work out yarn from a swatch?</h2>
<ol><li><strong>Weigh your swatch</strong> on a kitchen scale after knitting or crocheting it in the real yarn and stitch. A 4 in (10 cm) square is easy to measure.</li>
<li><strong>Work out the area</strong> of your piece and how many swatches fit into it. A 20 × 60 in scarf is 1,200 sq in, which is 75 squares of 4 × 4 in.</li>
<li><strong>Multiply</strong> the swatch weight by that number to get the grams you need.</li>
<li><strong>Turn grams into balls</strong> using the label: a 100 g ball needs grams ÷ 100, rounded up. Add about 10% for seams, edging and the swatch itself.</li></ol>
<h2>How many skeins should I buy?</h2>
<p>Divide the yards you need by the yards on one skein and round up, then add one if you can. Running short is worse than having a spare: a new skein from a different dye lot can show as a stripe. Many shops take back unused skeins, so ask before you buy. Keep track of what's left over in a stash list, and the <a href="{href("projects.html")}">project tracker</a> can hold the yarn details for each piece. For scarves by age and style, the <a href="{href("scarf-size-chart.html")}">scarf size chart</a> gives the size and yarn together, and for jumpers the <a href="{href("sweater-size-calculator.html")}">sweater size calculator</a> picks the size with the right ease and estimates the yarn.</p></div></section>'''
yc_faq = [
    ("How many skeins do I need for a blanket?", "A throw of about 125 by 150 cm (50 by 60 in) usually takes around 1,800 to 2,200 yards of worsted yarn when knitted, which is often 9 to 11 skeins of 200 yards. Crochet takes more. For other blanket sizes, use the blanket size calculator."),
    ("How do I work out yarn for a project that isn't listed?", "Pick a similar project in the list and adjust, or use a swatch: weigh a 10 cm (4 in) square, multiply by how many squares fit your piece to get the grams, then use the yards per gram on your yarn label. Add about 10 percent for seams and borders."),
    ("Does crochet use more yarn than knitting?", "Usually yes, often about 25 to 30 percent more for the same size piece, because crochet stitches are taller and denser."),
    ("Why does thinner yarn need more yards?", "Thin yarn makes small stitches, so you need many more of them, and much more length, to cover the same area."),
    ("How much yarn do I need for a beanie?", f"About {yc_yd('hat', 4)} yards of worsted yarn for a knitted adult beanie, about {yc_yd('hat', 5)} in bulky and about {yc_yd('hat', 3)} in DK. Crochet takes roughly a quarter more. These are estimates, so check your pattern."),
    ("How much yarn do I need for a scarf?", f"About {yc_yd('scarf', 4)} yards of worsted for a knitted scarf about 6 ft long, or about {yc_yd('scarf', 4, 1.27)} yards crocheted. Bulky yarn needs about {yc_yd('scarf', 5)} yards."),
]
page("yarn-calculator.html", "Yarn Calculator: How Much Yarn Do I Need? | Purl & Paper",
     "Free yarn calculator for knitting and crochet. Pick your project, size and yarn weight to see how many yards, metres and skeins you need.",
     yc, yc_faq, "Yarn calculator", app_name="Yarn calculator")

# ---------------- GAUGE ----------------
def _gc_w(sts, pg, yg): return sts / (yg / 4)
GC_ROWS = [(g, int(20 * g / 4)) for g in (12, 16, 18, 20, 22, 24, 28)]
gc_tbl = "".join(f"<tr><td><strong>{g} sts</strong> ({g / 4:g} per in)</td><td>{n}</td>" + "".join(f"<td>{_gc_w(n, g, g + d):.1f} in</td>" for d in (-2, -1, 1, 2)) + "</tr>" for g, n in GC_ROWS)
gc = top("Gauge converter", "Your swatch came out different from the pattern? See how big your piece will turn out, and how many stitches and rows to use instead.", "Gauge converter") + '''
<section style="padding-top:10px"><div class="wrap"><div class="quick"><strong>Quick answer:</strong> finished width = <strong>stitches ÷ your stitches per inch</strong>. A pattern with 100 stitches at 20 sts per 4 in (5 per inch) comes out 20 in wide. If your swatch has 18 sts per 4 in (4.5 per inch), the same 100 stitches make <strong>22.2 in</strong>. More stitches than the pattern: go <strong>up</strong> a needle or hook size. Fewer: go <strong>down</strong> a size. Or keep your gauge and change the numbers below.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><span class="label" id="gc-u-l">Gauge measured over</span><div class="seg" role="group" aria-labelledby="gc-u-l" id="gc-unit"><button type="button" data-v="in" aria-pressed="true">4 inches</button><button type="button" data-v="cm" aria-pressed="false">10 cm</button></div></div>
<h3 style="margin-top:8px">The pattern's gauge</h3>
<div class="row2"><div class="field"><label for="gc-ps">Stitches</label><input type="number" id="gc-ps" value="20" min="1" step="0.5" inputmode="decimal"></div><div class="field"><label for="gc-pr">Rows</label><input type="number" id="gc-pr" value="28" min="1" step="0.5" inputmode="decimal"></div></div>
<h3>Your swatch</h3>
<div class="row2"><div class="field"><label for="gc-ys">Stitches</label><input type="number" id="gc-ys" value="18" min="1" step="0.5" inputmode="decimal"></div><div class="field"><label for="gc-yr">Rows</label><input type="number" id="gc-yr" value="26" min="1" step="0.5" inputmode="decimal"></div></div>
<h3>From the pattern</h3>
<div class="row2"><div class="field"><label for="gc-cast">Stitches to cast on or chain</label><input type="number" id="gc-cast" value="100" min="1" inputmode="numeric"></div><div class="field"><label for="gc-len">Rows to work</label><input type="number" id="gc-len" value="140" min="1" inputmode="numeric"></div></div>
</div>
<div class="result" aria-live="polite" id="gc-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>Should I change needles or the numbers?</h2>
<p>If you have <strong>more</strong> stitches than the pattern, your fabric is tighter: go up a needle or hook size. If you have <strong>fewer</strong>, it's looser: go down a size. Changing tool size is usually the best first fix, because it keeps the fabric feel the designer intended.</p>
<p>If you love your fabric as it is, use the new stitch and row numbers above instead. Round to suit your stitch pattern: if it repeats over 4 stitches, pick the nearest multiple of 4.</p>
<div class="callout">Measure your swatch after washing and drying it the way you'll treat the finished piece. Many yarns grow or shrink a little.</div>
<h2>How much does one stitch off change the size?</h2>
<p>Each row of the table is a piece that should be 20 in (51 cm) wide at the pattern's gauge. The columns show how wide it really comes out if your swatch has 1 or 2 stitches more or fewer over 4 in.</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Pattern gauge (per 4 in)</th><th scope="col">Stitches for 20 in</th><th scope="col">You get 2 fewer</th><th scope="col">1 fewer</th><th scope="col">1 more</th><th scope="col">2 more</th></tr></thead><tbody>''' + gc_tbl + '''</tbody></table></div>
<p class="note">Plain maths: stitches ÷ (your stitches over 4 in ÷ 4). The thicker the yarn, the more one stitch matters.</p>
<h2>What does "20 sts and 28 rows = 4 in" mean?</h2>
<p>It's the pattern's gauge (tension in the UK): in a square of the fabric 4 in (10 cm) across, there are 20 stitches side to side and 28 rows top to bottom, with the needle or hook size given and usually after blocking. It tells you the size the designer's numbers will make.</p>
<h2>Does row gauge matter?</h2>
<p>Less than stitch gauge, for most patterns, because they usually say "work until the piece measures 10 in" rather than give a row count. It does matter when the pattern counts rows (raglan sleeves, top-down yokes, colourwork charts, crochet worked to a set number of rows) and for how much yarn you use. If only your rows are off, keep your needle and work to the length instead of the row count.</p>
<h2>How do I measure a swatch?</h2>
<ol><li>Make a swatch at least 6 inches (15 cm) wide in the stitch the pattern uses for its gauge, with the same needles or hook.</li>
<li>Wash and dry it, then lay it flat without stretching.</li>
<li>Count the stitches across 4 inches (10 cm) in the middle, away from the edges. Count half stitches too.</li>
<li>Do the same for rows, measuring up and down.</li></ol>
<p>For hats, socks and anything else worked in the round, knit the swatch in the round too if you can. Many knitters purl a little looser than they knit, so a flat swatch can give a slightly different number.</p>
<h2>Gauge for a hat or a sweater</h2>
<p>Small differences add up on fitted pieces. On a 20 inch hat, being half a stitch per inch off changes the size by about 2 inches. Got your stitches per inch? The <a href="@@HAT@@">hat size calculator</a> turns them into a cast-on count for any head size, and the <a href="@@YW@@">yarn weight chart</a> shows the usual gauge for each yarn.</p>
<p>What next? Turn your gauge into a starting number with the <a href="''' + href("cast-on-calculator.html") + '''">cast on calculator</a> or, for crochet, the <a href="''' + href("foundation-chain-calculator.html") + '''">foundation chain calculator</a>, and see how much yarn the new size takes with the <a href="''' + href("yarn-calculator.html") + '''">yarn calculator</a>. Making a jumper? The <a href="''' + href("sweater-size-calculator.html") + '''">sweater size calculator</a> picks the size with the right ease.</p></div></section>'''
gc = gc.replace("@@HAT@@", href("hat-size-chart.html")).replace("@@YW@@", href("yarn-weights.html"))
gc_faq = [
    ("How do I measure gauge in crochet?", "Crochet a swatch at least 6 inches wide in the pattern's stitch, block it, then count the stitches and rows over 4 inches (10 cm) in the middle. Include half stitches."),
    ("What is gauge in knitting and crochet?", "Gauge (called tension in the UK) is how many stitches and rows fit in a set width, usually 4 inches or 10 cm. Matching it is what makes a garment come out the size the pattern says."),
    ("Does gauge matter for scarves and blankets?", "Less. A scarf a little wider is usually fine, but it changes how much yarn you need. For fitted garments, hats and socks it matters a lot."),
    ("Why is my gauge different from the pattern?", "Everyone holds yarn with a different tension, and needle materials and yarn brands vary. That's normal, which is why patterns ask you to swatch."),    ("How do I work out the finished size from my gauge?", "Divide the number of stitches by your stitches per inch. 100 stitches at 4.5 stitches per inch make a piece about 22.2 in wide."),
    ("If I have too many stitches, do I go up or down a needle size?", "Up. More stitches per 4 in means your fabric is tighter than the pattern's, so a bigger needle or hook makes bigger stitches. Too few stitches: go down a size."),
    ("Does row gauge matter?", "Less than stitch gauge for most patterns, which say to work to a length. It matters when a pattern counts rows, such as raglans, yokes, charts and crochet worked to a set number of rows."),
]
page("gauge-converter.html", "Gauge Converter for Knitting and Crochet | Purl & Paper",
     "Free knitting and crochet gauge converter. Compare your swatch to the pattern, see the finished size, and get new stitch and row counts.",
     gc, gc_faq, "Gauge converter", app_name="Gauge converter", scripts=f'<script src="{asset("knit.js")}"></script>')

# ---------------- PROJECTS ----------------
pj = top("Project tracker", "Every work in progress in one place. Note the yarn, the hook or needles, how far you've got, and anything you'll want to remember next time.", "Project tracker") + '''
<section style="padding-top:10px"><div class="wrap">
<details class="sheet proj-form" id="pj-details" open><summary style="cursor:pointer;font:800 1.25rem var(--display)">Add a project</summary>
<form id="pj-form" style="margin-top:16px">
<div class="row2"><div class="field"><label for="pj-name">Project name</label><input type="text" id="pj-name" required placeholder="Sunday cardigan"></div>
<div class="field"><label for="pj-craft">Craft</label><select id="pj-craft"><option>Knitting</option><option>Crochet</option><option>Junk journal</option><option>Other</option></select></div></div>
<div class="row2"><div class="field"><label for="pj-yarn">Yarn or materials</label><input type="text" id="pj-yarn" placeholder="Worsted wool, 5 skeins, colour Moss"></div>
<div class="field"><label for="pj-tool">Hook or needles</label><input type="text" id="pj-tool" placeholder="5 mm circular"></div></div>
<div class="row2"><div class="field"><label for="pj-link">Pattern link (optional)</label><input type="url" id="pj-link" placeholder="https://"></div>
<div class="field"><label for="pj-start">Started</label><input type="date" id="pj-start"></div></div>
<div class="row2"><div class="field"><label for="pj-status">Status</label><select id="pj-status"><option>Planned</option><option selected>In progress</option><option>Finished</option><option>Frogged</option></select></div>
<div class="field"><label for="pj-prog">How far along (%)</label><input type="number" id="pj-prog" min="0" max="100" value="0" inputmode="numeric"></div></div>
<div class="field"><label for="pj-notes">Notes</label><textarea id="pj-notes" placeholder="Changed to 4.5 mm for the ribbing. Sleeves: decrease every 8th row."></textarea></div>
<button type="submit" class="btn gold">Save project</button> <button type="button" class="btn ghost" id="pj-cancel" hidden>Cancel editing</button>
</form></details>
<div class="toolbar"><div class="seg" role="group" aria-label="Show projects" id="pj-filter"><button type="button" data-v="" aria-pressed="true">All</button><button type="button" data-v="Planned" aria-pressed="false">Planned</button><button type="button" data-v="In progress" aria-pressed="false">In progress</button><button type="button" data-v="Finished" aria-pressed="false">Finished</button></div>
<span class="spacer"></span><button type="button" class="btn ghost sm" id="pj-export">Back up my projects</button><label class="btn ghost sm" for="pj-import" style="margin:0">Restore a backup</label><input type="file" id="pj-import" accept="application/json" hidden></div>
<div class="proj-list" id="pj-list"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>Getting the most from the tracker</h2>
<p>Write down anything you changed from the pattern the moment you change it: a different hook for the ribbing, an extra repeat on the sleeves, the colour you swapped in. Six weeks later, when you start the second sock or the matching mitten, that note saves you from guessing.</p>
<p>Keep the yarn label details too: the brand, colour name and dye lot. If you run short, the dye lot is what lets you find a skein that matches.</p>
<h2>Selling what you make?</h2>
<p>Note the hours and the cost of the yarn as you go. Those two numbers are most of a fair price, and our guide on <a href="@@PR@@">how to price crochet and knitting items</a> turns them into one, Etsy and craft fair fees included.</p>
<h2>Making gifts this year?</h2>
<p>Add each gift as a planned project, then check the timing in our <a href="@@GP@@">handmade gift planner</a>. It adds up the hours for every hat, scarf and blanket on your list and tells you whether they'll be finished by Christmas or another deadline. For how much yarn each one needs, use the <a href="@@YC@@">yarn calculator</a>.</p></div></section>'''.replace("@@PR@@", href("how-to-price-crochet-items.html")).replace("@@GP@@", href("crochet-knitting-gift-planner.html")).replace("@@YC@@", href("yarn-calculator.html"))
pj_faq = [
    ("Where are my projects saved?", "On this device, in your browser. Nothing is uploaded. Use 'Back up my projects' to download a file you can restore on another phone or computer."),
    ("What does 'frogged' mean?", "Frogging is pulling a project out to reuse the yarn. It comes from 'rip it, rip it', which sounds like a frog."),
    ("How do I keep track of several knitting projects at once?", "Give each one its own entry with the yarn, needle or hook size and a note of exactly where you stopped, like 'row 14 of the chart, right side next'. Set planned gifts to 'Planned' so you can see what's still to start."),
]
page("projects.html", "Knitting and Crochet Project Tracker (Free) | Purl & Paper",
     "Keep track of every knitting, crochet and journal project: yarn, hook or needle size, progress and notes. Free, private, saved on your device.",
     pj, pj_faq, "Project tracker", app_name="Project tracker")

# ---------------- PROMPTS ----------------
jp = top("Junk journal prompts", "Shuffle a whole spread: a theme, something to glue in, a technique to try, a colour palette and a question to write about. Lock the parts you like and shuffle the rest.", "Journal prompts") + '''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> a good junk journal prompt gives you a theme, one thing to glue in and one question to write about. Try "The first frost of the year" with a Christmas card envelope, and write about the smell of winter where you live. Press shuffle for a whole spread, or pick a season below for winter, Christmas, new year, spring, summer, autumn, memory or self-care prompts.</div>
<div class="toolbar"><label class="jp-sea-l" for="jp-season">Prompts for</label><select id="jp-season" class="jp-sea"><option value="">Any time of year</option>@@SETOPTS@@</select><button type="button" class="btn gold" id="jp-go">Shuffle my spread</button><button type="button" class="btn ghost" id="jp-save">Save this spread</button><button type="button" class="btn ghost" id="jp-print">Print</button></div>
<div class="journal" id="jp-spread" aria-live="polite">
<div class="jpage left">
<div class="jp jp-torn"><div class="k">Theme <button type="button" class="lock" data-lock="theme" aria-pressed="false" aria-label="Lock this">Lock</button></div><div class="v" data-slot="theme"></div></div>
<div class="jp jp-ticket"><div class="k">Glue this in <button type="button" class="lock" data-lock="ephemera" aria-pressed="false" aria-label="Lock this">Lock</button></div><div class="v" data-slot="ephemera"></div><span class="tk-no" aria-hidden="true">No. 0427</span></div>
</div>
<div class="jpage right">
<div class="jp jp-tag"><div class="k">Try this <button type="button" class="lock" data-lock="technique" aria-pressed="false" aria-label="Lock this">Lock</button></div><div class="v" data-slot="technique"></div></div>
<div class="jp jp-chips"><div class="k">Colour palette <button type="button" class="lock" data-lock="palette" aria-pressed="false" aria-label="Lock this">Lock</button></div><div data-slot="palette"></div></div>
<div class="jp jp-note"><div class="k">Write about <button type="button" class="lock" data-lock="write" aria-pressed="false" aria-label="Lock this">Lock</button></div><div class="v" data-slot="write"></div></div>
</div>
</div>
<h2 style="margin-top:46px">Saved spreads</h2>
<div class="saved" id="jp-saved"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>Junk journal prompts by season</h2>
<p class="muted">Every prompt the shuffle uses for each season, so you can pick one, print the page or plan a month of spreads.</p>
<div class="jp-lists">@@SETLISTS@@</div></div></section>
@@AD@@
<section style="padding-top:0"><div class="narrow prose"><h2>How do you use a junk journal prompt?</h2>
<ol><li><strong>Pick one prompt</strong> and read it twice. Don't wait for the perfect idea.</li>
<li><strong>Choose a background:</strong> a book page, a tea-stained sheet or a scrap of packaging.</li>
<li><strong>Add the focal piece</strong>: the ephemera the prompt suggests, or the closest thing in your stash.</li>
<li><strong>Write a few lines</strong> on a tag, card or envelope. Short is fine.</li>
<li><strong>Finish with one small detail</strong>: washi tape, a stamp, a stitched edge or a date.</li></ol>
<h2>Using prompts without getting stuck</h2>
<p>Treat a prompt as a starting point, not a rule. If "a ticket stub" isn't in your stash, use anything with printed numbers on it. If the palette doesn't suit the theme, keep just one colour from it.</p>
<p>A good rhythm for a two-page spread: lay down a background paper, add one big focal piece, tuck in something interactive (a pocket, flap or tag), and finish with a few words. New to all this? Start with our <a href="@@JJ@@">junk journaling guide for beginners</a>, and age your own background papers with our guide to <a href="@@TS@@">tea staining paper</a>.</p>
<h2>How often should you journal?</h2>
<p>As often as you enjoy it. Some people make one spread a week, others one page a day through December. A prompt a day works well for a month-long project like December Daily, because each page stays small and you don't have to decide what to make.</p>
<h2>What if I don't like writing?</h2>
<p>Skip the writing prompt and answer it with a picture, a list of three words or a single date. A junk journal is a scrapbook as much as a diary, and plenty of pages have no writing at all.</p>
<p>What next? Read the <a href="@@JJ@@">beginner's guide to junk journaling</a> (with a free supply checklist), age papers with the <a href="@@TS@@">tea staining guide and shade tester</a>, find things to glue in with our <a href="@@EP@@">ephemera ideas checklist</a>, and keep your journal and yarn projects in one place with the <a href="@@PJ@@">project tracker</a>.</p></div></section>'''
jp_faq = [
    ("What do you put in a junk journal?", "Anything flat and paper-like that you'd normally throw away: receipts, tickets, envelopes, tea bags, packaging, book pages, plus photos, washi tape, fabric and your own writing."),
    ("How do I get ideas for junk journal pages?", "Pick one theme and one thing to glue in, then build around them. The shuffle above does this for you, and you can lock what you like."),
    ("What are some winter or Christmas junk journal prompts?", "Try the first frost of the year, your favourite Christmas tradition, cards that came through the door, or a recipe that means Christmas to you. Glue in a card envelope, a gift tag or a strip of wrapping paper."),
    ("What should I write in a junk journal?", "Short answers to simple questions work best: what made you smile today, a smell that takes you back, a story someone in your family always tells. A list or a few words on a tag is enough."),
    ("How often should I use journal prompts?", "As often as you like. One spread a week is a relaxed pace; a prompt a day suits month-long projects like December Daily."),
]
_sets = D["prompts"]["sets"]
jp_setopts = "".join(f'<option value="{x["id"]}">{e(x["name"])}</option>' for x in _sets)
jp_lists = "".join(f'<div class="sheet jp-list"><h3>{e(x["name"])} prompts</h3><p class="k">Themes</p><ul>' + "".join(f"<li>{e(t)}</li>" for t in x["theme"]) +
                   '</ul><p class="k">Glue in</p><ul>' + "".join(f"<li>{e(t)}</li>" for t in x["ephemera"]) + '</ul><p class="k">Write about</p><ul>' + "".join(f"<li>{e(t)}</li>" for t in x["write"]) + "</ul></div>" for x in _sets)
jp = jp.replace("@@SETOPTS@@", jp_setopts).replace("@@SETLISTS@@", jp_lists).replace("@@AD@@", AD.format("jp-mid"))
jp = jp.replace("@@JJ@@", href("junk-journal-beginners.html")).replace("@@TS@@", href("how-to-tea-stain-paper.html")).replace("@@PJ@@", href("projects.html")).replace("@@EP@@", href("junk-journal-ephemera-ideas.html"))
page("journal-prompts.html", "Junk Journal Prompts: Generator + Winter, Christmas and Seasonal Ideas | Purl & Paper",
     "Free junk journal prompt generator with winter, Christmas, new year, spring, summer, autumn, memory and self-care prompts. Shuffle a theme, ephemera, technique, palette and question.",
     jp, jp_faq, "Journal prompts", app_name="Junk journal prompt generator")

# ---------------- YARN WEIGHTS ----------------
# (n, name, WPI text, wpi lo, wpi hi, m per 100 g text, yd per 100 g text, UK, AU/NZ, m lo, m hi). WPI and length: Yarn.com (WEBS) chart; names: Yarn.com, LoveCrafts, Wikipedia.
YW_ID = [(0, "Lace", "18 or more", 19, 99, "700 or more", "770 or more", "1 or 2 ply, cobweb", "2 ply", 700, 9999),
         (1, "Fingering", "14 to 18", 14, 18, "350 to 460", "380 to 500", "4 ply", "4 ply", 350, 460),
         (2, "Sport", "12 to 14", 12, 14, "240 to 350", "260 to 380", "5 ply (rare in the UK)", "5 ply", 240, 350),
         (3, "DK", "11 to 12", 11, 12, "180 to 240", "200 to 260", "DK (double knitting)", "8 ply", 180, 240),
         (4, "Worsted", "9 to 11", 9, 11, "140 to 180", "150 to 200", "Aran (a little thicker)", "10 ply", 140, 180),
         (5, "Bulky", "7 to 9", 7, 9, "90 to 140", "100 to 150", "Chunky", "12 ply", 90, 140),
         (6, "Super bulky", "5 to 6", 5, 6, "50 to 90", "55 to 100", "Super chunky", "14 ply", 50, 90),
         (7, "Jumbo", "4 or fewer", 0, 4, "under 50", "under 55", "Jumbo, giant", "16 ply and up", 0, 50)]
rows = "".join(f'<tr id="w{w["n"]}"><td><span class="wnum">{w["n"]}</span></td><td><strong>{e(w["name"])}</strong><br><span class="muted">{e(w["also"])}</span></td><td>{e(w["uk"])}</td><td>{e(w["knit"])} sts</td><td>{e(w["needle"])}</td><td>{e(w["croc"])}</td><td>{e(w["hook"])}</td><td>{e(w["use"])}</td></tr>' for w in D["weights"])
thick = "".join(f'<figure><i style="height:{14 + w["n"] * 6}px"></i>{w["n"]}</figure>' for w in D["weights"])
yw = top("Yarn weight chart", "Yarn is grouped from 0 (thinnest) to 7 (thickest). Find the number on your label, or the name in your pattern, to see the needle and hook size to start with.", "Yarn weight chart") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> yarn weight means thickness, numbered from <strong>0 Lace</strong> to <strong>7 Jumbo</strong>. The three most used are <strong>DK (3)</strong>, knit on about 4 mm needles and called 8 ply in Australia; <strong>worsted or aran (4)</strong>, about 5 mm needles or a 5.5 to 6.5 mm hook, 10 ply; and <strong>bulky or chunky (5)</strong>, 12 ply. No label? Count wraps per inch: about 11 to 12 is DK and 9 to 11 is worsted. The finder below works it out from wraps or from the label.</div>
<div class="thick" aria-hidden="true">{thick}</div><p class="note">Strand thickness, drawn to show the steps. Not to scale.</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">#</th><th scope="col">Weight</th><th scope="col">UK / AU name</th><th scope="col">Knit gauge (4 in / 10 cm)</th><th scope="col">Needles</th><th scope="col">Crochet gauge (4 in / 10 cm)</th><th scope="col">Hook</th><th scope="col">Good for</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Based on the Craft Yarn Council's Standard Yarn Weight System. These are starting points: lace patterns often use bigger needles than the chart suggests, and your own tension changes things too.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">What weight is my yarn?</h2>
<div class="field"><label>I know the</label><div class="seg" id="yw-mode" role="group" aria-label="Find the weight from"><button type="button" data-v="label" aria-pressed="true">Label length and weight</button><button type="button" data-v="wpi" aria-pressed="false">Wraps per inch</button></div></div>
<div id="yw-label"><div class="row2"><div class="field"><label for="yw-len">Length per ball</label><input id="yw-len" type="number" min="1" step="any" value="218" inputmode="decimal"></div><div class="field"><label for="yw-lu">Unit</label><select id="yw-lu"><option value="yd" selected>yards</option><option value="m">metres</option></select></div></div>
<div class="row2"><div class="field"><label for="yw-g">Ball weight</label><input id="yw-g" type="number" min="1" step="any" value="100" inputmode="decimal"></div><div class="field"><label for="yw-gu">Unit</label><select id="yw-gu"><option value="g" selected>grams</option><option value="oz">ounces</option></select></div></div></div>
<div id="yw-wpi" hidden><div class="field"><label for="yw-w">Wraps in one inch</label><input id="yw-w" type="number" min="1" max="60" step="1" value="10" inputmode="numeric"></div>
<p class="note">Wrap the yarn round a pencil or ruler, snug but not stretched, strands touching but not overlapping, and count the wraps in 1 in (2.5 cm). Count over 2 in and halve it for a truer number.</p></div>
<figure class="ts-fig"><svg id="yw-svg" viewBox="0 0 300 110" role="img" aria-label="Yarn weights 0 to 7 with your yarn marked"></svg></figure>
</div>
<div class="result" aria-live="polite" id="yw-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How do I tell a yarn's weight without a label?</h2>
<p>Count the <strong>wraps per inch</strong> (WPI). Wrap the yarn snugly round a ruler or pencil for one inch, strands touching but not overlapping, and count. If you still have the label, divide the length by the weight instead: the more metres per 100 g, the thinner the yarn. Typical ranges:</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">#</th><th scope="col">Weight</th><th scope="col">Wraps per inch</th><th scope="col">Metres per 100 g</th><th scope="col">Yards per 100 g</th></tr></thead><tbody>
{"".join(f'<tr><td><span class="wnum">{r[0]}</span></td><td>{r[1]}</td><td>{r[2]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>' for r in YW_ID)}</tbody></table></div>
<p class="note">Wraps per inch and metres per 100 g from Yarn.com's yarn weight chart (WEBS); yards rounded from those. Wikipedia's yarn weight table gives slightly different, overlapping ranges, so a yarn on the edge of two weights can be either. Fluffy, loosely spun and very dense yarns break the pattern: swatch to be sure.</p>
<h2>What are the UK and Australian names for yarn weights?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">US name (#)</th><th scope="col">UK name</th><th scope="col">Australia / NZ</th></tr></thead><tbody>
{"".join(f'<tr><td>{r[1]} ({r[0]})</td><td>{r[7]}</td><td>{r[8]}</td></tr>' for r in YW_ID)}</tbody></table></div>
<p class="note">From Yarn.com, LoveCrafts and Wikipedia's yarn weight table. In Australia and New Zealand "ply" is a thickness name, not a count of strands.</p>
<h2>Is DK the same as 8 ply? Is worsted the same as aran?</h2>
<p>DK (double knitting) is called 8 ply in Australia and New Zealand, so yes. Worsted and aran are both weight 4, but aran is a touch thicker, so check your gauge if you swap one for the other in a fitted garment. Chunky is the UK name for bulky (5), and 12 ply in Australia.</p>
<p>Planning a blanket? The <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a> turns your yarn weight and blanket size into yards and skeins.</p>
<h2>Can I swap one yarn for another?</h2>
<p>Stay in the same weight number, then knit or crochet a swatch. Two yarns in the same category can still differ, so check the length per 100 g on both labels: if they're close, the swap usually works. The <a href="{href("yarn-substitution-calculator.html")}">yarn substitution calculator</a> does the maths and tells you how many balls to buy, including when you hold two strands together. Got a ball with no label? Weigh it in the <a href="{href("yarn-yardage-calculator.html")}">yarn yardage calculator</a> to see how many yards are left.</p>
<p>What next? Check the hook or needle to start with on the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>, see how much you'll need with the <a href="{href("yarn-calculator.html")}">yarn calculator</a>, and fix a swatch that's off with the <a href="{href("gauge-converter.html")}">gauge converter</a>.</p></div></section>'''
yw_faq = [
    ("Is DK the same as worsted?", "No. DK is weight 3 (light) and worsted is weight 4 (medium), so worsted is a bit thicker. In the UK, aran is close to worsted."),
    ("What weight is 4 ply yarn?", "In the UK and Australia, 4 ply is about the same as US fingering, weight 1 (super fine)."),
    ("What does 'weight' mean if it's not grams?", "Yarn weight means thickness, not how heavy the ball is. A 100 g ball can be lace or super bulky."),
    ("How many wraps per inch is worsted yarn?", "About 9 to 11 wraps per inch. DK is about 11 to 12, and bulky about 7 to 9. Yarns on a boundary can be either weight, so swatch."),
    ("What is 8 ply yarn in the US?", "8 ply is the Australian and New Zealand name for DK, US weight 3 (light). 10 ply is worsted or aran, and 12 ply is bulky or chunky."),
    ("How can I tell the weight from the yarn label?", "Divide the length by the ball weight. About 180 to 240 metres per 100 g is DK, 140 to 180 is worsted, and 90 to 140 is bulky."),
]
page("yarn-weights.html", "Yarn Weight Chart: Lace to Jumbo, Needle and Hook Sizes | Purl & Paper",
     "Yarn weight chart from 0 lace to 7 jumbo: US, UK and Australian (ply) names, wraps per inch, metres per 100 g, gauge, needle and hook sizes. With a finder: what weight is my yarn?",
     yw + f'''<section><div class="wrap"><div class="aff-box"><h3>Need hooks, needles or yarn?</h3><ul class="aff-links"><li><a href="/go/crochet-hooks" rel="sponsored nofollow noopener" target="_blank">Crochet hooks</a></li><li><a href="/go/knitting-needles" rel="sponsored nofollow noopener" target="_blank">Knitting needles</a></li><li><a href="/go/yarn-by-weight" rel="sponsored nofollow noopener" target="_blank">Yarn by weight</a></li><li><a href="/go/free-patterns" rel="sponsored nofollow noopener" target="_blank">Free patterns</a></li></ul>{AFF_NOTE}</div></div></section>''', yw_faq, "Yarn weight chart", app_name="Yarn weight finder", scripts=f"<script>window.YWID={json.dumps([[r[0], r[1], r[3], r[4], r[9], r[10]] for r in YW_ID])};</script>")

# ---------------- HOOK / NEEDLE SIZES ----------------
srows = "".join(f'<tr data-mm="{e(s[0][:-3])}"><td><strong>{e(s[0])}</strong></td><td>{e(s[1])}</td><td>{e(s[2])}</td><td>{e(s[3])}</td></tr>' for s in D["sizes"])
hw_rows = "".join(f'<tr><td><strong>{w["n"]} {e(w["name"])}</strong><br><span class="muted">{e(w["also"])}</span></td><td>{e(w["needle"])}</td><td>{e(w["hook"])}</td></tr>' for w in D["weights"])
hn = top("Hook and needle size chart", "Metric, US and old UK sizes side by side. Type any size to jump to it.", "Hook and needle sizes") + f'''
<section style="padding-top:10px"><div class="narrow">
<div class="quick"><strong>Quick answer:</strong> go by the millimetre size. A 5 mm hook is a US H-8; a 5 mm knitting needle is a US 8 and an old UK 6. A 4 mm needle is a US 6 (UK 8), and a 4 mm hook is a G-6. For worsted yarn most people start with a 5.5 mm (I-9) hook or 4.5 to 5.5 mm (US 7 to 9) needles.</div>
<div class="finder"><div class="field"><label for="hn-q">Find a size</label><input type="search" id="hn-q" placeholder="e.g. 4.5, US 8, H-8, UK 6"></div><p class="note" id="hn-hit" style="margin:0 0 12px"></p></div>
<div class="tbl-wrap"><table id="hn-table"><thead><tr><th scope="col">Metric</th><th scope="col">US knitting needle</th><th scope="col">Old UK / Canadian needle</th><th scope="col">US crochet hook</th></tr></thead><tbody>{srows}</tbody></table></div>
<p class="note" style="margin-top:12px">"—" means there's no common size at that point. Brands sometimes label in-between sizes differently, so the millimetre size is the one to trust.</p>
</div></section>
<section style="padding-top:0"><div class="narrow"><h2>Which hook or needle size for each yarn weight?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Yarn weight</th><th scope="col">Knitting needles</th><th scope="col">Crochet hook</th></tr></thead><tbody>{hw_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Recommended starting ranges from the Craft Yarn Council's Standard Yarn Weight System. Your yarn label and your swatch come first: if you have too many stitches, go up a size; too few, go down. More detail on each weight is on the <a href="{href("yarn-weights.html")}">yarn weight chart</a>.</p></div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>Why go by millimetres?</h2>
<p>US letters and numbers, and old UK numbers, were never fully standard, and the old UK system runs backwards (a bigger number means a thinner needle). The metric size is printed on almost every modern hook and needle, so if a pattern gives a millimetre size, use that.</p>
<h2>Are steel crochet hooks sized differently?</h2>
<p>Yes. Tiny steel hooks for crochet thread use their own numbers, where a <strong>higher</strong> number is a <strong>smaller</strong> hook. Check the millimetre size on the handle.</p>
<h2>What size needles for socks?</h2>
<p>Most socks in fingering yarn are knitted on 2.25 to 2.75 mm needles (US 1 to 2), smaller than the yarn label often suggests, so the fabric is firm and hard-wearing. The <a href="{href("sock-size-chart.html")}">sock size chart and calculator</a> turns your gauge into a cast-on number.</p>
<h2>My stitches don't match the pattern. Which way do I change size?</h2>
<ul><li><strong>Too many stitches per 4 in:</strong> your fabric is tight, so go up a needle or hook size.</li>
<li><strong>Too few stitches:</strong> your fabric is loose, so go down a size.</li>
<li>One size step usually changes gauge by about half a stitch per inch, so swatch again after you switch.</li></ul>
<p>What next? The <a href="{href("gauge-converter.html")}">gauge converter</a> shows how big your piece will turn out if you keep your gauge, and the <a href="{href("yarn-calculator.html")}">yarn calculator</a> tells you how much yarn to buy. Following a UK crochet pattern? Check the <a href="{href("crochet-terms.html")}">US and UK crochet terms</a> too, or decode a knitting pattern with the <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a>. Starting a scarf or blanket? The <a href="{href("cast-on-calculator.html")}">cast on calculator</a> turns your gauge into a cast-on number.</p></div></section>'''
hn_faq = [
    ("What size is an H crochet hook?", "An H-8 hook is 5 mm."),
    ("What is a US size 8 knitting needle in mm?", "A US 8 needle is 5 mm, the same as an old UK size 6."),
    ("What size hook for worsted yarn?", "Worsted (weight 4) usually starts with a 5.5 to 6.5 mm hook (I-9 to K-10½). Check your yarn label and swatch."),
    ("What size is a G crochet hook?", "A G-6 hook is 4 mm. Some brands also sell a 4.25 mm G hook, so check the millimetre size on the handle."),
    ("What is a 4 mm knitting needle in US size?", "A 4 mm knitting needle is a US 6, the same as an old UK size 8."),
    ("What size needles for sock yarn?", "Socks in fingering yarn are usually knitted on 2.25 to 2.75 mm needles (US 1 to 2) for a firm fabric."),
    ("Should I go up or down a needle size to get gauge?", "If you have more stitches per 4 inches than the pattern, go up a size. If you have fewer, go down a size, then swatch again."),
]
page("hook-needle-sizes.html", "Crochet Hook Size Chart and Knitting Needle Sizes (mm, US, UK) | Purl & Paper",
     "Crochet hook and knitting needle size conversion chart: metric mm, US numbers and letters, and old UK sizes, with a quick size finder.",
     hn + f'''<section><div class="wrap"><div class="aff-box"><h3>Need hooks, needles or yarn?</h3><ul class="aff-links"><li><a href="/go/crochet-hooks" rel="sponsored nofollow noopener" target="_blank">Crochet hooks</a></li><li><a href="/go/knitting-needles" rel="sponsored nofollow noopener" target="_blank">Knitting needles</a></li><li><a href="/go/yarn-by-weight" rel="sponsored nofollow noopener" target="_blank">Yarn by weight</a></li><li><a href="/go/free-patterns" rel="sponsored nofollow noopener" target="_blank">Free patterns</a></li></ul>{AFF_NOTE}</div></div></section>''', hn_faq, "Hook and needle sizes")

# ---------------- CROCHET TERMS ----------------
trows = "".join(f'<tr><td><strong>{e(t[0])}</strong>{f" ({e(t[1])})" if t[1] else ""}</td><td><strong>{e(t[2])}</strong>{f" ({e(t[3])})" if t[3] else ""}</td><td class="muted">{e(t[4])}</td></tr>' for t in D["terms"])
ct = top("US vs UK crochet terms", "The same stitch has a different name on each side of the Atlantic. Here's the full conversion, and how to tell which terms your pattern uses.", "US vs UK crochet terms") + f'''
<section style="padding-top:10px"><div class="narrow">
<div class="quick" style="margin-top:0"><strong>Quick answer:</strong> UK crochet names are one step "taller" than US names. A UK double crochet (dc) is a US single crochet (sc), a UK half treble (htr) is a US half double (hdc), a UK treble (tr) is a US double (dc), and a UK double treble (dtr) is a US treble (tr). Chain and slip stitch are the same in both. If a pattern has "single crochet" in it, it's written in US terms.</div>
<div class="tbl-wrap"><table><thead><tr><th scope="col">US term</th><th scope="col">UK term</th><th scope="col">Note</th></tr></thead><tbody>{trows}</tbody></table></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How can I tell if a crochet pattern uses US or UK terms?</h2>
<ul><li><strong>Look for "single crochet" or "sc".</strong> UK patterns don't have a single crochet, so if you see one, it's US.</li>
<li><strong>Check the spelling and words.</strong> "Colour", "tension" and "miss" point to a UK pattern; "color", "gauge" and "skip" point to US.</li>
<li><strong>Check the hook sizes.</strong> Letter sizes like H-8 suggest US; millimetres only don't tell you much.</li>
<li><strong>Read the notes at the top.</strong> Most designers say which terms they use.</li></ul>
<h2>Why are US and UK crochet terms different?</h2>
<p>The two systems count differently. Take the shortest stitch: you put the hook in and pull up a loop, so there are 2 loops on the hook, then you yarn over and pull through once to finish. US names count that finishing pull-through (one, so "single crochet"); UK names count the 2 loops on the hook (so "double crochet"). Same stitch, different counting. See every stitch drawn step by step in <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>.</p>
<h2>Crochet abbreviations: US and UK</h2>
<p>These short forms look the same in both kinds of pattern. Only the stitch names in the table above change.</p>
</div><div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Abbreviation</th><th scope="col">Means</th><th scope="col">Note</th></tr></thead><tbody><tr><td><strong>ch</strong></td><td>chain</td><td class="muted">same in both</td></tr><tr><td><strong>sl st</strong></td><td>slip stitch</td><td class="muted">same in both (UK patterns sometimes say ss)</td></tr><tr><td><strong>st(s)</strong></td><td>stitch(es)</td><td class="muted"></td></tr><tr><td><strong>sp</strong></td><td>space</td><td class="muted">e.g. ch-2 sp, the gap under a chain of 2</td></tr><tr><td><strong>rnd</strong></td><td>round</td><td class="muted">worked in a circle or square</td></tr><tr><td><strong>RS / WS</strong></td><td>right side / wrong side</td><td class="muted"></td></tr><tr><td><strong>rep</strong></td><td>repeat</td><td class="muted"></td></tr><tr><td><strong>yo / yoh</strong></td><td>yarn over / yarn over hook</td><td class="muted">US says yo, UK often yoh or yrh</td></tr><tr><td><strong>sk / miss</strong></td><td>skip</td><td class="muted">US skip, UK miss</td></tr><tr><td><strong>inc</strong></td><td>increase</td><td class="muted">2 or more stitches in one stitch</td></tr><tr><td><strong>dec / tog</strong></td><td>decrease / together</td><td class="muted">e.g. sc2tog (US) is dc2tog (UK)</td></tr><tr><td><strong>BLO / FLO</strong></td><td>back loop only / front loop only</td><td class="muted"></td></tr><tr><td><strong>beg</strong></td><td>beginning</td><td class="muted"></td></tr><tr><td><strong>cont</strong></td><td>continue</td><td class="muted"></td></tr><tr><td><strong>FO</strong></td><td>fasten off</td><td class="muted">same in both</td></tr><tr><td><strong>*  *</strong></td><td>repeat the part between the asterisks</td><td class="muted"></td></tr></tbody></table></div></div>
<div class="narrow prose"><h2>Crochet decreases in US and UK terms</h2>
<p>Decreases follow the same one-step shift, because they're named after the stitch they're made from. "2tog" means work two stitches together into one.</p></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">US decrease</th><th scope="col">UK decrease</th><th scope="col">What you do</th></tr></thead><tbody>
<tr><td><strong>sc2tog</strong></td><td><strong>dc2tog</strong></td><td class="muted">Start a stitch in each of the next 2 stitches, then finish them together. Loses 1 stitch.</td></tr>
<tr><td><strong>hdc2tog</strong></td><td><strong>htr2tog</strong></td><td class="muted">The same with half double (half treble) stitches.</td></tr>
<tr><td><strong>dc2tog</strong></td><td><strong>tr2tog</strong></td><td class="muted">The same with double (treble) stitches.</td></tr>
<tr><td><strong>sc3tog</strong></td><td><strong>dc3tog</strong></td><td class="muted">Three stitches into one. Loses 2 stitches.</td></tr>
<tr><td><strong>invisible decrease</strong></td><td><strong>invisible decrease</strong></td><td class="muted">For amigurumi: work through the front loops of 2 stitches only. Same name in both.</td></tr></tbody></table></div></div>
<div class="narrow prose"><h2>Is it a mistake if my pattern is in UK terms?</h2>
<p>No. Both systems describe exactly the same stitches, and neither is "right". The trouble only starts when you read a UK pattern with US names in your head: every stitch comes out one step too tall and the piece grows much bigger and looser than it should. Pick one system per pattern, and if it helps, write the conversions in pencil at the top.</p>
<h2>One granny square round, written both ways</h2>
<p>Here's the second round of a classic granny square. Same stitches, same square, two sets of names.</p>
<p><strong>US terms:</strong> sl st into the ch-2 sp, ch 3 (counts as dc), 2 dc in same sp, ch 1, *(3 dc, ch 2, 3 dc) in next ch-2 corner sp, ch 1; rep from * around, ending with 3 dc in the first sp, ch 2, sl st to top of ch 3.</p>
<p><strong>UK terms:</strong> ss into the ch-2 sp, ch 3 (counts as tr), 2 tr in same sp, ch 1, *(3 tr, ch 2, 3 tr) in next ch-2 corner sp, ch 1; rep from * around, ending with 3 tr in the first sp, ch 2, ss to top of ch 3.</p>
<p>Planning a whole blanket of squares? The <a href="@@GS@@">granny square blanket calculator</a> works out how many squares, the layout and roughly how much yarn. Crocheting in the round? The <a href="@@CI@@">crochet circle calculator</a> gives the stitch count for every round in sc, hdc or dc, and an amigurumi ball pattern.</p>
<p>Learning the basics? See our step-by-step guides to the <a href="@@MR@@">magic ring</a> and <a href="@@CC@@">changing colours in crochet</a>.</p>
<p>What next? Finished? <a href="@@WE@@">Fasten off and weave in your ends</a> so they never poke out. Knit as well? Our <a href="@@KA@@">knitting abbreviations list</a> explains k2tog, ssk, M1 and the rest, and translates a whole pattern line. Working out hook sizes from a UK pattern? See the <a href="@@HN@@">hook and needle size chart</a>, and keep count of rows with the <a href="@@RC@@">row counter</a>.</p></div></section>'''.replace("@@KA@@", href("knitting-abbreviations.html")).replace("@@WE@@", href("how-to-weave-in-ends.html")).replace("@@MR@@", href("how-to-crochet-magic-ring.html")).replace("@@CC@@", href("how-to-change-colors-in-crochet.html")).replace("@@HN@@", href("hook-needle-sizes.html")).replace("@@RC@@", href("row-counter.html")).replace("@@GS@@", href("granny-square-blanket-calculator.html")).replace("@@CI@@", href("crochet-circle-calculator.html"))
ct_faq = [
    ("Is UK double crochet the same as US single crochet?", "Yes. A UK double crochet (dc) is worked exactly like a US single crochet (sc)."),
    ("What is a treble crochet in US terms?", "A UK treble (tr) is a US double crochet (dc). A US treble (tr) is a UK double treble (dtr)."),
    ("What does ch-2 sp mean in crochet?", "It means the space under a chain of 2 made on the round before. You work the new stitches into that gap, not into the chains themselves. It's written the same way in US and UK patterns."),
    ("What is hdc in UK crochet terms?", "A US half double crochet (hdc) is a UK half treble crochet (htr). The stitch is worked the same way."),
    ("What is sc2tog in UK terms?", "A US sc2tog (single crochet 2 together) is a UK dc2tog (double crochet 2 together). It's the same decrease."),
    ("Are Japanese and European crochet patterns US or UK?", "Many use symbol charts instead of words, which read the same everywhere. Written patterns translated into English can use either set of terms, so check the notes or look for 'single crochet'."),
    ("Is a granny square made with double or treble crochet?", "Both, depending on the pattern's terms. A classic granny square uses clusters of US double crochet, which a UK pattern calls treble crochet. The stitch is the same."),
]
page("crochet-terms.html", "US vs UK Crochet Terms and Abbreviations: Conversion Chart | Purl & Paper",
     "US and UK crochet terms side by side: single crochet vs double crochet, treble, half treble and more, common abbreviations, how to tell which a pattern uses, and a granny square round in both.",
     ct, ct_faq, "US vs UK crochet terms")

# ---------------- JUNK JOURNAL BEGINNERS ----------------
jj = top("Junk journaling for beginners", "A junk journal is a handmade book filled with paper you'd normally throw away. Here's how to start one for free, what you need, how to make your first one, and how to fill it.", "Junk journaling for beginners") + f'''
<section style="padding-top:10px"><div class="narrow prose">
<div class="quick"><strong>Quick answer:</strong> to start a junk journal, collect 5 to 8 sheets of mixed paper from around the house (envelopes, book pages, paper bags), fold them in half together, wrap them in a card cover from a cereal box, and sew along the fold with a needle and thread. Then glue in tickets, labels and photos, and write a little. You don't need to buy anything to begin.</div>
<h2>What is a junk journal?</h2>
<p>It's part scrapbook, part diary, part art project. The pages are made from mixed papers like envelopes, book pages, paper bags and packaging, and you decorate them with ephemera (small bits of everyday paper like tickets, receipts and labels). There are no rules about what it should look like, and "messy" is part of the charm.</p>
<h2>What you need to start</h2>
<ul><li><strong>Paper for pages:</strong> envelopes, paper bags, old book or dictionary pages, printer paper stained with tea, cereal box card for covers.</li>
<li><strong>Glue:</strong> a glue stick is enough to start. Matte gel medium or PVA glue holds heavier pieces.</li>
<li><strong>Something to bind with:</strong> a needle, strong thread or thin twine, and a pin or awl to poke holes.</li>
<li><strong>Scissors and a ruler.</strong></li>
<li><strong>Ephemera:</strong> start a box today and drop in anything interesting. Our <a href="{href("journal-prompts.html")}">prompt generator</a> suggests what to use.</li></ul>
<div class="callout">You don't need to buy kits or special paper. Most beginners' first journal is made almost entirely from things already in the house.</div>
<h2>How do I start a junk journal for free?</h2>
<p>Spend a week saving paper instead of recycling it. By the weekend you'll have more than enough for a first journal. Places to look:</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Use it for</th><th scope="col">Free from around the house</th></tr></thead><tbody>
<tr><td>Pages</td><td>Envelopes (the patterned insides too), brown paper bags, old book or dictionary pages, printer paper, sheet music, maps, gift wrap, kraft packing paper</td></tr>
<tr><td>Covers</td><td>Cereal or shoe box card, an old hardback book cover, a folder, fabric scraps glued over card</td></tr>
<tr><td>Ephemera</td><td>Tickets, receipts, tea bag tags, labels, stamps, postcards, seed packets, food packaging with nice type, leaflets</td></tr>
<tr><td>Pockets and tags</td><td>Cut-down envelopes, the corners of envelopes, luggage-style tags cut from card, paper bags folded in half</td></tr>
<tr><td>Decoration</td><td>Ribbon and string from parcels, buttons, lace, pressed leaves and flowers, magazine cut-outs</td></tr>
<tr><td>Binding</td><td>A darning needle, embroidery thread, dental floss or thin twine, a drawing pin to poke holes</td></tr></tbody></table></div>
<p>For a long list of free things to save, see our <a href="{href("junk-journal-ephemera-ideas.html")}">junk journal ephemera ideas</a> checklist. The only things most people end up buying are a glue stick and, later, a few nice papers. If plain paper looks too new, give it an aged look with a cup of tea: our guide to <a href="{href("how-to-tea-stain-paper.html")}">tea staining paper</a> has the recipe and a shade tester.</p>
<h2>Junk journal supply checklist</h2>
<p>Tick these off, pick a budget and print a shopping list with our full <a href="{href("junk-journal-supply-checklist.html")}">junk journal supply checklist</a>.</p>
<ul><li><strong>Must have:</strong> paper for pages, card for a cover, glue stick, scissors, needle and thread, something to poke holes.</li>
<li><strong>Nice to have:</strong> a bone folder or the back of a spoon for crisp folds, a craft knife and ruler, PVA or matte gel medium, washi tape, a waterproof pen.</li>
<li><strong>Later:</strong> an awl, waxed linen thread, ink pads and stamps, a corner rounder, printable kits for themed pages.</li></ul>
<h2>Make your first signature (a small booklet)</h2>
<p>A signature is a stack of folded pages sewn together at the fold. One signature makes a slim journal; several make a thick one.</p>
<ol><li><strong>Gather 5 to 8 sheets</strong> of mixed paper, trimmed roughly to the same size.</li>
<li><strong>Fold them in half together</strong> so they nest inside each other. Press the fold well.</li>
<li><strong>Fold a cover</strong> from thicker card a little bigger than the pages, and put the pages inside it.</li>
<li><strong>Poke three holes</strong> along the fold from the inside: one in the middle, and one about 2 cm (an inch) from each end.</li>
<li><strong>Sew a pamphlet stitch:</strong> go out through the middle hole, back in through the top hole, along the inside and out through the bottom hole, then back in through the middle. Tie the two ends around the long stitch inside and trim.</li></ol>
<h2>Fill the pages</h2>
<ul><li><strong>Start with a background:</strong> glue down a larger piece of paper or fabric.</li>
<li><strong>Add one focal point:</strong> a photo, a label, a big pressed leaf.</li>
<li><strong>Add something to touch:</strong> a pocket from half an envelope, a tag tucked in, a flap that lifts.</li>
<li><strong>Write a little:</strong> a date, a line about the day, a list.</li></ul>
<h2>Easy techniques that look great</h2>
<ul><li><strong>Tea staining:</strong> brush cooled black tea onto paper, or dip it, then dry flat. Coffee gives a darker brown. See <a href="{href("how-to-tea-stain-paper.html")}">how to tea stain paper</a> for the full method.</li>
<li><strong>Torn edges:</strong> tear paper against a ruler for a soft, aged edge.</li>
<li><strong>Layering:</strong> stack three papers from biggest to smallest, slightly off-centre.</li>
<li><strong>Hand stitching:</strong> a running stitch around a photo frames it instantly.</li></ul>
<h2>How do I make a thicker journal?</h2>
<p>Make three to six signatures, then sew each one to a spine made from a strip of card or fabric. Leave room in the spine: a junk journal gets much fatter once the pages are filled. A good first size is half a sheet of letter or A4 paper, folded. Not sure how many sheets or how much thread? The <a href="{href("junk-journal-signature-calculator.html")}">signature calculator</a> works out pages, spine thickness, hole spacing and thread.</p>
<h2>What should I put on the first page?</h2>
<p>Something low-pressure: the date you started, a list of things you saw this week, or one ticket and a sentence about it. Stuck for ideas? The <a href="{href("journal-prompts.html")}">junk journal prompt generator</a> shuffles a theme, a piece of ephemera, a technique and a colour palette for you.</p>
</div></section>'''
jj_faq = [
    ("Do I need special supplies to make a junk journal?", "No. Paper from around the house, a glue stick, a needle and thread are enough for your first one."),
    ("What's the difference between a junk journal and a scrapbook?", "Scrapbooks usually use bought, acid-free supplies and focus on photos. Junk journals are made from recycled paper and everyday ephemera, and mix in writing and art."),
    ("How many pages should a junk journal have?", "There's no rule. A single signature of 5 to 8 folded sheets (20 to 32 pages) is a good first project."),
    ("How do I start a junk journal for free?", "Save paper for a week: envelopes, paper bags, book pages, tickets and packaging. Fold 5 to 8 sheets into a booklet, add a cereal box cover and sew the fold with any needle and strong thread."),
    ("What glue is best for junk journals?", "A glue stick is fine for paper. For heavier pieces like card, fabric or buttons, use PVA glue or matte gel medium, applied thinly so pages don't wrinkle."),
    ("How do I make paper look old for a junk journal?", "Tea stain it: brush or dip the paper in strong cooled black tea, add a sprinkle of instant coffee for spots, and dry it flat. Crumpling first and tearing the edges adds to the aged look."),
]
page("junk-journal-beginners.html", "Junk Journaling for Beginners: How to Start a Junk Journal for Free | Purl & Paper",
     "How to start a junk journal for free: what it is, a supply checklist, where to find free paper and ephemera, how to sew your first signature, and easy techniques to fill the pages.",
     jj, jj_faq, "Junk journaling for beginners")

# ---------------- BLANKET SIZE CALCULATOR ----------------
bopts = "".join(f'<option value="{b["id"]}"{" selected" if b["id"] == "throw" else ""}>{e(b["name"])} ({b["w"]} × {b["l"]} in)</option>' for b in D["blankets"]) + '<option value="custom">My own size</option>'
bw_opts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"])})</option>' for w in D["weights"] if w["n"] >= 1)
brows = "".join(f'<tr><td><strong>{e(b["name"])}</strong></td><td>{b["w"]} × {b["l"]} in</td><td>{round(b["w"] * 2.54)} × {round(b["l"] * 2.54)} cm</td><td>{e(b["range"])}</td><td>{e(b["use"])}</td></tr>' for b in D["blankets"])
BK_M = {w["n"]: w["m"] for w in D["weights"]}
def bk_yd(b, wn, craft=1.0): return b["w"] * b["l"] * 0.667 * BK_M[wn] * craft
def bk_rng(b, wn, craft=1.0): y = bk_yd(b, wn, craft); return f"{round(y * 0.88, -2):,.0f}–{round(y * 1.12, -2):,.0f}"
BK_TW = [(3, "DK"), (4, "Worsted"), (5, "Bulky"), (6, "Super bulky")]
bk_ids = ("baby", "crib", "throw", "twin", "queen", "king")
bk_yrows = "".join(f'<tr><th scope="row">{e(b["name"])}<br><span class="muted">{b["w"]} × {b["l"]} in</span></th>' + "".join(f"<td>{bk_rng(b, k, 1.27)} yd</td>" for k, _ in BK_TW) + f"<td>{bk_rng(b, 4)} yd</td></tr>" for b in D["blankets"] if b["id"] in bk_ids)
_bk_th = [b for b in D["blankets"] if b["id"] == "throw"][0]; _bk_by = [b for b in D["blankets"] if b["id"] == "baby"][0]
bk = top("Blanket size calculator", "Pick a blanket size or type your own, choose your yarn, and see the finished size next to a bed, plus how many yards and skeins to buy.", "Blanket size calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> a throw blanket is usually about <strong>50 × 60 in</strong> (127 × 152 cm), a baby blanket 30 to 40 in square, and a queen bed blanket about 90 × 100 in. A crocheted throw in worsted yarn takes roughly <strong>{bk_rng(_bk_th, 4, 1.27)} yards</strong>, and a knitted one about {bk_rng(_bk_th, 4)} yards. A crocheted baby blanket in DK takes about {bk_rng(_bk_by, 3, 1.27)} yards. These are estimates for plain stitches; use the calculator for your own size and yarn.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="bk-size">Blanket size</label><select id="bk-size">{bopts}</select></div>
<div class="row2" id="bk-custom" hidden><div class="field"><label for="bk-w">Width (in)</label><input type="number" id="bk-w" value="50" min="6" max="140" inputmode="decimal"></div><div class="field"><label for="bk-l">Length (in)</label><input type="number" id="bk-l" value="60" min="6" max="140" inputmode="decimal"></div></div>
<div class="field"><span class="label" id="bk-craft-l">Knitting or crochet?</span><div class="seg" role="group" aria-labelledby="bk-craft-l" id="bk-craft"><button type="button" data-v="knit" aria-pressed="false">Knitting</button><button type="button" data-v="crochet" aria-pressed="true">Crochet</button></div></div>
<div class="field"><label for="bk-weight">Yarn weight</label><select id="bk-weight">{bw_opts}</select></div>
<div class="field"><span class="label" id="bk-dense-l">Stitch pattern</span><div class="seg" role="group" aria-labelledby="bk-dense-l" id="bk-dense"><button type="button" data-v="1" aria-pressed="true">Plain</button><button type="button" data-v="1.15" aria-pressed="false">Textured or cables</button><button type="button" data-v="0.85" aria-pressed="false">Lacy</button></div></div>
<div class="row2"><div class="field"><label for="bk-skein">Length per skein</label><input type="number" id="bk-skein" value="200" min="1" inputmode="decimal"></div>
<div class="field"><label for="bk-unit">Unit on the label</label><select id="bk-unit"><option value="yd">yards</option><option value="m">metres</option></select></div></div>
<figure class="bk-fig"><svg id="bk-svg" viewBox="0 0 320 240" role="img" aria-label="Blanket drawn to scale next to a bed"></svg><figcaption class="note" id="bk-cap">Drawn to scale.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="bk-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>Blanket size chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Blanket</th><th scope="col">Size we use</th><th scope="col">In cm</th><th scope="col">Common range</th><th scope="col">Good for</th></tr></thead><tbody>{brows}</tbody></table></div>
<p class="note" style="margin-top:12px">There is no single official blanket standard. These are the sizes most often quoted by crochet and knitting designers, so patterns can differ by a few inches. Bed sizes include some drop over the sides.</p>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How much yarn do I need for a blanket?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Blanket</th>{"".join(f'<th scope="col">Crochet, {n}</th>' for _, n in BK_TW)}<th scope="col">Knit, worsted</th></tr></thead><tbody>{bk_yrows}</tbody></table></div>
<p class="note" style="margin-top:12px">Our estimates from the calculator's own model for plain stitches, before any border or fringe, as a low to high range. Divide by the yards on your yarn label for skeins, and buy enough for the high end.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How the yarn estimate works</h2>
<p>We work out the blanket's area and multiply it by a typical amount of yarn per square inch for plain worsted knitting, then adjust for your yarn: thinner yarn needs more length, thicker yarn less. Crochet usually takes about a quarter more yarn than knitting, cables and bobbles take more again, and open lace stitches take a little less. Granny squares are a special case, because the joins and border add up: use the <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> for those.</p>
<p>The answer is a range, because tension, stitch and borders all change it. Buy enough for the high end, from one dye lot. For hats, scarves and other projects, use our <a href="{href("yarn-calculator.html")}">yarn calculator</a>, and if your swatch doesn't match the pattern, the <a href="{href("gauge-converter.html")}">gauge converter</a> shows how big the blanket will really be. Knitting it? The <a href="{href("cast-on-calculator.html")}">cast on calculator</a> tells you how many stitches to start with for your width and gauge.</p>
<div class="callout"><strong>Allow for the border.</strong> A few rounds of border can add 5 to 10 percent more yarn on a big blanket. Fringe or tassels add more.</div>
<h2>What size blanket should I make?</h2>
<p>For a gift, a throw (about 50 × 60 in) is the safest choice: it fits a sofa, the foot of a bed or a lap. For a baby, 30 to 36 inches square is easy to carry and wash. For a bed, measure the top of the mattress and add the drop you want on each side, usually 10 to 15 inches.</p>
<p>Making a long blanket? Keep count of rows or rounds with our <a href="{href("row-counter.html")}">row counter</a>, and log yarn and hours in the <a href="{href("projects.html")}">project tracker</a>. Not sure which yarn is which? See the <a href="{href("yarn-weights.html")}">yarn weight chart</a>. Making it from squares? The <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> tells you how many to make.</p>
<h2>How big is a temperature blanket?</h2>
<p>A temperature blanket's length comes from the number of days, not a size chart: 365 rows of single crochet in worsted yarn is roughly 100 in long, longer than a queen bed. Pick the width from the chart above, then check the length, the colours and the yarn for each colour with our <a href="{href("temperature-blanket-planner.html")}">temperature blanket planner</a>.</p>
<h2>How do I make a blanket bigger or smaller?</h2>
<p>For a blanket worked in rows, change the width with the foundation chain or cast-on (the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> or, for crochet, the <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a> does the maths), and the length by working more or fewer rows. Going up one size, say from throw to twin, roughly doubles the yarn, so check the new amount above before you start. Working corner to corner? The <a href="{href("c2c-blanket-calculator.html")}">C2C blanket calculator</a> turns any size here into tiles and rows. Wondering how long it will take? The <a href="{href("crochet-time-estimator.html")}">crochet time calculator</a> gives the hours and a finish date.</p>
<h2>How much should I sell a blanket for?</h2>
<p>Count the skeins from this calculator, add your hours at a fair hourly rate and a little for overheads and fees. Our <a href="{href("how-to-price-a-crochet-blanket.html")}">crochet blanket price calculator</a> estimates the hours too, and has a price chart from lovey to king size.</p></div></section>'''
bk_faq = [
    ("How many yards of yarn for a baby blanket?", f"A crocheted 36 × 36 in baby blanket takes roughly {bk_rng(_bk_by, 3, 1.27)} yards of DK yarn or {bk_rng(_bk_by, 4, 1.27)} yards of worsted. A knitted one takes a little less. These are estimates for plain stitches."),
    ("How long is a temperature blanket?", "One row a day for a year is 365 rows, which is roughly 100 in in worsted single crochet at a typical gauge. Thinner yarn, garter stitch or a square per day keeps it shorter. Our temperature blanket planner works it out for your stitch and gauge."),
    ("What size is a crochet throw blanket?", "Most throws are about 50 × 60 inches (127 × 152 cm). Some patterns go up to 54 × 72 inches for a longer sofa blanket."),
    ("What size is a baby blanket?", "A baby or receiving blanket is usually 30 to 40 inches square. A stroller blanket is a little smaller, about 30 × 36 inches, and a crib blanket can be as big as 45 × 60 inches."),
    ("How much yarn for a queen size crochet blanket?", "Very roughly 6,700 to 8,500 yards of worsted weight yarn for plain crochet, which is often 34 to 43 skeins of 200 yards. Chunky yarn needs far fewer yards. Use the calculator for your own yarn, and treat it as an estimate."),
    ("How many skeins for a throw blanket?", "In worsted yarn, a knitted throw takes roughly 1,800 to 2,200 yards and a crocheted one about 2,300 to 2,800 yards, so roughly 10 to 15 skeins of 200 yards once you allow a little spare. These are estimates."),
]
page("blanket-size-calculator.html", "Blanket Size Chart and Yarn Calculator for Crochet and Knitting | Purl & Paper",
     "Free blanket size chart and calculator: lovey, baby, crib, throw, twin, queen and king sizes in inches and cm, with the yards and skeins for your yarn weight.",
     bk, bk_faq, "Blanket size calculator", app_name="Blanket size calculator")

# ---------------- HANDMADE GIFT PLANNER ----------------
import datetime as _dt
_today = _dt.date.today()
_xmas = _dt.date(_today.year if _today <= _dt.date(_today.year, 12, 25) else _today.year + 1, 12, 25)
GP_DAYS = (_xmas - _today).days
GP_WK = GP_DAYS / 7
_GI = {g["id"]: g for g in D["gifts"]}
GP_HW = [3, 5, 7, 10, 14]
def gp_fit(h, gid, craft): return int(h // _GI[gid][craft])
def gp_n(h, gid, craft, one, many): n = gp_fit(h, gid, craft); return f"{n} {one if n == 1 else many}"
gp_fit_rows = "".join(f'<tr><td><strong>{hw} h a week</strong></td><td>{hw * GP_WK:.0f} h</td><td>{gp_n(hw * GP_WK, "hat", "knit", "hat", "hats")} or {gp_n(hw * GP_WK, "scarf", "knit", "scarf", "scarves")}</td><td>{gp_n(hw * GP_WK, "hat", "crochet", "hat", "hats")} or {gp_n(hw * GP_WK, "throw", "crochet", "throw", "throws")}</td><td>{gp_fit(hw * GP_WK, "ornament", "crochet")}</td></tr>' for hw in GP_HW)
GP_QUICK = [g for g in D["gifts"] if g["crochet"] <= 6 or g["knit"] <= 6]
gp_quick_txt = ", ".join(f'{g["name"] if g["name"].startswith("Christmas") else g["name"][0].lower() + g["name"][1:]} (about {g["knit"]:g} h knit, {g["crochet"]:g} h crochet)' for g in GP_QUICK)
GP_TOP = f'''<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> there are <strong>{GP_DAYS} days ({GP_WK:.1f} weeks) until Christmas</strong> on {_xmas.strftime("%d %B %Y").lstrip("0")}. At 7 hours of crafting a week that's about <strong>{7 * GP_WK:.0f} hours</strong>: enough for roughly {gp_fit(7 * GP_WK, "hat", "knit")} knitted hats, or {gp_fit(7 * GP_WK, "hat", "crochet")} crocheted hats, by our typical times. A crochet throw takes about {_GI["throw"]["crochet"]:g} hours and a knitted one about {_GI["throw"]["knit"]:g}, so start the big gifts first. Add your own list below to check every gift.</div></div></section>
'''
GP_FIT = f'''<section style="padding-top:0"><div class="wrap"><h2>What can I still make before Christmas?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">If you craft</th><th scope="col">Time left ({GP_DAYS} days)</th><th scope="col">Knitting</th><th scope="col">Crochet</th><th scope="col">Crochet ornaments</th></tr></thead><tbody>{gp_fit_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Counted from {_today.strftime("%d %B %Y").lstrip("0")} to Christmas Day, using the typical hours in the table below (worsted yarn, a comfortable maker). Each column is one kind of gift on its own; mix and match in the planner. Leave a few days for blocking, wrapping and post.</p>
<h3 style="margin-top:22px">Quick gifts for the last weeks</h3>
<p>Each of these takes an evening or a weekend for most makers: {e(gp_quick_txt)}. Chunky yarn cuts the time again: the planner allows about a third less.</p>
</div></section>
'''
SRC = {"lc": "LoveCrafts", "lc-k": "LoveCrafts (knit); our estimate (crochet)", "lc-c": "LoveCrafts (crochet); our estimate (knit)", "est": "Our estimate"}
gp_opts = "".join(f'<option value="{g["id"]}"{" selected" if g["id"] == "hat" else ""}>{e(g["name"])}</option>' for g in D["gifts"])
gp_rows = "".join(f'<tr><td><strong>{e(g["name"])}</strong></td><td>{g["knit"]:g} h</td><td>{g["crochet"]:g} h</td><td class="muted">{e(SRC[g["src"]])}</td></tr>' for g in D["gifts"])
gp = top("Handmade gift planner", "List the hats, scarves and blankets you want to give, tell us how many hours a week you can craft, and see if they'll all be ready by Christmas, or which ones to swap for something quicker.", "Handmade gift planner") + GP_TOP + f'''
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h3 style="margin-top:0">Your time</h3>
<div class="row2"><div class="field"><label for="gp-due">Finish by</label><input type="date" id="gp-due"></div>
<div class="field"><label for="gp-hrs">Hours I can craft a week</label><input type="number" id="gp-hrs" value="7" min="0.5" max="100" step="0.5" inputmode="decimal"></div></div>
<div class="field"><span class="label" id="gp-speed-l">How fast are you?</span><div class="seg" role="group" aria-labelledby="gp-speed-l" id="gp-speed"><button type="button" data-v="1.25" aria-pressed="false">Still learning</button><button type="button" data-v="1" aria-pressed="true">Comfortable</button><button type="button" data-v="0.8" aria-pressed="false">Speedy</button></div></div>
<h3>Add a gift</h3>
<form id="gp-form">
<div class="row2"><div class="field"><label for="gp-who">Who is it for?</label><input type="text" id="gp-who" placeholder="Mum" maxlength="40"></div>
<div class="field"><label for="gp-proj">What are you making?</label><select id="gp-proj">{gp_opts}</select></div></div>
<div class="field"><span class="label" id="gp-craft-l">Knitting or crochet?</span><div class="seg" role="group" aria-labelledby="gp-craft-l" id="gp-craft"><button type="button" data-v="knit" aria-pressed="true">Knitting</button><button type="button" data-v="crochet" aria-pressed="false">Crochet</button></div></div>
<div class="row2"><div class="field"><label for="gp-yarn">Yarn thickness</label><select id="gp-yarn"><option value="1.3">Fine (fingering to DK)</option><option value="1" selected>Medium (worsted, aran)</option><option value="0.65">Chunky or bulky</option></select></div>
<div class="field"><label for="gp-h">Hours to make it</label><input type="number" id="gp-h" min="0.5" max="300" step="0.5" inputmode="decimal"></div></div>
<p class="note" id="gp-hint" style="margin:-4px 0 14px"></p>
<button type="submit" class="btn gold">Add to my list</button>
</form>
<h3 style="margin-top:26px">My gift list</h3>
<ol class="gp-list" id="gp-list"></ol>
<div class="toolbar" style="margin-top:14px"><button type="button" class="btn ghost sm" id="gp-print">Print my list</button><button type="button" class="btn ghost sm" id="gp-clear">Clear the list</button></div>
</div>
<div class="result" aria-live="polite" id="gp-out"></div>
</div></section>
{GP_FIT}<section style="padding-top:0"><div class="wrap"><h2>How long does it take to knit or crochet a gift?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Gift</th><th scope="col">Knitting</th><th scope="col">Crochet</th><th scope="col">Where the number comes from</th></tr></thead><tbody>{gp_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Hours for a comfortable, not brand-new, maker in medium (worsted) yarn. Hat, scarf, socks, blanket and sweater times follow the middle skill level in LoveCrafts' knitting and crochet time guides; the rest are our own rough estimates for simple patterns. Everyone's pace is different, so treat every number as a starting point and change the hours to suit you.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How the planner works</h2>
<p>It takes your hours per week and the days left until your finish date to work out how much crafting time you really have. Then it lines your gifts up in the order you listed them, like beads on a strand, and shows roughly when each one will be done. Anything that runs past the deadline turns red.</p>
<p>Fine yarn makes small stitches, so it takes longer to cover the same area; chunky yarn works up much faster. The planner allows about 30 percent more time for fine yarn and about a third less for chunky. If you've timed yourself on a similar project, type your own hours instead.</p>
<div class="callout"><strong>Time yourself once.</strong> Work for 30 minutes on your swatch or the first rows of the gift and count how much you finished. Multiply out to the whole piece and you'll have a far better number than any chart.</div>
<h2>When should I start knitting Christmas gifts?</h2>
<p>Count back from the hours. A throw or sweater is 25 to 65 hours, so at 5 hours a week it needs to start 5 to 13 weeks before Christmas. Hats, cowls and mittens fit into the last month. Our tip: add a week at the end for blocking, weaving in ends and posting, and plan nothing new for the final few days.</p>
<h2>Making it all fit</h2>
<ul><li><strong>Start the biggest gift first.</strong> Put blankets and sweaters at the top of the list so the small things fill the last weeks.</li>
<li><strong>Swap the yarn, not the gift.</strong> A hat in chunky yarn can take half the time of one in DK.</li>
<li><strong>Keep a few quick makes in reserve.</strong> Dishcloths, ornaments and headbands take an evening or two.</li>
<li><strong>Give an IOU.</strong> A wrapped skein with a note saying what it will become is a lovely gift too.</li></ul>
<p>Want a closer figure for one big gift? The <a href="{href("crochet-time-estimator.html")}">crochet and knitting time calculator</a> counts the stitches for your size, yarn and stitch, uses your own pace (time yourself for a minute), and gives the date you'll finish.</p>
<p>Once you know what you're making, check how much yarn to buy with the <a href="{href("yarn-calculator.html")}">yarn calculator</a> or, for blankets, the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>. Keep notes on each gift in the <a href="{href("projects.html")}">project tracker</a>, and count rows with the <a href="{href("row-counter.html")}">row counter</a>.</p></div></section>'''
gp_faq = [
    ("How long does it take to knit a hat?", "Roughly 7 to 11 hours for a simple adult hat in worsted yarn, depending on experience. A chunky hat can be done in an evening or two."),
    ("How long does it take to crochet a blanket?", "A throw often takes 20 to 30 hours of crochet, and a knitted one about twice as long. Bigger blankets, fine yarn and fancy stitches take longer."),
    ("What can I knit or crochet in one evening?", "A dishcloth, an ornament, a headband or a chunky cowl are all realistic in one to three hours for most makers."),
    ("Is it too late to make Christmas gifts?", "Usually not. Even one hour a day gives you over 30 hours in five weeks, enough for a couple of hats and a scarf. Put your numbers into the planner to see what fits."),
    ("How many days are left to make Christmas gifts?", f"On {_today.strftime('%d %B %Y').lstrip('0')} there are {GP_DAYS} days until Christmas. At 7 hours of crafting a week that's about {7 * GP_WK:.0f} hours, roughly {gp_fit(7 * GP_WK, 'hat', 'knit')} knitted hats by our typical times."),
    ("When should I start knitting Christmas gifts?", "Big gifts like throws and sweaters take 25 to 65 hours, so start them two to three months ahead if you knit a few hours a week. Hats, cowls and mittens can be made in the last month. Leave a week for blocking, wrapping and post."),
    ("Where is my gift list saved?", "On this device, in your browser. Nothing is uploaded. Use 'Print my list' to keep a paper copy."),
]
page("crochet-knitting-gift-planner.html", "Christmas Knitting and Crochet Gift Planner: Will It Be Ready in Time? | Purl & Paper",
     "Free handmade gift planner for knitters and crocheters. List your gifts, add your crafting hours per week and see if they'll be finished by Christmas, plus how long hats, scarves and blankets take.",
     gp, gp_faq, "Handmade gift planner", app_name="Handmade gift planner")

# ---------------- HAT SIZE CHART + CALCULATOR ----------------
H = D["hats"]
h_opts = "".join(f'<option value="{x["id"]}"{" selected" if x["id"] == "adult" else ""}>{e(x["name"])} ({e(x["age"])})</option>' for x in H) + '<option value="custom">I measured a head</option>'
h_rows = "".join(f'<tr><td><strong>{e(x["name"])}</strong><br><span class="muted">{e(x["age"])}</span></td><td>{x["head"]:g} in<br><span class="muted">{round(x["head"] * 2.54)} cm</span></td><td>{e(x["cyc"])}</td>'
                 f'<td>{round(x["head"] * 0.88 * 2) / 2:g} in<br><span class="muted">{round(x["head"] * 0.88 * 2.54)} cm</span></td><td>{e(x["h"])} in<br><span class="muted">{round(x["hn"] * 2.54)} cm</span></td></tr>' for x in H)
def ht_co(head, g4, rep=8): return max(rep, int(head * 0.88 * g4 / 4 / rep + 0.5) * rep)
HT_G = {1: 28, 2: 24, 3: 22, 4: 18, 5: 14, 6: 9, 7: 6}   # same typical knit gauges as the cast on calculator
HT_W = [(1, "Fingering"), (3, "DK"), (4, "Worsted"), (5, "Bulky"), (6, "Super bulky")]
ht_co_rows = "".join(f'<tr><td><strong>{e(x["name"])}</strong><br><span class="muted">{x["head"]:g} in head</span></td>' + "".join(f"<td>{ht_co(x['head'], HT_G[k])}</td>" for k, _ in HT_W) + "</tr>" for x in H if x["id"] != "preemie")
ht_cr_rows = "".join(f'<tr><td><strong>{e(x["name"])}</strong></td><td>{x["head"] * 0.92:.1f} in</td><td>{x["head"] * 0.92 / 3.14159:.1f} in ({x["head"] * 0.92 / 3.14159 * 2.54:.0f} cm)</td><td>{e(x["h"])} in</td></tr>' for x in H)
_ht_ad = [x for x in H if x["id"] == "adult"][0]
ht = top("Hat size chart and calculator", "Head sizes from preemie to large adult, how much smaller to make the hat, and the exact number of stitches to cast on (or how wide to crochet the crown) for your yarn.", "Hat size chart") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> an average adult head is <strong>22 in (56 cm)</strong> around, so a fitted beanie is made about <strong>19.5 in around and 11 in tall</strong>. A newborn hat is about 12 to 13 in around and 6 in tall. In worsted yarn (about 4.5 stitches per inch) cast on about <strong>{ht_co(22, 18)} stitches</strong> for an adult hat. Make the hat 10 to 15 percent smaller than the head so it stays on.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="ht-size">Who is it for?</label><select id="ht-size">{h_opts}</select></div>
<div class="row2" id="ht-custom" hidden><div class="field"><label for="ht-head">Head measurement</label><input type="number" id="ht-head" value="22" min="8" max="70" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="ht-hu">Unit</label><select id="ht-hu"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><span class="label" id="ht-craft-l">Knitting or crochet?</span><div class="seg" role="group" aria-labelledby="ht-craft-l" id="ht-craft"><button type="button" data-v="knit" aria-pressed="true">Knitting</button><button type="button" data-v="crochet" aria-pressed="false">Crochet</button></div></div>
<div class="field"><label for="ht-ease">How snug?</label><select id="ht-ease"><option value="15">Snug, stretchy rib (about 15% smaller)</option><option value="12" selected>Classic beanie (about 12% smaller)</option><option value="8">Relaxed, firm fabric (about 8% smaller)</option><option value="3">Loose or slouchy band (about 3% smaller)</option></select></div>
<div class="row2"><div class="field"><label for="ht-g">Stitches in your swatch</label><input type="number" id="ht-g" value="18" min="4" max="60" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="ht-gu">Measured over</label><select id="ht-gu"><option value="4">4 in</option><option value="10">10 cm</option></select></div></div>
<div class="field"><label for="ht-rep">Round the count to a multiple of</label><select id="ht-rep"><option value="1">Any number</option><option value="2">2 (1x1 rib)</option><option value="4">4 (2x2 rib)</option><option value="8" selected>8 (rib plus an easy crown)</option><option value="6">6 (crochet crown of 6 wedges)</option></select></div>
<figure class="ht-fig"><svg id="ht-svg" viewBox="0 0 320 230" role="img" aria-label="Hat drawn with its width and height"></svg><figcaption class="note" id="ht-cap">Your hat.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="ht-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>What size should a hat be? Hat size chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size</th><th scope="col">Typical head</th><th scope="col">Craft Yarn Council range</th><th scope="col">Hat width around (12% smaller)</th><th scope="col">Hat height</th></tr></thead><tbody>{h_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Head ranges are from the Craft Yarn Council's head circumference chart. The typical head is the middle size that yarn companies and hat designers most often quote. Hat height runs from the bottom of an unfolded brim to the top of the crown on a fitted beanie, as listed by Knit Picks. Add 2 to 3 inches for a slouchy hat or a brim you fold up (our rule of thumb). Heads vary, so measure when you can.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How do I measure a head for a hat?</h2>
<p>Wrap a soft tape measure around the head just above the eyebrows and ears, across the widest part at the back. Keep it level and comfortably snug, not tight. Making a surprise gift? Lay a hat the person already wears flat, without stretching it, measure across and double it.</p>
<h2>Why is a hat smaller than the head?</h2>
<p>Knitted and crocheted fabric stretches, so a hat made the exact size of the head slides down over the eyes. Designers make the hat a little smaller, which is called negative ease. Most patterns use around 2 to 3 inches less than the head on an adult, or roughly 10 to 15 percent.</p>
<ul><li><strong>Ribbing</strong> pulls in and springs back, so ribbed hats can be made smaller.</li>
<li><strong>Thick yarn</strong> and firm stitches stretch less, so they need less ease.</li>
<li><strong>Crochet</strong> usually stretches less than knitting, so many crocheters make the band only a little smaller than the head. That's why the calculator suggests less ease for crochet.</li>
<li><strong>Babies and children</strong> grow fast. When in doubt, go a little bigger.</li></ul>
<div class="callout"><strong>Swatch in the round if you can.</strong> Measure your stitches over 4 inches (10 cm) after washing the swatch. Half a stitch per inch can change an adult hat by 2 inches.</div>
<h2>How many stitches do I cast on for a hat?</h2>
<p>Multiply the hat width by your stitches per inch, then round to a number that suits your rib and crown. For example, a 22 inch head with 12 percent ease gives a 19.4 inch hat. At 4.5 stitches per inch that's 87 stitches, so cast on 88. Knit until the hat is about 2.5 to 3 inches short of the full height, then start the crown decreases. Adding stitches after a ribbed brim? The <a href="{href("increase-decrease-calculator.html")}">increase evenly calculator</a> spaces them for you.</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size</th>{"".join(f'<th scope="col">{n}<br><span class="muted">{HT_G[w]} sts / 4 in</span></th>' for w, n in HT_W)}</tr></thead><tbody>{ht_co_rows}</tbody></table></div>
<p class="note">Cast-on for a knitted beanie made 12 percent smaller than the head, rounded to a multiple of 8, at a typical gauge for each yarn weight (the middle of the Craft Yarn Council knit range). Our own maths: use the calculator with your swatch.</p>
<h2>How big should a crochet hat crown be?</h2>
<p>Work a flat circle, increasing each round, until it measures the hat width divided by 3.14 across. Then stop increasing and work even rounds until the hat reaches the full height, measured from the centre of the crown. For a 19 inch hat that's a circle about 6 inches across.</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size</th><th scope="col">Hat around (8% smaller)</th><th scope="col">Crown circle across</th><th scope="col">Full height</th></tr></thead><tbody>{ht_cr_rows}</tbody></table></div>
<p class="note">Crown size = hat width ÷ 3.14, with about 8 percent ease for firmer crochet fabric (the calculator's crochet setting). Work the flat circle with the <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a>, which writes out every round.</p>
<h2>How much yarn do I need for a hat?</h2>
<p>A simple adult beanie takes roughly {yc_yd("hat", 4)} yards of worsted yarn, about {yc_yd("hat", 3)} of DK or {yc_yd("hat", 5)} of bulky (our estimates, the same model as the <a href="{href("yarn-calculator.html")}">yarn calculator</a>). A child's hat takes about {yc_yd("kidhat", 4)} yards of worsted. A folded brim, pompom, cables or a slouchy shape all add more, so buy one extra ball.</p>
<h2>How tall should a hat be?</h2>
<p>For a fitted adult beanie, about {_ht_ad["h"]} in from the bottom edge to the top of the crown. Add 2 to 3 in for a brim you fold up or a slouchy fit. Start the crown decreases about 2.5 to 3 in before the full height on a knitted hat. Measure from the centre of the crown on a top-down crochet hat.</p>
<p>New to hats? Our guide to <a href="{href("how-to-knit-in-the-round.html")}">knitting in the round</a> shows the join and which circular needle to use (16 in for most hats). Not sure which yarn to use? See the <a href="{href("yarn-weights.html")}">yarn weight chart</a> and the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>. Swatch doesn't match the pattern? The <a href="{href("gauge-converter.html")}">gauge converter</a> shows the size you'll really get. A simple adult beanie takes roughly 200 yards of worsted yarn; the <a href="{href("yarn-calculator.html")}">yarn calculator</a> covers other weights. Making hats for Christmas? Check the timing in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Matching socks? The <a href="{href("sock-size-chart.html")}">sock size chart</a> works out the cast-on the same way.</p></div></section>'''
ht_faq = [
    ("What size should an adult knit hat be?", "Most adult heads are 21 to 24 inches around. A fitted beanie is usually made 2 to 3 inches smaller, so about 19 to 21 inches around, and about 11 inches tall before any fold-up brim."),
    ("How many stitches do I cast on for a hat?", "Multiply the hat width (head size minus about 12 percent) by your stitches per inch, then round to suit your rib. In worsted yarn at 4.5 stitches per inch, an average adult hat is about 88 stitches."),
    ("How big should a crochet hat crown circle be?", "Divide the hat width by 3.14. For an adult hat about 20 inches around, increase until the flat circle is about 6.4 inches across, then work even."),
    ("What size is a newborn hat?", "A newborn head is about 14 inches around, so a newborn hat is usually about 12 to 13 inches around and 6 inches tall."),
    ("How many stitches do I cast on for a hat in bulky yarn?", f"At about 3.5 stitches per inch, an average adult hat needs about {ht_co(22, 14)} stitches and a child's hat about {ht_co(20, 14)}. Swatch and use the calculator for your own gauge."),
    ("How much yarn do I need for a beanie?", f"Roughly {yc_yd('hat', 4)} yards of worsted yarn for a simple adult beanie, or about {yc_yd('kidhat', 4)} yards for a child's hat. Add more for a folded brim, cables or a pompom."),
    ("What is negative ease in a hat?", "It means the hat is smaller than the head, so the stretchy fabric holds it in place. Hats usually have about 10 to 15 percent negative ease, more for ribbing and less for thick or firm fabric."),
]
page("hat-size-chart.html", "Hat Size Chart for Knitting and Crochet, with Stitch Calculator | Purl & Paper",
     "Free knit and crochet hat size chart from preemie to adult, with head sizes, hat height and negative ease, plus a calculator for cast-on stitches or crochet crown size.",
     ht, ht_faq, "Hat size chart", app_name="Hat size calculator")

# ---------------- GRANNY SQUARE BLANKET CALCULATOR ----------------
GS_SIZES = [("baby", "Baby", 36, 36), ("lap", "Lapghan", 36, 48), ("throw", "Throw", 50, 60), ("twin", "Twin", 66, 90), ("queen", "Queen", 90, 100), ("king", "King", 108, 100)]
def gs_count(t, s): return max(1, int(t / s + 0.5))
gs_rows = "".join(f'<tr><td><strong>{n}</strong><br><span class="muted">{w} × {l} in</span></td>' + "".join(
    f'<td>{gs_count(w, s) * gs_count(l, s)}<br><span class="muted">{gs_count(w, s)} × {gs_count(l, s)}</span></td>' for s in (4, 5, 6, 8, 12)) + "</tr>" for _, n, w, l in GS_SIZES)
gs_opts = "".join(f'<option value="{b["id"]}"{" selected" if b["id"] == "throw" else ""}>{e(b["name"])} ({b["w"]} × {b["l"]} in)</option>' for b in D["blankets"]) + '<option value="custom">My own size</option>'
gs_w = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"])})</option>' for w in D["weights"] if 1 <= w["n"] <= 6)
GS_SK = [(4, "4 in"), (5, "5 in"), (6, "6 in"), (8, "8 in"), (12, "12 in")]
def gs_per_sq(s): return s * s * 0.9   # yd of worsted per square: same 0.9 yd per sq in estimate as the calculator
gs_sk_rows = "".join(f'<tr><td><strong>{n}</strong></td><td>about {gs_per_sq(s):,.0f} yd</td><td>{int(200 // gs_per_sq(s))}</td><td>{int(364 // gs_per_sq(s))}</td></tr>' for s, n in GS_SK)
gs = top("Granny square blanket calculator", "How many granny squares you need for any blanket, how to lay them out, and roughly how much yarn the squares, joins and border will take.", "Granny square calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> divide the blanket width by the size of one square, then the length, and multiply. A 50 × 60 in throw of 6 in squares is about 8 across × 10 down = <strong>80 squares</strong> before a border. In worsted yarn, allow roughly a yard of yarn per square inch of blanket, joins and border included, so about 3,000 yards for that throw.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="gs-size">Blanket size</label><select id="gs-size">{gs_opts}</select></div>
<div class="row2" id="gs-custom" hidden><div class="field"><label for="gs-bw">Width (in)</label><input type="number" id="gs-bw" value="50" min="6" max="140" inputmode="decimal"></div><div class="field"><label for="gs-bl">Length (in)</label><input type="number" id="gs-bl" value="60" min="6" max="140" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="gs-sq">Size of one square</label><input type="number" id="gs-sq" value="6" min="1" max="40" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="gs-su">Unit</label><select id="gs-su"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><label for="gs-join">How will you join them?</label><select id="gs-join"><option value="0|0.05">Sewn seam (whip or mattress stitch)</option><option value="0|0.06">Join as you go</option><option value="0.25|0.08" selected>Slip stitch or single crochet seam</option><option value="0.5|0.12">Decorative join (zipper, flat braid)</option></select></div>
<div class="field"><label for="gs-border">Border width on each side (in)</label><input type="number" id="gs-border" value="1" min="0" max="12" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="gs-weight">Yarn weight</label><select id="gs-weight">{gs_w}</select></div>
<div class="field"><label for="gs-ypsq">Yarn in one finished square (optional)</label><input type="number" id="gs-ypsq" placeholder="Leave blank for our estimate" min="0" step="0.5" inputmode="decimal"><span class="note">Make one square, unravel or measure the leftover, and type the yards here for a better answer.</span></div>
<div class="row2"><div class="field"><label for="gs-skein">Length per skein</label><input type="number" id="gs-skein" value="200" min="1" inputmode="decimal"></div>
<div class="field"><label for="gs-unit">Unit on the label</label><select id="gs-unit"><option value="yd">yards</option><option value="m">metres</option></select></div></div>
<div class="field"><label for="gs-cols">Colours (each square in one colour)</label><input type="number" id="gs-cols" value="4" min="1" max="12" inputmode="numeric"></div>
<figure class="gs-fig"><svg id="gs-svg" viewBox="0 0 320 320" role="img" aria-label="Your granny square layout"></svg><figcaption class="note" id="gs-cap">Your layout.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="gs-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How many granny squares for a blanket?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Blanket</th><th scope="col">4 in squares</th><th scope="col">5 in squares</th><th scope="col">6 in squares</th><th scope="col">8 in squares</th><th scope="col">12 in squares</th></tr></thead><tbody>{gs_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Total squares, with squares across × squares down underneath. Worked out from the blanket sizes on our <a href="{href("blanket-size-calculator.html")}">blanket size chart</a>, rounded to the nearest whole square, before any joining or border. A border adds width all round, so you can often drop a row or column. Use the calculator above for your own size, join and border.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How to work out the number of squares</h2>
<ol><li><strong>Make one square and block it.</strong> Measure it flat, side to side. Squares from the same pattern can vary by half an inch between crocheters, so measure yours.</li>
<li><strong>Take off the border.</strong> If the border will be 2 inches wide, a 50 inch blanket needs 46 inches of squares.</li>
<li><strong>Divide by the square size.</strong> 46 ÷ 6 = 7.7, so 8 squares across. Do the same for the length.</li>
<li><strong>Multiply across by down.</strong> 8 across × 10 down = 80 squares.</li></ol>
<p>A joining round or a decorative join adds a little to every seam. Over 10 seams a quarter inch each adds 2.5 inches, which is why the calculator asks how you'll join.</p>
<div class="callout"><strong>Odd numbers look better</strong> for patterns with a centre, like a checkerboard or a big diamond. If the count lands on an even number, try a slightly wider border to go down one, or a narrower one to go up.</div>
<h2>How much yarn does a granny square take?</h2>
<p>A classic 5 inch granny square of five rounds in worsted yarn uses roughly 25 to 30 yards, and finished granny blankets in worsted usually come out at about a yard of yarn for every square inch of blanket, joins and border included. One published 50 × 66 inch throw of 8 inch squares, for example, calls for about 3,300 yards. The calculator uses a little under a yard per square inch for the squares, then adds the joins and border, and scales it all for your yarn weight. Solid granny squares and squares with popcorns take more; lacy squares take less. Treat our numbers as estimates, and if you've made one square already, type its yardage in for a much better answer.</p>
<ul><li><strong>Joining</strong> takes about 5 to 12 percent of the yarn in the squares, depending on the method.</li>
<li><strong>The border</strong> is worked in solid rounds, so even a narrow one adds up on a big blanket.</li>
<li><strong>Several colours?</strong> Each colour only needs to cover its own squares, but buy at least one spare skein of the colour you'll join and border with.</li></ul>
<h2>How many granny squares can I make from one skein?</h2></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Square size</th><th scope="col">Yarn per square (worsted)</th><th scope="col">From a 200 yd skein</th><th scope="col">From a 364 yd skein</th></tr></thead><tbody>@@GSSK@@</tbody></table></div></div>
<div class="narrow prose"><p class="note">Our estimate, from the same 0.9 yards per square inch the calculator uses for classic granny squares in worsted. Solid squares use more. Weigh one finished square to check: if a 6 in square weighs 16 g and your yarn is 2 yd per gram, it used about 32 yd.</p>
<h2>Using up leftover yarn in granny squares</h2>
<p>Granny squares are the classic stash buster, since each round can be a different colour. Stick to one yarn weight across the blanket so the squares come out the same size, and keep the joining and border colour the same throughout. To see how far your odds and ends will go, weigh each ball and add them up in the <a href="@@YY@@">yarn yardage calculator</a>, then divide by the yarn per square above.</p>
<h2>Squares versus a one-piece granny blanket</h2>
<p>Separate squares are portable and easy to fit in, and you can stop the moment the blanket is big enough. A giant granny square worked as one piece has no seams to sew, but it gets heavy and you can't change its shape later. Either way, check the size against a bed or sofa with the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>, keep count of finished squares with the <a href="{href("row-counter.html")}">row counter</a>, and see how long it will take in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Following a UK pattern? Our <a href="{href("crochet-terms.html")}">US and UK crochet terms</a> page explains why a UK treble is a US double.</p></div></section>'''
gs = gs.replace("@@GSSK@@", gs_sk_rows).replace("@@YY@@", href("yarn-yardage-calculator.html"))
gs_faq = [
    ("How many granny squares do I need for a throw blanket?", "With 6 inch squares, a 50 × 60 inch throw takes about 8 across by 10 down, or 80 squares, before a border. With 4 inch squares it's about 195."),
    ("How many 6 inch granny squares for a queen blanket?", "About 15 across by 17 down, or 255 squares, for a 90 × 100 inch queen blanket with no border. A 3 inch border on each side brings it down to about 14 × 16, or 224."),
    ("How much yarn is in one granny square?", "A 5 inch worsted granny square of five rounds uses roughly 25 to 30 yards. For a whole blanket, allow roughly a yard of worsted yarn per square inch of blanket, so about 3,000 yards for a 50 × 60 inch throw. This is an estimate; measure one of yours to be sure."),
    ("How many granny squares for a baby blanket?", "A 36 inch square baby blanket takes 36 squares of 6 inches (6 × 6), or 81 squares of 4 inches (9 × 9), before a border."),
    ("How many granny squares can you make with one skein of yarn?", "Roughly 6 squares of 6 inches, or 8 of 5 inches, from a 200 yard skein of worsted, by our estimate. A big 364 yard acrylic skein makes about 11 of 6 inches. Solid squares use more yarn."),
    ("Can I mix yarn brands in a granny square blanket?", "Yes, as long as they're the same yarn weight and give similar gauge, so the squares come out the same size. Make one square in each yarn and measure before you commit."),
    ("Does joining granny squares make the blanket bigger?", "Sewn seams and join as you go add almost nothing. A slip stitch or single crochet seam adds roughly a quarter inch per seam, and decorative joins can add half an inch or more."),
]
page("granny-square-blanket-calculator.html", "Granny Square Blanket Calculator: How Many Squares and How Much Yarn | Purl & Paper",
     "Free granny square calculator: how many squares for a baby, throw, twin, queen or king blanket, the layout, and an estimate of the yarn for squares, joins and border.",
     gs, gs_faq, "Granny square calculator", app_name="Granny square blanket calculator")

# ---------------- INCREASE / DECREASE EVENLY CALCULATOR ----------------
def spacing(S, N, kind, flat):
    """Same maths as app.js. kind: m1 (inc between sts), into (inc worked into a st), dec (2 sts worked together).
    Returns list of (plain, action) tokens and the trailing plain count, or None if impossible."""
    use = {"m1": 0, "into": 1, "dec": 2}[kind]
    if N < 1 or S < 1 or N * max(use, 1) > S: return None
    L = [((i + 1) * S) // N - (i * S) // N for i in range(N)]
    p = [x - use for x in L]
    if flat:
        a = p[-1] // 2
        return [(a, 1)] + [(x, 1) for x in p[:-1]], p[-1] - a
    return [(x, 1) for x in p], 0
def spacing_text(S, N, kind, flat, craft="knit"):
    r = spacing(S, N, kind, flat)
    if not r: return "not possible"
    toks, tail = r
    if craft == "knit":
        act = {"m1": "M1", "into": "kfb", "dec": "k2tog"}[kind]
        unit = lambda n: f"K{n}"
    else:
        act = "dec" if kind == "dec" else "inc"
        unit = lambda n: f"{n} sc"
    def tok(t): return ", ".join(([unit(t[0])] if t[0] else []) + [act])
    out, i = [], 0
    while i < len(toks):
        best = (1, 1)
        for per in (1, 2, 3):
            c = 1
            while i + (c + 1) * per <= len(toks) and toks[i + c * per:i + (c + 1) * per] == toks[i:i + per]: c += 1
            if c >= 2 and c * per > best[0] * best[1] and not (best[1] >= 2 and per > best[0]): best = (per, c)
        per, c = best
        blk = ", ".join(tok(t) for t in toks[i:i + per])
        out.append(blk if c == 1 else ((f"[{blk}] {c} times") if craft == "knit" else f"({blk}) {c} times"))
        i += per * c
    if tail: out.append(unit(tail))
    return ", ".join(out)
ID_EX = [(48, 12, "m1", True), (60, 8, "m1", False), (80, 10, "into", True), (90, 10, "dec", True), (72, 12, "dec", False), (120, 20, "dec", False)]
ID_KINDS_T = [("Knit", "M1 (make 1)", "Increase", "Lift the bar between stitches and knit into its back. Nearly invisible; M1L and M1R lean left and right."),
    ("Knit", "kfb", "Increase", "Knit into the front, then the back of the same stitch. Leaves a small bar; easy for beginners."),
    ("Knit", "yo (yarn over)", "Increase", "Wrap the yarn over the needle. Makes a hole on purpose, used in lace."),
    ("Knit", "k2tog", "Decrease", "Knit 2 stitches together. Leans to the right."),
    ("Knit", "ssk", "Decrease", "Slip, slip, knit the 2 together through the back. Leans to the left; pairs with k2tog."),
    ("Knit", "p2tog", "Decrease", "Purl 2 together, for decreasing on a purl row."),
    ("Crochet", "inc (2 sc in one stitch)", "Increase", "Work 2 stitches into the same stitch."),
    ("Crochet", "sc2tog / dec", "Decrease", "Pull up a loop in each of 2 stitches, then yarn over through all 3 loops."),
    ("Crochet", "invdec", "Decrease", "Front loops of 2 stitches, then finish like one stitch. No bump: best for amigurumi.")]
ID_KINDS = '<div class="tbl-wrap"><table><thead><tr><th scope="col">Craft</th><th scope="col">Abbreviation</th><th scope="col">Type</th><th scope="col">What it does</th></tr></thead><tbody>' + "".join(f"<tr><td>{a}</td><td><code>{e(b)}</code></td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in ID_KINDS_T) + "</tbody></table></div>"
id_rows = "".join(f'<tr><td>{S} sts</td><td>{"Increase" if k != "dec" else "Decrease"} {N}</td><td>{"Flat" if fl else "In the round"}</td><td><code>{e(spacing_text(S, N, k, fl))}</code></td><td>{S + N if k != "dec" else S - N}</td></tr>' for S, N, k, fl in ID_EX)
idc = top("Increase and decrease evenly calculator", "Type how many stitches you have and how many to add or take away. You get a written line you can follow, with the increases or decreases spread as evenly as the maths allows.", "Increase evenly calculator") + f'''
<section style="padding-top:10px"><div class="wrap tool">
<div class="sheet">
<div class="field"><span class="label" id="id-craft-l">Knitting or crochet?</span><div class="seg" role="group" aria-labelledby="id-craft-l" id="id-craft"><button type="button" data-v="knit" aria-pressed="true">Knitting</button><button type="button" data-v="crochet" aria-pressed="false">Crochet</button></div></div>
<div class="field"><span class="label" id="id-dir-l">Add or take away?</span><div class="seg" role="group" aria-labelledby="id-dir-l" id="id-dir"><button type="button" data-v="inc" aria-pressed="true">Increase</button><button type="button" data-v="dec" aria-pressed="false">Decrease</button></div></div>
<div class="row2"><div class="field"><label for="id-s">Stitches you have now</label><input type="number" id="id-s" value="60" min="2" max="2000" inputmode="numeric"></div>
<div class="field"><label for="id-n" id="id-n-l">How many to increase</label><input type="number" id="id-n" value="12" min="1" max="1000" inputmode="numeric"></div></div>
<p class="note" id="id-target" style="margin-top:-6px">You'll end with 72 stitches.</p>
<div class="field"><span class="label" id="id-way-l">Working</span><div class="seg" role="group" aria-labelledby="id-way-l" id="id-way"><button type="button" data-v="flat" aria-pressed="true">Flat, in rows</button><button type="button" data-v="round" aria-pressed="false">In the round</button></div></div>
<div class="field" id="id-kind-f"><label for="id-kind">Increase type</label><select id="id-kind"><option value="m1">M1, make one between stitches</option><option value="into">Kfb, knit front and back of a stitch</option></select></div>
<label class="switch" id="id-stag-f" hidden><input type="checkbox" id="id-stag"> Stagger: start halfway into a repeat (so increases don't stack up round after round)</label>
<figure class="id-fig"><svg id="id-svg" viewBox="0 0 320 120" role="img" aria-label="Your stitches with the increases or decreases marked"></svg><figcaption class="note" id="id-cap">Your row.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="id-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<div class="quick"><strong>Quick answer:</strong> divide the stitches you have by the number of increases or decreases. For 60 stitches and 12 increases, 60 ÷ 12 = 5, so work K5, M1 twelve times in the round, or start with K2 or K3 when working flat so the first and last increase sit away from the edges. If it doesn't divide exactly, alternate the shorter and longer gaps.</div>
<h2>How do you increase evenly across a row?</h2>
<ol><li><strong>Divide.</strong> Stitches now ÷ increases. 80 ÷ 10 = 8, so there's an increase every 8 stitches.</li>
<li><strong>Working flat, split one gap.</strong> Put half a gap at each end: K4, M1, then (K8, M1) nine times, K4. That keeps increases off the selvedge, where they'd be hidden in the seam or look untidy.</li>
<li><strong>In the round, there are no edges.</strong> (K8, M1) ten times brings you back to the start.</li>
<li><strong>If it doesn't divide exactly</strong>, some gaps are one stitch longer. 62 ÷ 8 = 7.75, so six gaps of 8 and two of 7. The calculator spreads the longer gaps out instead of bunching them at one end.</li></ol>
<h2>How do you decrease evenly?</h2>
<p>The same way, with one difference: each decrease uses two stitches. If you need to decrease 10 from 90, every 9 stitches hold one decrease, so you knit 7 and then knit 2 together. Forgetting this is the most common reason a row ends with the wrong count. In crochet a decrease (sc2tog) also works two stitches together: our guide to <a href="{href("how-to-crochet-decrease.html")}">how to decrease in crochet</a> shows sc2tog and the invisible decrease step by step.</p>
<h2>Which increase or decrease should I use?</h2>{ID_KINDS}
<p class="note">Lean directions as described in standard knitting references. When a pattern just says "inc" or "dec", it usually means the simplest one: kfb or M1 for knitting, 2 sc in one stitch or sc2tog for crochet.</p>
<h2>Increases worked into a stitch use it up</h2>
<p>A make one (M1) is lifted from the bar between stitches, so it doesn't use a stitch. Kfb and the crochet increase (2 sc in the same stitch) are worked into a stitch, so that stitch counts as part of the gap. "Sc 4, inc" is 5 stitches of the old round becoming 6. Pick the right type in the calculator and it adjusts.</p>
<div class="callout"><strong>Crochet circles and hat crowns:</strong> if every round starts with its increase in the same place, the circle turns into a hexagon. Tick "Stagger" on alternate rounds to start halfway into a repeat. The count is the same; only the position moves.</div>
<h2>Examples worked out</h2></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">You have</th><th scope="col">Change</th><th scope="col">Working</th><th scope="col">Instruction</th><th scope="col">You end with</th></tr></thead><tbody>{id_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Square brackets mean repeat what's inside. The numbers come from the same maths as the calculator above.</p></div>
<div class="narrow prose"><h2>What next?</h2>
<p>Changing the stitch count because your swatch came out different? Check the new number with the <a href="{href("gauge-converter.html")}">gauge converter</a>. Shaping a hat crown? The <a href="{href("hat-size-chart.html")}">hat size calculator</a> gives the cast-on and where to start decreasing. Working in the round? The <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a> writes out every round of a flat circle or amigurumi ball. Keep track of increase rows with a second counter in the <a href="{href("row-counter.html")}">row counter</a>, and if a UK crochet pattern says "inc" in trebles, the <a href="{href("crochet-terms.html")}">US and UK crochet terms</a> chart translates it.</p></div></section>'''
id_faq = [
    ("How do I increase evenly across a row in knitting?", "Divide your stitches by the number of increases to get the gap. Working flat, split one gap between the two ends: for 80 stitches and 10 increases, K4, M1, (K8, M1) nine times, K4. In the round, just repeat (K8, M1) ten times."),
    ("How do I decrease evenly across a row?", "Divide your stitches by the number of decreases, then knit two fewer than that before each k2tog, because a decrease uses two stitches. For 90 stitches and 10 decreases: (K7, k2tog) ten times gives 80."),
    ("What if the stitches don't divide evenly by the increases?", "Some gaps are one stitch longer than others. For 62 stitches and 8 increases, six gaps are 8 stitches and two are 7. Spread the longer gaps out; the calculator does this for you."),
    ("Does kfb count as a stitch when spacing increases?", "Yes. Kfb and the crochet 2 sc in one stitch are worked into a stitch, so that stitch is part of the gap. M1 is made between stitches and uses none."),
    ("Why does my crochet circle look like a hexagon?", "The increases are stacking in the same place every round. Start alternate rounds halfway into the repeat, so the increases fall between the ones below."),
    ("What's the difference between k2tog and ssk?", "Both knit 2 stitches together to take one away. K2tog leans to the right and ssk leans to the left, so patterns often pair them on either side of a V-neck or raglan line."),
    ("How do I decrease 6 stitches evenly in a crochet round of 36?", "6 decreases use 12 stitches, leaving 24 plain stitches, 4 before each decrease: (sc 4, sc2tog) 6 times gives 30."),
]
page("increase-decrease-calculator.html", "Increase and Decrease Evenly Calculator for Knitting and Crochet | Purl & Paper",
     "Free calculator to increase or decrease evenly across a row or round, for knitting (M1, kfb, k2tog) and crochet (inc, sc2tog), with a written instruction and a stitch diagram.",
     idc, id_faq, "Increase evenly calculator", app_name="Increase and decrease evenly calculator")

# ---------------- HOW TO PRICE CROCHET ITEMS (guide + calculator) ----------------
PR_EX = [("Beanie", 5, 2.5), ("Amigurumi toy (15 cm)", 6, 5), ("Granny square throw", 60, 45), ("Market tote bag", 7, 4), ("Baby blanket", 35, 25)]
def pr_base(m, h, rate=15, oh=0.10): return (m + h * rate) * (1 + oh)
def pr_etsy(b): return (b + 0.45) / (1 - 0.095)
pr_rows = "".join(f'<tr><td>{n}</td><td>${m}</td><td>{h} h</td><td>${pr_base(m, h):,.0f}</td><td>${pr_etsy(pr_base(m, h)):,.0f}</td><td>${m * 3:,.0f}</td></tr>' for n, m, h in [(a, c, b) for a, b, c in PR_EX])
prc = top("How to price crochet and knitting items", "A fair price covers your materials, pays you for your time, and still leaves that after the shop or card reader takes its cut. Here's the formula, and a calculator that does the sums.", "How to price crochet") + f'''
<section style="padding-top:10px"><div class="narrow prose"><div class="quick"><strong>Quick answer:</strong> price = (materials + hours × your hourly rate) + a little for overheads, then add the selling fees. A beanie with $5 of yarn and 2.5 hours at $15 an hour is $42.50, about $47 with 10% for overheads, and about $52 on Etsy once its fees are covered. "Materials × 3" would say $15, which pays you about $4 an hour.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="pr-m">Materials for one item ($)</label><input type="number" id="pr-m" value="8" min="0" step="0.01" inputmode="decimal"><span class="note">Yarn (the share you used, stash yarn included), stuffing, eyes, buttons, labels, tags and packaging.</span></div>
<div class="row2"><div class="field"><label for="pr-h">Hours to make it</label><input type="number" id="pr-h" value="4" min="0" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="pr-r">Your hourly rate ($)</label><input type="number" id="pr-r" value="15" min="0" step="0.5" inputmode="decimal"></div></div>
<div class="field"><label for="pr-oh">Overheads (%)</label><input type="number" id="pr-oh" value="10" min="0" max="100" step="1" inputmode="decimal"><span class="note">Hooks, needles, printer ink, your phone photos, travel to the post office. 10% is our starting suggestion; raise it if you spend a lot on these.</span></div>
<div class="field"><label for="pr-ch">Where will you sell it?</label><select id="pr-ch"><option value="etsy">Etsy (US fees)</option><option value="fair">Craft fair or market</option><option value="direct">Direct to friends (cash or bank transfer)</option><option value="consign">Shop on consignment</option></select></div>
<div class="field"><label for="pr-cur">Currency</label><select id="pr-cur"><option value="$" selected>$ (US, CA, AU)</option><option value="£">£ (UK)</option><option value="€">€ (EU)</option><option value="₹">₹ (India)</option><option value="Rs ">Rs (Pakistan)</option></select><span class="note">Only the symbol changes: enter your own local prices and hourly rate. The Etsy fee setting uses US fees.</span></div>
<div id="pr-fair"><div class="row2"><div class="field"><label for="pr-bf">Booth or table fee ($)</label><input type="number" id="pr-bf" value="40" min="0" step="1" inputmode="decimal"></div>
<div class="field"><label for="pr-bn">Items you expect to sell</label><input type="number" id="pr-bn" value="20" min="1" step="1" inputmode="numeric"></div></div>
<div class="field"><label for="pr-cf">Card reader fee (%)</label><input type="number" id="pr-cf" value="3" min="0" max="20" step="0.1" inputmode="decimal"><span class="note">Most card readers take roughly 2.5 to 3.5% of each sale. Check your provider's rate.</span></div></div>
<div class="field" id="pr-con" hidden><label for="pr-cp">Shop's share (%)</label><input type="number" id="pr-cp" value="35" min="0" max="80" step="1" inputmode="decimal"><span class="note">Consignment shops usually keep somewhere between 20 and 50%.</span></div>
<div class="field"><label for="pr-try">A price you had in mind (optional, $)</label><input type="number" id="pr-try" placeholder="e.g. 30" min="0" step="0.5" inputmode="decimal"><span class="note">We'll show what you'd really earn per hour at that price.</span></div>
</div>
<div class="result" aria-live="polite" id="pr-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>What is the formula for pricing crochet items?</h2>
<p>Most experienced sellers use some version of this:</p>
<ol><li><strong>Materials.</strong> Every bit that goes into or onto the item: the yarn you used (work out the share of a skein by weight), stuffing, safety eyes, buttons, labels, tags, the bag it goes in.</li>
<li><strong>Labour.</strong> Hours × an hourly rate. Time yourself on the next one and round up to the nearest quarter hour; most people guess low.</li>
<li><strong>Overheads.</strong> Tools wear out and photos, printing and trips to the post office cost money. A percentage on top covers them without tracking every penny.</li>
<li><strong>Fees.</strong> Whoever processes the payment takes a cut. Add it on top, or it comes out of your hourly rate.</li></ol>
<p>Shipping is separate: charge what it costs you to post. (On Etsy the 6.5% transaction fee applies to the shipping you charge too.)</p>
<h2>What hourly rate should I charge for crochet?</h2>
<p>Start at no less than your local minimum wage. Popular crochet business guides suggest somewhere between $12 and $20 an hour in the US, and more for skilled work like garments, colourwork or custom orders. You can make your own choices about charging less for a friend, but price your shop items as a job, so a sale never costs you money.</p>
<h2>How much are Etsy's fees on a handmade item?</h2>
<ul><li><strong>Listing fee:</strong> $0.20 per item, renewed every 4 months or when it sells.</li>
<li><strong>Transaction fee:</strong> 6.5% of the order total, shipping and gift wrap included.</li>
<li><strong>Payment processing (US):</strong> 3% + $0.25 per order.</li>
<li><strong>Offsite Ads:</strong> 12 or 15% of an order, but only when the sale came from an ad Etsy placed for you.</li></ul>
<p>Together that's roughly 9.5% plus $0.45 on most sales, which the calculator adds for you. Fees change, and they're different outside the US, so check Etsy's own fees page before you set prices for the year.</p>
<h2>Why not just charge materials × 3?</h2>
<p>Because it ignores time. A beanie that takes 2 hours and a blanket that takes 45 can use similar money's worth of yarn. "Materials × 3" prices them almost the same and pays you a few dollars an hour for the blanket. It works for quick, cheap-to-make items, and that's about it.</p>
<h2>Example prices</h2></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Item</th><th scope="col">Materials</th><th scope="col">Time</th><th scope="col">Fair price</th><th scope="col">On Etsy</th><th scope="col">Materials × 3</th></tr></thead><tbody>{pr_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Our own examples, at $15 an hour plus 10% overheads; the Etsy column adds US fees (9.5% + $0.45). Materials and hours are typical guesses; use your own. Prices are rounded.</p></div>
<div class="narrow prose"><h2>What if the price feels too high?</h2>
<p>That's normal, and it's a sign the item takes real skill and time. You have three honest choices: sell it anyway to buyers who value handmade (craft fairs and gift buyers often do), make it faster (thicker yarn, a simpler stitch, fewer colour changes), or make something smaller that sells at a price you're happy with. Lowering your hourly rate until it hurts is the one that burns people out.</p>
<h2>How do I price a crochet blanket?</h2>
<p>With the same formula, but time matters even more: a throw can take 20 hours or more, so a fair price often lands in the hundreds. Count whole skeins, time yourself on a few rows and multiply out. Our <a href="{href("how-to-price-a-crochet-blanket.html")}">crochet blanket price calculator</a> estimates the yarn and hours for any size from lovey to king, and shows ways to bring the price down without working for free.</p>
<h2>How do I price amigurumi?</h2>
<p>Amigurumi is small but slow: tight single crochet on a small hook, plus the time to stuff, sew on limbs and embroider a face. Our tips:</p>
<ul><li><strong>Time the whole toy</strong>, sewing and finishing included. The parts often take as long as the body.</li>
<li><strong>Count every extra:</strong> stuffing, safety eyes, a ribbon or a gift tag, as well as the share of each skein you used.</li>
<li><strong>Offer sizes.</strong> A palm-sized toy or keyring at a lower price sells next to bigger pieces that show off your work.</li>
<li><strong>Check toy safety rules</strong> where you sell, especially for babies and young children (in the US, toys for children fall under the CPSIA). Embroidered eyes instead of safety eyes are a common choice for baby toys.</li></ul>
<p>Our <a href="{href("how-to-price-amigurumi.html")}">amigurumi price calculator</a> estimates the hours from the toy's size and number of parts, with a price chart from keyring to large plush. Or put your own materials and hours into the calculator above.</p>
<h2>How do I price a crochet commission or custom order?</h2>
<p>Use the same formula, then add for the extra work a custom piece brings:</p>
<ul><li><strong>Time a sample first.</strong> Work a swatch of the stitch and time it, then multiply out before you quote (EyeLoveKnots).</li>
<li><strong>Charge for design time.</strong> Sketching, working out a new size or shape and test pieces are part of the job (Hostinger).</li>
<li><strong>Use fixed add-ons</strong> for common requests, such as an embroidered name or an extra colour, so each quote is quick (Hostinger).</li>
<li><strong>Take payment up front</strong> before you buy the yarn (B.Hooked, EyeLoveKnots), and give a finish date you can keep (Daisy Cottage Designs).</li>
<li><strong>Stick to the quote.</strong> If you underestimated, raise the price for the next one, not this one (EyeLoveKnots). Changes after you start are new work, so quote them.</li></ul>
<p>For blankets, the <a href="{href("how-to-price-a-crochet-blanket.html")}">blanket price calculator</a> estimates the hours for you; for toys, use the <a href="{href("how-to-price-amigurumi.html")}">amigurumi price calculator</a>.</p>
<h2>How do I price crochet outside the US, for example in India or the UK?</h2>
<p>The formula doesn't change: materials + hours × an hourly rate + overheads + fees. Pick your currency in the calculator and use local numbers: what you paid for the yarn, and an hourly rate no lower than your local minimum wage. Fees are what differ most. Etsy's transaction fee is 6.5% everywhere, but payment processing and listing costs vary by country, and local marketplaces, card readers and Instagram or WhatsApp sales all have their own costs, so check the rates for where you sell. Our <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a> covers US and UK fees.</p>
<h2>Pricing for a craft fair</h2>
<ul><li><strong>Spread the table fee</strong> over the items you realistically expect to sell, not the number you're bringing.</li>
<li><strong>Bring a range</strong>: a few small makes under $15 (scrunchies, coasters, keychains) so people can buy something, and bigger pieces that show what you can do.</li>
<li><strong>Use round prices</strong> like $15, $25, $40. They're quicker to take and to make change for.</li></ul>
<p>Packing for the day? Our <a href="{href("craft-fair-checklist.html")}">craft fair checklist</a> covers the booth, payments, packaging and a cash float, and works out how much stock to bring.</p>
<h2>What next?</h2>
<p>Not sure how long an item takes? The <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a> has typical hours for 14 projects. Work out the yarn first with the <a href="{href("yarn-calculator.html")}">yarn calculator</a>, then log each make with its hours and yarn in the <a href="{href("projects.html")}">project tracker</a> so the next price is easier. Want this as a spreadsheet you can keep? Our pricing calculator in the shop below does it for every item you make.</p></div></section>'''
pr_faq = [
    ("What is the formula for pricing crochet items?", "Materials + (hours × your hourly rate), plus a percentage for overheads such as tools and packaging, plus the selling fees. Shipping is charged separately."),
    ("What hourly rate should I charge for crochet?", "At least your local minimum wage. Crochet business guides commonly suggest $12 to $20 an hour in the US, more for skilled or custom work."),
    ("How much should I charge for a crochet hat?", "With about $5 of yarn and 2.5 hours at $15 an hour, around $45 to $50, or about $52 on Etsy once fees are covered. Quick chunky hats can be less; colourwork or fine yarn more."),
    ("How much does Etsy take from a sale?", "In the US, 6.5% of the order including shipping, plus 3% + $0.25 for payment processing and $0.20 to list. That's roughly 9.5% + $0.45, more if the sale came from an Offsite Ad."),
    ("Is materials times 3 a good way to price crochet?", "Only for quick items. It ignores time, so anything that takes more than an hour or two ends up paying you very little."),
    ("How much should I charge for a crochet blanket?", "Add the whole skeins you used, your hours at a fair hourly rate, about 10% for overheads, then the fees. A worsted throw can take 20 to 25 hours, so a fair price is often a few hundred dollars. Chunky yarn and simple stitches make blankets quicker and cheaper to sell."),
    ("How do I price a crochet commission?", "Time a sample, then quote materials plus hours at your rate, with extra for design time and fixed add-ons for things like names. Take payment before you buy the yarn and give a finish date."),
    ("How do I price crochet items in India or outside the US?", "Use the same formula in your own currency: materials + hours × at least your local minimum wage + overheads + the fees where you sell. Only the fees and the numbers change."),
    ("How much should I charge for amigurumi?", "Price the whole toy's time, including stuffing, sewing on parts and the face, plus yarn, stuffing and eyes, then fees. A 15 cm toy that takes 5 hours with $6 of materials is around $89 at $15 an hour with 10% overheads."),
]
page("how-to-price-crochet-items.html", "How to Price Crochet and Knitting Items (Free Calculator) | Purl & Paper",
     "The formula for pricing crochet and knitted items to sell: materials, an hourly rate, overheads and Etsy or craft fair fees, with a free calculator and example prices.",
     prc, pr_faq, "How to price crochet", app_name="Crochet and knitting price calculator")

# ---------------- ETSY FEE CALCULATOR (senior SEO pass 25 Nov 2026; funnels to the pricing + business spreadsheets) ----------------
ef = top("Etsy fee calculator for handmade sellers", "Enter your price, shipping and costs. See every Etsy fee, what you keep, and the price you need to charge for the profit you want.", "Etsy fee calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> on a US sale Etsy takes a <strong>$0.20 listing fee</strong>, a <strong>6.5% transaction fee</strong> on the item price plus shipping, and <strong>3% + $0.25 payment processing</strong>. That is about 9.5% + $0.45 per order, or about a quarter of the order if the sale came through an Offsite Ad (15%, or 12% for shops over $10,000 a year).</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="ef-reg">Where your shop is</label><select id="ef-reg"><option value="us">United States ($)</option><option value="uk">United Kingdom (£)</option></select></div>
<div class="row2"><div class="field"><label for="ef-price">Item price</label><input type="number" id="ef-price" value="35" min="0" step="0.01" inputmode="decimal"></div>
<div class="field"><label for="ef-ship">Shipping you charge</label><input type="number" id="ef-ship" value="5" min="0" step="0.01" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="ef-cost">Your materials + packaging</label><input type="number" id="ef-cost" value="8" min="0" step="0.01" inputmode="decimal"></div>
<div class="field"><label for="ef-post">What postage costs you</label><input type="number" id="ef-post" value="5" min="0" step="0.01" inputmode="decimal"></div></div>
<div class="field"><label for="ef-ads">Did the sale come from an Offsite Ad?</label><select id="ef-ads"><option value="0">No</option><option value="0.15">Yes, 15% (shop under $10k a year)</option><option value="0.12">Yes, 12% (shop over $10k a year)</option></select></div>
<div class="field"><label for="ef-goal">Profit you want per sale (for the price finder)</label><input type="number" id="ef-goal" value="20" min="0" step="0.5" inputmode="decimal"></div>
</div>
<div class="result" aria-live="polite" id="ef-out"></div>
</div></section>
<script>(function(){{var R={{us:{{c:"$",tx:.065,pp:.03,pf:.25,lf:.20}},uk:{{c:"£",tx:.065,pp:.04,pf:.20,lf:.16}}}};function v(i){{return parseFloat(document.getElementById(i).value)||0}}function m(c,x){{return c+x.toFixed(2)}}
function run(){{var r=R[document.getElementById("ef-reg").value],P=v("ef-price"),S=v("ef-ship"),C=v("ef-cost"),Q=v("ef-post"),A=+document.getElementById("ef-ads").value,G=v("ef-goal"),T=P+S;
var lf=r.lf,tx=T*r.tx,pp=T*r.pp+r.pf,ad=T*A,fees=lf+tx+pp+ad,keep=T-fees,prof=keep-C-Q,rate=1-r.tx-r.pp-A,need=(G+C+Q+lf+r.pf)/rate-S;
document.getElementById("ef-out").innerHTML="<h2>Your Etsy fees</h2><table class=\\"mt\\"><tbody><tr><td>Listing fee</td><td>"+m(r.c,lf)+"</td></tr><tr><td>Transaction fee (6.5%)</td><td>"+m(r.c,tx)+"</td></tr><tr><td>Payment processing</td><td>"+m(r.c,pp)+"</td></tr>"+(A?"<tr><td>Offsite Ads ("+Math.round(A*100)+"%)</td><td>"+m(r.c,ad)+"</td></tr>":"")+"<tr><td><strong>Total Etsy fees</strong></td><td><strong>"+m(r.c,fees)+"</strong> ("+(T?Math.round(fees/T*1000)/10:0)+"% of the order)</td></tr><tr><td>Etsy pays you</td><td>"+m(r.c,keep)+"</td></tr><tr><td><strong>Your profit</strong> after materials and postage</td><td><strong>"+m(r.c,prof)+"</strong></td></tr></tbody></table><p>To make <strong>"+m(r.c,G)+"</strong> profit per sale with this shipping, charge at least <strong>"+m(r.c,Math.max(0,need))+"</strong> for the item.</p><p class=\\"muted\\">Profit before your time. Add your hours with the <a href=\\"{href("how-to-price-crochet-items.html")}\\">crochet pricing calculator</a>.</p>"}}
["ef-reg","ef-price","ef-ship","ef-cost","ef-post","ef-ads","ef-goal"].forEach(function(i){{document.getElementById(i).addEventListener("input",run)}});run()}})();</script>
<section><div class="wrap"><div class="narrow prose"><h2>Every Etsy fee, explained</h2>
<table class="mt"><thead><tr><th scope="col">Fee</th><th scope="col">US shop</th><th scope="col">UK shop</th><th scope="col">Charged on</th></tr></thead><tbody>
<tr><td>Listing fee</td><td>$0.20</td><td>$0.20 (about £0.16)</td><td>Each listing, renewed every 4 months or when it sells</td></tr>
<tr><td>Transaction fee</td><td>6.5%</td><td>6.5%</td><td>Item price + shipping + gift wrap</td></tr>
<tr><td>Payment processing</td><td>3% + $0.25</td><td>4% + £0.20</td><td>The full amount the buyer pays</td></tr>
<tr><td>Offsite Ads</td><td>15% (12% over $10k/yr)</td><td>15% (12% over $10k/yr)</td><td>Only sales that came from an Etsy ad on another site</td></tr>
</tbody></table>
<p class="muted">Rates checked against Etsy fee guides published in 2026 (Marmalead, Checkout Page, Printify). Etsy can change its fees, so check the Fees and Payments policy in your shop dashboard before you set prices. UK and EU shops can also be charged VAT on Etsy's fees.</p>
<h2>Three ways handmade sellers lose money on fees</h2>
<ul><li><strong>Free shipping without raising the price.</strong> The 6.5% applies to shipping too, so moving postage into the item price costs the same in fees but the postage still has to be paid.</li>
<li><strong>Cheap items.</strong> The fixed $0.45 (listing + processing) eats a much bigger share of a $5 bookmark than of a $60 blanket. Bundle small makes, or price them in sets.</li>
<li><strong>Forgetting Offsite Ads.</strong> One ad sale can take 12 to 15% more. Price so that even an ad sale still pays for your materials.</li></ul>
<h2>Work out the whole price, not just fees</h2>
<p>Fees are the last step. Start with materials and your time in the <a href="{href("how-to-price-crochet-items.html")}">crochet and knitting pricing calculator</a>, or see <a href="{href("how-to-price-a-crochet-blanket.html")}">how to price a crochet blanket</a>. Selling in person too? The <a href="{href("craft-fair-checklist.html")}">craft fair checklist</a> covers card readers, floats and stock.</p>
<p>Want it all in one place? Our <strong>pricing spreadsheets</strong> track materials, hours, Etsy fees and profit for every item you make.</p></div></div></section>
{shop_box("etsy-fee-calculator.html")}'''
ef_faq = [
    ("How much does Etsy take per sale?", "In the US, $0.20 to list, 6.5% of the item price plus shipping, and 3% + $0.25 for payment processing. That is about 9.5% + $0.45 per order. If the sale came from an Offsite Ad, add 15% (12% for shops selling over $10,000 a year)."),
    ("Does Etsy charge fees on shipping?", "Yes. The 6.5% transaction fee and the payment processing fee both apply to the shipping you charge, not just the item price."),
    ("What are Etsy fees in the UK?", "The same $0.20 listing fee and 6.5% transaction fee, with payment processing of 4% + £0.20. UK shops can also be charged VAT on Etsy's fees."),
    ("How do I price my item to cover Etsy fees?", "Add your materials, postage, the fixed fees and the profit you want, then divide by what is left after the percentage fees (about 0.905 in the US). The calculator above does this for you."),
    ("Can I turn off Etsy Offsite Ads?", "Shops that made under $10,000 in the past 12 months can opt out in their shop settings. Bigger shops are enrolled at the 12% rate."),
]
page("etsy-fee-calculator.html", "Etsy Fee Calculator 2026: Fees, Profit and Price to Charge (US + UK) | Purl & Paper",
     "Free Etsy fee calculator for handmade sellers: listing, 6.5% transaction, payment processing and Offsite Ads fees, your profit, and the price to charge. US and UK.",
     ef, ef_faq, "Etsy fee calculator", app_name="Etsy fee calculator")

# ---------------- SOCK SIZE CHART + CALCULATOR ----------------
SK = D["socks"]
SOCK_K = 1.32   # yd of fingering per sq in of sock fabric (leg + foot, heel and toe included). Our estimate: a women's medium pair ~350 yd.
def sk_mid(x): return (x["lmin"] + x["lmax"]) / 2
def sk_co(circ, spi=8, ease=0.10, rep=4): return max(rep, int(circ * (1 - ease) * spi / rep + 0.5) * rep)
def sk_yd(x, f=1.0): return int(SOCK_K * x["circ"] * (sk_mid(x) + x["leg"]) * 2 * f / 5 + 0.5) * 5
sk_opts = "".join(f'<option value="{x["id"]}"{" selected" if x["id"] == "women-m" else ""}>{e(x["name"])} ({e(x["shoe"])})</option>' for x in SK) + '<option value="custom">I measured a foot</option>'
sk_rows = "".join(f'<tr><td><strong>{e(x["name"])}</strong><br><span class="muted">{e(x["shoe"] if x["shoe"] == x["age"] else x["age"] + ", " + x["shoe"])}</span></td><td>{x["circ"]:g} in<br><span class="muted">{round(x["circ"] * 2.54, 1):g} cm</span></td>'
                  f'<td>{x["lmin"]:g}–{x["lmax"]:g} in<br><span class="muted">{round(x["lmin"] * 2.54)}–{round(x["lmax"] * 2.54)} cm</span></td><td>{x["leg"]:g} in<br><span class="muted">{round(x["leg"] * 2.54)} cm</span></td>'
                  f'<td>{sk_co(x["circ"])}</td><td>about {sk_yd(x)} yd</td></tr>' for x in SK)
_wm = next(x for x in SK if x["id"] == "women-m"); _mm = next(x for x in SK if x["id"] == "men-m"); _ml = next(x for x in SK if x["id"] == "men-l")
sk = top("Sock size chart and sock knitting calculator", "Foot sizes from baby to men's 14, how much smaller to knit the sock, and the numbers for your cast-on, heel flap, gusset and toe, worked out from your own gauge.", "Sock size chart") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> knit socks about 10% smaller around than the foot. A women's medium foot (US 7–9½) is about 8 in around, so the sock is about 7.2 in; at 8 stitches per inch in fingering yarn that's <strong>{sk_co(_wm["circ"])} stitches</strong>. A men's medium (US 9–11½) foot is about 9 in around, so <strong>{sk_co(_mm["circ"])} stitches</strong>. Start the toe when the foot measures 2 in less than the whole foot.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="sk-size">Who is it for?</label><select id="sk-size">{sk_opts}</select></div>
<div id="sk-custom" hidden><div class="row2"><div class="field"><label for="sk-circ">Foot around (ball of foot)</label><input type="number" id="sk-circ" value="8" min="3" max="40" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="sk-len">Foot length (heel to toe)</label><input type="number" id="sk-len" value="9.5" min="3" max="40" step="0.25" inputmode="decimal"></div></div>
<div class="field"><label for="sk-mu">Unit</label><select id="sk-mu"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><label for="sk-yarn">Yarn</label><select id="sk-yarn"><option value="1|32" selected>Fingering or sock yarn (4 ply)</option><option value="0.8|26">Sport (5 ply)</option><option value="0.65|22">DK (8 ply)</option></select></div>
<div class="row2"><div class="field"><label for="sk-g">Stitches in your swatch</label><input type="number" id="sk-g" value="32" min="8" max="60" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="sk-gu">Measured over</label><select id="sk-gu"><option value="4">4 in</option><option value="10">10 cm</option></select></div></div>
<div class="field"><label for="sk-ease">How snug?</label><select id="sk-ease"><option value="15">Firm, for thin or very stretchy yarn (15% smaller)</option><option value="10" selected>Standard fit (10% smaller)</option><option value="5">Roomy, for thick yarn or bed socks (5% smaller)</option></select></div>
<div class="field"><label for="sk-rep">Round the count to a multiple of</label><select id="sk-rep"><option value="2">2 (1x1 rib)</option><option value="4" selected>4 (2x2 rib, 4 needles)</option><option value="8">8 (bigger stitch patterns)</option></select></div>
<figure class="ht-fig"><svg id="sk-svg" viewBox="0 0 320 240" role="img" aria-label="Sock drawn with its leg and foot lengths"></svg><figcaption class="note" id="sk-cap">Your sock.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="sk-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>What size sock do I knit? Sock size chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size</th><th scope="col">Foot around</th><th scope="col">Foot length</th><th scope="col">Leg (cuff to heel)</th><th scope="col">Cast on at 8 sts/in</th><th scope="col">Fingering yarn, pair</th></tr></thead><tbody>{sk_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Foot around, foot length and leg height are from the Craft Yarn Council's foot size chart (US shoe sizes). Cast-on counts are our own maths: 10% negative ease at 8 stitches per inch, rounded to a multiple of 4. Yarn per pair is our estimate for plain stockinette socks with a ribbed cuff; textured stitches, cables and taller legs need more. Buy an extra ball if you're between amounts.</p>
</div></section>
{AD.format("sock-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How do I measure a foot for socks?</h2>
<ul><li><strong>Around:</strong> wrap a soft tape around the widest part of the foot, across the ball just behind the toes. Keep it snug, not tight.</li>
<li><strong>Length:</strong> stand on a piece of paper, mark the back of the heel and the tip of the longest toe, and measure between the marks.</li>
<li><strong>Making a surprise?</strong> Use the chart for their shoe size, or measure a pair of their own socks laid flat (double the width).</li></ul>
<p>The ankle is usually about the same size around as the ball of the foot, so a plain sock keeps the same stitch count from cuff to toe.</p>
<h2>How much negative ease should socks have?</h2>
<p>About 10%. A sock that's slightly smaller than the foot stretches to hug it and doesn't wrinkle or slip down. Knitty and Mary Maxim both recommend around 10%. Go a little smaller for loose, stretchy fabric and a little bigger for thick yarn, firm stitch patterns or colourwork, which stretch less.</p>
<h2>How many stitches do I cast on for socks?</h2>
<p>Multiply the foot measurement by 0.9, then by your stitches per inch, and round to a number that fits your rib. A women's medium foot of 8 in × 0.9 = 7.2 in. At 8 stitches per inch that's 57.6, so cast on {sk_co(_wm["circ"])}. At 7.5 stitches per inch it's 54, which rounds to 56 too. Thicker sock yarn at 6.5 stitches per inch gives 47, so cast on 48.</p>
<div class="callout"><strong>Swatch in the round</strong> on the needles you'll use, then wash and dry it. Sock gauge is tight (often 28 to 32 stitches over 4 in), so a quarter stitch per inch changes a sock by about 2 stitches.</div>
<h2>Heel flap, gusset and toe: the numbers</h2>
<ol><li><strong>Leg:</strong> knit the cuff and leg to the height you like. The chart gives a standard crew height.</li>
<li><strong>Heel flap:</strong> work back and forth on half the stitches. Many patterns make the flap about as many rows as it has stitches, so it ends up roughly square; others use fewer rows for a shallower heel.</li>
<li><strong>Turn the heel,</strong> then pick up about one stitch for every two flap rows along each side, plus one in the corner to close the gap.</li>
<li><strong>Gusset:</strong> decrease 2 stitches every other round until you're back to the cast-on count.</li>
<li><strong>Foot:</strong> knit straight until the sock measures 2 in less than the whole foot (adults). Children's toes are shorter, so the calculator uses about a fifth of the foot length for small sizes (our estimate).</li>
<li><strong>Toe:</strong> decrease 4 stitches every other round until about half the stitches are left, then every round until about a quarter remain. Graft the toe closed.</li></ol>
<p>Knitting toe-up? Use the same stitch count for the foot, work the toe increases first, and start the heel when the foot reaches the front of the ankle. Spacing increases or decreases around a cuff? The <a href="{href("increase-decrease-calculator.html")}">increase evenly calculator</a> writes the round out for you.</p>
<h2>How much yarn do I need for a pair of socks?</h2>
<p>One 100 g skein of fingering sock yarn (usually around 400 to 460 yards) makes a pair of plain adult socks in most sizes up to a men's medium. A men's large or a tall leg can need around {sk_yd(_ml)} yards, so buy a little extra. Children's socks often fit in one 50 g ball. Sport and DK socks use fewer yards but more grams. The calculator above gives an estimate for your size and yarn.</p>
<h2>What about crochet socks?</h2>
<p>Crochet stretches less than knitting, so crochet sock patterns usually leave less negative ease. Measure the same way, then follow your pattern's ease and try the sock on as you go.</p>
<p>What next? Check your needle size on the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>, see what "fingering" means on the <a href="{href("yarn-weights.html")}">yarn weight chart</a>, keep track of heel rows with the <a href="{href("row-counter.html")}">row counter</a>, and see if gift socks will be ready by Christmas in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Matching hat? Try the <a href="{href("hat-size-chart.html")}">hat size calculator</a>.</p></div></section>'''
sk_faq = [
    ("How many stitches do I cast on for women's socks?", f"For an average women's foot (about 8 in around) in fingering yarn at 8 stitches per inch, cast on about {sk_co(_wm['circ'])} stitches. That's 10% smaller than the foot, rounded to a multiple of 4."),
    ("How many stitches for men's socks?", f"An average men's foot (US 9–11½) is about 9 in around, so at 8 stitches per inch cast on about {sk_co(_mm['circ'])} stitches. A large men's foot (US 12–14) needs about {sk_co(_ml['circ'])}."),
    ("How much negative ease for socks?", "About 10%. Knit the sock 10% smaller around than the ball of the foot so it stretches to fit; a little more for loose fabric, a little less for thick yarn or colourwork."),
    ("When do I start the toe on a sock?", "On a cuff-down adult sock, start the toe decreases when the foot measures about 2 inches less than the full length of the foot. Children's toes are shorter."),
    ("How much yarn do I need for socks?", "A pair of plain adult socks usually takes one 100 g skein of fingering yarn, roughly 350 to 450 yards. Large men's sizes and tall legs may need more, and children's socks often fit in a 50 g ball."),
    ("How long should a heel flap be?", "Work the heel flap on half the stitches. Many patterns make it about as many rows as it has stitches, so it's roughly square; some use fewer rows for a shallower heel."),
]
page("sock-size-chart.html", "Sock Size Chart for Knitting, with Cast-On Calculator | Purl & Paper",
     "Free sock size chart from baby to men's 14 (foot around, length, leg height) plus a sock knitting calculator: cast-on stitches, heel flap, gusset, toe and yarn for your gauge.",
     sk, sk_faq, "Sock size chart", app_name="Sock knitting calculator")

# ---------------- YARN SUBSTITUTION CALCULATOR ----------------
W_OPTS = lambda sel: "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == sel else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])})</option>' for w in D["weights"])
def ys_need(n, per, per2, strands=1): return n * per * strands / per2
def ys_buy(n, per, per2, strands=1):
    x = ys_need(n, per, per2, strands); return x, int(-(-round(x, 6) // 1))
YS_EX = [("10 balls of 120 m", 10, 120, "75 m balls", 75, 1, "m"),
         ("9 skeins of 200 yd", 9, 200, "109 yd skeins", 109, 1, "yd"),
         ("5 skeins of 200 yd", 5, 200, "170 yd skeins", 170, 1, "yd"),
         ("6 skeins of 220 yd (worsted)", 6, 220, "one-pound skeins of 364 yd", 364, 1, "yd"),
         ("8 balls of 120 m (DK)", 8, 120, "200 m fingering balls, held double", 200, 2, "m")]
def fmt_n(x): return f"{x:,.0f}"
ys_rows = "".join(f'<tr><td>{e(a)}</td><td>{fmt_n(n * p * s)} {u}{" (×2 strands)" if s > 1 else ""}</td><td>{e(b)}</td><td>{ys_buy(n, p, q, s)[0]:.1f}</td><td><strong>{ys_buy(n, p, q, s)[1]}</strong></td></tr>'
                  for a, n, p, b, q, s, u in YS_EX)
ys = top("Yarn substitution calculator", "Swapping the yarn in a pattern? Find out how many balls of your yarn to buy, check it's a similar thickness, and see what happens if you hold two strands together.", "Yarn substitution calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> multiply the pattern's number of balls by the length of one ball to get the total length. Divide that by the length of one ball of your yarn, then round up. A pattern asking for 10 balls of 120 m needs 1,200 m, so with 75 m balls you buy <strong>16</strong>. Keep both lengths in the same unit, stay in the same yarn weight, and swatch before you start.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">The pattern's yarn</h2>
<div class="row2"><div class="field"><label for="ys-n">Balls or skeins</label><input type="number" id="ys-n" value="10" min="0.5" max="200" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="ys-pw">Yarn weight</label><select id="ys-pw">{W_OPTS(4)}</select></div></div>
<div class="row2"><div class="field"><label for="ys-pl">Length per ball</label><input type="number" id="ys-pl" value="120" min="1" max="3000" step="1" inputmode="decimal"></div>
<div class="field"><label for="ys-pu">Unit</label><select id="ys-pu"><option value="m">metres</option><option value="yd">yards</option></select></div></div>
<div class="field"><label for="ys-pg">Grams per ball (optional, for the thickness check)</label><input type="number" id="ys-pg" value="50" min="0" max="1000" step="1" inputmode="decimal"></div>
<hr class="stitch" style="margin:14px 0 18px">
<h2 style="font-size:1.25rem;margin-bottom:10px">Your yarn</h2>
<div class="row2"><div class="field"><label for="ys-ml">Length per ball</label><input type="number" id="ys-ml" value="100" min="1" max="3000" step="1" inputmode="decimal"></div>
<div class="field"><label for="ys-mu">Unit</label><select id="ys-mu"><option value="m">metres</option><option value="yd">yards</option></select></div></div>
<div class="row2"><div class="field"><label for="ys-mg">Grams per ball (optional)</label><input type="number" id="ys-mg" value="40" min="0" max="1000" step="1" inputmode="decimal"></div>
<div class="field"><label for="ys-mw">Yarn weight</label><select id="ys-mw">{W_OPTS(4)}</select></div></div>
<div class="field"><label>Strands</label><div class="seg" id="ys-st" role="group" aria-label="Strands held together"><button type="button" data-v="1" aria-pressed="true">One strand</button><button type="button" data-v="2" aria-pressed="false">Held double</button></div></div>
<div class="field"><label>Spare</label><div class="seg" id="ys-sp" role="group" aria-label="Spare yarn"><button type="button" data-v="0" aria-pressed="false">None</button><button type="button" data-v="10" aria-pressed="true">Add 10%</button><button type="button" data-v="ball" aria-pressed="false">One extra ball</button></div></div>
</div>
<div class="result" aria-live="polite" id="ys-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>Yarn substitution examples</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Pattern asks for</th><th scope="col">Total length</th><th scope="col">Your yarn</th><th scope="col">Exact balls</th><th scope="col">Buy</th></tr></thead><tbody>{ys_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Worked with the same formula as the calculator, before any spare. Our own examples.</p>
</div></section>
{AD.format("ys-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How do I work out how much substitute yarn I need?</h2>
<ol><li><strong>Find the total length</strong> the pattern uses: number of balls × length of one ball. Nine skeins of 200 yards is 1,800 yards.</li>
<li><strong>Divide by the length of one ball of your yarn.</strong> 1,800 ÷ 109 = 16.5.</li>
<li><strong>Round up.</strong> You can't buy half a ball, so that's 17.</li></ol>
<p>Always compare length, not grams. Two 50 g balls can hold very different lengths: a fluffy wool might give 150 m, while a dense cotton of the same thickness gives 100 m. One yard is 0.9144 m and one metre is 1.094 yards, so if one label is in yards and the other in metres, the calculator converts for you.</p>
<h2>What should match when I swap a yarn?</h2>
<ul><li><strong>Yarn weight.</strong> Start with the same weight number (DK for DK, worsted for worsted). See the <a href="{href("yarn-weights.html")}">yarn weight chart</a> if a label uses a UK or Australian name.</li>
<li><strong>Gauge.</strong> Knit or crochet a swatch with the pattern's needle or hook, wash and dry it, and measure. Being a stitch or two out over 10 cm is usually fixable with a different needle or hook size. The <a href="{href("gauge-converter.html")}">gauge converter</a> shows how much a difference changes the finished size.</li>
<li><strong>Length per 100 g.</strong> Within one weight there's a range. If your yarn has a similar length per gram to the pattern yarn, the thickness is probably close. The calculator compares them if you enter the grams.</li>
<li><strong>Fibre.</strong> Wool is springy and holds ribbing; cotton and bamboo are heavier, drape more and stretch less. Swapping wool for cotton in a fitted sweater can make it grow and hang. Blankets, shawls and scarves are more forgiving.</li>
<li><strong>Texture.</strong> A plied, smooth yarn shows stitches and cables clearly. Single-ply, fuzzy, chenille or boucle yarns blur them.</li></ul>
<div class="callout"><strong>Buy one extra ball.</strong> Swatching uses yarn, and your tension may be looser than the designer's. Buying 10 to 15% more, or one extra ball, saves hunting for a matching dye lot later. Check all balls share the same dye lot number on the label.</div>
<h2>Can I hold two strands together instead?</h2>
<p>Yes, two thinner yarns held together can stand in for one thicker yarn, but you'll need twice the length, and you must swatch, because doubled yarn doesn't always behave like a single strand of the heavier weight. Common rules of thumb:</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Two strands of</th><th scope="col">Works roughly like</th></tr></thead><tbody>
<tr><td>Fingering (1)</td><td>DK or sport (3 or 2)</td></tr><tr><td>Sport (2)</td><td>Worsted (4)</td></tr><tr><td>DK (3)</td><td>Worsted or aran (4)</td></tr><tr><td>Worsted or aran (4)</td><td>Chunky or bulky (5)</td></tr></tbody></table></div>
<p class="note">Rules of thumb from LoveCrafts and Love Life Yarn. Treat them as starting points for a swatch, not a guarantee.</p>
<h2>What if my yarn is a different weight?</h2>
<p>It can work, but the pattern's numbers won't. A thicker yarn at the pattern's stitch count makes a bigger piece; a thinner one makes a smaller, denser piece. For a blanket or scarf, that may not matter, and the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a> or <a href="{href("yarn-calculator.html")}">yarn calculator</a> can re-estimate the yarn. For anything that has to fit, match the weight or rework the stitch counts from your own gauge.</p>
<p>Using up a leftover ball with no label? Weigh it in the <a href="{href("yarn-yardage-calculator.html")}">yarn yardage calculator</a> to see how many yards are left before you start.</p>
<p>What next? Note the yarn you chose in the <a href="{href("projects.html")}">project tracker</a>, and check the needle or hook to start with on the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>.</p></div></section>'''
ys_faq = [
    ("How do I calculate how much yarn I need when substituting?", "Multiply the pattern's number of balls by the length per ball to get the total length, then divide by the length per ball of your yarn and round up. Use the same unit (yards or metres) for both."),
    ("Can I substitute yarn by weight in grams?", "Not safely. Two yarns of the same weight in grams can have very different lengths. Always compare length (yards or metres), and use grams only to check the yarns are a similar thickness."),
    ("What happens if I use a different yarn weight than the pattern?", "Your gauge changes, so the piece comes out bigger or smaller than the pattern says, and the yarn amount changes too. Match the weight, or work out new stitch counts from your swatch."),
    ("Is two strands of DK the same as worsted?", "Roughly. Two strands of DK held together usually work like a worsted or aran yarn, but swatch first, and remember you'll need twice the length of DK."),
    ("How much extra yarn should I buy when substituting?", "Round up to the next whole ball, then add about 10 to 15% or one extra ball for swatching and differences in tension. Buy it all from the same dye lot."),
]
page("yarn-substitution-calculator.html", "Yarn Substitution Calculator: How Many Balls of a Different Yarn? | Purl & Paper",
     "Free yarn substitution calculator: turn the pattern's yarn into balls of your yarn (yards or metres), check the thickness by length per 100 g, and plan holding two strands together.",
     ys, ys_faq, "Yarn substitution calculator", app_name="Yarn substitution calculator")

# ---------------- HOW TO TEA STAIN PAPER (guide + shade tester) ----------------
ts = top("How to tea stain paper for junk journals", "Turn plain paper into warm, aged pages with a cup of tea. Here's the recipe, four ways to apply it, how to dry it flat, and how to add spots, rings and torn edges.", "How to tea stain paper") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> steep about 3 black tea bags in half a cup of hot water for 5 minutes. Let it cool a little, then brush, sponge or dip the paper, letting some tea puddle for a natural look. Dry it flat, or speed it up on a baking sheet in a low oven (about 200°F / 95°C) for around 5 minutes while you watch it. Thick paper like watercolour or mixed-media paper works best.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Try a tea shade before you stain</h2>
<div class="field"><label for="ts-tea">What's in the cup?</label><select id="ts-tea"><option value="black" selected>Black tea</option><option value="green">Green tea</option><option value="coffee">Instant coffee</option><option value="herbal">Herbal or fruit tea</option></select></div>
<div class="field"><label>Strength</label><div class="seg" id="ts-str" role="group" aria-label="Strength"><button type="button" data-v="1" aria-pressed="false">Light</button><button type="button" data-v="2" aria-pressed="true">Medium</button><button type="button" data-v="3" aria-pressed="false">Strong</button></div></div>
<div class="field"><label for="ts-how">How you apply it</label><select id="ts-how"><option value="brush" selected>Brush or sponge</option><option value="dip">Dip or soak</option><option value="dab">Dab with the wet tea bag</option><option value="pour">Pour on a tray and press</option></select></div>
<div class="field"><label>Coats</label><div class="seg" id="ts-coats" role="group" aria-label="Coats"><button type="button" data-v="1" aria-pressed="true">1</button><button type="button" data-v="2" aria-pressed="false">2</button><button type="button" data-v="3" aria-pressed="false">3</button></div></div>
<fieldset class="field ts-ex"><legend>Extras</legend>
<label><input type="checkbox" id="ts-spots"> Age spots (sprinkled tea or coffee)</label>
<label><input type="checkbox" id="ts-ring"> Mug ring</label>
<label><input type="checkbox" id="ts-crumple"> Crumpled first</label>
<label><input type="checkbox" id="ts-torn" checked> Torn edges</label></fieldset>
<figure class="ts-fig"><svg id="ts-svg" viewBox="0 0 300 380" role="img" aria-label="Preview of a tea stained page"></svg><figcaption class="note">A rough preview. Real colours depend on your paper and tea.</figcaption></figure>
<p><button type="button" class="btn ghost" id="ts-again">Stain another sheet</button></p>
</div>
<div class="result" aria-live="polite" id="ts-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>What you need</h2>
<ul><li><strong>Tea:</strong> plain black tea bags (no milk). Used bags work for dabbing.</li>
<li><strong>Paper:</strong> watercolour, mixed-media or heavy cardstock is the easiest. Printer paper works if you're gentle.</li>
<li><strong>A shallow tray or baking sheet</strong>, a wide brush or sponge, paper towels and something flat and heavy, like a stack of books.</li>
<li><strong>Optional:</strong> instant coffee or instant tea for spots, a mug for rings, a waterproof pen if you want to write first.</li></ul>
<h2>How to tea stain paper, step by step</h2>
<ol><li><strong>Brew it strong.</strong> About 3 black tea bags in half a cup of hot water, steeped for about 5 minutes. More bags, or a longer steep, gives a deeper colour.</li>
<li><strong>Let it cool a little.</strong> Hot tea burns fingers and can turn black tea more orange.</li>
<li><strong>Protect the table</strong> and lay the paper on the tray. Crumple it first if you want creases.</li>
<li><strong>Apply the tea</strong> with one of the methods below. Let it pool in places; uneven is what makes it look old.</li>
<li><strong>Add extras while it's damp:</strong> sprinkle a few grains of instant tea or coffee for spots, or stand a wet mug on it for a ring.</li>
<li><strong>Dry it flat</strong> (see below). For a darker sheet, add another coat once it's dry.</li></ol>
<h2>Four ways to apply the tea</h2>
<ul><li><strong>Brush or sponge:</strong> the most control. Paint the whole sheet, just the edges, or let drops fall from the brush.</li>
<li><strong>Dip or soak:</strong> lay the sheet in a shallow tray of tea for a few minutes. The longer it sits, the darker it gets, but thin paper can turn to mush, so lift it gently with both hands.</li>
<li><strong>Dab with the tea bag:</strong> squeeze a wet bag and press it over the page for blotchy, patchy colour. Good for using up bags from your own cups.</li>
<li><strong>Pour and press:</strong> pour a little tea onto a rimmed baking sheet, lay the paper in it, press, wait a couple of minutes and lift. This gives puddles and tide lines.</li></ul>
<h2>Which paper is best for tea staining?</h2>
<p>Thick paper holds up best when wet. Watercolour paper (especially smooth hot-press) and mixed-media paper barely buckle. Cardstock and heavy cotton or rag paper are good too. Thin copy paper tears and can fall apart in a soak, so brush it rather than dipping. You can stain pages that are already sewn into a journal: brush them and put waxed paper or foil between wet pages so they don't stick.</p>
<h2>How to dry tea stained paper flat</h2>
<ul><li><strong>Air dry:</strong> lay it flat on a towel, away from direct sun. It can take several hours, up to a day for a soaked sheet.</li>
<li><strong>Press it:</strong> once it's only damp, put a paper towel on top and weigh it down with books, or a sheet of glass, so it dries flat. Don't move a wet sheet more than you have to; it tears easily.</li>
<li><strong>Oven:</strong> on a baking sheet in a low oven, about 200°F (95°C) or your lowest setting, for about 5 minutes. Baking also deepens the colour. Stay right there: paper can scorch or go brittle quickly. Keep it on the tray, away from the heating elements, and use oven gloves.</li>
<li><strong>Hair dryer:</strong> on a low setting, for one sheet when you're in a hurry.</li></ul>
<div class="callout"><strong>Safety first:</strong> let the tea cool before children help, never leave paper in the oven unattended, and keep the oven at its lowest setting.</div>
<h2>Tea stain colours: black, green, coffee and herbal</h2>
<ul><li><strong>Black tea</strong> gives the classic warm, golden brown. It's the most reliable.</li>
<li><strong>Green tea</strong> gives a paler, yellow-green tint and needs more bags for the same depth.</li>
<li><strong>Instant coffee</strong> stains darker and browner, good for "very old" pages and spots.</li>
<li><strong>Herbal and fruit teas</strong> are a gamble: a red tea can dry grey or green. Test a scrap first.</li></ul>
<h2>Easy ways to make paper look older</h2>
<ul><li><strong>Age spots:</strong> sprinkle a pinch of instant tea or coffee onto damp (not soaking) paper and brush the grains off when dry.</li>
<li><strong>Rings:</strong> stand a wet mug or teapot on the sheet while it dries.</li>
<li><strong>Creases:</strong> crumple the paper before staining; tea collects in the folds and darkens them.</li>
<li><strong>Soft torn edges:</strong> rub or tear the edges while wet for a worn, fuzzy edge.</li>
<li><strong>Speckles:</strong> flick clean water on first, then brush tea over.</li>
<li><strong>Writing:</strong> write or stamp on the page before staining, with a waterproof pen, so the ink ages with the paper.</li></ul>
<h2>Will tea stained paper fade?</h2>
<p>It can. Tea isn't a lightfast dye, so a page left in a sunny window will fade over time. Inside a closed journal it keeps its colour well. Seal a page with matte gel medium if you want extra protection.</p>
<p>What next? Use your stained paper in your first journal with our <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a> guide, then shuffle a theme for the page with the <a href="{href("journal-prompts.html")}">junk journal prompt generator</a>, and pick things to glue on top from our <a href="{href("junk-journal-ephemera-ideas.html")}">ephemera ideas checklist</a>. Prefer ready-made aged papers? Our Tea Room kit below is printable tea-stained pages.</p></div></section>'''
ts_faq = [
    ("How do you tea stain paper?", "Steep about 3 black tea bags in half a cup of hot water for 5 minutes, let it cool a little, then brush, dip or dab it onto the paper. Let some tea puddle for a natural look and dry the sheet flat."),
    ("How long do you soak paper in tea?", "A few minutes is enough for most papers. Longer gives a darker colour, but thin paper can fall apart, so brush thin paper instead of soaking it."),
    ("Can you dry tea stained paper in the oven?", "Yes. Put it on a baking sheet in a low oven, about 200°F (95°C) or your lowest setting, for around 5 minutes. Watch it the whole time, because paper can scorch or turn brittle."),
    ("What paper is best for tea staining?", "Watercolour, mixed-media and heavy cardstock hold up best when wet. Thin printer paper works if you brush it gently rather than soaking."),
    ("Is coffee or tea better for staining paper?", "Black tea gives a warm golden brown. Coffee gives a darker, browner stain. Many journalers use tea for the page and a sprinkle of instant coffee for age spots."),
    ("How do you stop tea stained paper from curling?", "Dry it flat. Once it's only damp, cover it with a paper towel and press it under heavy books or a sheet of glass until fully dry."),
]
page("how-to-tea-stain-paper.html", "How to Tea Stain Paper for Junk Journals (Oven or Air Dry) | Purl & Paper",
     "How to tea stain paper for junk journals: the tea recipe, four ways to apply it, the best paper, drying flat or in the oven, and easy age spots, rings and torn edges. With a shade tester.",
     ts, ts_faq, "How to tea stain paper")

# ---------------- CAST ON CALCULATOR ----------------
CO_G = {1: 28, 2: 24, 3: 22, 4: 18, 5: 14, 6: 9, 7: 6}   # typical stitches per 4 in: middle of each Craft Yarn Council knit range (jumbo: 6 and fewer)
CO_TAIL = 4.5   # long-tail estimate: tail per stitch = 4.5 / stitches per inch (about 1 in per stitch at worsted), plus 6 in. Our estimate.
def co_count(width, g4, mult=1, extra=0, border=0, selv=1):
    spi = g4 / 4; b = int(border * spi + 0.5) if border else 0
    reps = max(1, int((width * spi - 2 * b - 2 * selv - extra) / mult + 0.5))
    return reps * mult + extra + 2 * b + 2 * selv
CO_PRE = [("scarf-child", "Child's scarf", 6, "flat"), ("scarf", "Adult scarf", 8, "flat"), ("scarf-wide", "Wide scarf", 10, "flat"), ("wrap", "Wrap or stole", 20, "flat"),
          ("dishcloth", "Dishcloth", 8, "flat"), ("cowl", "Cowl (in the round)", 24, "round"), ("infinity", "Infinity scarf (in the round)", 55, "round")]
co_bl = [b for b in D["blankets"] if b["id"] in ("lovey", "stroller", "baby", "crib", "throw", "twin", "queen")]
co_opts = "".join(f'<option value="{w}|{m}"{" selected" if k == "scarf" else ""}>{e(n)}, {w} in{" around" if m == "round" else " wide"}</option>' for k, n, w, m in CO_PRE) + \
          "".join(f'<option value="{b["w"]}|flat">{e(b["name"])} blanket, {b["w"]} in wide</option>' for b in co_bl) + '<option value="custom">My own width</option>'
co_wopts = "".join(f'<option value="{w["n"]}|{CO_G[w["n"]]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])})</option>' for w in D["weights"] if w["n"] in CO_G)
CO_EX = [("Child's scarf", 6), ("Dishcloth", 8), ("Adult scarf", 8), ("Wide scarf", 10), ("Baby blanket", 36), ("Throw blanket", 50)]
CO_EXW = [(1, "Fingering"), (3, "DK"), (4, "Worsted"), (5, "Bulky"), (6, "Super bulky")]
co_rows = "".join(f'<tr><td><strong>{e(n)}</strong><br><span class="muted">{w} in ({round(w * 2.54)} cm) wide</span></td>' + "".join(f"<td>{co_count(w, CO_G[k])}</td>" for k, _ in CO_EXW) + "</tr>" for n, w in CO_EX)
_co_sc = co_count(8, 18); _co_th = co_count(50, 18); _co_ch = co_count(8, 9)
co = top("Cast on calculator: how many stitches to cast on", "Pick what you're making, your yarn and your gauge. Get the cast-on number that fits your stitch pattern, borders and edge stitches, how wide it will really be, and how long to leave the tail.", "Cast on calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> multiply the width you want by your stitches per inch, then round to fit your stitch pattern. An 8 in adult scarf in worsted yarn (about 18 stitches per 4 in, so 4.5 per inch) needs about <strong>{_co_sc} stitches</strong>. A 50 in throw blanket in worsted needs about <strong>{_co_th}</strong>. Super bulky yarn at 9 stitches per 4 in needs only about {_co_ch} stitches for a scarf. Swatch first, because your gauge decides the number.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="co-what">What are you making?</label><select id="co-what">{co_opts}</select></div>
<div id="co-custom" hidden><div class="row2"><div class="field"><label for="co-w">Width (or around, for in the round)</label><input type="number" id="co-w" value="8" min="1" max="200" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="co-wu">Unit</label><select id="co-wu"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><label for="co-mode">Knitted</label><select id="co-mode"><option value="flat">Flat, back and forth</option><option value="round">In the round</option></select></div></div>
<div class="field"><label for="co-yarn">Yarn weight</label><select id="co-yarn">{co_wopts}</select></div>
<div class="row2"><div class="field"><label for="co-g">Stitches in your swatch</label><input type="number" id="co-g" value="18" min="2" max="60" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="co-gu">Measured over</label><select id="co-gu"><option value="4">4 in</option><option value="10">10 cm</option></select></div></div>
<div class="field"><label for="co-pat">Stitch pattern</label><select id="co-pat"><option value="1|0|0" selected>Stockinette or garter (any number)</option><option value="2|1|0">1x1 rib (multiple of 2 + 1 flat)</option><option value="4|2|0">2x2 rib (multiple of 4 + 2 flat)</option><option value="2|1|0">Seed or moss stitch (multiple of 2 + 1 flat)</option><option value="custom">My pattern's repeat</option></select></div>
<div class="row2" id="co-rep" hidden><div class="field"><label for="co-m">Multiple of</label><input type="number" id="co-m" value="6" min="1" max="80" step="1" inputmode="numeric"></div>
<div class="field"><label for="co-x">Plus (extra stitches)</label><input type="number" id="co-x" value="0" min="0" max="40" step="1" inputmode="numeric"></div></div>
<div id="co-flat"><div class="field"><label for="co-b">Border on each side</label><select id="co-b"><option value="0" selected>No border</option><option value="0.5">½ in garter or seed border</option><option value="1">1 in border</option><option value="1.5">1½ in border</option><option value="2">2 in border (blankets)</option></select></div>
<div class="field"><label for="co-s">Edge stitches</label><select id="co-s"><option value="0">None</option><option value="1" selected>1 each side (slip it for a neat edge)</option><option value="2">2 each side</option></select></div></div>
<figure class="co-fig"><svg id="co-svg" viewBox="0 0 320 170" role="img" aria-label="Cast-on row divided into border, edge and pattern stitches"></svg><figcaption class="note" id="co-cap">Your cast-on.</figcaption>
<ul class="co-key"><li><i style="background:#2f8f8a"></i>Border</li><li><i style="background:#f4a823"></i>Edge stitch</li><li><i style="background:#b8326a"></i>Pattern repeats</li></ul></figure>
</div>
<div class="result" aria-live="polite" id="co-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How many stitches to cast on for a scarf or blanket?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Project</th>{"".join(f'<th scope="col">{n}<br><span class="muted">{CO_G[k]} sts / 4 in</span></th>' for k, n in CO_EXW)}</tr></thead><tbody>{co_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Our own maths at a typical gauge for each yarn weight (the middle of the Craft Yarn Council's range on the label), stockinette or garter with one edge stitch each side and no border. Your swatch will differ, so use the calculator with your own gauge. Scarf widths follow common guidance of 8 to 10 in for adults and 5 to 7 in for children; blanket widths are the short edge from our <a href="{href("blanket-size-calculator.html")}">blanket size chart</a>; the dishcloth width is a typical size.</p>
</div></section>
{AD.format("co-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How do I work out how many stitches to cast on?</h2>
<ol><li><strong>Knit a swatch</strong> in the yarn, needles and stitch you'll use, at least 4 in (10 cm) wide. Wash and dry it the way you'll treat the finished piece.</li>
<li><strong>Count the stitches</strong> across 4 in and divide by 4 for stitches per inch (or by 10 for stitches per cm).</li>
<li><strong>Multiply by the width</strong> you want. 4.5 stitches per inch × 8 in = 36 stitches.</li>
<li><strong>Take off the border and edge stitches</strong>, round what's left to your pattern's repeat, then add them back.</li></ol>
<p>A few stitches either way rarely matters for a scarf or blanket. It matters more for fitted things like hats and socks, which have their own calculators: <a href="{href("hat-size-chart.html")}">hat size</a> and <a href="{href("sock-size-chart.html")}">sock size</a>.</p>
<h2>What does "multiple of 4 plus 2" mean?</h2>
<p>It's how patterns tell you which numbers work. Cast on any number you can make from 4 × something, then add 2. So 22, 26, 30 and 34 all work for "multiple of 4 + 2", but 24 doesn't. A 12-stitch lace repeat worked 10 times is 120 stitches; add a 10-stitch seed border on each side and you cast on 140. Count the border twice, once for each edge.</p>
<p>Knitting in the round usually needs only the multiple, because the round has no edges to balance. If you mix two stitch patterns (say a rib and a cable), the number has to suit both.</p>
<div class="callout"><strong>Does a garter border change the count?</strong> Garter stitch works on any number, so a garter border just adds its stitches to each side. A rib border needs the count to suit the rib too, for example a multiple of 4 for 2x2 rib in the round.</div>
<h2>How long a tail for a long-tail cast on?</h2>
<p>New to it? Our step-by-step guide to <a href="{href("how-to-cast-on-knitting.html")}">how to cast on knitting</a> shows the long-tail cast on in drawings, with a tail table for every yarn weight. A common rule is about 1 in of tail per stitch for worsted yarn, plus a few inches to weave in. Thinner yarn needs less, thick yarn more, so the calculator scales it by your gauge (our estimate). For a big cast-on, wrap the yarn around the needle 10 times, measure that length, and multiply by the number of stitches ÷ 10. Casting on a blanket? Use two ends of the ball (one from the middle, one from the outside) so you can't run out.</p>
<h2>Which needle should I use for a wide cast-on?</h2>
<p>Straight needles hold a scarf or dishcloth easily. For a wrap or blanket, use a long circular needle (32 to 40 in, or longer for big blankets) and knit back and forth: the weight sits on the cable instead of your wrists. In the round, pick a circular that is shorter than the piece is around, so the stitches reach without stretching. A 16 in circular suits hats, 24 in suits most cowls, and a long infinity scarf can go on a 32 to 47 in cable.</p>
<h2>How many chains for crochet?</h2>
<p>Work out the number of stitches the same way, from your crochet swatch. Then chain that number plus the turning chain your pattern's first row asks for (often 1 extra for single crochet, more for taller stitches). Your pattern says which chain to start in, and that decides the exact number. The <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a> works it out for sc, hdc, dc and treble.</p>
<p>What next? Check your needle size on the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>, see how much yarn it takes with the <a href="{href("yarn-calculator.html")}">yarn calculator</a> or <a href="{href("blanket-size-calculator.html")}">blanket calculator</a>, see the size your swatch will really give with the <a href="{href("gauge-converter.html")}">gauge converter</a>, and space out shaping with the <a href="{href("increase-decrease-calculator.html")}">increase evenly calculator</a>. At the other end, our <a href="{href("how-to-bind-off-knitting.html")}">bind off guide</a> shows which bind off to use and how much yarn to keep for it.</p></div></section>'''
co_faq = [
    ("How many stitches do I cast on for a scarf?", f"For an 8 in adult scarf in worsted yarn at about 4.5 stitches per inch, cast on about {_co_sc} stitches. Use about {co_count(8, 28)} in fingering, {co_count(8, 14)} in bulky and {_co_ch} in super bulky yarn. Children's scarves are 5 to 7 in wide."),
    ("How many stitches do I cast on for a blanket?", f"Multiply the blanket's width by your stitches per inch. A 36 in baby blanket in worsted needs about {co_count(36, 18)} stitches, and a 50 in throw about {_co_th}. Bulky yarn needs about {co_count(50, 14)} for a throw."),
    ("How do I calculate stitches to cast on?", "Knit a swatch, count the stitches in 4 in and divide by 4 to get stitches per inch. Multiply by the width you want, then round to your stitch pattern's repeat and add any border and edge stitches."),
    ("What does multiple of 4 plus 2 mean in knitting?", "Cast on a number that is 4 times something, plus 2: for example 22, 26, 30 or 34. It makes the stitch pattern line up at both edges."),
    ("How much tail do I need for a long-tail cast on?", "About 1 in per stitch in worsted yarn, plus a few inches, less for thin yarn and more for thick yarn. For a large cast-on, wrap the yarn 10 times around the needle, measure it, and scale up."),
    ("How many stitches for an infinity scarf?", f"Multiply the distance around (usually 50 to 60 in) by your stitches per inch. At 4.5 stitches per inch, 55 in around is about {co_count(55, 18, 1, 0, 0, 0)} stitches, worked on a circular needle a little shorter than the scarf."),
]
page("cast-on-calculator.html", "Cast On Calculator: How Many Stitches to Cast On? | Purl & Paper",
     "How many stitches to cast on for a scarf, blanket, dishcloth or cowl: free knitting cast-on calculator for your gauge, stitch pattern multiple, borders and long-tail length.",
     co, co_faq, "Cast on calculator", app_name="Knitting cast on calculator")

# ---------------- CROCHET CIRCLE + AMIGURUMI BALL CALCULATOR ----------------
CI_G = {1: 26, 2: 18, 3: 14, 4: 12, 5: 9, 6: 8, 7: 6}   # single crochet per 4 in: middle of each Craft Yarn Council crochet range
CI_AMI = 1.25   # amigurumi is worked on a smaller hook, so about a quarter more stitches per inch. Our estimate.
CI_ST = {"sc": ("single crochet", 6), "hdc": ("half double crochet", 8), "dc": ("double crochet", 12)}
def ci_rep(m, st, inc, s):
    if m <= 0: return f"{inc} × {s}"
    return f"({m} {st}, {inc}) × {s}"
def ci_stag(m, st, inc, s):
    a, b = m - m // 2, m // 2
    return f"{a} {st}, {inc}, ({m} {st}, {inc}) × {s - 1}" + (f", {b} {st}" if b else "")
def ci_round(r, st, s):
    if r == 1: return f"{s} {st} in a magic ring", s
    if r == 2: return f"inc × {s} (2 {st} in every stitch)", 2 * s
    m = r - 2
    return (ci_stag(m, st, "inc", s) if r % 2 == 0 else ci_rep(m, st, "inc", s)), s * r
def ci_ball(n):
    out = [("Increase", r) + ci_round(r, "sc", 6) for r in range(1, n + 1)]
    r = n
    for _ in range(n):
        r += 1; out.append(("Even", r, f"sc in each stitch", 6 * n))
    for k in range(n - 1, 0, -1):
        r += 1; m = k - 1
        out.append(("Decrease", r, ci_stag(m, "sc", "dec", 6) if (m and k % 2 == 0) else ci_rep(m, "sc", "dec", 6), 6 * k))
    return out
def ci_d(n, g4): return n / (3.14159 * g4 / 4)
ci_wopts = "".join(f'<option value="{w["n"]}|{CI_G[w["n"]]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])})</option>' for w in D["weights"] if w["n"] in CI_G)
ci_rows = "".join(f'<tr><td><strong>{r}</strong></td>' + "".join(f'<td>{ci_round(r, k, s)[1]}<br><span class="muted">{ci_d(ci_round(r, k, s)[1], 12):.1f} in</span></td>' for k, (_, s) in CI_ST.items()) + f'<td>{e(ci_round(r, "sc", 6)[0])}</td></tr>' for r in range(1, 13))
CI_BW = [(3, "DK"), (4, "Worsted"), (6, "Super bulky")]
ci_brows = "".join(f'<tr><td><strong>{n}</strong></td><td>{6 * n}</td><td>{3 * n - 1}</td>' + "".join(f'<td>{ci_d(6 * n, CI_G[k] * CI_AMI):.1f} in ({ci_d(6 * n, CI_G[k] * CI_AMI) * 2.54:.0f} cm)</td>' for k, _ in CI_BW) + "</tr>" for n in range(3, 11))
_ci10 = ci_d(60, 12); _ci_b5 = ci_d(30, 12 * CI_AMI)
ci = top("Crochet circle calculator and amigurumi ball pattern", "How many stitches in each round of a flat circle in single, half double or double crochet, how many rounds for the size you want, and a full ball pattern for amigurumi, written out round by round.", "Crochet circle calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> a flat circle starts with a set number of stitches and adds that same number every round. Single crochet: <strong>6, then +6</strong> (6, 12, 18, 24…). Half double: <strong>8, then +8</strong>. Double: usually <strong>12, then +12</strong> (some patterns use 10). Round 2 increases in every stitch, then each round puts one more plain stitch between increases. In worsted yarn, 10 rounds of single crochet makes a circle about {_ci10:.0f} in across (our estimate).</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><span class="label" id="ci-shape-l">What are you making?</span><div class="seg" role="group" aria-labelledby="ci-shape-l" id="ci-shape"><button type="button" data-v="flat" aria-pressed="true">Flat circle</button><button type="button" data-v="ball" aria-pressed="false">Amigurumi ball</button></div></div>
<div id="ci-flat"><div class="field"><label for="ci-st">Stitch</label><select id="ci-st"><option value="sc|6" selected>Single crochet (sc), 6 to start</option><option value="hdc|8">Half double crochet (hdc), 8 to start</option><option value="dc|12">Double crochet (dc), 12 to start</option><option value="dc|10">Double crochet (dc), 10 to start</option></select></div></div>
<div class="field"><span class="label" id="ci-goal-l">Work out</span><div class="seg" role="group" aria-labelledby="ci-goal-l" id="ci-goal"><button type="button" data-v="size" aria-pressed="true">Rounds for my size</button><button type="button" data-v="rounds" aria-pressed="false">Size of my rounds</button></div></div>
<div class="row2" id="ci-size-f"><div class="field"><label for="ci-d">Size across</label><input type="number" id="ci-d" value="8" min="0.5" max="80" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="ci-du">Unit</label><select id="ci-du"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field" id="ci-n-f" hidden><label for="ci-n" id="ci-n-l">Rounds</label><input type="number" id="ci-n" value="10" min="1" max="60" step="1" inputmode="numeric"></div>
<div class="field"><label for="ci-yarn">Yarn weight</label><select id="ci-yarn">{ci_wopts}</select></div>
<div class="row2"><div class="field"><label for="ci-g">Single crochet in your swatch</label><input type="number" id="ci-g" value="12" min="2" max="60" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="ci-gu">Measured over</label><select id="ci-gu"><option value="4">4 in</option><option value="10">10 cm</option></select></div></div>
<p class="note" id="ci-gnote">Count the stitches across 4 in of single crochet. For half double or double, count across your swatch the same way: the width of each stitch is what sets the size.</p>
<figure class="co-fig"><svg id="ci-svg" viewBox="0 0 320 260" role="img" aria-label="Drawing of the circle or ball, round by round"></svg><figcaption class="note" id="ci-cap">Your circle.</figcaption>
<ul class="co-key" id="ci-key"></ul></figure>
</div>
<div class="result" aria-live="polite" id="ci-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>Crochet circle increase chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Round</th><th scope="col">Single crochet<br><span class="muted">6 + 6</span></th><th scope="col">Half double<br><span class="muted">8 + 8</span></th><th scope="col">Double<br><span class="muted">12 + 12</span></th><th scope="col">Single crochet round, written out</th></tr></thead><tbody>{ci_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Stitch counts follow the usual starting numbers (6 sc, 8 hdc, 12 dc). Sizes under each count are our estimate for worsted yarn at 12 stitches per 4 in, worked out from the distance around (stitches ÷ stitches per inch ÷ 3.14). Taller stitches make a bigger circle in fewer rounds. inc = 2 stitches in the same stitch. Even rounds start part-way into a repeat so the increases don't stack into a hexagon.</p>
</div></section>
{AD.format("ci-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How do you crochet a flat circle?</h2>
<ol><li><strong>Start with a magic ring</strong> (or chain 4 and join). Work 6 sc, 8 hdc or 12 dc into it and pull the ring tight.</li>
<li><strong>Round 2:</strong> work 2 stitches into every stitch. You now have double the starting number.</li>
<li><strong>Round 3:</strong> 1 stitch, then 2 in the next stitch, all the way round.</li>
<li><strong>Each round after:</strong> add one more plain stitch between the increases. Round 4 has 2 plain stitches between, round 5 has 3, and so on. You add the starting number of stitches every round.</li>
<li><strong>Mark the first stitch</strong> of each round with a stitch marker, and count at the end of every round.</li></ol>
<p>Work in a spiral for amigurumi and small pieces, or join each round with a slip stitch and chain up for coasters, rugs and mandalas. Check whether your pattern's turning chain counts as a stitch: for double crochet many patterns say chain 3 counts as the first dc, others chain 2 or 1 and don't count it.</p>
<h2>Why is my crochet circle wavy or cupping?</h2>
<p><strong>Ruffles or waves</strong> mean too many stitches: you've added extra increases, or your tension is loose for the hook. <strong>Cupping or curling up</strong> means too few: an increase got missed, or you crochet tightly. Count the last round. If the number is right, try a hook one size up (for cupping) or down (for ruffles). If it's wrong, pull back to the last correct round and redo it.</p>
<div class="callout"><strong>Why does my circle look like a hexagon?</strong> If every increase lands on top of the one below, they line up into six corners. Start every other round part-way through a repeat (the calculator and chart do this for you), or put each increase in the second stitch of the last round's increase.</div>
<h2>How do I crochet an amigurumi ball?</h2>
<p>A ball is a flat circle, then straight sides, then the circle again in reverse. Work single crochet in a spiral:</p>
<ol><li><strong>Increase</strong> for as many rounds as you want the ball's size (5 rounds gives 30 stitches).</li>
<li><strong>Work even</strong>, one sc in each stitch, for about the same number of rounds. Some designers add one more for a rounder look.</li>
<li><strong>Decrease</strong> the same way you increased, 6 stitches per round, until 6 are left.</li>
<li><strong>Stuff</strong> when the hole is still big enough (around 18 stitches), and top it up just before the last round.</li>
<li>Fasten off, weave the tail through the front loops of the last 6 stitches, and pull it closed.</li></ol>
<p>Use a hook a few sizes smaller than the yarn label asks for, so the stitches are tight and the stuffing doesn't show. An invisible decrease (through the front loops only) gives a smoother ball.</p>
<h2>Amigurumi ball sizes</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Increase rounds</th><th scope="col">Most stitches</th><th scope="col">Total rounds</th>{"".join(f'<th scope="col">{n}</th>' for _, n in CI_BW)}</tr></thead><tbody>{ci_brows}</tbody></table></div>
<p class="note">Our estimate, at a tight amigurumi tension (about a quarter more stitches per inch than the yarn's usual single crochet gauge, from working on a smaller hook). Your own hook and hands change it, so crochet the first few rounds and measure. A 5-round ball in worsted comes out about {_ci_b5:.1f} in across.</p>
<p>New to starting in the round? Our step-by-step <a href="{href("how-to-crochet-magic-ring.html")}">magic ring guide</a> shows how to start without a hole, and <a href="{href("how-to-change-colors-in-crochet.html")}">how to change colours in crochet</a> covers striped circles.</p>
<p>What next? Closing an amigurumi ball? Our guide to <a href="{href("how-to-crochet-decrease.html")}">decreasing in crochet</a> shows the invisible decrease and writes the closing rounds. Shaping something that isn't round? The <a href="{href("increase-decrease-calculator.html")}">increase evenly calculator</a> spaces increases across any row. Making a crochet hat? The <a href="{href("hat-size-chart.html")}">hat size calculator</a> gives the crown circle size for any head. Reading a UK pattern? Check the <a href="{href("crochet-terms.html")}">US and UK crochet terms</a>, and keep count of your rounds with the <a href="{href("row-counter.html")}">row counter</a>. Selling your toys? See <a href="{href("how-to-price-amigurumi.html")}">how to price amigurumi</a>.</p></div></section>'''
ci_faq = [
    ("How many stitches do you increase in a crochet circle?", "Add the same number you started with, every round: 6 for single crochet, 8 for half double crochet and usually 12 for double crochet (10 in some patterns)."),
    ("How many single crochet stitches in a magic ring?", "Six is the usual number for a flat circle or amigurumi. Round 2 then has 12, round 3 has 18 and round 4 has 24."),
    ("How many rounds for a 6 inch crochet circle?", f"In worsted yarn at 12 single crochet per 4 in, about {round(6 * 3.14159 * 3 / 6)} rounds of single crochet, or about {round(6 * 3.14159 * 3 / 12)} rounds of double crochet. Your gauge decides it, so measure as you go."),
    ("Why is my crochet circle not flat?", "If it ruffles, there are too many stitches; if it cups, there are too few or you crochet tightly. Count the last round, and try a different hook size if the count is right."),
    ("How do I stop my crochet circle looking like a hexagon?", "Move the increases each round. Start every other round part-way into a repeat, so the increases don't sit on top of each other."),
    ("How many rounds to work even on an amigurumi ball?", "About as many as you increased. Five increase rounds, five even rounds and then decrease back down to 6 stitches makes a round ball."),
]
page("crochet-circle-calculator.html", "Crochet Circle Calculator: Increase Chart and Amigurumi Ball | Purl & Paper",
     "Free crochet circle calculator: stitches per round for sc, hdc and dc, how many rounds for your size, a flat circle increase chart and an amigurumi ball pattern written out round by round.",
     ci, ci_faq, "Crochet circle calculator", app_name="Crochet circle calculator")

# ---------------- KNITTING ABBREVIATIONS ----------------
# (shown, decoder keys, short meaning used in the translation, longer how-to, group, UK note)
KA = [
 ("k", ["k"], "knit", "Knit the stitch. A number after it means knit that many: k3 = knit 3.", "Basic stitches", ""),
 ("p", ["p"], "purl", "Purl the stitch. p2 = purl 2.", "Basic stitches", ""),
 ("st(s)", ["st", "sts"], "stitch(es)", "One loop on the needle is one stitch.", "Basic stitches", ""),
 ("St st", ["st st"], "stockinette stitch", "Knit the right-side rows and purl the wrong-side rows. In the round, knit every round.", "Basic stitches", "UK: stocking stitch"),
 ("rev St st", ["rev st st"], "reverse stockinette stitch", "Stockinette with the bumpy purl side used as the right side.", "Basic stitches", "UK: reverse stocking stitch"),
 ("g st", ["g st"], "garter stitch", "Knit every row when working flat. In the round, knit one round and purl the next.", "Basic stitches", ""),
 ("rib", ["rib"], "rib", "Columns of knits and purls, such as k1, p1 or k2, p2. Knit the knits and purl the purls as they face you.", "Basic stitches", ""),
 ("seed st", ["seed st"], "seed stitch", "k1, p1 that shifts every row, so you knit the purls and purl the knits.", "Basic stitches", "UK: moss stitch"),
 ("tbl", ["tbl"], "through the back loop", "Work into the back leg of the stitch, which twists it. k1 tbl = knit 1 through the back loop.", "Basic stitches", ""),
 ("tfl", ["tfl"], "through the front loop", "Work into the front leg of the stitch, the usual way.", "Basic stitches", ""),
 ("k1b", ["k1b", "kb"], "knit into the stitch below", "Knit into the stitch in the row below the next one on the needle.", "Basic stitches", ""),
 ("kwise / pwise", ["kwise", "pwise"], "knitwise / purlwise", "Put the needle in as if to knit (or purl). Usually used with slipping.", "Basic stitches", ""),
 ("CO", ["co"], "cast on", "Put the first stitches on the needle.", "Basic stitches", ""),
 ("BO", ["bo"], "bind off", "Take the stitches off so they don't unravel.", "Basic stitches", "UK: cast off"),
 ("pu", ["pu", "puk"], "pick up (and knit)", "Pull new stitches up through the edge of the piece, for a collar, border or gusset.", "Basic stitches", ""),
 ("w&t", ["w&t"], "wrap and turn", "For short rows: slip the next stitch, move the yarn to the other side, slip the stitch back and turn the work.", "Basic stitches", ""),
 ("MB", ["mb"], "make bobble", "Work several stitches into one stitch, then join them into a bump. The pattern says exactly how.", "Basic stitches", ""),
 ("inc", ["inc", "incs"], "increase", "Make one or more extra stitches. The pattern or its notes say which method.", "Increases", ""),
 ("kfb", ["kfb", "kf&b"], "knit into the front and back", "Knit the stitch but leave it on the needle, then knit into its back loop too. Turns 1 stitch into 2.", "Increases", ""),
 ("pfb", ["pfb"], "purl into the front and back", "The purl version of kfb. Turns 1 stitch into 2.", "Increases", ""),
 ("M1 / M1L", ["m1", "m1l", "m1k"], "make one (left-leaning)", "Lift the bar between two stitches from front to back with the left needle and knit it through the back loop.", "Increases", ""),
 ("M1R", ["m1r"], "make one right", "Lift the bar between two stitches from back to front and knit it through the front loop. Leans right.", "Increases", ""),
 ("M1p", ["m1p", "m1lp", "m1rp", "m1pl", "m1pr"], "make one purlwise", "Lift the bar between two stitches and purl it. L and R versions lean left or right.", "Increases", ""),
 ("kll / krl", ["kll", "krl", "lli", "rli"], "lifted increase (left / right)", "Knit into the stitch below the one on the needle (or two below for the left one) to add a stitch.", "Increases", ""),
 ("yo", ["yo"], "yarn over", "Wrap the yarn over the right needle to make a new stitch with a small hole under it. Used for lace and eyelets.", "Increases", "UK: yf, yfwd, yon or yrn"),
 ("yo2", ["yo2"], "yarn over twice", "Wrap the yarn round the needle twice. The pattern says how to work the extra loop next row.", "Increases", ""),
 ("dec", ["dec", "decs"], "decrease", "Lose one or more stitches. The pattern or its notes say which method.", "Decreases", ""),
 ("k2tog", ["k2tog"], "knit 2 together", "Knit two stitches as if they were one. Leans right. Loses 1 stitch.", "Decreases", ""),
 ("p2tog", ["p2tog"], "purl 2 together", "Purl two stitches as one. Loses 1 stitch.", "Decreases", ""),
 ("k3tog", ["k3tog"], "knit 3 together", "Knit three stitches as one. Leans right. Loses 2 stitches.", "Decreases", ""),
 ("ssk", ["ssk"], "slip, slip, knit", "Slip two stitches knitwise one at a time, put the left needle into their fronts and knit them together through the back loops. Leans left. Loses 1 stitch.", "Decreases", ""),
 ("ssp", ["ssp"], "slip, slip, purl", "Slip two stitches knitwise one at a time, put them back and purl them together through the back loops. Loses 1 stitch.", "Decreases", ""),
 ("sssk", ["sssk"], "slip, slip, slip, knit", "Like ssk but with three stitches. Leans left. Loses 2 stitches.", "Decreases", ""),
 ("skp", ["skp", "skpo"], "slip 1, knit 1, pass the slipped stitch over", "Slip 1 knitwise, knit 1, then lift the slipped stitch over the knitted one. Leans left. Loses 1 stitch.", "Decreases", "UK patterns often write skpo"),
 ("sk2p", ["sk2p", "sk2po"], "slip 1, knit 2 together, pass the slipped stitch over", "A left-leaning double decrease. Loses 2 stitches.", "Decreases", ""),
 ("s2kp / cdd", ["s2kp", "s2kp2", "cdd"], "centred double decrease", "Slip 2 together knitwise, knit 1, pass both slipped stitches over. The middle stitch stays on top. Loses 2 stitches.", "Decreases", ""),
 ("psso", ["psso"], "pass the slipped stitch over", "Lift a stitch you slipped earlier over the one you just worked and off the needle.", "Decreases", ""),
 ("p2sso", ["p2sso"], "pass 2 slipped stitches over", "Lift the two slipped stitches over the one you just worked.", "Decreases", ""),
 ("pnso", ["pnso"], "pass the next stitch over", "Lift the next stitch over and off the needle.", "Decreases", ""),
 ("tog", ["tog"], "together", "Work the stitches as one, as in k2tog.", "Decreases", ""),
 ("sl", ["sl"], "slip", "Move a stitch to the right needle without working it. Most patterns mean purlwise unless they say otherwise or it's part of a decrease.", "Slipping and yarn", ""),
 ("sl1k / sl1p", ["sl1k", "sl1p", "sl1", "sl2", "sl1-k1-psso"], "slip 1 knitwise / purlwise", "Slip one stitch, putting the needle in as if to knit (k) or purl (p).", "Slipping and yarn", ""),
 ("sl st", ["sl st"], "slip stitch", "A stitch moved without being worked.", "Slipping and yarn", "Canada: ss"),
 ("wyib / wyif", ["wyib", "wyif"], "with yarn in back / in front", "Keep the yarn behind (or in front of) the work while you slip.", "Slipping and yarn", ""),
 ("yb / yf", ["yb", "yf", "yfwd", "ybk"], "yarn to the back / yarn forward", "Move the yarn between the needles to the back or the front. In UK lace, yfwd between two knit stitches makes a yarn over.", "Slipping and yarn", ""),
 ("yon / yrn", ["yon", "yrn", "yfon", "yfrn"], "yarn over (UK style)", "UK names for a yarn over, depending on whether the stitches either side are knits or purls.", "Slipping and yarn", "US: yo"),
 ("cn", ["cn"], "cable needle", "A short needle that holds stitches out of the way while you cross a cable.", "Cables and twists", ""),
 ("C4F / C4B", ["c4f", "c4b"], "cable 4 front / back", "Slip 2 stitches to a cable needle and hold it in front (or back), knit 2, then knit the 2 from the cable needle. Front leans left, back leans right. C6F, C8B and so on work the same way with more stitches.", "Cables and twists", ""),
 ("LC / RC", ["lc", "rc"], "left cross / right cross", "A cable crossing to the left (cable needle held in front) or to the right (held in back). Numbers like 2/2 LC give how many stitches cross.", "Cables and twists", ""),
 ("LT / RT", ["lt", "rt"], "left twist / right twist", "A tiny two-stitch cross, often worked without a cable needle.", "Cables and twists", "Some UK patterns: FT / BT"),
 ("FC / BC", ["fc", "bc"], "front cross / back cross", "Older names for a cable held in front or behind.", "Cables and twists", ""),
 ("pm", ["pm"], "place marker", "Put a stitch marker on the needle here.", "Markers and colours", ""),
 ("sm", ["sm"], "slip marker", "Move the marker from the left needle to the right.", "Markers and colours", ""),
 ("rm", ["rm"], "remove marker", "Take the marker off.", "Markers and colours", ""),
 ("m", ["m"], "marker (or metres)", "A stitch marker. In measurements, m means metres.", "Markers and colours", ""),
 ("BOR", ["bor"], "beginning of round", "Where each round starts, usually shown with a different marker.", "Markers and colours", ""),
 ("MC / CC", ["mc", "cc"], "main colour / contrast colour", "The main yarn, and the second colour used for stripes or colourwork.", "Markers and colours", ""),
 ("CA / CB", ["ca", "cb"], "colour A / colour B", "Names for the yarns in a pattern with several colours.", "Markers and colours", ""),
 ("RS / WS", ["rs", "ws"], "right side / wrong side", "The side that shows when it's finished, and the side that faces inwards.", "Pattern words", ""),
 ("rnd(s)", ["rnd", "rnds"], "round(s)", "One trip round the work when knitting in the round.", "Pattern words", ""),
 ("rep", ["rep", "reps"], "repeat", "Work the instructions again.", "Pattern words", ""),
 ("rem", ["rem"], "remaining", "The stitches left, often given after a decrease row: 64 sts rem.", "Pattern words", ""),
 ("beg", ["beg"], "beginning", "The start of a row, round or pattern.", "Pattern words", ""),
 ("cont", ["cont"], "continue", "Keep working as you have been.", "Pattern words", ""),
 ("alt", ["alt"], "alternate", "Every other one: on alt rows means every second row.", "Pattern words", ""),
 ("foll", ["foll"], "following", "The next one, as in the foll 4 rows.", "Pattern words", ""),
 ("patt / pat", ["patt", "pat"], "pattern", "The stitch pattern, or the pattern as written.", "Pattern words", ""),
 ("prev", ["prev"], "previous", "The one before.", "Pattern words", ""),
 ("bet", ["bet"], "between", "", "Pattern words", ""),
 ("approx", ["approx"], "approximately", "", "Pattern words", ""),
 ("incl", ["incl"], "including", "", "Pattern words", ""),
 ("LH / RH", ["lh", "rh"], "left-hand / right-hand", "Usually the left or right needle.", "Pattern words", ""),
 ("lp(s)", ["lp", "lps"], "loop(s)", "", "Pattern words", ""),
 ("dpn(s)", ["dpn", "dpns"], "double-pointed needle(s)", "Short needles with a point at each end, used for small rounds like socks and hat crowns.", "Pattern words", ""),
 ("EOR", ["eor"], "every other row (or end of row)", "Check the pattern's notes: some use it for every other row, some for end of row.", "Pattern words", ""),
 ("work even", ["work even"], "work without shaping", "Carry on in pattern with no increases or decreases.", "Pattern words", "UK: work straight"),
 ("*", ["*"], "repeat from *", "Repeat the instructions after the asterisk as many times as the pattern says, or to the end.", "Symbols and sizes", ""),
 ("[ ] or ( )", ["[ ]"], "repeat the part in brackets", "Work everything inside the brackets the number of times written after them: [k2, p2] 3 times.", "Symbols and sizes", ""),
 ("\" / in", ["in"], "inches", "1 in = 2.54 cm.", "Symbols and sizes", ""),
 ("cm / mm", ["cm", "mm"], "centimetres / millimetres", "Needle sizes are given in mm everywhere.", "Symbols and sizes", ""),
 ("g / oz", ["g", "oz"], "grams / ounces", "Yarn weight on the ball band. 1 oz is about 28 g.", "Symbols and sizes", ""),
 ("yd / m", ["yd", "yds"], "yards / metres", "Yarn length. 1 yd = 0.914 m.", "Symbols and sizes", ""),
]
KA_GROUPS = ["Basic stitches", "Increases", "Decreases", "Slipping and yarn", "Cables and twists", "Markers and colours", "Pattern words", "Symbols and sizes"]
KA_UK = [("bind off", "cast off"), ("gauge", "tension"), ("stockinette stitch", "stocking stitch"), ("seed stitch", "moss stitch"), ("moss stitch (seed stitch stacked in pairs of rows)", "double moss stitch"),
         ("yarn over (yo)", "yarn forward (yfwd / yf), yarn over needle (yon) or yarn round needle (yrn)"), ("skp", "skpo"), ("work even", "work straight"), ("color", "colour"), ("worsted yarn", "aran (close, not identical)")]
ka_rows = "".join(f'<tr data-g="{e(g)}" data-s="{e((a + " " + s + " " + l + " " + uk).lower())}"><td><strong>{e(a)}</strong></td><td>{e(s)}{f"<br><span class=\"muted\">{e(l)}</span>" if l else ""}</td><td class="muted">{e(uk)}</td></tr>' for a, _, s, l, g, uk in KA)
ka_js = json.dumps([[k, s, a, l] for a, keys, s, l, g, uk in KA for k in keys], ensure_ascii=False)
KA_EX = [("Lace row", "K2, M1, *k2tog, yo; rep from * to last 2 sts, k2.", "Knit 2, make one, then knit 2 together and yarn over again and again until 2 stitches are left, then knit 2."),
         ("Edge stitches", "Sl1 wyif, k1, p2, k2, ssk, pm, k to end.", "Slip 1 with the yarn in front, knit 1, purl 2, knit 2, slip-slip-knit, place a marker, knit to the end of the row."),
         ("Cable round", "Rnd 1: *C4F, p2; rep from * to BOR.", "Round 1: cross 4 stitches to the left (2 on a cable needle held in front), purl 2, and repeat to the beginning-of-round marker."),
         ("Decrease round", "Dec rnd: k1, k2tog, k to last 3 sts, ssk, k1. 2 sts dec'd.", "Knit 1, knit 2 together (leans right), knit to the last 3 stitches, slip-slip-knit (leans left), knit 1. You lose 2 stitches.")]
ka = top("Knitting abbreviations", "Every common knitting abbreviation in plain English, with how to work it, the UK names, and a pattern decoder that translates a whole line for you.", "Knitting abbreviations") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> the ones you'll see most are <strong>k</strong> (knit), <strong>p</strong> (purl), <strong>st</strong> (stitch), <strong>k2tog</strong> (knit 2 together, a right-leaning decrease), <strong>ssk</strong> (slip, slip, knit, a left-leaning decrease), <strong>M1</strong> (make one, an increase), <strong>yo</strong> (yarn over, which makes a stitch and a hole), <strong>sl</strong> (slip), <strong>pm</strong> (place marker), <strong>rep</strong> (repeat) and <strong>RS / WS</strong> (right side / wrong side). A number after k or p tells you how many: k3 means knit 3.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Pattern decoder</h2>
<div class="field"><label for="ka-in">Paste a line from your pattern</label><textarea id="ka-in" spellcheck="false">K2, M1, *k2tog, yo; rep from * to last 2 sts, k2.</textarea></div>
<div class="field"><label>Try an example</label><div class="ka-ex">{"".join(f'<button type="button" class="lock" data-ex="{e(x)}">{e(n)}</button>' for n, x, _ in KA_EX)}</div></div>
<p class="note" style="margin:0">It works on your device and knows the {len(KA)} abbreviations below, plus numbers like k12, p3 and cables like C6B. Anything it doesn't know is left as it is.</p>
</div>
<div class="result" id="ka-out" aria-live="polite"><h3>In plain English</h3><p class="ka-line" id="ka-plain"></p><hr><h3>Abbreviations in this line</h3><ul class="ka-found" id="ka-found"></ul></div>
</div></section>
{AD.format("ka-mid")}
<section style="padding-top:0" id="list"><div class="narrow prose"><h2>Knitting abbreviations list</h2>
<p>Search or pick a group. Each one has what it stands for and, where it helps, how to work it. Your pattern's own notes always win, because a few designers use their own short forms.</p></div>
<div class="narrow"><div class="finder"><div class="field"><label for="ka-q">Search abbreviations</label><input type="search" id="ka-q" placeholder="e.g. ssk, yo, cable, decrease"></div></div>
<div class="filters" id="ka-g" role="group" aria-label="Group"><button type="button" class="lock" data-g="" aria-pressed="true">All</button>{"".join(f'<button type="button" class="lock" data-g="{e(g)}" aria-pressed="false">{e(g)}</button>' for g in KA_GROUPS)}</div>
<div class="tbl-wrap"><table class="ka-tbl"><thead><tr><th scope="col">Abbreviation</th><th scope="col">Means</th><th scope="col">UK or other name</th></tr></thead><tbody id="ka-body">{ka_rows}</tbody></table></div>
<p class="note" id="ka-none" hidden>Nothing matches. Try fewer letters, or check the pattern's own abbreviation list.</p></div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>What's the difference between k2tog and ssk?</h2>
<p>Both turn two stitches into one. <strong>k2tog</strong> leans to the right and <strong>ssk</strong> leans to the left. Patterns pair them so shaping looks tidy on both edges, such as the sides of a hat crown, a raglan line or a sock toe: ssk at the start of the shaping and k2tog at the end, or the other way round, as the pattern says. If you swap them nothing goes wrong with the count, the line just leans the other way.</p>
<h2>What does * mean in a knitting pattern?</h2>
<p>An asterisk marks the start of a repeat. "*k2, p2; rep from * to end" means knit 2, purl 2, and keep doing that until the row ends. Two asterisks (**) mark a second, longer repeat, and square brackets or round brackets mean "work this group the number of times written after it": [k1, p1] 4 times.</p>
<h2>UK and US knitting terms</h2>
<p>Most knitting abbreviations are the same in both, unlike crochet, where the stitch names really change (see our <a href="@@CT@@">US vs UK crochet terms</a>). A few words do differ:</p></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">US pattern</th><th scope="col">UK pattern</th></tr></thead><tbody>{"".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in KA_UK)}</tbody></table></div></div>
<div class="narrow prose"><p>Needle sizes can also be written differently: US numbers, metric mm and old UK numbers. The <a href="@@HN@@">hook and needle size chart</a> converts them, and the <a href="@@YW@@">yarn weight chart</a> gives the UK names for each yarn.</p>
<h2>Four pattern lines, translated</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">The pattern says</th><th scope="col">In plain English</th></tr></thead><tbody>{"".join(f"<tr><td><code>{e(x)}</code></td><td>{e(y)}</td></tr>" for _, x, y in KA_EX)}</tbody></table></div>
<h2>How do I read a knitting pattern for the first time?</h2>
<ol><li><strong>Read the notes at the top first.</strong> They list the abbreviations, special stitches and whether the piece is worked flat or in the round.</li>
<li><strong>Check the gauge</strong> and knit a swatch. Our <a href="@@GC@@">gauge converter</a> shows what happens if yours is different.</li>
<li><strong>Read one row at a time</strong> and say it out loud in plain words, or paste it into the decoder above.</li>
<li><strong>Check the stitch count</strong> at the end of each shaping row. Most patterns give it in brackets or after a dash.</li>
<li><strong>Keep your place.</strong> The <a href="@@RC@@">row counter</a> keeps count and repeat numbers for you.</li>
<li><strong>Dropped one?</strong> Don't panic or rip back yet: our guide to <a href="@@DS@@">fixing a dropped stitch</a> shows how to ladder it back up with a crochet hook.</li></ol>
<p>Shaping a row yourself? The <a href="@@ID@@">increase and decrease evenly calculator</a> writes the row out in these same abbreviations, and the <a href="@@CO@@">cast on calculator</a> tells you how many stitches to start with. Pattern says "BO" or "cast off"? Our <a href="@@BO@@">bind off guide</a> shows how, and which stretchy bind off to use. "PU" or "pick up and knit"? See <a href="@@PU@@">how to pick up stitches</a>, with a calculator for how many.</p>
<p class="note">Abbreviations follow the Craft Yarn Council's knitting abbreviations list and LoveCrafts' guide; UK names from Little Red Window's UK vs US terms guide. Explanations are in our own words.</p></div></section>'''
for k_, f_ in (("@@PU@@", "how-to-pick-up-stitches-knitting.html"), ("@@DS@@", "how-to-fix-a-dropped-stitch.html"), ("@@BO@@", "how-to-bind-off-knitting.html"), ("@@CT@@", "crochet-terms.html"), ("@@HN@@", "hook-needle-sizes.html"), ("@@YW@@", "yarn-weights.html"), ("@@GC@@", "gauge-converter.html"), ("@@RC@@", "row-counter.html"), ("@@ID@@", "increase-decrease-calculator.html"), ("@@CO@@", "cast-on-calculator.html")):
    ka = ka.replace(k_, href(f_))
ka_faq = [
    ("What does k2tog mean in knitting?", "Knit 2 together: put the needle into the next two stitches as if to knit and knit them as one. It's a decrease that leans to the right and loses one stitch."),
    ("What does ssk mean in knitting?", "Slip, slip, knit: slip two stitches knitwise one at a time, then knit them together through the back loops. It's a decrease that leans to the left."),
    ("What does M1 mean in knitting?", "Make one: an increase made by lifting the bar of yarn between two stitches onto the left needle and knitting it through the back loop, so it doesn't leave a hole. M1L leans left and M1R leans right."),
    ("What does yo mean in knitting?", "Yarn over: wrap the yarn over the right needle before the next stitch. It adds a stitch and leaves a small hole, which is how lace and eyelets are made. UK patterns may call it yfwd, yon or yrn."),
    ("What does pm and sm mean in knitting?", "pm means place a stitch marker on your needle, and sm means slip the marker from the left needle to the right when you reach it."),
    ("Are knitting abbreviations different in the UK?", "Mostly no. The big differences are words: cast off instead of bind off, tension instead of gauge, stocking stitch instead of stockinette, moss stitch instead of seed stitch, and yfwd, yon or yrn for a yarn over."),
    ("What does RS and WS mean in knitting?", "RS is the right side, the side that shows on the finished piece. WS is the wrong side, which faces inwards."),
]
page("knitting-abbreviations.html", "Knitting Abbreviations: Full List, UK Terms and a Pattern Decoder | Purl & Paper",
     "Every common knitting abbreviation in plain English (k2tog, ssk, M1, yo, psso, pm and more), how to work each one, UK vs US terms, and a free decoder that translates a pattern line for you.",
     ka, ka_faq, "Knitting abbreviations", scripts=f"<script>window.KA={ka_js};</script>", app_name="Knitting pattern decoder")

# ---------------- JUNK JOURNAL EPHEMERA IDEAS ----------------
EP = [
 ("Around the house", "house", [
   ("Envelopes", "The patterned security linings make great backgrounds; the envelope itself becomes a pocket."),
   ("Old book or dictionary pages", "Use as backgrounds or cut out single words for titles."),
   ("Brown paper bags", "Fold in half for a page with a pocket at the open end."),
   ("Sheet music", "Tear strips for borders or use a whole page behind a photo."),
   ("Old maps", "Perfect behind travel memories; fold big ones as a fold-out page."),
   ("Gift wrap scraps", "Cut into strips, frames or a cover wrap."),
   ("Wallpaper scraps or samples", "Thick and patterned, good for covers and pockets."),
   ("Greeting and Christmas cards", "Cut out the picture panel; keep the message inside a pocket."),
   ("Postcards", "Glue in as a flip-up page so you can read the back."),
   ("Photos and photo-booth strips", "Use copies of photos you want to keep safe."),
   ("Old calendars", "The pictures make backgrounds and the date grids make tags."),
   ("Notebook or graph paper", "Tear out pages for journaling spots."),
   ("Cereal box card", "Covers, tags and stiff pockets."),
   ("Tissue paper from parcels", "Glue thinly for a soft layered background."),
 ]),
 ("Kitchen and food", "kitchen", [
   ("Tea bag tags and wrappers", "Small, printed and perfect for tucking under a photo corner."),
   ("Used tea bags, dried and emptied", "Flatten the paper for a stained, see-through layer."),
   ("Fruit and food stickers", "Little pops of colour and type. Peel and stick."),
   ("Food labels and packaging", "Look for nice lettering on jars, tins and flour bags."),
   ("Chocolate and sweet wrappers", "Smooth flat and glue down; foil adds shine."),
   ("Paper napkins", "Separate the printed top layer and glue it on for a painted look."),
   ("Paper doilies", "Layer behind photos or use half as a tuck spot."),
   ("Cupcake liners", "Flatten into circles for frames and flowers."),
   ("Sugar and coffee sachets", "Empty, flatten and tuck in a café page."),
   ("Recipe cards", "Your own handwriting or a family recipe makes a page on its own."),
   ("Receipts", "Save the story, but use a copy if it matters (see the receipt note below)."),
 ]),
 ("Post and print", "post", [
   ("Stamps", "Soak or cut them off envelopes; use them as small focal points."),
   ("Postmarks and airmail envelopes", "Cut out the corner with the stamp and postmark together."),
   ("Junk mail with nice lettering", "Cut out big numbers and words for page titles."),
   ("Catalogue and magazine pages", "Cut out pictures, colours and words."),
   ("Newspaper headlines", "Date a page with the day's headline."),
   ("Seed packets", "Open flat for a garden spread, or keep whole as a pocket."),
   ("Business cards", "Turn them over: the blank back is a ready-made journaling card."),
   ("Flyers and leaflets", "Use event leaflets on the page about that day."),
 ]),
 ("Out and about", "out", [
   ("Tickets (train, bus, cinema, concert)", "The classic. Tuck under a belly band or glue with the date showing."),
   ("Museum maps and leaflets", "Cut out the floor plan or the logo for a trip page."),
   ("Takeaway menus", "The lettering and prices date a page nicely."),
   ("Bookmarks from shops", "Slip into the spine as a page marker."),
   ("Luggage tags and wristbands", "Tie on with string through a punched hole."),
   ("Boarding passes", "Often thermal paper, so copy it before it fades."),
   ("Coasters", "Thick card for a cover or a sturdy pocket."),
   ("Pressed leaves and flowers", "Press for a week or two between book pages, then glue."),
   ("Paint colour swatches", "Free palettes and tags, if the shop is happy for you to take a few."),
 ]),
 ("Sewing and craft box", "craft", [
   ("Fabric scraps", "Glue or stitch on for texture."),
   ("Ribbon, lace and string", "Ties, bookmarks and belly bands."),
   ("Buttons", "Use as a closure with string wound round it."),
   ("Clothing and swing tags", "Ready-made tags with a hole already punched."),
   ("Yarn ball bands", "Keep the band from a favourite yarn on your project page."),
   ("Sewing pattern tissue", "Thin and printed, lovely glued over a background."),
   ("Washi tape ends", "The last bit of a roll is still enough to tape a corner."),
   ("Fabric selvedges", "The printed edge strip makes a ready-made border."),
 ]),
 ("Vintage finds", "vintage", [
   ("Old letters and postcards", "Ask family first, and use a copy of anything precious."),
   ("Ledger or account book pages", "Columns and handwriting make beautiful backgrounds."),
   ("Playing cards", "Odd cards from an old deck become tags and journaling cards."),
   ("Old photographs", "Garage sales and antiques fairs sell boxes of them cheaply."),
   ("Lottery and raffle tickets", "Small, numbered and colourful."),
   ("Film strips and slides", "Tape over a window cut into a page."),
 ]),
 ("Make your own", "make", [
   ("Tea-stained paper", "Plain paper plus a cup of tea gives aged pages."),
   ("Tags cut from card", "Cut a rectangle, snip the top corners and punch a hole."),
   ("Pockets from envelopes", "Cut an envelope in half and you have two pockets."),
   ("Hand-lettered labels", "Write a word or date on a strip of paper and age the edges."),
   ("Rubbings and stamps", "Rub a crayon over a leaf or coin, or print with a potato stamp."),
   ("Printed ephemera", "Print tickets, labels and tags when you want a theme fast."),
 ]),
]
EP_N = sum(len(x[2]) for x in EP)
def _ep_id(t): return "".join(c if c.isalnum() else "-" for c in t.lower()).strip("-")[:40]
ep_list = "".join(f'<fieldset class="ep-grp sheet" data-g="{gid}"><legend>{e(gn)} <span class="muted ep-gc" data-g="{gid}"></span></legend><ul>' +
                  "".join(f'<li><label><input type="checkbox" data-id="{gid}-{_ep_id(n)}" data-n="{e(n)}"> <strong>{e(n)}</strong></label><span>{e(t)}</span></li>' for n, t in items) + "</ul></fieldset>"
                  for gn, gid, items in EP)
EP_USE = [("Tuck spot", "Glue a strip of paper, lace or a doily along three sides, or just the ends, and slide tickets and tags behind it."),
          ("Pocket", "Half an envelope or a folded paper bag glued at the sides and bottom. Holds anything loose."),
          ("Belly band", "A strip of paper or ribbon wrapped round the page. Tuck tickets and cards under it."),
          ("Fold-out", "Glue one edge of a big map, menu or sheet of music and fold it to fit the page."),
          ("Flip-up", "Glue only the top edge of a postcard or photo so you can lift it and read the back."),
          ("Layer cluster", "Stack three or four pieces from biggest to smallest, slightly off-centre, with one focal piece on top.")]
ep = top("Junk journal ephemera ideas", f"{EP_N} free ephemera ideas for your junk journal, where to find them, how to use them on a page, and a checklist that remembers what you've collected.", "Junk journal ephemera ideas") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> ephemera is everyday paper made to be used once and thrown away, like tickets, receipts, labels, tags, stamps, postcards and packaging. In a junk journal you glue it in, tuck it in pockets or tie it on to tell the story of a day. Most of it is free: start a box at home and drop in anything with nice colours, lettering or a memory attached.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div>
<div class="toolbar"><strong id="ep-count" aria-live="polite">0 of {EP_N} collected</strong><span class="spacer"></span><button type="button" class="btn ghost" id="ep-print">Print my list</button><button type="button" class="linkbtn" id="ep-clear">Clear ticks</button></div>
<div class="ep-list" id="ep-list">{ep_list}</div>
</div>
<div class="result" id="ep-out" aria-live="polite"><h3>Ephemera for your next page</h3><p class="sub" id="ep-hint">Tick what you've got (or leave it blank to pick from everything), then shuffle.</p>
<div class="ep-pile" id="ep-pile"></div><p id="ep-how"></p>
<div class="btns" style="margin-top:12px"><button type="button" class="btn gold" id="ep-go">Pick 3 for a page</button></div>
<hr><p class="sub">Your ticks are saved on this device only. Nothing is uploaded.</p></div>
</div></section>
{AD.format("ep-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>What is ephemera in junk journaling?</h2>
<p>Ephemera means paper things made for a short time or one occasion: a concert ticket, a sweet wrapper, a seed packet, a bus ticket, a gift tag. They're meant to be thrown away, which is exactly why they're special once they're kept. In a junk journal, ephemera is anything you add to the pages to decorate them or hold a memory, from a fruit sticker to a whole old letter.</p>
<h2>Where can I find free ephemera?</h2>
<ul><li><strong>Your own bin and recycling.</strong> Envelopes, packaging, labels, paper bags and junk mail.</li>
<li><strong>Your wallet and pockets.</strong> Receipts, tickets, business cards and loyalty cards that have run out.</li>
<li><strong>Boxes of old cards and photos.</strong> Ask before you cut anything that belongs to someone else.</li>
<li><strong>Days out.</strong> Museum leaflets, maps, menus, wristbands and brochures are free to take.</li>
<li><strong>Your craft box.</strong> Yarn ball bands, fabric scraps, ribbon, buttons and tags.</li>
<li><strong>Garage sales and antiques fairs</strong> for vintage paper, which costs a little but is often cheap by the bag.</li></ul>
<h2>How do I use ephemera on a junk journal page?</h2></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Technique</th><th scope="col">How</th></tr></thead><tbody>{"".join(f"<tr><td><strong>{e(a)}</strong></td><td>{e(b)}</td></tr>" for a, b in EP_USE)}</tbody></table></div></div>
<div class="narrow prose"><p>Lay everything out before you glue, so you can move pieces around. Three to five pieces is plenty for one spread (our rule of thumb); more starts to look busy. Add a line of writing, a date or a doodle to pull it together. Stuck for a theme? The <a href="@@JP@@">journal prompt generator</a> picks a theme, a piece of ephemera and a technique for you.</p>
<h2>Do receipts fade in a junk journal?</h2>
<p>Most shop receipts, boarding passes and some tickets are printed on thermal paper, which isn't made to last. Archive guides from the National Archives of Australia and the University of Illinois say it can fade noticeably within about five years, faster with heat, light and humidity. If a receipt matters to you, photocopy or scan it and glue in the copy, or keep the original in a pocket away from light. Treat fading as part of the charm for everything else.</p>
<h2>How should I store ephemera?</h2>
<ul><li><strong>Sort by type or colour</strong> into envelopes or zip bags: tickets, tags, labels, papers, fabric.</li>
<li><strong>Keep it flat</strong> in a shoe box, file folder or a spare journal, so it doesn't curl.</li>
<li><strong>Keep it dry and out of the sun,</strong> especially photos and thermal paper.</li>
<li><strong>Theme bags work well:</strong> fill one envelope per trip, season or month, then make a spread from it.</li></ul>
<h2>Can I make my own ephemera?</h2>
<p>Yes, and it's half the fun. Stain plain paper with tea (our <a href="@@TS@@">tea staining guide</a> has the recipe), cut tags from cereal box card, turn envelopes into pockets, and write labels by hand. If you'd like a themed set ready to cut out, our printable ephemera packs below do exactly that. New to all this? Start with <a href="@@JJ@@">junk journaling for beginners</a>, and see what else you need in our <a href="@@JS@@">junk journal supply checklist</a>.</p>
<p class="note">Ideas and techniques gathered from LoveCrafts' ephemera guide, Upcycle My Stuff and My Modern Met's junk journal guides; thermal paper advice from the National Archives of Australia and the University of Illinois preservation guide. Descriptions are our own.</p></div></section>'''
for k_, f_ in (("@@JP@@", "journal-prompts.html"), ("@@TS@@", "how-to-tea-stain-paper.html"), ("@@JJ@@", "junk-journal-beginners.html"), ("@@JS@@", "junk-journal-supply-checklist.html")):
    ep = ep.replace(k_, href(f_))
ep_faq = [
    ("What is ephemera in a junk journal?", "Everyday paper made for one use or a short time, like tickets, receipts, labels, tags, stamps and packaging, that you glue or tuck into your journal to decorate it and keep a memory."),
    ("Where can I get free ephemera for junk journaling?", "Start at home: envelopes, food labels, tea bag tags, junk mail, old cards and postcards. Add tickets, maps and leaflets from days out, and ball bands, ribbon and fabric from your craft box."),
    ("Can you put receipts in a junk journal?", "Yes, but most receipts are thermal paper and can fade within a few years. Glue in a photocopy or scan if you want to keep it, and keep originals away from light and heat."),
    ("How do you make your own ephemera?", "Tea stain plain paper, cut tags from cereal box card, turn envelopes into pockets, hand-letter labels, or print themed ephemera sheets and cut them out."),
    ("How much ephemera do I need for a junk journal?", "Less than you think. Three to five pieces per spread is a good start. A shoe box of saved paper will fill a first journal with room to spare."),
    ("How do I store junk journal ephemera?", "Flat and dry, sorted into envelopes or zip bags by type, colour or theme, in a box or file folder out of direct sun."),
]
page("junk-journal-ephemera-ideas.html", "Junk Journal Ephemera Ideas: 60+ Free Things to Use (Checklist) | Purl & Paper",
     f"{EP_N} free junk journal ephemera ideas from around the house, the kitchen, the post and days out, where to find them, how to use them on a page, whether receipts fade, plus a checklist that saves your ticks.",
     ep, ep_faq, "Junk journal ephemera ideas", app_name="Junk journal ephemera checklist")

# ---------------- TEMPERATURE BLANKET PLANNER ----------------
TB = D["tblanket"]; TB_YD = 0.667   # yd per sq in of plain worsted knitting, the same model as the blanket size calculator
TB_M = {w["n"]: w["m"] for w in D["weights"]}
def tb_st(i): return [s for s in TB["stitches"] if s["id"] == i][0]
def tb_len(st, wn, rows):
    base = (TB["cg"] if st["craft"] == "crochet" else TB["kg"])[str(wn)]
    return rows / (base * st["r"] / 4)
def tb_yd(st, wn, width, rows): return width * tb_len(st, wn, rows) * TB_YD * TB_M[wn] * (1.27 if st["craft"] == "crochet" else 1) * st["d"]
def tb_sts(st, wn, width):
    base = (TB["cg"] if st["craft"] == "crochet" else TB["kg"])[str(wn)]
    n = int(width * base * st["w"] / 4 + 0.5)
    return n + (n % 2 if st.get("even") else 0)
def tb_fmt_len(x): return f"{x:.0f} in ({x * 2.54:.0f} cm)"
TB_ROWS = [("sc", 1), ("moss", 1), ("hdc", 1), ("dc", 1), ("garter", 2), ("st", 1)]
TB_SHORT = {"sc": "Single crochet (UK dc)", "moss": "Moss / linen stitch", "hdc": "Half double crochet (UK htr)", "dc": "Double crochet (UK tr)", "garter": "Garter stitch, 2 rows a day", "st": "Stockinette, 1 row a day"}
tb_rows = "".join(f'<tr><th scope="row">{e(TB_SHORT[i])}</th>' + "".join(f"<td>{tb_fmt_len(tb_len(tb_st(i), w, 365 * r))}</td>" for w in (3, 4, 5)) +
                  f"<td>{fmt_n(round(tb_yd(tb_st(i), 4, 50, 365 * r), -1))} yd</td></tr>" for i, r in TB_ROWS)
_tb_sc = tb_len(tb_st("sc"), 4, 365); _tb_scy = round(tb_yd(tb_st("sc"), 4, 50, 365), -2); _tb_g = tb_len(tb_st("garter"), 4, 730)
_tb_mo = tb_len(tb_st("moss"), 4, 365); _tb_dk = tb_len(tb_st("sc"), 3, 365)
tb_st_opts = "".join(f'<option value="{s["id"]}"{" selected" if s["id"] == "sc" else ""}>{e(s["name"])}</option>' for s in TB["stitches"])
tb_w_opts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])})</option>' for w in D["weights"] if 1 <= w["n"] <= 6)
tb_p_opts = "".join(f'<option value="{p["id"]}">{e(p["name"])}</option>' for p in TB["palettes"])
tb = top("Temperature blanket planner: colours, ranges and yarn", "Set your coldest and hottest temperatures, how many degrees each colour covers, your stitch and yarn. Get a colour key you can edit, how long the blanket will be, the foundation chain or cast-on, and how much yarn to buy for each colour. Paste last year's temperatures to see the real blanket.", "Temperature blanket planner") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> a temperature blanket has one row (or two) for every day of the year, coloured by that day's temperature. Most makers use <strong>8 to 10 colours</strong>, each covering about <strong>5 to 10°F</strong> (or 3 to 5°C), from their area's usual coldest day to its hottest. 365 rows of single crochet in worsted yarn come out about <strong>{_tb_sc:.0f} in long</strong>, and a 50 in wide blanket needs roughly <strong>{fmt_n(_tb_scy)} yards</strong>. Garter stitch at two rows a day is shorter, about {_tb_g:.0f} in. These are estimates at a typical gauge: put your own swatch in below.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><span class="label" id="tb-unit-l">Temperatures in</span><div class="seg" role="group" aria-labelledby="tb-unit-l" id="tb-unit"><button type="button" data-v="F" aria-pressed="true">°F</button><button type="button" data-v="C" aria-pressed="false">°C</button></div></div>
<div class="row3"><div class="field"><label for="tb-lo">Coldest: below</label><input type="number" id="tb-lo" value="20" min="-80" max="120" step="1" inputmode="numeric"></div>
<div class="field"><label for="tb-hi">Hottest: from</label><input type="number" id="tb-hi" value="100" min="-60" max="140" step="1" inputmode="numeric"></div>
<div class="field"><label for="tb-step">Degrees per colour</label><input type="number" id="tb-step" value="10" min="1" max="30" step="1" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="tb-pal">Colour set</label><select id="tb-pal">{tb_p_opts}</select></div>
<div class="field"><label for="tb-mode">Rows per day</label><select id="tb-mode"><option value="1">1 row a day</option><option value="2">2 rows a day</option><option value="hl">2 rows: high, then low</option></select></div></div>
<div class="row2"><div class="field"><label for="tb-st">Stitch</label><select id="tb-st">{tb_st_opts}</select></div>
<div class="field"><label for="tb-y">Yarn weight</label><select id="tb-y">{tb_w_opts}</select></div></div>
<div class="row3"><div class="field"><label for="tb-w">Blanket width</label><input type="number" id="tb-w" value="50" min="6" max="140" step="1" inputmode="decimal"></div>
<div class="field"><label for="tb-wu">Unit</label><select id="tb-wu"><option value="in">inches</option><option value="cm">cm</option></select></div>
<div class="field"><label for="tb-days">Days</label><select id="tb-days"><option value="365">A year, 365</option><option value="366">Leap year, 366</option><option value="183">Half a year</option><option value="92">A season (3 months)</option><option value="31">One month (a scarf)</option></select></div></div>
<div class="row2"><div class="field"><label for="tb-sep">Rows between months</label><select id="tb-sep"><option value="0">None</option><option value="1">1 row in a border colour</option><option value="2">2 rows in a border colour</option></select></div>
<div class="field"><label for="tb-sk">Yarn per skein (yd)</label><input type="number" id="tb-sk" value="200" min="10" max="2000" step="1" inputmode="numeric"></div></div>
<details class="tb-more"><summary>Use my own swatch</summary>
<div class="row3"><div class="field"><label for="tb-gs">Stitches</label><input type="number" id="tb-gs" min="2" max="60" step="0.5" inputmode="decimal" placeholder="typical"></div>
<div class="field"><label for="tb-gr">Rows</label><input type="number" id="tb-gr" min="2" max="80" step="0.5" inputmode="decimal" placeholder="typical"></div>
<div class="field"><label for="tb-gu">Measured over</label><select id="tb-gu"><option value="4">4 in</option><option value="10">10 cm</option></select></div></div>
<p class="note">Leave blank to use a typical gauge for the yarn and stitch (our estimate).</p></details>
<details class="tb-more" id="tb-data-d"><summary>Paste real temperatures (optional)</summary>
<div class="field"><label for="tb-data">One day per line, in order from the first day. For "high, then low", put both on the line: 41, 28</label>
<textarea id="tb-data" rows="6" placeholder="34&#10;29&#10;41, 28"></textarea></div>
<p class="note">Copy last year's daily highs from a weather history site (see below) to see your blanket and the real yarn for each colour. Nothing is uploaded.</p></details>
<h3 class="tb-h">Your colour key</h3>
<p class="note">Tap a swatch to change its colour.</p>
<div class="tbl-wrap tb-key-wrap"><table class="tb-key"><thead><tr><th scope="col">Colour</th><th scope="col">Temperature</th><th scope="col" id="tb-kd">Days</th><th scope="col">Yarn</th></tr></thead><tbody id="tb-key"></tbody></table></div>
<p class="btns" style="margin-top:12px"><button type="button" class="btn gold sm" id="tb-copy">Copy colour key</button><button type="button" class="btn ghost sm" id="tb-reset">Reset colours</button></p>
</div>
<div class="result" aria-live="polite"><div id="tb-out"></div>
<figure class="tb-fig"><svg id="tb-svg" viewBox="0 0 220 300" role="img" aria-label="Your temperature blanket drawn in your colours"></svg><figcaption class="note" id="tb-cap">Sample year.</figcaption></figure></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How long will a 365-row temperature blanket be?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Stitch</th><th scope="col">DK</th><th scope="col">Worsted</th><th scope="col">Bulky</th><th scope="col">Yarn, worsted, 50 in wide</th></tr></thead><tbody>{tb_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Our estimates for one year (365 days), worked by the same maths as the planner. Gauges are typical values: the middle of the Craft Yarn Council range for each yarn weight, with our own row-height factors for each stitch. Real blankets vary a lot with hook size and tension, so swatch and use the planner with your own numbers. Yarn is a middle estimate; buy 10 percent more.</p>
</div></section>
{AD.format("tb-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How many colours do you need for a temperature blanket?</h2>
<p>Most temperature blankets use between 6 and 12 colours, and 8 to 10 is the most common. Fewer colours give bold, wide stripes; more colours show small changes from day to day but cost more yarn and more ends to weave in. Work it out from your weather: take the range from your usual coldest day to your usual hottest, and divide it by how many degrees you want each colour to cover.</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Climate</th><th scope="col">Coldest colour</th><th scope="col">Each colour</th><th scope="col">Colours</th></tr></thead><tbody>
<tr><td>Hot summers, cold winters (much of the US), °F</td><td>Below 10°F</td><td>10°F</td><td>11</td></tr>
<tr><td>Same climate, fewer colours, °F</td><td>Below 20°F</td><td>15°F</td><td>7</td></tr>
<tr><td>Mild all year (UK, coastal), °C</td><td>Below 0°C</td><td>3°C</td><td>10</td></tr>
<tr><td>Hot all year, °F</td><td>Below 60°F</td><td>5°F</td><td>9</td></tr>
</tbody></table></div>
<p>Each row counts the end colours too: one for anything colder than your lowest number and one for anything hotter than your highest. Many makers keep those two for rare days and pick a bold contrast for them, so a record heatwave or a deep freeze stands out.</p>
<h2>How do I choose my temperature ranges?</h2>
<ol><li><strong>Look up last year</strong> (or the last few years) for your town. Weather Underground's history pages, NOAA's Climate Data Online (US), the Met Office (UK) and your own national weather service all list daily highs and lows.</li>
<li><strong>Note the usual lowest and highest</strong> daily values for the temperature you'll track. Ignore one freak day: it can go in an end colour.</li>
<li><strong>Pick a step</strong>. A spread of about 100°F suits 10°F per colour; a narrower spread of 60 to 70°F suits 5 to 7°F, and in Celsius 2 to 5° per colour is usual.</li>
<li><strong>Check the middle</strong>. Most days fall in the middle bands, so give those colours you love, and buy more of them.</li></ol>
<div class="callout"><strong>Tip:</strong> paste last year's daily highs into the planner. It counts the days for each colour, so you can see if one colour would take over half the blanket and change the step before you buy yarn.</div>
<h2>Should I use the high, the low or the average?</h2>
<p>Any of them works; just pick one and stick with it all year. The daily high is the most common choice because it's the number in every forecast. The average gives gentler stripes. For more detail, work two rows a day: the high, then the low. That doubles the rows, so use a thinner yarn or a narrower blanket, or the blanket gets very long.</p>
<h2>Why is my temperature blanket so long?</h2>
<p>Because 365 rows is a lot of rows. Even short single crochet stitches in worsted yarn add up to well over 2 metres, which is longer than a queen bed. To keep it a usable size, choose a shorter stitch or thinner yarn (DK single crochet comes out about {_tb_dk:.0f} in), or knit garter stitch, where two rows make one ridge. Moss stitch, a mix of single crochet and chains, is popular because it lies flat and shows colour stripes neatly (about {_tb_mo:.0f} in in worsted). Some makers work each day as a granny square or hexagon instead, then join them in a grid, which gives a square blanket with no length problem.</p>
<h2>How much yarn does a temperature blanket take?</h2>
<p>A full-size year blanket usually takes 3,000 to 5,000 yards of worsted yarn, split across your colours. The planner gives the total and an even share per colour, or the exact share if you paste real temperatures. For your own yarn, crochet one row, weigh the ball before and after, and multiply by the number of days: 7 g a day for 365 days is 2,555 g, plus about 10 percent spare.</p>
<p>Buying it all at once keeps dye lots matching, while buying a ball of each colour and adding more as the months go spreads the cost. If you buy as you go, choose a yarn that's widely stocked so you can still get it in October. Machine-washable acrylic or a cotton blend is easy to care for in a blanket this big.</p>
<p>Crocheting it in rows? Change colour on the last stitch of the row and carry colours up the side when a stripe is 2 or 4 rows: our guide to <a href="{href("how-to-change-colors-in-crochet.html")}">changing colours in crochet</a> has a stripe planner that shows which colours to carry and which to cut.</p>
<h2>How do I keep up with a temperature blanket?</h2>
<ul><li><strong>Log temperatures daily</strong>, even when you don't crochet. Then you can catch up in batches at the weekend.</li>
<li><strong>Add a month row</strong> in a neutral or border colour between months. It makes the blanket easy to read and gives you a checkpoint.</li>
<li><strong>Count rows</strong> with our <a href="{href("row-counter.html")}">row counter</a>, one tap per day.</li>
<li><strong>Weave ends in as you go</strong>, or leave 5 in tails at the edges and knot them into a fringe at the end.</li>
<li><strong>Started late?</strong> Use the past months' temperatures to catch up, or make it a "last year" blanket from a full year of history.</li></ul>
<p>Prefer stripes without the weather? The <a href="{href("stripe-generator.html")}">random stripe generator</a> picks colours and widths for you.</p>
<p>What next? Check the finished size against a bed with the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>, work out the foundation for a different stitch with the <a href="{href("cast-on-calculator.html")}">cast on calculator</a>, plan a granny square version with the <a href="{href("granny-square-blanket-calculator.html")}">granny square calculator</a>, and keep notes on your yarn and colours in the <a href="{href("projects.html")}">project tracker</a>.</p></div></section>'''
tb_faq = [
    ("How many colours do you need for a temperature blanket?", "Most use 8 to 10 colours, each covering about 5 to 10°F (3 to 5°C), plus one colour for anything colder than your range and one for anything hotter. Fewer colours give bolder stripes."),
    ("What temperature ranges should I use?", "Look up last year's daily highs (or lows) for your town, find the usual coldest and hottest, and split that spread into equal steps. About 10°F per colour suits a 100°F spread; 5 to 7°F suits a narrower one."),
    ("How big is a temperature blanket?", f"One row a day for a year is 365 rows. In worsted single crochet that's roughly {_tb_sc:.0f} in long at a typical gauge, and in moss stitch about {_tb_mo:.0f} in, so many makers use DK yarn, garter stitch or a granny square per day to keep it a usable size."),
    ("How much yarn do I need for a temperature blanket?", f"A 50 in wide worsted blanket in single crochet takes about {fmt_n(_tb_scy)} yards (our estimate). Weigh one row of your own yarn and multiply by 365, then add 10 percent."),
    ("Should I use the high or the average temperature?", "Either works. The daily high is the most common because it's easy to find. You can also work two rows a day, the high and then the low, but that doubles the length."),
    ("What if I miss a day or fall behind?", "Keep writing the temperatures down every day, then catch up when you have time. Weather history sites keep the daily records, so you can always look up a missed day."),
]
page("temperature-blanket-planner.html", "Temperature Blanket Planner 2027: Colors, Ranges and Yarn Calculator | Purl & Paper",
     "Free temperature blanket planner: pick your temperature ranges and colours, see how long a 365-row crochet or knit blanket will be, the foundation chain and how much yarn per colour. Paste real temperatures to preview it.",
     tb, tb_faq, "Temperature blanket planner", app_name="Temperature blanket planner")

# ---------------- YARN YARDAGE CALCULATOR (how much yarn is left) ----------------
YY_EX = [("Fingering, 100 g / 400 m", 400 * 1.0936, 100), ("DK, 100 g / 230 m", 230 * 1.0936, 100), ("Worsted, 100 g / 200 yd", 200, 100), ("Worsted, 198 g / 364 yd (big acrylic skein)", 364, 198), ("Bulky, 100 g / 120 yd", 120, 100)]
YY_G = [5, 10, 20, 25, 50]
def yy_left(yd, g, w): return yd / g * w
yy_rows = "".join(f'<tr><td><strong>{e(n)}</strong><br><span class="muted">{yd / g:.2f} yd per gram</span></td>' + "".join(f'<td>{yy_left(yd, g, w):,.0f} yd</td>' for w in YY_G) + "</tr>" for n, yd, g in YY_EX)
yy = top("Yarn yardage calculator", "Weigh a leftover ball and find out how many yards or metres are left, even with no label. Add several scraps at once and check if you have enough for your next project.", "Yarn yardage calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> divide the length on the label by the grams on the label to get the length per gram, then multiply by what your leftover weighs. A worsted ball of 200 yd in 100 g gives 2 yd per gram, so a 37 g leftover has about <strong>74 yards</strong> left. No label? Measure off 10 yards, weigh it, and use that instead.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label>How do you know the yarn's length?</label><div class="seg" id="yy-mode" role="group" aria-label="Where the length comes from"><button type="button" data-v="label" aria-pressed="true">From the label</button><button type="button" data-v="measure" aria-pressed="false">I'll weigh a measured piece</button></div></div>
<div id="yy-lab">
<div class="row2"><div class="field"><label for="yy-ll">Length of a full ball</label><input type="number" id="yy-ll" value="200" min="1" max="5000" step="1" inputmode="decimal"></div>
<div class="field"><label for="yy-lu">Unit</label><select id="yy-lu"><option value="yd">yards</option><option value="m">metres</option></select></div></div>
<div class="row2"><div class="field"><label for="yy-lg">Weight of a full ball</label><input type="number" id="yy-lg" value="100" min="1" max="2000" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="yy-lgu">Unit</label><select id="yy-lgu"><option value="g">grams</option><option value="oz">ounces</option></select></div></div>
</div>
<div id="yy-mea" hidden>
<div class="row2"><div class="field"><label for="yy-ml">Length you measured</label><input type="number" id="yy-ml" value="10" min="0.5" max="500" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="yy-mu">Unit</label><select id="yy-mu"><option value="yd">yards</option><option value="m">metres</option></select></div></div>
<div class="field"><label for="yy-mg">What that piece weighs (grams)</label><input type="number" id="yy-mg" value="5" min="0.1" max="1000" step="0.1" inputmode="decimal"><span class="note">Measure enough to weigh at least 10 g if your scale only shows whole grams.</span></div>
</div>
<hr class="stitch" style="margin:14px 0 18px">
<div class="field"><label>Your leftovers</label><div class="seg" id="yy-wu" role="group" aria-label="Scale unit"><button type="button" data-v="g" aria-pressed="true">grams</button><button type="button" data-v="oz" aria-pressed="false">ounces</button></div></div>
<ol class="yy-list" id="yy-list"></ol>
<p><button type="button" class="btn ghost sm" id="yy-add">Add another ball</button></p>
<div class="field"><label for="yy-core">Card core, cone or tube to take off each ball (grams)</label><input type="number" id="yy-core" value="0" min="0" max="500" step="0.5" inputmode="decimal"><span class="note">Weigh an empty core of the same kind, or leave 0 for a centre-pull ball or cake.</span></div>
<div class="row2"><div class="field"><label for="yy-need">Your project needs (optional)</label><input type="number" id="yy-need" placeholder="e.g. 150" min="0" max="100000" step="1" inputmode="decimal"></div>
<div class="field"><label for="yy-nu">Unit</label><select id="yy-nu"><option value="yd">yards</option><option value="m">metres</option></select></div></div>
</div>
<div class="result" aria-live="polite" id="yy-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How many yards are in 10, 25 or 50 grams of yarn?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">If the label says</th>{"".join(f'<th scope="col">{w} g left</th>' for w in YY_G)}</tr></thead><tbody>{yy_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Worked out with the same formula as the calculator, from example labels. Yarns of the same weight vary a lot, so use your own label for a real answer. 1 yard = 0.9144 m.</p>
</div></section>
{AD.format("yy-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How do I work out how much yarn is left in a ball?</h2>
<ol><li><strong>Find the label numbers.</strong> You need the length and the weight of a full ball, for example 200 yd and 100 g.</li>
<li><strong>Work out the length per gram.</strong> 200 ÷ 100 = 2 yards per gram.</li>
<li><strong>Weigh the leftover</strong> on a kitchen scale in grams. Put it in a small bowl if it rolls, and zero the scale with the bowl on first.</li>
<li><strong>Multiply.</strong> 37 g × 2 = 74 yards left.</li></ol>
<p>The same sum works backwards. Need 120 yards? 120 ÷ 2 = 60 g, so wind off yarn until the ball has dropped by 60 g. Knitting designers and yarn shops such as Elizabeth Smith Knits and Pacific Knit Co. use exactly this method for partial skeins.</p>
<h2>What if I lost the label?</h2>
<p>If you know the brand and colour, look the yarn up on the maker's site or a yarn database. If not, make your own label:</p>
<ol><li>Measure off a length you can count easily, like 10 yards or 10 metres. A tape measure or a table of known length helps.</li>
<li>Weigh that piece. If your scale shows whole grams only, measure a longer piece (20 or 30 yards) so the weight is at least 10 g. A 1 g error on 5 g is 20 percent; on 20 g it is 5 percent.</li>
<li>Choose "I'll weigh a measured piece" in the calculator and type both numbers in. Wind the piece back on: you haven't lost it.</li></ol>
<h2>How accurate is weighing yarn?</h2>
<ul><li><strong>Labels are rounded.</strong> A "100 g" ball can weigh a few grams more or less, and the length on the label is the maker's estimate, so treat your answer as close, not exact.</li>
<li><strong>Your scale matters.</strong> A kitchen scale that reads in whole grams is fine for most leftovers. A small jewellery or postage scale that shows 0.1 g is better for tiny scraps and mini skeins.</li>
<li><strong>Take off the core.</strong> Big acrylic skeins, cones and some cotton balls are wound on card or plastic. Weigh an empty one and type it in so it isn't counted as yarn.</li>
<li><strong>Weigh dry yarn.</strong> Damp or freshly washed yarn weighs more.</li></ul>
<div class="callout"><strong>Leave some spare.</strong> If the leftover only just covers what a project needs, it's a gamble. Our rule of thumb is to have about 10 percent more than the pattern asks for, more for anything you can't easily finish in a different colour.</div>
<h2>How many skeins did my finished project use?</h2>
<p>Weigh the finished piece and divide by the weight of one ball. A hat that weighs 140 g used 1.4 balls of 100 g yarn, which tells you to buy two next time. It's the quickest way to write your own pattern notes, and handy for the <a href="{href("projects.html")}">project tracker</a> or pricing an item with our <a href="{href("how-to-price-crochet-items.html")}">pricing guide</a>.</p>
<h2>What can I make with my leftovers?</h2>
<p>Once you know the yards, check the amount against the <a href="{href("yarn-calculator.html")}">yarn calculator</a> for hats, scarves and more. Small amounts in one weight make good granny squares (see the <a href="{href("granny-square-blanket-calculator.html")}">granny square calculator</a>), and lots of different colours are perfect for stripes. Swapping a leftover into a pattern that names another yarn? The <a href="{href("yarn-substitution-calculator.html")}">yarn substitution calculator</a> turns the pattern's balls into yours.</p>
<p class="note">Method from Elizabeth Smith Knits, Pacific Knit Co. and Andrea Rangel's yarn weighing tutorials (formula, whole-gram scales, label weights being approximate). The measured-piece method, table and spare-yarn rule of thumb are our own.</p></div></section>'''
yy_faq = [
    ("How do I calculate yards of yarn from grams?", "Divide the yards on the label by the grams on the label to get yards per gram, then multiply by the grams you have. For a 200 yd, 100 g ball that's 2 yards per gram, so 50 g is about 100 yards."),
    ("How much yarn is left in my skein?", "Weigh it in grams and multiply by the label's length per gram. If the skein is wound on a card core or cone, weigh an empty one and subtract it first."),
    ("How do I find the yardage of yarn with no label?", "Measure off 10 or 20 yards, weigh that piece, and divide the length by its weight to get yards per gram. Then weigh the whole ball and multiply."),
    ("How many yards are in 50 grams of yarn?", "It depends on the thickness. 50 g is about 220 yd of fingering, 125 yd of DK, 100 yd of a typical worsted and 60 yd of bulky, but check your own label because yarns vary."),
    ("Is weighing yarn accurate?", "Close enough for planning. Labels are rounded and kitchen scales read to the nearest gram, so add about 10 percent spare when a leftover only just covers a project."),
    ("How do I know how many skeins I used?", "Weigh the finished project and divide by the weight of one full skein. A 140 g hat used about 1.4 skeins of 100 g yarn."),
]
page("yarn-yardage-calculator.html", "Yarn Yardage Calculator: How Much Yarn Is Left? (Weigh It) | Purl & Paper",
     "Free yarn yardage calculator: weigh a leftover ball or scrap to see how many yards or metres are left, work without a label, take off a cone or core, and check if it's enough for your project.",
     yy, yy_faq, "Yarn yardage calculator", app_name="Yarn yardage calculator")

# ---------------- CRAFT FAIR CHECKLIST (crochet, knit and paper sellers) ----------------
CF = [
 ("Before the day", "before", [
   ("Confirm the details", "Date, set-up time, booth size, whether a table or power is included, and where to park."),
   ("Make a stock list", "Every item and how many, so you can count what sold afterwards."),
   ("Price everything", "A tag on every item, plus a few signs for groups at the same price."),
   ("Practise your set-up at home", "Lay it out on a table the same size and take a photo to copy on the day."),
   ("Charge and test the card reader", "Do a test sale at home so you know it connects."),
   ("Get your cash float", "Small notes and coins from the bank a few days before."),
   ("Check the weather", "Pack layers, and rain covers for outdoor fairs."),
   ("Pack the car the night before", "Heavy boxes first, the table and display on top so they come out first."),
 ]),
 ("Booth and display", "booth", [
   ("Table, if the fair doesn't give one", "Check the size you're allowed before you buy."),
   ("Tablecloth that reaches the floor", "Hides boxes and spare stock under the table."),
   ("Risers, crates or baskets", "Height makes a table look full and lets people see from the aisle."),
   ("Hat stands, heads or hooks", "Beanies, scarves and shawls sell better when people can see the shape."),
   ("Stands or easels for prints and cards", "Paper goods disappear when they lie flat."),
   ("Sign with your shop name", "At eye level or higher, so people remember you."),
   ("Mirror", "For anyone trying on a hat, scarf or shawl."),
   ("Clip lights and an extension lead", "Only if the fair has power for you. Indoor halls can be dim."),
   ("Clips, hooks and S-hooks", "For hanging items from a grid wall or rail."),
   ("A chair or stool", "Something you can perch on and still be at eye level."),
 ]),
 ("Money and payments", "money", [
   ("Card reader and phone", "Fully charged, with the app logged in."),
   ("Power bank and cable", "Card payments and photos drain a phone fast."),
   ("Cash float in small notes and coins", "Enough to give change for your first few sales."),
   ("Cash box, pouch or apron", "An apron keeps money on you, not on the table."),
   ("Sales notebook or app", "Write down what sold and the price as you go."),
   ("Calculator", "For bundle deals and quick totals."),
   ("QR code for payment or your shop", "Printed on a small sign."),
   ("A way to send receipts", "Most card apps can email or text one."),
 ]),
 ("Price tags and signs", "price", [
   ("Price on every item", "Many shoppers won't ask, they just walk on."),
   ("Group price signs", "\"All hats $25\" is quicker to read than 20 tags."),
   ("Bundle or deal sign", "\"Any 3 cards for $10\" moves small items."),
   ("Sizes on wearables", "Baby, child, adult on hats, mittens and socks."),
   ("Care labels for knits and crochet", "Fibre and how to wash it. Buyers often ask."),
   ("\"Custom orders welcome\" sign", "With how to contact you after the fair."),
   ("Spare blank tags and a pen", "For anything that loses its tag."),
 ]),
 ("Packaging", "pack", [
   ("Bags, more than you think", "Paper bags in two or three sizes."),
   ("Tissue paper", "Wrap gifts and delicate pieces."),
   ("Clear sleeves or cello bags", "Keep cards, prints and journals clean and dry."),
   ("Stickers or tape to close bags", "A shop-name sticker is cheap branding."),
   ("Thank-you or care cards", "Drop one in each bag with your shop link."),
   ("Gift tags", "Offer to tag gifts at Christmas fairs."),
   ("A sturdy box for spare stock", "Restock the table as things sell."),
 ]),
 ("Marketing", "market", [
   ("Business cards", "With your Etsy shop, social handle and email."),
   ("Email sign-up sheet or QR code", "People who don't buy today often buy later."),
   ("Social media sign", "Your handle, big enough to photograph."),
   ("A few photos of past custom orders", "In a small album or on a tablet."),
 ]),
 ("Tools and fix-it kit", "tools", [
   ("Scissors", ""),
   ("Clear tape and masking tape", "For signs, tablecloths and quick fixes."),
   ("Safety pins", "For attaching tags to soft items without damage."),
   ("Zip ties and clips", "For banners and grid walls."),
   ("Pens and a marker", "Signs, receipts and sold notes."),
   ("Crochet hook and darning needle", "Fix a pulled stitch or loose end on the spot."),
   ("Tape measure", "For people asking \"will this fit?\""),
   ("Lint roller", "Dark yarn and tablecloths pick up fluff."),
   ("Bin bag", "Leave your space tidy."),
 ]),
 ("Yarn and paper extras", "extras", [
   ("A swatch people can touch", "Shoppers want to feel yarn. A labelled swatch saves your stock from handling."),
   ("Hat or sock size card", "A small chart helps gift buyers pick the right size."),
   ("Work in progress", "Crocheting or knitting at the booth starts conversations."),
   ("A sample journal to flip through", "Let people handle one copy instead of every journal."),
   ("Weights or clips for paper", "Stops cards and prints lifting in a draught or wind."),
   ("Rain-proof tubs for paper stock", "Paper and damp don't mix."),
 ]),
 ("Comfort", "comfort", [
   ("Water and snacks", "You may not get a break for hours."),
   ("Warm layers and comfortable shoes", "Halls and car parks get cold. You'll stand for most of the day."),
   ("Hand warmers", "Winter fairs especially."),
   ("Hand sanitiser and tissues", ""),
   ("Small first aid kit and painkillers", ""),
   ("A friend for breaks", "Or ask a neighbouring stall to watch your table."),
 ]),
 ("Outdoor fair extras", "outdoor", [
   ("Pop-up canopy (often 10 × 10 ft)", "Check the size the fair allows."),
   ("Tent weights on every leg", "Wind can lift a tent fast; see the weight tip below."),
   ("Side walls", "Shelter from wind, rain and low sun."),
   ("Plastic covers or a tarp", "Throw over the table if it rains."),
   ("Sunscreen, hat and lip balm", ""),
   ("Cool box", "For drinks and lunch on a warm day."),
 ]),
]
CF_N = sum(len(x[2]) for x in CF)
def _cf_id(t): return "".join(c if c.isalnum() else "-" for c in t.lower()).strip("-")[:40]
cf_list = "".join(f'<fieldset class="ep-grp sheet" data-g="{gid}"><legend>{e(gn)} <span class="muted ep-gc" data-g="{gid}"></span></legend><ul>' +
                  "".join(f'<li><label><input type="checkbox" data-id="{gid}-{_cf_id(n)}"> <strong>{e(n)}</strong></label>' + (f'<span>{e(t)}</span>' if t else "") + '</li>' for n, t in items) + "</ul></fieldset>"
                  for gn, gid, items in CF)
cf = top("Craft fair checklist", f"Everything to pack for a craft fair or Christmas market: {CF_N} things for your booth, payments, packaging and comfort, with extras for crochet, knitting and paper goods. Tick as you pack; it remembers.", "Craft fair checklist") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> the essentials are a table and floor-length cloth, a sign with your shop name, a price on every item, a charged card reader plus a cash float in small notes and coins, bags, business cards, and water and warm layers for you. Bring more stock than you expect to sell (two to three times is a common rule of thumb), with something at a low price point, and set it all up once at home first.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div>
<div class="toolbar"><strong id="cf-count" aria-live="polite">0 of {CF_N} packed</strong><span class="spacer"></span><button type="button" class="btn ghost" id="cf-print">Print my list</button><button type="button" class="linkbtn" id="cf-clear">Clear ticks</button></div>
<div class="ep-list" id="cf-list">{cf_list}</div>
</div>
<div class="result" id="cf-out" aria-live="polite"><h3>Stock and cash planner</h3>
<div class="field"><label for="cf-goal">What you hope to take ($)</label><input type="number" id="cf-goal" value="400" min="0" max="100000" step="10" inputmode="decimal"></div>
<div class="field"><label for="cf-avg">Your typical price ($)</label><input type="number" id="cf-avg" value="20" min="1" max="5000" step="1" inputmode="decimal"></div>
<div class="field"><label for="cf-date">Fair date (optional)</label><input type="date" id="cf-date"></div>
<div id="cf-res"></div>
<hr><p class="sub">Your ticks and numbers are saved on this device only. Nothing is uploaded.</p></div>
</div></section>
{AD.format("cf-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How much stock should I bring to a craft fair?</h2>
<p>A common rule of thumb, from craft business guides such as Craftybase, is to bring two to three times what you expect to sell. A full table sells better than a sparse one, and you can't sell what you left at home. To guess what you'll sell, divide the amount you hope to take by your typical price: $400 at $20 an item is about 20 sales, so bring 40 to 60 pieces. The planner above does this sum for you.</p>
<p>Bring a range of prices, too. Small things like coasters, bookmarks, cards and ornaments are easy yes-purchases, while blankets and big shawls draw people in even when they don't sell. Our own rule of thumb is about half your pieces at the lowest price band, a third in the middle and the rest as bigger showpieces. It's a starting point; after one or two fairs, your sales notebook will tell you what your buyers like.</p>
<h2>How much cash float do I need?</h2>
<p>Most sellers start with around $50 to $100 in small notes and coins, which is the range Craftybase suggests. Round prices make change easy: $20 instead of $19.50 means you rarely need coins. Keep the float on you in an apron or pouch, and take card payments too, since many shoppers carry little cash.</p>
<h2>How should I price items for a craft fair?</h2>
<p>Price them the same way you would online: materials, your time at an hourly rate, a little for overheads, and the booth fee shared across what you expect to sell. Our guide on <a href="{href("how-to-price-crochet-items.html")}">how to price crochet and knitted items</a> has a calculator with a craft fair option. Fairs have no Etsy fees, but card readers take a small cut of each sale, so leave room for that.</p>
<h2>How do I set up a craft fair booth?</h2>
<ul><li><strong>Use height.</strong> Crates, shelves and stands lift items to eye level and make a table look full.</li>
<li><strong>Group by type and price.</strong> All hats together under one price sign is easier to shop than a mix.</li>
<li><strong>Leave the front edge open</strong> for people to pick things up, and keep spare stock under the table.</li>
<li><strong>Show how things look in use.</strong> A beanie on a stand, a shawl draped, a junk journal open on a page.</li>
<li><strong>Practise at home</strong> and take a photo, so set-up on the day takes minutes, not an hour.</li></ul>
<h2>What do I need for an outdoor craft fair?</h2>
<p>A pop-up canopy, side walls, rain covers and, above all, weights on every leg. Annie Andre's craft fair guide suggests at least 15 lb per leg in windy spots, with 20 lb better; buckets of sand or bags of gravel work. Paper goods need extra care outdoors: keep stock in plastic tubs, display cards in clear sleeves and use clips or small weights so a gust doesn't take them.</p>
<h2>Selling crochet, knitting or junk journals at a fair</h2>
<p>Handmade yarn goods sell on touch, so let people handle a swatch or a sample rather than every piece. Put sizes on wearables and keep a small size card handy for gift buyers (our <a href="{href("hat-size-chart.html")}">hat size chart</a> has the numbers). Working on a project at the booth gives people a reason to stop and chat, and a "custom orders welcome" sign turns that chat into orders later. For junk journals, keep one sample to flip through and the rest wrapped. Planning what to make before the fair? The <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a> shows how many pieces you can finish in time.</p>
<p class="note">Checklist and tips drawn from Craftybase's craft show checklist (stock of two to three times expected sales, a $50 to $100 float, a price on every item, test the card reader), Made Urban's craft show preparation timeline, and Annie Andre's craft fair checklist (round prices for easy change, floor-length table covers, 15 to 20 lb tent weights). The yarn and paper extras, the price-band split and all wording are our own.</p></div></section>'''
cf_faq = [
    ("What should I bring to my first craft fair?", "A table and floor-length cloth, display risers, a sign with your shop name, prices on every item, a charged card reader and phone, a cash float in small notes, bags, business cards, a fix-it kit (tape, scissors, safety pins), and water, snacks and warm layers for yourself."),
    ("How much inventory should I bring to a craft fair?", "A common rule of thumb is two to three times what you expect to sell. Divide your sales goal by your typical price to estimate sales: $400 at $20 an item is about 20 sales, so bring 40 to 60 pieces across a range of prices."),
    ("How much change should I bring to a craft fair?", "Around $50 to $100 in small notes and coins is a common starting float. Round prices to whole dollars so you rarely need coins, and take card payments too."),
    ("Do I need a card reader for a craft fair?", "It's strongly recommended, as many shoppers carry little cash. A phone card reader is cheap; charge it, bring a power bank, and test a sale at home before the day."),
    ("How heavy should tent weights be at a craft fair?", "At least 15 lb per leg is a common minimum in windy places, with 20 lb or more better. Many fairs require weights on every leg, so check the rules."),
    ("What sells well at craft fairs for crocheters?", "Small, giftable items at lower prices tend to move quickly, like ornaments, coasters, hats and small toys, with a few larger showpieces to draw people in. Keep notes on what sells and adjust for the next fair."),
]
page("craft-fair-checklist.html", "Craft Fair Checklist: What to Bring (Printable, for Crochet & Paper Sellers) | Purl & Paper",
     f"Free craft fair checklist: {CF_N} things to pack for your booth, payments, packaging and comfort, extras for crochet, knitting and junk journal sellers, how much stock and cash float to bring, and a planner that remembers your ticks.",
     cf, cf_faq, "Craft fair checklist", app_name="Craft fair checklist and stock planner")

# ---------------- FOUNDATION CHAIN CALCULATOR (crochet) ----------------
FC_ST = {"sc": ("Single crochet (UK dc)", 2, 0, 1.0, 1.15), "hdc": ("Half double crochet (UK htr)", 3, 0, 0.95, 0.8),
         "dc": ("Double crochet (UK tr)", 4, 1, 0.9, 0.6), "tr": ("Treble crochet (UK dtr)", 5, 1, 0.85, 0.45)}
# id: (name, start in Nth chain from hook, skipped chains count as a stitch, stitch width vs sc, rows per 4 in vs sc stitches per 4 in). Width and row factors are our estimates.
def fc_chain(n, k, counts): return n + (k - 1) - (1 if counts else 0)
def fc_g(wn, st): return round(CI_G[wn] * FC_ST[st][3] * 2) / 2   # typical gauge, rounded to ½ stitch like the calculator
def fc_sts(width, wn, st): return max(2, int(width * fc_g(wn, st) / 4 + 0.5))
def fc_ch(width, wn, st): s = FC_ST[st]; return fc_chain(fc_sts(width, wn, st), s[1], s[2])
FC_PRE = [("scarf-child", "Child's scarf", 6, 45), ("scarf", "Adult scarf", 8, 65), ("scarf-wide", "Wide scarf", 10, 70), ("dishcloth", "Dishcloth", 8, 8), ("wrap", "Wrap or stole", 20, 70)]
fc_bl = [b for b in D["blankets"] if b["id"] in ("lovey", "stroller", "baby", "crib", "throw", "twin", "queen", "king")]
fc_opts = "".join(f'<option value="{w}|{l}"{" selected" if k == "baby" else ""}>{e(n)}, {w} in wide</option>' for k, n, w, l in FC_PRE) + \
          "".join(f'<option value="{b["w"]}|{b["l"]}"{" selected" if b["id"] == "baby" else ""}>{e(b["name"])} blanket, {b["w"]} × {b["l"]} in</option>' for b in fc_bl) + '<option value="custom">My own size</option>'
fc_wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])}), about {CI_G[w["n"]]} sc per 4 in</option>' for w in D["weights"] if w["n"] in CI_G)
fc_sopts = "".join(f'<option value="{k}"{" selected" if k == "dc" else ""}>{e(v[0])}</option>' for k, v in FC_ST.items())
FC_EX = [("Adult scarf", 8)] + [(b["name"] + " blanket", b["w"]) for b in fc_bl if b["id"] in ("baby", "crib", "throw", "twin", "queen")]
FC_EXC = [("sc", 3, "DK sc"), ("sc", 4, "Worsted sc"), ("hdc", 4, "Worsted hdc"), ("dc", 4, "Worsted dc"), ("sc", 5, "Bulky sc"), ("dc", 5, "Bulky dc"), ("dc", 6, "Super bulky dc")]
fc_rows = "".join(f'<tr><td><strong>{e(n)}</strong><br><span class="muted">{w} in ({round(w * 2.54)} cm) wide</span></td>' + "".join(f"<td>{fc_ch(w, wn, st)}</td>" for st, wn, _ in FC_EXC) + "</tr>" for n, w in FC_EX)
_fc_bb = fc_ch(36, 4, "dc"); _fc_bbs = fc_sts(36, 4, "dc"); _fc_sc = fc_ch(8, 4, "sc"); _fc_th = fc_ch(50, 4, "dc"); _fc_thsc = fc_ch(50, 4, "sc")
fc = top("Foundation chain calculator: how many chains to start?", "Pick what you're making, your yarn and your stitch. Get the number of chains, the first row written out, how wide it will really be, and about how many rows to reach the length.", "Foundation chain calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> chain the number of stitches you need across, plus the turning chain your first stitch skips: <strong>+1 for single crochet</strong>, about <strong>+2 for half double</strong>, <strong>+2 for double crochet</strong> (when the skipped chains count as the first stitch) and +3 for treble. A 36 in baby blanket in worsted double crochet needs about <strong>{_fc_bb} chains</strong> ({_fc_bbs} stitches). An 8 in scarf in worsted single crochet needs about <strong>{_fc_sc}</strong>. Swatch first, because your gauge decides the number.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="fc-what">What are you making?</label><select id="fc-what">{fc_opts}</select></div>
<div id="fc-custom" hidden><div class="row2"><div class="field"><label for="fc-w">Width</label><input type="number" id="fc-w" value="40" min="1" max="200" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="fc-l">Length</label><input type="number" id="fc-l" value="50" min="1" max="200" step="0.5" inputmode="decimal"></div></div>
<div class="field"><label for="fc-u">Unit</label><select id="fc-u"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><label for="fc-st">Stitch for the first row</label><select id="fc-st">{fc_sopts}</select></div>
<div class="field"><label for="fc-yarn">Yarn weight</label><select id="fc-yarn">{fc_wopts}</select></div>
<div class="row2"><div class="field"><label for="fc-g">Stitches in your swatch</label><input type="number" id="fc-g" value="11" min="2" max="60" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="fc-gu">Measured over</label><select id="fc-gu"><option value="4">4 in</option><option value="10">10 cm</option></select></div></div>
<p class="note" id="fc-gnote" style="margin:-4px 0 12px">Count stitches in the stitch you'll use. Filled in with a typical number until you change it.</p>
<div class="row2"><div class="field"><label for="fc-k">First stitch goes in the</label><select id="fc-k"><option value="2">2nd chain from hook</option><option value="3">3rd chain from hook</option><option value="4" selected>4th chain from hook</option><option value="5">5th chain from hook</option><option value="6">6th chain from hook</option></select></div>
<div class="field"><label for="fc-cnt">Skipped chains count as a stitch?</label><select id="fc-cnt"><option value="1" selected>Yes, as the first stitch</option><option value="0">No</option></select></div></div>
<div class="field"><label for="fc-pat">Stitch pattern</label><select id="fc-pat"><option value="plain" selected>Plain rows (any number)</option><option value="custom">My pattern says "chain a multiple of … plus …"</option></select></div>
<div class="row2" id="fc-rep" hidden><div class="field"><label for="fc-m">Multiple of</label><input type="number" id="fc-m" value="4" min="1" max="60" step="1" inputmode="numeric"></div>
<div class="field"><label for="fc-x">Plus</label><input type="number" id="fc-x" value="3" min="0" max="40" step="1" inputmode="numeric"></div></div>
<div class="field"><label for="fc-b">Border you'll add later, each side</label><select id="fc-b"><option value="0" selected>No border</option><option value="1">1 in</option><option value="2">2 in</option><option value="3">3 in</option></select></div>
<figure class="co-fig"><svg id="fc-svg" viewBox="0 0 320 190" role="img" aria-label="Foundation chain with the turning chain and first row"></svg><figcaption class="note" id="fc-cap">Your foundation chain.</figcaption>
<ul class="co-key"><li><i style="background:#b8326a"></i>Chains you work into</li><li><i style="background:#f4a823"></i>Skipped (turning) chains</li><li><i style="background:#2f8f8a"></i>First row</li></ul></figure>
</div>
<div class="result" aria-live="polite" id="fc-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How many chains for a crochet blanket?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Project</th>{"".join(f'<th scope="col">{e(n)}<br><span class="muted">{fc_g(wn, st):g} sts / 4 in</span></th>' for st, wn, n in FC_EXC)}</tr></thead><tbody>{fc_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Foundation chains worked out with the same maths as the calculator: typical single crochet gauge for each yarn weight (the middle of the Craft Yarn Council's crochet range), with half doubles a little and doubles about a tenth wider per stitch (our estimate). Single crochet starts in the 2nd chain from the hook, half double in the 3rd (chains not counted), double in the 4th (chains count as the first stitch). Your swatch will differ, so use the calculator with your own gauge. Blanket widths are from our <a href="{href("blanket-size-calculator.html")}">blanket size chart</a>.</p>
</div></section>
{AD.format("fc-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How do I work out my foundation chain?</h2>
<ol><li><strong>Crochet a swatch</strong> in the yarn, hook and stitch you'll use, at least 4 in (10 cm) wide, or about 6 in for a blanket.</li>
<li><strong>Count the stitches</strong> across 4 in and divide by 4 to get stitches per inch.</li>
<li><strong>Multiply by the width</strong> you want. 3 double crochets per inch × 36 in = 108 stitches.</li>
<li><strong>Add the turning chain</strong> for your stitch (see below), then round to your pattern's multiple if it has one.</li></ol>
<p>B.Hooked's method skips the maths: chain 10, measure them, and divide the width you want by that length. If 10 chains measure 2.5 in, a 40 in blanket needs 16 sets of 10, so 160 chains. Use the same yarn and hook as the project.</p>
<h2>How many extra chains for single, half double and double crochet?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Stitch (US, UK)</th><th scope="col">Turning chain</th><th scope="col">Common first row</th><th scope="col">Chain</th></tr></thead><tbody>
<tr><td><strong>Single crochet</strong> (UK double)</td><td>1</td><td>Sc in 2nd ch from hook</td><td>Stitches + 1</td></tr>
<tr><td><strong>Half double</strong> (UK half treble)</td><td>2</td><td>Hdc in 3rd ch from hook, chains not counted</td><td>Stitches + 2</td></tr>
<tr><td><strong>Double crochet</strong> (UK treble)</td><td>3</td><td>Dc in 4th ch from hook, chains count as 1st dc</td><td>Stitches + 2</td></tr>
<tr><td><strong>Double crochet</strong>, other style</td><td>2 or 3</td><td>Dc in 3rd ch from hook, chains not counted</td><td>Stitches + 2</td></tr>
<tr><td><strong>Treble</strong> (UK double treble)</td><td>4</td><td>Tr in 5th ch from hook, chains count as 1st tr</td><td>Stitches + 3</td></tr></tbody></table></div>
<p>The rule behind the table: chains = stitches + (the chain you start in − 1), minus 1 if the skipped chains count as a stitch. Your pattern's first row tells you which chain to start in, so set that in the calculator and it does the rest. The turning-chain heights (1 for sc up to 4 for treble) follow the usual standard; for taller stitches the turning chain almost always counts as a stitch, for single crochet it doesn't.</p>
<h2>What does "chain a multiple of 4 plus 3" mean?</h2>
<p>Chain any number you can make from 4 × something, then add 3. So 43, 47 and 51 all work, but 45 doesn't. The plus part already covers the turning chain and the edges, so don't add a turning chain on top. Pick "My pattern says chain a multiple of…" in the calculator and it rounds to the nearest number that fits.</p>
<h2>Why is my foundation chain too tight?</h2>
<p>Chains are narrower than the stitches worked into them, so a tight chain makes the bottom edge pull in and the piece flare as it grows. Loosen your tension on the chain, or make the chain with a hook one size larger than the pattern asks for and switch back for row 1. A slightly loose chain looks messy at first, but the first row takes up the slack.</p>
<div class="callout"><strong>Long chain? Chain a few extra.</strong> Counting 200 chains is where mistakes happen. Chain 5 to 10 more than you need and put a stitch marker every 20 or 25 chains. Unpick the spare chains from the tail once row 1 is done. Some crocheters skip the chain and use a foundation single crochet row, which makes the chain and the first row together and stays stretchy.</div>
<h2>How many rows will my blanket be?</h2>
<p>Divide the length you want by the height of one row. Measure it on your swatch: count the rows in 4 in and divide by 4. Taller stitches need fewer rows. In worsted yarn, single crochet is roughly 3 to 4 rows per inch, double crochet about 2 (our estimates, used by the calculator until you change the stitch). Count rows with the <a href="{href("row-counter.html")}">row counter</a>.</p>
<p>What next? See how much yarn it takes with the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a> or the <a href="{href("yarn-calculator.html")}">yarn calculator</a>, check the hook for your yarn on the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>, convert pattern terms with the <a href="{href("crochet-terms.html")}">US vs UK crochet terms</a> chart, and knitting the same piece? The <a href="{href("cast-on-calculator.html")}">cast on calculator</a> does the knit version. Not sure how long a scarf should be? See the <a href="{href("scarf-size-chart.html")}">scarf size chart</a>. Making a corner to corner blanket instead? Use the <a href="{href("c2c-blanket-calculator.html")}">C2C blanket calculator</a>.</p></div></section>'''
fc_faq = [
    ("How many chains do I need for a baby blanket?", f"For a 36 in baby blanket in worsted yarn, chain about {_fc_bb} for double crochet or about {fc_ch(36, 4, 'sc')} for single crochet. Bulky yarn needs about {fc_ch(36, 5, 'dc')} for double crochet. Swatch and check your own gauge."),
    ("How many chains do I need for a throw blanket?", f"A 50 in throw in worsted yarn needs about {_fc_th} chains for double crochet or {_fc_thsc} for single crochet. Multiply the width by your stitches per inch and add the turning chain."),
    ("How many chains for a crochet scarf?", f"An 8 in adult scarf in worsted single crochet needs about {_fc_sc} chains, or {fc_ch(8, 4, 'dc')} for double crochet. Children's scarves are about 6 in wide."),
    ("Do you add a turning chain to the foundation chain?", "Yes. Add 1 for single crochet, 2 for half double and 2 or 3 for double crochet, depending on whether the skipped chains count as the first stitch. If your pattern says chain a multiple plus a number, that number already includes it."),
    ("How do I calculate a foundation chain?", "Divide the stitches in a 4 in swatch by 4 to get stitches per inch, multiply by the width you want, then add the turning chain for your stitch and round to any multiple your pattern gives."),
    ("Why does my crochet get wider at the top?", "Usually the foundation chain is too tight, so the bottom edge pulls in. Chain more loosely or use a hook one size larger just for the chain."),
]
page("foundation-chain-calculator.html", "Foundation Chain Calculator: How Many Chains for a Crochet Blanket or Scarf? | Purl & Paper",
     "How many chains to start a crochet blanket, scarf or dishcloth: free foundation chain calculator for your gauge and stitch (sc, hdc, dc, tr), turning chains, pattern multiples, borders and rows to length.",
     fc, fc_faq, "Foundation chain calculator", app_name="Crochet foundation chain calculator")

# ---------------- JUNK JOURNAL SIGNATURE CALCULATOR ----------------
JS_PAPER = [("letter", "US Letter, 8.5 × 11 in", 11, 8.5), ("a4", "A4, 210 × 297 mm", 297 / 25.4, 210 / 25.4), ("legal", "US Legal, 8.5 × 14 in", 14, 8.5),
            ("tabloid", "Tabloid, 11 × 17 in", 17, 11), ("scrap12", "12 × 12 in scrapbook paper", 12, 12), ("halfletter", "Half letter, 5.5 × 8.5 in", 8.5, 5.5),
            ("a5", "A5, 148 × 210 mm", 210 / 25.4, 148 / 25.4)]   # (id, name, edge you fold across (becomes 2 page widths), other edge = page height)
JS_T = [("copy", "Printer or copy paper (80 gsm, 20 lb)", 0.1), ("heavy", "Heavier printer paper (100 to 120 gsm)", 0.13), ("mixed", "Mixed junk papers (old book pages, envelopes)", 0.16),
        ("card", "Light cardstock (65 lb, about 176 gsm)", 0.23), ("mm", "Mixed media or watercolour paper", 0.33)]   # sheet thickness in mm: our estimates
def js_holes(h): return 3 if h <= 6 else (5 if h <= 10 else 7)
def js_spine_mm(sheets, sigs, t, puff=1.0): return sheets * 2 * sigs * t * 1.15 * puff
js_popts = "".join(f'<option value="{i}|{a:.3f}|{b:.3f}"{" selected" if i == "letter" else ""}>{e(n)}, folds to {a / 2:.3g} × {b:.3g} in</option>' for i, n, a, b in JS_PAPER) + '<option value="custom">My own sheet size</option>'
js_topts = "".join(f'<option value="{t}"{" selected" if i == "copy" else ""}>{e(n)}</option>' for i, n, t in JS_T)
js_rows = "".join(f'<tr><td><strong>{s} sheets</strong><br><span class="muted">{s * 2} leaves</span></td><td>{s * 4}</td>' + "".join(f"<td>{s * 4 * g}</td>" for g in (3, 4, 5, 6)) + "</tr>" for s in (3, 4, 5, 6, 8, 10))
js_prow = "".join(f'<tr><td><strong>{e(n)}</strong></td><td>{a / 2:.3g} × {b:.3g} in<br><span class="muted">{a / 2 * 2.54:.1f} × {b * 2.54:.1f} cm</span></td><td>{js_holes(b)}</td><td>{b * 3 / 36:.2g} yd ({b * 3 * 2.54 / 100:.2g} m)</td></tr>' for i, n, a, b in JS_PAPER)
js = top("Junk journal signature calculator", "Pick your paper, how many sheets go in each signature and how many signatures you want. Get the page count, finished page size, how thick the spine will be, where to punch the sewing holes and how much thread to cut.", "Signature calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> every sheet you fold in half makes <strong>2 leaves and 4 pages</strong>. A signature of 5 sheets has 20 pages, and a journal of 4 such signatures has 80 pages. US Letter paper folded in half gives 5.5 × 8.5 in pages; A4 gives A5 pages. Most junk journalers use 4 to 8 sheets per signature, sewn with 3 or 5 holes and about 3 times the spine height of thread.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="js-paper">Paper you're folding</label><select id="js-paper">{js_popts}</select></div>
<div id="js-custom" hidden><div class="row2"><div class="field"><label for="js-a">Sheet width (the edge you fold across)</label><input type="number" id="js-a" value="11" min="2" max="40" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="js-bb">Sheet height (stays the same)</label><input type="number" id="js-bb" value="8.5" min="2" max="40" step="0.25" inputmode="decimal"></div></div>
<div class="field"><label for="js-u">Unit</label><select id="js-u"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><span class="label" id="js-mode-l">Plan by</span><div class="seg" role="group" aria-labelledby="js-mode-l" id="js-mode"><button type="button" data-v="sigs" aria-pressed="true">Number of signatures</button><button type="button" data-v="pages" aria-pressed="false">Pages I want</button></div></div>
<div class="row2"><div class="field"><label for="js-s">Sheets per signature</label><input type="number" id="js-s" value="5" min="1" max="20" step="1" inputmode="numeric"></div>
<div class="field" id="js-n-f"><label for="js-n">Signatures</label><input type="number" id="js-n" value="4" min="1" max="20" step="1" inputmode="numeric"></div>
<div class="field" id="js-p-f" hidden><label for="js-p">Pages I want</label><input type="number" id="js-p" value="80" min="4" max="800" step="4" inputmode="numeric"></div></div>
<div class="field"><label for="js-t">Paper type</label><select id="js-t">{js_topts}</select></div>
<div class="field"><label for="js-puff">Tuck-ins, pockets and ephemera added later</label><select id="js-puff"><option value="1">None, flat pages</option><option value="1.4" selected>Some (a few pockets and tucks)</option><option value="1.8">Lots (a chunky, stuffed journal)</option></select></div>
<figure class="co-fig"><svg id="js-svg" viewBox="0 0 320 210" role="img" aria-label="Open signature with sewing holes, and the signatures stacked at the spine"></svg><figcaption class="note" id="js-cap">Your journal.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="js-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How many pages in a junk journal signature?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Sheets per signature</th><th scope="col">Pages in one signature</th><th scope="col">3 signatures</th><th scope="col">4 signatures</th><th scope="col">5 signatures</th><th scope="col">6 signatures</th></tr></thead><tbody>{js_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Pages count both sides of every leaf: one folded sheet = 2 leaves = 4 pages. Add a cover and any tip-ins on top.</p>
<h2 style="margin-top:34px">What size will my pages be?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Sheet, folded in half</th><th scope="col">Page size</th><th scope="col">Sewing holes</th><th scope="col">Thread per signature</th></tr></thead><tbody>{js_prow}</tbody></table></div>
<p class="note" style="margin-top:12px">Page size is plain maths. Hole counts follow our rule of thumb (3 holes up to a 6 in spine, 5 up to 10 in, 7 above; bookbinding guides use an odd number, usually 3, 5 or 7). Thread is about 3 times the page height for a pamphlet stitch, as The Creative Folk suggests; cut a little more if you're new to it.</p>
</div></section>
{AD.format("js-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>What is a signature in a junk journal?</h2>
<p>A signature is a small stack of sheets folded in half together, so they nest inside each other and share one fold. You sew through the fold to hold them together. One signature makes a slim booklet; sew several into one cover and you have a thicker journal. Printers use the same word for the folded sections of a book.</p>
<h2>How many sheets should go in a signature?</h2>
<p>Most junk journals use 4 to 8 sheets per signature. A Coptic-bound travel journal tutorial we read uses 4 folded sheets per signature (16 pages); our <a href="{href("junk-journal-beginners.html")}">beginner's guide</a> suggests 5 to 8 sheets for a first project. Thin paper can take more; cardstock or thick found papers fewer. Too many sheets and the fold won't close flat, and the inner sheets stick out at the edge (trim them, or keep the uneven look).</p>
<h2>How many signatures does a junk journal need?</h2>
<p>There's no fixed number. A slim travel journal might have 1 or 2, a chunky "stuffed" journal 4 to 6. Remember that a junk journal grows: every pocket, tag and tuck-in adds thickness, so leave room in the spine. The calculator's ephemera setting adds that bulk to the spine estimate.</p>
<h2>How do I sew a signature with a pamphlet stitch?</h2>
<ol><li><strong>Mark the holes</strong> on a strip of scrap card folded like your signature: one in the centre of the fold and the rest evenly spaced, with the end holes about ½ to ¾ in from the top and bottom.</li>
<li><strong>Pierce the fold</strong> from the inside using the strip as a guide, with an awl or a thick needle. An old phone book or folded towel underneath helps.</li>
<li><strong>Cut the thread</strong> about 3 times the height of the spine.</li>
<li><strong>For 3 holes:</strong> go out through the centre from inside (leave a tail), in at the top hole, out at the bottom hole, then back in through the centre. Tie the two ends around the long stitch and trim.</li>
<li><strong>For 5 holes:</strong> work the same way, filling in the extra holes in a figure-of-eight and finishing back in the centre.</li></ol>
<div class="callout"><strong>Sewing into a cover?</strong> Punch matching holes in the cover's spine, one set for each signature, spaced a little apart so the signatures can sit side by side. Each signature then gets its own pamphlet stitch through the cover.</div>
<h2>How thick will my junk journal be?</h2>
<p>Each folded sheet adds two layers of paper at the spine. Printer paper is about 0.1 mm thick, so 4 signatures of 5 sheets come to roughly 4 to 5 mm before anything is added. Pockets, tags and ephemera can double that. The calculator gives an estimate with a range; measure a stack of your own paper for a closer number, and make the cover spine a little wider than you think.</p>
<h2>Which paper should I use for signatures?</h2>
<p>Printer paper folds cleanly and is easy to sew. Mix in old book pages, envelopes, kraft paper, graph paper and <a href="{href("how-to-tea-stain-paper.html")}">tea-stained pages</a> for the layered look. If a fold cracks or fights you, try folding the sheet the other way: paper folds more easily along its grain.</p>
<p>What next? Fill your pages with <a href="{href("junk-journal-ephemera-ideas.html")}">ephemera ideas</a>, get a prompt for each spread from the <a href="{href("journal-prompts.html")}">journal prompt generator</a>, age your paper with the <a href="{href("how-to-tea-stain-paper.html")}">tea staining guide</a>, or start from the beginning with <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a>.</p></div></section>'''
js_faq = [
    ("How many pages are in a signature?", "Each folded sheet makes 4 pages (2 leaves). A signature of 4 sheets has 16 pages, 5 sheets 20 pages and 8 sheets 32 pages."),
    ("How many sheets of paper should be in a junk journal signature?", "Most junk journals use 4 to 8 folded sheets per signature. Use fewer with thick paper or cardstock so the fold still closes flat."),
    ("How many signatures should a junk journal have?", "There is no set number: 1 or 2 for a slim travel journal, 4 to 6 for a chunky one. Leave room in the spine for the pockets and ephemera you'll add."),
    ("What size is a junk journal made from letter paper?", "US Letter (8.5 × 11 in) folded in half gives 5.5 × 8.5 in pages, the most common junk journal size. A4 folded in half gives A5 pages (about 5.8 × 8.3 in)."),
    ("How much thread do I need to sew a signature?", "For a pamphlet stitch, cut about 3 times the height of the spine. For an 8.5 in tall journal that's about 26 in (0.7 yd) per signature."),
    ("How many holes do I need to sew a signature?", "Use an odd number so you start and finish in the centre: 3 holes for small journals and 5 for most letter-size journals. Very tall journals can use 7."),
]
page("junk-journal-signature-calculator.html", "Junk Journal Signature Calculator: Pages, Sheets, Spine and Sewing Holes | Purl & Paper",
     "How many pages in a junk journal signature, how many sheets and signatures to use, page sizes for letter, A4 and 12x12 paper, spine thickness, sewing hole spacing and thread length: free junk journal signature calculator.",
     js, js_faq, "Signature calculator", app_name="Junk journal signature calculator")

# ---------------- ABOUT / PRIVACY / 404 ----------------
page("about.html", "About Purl & Paper", "About Purl & Paper, free tools for knitting, crochet and junk journaling.",
     top("About Purl &amp; Paper", "Free, simple tools for people who make things with yarn and paper.", "About") + '''<section style="padding-top:10px"><div class="narrow prose">
<p>Purl &amp; Paper started from a simple wish: a row counter that doesn't let the phone go to sleep, and a quick answer to "how much yarn do I need?". It grew into a small set of tools and charts for knitters, crocheters and junk journalers.</p>
<p>Everything is free to use and works in your browser. Your counters, projects and saved prompts stay on your own device. The site is supported by ads.</p>
<p>Yarn amounts and size conversions come from widely used industry standards and typical pattern amounts. They're estimates, so always check your pattern and your own swatch.</p>
<h2>Contact</h2><p>Spotted a mistake or have an idea for a tool? Email <a href="mailto:awaiskaramat@hotmail.com">awaiskaramat@hotmail.com</a>.</p></div></section>''', crumb="About")
page("privacy.html", "Privacy Policy | Purl & Paper", "How Purl & Paper handles your data.",
     top("Privacy policy", "Short version: your counters, projects and saved prompts never leave your device.", "Privacy") + f'''<section style="padding-top:10px"><div class="narrow prose">
<h2>Email list</h2><p>If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the free printables and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time.</p>
<h2>What we store</h2><p>The tools save your counters, projects and saved prompts in your browser's local storage on your device. We can't see them and they're not sent to us. Clearing your browser data removes them.</p>
<h2>Analytics</h2><p>We use Google Analytics to count visits and see which pages are useful. It uses cookies and collects information such as pages viewed, device type and approximate location. It doesn't tell us who you are.</p>
<h2>Advertising</h2><p>We show ads through Google AdSense. Google and its partners may use cookies to show ads based on your visits to this and other sites. You can turn off personalised ads in <a href="https://adssettings.google.com" rel="nofollow noopener">Google's ad settings</a>. More detail is in <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow noopener">how Google uses information from sites that use its services</a>.</p>
<h2>Changes</h2><p>We'll update this page if anything changes. Last updated {e(UPDATED)}.</p></div></section>''', crumb="Privacy")
page("404.html", "Page not found | Purl & Paper", "This page doesn't exist.",
     f'<section><div class="narrow" style="text-align:center"><h1>Dropped a stitch.</h1><p class="lead" style="margin-inline:auto">This page doesn\'t exist. It may have moved.</p><div class="btns" style="justify-content:center"><a class="btn gold" href="{href("index.html")}">Back to the home page</a><a class="btn ghost" href="{href("row-counter.html")}">Open the row counter</a></div></div></section>')

# ---------------- HOW TO CROCHET A MAGIC RING (guide + round 1 writer) ----------------
import math as _m
_Y, _Y2, _HK, _MG, _TL = "#b8326a", "#d97aa0", "#1f2a44", "#f4a823", "#2f8f8a"
def _sts(n, r, cx=110, cy=78, hi=None, col=_Y):
    o = ""
    for i in range(n):
        a = -_m.pi / 2 + 2 * _m.pi * i / n
        x, y = cx + r * _m.cos(a), cy + r * _m.sin(a)
        c = _TL if hi == i else col
        o += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="5.5" ry="9" transform="rotate({_m.degrees(a) + 90:.1f} {x:.1f} {y:.1f})" fill="#fbfcfa" stroke="{c}" stroke-width="3.2"/>'
    return o
def _hook(x, y, ang=-40, ln=90):
    a = _m.radians(ang); ex, ey = x + ln * _m.cos(a), y + ln * _m.sin(a)
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{_HK}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M{x:.1f} {y:.1f} q-7 3 -8 -5" fill="none" stroke="{_HK}" stroke-width="4" stroke-linecap="round"/>')
_LOOP = f'<path d="M168 150 C86 118 52 42 110 34 C168 42 134 118 52 150" fill="none" stroke="{_Y}" stroke-width="7" stroke-linecap="round"/><circle cx="40" cy="146" r="13" fill="{_Y}"/><path d="M31 140q9 6 18 0M30 150q10 -5 20 0" stroke="#fbfcfa" stroke-width="1.6" fill="none" opacity=".6"/>'
_LBL = lambda x, y, t, a="start": f'<text x="{x}" y="{y}" font-size="11" fill="#4a5470" text-anchor="{a}" font-family="Atkinson Hyperlegible, sans-serif">{t}</text>'
def _ring(r, tail_len=40, arrow=False):
    o = f'<circle cx="110" cy="78" r="{r}" fill="none" stroke="{_Y}" stroke-width="5"/><circle cx="110" cy="78" r="{r + 4}" fill="none" stroke="{_Y2}" stroke-width="3"/>'
    o += f'<path d="M{110 + r * .5:.1f} {78 + r * .87:.1f} q10 {tail_len * .6:.0f} 22 {tail_len:.0f}" fill="none" stroke="{_Y2}" stroke-width="4" stroke-linecap="round"/>'
    if arrow:
        o += f'<path d="M{142 + r * .5:.1f} {92 + r * .87:.1f} l9 21 M{145 + r * .5:.1f} {115 + r * .87:.1f} l6 -2 l-1 -7" fill="none" stroke="{_MG}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
    return o
MR_STEPS = [
    ("Make a loop", "Lay the yarn in a loop so the tail end crosses over the working yarn (the strand from the ball). Pinch the cross, or wrap it round two fingers.",
     _LOOP + _LBL(176, 150, "tail") + _LBL(12, 122, "working yarn")),
    ("Pull up a loop", "Put the hook through the middle of the ring, catch the working yarn (not the tail) and pull a loop back through.",
     _LOOP + _hook(112, 86, -45, 95) + f'<ellipse cx="112" cy="80" rx="7" ry="11" fill="none" stroke="{_Y}" stroke-width="4"/>' + _LBL(176, 150, "tail")),
    ("Chain 1", "Yarn over and pull through the loop on the hook. This chain holds the ring shut while you work. It doesn't count as a stitch (ch 2 for hdc, ch 3 for dc).",
     _ring(34) + f'<ellipse cx="110" cy="36" rx="6" ry="10" fill="#fbfcfa" stroke="{_Y}" stroke-width="3.5"/>' + _hook(112, 22, -30, 85) + _LBL(16, 30, "ch 1")),
    ("Work stitches into the ring", "Put the hook through the centre, under the ring and the tail together, and make your stitches. Six single crochet is the usual start.",
     _ring(34) + _sts(6, 46) + _hook(152, 50, -40, 70) + _LBL(16, 150, "under the ring and the tail")),
    ("Pull the tail to close", "Hold the stitches and pull the tail firmly. The ring shrinks until the hole closes. Pull again after round 2 if it opens a little.",
     _ring(7, 52, True) + _sts(6, 22) + _LBL(16, 150, "pull the tail")),
    ("Join, or keep going in a spiral", "Slip stitch into the first stitch to join, or skip the join and work round 2 straight into the first stitch, with a marker in it.",
     _ring(7, 40) + _sts(6, 22, hi=0) + f'<path d="M110 30 l-5 -10 l10 0 z" fill="{_TL}"/>' + _LBL(120, 24, "marker in stitch 1")),
]
def mr_fig(i, s):
    return (f'<figure class="mr-step"><svg viewBox="0 0 220 160" role="img" aria-label="Step {i}: {e(s[0])}">{s[2]}</svg>'
            f'<figcaption><strong>{i}. {e(s[0])}</strong> {e(s[1])}</figcaption></figure>')
mr_steps_html = "".join(mr_fig(i + 1, s) for i, s in enumerate(MR_STEPS))
MR_TAB = [("Single crochet (sc)", "ch 1", "No", "6", "6, 12, 18, 24"), ("Half double crochet (hdc)", "ch 2", "Usually no", "8", "8, 16, 24, 32"),
          ("Double crochet (dc)", "ch 3", "Varies: check the pattern", "10 or 12", "12, 24, 36, 48"), ("Amigurumi (sc, worked tight)", "ch 1", "No", "6", "6, 12, 18 (spiral, no joins)")]
mr = top("How to crochet a magic ring", "The magic ring (or magic circle) starts a round without a hole in the middle. Here it is in six drawings, with a helper that writes your first rounds for you.", "How to crochet a magic ring") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> make a loop with the tail crossing over the working yarn, put the hook through, pull up a loop of the working yarn and <strong>chain 1</strong> (it doesn't count). Work <strong>6 single crochet</strong> into the ring, going under both the ring and the tail, then <strong>pull the tail</strong> to close the hole. Join with a slip stitch to the first stitch, or keep going in a spiral. For half double crochet start with ch 2 and 8 hdc; for double crochet, ch 3 and 10 to 12 dc.</div>
<div class="mr-steps">{mr_steps_html}</div>
<p class="note">New to the stitches themselves? Start with <a href="{href("basic-crochet-stitches.html")}">basic crochet stitches</a>. Our own drawings, shown for right-handed crochet. Left-handed? It's the same steps mirrored: the tail sits on the other side.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Write my first rounds</h2>
<div class="field"><label>First round stitch</label><div class="seg" id="mr-st" role="group" aria-label="Stitch"><button type="button" data-v="sc" aria-pressed="true">sc</button><button type="button" data-v="hdc" aria-pressed="false">hdc</button><button type="button" data-v="dc" aria-pressed="false">dc</button></div></div>
<div class="field"><label for="mr-n">Stitches in the ring</label><input id="mr-n" type="number" min="3" max="16" value="6" inputmode="numeric"></div>
<div class="field"><label>Rounds</label><div class="seg" id="mr-join" role="group" aria-label="Rounds"><button type="button" data-v="join" aria-pressed="true">Joined</button><button type="button" data-v="spiral" aria-pressed="false">Spiral (amigurumi)</button></div></div>
<div class="field"><label for="mr-r">How many rounds to write</label><select id="mr-r"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6</option></select></div>
<div class="field" id="mr-cnt-f"><label><input type="checkbox" id="mr-cnt"> The starting chain counts as a stitch</label></div>
<figure class="ts-fig"><svg id="mr-svg" viewBox="0 0 220 220" role="img" aria-label="Your rounds seen from above"></svg><figcaption class="note" id="mr-cap"></figcaption></figure>
</div>
<div class="result" aria-live="polite" id="mr-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>How many stitches go in a magic ring?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">First round</th><th scope="col">Start with</th><th scope="col">Chain counts as a stitch?</th><th scope="col">Stitches in the ring</th><th scope="col">Flat circle counts, rounds 1 to 4</th></tr></thead><tbody>
{"".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{x}</td></tr>" for a, b, c, d, x in MR_TAB)}</tbody></table></div>
<p class="note">Common starting counts from Sarah Maker, Love Life Yarn and B.Hooked. Patterns vary from about 3 to 12 or more stitches, so follow yours. To keep a circle flat, add the first round's count again every round; the <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a> writes every round out to the size you want.</p>
<h2>Which strand do I pull to close a magic ring?</h2>
<p>The <strong>tail</strong>: the short end you started with. The working yarn runs to the ball. If you pull and nothing moves, you're pulling the working yarn, or your stitches went over the ring but not over the tail. Every stitch in round 1 has to go under both strands, or the tail can't slide.</p>
<h2>Why won't my magic ring close?</h2>
<ul><li><strong>The tail wasn't worked over.</strong> Look at the back: the tail should disappear inside the stitches all the way round.</li>
<li><strong>The stitches are gripping the tail.</strong> Hold round 1 a little looser, or pull the tail a bit before you finish the round so it's already sliding.</li>
<li><strong>Fuzzy or sticky yarn.</strong> Chenille, velvet and mohair can grab or snap. Make round 1 loose, or make the ring in a smooth cotton and change yarn after it.</li>
<li><strong>Too many stitches.</strong> A ring of 12 or more tall stitches can't fully close. A small hole is normal for a dc ring.</li></ul>
<h2>How do I stop a magic ring coming undone?</h2>
<p>Leave a tail of at least 6 in (15 cm). When the piece is done, thread the tail on a yarn needle, pull the ring closed once more, and weave the tail in round the back of round 1, then back the other way through a few stitches so it can't slide out. Don't trim it short until the end. A knot isn't needed, and it can make a lump on the right side.</p>
<h2>What's the difference between a magic ring and a magic circle?</h2>
<p>None: magic ring, magic circle, magic loop and adjustable ring are all names for the same start. A <strong>double magic ring</strong> is the same idea with the yarn wrapped twice, so there are two strands to work over. It's even more secure, and closing it takes two pulls, one for each strand.</p>
<h2>What can I use instead of a magic ring?</h2>
<ul><li><strong>Chain 2,</strong> then work your first round into the 2nd chain from the hook. Easy, though it leaves a small hole and can't be tightened later.</li>
<li><strong>Chain 4 and join</strong> with a slip stitch to make a ring, then work into the ring. This leaves a clear hole, which is fine for granny squares and mandalas.</li></ul>
<h2>Joined rounds or a spiral?</h2>
<p><strong>Joined</strong> rounds end with a slip stitch into the first stitch and start with a chain. They make a neat line of joins and stripes that stay straight: good for coasters, hats and granny circles. <strong>Spiral</strong> rounds just keep going, so there's no seam, which is why amigurumi patterns use them. Put a stitch marker in the first stitch of every round so you don't lose count, and keep count with our <a href="{href("row-counter.html")}">row counter</a>.</p>
<p>What next? Plan a flat circle or amigurumi ball with the <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a>, close it up with our guide to <a href="{href("how-to-crochet-decrease.html")}">decreasing in crochet</a>, learn <a href="{href("how-to-change-colors-in-crochet.html")}">how to change colours in crochet</a> for a striped circle, and check a pattern's stitch names on the <a href="{href("crochet-terms.html")}">US vs UK crochet terms</a> chart. Done? Hide the tails with our guide to <a href="{href("how-to-weave-in-ends.html")}">fastening off and weaving in ends</a>.</p></div></section>'''
mr_faq = [
    ("How do you crochet a magic ring?", "Make a loop with the tail crossing over the working yarn, put the hook through, pull up a loop of the working yarn and chain 1. Work your stitches into the ring, under both the ring and the tail, then pull the tail to close the hole."),
    ("How many stitches go in a magic ring?", "Usually 6 single crochet. Half double crochet rings often start with 8, and double crochet with 10 to 12. Your pattern may say otherwise, so follow it."),
    ("Does the chain 1 count as a stitch in a magic ring?", "No. The ch 1 for single crochet just holds the ring. For taller stitches, some patterns count the ch 3 as the first double crochet and some don't, so check yours."),
    ("Which end do you pull to close a magic ring?", "The tail, the short end you started with. If it won't move, your stitches didn't go over the tail, or you're pulling the working yarn."),
    ("Why does my magic ring keep coming open?", "The tail wasn't woven in firmly. Pull the ring tight again, then weave the tail in round the back of round 1 and back the other way so it can't slide out."),
    ("Is a magic circle the same as a magic ring?", "Yes. Magic ring, magic circle, magic loop and adjustable ring are different names for the same start."),
]
page("how-to-crochet-magic-ring.html", "How to Crochet a Magic Ring (Step by Step + Round 1 Writer) | Purl & Paper",
     "How to crochet a magic ring (magic circle) in 6 simple drawings: which strand to pull, how many stitches go in, why it won't close and how to stop it undoing. With a helper that writes your first rounds.",
     mr, mr_faq, "How to crochet a magic ring", app_name="Magic ring round writer")

# ---------------- HOW TO CHANGE COLORS IN CROCHET (guide + stripe planner) ----------------
def _cc_stitch(top_col, low_col, label):
    return (f'<svg viewBox="0 0 220 150" role="img" aria-label="{e(label)}">'
            f'<rect x="20" y="104" width="180" height="20" rx="6" fill="{low_col}" opacity=".9"/>'
            f'<path d="M70 104 L70 58" stroke="{low_col}" stroke-width="7" stroke-linecap="round"/>'
            f'<ellipse cx="96" cy="50" rx="9" ry="13" fill="none" stroke="{low_col}" stroke-width="5"/>'
            f'<ellipse cx="122" cy="50" rx="9" ry="13" fill="none" stroke="{low_col}" stroke-width="5"/>'
            f'<path d="M190 34 C160 30 150 48 132 50" fill="none" stroke="{top_col}" stroke-width="7" stroke-linecap="round"/>'
            + _hook(86, 50, -15, 120) +
            f'<path d="M70 58 C60 40 40 30 22 34" fill="none" stroke="{low_col}" stroke-width="5" stroke-dasharray="2 7" stroke-linecap="round"/>'
            + _LBL(204, 72, "new colour", "end") + _LBL(18, 26, "old colour drops") + _LBL(110, 142, "2 loops left on the hook", "middle") + "</svg>")
CC_COLS = ("#f2e6cf", "#b8326a", "#2f8f8a", "#f4a823", "#1f2a44", "#c9a37a")
def _cc_side():
    o = '<svg viewBox="0 0 220 150" role="img" aria-label="Stripes of two rows with the unused colour carried up the side">'
    for i in range(6):
        c = CC_COLS[0] if (i // 2) % 2 == 0 else CC_COLS[1]
        o += f'<rect x="40" y="{124 - i * 18}" width="150" height="15" rx="4" fill="{c}" stroke="rgba(31,42,68,.18)"/>'
    o += f'<path d="M36 128 C30 118 30 100 36 92" fill="none" stroke="{CC_COLS[1]}" stroke-width="3.5"/><path d="M36 92 C30 82 30 64 36 56" fill="none" stroke="#d8c7a4" stroke-width="3.5"/><path d="M36 56 C30 46 30 28 36 20" fill="none" stroke="{CC_COLS[1]}" stroke-width="3.5"/>'
    return o + _LBL(200, 30, "2-row stripes", "end") + _LBL(14, 146, "unused colour carried up this edge") + "</svg>"
def _cc_round():
    o = '<svg viewBox="0 0 220 150" role="img" aria-label="Rounds joined with a slip stitch, new colour starting at the join">'
    for r, c in ((60, CC_COLS[2]), (44, CC_COLS[0]), (28, CC_COLS[1])):
        o += f'<circle cx="100" cy="75" r="{r}" fill="none" stroke="{c}" stroke-width="13"/>'
    o += f'<line x1="100" y1="6" x2="100" y2="58" stroke="{_HK}" stroke-width="2" stroke-dasharray="3 4"/><circle cx="100" cy="15" r="5" fill="{_MG}"/>'
    return o + _LBL(100, 148, "every join lines up at the top", "middle") + "</svg>"
CC_HOW = [("Single crochet", "Insert, yarn over, pull up a loop (2 loops on the hook). Drop the old colour, then finish the stitch: yarn over with the new colour and pull through both loops."),
          ("Half double crochet", "Yarn over, insert, yarn over, pull up a loop (3 loops on the hook). Drop the old colour and pull the new colour through all 3 loops."),
          ("Double crochet", "Work the stitch until 2 loops are left on the hook. Drop the old colour and pull the new colour through those last 2."),
          ("Treble crochet", "Work until the last 2 loops, then finish with the new colour, the same as double crochet."),
          ("Slip stitch join (rounds)", "Insert into the first stitch of the round, then pull the new colour through the stitch and the loop on the hook.")]
cc = top("How to change colours in crochet", "Change colour on the last yarn over of the stitch before, and the new colour starts clean. Here's how for every stitch, at the end of a row, mid-row and in rounds, plus a stripe planner that tells you when to carry the yarn and when to cut.", "How to change colours in crochet") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> work the last stitch in the old colour until <strong>2 loops are left on the hook</strong> (3 for half double). Drop the old colour, <strong>yarn over with the new colour and pull through</strong> to finish the stitch. At the end of a row, do this on the last stitch, then chain and turn. Leave both tails about <strong>6 in (15 cm)</strong> long and weave them in later. For stripes of an even number of rows, you don't need to cut: carry the unused colour up the side.</div>
<div class="cc-figs">
<figure class="mr-step">{_cc_stitch("#2f8f8a", "#b8326a", "Finishing a stitch with the new colour")}<figcaption><strong>Change on the last yarn over.</strong> The stitch before the new colour is finished with it, so the next stitch starts in the new colour, with no little loop of the old one on top.</figcaption></figure>
<figure class="mr-step">{_cc_side()}<figcaption><strong>Carry it up the side.</strong> With stripes of 2, 4 or 6 rows, the colour you dropped is waiting at the same edge when you need it again. Just pick it up: no cutting.</figcaption></figure>
<figure class="mr-step">{_cc_round()}<figcaption><strong>In rounds, change at the join.</strong> Join with a slip stitch in the new colour, so every colour change sits on the same line at the back.</figcaption></figure></div>
<p class="note">Our own drawings.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Stripe planner: carry or cut?</h2>
<div class="field"><label>Worked in</label><div class="seg" id="cc-mode" role="group" aria-label="Worked in"><button type="button" data-v="rows" aria-pressed="true">Rows (turning)</button><button type="button" data-v="rounds" aria-pressed="false">Joined rounds</button></div></div>
<div id="cc-list" class="cc-list" aria-label="Stripes, bottom to top"></div>
<div class="toolbar"><button type="button" class="btn ghost" id="cc-add">Add a stripe</button><span class="spacer"></span><label for="cc-rep" class="muted">Repeat</label><select id="cc-rep">{"".join(f'<option value="{i}"{" selected" if i == 3 else ""}>{i}×</option>' for i in range(1, 11))}</select></div>
<figure class="ts-fig"><svg id="cc-svg" viewBox="0 0 260 300" role="img" aria-label="Your stripes, with carried yarn on the edges"></svg><figcaption class="note">Dots: a colour joined. Lines on the edges: yarn carried up, not cut.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="cc-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>How do I change colour for each stitch?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Stitch</th><th scope="col">When to bring in the new colour</th></tr></thead><tbody>
{"".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td></tr>" for a, b in CC_HOW)}</tbody></table></div>
<p class="note">The last-yarn-over method is the standard one in most patterns (Crochet Spot, ChristaCo Design, MJ's Off The Hook Designs). Stitch names are US terms; in UK terms sc is dc and dc is tr. See <a href="{href("crochet-terms.html")}">US vs UK crochet terms</a>.</p>
<h2>How do I change colour at the end of a row?</h2>
<ol><li>Work to the <strong>last stitch</strong> of the row in the old colour.</li>
<li>Stop with the last 2 loops on the hook (3 for hdc).</li>
<li>Drop the old colour to the back and finish the stitch with the new colour.</li>
<li>Chain for your turning chain in the new colour, turn, and carry on.</li></ol>
<p>Changing in the turning chain instead leaves a loop of the old colour on the edge, which shows. To stop the first stitches coming loose, give both tails a gentle tug, or work the first few stitches over the new tail.</p>
<h2>How do I change colour in the middle of a row?</h2>
<p>The same way: finish the stitch <em>before</em> the new colour with the new colour. If you'll need the old colour again a few stitches later, don't cut it. Lay it along the tops of the stitches you're working into and crochet over it, so it travels with you, hidden inside the stitches (this is tapestry crochet). Keep the carried strand just snug enough to lie flat: too tight and the fabric puckers, too loose and loops catch. For a big block of colour, use a separate small ball or bobbin for each area instead.</p>
<h2>How do I change colour in rounds?</h2>
<p>In <strong>joined</strong> rounds, finish the round in the old colour, then make the slip stitch join with the new colour: insert into the first stitch, pull the new colour through the stitch and the loop on the hook, and chain up. All your changes then line up at one spot, which you can keep at the back. In <strong>spiral</strong> rounds (amigurumi) there's no join, so the stripe always ends with a small step, called a jog. To soften it, change colour on the last yarn over, then work a slip stitch or a shorter stitch at the start of the new colour.</p>
<h2>How do I change colours without cutting the yarn?</h2>
<ul><li><strong>Carry up the side</strong> for stripes in rows. It works when each stripe is an <strong>even number of rows</strong>: 2, 4 or 6. Then the dropped colour is at the same edge when you need it again. With odd-row stripes, the colour ends up at the wrong edge.</li>
<li><strong>Trap the strand.</strong> When you pick a colour up, work your turning chain or first stitch over the carried strand so it doesn't make a big loop at the edge. A border later covers it completely.</li>
<li><strong>Carry along the row</strong> (tapestry crochet) for colour changes inside the row.</li>
<li><strong>Carry behind the join</strong> in joined rounds.</li></ul>
<p>Carry long gaps loosely. Over many rows a carried strand can pull the edge in or show through pale colours, so for a long gap between uses it's often neater to cut and rejoin. As a rule of thumb we cut once a colour would be carried more than about 8 rows (our estimate, about 3 in of edge); the planner above uses that.</p>
<h2>Should I knot the yarn when changing colours?</h2>
<p>You don't need to. A well woven-in tail holds better than a knot, and knots can work loose or poke through on the right side. Some crocheters tie the two tails together loosely to stop the first stitch slipping while they work, then untie it before weaving in. Or use a Russian join to join yarn of the same kind with no ends to weave.</p>
<h2>How do I weave in the ends?</h2>
<p>Our full guide to <a href="{href("how-to-weave-in-ends.html")}">weaving in ends</a> covers slippery and chunky yarn, amigurumi and the invisible fasten off. In short: leave about 6 in (15 cm). Thread the tail on a blunt yarn needle and weave it through the back of stitches of the <strong>same colour</strong>, so it doesn't show. Go one way for an inch or two, then turn and go back a short way through different stitches, and trim close. To save time, crochet over the tails as you go: hold them along the top of the row and work the next few stitches over them.</p>
<p>Want the stripes picked for you? The <a href="{href("stripe-generator.html")}">random stripe generator</a> makes a random, Fibonacci or even stripe pattern from your colours and prints the row list.</p>
<p>What next? Plan a striped temperature blanket with the <a href="{href("temperature-blanket-planner.html")}">temperature blanket planner</a>, start the right number of chains with the <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a>, or start a striped circle with a <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>. Using up scraps? Weigh them in the <a href="{href("yarn-yardage-calculator.html")}">yarn yardage calculator</a> first.</p></div></section>'''
cc_faq = [
    ("How do you change colours in crochet?", "Work the last stitch before the change in the old colour until 2 loops are left on the hook, drop the old colour, then yarn over with the new colour and pull through to finish the stitch."),
    ("Do you change colour before or after the turning chain?", "Before. Change on the last yarn over of the last stitch of the row, then make the turning chain in the new colour."),
    ("How do you change colours in crochet without cutting the yarn?", "For stripes with an even number of rows, carry the unused colour up the side of the work and pick it up when you need it. Inside a row, crochet over the unused colour so it travels inside the stitches."),
    ("Should I tie a knot when changing yarn colours?", "It isn't needed. Weaving the ends in well holds better and doesn't make a lump. If you tie the tails to hold them while you work, untie them before weaving in."),
    ("How long should the tail be when changing colours?", "About 6 in (15 cm) is plenty to weave in with a yarn needle."),
    ("How do you change colour in a spiral round?", "Change on the last yarn over of the last stitch, as usual. Spirals always leave a small jog at the change; a slip stitch or shorter stitch at the start of the new colour softens it."),
]
page("how-to-change-colors-in-crochet.html", "How to Change Colors in Crochet (Without Cutting) + Stripe Planner | Purl & Paper",
     "How to change colours in crochet: the last yarn over method for sc, hdc and dc, at the end of a row, mid-row and in rounds; carrying yarn up the side without cutting; knots and tails. With a stripe planner.",
     cc, cc_faq, "How to change colours in crochet", app_name="Crochet stripe planner")

# ---------------- HOW TO BIND OFF KNITTING (guide + bind off chooser) ----------------
_ND = "#c9a37a"
def _needle(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{_ND}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="1.5" stroke-linecap="round" opacity=".5"/>')
def _kst(x, y, col=_Y, w=3.2):
    return f'<path d="M{x - 8} {y - 12} Q{x} {y + 2} {x} {y + 12} M{x + 8} {y - 12} Q{x} {y + 2} {x} {y + 12}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
def _bo_fabric(n_done):
    o = '<rect x="20" y="98" width="180" height="40" rx="6" fill="#f2e6cf"/>'
    for r in range(2):
        for i in range(9):
            o += _kst(32 + i * 20, 108 + r * 18, "#d97aa0", 2.4)
    for i in range(n_done):   # finished bound-off chain along the top
        cx = 32 + i * 20
        o += f'<ellipse cx="{cx + 10}" cy="92" rx="11" ry="5" fill="none" stroke="{_Y}" stroke-width="3"/>'
    return o
def bo_fig(i):
    if i == 1:
        body = (_bo_fabric(0) + _needle(10, 74, 120, 74) + _needle(120, 70, 210, 40)
                + f'<ellipse cx="120" cy="74" rx="7" ry="12" fill="none" stroke="{_Y}" stroke-width="3.2"/><ellipse cx="98" cy="74" rx="7" ry="12" fill="none" stroke="{_TL}" stroke-width="3.2"/>'
                + _LBL(22, 22, "2 stitches on the right needle") + _LBL(22, 64, "right needle"))
        cap = ("<strong>Knit 2 stitches.</strong>", "Knit the first two stitches as normal. They sit on the right needle. If your bind offs come out tight, hold a needle 1 or 2 sizes larger in your right hand.")
    elif i == 2:
        body = (_bo_fabric(0) + _needle(20, 74, 140, 74) + _needle(130, 66, 210, 30)
                + f'<ellipse cx="118" cy="74" rx="7" ry="12" fill="none" stroke="{_Y}" stroke-width="3.2"/>'
                + f'<path d="M96 76 C96 46 120 40 122 60" fill="none" stroke="{_TL}" stroke-width="3.2"/><path d="M114 52 l9 9 l3 -12" fill="none" stroke="{_HK}" stroke-width="2.4" stroke-linecap="round"/>'
                + _LBL(22, 22, "lift the first stitch over the second") + _LBL(110, 148, "and off the needle", "middle"))
        cap = ("<strong>Lift the first over.</strong>", "Put the left needle into the first (right-hand) stitch, lift it over the second stitch and off. One stitch bound off, one left on the right needle.")
    elif i == 3:
        body = (_bo_fabric(4) + _needle(20, 74, 130, 74) + _needle(130, 70, 210, 40)
                + f'<ellipse cx="114" cy="74" rx="7" ry="12" fill="none" stroke="{_TL}" stroke-width="3.2"/>'
                + _LBL(22, 22, "knit 1, lift over, again and again") + _LBL(110, 148, "a neat chain grows along the top", "middle"))
        cap = ("<strong>Knit 1, lift over. Repeat.</strong>", "Knit one more stitch so there are two on the right needle again, and lift the first over. Keep going until one stitch is left. Bind off loosely: the edge should stretch as much as the fabric.")
    else:
        body = (_bo_fabric(9) + f'<ellipse cx="196" cy="74" rx="9" ry="16" fill="none" stroke="{_Y}" stroke-width="3.2"/>'
                + f'<path d="M196 90 C206 110 214 130 214 146" fill="none" stroke="{_Y}" stroke-width="3.2"/><path d="M188 58 C160 40 120 40 60 50" fill="none" stroke="{_Y}" stroke-width="3.2" stroke-dasharray="2 6" stroke-linecap="round"/>'
                + f'<path d="M182 46 l-4 8 M190 44 l-2 8" stroke="{_HK}" stroke-width="2"/>'
                + _LBL(22, 22, "cut, leave 8 in (20 cm), pull through") + _LBL(110, 148, "tug the tail to close the loop", "middle"))
        cap = ("<strong>Pull the tail through.</strong>", "Cut the yarn, leaving about 8 in (20 cm). Pull the last loop big, take it off the needle and pull the tail right through it. Tug to close, then weave the tail in.")
    return (f'<figure class="mr-step"><svg viewBox="0 0 220 160" role="img" aria-label="Bind off step {i}">{body}</svg>'
            f'<figcaption>{cap[0]}{cap[1]}</figcaption></figure>')

BO_METHODS = [  # name, stretch 1-3, best for, how it works
    ("Basic (standard) bind off", 1, "Scarves, blankets, dishcloths, buttonbands and edges you'll sew into a seam", "Knit 2, lift the first over the second; knit 1, lift over; repeat. Firm, with little stretch."),
    ("Bind off in pattern", 2, "Ribbing: hat brims, cuffs and collars worked last", "The same lift-over, but knit the knit stitches and purl the purl stitches, so the edge follows the rib."),
    ("Jeny's surprisingly stretchy bind off", 3, "Toe-up sock cuffs, top-down sleeve cuffs, hems and necklines", "Wrap a yarn over before each stitch (the other way round before a purl), work the stitch, then lift the yarn over and the old stitch over it."),
    ("Long-tail bind off", 2, "Garter and stockinette edges you want to match a long-tail cast on", "Worked with a long tail, about 4 times the edge, so it mirrors the long-tail cast on."),
    ("Sewn bind off (Elizabeth Zimmermann)", 2, "Garter stitch edges and anything that needs a soft, neat edge", "Worked with a tapestry needle and a tail 3 to 4 times the edge: through two stitches purlwise, back through the first knitwise, drop it."),
    ("Tubular bind off", 3, "1×1 rib on sock cuffs, necklines and brims", "A sewn bind off that runs the yarn round the knit and purl stitches like a tube. Very stretchy and almost invisible."),
    ("Three-needle bind off", 1, "Shoulder seams and joining two sets of live stitches", "Hold both needles together, knit one stitch from each, then bind off as normal. Joins and binds off in one go."),
]
BO_NEEDLE = [("A little tight", "Use a right needle 1 size larger"), ("Very tight, won't stretch to the fabric's width", "Use a right needle 2 sizes larger, or a stretchy bind off"), ("Ribbed edge", "Bind off in pattern with the working needle or 1 size larger"), ("Lace to be blocked hard", "Needle at least 2 sizes larger, or Jeny's stretchy")]
def _bo_dots(n): return "".join("●" if k < n else "○" for k in range(3))
bo = top("How to bind off knitting", "Binding off (casting off in the UK) closes the last row so it can't unravel. Here's the basic bind off in four drawings, how to keep it loose, which stretchy bind off to use for cuffs, socks and necklines, and a chooser that tells you how much yarn to keep.", "How to bind off knitting") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> <strong>knit 2 stitches, lift the first over the second</strong> and off the needle. Then <strong>knit 1 more and lift over again</strong>; repeat until 1 stitch is left. Cut the yarn leaving about <strong>8 in (20 cm)</strong>, pull it through the last loop and tug. For ribbing, knit the knits and purl the purls as you bind off. If the edge is tight, use a needle <strong>1 or 2 sizes larger</strong> in your right hand.</div>
<div class="mr-steps">{"".join(bo_fig(i) for i in range(1, 5))}</div>
<p class="note">Our own drawings. "Bind off" (US) and "cast off" (UK) are the same thing.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Bind off chooser</h2>
<div class="field"><label for="bo-edge">What are you binding off?</label><select id="bo-edge">
<option value="scarf" selected>Scarf, blanket or dishcloth end</option><option value="rib">Ribbed hat brim, cuff or collar</option><option value="neck">Sweater neckline, sleeve cuff or hem (top down)</option><option value="sock">Toe-up sock cuff</option><option value="rib11">1×1 rib that must stretch and look invisible</option><option value="shawl">Lace shawl that will be blocked</option><option value="garter">Garter edge to match a long-tail cast on</option><option value="seam">Shoulder seam (two pieces of live stitches)</option></select></div>
<div class="field"><label>Worked</label><div class="seg" id="bo-way" role="group" aria-label="Worked"><button type="button" data-v="flat" aria-pressed="true">Flat (rows)</button><button type="button" data-v="round" aria-pressed="false">In the round</button></div></div>
<div class="row2"><div class="field"><label for="bo-w">Edge width (or round all the way)</label><input id="bo-w" type="number" min="1" max="400" step="any" value="8" inputmode="decimal"></div><div class="field"><label for="bo-u">Unit</label><select id="bo-u"><option value="in" selected>inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><label for="bo-n">Stitches on the needle</label><input id="bo-n" type="number" min="2" max="2000" step="1" value="36" inputmode="numeric"></div>
<figure class="ts-fig"><svg id="bo-svg" viewBox="0 0 300 140" role="img" aria-label="The edge and the yarn the bind off needs, to scale"></svg><figcaption class="note">Top bar: your edge. Below: the yarn to keep, folded to the edge's width.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="bo-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>Which bind off should I use?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Bind off</th><th scope="col">Stretch</th><th scope="col">Best for</th><th scope="col">How it works</th></tr></thead><tbody>
{"".join(f'<tr><td><strong>{a}</strong></td><td aria-label="{s} of 3">{_bo_dots(s)}</td><td>{b}</td><td>{c}</td></tr>' for a, s, b, c in BO_METHODS)}</tbody></table></div>
<p class="note">Uses from Wikipedia's binding off article, Purl Soho's long-tail and Elizabeth Zimmermann bind off tutorials and Cocoknits' guide to Jeny's stretchy bind off. Stretch dots are our rough comparison.</p>
<h2>How do I bind off in rib (bind off in pattern)?</h2>
<p>Work each stitch the way it looks: knit the knit stitches, purl the purl stitches, and lift the first stitch over the second after each one, just as in the basic bind off. Before a purl stitch the yarn goes to the front; bring it to the back for the next knit. The edge then follows the slope of the rib instead of pulling it in. Use your working needle or one size larger.</p>
<h2>Why is my bind off so tight, and how do I fix it?</h2>
<ul><li><strong>Go up a needle size</strong> for the bind-off row only: hold a needle 1 or 2 sizes larger in your right hand (Wikipedia suggests at least 2 sizes larger for a loose edge).</li>
<li><strong>Don't tug</strong> each stitch after lifting it over. Let the loop sit at the needle's full width.</li>
<li><strong>Check it stretches</strong> as far as the fabric below. If it doesn't, rip back the bind-off row (just one row) and try again.</li>
<li><strong>Switch to a stretchy bind off</strong> for cuffs, sock tops and necklines: Jeny's surprisingly stretchy or a tubular bind off.</li></ul>
<div class="tbl-wrap"><table><thead><tr><th scope="col">If your edge is…</th><th scope="col">Try</th></tr></thead><tbody>{"".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in BO_NEEDLE)}</tbody></table></div>
<h2>How long a tail should I leave after binding off?</h2>
<p>About <strong>6 to 8 in (15 to 20 cm)</strong> to weave in (Purl Soho says at least 8 in). Leave more if you'll sew a seam with it: roughly the length of the seam plus 8 in is a handy guide (our estimate). Sewn and long-tail bind offs use the tail itself, so cut it <strong>3 to 4 times the edge width</strong> before you start.</p>
<h2>How much yarn does a bind off use?</h2>
<p>A basic bind off uses a little more than a row of knitting. Purl Soho's tip is to measure a row you've already worked. We plan on about <strong>3 times the edge width</strong> for a basic bind off (our estimate). Stretchy bind offs use more: one knitter quoted by Cocoknits found Jeny's uses about 6¼ times the width. If you're close to the end of the ball, join new yarn at the start of the bind-off row, not halfway along.</p>
<h2>How do I fix the loose last stitch at the end?</h2>
<p>The last bound-off stitch often makes a big loop, or a little "ear" on the corner. An easy fix: when 2 stitches are left on the left needle, knit them together, then lift the last stitch over it, so the final loop is smaller. Then pull the tail firmly through the last loop and give the corner a tug before weaving in.</p>
<h2>How do I bind off in the round?</h2>
<p>Bind off all the way round as normal. When one stitch is left, cut the yarn and pull it through. To hide the step where the round started, thread the tail on a tapestry needle, take it under both legs of the <strong>first</strong> bound-off stitch, then back down into the centre of the <strong>last</strong> one. It makes a fake stitch that closes the gap.</p>
<h2>How do I bind off in the middle of a row?</h2>
<p>For shoulders, armholes or buttonholes, patterns say "bind off 6 stitches" and then carry on. Bind off the 6 as normal. The stitch left on the right needle after the last lift-over is the <strong>first stitch</strong> of the rest of the row, so count it.</p>
<h2>Bind off knitwise or purlwise?</h2>
<p>Bind off on a right-side row knitwise unless the pattern says otherwise. Binding off purlwise on a wrong-side row works the same way, with purl stitches. In ribbing, bind off in pattern. If the pattern just says "bind off in pattern", do the stitch the fabric shows.</p>
<p>What next? Weave the tail in neatly with our guide to <a href="{href("how-to-weave-in-ends.html")}">weaving in ends</a>, start the next piece with our <a href="{href("how-to-cast-on-knitting.html")}">cast on guide</a> and the <a href="{href("cast-on-calculator.html")}">cast on calculator</a>, or decode a pattern line with the <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a>. Spotted a ladder before you bound off? Here's <a href="{href("how-to-fix-a-dropped-stitch.html")}">how to fix a dropped stitch</a>. Adding a neckband or button band? See <a href="{href("how-to-pick-up-stitches-knitting.html")}">how to pick up stitches</a>.</p></div></section>'''
bo_faq = [
    ("How do you bind off in knitting?", "Knit 2 stitches, lift the first over the second and off the needle. Knit 1 more and lift over again; repeat until 1 stitch is left. Cut the yarn and pull it through the last loop."),
    ("Is casting off the same as binding off?", "Yes. Cast off is the UK name and bind off is the US name for the same thing: closing the last row so it can't unravel."),
    ("Why is my bind off too tight?", "Most knitters bind off tighter than they knit. Use a needle 1 or 2 sizes larger in your right hand for the bind-off row, don't tug each stitch, or use a stretchy bind off for cuffs and necklines."),
    ("How long should the tail be after binding off?", "About 6 to 8 in (15 to 20 cm) to weave in. Leave the seam length plus about 8 in if you'll sew a seam with it."),
    ("What is the stretchiest bind off?", "Jeny's surprisingly stretchy bind off and the tubular bind off are the usual choices for toe-up sock cuffs, sleeve cuffs, necklines and 1×1 rib."),
    ("How do you bind off in rib?", "Bind off in pattern: knit the knit stitches and purl the purl stitches, lifting the first over the second after each one."),
]
page("how-to-bind-off-knitting.html", "How to Bind Off Knitting (Cast Off) + Stretchy Bind Off Chooser | Purl & Paper",
     "How to bind off knitting step by step: the basic bind off in 4 drawings, binding off in rib, stretchy bind offs for cuffs, socks and necklines, fixing a tight edge and the last stitch, and how long a tail to leave.",
     bo, bo_faq, "How to bind off knitting", app_name="Bind off chooser")

# ---------------- HOW TO WEAVE IN ENDS (crochet + knitting, fasten off) ----------------
def _we_grid(knit):
    o = '<rect x="14" y="14" width="192" height="120" rx="8" fill="#f2e6cf"/>'
    for r in range(5):
        for i in range(8):
            x, y = 30 + i * 23, 32 + r * 22
            if knit: o += f'<path d="M{x - 7} {y - 6} q7 6 0 12 M{x + 7} {y - 6} q-7 6 0 12" fill="none" stroke="#d97aa0" stroke-width="2.4" stroke-linecap="round"/>'
            else: o += f'<rect x="{x - 4}" y="{y - 8}" width="8" height="17" rx="3" fill="none" stroke="#d97aa0" stroke-width="2.4"/>'
    return o
def we_fig(i):
    if i == 1:
        body = (f'<path d="M30 126 L190 126" stroke="#d97aa0" stroke-width="12" stroke-linecap="round"/>' + _hook(118, 70, -35, 90)
                + f'<ellipse cx="112" cy="84" rx="10" ry="16" fill="none" stroke="{_Y}" stroke-width="3.6"/><path d="M112 100 C110 112 108 118 104 126" stroke="{_Y}" stroke-width="3.6" fill="none"/>'
                + f'<path d="M60 40 C80 60 96 70 106 78" fill="none" stroke="{_Y}" stroke-width="3.6" stroke-dasharray="2 6" stroke-linecap="round"/>'
                + _LBL(20, 24, "cut, leave 6 in (15 cm)") + _LBL(204, 112, "pull the tail through", "end") + _LBL(110, 150, "tug gently to lock it", "middle"))
        cap = ("<strong>Fasten off (crochet).</strong>", "After the last stitch, cut the yarn leaving about 6 in (15 cm). Yarn over and pull the cut end all the way through the loop on the hook, then tug gently.")
    elif i == 2:
        body = (_we_grid(False) + f'<path d="M190 120 L60 120 Q44 120 44 104 L44 76 Q44 66 56 66 L150 66" fill="none" stroke="{_TL}" stroke-width="3.4" stroke-linecap="round"/><circle cx="150" cy="66" r="4" fill="{_MG}"/>'
                + _LBL(20, 150, "through the stitch posts, then turn back"))
        cap = ("<strong>Weave in crochet.</strong>", "On the wrong side, run the tail through the posts of a few stitches, about 1 to 2 in (3 to 5 cm). Turn and go back the other way through different strands. Add a third turn for blankets.")
    elif i == 3:
        body = (_we_grid(True) + f'<path d="M190 118 Q168 108 168 98 Q168 88 146 88 Q124 88 124 76 Q124 66 102 66 Q80 66 80 54 L60 44" fill="none" stroke="{_TL}" stroke-width="3.4" stroke-linecap="round"/><circle cx="60" cy="44" r="4" fill="{_MG}"/>'
                + _LBL(20, 150, "follow the purl bumps on the wrong side"))
        cap = ("<strong>Weave in knitting.</strong>", "On the purl side, follow the path of the yarn through the stitches (duplicate stitch), over 3 to 5 stitches for wool, 5 to 7 for slippery yarn. Split the plies as you go back for extra grip.")
    else:
        body = (_we_grid(False) + f'<path d="M30 70 L120 70" stroke="{_TL}" stroke-width="3.4"/><path d="M120 70 l14 -8" stroke="{_TL}" stroke-width="3.4" stroke-linecap="round"/>'
                + f'<path d="M150 40 l20 20 M170 40 l-20 20" stroke="{_HK}" stroke-width="3"/><circle cx="146" cy="36" r="6" fill="none" stroke="{_HK}" stroke-width="3"/><circle cx="174" cy="36" r="6" fill="none" stroke="{_HK}" stroke-width="3"/>'
                + f'<path d="M24 108 L60 108 M24 108 l8 -6 M24 108 l8 6 M196 108 L160 108 M196 108 l-8 -6 M196 108 l-8 6" stroke="{_HK}" stroke-width="2.4" fill="none"/>'
                + _LBL(110, 150, "stretch the fabric, then trim close", "middle"))
        cap = ("<strong>Stretch, then trim.</strong>", "Give the fabric a gentle stretch so the tail settles, then snip it close. Don't pull so hard the stitches pucker. Weave ends in before you block.")
    return (f'<figure class="mr-step"><svg viewBox="0 0 220 160" role="img" aria-label="Weaving in ends step {i}">{body}</svg>'
            f'<figcaption>{cap[0]}{cap[1]}</figcaption></figure>')
WE_YARN = [("Wool and other grippy yarn", "6 in (15 cm)", "3-5 stitches each way, 2 directions"),
           ("Cotton, acrylic and smooth yarn", "6 in (15 cm)", "5-7 stitches each way, split the plies"),
           ("Slippery yarn: superwash, silk, bamboo", "6-8 in (15-20 cm)", "5-7 stitches, 3 directions; sewing thread for extra hold"),
           ("Bulky and super bulky", "8 in (20 cm)", "Split the plies and weave each one separately"),
           ("Chenille, velvet and T-shirt yarn", "8 in (20 cm)", "Can't be split: pull through with a small crochet hook")]
we = top("How to weave in ends", "Every project finishes with tails to hide. Here's how to fasten off in crochet, weave in ends in crochet and knitting so they never poke out, what to do with slippery and chunky yarn, and a helper that tells you how long to leave, how far to weave and how long it'll take.", "How to weave in ends") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> leave a tail of about <strong>6 in (15 cm)</strong> (8 in for chunky yarn). Thread it on a blunt tapestry needle and, on the <strong>wrong side</strong>, run it through about 1 to 2 in (3 to 5 cm) of stitches of the same colour. Then <strong>change direction</strong> and go back through different strands; turn a third time for blankets and things that get washed a lot. Gently stretch the fabric and trim close. Weave ends in <strong>before blocking</strong>, and skip the knots.</div>
<div class="mr-steps">{"".join(we_fig(i) for i in range(1, 5))}</div>
<p class="note">Our own drawings.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Weaving in ends helper</h2>
<div class="field"><label>I'm working in</label><div class="seg" id="we-craft" role="group" aria-label="Craft"><button type="button" data-v="crochet" aria-pressed="true">Crochet</button><button type="button" data-v="knit" aria-pressed="false">Knitting</button></div></div>
<div class="field"><label for="we-fab">The fabric</label><select id="we-fab"><option value="rows" selected>Rows, flat (scarf, blanket, dishcloth)</option><option value="rounds">Rounds (hat, cowl, circle)</option><option value="granny">Granny squares or motifs</option><option value="ami">Amigurumi or stuffed toy</option><option value="stripes">Stripes or colourwork</option><option value="lace">Lace or open stitches</option><option value="rib">Ribbing</option></select></div>
<div class="field"><label for="we-yarn">The yarn</label><select id="we-yarn"><option value="wool" selected>Wool or other grippy yarn</option><option value="smooth">Cotton, acrylic or smooth yarn</option><option value="slip">Slippery: superwash, silk, bamboo</option><option value="bulky">Bulky or super bulky</option><option value="chenille">Chenille, velvet or T-shirt yarn</option><option value="fuzzy">Fuzzy: mohair, alpaca, brushed yarn</option></select></div>
<div class="row2"><div class="field"><label for="we-use">It will be</label><select id="we-use"><option value="wear" selected>Worn (hat, sweater, socks)</option><option value="heavy">Washed a lot (blanket, baby item, dishcloth)</option><option value="deco">Decorative (wall hanging, ornament)</option></select></div><div class="field"><label for="we-n">Ends to weave in</label><input id="we-n" type="number" min="1" max="2000" step="1" value="12" inputmode="numeric"></div></div>
<figure class="ts-fig"><svg id="we-svg" viewBox="0 0 260 150" role="img" aria-label="The path to weave the tail, on the wrong side"></svg><figcaption class="note">The path your tail takes, on the wrong side. The dot is where you trim.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="we-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>How long should the tail be to weave in?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Yarn</th><th scope="col">Tail to leave</th><th scope="col">How far to weave</th></tr></thead><tbody>
{"".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in WE_YARN)}</tbody></table></div>
<p class="note">Tail lengths from Make and Do Crew, MJ's Off The Hook Designs and Yarnspirations (6 in is the common minimum; thicker yarn needs more). Stitch counts from Cocoknits' duplicate stitch guide. The 8 in for bulky yarn is our rounding.</p>
<h2>How do I fasten off in crochet?</h2>
<ol><li>Finish the last stitch. Chain 1 if your pattern says so.</li>
<li>Cut the yarn, leaving about 6 in (15 cm).</li>
<li>Yarn over and pull the cut end all the way through the loop on the hook.</li>
<li>Tug the tail gently to close the loop. Not so hard that the last stitch puckers.</li></ol>
<h2>What is an invisible fasten off?</h2>
<p>On joined rounds, a normal fasten off leaves a little bump at the join. For a smoother finish, skip the slip stitch join: cut the yarn after the last stitch and pull the tail straight up through the last stitch. Thread it on a tapestry needle, pass it under <strong>both top loops</strong> of the first stitch of the round (skip the turning chain), then go back down into the centre of the last stitch. It makes a stitch that looks like all the others. Weave in on the wrong side.</p>
<h2>How do I weave in ends in crochet?</h2>
<p>Turn the work to the wrong side. Run the tail through the posts or along the tops of 4 to 6 stitches, about 1 to 2 in. Turn and go back the other way, skipping one strand, so the tail zigzags. MJ's Off The Hook Designs weaves in at least two directions and adds a third for things that get heavy use. On granny squares, Make and Do Crew weave under the thick clusters and change direction once. For a magic ring, weave round the first-round stitches, then reverse and tug: it pulls the centre closed too.</p>
<h2>How do I weave in ends in knitting?</h2>
<ul><li><strong>Duplicate stitch</strong> (Swiss darning): on the purl side, follow the path of the yarn through the stitches. It holds better than a straight line and doesn't show on the front (Cocoknits).</li>
<li><strong>Along a seam or edge:</strong> if there's a seam or a selvedge, weave up through it, then back.</li>
<li><strong>In ribbing:</strong> weave up and down inside one column of stitches so the rib can still stretch.</li>
<li><strong>Cast-on and bind-off tails:</strong> weave along the edge for a few stitches, then turn into the fabric. At the top of a hat, thread the tail through the live stitches, pull them closed and weave in on the inside.</li></ul>
<h2>Should I tie a knot before weaving in?</h2>
<p>No. Knots can work loose and poke through to the front, and you can feel them in a garment. A well woven-in tail holds better. Make and Do Crew also say not to use glue or a lighter; a fabric-safe glue is fine only as an extra layer on something decorative.</p>
<h2>How do I weave in slippery or chunky yarn?</h2>
<p>For <strong>slippery yarn</strong> (superwash, silk, bamboo, some cottons), weave further, 5 to 7 stitches each way, split the plies on the way back, and make three turns. Cocoknits' extra trick: whipstitch the tails together with sewing thread, then knot and clip the thread, not the yarn. For <strong>chunky yarn</strong>, split the plies and weave each one on its own so there's no lump. <strong>Chenille, velvet and T-shirt yarn</strong> can't be split, so pull them through with a small crochet hook (Make and Do Crew). <strong>Fuzzy yarn</strong> like mohair grabs on to itself, so a short weave holds well, but it's hard to undo, so weave in carefully the first time.</p>
<h2>How do I hide ends in amigurumi?</h2>
<p>After fastening off, close any opening by sewing through the front loops of the last round and pulling tight. Then push the needle into the toy, through the stuffing and out the other side. Pull the tail a little so the toy squashes, snip it close and let go: the end disappears inside.</p>
<h2>Should I weave in ends before or after blocking?</h2>
<p>Before. Yarnspirations and Make and Do Crew both weave in ends before blocking or seaming, so blocking sets the tails in place with the stitches. Some knitters leave the last bit untrimmed until after blocking, then snip it, so the tail can't pull back through when the fabric relaxes.</p>
<h2>How do I weave in fewer ends?</h2>
<ul><li><strong>Crochet over the tails:</strong> lay them along the top of the row and work the next few stitches over them.</li>
<li><strong>Weave in as you go</strong> on big or many-colour projects, so you don't face a pile at the end (Make and Do Crew).</li>
<li><strong>Carry yarn up the side</strong> for even-row stripes instead of cutting. Our <a href="{href("how-to-change-colors-in-crochet.html")}">stripe planner</a> counts the ends for you.</li>
<li><strong>Join same-colour yarn with a Russian join or spit splice</strong> (for wool that felts), which leaves no ends at all.</li></ul>
<p>What next? Learn the neatest way to finish knitting with our <a href="{href("how-to-bind-off-knitting.html")}">bind off guide</a>, plan stripes with fewer ends in the <a href="{href("how-to-change-colors-in-crochet.html")}">colour change guide</a>, or start your next round neatly with a <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>.</p></div></section>'''
we_faq = [
    ("How long should a tail be to weave in?", "About 6 in (15 cm) for most yarn. Leave about 8 in (20 cm) for chunky, slippery or chenille yarn."),
    ("How do you weave in ends in crochet?", "On the wrong side, run the tail through the posts of a few stitches for about 1 to 2 in, then turn and go back the other way through different strands. Add a third direction for blankets. Stretch gently and trim."),
    ("How do you weave in ends in knitting?", "On the purl side, follow the path of the yarn through 3 to 5 stitches (duplicate stitch), then come back the other way, splitting the plies. Use 5 to 7 stitches for slippery yarn."),
    ("Should I tie a knot before weaving in ends?", "No. Knots can work loose and poke through. Weaving in two or three directions holds better."),
    ("Do you weave in ends before or after blocking?", "Before. Blocking then sets the tails in place. Some knitters trim the last bit after blocking."),
    ("How do you fasten off in crochet?", "Cut the yarn leaving about 6 in (15 cm), yarn over and pull the cut end all the way through the loop on the hook, then tug gently."),
    ("How do you stop ends coming out of slippery yarn?", "Weave further (5 to 7 stitches each way), split the plies, change direction three times, and for extra hold whipstitch the tails together with sewing thread."),
]
page("how-to-weave-in-ends.html", "How to Weave in Ends (Crochet and Knitting) + Fasten Off | Purl & Paper",
     "How to fasten off and weave in ends in crochet and knitting so they never come undone: tail length, duplicate stitch, invisible fasten off, slippery and chunky yarn, amigurumi, and a helper for your yarn.",
     we, we_faq, "How to weave in ends", app_name="Weaving in ends helper")

# ---------------- HOW TO CAST ON KNITTING (guide + long-tail tail calculator + cast on chooser) ----------------
def lt_tail(sts, g4, per=None):
    """Long-tail estimate, same model as the cast on calculator: 4.5 / stitches per inch per stitch (about 1 in at worsted), plus 6 in."""
    p = per if per else CO_TAIL / (g4 / 4)
    return sts * p + 6
def _lt_fmt(inch): return f"{inch:.0f} in" if inch < 36 else f"{inch / 36:.1f} yd"
def _lt_base(knot_x=110, n_sts=0):
    o = _needle(14, 52, 206, 52)
    for k in range(n_sts):
        o += f'<ellipse cx="{70 + k * 20}" cy="52" rx="7" ry="13" fill="none" stroke="{_Y}" stroke-width="3.2"/>'
    o += f'<ellipse cx="{knot_x}" cy="52" rx="7" ry="13" fill="none" stroke="{_Y}" stroke-width="3.2"/>'
    return o
def _lt_hand(arrow=False):
    # thumb (left) holds the tail, finger (right) holds the ball yarn; both strands run to the palm below
    o = (f'<circle cx="58" cy="112" r="11" fill="#f2e6cf" stroke="#c9a37a" stroke-width="2"/><circle cx="166" cy="104" r="11" fill="#f2e6cf" stroke="#c9a37a" stroke-width="2"/>'
         f'<path d="M110 64 C96 80 70 92 60 101 M58 123 C70 140 96 148 108 152" fill="none" stroke="{_Y}" stroke-width="3.4" stroke-linecap="round"/>'
         f'<path d="M110 64 C126 76 152 86 164 93 M166 115 C150 136 124 148 112 152" fill="none" stroke="{_TL}" stroke-width="3.4" stroke-linecap="round"/>')
    if arrow:
        o += f'<path d="M76 104 C92 84 132 78 150 90" fill="none" stroke="{_MG}" stroke-width="3.2" stroke-dasharray="5 4" stroke-linecap="round"/><path d="M150 90 l-9 -1 m9 1 l-4 8" stroke="{_MG}" stroke-width="3.2" stroke-linecap="round"/>'
    return o
LT_STEPS = [
    ("Measure the tail, make a slip knot", "Pull out the tail: about 1 in (2.5 cm) per stitch in worsted yarn plus 6 in, less for thin yarn and more for thick (the calculator below does it). Make a slip knot there and put it on the needle.",
     _lt_base() + f'<path d="M104 64 C80 90 40 96 22 120 C40 130 110 120 200 136" fill="none" stroke="{_Y}" stroke-width="3.2" stroke-linecap="round"/>'
     + f'<path d="M30 146 H200" stroke="{_HK}" stroke-width="2"/>' + "".join(f'<path d="M{30 + k * 17} 146 v-6" stroke="{_HK}" stroke-width="1.6"/>' for k in range(11))
     + _LBL(14, 24, "slip knot on the needle") + _LBL(200, 128, "tail", "end")),
    ("Hold the slingshot", "Tail over your thumb, ball yarn over your index finger, both ends held in your palm. The needle sits on top with the slip knot, making a V of yarn.",
     _lt_base() + _lt_hand() + _LBL(14, 24, "thumb: tail") + _LBL(206, 24, "finger: ball yarn", "end")),
    ("Up through the thumb loop, over the finger strand", "Take the needle tip up through the loop on your thumb, then over and behind the strand on your index finger to catch it.",
     _lt_base() + _lt_hand(True) + _LBL(14, 24, "under, then over and catch")),
    ("Back through, drop the loop, snug it", "Bring the caught yarn back down through the thumb loop. Let the loop slide off your thumb, then spread thumb and finger to snug the new stitch. Repeat for every stitch.",
     _lt_base(150, 4) + _LBL(14, 24, "one new stitch each time") + f'<path d="M150 70 v24" stroke="{_MG}" stroke-width="3" stroke-linecap="round"/><path d="M144 88 l6 8 l6 -8" fill="none" stroke="{_MG}" stroke-width="3" stroke-linecap="round"/>'
     + _LBL(110, 120, "snug, not tight: the stitches should slide", "middle")),
]
def lt_fig(i, s):
    return (f'<figure class="mr-step"><svg viewBox="0 0 220 160" role="img" aria-label="Long-tail cast on step {i}: {e(s[0])}">{s[2]}</svg>'
            f'<figcaption><strong>{i}. {e(s[0])}</strong> {e(s[1])}</figcaption></figure>')
CN_METHODS = [  # name, stretch 1-3, tail to estimate?, best for, note
    ("Long-tail", 2, "Yes", "Almost everything: scarves, blankets, hats, sweaters", "The one most knitters use. Neat, fairly stretchy, and it already counts as a first row of sorts."),
    ("Knitted", 2, "No", "Beginners, and adding stitches at the start of a row", "Knit a stitch and put it back on the left needle. No tail to guess."),
    ("Cable", 1, "No", "Firm edges: bags, dishcloths, button bands, edges you'll pick up from", "Like the knitted cast on but worked between stitches. Neat, corded and firm."),
    ("Backward loop", 3, "No", "Adding a few stitches mid-row or at the end of a row (buttonholes, thumbs)", "The easiest to make, but the first row is fiddly and it can stretch out of shape."),
    ("German twisted", 3, "Yes", "Top-down sock cuffs, ribbed brims, garter edges", "A long-tail cast on with an extra twist. Very stretchy; a favourite with sock knitters."),
    ("Tubular", 3, "Yes (or waste yarn)", "1×1 rib on brims, cuffs and necklines", "Rolls the rib round the edge so it's almost invisible and very elastic."),
    ("Provisional", 2, "No (waste yarn)", "Edges you'll knit from later, or graft closed", "Worked over waste yarn you pull out later to free live stitches."),
]
CN_W = [(1, "Fingering"), (3, "DK"), (4, "Worsted"), (5, "Bulky"), (6, "Super bulky")]
CN_N = [20, 40, 60, 100, 150, 200]
cn_rows = "".join(f'<tr><td><strong>{n} stitches</strong></td>' + "".join(f"<td>{_lt_fmt(lt_tail(n, CO_G[k]))}</td>" for k, _ in CN_W) + "</tr>" for n in CN_N)
_cn40 = lt_tail(40, 18); _cn100 = lt_tail(100, 18)
cn_wopts = "".join(f'<option value="{CO_G[w["n"]]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} (about {CO_G[w["n"]]} sts per 4 in)</option>' for w in D["weights"] if w["n"] in CO_G)
cn = top("How to cast on knitting", "Casting on puts the first stitches on your needle. Here's the long-tail cast on in four drawings, how long a tail to leave for any number of stitches, and which cast on to use for scarves, hats, socks and firm edges.", "How to cast on knitting") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> the <strong>long-tail cast on</strong> is the one most knitters use. Pull out a tail of about <strong>1 in (2.5 cm) per stitch</strong> in worsted yarn, plus 6 in to weave in (so about <strong>{_lt_fmt(_cn40)}</strong> for 40 stitches), make a slip knot and hold the tail over your thumb and the ball yarn over your finger. Go up through the thumb loop, catch the finger strand, come back down and snug it. Repeat. If guessing the tail worries you, use the <strong>knitted cast on</strong> instead: it needs no tail.</div>
<div class="mr-steps">{"".join(lt_fig(i + 1, s) for i, s in enumerate(LT_STEPS))}</div>
<p class="note">Our own drawings, shown for right-handed knitting. The slip knot counts as your first stitch.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Cast on chooser and tail calculator</h2>
<div class="field"><label for="cn-what">What are you casting on?</label><select id="cn-what">
<option value="first" selected>My first project (scarf, dishcloth)</option><option value="scarf">Scarf, blanket or wrap</option><option value="big">A big blanket (lots of stitches)</option><option value="rib">Ribbed hat brim, cuff or sweater hem</option><option value="rib11">1×1 rib that must look invisible and stretch</option><option value="sock">Top-down sock cuff</option><option value="firm">Firm edge: bag, dishcloth, button band</option><option value="later">An edge I'll knit from later or graft</option><option value="add">A few extra stitches mid-project (buttonhole, thumb)</option></select></div>
<div class="row2"><div class="field"><label for="cn-n">Stitches to cast on</label><input id="cn-n" type="number" min="1" max="2000" step="1" value="40" inputmode="numeric"></div>
<div class="field"><label for="cn-y">Yarn weight</label><select id="cn-y">{cn_wopts}</select></div></div>
<details class="cn-more"><summary>I measured my own yarn (most accurate)</summary>
<p class="note">Wrap the yarn round your needle 10 times, unwind it and measure that length (Elizabeth Smith's wrap method). Each wrap is about one stitch.</p>
<div class="row2"><div class="field"><label for="cn-wrap">Length of 10 wraps</label><input id="cn-wrap" type="number" min="0" max="200" step="any" placeholder="e.g. 9" inputmode="decimal"></div>
<div class="field"><label for="cn-u">Unit</label><select id="cn-u"><option value="in" selected>inches</option><option value="cm">cm</option></select></div></div></details>
<figure class="ts-fig"><svg id="cn-svg" viewBox="0 0 300 120" role="img" aria-label="The tail you need, drawn against a 1 yard ruler"></svg><figcaption class="note" id="cn-cap">The tail to pull out, drawn against a ruler.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="cn-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>How much tail do I need for a long-tail cast on?</h2>
<p>A common rule (Marly Bird's) is <strong>about 1 in of tail per stitch</strong>, plus about 6 in to weave in: 100 stitches need roughly 106 in, or 3 yd. That fits worsted yarn. Thin yarn makes smaller stitches and needs less; thick yarn needs more, so we scale it by the yarn's typical gauge (our estimate). The most accurate way is to <strong>wrap the yarn round your needle once per stitch</strong> (or 10 times and multiply), as Elizabeth Smith Knits and Marly Bird both suggest. When in doubt, go longer: a spare foot of yarn costs nothing.</p></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Stitches</th>{"".join(f'<th scope="col">{n}<br><span class="muted">{CO_G[k]} sts / 4 in</span></th>' for k, n in CN_W)}</tr></thead><tbody>{cn_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Tail to pull out before your slip knot, including 6 in to weave in. Our estimate from the same maths as the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> (about 1 in per stitch at worsted gauge, scaled by each weight's typical gauge from the Craft Yarn Council ranges). Loose knitters and bigger needles need a little more.</p></div>
<div class="narrow prose">
<h2>What if I run out of tail?</h2>
<ul><li><strong>Pull it out and start again</strong> with a longer tail. It's annoying but it's only one row.</li>
<li><strong>Use two strands instead of a tail.</strong> Take one end from the outside of the ball and one from the middle (or use two balls), tie them in a slip knot and cast on with one over your thumb and one over your finger. You never run short. Cut the thumb strand afterwards; the slip knot doesn't count as a stitch here, so drop it at the end of the first row. It leaves two extra ends to weave in.</li>
<li><strong>Finish with the knitted cast on.</strong> If you're only a few stitches short, Marly Bird suggests adding the last ones with the knitted cast on.</li></ul>
<h2>Which cast on is best for beginners?</h2>
<p>Teachers disagree. The <strong>backward loop</strong> is the easiest to make, but the first row is fiddly and loose, so it's better for adding a few stitches. The <strong>knitted cast on</strong> and the <strong>cable cast on</strong> use the same move as a knit stitch, so many teachers start with one of them, and there's no tail to guess. The <strong>long-tail</strong> takes a little longer to learn but it's the one you'll use most, so it's worth learning early.</p>
<h2>Which cast on should I use?</h2></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Cast on</th><th scope="col">Stretch</th><th scope="col">Tail to guess?</th><th scope="col">Best for</th><th scope="col">What it's like</th></tr></thead><tbody>
{"".join(f'<tr><td><strong>{a}</strong></td><td aria-label="{s} of 3">{_bo_dots(s)}</td><td>{t}</td><td>{b}</td><td>{c}</td></tr>' for a, s, t, b, c in CN_METHODS)}</tbody></table></div>
<p class="note" style="margin-top:12px">Uses from Wikipedia's casting on article, Little Red Window's cast on comparison and LoveCrafts' cable cast on guide. Stretch dots are our rough comparison.</p></div>
<div class="narrow prose">
<h2>Which cast on is stretchy?</h2>
<p>For anything that has to go over a head, hand or heel, use a stretchy cast on: the <strong>long-tail</strong> is fairly stretchy, the <strong>German twisted</strong> (a long-tail with an extra twist) is very stretchy, and the <strong>tubular</strong> cast on is the most elastic for 1×1 rib. The <strong>cable cast on</strong> is firm, so keep it for bags, dishcloths and edges you'll pick up stitches from.</p>
<h2>Why is my cast on too tight?</h2>
<ul><li><strong>Use a bigger needle</strong> for the cast on only: 1 or 2 sizes up, then switch back for the first row.</li>
<li><strong>Cast on over two needles</strong> held together, then slide one out. Marly Bird recommends it for ribbing.</li>
<li><strong>Leave a gap</strong> of about the width of a stitch between stitches on the needle, and don't yank the yarn after each one. They should slide easily.</li></ul>
<h2>Does the cast on count as a row?</h2>
<p>Usually not: patterns start counting at the first row you knit. But the long-tail cast on looks like a row of knit stitches on one side, so some knitters treat the next row as a wrong-side row (Little Red Window). Follow your pattern if it says which side faces you.</p>
<h2>How do I cast on to knit in the round?</h2>
<ol><li>Cast on all the stitches onto a circular needle shorter than the piece is around (a 16 in circular for a hat).</li>
<li>Spread them round the needle and check the bottom edge runs along the inside of the circle all the way round, with no twist. A twist can't be fixed later.</li>
<li>Put a marker on the right needle, then knit the first stitch on the left needle with the working yarn, pulling it snug. That joins the round.</li></ol>
<p>What next? Knitting a hat or socks? See <a href="{href("how-to-knit-in-the-round.html")}">how to knit in the round</a> to join without twisting. Work out how many stitches to cast on with the <a href="{href("cast-on-calculator.html")}">cast on calculator</a>, decode the first pattern row with the <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a>, and when you get to the end, our <a href="{href("how-to-bind-off-knitting.html")}">bind off guide</a> finishes it neatly. Dropped a stitch on the way? See <a href="{href("how-to-fix-a-dropped-stitch.html")}">how to fix a dropped stitch</a>. Adding a neckband or button band? See <a href="{href("how-to-pick-up-stitches-knitting.html")}">how to pick up stitches</a>.</p></div></section>'''
cn_faq = [
    ("How do you cast on in knitting?", "The long-tail cast on is the most used: leave a tail of about 1 in per stitch, make a slip knot on the needle, hold the tail over your thumb and the ball yarn over your index finger, go up through the thumb loop, catch the finger strand, come back down and snug the stitch. Repeat."),
    ("How long should the tail be for a long-tail cast on?", f"About 1 in (2.5 cm) per stitch in worsted yarn, plus about 6 in to weave in. That's roughly {_lt_fmt(_cn40)} for 40 stitches and {_lt_fmt(_cn100)} for 100. Thin yarn needs less and thick yarn more. Wrapping the yarn round the needle once per stitch gives an exact measure."),
    ("What's the easiest cast on for beginners?", "The backward loop is the easiest to make, but its first row is fiddly. Many teachers start beginners on the knitted or cable cast on, which use the same move as a knit stitch and need no tail."),
    ("What is the stretchiest cast on?", "The tubular cast on (for 1×1 rib) and the German twisted cast on are the stretchiest. The long-tail is fairly stretchy too. The cable cast on is firm."),
    ("Why is my cast on so tight?", "Cast on with a needle 1 or 2 sizes larger, or over two needles held together, and leave a small gap between stitches. Switch back to the right needle for the first row."),
    ("Does the cast on count as the first row?", "Usually not. Patterns start counting at the first row you knit after the cast on, unless they say otherwise."),
]
page("how-to-cast-on-knitting.html", "How to Cast On Knitting (Long-Tail) + Tail Length Calculator | Purl & Paper",
     "How to cast on knitting: the long-tail cast on in 4 drawings, how long a tail to leave for any number of stitches, what to do if it runs out, and which cast on to use for scarves, hats, socks and firm edges.",
     cn, cn_faq, "How to cast on knitting", app_name="Long-tail cast on calculator")

# ---------------- HOW TO DECREASE IN CROCHET (guide + decrease round writer) ----------------
DC_NAME = {"sc": ("sc", "sc2tog", "sc3tog"), "hdc": ("hdc", "hdc2tog", "hdc3tog"), "dc": ("dc", "dc2tog", "dc3tog")}
def dc_round(S, T, st="sc", inv=False, stagger=False):
    """Same maths as app.js: one round (or row) from S to T stitches with 2-together decreases. None if not possible."""
    D = S - T
    if D < 1 or 2 * D > S: return None
    a, ex = divmod(S - 2 * D, D)
    s, dec = DC_NAME[st][0], ("invdec" if inv and st == "sc" else DC_NAME[st][1])
    w = lambda n: f"{s} {n}" if n else ""
    j = lambda *p: ", ".join(x for x in p if x)
    if a == 0 and ex == 0: return f"{dec} around ({T})"
    if ex == 0:
        if stagger and a >= 2:
            h = a // 2
            mid = f"[{dec}, {w(a)}] × {D - 1}, " if D > 1 else ""
            return j(w(h), mid + dec, w(a - h)) + f" ({T})"
        return f"[{j(w(a), dec)}] × {D} ({T})"
    return f"[{j(w(a + 1), dec)}] × {ex}, [{j(w(a), dec)}] × {D - ex} ({T})"
def dc_close(S, per=6, end=6, st="sc", inv=True):
    out, n, k = [], S, 0
    while n > end:
        t = max(end, n - per)
        if 2 * (n - t) > n: t = (n + 1) // 2
        out.append((n, t, dc_round(n, t, st, inv, k % 2 == 1))); n = t; k += 1
    return out
def _dc_posts(n=6, top_hi=(), front=False):
    o = '<rect x="14" y="96" width="192" height="50" rx="6" fill="#f2e6cf"/>'
    for i in range(n):
        x = 34 + i * 30
        o += f'<rect x="{x - 4}" y="100" width="8" height="40" rx="3" fill="none" stroke="{_Y2}" stroke-width="2.4"/>'
        c = _TL if i in top_hi else _Y
        o += f'<ellipse cx="{x}" cy="90" rx="13" ry="6" fill="#fbfcfa" stroke="{c}" stroke-width="3.2"/>'
        if front and i in top_hi:
            o += f'<path d="M{x - 13} 90 Q{x} 102 {x + 13} 90" fill="none" stroke="{_MG}" stroke-width="3.6"/>'
    return o
def _dc_loops(x, y, n, ang=-40):
    a = _m.radians(ang)
    return "".join(f'<ellipse cx="{x + (12 + k * 11) * _m.cos(a):.1f}" cy="{y + (12 + k * 11) * _m.sin(a):.1f}" rx="4" ry="8" transform="rotate({ang + 90} {x + (12 + k * 11) * _m.cos(a):.1f} {y + (12 + k * 11) * _m.sin(a):.1f})" fill="none" stroke="{_Y}" stroke-width="3"/>' for k in range(n))
DC_STEPS = [
    ("Pull up a loop in the next stitch", "Insert the hook in the next stitch, yarn over and pull up a loop. Don't finish the stitch: there are 2 loops on the hook.",
     _dc_posts(6, (2,)) + _hook(94, 80, -40, 100) + _dc_loops(94, 80, 2) + _LBL(14, 24, "2 loops on the hook")),
    ("Pull up a loop in the stitch after", "Insert the hook in the following stitch, yarn over and pull up another loop. Now there are 3 loops on the hook.",
     _dc_posts(6, (2, 3)) + _hook(124, 80, -40, 90) + _dc_loops(124, 80, 3) + _LBL(14, 24, "3 loops on the hook")),
    ("Yarn over, pull through all 3", "Yarn over and pull through all 3 loops. One stitch now sits on top of two: that's a single crochet decrease, sc2tog.",
     _dc_posts(6) + f'<path d="M94 86 L109 60 L124 86" fill="none" stroke="{_TL}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/><ellipse cx="109" cy="56" rx="12" ry="5.5" fill="#fbfcfa" stroke="{_TL}" stroke-width="3.2"/>'
     + _LBL(14, 24, "2 stitches become 1")),
    ("Invisible decrease: front loops only", "For amigurumi: insert the hook under the front loop only of the next stitch, then the front loop of the one after (no yarn overs, 3 loops). Yarn over, pull through 2; yarn over, pull through the last 2.",
     _dc_posts(6, (2, 3), True) + _hook(126, 92, -35, 92) + _LBL(14, 24, "front loops only: no bump, no gap")),
]
def dc_fig(i, s):
    return (f'<figure class="mr-step"><svg viewBox="0 0 220 160" role="img" aria-label="Decrease step {i}: {e(s[0])}">{s[2]}</svg>'
            f'<figcaption><strong>{i}. {e(s[0])}</strong> {e(s[1])}</figcaption></figure>')
DC_TAB = [
    ("Single crochet 2 together", "sc2tog (dec)", "dc2tog", "Pull up a loop in each of the next 2 stitches (3 loops), yarn over, pull through all 3.", "1"),
    ("Invisible decrease", "invdec", "invdec", "Front loops of the next 2 stitches, no yarn overs (3 loops). Yarn over, through 2; yarn over, through 2.", "1"),
    ("Half double crochet 2 together", "hdc2tog", "htr2tog", "Yarn over, pull up a loop in the next stitch; yarn over, pull up a loop in the one after (5 loops). Yarn over, pull through all 5.", "1"),
    ("Double crochet 2 together", "dc2tog", "tr2tog", "Yarn over, pull up a loop, yarn over, through 2 (2 left). Do the same in the next stitch (3 loops). Yarn over, through all 3.", "1"),
    ("Single crochet 3 together", "sc3tog", "dc3tog", "Pull up a loop in each of the next 3 stitches (4 loops), yarn over, through all 4.", "2"),
]
DC_EX = [(48, 42), (36, 30), (30, 24), (24, 18), (18, 12), (12, 6), (40, 30), (50, 44)]
dc_ex_rows = "".join(f'<tr><td>{S}</td><td>{T}</td><td><code>{e(dc_round(S, T))}</code></td><td><code>{e(dc_round(S, T, stagger=True))}</code></td></tr>' for S, T in DC_EX)
dc_close36 = "".join(f"<li>Round {i + 1}: <code>{e(r)}</code></li>" for i, (_, _, r) in enumerate(dc_close(36)))
dcp = top("How to decrease in crochet", "A decrease turns two stitches into one, so your work gets narrower or your amigurumi closes up. Here's the single crochet decrease (sc2tog) and the invisible decrease in four drawings, the other decreases, and a helper that writes your decrease rounds.", "How to decrease in crochet") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> to <strong>single crochet 2 together (sc2tog)</strong>, insert the hook in the next stitch and pull up a loop, insert in the stitch after and pull up a loop (<strong>3 loops</strong> on the hook), then yarn over and pull through all 3. Two stitches become one. For amigurumi, use the <strong>invisible decrease</strong>: front loops only of the next 2 stitches, yarn over and pull through 2, yarn over and pull through the last 2. To close a ball, take away 6 stitches a round: 36, 30, 24, 18, 12, 6.</div>
<div class="mr-steps">{"".join(dc_fig(i + 1, s) for i, s in enumerate(DC_STEPS))}</div>
<p class="note">Our own drawings, in US terms. UK patterns call sc2tog "dc2tog": see the <a href="{href("crochet-terms.html")}">US and UK crochet terms</a>.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Decrease round writer</h2>
<div class="field"><span class="label" id="dc-mode-l">I want to</span><div class="seg" role="group" aria-labelledby="dc-mode-l" id="dc-mode"><button type="button" data-v="close" aria-pressed="true">Close an amigurumi</button><button type="button" data-v="one" aria-pressed="false">Decrease one round or row</button></div></div>
<div class="row2"><div class="field"><label for="dc-s">Stitches you have now</label><input id="dc-s" type="number" min="2" max="1000" step="1" value="36" inputmode="numeric"></div>
<div class="field" id="dc-t-f" hidden><label for="dc-t">Stitches you want</label><input id="dc-t" type="number" min="1" max="1000" step="1" value="30" inputmode="numeric"></div>
<div class="field" id="dc-per-f"><label for="dc-per">Take away each round</label><select id="dc-per"><option value="6" selected>6 (started with 6 in a magic ring)</option><option value="8">8 (started with 8)</option><option value="10">10</option><option value="12">12 (started with 12)</option></select></div></div>
<div class="row2"><div class="field"><label for="dc-st">Stitch</label><select id="dc-st"><option value="sc" selected>Single crochet (sc)</option><option value="hdc">Half double (hdc)</option><option value="dc">Double crochet (dc)</option></select></div>
<div class="field"><label for="dc-type">Decrease</label><select id="dc-type"><option value="inv" selected>Invisible (front loops)</option><option value="std">Standard (2 together)</option></select></div></div>
<div class="field" id="dc-way-f" hidden><span class="label" id="dc-way-l">Working</span><div class="seg" role="group" aria-labelledby="dc-way-l" id="dc-way"><button type="button" data-v="round" aria-pressed="true">In rounds</button><button type="button" data-v="flat" aria-pressed="false">In rows</button></div></div>
<figure class="ts-fig"><svg id="dc-svg" viewBox="0 0 300 200" role="img" aria-label="The stitches of the first round with each decrease marked"></svg><figcaption class="note" id="dc-cap">Your round seen from above. Pink pairs are worked together.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="dc-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>How do you decrease in crochet?</h2>
<p>Every crochet decrease works the same way: start a stitch in each of two (or three) stitches, but stop each one just before its last step, so the loops pile up on your hook. Then finish them all at once with one yarn over. The table shows the usual ones.</p></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Decrease</th><th scope="col">US</th><th scope="col">UK</th><th scope="col">How</th><th scope="col">Stitches taken away</th></tr></thead><tbody>
{"".join(f"<tr><td><strong>{a}</strong></td><td><code>{b}</code></td><td><code>{c}</code></td><td>{d}</td><td>{x}</td></tr>" for a, b, c, d, x in DC_TAB)}</tbody></table></div>
<p class="note" style="margin-top:12px">Steps from Handy Little Me and One Little Project (sc2tog), PlanetJune, Moogly and Desert Blossom Crafts (invisible decrease) and Moogly (hdc2tog, dc2tog). A 3-together decrease takes away 2 stitches.</p></div>
<div class="narrow prose">
<h2>What is the invisible decrease, and when should I use it?</h2>
<p>The invisible decrease (invdec) was made popular by PlanetJune for amigurumi. You go through the <strong>front loops only</strong> of two stitches and don't yarn over until both are on the hook. Because the back loops stay put, there's no bump or gap where the decrease was. Use it for amigurumi, hats and anything in tight single crochet where a standard sc2tog would show. In flat, loose work the difference is small, so either is fine. Moogly also shows an invisible version for double crochet.</p>
<h2>Why do my decreases leave holes or bumps?</h2>
<ul><li><strong>Bumps:</strong> a standard sc2tog through both loops leaves 3 loops to pull through, which makes a thicker stitch. Switch to the invisible decrease.</li>
<li><strong>Gaps:</strong> PlanetJune says the gap comes from the working loop getting longer. Tug the loop on your hook snug before you yarn over, and again before the next stitch.</li>
<li><strong>Holes in amigurumi:</strong> go down a hook size so the fabric is tight, and keep your tension even through the decreases.</li></ul>
<h2>How do you close an amigurumi ball?</h2>
<p>Most amigurumi starts with 6 stitches and adds 6 every round, so it closes by doing the opposite: take away 6 stitches every round until 6 are left. From 36 stitches that's 5 rounds:</p>
<ol class="dc-list">{dc_close36}</ol>
<p class="note">Our own maths. Alternate rounds start halfway into the repeat so the decreases don't stack into corners.</p>
<ol><li><strong>Stuff as you go.</strong> Stuff firmly before the hole gets too small for your fingers, usually around 12 to 18 stitches (our tip), then top up through the gap.</li>
<li><strong>Fasten off</strong> with a tail of about 6 in (15 cm) (The Woobles, Stitch by Fay).</li>
<li><strong>Close the hole:</strong> thread the tail on a needle and go through the <strong>front loop only</strong> of each of the last stitches, all in the same direction, then pull the tail tight. The hole closes like a drawstring.</li>
<li><strong>Hide the tail:</strong> push the needle in through the middle of the closed hole and out somewhere else on the toy, pull, and snip close. The end disappears inside.</li></ol>
<h2>What does "dec" mean in a crochet pattern?</h2>
<p>"Dec" means decrease: work two stitches together, usually sc2tog unless the pattern says otherwise. "Dec around" or "dec 6 times" means do it over and over, so 12 stitches become 6. A pattern line like "*sc 4, dec* 6 times (30)" means 4 single crochet then 1 decrease, 6 times, ending with 30 stitches. Each decrease counts as <strong>one</strong> stitch when you count your round.</p>
<h2>How do I decrease evenly across a round or row?</h2>
<p>Each decrease uses 2 stitches. Take the decreases away from your stitch count to see how many stitches you end with, then spread the plain stitches between the decreases. For 36 stitches down to 30: 6 decreases use 12 stitches, which leaves 24 plain ones, 4 before each decrease. The helper above does this for any number, and the <a href="{href("increase-decrease-calculator.html")}">increase and decrease evenly calculator</a> does the same for knitting too.</p>
<h2>How do I decrease at the end of a row?</h2>
<p>To shape a triangle or a sleeve, decrease at the edges instead of across the row: work sc2tog over the first two stitches and again over the last two. That takes away 2 stitches per row and keeps the edges smooth. Some patterns skip a stitch instead, which works but leaves a small hole.</p>
<p>What next? Start your next ball neatly with a <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>, plan the increase rounds with the <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a>, and hide your tails with our guide to <a href="{href("how-to-weave-in-ends.html")}">weaving in ends</a>. Selling your toys? See <a href="{href("how-to-price-amigurumi.html")}">how to price amigurumi</a>.</p></div></section>'''
dc_faq = [
    ("How do you decrease in crochet?", "For a single crochet decrease (sc2tog), insert the hook in the next stitch and pull up a loop, insert in the stitch after and pull up a loop, then yarn over and pull through all 3 loops. Two stitches become one."),
    ("What is an invisible decrease in crochet?", "A decrease for amigurumi: insert the hook in the front loop only of the next 2 stitches (3 loops on the hook), yarn over and pull through 2, then yarn over and pull through the last 2. It leaves no bump or gap."),
    ("Does a decrease count as one stitch?", "Yes. Two stitches worked together make one stitch, so count each decrease as one when you count your round."),
    ("How do you close an amigurumi?", "Decrease 6 stitches a round until 6 are left (36, 30, 24, 18, 12, 6), stuffing as you go. Fasten off with a 6 in tail, sew through the front loop of each last stitch, pull tight, then push the needle through the toy and snip."),
    ("What does sc 4, dec mean?", "Work 4 single crochet, then 1 decrease (sc2tog). Repeated 6 times on 36 stitches it leaves 30."),
    ("Why does my crochet decrease leave a hole?", "The working loop has probably grown too long. Tug it snug before each yarn over, use the invisible decrease, and try a smaller hook for amigurumi."),
]
page("how-to-crochet-decrease.html", "How to Decrease in Crochet (sc2tog, Invisible Decrease) + Round Writer | Purl & Paper",
     "How to decrease in crochet: sc2tog and the invisible decrease in 4 drawings, hdc2tog and dc2tog, fixing holes and bumps, closing amigurumi, and a helper that writes your decrease rounds.",
     dcp, dc_faq, "How to decrease in crochet", app_name="Crochet decrease round writer")


# ---------------- HOW TO FIX A DROPPED STITCH (guide + fix helper) ----------------
def _ds_fab(loop_row, hook=False, hi_rung=False, marker=False, on_needle=False, rung_lbl=False):
    """Knit fabric, 7 columns x 6 rows. Column 3 has a ladder above loop_row (live loop at loop_row)."""
    o = '<rect x="18" y="34" width="184" height="124" rx="8" fill="#f2e6cf"/>' + _needle(8, 26, 212, 26)
    ys = [146 - k * 20 for k in range(6)]
    for c in range(7):
        x = 40 + c * 23
        for k in range(6):
            if c == 3 and k >= loop_row and not on_needle:
                continue
            o += _kst(x, ys[k], _Y2 if c != 3 else _Y, 2.4 if c != 3 else 3)
        if c != 3 or on_needle:
            o += f'<ellipse cx="{x}" cy="26" rx="6" ry="10" fill="none" stroke="{_Y2 if c != 3 else _Y}" stroke-width="2.6"/>'
    if not on_needle:
        x = 40 + 3 * 23
        for k in range(loop_row, 6):
            col = _TL if (hi_rung and k == loop_row) else _Y2
            y = ys[k] - 10
            o += f'<path d="M{x - 13} {y} Q{x} {y + 5} {x + 13} {y}" fill="none" stroke="{col}" stroke-width="{3.6 if col == _TL else 2.6}" stroke-linecap="round"/>'
        ly = ys[loop_row] + 4
        o += f'<ellipse cx="{x}" cy="{ly}" rx="7" ry="11" fill="#fbfcfa" stroke="{_Y}" stroke-width="3.4"/>'
        if marker:
            o += (f'<path d="M{x + 6} {ly + 6} q14 10 28 2" fill="none" stroke="{_MG}" stroke-width="3.2" stroke-linecap="round"/>'
                  f'<circle cx="{x + 36}" cy="{ly + 6}" r="6" fill="none" stroke="{_MG}" stroke-width="3.2"/>')
        if hook:
            o += _hook(x + 2, ly - 2, -55, 95)
        if rung_lbl:
            o += _LBL(20, 167, "teal = the bottom rung")
    return o
DS_STEPS = [
    ("Catch it", "Slide a locking stitch marker, safety pin or spare needle through the loose loop so it can't run any further.", _ds_fab(2, marker=True)),
    ("Hook in from the front", "With the knit side facing you, put a crochet hook into the loop from front to back, hook pointing up.", _ds_fab(2, hook=True, hi_rung=True, rung_lbl=True)),
    ("Pull the bottom rung through", "Catch the lowest loose strand of the ladder and pull it through the loop. That's one row fixed. Repeat, one rung at a time, in order.", _ds_fab(3, hook=True, hi_rung=True)),
    ("Put it back on the needle", "When no rungs are left, put the loop on the left needle without twisting it: the leg nearest the needle tip sits in front. Knit on.", _ds_fab(6, on_needle=True)),
]
def ds_fig(i, s):
    return (f'<figure class="mr-step"><svg viewBox="0 0 220 172" role="img" aria-label="Dropped stitch step {i}: {e(s[0])}">{s[2]}</svg>'
            f'<figcaption><strong>{i}. {e(s[0])}</strong> {e(s[1])}</figcaption></figure>')
DS_TAB = [
    ("Stockinette, knit side facing", "Every rung is a knit pickup", "Hook in from the front, pull each rung through toward you."),
    ("Stockinette, purl side facing", "Every rung is a purl pickup", "Easiest: turn the work so the knit side faces you, then it's all knit pickups."),
    ("Garter stitch", "Knit and purl rungs take turns", "Check the bottom strand: a V is knit, a bump is purl. Then switch sides each rung (or turn the work)."),
    ("Rib (k2, p2 or k1, p1)", "The whole column is the same", "A knit column is fixed from the right side. A purl column: turn the work and fix it as knit from the back."),
    ("Seed or moss stitch", "Knit and purl rungs take turns", "Like garter: work out the bottom one, then alternate."),
]
dsp = top("How to fix a dropped stitch in knitting", "A dropped stitch runs down your knitting like a ladder, but it's nearly always fixable without ripping back. Here's how in four drawings, for stockinette, garter and rib, plus a helper that tells you exactly how to pick up each rung.", "How to fix a dropped stitch") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> first <strong>catch the loose loop</strong> with a stitch marker or safety pin so it can't run further. Then, with the <strong>knit side facing you</strong>, put a crochet hook (about your needle size or a little smaller) into the loop from the front, catch the <strong>lowest loose strand</strong> of the ladder and pull it through. Repeat up the ladder, one strand per row, then put the stitch back on the left needle with its front leg toward the tip so it isn't twisted. In garter stitch, switch between knit and purl pickups on each row.</div>
<div class="mr-steps">{"".join(ds_fig(i + 1, s) for i, s in enumerate(DS_STEPS))}</div>
<p class="note">Our own drawings. The loose strands across the gap are the "ladder"; each one is one row of the dropped stitch.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Dropped stitch helper</h2>
<div class="field"><label for="ds-fab">What's the fabric?</label><select id="ds-fab"><option value="stk" selected>Stockinette, knit side facing me</option><option value="stp">Stockinette, purl side facing me</option><option value="gar">Garter stitch</option><option value="ribk">Rib, it fell from a knit column</option><option value="ribp">Rib, it fell from a purl column</option><option value="seed">Seed or moss stitch</option></select></div>
<div class="field" id="ds-first-f" hidden><span class="label" id="ds-first-l">The bottom loose strand makes a</span><div class="seg" role="group" aria-labelledby="ds-first-l" id="ds-first"><button type="button" data-v="k" aria-pressed="true">V (knit)</button><button type="button" data-v="p" aria-pressed="false">Bump (purl)</button></div><span class="note" style="display:block;margin-top:6px">Follow the lowest strand to the stitch beside the gap: a V means knit, a bump means purl.</span></div>
<div class="row2"><div class="field"><label for="ds-rows">Rows it has run down</label><input id="ds-rows" type="number" min="1" max="200" step="1" value="5" inputmode="numeric"><span class="note">Count the loose strands.</span></div>
<div class="field"><label for="ds-n">Stitches dropped</label><input id="ds-n" type="number" min="1" max="20" step="1" value="1" inputmode="numeric"></div></div>
<div class="row2"><div class="field"><label for="ds-mm">Needle size (mm)</label><input id="ds-mm" type="number" min="1.5" max="25" step="0.25" value="4" inputmode="decimal"></div>
<div class="field"><label for="ds-above">In that column above the drop</label><select id="ds-above"><option value="plain" selected>Plain knitting</option><option value="shape">An increase or decrease</option><option value="fancy">Cables, lace or colourwork</option></select></div></div>
<div class="field"><span class="label" id="ds-when-l">Are you still knitting?</span><div class="seg" role="group" aria-labelledby="ds-when-l" id="ds-when"><button type="button" data-v="live" aria-pressed="true">Yes, stitches on the needle</button><button type="button" data-v="done" aria-pressed="false">No, already bound off</button></div></div>
<figure class="ts-fig"><svg id="ds-svg" viewBox="0 0 300 230" role="img" aria-label="Your ladder with each rung marked knit or purl"></svg><figcaption class="note" id="ds-cap">Your ladder: work from the bottom rung up.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="ds-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>How do you pick up a dropped stitch in different stitches?</h2>
<p>The only thing that changes between fabrics is whether each rung is pulled through as a knit or a purl. Pulling from the front (rung coming toward you) makes a knit stitch; pulling from the back makes a purl.</p></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Fabric</th><th scope="col">The rungs are</th><th scope="col">How to fix it</th></tr></thead><tbody>
{"".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in DS_TAB)}</tbody></table></div>
<p class="note" style="margin-top:12px">Knit and purl pickups from Dummies and LoveCrafts; the crochet hook method from Yarnspirations and Garnstudio (DROPS). Rib and seed rows are our own summary of the same rule.</p></div>
<div class="narrow prose">
<h2>How do I fix a dropped stitch several rows down?</h2>
<p>Exactly the same way, just with more rungs. The key is to take them <strong>in order from the bottom</strong>: Dummies warns that pulling a strand from the wrong row leaves an obvious glitch. Check each new stitch looks like the ones beside it as you go. When you reach the top, the last stitch goes on the left needle and you knit it as normal.</p>
<p>If the stitch has run a long way, the fixed column can look tight or loose. Give the fabric a gentle tug sideways and lengthways to share the yarn out (Dummies), and washing or blocking evens it out further, because damp yarn relaxes (LoveCrafts).</p>
<h2>Which crochet hook should I use?</h2>
<p>About the same size as your knitting needles or a little smaller (LoveCrafts). A hook much bigger than the needle stretches the stitch; much smaller and it slips off the rung. No hook? You can work the rungs with your knitting needles by lifting the loop over each strand, it's just fiddlier.</p>
<h2>How do I put the stitch back on the needle without twisting it?</h2>
<p>Look at the stitches next to it: each one has two legs, one in front of the needle and one behind. For most knitters the leg in front sits nearer the tip of the left needle. Put your rescued stitch on the same way. If it's twisted, the legs cross at the bottom; knit it through the back loop, or slip it off and put it back the other way round.</p>
<h2>What if I've dropped more than one stitch?</h2>
<p>Catch every loose loop with its own marker or safety pin first (Yarnspirations), then fix them one at a time. For several stitches, a stiff yarn or a deep drop, LoveCrafts suggests working the rungs with a spare pair of needles about the same size as yours.</p>
<h2>When should I rip back instead?</h2>
<ul><li><strong>Something happens in that column above the drop.</strong> A decrease, increase, cable cross or lace yarn over can't be rebuilt with a hook unless you know exactly how to work it. Rip back to below the drop, or ladder up only as far as the shaping.</li>
<li><strong>It ran a very long way.</strong> Yarnspirations says a drop caught within a few rows is easy, but once several inches have been worked it's often easier to unravel back to it.</li>
<li><strong>You can't tell which rung is which.</strong> If the ladder is tangled or the yarn is fuzzy, ripping back can be quicker than untangling.</li></ul>
<p>Our tip for next time: before a tricky section, thread a smooth waste yarn through every stitch of one row with a tapestry needle. That "lifeline" stops you ripping back further than that row.</p>
<h2>What if I find it after binding off?</h2>
<p>It can still be fixed. Catch the loop, ladder it up to the top, then sew it down to the bound off edge with a length of matching yarn, going through the loop at least once (LoveCrafts). Weave the ends in, as in our guide to <a href="{href("how-to-weave-in-ends.html")}">weaving in ends</a>.</p>
<h2>How do I stop dropping stitches?</h2>
<p>Our tips: finish the row before you put your knitting down, push the stitches back from the needle tips (or use point protectors) when you stop, and try grippier wooden or bamboo needles if your yarn is slippery. Keep a locking stitch marker on your project bag for emergencies. Losing track of rows when you fix one? The <a href="{href("row-counter.html")}">row counter</a> keeps count for you.</p>
<p>What next? New to the basics? See <a href="{href("how-to-cast-on-knitting.html")}">how to cast on</a>, <a href="{href("how-to-bind-off-knitting.html")}">how to bind off</a> and what all those letters mean in our <a href="{href("knitting-abbreviations.html")}">knitting abbreviations</a> list.</p></div></section>'''
ds_faq = [
    ("How do you fix a dropped stitch in knitting?", "Catch the loose loop with a stitch marker. With the knit side facing you, put a crochet hook into the loop from the front, catch the lowest loose strand of the ladder and pull it through. Repeat for each strand, then put the stitch back on the left needle without twisting it."),
    ("Can you fix a dropped stitch several rows down?", "Yes. Work up the ladder one strand per row, starting with the lowest, and check each new stitch matches its neighbours. If there's a cable, lace or decrease in that column above the drop, it's usually easier to rip back."),
    ("How do you fix a dropped stitch in garter stitch?", "Garter stitch alternates knit and purl rows in each column, so switch for every strand: pull one through from the front (knit), the next from the back (purl), or turn the work over between strands."),
    ("How do you fix a dropped purl stitch?", "Turn the work so the knit side faces you; a purl stitch is a knit stitch from the other side. Fix it with a crochet hook as a knit, then turn back."),
    ("What size crochet hook do I need to pick up a dropped stitch?", "About the same size as your knitting needle or a little smaller."),
    ("Can I fix a dropped stitch after binding off?", "Yes. Ladder it up to the top with a crochet hook, then sew the top loop to the bound off edge with matching yarn and weave in the ends."),
]
page("how-to-fix-a-dropped-stitch.html", "How to Fix a Dropped Stitch in Knitting (Even Rows Down) | Purl & Paper",
     "How to fix a dropped stitch in knitting: catch it, ladder it up with a crochet hook in 4 drawings, garter, rib and purl stitches, twisted stitches, after binding off, and when to rip back. Free helper.",
     dsp, ds_faq, "How to fix a dropped stitch", app_name="Dropped stitch helper")

# ---------------- HOW TO PRICE A CROCHET BLANKET (guide + calculator) ----------------
BP_TF = {1: 1.45, 2: 1.35, 3: 1.2, 4: 1, 5: 0.75, 6: 0.6, 7: 0.45}   # our estimate: time vs worsted (gift planner uses 1.3 fine / 0.65 chunky)
BP_TH = 25 / 3000   # crochet hours per sq in in worsted: LoveCrafts' ~25 h for a 50 x 60 in throw (same as the gift planner)
def bp_hours(b, wn, knit=False): return b["w"] * b["l"] * BP_TH * BP_TF[wn] * (2 if knit else 1)
def bp_sk(b, wn, sk=200, knit=False): return _m.ceil(bk_yd(b, wn, 1 if knit else 1.27) / sk)
def bp_mat(b, wn, sk=200, cost=6, extra=3, knit=False): return bp_sk(b, wn, sk, knit) * cost + extra
def bp_price(b, wn, rate=15, oh=0.10, knit=False): return pr_base(bp_mat(b, wn, knit=knit), bp_hours(b, wn, knit), rate, oh)
def _bp_r(x): return f"${round(x / 5) * 5:,.0f}"
BP_IDS = ("lovey", "baby", "lap", "throw", "twin", "queen", "king")
_BPB = {b["id"]: b for b in D["blankets"]}
bp_rows = "".join(f'<tr><th scope="row">{e(_BPB[i]["name"])}<br><span class="muted">{_BPB[i]["w"]} × {_BPB[i]["l"]} in</span></th><td>{bp_hours(_BPB[i], 4):.0f} h</td><td>{bp_sk(_BPB[i], 4)} (${bp_mat(_BPB[i], 4):,.0f})</td>'
                  + "".join(f"<td>{_bp_r(bp_price(_BPB[i], 4, r))}</td>" for r in (12, 15, 20)) + f'<td>{_bp_r(pr_etsy(bp_price(_BPB[i], 4)))}</td><td class="muted">{_bp_r(bp_mat(_BPB[i], 4) * 3)}</td></tr>' for i in BP_IDS)
_bpt = _BPB["throw"]; _bpb = _BPB["baby"]
bp_wrows = "".join(f'<tr><th scope="row">{n}</th><td>{bp_hours(_bpt, k):.0f} h</td><td>{round(bk_yd(_bpt, k, 1.27), -2):,.0f} yd</td><td>{_bp_r(bp_price(_bpt, k))}</td></tr>' for k, n in ((3, "DK"), (4, "Worsted"), (5, "Bulky"), (6, "Super bulky")))
bp_sopts = "".join(f'<option value="{b["id"]}"{" selected" if b["id"] == "throw" else ""}>{e(b["name"])} ({b["w"]} × {b["l"]} in)</option>' for b in D["blankets"]) + '<option value="custom">My own size</option>'
bp_wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"])})</option>' for w in D["weights"] if w["n"] >= 1)
bpp = top("How to price a crochet blanket", "Blankets are the hardest thing to price: lots of yarn and a lot of hours. Pick a size and yarn and this calculator estimates the yarn, the hours and a fair price, and shows why the shortcut formulas leave you working for pennies.", "How to price a crochet blanket") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> price a blanket the same way as anything handmade: <strong>yarn and extras + (hours × your hourly rate)</strong>, plus about 10% for overheads, plus selling fees. A crocheted throw (50 × 60 in) in worsted yarn takes about {bp_sk(_bpt, 4)} skeins of 200 yd and roughly {bp_hours(_bpt, 4):.0f} hours, so at $15 an hour it comes to about <strong>{_bp_r(bp_price(_bpt, 4))}</strong>. A baby blanket is about {_bp_r(bp_price(_bpb, 4))}. Those are fair prices for your time, and higher than many shoppers expect, so chunky yarn and quick stitches are how most blanket sellers bring the price down. Hours and yarn are estimates; time yourself for your own number.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Blanket price calculator</h2>
<div class="field"><label for="bp-size">Blanket size</label><select id="bp-size">{bp_sopts}</select></div>
<div class="row2" id="bp-custom" hidden><div class="field"><label for="bp-w">Width (in)</label><input type="number" id="bp-w" value="50" min="6" max="140" inputmode="decimal"></div><div class="field"><label for="bp-l">Length (in)</label><input type="number" id="bp-l" value="60" min="6" max="140" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><span class="label" id="bp-craft-l">Made with</span><div class="seg" role="group" aria-labelledby="bp-craft-l" id="bp-craft"><button type="button" data-v="crochet" aria-pressed="true">Crochet</button><button type="button" data-v="knit" aria-pressed="false">Knitting</button></div></div>
<div class="field"><label for="bp-weight">Yarn weight</label><select id="bp-weight">{bp_wopts}</select></div></div>
<div class="row2"><div class="field"><label for="bp-sk">Yards per skein</label><input type="number" id="bp-sk" value="200" min="10" step="1" inputmode="numeric"></div>
<div class="field"><label for="bp-cost">Price per skein ($)</label><input type="number" id="bp-cost" value="6" min="0" step="0.01" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="bp-extra">Extras ($)</label><input type="number" id="bp-extra" value="3" min="0" step="0.5" inputmode="decimal"><span class="note">Label, tag, bag or box.</span></div>
<div class="field"><label for="bp-speed">How fast are you?</label><select id="bp-speed"><option value="1.25">Still learning</option><option value="1" selected>Comfortable</option><option value="0.8">Speedy</option></select></div></div>
<div class="row2"><div class="field"><label for="bp-h">Hours to make it</label><input type="number" id="bp-h" min="0.5" max="500" step="0.5" inputmode="decimal" placeholder="we'll estimate"><span class="note" id="bp-h-note">Leave empty to use our estimate.</span></div>
<div class="field"><label for="bp-rate">Your hourly rate ($)</label><input type="number" id="bp-rate" value="15" min="0" step="0.5" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="bp-oh">Overheads (%)</label><input type="number" id="bp-oh" value="10" min="0" max="100" step="1" inputmode="decimal"></div>
<div class="field"><label for="bp-ch">Selling on</label><select id="bp-ch"><option value="etsy">Etsy (US fees)</option><option value="fair">Craft fair (card reader 3%)</option><option value="direct">Direct, no fees</option></select></div></div>
<div class="field"><label for="bp-try">A price you had in mind (optional, $)</label><input type="number" id="bp-try" placeholder="e.g. 120" min="0" step="1" inputmode="decimal"></div>
<figure class="ts-fig"><svg id="bp-svg" viewBox="0 0 300 150" role="img" aria-label="What the price is made of: yarn, your time, overheads and fees"></svg><figcaption class="note" id="bp-cap">Where the money goes.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="bp-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How much should I charge for a crochet blanket?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Blanket</th><th scope="col">Hours</th><th scope="col">Skeins (yarn + extras)</th><th scope="col">At $12/h</th><th scope="col">At $15/h</th><th scope="col">At $20/h</th><th scope="col">On Etsy at $15/h</th><th scope="col">Materials × 3</th></tr></thead><tbody>{bp_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Our estimates for plain crochet in worsted yarn, 200 yd skeins at $6, $3 of extras and 10% overheads, rounded to $5. Hours scale from LoveCrafts' typical 25 hours for a crocheted throw; yarn from our <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>. The Etsy column adds US fees (about 9.5% + $0.45). Time yourself and change the numbers in the calculator.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>What's the formula for pricing a blanket?</h2>
<ol><li><strong>Yarn.</strong> Count whole skeins, not just the yards you used. The Crochet Crowd suggests charging the full ball even if some is left over, since leftovers rarely get used up.</li>
<li><strong>Extras.</strong> Labels, a care tag, a bag or box. Shipping is separate: charge what it costs to post.</li>
<li><strong>Time.</strong> Hours × an hourly rate. B.Hooked suggests starting from your local minimum wage and says many sellers land between $12 and $20 an hour; EyeLoveKnots says never go below your area's minimum wage.</li>
<li><strong>Overheads and fees.</strong> A percentage for tools, photos and trips to the post office, then the shop's or card reader's cut on top.</li></ol>
<p>The full method, with craft fair and consignment fees, is in our guide to <a href="{href("how-to-price-crochet-items.html")}">pricing crochet and knitting items</a>.</p>
<h2>Why does "materials × 3" undercharge for blankets?</h2>
<p>Because a blanket's cost is mostly time. EyeLoveKnots gives the example of $40 of yarn: times 3 is $120, for a blanket that took around 20 hours. That's well under minimum wage before any fees. The last column of the table shows the same thing: the bigger the blanket, the further "materials × 3" falls behind a fair price. Daisy Cottage Designs uses materials × 2 plus labour plus expenses: doubling the yarn covers waste and overheads, and the hours are still paid. She found it gave a far more sellable price than Etsy's suggested method of doubling a wholesale price.</p>
<h2>How long does it take to crochet a blanket?</h2>
<p>It depends on size, yarn and stitch far more than on skill. Sellers' own examples: B.Hooked times a blanket at 15 hours, EyeLoveKnots says about 18 hours each for 60 × 70 in ripple afghans, and The Crochet Crowd uses about 20 hours for an afghan. LoveCrafts' time guide puts a crocheted throw at around 25 hours for an average maker. Knitting usually takes about twice as long. Thicker yarn makes the biggest difference:</p></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Throw, 50 × 60 in, in</th><th scope="col">About</th><th scope="col">Yarn</th><th scope="col">Price at $15/h</th></tr></thead><tbody>{bp_wrows}</tbody></table></div>
<p class="note" style="margin-top:12px">Our estimates, same model as the calculator. Thinner yarn makes smaller stitches, so it takes longer to cover the same area.</p></div>
<div class="narrow prose">
<h2>What do crochet blankets actually sell for?</h2>
<p>Real examples from sellers who've shared their maths: B.Hooked works a 15-hour blanket out at about $237; EyeLoveKnots priced 60 × 70 in afghans at about $215 each plus shipping; The Crochet Crowd's 20-hour afghan example comes to about $300 Canadian. All three say a price like that needs the right buyer, which is why the venue matters: The Crochet Crowd points out the same item sells for far more at a juried craft show than at a church sale.</p>
<h2>What if my price feels too high?</h2>
<ul><li><strong>Make it faster, not cheaper.</strong> Bulky or super bulky yarn and a simple stitch can cut the hours by a third or more (see the table above).</li>
<li><strong>Make it smaller.</strong> Loveys, baby and lap blankets reach a price more shoppers will pay.</li>
<li><strong>Sell to buyers who value handmade.</strong> Gift buyers, baby showers and custom orders, rather than competing with shop-bought throws.</li>
<li><strong>Don't drop your hourly rate to nothing.</strong> A blanket that sells for the cost of the yarn has cost you 20 hours.</li></ul>
<h2>How do I price a custom or commission blanket?</h2>
<ul><li><strong>Time a sample first.</strong> EyeLoveKnots works up a sample of the stitch and times it before giving a quote.</li>
<li><strong>Get paid before you buy yarn.</strong> B.Hooked and EyeLoveKnots both take payment up front for custom orders.</li>
<li><strong>Give a finish date</strong> and stick to it; Daisy Cottage Designs suggests promising a little less than you can do.</li>
<li><strong>Never charge more than the quote.</strong> If you underestimated, that's the lesson for the next one (EyeLoveKnots).</li>
<li><strong>Charge for changes.</strong> Our tip: a different size or colour change after you start is new work, so quote it.</li></ul>
<p>What next? Work out the size and yarn with the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>, see how long it'll take alongside your other makes in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>, and if you're selling at a market, pack with our <a href="{href("craft-fair-checklist.html")}">craft fair checklist</a>. Making it from squares? Use the <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> for the yarn.</p></div></section>'''
bp_faq = [
    ("How much should I charge for a crochet blanket?", f"Add the yarn and extras, your hours times an hourly rate, about 10% for overheads, then the selling fees. For a worsted throw (about {bp_hours(_bpt, 4):.0f} hours and {bp_sk(_bpt, 4)} skeins) at $15 an hour that's roughly {_bp_r(bp_price(_bpt, 4))}. Faster makers and chunky yarn bring it down."),
    ("How much should I charge for a crochet baby blanket?", f"Roughly {_bp_r(bp_price(_bpb, 4, 12))} to {_bp_r(bp_price(_bpb, 4, 20))} for a 36 in square blanket in worsted yarn at $12 to $20 an hour, by our estimate of about {bp_hours(_bpb, 4):.0f} hours. Chunky yarn or a smaller size gets it lower."),
    ("How many hours does it take to crochet a blanket?", "Sellers report about 15 to 20 hours for an afghan, and LoveCrafts puts a throw at around 25 hours. Bulky yarn is faster, fine yarn slower, and knitting takes about twice as long."),
    ("Is materials times 3 a good way to price a blanket?", "No. A blanket's cost is mostly time, so materials times 3 can pay you only a few dollars an hour. Add your hours times an hourly rate instead."),
    ("Should I charge for the whole skein?", "Most sellers do. The Crochet Crowd suggests charging the full ball price even if some is left, since small leftovers are hard to use."),
    ("How do I price a custom blanket order?", "Time a sample of the stitch, quote yarn plus hours at your rate, take payment before you buy the yarn, give a finish date and don't charge more than you quoted."),
]
page("how-to-price-a-crochet-blanket.html", "How to Price a Crochet Blanket (Free Blanket Price Calculator) | Purl & Paper",
     "How much to charge for a crochet blanket: a free calculator for yarn, hours and a fair price by size, a price chart from baby to king, how long blankets take, and pricing custom orders.",
     bpp, bp_faq, "How to price a crochet blanket", app_name="Crochet blanket price calculator")

# ---------------- HOW TO KNIT IN THE ROUND (guide + needle length finder) ----------------
KR_LEN = [(9, 23), (12, 30), (16, 40), (24, 60), (32, 80), (40, 100), (47, 120), (60, 150)]
def kr_pick(c):   # our rule: longest common circular <= circumference (+10% for small stretchy tubes)
    ok = [l for l, _ in KR_LEN if l <= (c * 1.1 if c < 12 else c)]
    return ok[-1] if ok else None
def _kr_pt(t, r=58, cx=110, cy=96):
    a = _m.radians(t - 90); return cx + r * _m.cos(a), cy + r * _m.sin(a)
def _kr_ring(step):
    g = ""
    # cable: arc from 28 deg round the bottom to 332 deg
    x1, y1 = _kr_pt(28); x2, y2 = _kr_pt(332)
    g += f'<path d="M{x1:.1f} {y1:.1f} A58 58 0 1 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{_HK}" stroke-width="2.5"/>'
    # tips
    for t, dx in ((28, 1), (332, -1)):
        x, y = _kr_pt(t)
        g += _needle(x, y, x + dx * 22, y - 34)
    # stitches round the cable
    for t in range(40, 330, 18):
        x, y = _kr_pt(t)
        g += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="4.5" ry="7.5" transform="rotate({t} {x:.1f} {y:.1f})" fill="none" stroke="{_Y}" stroke-width="2.6"/>'
    if step >= 2:   # cast-on edge on the inside, all the way round
        xa, ya = _kr_pt(40, 47); xb, yb = _kr_pt(320, 47)
        g += f'<path d="M{xa:.1f} {ya:.1f} A47 47 0 1 1 {xb:.1f} {yb:.1f}" fill="none" stroke="{_TL}" stroke-width="3" stroke-dasharray="{"0" if step == 2 else "5 4"}"/>'
    if step == 2:
        g += f'<text x="110" y="100" text-anchor="middle" font-size="11" fill="{_TL}" font-weight="700">edge on the</text><text x="110" y="113" text-anchor="middle" font-size="11" fill="{_TL}" font-weight="700">inside all round</text>'
    if step >= 3:   # marker on the right tip
        x, y = _kr_pt(28)
        g += f'<circle cx="{x + 9:.1f}" cy="{y - 14:.1f}" r="6" fill="none" stroke="{_MG}" stroke-width="4"/>'
        if step == 3: g += f'<text x="{x + 20:.1f}" y="{y - 22:.1f}" font-size="11" fill="{_HK}">marker</text>'
    if step == 4:   # working yarn from the right tip to the first stitch on the left
        xr, yr = _kr_pt(28); xl, yl = _kr_pt(332)
        g += f'<path d="M{xr + 4:.1f} {yr - 4:.1f} C{xr + 30:.1f} {yr - 30:.1f} {xr + 40:.1f} {yr + 40:.1f} {xr + 70:.1f} {yr + 30:.1f}" fill="none" stroke="{_Y2}" stroke-width="3" stroke-linecap="round"/>'
        g += f'<path d="M{xr - 6:.1f} {yr - 18:.1f} Q110 {yr - 52:.1f} {xl + 8:.1f} {yl - 18:.1f}" fill="none" stroke="{_HK}" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#kr-ar)"/>'
        g += f'<text x="{xr + 18:.1f}" y="{yr + 58:.1f}" text-anchor="middle" font-size="11" fill="{_HK}">working yarn</text>'
    return '<defs><marker id="kr-ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#1f2a44"/></marker></defs>' + g
KR_STEPS = [
    ("Cast on and spread out.", "Cast on all your stitches, then slide them round onto the cable so they reach both tips without stretching."),
    ("Check for a twist.", "Lay it flat. The cast-on edge should sit on the inside of the ring the whole way round, never looping over the cable."),
    ("Place a marker.", "Hold the tip with the working yarn in your right hand and slip a stitch marker onto it. That's the start of every round."),
    ("Knit the first stitch.", "With the working yarn (not the tail), knit the first stitch on the left tip and pull it snug. Knit round to the marker: one round done."),
]
def kr_fig(i, s):
    return (f'<figure class="mr-step"><svg viewBox="0 0 220 172" role="img" aria-label="Knitting in the round step {i}: {e(s[0])}">{_kr_ring(i)}</svg>'
            f'<figcaption><strong>{i}. {e(s[0])}</strong> {e(s[1])}</figcaption></figure>')
KR_USE = [(9, "Socks, mittens, sleeves, baby hats"), (12, "Socks and sleeves for some knitters; not every brand makes it"),
          (16, "Adult hats, neck-warmer cowls, armhole and neck trims"), (24, "Kids' sweaters, the start of a top-down sweater, shawl starts, medium cowls"),
          (32, "Adult sweater bodies, shawls, infinity cowls, baby blankets, magic loop"), (40, "Bigger sweaters, blankets, magic loop"),
          (47, "Big blankets and wide shawls"), (60, "Very large blankets and borders")]
kr_rows = "".join(f'<tr><td><strong>{l} in ({cm} cm)</strong></td><td>About {l} in ({cm} cm) or more</td><td>{e(u)}</td></tr>' for (l, cm), (_, u) in zip(KR_LEN, KR_USE))
KR_PROJ = [("Sock (adult)", 8.5), ("Mitten or sleeve cuff", 8), ("Baby hat", 15), ("Child hat", 18), ("Adult hat", 21), ("Cowl", 24), ("Child sweater", 28), ("Adult sweater body", 40), ("Big sweater body", 50)]
kr_prows = "".join(f'<tr><td><strong>{e(n)}</strong></td><td>{c:g} in ({c * 2.54:.0f} cm)</td><td>{kr_pick(c) or "None"}{" in" if kr_pick(c) else ""}</td><td>{"Magic loop (32 in or longer), DPNs or two circulars" if c < 12 else "Magic loop or DPNs when the crown or cuff gets small" if c < 30 else "Magic loop for the sleeves"}</td></tr>' for n, c in KR_PROJ)
KR_JOIN = [("Plain join", "Knit the first cast-on stitch with the working yarn and pull it snug.", "Most projects; it's what patterns mean by \"join\""),
           ("Swap the end stitches", "Slip the first stitch from the left tip to the right, lift the stitch next to it over and onto the left tip, then start knitting.", "A tighter, neater join"),
           ("Extra stitch", "Cast on one more stitch than you need, slip it to the left tip, then knit it together with the first stitch.", "A firm join with no gap"),
           ("Knit one row first", "Knit one row flat, then join and knit in the round. Sew the tiny gap with the cast-on tail when you weave in.", "Lots of stitches, or if twists keep catching you out")]
krp = top("How to knit in the round", "Hats, cowls, socks and sweater bodies are knitted in a tube with no seam. Here's how to join without twisting in four drawings, which circular needle length you need, and a finder that picks the needle for your project.", "How to knit in the round") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> cast on onto a <strong>circular needle shorter than your project's circumference</strong> (a 16 in / 40 cm circular for an adult hat), spread the stitches round the cable and check the cast-on edge sits on the <strong>inside of the ring with no twist</strong>. Put a marker on the right tip, then knit the first stitch on the left tip with the working yarn and pull it snug. Knitting every round makes stockinette. For socks, sleeves and hat crowns too small for any circular, use magic loop on a 32 in (80 cm) or longer needle, or double-pointed needles.</div>
<div class="mr-steps">{"".join(kr_fig(i + 1, s) for i, s in enumerate(KR_STEPS))}</div>
<p class="note">Our own drawings of a circular needle seen from above.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Circular needle length finder</h2>
<div class="field"><span class="label" id="kr-mode-l">I know</span><div class="seg" role="group" aria-labelledby="kr-mode-l" id="kr-mode"><button type="button" data-v="size" aria-pressed="true">The size around</button><button type="button" data-v="sts" aria-pressed="false">My stitch count</button></div></div>
<div class="field"><span class="label" id="kr-unit-l">Units</span><div class="seg" role="group" aria-labelledby="kr-unit-l" id="kr-unit"><button type="button" data-v="in" aria-pressed="true">Inches</button><button type="button" data-v="cm" aria-pressed="false">cm</button></div></div>
<div id="kr-size-f"><div class="field"><label for="kr-proj">What are you making?</label><select id="kr-proj">{"".join(f'<option value="{c}"{" selected" if n == "Adult hat" else ""}>{e(n)}</option>' for n, c in KR_PROJ)}<option value="own">My own measurement</option></select></div>
<div class="field"><label for="kr-c" id="kr-c-l">Size around (in)</label><input id="kr-c" type="number" min="3" max="200" step="0.5" value="21" inputmode="decimal"><span class="note">The finished circumference, before any shaping.</span></div></div>
<div id="kr-sts-f" hidden><div class="row2"><div class="field"><label for="kr-n">Stitches cast on</label><input id="kr-n" type="number" min="8" max="2000" step="1" value="96" inputmode="numeric"></div>
<div class="field"><label for="kr-g" id="kr-g-l">Stitches per 4 in</label><input id="kr-g" type="number" min="4" max="60" step="0.5" value="20" inputmode="decimal"><span class="note">Your gauge, from the ball band or swatch.</span></div></div></div>
<figure class="ts-fig"><svg id="kr-svg" viewBox="0 0 300 220" role="img" aria-label="Your project's size around compared with the needle"></svg><figcaption class="note" id="kr-cap">Your project (pink) and the needle (gold), to scale.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="kr-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>What length circular needle do I need?</h2>
<p>Pick a circular that is <strong>shorter than the circumference</strong> of what you're knitting, so the stitches reach from tip to tip without stretching (Knit Picks). Length is measured from tip to tip, not just the cable (Elizabeth Smith Knits). A needle that's a bit short is fine: the stitches bunch up on the cable. One that's too long stretches them and they won't meet.</p></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Circular needle</th><th scope="col">For a circumference of</th><th scope="col">Good for</th></tr></thead><tbody>{kr_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Uses from Elizabeth Smith Knits' guide to circular lengths; the 12, 47 and 60 in rows and the cm sizes are our own summary of common sizes sold. Some brands sell 29 in instead of 32 in, which works the same.</p>
<h2 style="margin-top:28px">Which needle for a hat, sock or sweater?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Project</th><th scope="col">Typical size around</th><th scope="col">Circular to start</th><th scope="col">Also need</th></tr></thead><tbody>{kr_prows}</tbody></table></div>
<p class="note" style="margin-top:12px">Sizes are typical adult and child measurements, rounded (see our <a href="{href("hat-size-chart.html")}">hat size chart</a> and <a href="{href("sock-size-chart.html")}">sock size chart</a>). Needle picked by our rule: the longest common length no longer than the circumference (up to about 10% longer for socks and sleeves, which stretch).</p></div>
<div class="narrow prose">
<h2>How do you join in the round without twisting?</h2>
<p>Before the first stitch, lay the needle flat and run your finger along the cast-on edge. It should sit on the <strong>inside of the ring</strong> (or all along the bottom of the needle) the whole way round, never spiralling over the cable (Knit Picks). Then join with the working yarn. If counting a long cast-on gets confusing, Cocoknits knits one row flat first: a flat row makes the edge easy to see, and the small gap is sewn shut with the tail later.</p>
<h2>What are the ways to join?</h2></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Join</th><th scope="col">How</th><th scope="col">Best for</th></tr></thead><tbody>
{"".join(f"<tr><td><strong>{e(a)}</strong></td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in KR_JOIN)}</tbody></table></div>
<p class="note" style="margin-top:12px">Plain join from Knit Picks and Berroco; knit-a-row-first from Cocoknits; swap and extra-stitch joins are common methods also mentioned by Berroco readers.</p></div>
<div class="narrow prose">
<h2>I twisted my join. Can I fix it?</h2>
<p>If you haven't knitted a full round yet, spin the stitches round the needle until the edge lies flat on the inside, then join (Berroco). Once you've knitted a round or more, the twist is locked in: Knit Picks says it can't be corrected later, so rip back and cast on again. (A twisted tube becomes a Möbius loop, which some knitters make on purpose for cowls, but not for a hat.)</p>
<h2>How do I close the gap at the join?</h2>
<p>A little ladder at the join is normal. Our tips: pull the first two or three stitches snug, or use the swap or extra-stitch join above. Any gap left over is closed when you weave in the cast-on tail: take it across the gap to the stitch on the other side, then weave it in as in our <a href="{href("how-to-weave-in-ends.html")}">weaving in ends</a> guide.</p>
<h2>What if my project is smaller than any circular?</h2>
<p>Socks, mittens, sleeves and the top of a hat get too small for even a 16 in needle. You have three choices:</p>
<ul><li><strong>Magic loop:</strong> one long circular, 32 in (80 cm) or 40 in (100 cm), with the extra cable pulled out as a loop at two points so half the stitches sit on each tip.</li>
<li><strong>Double-pointed needles (DPNs):</strong> the stitches are shared over 3 or 4 short needles and you knit with a spare one.</li>
<li><strong>Two circulars:</strong> half the stitches on each needle, each knitted with its own tips.</li></ul>
<p>For a hat, start on a 16 in circular and change to magic loop or DPNs when the crown decreases make the stitches stretch.</p>
<h2>Is knitting in the round the same as knitting flat?</h2>
<p>The stitches are the same, but you never turn the work, so the right side always faces you. That changes some stitch patterns:</p>
<ul><li><strong>Stockinette:</strong> knit every round (flat, you knit one row and purl the next).</li>
<li><strong>Garter stitch:</strong> knit one round, purl one round.</li>
<li><strong>Rib:</strong> knit the knits and purl the purls, every round. The stitch count must be a multiple of the rib (4 for k2, p2).</li></ul>
<p>Rounds spiral, so stripes show a small step at the start of the round. Our tip for a neater stripe: on the second round of a new colour, slip the first stitch purlwise, then knit on. Keep count of rounds with the <a href="{href("row-counter.html")}">row counter</a>.</p>
<p>What next? Work out the stitches with the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> or the <a href="{href("hat-size-chart.html")}">hat size calculator</a>, learn the <a href="{href("how-to-cast-on-knitting.html")}">long-tail cast on</a>, and finish the brim with a stretchy edge from our <a href="{href("how-to-bind-off-knitting.html")}">bind off guide</a>. Adding a neckband or button band? See <a href="{href("how-to-pick-up-stitches-knitting.html")}">how to pick up stitches</a>.</p></div></section>'''
kr_faq = [
    ("How do you join knitting in the round?", "Cast on onto a circular needle shorter than the project, spread the stitches round the cable and check the cast-on edge sits on the inside with no twist. Place a marker on the right tip, then knit the first stitch on the left tip with the working yarn and pull it snug."),
    ("What size circular needle do I need for a hat?", "A 16 inch (40 cm) circular for an adult or child hat. Change to magic loop or double-pointed needles when the crown gets too small. A 24 inch needle is too long for most hats."),
    ("Can I knit a hat on a 24 inch circular needle?", "Usually not. Most adult hats are about 20 to 22 inches around, shorter than the needle, so the stitches won't stretch round it. Use a 16 inch circular, or magic loop on a 32 inch or longer needle."),
    ("How do I fix a twisted join in the round?", "If you haven't knitted a full round, spin the stitches until the edge lies flat on the inside and then join. After a full round the twist can't be undone, so rip back and cast on again."),
    ("How do you knit stockinette in the round?", "Knit every round. Because you never turn the work, the right side always faces you, so there are no purl rows."),
    ("What is magic loop?", "A way to knit a small tube on one long circular needle (32 in / 80 cm or longer): the extra cable is pulled out as a loop at two points so half the stitches sit on each tip."),
]
page("how-to-knit-in-the-round.html", "How to Knit in the Round: Join Without Twisting + Needle Length Finder | Purl & Paper",
     "How to knit in the round on circular needles: join without twisting in 4 drawings, which circular needle length for hats, socks and sweaters, magic loop and DPNs, fixing a twisted join. Free needle length finder.",
     krp, kr_faq, "How to knit in the round", app_name="Circular needle length finder")

# ---------------- JUNK JOURNAL SUPPLY CHECKLIST ----------------
# (name, tier: free/basic/extra, what it's for, free swap)
JS = [
 ("The journal itself", "base", [
   ("Paper for the pages", "free", "Printer paper, old book pages, envelopes, brown paper bags, wrapping paper, maps or sheet music.", "Anything paper you'd recycle"),
   ("A cover", "free", "An old hardback book cover, a cereal box covered in paper, or a folded piece of card.", "Cereal box or old book"),
   ("Thread or string", "free", "To sew the folded pages in. Embroidery floss, waxed thread, twine or strong string.", "String or dental floss"),
   ("A big-eye needle", "basic", "A tapestry or bookbinding needle to sew the pages. Pricker for holes optional.", "A stapler for small booklets"),
   ("Something to poke holes", "free", "An awl, a push pin or a thick needle for the sewing holes.", "A push pin"),
 ]),
 ("Cutting and folding", "tools", [
   ("Scissors", "free", "Everyday scissors do almost everything.", ""),
   ("Ruler and pencil", "free", "Measure pages and mark folds and hole positions.", ""),
   ("Bone folder", "extra", "Makes crisp, flat folds.", "The back of a spoon"),
   ("Paper trimmer", "extra", "Fast, straight cuts on lots of paper.", "Ruler and scissors"),
   ("Craft knife and mat", "extra", "Windows, slots and tiny cuts.", "Small scissors"),
   ("Hole punch", "extra", "Holes for tags and ribbon.", "A push pin and a pencil"),
 ]),
 ("Sticking things down", "glue", [
   ("Glue stick", "basic", "The everyday adhesive for paper on paper. Least likely to wrinkle thin pages.", "School glue spread thin"),
   ("Liquid or tacky glue", "basic", "Heavier things: fabric, lace, buttons, card.", ""),
   ("Double-sided tape", "extra", "Clean, flat and instant. Tape runners are the easy version.", "Glue stick"),
   ("Washi tape", "basic", "Sticks and decorates at once, and lifts off again.", "Strips of paper and glue"),
   ("Paper clips and bulldog clips", "free", "Hold layers while glue dries, or clip on extras.", ""),
 ]),
 ("Ephemera and pretty things", "deco", [
   ("Tickets, receipts and labels", "free", "The everyday paper that tells the story of a day.", ""),
   ("Postcards, cards and envelopes", "free", "Envelopes become pockets; cards become tuck-ins.", ""),
   ("Tags", "free", "Cut from card with the top corners snipped.", "Cut your own from a cereal box"),
   ("Ribbon, lace, string and trims", "free", "From gift wrap, clothes and packaging.", ""),
   ("Buttons and fabric scraps", "free", "Texture on covers and pages.", ""),
   ("Pressed flowers and leaves", "free", "Press them in a heavy book for a week or two.", ""),
   ("Stickers", "extra", "Quick focal points and labels.", "Cut motifs from magazines"),
   ("Printables", "extra", "Journaling cards, ephemera sheets and full kits to print at home.", "Free printables"),
 ]),
 ("Colour, ageing and writing", "colour", [
   ("Pens", "free", "Any pen for journaling; a fine black pen for labels.", ""),
   ("Tea or coffee", "free", "For staining paper an antique brown.", ""),
   ("Coloured pencils or crayons", "free", "Colour, edges and rubbings.", ""),
   ("Ink pad", "extra", "Ink the edges of paper to age them, and use with stamps.", "Rub a tea bag or brown crayon on the edges"),
   ("Stamps", "extra", "Repeat patterns, dates and words.", "Cut a stamp from a potato or eraser"),
   ("Watercolours or paint", "extra", "Washes of colour behind journaling.", "Tea, coffee or watered-down crayon"),
 ]),
]
JS_N = sum(len(x[2]) for x in JS)
JS_TIER = {"free": "Free from home", "basic": "Worth buying first", "extra": "Nice to have"}
def _js_id(t): return "".join(c if c.isalnum() else "-" for c in t.lower()).strip("-")[:40]
js_list = "".join(f'<fieldset class="ep-grp sheet" data-g="{gid}"><legend>{e(gn)} <span class="muted ep-gc" data-g="{gid}"></span></legend><ul>' +
                  "".join(f'<li data-t="{t}"><label><input type="checkbox" data-id="{gid}-{_js_id(n)}" data-n="{e(n)}" data-t="{t}" data-s="{e(sw) if t != "free" else ""}"> <strong>{e(n)}</strong> <span class="js-tier js-{t}">{JS_TIER[t]}</span></label><span>{e(d)}{(" Free swap: " + e(sw[0].lower() + sw[1:]) + ".") if sw and t != "free" else ""}</span></li>' for n, t, d, sw in items) + "</ul></fieldset>"
                  for gn, gid, items in JS)
js_counts = {k: sum(1 for g in JS for it in g[2] if it[1] == k) for k in JS_TIER}
# own printable: a pocket and 3 tags with cut lines
def _js_tag(x, y, w, h, word):
    c = 14
    return (f'<path d="M{x + c} {y} H{x + w - c} L{x + w} {y + c} V{y + h} H{x} V{y + c} Z" fill="#f6efe2" stroke="#1f2a44" stroke-width="1.4" stroke-dasharray="6 4"/>'
            f'<circle cx="{x + w / 2}" cy="{y + 22}" r="6" fill="#fff" stroke="#1f2a44" stroke-width="1.2"/>'
            + "".join(f'<line x1="{x + 14}" y1="{yy}" x2="{x + w - 14}" y2="{yy}" stroke="#b8326a" stroke-width=".8" opacity=".5"/>' for yy in range(y + 70, y + h - 10, 22))
            + f'<text x="{x + w / 2}" y="{y + 52}" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="17" fill="#1f2a44">{word}</text>')
JS_TPL = ('<svg id="js-tpl" viewBox="0 0 612 792" role="img" aria-label="Printable template: a pocket and three tags with dashed cut lines" style="background:#fff">'
          '<text x="306" y="44" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="24" fill="#1f2a44">Pocket and tags</text>'
          '<text x="306" y="66" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#4a5470">Cut on the dashed lines, fold on the dotted ones. Print on card or tea-stain it first. Free from purlandpaperco.com</text>'
          + _js_tag(46, 96, 150, 300, "Today") + _js_tag(231, 96, 150, 300, "Found") + _js_tag(416, 96, 150, 300, "Keep")
          + '<rect x="96" y="440" width="420" height="300" fill="#fbe1a6" stroke="#1f2a44" stroke-width="1.4" stroke-dasharray="6 4"/>'
          '<path d="M96 440 h-34 v300 h34 M516 440 h34 v300 h-34 M96 740 v30 h420 v-30" fill="#f6efe2" stroke="#1f2a44" stroke-width="1.4" stroke-dasharray="6 4"/>'
          '<path d="M96 440 V740 M516 440 V740 M96 740 H516" stroke="#1f2a44" stroke-width="1" stroke-dasharray="1 4"/>'
          '<path d="M96 440 Q306 500 516 440" fill="none" stroke="#b8326a" stroke-width="1.4" stroke-dasharray="6 4"/>'
          '<text x="306" y="620" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="26" fill="#1f2a44">Little things</text>'
          '<text x="79" y="600" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#4a5470" transform="rotate(-90 79 600)">glue flap</text>'
          '<text x="533" y="600" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#4a5470" transform="rotate(90 533 600)">glue flap</text>'
          '<text x="306" y="760" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#4a5470">glue flap</text></svg>')
jsp = top("Junk journal supply checklist", f"Everything you need to start a junk journal, and the {js_counts['free']} things you probably already have at home. Tick what you've got, pick a budget and get a short shopping list, plus a free pocket and tag template to print.", "Junk journal supply checklist") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> to start a junk journal you need <strong>paper, a cover, something to stick with, scissors and thread (or a stapler)</strong> to bind it. That's it: Stampin' Up's starter list is paper, scissors or a trimmer, adhesive, pens and ephemera. Most of it is free from home: old envelopes, book pages, cereal boxes, receipts and tickets. If you buy anything first, make it a good <strong>glue stick, washi tape and a big-eye needle</strong>. Ink pads, stamps, stickers and printables are extras you can add later.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div>
<div class="toolbar"><strong id="js-count" aria-live="polite">0 of {JS_N} ticked</strong><span class="spacer"></span><button type="button" class="btn ghost" id="js-print">Print my list</button><button type="button" class="linkbtn" id="js-clear">Clear ticks</button></div>
<p class="note" style="margin:0 0 12px">Tick what you already have. Your ticks stay on this device.</p>
<div class="ep-list" id="js-list">{js_list}</div>
</div>
<div class="result" aria-live="polite">
<h3>Your plan</h3>
<div class="field"><span class="label" id="js-plan-l" style="color:inherit">I want to</span><div class="seg" role="group" aria-labelledby="js-plan-l" id="js-plan"><button type="button" data-v="free" aria-pressed="false">Start free</button><button type="button" data-v="basic" aria-pressed="true">Buy the basics</button><button type="button" data-v="extra" aria-pressed="false">Get everything</button></div></div>
<div id="js-out"></div>
</div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>What supplies do I need to start a junk journal?</h2>
<p>Only five things are must-haves: <strong>paper, a cover, an adhesive, scissors and a way to bind it</strong> (thread and a needle, or a stapler for a thin booklet). Stampin' Up's list of basics is paper, a trimmer or scissors, adhesive, pens or markers, and ephemera, with stamps, ink, ribbon and embellishments as add-ons. 101 Planners groups supplies the same way: paper, ephemera, decorations, writing tools and adhesives.</p>
<h2>What can I use for free?</h2>
<ul><li><strong>Pages:</strong> printer paper, old book and magazine pages, envelopes, wrapping paper, brown bags, maps and sheet music.</li>
<li><strong>Cover:</strong> the cover of a worn-out hardback, or a cereal box covered with paper or fabric.</li>
<li><strong>Ephemera:</strong> receipts, tickets, tags, labels, postcards, packaging, napkins and stamps from your post (101 Planners). Our <a href="{href("junk-journal-ephemera-ideas.html")}">62 ephemera ideas</a> has a list to tick off.</li>
<li><strong>Decoration:</strong> ribbon and lace from gift wrap, buttons, fabric scraps, and pressed leaves and flowers.</li>
<li><strong>Ageing:</strong> a cup of tea. Our <a href="{href("how-to-tea-stain-paper.html")}">tea staining guide</a> shows how.</li></ul>
<h2>What's worth buying first?</h2>
<p>Our picks for a small first shop: a <strong>glue stick</strong> (dries flat on thin paper), a <strong>tacky glue</strong> for lace and buttons, a roll or two of <strong>washi tape</strong>, and a <strong>big-eye needle</strong> for sewing signatures. A <strong>bone folder</strong> and an <strong>ink pad</strong> are the next most useful. 101 Planners suggests paper of about 100 gsm or more if you'll write or paint on the pages, so ink doesn't show through.</p>
<h2>What glue is best for a junk journal?</h2>
<ul><li><strong>Glue stick:</strong> paper on paper. Thin, flat and quick.</li>
<li><strong>Tacky or liquid glue:</strong> fabric, lace, buttons and heavy card. Use a thin layer so pages don't buckle.</li>
<li><strong>Double-sided tape or a tape runner:</strong> instant and flat, good for photos and pockets.</li>
<li><strong>Glue dots:</strong> small heavy things like buttons and charms.</li></ul>
<p>Our tip: put heavy pages under a book while they dry so they stay flat.</p>
<h2>How do I bind the pages?</h2>
<p>Fold a few sheets in half, nest them together into a "signature", poke 3 or 5 holes along the fold and sew through them into the cover. Our <a href="{href("junk-journal-signature-calculator.html")}">signature calculator</a> works out how many sheets, where the holes go and how much thread you need. For a first try, a thin booklet stapled down the middle works too.</p>
<h2>Free pocket and tag template</h2>
<p>Our own design: one pocket and three tags with cut and fold lines. Print it on card, or on plain paper and tea-stain it, then tuck the tags into the pocket.</p></div>
<div class="narrow"><div class="sheet js-tpl-wrap">{JS_TPL}<div class="toolbar" style="margin-top:12px"><button type="button" class="btn gold" id="js-tpl-print">Print the template</button></div></div></div>
<div class="narrow prose"><p>Want more free printables? Sign up below for our free sampler with journaling cards and a vintage ephemera sheet. New to all of this? Start with <a href="{href("junk-journal-beginners.html")}">junk journaling for beginners</a>, then grab an idea from the <a href="{href("journal-prompts.html")}">journal prompt generator</a>.</p></div></section>'''
js_faq = [
    ("What supplies do I need to start a junk journal?", "Paper, a cover, an adhesive such as a glue stick, scissors, and thread and a needle (or a stapler) to bind it. Ephemera like tickets and receipts, washi tape and pens are the next things to gather."),
    ("Can I make a junk journal for free?", "Yes. Use printer paper, envelopes and old book pages for the pages, a cereal box or old book cover, string to sew it, and receipts, tickets and packaging as ephemera."),
    ("What is the best glue for junk journals?", "A glue stick for paper on paper, tacky glue for fabric, lace and buttons, and double-sided tape or glue dots for instant, flat hold."),
    ("What paper is best for junk journal pages?", "Any paper works, and mixing types is part of the look. For pages you'll write or paint on, paper of about 100 gsm or heavier stops ink showing through."),
    ("Do I need a sewing needle to make a junk journal?", "A big-eye tapestry or bookbinding needle is easiest for sewing signatures. For a thin first journal you can staple the fold instead."),
    ("Where are my ticks saved?", "On this device, in your browser. Nothing is uploaded. Use 'Print my list' to keep a paper copy."),
]
page("junk-journal-supply-checklist.html", "Junk Journal Supply Checklist: What You Need (Mostly Free) | Purl & Paper",
     f"Junk journal supplies for beginners: a {JS_N}-item checklist of what you need, what's free at home and what to buy first, best glue and paper, how to bind, plus a free printable pocket and tag template.",
     jsp, js_faq, "Junk journal supply checklist", app_name="Junk journal supply checklist")

# ---------------- HOW TO PICK UP STITCHES (guide + pick up calculator) ----------------
def _pu_fab(step):
    """Side edge of stockinette: 5 columns x 8 rows, edge column on the right. Needle along the right edge."""
    o = '<rect x="14" y="14" width="150" height="148" rx="8" fill="#f2e6cf"/>'
    ys = [30 + k * 17.5 for k in range(8)]
    for c in range(5):
        x = 36 + c * 24
        for y in ys:
            o += _kst(x, y + 6, _Y2 if c < 4 else _Y, 2.4 if c < 4 else 3)
    gx = 144   # the gap between the edge column and the next one
    if step == 1:
        o += f'<line x1="{gx}" y1="20" x2="{gx}" y2="160" stroke="{_TL}" stroke-width="3" stroke-dasharray="5 4"/>'
        o += _LBL(170, 40, "pick up") + _LBL(170, 54, "in this gap")
        o += f'<path d="M168 66 q-10 6 -20 6" fill="none" stroke="{_TL}" stroke-width="2" marker-end="none"/>'
    picked = {2: [], 3: [0], 4: [0, 1, 2, 4, 5, 6]}.get(step, [])
    if step >= 2:
        o += _needle(196, 12, 196, 166)
        for k in picked:
            y = ys[k] + 6
            o += (f'<path d="M{gx} {y} L190 {y}" stroke="{_TL}" stroke-width="2.6" stroke-linecap="round"/>'
                  f'<ellipse cx="196" cy="{y}" rx="9" ry="5.5" fill="none" stroke="{_TL}" stroke-width="3"/>')
    if step == 2:
        y = ys[0] + 6
        o += (f'<line x1="{gx - 4}" y1="{y + 2}" x2="186" y2="{y - 8}" stroke="{_ND}" stroke-width="6" stroke-linecap="round"/>'
              f'<path d="M206 {y - 22} C214 {y - 8} 200 {y + 2} 188 {y - 6}" fill="none" stroke="{_TL}" stroke-width="3" stroke-linecap="round"/>')
        o += _LBL(89, 175, "needle in, yarn round", "middle")
    if step == 3:
        o += _LBL(89, 175, "one loop = one stitch", "middle")
    if step == 4:
        y = ys[3] + 6
        o += f'<text x="172" y="{y + 4}" font-size="13" fill="{_Y}" font-weight="700" text-anchor="middle">×</text>'
        o += _LBL(89, 175, "3 picked up, 1 row skipped", "middle")
    return o
PU_STEPS = [
    ("Find the gap", "Right side facing you, look along the edge. You'll pick up between the edge stitch and the stitch next to it, one full stitch in.", _pu_fab(1)),
    ("Needle in, yarn round", "Push the needle tip through the gap from front to back, wrap the working yarn round it as if to knit.", _pu_fab(2)),
    ("Pull a loop through", "Draw the loop to the front. That loop is your first picked-up stitch, sitting on the needle.", _pu_fab(3)),
    ("Repeat, skipping a row now and then", "Work down the edge. For the usual 3 for 4 rows, pick up in 3 rows and skip the 4th, so the band doesn't ripple.", _pu_fab(4)),
]
def pu_fig(i, s):
    return (f'<figure class="mr-step"><svg viewBox="0 0 220 180" role="img" aria-label="Picking up stitches step {i}: {e(s[0])}">{s[2]}</svg>'
            f'<figcaption><strong>{i}. {e(s[0])}</strong> {e(s[1])}</figcaption></figure>')
def pu_rib(n, mult, extra):   # nearest count that fits mult*k + extra
    k = max(1, round((n - extra) / mult)); return mult * k + extra
PU_ROWS = [20, 40, 60, 80, 100, 120, 150, 200]
pu_rows = "".join(f'<tr><th scope="row">{r} rows</th><td>{round(r * 3 / 4)}</td><td>{round(r * 2 / 3)}</td><td>{r // 2}</td><td>{pu_rib(round(r * 3 / 4), 4, 2)}</td></tr>' for r in PU_ROWS)
PU_TAB = [
    ("Side edge of stockinette, rib or seed", "3 stitches for every 4 rows (or 2 for every 3)", "Wikipedia, Knotions, Purl Soho, Interweave"),
    ("Side edge of garter stitch", "1 stitch per garter ridge (1 for every 2 rows)", "Wikipedia, Purl Soho"),
    ("Cast on or bound off edge", "1 stitch in every stitch", "Wikipedia, Knotions, Quince & Co."),
    ("Neckline curve or diagonal", "Each part on its own: 1 per stitch on flat parts, 3 for 4 rows on straight sides, between those on slopes", "Interweave, Purl Soho"),
    ("Loose or wide-gauge edge", "Try 4 for every 5 rows if 3 for 4 looks gappy", "LoveCrafts, Purl Soho"),
]
pup = top("How to pick up stitches in knitting", "Picking up stitches adds a new piece of knitting straight onto an edge, for a neckband, a button band or a border, with no sewing. Here's how in four drawings, the usual ratios, and a calculator that tells you how many to pick up and how to space them.", "How to pick up stitches") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> with the <strong>right side facing</strong>, push the needle through the fabric <strong>one full stitch in from the edge</strong>, wrap the yarn as if to knit and pull a loop through. Each loop is one new stitch. On the side of stockinette or rib, pick up <strong>3 stitches for every 4 rows</strong> (or 2 for every 3), so 80 rows gives 60 stitches. On garter stitch pick up <strong>1 per ridge</strong>. Along a cast on or bound off edge pick up <strong>1 in every stitch</strong>. If your pattern gives a number, follow it and spread the stitches evenly with markers.</div>
<div class="mr-steps">{"".join(pu_fig(i + 1, s) for i, s in enumerate(PU_STEPS))}</div>
<p class="note">Our own drawings of a side edge, right side facing. The teal loops are the picked-up stitches.</p>
</div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Pick up stitches calculator</h2>
<div class="field"><label for="pu-edge">Which edge?</label><select id="pu-edge"><option value="side" selected>Side edge (rows), stockinette, rib or seed</option><option value="garter">Side edge (rows), garter stitch</option><option value="top">Cast on or bound off edge (stitches)</option></select></div>
<div class="field"><span class="label" id="pu-how-l">How long is the edge?</span><div class="seg" role="group" aria-labelledby="pu-how-l" id="pu-how"><button type="button" data-v="count" aria-pressed="true">I counted</button><button type="button" data-v="measure" aria-pressed="false">I'll measure it</button></div></div>
<div class="field" id="pu-count-f"><label for="pu-n" id="pu-n-l">Rows along the edge</label><input id="pu-n" type="number" min="2" max="2000" step="1" value="80" inputmode="numeric"><span class="note" id="pu-n-note">Count the rows, or measure instead.</span></div>
<div id="pu-measure-f" hidden><div class="row2"><div class="field"><label for="pu-len">Edge length</label><input id="pu-len" type="number" min="0.5" max="400" step="0.25" value="10" inputmode="decimal"></div>
<div class="field"><label for="pu-unit">Unit</label><select id="pu-unit"><option value="in" selected>inches (gauge per 4 in)</option><option value="cm">cm (gauge per 10 cm)</option></select></div></div>
<div class="field"><label for="pu-g" id="pu-g-l">Rows in 4 in of the body</label><input id="pu-g" type="number" min="2" max="120" step="0.5" value="28" inputmode="decimal"></div></div>
<div class="field"><label for="pu-ratio">Ratio</label><select id="pu-ratio"><option value="auto" selected>Usual for this edge</option><option value="0.75">3 for every 4 rows</option><option value="0.6667">2 for every 3 rows</option><option value="0.8">4 for every 5 rows</option><option value="0.5">1 for every 2 rows (1 per garter ridge)</option><option value="1">1 for every row or stitch</option><option value="gauge">Work it out from my gauge</option></select></div>
<div class="row2" id="pu-gauge-f" hidden><div class="field"><label for="pu-bg">Band: stitches in 4 in</label><input id="pu-bg" type="number" min="4" max="60" step="0.5" value="22" inputmode="decimal"></div>
<div class="field"><label for="pu-rg">Body: rows in 4 in</label><input id="pu-rg" type="number" min="4" max="80" step="0.5" value="30" inputmode="decimal"></div></div>
<div class="field"><label for="pu-target">My pattern says pick up (optional)</label><input id="pu-target" type="number" min="1" max="2000" step="1" placeholder="e.g. 94" inputmode="numeric"><span class="note">We'll spread exactly that many along your edge.</span></div>
<div class="row2"><div class="field"><label for="pu-band">The band is</label><select id="pu-band"><option value="none" selected>Garter, stockinette or anything</option><option value="r1">1×1 rib (k1, p1)</option><option value="r2">2×2 rib (k2, p2)</option></select></div>
<div class="field"><span class="label" id="pu-flat-l">Worked</span><div class="seg" role="group" aria-labelledby="pu-flat-l" id="pu-flat"><button type="button" data-v="flat" aria-pressed="true">Flat</button><button type="button" data-v="round" aria-pressed="false">In the round</button></div></div></div>
<figure class="ts-fig"><svg id="pu-svg" viewBox="0 0 300 150" role="img" aria-label="Your edge, showing which rows to pick up in and which to skip"></svg><figcaption class="note" id="pu-cap">Pick up at the dots, skip the gaps.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="pu-out"></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>How many stitches do I pick up?</h2>
<p>Knitted stitches are wider than they are tall, so there are more rows than stitches in an inch. If you picked up one stitch for every row on a side edge, the band would have too many stitches and ripple. That's why the usual ratios skip a row now and then:</p></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Edge</th><th scope="col">Usual ratio</th><th scope="col">Who says so</th></tr></thead><tbody>
{"".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td><td class='muted'>{c}</td></tr>" for a, b, c in PU_TAB)}</tbody></table></div>
<p class="note" style="margin-top:12px">Purl Soho says to choose between 3 for 4 and 2 for 3 by your gauge. Your pattern's number always wins over a rule of thumb.</p></div>
<div class="narrow prose"><h2>How many stitches for 40, 80 or 120 rows?</h2></div>
<div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Edge</th><th scope="col">3 for 4</th><th scope="col">2 for 3</th><th scope="col">1 per ridge (garter)</th><th scope="col">3 for 4, fitted to 2×2 rib (flat)</th></tr></thead><tbody>{pu_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Our sums, rounded to the nearest stitch. The last column rounds to a multiple of 4 + 2, so a flat 2×2 rib band starts and ends with k2.</p></div>
<div class="narrow prose">
<h2>Where exactly do I put the needle?</h2>
<ul><li><strong>Side edges:</strong> between the edge stitch and the next one in (Quince &amp; Co., Interweave). Going a full stitch in hides the wobbly edge stitch on the wrong side.</li>
<li><strong>Cast on or bound off edges:</strong> into the middle of the V of each stitch just below the edge, one new stitch per stitch (Quince &amp; Co., Interweave). Going into the centre lines the new band up with the columns below.</li>
<li><strong>Curves and slopes:</strong> one full stitch in from the shaped edge, and not into the little holes where bound off steps meet (Purl Soho).</li></ul>
<h2>What's the difference between "pick up" and "pick up and knit"?</h2>
<p>Most patterns mean the same thing: draw a loop of working yarn through the edge, which puts a new stitch on your needle. Some knitters pick up all the loops first and then knit them, others knit each one as it's picked up (Wikipedia). LoveCrafts draws a small line between them: with "pick up" the new loops wait on the needle to be knitted on the next row, with "pick up and knit" each loop is knitted as you go. If your pattern says "pick up and knit", use the working yarn as in the drawings. The row you pick up is not usually counted as the band's first row.</p>
<h2>How do I space picked-up stitches evenly?</h2>
<ol><li>Divide the edge in half and then in quarters with locking stitch markers (Interweave, Purl Soho).</li>
<li>Divide your stitch count by the number of sections. The calculator above does it and lists rows and stitches for each section.</li>
<li>Pick up that many in each section, using a steady rhythm such as "pick up 3, skip 1". Don't skip two rows in a row (Quince &amp; Co.).</li>
<li>Count at each marker, so a mistake costs you one section, not the whole edge.</li></ol>
<h2>How do I pick up stitches around a neckline?</h2>
<p>Treat each part of the neck as its own edge (Interweave): the bound off stitches at the centre front and back neck (1 per stitch), the straight sides (3 for 4 rows), and the decreased slopes in between. Put markers where each part changes, mirror the counts on both sides, and start at a shoulder seam or the centre back. Necklines are usually picked up in the round on a 16 in circular needle; see <a href="{href("how-to-knit-in-the-round.html")}">how to knit in the round</a>.</p>
<h2>Why do I get holes, and how do I stop them?</h2>
<ul><li><strong>Use a smaller needle for the pick-up row</strong> (Interweave, Purl Soho), then switch to the band's needle on the next row.</li>
<li><strong>Don't pick up into existing holes</strong> where bound off steps meet the slope; go one stitch in.</li>
<li><strong>Pick up an extra stitch at a gap</strong> and knit it together with its neighbour on the next row (Knotions).</li>
<li><strong>Plain edges pick up best.</strong> Slipped-stitch edges have one edge stitch for every two rows, which leaves fewer places to pick up and can make gaps (Interweave, Purl Soho).</li>
<li><strong>Snug the first stitch:</strong> after a round, give the tail a gentle tug (Purl Soho), then weave it in, see <a href="{href("how-to-weave-in-ends.html")}">weaving in ends</a>.</li></ul>
<h2>What if I picked up the wrong number?</h2>
<p>A few stitches out is fine. On the first row of the band, k2tog or p2tog to lose a stitch, or work into the front and back of a stitch to add one (Interweave). Spread the fixes out, as the <a href="{href("increase-decrease-calculator.html")}">increase and decrease evenly calculator</a> shows. If the band ripples or pulls in a lot, pull it out and pick up again: it's only one row.</p>
<p>What next? Finish the band with a stretchy edge from our <a href="{href("how-to-bind-off-knitting.html")}">bind off guide</a>, check what "PU" and "pick up and k" mean in the <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list</a>, or start the next piece with the <a href="{href("cast-on-calculator.html")}">cast on calculator</a>.</p></div></section>'''
pu_faq = [
    ("How many stitches do I pick up along a side edge?", "Usually 3 stitches for every 4 rows on stockinette, rib or seed stitch (or 2 for every 3 rows), so 80 rows gives 60 stitches. On garter stitch pick up 1 stitch per ridge. Follow your pattern's number if it gives one."),
    ("How do you pick up stitches in knitting?", "With the right side facing, put the needle through the fabric one full stitch in from the edge, wrap the yarn as if to knit and pull a loop through. Each loop is a new stitch. Skip a row now and then on side edges so the band lies flat."),
    ("How many stitches do I pick up along a cast on or bound off edge?", "One in every stitch, going into the centre of each V just below the edge."),
    ("Is the pick up row counted as the first row?", "Not usually. The row you pick up puts stitches on the needle; the band's first row is the next one you work. Check your pattern."),
    ("How do I avoid holes when picking up stitches?", "Pick up with a smaller needle, go one full stitch in from the edge, avoid the holes where bound off steps meet a slope, and pick up an extra stitch at a gap and knit it together with its neighbour on the next row."),
    ("What does 'pick up and knit 3 stitches for every 4 rows' mean?", "Pull a new loop through the edge in 3 rows, skip the 4th row, and repeat along the edge."),
]
page("how-to-pick-up-stitches-knitting.html", "How to Pick Up Stitches in Knitting (+ Pick Up Calculator) | Purl & Paper",
     "How to pick up stitches in knitting in 4 drawings: 3 for 4 rows, garter and cast on edges, necklines, spacing with markers and fixing holes. Free calculator for how many and how to space them.",
     pup, pu_faq, "How to pick up stitches", app_name="Pick up stitches calculator")

# ---------------- HOW TO PRICE AMIGURUMI (guide + calculator) ----------------
AM_SPM = 12   # single crochet per minute in tight amigurumi fabric, comfortable maker. Our estimate.
def am_spsi(w): return (CI_G[w] * CI_AMI / 4) ** 2   # stitches per sq in, same gauge model as the crochet circle calculator
def am_sts(h, w, cx): return 3.14159 * h * h * am_spsi(w) * cx   # about the surface of a ball as tall as the toy, x complexity
def am_hours(h, w, cx, parts, face="eyes"):
    return am_sts(h, w, cx) / (AM_SPM * 60) + parts * 10 / 60 + (5 if face == "eyes" else 20) / 60 + (10 + h * 1.5) / 60
AM_SIZES = [("key", "Keyring or mini", 3, 8, 2, 1.0, 1, 1.5), ("small", "Small toy", 6, 15, 6, 1.3, 3, 2.5),
            ("medium", "Medium toy", 10, 25, 6, 1.3, 7, 4), ("large", "Large plush", 16, 40, 6, 1.3, 14, 7)]
AM_CX = {1.0: "simple", 1.3: "typical", 1.7: "detailed"}
def am_row(s, w=4):
    _, n, h, cm, parts, cx, y, o = s
    hr = am_hours(h, w, cx, parts); mat = y + o
    return hr, mat
def _am_r(x): return f"${x:,.0f}" if x < 20 else f"${round(x / 5) * 5:,.0f}"
am_rows = ""
for s in AM_SIZES:
    hr, mat = am_row(s)
    am_rows += (f'<tr><th scope="row">{e(s[1])}<br><span class="muted">{s[2]} in ({s[3]} cm)</span></th><td>{hr:.1f} h</td><td>${mat:,.2f}</td>'
                + "".join(f"<td>{_am_r(pr_base(mat, hr, r))}</td>" for r in (12, 15, 20)) + f'<td>{_am_r(pr_etsy(pr_base(mat, hr)))}</td><td class="muted">${mat * 3:,.0f} (${max(0, (mat * 3 - mat) / hr):.2f}/h)</td></tr>')
_aml = AM_SIZES[3]; _amp_h = am_hours(_aml[2], 6, _aml[5], _aml[6])
am_rows += (f'<tr><th scope="row">Large plush in chunky chenille<br><span class="muted">16 in (40 cm), super bulky</span></th><td>{_amp_h:.1f} h</td><td>${_aml[6] + _aml[7]:,.2f}</td>'
            + "".join(f"<td>{_am_r(pr_base(_aml[6] + _aml[7], _amp_h, r))}</td>" for r in (12, 15, 20)) + f'<td>{_am_r(pr_etsy(pr_base(_aml[6] + _aml[7], _amp_h)))}</td><td class="muted">${(_aml[6] + _aml[7]) * 3:,.0f}</td></tr>')
_ams = AM_SIZES[1]; _ams_h, _ams_m = am_row(_ams); _ams_p = pr_base(_ams_m, _ams_h)
_amk = AM_SIZES[0]; _amk_h, _amk_m = am_row(_amk)
am_sopts = "".join(f'<option value="{k}" data-h="{h}" data-parts="{p}" data-cx="{cx}" data-y="{y}" data-o="{o}"{" selected" if k == "small" else ""}>{e(n)}, about {h} in ({cm} cm)</option>' for k, n, h, cm, p, cx, y, o in AM_SIZES) + '<option value="custom">My own size</option>'
am_wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])})</option>' for w in D["weights"] if w["n"] in CI_G and 1 <= w["n"] <= 6)
amp = top("How to price amigurumi", "Crochet toys are small but slow: tight stitches, lots of little parts and a face to sew on. This calculator estimates the hours from the toy's size and parts, adds stuffing, eyes and fees, and gives you a price that pays for your time.", "How to price amigurumi") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> price amigurumi like any handmade item: <strong>materials + (hours × your hourly rate)</strong>, plus about 10% for overheads, plus selling fees. The catch is the hours: count the time to make and sew on every part, stuff it and do the face, not just the body. By our estimate a 6 in (15 cm) toy in worsted yarn with 6 parts takes about <strong>{_ams_h:.0f} hours</strong>, so with ${_ams_m:.2f} of materials at $15 an hour it comes to about <strong>{_am_r(_ams_p)}</strong> (about {_am_r(pr_etsy(_ams_p))} on Etsy). A simple keyring takes about {_amk_h:.0f} hour and is about {_am_r(pr_base(_amk_m, _amk_h))}. Many toys sell for less than this, so smaller and simpler toys are how sellers hit lower prices without working for free.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="font-size:1.25rem;margin-bottom:10px">Amigurumi price calculator</h2>
<div class="field"><label for="am-size">Toy size</label><select id="am-size">{am_sopts}</select></div>
<div class="row2" id="am-custom" hidden><div class="field"><label for="am-hgt">Height</label><input type="number" id="am-hgt" value="8" min="1" max="60" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="am-hu">Unit</label><select id="am-hu"><option value="in" selected>inches</option><option value="cm">cm</option></select></div></div>
<div class="row2"><div class="field"><label for="am-w">Yarn weight</label><select id="am-w">{am_wopts}</select></div>
<div class="field"><label for="am-cx">How detailed?</label><select id="am-cx"><option value="1">Simple: a ball or one-piece body</option><option value="1.3" selected>Typical: head, body, arms, legs, ears</option><option value="1.7">Detailed: clothes, colour changes, tiny parts</option></select></div></div>
<div class="row2"><div class="field"><label for="am-parts">Parts to sew on</label><input type="number" id="am-parts" value="6" min="0" max="60" step="1" inputmode="numeric"><span class="note">Arms, legs, ears, tail, nose…</span></div>
<div class="field"><label for="am-face">Eyes</label><select id="am-face"><option value="eyes" selected>Safety eyes</option><option value="emb">Embroidered (for babies)</option></select></div></div>
<div class="row2"><div class="field"><label for="am-y">Yarn used</label><input type="number" id="am-y" value="3" min="0" step="0.25" inputmode="decimal"><span class="note">The share of each skein you used.</span></div>
<div class="field"><label for="am-o">Stuffing, eyes, tag, bag</label><input type="number" id="am-o" value="2.5" min="0" step="0.25" inputmode="decimal"></div></div>
<div class="row2"><div class="field"><label for="am-speed">How fast are you?</label><select id="am-speed"><option value="1.3">Still learning</option><option value="1" selected>Comfortable</option><option value="0.75">Speedy</option></select></div>
<div class="field"><label for="am-h">Hours to make it</label><input type="number" id="am-h" min="0.25" max="200" step="0.25" inputmode="decimal" placeholder="we'll estimate"><span class="note" id="am-h-note">Leave empty to use our estimate.</span></div></div>
<div class="row2"><div class="field"><label for="am-rate">Your hourly rate</label><input type="number" id="am-rate" value="15" min="0" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="am-cur">Currency</label><select id="am-cur"><option value="$" selected>$ (US, CA, AU)</option><option value="£">£ (UK)</option><option value="€">€ (EU)</option><option value="₹">₹ (India)</option><option value="Rs ">Rs (Pakistan)</option></select></div></div>
<div class="row2"><div class="field"><label for="am-oh">Overheads (%)</label><input type="number" id="am-oh" value="10" min="0" max="100" step="1" inputmode="decimal"></div>
<div class="field"><label for="am-ch">Selling on</label><select id="am-ch"><option value="etsy">Etsy (US fees)</option><option value="fair">Craft fair (card reader 3%)</option><option value="direct" selected>Direct, no fees</option></select></div></div>
<div class="field"><label for="am-try">A price you had in mind (optional)</label><input type="number" id="am-try" placeholder="e.g. 25" min="0" step="1" inputmode="decimal"></div>
<figure class="ts-fig"><svg id="am-svg" viewBox="0 0 300 150" role="img" aria-label="Where the hours go: crocheting, sewing parts, face and stuffing"></svg><figcaption class="note" id="am-cap">Where the hours go.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="am-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How much should I charge for amigurumi?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Toy</th><th scope="col">Hours</th><th scope="col">Materials</th><th scope="col">At $12/h</th><th scope="col">At $15/h</th><th scope="col">At $20/h</th><th scope="col">On Etsy at $15/h</th><th scope="col">Materials × 3 (pay per hour)</th></tr></thead><tbody>{am_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Our estimates for worsted yarn unless stated, with 10% overheads, rounded to $5 above $20. Hours: about the surface of a ball as tall as the toy, at amigurumi gauge and {AM_SPM} single crochet a minute, plus 10 minutes per part, the face and stuffing. Time your own toy and put the real hours in the calculator.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>What's the formula for pricing crochet toys?</h2>
<ol><li><strong>Materials.</strong> The share of each skein you used, plus stuffing, safety eyes, a tag and packaging. Hostinger's pricing guide suggests adding 10 to 15% to the yarn for waste.</li>
<li><strong>Time.</strong> Every minute: crocheting, stuffing, sewing on parts, the face, and packing. Hours × an hourly rate, at least your local minimum wage.</li>
<li><strong>Overheads.</strong> A percentage for hooks, photos, your shop and trips to the post office.</li>
<li><strong>Fees.</strong> The shop's or card reader's cut, added on top so it doesn't come out of your pay.</li></ol>
<p>The full method, with craft fair and consignment fees, is in our guide to <a href="{href("how-to-price-crochet-items.html")}">pricing crochet items</a>.</p>
<h2>Why doesn't "materials × 3" work for amigurumi?</h2>
<p>Because a toy uses very little yarn. June Gilbank of PlanetJune points out that a toy made from under half a ball of yarn can take as long as a blanket made from 5 or 6 balls, so tripling the materials badly underprices it. The last column of the table shows what "materials × 3" would pay you an hour. She also argues a full hourly wage can make toys hard to sell, and aims for a middle ground that covers materials, time and how complex the design is.</p>
<h2>How long does it take to crochet an amigurumi?</h2>
<p>From under an hour for a tiny toy to a few days for a big, detailed plush. One market seller on the Ribblr forum makes small chickens and bunnies in under an hour each. Our <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a> uses about 6 hours for a small toy. The parts take longer than people expect: a body is one piece, but four legs, two arms, two ears and a tail are nine more pieces to crochet, stuff and sew on. Time yourself on the next one, start to finish, and use that.</p>
<h2>What do crochet toys actually sell for?</h2>
<p>Often less than the formula says. The Ribblr seller above priced chickens at $5 to $8 and bunnies and octopuses at $8 to $12 for a small market, where shoppers had little to spend. Prices like that only work for toys that take under an hour. Ways to close the gap:</p>
<ul><li><strong>Make a small, quick range:</strong> keyrings, minis and one-piece toys that take under an hour, for buyers who want something under $15.</li>
<li><strong>Keep bigger toys for buyers who value them:</strong> gifts, custom pets and characters, and online shoppers looking for something special.</li>
<li><strong>Use thicker yarn for big plush:</strong> chunky chenille covers a big toy in about half the stitches (see the table).</li>
<li><strong>Don't undercut other makers.</strong> PlanetJune warns against it; selling faster than you can make, or sore hands, are signs your price is too low.</li></ul>
<h2>How do I price a custom amigurumi order?</h2>
<ul><li><strong>Charge for the design time.</strong> Working out a new character, sketching and test pieces is real work (Hostinger).</li>
<li><strong>Set fixed add-ons</strong> for common requests, such as a name embroidered on, a scarf or a different colour, so you don't quote from scratch each time (Hostinger).</li>
<li><strong>Take payment before you start</strong> and give a finish date; see the custom order tips in our <a href="{href("how-to-price-crochet-items.html")}">pricing guide</a>.</li></ul>
<h2>Can I sell toys made from someone else's pattern?</h2>
<p>It depends on the designer. PlanetJune lets people sell toys made from her patterns as long as they credit her as the designer; other designers don't allow it at all. Check the pattern's terms before you list, and credit the designer in your listing when they ask for it. Your own designs are yours to sell, and you can charge more for them.</p>
<h2>Are there safety rules for selling crochet toys?</h2>
<p>Yes. Toys made for children are covered by toy safety laws in most countries, handmade ones included. In the US, start with the Consumer Product Safety Commission's Online Sellers Safety Guide; in the UK and EU, look up the toy safety rules for your country. Our tips: use safety eyes with locking backs and give each a firm tug test, sew parts on securely, and embroider eyes and noses for toys meant for babies and young children. If a toy is a decoration, not for children, say so clearly in the listing. This is general information, not legal advice.</p>
<p>What next? Plan the toy's rounds with the <a href="{href("crochet-circle-calculator.html")}">crochet circle and amigurumi ball calculator</a>, close it neatly with the <a href="{href("how-to-crochet-decrease.html")}">invisible decrease</a>, start each piece with a <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>, and check what Etsy will take with the <a href="{href("etsy-fee-calculator.html")}">Etsy fee calculator</a>.</p></div></section>'''
am_faq = [
    ("How much should I charge for an amigurumi?", f"Add materials, your hours times an hourly rate, about 10% for overheads, then selling fees. By our estimate a 6 in (15 cm) toy with 6 parts takes about {_ams_h:.0f} hours, which at $15 an hour is about {_am_r(_ams_p)}. Keyrings and one-piece toys can be under $25."),
    ("How long does it take to crochet an amigurumi?", "From under an hour for a mini or keyring to several hours for a 6 in toy with limbs and ears, and a day or more for a large plush. Sewing on parts often takes as long as the body."),
    ("Is materials times 3 a good way to price crochet toys?", "No. Toys use little yarn but a lot of time, so materials times 3 can pay you a few dollars an hour. Price your hours instead."),
    ("Can I sell amigurumi made from a pattern?", "Only if the designer allows it. Some, like PlanetJune, allow sales with credit to the designer; others don't. Check the pattern's terms."),
    ("Do I need safety eyes or embroidered eyes for toys I sell?", "For toys meant for babies and young children, many makers embroider the eyes. If you use safety eyes, use ones with locking backs and check the toy safety rules where you sell."),
    ("How do I price custom crochet toys?", "Add your design time, use fixed prices for common add-ons like a name or a scarf, take payment before you start and give a finish date."),
]
page("how-to-price-amigurumi.html", "How to Price Amigurumi (Crochet Toy Price Calculator) | Purl & Paper",
     "How much to charge for amigurumi and crochet toys: a free calculator that estimates hours from size and parts, a price chart from keyring to large plush, custom orders, pattern rights and toy safety.",
     amp, am_faq, "How to price amigurumi", app_name="Amigurumi price calculator")

# ---------------- C2C BLANKET CALCULATOR (corner to corner crochet) ----------------
C2C_T = {2: 0.5, 3: 0.65, 4: 0.8, 5: 1.25, 6: 1.65}   # inches per tile. Worsted 5 tiles = 4 in (Lion Brand graphgan kit), bulky 4 = 5 in (Premier Yarns C2C throw), super bulky 3 = 5 in (EyeLoveKnots); fine and DK are our estimates
C2C_YPS = 0.667 * 1.27   # yd per sq in of worsted crochet: same model as the blanket calculator (checked against a 48 x 50 in aran C2C throw that takes 1,953 yd)
def c2c_ab(w, l, t): return max(1, int(w / t + 0.5)), max(1, int(l / t + 0.5))
def c2c_yd(w, l, wn): return w * l * C2C_YPS * BK_M[wn]
def c2c_rng(w, l, wn): y = c2c_yd(w, l, wn); return f"{round(y * 0.9, -2):,.0f}–{round(y * 1.1, -2):,.0f}"
c2c_bl = [b for b in D["blankets"] if b["id"] in ("lovey", "baby", "crib", "lap", "throw", "twin", "queen", "king")]
c2c_opts = "".join(f'<option value="{b["w"]}|{b["l"]}"{" selected" if b["id"] == "throw" else ""}>{e(b["name"])}, {b["w"]} × {b["l"]} in</option>' for b in c2c_bl) + '<option value="custom">My own size</option>'
c2c_wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])}), about {4 / C2C_T[w["n"]]:.1f} tiles per 4 in</option>' for w in D["weights"] if w["n"] in C2C_T)
C2C_TW = [(3, "DK"), (4, "Worsted"), (5, "Bulky"), (6, "Super bulky")]
def _c2c_cell(b, wn):
    a, c = c2c_ab(b["w"], b["l"], C2C_T[wn]); return f'<td>{a} × {c}<br><span class="muted">{a * c:,} tiles</span></td>'
c2c_rows = "".join(f'<tr><th scope="row">{e(b["name"])}<br><span class="muted">{b["w"]} × {b["l"]} in</span></th>' + "".join(_c2c_cell(b, wn) for wn, _ in C2C_TW) + f'<td>{c2c_rng(b["w"], b["l"], 4)} yd</td></tr>' for b in c2c_bl)
_c2_th = [b for b in D["blankets"] if b["id"] == "throw"][0]; _c2_a, _c2_b = c2c_ab(50, 60, 0.8); _c2_ba, _c2_bb = c2c_ab(36, 36, 0.8); _c2_bk = c2c_ab(50, 60, 1.25)
C2C_SVG = '''<svg viewBox="0 0 300 170" role="img" aria-label="Three C2C tiles: chain 6 and 3 double crochet, then the next tile hooked onto the chain-3 space"><rect width="300" height="170" fill="#fff"/>
<g stroke="#1f2a44" stroke-width="2" fill="none"><rect x="30" y="80" width="56" height="56" rx="4" fill="#f6d9e5"/><rect x="86" y="80" width="56" height="56" rx="4" fill="#fbe7c2"/><rect x="30" y="24" width="56" height="56" rx="4" fill="#d6ecea"/></g>
<g stroke="#b8326a" stroke-width="2.6" stroke-linecap="round"><path d="M44 130v-40M56 130v-40M68 130v-40"/></g><path d="M34 90q4-8 0-14M34 104q4-8 0-14M34 118q4-8 0-14" stroke="#f4a823" stroke-width="2.4" fill="none"/>
<g stroke="#b8326a" stroke-width="2.6" stroke-linecap="round" transform="rotate(90 114 108)"><path d="M100 128v-40M112 128v-40M124 128v-40"/></g>
<g stroke="#2f8f8a" stroke-width="2.6" stroke-linecap="round" transform="rotate(90 58 52)"><path d="M44 72v-40M56 72v-40M68 72v-40"/></g>
<g font-size="11" fill="#1f2a44" font-weight="700"><text x="58" y="152" text-anchor="middle">Row 1: 1 tile</text><text x="114" y="152" text-anchor="middle">Row 2</text><text x="58" y="18" text-anchor="middle">Row 2</text></g>
<g font-size="11" fill="#1f2a44"><text x="160" y="40">A tile = 3 chains</text><text x="160" y="56">(the turning chain) + 3 dc.</text><text x="160" y="84">Each new row starts</text><text x="160" y="100">with ch 6 and adds a tile</text><text x="160" y="116">at both ends until the</text><text x="160" y="132">blanket is wide enough.</text></g></svg>'''
c2c = top("C2C blanket calculator", "Pick a blanket size and your yarn. Get how many tiles wide and tall, when to start decreasing for a rectangle, how many rows and how much yarn to buy. Corner to corner crochet, worked out for you.", "C2C blanket calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> divide the width and length you want by the size of one tile. In worsted yarn a tile is about 0.8 in (5 tiles to 4 in), so a 50 × 60 in throw is about <strong>{_c2_a} × {_c2_b} tiles</strong> ({_c2_a * _c2_b:,} in all) and takes roughly <strong>{c2c_rng(50, 60, 4)} yards</strong>. A 36 in square baby blanket is about {_c2_ba} × {_c2_ba} tiles. Increase until a row has {_c2_a} tiles (the short side), work {_c2_b - _c2_a} rows that increase at one edge and decrease at the other, then decrease to one tile. Make a swatch: your tile size decides everything.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="c2-what">Blanket size</label><select id="c2-what">{c2c_opts}</select></div>
<div id="c2-custom" hidden><div class="row2"><div class="field"><label for="c2-w">Width</label><input type="number" id="c2-w" value="40" min="2" max="200" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="c2-l">Length</label><input type="number" id="c2-l" value="50" min="2" max="200" step="0.5" inputmode="decimal"></div></div>
<div class="field"><label for="c2-u">Unit</label><select id="c2-u"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><label for="c2-yarn">Yarn weight</label><select id="c2-yarn">{c2c_wopts}</select></div>
<div class="row2"><div class="field"><label for="c2-g">Tiles in your swatch</label><input type="number" id="c2-g" value="5" min="0.5" max="20" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="c2-gu">Measured over</label><select id="c2-gu"><option value="4">4 in</option><option value="10">10 cm</option></select></div></div>
<p class="note" id="c2-gnote" style="margin:-4px 0 12px">Count tiles along one straight edge of a small C2C square. Filled in with a typical number until you change it.</p>
<div class="row2"><div class="field"><label for="c2-sk">Yards in one skein</label><input type="number" id="c2-sk" value="200" min="10" max="3000" step="1" inputmode="numeric"></div>
<div class="field"><label for="c2-col">Colours (for a striped or graph blanket)</label><select id="c2-col"><option value="1" selected>1 colour</option><option value="2">2 colours</option><option value="3">3 colours</option><option value="4">4 colours</option><option value="5">5 colours</option><option value="6">6 colours</option></select></div></div>
<figure class="co-fig"><svg id="c2-svg" viewBox="0 0 320 240" role="img" aria-label="Your blanket as a grid of tiles with the increase, straight and decrease sections"></svg><figcaption class="note" id="c2-cap">Your blanket, tile by tile.</figcaption>
<ul class="co-key"><li><i style="background:#b8326a"></i>Increase both edges</li><li><i style="background:#f4a823"></i>Increase one edge, decrease the other</li><li><i style="background:#2f8f8a"></i>Decrease both edges</li></ul></figure>
</div>
<div class="result" aria-live="polite" id="c2-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How many C2C tiles for a blanket?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Blanket</th>{"".join(f'<th scope="col">{n}<br><span class="muted">{4 / C2C_T[wn]:.1f} tiles per 4 in</span></th>' for wn, n in C2C_TW)}<th scope="col">Yarn in worsted</th></tr></thead><tbody>{c2c_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Tiles wide × tiles tall, rounded to whole tiles. Tile sizes: worsted 5 tiles to 4 in (as in Lion Brand's C2C graphgan kit), bulky 4 tiles to 5 in (Premier Yarns' C2C throw), super bulky 3 tiles to 5 in (EyeLoveKnots' super chunky C2C afghan); DK is our estimate. Yarn is our estimate from the same model as our <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>, which comes out close to a published 48 × 50 in aran C2C throw that uses 1,953 yards. Your tension changes both, so swatch.</p>
</div></section>
{AD.format("c2-mid")}
<section style="padding-top:0"><div class="narrow prose"><h2>How does corner to corner crochet work?</h2>
<figure class="co-fig">{C2C_SVG}<figcaption class="note">Our drawing: each tile is a short chain and 3 double crochets, worked on the diagonal.</figcaption></figure>
<p>C2C is worked in diagonal rows of small blocks, called tiles or boxes. Each tile is 3 chains plus 3 double crochets. You start in one corner with a single tile, and every row adds one tile until the blanket is as wide as you want. Then you decrease one tile per row until you finish at the opposite corner. Because every tile is a square, a C2C blanket works like a grid of pixels, which is why it's so popular for picture blankets ("graphgans").</p>
<ol><li><strong>Row 1:</strong> chain 6, double crochet in the 4th chain from the hook and in the next 2 chains. That's one tile.</li>
<li><strong>Increase rows:</strong> chain 6, dc in the 4th chain from the hook and the next 2, then slip stitch into the chain-3 space of the tile below and work ch 3 and 3 dc in that same space for every tile across. Each row ends up one tile longer.</li>
<li><strong>Decrease rows:</strong> slip stitch across the top of the last tile instead of chaining 6, then work tiles as before, but don't add one at the end.</li></ol>
<h2>How do I make a rectangle in C2C?</h2>
<p>Increase at both edges until a row has as many tiles as the short side. After that, keep increasing along the long edge and decrease along the short edge, so each row stays the same length. When the long side reaches its count too, decrease at both edges to the last tile. For a blanket {_c2_a} tiles wide and {_c2_b} tall:</p>
<ul><li>Rows 1 to {_c2_a}: increase at both edges.</li>
<li>Rows {_c2_a + 1} to {_c2_b}: increase on the long side, decrease on the short side ({_c2_b - _c2_a} rows).</li>
<li>Rows {_c2_b + 1} to {_c2_a + _c2_b - 1}: decrease at both edges.</li></ul>
<p>Total rows are always tiles wide + tiles tall − 1. The calculator writes this out for your size, and the drawing shows where each section sits. Keep a stitch marker on the edge that keeps growing; it's easy to forget which side is which.</p>
<h2>How big is a C2C tile?</h2>
<p>It depends on your yarn, hook and hands. Published patterns give about 5 tiles to 4 in in worsted yarn, 4 tiles to 5 in in bulky and 3 tiles to 5 in in super bulky. To find yours, crochet a small square of about 10 rows, block it lightly, then count the tiles along one straight edge across 4 in (10 cm). Make Do Crew suggests a smaller hook if the tiles have big gaps and a bigger one if they're stiff.</p>
<h2>How much yarn does a C2C blanket take?</h2>
<p>The table gives our estimates. For a closer number, use Make and Do Crew's method: crochet the first 10 rows (55 tiles), weigh them or measure the yarn used, and divide by 55 to get the yarn per tile. Multiply by the total tiles and add 10 percent. Our <a href="{href("yarn-yardage-calculator.html")}">yarn yardage calculator</a> turns grams into yards. For a graph blanket, count the squares of each colour on the graph and use the same yarn per tile.</p>
<div class="callout"><strong>Planning a picture blanket?</strong> Your graph needs one square per tile, so a blanket {_c2_a} × {_c2_b} tiles needs a {_c2_a} × {_c2_b} grid. Read the graph diagonally from the starting corner. Lots of colour changes? Wind small bobbins for each colour and weave in ends every few rows, not at the end (see <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>).</div>
<h2>Why is my C2C blanket not square?</h2>
<ul><li><strong>Tension changes</strong> between the chain-6 edge and the slip-stitch edge can pull one side in. Keep the chains loose.</li>
<li><strong>A miscounted row.</strong> Count tiles along each edge at the corner: both edges should have the number you planned.</li>
<li><strong>It needs blocking.</strong> C2C often looks wavy until it's washed and pinned flat. A border of single crochet or half double crochet around the edge also straightens it.</li></ul>
<p>What next? Check standard sizes on the <a href="{href("blanket-size-calculator.html")}">blanket size chart</a>, plan a squares blanket with the <a href="{href("granny-square-blanket-calculator.html")}">granny square calculator</a>, count rows with the <a href="{href("row-counter.html")}">row counter</a>, or work out a fair selling price with <a href="{href("how-to-price-a-crochet-blanket.html")}">how to price a crochet blanket</a>.</p></div></section>'''
c2c_faq = [
    ("How many C2C tiles for a throw blanket?", f"About {_c2_a} × {_c2_b} tiles ({_c2_a * _c2_b:,} in all) for a 50 × 60 in throw in worsted yarn at 5 tiles to 4 in, or about {_c2_bk[0]} × {_c2_bk[1]} in bulky yarn. Divide each side by your own tile size."),
    ("How many C2C tiles for a baby blanket?", f"About {_c2_ba} × {_c2_ba} tiles for a 36 in square baby blanket in worsted yarn, or {c2c_ab(30, 35, 0.8)[0]} × {c2c_ab(30, 35, 0.8)[1]} for a 30 × 35 in one."),
    ("How much yarn do I need for a C2C blanket?", f"Roughly {c2c_rng(36, 36, 4)} yards of worsted for a 36 in baby blanket and {c2c_rng(50, 60, 4)} yards for a 50 × 60 in throw (our estimates). For a closer figure, weigh the first 55 tiles and multiply up."),
    ("When do I start decreasing in C2C?", "For a square, after the row whose tile count equals the number of tiles across. For a rectangle, decrease on the short side once a row reaches the short side's count, keep increasing on the long side, and decrease on both sides once the long side is done too."),
    ("How many rows is a C2C blanket?", "Tiles wide plus tiles tall minus one. A blanket 60 × 75 tiles has 134 diagonal rows."),
    ("How big is one C2C tile?", "About 0.8 in in worsted yarn (5 tiles to 4 in), about 1.25 in in bulky and about 1.65 in in super bulky, from published patterns. Your swatch decides."),
]
page("c2c-blanket-calculator.html", "C2C Blanket Calculator: How Many Tiles, Rows and Yarn? | Purl & Paper",
     "Free C2C (corner to corner) crochet blanket calculator: how many tiles wide and tall for any blanket size, when to start decreasing for a rectangle, total rows and how much yarn, with a tile chart from baby to king.",
     c2c, c2c_faq, "C2C blanket calculator", app_name="C2C blanket calculator")

# ---------------- SCARF SIZE CHART + YARN CALCULATOR ----------------
SC_SIZES = [("child4", "Child, 4 to 5 years", 35, 40, 4, "flat"), ("child6", "Child, 6 to 10 years", 50, 60, 5, "flat"), ("teen", "Teen", 55, 65, 6, "flat"),
            ("women", "Adult, women's", 60, 70, 7, "flat"), ("men", "Adult, men's", 65, 75, 7, "flat"), ("skinny", "Skinny scarf", 60, 70, 3.5, "flat"),
            ("long", "Long scarf (wraps twice)", 75, 90, 8, "flat"), ("super", "Super long scarf", 90, 110, 8, "flat"), ("wrap", "Wrap or stole", 70, 72, 20, "flat"),
            ("infinity", "Infinity scarf", 56, 60, 9, "loop"), ("cowl", "Adult cowl", 24, 30, 9, "loop"), ("kidcowl", "Child cowl", 18, 22, 7, "loop")]
SC_NOTE = {"child4": "Leave room to grow", "child6": "Madison Knitters' Guild", "teen": "Our estimate, between child and adult", "women": "Or about the wearer's height", "men": "Madison Knitters' Guild: 60 to 80 in",
           "skinny": "4 in or narrower", "long": "Wraps twice with ends hanging", "super": "Desert Blossom Crafts: 90 to 120 in", "wrap": "Sew Guide stole size", "infinity": "Around, loops twice", "cowl": "Around, one loop", "kidcowl": "Madison Knitters' Guild"}
SC_K = 0.667   # yd per sq in of worsted stockinette: same area model as our blanket and yarn calculators; crochet × 1.27
def sc_mid(s): return (s[2] + s[3]) / 2
def sc_yd(s, wn, craft=1.0): return s[4] * sc_mid(s) * SC_K * BK_M[wn] * craft
def sc_rng(s, wn, craft=1.0): y = sc_yd(s, wn, craft); r = 10 if y < 400 else 50; return f"{round(y * 0.88 / r) * r:,.0f}–{round(y * 1.12 / r) * r:,.0f}"
sc_opts = "".join(f'<option value="{k}"{" selected" if k == "women" else ""}>{e(n)}, {(a + b) / 2:g} × {w:g} in</option>' for k, n, a, b, w, t in SC_SIZES) + '<option value="height">As long as the wearer is tall</option><option value="custom">My own size</option>'
sc_wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])})</option>' for w in D["weights"] if 1 <= w["n"] <= 7)
sc_crows = "".join(f'<tr><td><strong>{e(n)}</strong></td><td>{a:g}–{b:g} in<br><span class="muted">{round(a * 2.54)}–{round(b * 2.54)} cm</span></td><td>{w:g} in<br><span class="muted">{round(w * 2.54)} cm</span></td><td>{e(SC_NOTE[k])}</td></tr>' for k, n, a, b, w, t in SC_SIZES)
SC_TW = [(3, "DK"), (4, "Worsted"), (5, "Bulky"), (6, "Super bulky")]
sc_yrows = "".join(f'<tr><th scope="row">{e(s[1])}<br><span class="muted">{sc_mid(s):g} × {s[4]:g} in</span></th>' + "".join(f"<td>{sc_rng(s, wn)}</td><td>{sc_rng(s, wn, 1.27)}</td>" for wn, _ in SC_TW[1:3]) + "</tr>" for s in SC_SIZES if s[0] in ("child6", "women", "men", "long", "infinity", "cowl", "wrap"))
_sw = [s for s in SC_SIZES if s[0] == "women"][0]; _sm = [s for s in SC_SIZES if s[0] == "men"][0]; _si = [s for s in SC_SIZES if s[0] == "infinity"][0]
SC_RULER = '''<svg viewBox="0 0 300 120" role="img" aria-label="A scarf as long as the wearer is tall, about as wide as a hand span"><rect width="300" height="120" fill="#fff"/>
<circle cx="34" cy="26" r="10" fill="#1f2a44"/><path d="M34 36v40M34 76l-10 30M34 76l10 30M34 46l-14 18M34 46l14 18" stroke="#1f2a44" stroke-width="4" stroke-linecap="round" fill="none"/>
<path d="M64 14v96" stroke="#f4a823" stroke-width="2" stroke-dasharray="4 3"/><text x="70" y="64" font-size="11" fill="#1f2a44">height</text>
<rect x="110" y="44" width="176" height="26" rx="4" fill="#b8326a"/><path d="M118 50l6 7 6-7M130 50l6 7 6-7M142 50l6 7 6-7M154 50l6 7 6-7M166 50l6 7 6-7M178 50l6 7 6-7M190 50l6 7 6-7M202 50l6 7 6-7M214 50l6 7 6-7M226 50l6 7 6-7M238 50l6 7 6-7M250 50l6 7 6-7M262 50l6 7 6-7M118 60l6 7 6-7M130 60l6 7 6-7M142 60l6 7 6-7M154 60l6 7 6-7M166 60l6 7 6-7M178 60l6 7 6-7M190 60l6 7 6-7M202 60l6 7 6-7M214 60l6 7 6-7M226 60l6 7 6-7M238 60l6 7 6-7M250 60l6 7 6-7M262 60l6 7 6-7" stroke="rgba(255,255,255,.55)" stroke-width="1.4" fill="none"/>
<path d="M110 84h176M110 80v8M286 80v8" stroke="#2f8f8a" stroke-width="2"/><text x="198" y="102" text-anchor="middle" font-size="11" fill="#1f2a44">scarf length ≈ height</text><text x="198" y="34" text-anchor="middle" font-size="11" fill="#1f2a44">width ≈ a hand span</text></svg>'''
scf = top("Scarf size chart and yarn calculator", "How long and wide a scarf should be for a child, teen, woman or man, plus infinity scarves and cowls. Pick a size and yarn to get the stitches to cast on, the chains to start and the yards to buy.", "Scarf size chart") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> an adult scarf is usually <strong>60 to 70 in long</strong> (150 to 180 cm) and <strong>6 to 8 in wide</strong>; men's often run a little longer, up to about 75 in. A child of 6 to 10 needs about 50 to 60 in, and a long scarf that wraps twice 75 to 90 in. An easy rule: make it about as long as the wearer is tall. A 65 × 7 in scarf takes roughly <strong>{sc_rng(_sw, 4)} yards</strong> of worsted knitted, or {sc_rng(_sw, 4, 1.27)} crocheted (our estimates).</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="sf-what">Who is it for?</label><select id="sf-what">{sc_opts}</select></div>
<div id="sf-hgt" hidden><div class="row2"><div class="field"><label for="sf-h">Wearer's height</label><input type="number" id="sf-h" value="66" min="20" max="250" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="sf-hw">Width</label><input type="number" id="sf-hw" value="7" min="1" max="40" step="0.5" inputmode="decimal"></div></div></div>
<div id="sf-custom" hidden><div class="row2"><div class="field"><label for="sf-l">Length</label><input type="number" id="sf-l" value="65" min="5" max="250" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="sf-w">Width</label><input type="number" id="sf-w" value="7" min="1" max="40" step="0.5" inputmode="decimal"></div></div>
<div class="field"><label for="sf-t">Shape</label><select id="sf-t"><option value="flat">Straight scarf</option><option value="loop">Loop (infinity or cowl): length is around</option></select></div></div>
<div class="field"><label for="sf-u">Unit</label><select id="sf-u"><option value="in">inches</option><option value="cm">cm</option></select></div>
<div class="field"><label>Made with</label><div class="seg" id="sf-craft" role="group" aria-label="Knit or crochet"><button type="button" data-v="knit" aria-pressed="true">Knitting</button><button type="button" data-v="crochet" aria-pressed="false">Crochet</button></div></div>
<div class="field"><label for="sf-yarn">Yarn weight</label><select id="sf-yarn">{sc_wopts}</select></div>
<div class="field"><label for="sf-tex">Stitch pattern</label><select id="sf-tex"><option value="1">Plain: stockinette, single or double crochet</option><option value="1.15">Garter or seed stitch</option><option value="1.25">Ribbing or textured stitches</option><option value="1.4">Cables or brioche</option></select></div>
<div class="row2"><div class="field"><label for="sf-sk">Yards in one skein</label><input type="number" id="sf-sk" value="200" min="10" max="3000" step="1" inputmode="numeric"></div>
<div class="field"><label for="sf-fr">Fringe</label><select id="sf-fr"><option value="0">No fringe</option><option value="4">Short fringe, 4 in</option><option value="6">Long fringe, 6 in</option></select></div></div>
<figure class="co-fig"><svg id="sf-svg" viewBox="0 0 320 170" role="img" aria-label="Your scarf drawn to scale next to a 6 ft ruler"></svg><figcaption class="note" id="sf-cap">Your scarf, to scale.</figcaption></figure>
</div>
<div class="result" aria-live="polite" id="sf-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>Scarf size chart: how long and wide should a scarf be?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Scarf</th><th scope="col">Length (or around)</th><th scope="col">Width</th><th scope="col">Notes</th></tr></thead><tbody>{sc_crows}</tbody></table></div>
<p class="note" style="margin-top:12px">Ranges drawn from the Madison Knitters' Guild sizing guide (children 4–5: 35–40 in, 6–10: 50–60 in; women 45–70 in, men 60–80 in; widths 5–7 in; child cowls 18–22 in around), Desert Blossom Crafts (5–8 in typical width, 4 in or less for skinny, super long 90–120 in), AllFreeCrochet (adult average about 65 in) and Sew Guide (infinity about 58 in around, stole about 20 × 70 in). Teen sizes, the widths we picked and the cowl range are our middle-of-the-road choices.</p>
</div></section>
{AD.format("sf-mid")}
<section style="padding-top:0"><div class="wrap"><h2>How much yarn for a scarf?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Scarf</th><th scope="col">Worsted, knit</th><th scope="col">Worsted, crochet</th><th scope="col">Bulky, knit</th><th scope="col">Bulky, crochet</th></tr></thead><tbody>{sc_yrows}</tbody></table></div>
<p class="note" style="margin-top:12px">Yards, for plain stitches, from the same area model as our <a href="{href("yarn-calculator.html")}">yarn calculator</a>: our estimates, with crochet using about a quarter more. Ribbing, cables and brioche take more; the calculator adds for them. Buy an extra skein from the same dye lot if you can.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose">
<h2>Is there a rule for scarf length?</h2>
<figure class="co-fig">{SC_RULER}<figcaption class="note">Our drawing of the old rule of thumb.</figcaption></figure>
<p>The old rule is to make a scarf about as long as the wearer is tall, or as long as their arm span. It's a starting point, not a law: AllFreeCrochet notes plenty of people prefer shorter. For width, a hand span (thumb to little finger, spread) is a handy guide, and a longer scarf usually looks better a little wider. Choose "As long as the wearer is tall" in the calculator to use it.</p>
<h2>How wide should a scarf be?</h2>
<p>About 6 to 8 in for most adult scarves, 5 to 7 in for a classic men's scarf, 3 to 5 in for children, and 4 in or less for a skinny scarf. Wraps and stoles are 18 to 22 in wide. Remember that ribbing pulls in, so swatch in the real stitch before you count your cast on.</p>
<h2>How long is an infinity scarf?</h2>
<p>An infinity scarf that loops twice is about 56 to 60 in around and 8 to 10 in wide. A cowl that sits close to the neck in one loop is about 24 to 30 in around, and a child's cowl about 18 to 22 in. Knit it flat and sew the ends together (add a twist first for a Möbius look), or work it in the round; see <a href="{href("how-to-knit-in-the-round.html")}">how to knit in the round</a>.</p>
<h2>How many stitches do I cast on for a scarf?</h2>
<p>Multiply the width by your stitches per inch. At 18 stitches per 4 in (4.5 per inch), a 7 in scarf needs about 32 stitches. In crochet, add the turning chain to the foundation chain. The calculator does this from the typical gauge for your yarn; use your own with the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> or the <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a>.</p>
<h2>Are scarves safe for toddlers?</h2>
<p>Long scarves can catch on things, so many makers skip them for children under about 3 or 4 (AllFreeCrochet raises the same worry) and make a snug cowl or neck warmer instead. For any child's scarf, leave off loose fringe, buttons and pom-poms that could come off.</p>
<h2>How much yarn does fringe take?</h2>
<p>More than you'd think. Each tassel is folded in half, so every strand is twice the fringe length plus about an inch for the knot. With 4 strands per tassel, a tassel every inch or so, and fringe at both ends, a 7 in wide scarf with 6 in fringe uses about 20 yards. The calculator adds it for you.</p>
<p>What next? Make it a gift: check the timing in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>, size matching headwear with the <a href="{href("hat-size-chart.html")}">hat size chart</a>, and when you finish, <a href="{href("how-to-bind-off-knitting.html")}">bind off</a> loosely and <a href="{href("how-to-weave-in-ends.html")}">weave in the ends</a>.</p></div></section>'''
scf_faq = [
    ("How long should a scarf be?", "60 to 70 in (150 to 180 cm) for most adults, up to about 75 in for men, 50 to 60 in for children of 6 to 10, and 75 to 90 in for a long scarf that wraps twice. A simple rule is about the wearer's height."),
    ("How wide should a scarf be?", "About 6 to 8 in for adults, 5 to 7 in for a classic men's scarf, 3 to 5 in for children and 4 in or less for a skinny scarf."),
    ("How much yarn do I need for a scarf?", f"Roughly {sc_rng(_sw, 4)} yards of worsted for a 65 × 7 in knitted scarf, or {sc_rng(_sw, 4, 1.27)} crocheted. Bulky yarn takes about {sc_rng(_sw, 5)} yards knitted. These are our estimates for plain stitches; ribbing and cables take more."),
    ("How long is an infinity scarf?", "About 56 to 60 in around and 8 to 10 in wide so it loops twice. A one-loop cowl is about 24 to 30 in around."),
    ("How long should a child's scarf be?", "About 35 to 40 in for ages 4 to 5 and 50 to 60 in for ages 6 to 10, and 3 to 5 in wide. For toddlers, a cowl is safer."),
    ("How many stitches do I cast on for a scarf?", "Width times stitches per inch. In worsted at 18 stitches per 4 in, a 7 in scarf is about 32 stitches. Swatch in your stitch pattern first."),
]
page("scarf-size-chart.html", "Scarf Size Chart: How Long and Wide Should a Scarf Be? (+ Yarn Calculator) | Purl & Paper",
     "Scarf size chart for children, teens, women and men, plus infinity scarves and cowls, with a free calculator for the stitches to cast on, the chains to start and the yards of yarn to buy.",
     scf, scf_faq, "Scarf size chart", app_name="Scarf size and yarn calculator")


# ---------------- CROCHET & KNITTING TIME ESTIMATOR ----------------
# Stitch count = (width × stitches per inch) × (length × rows per inch); hours = stitches × time per stitch ÷ pace.
# Typical stitches per 4 in: middle of the Craft Yarn Council ranges (knit stockinette, crochet sc). Row and time factors are our estimates.
TE_K = {1: 28, 2: 24, 3: 22, 4: 18, 5: 14, 6: 9, 7: 6}
TE_C = {1: 26, 2: 18, 3: 14, 4: 12, 5: 9, 6: 8, 7: 6}
# id: (craft, label, stitches factor, rows per 4 in as a multiple of stitches per 4 in, time per stitch vs a plain sc / knit stitch, finishing)
TE_ST = {"sc": ("c", "Single crochet", 1.0, 1.2, 1.0, 1.05), "hdc": ("c", "Half double crochet", 0.95, 0.85, 1.25, 1.05),
         "dc": ("c", "Double crochet", 0.9, 0.6, 1.5, 1.05), "granny": ("c", "Granny squares or clusters (joined)", 0.9, 0.6, 1.6, 1.15),
         "moss": ("c", "Moss or linen stitch (sc, ch 1)", 1.0, 1.2, 0.85, 1.05), "textured": ("c", "Bobbles, puffs or textured", 0.9, 0.8, 1.8, 1.05),
         "st": ("k", "Stockinette", 1.0, 1.33, 1.0, 1.05), "garter": ("k", "Garter stitch", 1.0, 1.8, 1.0, 1.05),
         "rib": ("k", "Ribbing", 1.2, 1.33, 1.15, 1.05), "seed": ("k", "Seed or moss stitch", 1.0, 1.5, 1.25, 1.05),
         "cable": ("k", "Cables", 1.15, 1.33, 1.5, 1.05), "colour": ("k", "Colourwork (Fair Isle)", 1.05, 1.1, 1.6, 1.1)}
TE_PROJ = [("dish", "Dishcloth", 8, 8), ("hat", "Adult hat", 20, 8), ("cowl", "Cowl", 27, 9), ("scarf", "Scarf", 65, 7), ("pillow", "Cushion cover (front and back)", 36, 18),
           ("baby", "Baby blanket", 36, 36), ("throw", "Throw blanket", 50, 60), ("twin", "Twin blanket", 66, 90), ("queen", "Queen blanket", 90, 90), ("king", "King blanket", 108, 90)]
for _b in D["blankets"]:
    for _i, _p in enumerate(TE_PROJ):
        if _p[0] == _b["id"]: TE_PROJ[_i] = (_p[0], _p[1], _b["w"], _b["l"])
def te_sts(w, l, wn, st):
    s = TE_ST[st]; base = (TE_C if s[0] == "c" else TE_K)[wn] * s[2]
    return (w * base / 4) * (l * base * s[3] / 4)
def te_hrs(w, l, wn, st, spm=20): s = TE_ST[st]; return te_sts(w, l, wn, st) * s[4] * s[5] / spm / 60
def te_fmt(h):
    if h < 1: return f"{max(5, round(h * 60 / 5) * 5):.0f} min"
    return f"{h:.1f} h" if h < 10 else f"{h:,.0f} h"
def te_rng(h): return f"{te_fmt(h * 0.8)}–{te_fmt(h * 1.2)}"
te_popts = "".join(f'<option value="{k}|{w}|{l}"{" selected" if k == "throw" else ""}>{e(n)}, {w} × {l} in</option>' for k, n, w, l in TE_PROJ) + '<option value="custom">My own size</option><option value="count">I know the stitch count</option>'
te_wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])})</option>' for w in D["weights"] if 1 <= w["n"] <= 7)
te_copts = "".join(f'<option value="{k}" data-c="{s[0]}"{" selected" if k == "sc" else ""}>{e(s[1])}</option>' for k, s in TE_ST.items())
te_rows = "".join(f'<tr><th scope="row">{e(n)}<br><span class="muted">{w} × {l} in</span></th><td>{te_rng(te_hrs(w, l, 4, "sc"))}</td><td>{te_rng(te_hrs(w, l, 4, "dc"))}</td><td>{te_rng(te_hrs(w, l, 4, "st"))}</td><td>{te_rng(te_hrs(w, l, 5, "dc"))}</td></tr>' for k, n, w, l in TE_PROJ)
_te_th = [p for p in TE_PROJ if p[0] == "throw"][0]; _te_bb = [p for p in TE_PROJ if p[0] == "baby"][0]; _te_sf = [p for p in TE_PROJ if p[0] == "scarf"][0]; _te_ht = [p for p in TE_PROJ if p[0] == "hat"][0]
_te_ths = te_sts(_te_th[2], _te_th[3], 4, "sc")
TE_SVG = '''<svg viewBox="0 0 300 130" role="img" aria-label="Taller stitches cover more fabric per stitch: single, half double and double crochet side by side"><rect width="300" height="130" fill="#fff"/>
<path d="M20 112h260" stroke="#1f2a44" stroke-width="2"/>
<g stroke="#b8326a" stroke-width="3" stroke-linecap="round"><path d="M40 112v-22M52 112v-22M64 112v-22"/></g><g stroke="#f4a823" stroke-width="3" stroke-linecap="round"><path d="M120 112v-32M132 112v-32M144 112v-32"/></g><g stroke="#2f8f8a" stroke-width="3" stroke-linecap="round"><path d="M200 112v-46M212 112v-46M224 112v-46"/><path d="M196 92l20-6M208 92l20-6" stroke-width="2"/></g>
<path d="M120 94l16-5M132 94l16-5" stroke="#f4a823" stroke-width="2"/>
<g font-size="11" fill="#1f2a44" font-weight="700" text-anchor="middle"><text x="52" y="76">sc</text><text x="132" y="68">hdc</text><text x="212" y="56">dc</text></g>
<g font-size="10" fill="#1f2a44" text-anchor="middle"><text x="52" y="126">short, quick</text><text x="132" y="126">a bit taller</text><text x="212" y="126">tallest: fewer rows</text></g>
<text x="270" y="28" font-size="10" fill="#1f2a44" text-anchor="end">same width, fewer rows to fill a blanket</text></svg>'''
tep = top("How long does it take to crochet or knit a blanket?", "A free time calculator for crochet and knitting. Pick the project, yarn and stitch, set your pace (or time yourself for one minute), and see the stitches, the hours and the date you'll finish. Handy for Christmas gifts and commissions.", "Crochet and knitting time calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> a {_te_th[2]} × {_te_th[3]} in throw in worsted single crochet is about <strong>{round(_te_ths, -3):,.0f} stitches</strong>, which at a steady 20 stitches a minute is roughly <strong>{te_rng(te_hrs(_te_th[2], _te_th[3], 4, "sc"))}</strong> of crochet. In double crochet it's about {te_rng(te_hrs(_te_th[2], _te_th[3], 4, "dc"))}, because taller stitches fill the blanket with fewer rows. A baby blanket is about a third of a throw, a scarf {te_rng(te_hrs(_te_sf[2], _te_sf[3], 4, "dc"))} and a hat {te_rng(te_hrs(_te_ht[2], _te_ht[3], 4, "dc"))}. These are our estimates: time yourself for one minute below and the calculator uses your own pace.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label>Made with</label><div class="seg" id="te-craft" role="group" aria-label="Crochet or knitting"><button type="button" data-v="c" aria-pressed="true">Crochet</button><button type="button" data-v="k" aria-pressed="false">Knitting</button></div></div>
<div class="field"><label for="te-what">Project</label><select id="te-what">{te_popts}</select></div>
<div id="te-custom" hidden><div class="row2"><div class="field"><label for="te-w">Width</label><input type="number" id="te-w" value="40" min="1" max="200" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="te-l">Length</label><input type="number" id="te-l" value="50" min="1" max="200" step="0.5" inputmode="decimal"></div></div>
<div class="field"><label for="te-u">Unit</label><select id="te-u"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div id="te-cnt" hidden><div class="field"><label for="te-n">Total stitches</label><input type="number" id="te-n" value="20000" min="10" max="2000000" step="10" inputmode="numeric"></div><p class="note" style="margin:-4px 0 12px">Stitches per row × rows. Patterns often give the count for each round or row.</p></div>
<div id="te-size"><div class="field"><label for="te-yarn">Yarn weight</label><select id="te-yarn">{te_wopts}</select></div>
<div class="field"><label for="te-st">Main stitch</label><select id="te-st">{te_copts}</select></div></div>
<div class="field"><label for="te-spm">Your pace</label><select id="te-spm"><option value="10">Relaxed or new: about 10 stitches a minute</option><option value="15">Getting there: about 15</option><option value="20" selected>Steady: about 20</option><option value="25">Confident: about 25</option><option value="30">Quick: about 30</option><option value="40">Very fast: about 40</option><option value="own">My own pace</option></select></div>
<div id="te-own" hidden><div class="row2"><div class="field"><label for="te-my">Stitches in one minute</label><input type="number" id="te-my" value="20" min="1" max="150" step="1" inputmode="numeric"></div>
<div class="field"><label>&nbsp;</label><button type="button" class="btn sm" id="te-go">Time me for 1 minute</button></div></div><p class="note" id="te-tnote" style="margin:-4px 0 12px">Press the button, work your main stitch at your normal speed, and type how many you made when it beeps.</p></div>
<div class="row2"><div class="field"><label for="te-hd">Hours a day</label><input type="number" id="te-hd" value="1" min="0.1" max="16" step="0.25" inputmode="decimal"></div>
<div class="field"><label for="te-dw">Days a week</label><select id="te-dw"><option value="7">Every day</option><option value="6">6 days</option><option value="5" selected>5 days</option><option value="4">4 days</option><option value="3">3 days</option><option value="2">Weekends</option><option value="1">1 day</option></select></div></div>
<div class="field"><label for="te-by">Needed by (optional)</label><input type="date" id="te-by"></div>
</div>
<div class="result" aria-live="polite" id="te-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How long does it take to crochet or knit? Time chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Project</th><th scope="col">Worsted, single crochet</th><th scope="col">Worsted, double crochet</th><th scope="col">Worsted, knit stockinette</th><th scope="col">Bulky, double crochet</th></tr></thead><tbody>{te_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Hours at a steady 20 stitches a minute, our estimates. Stitch counts use the middle of the Craft Yarn Council's typical gauge for each yarn weight; rows per inch, the extra time for taller stitches and 5% for edging and ends are our own figures. For scale, Briana K Designs counts about 42,000 stitches in a 50 × 60 in throw, and LoveCrochet puts a blanket at 20 to 30 hours and a hat at 7 to 12 hours depending on skill. Twice as fast? Halve the hours.</p>
</div></section>
{AD.format("te-mid")}
<section style="padding-top:0"><div class="narrow prose">
<h2>How do I work out how long a project will take?</h2>
<ol><li><strong>Count the stitches.</strong> Stitches across × rows. Use your swatch: stitches per inch × width, and rows per inch × length. Or take the counts from the pattern.</li>
<li><strong>Time yourself.</strong> Set a timer for one minute and work your main stitch at your normal speed, not your fastest. Do it twice and take the average.</li>
<li><strong>Divide.</strong> Stitches ÷ stitches per minute ÷ 60 = hours. Add about 5% for edging and weaving in ends, more for seaming squares.</li>
<li><strong>Spread it out.</strong> Hours ÷ hours a day = days. Most people craft less than they think, so count real evenings, not perfect ones.</li></ol>
<p>The calculator does all four. It also gives a range of 20% either way, because nobody keeps the same pace for 30 hours.</p>
<h2>Which crochet stitch is fastest for a blanket?</h2>
<figure class="co-fig">{TE_SVG}<figcaption class="note">Our drawing: taller stitches cover more height per stitch.</figcaption></figure>
<p>Double crochet usually finishes a blanket fastest of the basic stitches. Each one takes a little longer than a single crochet, but it's about twice as tall, so you need far fewer rows. By our estimate a worsted throw takes about {te_rng(te_hrs(_te_th[2], _te_th[3], 4, "sc"))} in single crochet and {te_rng(te_hrs(_te_th[2], _te_th[3], 4, "dc"))} in double crochet. Going up a yarn weight saves even more: the same throw in bulky double crochet is about {te_rng(te_hrs(_te_th[2], _te_th[3], 5, "dc"))}. Bobbles, puffs and cables are slow, and granny squares add time for joining.</p>
<h2>Is crochet faster than knitting?</h2>
<p>Usually, yes, for the same fabric. Crochet stitches are taller than knit stitches, so you need fewer of them to cover the same area. Our chart puts a worsted throw at about {te_rng(te_hrs(_te_th[2], _te_th[3], 4, "st"))} in stockinette against {te_rng(te_hrs(_te_th[2], _te_th[3], 4, "dc"))} in double crochet. A fast knitter can still beat a slow crocheter, so time yourself.</p>
<h2>Can I finish a handmade gift by Christmas?</h2>
<p>Put the date in "Needed by" and the calculator says whether you're on track, or how many minutes a day you'd need. If the answer is a stretch, pick a thicker yarn, a taller stitch or a smaller project: a throw becomes a lap blanket, a blanket becomes a cowl. Planning several gifts? The <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a> adds them all up against the days you have left.</p>
<h2>How do I use the hours to price my work?</h2>
<p>Hours are the biggest part of a fair price for crochet and knitting. Multiply them by the hourly rate you want, add materials and fees, and you have a starting price. Our guides do the sums: <a href="{href("how-to-price-a-crochet-blanket.html")}">how to price a crochet blanket</a>, <a href="{href("how-to-price-amigurumi.html")}">how to price amigurumi</a> and <a href="{href("how-to-price-crochet-items.html")}">how to price crochet items</a>. For commissions, quote from the slow end of the range: something always comes up.</p>
<h2>How can I crochet or knit faster?</h2>
<ul><li><strong>Hold the yarn the same way every time</strong> so your tension stays even and you don't stop to adjust.</li>
<li><strong>Use a smooth yarn and a hook or needles that suit you.</strong> Splitty or sticky yarn slows every stitch.</li>
<li><strong>Keep the work close to the tip</strong> and make small movements; most speed comes from wasting less motion.</li>
<li><strong>Count with a <a href="{href("row-counter.html")}">row counter</a></strong> so you don't stop to recount.</li>
<li><strong>Weave in ends as you go</strong> so the finishing doesn't pile up at the end (see <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>).</li></ul>
<p>What next? Get the size right with the <a href="{href("blanket-size-calculator.html")}">blanket size chart</a>, the yarn with the <a href="{href("yarn-calculator.html")}">yarn calculator</a>, and plan colours with the <a href="{href("stripe-generator.html")}">random stripe generator</a>.</p></div></section>'''
te_faq = [
    ("How long does it take to crochet a blanket?", f"By our estimate a {_te_th[2]} × {_te_th[3]} in throw in worsted yarn takes about {te_rng(te_hrs(_te_th[2], _te_th[3], 4, 'sc'))} in single crochet or {te_rng(te_hrs(_te_th[2], _te_th[3], 4, 'dc'))} in double crochet at 20 stitches a minute. A {_te_bb[2]} in baby blanket takes about {te_rng(te_hrs(_te_bb[2], _te_bb[3], 4, 'dc'))} in double crochet."),
    ("How many stitches are in a crochet blanket?", f"Tens of thousands. A {_te_th[2]} × {_te_th[3]} in throw in worsted single crochet is about {round(_te_ths, -3):,.0f} stitches by our estimate, and Briana K Designs counts about 42,000. Double crochet needs far fewer."),
    ("How many stitches per minute does the average crocheter make?", "Something like 10 to 35 stitches a minute, depending on experience and the stitch. Briana K Designs' time estimator runs from 10 for a relaxed pace to 35 for a quick one. Time yourself for one minute to know yours."),
    ("How long does it take to knit a blanket?", f"About {te_rng(te_hrs(_te_th[2], _te_th[3], 4, 'st'))} for a worsted throw in stockinette at 20 stitches a minute (our estimate), and about half that in bulky yarn. Garter and cables take longer."),
    ("How long does it take to crochet a scarf?", f"About {te_rng(te_hrs(_te_sf[2], _te_sf[3], 4, 'dc'))} for a 65 × 7 in worsted scarf in double crochet at 20 stitches a minute, or {te_rng(te_hrs(_te_sf[2], _te_sf[3], 4, 'sc'))} in single crochet (our estimates)."),
    ("What is the fastest crochet stitch for a blanket?", "Of the basic stitches, double crochet: it is about twice as tall as single crochet, so a blanket needs far fewer rows. Treble crochet and a bigger yarn are faster still."),
]
page("crochet-time-estimator.html", "How Long Does It Take to Crochet a Blanket? (Time Calculator) | Purl & Paper",
     "Free crochet and knitting time calculator: stitches, hours and your finish date for a blanket, scarf, hat or any size, by yarn, stitch and your own pace, with a time chart from dishcloth to king blanket.",
     tep, te_faq, "Crochet and knitting time calculator", app_name="Crochet and knitting time calculator")

# ---------------- RANDOM STRIPE GENERATOR ----------------
SG_PAL = ["#1f2a44", "#b8326a", "#f4a823", "#2f8f8a", "#e9dfcf", "#8a5a9e", "#d9643a", "#7fb069"]
SG_DEMO = '<svg viewBox="0 0 300 110" role="img" aria-label="Three stripe styles: random widths, Fibonacci widths and an even repeat"><rect width="300" height="110" fill="#fff"/>' + "".join(
    f'<rect x="{x0}" y="{y}" width="80" height="{h}" fill="{SG_PAL[c]}"/>' for x0, seq in ((10, [(0, 6), (2, 14), (1, 4), (3, 10), (0, 8), (2, 4), (1, 12), (3, 8), (0, 10), (2, 4)]),
                                                                          (110, [(0, 4), (1, 4), (2, 8), (3, 12), (0, 20), (1, 12), (2, 8), (3, 4), (0, 4), (1, 4)]),
                                                                          (210, [(0, 8), (1, 8), (2, 8), (3, 8), (0, 8), (1, 8), (2, 8), (3, 8), (0, 8), (1, 8)]))
    for c, h, y in (lambda s: [(c, h, 6 + sum(hh for _, hh in s[:i])) for i, (c, h) in enumerate(s)])(seq)) + \
    '<g font-size="11" fill="#1f2a44" font-weight="700" text-anchor="middle"><text x="50" y="104">Random</text><text x="150" y="104">Fibonacci</text><text x="250" y="104">Even repeat</text></g></svg>'
sgp = top("Random stripe generator", "Pick your yarn colours and how many rows, and get a random stripe pattern for a crochet or knitting blanket, scarf or hat. Shuffle until you love it, then print the row-by-row list. Fibonacci and even stripes too.", "Random stripe generator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>How it works:</strong> choose 2 to 8 colours, the total number of rows and the narrowest and widest stripe you want. Press <strong>Shuffle</strong> for a new random pattern; the preview and the row list update at once. The generator never puts the same colour next to itself, keeps your last pattern on this device, and can split your yarn between the colours. For an even-looking blanket, use even stripe widths (2, 4, 6 rows) so you can carry the yarn up the side.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label for="sg-n">How many colours?</label><select id="sg-n"><option>2</option><option>3</option><option selected>4</option><option>5</option><option>6</option><option>7</option><option>8</option></select></div>
<div class="field"><label>Your colours</label><div class="sg-cols" id="sg-cols"></div><p class="note" style="margin:6px 0 0">Tap a swatch to change its colour. Names are optional, for the printed list.</p></div>
<div class="field"><label for="sg-mode">Stripe style</label><select id="sg-mode"><option value="random">Random widths</option><option value="fib">Fibonacci (1, 1, 2, 3, 5, 8 rows)</option><option value="even">Even repeat</option></select></div>
<div class="row2"><div class="field"><label for="sg-rows">Total rows</label><input type="number" id="sg-rows" value="120" min="4" max="1000" step="1" inputmode="numeric"></div>
<div class="field"><label for="sg-mult">Stripe widths in steps of</label><select id="sg-mult"><option value="1">1 row</option><option value="2" selected>2 rows (carry yarn up the side)</option><option value="4">4 rows</option></select></div></div>
<div class="row2" id="sg-rng"><div class="field"><label for="sg-min">Narrowest stripe (rows)</label><input type="number" id="sg-min" value="2" min="1" max="100" step="1" inputmode="numeric"></div>
<div class="field"><label for="sg-max">Widest stripe (rows)</label><input type="number" id="sg-max" value="10" min="1" max="200" step="1" inputmode="numeric"></div></div>
<div class="field"><label for="sg-yd">Total yarn for the project, yards (optional)</label><input type="number" id="sg-yd" value="" min="0" max="20000" step="10" inputmode="numeric" placeholder="for example 1500"></div>
<div class="btns" style="margin-top:8px"><button type="button" class="btn" id="sg-go">Shuffle</button><button type="button" class="btn ghost" id="sg-print">Print pattern</button></div>
</div>
<div class="result" aria-live="polite"><figure class="co-fig" style="margin:0 0 12px"><svg id="sg-svg" viewBox="0 0 300 200" role="img" aria-label="Preview of your striped blanket"></svg><figcaption class="note">Your stripes, to scale, row 1 at the bottom.</figcaption></figure><div id="sg-out"></div></div>
</div></section>
{AD.format("sg-mid")}
<section style="padding-top:0"><div class="narrow prose">
<h2>Random, Fibonacci or even stripes?</h2>
<figure class="co-fig">{SG_DEMO}<figcaption class="note">Our drawing of the three styles in the generator.</figcaption></figure>
<ul><li><strong>Random stripes</strong> pick a colour and a width at random each time, between your narrowest and widest stripe. They look relaxed and scrappy, and they're great for using up leftovers.</li>
<li><strong>Fibonacci stripes</strong> use widths from the Fibonacci sequence (1, 1, 2, 3, 5, 8, each the sum of the two before), going up and back down. The widths feel balanced, which is why the sequence turns up in so many designs.</li>
<li><strong>Even stripes</strong> repeat every colour at the same width. Classic, easy to memorise, and simple to plan yarn for.</li></ul>
<h2>How many rows should a stripe be?</h2>
<p>Use an even number of rows (2, 4, 6) when you work flat in rows. Then every new colour starts on the same edge as the last, and you can carry the unused yarn loosely up the side instead of cutting it, which means far fewer ends to weave in. Set "Stripe widths in steps of" to 2 rows. Odd widths are fine too; you'll just cut the yarn more often. Our guide to <a href="{href("how-to-change-colors-in-crochet.html")}">changing colours in crochet</a> shows how to switch neatly and when to carry or cut.</p>
<h2>How do I choose colours for a striped blanket?</h2>
<ul><li><strong>Mix light, medium and dark.</strong> Stripes stand out through contrast in lightness more than in hue. Take a black and white photo of your yarns: if two look the same grey, they'll blur together.</li>
<li><strong>Pick one main colour</strong> and use it more often, then add one bright accent you use sparingly.</li>
<li><strong>Odd numbers of colours</strong> (3, 5, 7) make a repeat harder to spot, so random stripes look more random.</li>
<li><strong>Use the preview.</strong> If it looks too busy, raise the narrowest stripe; if it looks heavy, lower the widest.</li></ul>
<h2>How much yarn of each colour do I need?</h2>
<p>Enter the total yarn for the project and the generator splits it by the rows in each colour, plus 10% spare per colour. Don't know the total? Get it from the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>, <a href="{href("scarf-size-chart.html")}">scarf size chart</a> or <a href="{href("yarn-calculator.html")}">yarn calculator</a>. And for rows: multiply the length you want by your rows per inch, or use the "rows to reach a length" helper on the <a href="{href("row-counter.html")}">row counter</a>.</p>
<div class="callout"><strong>Want the weather to pick your stripes?</strong> A temperature blanket uses one stripe a day, coloured by the day's temperature. Plan one with the <a href="{href("temperature-blanket-planner.html")}">temperature blanket planner</a>.</div>
<h2>Will my stripes look the same in knitting and crochet?</h2>
<p>The order and widths will, but the height of a row differs. A row of double crochet is about twice as tall as a row of single crochet, and knitting rows are shorter still, so 120 rows can be anything from about 30 in to well over 60 in. Check your row gauge before you decide on the total. In knitting, change colour at the start of a right side row for clean stripes; in ribbing, the purl bumps of a new colour show on the front, so work the first row of each stripe in knit.</p>
<p>What next? Find out how long your striped blanket will take with the <a href="{href("crochet-time-estimator.html")}">crochet time calculator</a>, and tick off rows as you go with the <a href="{href("row-counter.html")}">row counter</a>.</p></div></section>'''
sg_faq = [
    ("What is a random stripe generator?", "A tool that picks stripe colours and widths for you so the pattern looks random, not planned. Ours lets you choose your yarn colours, the total rows and the narrowest and widest stripe, then prints a row-by-row list."),
    ("How do you make random stripes look good?", "Mix light, medium and dark colours, never put the same colour next to itself, and keep stripe widths within a range, for example 2 to 10 rows. Shuffle until the preview looks balanced."),
    ("What are Fibonacci stripes?", "Stripes whose widths follow the Fibonacci sequence: 1, 1, 2, 3, 5, 8 rows, where each number is the sum of the two before. Many designers use them because the widths look naturally balanced."),
    ("How many rows should each stripe be in crochet?", "An even number, like 2 or 4 rows, if you want to carry the yarn up the side instead of cutting it each time. Wider stripes mean fewer colour changes and fewer ends."),
    ("How do I work out how much yarn of each colour I need for stripes?", "Split the project's total yarn by the share of rows in each colour, and add about 10% for each. The generator does this when you enter the total."),
    ("How many colours should a striped blanket have?", "Anything from 2 for a classic stripe to 8 or more for a scrappy look. Three to five colours is a popular middle ground, and an odd number makes random stripes look less repetitive."),
]
page("stripe-generator.html", "Random Stripe Generator for Crochet and Knitting (Free) | Purl & Paper",
     "Free random stripe generator for crochet and knitting blankets, scarves and hats: pick your colours, rows and stripe widths, shuffle, and print a row-by-row stripe pattern with yarn per colour. Fibonacci and even stripes too.",
     sgp, sg_faq, "Random stripe generator", app_name="Random stripe generator")


# ---------------- BASIC CROCHET STITCHES (stitch library + step-by-step stepper, US/UK toggle) ----------------
def T(us, uk): return f'<span class="tm" data-us="{e(us)}" data-uk="{e(uk)}">{e(us)}</span>'
_BS_U = {"sl": 9, "sc": 22, "hdc": 32, "dc": 44, "tr": 58}
def bs_scene(kind, loops, act="", done=False, chains=0, yo=False):
    """Own step drawing: previous row of stitches, current row in berry, the hook with its loops."""
    g = '<rect width="260" height="170" fill="#fff"/>'
    if kind == "ch":
        n = chains
        for i in range(n):
            x = 196 - 22 * (n - i)
            g += f'<ellipse cx="{x}" cy="112" rx="11" ry="6.5" fill="#fbfcfa" stroke="{_Y}" stroke-width="3.4"/>'
        g += f'<path d="M{196 - 22 * n - 12} 112 q-18 4 -26 22" fill="none" stroke="{_Y2}" stroke-width="4" stroke-linecap="round"/>' if n else ""
        tipx, tipy = 200, 104
        g += f'<text x="14" y="160" font-size="11" fill="#4a5470">{n} chain{"" if n == 1 else "s"} made</text>' if n else '<text x="14" y="160" font-size="11" fill="#4a5470">slip knot on the hook</text>'
    else:
        h = _BS_U[kind]
        for i in range(6):   # previous row
            x = 24 + 34 * i
            g += f'<rect x="{x}" y="128" width="22" height="26" rx="5" fill="#e9dfcf" stroke="#1f2a44" stroke-width="1.6"/><ellipse cx="{x + 11}" cy="126" rx="12" ry="5" fill="#fbfcfa" stroke="#1f2a44" stroke-width="1.6"/>'
        for i in range(4 + (1 if done else 0)):   # current row
            x = 24 + 34 * i
            g += f'<rect x="{x + 3}" y="{120 - h}" width="16" height="{h}" rx="4" fill="#fbfcfa" stroke="{_Y}" stroke-width="3"/>'
            if kind in ("hdc", "dc", "tr"): g += f'<path d="M{x + 4} {120 - h * .55:.0f} l14 -6" stroke="{_Y}" stroke-width="2.4"/>'
            if kind == "tr": g += f'<path d="M{x + 4} {120 - h * .3:.0f} l14 -6" stroke="{_Y}" stroke-width="2.4"/>'
            g += f'<ellipse cx="{x + 11}" cy="{118 - h}" rx="12" ry="5" fill="#fbfcfa" stroke="{_Y}" stroke-width="3"/>'
        g += f'<ellipse cx="{24 + 34 * 4 + 11}" cy="126" rx="12" ry="5" fill="none" stroke="{_TL}" stroke-width="3" stroke-dasharray="{"0" if done else "4 3"}"/>'
        if act == "insert": tipx, tipy = 24 + 34 * 4 + 12, 128
        else: tipx, tipy = 206, 112 - h
    # hook shaft from tip up and to the right
    ang = _m.radians(-50); L = 120
    ex, ey = tipx + L * _m.cos(ang), tipy + L * _m.sin(ang)
    g += f'<line x1="{tipx}" y1="{tipy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{_HK}" stroke-width="7" stroke-linecap="round"/><path d="M{tipx} {tipy} q-8 2 -8 -7" fill="none" stroke="{_HK}" stroke-width="4" stroke-linecap="round"/>'
    for j in range(loops):
        d = 22 + 13 * j; cx, cy = tipx + d * _m.cos(ang), tipy + d * _m.sin(ang)
        g += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="5" ry="11" transform="rotate(-50 {cx:.1f} {cy:.1f})" fill="none" stroke="{_MG if (yo and j == 0 and act != "pull") else _Y}" stroke-width="3.6"/>'
    if act == "yo":
        g += f'<path d="M{tipx - 4} {tipy - 18} q-16 4 -8 18" fill="none" stroke="{_MG}" stroke-width="4" stroke-linecap="round"/><path d="M{tipx - 13} {tipy + 1} l1 -8 M{tipx - 13} {tipy + 1} l7 -3" stroke="{_MG}" stroke-width="3" stroke-linecap="round"/>'
    if act.startswith("pull"):
        k = int(act[4:] or 1); d1 = 22 + 13 * (k - 1) + 10
        x1, y1 = tipx + d1 * _m.cos(ang), tipy + d1 * _m.sin(ang)
        g += f'<path d="M{tipx + 8} {tipy + 6} Q{(tipx + x1) / 2 + 22:.0f} {(tipy + y1) / 2 + 18:.0f} {x1 + 10:.1f} {y1 + 6:.1f}" fill="none" stroke="{_TL}" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="6 4"/><circle cx="{x1 + 10:.1f}" cy="{y1 + 6:.1f}" r="4" fill="{_TL}"/>'
    if act == "insert":
        g += f'<text x="{tipx - 16}" y="166" font-size="11" fill="{_TL}" font-weight="700" text-anchor="end">into this stitch</text>'
    g += f'<text x="14" y="22" font-size="12" fill="#1f2a44" font-weight="700">{loops} loop{"" if loops == 1 else "s"} on hook</text>'
    return g

# kind, US name, UK name, US abbr, UK abbr, turning chain, steps [(title, text, loops, act, done, chains, yo)]
BS = [
 ("ch", "chain", "chain", "ch", "ch", "—", [
   ("Slip knot on the hook", "Make a slip knot and put it on the hook. It isn't counted as a chain.", 1, "", False, 0, False),
   ("Yarn over", "Wrap the yarn over the hook from back to front.", 1, "yo", False, 0, True),
   ("Pull through", "Pull the wrapped yarn through the loop on the hook. That's 1 chain. Repeat for as many as you need.", 1, "pull1", False, 1, False),
   ("Keep going", "Count the V shapes, not the loop on the hook. Keep them loose and even so the next row goes in easily.", 1, "", False, 5, False)]),
 ("sl", "slip stitch", "slip stitch", "sl st", "ss", "none", [
   ("Insert the hook", "Put the hook into the stitch, under both top loops.", 1, "insert", False, 0, False),
   ("Yarn over", "Wrap the yarn over the hook.", 1, "yo", False, 0, True),
   ("Pull through everything", "Pull the yarn through the stitch and the loop on the hook in one go. Done: the flattest stitch, used to join rounds and move along an edge.", 1, "pull1", True, 0, False)]),
 ("sc", "single crochet", "double crochet", "sc", "dc", "1", [
   ("Insert the hook", "Put the hook into the stitch, under both top loops.", 1, "insert", False, 0, False),
   ("Yarn over and pull up a loop", "Wrap the yarn and pull it back through the stitch.", 2, "pull1", False, 0, False),
   ("Yarn over", "Wrap the yarn over the hook again.", 2, "yo", False, 0, True),
   ("Pull through both loops", "Pull through the 2 loops on the hook. One stitch done, 1 loop left.", 1, "pull2", True, 0, False)]),
 ("hdc", "half double crochet", "half treble", "hdc", "htr", "2", [
   ("Yarn over first", "Wrap the yarn over the hook before you go into the stitch.", 2, "yo", False, 0, True),
   ("Insert the hook", "Put the hook into the next stitch.", 2, "insert", False, 0, False),
   ("Yarn over and pull up a loop", "Wrap and pull back through the stitch. You have 3 loops.", 3, "pull1", False, 0, False),
   ("Yarn over, pull through all 3", "Wrap once more and pull through all 3 loops at once. Done.", 1, "pull3", True, 0, False)]),
 ("dc", "double crochet", "treble", "dc", "tr", "3", [
   ("Yarn over first", "Wrap the yarn over the hook once.", 2, "yo", False, 0, True),
   ("Insert the hook", "Put the hook into the next stitch.", 2, "insert", False, 0, False),
   ("Yarn over and pull up a loop", "Wrap and pull back through the stitch. You have 3 loops.", 3, "pull1", False, 0, False),
   ("Yarn over, pull through 2", "Wrap and pull through the first 2 loops only. 2 loops left.", 2, "pull2", False, 0, False),
   ("Yarn over, pull through the last 2", "Wrap and pull through the last 2 loops. Done.", 1, "pull2", True, 0, False)]),
 ("tr", "treble crochet", "double treble", "tr", "dtr", "4", [
   ("Yarn over twice", "Wrap the yarn over the hook two times.", 3, "yo", False, 0, True),
   ("Insert the hook", "Put the hook into the next stitch.", 3, "insert", False, 0, False),
   ("Yarn over and pull up a loop", "Wrap and pull back through the stitch. You have 4 loops.", 4, "pull1", False, 0, False),
   ("Yarn over, pull through 2", "Wrap and pull through the first 2 loops only. 3 loops left.", 3, "pull2", False, 0, False),
   ("Yarn over, pull through 2 again", "Wrap and pull through the next 2 loops. 2 loops left.", 2, "pull2", False, 0, False),
   ("Yarn over, pull through the last 2", "Wrap and pull through the last 2 loops: one treble finished. It's the tallest of the basic stitches.", 1, "pull2", True, 0, False)]),
]
BS_USE = {"ch": "Starting chains, spaces in lace and granny squares, turning chains", "sl": "Joining rounds, moving along an edge, a firm edging",
          "sc": "Amigurumi, dishcloths, bags, firm dense fabric", "hdc": "Hats, blankets, a warm fabric that works up quicker than sc",
          "dc": "Blankets, granny squares, shawls: fast and drapey", "tr": "Lace, tall rows, fast airy blankets"}
BS_H = {"ch": "—", "sl": "almost flat", "sc": "1 (square-ish)", "hdc": "about 1½", "dc": "about 2", "tr": "about 2½ to 3"}
def bs_svg(kind, st, i):
    t, txt, lp, act, dn, chn, yo = st
    return f'<svg viewBox="0 0 260 170" role="img" aria-label="{e(t)}">{bs_scene(kind, lp, act, dn, chn, yo)}</svg>'
BS_JS = {k: [{"t": s[0], "x": s[1], "s": bs_svg(k, s, i)} for i, s in enumerate(st)] for k, us, uk, a, ua, tc, st in BS}
bs_tabs = "".join(f'<button type="button" data-v="{k}" aria-pressed="{"true" if k == "sc" else "false"}">{T(a, ua)}</button>' for k, us, uk, a, ua, tc, st in BS)
bs_rows = "".join(f'<tr><td><strong>{T(us, uk)}</strong></td><td><code>{T(a, ua)}</code></td><td><span class="muted">{e(uk if k not in ("ch", "sl") else us)}</span></td><td>{e(tc)}</td><td>{e(BS_H[k])}</td><td>{e(BS_USE[k])}</td></tr>' for k, us, uk, a, ua, tc, st in BS)
def bs_sec(k, us, uk, a, ua, tc, st):
    last = st[-1]
    tch = "" if tc in ("—", "none") else f' Turning chain: <strong>ch {tc}</strong>.'
    return (f'<h2 id="st-{k}">How to {T(us, uk)} ({T(a, ua)})</h2><figure class="co-fig">{bs_svg(k, last, len(st) - 1)}<figcaption class="note">Our drawing: the {e(us)} row in berry on the row below.</figcaption></figure>'
            f'<ol>' + "".join(f"<li><strong>{e(s[0])}.</strong> {e(s[1])}</li>" for s in st) + f'</ol><p class="sub">{e(BS_USE[k])}.{tch}</p>')
bs_secs = "".join(bs_sec(*b) for b in BS)
BS_ANAT = f'''<svg viewBox="0 0 300 130" role="img" aria-label="Top of a crochet stitch: front loop, back loop and the post"><rect width="300" height="130" fill="#fff"/>
<rect x="120" y="44" width="60" height="70" rx="10" fill="#fbfcfa" stroke="{_Y}" stroke-width="4"/><ellipse cx="150" cy="40" rx="44" ry="14" fill="none" stroke="{_Y}" stroke-width="5"/>
<path d="M106 46 q44 18 88 0" fill="none" stroke="{_MG}" stroke-width="5"/>
<text x="16" y="62" font-size="12" fill="#1f2a44" font-weight="700">front loop</text><path d="M84 58 l24 -6" stroke="#1f2a44" stroke-width="1.6"/>
<text x="210" y="22" font-size="12" fill="#1f2a44" font-weight="700">back loop</text><path d="M208 20 l-20 10" stroke="#1f2a44" stroke-width="1.6"/>
<text x="200" y="96" font-size="12" fill="#1f2a44" font-weight="700">post</text><path d="M198 92 l-16 -4" stroke="#1f2a44" stroke-width="1.6"/></svg>'''
bsp = top("Basic crochet stitches for beginners", "The six stitches nearly every crochet pattern is built from: chain, slip stitch, single, half double, double and treble crochet. Step through each one in our drawings, and switch between US and UK names with one tap.", "Basic crochet stitches") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> the basic crochet stitches, shortest to tallest, are the <strong>{T("chain (ch)", "chain (ch)")}</strong>, <strong>{T("slip stitch (sl st)", "slip stitch (ss)")}</strong>, <strong>{T("single crochet (sc)", "double crochet (dc)")}</strong>, <strong>{T("half double crochet (hdc)", "half treble (htr)")}</strong>, <strong>{T("double crochet (dc)", "treble (tr)")}</strong> and <strong>{T("treble crochet (tr)", "double treble (dtr)")}</strong>. Each taller stitch starts with one more yarn over, and needs one more turning chain: 1 for {T("sc", "dc")}, 2 for {T("hdc", "htr")}, 3 for {T("dc", "tr")} and 4 for {T("tr", "dtr")}. Learn the chain and {T("single crochet", "double crochet")} first; the rest are the same moves with extra yarn overs.</div>
<div class="bs-terms"><span>Stitch names:</span><div class="seg" id="bs-terms" role="group" aria-label="US or UK crochet terms"><button type="button" data-v="us" aria-pressed="true">US terms</button><button type="button" data-v="uk" aria-pressed="false">UK terms</button></div></div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<h2 style="margin-top:0">Step through a stitch</h2>
<div class="field"><label>Pick a stitch</label><div class="seg" id="bs-st" role="group" aria-label="Stitch">{bs_tabs}</div></div>
<p class="note" style="margin:6px 0 0">Use the buttons or the arrow keys. The counter shows the loops on your hook after each step: if yours differs, go back a step.</p>
<div class="btns" style="margin-top:12px"><button type="button" class="btn ghost" id="bs-prev">Back</button><button type="button" class="btn" id="bs-next">Next step</button></div>

</div>
<div class="result" aria-live="polite"><figure class="co-fig" style="margin:0 0 10px"><svg id="bs-svg" viewBox="0 0 260 170" role="img" aria-label="Step drawing"></svg></figure><div id="bs-out"></div></div>
</div></section>
<script>window.PP_BS = {json.dumps(BS_JS)};</script>
<section style="padding-top:0"><div class="wrap"><h2>Crochet stitch chart: US, UK, turning chains and height</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Stitch</th><th scope="col">Abbreviation</th><th scope="col">Called in UK patterns</th><th scope="col">Turning chain</th><th scope="col">Height (sc = 1)</th><th scope="col">Good for</th></tr></thead><tbody>{bs_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Turning chains are the usual numbers (Craft Yarn Council, Lion Brand and most patterns); some designers use one fewer, so follow your pattern. Heights are rough guides from our own swatches; they change with your yarn and hook. The third column is always the UK name, whichever terms you've picked above.</p></div></section>
{AD.format("bs-mid")}
<section style="padding-top:0"><div class="narrow prose">
<h2>Where do I put the hook? Front loop, back loop and post</h2>
<figure class="co-fig">{BS_ANAT}<figcaption class="note">Our drawing of the top of a stitch.</figcaption></figure>
<p>The top of every stitch looks like a sideways V, or a chain lying on its side. Unless the pattern says otherwise, put the hook <strong>under both loops</strong> of the V. Going into only the <strong>back loop</strong> (BLO) leaves a ridge that makes stretchy ribbing; the <strong>front loop</strong> (FLO) leaves a ridge on the other side. Working around the <strong>post</strong>, the upright body of the stitch, makes raised textures like front and back post double crochet.</p>
{bs_secs}
<h2>Does the turning chain count as a stitch?</h2>
<p>For {T("single crochet", "double crochet (UK)")}, no: chain 1, turn, and work into the first stitch. For taller stitches it depends on the pattern. Many count the chain 3 of a {T("double crochet", "treble")} row as the first stitch, so you skip the first stitch and work the last stitch into the top of the turning chain. Others say "chain 2 (does not count)". Check the note at the start of the pattern, and count your stitches at the end of the first few rows.</p>
<h2>Why is my crochet getting wider or narrower?</h2>
<p>Almost always a stitch gained or lost at the edges. A stitch added in the first stitch (when the turning chain also counts) or one missed at the end (the top of the turning chain is easy to miss) changes the count each row. Put a stitch marker in the first and last stitch of every row, count after each row for a while, and use a <a href="{href("row-counter.html")}">row counter</a> to keep your place.</p>
<h2>Why are US and UK crochet terms different?</h2>
<p>They count differently. US names count the pull-throughs that finish the stitch after you pull up a loop; UK names count the loops on the hook right after you pull up that first loop. So the same stitch is a US single crochet and a UK double crochet. A pattern with "sc" anywhere in it is US: there is no sc in UK terms. Our <a href="{href("crochet-terms.html")}">US vs UK crochet terms chart</a> has the full list.</p>
<div class="callout"><strong>Ready for a first project?</strong> A dishcloth or a scarf in {T("single or half double crochet", "double crochet or half treble")} is the classic start. Work out the starting chain with the <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a> and the yarn with the <a href="{href("yarn-calculator.html")}">yarn calculator</a>.</div>
<p>What next? Start a round with the <a href="{href("how-to-crochet-magic-ring.html")}">magic ring</a>, shape with <a href="{href("how-to-crochet-decrease.html")}">crochet decreases</a>, and finish neatly with <a href="{href("how-to-weave-in-ends.html")}">how to weave in ends</a>. Picking a hook? See the <a href="{href("hook-needle-sizes.html")}">hook size chart</a>.</p></div></section>'''
bs_faq = [
    ("What are the basic crochet stitches?", "Chain (ch), slip stitch (sl st), single crochet (sc), half double crochet (hdc), double crochet (dc) and treble crochet (tr), in US terms. Almost every other stitch is a mix of these."),
    ("What is the easiest crochet stitch for beginners?", "The chain, then single crochet. Single crochet is just insert, pull up a loop, and pull through two, so it's the best first stitch for practising even tension."),
    ("How many chains do you need to turn for each crochet stitch?", "Usually 1 for single crochet, 2 for half double, 3 for double and 4 for treble crochet (US terms). Some patterns use one fewer, so check yours."),
    ("Is UK double crochet the same as US single crochet?", "Yes. UK double crochet (dc) is US single crochet (sc), UK treble (tr) is US double crochet (dc), and UK half treble (htr) is US half double crochet (hdc)."),
    ("How many loops should be on my hook?", "After a finished stitch, 1. Mid-stitch: 2 for single crochet, 3 for half double and double crochet, 4 for treble crochet, right after you pull up the loop through the stitch."),
    ("How tall is a double crochet compared to a single crochet?", "About twice as tall. A half double is about one and a half times, and a treble about two and a half to three times, depending on your yarn and tension."),
]
page("basic-crochet-stitches.html", "Basic Crochet Stitches for Beginners: Step by Step (US & UK) | Purl & Paper",
     "Learn the 6 basic crochet stitches step by step: chain, slip stitch, single, half double, double and treble crochet, with our own drawings, a loops-on-hook stepper, US/UK names and a stitch height and turning chain chart.",
     bsp, bs_faq, "Basic crochet stitches", app_name="Crochet stitch stepper")


# ---------------- SWEATER SIZE CALCULATOR (ease + which size to make + yarn estimate) ----------------
# Ease ranges: Craft Yarn Council "Bust/Chest Fit and Ease Chart" (craftyarncouncil.com/standards/body-sizing). Midpoints are ours.
SW_FIT = [("vclose", "Very close fitting (negative ease)", -4, -2), ("close", "Close fitting (zero ease)", 0, 0), ("classic", "Classic fit", 2, 4),
          ("loose", "Loose fit", 4, 6), ("over", "Oversized", 6, 10)]
SW_K = 0.667 * 1.25   # yd per sq in of worsted stockinette (our blanket/scarf area model) + 25% for shaping, seams and swatching: our estimate, checked against typical 1,000-1,500 yd adult worsted pullovers; crochet × 1.27
SW_SL = {"long": 18, "three": 11, "short": 4, "none": 0}   # underarm to cuff, adult defaults (our estimates; measure your own)
def sw_area(chest, length, sleeve, arm=None):
    arm = arm or max(10, chest * 0.33)   # finished upper arm about a third of the finished chest: our estimate
    cuff = 8 if sleeve > 6 else arm
    return chest * length + 2 * sleeve * (arm + cuff) / 2 + chest * 1.5   # + neckband, cuffs and hem bands
def sw_yd(chest, length, sleeve, wn, craft=1.0): return sw_area(chest, length, sleeve) * SW_K * BK_M[wn] * craft
def sw_rng(y): return f"{round(y * 0.88, -2):,.0f}–{round(y * 1.12, -2):,.0f}"
# Example chests for the yarn table: finished = body + classic ease. Lengths: our estimates for a hip-length pullover.
SW_EX = [("Child, about age 6 (25 in chest)", 28, 16, 12), ("Child, about age 10 (28 in chest)", 31, 18, 14.5), ("Adult, 34 in chest", 37, 23, 17.5),
         ("Adult, 38 in chest", 41, 24, 18), ("Adult, 42 in chest", 45, 25, 18.5), ("Adult, 46 in chest", 49, 26, 19), ("Adult, 50 in chest", 53, 27, 19.5)]
SW_TW = [(3, "DK"), (4, "Worsted"), (5, "Bulky")]
sw_yrows = "".join(f'<tr><th scope="row">{e(n)}<br><span class="muted">{c:g} in finished, {l:g} in long</span></th>' + "".join(f"<td>{sw_rng(sw_yd(c, l, s, wn))}</td>" for wn, _ in SW_TW) + f"<td>{sw_rng(sw_yd(c, l, s, 4, 1.27))}</td></tr>" for n, c, l, s in SW_EX)
def sw_ez(a, b, k=1, u="in"):
    f = lambda x: ("+" if x > 0 else ("−" if x < 0 else "")) + f"{abs(round(x * k)):g}"
    if a == b: return f"0 {u} (same as your body)"
    if a >= 6: return f"{f(a)} {u} or more"
    return f"{f(a)} to {f(b)} {u}"
sw_frows = "".join(f'<tr><td><strong>{e(n)}</strong></td><td>{sw_ez(a, b)}</td><td>{sw_ez(a, b, 2.54, "cm")}</td></tr>' for k, n, a, b in SW_FIT)
sw_fopts = "".join(f'<option value="{k}"{" selected" if k == "classic" else ""}>{e(n)}: {sw_ez(a, b)}</option>' for k, n, a, b in SW_FIT)
sw_wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"].split(",")[0])})</option>' for w in D["weights"] if 1 <= w["n"] <= 6)
_sw38 = sw_yd(41, 24, 18, 4); _sw38c = sw_yd(41, 24, 18, 4, 1.27); _sw42b = sw_yd(45, 25, 18.5, 5)
SW_SVG = f'''<svg viewBox="0 0 300 150" role="img" aria-label="Where to measure: around the fullest part of the chest, length from shoulder to hem, sleeve from underarm to cuff"><rect width="300" height="150" fill="#fff"/>
<path d="M110 20 l-40 18 l-40 70 l18 8 l32 -52 v76 h120 v-76 l32 52 l18 -8 l-40 -70 l-40 -18 q-20 14 -40 0 z" fill="#fbfcfa" stroke="{_Y}" stroke-width="4" stroke-linejoin="round"/>
<path d="M80 62 h140" stroke="{_TL}" stroke-width="3" stroke-dasharray="6 4"/><text x="150" y="56" font-size="11" fill="#1f2a44" font-weight="700" text-anchor="middle">chest, all the way round</text>
<path d="M240 20 v120" stroke="{_MG}" stroke-width="3"/><text x="246" y="84" font-size="11" fill="#1f2a44" font-weight="700">length</text>
<path d="M216 62 l40 52" stroke="{_HK}" stroke-width="3"/><text x="198" y="132" font-size="11" fill="#1f2a44" font-weight="700" text-anchor="end">sleeve: underarm to cuff</text></svg>'''
swp = top("Sweater size calculator", "Which size sweater should you knit or crochet? Enter your chest or bust measurement and the fit you like, and get the finished size to choose, the ease you'd get in each pattern size, and an estimate of how much yarn to buy.", "Sweater size calculator") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="quick"><strong>Quick answer:</strong> measure around the fullest part of your chest or bust, then <strong>add the ease</strong> for the fit you want and pick the pattern size whose <strong>finished</strong> chest is closest. The Craft Yarn Council's guide: very close fitting is about 2 to 4 in (5 to 10 cm) <em>less</em> than your body, close fitting is the same, classic fit is 2 to 4 in more, loose fit 4 to 6 in more, and oversized 6 in (15 cm) or more. A 38 in chest in a classic fit wants a sweater of about 40 to 42 in. Yarn: an adult worsted pullover takes roughly {sw_rng(_sw38)} yd knitted, more if crocheted.</div></div></section>
<section style="padding-top:0"><div class="wrap tool">
<div class="sheet">
<div class="field"><label>Knitting or crochet?</label><div class="seg" id="sw-craft" role="group" aria-label="Knit or crochet"><button type="button" data-v="knit" aria-pressed="true">Knitting</button><button type="button" data-v="crochet" aria-pressed="false">Crochet</button></div></div>
<div class="row2"><div class="field"><label for="sw-chest">Your chest or bust (body)</label><input type="number" id="sw-chest" value="38" min="14" max="80" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="sw-u">Units</label><select id="sw-u"><option value="in">inches</option><option value="cm">cm</option></select></div></div>
<div class="field"><label for="sw-fit">Fit you want</label><select id="sw-fit">{sw_fopts}</select></div>
<div class="field"><label for="sw-sizes">Finished chest sizes in your pattern (optional)</label><input type="text" id="sw-sizes" value="" placeholder="for example 34, 38, 42, 46, 50" inputmode="decimal"><p class="note" style="margin:6px 0 0">Copy the "finished measurements" or "actual chest" numbers, not the "to fit" ones.</p></div>
<div class="row2"><div class="field"><label for="sw-len">Body length, shoulder to hem</label><input type="number" id="sw-len" value="24" min="6" max="45" step="0.5" inputmode="decimal"></div>
<div class="field"><label for="sw-sl">Sleeves</label><select id="sw-sl"><option value="long">Long</option><option value="three">Three-quarter</option><option value="short">Short</option><option value="none">Sleeveless (vest)</option></select></div></div>
<div class="field"><label for="sw-sll">Sleeve length, underarm to cuff</label><input type="number" id="sw-sll" value="18" min="0" max="30" step="0.5" inputmode="decimal"></div>
<div class="row2"><div class="field"><label for="sw-yarn">Yarn weight</label><select id="sw-yarn">{sw_wopts}</select></div>
<div class="field"><label for="sw-tex">Stitch pattern</label><select id="sw-tex"><option value="1">Plain: stockinette, sc, hdc or dc</option><option value="1.15">Garter, seed or moss</option><option value="1.25">Ribbing or textured stitches</option><option value="1.4">Cables or brioche</option></select></div></div>
<div class="field"><label for="sw-sk">Yards per skein</label><input type="number" id="sw-sk" value="200" min="10" max="2000" step="1" inputmode="numeric"></div>
</div>
<div class="result" aria-live="polite" id="sw-out"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><h2>How much ease should a sweater have?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Fit</th><th scope="col">Ease at the chest</th><th scope="col">In cm</th></tr></thead><tbody>{sw_frows}</tbody></table></div>
<p class="note" style="margin-top:12px">From the Craft Yarn Council's bust/chest fit and ease chart: a negative number means the sweater is smaller than you and stretches to fit.</p>
<h2>How much yarn for a sweater? Yarn chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size (classic fit, long sleeves)</th><th scope="col">Knit, DK</th><th scope="col">Knit, worsted</th><th scope="col">Knit, bulky</th><th scope="col">Crochet, worsted</th></tr></thead><tbody>{sw_yrows}</tbody></table></div>
<p class="note" style="margin-top:12px">Yards, our estimates for a plain hip-length pullover: fabric area (body, sleeves and bands) × the same yards per square inch as our blanket and scarf calculators, plus 25% for shaping, seams and a swatch, ±12%. Lengths and sleeve lengths are our typical figures, so measure yourself or a sweater you like. Cables, texture and crochet use more. Your pattern's yardage always wins: buy that, plus a skein.</p></div></section>
{AD.format("sw-mid")}
<section style="padding-top:0"><div class="narrow prose">
<h2>How do I measure myself for a sweater?</h2>
<figure class="co-fig">{SW_SVG}<figcaption class="note">Our drawing of the three measurements the calculator uses.</figcaption></figure>
<ul><li><strong>Chest or bust:</strong> around the fullest part, under the arms, with the tape level and snug but not tight. Wear what you'd wear under the sweater.</li>
<li><strong>Length:</strong> from the top of the shoulder, next to the neck, down to where you want the hem. Hip length is typical; cropped is shorter.</li>
<li><strong>Sleeve:</strong> from the underarm to the wrist with your arm relaxed.</li></ul>
<p>Easier still: lay a sweater that fits the way you like flat, measure across the chest just under the arms and double it. That's the finished chest to look for in a pattern, ease already included.</p>
<h2>What is ease in knitting and crochet?</h2>
<p>Ease is the difference between your body and the finished garment. A 38 in chest in a 42 in sweater has 4 in of positive ease, so it hangs a little loose. Negative ease, a sweater smaller than you, works only for stretchy fabric like ribbing and fitted tops. Hats and socks are usually made with negative ease too so they stay put; our <a href="{href("hat-size-chart.html")}">hat size chart</a> and <a href="{href("sock-size-chart.html")}">sock size chart</a> build it in.</p>
<h2>Which size should I make if I'm between sizes?</h2>
<p>Go by the fit the designer shows. Most patterns say how much ease the sample has ("shown with 4 in of positive ease"): add that to your chest and pick the nearest finished size. If you're between two, the larger one is usually the safer choice for a pullover, and the smaller one for a cardigan you'll wear open or a fitted top. Check the length and sleeves too: those are easy to change while you knit, the chest isn't.</p>
<h2>Why does crochet take more yarn than knitting?</h2>
<p>Crochet stitches are thicker and denser, so the same area uses more yarn, roughly a quarter more by our estimate. A crocheted sweater can also feel heavier, so choose a lighter yarn or an open stitch for drape. Whichever you make, a gauge swatch tells you whether your size will come out right: compare it with the pattern in the <a href="{href("gauge-converter.html")}">gauge converter</a>.</p>
<h2>How many skeins do I need for a sweater?</h2>
<p>Divide the yards by the yards on one skein and round up, then buy one more of the same dye lot. Running short on a sweater is painful because the last skein often shows as a stripe if the dye lot changes. Swapping to a different yarn than the pattern uses? The <a href="{href("yarn-substitution-calculator.html")}">yarn substitution calculator</a> turns the pattern's balls into yours.</p>
<div class="callout"><strong>Making it as a gift?</strong> A sweater is a big project: the <a href="{href("crochet-time-estimator.html")}">time calculator</a> says how many evenings it will take, and the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a> checks it fits before Christmas.</div>
<p>What next? Plan the starting stitches with the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> or the <a href="{href("foundation-chain-calculator.html")}">foundation chain calculator</a>, and keep the yarn and size details in the <a href="{href("projects.html")}">project tracker</a>.</p></div></section>'''
sw_faq = [
    ("What size sweater should I knit?", "Add the ease you want to your chest measurement and pick the pattern size whose finished chest is closest. For a classic fit that's about 2 to 4 in more than your chest, so a 38 in chest makes a 40 to 42 in sweater."),
    ("How much ease should a sweater have?", "The Craft Yarn Council's guide: very close fitting 2 to 4 in less than your body, close fitting 0, classic fit 2 to 4 in more, loose fit 4 to 6 in more, oversized 6 in or more."),
    ("How much yarn do I need to knit a sweater?", f"By our estimate an adult 38 in chest pullover with classic ease and long sleeves takes about {sw_rng(_sw38)} yd of worsted, or about {sw_rng(_sw42b)} yd of bulky for a 42 in chest. Always check your pattern."),
    ("How much yarn do I need to crochet a sweater?", f"About a quarter more than knitting: roughly {sw_rng(_sw38c)} yd of worsted for an adult 38 in chest pullover with long sleeves, by our estimate."),
    ("What does finished chest mean in a pattern?", "The measurement around the sweater itself, ease included. Compare it with your body measurement plus the ease you want, not with your body alone."),
    ("Should I size up or down between sweater sizes?", "Usually up for a pullover, and down for a fitted top or an open cardigan. Look at how much ease the pattern sample is shown with and match that."),
]
page("sweater-size-calculator.html", "What Size Sweater Should I Knit or Crochet? Ease & Yarn Calculator | Purl & Paper",
     "Free sweater size calculator for knitting and crochet: add the right ease for your fit (Craft Yarn Council chart), find which pattern size to make, and estimate the yarn and skeins for a pullover in DK, worsted or bulky.",
     swp, sw_faq, "Sweater size calculator", app_name="Sweater size and yarn calculator")

exec((ROOT / "crafts.py").read_text())

# ---------------- SITEMAP / ROBOTS ----------------
page("thanks.html", "Check your inbox | Purl & Paper", "Confirm your email to get your free printables.", NL_THANKS)
page("welcome.html", "Your free printables | Purl & Paper", "Download your free printable sampler.", NL_WELCOME)

LASTMOD = {"basic-crochet-stitches.html": "2026-11-26", "sweater-size-calculator.html": "2026-11-26", "crochet-time-estimator.html": "2026-11-25", "stripe-generator.html": "2026-11-25", "c2c-blanket-calculator.html": "2026-11-25", "scarf-size-chart.html": "2026-11-25", "how-to-pick-up-stitches-knitting.html": "2026-11-25", "how-to-price-amigurumi.html": "2026-11-25", "how-to-knit-in-the-round.html": "2026-11-25", "junk-journal-supply-checklist.html": "2026-11-25", "crochet-knitting-gift-planner.html": "2026-11-25", "etsy-fee-calculator.html": "2026-11-25", "hook-needle-sizes.html": "2026-11-25", "how-to-fix-a-dropped-stitch.html": "2026-11-24", "how-to-price-a-crochet-blanket.html": "2026-11-24", "how-to-price-crochet-items.html": "2026-11-25", "blanket-size-calculator.html": "2026-11-24", "knitting-abbreviations.html": "2026-11-24", "how-to-cast-on-knitting.html": "2026-11-25", "how-to-crochet-decrease.html": "2026-11-24", "increase-decrease-calculator.html": "2026-11-24", "cast-on-calculator.html": "2026-11-24", "how-to-bind-off-knitting.html": "2026-11-24", "how-to-weave-in-ends.html": "2026-11-24", "how-to-crochet-magic-ring.html": "2026-11-24", "how-to-change-colors-in-crochet.html": "2026-11-24", "foundation-chain-calculator.html": "2026-11-23", "junk-journal-signature-calculator.html": "2026-11-23", "hat-size-chart.html": "2026-11-25", "junk-journal-beginners.html": "2026-11-25", "yarn-yardage-calculator.html": "2026-11-23", "craft-fair-checklist.html": "2026-11-23", "granny-square-blanket-calculator.html": "2026-11-23", "temperature-blanket-planner.html": "2026-11-23", "junk-journal-ephemera-ideas.html": "2026-11-25", "crochet-circle-calculator.html": "2026-11-22", "yarn-calculator.html": "2026-11-22", "journal-prompts.html": "2026-11-22", "yarn-substitution-calculator.html": "2026-11-23", "how-to-tea-stain-paper.html": "2026-11-22", "yarn-weights.html": "2026-11-24", "sock-size-chart.html": "2026-11-22", "hook-needle-sizes.html": "2026-11-22", "row-counter.html": "2026-11-25", "crochet-terms.html": "2026-11-23", "gauge-converter.html": "2026-11-24", "projects.html": "2026-11-20", "index.html": "2026-11-23"}
pages = list(dict.fromkeys(["index.html"] + [f for f, _ in NAV + TOOLS_MORE] + [f for f, _ in GUIDES] + [f for f, _, _ in CRAFTS] + ["about.html", "privacy.html"]))
for _f, _, _ in CRAFTS: LASTMOD.setdefault(_f, "2026-11-25")
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{canon(p)}</loc><lastmod>{LASTMOD.get(p, '2026-11-19')}</lastmod></url>\n" for p in pages) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
(ROOT / "ads.txt").write_text("google.com, pub-1558743317014653, DIRECT, f08c47fec0942fa0\n")
print("built", len(pages) + 1, "pages", "(preview)" if PREVIEW else "")
write_redirects(ROOT)
# Keep the Direct Upload zip under the 3.8 MB browser upload limit: OG images at 960x504, JPEG q50.
from PIL import Image as _Im
for _f in (ROOT / "assets" / "og").glob("*.jpg"):
    _i = _Im.open(_f)
    if _i.width > 960: _i.convert("RGB").resize((960, 504), _Im.LANCZOS).save(_f, quality=50, optimize=True, progressive=True)
