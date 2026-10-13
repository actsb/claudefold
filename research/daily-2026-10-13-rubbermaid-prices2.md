# Rubbermaid Brilliance 10-piece Tritan: price + channels brief, round 2
Compiled 2026-10-13. Supersedes the weak parts of `research/daily-2026-10-11-rubbermaid-prices.md`.
HARD RULE: no Amazon price appears as a number here. Amazon appears only as a percent-off label from a non-Amazon deal post (Slickdeals / Hip2Save), with the post date. No Amazon ratings, counts or quotes.

## Method (what was actually opened)
Bash curl with browser User-Agent, -L -m 30. Status per page:
- OPENED: homedepot.com product page (200, price + return window in page data), target.com 22-pc product page (200, title/rating only, price is JS-loaded), slickdeals.net posts and search (200), hip2save.com (200).
- BLOCKED, so UNVERIFIED: walmart.com (bot wall "Robot or human?"), rubbermaid.com (Cloudflare 403, every path incl. warranty/FAQ), oxo.com (403), pyrexhome.com (429), espressoparts.com (429), kroger.com (connection failed, no response), costco.com (search page returned no products; 2 tried product URLs 404), customerservice.costco.com (401), target.com help/returns (opened but no policy text in static HTML). newellbrands.com has no warranty text. rubbermaidus.com is NOT the official store (third-party looking site), ignored. Wayback has no snapshot of the rubbermaid.com warranty page.
- Slickdeals "% off" is the poster's comparison price vs the deal price, not an official MSRP. Treat as "deal depth", not list price.
- Correction to the 10-11 brief: the "Walmart $17.99, 2022" row was an Amazon post (Slickdeals 16285192 family; the Slickdeals post 15898450 dated 2022-07-11 is an Amazon listing). Drop it. The 2025-07 "Target Circle $17.59" row (Slickdeals 18426148, 2025-07-05) is also an Amazon post, 40% off. Drop it. Likewise the OXO 10-pc Slickdeals post is an Amazon listing (22% off, 2026-02-01): percent only.

## 1. Dated non-Amazon prices
"Piece" = each container and each lid counted separately. "Container" = piece count / 2.
| Retailer | Item | Price | Date | Per piece | Per container | Source / status |
|---|---|---|---|---|---|---|
| Walmart (4-pack, per-set math by deal post) | Brilliance 10-pc StainShield, 5 containers + 5 lids (2x1.3-cup, 2x3.2-cup, 1x4.7-cup) | $67.39 for 4 sets = $16.85 per set (27% off per post) | 2025-12-24 | $1.69 | $3.37 | https://slickdeals.net/f/19015273 ; page shows Walmart rating 4.6 of 5, 2,890 reviews on that date. Buying 4 sets is not a single-set price. |
| Walmart | 18-pc Brilliance Clear Tritan leak-proof | $28.32 (33% off per post) | 2026-02-13 | $1.57 | $3.15 (9 containers assumed) | https://slickdeals.net/f/19204945 |
| Walmart | 5-pc StainShield | $19.80 (13% off) | 2025-11-02 | $1.98 | $3.96 | https://slickdeals.net/f/18759028 |
| Walmart | 10-pc single set | $19.82 | UNVERIFIED (undated; Walmart blocked) | $1.98 | $3.96 | https://www.walmart.com/ip/seort/2850383295 |
| Target | 12-pc Brilliance, 3 colors | $19.99 (50% off) | 2026-02-12 | $1.67 | $3.33 | https://slickdeals.net/f/19202995 (expired) |
| Target | Rubbermaid Brilliance 10-pc GLASS (2x1.3-cup, 2x3.2-cup, 1x8-cup + lids; oven-safe to 450F per Hip2Save) | $28.49, reg. $54.99 (47% off); Circle card +5% | 2026-09-09 (Slickdeals) and 2026-09-15 (Hip2Save) | $2.85 | $5.70 | https://slickdeals.net/f/19992999 ; https://hip2save.com/deals/target-rubbermaid-brilliance/ (Kohl's compare price $62.99 per Hip2Save) |
| Target | 22-pc plastic set page (fetched 2026-10-13) | price not in static page | 2026-10-13 | n/a | n/a | https://www.target.com/p/rubbermaid-brilliance-22pc-plastic-food-storage-container-set-clear/-/A-88450135 ; title says "1 Year Warranty"; Target rating 4.5 of 5, 1,585 reviews on the fetch date |
| Home Depot | Brilliance 20-pc (Model 1990616, Internet #310354384) | $50.65 online; "$25 off" only with a new Home Depot card; price valid until 2026-10-13 | 2026-10-13 | $2.53 | $5.07 | https://www.homedepot.com/p/Rubbermaid-Brilliance-20-Piece-Food-Storage-Container-Set-1990616/310354384 ; Home Depot rating 4.4 of 5, 1,242 reviews. Local store prices may differ. Home Depot has no 10-pc page found. |
| Costco | 16-pc Brilliance (8 containers + 8 lids) | $29.97 (member post; no list shown) | 2024-12-14 | $1.87 | $3.75 | https://slickdeals.net/f/17991816 ; current Costco price not retrievable, UNVERIFIED |
| MorningSave | 16-pc Brilliance | $29.99 + shipping code (53% off) | 2025-01-07 | $1.87 | $3.75 | https://slickdeals.net/f/18042876 |
| Kroger | none | n/a | n/a | n/a | n/a | UNVERIFIED (site unreachable) |
| Rubbermaid / Newell store | none | n/a | n/a | n/a | n/a | UNVERIFIED (Cloudflare 403) |

Not retrievable at all: any 10-pc Tritan price at Home Depot, Costco, Kroger or the brand store. The only dated single-set 10-pc non-Amazon number is the Walmart 4-pack math ($16.85 per set, 2025-12-24). That is a better anchor than the old 2020/2023 rows.

## 2. Comparison sets, cost per piece and per container
| Set | Price (non-Amazon) | Date | Pieces | Containers | Per piece | Per container |
|---|---|---|---|---|---|---|
| Rubbermaid Brilliance 10-pc Tritan (Walmart 4-pack math) | $16.85 | 2025-12-24 | 10 | 5 | $1.69 | $3.37 |
| Rubbermaid Brilliance 12-pc (Target sale) | $19.99 | 2026-02-12 | 12 | 6 | $1.67 | $3.33 |
| Rubbermaid Brilliance 18-pc (Walmart sale) | $28.32 | 2026-02-13 | 18 | 9 | $1.57 | $3.15 |
| Rubbermaid Brilliance 20-pc (Home Depot, regular) | $50.65 | 2026-10-13 | 20 | 10 | $2.53 | $5.07 |
| Rubbermaid Brilliance 16-pc (Costco, member) | $29.97 | 2024-12-14 | 16 | 8 | $1.87 | $3.75 |
| Rubbermaid Brilliance 10-pc glass (Target sale) | $28.49 | 2026-09-09 | 10 | 5 | $2.85 | $5.70 |
| Pyrex 18-pc glass (Target, Slickdeals 17346111) | $29.99 | 2024-03-11 | 18 | 9 | $1.67 | $3.33 |
| Pyrex 18-pc glass (Target, Circle member, 48% off, Slickdeals 17412294) | $23.00 | 2024-04-07 | 18 | 9 | $1.28 | $2.56 |
| Snapware Pyrex 18-pc (Costco in-store, 44% off, Slickdeals 17036899) | $20.00 | 2023-11-04 | 18 | 9 | $1.11 | $2.22 |
| OXO Good Grips POP 10-pc | $112.99 (Espresso Parts, undated; page now 429) | UNVERIFIED | 10 containers + lids (lids bundled, 20 parts) | 10 | $5.65 per part if lids counted, $11.30 if not | $11.30 |

Notes:
- Pyrex 18-pc is assumed to be 9 containers + 9 lids (standard for that set; the posts say "18-piece"). Pyrex glass sets are the dated lows from 2023-24; I found no 2026 non-Amazon Pyrex price. Treat as "what it has sold for", UNVERIFIED for today.
- Pyrex is glass (oven-safe, heavier, snap-on lids that are less leak-proof than latched ones, per product type, not tested here). Rubbermaid Tritan is plastic and lighter.
- OXO POP is a different product: airtight dry-goods canisters (flour, cereal, pasta), 10 containers in seven sizes per the maker's listing as quoted on Slickdeals. It is not leak-proof for liquids. The 10-11 brief said "about 7 containers": that was wrong, it is 10. At $11.30 per container it costs about 3.4x the Rubbermaid sale rate; at the Amazon-post 22% off it would still be in the same class (percent only, no Amazon dollars).
- Rubbermaid sale prices per piece ($1.57 to $1.69) are within about 0.1 to 0.6 of Pyrex Target-sale prices ($1.28 to $1.67) and above the Costco Pyrex low ($1.11). Rubbermaid regular price at Home Depot ($2.53) is about 50% higher than its sale rate.

## 3. Warranty and returns
- OFFICIAL rubbermaid.com warranty page: could not be opened (Cloudflare 403 on all paths; no Wayback copy). Warranty terms from the brand: UNVERIFIED. Do not state "lifetime" as fact.
- Target product page (fetched 2026-10-13), 22-pc Brilliance: page title says "1 Year Warranty". This is the only retailer-page warranty text I could open. It conflicts with the earlier "lifetime" and "120 day" claims, which were second-hand.
- Home Depot product page (2026-10-13): "Free & Easy Returns In Store or Online. Return this item within 90 days of purchase."
- Target return window: help page opened but the policy text did not load. UNVERIFIED.
- Walmart (90-day, earlier brief), Costco (member satisfaction guarantee), Kroger: UNVERIFIED (blocked).
- Replacement lids: not rechecked; no new facts.

## 4. Deal depth by event (percent only; Slickdeals/Hip2Save posts, dates as shown)
Amazon items appear with their post's "% off" label only.
Prime Day / July window:
- 2024-07-16: 22-pc Brilliance set, 50% off (Slickdeals 17626509; also 50% off the same day in a non-Prime "free shipping" post 2024-06-22, 17573724).
- 2025-06-30 and 2025-07-05: 10-pc Tritan set, 40% off (Slickdeals 18412504 and 18426148). Same week: 4-pack 4.7-cup 40% off.
- 2026-06-23: 10-pc Tritan set, 22% off (Slickdeals 19666284). 2026-07-12: 10-pc Tritan set, 19% off (Slickdeals 19750659). Prime Day 2026 exact dates not confirmed.
Prime Big Deal Days / October:
- 2025-10-05 to 10-07: 5-pack 2-compartment 36% off; 5-pack 3.2-cup 30% off (Prime); 6-pc round 46% off; 10-pc 1.3-cup 34% off (Slickdeals 18664213, 18666484, 18666565, 18673705).
- 2026-09-26 to 10-06: 5-pack 3.2-cup 25% off, 9-pk glass 25% off, 14-pc 30% off (Slickdeals 20066247, 20066112, 20070273, 20105925). 10-pc set not posted in that window.
Black Friday / Cyber Week:
- 2025-11-09: 10-pc leak-proof set, 40% off (Slickdeals 18784723). 2025-11-20: 14-pc 40% off. 2025-11-22 (Walmart): 9.6-cup container 52% off (18850249). 2025-11-02 (Walmart): 5-pc StainShield 13% off. 2025-11-27: no 10-pc post found.
- 2023-11-28: 10-pc set, 33% off (Slickdeals 17121496).
Non-Amazon retailer markdowns: Target 12-pc 50% off (2026-02-12); Target glass 10-pc 47% off (2026-09-09); Walmart 18-pc 33% off (2026-02-13); Walmart 10-pc 4-pack 27% off (2025-12-24); Kohl's 7-pc pantry 43% off (2026-06-30); eBay 12-pc 60% off (2026-05-13).
Pattern: the 10-pc set has been posted at 40% off in mid-2025 and Nov 2025, but only 19 to 22% off in June-July 2026. Event discounts across Brilliance run 19 to 46% for Prime events and 27 to 50% at Target/Walmart. Use "20 to 40% off" as the band for the 10-pc, stating that 2026 summer was shallower than 2025.

## 5. When Amazon is not the cheapest (directional, no Amazon dollars compared)
- Per piece, the best dated non-Amazon Rubbermaid rates are the Walmart 18-pc ($1.57, Feb 2026) and Target 12-pc ($1.67, Feb 2026), lower than the Walmart 10-pc rate ($1.69). Larger sets are cheaper per piece.
- Pyrex 18-pc glass at Target/Costco in 2023-24 beat every Rubbermaid per-piece rate except the Walmart 18-pc. Not current.
- Home Depot's regular 20-pc price ($50.65) is far above sale rates, so skip it unless a bundle or card offer applies.
- Free store pickup at Target avoids shipping minimums; Walmart+ or $35 minimum applies per the posts.
- Caveat: no live price comparison with Amazon was made or may be published.

## Verification gaps for the next brief
Walmart live price and return window, Costco current price and policy, Kroger, rubbermaid.com store and warranty, Target 10-pc price and return window, OXO and Pyrex current non-Amazon prices.
