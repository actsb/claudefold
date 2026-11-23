# Winter products to cover next (Dec 2026 – Feb 2027): demand, scoring and blueprints for the top 3

Compiled 2026-11-23 for Verdict Picks (https://acts39.blogspot.com). About 50 web searches and 12 page fetches, plus three own data pulls:
* Google autocomplete for 24 seed queries;
* the CPSC SaferProducts recall API (all recalls 2025-01-01 → 2026-11-23, 950 records);
* the ENERGY STAR open-data catalog.

This brief extends `research/reader-demand-2026-10.md` (§4.2 recall checker, winter running-cost calculator), `research/strategy-2026-10-amazon.md` (commission table, winter storm calendar) and `research/bf-devices-blueprint-2026-11.md` (evidence tags). It does not repeat them.

**Evidence tags** (same scheme as `bf-devices-blueprint-2026-11.md`):
* **[Official]**: government, regulator or maker page.
* **[Independent]**: named press, lab or academic source.
* **[Vendor]**: a company describing its own product, or a data seller describing its own data.
* **[Weak]**: SEO sites, aggregators, mirrors, forums, search snippets I could not open.
* **[Own data]**: a pull I ran for this brief.
* **[Inference]**: my reasoning, not a sourced fact.
* **UNVERIFIED**: not confirmed. Do not publish as fact.

**Hard rules reminder:** no Amazon prices, star ratings, review counts or review quotes. Prices only from other US stores, with the store and the date. Every price in this file comes from a **search snippet seen 2026-11-23, with no date on the listing itself**, so treat it as **[Weak]**. Re-read each price on the store page the day the post goes live, and print that date.

---

## 0. Two findings that affect posts already live (act before new posts)

1. **The Dreo DR-HSH015 space heater was recalled on 2026-10-29.**
   * About 338,800 units (plus about 36,300 in Canada). Only units made April 2025 – January 2026 are covered. Dreo has 17 reports of ignition, three with property damage and one burn injury. The remedy is a free replacement.
   * It was sold at Costco stores and online at Dreo.com, BestBuy.com, Kohls.com, Lowes.com, QVC.com, HomeDepot.com, B2BRenew.com and Costco.com from September 2025 through October 2026, for $70–$110.
   * Source: [Official] CPSC recall 27-054, https://cpsc.gov/Recalls/2027/DREO-Recalls-DR-HSH015-Space-Heaters-Due-to-Fire-and-Burn-Hazards (2026-10-29; the URL says "2027" because of CPSC's fiscal year). Confirmed via the SaferProducts API [Own data].
   * **Our post `posts/2026-10-dreo-space-heater` names the DR-HSH015** in its store table ("Costco $79.99 online, Feb 11, 2026, A different Dreo (DR-HSH015)": `post.html`, `infographics.json`, `images/stores.svg`). Its recall line mentions only "the 2023 recall check". **The post needs a recall note for DR-HSH015.** I did not edit it.
2. **Ororo recalled its PD10K-Pro heated-apparel battery packs on 2026-11-19.**
   * About 269 units (plus 24 in Canada), sold on Ororowear.com and **Amazon.com** in Sept–Oct 2026 for about $109. One overheating report, no injuries.
   * Source: [Official] CPSC recall 27-097, https://cpsc.gov/Recalls/2027/Ororo-Recalls-Rechargeable-Lithium-Ion-Battery-Packs-Due-to-Risk-of-Serious-Injury-from-Fire-and-Burn-Hazards (2026-11-19).
   * Ororo is the most-picked heated vest brand (Bob Vila, PopSci; §5.1), and its own blog says "all ororo batteries are UL certified" ([Vendor] https://www.ororowear.com/blogs/story/ororo-batteries-why-ul-certification-matters, undated). Use this in any heated-apparel coverage.

---

## 1. Demand: what US shoppers search for in winter

### 1.1 Published seasonal data

| Signal | What it shows | Source |
|---|---|---|
| Google: "cozy" searches peak every December; "sweater weather" rises in fall and winter | Search interest in comfort and warmth is seasonal | [Official] Google Keyword blog, https://blog.google/products/search/search-interest-trends-history-winter-cozy/ (2022-12-15). This is the only Google-published Trends article I found, and it names no products. |
| Slickdeals Jan 2026 search insights: top winter keywords were **snow blower, generator, heater, space heater, snow shovel, snow boots, jacket, humidifier** ("thousands of searches"; no percentages) | Humidifier and snow blower demand is still strong in January | [Vendor] https://daily.slickdeals.net/shopping/january-2026-search-insights/ (2026-02-20) |
| Planalytics: during Winter Storm Fern, local demand ran **50%–500% above normal** for heaters, blankets, ice melt, shovels and scrapers, boots, coats, gloves and **hand warmers** | Storm spikes are real but short and regional | [Vendor] https://www.planalytics.com/?p=12790 ("Monster Storm Disrupts Business…", 2026-01-27) |
| Sam's Club: online sales of snow blowers, shovels, lanterns and work lights rose **more than 2,800%** year over year; winter-weather searches rose **more than 1,500%** week over week | Storm-driven, short window | [Official] https://corporate.walmart.com/about/samsclub/news/2026/01/29/serving-our-members-through-the-storm (2026-01-29, snippet) |
| Square: total sales **+472% week over week** by Feb 1 after the storm | Pent-up demand after the storm | [Vendor] https://squareup.com/us/en/press/winter-storm-sales-freeze (2026, snippet) |
| Accio summaries of Google Trends: "ultrasonic / smart room humidifier" peaks in **Nov 2025 and Jan 2026**; Salehoo lists a **December** seasonal peak; Accio says rechargeable magnetic hand-warmer sales on Amazon peaked in **January 2026** | Humidifiers and hand warmers peak Nov–Jan | [Weak] https://www.accio.com/business/room-humidifier-trends ; https://www.salehoo.com/trends/humidifiers ; https://www.accio.com/business/electric-hand-warmer-trends (2025–26) |
| SAD searches peak in **November and again in January** (UK, 5 years of Google data). A US analysis of "seasonal depression" expects a mid-November peak | Light-therapy demand runs Nov–Jan | [Weak] search snippets for https://girlabouttravel.co.uk/article/blue-monday-sad-research/ and a krdo.com/Stacker item (undated) |
| Pinterest Predicts 2026 (released 2025-12-09): 21 trends, with "comfort" the top emotional need. **No winter-product trend relevant to us** (the closest are cabbage recipes and high-collar jackets) | Not useful for product picks | [Vendor] https://newsroom.pinterest.com/news/pinterest-predicts-nonconformity-self-preservation-and-escapism-drive-21-trends-for-2026/ (2025-12-09) |

**NRF/Adobe:** I found no NRF or Adobe figures for winter categories (humidifiers, hand warmers and so on). Those firms report on total holiday e-commerce, not these categories.

### 1.2 Own data: Google autocomplete (US, English), pulled 2026-11-23

Method: `suggestqueries.google.com`, `client=firefox&hl=en&gl=us`. This shows what people type, not search volume.

| Seed | Suggestions that matter (verbatim) |
|---|---|
| rechargeable hand warmer(s) safe | "rechargeable hand warmer **recall**", "are rechargeable hand warmers **safe for kids**", "are rechargeable hand warmers safe **reddit**", "**safest** rechargeable hand warmers", "**best and safest** rechargeable hand warmers", "how long do rechargeable hand warmers last" |
| hand warmer recall | "hand warmer recall **amazon**", "…**2026**", "…**ocoopa**", "…**death**", "…**list**", "…reddit" |
| humidifier white dust | "…**harmful**", "…everywhere", "…reddit", "…solution", "…filter", "…electronics" |
| humidifier mold | "humidifier mold free", "…resistant", "…prevention", "…symptoms", "…risk" |
| warm mist vs cool mist | "…for baby", "…for cough", "…reddit", "…for dry skin", "…for congestion", "…**for winter**" |
| humidifier for | bedroom, baby, house, plants, basement, cough, congestion, furnace, allergies |
| sad lamp / light therapy lamp / 10000 lux | "sad lamp **10000 lux**", "sad lamp reddit", "sad lamp **vitamin d**", "sad lamp alarm clock", "light therapy lamp for seasonal depression", "10000 lux light box", "**10000 lux to lumens**", "10000 lux artificial light **huberman**" |
| heated vest / battery | "heated vest **costco**", "…**milwaukee**", "…**ororo**", "heated vest battery **life**", "heated vest battery **on airplane**", "heated vest battery included" |
| heated socks / gloves | "heated socks **costco**", "heated gloves **for arthritis**" |
| ice melt safe for | "…concrete", "…pets", "…new concrete", "…pavers", "…concrete and pets", "…wood decks and pets", "ice melt pet safe home depot" |
| cordless snow blower / electric snow shovel | "…home depot", "…costco", "…clearance", "electric snow shovel vs snow blower", "…ryobi", "…ego" |
| smart thermostat worth | "…worth it reddit", "nest thermostat worth it", "ecobee… worth it" |
| boot dryer | "…with ozone", "…for work boots", "…tractor supply" |
| heated bird bath | "…solar", "…for deck railing", "…menards" |
| heated car seat cover | "…with auto shut off", "…usb" |

**Readings:**
* **Safety wording appears only in hand warmers** ("safest", "recall list", "death"). This is the clearest gap for a research site.
* For humidifiers, the questions are "harmful", "mold" and "for winter".
* For SAD lamps, people type the number itself ("10000 lux") and "reddit".
* Snow blower and ice-melt queries point to big-box stores (Home Depot, Costco), not Amazon.

### 1.3 Reddit

reddit.com did not appear in my search tool's results. I found only secondary pages that cite Reddit, for example a gummysearch/reddirecs page naming the Venta LW15, Vornado Evap40 and Levoit Classic 300S, with an r/BuyItForLife line on the Evap40: "simple knobs and switches; no fancy electronics to fail" ([Weak] https://reddirecs-ssr.pages.dev/humidifier/model/vornado-evap40-evaporative-humidifier, undated). **Before writing, check these by hand** (sort by Top, past year):
* r/BuyItForLife "humidifier";
* r/HomeImprovement "humidifier white dust";
* r/SeasonalAffective "lamp distance";
* r/Frugal "hand warmers";
* r/Alaska and r/ColdWeather "rechargeable hand warmer";
* r/Costco "heated socks recall".

---

## 2. Scoring all candidates

Each factor is scored 1–5. **Gap is weighted ×2**, because a near-zero-authority site can only win where incumbents leave a hole that public, verifiable numbers can fill. Total = Demand + 2×Gap + Monetization + Safety + Timing (max 30).

| Candidate | Demand | Gap (×2) | Monetization | Safety/recall angle | Timing Dec–Feb | **Total** | Key evidence |
|---|---|---|---|---|---|---|---|
| **Rechargeable hand warmers** | 4 | 5 | 2 | 5 | 5 | **26** | 3 CPSC recalls in 2026, about **1.58 M US units** (§3.1); ranking reviews still lead with OCOOPA (Bob Vila, GearJunkie); autocomplete shows "safest" and "recall list". Rate 3% (Sports/Outdoors) or 1% (Health), UNVERIFIED; $15–$60 |
| **Humidifiers** | 5 | 3 | 3 | 3 | 5 | **22** | Highest demand (Slickdeals Jan list; autocomplete); EPA page updated 2026-04-29; incumbents (RTINGS, CR, Wirecutter, HouseFresh) are strong, but none prints the **monthly running cost** with EPA-recommended distilled water. Home 3%; $40–$200 |
| **SAD / light-therapy lamps** | 4 | 5 | 1 | 2 | 5 | **22** | Yale and a peer-reviewed 24-device study give **measured lux at distance**, while listings say "10,000 lux" with inconsistent or no distance (§3.3). Amazon shows them under "Health & Household" → likely **1%** (UNVERIFIED) |
| Heated vests / jackets / socks / gloves / insoles | 4 | 3 | 4 | 4 | 4 | 22 | Ororo battery recall 2026-11-19; 32 Degrees socks (207,806 units, Costco, 2026-04-23); 5+ CPSC heated-insole warnings in 2026. Apparel 4%; $90–$200. The gap needs field testing that we cannot do. **Runner-up; sketch in §5.1** |
| Boot dryers | 3 | 3 | 2 | 3 | 4 | 18 | OdorStop boot dryer recall, 13,000 units ([Official] https://www.cpsc.gov/Recalls/2025/OdorStop-Recalls-Boot-and-Shoe-Dryers-and-Deodorizers-Due-to-Fire-Hazard, 2025-02-20); "with ozone" in autocomplete (an ozone-safety angle) |
| Ice melt (pet- and concrete-safe) | 4 | 3 | 1 | 2 | 4 | 17 | "Pet safe" is not a regulated term (ASPCA; CR); EPA Safer Choice lists deicers. Low ticket price, heavy item, Amazon is not the main channel. Sketch in §5.2 |
| Heated car seat covers | 2 | 3 | 3 | 2 | 4 | 17 | Automotive 4.5%; "auto shut off" in autocomplete; no 2025–26 CPSC recall found |
| Cordless snow blowers / electric shovels | 4 | 2 | 3 | 2 | 3 | 16 | Slickdeals top keyword; Sam's +2,800%; CR, Bob Vila and This Old House rank. Ryobi sells through Home Depot and EGO mainly through Lowe's; demand depends on weather; Ariens snow thrower recall 2025-02-06 |
| Smart thermostats | 4 | 2 | 3 | 1 | 3 | 15 | Strong data (ENERGY STAR dataset `7p2p-wkbf`, 121 models, updated 2026-11-13; "approximately 8%… or $50 per year"), but Wirecutter, CNET and The Verge own the topic. Sketch in §5.3 |
| Weather radios / outage kits | 3 | 3 | 2 | 1 | 3 | 15 | NWS recommends the "Public Alert" and/or "NWR All Hazards" logos, not brands (§5.4). Overlaps our winter car kit |
| Heated bird baths | 2 | 3 | 2 | 1 | 4 | 15 | Thin demand evidence; no recalls found |
| Window insulation kits / draft stoppers | 3 | 2 | 1 | 1 | 4 | 13 | Cheap, low commission, DIY content dominated by Home Depot and Lowe's |

**Tie-breaks among the 22s [Inference]:**
* **Humidifiers** win on demand.
* **SAD lamps** beat heated apparel, because their verified numbers (Yale and journal measurements) can be collected from desk research. A heated-apparel guide needs field runtime tests we cannot run.
* SAD lamps also diversify the queue: we already have two battery-heated posts in the hand-warmer blueprint's orbit.
* **If revenue per sale matters more than the data gap, swap #3 for heated vests** (Apparel 4% on $100–$200 versus about 1% on a $50–$180 lamp).

### 2.1 Commission reference

[Official] Amazon Associates Standard Commission Income Statement, https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ, read 2026-11-23. The page has no effective date (only "© 1996-2025").

| Rate | Categories |
|---|---|
| 4.5% | Kitchen, Automotive |
| 4.0% | Apparel, Shoes, "All Other Categories" |
| 3.0% | Home, Home Improvement, Lawn & Garden, Outdoors, Sports, Tools, Pets Products |
| 1.0% | Health & Personal Care, Grocery |

Amazon's own category assignment for each product decides its rate. Mirror sites show the Carex Day-Light lamps ranked under "**Health & Household** › Light Therapy Products" ([Weak] desertcart mirrors, e.g. https://www.desertcart.com.cy/products/15514400-carex-day-light-classic-plus-sunlight-therapy-lamp-10000-lux). Hand-warmer and humidifier categories are **UNVERIFIED**. Check the earnings report after the first sales.

---

## 3. The top 3 blueprints

### 3.1 #1: Rechargeable hand warmers: the 2026 recall list and the safest picks (publish Dec 1–5)

**Why now:**
* Three CPSC recalls in 2026, one with a death.
* Every top-ranking "best rechargeable hand warmer" page I found still reads as a pre-recall ranking. Bob Vila's earlier top pick, the OCOOPA H01, is on the recall list. Bob Vila's current pick (UT3 PRO) and GearJunkie's pick (UT3 PRO, 8/10) are OCOOPA models whose model numbers I could not map ([Weak] snippets of https://www.bobvila.com/reviews/best-rechargeable-hand-warmers-for-warmth/ (dated Feb 2026) and https://gearjunkie.com/winter/best-hand-warmers).
* NBC Select's recall article (updated 2026-08-10) recommends only disposable HotHands and gloves, and quotes no expert ([Independent] https://nbcnews.com/select/shopping/ocoopa-hand-warmer-recall-rcna591394).

**Target long-tail queries:** "safest rechargeable hand warmers" (primary), "hand warmer recall list", "hand warmer recall 2026", "are rechargeable hand warmers safe".

**Title (formula):** *Rechargeable Hand Warmers Sold as "UL Certified": 1.58 Million Were Recalled in 2026. Check These 8 Model Numbers First*
* Safer fallback if the UL claim cannot be documented: *Rechargeable Hand Warmers: 1.58 Million Recalled in 2026. 8 Model Numbers to Check Before You Charge One*
* The 1,582,500 total and the 8 model numbers are computed in the table below.

**The recall facts (all [Official], CPSC):**

| Recall | Date / No. | US units | Models (printed on the underside) | Incidents | Sold | Remedy | URL |
|---|---|---|---|---|---|---|---|
| OCOOPA Direct (Shenzhen Street Cat Technology) | 2026-07-30 / 26-659 | about 1.5 million | **UT3053, UT3056, ZLS-118, ZLS-118S, ZLS-118D, H01, H01(PD)** | 1,480 overheating reports, 15 fires, 350 burn injuries, **1 death** (83-year-old, Feb 2026; CPSC page says San José, other outlets say San Diego) | Amazon.com, Ocoopa.com, Ocoopa.net, Walmart.com, Sept 2018 – May 2026, $15–$60 | Refund (gift card or original payment); write "RECALLED" on the unit and send a photo with the model and batch number | https://www.cpsc.gov/Recalls/2026/OCOOPA-Direct-Recalls-1-5-Million-Rechargeable-Hand-Warmers-Due-to-Risk-of-Serious-Injury-or-Death-from-Fire-and-Burn-Hazards-One-Death-Reported-Imported-by-Shenzhen-Street-Cat-Technology |
| Kobayashi (HotHands) | 2026-10-01 / 27-011 | about 77,000 (+72 Canada) | **H163650**; only electric units with the white HotHands logo | None reported | Bass Pro, Meijer, Target, Home Depot, **Amazon.com**, July 2025 – Aug 2026, $30–$40 | Refund (866-534-9986) | https://www.cpsc.gov/Recalls/2027/Kobayashi-Recalls-Rechargeable-Hand-Warmers-Due-to-Risk-of-Serious-Injury-from-Fire-and-Burn-Hazards |
| Gobi Heat (Dragon Gear) | 2026-10-01 / 27-009 | about 5,500 (+47 Canada) | **UT3053** | None reported | GobiHeat.com, Oct 2024 – Aug 2026, $20–$40 | Refund, or store credit of the price plus 20% | https://www.cpsc.gov/Recalls/2027/Gobi-Heat-Recalls-Rechargeable-Hand-Warmers-Due-to-Risk-of-Serious-Injury-from-Fire-and-Burn-Hazards |

**Story angles the data supports:**
* **The same model number appears under two brands.** Gobi Heat's recalled model is **UT3053**, the same number as OCOOPA's UT3 Lite. Retail listings map UT3053 to "UT3 Lite" ([Weak] e.g. https://online.challenger.sg/products/ocoopa-ut3053-bk_bk-plus-ut3-lite-plus-hand-warmer.oembed ; https://ca.manuals.plus/asin/B0FKGY7Y82) and UT3056 to "UT4 Young" ([Weak] https://www.newegg.com/ocoopa-ut3056-bk-bk-hand-warmerx2-black-x004bcinml/p/10C-00U9-00025).
* **Rebranded units are on sale.** Newegg lists **"NewAir"-branded UT3 Lite and UT3056 units** ([Weak] https://www.newegg.com/newair-ut3-lite/p/10C-00U9-00027 ; https://www.newegg.com/newair-ut3056-bu-bk/p/10C-00U9-00032). [Inference] **The model number, not the brand, is what to check.** This is the post's core service.
* **UL claims sit on recalled-brand listings.**
  * A Walmart OCOOPA listing title includes "UL Certified" ([Weak] https://www.walmart.com/ip/OCOOPA-Hand-Warmers-Rechargeable-2-Pack-Magnetic-Electric-Hand-Warmer-IP45-Water-Resistant-UL-Certified-Tech-Gift-for-Women-Men-Raynauds/8395967266). Retail listings also cite **UL file E535516** for OCOOPA UT3 Lite, UT4 Young and UT4 Urban ([Weak] search summary).
  * **Before publishing any UL statement,** look up E535516 in UL Product iQ (https://productiq.ulprospector.com, free account) and record what it actually covers: the battery cell, the pack, or the whole device, and which standard.
  * [Inference] A UL mark on a battery cell does not certify the finished warmer. Do not print that until UL's listing shows what it covers.
* **No other 2025–26 CPSC recalls.** My SaferProducts pull found no other rechargeable hand-warmer recalls in 2025–26 [Own data]. Re-run it weekly with `https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallDateStart=2026-01-01` and filter for "hand warmer".
* **Related CPSC actions to link from the post:**
  * 32 Degrees heated socks, recall 26-435, about 207,806 units, Costco only, 2026-04-23, 13 burns ([Official] https://www.cpsc.gov/Recalls/2026/32-Degrees-Recalls-Heated-Socks-Due-to-Burn-Hazard).
  * CPSC warnings on heated insoles sold on Amazon in 2026: Junsyoung, ZroeZroe, Meisinuo, COOWALK/COOWALI, METASONO ([Official] e.g. https://www.cpsc.gov/Warnings/2026/CPSC-Warns-Consumers-to-Stop-Using-COOWALK-COOWALI-Heated-Insoles-Immediately-Due-to-Risk-of-Serious-Burn-Injury-from-Fire-Hazard ; warning numbers 26-316, 26-464, 26-533, 26-612, 26-613 per snippets).
  * The Velazzio heated-gloves warning (2025-07-31: 137 overheating incidents, 119 burns; [Official] https://www.cpsc.gov/Warnings/2025/CPSC-Warns-Consumers-to-Immediately-Stop-Using-Velazzio-Thermo1-Battery-Heated-Gloves-Due-to-Burn-Hazard-Risk-of-Serious-Injury-Sold-on-Amazon-com).

**Picks (exact models; none appears in any 2025–26 CPSC recall or warning I found):**

| Role | Model | Maker claims | Non-Amazon price seen (snippet, 2026-11-23; recheck) |
|---|---|---|---|
| Best rechargeable, brand with a long US warranty history | **Zippo HeatBank 9s** (single unit; the 9s Plus is a variant) | "up to 9 hours", 6 heat levels, 1-year warranty ([Official] https://www.zippo.com/products/heatbank-9s-rechargeable-hand-warmer-box); battery listed as lithium polymer by REI and lithium-ion by Sportsman's; **no mAh or UL data found** | Academy $39.99 (https://www.academy.com/p/zippo-heatbank-9s-rechargeable-hand-warmer?sku=black); Zippo.com $59.95, sold out |
| Big-box pick (Target, Lowe's, Dick's, Ace) | **Thaw 2K Rechargeable Hand Warmer 2-pack** (and **Thaw 5K** for longer runtime) | 2K: 2000 mAh, "up to 4 hours", 120°F max, 1-year warranty (Target https://www.target.com/p/thaw-2pk-rechargeable-hand-warmers/-/A-95288258); 5K: about 3.5 h high to 7 h low (Dick's https://www.dickssportinggoods.com/p/thaw-5k-warmerlight-portable-and-rechargeable-hand-warmer-25thaucasu5kwrmrlgbeb/25thaucasu5kwrmrlgbeb). **Who makes Thaw: UNVERIFIED** | collect |
| Hottest in independent testing | **Unihand** rechargeable (exact model to confirm) | Outdoor Life called it "the hottest hand warmer in my test" ([Independent] https://www.outdoorlife.com/gear/best-rechargeable-hand-warmers/, 2026) | collect |
| No battery, lowest risk, budget | **HotHands Hand Warmers (air-activated, "up to 10 hours")**. The HotHands recall covers only the electric H163650 | about 135°F average, up to 10 h (Walmart listing) | Walmart 40-pair $23.99 (https://www.walmart.com/ip/10910809); 10-pair $7.48 |
| **Do not pick (show in the recall table instead)** | OCOOPA UT3 PRO / UT5 / UT4 Urban, etc. | Only list them as "not recalled" if the underside model number is confirmed outside the 7 recalled numbers **and** OCOOPA confirms it in writing. [Inference] After 1 death and 350 burns, leading with OCOOPA would undercut the post | — |

**Verified data to collect, with the public source for each:**
1. Recall model numbers, units, incidents and remedies: CPSC pages above, plus the SaferProducts API (weekly).
2. Health Canada recall of OCOOPA (cross-check of the model list): https://recalls-rappels.canada.ca/en/alert-recall/ocoopa-rechargeable-hand-warmers-recalled-due-fire-hazard
3. UL status of each pick: UL Product iQ by file number. Ask each maker for its UL file number by email and print "not provided" if it does not answer.
4. Battery mAh, Wh and max °F: maker manual or spec page (Zippo, Thaw, Unihand). Wh = mAh × V ÷ 1000.
5. Runtime by level: maker claim, plus Outdoor Life's measured results where available.
6. Flying rules: [Official] FAA PackSafe, https://www.faa.gov/hazmat/packsafe/airline-passengers-and-batteries ("100 watt hours (Wh) per battery"; spare lithium batteries carry-on only). The TSA has no specific hand-warmer entry in what I found: a TSA blog says devices with batteries ≤100 Wh can go in either bag ([Official] https://tsa.gov/blog/2020/06/17/staying-charged-go, 2020-06-17). **Print the FAA wording, not travel-blog wording.**
7. Disposal of recalled lithium units: CPSC remedy text ("do not put in the trash… household hazardous waste").
8. Cost math (verified numbers): HotHands at Walmart's 40-pair price works out to **$0.60 per pair, or about 6¢ per hour** at the "up to 10 hours" claim. A $39.99 HeatBank breaks even after about **67 disposable pairs** (it heats one hand; a two-hand comparison needs two units). Recompute with the prices on publish day.

**Table columns:** Model and printed model number · Recall status (CPSC no. and date, or "none found as of [date]") · UL file no. and what it covers (Product iQ, Y/N) · Battery mAh / Wh · Max temp claimed (°F) · Runtime high/low (maker) · Auto shut-off (Y/N) · Warranty · Price, store, date (non-Amazon) · Cost per hour vs disposables.

**Buy now or wait:**
* **Own a warmer already?** Check its model number before using it this season. If it is UT3053, UT3056, ZLS-118/118S/118D, H01, H01(PD) or H163650, stop using it now and claim the refund.
* **Buy a rechargeable now** if you use warmers on 20+ cold days a season, the maker answers the UL question, and the model is not on the list.
* **Buy disposables now** if you use them a few days a season. At about 6¢ per hour, the rechargeable takes about 67 uses to pay back.
* **Wait** on unknown brands that say "UL certified" without a file number.
* [Inference] After-Christmas clearance at Target, Dick's and Academy is likely. Do not promise it.

**10 FAQ (from autocomplete and recall coverage):**
1. Are rechargeable hand warmers safe?
2. Which rechargeable hand warmers were recalled in 2026?
3. How do I tell if my OCOOPA hand warmer is recalled?
4. Are HotHands recalled? (Only the electric model H163650 with the white logo.)
5. Are rechargeable hand warmers safe for kids?
6. Can rechargeable hand warmers catch fire or explode?
7. Can you take a rechargeable hand warmer on a plane?
8. How long do rechargeable hand warmers last (per charge and in years)?
9. Rechargeable vs disposable hand warmers: which is cheaper?
10. How do I dispose of a recalled hand warmer?

**Links to our posts:** heated blanket recalls; winter car emergency kit (warmers belong in it); jump starter sizes (lithium safety).

---

### 3.2 #2: Humidifiers: the real monthly cost of following the EPA's distilled-water advice (publish Dec 8–15)

**Why:**
* Highest winter demand: humidifier is on Slickdeals' January 2026 top-keyword list, and autocomplete shows "harmful", "mold" and "for winter".
* Incumbents test hard: RTINGS confirmed its picks in October 2026 (https://www.rtings.com/humidifier/reviews/best/humidifiers); CR's 2026 top midsized pick is the Dreo HM524S (paywalled, snippet); HouseFresh ran a tap-vs-distilled particle test.
* **None of them gives a dollar figure for the running cost** (distilled water + filters + electricity) next to the EPA rule.
* There is **no ENERGY STAR humidifier dataset**. The open-data catalog returned none [Own data, 2026-11-23]. There is also no current AHAM humidifier directory: only a 1996-era "AHAM Certified Rating Water Output" trademark (HU-1) appears ([Weak] https://trademarks.justia.com/750/71/…-75071433.html). So **output claims are maker-only**, and the post should say so.

**Target long-tail queries:** "do I need distilled water for my humidifier", "humidifier white dust harmful", "warm mist vs cool mist humidifier for winter", "cost to run a humidifier".

**Title (formula):** *"Use Distilled Water," Says the EPA: That's $26 to $130 a Month for One Popular 6-Liter Humidifier*
* The math, from the sources below:
  * Levoit LV600HH, cool mist 300 mL/h × 8 h/day → 0.63 gal/day → **$26/month** at $1.37/gal.
  * Warm mist 500 mL/h × 24 h → 3.17 gal/day → **$130/month**.
* Electricity adds up to **$12.20/month** at 280 W × 8 h/day × 18.16¢/kWh. 280 W is the rated maximum, so this is an upper bound.

**Facts already verified:**
* **EPA** ([Official] https://www.epa.gov/indoor-air-quality-iaq/use-and-care-home-humidifiers, "Last updated on April 29, 2026"; PDF version June 2022):
  * "Use water with low mineral content…"; bottled water "labeled 'distilled'" is listed first.
  * "Watch for the appearance of 'white dust,' which would indicate that minerals are not being removed."
  * "ultrasonic or impeller humidifiers are very efficient at dispersing minerals in tap water into the air."
  * "Clean portable humidifiers every third day"; empty, dry and refill daily.
  * "Do not humidify to indoor relative humidity levels exceeding 50 percent."
  * Health effects "are not fully understood."
  * The page gives **no 30% lower bound**. The 30–50% range is Mayo Clinic's: [Independent] https://mayoclinic.org/diseases-conditions/common-cold/in-depth/humidifiers/art-20048021 (verify the exact wording).
* **Mayo Clinic:** warm-mist and cool-mist humidifiers are equally effective; cool mist is safer around children (burn risk). [Independent] https://www.mayoclinic.org/healthy-lifestyle/adult-health/expert-answers/saliva/faq-20058199
* **RTINGS white-dust research** (updated 2026-05-13): tested Montreal tap water at about 120 ppm hardness, distilled water and a 1,000 ppm solution. It concludes evaporative units are "a safer, more health-conscious option" if you can't keep buying distilled water. [Independent] https://rtings.com/humidifier/learn/research/white-dust. The page body did not load for me. Read the PM2.5 numbers by hand before quoting them; the snippet's claim that "even distilled produced a lot of dust" may refer to the 1,000 ppm test (**UNVERIFIED**).
* **Electricity price:** U.S. residential average **18.16¢/kWh, August 2026** (17.57¢ Aug 2025), preliminary. [Official] EIA Electric Power Monthly Table 5.3, https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_3 (released 2026-10-23).
* **Distilled water:** Great Value 1 gal **$1.37** at Walmart ([Weak] snippet of https://www.walmart.com/ip/10315382; aislegopher shows $1.37 through 2026-06-04).
* **Recalls:** no humidifier recall in CPSC records from 2025-01-01 to 2026-11-23. The full-text search found no "humidif" anywhere [Own data].
  * A "Fridababy 3-in-1 humidifier recall, April 2026, 15,000 units" story appears only on two spam-laden sites (trueartists.com, mdi.us.com) and **is not in the CPSC database**. Treat it as false and do not repeat it.
  * Older official humidifier recalls: Hunter 2006; Research Products steam humidifiers 2023, https://www.cpsc.gov/recalls/2023/research-products-recalls-steam-humidifiers-due-to-fire-hazard

**Picks (exact models; one of each type, so the cost table means something):**

| Type | Model | Maker specs verified so far | Consumable |
|---|---|---|---|
| Hybrid ultrasonic (warm + cool) | **Levoit LV600HH** | 6 L tank; max warm 500 mL/h, max cool 300 mL/h; rated 280 W; 120 V ([Official] manual https://levoit.com/cdn/shop/files/07.02_ML_HOHIHC11EL_LV600HH_Hybrid-Ultrasonic-Humidifier-WEB.pdf) | Distilled water advised (check the manual's wording); optional demineralization cartridge (price: collect) |
| Smart ultrasonic (cool) | **Levoit Classic 300S** | collect from manual | Distilled water |
| Evaporative (wick) | **Honeywell HCM-350** (the "germ free" cool-moisture model, long cited as a Wirecutter pick, [Weak]) | Uses filter **HAC-504 / "Filter A"** ([Official] manual excerpt https://www.appliancefactoryparts.com/content/pdfs/168068-1.pdf); output and wick interval: collect from the manual's "Changing Filter" page (https://manualslib.com/manual/399371/Honeywell-Hcm-350-Germ-Free-Cool-Mist-Humidifier.html?page=4) | HAC-504 at Walmart $17.44 ([Weak] https://www.walmart.com/ip/220106921) |
| Evaporative, BIFL favourite | **Vornado Evap40** | collect | Vornado MD1-0002 wick (collect) |
| Warm mist (steam) | **Vicks V750 Warm Mist** | 1 gal tank, "up to 24 hours" (Vicks); **260 W per Direct Energy** ([Weak] https://apps.directenergy.com/learning-center/how-much-energy-humidifier-use). Confirm with the manual | No filter; scale cleaning |
| Optional premium (air washer) | **Venta LW15 Original** | filter-free, tap water (maker claim; [Weak] Reddit-derived summary) | Venta "Hygiene Additive" (collect) |

**Verified data to collect:**
1. For each model, from the maker manual (PDF): tank L, max output mL/h, rated W, whether tap water is OK, cleaning interval, filter part number and interval.
2. Store prices with dates: Walmart, Target, Home Depot and Best Buy, for the unit, its filter or cartridge, and distilled water.
3. EPA page (2026-04-29) and Mayo pages: quote them verbatim.
4. RTINGS white-dust PM2.5 numbers: read by hand.
5. EIA price: refresh on publish day (Table 5.3).
6. CPSC: re-run the SaferProducts query for "humidif" on publish day.
7. Optional own measurement: none needed. Every number is computed from public specs. Say so in the method box.

**Table columns:** Model · Type · Tank (L) · Max output (mL/h, maker) · Rated W · Tap water OK per manual? · Cleaning interval per manual vs EPA's "every third day" · Consumable (part, store, price, date, interval) · **$/month distilled water at 8 h/day** · **$/month electricity at 8 h/day (18.16¢)** · CPSC recall check (date checked).

**Buy now or wait:**
* **First:** buy a hygrometer (about $10; collect a Walmart or Target price) and measure. If indoor RH is already 30–50%, you don't need one. If it is above 50%, the EPA says don't humidify; link our queued dehumidifier post.
* **Buy now** if RH is under 30% and you have hard water. Choose evaporative to avoid the distilled-water bill.
* **Ultrasonic only if** you will buy distilled water. Show the $26/month line next to the price.
* [Inference] Big-box stores clear humidifiers in late Jan–Feb. Do not promise a price.

**10 FAQ:**
1. Warm mist or cool mist: which is better in winter?
2. Do I need distilled water in my humidifier?
3. Is humidifier white dust harmful?
4. How often should I clean my humidifier?
5. Can I use tap water in an evaporative humidifier?
6. What humidity should my house be in winter?
7. Can a humidifier cause mold?
8. Humidifier for a cough or congestion: does it help? (Cite Mayo; no medical claims.)
9. Where should I put a humidifier in the bedroom?
10. How much does it cost to run a humidifier per month?

**Links to our posts:** dehumidifiers (queued Dec); heated mattress pad vs electric blanket vs space heater cost per night (same cost-per-night method); shower filters (queued; hard-water angle).

---

### 3.3 #3: SAD / light-therapy lamps: what "10,000 lux" means at your actual sitting distance (publish Dec 29 – Jan 5)

**Why:**
* Demand peaks Nov–Jan; autocomplete shows "sad lamp 10000 lux", "10000 lux light box", "reddit" and "vitamin d".
* **This category has the best public measurement data of all the candidates,** and listings contradict it:
  * Retailers give the Carex Day-Light Classic Plus distance as 6 in, 10 in, 12–14 in or "up to 2 feet".
  * Verilux tells buyers its Lucent gives "10,000 LUX… between 6 and 24 inches away from your face" (Verilux answer on Best Buy Q&A).
  * Verilux also says most HappyLights give 10,000 lux at "no more than 24 inches" ([Vendor] https://verilux.com/pages/10000-lux).
  * Top Ten Reviews measured a HappyLight Full-Size reaching 10,000 lux only at **2.5 inches** ([Independent] https://www.toptenreviews.com/light-therapy-lamps-verilux-happylight-full-size-review).
* **Incumbents:**
  * Wirecutter picks the Carex Day-Light Elite (secondary snippets).
  * CNN Underscored picks a Verilux.
  * Many low-quality "tested" pages exist.
  * None that I found tabulates Yale's measured numbers against listing claims.

**Target long-tail queries:** "how far should a SAD lamp be from your face", "10,000 lux at what distance", "sad lamp 10000 lux".

**Title (formula):** *10,000-Lux SAD Lamps: Only X of Y Listings Say at What Distance, and Yale Measured 10,000 Lux at 12–13 Inches*
* **X/Y comes from our listing audit** (data item 4 below).
* Fallback with numbers already verified: *"10,000 Lux" SAD Lamps: In a 24-Device Test, Only 7 Light Boxes Hit It at the Maker's Own Distance*

**Facts already verified:**
* **Oldham MA, Oldham MB, Desan PH**, "Commercially Available Phototherapy Devices for Treatment of Depression: Physical Characteristics of Emitted Light", *Psychiatric Research and Clinical Practice* 2019;1(2):49–57. [Independent, peer-reviewed] https://pmc.ncbi.nlm.nih.gov/articles/PMC9175704
  * 24 devices from 12 makers were tested.
  * **7 light boxes or desk lamps reached ≥10,000 lux at the manufacturer-recommended distance; only 3 (X1, X4, X6) met all criteria** (≥7,000 lux at distance, ≥5,000 lux off-center, acceptable glare).
  * Quotes: "Some devices advertised as '10,000-lux' devices produced this intensity only at unreasonably close distances"; "The U.S. Food and Drug Administration has not regulated the sale of bright-light therapy devices"; "Clinicians should only recommend light boxes that specify the distance at which they produce 10,000 lux."
  * Expert to cite: **Paul H. Desan, MD, PhD**, Yale (co-author). Cite the paper, not invented quotes.
* **Yale Department of Psychiatry, "How Should I Obtain a Light Box?"** [Independent/academic] https://medicine.yale.edu/psychiatry/research/programs/clinical_people/winter/obtain (footer "Updated February 4, 2025").
  * Criteria: "at least 7,500 lux at a reasonable distance (=11 inches)"; at least 5,000 lux with the head moved 5 inches off-axis; non-glaring.
  * Measured results:

  | Device | Light area | Lux at distance |
  |---|---|---|
  | Carex Day-Light Classic Plus | about 13×15 in | **10,000 lux at 13"** |
  | Day-Light Sky DL2000 | about 13×10 in | **11,000 at 12"** |
  | Day-Light Classic DL930 | about 16×13 in | 10,900 at 12" (discontinued) |
  | BOXelite (now BOXelite OS) | 15×12 in | **7,000 at about 16"** |
  | SunTouch Plus | not stated | **about 10,000 at 14"** |
  | BuddyLux | about 21.5 in square | 10,000 at 11"; 7,000 at nearly 16" |
  | NorthStar 10,000 | 21.5×11 in | maker: 10,000 at 24", "close to" Yale's result |
  | SunRay II | 22×12.5 in | maker: 10,000 at 23", "close to" Yale's result |

  * Yale: "Four weeks should be long enough to determine if the therapy will work for you."
  * Bold caveat on the page: "Failure to be included in this listing does not indicate a product does not meet our specifications…"
* **Mayo Clinic:** light boxes are "not regulated by the FDA" for SAD; usual guidance is 10,000 lux at about **16–24 inches**; follow the maker's distance; some lamps made for skin disorders emit UV that can harm eyes; talk to a clinician first, especially with **bipolar disorder** or eye conditions (glaucoma, cataracts). [Independent] https://www.mayoclinic.org/diseases-conditions/seasonal-affective-disorder/in-depth/seasonal-affective-disorder-treatment/art-20048298 (record the page date when you read it).
* **Maker distance claims seen:**
  * Carex Classic Plus: 10,000 lux "from 12" to 14"" and "blocks 99.3% of UV" ([Official] https://carex.com/products/carex-day-light-classic-plus-light-therapy-sun-lamp, snippet).
  * Carex Day-Light Elite: 10,000 / 5,000 / 2,500 / 1,000 lux, 12–14" ([Weak] retailer snippets; Carex page https://carex.com/products/carex-day-light-elite-light-therapy-lamp, distance to confirm).
  * Verilux Lumi and Lucent: 6–24" (above).
* **CPSC:** no light-therapy-lamp recall in 2025–26 [Own data]. (The BlockBlueLight rechargeable lamp recall of 2025-02-13 is not a SAD lamp.) The safety angle here is eyes/UV and medical cautions, not recalls.

**Picks:**

| Role | Model | Why |
|---|---|---|
| Best overall, measured | **Carex Day-Light Classic Plus** | Yale measured 10,000 lux at 13" with a large panel. Check current availability; Yale says the maker stopped selling it direct |
| Desk-lamp format, measured | **Carex Day-Light Sky (DL2000)** | Yale measured 11,000 at 12"; passed all three criteria as X6 in the 2019 paper |
| Wirecutter's pick, verify | **Carex Day-Light Elite** | Pick per secondary sources; collect the maker's distance |
| Sits farther away, large | **NorthStar 10,000** (Northern Light Technologies) | Maker claims 10,000 at 24"; Yale calls it "close to" its result |
| Budget, measured | **BOXelite OS** (NatureBright/Uplift?, maker to confirm) | Yale measured 7,000 at about 16"; meets Yale's 7,500@11" bar? Check |
| Popular small lamp, the contrast case | **Verilux HappyLight Lucent** (VT22) and **HappyLight Luxe** (VT43) | Best sellers at Target, Best Buy and Staples. Show the maker's "6–24 in" claim beside the physics and the Top Ten Reviews measurement. **Not** a top pick unless a maker lux-at-distance table appears |

**Verified data to collect:**
1. Yale page and Oldham 2019: done (above). Re-read Yale on publish day.
2. Each maker's lux-at-distance, light-emitting area (sq in), UV filtering and color temperature: maker pages and manuals.
3. Prices with dates: Target, Walmart, Best Buy, Staples and Kohl's (Carex Classic Plus is on Kohl's and Walmart; Verilux on Target, Best Buy and Staples).
4. **Listing audit (creates the X of Y):** take the first 20 "10,000 lux light therapy lamp" results each at Target, Walmart and Best Buy on one dated day. Record whether the listing states a distance for 10,000 lux, and what distance. Report X/Y and the median stated distance. Screenshot and archive each listing.
5. Return windows (Yale's 4-week trial): Target, Walmart, Best Buy and Kohl's return policies, with page dates.
6. Medical cautions: Mayo pages (above). Optionally the NIMH SAD page (https://www.nimh.nih.gov/health/publications/seasonal-affective-disorder, not yet read).
7. "SAD lamp vitamin D" FAQ: find an official source that light boxes filter UV and therefore do not make vitamin D (Carex's "99.3% UV" claim is a start; **UNVERIFIED** as a medical statement).

**Table columns:** Model · Maker's 10,000-lux distance (in) · Independent measurement (Yale or Oldham, lux @ in) · Meets Yale's 7,500 lux @ 11" (Y / N / not tested) · Light area (sq in) · UV filter claim · Color temp (K) · Price, store, date · Return window (days) at that store.

**Buy now or wait:**
* **Buy now (late Dec – early Jan)** from a store whose return window covers Yale's 4-week trial. Talk to a clinician first if you have bipolar disorder or eye disease (Mayo).
* **Wait / skip** any lamp that does not state a distance for 10,000 lux, or states only "up to 24 inches". The Oldham paper says clinicians should recommend only lamps that state the distance.
* [Inference] Prices are steady; January sales are not reliable. Do not promise them.

**10 FAQ:**
1. Do SAD lamps actually work?
2. How far should a SAD lamp be from your face?
3. How long should I use a SAD lamp each day?
4. What time of day should I use a light therapy lamp?
5. Do I need 10,000 lux?
6. Can a SAD lamp damage your eyes / does it emit UV?
7. Is a SAD lamp FDA approved?
8. Can I use a SAD lamp if I have bipolar disorder?
9. Does a SAD lamp give you vitamin D?
10. Is a sunrise alarm clock the same as a SAD lamp?

**YMYL guardrails [Inference]:** cite Mayo, Yale and the journal only. Add a "talk to your clinician" box and a crisis-line link (988). Make no treatment claims beyond what Yale and Mayo state.

**Monetization caveat:** likely 1% (Health & Personal Care). This post earns qualifying sales and links (clinic pages and Reddit answers cite Yale-type tables) more than revenue. Check whether Carex, Verilux or NorthStar run direct affiliate programs (not researched).

---

## 4. Publishing calendar [Inference]

| Window | Post | Reason |
|---|---|---|
| Dec 1–5 | #1 Rechargeable hand warmers recall list + safest picks | Gift season plus the first cold snaps; recall news is fresh (Oct 1, Nov 19) |
| Dec 8–15 | #2 Humidifier running cost | Interest peaks Dec–Jan (Accio, Salehoo); pairs with the queued dehumidifier post |
| Dec 29 – Jan 5 | #3 SAD lamps lux-at-distance | Searches peak again in January; it needs a few days to be crawled before mid-January |
| Ongoing | Dreo DR-HSH015 recall note on the existing Dreo post (§0) | It names a now-recalled model |

---

## 5. Runner-ups (short sketches, in case a slot opens)

### 5.1 Heated vests (Apparel 4%)
* **Title idea:** *"Up to 10 Hours" Heated Vests: Ororo's Own 14°F Test Got 3.3 Hours on High*
* **Facts:**
  * Ororo's 4800 mAh / 7.4 V / **35.4 Wh** pack claims 3/6/10 h on high/medium/low ([Vendor] https://ororowear.com/products/mini-5k-battery-4800-mah).
  * Ororo's own cold test got 3.3 h high, 6.67 h medium and 11.2 h low at 14°F ([Vendor] https://www.ororowear.com/blogs/story/how-long-will-my-heated-apparel-stay-heated).
  * Milwaukee M12 claims 8/4/2 h, battery not included ([Weak]).
  * Ororo PD10K-Pro recall (§0); 32 Degrees socks recall; heated-insole warnings.
  * FAA 100 Wh rule: the "heated vest battery on airplane" query; a 35.4 Wh pack qualifies as a spare in the carry-on.
* **Incumbents:** Outdoor Life (https://www.outdoorlife.com/gear/best-heated-vest/), Bob Vila (2026-03-24), PopSci, Field & Stream.
* **Picks to consider:** Ororo Men's Classic heated vest, Venustas women's heated vest, Milwaukee M12 heated vest, DeWalt 20V heated vest.

### 5.2 Pet- and concrete-safe ice melt (3%)
* "Pet safe" is unregulated:
  * ASPCA: no labeling requirements ([Independent] https://www.aspca.org/news/it-safe-use-de-icers-around-your-dog).
  * Consumer Reports also advises skepticism.
* Calcium chloride is the most dangerous if ingested (ASPCA Pro).
* EPA Safer Choice certifies deicers, e.g. Safe Step Sure Paws ([Official] product finder https://www.epa.gov/saferchoice/products, search "deicers").
* Concrete: calcium and magnesium chloride above about 15% concentration form damaging calcium oxychloride; ammonium nitrate and sulfate and urea "chemically react" with concrete ([Independent] Alberta guide https://www.alberta.ca/system/files/custom_downloaded_images/tr-tb-001a.pdf ; Purdue JTRP).
* **Weakness:** low ticket price, heavy items, and Home Depot and Lowe's own the query.

### 5.3 Smart thermostats
* ENERGY STAR: "approximately 8% of heating and cooling bills or $50 per year" ([Official] https://www.energystar.gov/products/heating_cooling/smart_thermostats/smart_thermostat_faq). Certification needs a lower 95% confidence limit of at least 8% heating-runtime reduction.
* Nest's own claim is 10–12% heating ([Vendor] https://support.google.com/googlenest/answer/9247497).
* Dataset `7p2p-wkbf`: 121 certified models, updated 2026-11-13; top brands First Alert 15, Sensi 12, Resideo 11, Ecobee 7, Google Nest 4 [Own data].
* A good evergreen "8% of what?" calculator post, but the competition is heavy.

### 5.4 Weather radios
* NWS "cannot recommend one brand", but advises looking for the **Public Alert** and/or **NWR All Hazards** logos. Certified makers may also sell non-certified models ([Official] https://weather.gov/dsb/nwr_receivers).
* The standard is CTA-2009-B.
* **Angle:** "X of Y best-selling weather radios carry the Public Alert logo." Better as a section in a refreshed winter-car-kit or outage post.

---

## 6. Things to verify by hand before writing

* **Google Trends (US, 5 years):**
  * "rechargeable hand warmer", "hand warmer recall";
  * "humidifier", "humidifier white dust";
  * "sad lamp", "light therapy lamp";
  * "heated vest".
  * Confirm the Nov–Jan peaks and the weeks they fall in. Published Trends citations were thin (§1.1).
* **Reddit threads** listed in §1.3.
* **UL Product iQ:** what file E535516 covers, and UL status for the Zippo HeatBank 9s, Thaw 2K/5K and Unihand.
* **Amazon category and commission rate** for each pick (Associates link builder or the first earnings report).
* **Manuals:** Honeywell HCM-350 output and wick interval; Levoit Classic 300S and Vornado Evap40 specs; Vicks V750 wattage from the manual.
* **RTINGS white-dust PM2.5 figures** (page body did not load).
* **All store prices,** re-read on publish day with dates.
* **Who makes Thaw;** the Unihand exact model; whether OCOOPA UT3 PRO's printed model number is outside the recall list.
