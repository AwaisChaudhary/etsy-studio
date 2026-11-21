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
TOOLS_MORE = [("blanket-size-calculator.html", "Blanket size calculator"), ("crochet-knitting-gift-planner.html", "Handmade gift planner"), ("hat-size-chart.html", "Hat size calculator"), ("granny-square-blanket-calculator.html", "Granny square calculator")]
GUIDES = [("yarn-weights.html", "Yarn weight chart"), ("hook-needle-sizes.html", "Hook and needle sizes"),
          ("crochet-terms.html", "US vs UK crochet terms"), ("junk-journal-beginners.html", "Junk journaling for beginners")]
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
 "christmas-gift-tags": ("Printable Christmas gift tags", "3.99", "4621715645/printable-christmas-gift-tags-holiday", "christmas-gift-tags"),
}
KNIT = ["2027-crochet-knitting-planner", "yarn-stash-tracker", "crochet-knitting-pricing-calculator"]
JJ = ["junk-journal-mega-bundle", "tea-room-junk-journal-kit", "night-garden-junk-journal-kit"]
SHOP_FOR = {"index.html": ["junk-journal-mega-bundle", "2027-crochet-knitting-planner", "night-garden-junk-journal-kit", "yarn-stash-tracker"],
            "row-counter.html": KNIT, "yarn-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator"],
            "gauge-converter.html": KNIT, "projects.html": KNIT, "yarn-weights.html": KNIT, "hook-needle-sizes.html": KNIT, "crochet-terms.html": KNIT,
            "journal-prompts.html": ["journaling-cards-3x4", "vintage-ephemera-pack", "junk-journal-mega-bundle"], "junk-journal-beginners.html": JJ,
            "blanket-size-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator"],
            "hat-size-chart.html": ["2027-crochet-knitting-planner", "christmas-gift-tags", "yarn-stash-tracker", "crochet-knitting-pricing-calculator"],
            "granny-square-blanket-calculator.html": ["yarn-stash-tracker", "2027-crochet-knitting-planner", "crochet-knitting-pricing-calculator", "christmas-gift-tags"],
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
<script>window.PP={json.dumps({k: D[k] for k in ("prompts", "projects", "weights", "blankets", "gifts", "hats")}, ensure_ascii=False)};</script>
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
</div><p class="guides-more">New on the work table: the <a href="{href("granny-square-blanket-calculator.html")}">granny square blanket calculator</a> (how many squares and how much yarn), the <a href="{href("hat-size-chart.html")}">hat size chart and cast-on calculator</a> (preemie to adult, knit or crochet), the <a href="{href("crochet-knitting-gift-planner.html")}">handmade Christmas gift planner</a> (will your knitted and crocheted gifts be ready in time?) and the <a href="{href("blanket-size-calculator.html")}">blanket size chart and yarn calculator</a>, from lovey to king size.</p></div></section>'''
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
<section style="padding-top:0"><div class="narrow prose"><h2>How to use the repeat counter</h2>
<p>Many patterns repeat a set of rows, like "repeat rows 1 to 8 six times". Put <strong>8</strong> in "Repeat every". The counter then shows which row of the repeat you're on and adds one to your repeat count each time you finish the set.</p>
<p>Use a second counter for something separate, like decreases on a sleeve or rounds on a hat crown, so you never have to keep two numbers in your head.</p></div></section>'''
rc_faq = [
    ("How do I stop my phone screen turning off while I knit?", "Tick 'Keep screen on'. It uses your browser's screen wake feature, which works in most up-to-date browsers on Android, iPhone and computers. It switches off when you leave the page."),
    ("Does the row counter work offline?", "Once the page has loaded it keeps working without a connection, and your counts are saved on your device."),
    ("Can I count rounds instead of rows?", "Yes. Rename the counter to 'Rounds' by tapping its name. It counts the same way."),
]
page("row-counter.html", "Free Online Row Counter for Knitting and Crochet | Purl & Paper",
     "A free row counter for knitting and crochet with big tap buttons, repeat counting, targets, multiple counters and a keep-screen-on switch. Saves automatically.",
     rc, rc_faq, "Row counter", app_name="Row counter")

# ---------------- YARN CALCULATOR ----------------
wopts = "".join(f'<option value="{w["n"]}"{" selected" if w["n"] == 4 else ""}>{w["n"]} {e(w["name"])} ({e(w["also"])})</option>' for w in D["weights"])
popts = "".join(f'<option value="{p["id"]}">{e(p["name"])}</option>' for p in D["projects"])
yc = top("How much yarn do I need?", "Choose what you're making, the size and your yarn weight. You get an estimate in yards and metres, and how many skeins to buy.", "Yarn calculator") + f'''
<section style="padding-top:10px"><div class="wrap tool">
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
<p>Blankets vary so much in size that a single number isn't much help. Our <a href="{href("blanket-size-calculator.html")}">blanket size calculator</a> lists the usual sizes from lovey to king, draws your blanket next to a bed, and works out the yarn from the exact width and length you want.</p></div></section>'''
yc_faq = [
    ("How many skeins do I need for a blanket?", "A throw of about 125 by 150 cm (50 by 60 in) usually takes around 1,800 to 2,200 yards of worsted yarn when knitted, which is often 9 to 11 skeins of 200 yards. Crochet takes more. For other blanket sizes, use the blanket size calculator."),
    ("How do I work out yarn for a project that isn't listed?", "Pick a similar project in the list and adjust, or use a swatch: weigh a 10 cm (4 in) square, multiply by how many squares fit your piece to get the grams, then use the yards per gram on your yarn label. Add about 10 percent for seams and borders."),
    ("Does crochet use more yarn than knitting?", "Usually yes, often about 25 to 30 percent more for the same size piece, because crochet stitches are taller and denser."),
    ("Why does thinner yarn need more yards?", "Thin yarn makes small stitches, so you need many more of them, and much more length, to cover the same area."),
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
<h2>Making gifts this year?</h2>
<p>Add each gift as a planned project, then check the timing in our <a href="@@GP@@">handmade gift planner</a>. It adds up the hours for every hat, scarf and blanket on your list and tells you whether they'll be finished by Christmas or another deadline. For how much yarn each one needs, use the <a href="@@YC@@">yarn calculator</a>.</p></div></section>'''.replace("@@GP@@", href("crochet-knitting-gift-planner.html")).replace("@@YC@@", href("yarn-calculator.html"))
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
<div class="toolbar"><button type="button" class="btn gold" id="jp-go">Shuffle my spread</button><button type="button" class="btn ghost" id="jp-save">Save this spread</button><button type="button" class="btn ghost" id="jp-print">Print</button></div>
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
<section style="padding-top:0"><div class="narrow prose"><h2>Using prompts without getting stuck</h2>
<p>Treat a prompt as a starting point, not a rule. If "a ticket stub" isn't in your stash, use anything with printed numbers on it. If the palette doesn't suit the theme, keep just one colour from it.</p>
<p>A good rhythm for a two-page spread: lay down a background paper, add one big focal piece, tuck in something interactive (a pocket, flap or tag), and finish with a few words. New to all this? Start with our <a href="@@JJ@@">junk journaling guide for beginners</a>.</p></div></section>'''
jp_faq = [
    ("What do you put in a junk journal?", "Anything flat and paper-like that you'd normally throw away: receipts, tickets, envelopes, tea bags, packaging, book pages, plus photos, washi tape, fabric and your own writing."),
    ("How do I get ideas for junk journal pages?", "Pick one theme and one thing to glue in, then build around them. The shuffle above does this for you, and you can lock what you like."),
]
jp = jp.replace("@@JJ@@", href("junk-journal-beginners.html"))
page("journal-prompts.html", "Junk Journal Prompts Generator: Ideas for Your Next Spread | Purl & Paper",
     "Free junk journal prompt generator. Shuffle a theme, ephemera to use, a technique, a colour palette and a writing prompt, then lock and save your favourites.",
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
<p>Stay in the same weight number, then knit or crochet a swatch. Two yarns in the same category can still differ, so check the length per 100 g on both labels: if they're close, the swap usually works.</p></div></section>'''
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
hn = top("Hook and needle size chart", "Metric, US and old UK sizes side by side. Type any size to jump to it.", "Hook and needle sizes") + f'''
<section style="padding-top:10px"><div class="narrow">
<div class="finder"><div class="field"><label for="hn-q">Find a size</label><input type="search" id="hn-q" placeholder="e.g. 4.5, US 8, H-8, UK 6"></div><p class="note" id="hn-hit" style="margin:0 0 12px"></p></div>
<div class="tbl-wrap"><table id="hn-table"><thead><tr><th scope="col">Metric</th><th scope="col">US knitting needle</th><th scope="col">Old UK / Canadian needle</th><th scope="col">US crochet hook</th></tr></thead><tbody>{srows}</tbody></table></div>
<p class="note" style="margin-top:12px">"—" means there's no common size at that point. Brands sometimes label in-between sizes differently, so the millimetre size is the one to trust.</p>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>Always go by millimetres</h2>
<p>US letters and numbers, and old UK numbers, were never fully standard, and the old UK system runs backwards (a bigger number means a thinner needle). The metric size is printed on almost every modern hook and needle, so if a pattern gives a millimetre size, use that.</p>
<h2>Steel crochet hooks are different</h2>
<p>Tiny steel hooks for crochet thread use their own numbers, where a <strong>higher</strong> number is a <strong>smaller</strong> hook. Check the millimetre size on the handle.</p></div></section>'''
hn_faq = [
    ("What size is an H crochet hook?", "An H-8 hook is 5 mm."),
    ("What is a US size 8 knitting needle in mm?", "A US 8 needle is 5 mm, the same as an old UK size 6."),
    ("What size hook for worsted yarn?", "Worsted (weight 4) usually starts with a 5.5 to 6.5 mm hook (I-9 to K-10½). Check your yarn label and swatch."),
]
page("hook-needle-sizes.html", "Crochet Hook and Knitting Needle Size Chart (mm, US, UK) | Purl & Paper",
     "Crochet hook and knitting needle size conversion chart: metric mm, US numbers and letters, and old UK sizes, with a quick size finder.",
     hn + f'''<section><div class="wrap"><div class="aff-box"><h3>Need hooks, needles or yarn?</h3><ul class="aff-links"><li><a href="/go/crochet-hooks" rel="sponsored nofollow noopener" target="_blank">Crochet hooks</a></li><li><a href="/go/knitting-needles" rel="sponsored nofollow noopener" target="_blank">Knitting needles</a></li><li><a href="/go/yarn-by-weight" rel="sponsored nofollow noopener" target="_blank">Yarn by weight</a></li><li><a href="/go/free-patterns" rel="sponsored nofollow noopener" target="_blank">Free patterns</a></li></ul>{AFF_NOTE}</div></div></section>''', hn_faq, "Hook and needle sizes")

# ---------------- CROCHET TERMS ----------------
trows = "".join(f'<tr><td><strong>{e(t[0])}</strong>{f" ({e(t[1])})" if t[1] else ""}</td><td><strong>{e(t[2])}</strong>{f" ({e(t[3])})" if t[3] else ""}</td><td class="muted">{e(t[4])}</td></tr>' for t in D["terms"])
ct = top("US vs UK crochet terms", "The same stitch has a different name on each side of the Atlantic. Here's the full conversion, and how to tell which terms your pattern uses.", "US vs UK crochet terms") + f'''
<section style="padding-top:10px"><div class="narrow">
<div class="callout" style="margin-top:0"><strong>The short version:</strong> UK names are one step "taller" than US names. A UK double crochet is a US single crochet, a UK treble is a US double, and so on.</div>
<div class="tbl-wrap"><table><thead><tr><th scope="col">US term</th><th scope="col">UK term</th><th scope="col">Note</th></tr></thead><tbody>{trows}</tbody></table></div>
</div></section>
<section style="padding-top:0"><div class="narrow prose"><h2>How to tell if a pattern uses US or UK terms</h2>
<ul><li><strong>Look for "single crochet" or "sc".</strong> UK patterns don't have a single crochet, so if you see one, it's US.</li>
<li><strong>Check the spelling and words.</strong> "Colour", "tension" and "miss" point to a UK pattern; "color", "gauge" and "skip" point to US.</li>
<li><strong>Check the hook sizes.</strong> Letter sizes like H-8 suggest US; millimetres only don't tell you much.</li>
<li><strong>Read the notes at the top.</strong> Most designers say which terms they use.</li></ul>
<h2>Why are they different?</h2>
<p>The two systems count differently. US names count the loops left on the hook after the first "yarn over and pull through"; UK names count the yarn wraps made at the start of the stitch. Same stitch, different counting.</p>
<h2>Crochet abbreviations: US and UK</h2>
<p>These short forms look the same in both kinds of pattern. Only the stitch names in the table above change.</p>
</div><div class="narrow"><div class="tbl-wrap"><table><thead><tr><th scope="col">Abbreviation</th><th scope="col">Means</th><th scope="col">Note</th></tr></thead><tbody><tr><td><strong>ch</strong></td><td>chain</td><td class="muted">same in both</td></tr><tr><td><strong>sl st</strong></td><td>slip stitch</td><td class="muted">same in both (UK patterns sometimes say ss)</td></tr><tr><td><strong>st(s)</strong></td><td>stitch(es)</td><td class="muted"></td></tr><tr><td><strong>sp</strong></td><td>space</td><td class="muted">e.g. ch-2 sp, the gap under a chain of 2</td></tr><tr><td><strong>rnd</strong></td><td>round</td><td class="muted">worked in a circle or square</td></tr><tr><td><strong>RS / WS</strong></td><td>right side / wrong side</td><td class="muted"></td></tr><tr><td><strong>rep</strong></td><td>repeat</td><td class="muted"></td></tr><tr><td><strong>yo / yoh</strong></td><td>yarn over / yarn over hook</td><td class="muted">US says yo, UK often yoh or yrh</td></tr><tr><td><strong>sk / miss</strong></td><td>skip</td><td class="muted">US skip, UK miss</td></tr><tr><td><strong>inc</strong></td><td>increase</td><td class="muted">2 or more stitches in one stitch</td></tr><tr><td><strong>dec / tog</strong></td><td>decrease / together</td><td class="muted">e.g. sc2tog (US) is dc2tog (UK)</td></tr><tr><td><strong>BLO / FLO</strong></td><td>back loop only / front loop only</td><td class="muted"></td></tr><tr><td><strong>beg</strong></td><td>beginning</td><td class="muted"></td></tr><tr><td><strong>cont</strong></td><td>continue</td><td class="muted"></td></tr><tr><td><strong>FO</strong></td><td>fasten off</td><td class="muted">same in both</td></tr><tr><td><strong>*  *</strong></td><td>repeat the part between the asterisks</td><td class="muted"></td></tr></tbody></table></div></div>
<div class="narrow prose"><h2>One granny square round, written both ways</h2>
<p>Here's the second round of a classic granny square. Same stitches, same square, two sets of names.</p>
<p><strong>US terms:</strong> sl st into the ch-2 sp, ch 3 (counts as dc), 2 dc in same sp, ch 1, *(3 dc, ch 2, 3 dc) in next ch-2 corner sp, ch 1; rep from * around, ending with 3 dc in the first sp, ch 2, sl st to top of ch 3.</p>
<p><strong>UK terms:</strong> ss into the ch-2 sp, ch 3 (counts as tr), 2 tr in same sp, ch 1, *(3 tr, ch 2, 3 tr) in next ch-2 corner sp, ch 1; rep from * around, ending with 3 tr in the first sp, ch 2, ss to top of ch 3.</p>
<p>Planning a whole blanket of squares? The <a href="@@GS@@">granny square blanket calculator</a> works out how many squares, the layout and roughly how much yarn.</p></div></section>'''.replace("@@GS@@", href("granny-square-blanket-calculator.html"))
ct_faq = [
    ("Is UK double crochet the same as US single crochet?", "Yes. A UK double crochet (dc) is worked exactly like a US single crochet (sc)."),
    ("What is a treble crochet in US terms?", "A UK treble (tr) is a US double crochet (dc). A US treble (tr) is a UK double treble (dtr)."),
    ("What does ch-2 sp mean in crochet?", "It means the space under a chain of 2 made on the round before. You work the new stitches into that gap, not into the chains themselves. It's written the same way in US and UK patterns."),
    ("Is a granny square made with double or treble crochet?", "Both, depending on the pattern's terms. A classic granny square uses clusters of US double crochet, which a UK pattern calls treble crochet. The stitch is the same."),
]
page("crochet-terms.html", "US vs UK Crochet Terms and Abbreviations: Conversion Chart | Purl & Paper",
     "US and UK crochet terms side by side: single crochet vs double crochet, treble, half treble and more, common abbreviations, how to tell which a pattern uses, and a granny square round in both.",
     ct, ct_faq, "US vs UK crochet terms")

# ---------------- JUNK JOURNAL BEGINNERS ----------------
jj = top("Junk journaling for beginners", "A junk journal is a handmade book filled with paper you'd normally throw away. Here's what you need, how to make your first one, and how to fill it.", "Junk journaling for beginners") + f'''
<section style="padding-top:10px"><div class="narrow prose">
<h2>What is a junk journal?</h2>
<p>It's part scrapbook, part diary, part art project. The pages are made from mixed papers like envelopes, book pages, paper bags and packaging, and you decorate them with ephemera (small bits of everyday paper like tickets, receipts and labels). There are no rules about what it should look like, and "messy" is part of the charm.</p>
<h2>What you need to start</h2>
<ul><li><strong>Paper for pages:</strong> envelopes, paper bags, old book or dictionary pages, printer paper stained with tea, cereal box card for covers.</li>
<li><strong>Glue:</strong> a glue stick is enough to start. Matte gel medium or PVA glue holds heavier pieces.</li>
<li><strong>Something to bind with:</strong> a needle, strong thread or thin twine, and a pin or awl to poke holes.</li>
<li><strong>Scissors and a ruler.</strong></li>
<li><strong>Ephemera:</strong> start a box today and drop in anything interesting. Our <a href="{href("journal-prompts.html")}">prompt generator</a> suggests what to use.</li></ul>
<div class="callout">You don't need to buy kits or special paper. Most beginners' first journal is made almost entirely from things already in the house.</div>
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
<ul><li><strong>Tea staining:</strong> brush cooled black tea onto paper, or dip it, then dry flat. Coffee gives a darker brown.</li>
<li><strong>Torn edges:</strong> tear paper against a ruler for a soft, aged edge.</li>
<li><strong>Layering:</strong> stack three papers from biggest to smallest, slightly off-centre.</li>
<li><strong>Hand stitching:</strong> a running stitch around a photo frames it instantly.</li></ul>
</div></section>'''
jj_faq = [
    ("Do I need special supplies to make a junk journal?", "No. Paper from around the house, a glue stick, a needle and thread are enough for your first one."),
    ("What's the difference between a junk journal and a scrapbook?", "Scrapbooks usually use bought, acid-free supplies and focus on photos. Junk journals are made from recycled paper and everyday ephemera, and mix in writing and art."),
    ("How many pages should a junk journal have?", "There's no rule. A single signature of 5 to 8 folded sheets (20 to 32 pages) is a good first project."),
]
page("junk-journal-beginners.html", "Junk Journaling for Beginners: Supplies, Binding and Ideas | Purl & Paper",
     "How to start a junk journal: what it is, the free supplies you need, how to sew your first signature, and easy techniques to fill the pages.",
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
<p>The answer is a range, because tension, stitch and borders all change it. Buy enough for the high end, from one dye lot. For hats, scarves and other projects, use our <a href="{href("yarn-calculator.html")}">yarn calculator</a>, and if your swatch doesn't match the pattern, the <a href="{href("gauge-converter.html")}">gauge converter</a> shows how big the blanket will really be.</p>
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
<p>Multiply the hat width by your stitches per inch, then round to a number that suits your rib and crown. For example, a 22 inch head with 12 percent ease gives a 19.4 inch hat. At 4.5 stitches per inch that's 87 stitches, so cast on 88. Knit until the hat is about 2.5 to 3 inches short of the full height, then start the crown decreases.</p>
<h2>Crocheting a hat from the top down</h2>
<p>Work a flat circle, increasing each round, until it measures the hat width divided by 3.14 across. Then stop increasing and work even rounds until the hat reaches the full height, measured from the centre of the crown. For a 19 inch hat that's a circle about 6 inches across.</p>
<p>Not sure which yarn to use? See the <a href="{href("yarn-weights.html")}">yarn weight chart</a> and the <a href="{href("hook-needle-sizes.html")}">hook and needle size chart</a>. Swatch doesn't match the pattern? The <a href="{href("gauge-converter.html")}">gauge converter</a> shows the size you'll really get. A simple adult beanie takes roughly 200 yards of worsted yarn; the <a href="{href("yarn-calculator.html")}">yarn calculator</a> covers other weights. Making hats for Christmas? Check the timing in the <a href="{href("crochet-knitting-gift-planner.html")}">handmade gift planner</a>.</p></div></section>'''
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

LASTMOD = {"granny-square-blanket-calculator.html": "2026-11-21", "crochet-terms.html": "2026-11-21", "hat-size-chart.html": "2026-11-21", "gauge-converter.html": "2026-11-21", "blanket-size-calculator.html": "2026-11-20", "yarn-calculator.html": "2026-11-20", "yarn-weights.html": "2026-11-20",
           "crochet-knitting-gift-planner.html": "2026-11-20", "projects.html": "2026-11-20", "index.html": "2026-11-21"}
pages = ["index.html"] + [f for f, _ in NAV + TOOLS_MORE] + [f for f, _ in GUIDES] + ["about.html", "privacy.html"]
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{canon(p)}</loc><lastmod>{LASTMOD.get(p, '2026-11-19')}</lastmod></url>\n" for p in pages) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
(ROOT / "ads.txt").write_text("google.com, pub-1558743317014653, DIRECT, f08c47fec0942fa0\n")
print("built", len(pages) + 1, "pages", "(preview)" if PREVIEW else "")
write_redirects(ROOT)
