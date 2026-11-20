# Awais — business operations log (source of truth)

Read this first in every session. Update it whenever a decision, list, rule or result changes.
Owner: Awais Chaudhary, Asia/Karachi (PKT). Goal: automated online income, $50k–100k/month over time.

## Standing instructions
- Act without waiting for approval; fix problems immediately; never abandon lower-priority work.
- "Data is everything." Be his manager: remind him of anything only he can do.
- Hard limits: never type passwords/bank/ID numbers; never buy anything (domains are his to buy); no trading advice;
  original art only + honest AI disclosure; don't touch AdSense settings/ads.txt; never solicit ad clicks;
  don't post as him on Reddit/Discord; no thin mass SEO pages; account-setting changes need his OK in chat;
  Google Ads (paid) off unless he gives a budget.

## Sites
| Site | Status |
|---|---|
| NeonCoast (GTA 6 guide) | Live. :07 data run + :37 map run every hour until 30 Nov; SEO twice daily. 169 pins, 88 missions, 47 cars, 55 trophies (20 Nov). Waiting on AdSense. |
| DayOneDrop | Live. AdSense verification check daily 09:05. |
| padelglassbox.com (PadelPicker) | Live. Add to AdSense only after NeonCoast/DayOneDrop approval. |
| ZAWN Technologies | Company site. |
| purlandpaperco.com (Purl & Paper crafts) | Live 19–20 Nov. GA4 G-CDBWSR0KT3, Search Console + sitemap done. Daily SEO (cloud) + daily listings/pins/deploy (18:54, needs "Require this computer"). |
| Etsy / Gumroad / Pinterest | 10 Etsy + 10 Gumroad products, Pinterest business with 3 boards. Ramp 3/day → 5/day from 27 Nov. |

## Pending for Awais
- Toggle "Require this computer" on the "Etsy, Gumroad & Pinterest daily batch" scheduled task.
- 1 Dec: AdSense check.

## Next-site pipeline
Agreed launch plan (resent by Awais 20 Nov):
1. NeonCoast (GTA 6) — live
2. DayOneDrop — live
3. Padel Glass Box — live 18 Nov
4. Crafts + junk journaling (Purl & Paper) — live 20 Nov
5. Hyrox — early December  <- NEXT
6. Home café / espresso — mid December
7. Home podcasting — January
8. LA28 Olympics fan guide — Feb–Mar
9. Mushroom kits or astrology (Claude's pick) — after that
Added 20 Nov (Awais agreed): Fable game guide, built alongside #7 in January, live by late Dec/early Jan (game out 23 Feb 2027, early access 18 Feb). Expect a fraction of GTA 6 traffic.
Still a candidate: 2027 total eclipse guide (2 Aug 2027).

## Hyrox site brief (site #5, early December)
- Awais: must have "wow factor" and bring massive traffic.
- Market: 2M+ athletes expected 2026/27, 107 race weekends on 6 continents. Already has fan sites (roxlyfe, hyranking, roxradar, rundida), so we must beat them on tools and data.
- Wow piece: race-day simulator. Enter run and station times to get a predicted finish, a percentile for your age group, a pacing plan per station and a printable race card.
- Traffic engine: one real data page per race weekend (dates, venue, divisions, weights, travel, past-results stats); "HYROX <city>" searches.
- Also: division weights/standards tables, training plans (also sold as Etsy/Gumroad printables), gear.
- Domain must not contain the HYROX trademark.
- Rule agreed 20 Nov: launch new sites without waiting for AdSense; ads go on all sites once one is approved.

## 20 Nov: 6-month roadmap and exit plan (sent to Awais)
- Dec: Hyrox + espresso live; Etsy 5/day; AdSense approval is the key unlock. Jan: podcasting + Fable. Feb–Mar: LA28, Fable launch spike. Apr–May: site 9, prune/double down, first sale candidates prepared.
- Exit rule: sell a site once it has 6+ months of steady profit; content sites sell around 24–45x monthly profit.
- Proposed SaaS #1: browser-based mockup studio for Etsy/Gumroad digital sellers (reuses tools/scenes.py), sold via Lemon Squeezy (Pakistan bank payouts supported). Awaiting Awais's go-ahead.
- Hyrox build paused at 02:43 (weights verified; 112-race calendar collected from rundida.com).
- 20 Nov 02:55: Awais happy to pay ~$10/domain and asked about 10 sites/month (100/year). Proposed instead: 4–6/month, rising toward 10 if quality and Claude usage hold; every site needs a real tool or data hook; 90-day keep/kill rule; separate AdSense risk carefully.

## Email newsletter (Kit) — set up 20 Nov 03:15
- beehiiv is not available in Pakistan; using Kit (account M AWAIS KARAMAT, from address awaiskaramat@hotmail.com).
- Forms (Clare inline, double opt-in, redirect to /thanks, after confirm to /welcome with PDF):
  Purl & Paper 10215409, NeonCoast 10215418, DayOneDrop 10215426, Padel Glass Box 10215431. Hyrox: create one at launch.
- Sites post a plain HTML form to https://app.kit.com/forms/<id>/subscriptions (field email_address); block is signup(file) in each build.py.
- Freebies built by work/freebies.py into each site's assets/free/ (rebuild NeonCoast/DayOneDrop PDFs weekly as data grows).
- Waiting on Awais: confirm Kit account email + confirm from-address email (otherwise confirmation emails don't send).
- Next: welcome sequence and weekly digest per site once subscribers arrive (Awais approved newsletters for all sites).

## Affiliate links — live 20 Nov 03:50
- System: each build.py has AFF dict -> writes Cloudflare _redirects (/go/<slug> -> store, 302); robots.txt Disallow /go/; links rel="sponsored nofollow"; disclosure line next to every placement. Script: etsy-studio/tools/add_affiliates.py. Every future site gets the same (Hyrox, espresso, podcasting, LA28).
- Placements: Padel (racket finder result + gear box on finder/beginners -> Padel Market), Purl & Paper (yarn calculator result, hook/needle + yarn weight pages -> LoveCrafts), DayOneDrop (Pre-order on Amazon on each game page), NeonCoast (home: GTA 6 + controllers on Amazon).
- Links currently go to plain store URLs (no commission yet). When each programme approves, swap URL in AFF and rebuild.
- Waiting on Awais to sign up (needs his identity + Payoneer): Awin (Padel Market), LoveCrafts affiliate (Post Affiliate Pro), Amazon Associates (US, Payoneer USD account for direct deposit).

## KDP — agreed 20 Nov 03:48
- Awais said go. Needs from him: KDP account + tax interview + bank/Payoneer. Claude designs books; AI disclosure honest on every title.
- 20 Nov 04:20: LoveCrafts affiliate applied (pending). Awin publisher account ZAWN Tech ID 3161628 created, under review (publisher pages not accessible yet) -> when approved: join Padel Market (+ other padel advertisers), swap AFF URLs. Amazon Associates: form filled (store ID purlandpaper, 4 sites) — Awais must tick Operating Agreement + Finish; then put tag into NeonCoast/DayOneDrop AFF URLs (&tag=<id>).
- KDP books 1 (Race Ready) and 2 (Knit & Crochet Project Journal) built: /home/claude/kdp/*, generators etsy-studio/tools/book_*.py, listing drafts etsy-studio/kdp/LISTINGS.md. Waiting on Awais's KDP account.
- 20 Nov 04:40: Amazon Associates COMPLETE (tag purlandpaper-20, tax done, Payoneer bank added, earning globally). Live on NeonCoast + DayOneDrop.
- Hyrox site built locally: /home/claude/hyrox-site (brand "Split Lab"; simulator, race calendar 70 races, weights, stations, 12-week plan, Amazon gear links). Not deployed: needs domain (splitlab.com taken) + Cloudflare Pages project + GA4 + Kit form.
- KDP postponed to 21 Nov at Awais's request.
- 20 Nov 05:05: KDP account set up; identity verification was in progress; payment = Pakistan bank *****704 for all marketplaces (Payoneer rejected by KDP's PSP rule). KDP verifies bank up to 3 days. Some marketplaces pay by wire with minimum thresholds.

## 20 Nov 16:00-17:15: TRAFFIC PUSH (Awais: "I need traffic, that's all I want")
Data (GA4 13-19 Nov): NeonCoast 95 users (16 Google), DayOneDrop 76, Padel ~60, Purl 20; most "direct" visits are data-centre bots (Ashburn/Boardman/Council Bluffs). GSC 16-18 Nov: NeonCoast 398 impressions, pos 8.9, ~50% "GTA 6 voice actors / who plays Jason and Lucia".
Done:
- Bing Webmaster Tools: neoncoast.org, getdayonedrop.com, padelglassbox.com, purlandpaperco.com added + verified (meta msvalidate.01 215145BE38DEE30C2985F40FB4D4041F in every build.py; never remove), sitemaps submitted, all URLs submitted (Bing quota 100/day/site). Bing also feeds ChatGPT search, Copilot, DuckDuckGo.
- Google: sitemaps resubmitted; indexing requested for new NeonCoast pages (GSC quota ~10/day/property; hit for neoncoast 20 Nov).
- NeonCoast: /characters rebuilt with launch credits (Dylan Rourke = Jason, 24 roles), homepage made post-launch (was still countdown), stale pre-launch wording fixed. SEO task now 4x daily + mandatory staleness sweep each run.
- DayOneDrop: month pages /months/<month>-2027 (6), 6 new game guides (Until Dawn 2, Metroid Ravenous, Forza Horizon 6 PS5, Witchbrook, Metro 2039, Wo Long 2). Sitemap 16 -> 30 URLs. SEO task fixed (fresh fetch/reset + verify push).
- Purl & Paper: blanket calculator deployed (site deploys only via zip upload; batch task does it nightly).
DAILY TRAFFIC LOOP (main session, at each morning check-in): read GSC queries per site (rows=100) -> find high-impression/low-CTR or stale pages -> fix -> push -> GSC request indexing (top 5-10) + Bing URL submit -> note in this file.
Next levers: more DayOneDrop game pages as facts appear (Kingdom Hearts IV, Pokemon Winds and Waves, 007 First Light Switch 2, Squadron 42, Stranger Than Heaven); Pinterest for Purl (needs "Require this computer"); Reddit posts are Awais's to make (drafts can be prepared).
- 20 Nov 16:50: Awais: "8 times a day, even for all sites... do whatever is needed, just bring traffic". Cadence now: NeonCoast SEO 8x/day (:23 every 3h) + data runs :07/:37 hourly to 30 Nov; DayOneDrop SEO 4x/day (00/06/12/18:19) + data 2x; Padel 3x/day (09/15/21:43, prompt fixed to clone without add_repo + verify push); Purl & Paper 3x/day (08/14/20:37); ZAWN blog 2x/day (11:13, 23:13). Rule stays: no thin pages; a run with nothing worthwhile improves an existing page.
- Purl & Paper only goes live via nightly Chrome zip upload. Proposed to Awais: new Git-connected Cloudflare Pages project + move purlandpaperco.com to it so it auto-deploys like the others (needs his OK: account change).
