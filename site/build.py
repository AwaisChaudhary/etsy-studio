#!/usr/bin/env python3
"""Builds the crafts site. `python3 build.py` = live (clean URLs). `python3 build.py --preview` = local files.
Change SITE / DOMAIN / GA_ID here once the domain is bought. Content data lives in assets/data.json."""
import json, html, pathlib, sys, hashlib

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
TOOLS_MORE = [("blanket-size-calculator.html", "Blanket size calculator"), ("crochet-knitting-gift-planner.html", "Handmade gift planner"), ("hat-size-chart.html", "Hat size calculator"), ("granny-square-blanket-calculator.html", "Granny square calculator"), ("increase-decrease-calculator.html", "Increase evenly calculator"), ("sock-size-chart.html", "Sock size calculator"), ("yarn-substitution-calculator.html", "Yarn substitution calculator"), ("cast-on-calculator.html", "Cast on calculator"), ("crochet-circle-calculator.html", "Crochet circle calculator")]
GUIDES = [("yarn-weights.html", "Yarn weight chart"), ("hook-needle-sizes.html", "Hook and needle sizes"),
          ("crochet-terms.html", "US vs UK crochet terms"), ("junk-journal-beginners.html", "Junk journaling for beginners"), ("how-to-price-crochet-items.html", "How to price crochet items"), ("how-to-tea-stain-paper.html", "How to tea stain paper"), ("knitting-abbreviations.html", "Knitting abbreviations"), ("junk-journal-ephemera-ideas.html", "Junk journal ephemera ideas")]
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
}
KNIT = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator"]
JJ = ["december-days-journal-kit", "junk-journal-mega-bundle", "tea-room-junk-journal-kit", "night-garden-junk-journal-kit"]
SHOP_FOR = {"index.html": ["junk-journal-mega-bundle", "2027-crochet-knitting-planner", "night-garden-junk-journal-kit", "yarn-stash-tracker"],
            "row-counter.html": KNIT, "yarn-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator"],
            "gauge-converter.html": KNIT, "projects.html": KNIT, "yarn-weights.html": KNIT, "hook-needle-sizes.html": KNIT, "crochet-terms.html": KNIT,
            "journal-prompts.html": ["december-days-journal-kit", "journaling-cards-3x4", "vintage-ephemera-pack", "junk-journal-mega-bundle"], "junk-journal-beginners.html": JJ,
            "blanket-size-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator"],
            "hat-size-chart.html": ["2027-crochet-knitting-planner", "christmas-gift-tags", "yarn-stash-tracker", "crochet-knitting-pricing-calculator"],
            "granny-square-blanket-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "increase-decrease-calculator.html": KNIT,
            "sock-size-chart.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "christmas-gift-tags", "crochet-knitting-pricing-calculator"],
            "how-to-price-crochet-items.html": ["crochet-knitting-pricing-calculator", "yarn-stash-tracker", "2027-crochet-knitting-planner", "christmas-gift-tags"],
            "yarn-substitution-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "crochet-circle-calculator.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "cast-on-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "how-to-tea-stain-paper.html": ["tea-room-junk-journal-kit", "vintage-ephemera-pack", "junk-journal-mega-bundle", "december-days-journal-kit"],
            "knitting-abbreviations.html": ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
            "junk-journal-ephemera-ideas.html": ["vintage-ephemera-pack", "journaling-cards-3x4", "junk-journal-mega-bundle", "tea-room-junk-journal-kit"],
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
<meta name="twitter:card" content="summary"><meta name="theme-color" content="#1f2a44">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='15' cy='17' r='12' fill='%23b8326a'/%3E%3Crect x='19' y='2' width='11' height='8' rx='2' fill='%23f4a823'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&display=swap" rel="stylesheet">
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
{shop_box(file)}
<footer><div class="wrap"><div class="fgrid">
<div><a class="brand" href="{href("index.html")}">{LOGO}<span>Purl <i>&amp;</i> Paper</span></a><p style="margin-top:12px" class="muted">Free tools for knitters, crocheters and junk journalers. Count your rows, plan your yarn, and never run out of ideas for the next page.</p></div>
<div><strong>Tools</strong><ul>{"".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in NAV + TOOLS_MORE)}</ul></div>
<div><strong>Shop</strong><ul><li><a href="{ETSY}" rel="noopener">Purl &amp; Paper on Etsy</a></li><li><a href="{GUM}" rel="noopener">Purl &amp; Paper on Gumroad</a></li><li><a href="https://www.pinterest.com/purlandpaperco/" rel="noopener">Pinterest</a></li></ul></div>
<div><strong>Guides</strong><ul>{"".join(f'<li><a href="{href(f)}">{n}</a></li>' for f, n in GUIDES)}<li><a href="{href("about.html")}">About and contact</a></li><li><a href="{href("privacy.html")}">Privacy policy</a></li></ul></div>
</div>
<p class="legal">{e(SITE)} is an independent site. Your counters, projects and saved prompts stay on your own device; nothing is uploaded. Yarn amounts are estimates, so always check your pattern. Last checked {e(UPDATED)}.</p>
</div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>window.PP={json.dumps({k: D[k] for k in ("prompts", "projects", "weights", "blankets", "gifts", "hats", "socks")}, ensure_ascii=False)};</script>
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
</div><p class="guides-more">New on the work table: a <a href="{href("knitting-abbreviations.html")}">knitting abbreviations list with a pattern decoder</a> (paste a line, get plain English), 62 <a href="{href("junk-journal-ephemera-ideas.html")}">junk journal ephemera ideas</a> with a checklist, the <a href="{href("crochet-circle-calculator.html")}">crochet circle calculator</a> (stitches per round and an amigurumi ball pattern), the <a href="{href("cast-on-calculator.html")}">cast on calculator</a> (how many stitches for a scarf, blanket or cowl), seasonal <a href="{href("journal-prompts.html")}">winter and Christmas journal prompts</a>, the <a href="{href("yarn-substitution-calculator.html")}">yarn substitution calculator</a> (how many balls of a different yarn), a guide to <a href="{href("how-to-tea-stain-paper.html")}">tea staining paper</a> for junk journals with a shade tester, the <a href="{href("sock-size-chart.html")}">sock size chart and cast-on calculator</a> (heel, gusset and toe numbers for your gauge), the <a href="{href("increase-decrease-calculator.html")}">increase and decrease evenly calculator</a> (it writes the row out for you), a guide to <a href="{href("how-to-price-crochet-items.html")}">pricing crochet items to sell</a> with a fee calculator, the <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> (how many squares and how much yarn), the <a href="{href("hat-size-chart.html")}">hat size chart and cast-on calculator</a> (preemie to adult, knit or crochet), the <a href="{href("crochet-knitting-gift-planner.html")}">handmade Christmas gift planner</a> (will your knitted and crocheted gifts be ready in time?) and the <a href="{href("blanket-size-calculator.html")}">blanket size chart and yarn calculator</a>, from lovey to king size.</p></div></section>'''
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
<p>Divide the yards you need by the yards on one skein and round up, then add one if you can. Running short is worse than having a spare: a new skein from a different dye lot can show as a stripe. Many shops take back unused skeins, so ask before you buy. Keep track of what's left over in a stash list, and the <a href="{href("projects.html")}">project tracker</a> can hold the yarn details for each piece.</p></div></section>'''
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
gc = top("Gauge converter", "Your swatch came out different from the pattern? See how big your piece will turn out, and how many stitches and rows to use instead.", "Gauge converter") + '''
<section style="padding-top:10px"><div class="wrap tool">
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
<section style="padding-top:0"><div class="narrow prose"><h2>Should you change needles or the numbers?</h2>
<p>If you have <strong>more</strong> stitches than the pattern, your fabric is tighter: go up a needle or hook size. If you have <strong>fewer</strong>, it's looser: go down a size. Changing tool size is usually the best first fix, because it keeps the fabric feel the designer intended.</p>
<p>If you love your fabric as it is, use the new stitch and row numbers above instead. Round to suit your stitch pattern: if it repeats over 4 stitches, pick the nearest multiple of 4.</p>
<div class="callout">Measure your swatch after washing and drying it the way you'll treat the finished piece. Many yarns grow or shrink a little.</div>
<h2>How to measure a swatch</h2>
<ol><li>Make a swatch at least 6 inches (15 cm) wide in the stitch the pattern uses for its gauge, with the same needles or hook.</li>
<li>Wash and dry it, then lay it flat without stretching.</li>
<li>Count the stitches across 4 inches (10 cm) in the middle, away from the edges. Count half stitches too.</li>
<li>Do the same for rows, measuring up and down.</li></ol>
<p>For hats, socks and anything else worked in the round, knit the swatch in the round too if you can. Many knitters purl a little looser than they knit, so a flat swatch can give a slightly different number.</p>
<h2>Gauge for a hat or a sweater</h2>
<p>Small differences add up on fitted pieces. On a 20 inch hat, being half a stitch per inch off changes the size by about 2 inches. Got your stitches per inch? The <a href="@@HAT@@">hat size calculator</a> turns them into a cast-on count for any head size, and the <a href="@@YW@@">yarn weight chart</a> shows the usual gauge for each yarn.</p></div></section>'''
gc = gc.replace("@@HAT@@", href("hat-size-chart.html")).replace("@@YW@@", href("yarn-weights.html"))
gc_faq = [
    ("How do I measure gauge in crochet?", "Crochet a swatch at least 6 inches wide in the pattern's stitch, block it, then count the stitches and rows over 4 inches (10 cm) in the middle. Include half stitches."),
    ("What is gauge in knitting and crochet?", "Gauge (called tension in the UK) is how many stitches and rows fit in a set width, usually 4 inches or 10 cm. Matching it is what makes a garment come out the size the pattern says."),
    ("Does gauge matter for scarves and blankets?", "Less. A scarf a little wider is usually fine, but it changes how much yarn you need. For fitted garments, hats and socks it matters a lot."),
    ("Why is my gauge different from the pattern?", "Everyone holds yarn with a different tension, and needle materials and yarn brands vary. That's normal, which is why patterns ask you to swatch."),
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
rows = "".join(f'<tr id="w{w["n"]}"><td><span class="wnum">{w["n"]}</span></td><td><strong>{e(w["name"])}</strong><br><span class="muted">{e(w["also"])}</span></td><td>{e(w["uk"])}</td><td>{e(w["knit"])} sts</td><td>{e(w["needle"])}</td><td>{e(w["croc"])}</td><td>{e(w["hook"])}</td><td>{e(w["use"])}</td></tr>' for w in D["weights"])
thick = "".join(f'<figure><i style="height:{14 + w["n"] * 6}px"></i>{w["n"]}</figure>' for w in D["weights"])
yw = top("Yarn weight chart", "Yarn is grouped from 0 (thinnest) to 7 (thickest). Find the number on your label, or the name in your pattern, to see the needle and hook size to start with.", "Yarn weight chart") + f'''
<section style="padding-top:10px"><div class="wrap">
<div class="thick" aria-hidden="true">{thick}</div><p class="note">Strand thickness, drawn to show the steps. Not to scale.</p>
<div class="tbl-wrap"><table><thead><tr><th scope="col">#</th><th scope="col">Weight</th><th scope="col">UK / AU name</th><th scope="col">Knit gauge (4 in / 10 cm)</th><th scope="col">Needles</th><th scope="col">Crochet gauge (4 in / 10 cm)</th><th scope="col">Hook</th><th scope="col">Good for</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Based on the Craft Yarn Council's Standard Yarn Weight System. These are starting points: lace patterns often use bigger needles than the chart suggests, and your own tension changes things too.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How to tell a yarn's weight without a label</h2>
<p>Wrap the yarn snugly (not stretched) around a ruler or pencil for one inch, strands touching but not overlapping, and count the wraps. That's the <strong>wraps per inch</strong>. Roughly: 18 or more is fingering or thinner, 12 to 14 is DK, 9 to 11 is worsted or aran, 7 to 8 is bulky, and 6 or fewer is super bulky.</p>
<p>Planning a blanket? The <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a> turns your yarn weight and blanket size into yards and skeins.</p>
<h2>Swapping one yarn for another</h2>
<p>Stay in the same weight number, then knit or crochet a swatch. Two yarns in the same category can still differ, so check the length per 100 g on both labels: if they're close, the swap usually works. The <a href="{href("yarn-substitution-calculator.html")}">yarn substitution calculator</a> does the maths and tells you how many balls to buy, including when you hold two strands together.</p></div></section>'''
yw_faq = [
    ("Is DK the same as worsted?", "No. DK is weight 3 (light) and worsted is weight 4 (medium), so worsted is a bit thicker. In the UK, aran is close to worsted."),
    ("What weight is 4 ply yarn?", "In the UK and Australia, 4 ply is about the same as US fingering, weight 1 (super fine)."),
    ("What does 'weight' mean if it's not grams?", "Yarn weight means thickness, not how heavy the ball is. A 100 g ball can be lace or super bulky."),
]
page("yarn-weights.html", "Yarn Weight Chart: Lace to Jumbo, Needle and Hook Sizes | Purl & Paper",
     "Yarn weight chart from 0 lace to 7 jumbo: US and UK names, knit and crochet gauge, needle and hook sizes, and what each weight is good for.",
     yw + f'''<section><div class="wrap"><div class="aff-box"><h3>Need hooks, needles or yarn?</h3><ul class="aff-links"><li><a href="/go/crochet-hooks" rel="sponsored nofollow noopener" target="_blank">Crochet hooks</a></li><li><a href="/go/knitting-needles" rel="sponsored nofollow noopener" target="_blank">Knitting needles</a></li><li><a href="/go/yarn-by-weight" rel="sponsored nofollow noopener" target="_blank">Yarn by weight</a></li><li><a href="/go/free-patterns" rel="sponsored nofollow noopener" target="_blank">Free patterns</a></li></ul>{AFF_NOTE}</div></div></section>''', yw_faq, "Yarn weight chart")

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
page("hook-needle-sizes.html", "Crochet Hook and Knitting Needle Size Chart (mm, US, UK) | Purl & Paper",
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
<p>The two systems count differently. US names count the loops left on the hook after the first "yarn over and pull through"; UK names count the yarn wraps made at the start of the stitch. Same stitch, different counting.</p>
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
<p>What next? Knit as well? Our <a href="@@KA@@">knitting abbreviations list</a> explains k2tog, ssk, M1 and the rest, and translates a whole pattern line. Working out hook sizes from a UK pattern? See the <a href="@@HN@@">hook and needle size chart</a>, and keep count of rows with the <a href="@@RC@@">row counter</a>.</p></div></section>'''.replace("@@KA@@", href("knitting-abbreviations.html")).replace("@@HN@@", href("hook-needle-sizes.html")).replace("@@RC@@", href("row-counter.html")).replace("@@GS@@", href("granny-square-blanket-calculator.html")).replace("@@CI@@", href("crochet-circle-calculator.html"))
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
<p>Make three to six signatures, then sew each one to a spine made from a strip of card or fabric. Leave room in the spine: a junk journal gets much fatter once the pages are filled. A good first size is half a sheet of letter or A4 paper, folded.</p>
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
bk = top("Blanket size calculator", "Pick a blanket size or type your own, choose your yarn, and see the finished size next to a bed, plus how many yards and skeins to buy.", "Blanket size calculator") + f'''
<section style="padding-top:10px"><div class="wrap tool">
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
<section style="padding-top:0"><div class="narrow prose"><h2>How the yarn estimate works</h2>
<p>We work out the blanket's area and multiply it by a typical amount of yarn per square inch for plain worsted knitting, then adjust for your yarn: thinner yarn needs more length, thicker yarn less. Crochet usually takes about a quarter more yarn than knitting, cables and bobbles take more again, and open lace stitches take a little less. Granny squares are a special case, because the joins and border add up: use the <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> for those.</p>
<p>The answer is a range, because tension, stitch and borders all change it. Buy enough for the high end, from one dye lot. For hats, scarves and other projects, use our <a href="{href("yarn-calculator.html")}">yarn calculator</a>, and if your swatch doesn't match the pattern, the <a href="{href("gauge-converter.html")}">gauge converter</a> shows how big the blanket will really be. Knitting it? The <a href="{href("cast-on-calculator.html")}">cast on calculator</a> tells you how many stitches to start with for your width and gauge.</p>
<div class="callout"><strong>Allow for the border.</strong> A few rounds of border can add 5 to 10 percent more yarn on a big blanket. Fringe or tassels add more.</div>
<h2>Choosing a size</h2>
<p>For a gift, a throw (about 50 × 60 in) is the safest choice: it fits a sofa, the foot of a bed or a lap. For a baby, 30 to 36 inches square is easy to carry and wash. For a bed, measure the top of the mattress and add the drop you want on each side, usually 10 to 15 inches.</p>
<p>Making a long blanket? Keep count of rows or rounds with our <a href="{href("row-counter.html")}">row counter</a>, and log yarn and hours in the <a href="{href("projects.html")}">project tracker</a>. Not sure which yarn is which? See the <a href="{href("yarn-weights.html")}">yarn weight chart</a>. Making it from squares? The <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> tells you how many to make.</p></div></section>'''
bk_faq = [
    ("What size is a crochet throw blanket?", "Most throws are about 50 × 60 inches (127 × 152 cm). Some patterns go up to 54 × 72 inches for a longer sofa blanket."),
    ("What size is a baby blanket?", "A baby or receiving blanket is usually 30 to 40 inches square. A stroller blanket is a little smaller, about 30 × 36 inches, and a crib blanket can be as big as 45 × 60 inches."),
    ("How much yarn for a queen size crochet blanket?", "Very roughly 6,700 to 8,500 yards of worsted weight yarn for plain crochet, which is often 34 to 43 skeins of 200 yards. Chunky yarn needs far fewer yards. Use the calculator for your own yarn, and treat it as an estimate."),
    ("How many skeins for a throw blanket?", "In worsted yarn, a knitted throw takes roughly 1,800 to 2,200 yards and a crocheted one about 2,300 to 2,800 yards, so roughly 10 to 15 skeins of 200 yards once you allow a little spare. These are estimates."),
]
page("blanket-size-calculator.html", "Blanket Size Chart and Yarn Calculator for Crochet and Knitting | Purl & Paper",
     "Free blanket size chart and calculator: lovey, baby, crib, throw, twin, queen and king sizes in inches and cm, with the yards and skeins for your yarn weight.",
     bk, bk_faq, "Blanket size calculator", app_name="Blanket size calculator")

# ---------------- HANDMADE GIFT PLANNER ----------------
SRC = {"lc": "LoveCrafts", "lc-k": "LoveCrafts (knit); our estimate (crochet)", "lc-c": "LoveCrafts (crochet); our estimate (knit)", "est": "Our estimate"}
gp_opts = "".join(f'<option value="{g["id"]}"{" selected" if g["id"] == "hat" else ""}>{e(g["name"])}</option>' for g in D["gifts"])
gp_rows = "".join(f'<tr><td><strong>{e(g["name"])}</strong></td><td>{g["knit"]:g} h</td><td>{g["crochet"]:g} h</td><td class="muted">{e(SRC[g["src"]])}</td></tr>' for g in D["gifts"])
gp = top("Handmade gift planner", "List the hats, scarves and blankets you want to give, tell us how many hours a week you can craft, and see if they'll all be ready by Christmas, or which ones to swap for something quicker.", "Handmade gift planner") + f'''
<section style="padding-top:10px"><div class="wrap tool">
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
<section style="padding-top:0"><div class="wrap"><h2>How long does it take to knit or crochet a gift?</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Gift</th><th scope="col">Knitting</th><th scope="col">Crochet</th><th scope="col">Where the number comes from</th></tr></thead><tbody>{gp_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Hours for a comfortable, not brand-new, maker in medium (worsted) yarn. Hat, scarf, socks, blanket and sweater times follow the middle skill level in LoveCrafts' knitting and crochet time guides; the rest are our own rough estimates for simple patterns. Everyone's pace is different, so treat every number as a starting point and change the hours to suit you.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How the planner works</h2>
<p>It takes your hours per week and the days left until your finish date to work out how much crafting time you really have. Then it lines your gifts up in the order you listed them, like beads on a strand, and shows roughly when each one will be done. Anything that runs past the deadline turns red.</p>
<p>Fine yarn makes small stitches, so it takes longer to cover the same area; chunky yarn works up much faster. The planner allows about 30 percent more time for fine yarn and about a third less for chunky. If you've timed yourself on a similar project, type your own hours instead.</p>
<div class="callout"><strong>Time yourself once.</strong> Work for 30 minutes on your swatch or the first rows of the gift and count how much you finished. Multiply out to the whole piece and you'll have a far better number than any chart.</div>
<h2>Making it all fit</h2>
<ul><li><strong>Start the biggest gift first.</strong> Put blankets and sweaters at the top of the list so the small things fill the last weeks.</li>
<li><strong>Swap the yarn, not the gift.</strong> A hat in chunky yarn can take half the time of one in DK.</li>
<li><strong>Keep a few quick makes in reserve.</strong> Dishcloths, ornaments and headbands take an evening or two.</li>
<li><strong>Give an IOU.</strong> A wrapped skein with a note saying what it will become is a lovely gift too.</li></ul>
<p>Once you know what you're making, check how much yarn to buy with the <a href="{href("yarn-calculator.html")}">yarn calculator</a> or, for blankets, the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>. Keep notes on each gift in the <a href="{href("projects.html")}">project tracker</a>, and count rows with the <a href="{href("row-counter.html")}">row counter</a>.</p></div></section>'''
gp_faq = [
    ("How long does it take to knit a hat?", "Roughly 7 to 11 hours for a simple adult hat in worsted yarn, depending on experience. A chunky hat can be done in an evening or two."),
    ("How long does it take to crochet a blanket?", "A throw often takes 20 to 30 hours of crochet, and a knitted one about twice as long. Bigger blankets, fine yarn and fancy stitches take longer."),
    ("What can I knit or crochet in one evening?", "A dishcloth, an ornament, a headband or a chunky cowl are all realistic in one to three hours for most makers."),
    ("Is it too late to make Christmas gifts?", "Usually not. Even one hour a day gives you over 30 hours in five weeks, enough for a couple of hats and a scarf. Put your numbers into the planner to see what fits."),
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
ht = top("Hat size chart and calculator", "Head sizes from preemie to large adult, how much smaller to make the hat, and the exact number of stitches to cast on (or how wide to crochet the crown) for your yarn.", "Hat size chart") + f'''
<section style="padding-top:10px"><div class="wrap tool">
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
<section style="padding-top:0"><div class="wrap"><h2>Hat size chart</h2>
<div class="tbl-wrap"><table><thead><tr><th scope="col">Size</th><th scope="col">Typical head</th><th scope="col">Craft Yarn Council range</th><th scope="col">Hat width around (12% smaller)</th><th scope="col">Hat height</th></tr></thead><tbody>{h_rows}</tbody></table></div>
<p class="note" style="margin-top:12px">Head ranges are from the Craft Yarn Council's head circumference chart. The typical head is the middle size that yarn companies and hat designers most often quote. Hat height runs from the bottom of an unfolded brim to the top of the crown on a fitted beanie, as listed by Knit Picks. Add 2 to 3 inches for a slouchy hat or a brim you fold up (our rule of thumb). Heads vary, so measure when you can.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How to measure a head for a hat</h2>
<p>Wrap a soft tape measure around the head just above the eyebrows and ears, across the widest part at the back. Keep it level and comfortably snug, not tight. Making a surprise gift? Lay a hat the person already wears flat, without stretching it, measure across and double it.</p>
<h2>Why a hat is smaller than the head</h2>
<p>Knitted and crocheted fabric stretches, so a hat made the exact size of the head slides down over the eyes. Designers make the hat a little smaller, which is called negative ease. Most patterns use around 2 to 3 inches less than the head on an adult, or roughly 10 to 15 percent.</p>
<ul><li><strong>Ribbing</strong> pulls in and springs back, so ribbed hats can be made smaller.</li>
<li><strong>Thick yarn</strong> and firm stitches stretch less, so they need less ease.</li>
<li><strong>Crochet</strong> usually stretches less than knitting, so many crocheters make the band only a little smaller than the head. That's why the calculator suggests less ease for crochet.</li>
<li><strong>Babies and children</strong> grow fast. When in doubt, go a little bigger.</li></ul>
<div class="callout"><strong>Swatch in the round if you can.</strong> Measure your stitches over 4 inches (10 cm) after washing the swatch. Half a stitch per inch can change an adult hat by 2 inches.</div>
<h2>Knitting a hat: the cast-on maths</h2>
<p>Multiply the hat width by your stitches per inch, then round to a number that suits your rib and crown. For example, a 22 inch head with 12 percent ease gives a 19.4 inch hat. At 4.5 stitches per inch that's 87 stitches, so cast on 88. Knit until the hat is about 2.5 to 3 inches short of the full height, then start the crown decreases. Adding stitches after a ribbed brim? The <a href="{href("increase-decrease-calculator.html")}">increase evenly calculator</a> spaces them for you.</p>
<h2>Crocheting a hat from the top down</h2>
<p>Work a flat circle, increasing each round, until it measures the hat width divided by 3.14 across. Then stop increasing and work even rounds until the hat reaches the full height, measured from the centre of the crown. For a 19 inch hat that's a circle about 6 inches across.</p>
<p>Not sure which yarn to use? See the <a href="{href("yarn-weights.html")}">yarn weight chart</a> and the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>. Swatch doesn't match the pattern? The <a href="{href("gauge-converter.html")}">gauge converter</a> shows the size you'll really get. A simple adult beanie takes roughly 200 yards of worsted yarn; the <a href="{href("yarn-calculator.html")}">yarn calculator</a> covers other weights. Making hats for Christmas? Check the timing in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Matching socks? The <a href="{href("sock-size-chart.html")}">sock size chart</a> works out the cast-on the same way.</p></div></section>'''
ht_faq = [
    ("What size should an adult knit hat be?", "Most adult heads are 21 to 24 inches around. A fitted beanie is usually made 2 to 3 inches smaller, so about 19 to 21 inches around, and about 11 inches tall before any fold-up brim."),
    ("How many stitches do I cast on for a hat?", "Multiply the hat width (head size minus about 12 percent) by your stitches per inch, then round to suit your rib. In worsted yarn at 4.5 stitches per inch, an average adult hat is about 88 stitches."),
    ("How big should a crochet hat crown circle be?", "Divide the hat width by 3.14. For an adult hat about 20 inches around, increase until the flat circle is about 6.4 inches across, then work even."),
    ("What size is a newborn hat?", "A newborn head is about 14 inches around, so a newborn hat is usually about 12 to 13 inches around and 6 inches tall."),
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
gs = top("Granny square blanket calculator", "How many granny squares you need for any blanket, how to lay them out, and roughly how much yarn the squares, joins and border will take.", "Granny square calculator") + f'''
<section style="padding-top:10px"><div class="wrap tool">
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
<h2>Squares versus a one-piece granny blanket</h2>
<p>Separate squares are portable and easy to fit in, and you can stop the moment the blanket is big enough. A giant granny square worked as one piece has no seams to sew, but it gets heavy and you can't change its shape later. Either way, check the size against a bed or sofa with the <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a>, keep count of finished squares with the <a href="{href("row-counter.html")}">row counter</a>, and see how long it will take in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>. Following a UK pattern? Our <a href="{href("crochet-terms.html")}">US and UK crochet terms</a> page explains why a UK treble is a US double.</p></div></section>'''
gs_faq = [
    ("How many granny squares do I need for a throw blanket?", "With 6 inch squares, a 50 × 60 inch throw takes about 8 across by 10 down, or 80 squares, before a border. With 4 inch squares it's about 195."),
    ("How many 6 inch granny squares for a queen blanket?", "About 15 across by 17 down, or 255 squares, for a 90 × 100 inch queen blanket with no border. A 3 inch border on each side brings it down to about 14 × 16, or 224."),
    ("How much yarn is in one granny square?", "A 5 inch worsted granny square of five rounds uses roughly 25 to 30 yards. For a whole blanket, allow roughly a yard of worsted yarn per square inch of blanket, so about 3,000 yards for a 50 × 60 inch throw. This is an estimate; measure one of yours to be sure."),
    ("How many granny squares for a baby blanket?", "A 36 inch square baby blanket takes 36 squares of 6 inches (6 × 6), or 81 squares of 4 inches (9 × 9), before a border."),
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
<p>The same way, with one difference: each decrease uses two stitches. If you need to decrease 10 from 90, every 9 stitches hold one decrease, so you knit 7 and then knit 2 together. Forgetting this is the most common reason a row ends with the wrong count. In crochet a decrease (sc2tog) also works two stitches together.</p>
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
<h2>Pricing for a craft fair</h2>
<ul><li><strong>Spread the table fee</strong> over the items you realistically expect to sell, not the number you're bringing.</li>
<li><strong>Bring a range</strong>: a few small makes under $15 (scrunchies, coasters, keychains) so people can buy something, and bigger pieces that show what you can do.</li>
<li><strong>Use round prices</strong> like $15, $25, $40. They're quicker to take and to make change for.</li></ul>
<h2>What next?</h2>
<p>Not sure how long an item takes? The <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a> has typical hours for 14 projects. Work out the yarn first with the <a href="{href("yarn-calculator.html")}">yarn calculator</a>, then log each make with its hours and yarn in the <a href="{href("projects.html")}">project tracker</a> so the next price is easier. Want this as a spreadsheet you can keep? Our pricing calculator in the shop below does it for every item you make.</p></div></section>'''
pr_faq = [
    ("What is the formula for pricing crochet items?", "Materials + (hours × your hourly rate), plus a percentage for overheads such as tools and packaging, plus the selling fees. Shipping is charged separately."),
    ("What hourly rate should I charge for crochet?", "At least your local minimum wage. Crochet business guides commonly suggest $12 to $20 an hour in the US, more for skilled or custom work."),
    ("How much should I charge for a crochet hat?", "With about $5 of yarn and 2.5 hours at $15 an hour, around $45 to $50, or about $52 on Etsy once fees are covered. Quick chunky hats can be less; colourwork or fine yarn more."),
    ("How much does Etsy take from a sale?", "In the US, 6.5% of the order including shipping, plus 3% + $0.25 for payment processing and $0.20 to list. That's roughly 9.5% + $0.45, more if the sale came from an Offsite Ad."),
    ("Is materials times 3 a good way to price crochet?", "Only for quick items. It ignores time, so anything that takes more than an hour or two ends up paying you very little."),
]
page("how-to-price-crochet-items.html", "How to Price Crochet and Knitting Items (Free Calculator) | Purl & Paper",
     "The formula for pricing crochet and knitted items to sell: materials, an hourly rate, overheads and Etsy or craft fair fees, with a free calculator and example prices.",
     prc, pr_faq, "How to price crochet", app_name="Crochet and knitting price calculator")

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
<p>A common rule is about 1 in of tail per stitch for worsted yarn, plus a few inches to weave in. Thinner yarn needs less, thick yarn more, so the calculator scales it by your gauge (our estimate). For a big cast-on, wrap the yarn around the needle 10 times, measure that length, and multiply by the number of stitches ÷ 10. Casting on a blanket? Use two ends of the ball (one from the middle, one from the outside) so you can't run out.</p>
<h2>Which needle should I use for a wide cast-on?</h2>
<p>Straight needles hold a scarf or dishcloth easily. For a wrap or blanket, use a long circular needle (32 to 40 in, or longer for big blankets) and knit back and forth: the weight sits on the cable instead of your wrists. In the round, pick a circular that is shorter than the piece is around, so the stitches reach without stretching. A 16 in circular suits hats, 24 in suits most cowls, and a long infinity scarf can go on a 32 to 47 in cable.</p>
<h2>How many chains for crochet?</h2>
<p>Work out the number of stitches the same way, from your crochet swatch. Then chain that number plus the turning chain your pattern's first row asks for (often 1 extra for single crochet, more for taller stitches). Your pattern says which chain to start in, and that decides the exact number.</p>
<p>What next? Check your needle size on the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>, see how much yarn it takes with the <a href="{href("yarn-calculator.html")}">yarn calculator</a> or <a href="{href("blanket-size-calculator.html")}">blanket calculator</a>, see the size your swatch will really give with the <a href="{href("gauge-converter.html")}">gauge converter</a>, and space out shaping with the <a href="{href("increase-decrease-calculator.html")}">increase evenly calculator</a>.</p></div></section>'''
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
<p>What next? Shaping something that isn't round? The <a href="{href("increase-decrease-calculator.html")}">increase evenly calculator</a> spaces increases across any row. Making a crochet hat? The <a href="{href("hat-size-chart.html")}">hat size calculator</a> gives the crown circle size for any head. Reading a UK pattern? Check the <a href="{href("crochet-terms.html")}">US and UK crochet terms</a>, and keep count of your rounds with the <a href="{href("row-counter.html")}">row counter</a>.</p></div></section>'''
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
<li><strong>Keep your place.</strong> The <a href="@@RC@@">row counter</a> keeps count and repeat numbers for you.</li></ol>
<p>Shaping a row yourself? The <a href="@@ID@@">increase and decrease evenly calculator</a> writes the row out in these same abbreviations, and the <a href="@@CO@@">cast on calculator</a> tells you how many stitches to start with.</p>
<p class="note">Abbreviations follow the Craft Yarn Council's knitting abbreviations list and LoveCrafts' guide; UK names from Little Red Window's UK vs US terms guide. Explanations are in our own words.</p></div></section>'''
for k_, f_ in (("@@CT@@", "crochet-terms.html"), ("@@HN@@", "hook-needle-sizes.html"), ("@@YW@@", "yarn-weights.html"), ("@@GC@@", "gauge-converter.html"), ("@@RC@@", "row-counter.html"), ("@@ID@@", "increase-decrease-calculator.html"), ("@@CO@@", "cast-on-calculator.html")):
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
<p>Yes, and it's half the fun. Stain plain paper with tea (our <a href="@@TS@@">tea staining guide</a> has the recipe), cut tags from cereal box card, turn envelopes into pockets, and write labels by hand. If you'd like a themed set ready to cut out, our printable ephemera packs below do exactly that. New to all this? Start with <a href="@@JJ@@">junk journaling for beginners</a>.</p>
<p class="note">Ideas and techniques gathered from LoveCrafts' ephemera guide, Upcycle My Stuff and My Modern Met's junk journal guides; thermal paper advice from the National Archives of Australia and the University of Illinois preservation guide. Descriptions are our own.</p></div></section>'''
for k_, f_ in (("@@JP@@", "journal-prompts.html"), ("@@TS@@", "how-to-tea-stain-paper.html"), ("@@JJ@@", "junk-journal-beginners.html")):
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

# ---------------- ABOUT / PRIVACY / 404 ----------------
page("about.html", "About Purl & Paper", "About Purl & Paper, free tools for knitting, crochet and junk journaling.",
     top("About Purl &amp; Paper", "Free, simple tools for people who make things with yarn and paper.", "About") + '''<section style="padding-top:10px"><div class="narrow prose">
<p>Purl &amp; Paper started from a simple wish: a row counter that doesn't let the phone go to sleep, and a quick answer to "how much yarn do I need?". It grew into a small set of tools and charts for knitters, crocheters and junk journalers.</p>
<p>Everything is free to use and works in your browser. Your counters, projects and saved prompts stay on your own device. The site is supported by ads.</p>
<p>Yarn amounts and size conversions come from widely used industry standards and typical pattern amounts. They're estimates, so always check your pattern and your own swatch.</p>
<h2>Contact</h2><p>Spotted a mistake or have an idea for a tool? We'd love to hear it. A contact address will be added here soon.</p></div></section>''', crumb="About")
page("privacy.html", "Privacy Policy | Purl & Paper", "How Purl & Paper handles your data.",
     top("Privacy policy", "Short version: your counters, projects and saved prompts never leave your device.", "Privacy") + f'''<section style="padding-top:10px"><div class="narrow prose">
<h2>Email list</h2><p>If you join our email list, we keep your email address with our email provider, Kit (kit.com), to send you the free printables and our updates. Every email has an unsubscribe link, and you can ask us to delete your address at any time.</p>
<h2>What we store</h2><p>The tools save your counters, projects and saved prompts in your browser's local storage on your device. We can't see them and they're not sent to us. Clearing your browser data removes them.</p>
<h2>Analytics</h2><p>We use Google Analytics to count visits and see which pages are useful. It uses cookies and collects information such as pages viewed, device type and approximate location. It doesn't tell us who you are.</p>
<h2>Advertising</h2><p>We show ads through Google AdSense. Google and its partners may use cookies to show ads based on your visits to this and other sites. You can turn off personalised ads in <a href="https://adssettings.google.com" rel="nofollow noopener">Google's ad settings</a>. More detail is in <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow noopener">how Google uses information from sites that use its services</a>.</p>
<h2>Changes</h2><p>We'll update this page if anything changes. Last updated {e(UPDATED)}.</p></div></section>''', crumb="Privacy")
page("404.html", "Page not found | Purl & Paper", "This page doesn't exist.",
     f'<section><div class="narrow" style="text-align:center"><h1>Dropped a stitch.</h1><p class="lead" style="margin-inline:auto">This page doesn\'t exist. It may have moved.</p><div class="btns" style="justify-content:center"><a class="btn gold" href="{href("index.html")}">Back to the home page</a><a class="btn ghost" href="{href("row-counter.html")}">Open the row counter</a></div></div></section>')

# ---------------- SITEMAP / ROBOTS ----------------
page("thanks.html", "Check your inbox | Purl & Paper", "Confirm your email to get your free printables.", NL_THANKS)
page("welcome.html", "Your free printables | Purl & Paper", "Download your free printable sampler.", NL_WELCOME)

LASTMOD = {"knitting-abbreviations.html": "2026-11-23", "junk-journal-ephemera-ideas.html": "2026-11-23", "crochet-circle-calculator.html": "2026-11-22", "yarn-calculator.html": "2026-11-22", "cast-on-calculator.html": "2026-11-22", "journal-prompts.html": "2026-11-22", "yarn-substitution-calculator.html": "2026-11-22", "how-to-tea-stain-paper.html": "2026-11-22", "junk-journal-beginners.html": "2026-11-23", "yarn-weights.html": "2026-11-22", "sock-size-chart.html": "2026-11-22", "hook-needle-sizes.html": "2026-11-22", "hat-size-chart.html": "2026-11-22", "increase-decrease-calculator.html": "2026-11-21", "how-to-price-crochet-items.html": "2026-11-21", "row-counter.html": "2026-11-21", "granny-square-blanket-calculator.html": "2026-11-21", "crochet-terms.html": "2026-11-23", "gauge-converter.html": "2026-11-21", "blanket-size-calculator.html": "2026-11-20", 
           "crochet-knitting-gift-planner.html": "2026-11-20", "projects.html": "2026-11-20", "index.html": "2026-11-23"}
pages = ["index.html"] + [f for f, _ in NAV + TOOLS_MORE] + [f for f, _ in GUIDES] + ["about.html", "privacy.html"]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{canon(p)}</loc><lastmod>{LASTMOD.get(p, '2026-11-19')}</lastmod></url>\n" for p in pages) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
(ROOT / "ads.txt").write_text("google.com, pub-1558743317014653, DIRECT, f08c47fec0942fa0\n")
print("built", len(pages) + 1, "pages", "(preview)" if PREVIEW else "")
write_redirects(ROOT)
