# Amazon-policy compliance sweep — replacement titles, descriptions and pin texts (2026-10-05)

For the owner to apply to the shared files the sweep did not edit (`daily/search-descriptions.md`, `pinterest/pins-2026-09.md`, `scripts/publish_blogger.py` titles, Blogger editor). Rules: daily/README.md §0 "Amazon data rules"; research/strategy-2026-10-amazon.md §1.3. Every post below now passes `scripts/check_post.py` with no "FAIL: Amazon policy" lines. "Unchanged" means the current text already follows the rules.

## 2026-09-prime-big-deal-days-2026
- FAILs before: 2, after: 0 (both were Amazon price trackers: camelcamelcamel and Keepa). After the edit check_post shows RESULT: PASS with no WARN lines.
- Title: unchanged — Prime Big Deal Days 2026: The 12 Deals Worth Waiting For (and the Price That Makes Each One Real)
- Search description (140 chars): Prime Big Deal Days 2026 (October 6–7): the price band that makes each of 12 deals real, from robot vacuums and AirPods to AirTag and Owala.
  - The old one said "the exact price". It broke no rule, but it no longer matches the post, which now gives bands. post-meta.md is updated to the new text.
- Pin title: unchanged (85 chars) — Prime Big Deal Days 2026: The 12 Deals Worth Waiting For (and the Real Price of Each)
- Pin description (401 chars): optional accuracy tweak, not a rule fix. Change "the exact price" to "the price band":
  - Amazon's fall sale runs October 6–7. Skip the "was $1,600" theatre: here is the price band that makes each of 12 deals real — Roborock and Dreame robot vacuums, AirPods Pro 3, Sony XM6, Anker, EcoFlow and Jackery power stations, Ray-Ban Meta, AirTag 2, Owala FreeSip and the Bissell Little Green — plus five traps and a two-minute plan. #primebigdealdays #primeday #amazondeals #dealalert #amazonfinds
- Pin alt: unchanged (139 chars)
- What changed:
  - **Price trackers:** removed the camelcamelcamel and Keepa steps and the price-history wording. They are replaced by a "check the exact model first" step, plus the existing checks: Amazon's "Lowest price in 30 days" label, the brand store and Walmart, and our table.
  - **Deal prices:** every deal price in the table, the cards and the takeaways is now a band with an approximate percentage off the brand list price (for example, "Under $900 (40%+ off list)" and "Under $80 (20% off list)"). The table columns are now "Brand list", "Typical 2026 band (US retailers)" and "Real deal in October".
  - **Dated low prices removed:** AirPods 4 at $89, Anker F2000 at $949, AirTag 4-pack at $79.99 as the "record", AirPods Pro summer low $169, X50 "touched $800", Jackery "$599 last Black Friday" and Bissell "$81". They are replaced by "Black Friday went lower last year" or by generic wording with no numbers.
  - **Prime fee:** dropped the "$14.99 a month or $139 a year" figures.
  - **Rating counts:** removed the Owala "117,000+ ratings at 4.6 stars". It is replaced by "Walmart shows 4.8 stars from 21,000+ owner reviews (checked September 2026)", from research/best-sellers-2026-09.md.
  - **Review wording:** the "From the reviews" intro now says the themes come from forums, other retailers and expert reviews. The AirTag owner line is credited to Tom's Guide and Macworld.
  - **Best-seller claims:** removed "Three of Amazon's most-bought products" and "Amazon's best sellers". The section heading, the card badges and the JSON-LD ItemList names now say "Small buy".
  - **Non-Amazon prices with sources:** Owala list $29.99 at owalalife.com (September 2026) and $23.99 in Owala's own Black Friday 2025 sale (NBC Select). AirTag list $99 at Apple. Bissell list $123.59 at Bissell.
  - **Ray-Ban Meta:** the text said "wait for Connect", which was stale. It now says the Gen 3 launched September 23 from $449 (9to5Google, from research/refresh-2026-10-05-smart-glasses.md). The card, table, plan and FAQ are updated to match.
  - **Prime trial line:** added "Not a Prime member? Deal prices need Prime; Amazon's 30-day trial counts." after the deal types. It links tryprimefree?tag=verdictpicks-20 with rel="nofollow sponsored noopener" and a "(paid link)" tag. The existing "Start the free trial" link also gets "(paid link)".
  - **Other text:** the byline now reads "Updated October 5, 2026". The Korean summary date is corrected (10월 6~7일 확정) and it now mentions bands.
  - **cover.json:** removed "$24 bottle … $899 robot" from the subtitle and the pin bullet, and "Best sellers" from the footer. The cover and pin were re-rendered and both fit with no clipping. cover.jpg was regenerated and is a new untracked file.
  - **Links:** all 14 Amazon links carry tag=verdictpicks-20 (12 product links plus 2 trial links).


## 2026-09-best-pet-products-on-amazon
- FAILs before: 1, after: 0 (before: 1 "FAIL: Amazon policy (Amazon price)" line, plus 4 WARNs for rank claims and the "RESULT: FAIL" line; after: "RESULT: PASS" with no FAIL and no WARN lines)
- Title: the current title "The 3 Best Pet Products on Amazon in 2026: a $25 Roller, an $85 Grooming Vacuum and the $699 Robot Litter Box (Good · Better · Best)" breaks the rules: $25 and $85 are Amazon prices, and it is over 100 chars. New title: "The 3 Best Pet Products on Amazon in 2026: Hair Roller, Grooming Vacuum, Robot Litter Box" (89 chars). Updated in post-meta.md.
- search description: "Our pet picks at three prices: ChomChom Roller, Neakasa P1 Pro grooming vacuum, Litter-Robot 4, with owner themes, returns and how to spot fakes." (145 chars). It replaces the old one, which had "Amazon's best", $25/$85 Amazon prices and "owner reviews". Updated in post-meta.md.
- pin title: unchanged ("Best Pet Products on Amazon 2026: Hair Roller, Grooming Vacuum, Robot Litter Box", 80 chars)
- pin description (old one had "What 200,000+ owners really say", a count built from Amazon ratings): "One pet product per problem: the ChomChom Roller for fur on the couch, the Neakasa P1 Pro grooming vacuum for fur on the dog, and the Litter-Robot 4 for the cat people. What owners and expert testers really say, what each costs to run, how Amazon delivery and returns work for pet gear, and how to spot the fakes. Starring Noeul the Jindo. #petproducts #doghair #catlitter #litterrobot #amazonfinds #petsupplies" (411 chars)
- pin alt (old one had "$25, $85 and $699"): "Verdict Picks guide to the best pet products on Amazon 2026: ChomChom Roller (under $30), Neakasa P1 Pro grooming vacuum (under $100 on sale) and Litter-Robot 4 ($699 direct)." (175 chars)
- What changed:
  - Rank and badge claims removed: "Amazon's No. 1 pet hair remover", "Amazon's best-selling pet hair remover" (Yahoo Shopping and Today rank quotes), "tops Amazon's cat hair-removal category" (in both the FAQ and the JSON-LD FAQ answer), "the top-selling grooming vacuum", "made this thing a best seller" and "why they're best sellers". They now say "our top pick" or name the expert testers (Wirecutter, CNN Underscored, Reader's Digest, Apartment Therapy).
  - Amazon rating figures removed: "4.5★, 190,000+ ratings" (Amazon numbers relayed by Reader's Digest) from the lead, Key takeaways, Korean summary, table, verdict line, card chip and owners text, voices.svg and cards/chomchom.svg. The "200,000+ owners" line came off the cover subtitle and the pin. Remaining ratings are non-Amazon and dated: Dogster 4.9/5; Neakasa store 4.8/5 from 770 reviews (Sept. 2026); Whisker 4.4/5 from 7,000+ verified reviews (Sept. 2026); Catster and Hepper (all from research/pet-products-2026-09.md).
  - Amazon prices removed: ChomChom $24.99 everyday, $27.99–$31.99 list and $12–$20 deal lows; Neakasa $130 list, $83–$85 and the $70–$75 floor; EVO $499 Prime Day; PETKIT $559.99/$440; M1 $499; Mini $19–$24; the "$25/$85" numbers in the lead, takeaways, Vera banner, tiers.svg and the "listed on Amazon" sentence (the linter FAIL). They are now price bands (under $30, under $100 on sale, under $25, roughly $450–$560, around $500), a Walmart price ($23.99 at Walmart, September 2026, from the research file), and Whisker direct prices ($699/$799/$599 reconditioned direct at litter-robot.com, Sept. 2026; EVO $599 direct; Costco bundle $699.99, July 2026).
  - The "when to buy" section and the table now give percent-off rules of thumb for Prime Big Deal Days (Oct 6–7) instead of Amazon deal prices: ChomChom 20–30% off is typical and 40%+ off is a buy-now; P1 Pro about a third off list is good and close to half off is the floor.
  - Content framed as coming from Amazon reviews was reworded as owner reports and expert tests. "Delivery stories from the reviews" became "Delivery: what to watch for". The table note about Amazon rating counts became a note on where the ratings come from.
  - Byline now reads "Updated October 5, 2026". Cover footer "Best sellers" became "Buying guide". The cover and pin were re-rendered, and the text fits with no clipping. tiers.svg, voices.svg and cards/chomchom.svg text was edited by hand and their PNGs re-rendered. amazon.png and cost.png were rewritten by the renderer but are byte-identical. images/cover.jpg was created by cover_jpeg and is untracked.
  - All 10 Amazon links still carry tag=verdictpicks-20, unchanged. The button wording is unchanged: the assembler generates "Check the price on Amazon →", and the post never had "See today's price".


## 2026-09-dog-essentials-on-amazon
- FAILs before: 3, after: 0 (RESULT: PASS; the one WARN, "Amazon's best-selling orthopedic bed", is also gone; 14/14 Amazon links still carry tag=verdictpicks-20)
- title: unchanged — Best-Value Dog Essentials on Amazon 2026: No-Pull Harness, KONG Classic, Poop Bags
- search description: unchanged, it follows the rules — "The 3 best-value dog essentials on Amazon: Rabbitgoo harness, KONG Classic, Earth Rated bags, and how Amazon compares with Chewy, Walmart, Temu." (144 chars)
- pin title: unchanged (86 chars); pin description: unchanged (346 chars); pin alt: unchanged (132 chars). None of the three has a rank, rating or Amazon price. Cover and pin artwork: unchanged ("Best Value on Amazon" is not a rank claim).
- What changed:
  - Removed Amazon rating and review counts: "100,000+ ratings at 4.5 stars" (Rabbitgoo: key takeaways, picks table, card, Korean summary "평가 10만 개 이상"), "236,000+ ratings" (Earth Rated card and table), and "4.8 stars, 115,000+ ratings" (Chuckit!). Replaced them with outside verdicts: KONG at 4.6 out of 5 from Chewy owners (Sept 2026, research/dog-essentials-2026-09.md); Earth Rated as CNN Underscored's 2026 test winner and Wirecutter's pick; Rebarkable's trainer verdict on the Rabbitgoo. Card owner lines are now labelled as owner themes from forums and trainer reviews.
  - Removed the rank claim "Amazon's best-selling orthopedic bed" and replaced it with "Our top pick for a budget orthopedic bed", plus a sourced price: $39.99 for the Large at Chewy (Sept 2026).
  - Turned Amazon prices into price bands: the "Typical Amazon price" table column (now "Price band"), the $20–$26 / $8–$16 / $9–$14 harness, KONG and bag ranges, the alternatives (Voyager, Escape Proof, 2 Hounds, Toppl, Pogi's), cost per year, the 12-row starter-kit table, kit totals and buy_total. Where research had a non-Amazon price, it is named with source and date: Chewy $9.96 and Walmart from $7.96 for the KONG Large, Chewy $14.99 for Earth Rated 270, Walmart $5.59 rollback for Chuckit!, Walmart $22.99 for the Casfuy grinder.
  - Removed the dated Amazon coupon and deal prices: "$13.99 regular and $9–$10 on a coupon at Amazon", "$11–$13 with a coupon", "1.5 cents a bag", "about $2 a month", "Prime Day brought it to $16 from $21", "Anything under $18". Deal advice for Prime Big Deal Days (Oct 6–7) is now a percentage: "roughly a quarter off" and "20% or more off the everyday price is a buy". The deal-day total for all three is now "15–25% off".
  - Removed "the Amazon best-seller lists and the review counts" from the method paragraph, and changed "reviews" to "complaints" or "opinions" where the text read like review content. The bagmath caption no longer makes the Amazon-vs-Chewy price claim.
  - bagmath.svg infographic (inlined in the post and shared in promo): replaced the Amazon-derived per-bag costs with bands; the Chewy row now carries its date. I re-rendered only bagmath.png and checked it: the text fits. No other artwork was regenerated.
  - The byline now reads "Updated October 5, 2026". FAQ and JSON-LD had no ratings or ranks; there is no aggregateRating.


## 2026-09-owala-freesip
- FAILs before: 0, after: 0 (the linter only gave 3 WARN lines for "Amazon's #1 bottle" before; it now gives none. The post still had many violations the linter missed, all fixed below.)
- Title: Owala FreeSip Review: Why One Lid Made It the Water Bottle to Beat (66 chars). Old title: "Owala FreeSip Review: How a Water Bottle Beat Stanley to #1 on Amazon". The post has no in-page H1, so the title lives in post-meta.md (updated there).
- Search description: Owala FreeSip review: why the sip-or-chug lid wins, which size fits your cup holder, when it's about 20% off, and how to keep the gasket clean. (143 chars)
- Pin title: Owala FreeSip Review: Why the Sip-or-Chug Lid Beat Stanley (58 chars). Old: "...How a $30 Bottle Beat Stanley to #1 on Amazon".
- Pin description: The sip-or-chug lid explained, which size fits your cup holder, what counts as a good sale (about 20% off list), and the two-minute fix that keeps the gasket mold-free. Owala vs Stanley vs Yeti in one honest read. #owala #waterbottle #hydration #hydrationbottle #waterbottlereview (280 chars). Removed "when it drops to $24" (an Amazon sale price) and #amazonbestsellers.
- Pin alt: unchanged (139 chars, compliant).
- What changed:
  - Amazon rank and badge claims ("number-one item in Amazon's entire Kitchen & Dining", "Amazon's #1 bottle" badge in cards, table and ItemList JSON-LD, "rare Amazon best seller", "knocked Stanley off Amazon's top spot", "Three reasons it's a best seller", the Korean summary's "아마존 주방 부문 1위"): replaced with "Our top pick", "hugely popular bottle" and "took the spotlight from the Stanley Quencher". The H2 is now "Three reasons it's our top pick".
  - Amazon rating data removed: "117,000+ ratings at 4.6 stars" (intro and card), Stanley "90,000+ ratings", and Rolling Stone's "10,000 bought in a month vs 7,000 Stanleys" (Amazon "bought in past month" data). Replaced with a Walmart figure: the 24 oz Very, Very Black listing showed 4.7 out of 5 from about 29,700 ratings (walmart.com/reviews/product/785624932, seen in a search snippet in October 2026; walmart.com itself was blocked to direct fetch). The line "one-star ones" became "owner reviews and expert tests". The line "Every leak review starts with 'I forgot to lock it'" became a generic owner theme.
  - Amazon prices and price history removed: $23.99 "sale floor", 32 oz $27–$28, "about $24" (takeaways, Vera, Korean summary, H2 verdict), ~$24–$28, and the Black Friday "$23.99, its lowest ever". Replaced with bands and percentage rules: "under $25 on sale", "about 20% off list", "32 oz under $30". The $29.99 list price (NBC News, Yahoo, 2026) and the 32 oz list of $35–$40 (Parade, Yahoo) stay. Stanley is now "under $50 (about $38 at Walmart, September 2026)" and Yeti "under $50". Black Friday now says Owala ran 20% off sitewide on its own store (NBC News Select, Nov 2025) and CNN Underscored saw up to 36% off some items (Cyber Monday 2025).
  - Prime Big Deal Days (Oct 6–7): "expect the same tier" became "treat roughly 20% off list as a good deal".
  - The ItemList JSON-LD names were rebuilt from the new card badges. The FAQ schema had no Amazon data.
  - Cover: subtitle "Amazon's #1 in Kitchen & Dining, 117,000+ ratings" was removed. The title is now "Owala FreeSip / The Bottle / Built on a Lid", the footer "Best-seller review" became "Our review", and the alt text (also the Pinterest Save description) was rewritten. The cover image alt in src was rewritten too. cover.png, pin.png and cover.jpg were re-rendered and checked: the text fits.
  - Byline: "· Updated October 5, 2026 ·".
- Notes:
  - brand/seo-configs.json (read only) has no "#1 on Amazon" title or description. But its "korean" field still says "아마존 주방 부문 1위 물병" and "(약 $24)", and its takeaway says "at about $24". seo_layer skips these because the src already has the takeaways box, so the built post is clean. They would come back only if the src box were removed. Worth cleaning in the config.
  - The built post.html's "More guides" block (from brand/site-index.json, outside my scope) still shows the Beckham pillows blurb "4.4 stars from 220,000+ ratings". That will clear when the site index is updated.
  - cover.jpg is a new untracked file. Only cover/pin SVG and PNG artwork changed; cards and strips were not regenerated.


## 2026-09-apple-airtag-2
- FAILs before: 0, after: 0 (RESULT: PASS, no WARN lines)
- Title: **Apple AirTag 2 Review: Is the 4-Pack Worth It for Your iPhone?** (62 chars). It replaces "Apple AirTag 2: Why Amazon Can't Keep the 4-Pack in Stock (and Whether You Need It)", which made an Amazon sales/stock claim. post-meta.md is updated.
- Search description (140 chars): AirTag 2 review: louder, finds things farther away, works with Apple Watch. Is the $99 4-pack worth it, when to buy, and who should skip it. The old one said "$79.99 for four at its Amazon low". post-meta.md is updated.
- Pin title (62): Apple AirTag 2 Review: Is the 4-Pack Worth It for Your iPhone? (the old one said "Keeps Selling Out on Amazon")
- Pin description (318): Louder speaker, farther Precision Finding and Apple Watch support. Apple lists the 4-pack at $99; we explain why about 20% off is the price to wait for, who should buy AirTag 2, who should get a Chipolo or Galaxy SmartTag instead, and the setup tips owners wish they had known. #airtag #apple #travelhacks #techgadgets (removed "$79.99 … record low" and #amazonbestsellers)
- Pin alt (154): Verdict Picks review of Apple AirTag 2: louder, farther finding, Apple Watch support, wait for about 20% off the 4-pack, iPhone only, alternatives inside.
- Pin text in pinterest/pins-2026-09.md was NOT edited. The replacements above need to be applied there.

### What changed
- **Amazon best-seller and badge claims:** removed. That covers the "Amazon best seller" badge in cards.json (which also feeds the table and the JSON-LD ItemList name), the H2 "Three reasons it's a best seller", the H2 "Why is everyone buying this?", the cover image alt "why the 4-pack is an Amazon best seller", "아마존 베스트셀러" in the Korean summary, and the cover footer "Best-seller review". They now read "Our top pick for iPhone" or neutral wording.
- **Amazon prices and dated Amazon price history:** removed. That covers $79.99 for four, $24 for one, $89 on Prime Day, the dates Aug/Sep 1, 5, 9 and 11, "record low" and "all-time low", the $62.99 Black Friday price for the original, and the $17 original AirTag. All of these came from Amazon deal posts in research/best-sellers-2026-09.md.
  - Replaced with Apple's list prices: $29 for one and $99 for four (apple.com, launch January 2026, per MacRumors and 9to5Mac in the research file).
  - Replaced with percentage rules of thumb: "about 20% off", "roughly $80 or less for four" as a band, "about a third off list" for last year's Black Friday, and "often under $20 on sale" for the original AirTag.
- **Prime Big Deal Days (Oct 6–7):** "the same $79.99" became "expect a similar ~20% off; we wouldn't count on much more".
- **Chipolo Pop and SmartTag2 prices:** "about $29" and "about $30" had no source, so they became the band "under $35".
- **Paraphrased Amazon review content:** removed. The "much louder" owner quote came from BGR's summary of Amazon shoppers. In cards.json and the "Loved" bullet it is now attributed to reviewers' measurements (about 85 dB against 66 dB, Airpinpoint, per the research file). The generic owner themes stay.
- **Cover.json:** the subtitle "$79.99 for four at Amazon's record low" became "$99 for four at Apple, often less on sale". The pin bullet became "Wait for about 20% off the 4-pack", and the alt and footer were cleaned up.
- **Rebuild:** I changed the byline to "Updated October 5, 2026" and ran seo_layer, assemble and build. Because cover.json changed, I also re-rendered the cover and pin (make_cover, make_pin, render_png, cover_jpeg). I checked both images by eye and the text fits.
- No non-Amazon owner ratings were added (none in the research), and no numbers were invented.


## 2026-09-bissell-little-green
- FAILs before: 0, after: 0 (check_post: RESULT: PASS, no WARN lines)
- Title: unchanged — Bissell Little Green Review: Behind a Million Before-and-After Videos (69 chars)
- Search description: unchanged — "Bissell Little Green review: what the viral spot cleaner really cleans, its limits, Mini vs classic, and the Black Friday price to wait for." (140 chars)
- Pin title (replace; the old one says "$95 Spot Cleaner", a typical Amazon sale price): "Bissell Little Green Review: What the Under-$100 Spot Cleaner Cleans (and Can't)" (80 chars)
- Pin description (replace; drops the #amazonbestsellers hashtag): "The machine behind a million before-and-after videos: what it really lifts out of couches, car seats and pet stains, where it falls short, Mini vs classic, and the Black Friday price worth waiting for. #bissell #littlegreen #cleaningtips #petstains #spotcleaner" (261 chars)
- Pin alt: unchanged — "Verdict Picks review of the Bissell Little Green spot cleaner: what it cleans and can't, Mini vs classic explained, the Black Friday price to wait for." (151 chars)

### What changed (src/00-easy.html, cards.json, cover.json; then rebuilt)
- **Amazon rank/badge claims removed:** the Mini's "#1 Best Seller" badge (body text, table, card badge, JSON-LD ItemList name) became "Our pick for small spaces · half the size". The H2 "Three reasons it's a best seller" became "Three reasons it sells". On the cover, "Best-seller review" and the alt text "best-seller story" became "Spot-cleaner review" and "spot-cleaner story".
- **Amazon rating counts removed:** "87,000-plus ratings" and "almost 100,000 fans" were cut. In their place: a Walmart.com owner rating of 4.4/5 from about 1,650 ratings, checked October 5, 2026 (from a web-search result snippet for walmart.com/reviews/product/436861322; the walmart.com page itself is blocked by the network proxy). The owners section now also cites Good Housekeeping's test result.
- **Amazon sales-rank numbers removed:** the ASInsight figures of about 60K and 30K units a month (estimates built on Amazon data) became a general line: ASInsight (2026) estimates the Mini now outsells the classic.
- **Amazon prices and price-tracker history removed:** $94.99–$129.99, $129.99 (camelcamelcamel), $81 and $81–$85 on Black Friday, $79.99 on Prime Day, $74.99 for the Mini on Cyber Monday, $82–$90 for the Mini Cordless, $129.99 for the Hoover, and "$69 at Walmart" (no date). The replacements:
  - bands: "about $95–$130", "usually under $100", "usually about $130"
  - Bissell list prices with a source: $123.59 for the classic, and the Mini Cordless list cut from $160 to $130 (9to5Toys, Feb 11, 2026)
  - in the table, the "Price at the time of writing" column is now "Typical price"
- **Prime Big Deal Days (Oct 6–7) and Black Friday deal prices** became a rule of thumb: about 25–30% off the $123.59 list (about $85–$95). The Black Friday line now cites the ~31% early discount reported by CNN Underscored (Nov 19, 2025). The key takeaway, the "When to buy" verdict line and Vera's Mini line ("at $80" is now "usually under $100") were changed the same way.
- **Review phrasing reworded so it doesn't read as Amazon review content:** "the one-star reviews" is now "unhappy owners", and "Every 'it smells' review" is now "Most 'it smells' complaints". The wet/dry-vac comparison and the old-pet-stain complaint are now credited to Digital Reviews and to an AOL reviewer.
- **Cover:** the subtitle "The $95 machine…" is now "The under-$100 machine behind the viral videos —". The cover and pin were re-rendered and checked by eye; the text fits. "A Million Sold" stays because it is Bissell's own claim.
- **Byline:** "Updated October 5, 2026". All 3 Amazon links still carry tag=verdictpicks-20, and the button wording is unchanged.


## 2026-09-claude-higgsfield-mcp-ai-video
- FAILs before: 0, after: 0 (check_post: RESULT: PASS, no WARN lines)
- Title: unchanged — Claude + Higgsfield MCP: From One Photo to an AI Product Video (2026 Setup, Credits, 13 Uses, US Rules) (103 chars; it has no Amazon claims)
- Search description: unchanged — "Claude + Higgsfield MCP explained: the photo-to-video workflow, the 10-minute setup, what a 15-second AI ad costs in credits, and the US rules." (143 chars)
- Pin title / description / alt: unchanged (title 94 chars, alt 130 chars; the description has no Amazon ratings, ranks or prices)
- Cover: unchanged (cover.json has no rank, rating or Amazon price text), so no artwork was regenerated
- What changed:
  - Light box card badge (cards.json and the src JSON-LD ItemList): "Input · the $30 that fixes half of all bad renders" became "Input · the cheap fix for half of all bad renders". The $30 was an unsourced number for a product sold through the Amazon link.
  - Desk-kit cards (light box, tripod, SSD), "owners" field, which the assembler labels "From the reviews:": the unattributed owner-review praise and complaints for products sold through Amazon links had no source (research/ai-video-tools-affiliate-2026-09.md has none) and were probably drawn from Amazon reviews. Each is now marked "Our own analysis, not owner reviews:", with the same practical points written as category things to check.
  - SSD card "check": "the counterfeits live in the \"4 TB for $30\" listings" became "the implausibly cheap, implausibly large listings", so there is no Amazon-listing price figure.
  - Byline now reads "· Updated October 5, 2026 ·".
  - Left as they were: Higgsfield, Claude, ElevenLabs, Kling, Veo, Runway and CapCut plan prices (software, outside the rule); the 3 Amazon links with tag=verdictpicks-20; the "See today's price" buttons; "Amazon's own video rules" and the Associates-agreement sentence (policy references, not ranks or ratings).
- Rebuilt with seo_layer, then assemble_post, then build_post.


## Shared issues found during the sweep (not fixed here: outside these seven folders)

- **"More guides" block (brand/site-index.json, built from daily/search-descriptions.md):** the Beckham Hotel Collection pillows description says "4.4 stars from 220,000+ ratings" (Amazon rating count). The bidet entry says "the $50 LUXE NEO 185", and the pet guide says "ChomChom Roller ($25), Neakasa P1 Pro ($85), Litter-Robot 4 ($699)". Both are probably Amazon prices. Every post that shows these descriptions repeats them. Fix them in daily/search-descriptions.md, then run `python3 scripts/site_index.py --inject`.
- **brand/seo-configs.json:** the takeaways, Korean summaries and H2 verdicts for AirTag 2, Owala, Bissell and Prime Big Deal Days still had Amazon prices, record lows and "아마존 베스트셀러 / 1위". These are cleaned in this commit. The built posts were already clean, because seo_layer keeps a post's existing takeaways box.
- **Generators:** the pet post's tiers.svg, voices.svg and cards/chomchom.svg were edited by hand. If scripts/pet_infographics.py or scripts/product_cards.py is re-run for that post, the old rating and price text comes back.
- **Card label:** the assembler still labels the cards' owner-themes field "From the reviews:" (scripts/assemble_post.py). A neutral label such as "What owners mention:" would read better.
- **Walmart figures from search snippets:** the proxy blocks walmart.com, so these were not opened: Bissell (4.4/5, about 1,650 ratings) and Owala 24 oz (4.7/5, about 29,700 ratings). The Prime Days post cites an earlier Owala Walmart figure from research/best-sellers-2026-09.md (4.8, 21,000+, September 2026). Check both on walmart.com.
