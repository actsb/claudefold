# Research brief 3: price, electricity data, channels (heated pad vs blanket vs space heater)
Prepared 2026-11-09. Rule followed: no Amazon prices/ratings/reviews, no price trackers. Anything not backed by a fetched or searched source is marked UNVERIFIED.
Method note: WebFetch of EIA/CPSC pages was read through a summarizer; spot rows were re-fetched verbatim and matched. Walmart, Kohl's, Target, Best Buy and Home Depot product pages blocked fetching (bot wall / 403), so retail prices below are search-result snippets, mostly undated.

## 1. EIA electricity data
- Source page: EIA Electric Power Monthly, Table 5.6.A "Average Price of Electricity to Ultimate Customers by End-Use Sector, by State, August 2026 and 2025 (Cents per Kilowatthour)". Data month August 2026 (preliminary), release date Oct 23, 2026, next release Nov 24, 2026. Fetched 2026-11-09.
  URL: https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a
- US residential average, Aug 2026: 18.16 c/kWh (Aug 2025: 17.57). Raw row verified: "U.S. Total: 18.16 17.57 ...".
- Note: August is a summer month; a winter heating-season price may differ. Annual averages come from the STEO below.
- STEO: October 2026 STEO (released Oct 6, 2026) shows residential price 18.2 c/kWh for 2026 and 18.7 c/kWh for 2027. URL: https://www.eia.gov/outlooks/steo/report/elec_coal_renew.php (fetched 2026-11-09; via summarizer, the page did not quote the number in a sentence, so confirm in the STEO table before printing). Next STEO due Nov 10, 2026. Earlier: May 2026 STEO 18.27 for 2026 (secondary report, UNVERIFIED primary).
- Lowest state Aug 2026: Nevada 12.72. Highest: Hawaii 47.18. Highest on mainland: Maine 32.11, Massachusetts 30.48, California 29.75. Lowest others: Louisiana 12.87, Utah 13.31, North Dakota 13.31, Idaho 13.37, Tennessee 13.42.
- Cross-check: American Default (secondary) also lists Hawaii 47.18, Maine 32.11, Mass. 30.48, California 29.75, US 18.16. https://americandefault.org/affordability/electricity/
- Electric-heat share: NOT found for main heating fuel. Only: 26% of US homes were all-electric in RECS 2020 (secondary summary), and "more than half of US households used natural gas for space heating" (EIA Today in Energy id=55940). https://www.eia.gov/todayinenergy/detail.php?id=55940 . State heating-fuel tables exist: https://www.eia.gov/consumption/residential/data/2020/state/pdf/State%20Space%20Heating%20Fuels.pdf (not read). Treat national electric-heat share as UNVERIFIED.

### State table, residential cents/kWh, EIA Table 5.6.A, August 2026 (prelim) and August 2025
```csv
state,aug2026_c_per_kwh,aug2025_c_per_kwh
Connecticut,24.51,30.17
Maine,32.11,28.14
Massachusetts,30.48,30.55
New Hampshire,27.64,24.44
Rhode Island,28.18,26.53
Vermont,23.84,22.10
New Jersey,24.61,24.70
New York,28.65,26.64
Pennsylvania,21.77,19.93
Illinois,19.32,18.03
Indiana,17.02,16.21
Michigan,22.99,20.73
Ohio,19.38,17.55
Wisconsin,19.41,18.44
Iowa,17.06,15.48
Kansas,15.47,14.65
Minnesota,17.20,16.89
Missouri,16.02,15.32
Nebraska,13.54,12.80
North Dakota,13.31,12.97
South Dakota,15.15,13.90
Delaware,18.70,16.85
District of Columbia,25.98,23.18
Florida,14.99,15.33
Georgia,15.90,15.55
Maryland,21.40,19.89
North Carolina,14.95,14.59
South Carolina,15.76,15.16
Virginia,17.64,15.85
West Virginia,16.31,15.62
Alabama,16.33,16.26
Kentucky,13.80,13.10
Mississippi,14.43,13.61
Tennessee,13.42,13.09
Arkansas,14.37,13.33
Louisiana,12.87,12.55
Oklahoma,14.82,14.42
Texas,15.91,15.40
Arizona,15.05,15.09
Colorado,17.17,16.21
Idaho,13.37,12.08
Montana,15.57,14.29
Nevada,12.72,12.54
New Mexico,16.51,15.98
Utah,13.31,13.62
Wyoming,14.43,14.33
California,29.75,30.92
Oregon,15.92,15.85
Washington,14.63,13.65
Alaska,29.41,27.79
Hawaii,47.18,38.53
US Total,18.16,17.57
```
(51 state/DC rows + US total. Caution: Connecticut dropping 30.17 to 24.51 year over year looks odd but the raw row was re-fetched and matches; EIA also issued a revision notice for Table 5.6.A earlier in 2026, https://www.eia.gov/electricity/monthly/includes/revision-notice.php . Preliminary data can be revised on Nov 24.)

### Cost math (formula, mine): cost = watts/1000 x hours x duty cycle x c/kWh
At the US 18.16 c/kWh: 1,500 W running continuously 8 h = 12 kWh = $2.18. At 50% duty cycle = 6 kWh = $1.09 (duty cycle is an assumption, see section 3). 100 W throw x 8 h = 0.8 kWh = 14.5 c (but see auto-off). 120 W pad x 8 h = 0.96 kWh = 17.4 c at full power (pads run less after warm-up; UNVERIFIED).
Hawaii 47.18: 1,500 W x 8 h = $5.66. Nevada 12.72: $1.53.

## 2. Retail prices and channels (non-Amazon)
Pages named exact models only where the snippet did. Date seen = date of this search, 2026-11-09, unless the source dated itself. Snippets can be stale; re-check before printing a price.

### Dreo Atom One (1500W PTC ceramic)
- Maker store: https://www.dreo.com/products/dreo-atom-one-space-heater . Fetched 2026-11-09: sale price $49.99, regular price not shown; page mentions a Black Friday "up to 50% off" sale; codes not combinable. A search snippet of the same page showed $41.00 (18% off, auto-applied code), undated. Specs on page: 1000-1500 W, digital thermostat 41-95 F, 1-12 h off timer. Warranty 12 months; 30-day money-back on undamaged items, buyer pays return shipping on non-defective returns. Model number not stated on page (image filenames hint "DR-HSH004", UNVERIFIED).
- Walmart/Target/Best Buy/Home Depot/Kohl's/Costco: NO listing naming the Atom One found. Walmart pages seen were other Dreo 1500W heaters (e.g. $39.99 was $59.99, undated). Do not use as an Atom One button; link to dreo.com plus UNVERIFIED second store.
- RECALL CAUTION: see section 4, Dreo DR-HSH015 recalled Oct 29, 2026 (a different model, not Atom One as far as sources say).

### Sunbeam queen heated mattress pad
- Walmart, Sunbeam Restful Quilted queen, 12 heat settings, 12 h auto-off: $59.87 (was $79.87) in search snippet, undated. https://www.walmart.com/ip/Sunbeam-Restful-Heated-Mattress-Pad-12-Heat-Settings-Full-White/1930837943 (that URL is the Full size; the queen listing ID was not confirmed, UNVERIFIED).
- Walmart Sunbeam Wi-Fi connected queen: from $77.99 (range $77.99-$89.90), wattage listed 120 W, undated. https://www.walmart.com/ip/Sunbeam-WiFi-Connected-Warm-Thermal-Heated-Mattress-Pad-Queen-White/908885838
- Walmart Sunbeam Premium Quilted queen $129.99 (snippet, undated). https://www.walmart.com/ip/Sunbeam-Premium-Luxury-Quilted-Electric-Heated-Mattress-Pad-Queen-Size/269083398
- Kohl's Sunbeam queen Wi-Fi dual-controller: listing exists, price not shown. https://www.kohls.com/product/prd-6310913/sunbeam-queen-size-electric-mattress-pad-with-dual-digital-controller-and-wi-fi-connection.jsp
- Target Sunbeam Restful King listing (not queen): https://target.com/p/king-restful-quilted-electric-heated-mattress-pad-white-sunbeam/-/A-89863070
- sunbeam.com product page: not found. Warranty: listings repeatedly say 5-year limited manufacturer warranty (retailer listings, model-dependent; one Overstock listing says 60 days). Sunbeam's own return policy: UNVERIFIED.

### Serta / Beautyrest / Biddeford queen heated pads (Walmart snippets, undated)
- Biddeford Quilted Electric Heated Mattress Pad, Queen, digital controller: https://www.walmart.com/ip/2966177773 (price ~$55.99 per snippet, UNVERIFIED).
- Serta Waterproof Heated Mattress Pad Queen: https://www.walmart.com/ip/Serta-Waterproof-Heated-Mattress-Pad-Queen-White/2665562036 ($124.99 per snippet; another Serta waterproof queen $38.70 sponsored).
- Beautyrest Heated Microfiber Mattress Pad with 3M Scotchgard, Queen: https://www.walmart.com/ip/48333216 (price not shown). Kohl's Beautyrest/related: https://www.kohls.com/product/prd-3535307/product.jsp (unverified identity).

### Bedsure
- 50x60 heated throw: no bedsure.com or non-Amazon store listing found for the 50x60 grey. Roughly $37-$45 on Amazon deals (not usable per rules) vs list ~$69. A Newegg listing showed $89.99 (may be a different model); Kohl's page https://www.kohls.com/product/prd-8001218/target= showed a Bedsure sherpa throw at $119.99 (different product). Target carries Bedsure blankets, e.g. queen solid flannel $54.99 (reg $109.98, seller Bedsure), https://www.target.com/p/-/A-94187691 , also https://target.com/p/heating-electric-blanket-solid-flannel-throw-size-olive-green-bedsure/-/A-94187693 (throw size, price not shown). Snippets undated.
- Bedsure heated mattress pad queen 60x80 seen at $68.39 on dealmoon, deal expired. https://www.dealmoon.com/en/68-bedsure-heated-mattress-pad-queen-60x80/5746459.html
- Returns/warranty: Newegg listing shows 30-day return; one Target listing 90-day return/90-day limited warranty. Bedsure's own policy page not read: UNVERIFIED. Bedsure maker site: https://bedsurehome.com

### Oil-filled radiators
- DeLonghi Comfort Temp KH390715CM-6A: delonghi.com US lists $89.95 but "temporarily out of stock" (via search snippet). https://www.delonghi.com/en-us/comfort-temp-full-room-radiant-heater-kh390715cm/p/KH390715CM-6A (fetch returned 404 on my attempt; page may have moved). 1500 W, three heat settings, adjustable thermostat (retailer listings). Warranty conflicting: 1-year vs 3-year (UNVERIFIED). US page said 30-day returns. Last verified deal: TRH0715-6A $59.95 in Jan 2024 (Slickdeals, expired). Kohl's: https://www.kohls.com/product/prd-6837739/delonghi-comfort-temp-full-room-radiant-heater.jsp (price not shown). Best Buy US listing seen was a different DeLonghi model (Dragon Digital $29.99 clearance, unverified date).
- Pelonis 1500W oil-filled (maker store): https://us.pelonis.com/shop/1500-watt-oil-filled-radiant-electric-space-heater-with-thermostat/ (503 on fetch; price unread). Walmart browse showed Pelonis PHO15A2AGW white at $118.44 (undated; high). Slickdeals Jan 27, 2026 listed it at $44 (Amazon, not usable).

### Black Friday 2025 and 2026
- BF 2025 (Walmart, via Bob Vila roundup, https://www.bobvila.com/reviews/black-friday-cyber-monday-space-heater-deal-2025): Dreo 1500W tilt heater $38.99 (was $73.99, about 47% off); Dreo 1500W with remote $33.99 (was $39.99, about 15% off). Slickdeals Walmart+ early access Dreo 1500W $29.99 vs $60 list (50%) https://slickdeals.net/f/18866413-walmart-early-access-dreo-space-heater-1500w-portable-heater-29-99 . These are not confirmed Atom One. Target Dreo deal: none found.
- Bedsure press release: heated mattress pads up to 30% off BF/CM 2025 (company claim). Bedsure BF guide: https://bedsurehome.com/blogs/bedsure/black-friday-bedding-deals-guide . No dated BF 2025 prices for Sunbeam/Kohl's found. Typical depth observed: 15-50% on space heaters, up to 30% on Bedsure pads; Dreo's own page says up to 50%.
- BF 2026: Black Friday is Nov 27, 2026. Digital Citizen (low-authority, secondary) reports Best Buy Doorbusters Nov 19-28, Walmart Nov 23-28, Target early sale Nov 5-7. No retailer-newsroom confirmation. https://www.digitalcitizen.life/black-friday-2026-sale-dates-walmart-best-buy-target-amazon-costco/ . Dreo.com already advertises a Black Friday sale (see above).

## 3. Usage facts
- Resistance heaters are 100% efficient per DOE (via Missouri DNR summary of DOE guidance, https://dnr.mo.gov/print/document-search/pub2849); no primary Energy.gov page on space-heater cycling was fetched (energy.gov/energysaver/space-heaters etc. returned 404).
- Duty cycle: no Energy.gov, manufacturer or extension source found giving a % for space heaters or oil radiators. Blog claims (30-50% reduction with thermostat; "about 50% duty cycle" for oil radiators) are UNVERIFIED. Recommend presenting full-power as the ceiling and showing a labeled "if it cycles to half" scenario, flagged as our assumption.
- Wattages: Dreo Atom One 1000-1500 W (dreo.com). DeLonghi KH390715CM 1500 W (retailer listings). Pelonis 1500 W (product title). Bedsure 50x60 throw 100 W, 3-hour auto shut-off, 6 heat levels, 4 timer settings (retailer/desertcart listings; maker page unread). Sunbeam Wi-Fi queen pad 120 W (Walmart listing). Other pads/blankets: UNVERIFIED; generic ranges 60-150 W cited by UK sources only.
- Preheat: Sunbeam preheat on some models, up to 30 min (Hunker, https://www.hunker.com/13409542/what-does-the-preheat-setting-on-a-sunbeam-mattress-pad-do ), not all models. Pad auto-off 12 h on the Restful (Walmart). Bedsure throw 3 h auto-off means it cannot run a full 8 h night without restarting.
- No maker/ENERGY STAR/DOE kWh-per-night figure for heated blankets found. DOE only gives the formula kWh = W x h / 1000 (https://www1.eere.energy.gov/education/pdfs/efficiency_wattdoesitcost.pdf).
- Thermostat setback (alternative): Energy.gov says turning the thermostat back 7-10 F for 8 h a day from its normal setting can save up to about 10% a year on heating and cooling. https://www.energy.gov/save/home-upgrades (also Renters page https://www.energy.gov/save/renters and 2022 guide https://www.energy.gov/sites/default/files/2022-08/energy-saver-guide-2022.pdf ). Heat-pump caveat: use a programmable/smart thermostat. The "1% per degree" rule is secondary and UNVERIFIED.

## 4. Recall check (CPSC, last 2 years: Nov 2024 to Nov 2026)
- Dreo: RECALL. DREO DR-HSH015 ceramic space heaters (black, ~11.5 x 13 in, remote; also sold as Whole-Room Heater 715), recall no. 27-054, Oct 29, 2026; ~338,800 US units; 17 ignition reports, 3 property damage, 1 hand burn; made Apr 2025-Jan 2026; sold Sept 2025-Oct 2026 at Costco, Dreo.com, BestBuy.com, Kohls.com, Lowes.com, HomeDepot.com, QVC.com for $70-$110. Atom One is not named; news says Dreo states other models are not recalled (secondary). Verify Atom One's model code on the box. https://cpsc.gov/Recalls/2027/DREO-Recalls-DR-HSH015-Space-Heaters-Due-to-Fire-and-Burn-Hazards (CPSC URL contains "2027"; it is the page returned by search and fetch).
- Sunbeam: only the Mar 2023 recall of queen heated blanket model 32810027 (distributor Star Elite, ~43,000 units, recall 23-157), outside 2 years. https://www.cpsc.gov/Recalls/2023/Sunbeam-Heated-Blankets-Recalled-Due-to-Burn-and-Fire-Hazards-Distributed-by-Star-Elite
- Bedsure (Bedshe International): Mar 9, 2023 recall 23-735, ~350,000 blankets/pads, controller fire hazard, models BS-HB5060, BS-HB6284, BS-HB7284, BS-LV0A, BS-HP2422, BS-HP1224, BS-HP2433; remedy refund at https://safety.bedsurehome.com/ . Outside 2 years but the 50x60 throw model BS-HB5060 is the one recalled; the current-production 50x60 throw status is UNVERIFIED, flag this in copy: check model/date code. Source: https://www.dhses.ny.gov/node/14731
- Serta, Beautyrest, Biddeford, DeLonghi, Pelonis: no recall in the last 2 years found (old ones: Biddeford 2001 blanket plug, DeLonghi 1991/1998, Pelonis 1989). Absence of search hits is not proof; CPSC database not queried directly.
- Other heated-blanket actions in the window (not our brands, show category risk): JKMAX ~195,000 heated blankets/pads, recall 26-778, sold on Amazon Sept 2022-July 2026, 577 reports, 53 burn injuries; Melinora warning no. 26-616, Jul 16, 2026 (~700 units, Amazon, manufacturer unresponsive); Octrot ~178,000 blankets (2026, secondary report). https://www.cpsc.gov/Warnings/2026/CPSC-Warns-Consumers-to-Stop-Using-Melinora-Electric-Heated-Blankets-Immediately-Due-to-Risk-of-Serious-Injury-from-Burn-and-Fire-Hazards

## 5. Look-alikes / counterfeits
- No source found that documents counterfeit or look-alike heated blankets on Temu/Shein specifically. Documented adjacent facts: Which? (UK) found Temu/TikTok Shop electric heaters with poor wiring, illegal plug and fake fuse (https://www.which.co.uk/news/article/electric-heaters-temu-tiktok-shop-a6c744h4Olcl); Channel 4 Dispatches found altered safety-certificate images on Temu listings (UK); UL Solutions notice 23PN-28 (Mar 2024) on unauthorized UL marks on desktop heaters sold by e-commerce sellers (https://www.ul.com/news/ul-solutions-warns-unauthorized-ul-marks-desktop-heaters); CPSC commissioners called for a Shein/Temu investigation (Sept 2024). The Melinora and JKMAX actions show unknown-brand marketplace blankets are the recall pattern, with sellers unresponsive. Suggest wording: buy from the maker or a major retailer, check ETL/UL mark and model number; do not claim counterfeits exist for blankets.
- Returns/warranties summary: Dreo 12-month warranty, 30-day returns (buyer pays non-defective return shipping). Sunbeam pads 5-year limited per listings (UNVERIFIED at maker). DeLonghi 30-day returns on US store, warranty 1 vs 3 years conflicting. Bedsure 30-90 days varies by seller. Pelonis: not read.
