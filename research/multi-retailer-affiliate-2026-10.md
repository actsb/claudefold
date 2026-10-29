# Earning from US retailers beyond Amazon: program-by-program research for Verdict Picks (October 2026)

Researched 2026-10-29 for https://acts39.blogspot.com: a US-audience buying-guide blog on a blogspot subdomain, 7 weeks old, near-zero traffic, run by a South Korean resident with no US company. Amazon Associates is in its 180-day first review. About 70 web searches and 45 page fetches, plus direct downloads of program pages and scripts.

**Evidence labels and limits**
- **[OFFICIAL]**: the retailer's, network's or regulator's own page, fetched on 2026-10-29 unless noted. Most program pages show no "last updated" date. These are marked "n.d." and should be read as "as seen on 2026-10-29".
- **[OFFICIAL-CODE]**: text pulled from the JavaScript bundle of an official single-page app (Target Partners, the Walmart affiliate site). This is the program's own text, but it is not a page a human sees in one place.
- **[3P]**: a third-party directory, blog or aggregator. Often stale or contradictory.
- **[INFERENCE]**: our reasoning.
- **UNVERIFIED**: nothing reliable was found.
- These pages were blocked or could not be loaded: homedepot.com, lowes.com, kohls.com, macys.com, petco.com, sharkninja.com, nytimes.com (Wirecutter), the eBay Partner Network agreement (behind a bot check), and the Skimlinks help center (Cloudflare). For those, claims rely on search snippets or third parties and are labelled that way.
- Quotes from official pages are exact but kept short. Some tools cap quotes, so a few long sentences appear as consecutive fragments.

---

## 0. Bottom line

1. **The big-box programs are mostly closed to us directly, and the barrier is residency, not traffic.**
   - **Walmart:** the agreement lists sites that are "non-US based or are websites that primarily serve a non-US based audience" as objectionable. The sign-up code on affiliates.walmart.com says "This program is limited to US residents".
   - **Target:** treats sites that "Are not US based" as unsuitable and asks for a **W-9**, which is a form for US persons.
   - **Walmart Creator:** requires US residence and a US bank account.

   A Korean resident should not sign either agreement directly. The realistic route to Walmart and Target clicks is a sub-affiliate network (Sovrn Commerce or Skimlinks), and even that depends on per-merchant geo rules we could not see (UNVERIFIED).
2. **Best Buy is not worth it.** Its Impact rate was cut to a "temporary 0% baseline" in April 2025, after a previous 0–0.5%. Its terms also say "YOU MAY NOT PLACE INDIVIDUAL PRODUCT OR SERVICE PRICING" without permission.
3. **Brand-direct programs on Impact pay 1.5–5× Amazon in our categories, and many say anyone can apply.**
   - Anker: 8%, 30-day cookie.
   - Roborock: 4–7%, 35-day cookie.
   - Dreame: at least 6%, 30-day cookie.
   - EcoFlow: at least 5%, 7-day cookie.
   - SharkNinja: "up to 20%".
   - Levoit: "up to 10%".

   Impact pays non-US partners by international EFT or PayPal from a $10 threshold, after a W-8BEN. This is the best first step.
4. **Amazon allows other retailers' links on the same page, but two Amazon rules bite:**
   - You may not use Amazon "Program Content" (its images and data) to promote products sold on other sites.
   - If you show Amazon's price in a comparison format, you must show Amazon's lowest new price, pulled from the API with a timestamp.
   - Separately, since 2024-12-20 you may not earn from Associates and another program (such as Levanta) on the same traffic or link.
5. **Price display is the hidden conflict.** Our posts already type in Walmart, Target and Best Buy prices with a source and date.
   - Walmart: allows a price "only if such information is provided to you" by Walmart.
   - Target: "you may not include price information… unless it is used as part of Target's Merchandiser Datafeed."
   - Best Buy: bans individual pricing outright without written permission.

   Once we join any of these (directly, and arguably through a sub-network), hand-typed prices for that retailer have to become feed or API prices, or "Check price" buttons. **[INFERENCE]** Today, as a non-member, we are not bound by their agreements, so the current practice is not a contract breach.
6. **Recommended order.** Details are in §3.
   1. Impact partner account, then 5–8 brand programs (Anker/Soundcore, Roborock, Dreame, EcoFlow, SharkNinja, Levoit, Chewy).
   2. One auto-affiliate network: Sovrn Commerce first, Skimlinks if Sovrn declines.
   3. Levanta for Amazon-only third-party brands, after the Amazon review is settled.
   4. Later, after a custom domain and real traffic: Home Depot, Lowe's and Wayfair through Impact or CJ, plus CJ and Rakuten accounts for specific brands (iRobot, Dyson).
   5. Skip: Walmart and Target direct, Best Buy, Costco, Howl.

---

## 1. Program-by-program facts

### 1.1 Walmart Affiliate Program (Impact) and Walmart Creator

**Network**
- [OFFICIAL] "Walmart currently uses Impact Radius as our Program service provider." Source: Walmart Operating Agreement for Affiliate Network, https://affiliates.walmart.com/terms, "Last updated June 2026".

**Eligibility: the blocker**
- [OFFICIAL] Section 3(a) lists as objectionable any site that "is non-US based or are websites that primarily serve a non-US based audience" (affiliates.walmart.com/terms, June 2026).
- [OFFICIAL-CODE] The registration code on affiliates.walmart.com contains the validation messages "This program is limited to US residents" and "You must reside in the United States to qualify". It also has a "U.S. State of Residence" step. Source: JS bundle of https://affiliates.walmart.com/, downloaded 2026-10-29. This code may serve the Creator flow that shares the platform. Either way, it signals residency screening.
- [3P] Walmart Creator requires US residency, and adding a foreign bank account "terminates" the account and forfeits commissions (https://creatorflow.so/blog/walmart-creator-program/, updated 2026-08-21). The Walmart Creator FAQ, as quoted, says: "Must be 18 or older and reside in the U.S." (via search snippets, 2026).

**Commission**
- [OFFICIAL] "Affiliates can earn up to 4% on each eligible sale" (https://affiliates.walmart.com/faqs, n.d.).
- [3P] Category table (Niche Pursuits, updated 2024-02-25, https://www.nichepursuits.com/walmart-affiliate-program/):
  - 4%: Home, Baby, Health & Beauty, Clothing, Patio & Garden, Sports & Outdoors, Jewelry, Gifts.
  - 1%: Electronics (including video games), Toys, Wireless, Photo.
  - Excluded: Tires, Food, video-game hardware, baby consumables.
- [3P] Walmart Creator is reported at 0–18% (creatorflow.so, argil.ai, 2026). The rate card is visible only after login.

**Cookie window**
- [OFFICIAL] The agreement only says "within the relevant cookie window" and gives no number of days.
- [3P] Affiliate program: 3 days (Niche Pursuits, 2024). Creator: 14 days, plus a 30-day lock (creatorflow.so, 2026).

**Payment**
- [OFFICIAL] "Approximately ninety (90) days following the end of each calendar month, you will receive a check" (Section 7).
- The agreement does not mention a W-8.

**Prices**
- [OFFICIAL] "You may include current price information in your product descriptions only if such information is provided to you" (Section 8). The Walmart site price governs.
- [OFFICIAL] The agreement also bans "price tracking and/or price alerting functionality" (Section 3(a), summary of the fetched text).

**Images and content**
- [OFFICIAL] Affiliates may display only the logos and "graphic images" that Walmart or the Platform provides. No "scrape" or "spider" of the site for images, logos or text. No redistributing or syndicating "Walmart's datafeed" to third parties.
- RSS feeds are for "personal, noncommercial use".

**Competitors and comparisons**
- [OFFICIAL] Exhibit A item 16: "You may not place the Trademarks adjacent to competitive brands, including prohibitions against … objectionable material and websites."
- Item 23: you may not use the Trademarks "alongside or in conjunction with" terms including "percent (%) off", "sale", or "coupons".
- No "dupe" comparisons.
- No bidding on Walmart or competitor trademarks.
- Paid search and ad networks are banned for regular affiliates.
- The agreement is non-exclusive and does not mention Amazon.
- **[INFERENCE]** A "Walmart" button sitting right next to an "Amazon" button may conflict with item 16 as literally written. Large publishers (RTINGS, Tom's Guide, KCL) do it routinely, probably under negotiated terms.

**Disclosure**
- [OFFICIAL] "clear and conspicuous" disclosure "placed next to the Qualifying Links". Paid endorsements are labelled "#WalmartPartner" or "paid link".

**Assessment**
- **Not available directly** to a Korean-resident publisher. Possible only through Sovrn or Skimlinks, where Walmart is listed: Sovrn (3P, referly) and Skimlinks' own page ("Login to your Skimlinks account to see the rates available to you", https://skimlinks.com/walmart-affiliate-program/).
- Whether Walmart accepts non-US sub-publishers through these networks is UNVERIFIED.

### 1.2 Target Partners (Impact)

**Eligibility**
- [OFFICIAL-CODE] The FAQ in the bundle at https://partners.target.com/ says: "Any website owner, blogger or creator network that runs a family-friendly website and has mainly US-based viewership is eligible."
- [OFFICIAL-CODE] The terms (§2.2 Unsuitable sites) list sites that "Are not US based or primarily serve or market to audiences not in the US".
- The same list includes sites that "Are unable to direct a reasonable amount of traffic by way of sales volume, clicks and page views", sites that "Are under construction", and sites that "Do not clearly state an online privacy policy".
- The Target Ambassadors (LTK) addendum requires "a legal resident of, and primarily based in, the United States".

**Tax and payment**
- [OFFICIAL-CODE] §9.8: "you may be required to fill out and submit a W-9 … Only after your W-9 has been received will you be eligible to receive Referral Fee payments".
- [OFFICIAL-CODE] §9.7: payment goes through the "Target Vendor's payment program".

**Cookie window**
- [OFFICIAL-CODE] "tracked within a 7-day cookie window".

**Commission**
- [OFFICIAL-CODE] Rates are set by your "Insertion Order/Contract". "Standard rates are published on affiliate.target.com."
- [3P] Strackr, 2024-05-11 (https://strackr.com/blog/target-affiliate-programs):
  - Home & Outdoor Living: 5%, rising to 8% with volume.
  - Health & Beauty: 1%.
  - Pet care, household commodities, video games and some other categories: 0%.

**Prices**
- [OFFICIAL-CODE] §11.3: "Due to occasional changes in price, you may not include price information in your site or Affiliate Materials unless it is used as part of Target's Merchandiser Datafeed from the Target Vendor."

**Images and content**
- [OFFICIAL-CODE] No "Scrape" or "spider" of Target.com "for Content (such as images, logos or text)" without written consent. Content supplied by Target stays Target's.

**Restrictions**
- [OFFICIAL-CODE] No bidding on Target brand keywords (including "target coupon").
- No using Qualifying Links as the destination URL of paid ads.
- No link manipulation or cloaking ("redirecting links to hide or manipulate their original source").
- Posting coupon workarounds leads to termination.

**Disclosure**
- [OFFICIAL-CODE] At the beginning of the content, state: "[INSERT YOUR NAME] is a participant in the Target Affiliate Marketing Program, an affiliate advertising and marketing program that pays commissions to affiliates, like me, that advertise and link to [INSERT APPLICABLE TARGET DOMAIN NAME] if you buy products from Target through my link."
- Or: "[Product/Service] purchase through this link [may be/is] commission eligible."
- Social posts use #PaidLink and #TargetPartner.

**Assessment**
- **Not available directly** (US-based site rule, W-9, traffic rule). Use a sub-network if possible, which is UNVERIFIED.

### 1.3 Best Buy (Impact)

**Program page**
- [OFFICIAL] Publishers sign up through Impact. Creators use creators.bestbuy.com. Source: https://www.bestbuy.com/site/misc/affiliate-program/pcmcat198500050002.c, n.d.

**Terms** ([OFFICIAL], https://www.bestbuy.com/site/clp/affiliate-terms-and-conditions/pcmcat748302046001.c, n.d.)
- Commission applies only to orders "shipped by a Best Buy Property to a U.S. shipping address and billed to a U.S. billing address".
- Residency is not restricted explicitly. Publishers must be adults.
- Payment: "Approximately sixty (60) days following the end of each calendar month, Impact will pay to you".
- Pricing: "YOU MAY NOT PLACE INDIVIDUAL PRODUCT OR SERVICE PRICING" (Sec. 7). Product images and descriptions also need prior written permission.
- No scraping.
- Disclosure must be "placed above the fold; scrolling should not be necessary to find the disclosure".
- No bidding on Best Buy trademarks or on "direct competitors of Best Buy".

**Rate**
- [3P, reputable] Marketing Brew, 2025-04-29 (https://www.marketingbrew.com/stories/2025/04/29/broader-economic-factors-are-putting-pressure-on-best-buy-s-affiliate-program): the Impact listing showed "a zero rate across all categories", described in an email as a "temporary 0% baseline". The rate before that was 0.5% or 0%.
- [3P] Lasso and Affilimate list 0.5% with a 1-day cookie (2025–26).

**Assessment**
- **Skip.** Near-zero pay, plus a ban on showing prices.

### 1.4 Home Depot (Impact)

- [3P, snippet of the official page https://www.homedepot.com/c/SF_MS_The_Home_Depot_Affiliate_Program; the page returned 403 to us]:
  - Account data is managed in Impact Radius.
  - Sites must be live when applying.
  - Canadian affiliates go to homedepot.ca.
  - The snippet showed a 1-day window for the affiliate program and 30 days for the installation program.
- [3P] Geniuslink, 2026-05-18 (https://geniuslink.com/blog/home-depot-affiliate-program/): "average commission percentage of only 2.14%", a 24-hour cookie, and an average basket "over $300".
- [3P] Older reports: 1% default, 8% on some home décor.
- Non-US publisher policy: UNVERIFIED.
- **Assessment:** later and optional. A short cookie and about 2%. Use mainly for bidets, tools and car-adjacent items only when Home Depot is clearly the best place to buy.

### 1.5 Lowe's

- [3P] About 2% (some sources say 0.8%), 0% on gift cards and lumber, 1-day cookie.
- The network is reported as Impact, CJ or both, and is inconsistent (bloggingtips, Niche Pursuits; official page 403).
- Lowe's is reported to be a Sovrn Commerce merchant (3P, referly).
- **Assessment:** later and optional.

### 1.6 Wayfair

- [3P] US program on CJ, commission 5–7%, cookie 7 days (lower-funnel) or 14 days (upper-funnel). FlexOffers lists Wayfair North America at 9.6% (FlexOffers' publisher rate, page updated 2026-09-30, https://www.flexoffers.com/affiliate-programs/wayfair-north-america-affiliate-program/).
- The official US page returned 429 to us. UNVERIFIED.
- **Assessment:** later, for furniture, sleep and comfort content.

### 1.7 Chewy

- [OFFICIAL] "Chewy runs its affiliate program through Impact." "Affiliates with websites can apply via Impact." Pay is monthly by bank or check. Source: https://www.chewy.com/app/content/affiliate, n.d., 2026.
- The page says "Earn commission on every eligible order … from both new and existing customers". It also says Impact credits "new customer orders" within the cookie window, which is internally inconsistent.
- [3P] Geniuslink, 2026-06-01: "flat $15 commission for each new customer order", 15-day cookie, "Chewy doesn't partner with coupon or deal sites". This describes the older Partnerize setup and may be stale.
- **Assessment:** apply through Impact (now). Pet content pays only 3% at Amazon.

### 1.8 Kohl's and Macy's

- Kohl's [3P]: Impact, about 3%, 7-day cookie (Geniuslink, 2026-05-18, https://geniuslink.com/blog/kohls-affiliate-program/).
- Macy's [3P]: Rakuten Advertising, about 3% base, 10-day cookie, and an inactivity fee after 12 months (Geniuslink, 2026-05-18, https://geniuslink.com/blog/macys-affiliate-program/).
- Both official pages returned 403.
- **Assessment:** off-niche. Skip unless gift guides grow.

### 1.9 eBay Partner Network (EPN)

- [OFFICIAL] Rate card PDF linked from https://epnpartnernetwork.ebay.com/our-program/rate-card (no date on the PDF):

  | Category | Rate | Cap |
  |---|---|---|
  | Home & Garden (incl. Appliances, Pet Supplies) | 3.0% of sale | $550 |
  | Electronics: TV/Video/Audio, Cell Phones | 2.0% | $550 |
  | Computers/Tablets | 1.5% | $550 |
  | eBay Motors | 4.0% | $100 |
  | Vehicle Parts & Accessories | 3.0% | $550 |
  | Business & Industrial | 2.5% | $225 |
  | Fashion | 4.0% | $550 |
  | All Other | 4.0% | $550 |

- [3P] 24-hour cookie. Payment by PayPal or direct deposit (11 countries), $10 minimum (bloggingtips; affpaying).
- One affiliate reported their account was closed because their country was not supported.
- Korea eligibility: **UNVERIFIED**. The agreement page sits behind a bot check.
- **Assessment:** low value for new-product buying guides. Optional.

### 1.10 Costco

- [3P] No product affiliate program. A CJ listing pays for **new memberships** only (manychat, reacheffect, coruzant, 2025–26).
- **Assessment:** skip. Keep citing Costco prices as information only.

### 1.11 Petco and PetSmart

- [3P only] Petco: about 2–4%, 7-day cookie, Impact (or CJ). PetSmart: 2–8%, network unconfirmed (revshare, linkclicky, 2026).
- Official pages blocked. UNVERIFIED.
- **Assessment:** Chewy first.

### 1.12 Bed Bath & Beyond (Beyond Inc / Overstock brand)

- [OFFICIAL] "Bed Bath & Beyond partners with Partnerize for tracking, reporting, and payment". "Up to 3% on U.S. sales". Source: https://www.bedbathandbeyond.com/affiliates, © 2026.
- Cookie window: UNVERIFIED.
- **Assessment:** low priority.

### 1.13 Brand-direct programs

| Brand | Network(s) | Rate | Cookie | Eligibility wording | Source (date) |
|---|---|---|---|---|---|
| **Anker** (incl. Soundcore) | Impact, Rakuten (LinkShare) | "Earn a consistent 8% commission on all transactions" (a graphic also shows "7%") | "30-day cookie duration" | program "allows anyone to join"; bans links placed directly in search engines, hidden links and pop-ups | [OFFICIAL] https://www.anker.com/become-an-affiliate (© 2025) |
| **Anker SOLIX** (power stations) | per site | "consistent 5% commission" (US page per 3P snippet; the EU page shows 8%) | 30 days | — | [3P snippet of ankersolix.com] |
| **Roborock** | Impact, CJ | "4%-7% commission on sales" | "35-day cookie duration" | every application reviewed; AOV $400+ | [OFFICIAL] https://us.roborock.com/pages/roborock-affiliate-program (n.d.) |
| **Dreame** | Impact, Webgains | "minimum 6% commission" | 30 days | refunds reversed | [OFFICIAL via snippet] https://www.dreametech.com/pages/affiliate-program |
| **EcoFlow** | CJ, Awin, Impact | "minimum of 5%" (the page also says "up to 5%") | 7 days | review in 2–3 business days; double attribution across networks is reversed | [OFFICIAL] https://us.ecoflow.com/pages/affiliate-program (© 2026) |
| **SharkNinja** (Shark, Ninja) | Impact | "Up to 20% commission on sales" | not stated | "Influencers and Publications" | [OFFICIAL storefront mirror] https://blqw-002.dx.commercecloud.salesforce.com/s/US-SharkNinja/affiliate.html (© 2025); sharkninja.com returned 403 |
| **Levoit** (VeSync) | Impact/CJ/Awin (varies) | "up to 10%" | 3P: 30 days | — | [OFFICIAL snippet] https://levoit.com/pages/affiliates |
| **eufy** (Anker) | — | official pages conflict: "starts at 7%" vs "up to 20%" | 30 days | — | [OFFICIAL snippets] eufy.com/affiliate, eufy.com/pages/affiliate |
| **iRobot** | CJ (UK official page; US per 3P) | 3P: 2–4% | 30 days (CA official page) | — | [OFFICIAL CA/UK pages]; rates 3P |
| **Dyson** | Rakuten (US, 3P) | 3P: 1–2% | 3P: 25–30 days | — | UNVERIFIED |
| **Jackery** | Impact/ShareASale-Awin/CJ | 3P: 5–8% (3.84% on one network) | 3P: 30 days | — | 3P |
| **Tushy / Brondell** (bidets) | Impact | 3P: about 4% / 4–5% | 3P: Brondell 30 days | — | 3P (linkclicky, flexoffers) |
| **NOCO** (car) | FlexOffers/other | 3P: 8% | 3P: 30 days | — | 3P (revshare) |
| **Instant Brands** | CJ | 3P: 1% | — | — | 3P |

**Assessment.** Brand programs are the most accessible high-rate option.
- **[INFERENCE]** Brand stores usually convert worse than Amazon (Prime, trust, reviews). Long cookies (30–35 days) partly make up for this.
- A brand that runs the same program on several networks (EcoFlow, Roborock) reverses orders credited twice, so join each brand on **one** network only.

### 1.14 Levanta, Amazon Creator Connections and brand bonuses on Amazon sales

**Associates conflict**
- [OFFICIAL, Levanta FAQ] Effective **2024-12-20**, Amazon's agreement prohibits "creators from earning commissions on the same traffic through multiple programs". Levanta links "will no longer accept Associates tags". You "choose whether to use links from Levanta OR Amazon Associates" for each product. Source: https://knowledge.levanta.io/articles/2364861905-amazon-associates-policy-update-faq.
- [OFFICIAL, Amazon Program Policies, "Updated: April 14, 2026"] Amazon may withhold commissions or terminate if you are "attempting to claim commissions from both Amazon Associates and another program using the same traffic". Source: https://affiliate-program.amazon.com/help/operating/policies.

**How Levanta works for creators**
- [OFFICIAL] https://levanta.io/creators/: free sign-up. Example rates: Kitchen/Cookware 15%, Electronics/Tech 20%, Home Improvement 25%. "a single monthly payment from all of your brands".
- [3P] Making Sense of Cents, updated 2025-09-17:
  - Brands approve each creator.
  - Paid monthly through **Stripe**, 30 days after month-end.
  - About a 14-day attribution window, and only the promoted item pays.
- No traffic minimum or country rule is published. UNVERIFIED for non-US creators.
- [3P] Stripe's pricing page marks South Korea as available for cross-border payouts. Stripe's changelog added Korean bank accounts for Global Payouts in May 2026. Source: https://docs.stripe.com/changelog/dahlia/2026-05-27/cross-border-payouts-20-new-bank-account-types.md. Whether Levanta enables that for creators: UNVERIFIED.

**Amazon Creator Connections**
- [OFFICIAL Amazon brand guide PDF, via snippet] "To be eligible for Creator Connections, Creators must be in at the Bronze tier or higher in Creator Stars" (https://m.media-amazon.com/images/G/28/TWGS/SU/AmazonCreatorConnections_BrandGuide.pdf).
- [3P] Bonuses of at least 10% are paid on top of the base Associates rate.
- **[INFERENCE]** Reachable only after the Associates account is approved and active. Check the Associates Central "Creator Connections" tab after approval.
- [OBSERVED] Krazy Coupon Lady's Amazon links carry `campaignId=amzn1.campaign…` parameters (KCL page source, 2026-10-29), which shows large publishers use these campaigns.

**Assessment**
- Levanta suits Amazon-only third-party brands (many bidet, car-accessory and pet brands). Use it per product, never adding our Associates tag to the same link.
- **[INFERENCE]** Until the 3 qualifying Associates sales are in, keep the money pages on Associates links, so Levanta does not divert the sales the review needs.

### 1.15 Auto-affiliate (sub-affiliate) networks

**Sovrn Commerce (formerly VigLink)**
- Approval:
  - [OFFICIAL] Flow is "Submit your site > Install Commerce > Generate Clicks > Get Approved". Review in up to 5 business days (https://knowledge.sovrn.com/kb/getting-started-with-sovrn-commerce, n.d.).
  - [OFFICIAL] "we must receive click traffic (made by a real human)" (https://www.sovrn.com/blog/getting-approved-for-commerce/, 2022-03-22).
  - No published traffic minimum. Geography and subdomain policy not addressed.
- Payment:
  - [OFFICIAL] "$50 for wire transfers" and "$25 for all other payment types (ACH, Check, eCheck and PayPal)". Net-90: January earnings are paid at the end of April (https://knowledge.sovrn.com/kb/payments-in-commerce, n.d.). PayPal users get tax documents from PayPal.
- Revenue share:
  - [3P] Publisher keeps about 75% (ShoutMeLoud; a VigLink executive quoted in AdExchanger: "we take 25%").
- Merchants:
  - Walmart and Lowe's are reported. Target, Best Buy and Home Depot reachable through Sovrn per Geniuslink ("Commission share rates apply", https://geniuslink.com/supported).
- Amazon:
  - [3P, AdExchanger] Amazon removed sub-networks (Skimlinks, Sovrn) from its program, so leave Amazon links on our own Associates tag.
- Tools:
  - [OFFICIAL KB mirror] A Price Comparison widget and API (comparisons.sovrn.com) show live multi-merchant prices. "You must be approved for Sovrn Commerce before you can implement a Price Comparison."
  - **This can supply Walmart and Target prices legitimately**, through the network rather than hand-typed. **[INFERENCE]** Whether that counts as "provided by" Walmart under §8 is not certain.

**Skimlinks (Connexity/Taboola)**
- Approval:
  - [3P snippet of help center] Fewer than 10 original articles means "Lack of Content". Coupon or deal sites without editorial content are excluded. Sites must be live and verifiably yours. Every application is manually reviewed.
  - [OFFICIAL] "Skimlinks currently monetizes traffic exclusively from North America, Europe and APAC." Sites without "a significant amount of traffic from these regions" may be denied. "We are unable to work with publishers located in the following countries: Myanmar, North Korea, Cuba, Sudan, Iran, and Syria" (https://skimlinks.com/program-policies/, n.d.).
  - Korea is not excluded.
- Payment:
  - [OFFICIAL] Threshold over $65, €55 or £50. "Publishers with US or UK bank accounts can be paid by direct deposit or PayPal"; others get PayPal only (https://www.skimlinks.com/insights/faq-skimlinks-payments/, n.d.). Commissions take about 90 days to clear.
- Revenue share:
  - [3P] 75/25.
- Amazon and existing links:
  - [3P snippet of help center] "As of March 31st, 2020, Skimlinks no longer works with Amazon as a Merchant".
  - Skimlinks "do[es] not overwrite any links that already have affiliate tracking", so our Amazon tags survive.
- Blogger:
  - Skimlinks has a Blogger install guide (3P mention). No evidence that blogspot is rejected.

**Howl (planethowl / howl.link)**
- [3P, Adweek] Howl "quietly sold the creator division of its business to Connexity … in August". "Some publishers say Howl still owes them money" (https://www.adweek.com/dealroom/howl-sells-creator-business-taboola-connexity/). Late payments are documented (https://www.adweek.com/media/affiliate-network-howl-late-payments-publishers/).
- howl.link now shows a creator waitlist.
- **Avoid.**

### 1.16 Networks (accounts to hold programs)

| Network | Non-US publishers | Payout to a Korean resident | Notes | Source |
|---|---|---|---|---|
| **Impact** | Yes (global partner base) | [OFFICIAL] "minimum payout threshold of $10 USD". International EFT (fee depends on currency) or **PayPal: "2% processing fee (up to $20…)"**. A country on wire becomes "FX Wire" with a fee | Non-US partners with US brands must file an electronic tax document (W-8BEN for individuals). One help page says this is due once earnings reach $2,000 in a US tax year; a snippet of another says no payout is released until the form is in. **File the W-8BEN at signup.** After 6 months without a way to pay you, Impact charges $10/month | https://help.impact.com/partner/…/how-do-partners-get-paid ; …/withdraw-funds-to-your-bank-account (n.d.) |
| **CJ** | Yes. [OFFICIAL] an active website with "a valid domain, and a top-level domain" | [3P] direct deposit or Payoneer at $50, check at $100; no PayPal | Brands: Wayfair, iRobot, Instant Brands, EcoFlow, Roborock | CJ support snippet; monetizepros (3P) |
| **Rakuten Advertising** | Yes (3P) | [OFFICIAL, 2020-05-05] "direct deposit payments to publishers in 74 countries" | Brands: Macy's, Dyson (3P), Anker (LinkShare link) | https://blog.rakutenadvertising.com/news/rakuten-advertising-publisher-payment-update/ |
| **Awin** (ShareASale merged into it) | Yes | [3P snippet of Awin wiki] minimum 20 USD/EUR/GBP, up to twice a month; refundable $1 sign-up check | ShareASale closed on 2025-10-06 | https://www.awin.com/us/news-and-events/awin-news/shareasale-to-awin-upgrade |
| **FlexOffers** | Yes (3P) | [OFFICIAL] "net 60"; there is a threshold, amount not stated. [3P] PayPal, Payoneer, bank; $25–$50 | Decline reasons include "Underdeveloped traffic sources", "Unestablished traffic sources" | https://supportbeta.flexoffers.com/knowledge/payment ; …/why-was-my-publisher-application-declined |
| **Partnerize** | Yes | [OFFICIAL blog] pays in "60+ currencies" to "214 countries and territories" | Brands: Bed Bath & Beyond; Chewy in the past | https://blog.partnerize.com/enhanced-partner-payments-interface-delivers-industry-leading-speed-and-transparency/ |

**Blogspot subdomains.** No network or retailer page we could read bans blogspot.com outright.
- CJ requires "a valid domain, and a top-level domain". **[INFERENCE]** acts39.blogspot.com should pass the URL format check, but reviewers often read a free subdomain as low-commitment.
- Target and Walmart reject "under construction" sites, and Target rejects sites without a privacy policy.
- **[INFERENCE]** A custom .com before applying to Impact brands and Sovrn/Skimlinks raises approval odds, and it avoids re-verifying every program later. If the switch is planned anyway, do it before applying.

---

## 2. Rules on mixing retailers

### 2.1 Amazon Associates allows it, with limits

Source: [OFFICIAL] Program Policies, "Updated: April 14, 2026", https://affiliate-program.amazon.com/help/operating/policies, and Operating Agreement, "Updated: October 15, 2025", https://affiliate-program.amazon.com/help/operating/agreement.

- **Other links are allowed.** Under the IP License, "parts of your Site that are not closely associated with the Program Content may contain links to sites other than an Amazon Site." Nothing prohibits other affiliate programs on the same site or page.
- **No Amazon content for other stores.** Participation Requirements 6(z): you will not use Program Content "to advertise or promote any products that are offered on any site that is not an Amazon Site". So do not use Amazon API images or data for the Walmart or brand-store button.
- **Price comparison rule.** Section 2(b): when Amazon prices appear in a "comparison" format alongside other sources, "you must display both the lowest "new" price and, if we provide it to you, the lowest "used" price". Amazon prices may be shown only via Amazon-served links or the Creators API or PA-API, with "a date/time stamp adjacent".
- **No double commissions.** Associates tags "should only be used to benefit from Amazon Associates commissions". There must be no attempt "to claim commissions from both Amazon Associates and another program using the same traffic".
- **No implied tie-ins.** 6(d) prohibits implying endorsement through "unrelated third-party materials in close proximity to Program Content". Each Amazon Mark must stand alone with spacing.
- **Disclosure.** "As an Amazon Associate I earn from qualifying purchases" must be stated "clearly and prominently" (Operating Agreement).
- **Practical pattern.**
  - Keep our current approach: no hand-typed Amazon price, and "Check price at Amazon".
  - Other retailers' prices may appear as text with source and date, as long as no Amazon price sits in the same comparison block.
  - Use our own photos or brand-press images for multi-retailer boxes, not Amazon API images.

### 2.2 Walmart and Target terms on appearing next to Amazon

- **Walmart:** no clause names Amazon. Exhibit A item 16 ("You may not place the Trademarks adjacent to competitive brands") and the ban on Walmart Trademarks next to "sale", "% off" and "coupons" are the relevant risks (§1.1).
  - **[INFERENCE]** Text buttons ("Check Walmart") are lower risk than Walmart logos next to an Amazon logo.
  - This only matters if we are bound by Walmart's agreement directly. Through a sub-network, Sovrn's or Skimlinks' terms and the merchant's network-level terms apply. Which merchant terms pass through: UNVERIFIED.
- **Target:** no anti-competitor placement clause found. The restrictions are paid search, link cloaking, price display (datafeed only) and scraping.
- **Best Buy:** only bans targeting competitors' brand names in search ads. Price display is banned.

---

## 3. What a new, low-traffic, non-US blogspot site can get into, ranked

| Rank | Program | Get in now? | Why |
|---|---|---|---|
| 1 | **Impact partner account** (free) | Yes | Global, $10 threshold, PayPal or international EFT, W-8BEN. It is a container: approval happens per brand |
| 2 | **Anker/Soundcore, Roborock, Dreame, EcoFlow, Levoit, SharkNinja, Chewy** (Impact brands) | Likely for some, now | Pages say "allows anyone to join" (Anker) or describe open review. Rates are 4–8% or more, cookies 7–35 days. **[INFERENCE]** Expect some declines until traffic exists; reapply in 60–90 days |
| 3 | **Sovrn Commerce** | Likely, after clicks | No traffic minimum, approval after real clicks, PayPal at $25, covers Walmart, Lowe's and others. Run on non-Amazon outbound links only |
| 3b | **Skimlinks** (if Sovrn declines; do not run both on the same links) | Likely if we have 10+ original posts | Clear content rule. PayPal-only payout at $65 is slower to reach |
| 4 | **Levanta** | Possible now; use after the Amazon review | Brands approve each creator. Higher rates on Amazon-sold third-party brands, but the same link cannot also carry our Associates tag |
| 5 | **CJ / Rakuten / Awin accounts** | Yes (accounts) | Only for specific brands (iRobot, Instant Brands, Wayfair on CJ; Dyson and Macy's on Rakuten; Jackery and Levoit on Awin) |
| 6 | **Home Depot, Lowe's, Wayfair, Kohl's** | Later | Low rates or 1-day cookies. Brand-new sites are often declined [3P]. Apply after a custom domain and about 5–10k monthly pageviews [INFERENCE] |
| 7 | **Amazon Creator Connections** | After Associates approval | Needs an active Associates account and reportedly a Creator Stars tier |
| 8 | **eBay Partner Network** | Unclear | Korea eligibility UNVERIFIED. 2–4% |
| — | **Walmart direct, Walmart Creator, Target direct** | **No** | US-based site or US-resident requirement, W-9 (Target), US bank (Creator) |
| — | **Best Buy** | Not worth it | 0–0.5%, no price display |
| — | **Costco** | No product program | Membership-only listing on CJ |
| — | **Howl** | Avoid | Payment problems, creator business sold |

**Suggested sequence for the next 60 days**
1. Week 1:
   - Decide on the custom domain now. If yes, switch first, because every program verifies the URL.
   - Add a privacy policy and a standing affiliate disclosure page (Target-style and Skimlinks checks look for these).
2. Week 1:
   - Open Impact and file the W-8BEN (Korea; treaty business-profits article; no US permanent establishment).
   - Apply to Roborock, Dreame, Anker, EcoFlow, SharkNinja, Levoit and Chewy. One network per brand.
3. Week 2:
   - Apply to Sovrn Commerce, install the JavaScript in the Blogger theme, and exclude amazon.com and existing tagged links.
   - Let it collect clicks for review.
4. After 3 Amazon sales and approval:
   - Check Creator Connections.
   - Try Levanta for Amazon-only brands, choosing one program per product.
5. At about 3 months, or 5–10k monthly pageviews:
   - Add CJ and Rakuten brands, Home Depot, Lowe's and Wayfair.
   - Re-check whether Walmart or Target can be reached through Sovrn's Merchant Explorer, which shows "approved countries" (3P referly).

---

## 4. Commission math for our categories

Amazon rates: [OFFICIAL] Standard Commission Income table, https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ (no date; © 1996-2025):
- Kitchen and Automotive: **4.5%**.
- Home, Home Improvement, Pets Products, Headphones, Lawn & Garden, Tools, Outdoors: **3%**.
- "All Other Categories": **4%**.
- Health & Personal Care: **1%**.

**[INFERENCE]** Which Amazon product group a given ASIN falls into (for example a robot vacuum as "Home" vs "Kitchen", or a power station as "Lawn & Garden" vs "All Other") shows only in the earnings report. Treat the mapping as an estimate.

| Category (example price) | Amazon | Walmart (via sub-network only) | Target | Best Buy | Home Depot | Best brand-direct option | Where it pays most |
|---|---|---|---|---|---|---|---|
| Robot vacuum ($400) | Home 3% = **$12** (24h) | Home 4% [3P], ×~0.75 via Sovrn ≈ $12 | Home 5–8% [3P], not reachable | 0–0.5% ≈ $0–2 | ~2% ≈ $8 (24h) | **Roborock 4–7% = $16–28 (35-day)**; Dreame ≥6% = $24+ (30-day); Shark "up to 20%" | **Brand direct** |
| Power station ($700) | likely 3–4% = **$21–28** (UNVERIFIED group) | Patio 4% / Electronics 1% [3P] | n/a | ~0–0.5% | ~2% | **EcoFlow ≥5% = $35+ (7-day)**; Anker SOLIX 5% = $35 (30-day); Jackery 5–8% [3P] | **Brand direct**, 30-day cookie preferred |
| Kitchen appliance (air fryer, $130) | Kitchen 4.5% = **$5.85** | Home 4% [3P] ≈ $3.90 net | 5–8% [3P], not reachable | — | — | **Ninja (SharkNinja) "up to 20%" ≈ up to $26** (actual tier unknown); Instant Brands ~1% [3P] | **Ninja direct**; otherwise Amazon |
| Pet supplies ($60 order) | Pets 3% = **$1.80** | Walmart pets: unclear [3P] | Pet care 0% [3P] | — | — | **Chewy** (Impact; [3P] $15 per new customer, older terms) | **Chewy** for new customers; Amazon for repeat buys |
| Car accessories (jump starter, $100) | Automotive 4.5% = **$4.50** | Auto not listed; tires excluded | — | — | — | NOCO 8% [3P] = $8 | Amazon is competitive; NOCO if approved |
| Bidets ($60 seat / $400 washlet) | Home Improvement 3% = **$1.80 / $12** | — | — | — | ~2% (24h) | Tushy ~4% [3P]; Brondell 4–5% [3P]; Levanta brand campaigns (15–25% claimed) | **Levanta** for Amazon-only brands (one program per link); otherwise Amazon |
| Earbuds ($80) | Headphones 3% = **$2.40** | Electronics 1% [3P] | Electronics 1% [3P] | 0–0.5% | — | **Soundcore (Anker) 8% = $6.40 (30-day)** | **Anker direct** |

**Reading the table**
- Big-box retailers pay the same as Amazon or less in every category we cover (Walmart 1–4%, Best Buy about 0%, Home Depot about 2%), and their cookies are as short (1–3 days).
- **[INFERENCE]** Their value to us is reader trust and price comparison, not higher commission.
- The higher rates are at the brands: robot vacuums, power stations, Ninja kitchen gear and Soundcore earbuds.
- Expected revenue still scales with traffic. At near-zero traffic, none of these numbers matter yet. The case for applying now is that approvals and verification take weeks.

---

## 5. How top product sites show multi-retailer buttons, and FTC requirements

### 5.1 Observed patterns

**Tom's Guide (Future plc)**
- Robot-vacuum guide, "last updated 5 October 2026" (https://www.tomsguide.com/us/best-robot-vacuums,review-2000.html, page source 2026-10-29).
- Disclosure directly under the byline: "When you purchase through links on our site, we may earn an affiliate commission. Here's how it works."
- Each pick has 2–3 buttons: "View at Amazon", "View at Best Buy", "View at Wayfair", "Check Best Buy", "Check Amazon".
- A price widget ("Round up of today's best deals") shows list and current prices with "View" and "See all prices", and the footer line "We check over 250 million products every day for the best prices".
- Prices come from an automated feed, not typed by writers.

**RTINGS**
- Disclosure: "Supported by you via membership, and when you purchase through links on our site, we may earn an affiliate commission." (https://www.rtings.com/vacuum/reviews/best/robot, fetched 2026-10-29).
- Its page config lists the US stores it can show: Amazon, BestBuy.com, B&H, Walmart.com, Target.com, HomeDepot.com, Lowes.com, Wayfair.com, Staples.com and others, plus "Prioritize Brand Store" (page source, 2026-10-29).
- Prices load dynamically.

**Wirecutter (NYT)**
- Pages are blocked to our tools. Secondary sources quote the standard line: "We independently review everything we recommend. When you buy through our links, we may earn a commission."
- The NYT help center says Wirecutter "may receive a commission" and editors are "never made aware of any business relationships with retailers" (https://thenewyorktimeshelpcenter.helpjuice.com/21869802882580-Wirecutter/21870729656596-Wirecutter-Product-Recommendations).
- [3P, Affiverse, 2026-03-11] Its "How We Make Money" page, updated 2026-03-03, says it links to the best retailer even when that retailer pays nothing.
- Wirecutter's exact "price at time of publishing" wording: **UNVERIFIED**.

**Hip2Save**
- Per-post disclosure under the byline, with a timestamped post (for example "Oct 28, 2026 @ 7:00 PM MDT"):
  - Non-Amazon post: "Hip2Save may earn a small commission at no extra cost to you via trusted partners and affiliate links in this post. Prices and availability are accurate as of time posted."
  - Amazon post: "As an Amazon Associate, Hip2Save earns a small commission from qualifying purchases in this post. Amazon prices and promotions are accurate at the time of posting and subject to change."
- Source: https://hip2save.com/deals/target-beauty-advent-calendar/ and https://hip2save.com/deals/amazon-pancake-syrup/, fetched 2026-10-29.
- Hip2Save shows Target prices. **[INFERENCE]** That suggests negotiated terms, or acceptance of the risk under Target §11.3.

**The Krazy Coupon Lady**
- Disclosure: "Most of the offers appearing on our site are from companies from which we receive compensation. We may receive a small payment from an affiliate if you click a link to purchase a product." (https://thekrazycouponlady.com/deals, 2026-10-29).
- Outbound links seen in the page source: Amazon with its own tag and Creator Connections `campaignId`, goto.walmart.com (Walmart on Impact), a CJ domain (tkqlhce.com), and creatorlink.shop.

### 5.2 FTC requirements (16 CFR Part 255, revised; 88 FR 48092, published and effective 2023-07-26)

**The rule** ([OFFICIAL] https://www.law.cornell.edu/cfr/text/16/255.5 and /255.0)
- §255.5(a): when a connection "might materially affect the weight or credibility of the endorsement, and that connection is not reasonably expected by the audience, such connection must be disclosed clearly and conspicuously."
- Example 11 (coffee-maker blog with affiliate links): "the reviews should clearly and conspicuously disclose the compensation."
- §255.0(f): "clear and conspicuous" means "difficult to miss (i.e., easily noticeable) and easily understandable by ordinary consumers". On the internet "the disclosure should be unavoidable".

**FTC FAQ** ([OFFICIAL] https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking, n.d.; reflects the 2023 revision)
- Example wording: "I get commissions for purchases made through links in this post." "The closer the disclosure is to your recommendation, the better."
- "Consumers might not understand that 'affiliate link' means that the person placing the link is getting paid". "a 'buy now' button would not be adequate."
- "'Paid link' right next to an affiliate link should be an adequate disclosure".
- "'Commissionable link' is probably not a clear disclosure."
- "A single disclosure on your home page won't be sufficient". Hyperlinked "disclosure" buttons are "easily avoidable".

**[INFERENCE] Template for Verdict Picks.** This meets the FTC rules and the Amazon, Target, Walmart and Best Buy wording at once.
- Top of every post, above the first link and above the fold (Best Buy):
  > *We earn commissions when you buy through links on this page, from Amazon (as an Amazon Associate I earn from qualifying purchases) and other retailers and brands. Prices and availability are as of [Oct 29, 2026, 9:00 AM ET] and can change.*
- Next to each button group, a small label "(paid links)". Button text should not say only "Buy now".
- If Target is ever joined directly, add its prescribed sentence. If Walmart is joined directly, add "#WalmartPartner" or "paid link" next to each Walmart link.
- Keep the standing disclosure page as well. On its own it is not enough.

---

## 6. Open questions to check after logging in

1. Sovrn Merchant Explorer and the Skimlinks Hub: are Walmart, Target, Home Depot and Best Buy shown as "approved" for a Korea-resident publisher or a US-traffic site? What are the net rates?
2. Impact "Supported Currencies": is KRW available by EFT, or only FX Wire? Compare the cost with PayPal (2%, capped at $20) and a USD account (Payoneer or Wise).
3. The actual tier each brand assigns (SharkNinja "up to 20%" and eufy "7–20%" are ceilings).
4. Levanta creator payouts to Korea through Stripe, and whether Levanta accepts non-US creators.
5. EPN country eligibility for Korea.
6. Whether Amazon credits our robot vacuums, power stations and bidets as Home, Home Improvement, Lawn & Garden or All Other (earnings report → product groups).
