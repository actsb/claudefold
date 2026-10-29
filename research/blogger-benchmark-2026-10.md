# Blogger benchmark: the biggest live Blogger sites and what Verdict Picks should copy

Researched 2026-10-29 for Verdict Picks (https://acts39.blogspot.com). Every site in the "verified" tables was fetched on 2026-10-29.

## Evidence key

- **[P] Primary.** I fetched it myself on 2026-10-29: the site's HTML, its Blogger JSON feed (`/feeds/posts/default?alt=json`) or a page on the site.
- **[3P] Third-party estimate.** Similarweb, Semrush, Kochava or Feedspot numbers. These are modelled estimates and are often badly off for small sites. Treat them as orders of magnitude only.
- **[SR] Self-reported.** The site's own media kit, About page or blog post.
- **[2ry] Secondary.** News coverage, listicles or blog posts about the site.
- **Similarweb figures.** Unless noted, these are "Total visits, last 3 months" from the free page at `similarweb.com/website/<domain>/`, data month September 2026, fetched 2026-10-29. Dividing by 3 gives a rough monthly figure.

### How Blogger was verified
The strongest marker is the site's own feed at `/feeds/posts/default?alt=json`, which returns an Atom id of the form `tag:blogger.com,1999:blog-<numeric id>`. Only Blogger serves this. Supporting markers were:
- `<meta content='blogger' name='generator'/>`
- `www.blogger.com/static/v1/widgets/...widgets.js`
- images on `blogger.googleusercontent.com`
- Blogger URL patterns (`/YYYY/MM/slug.html`, `/p/page.html`, `/search/label/...`)

Feed-derived numbers are also primary: total post count (`openSearch$totalResults`) and posts per month (from `published` dates).

---

## TL;DR (top findings)

1. **Big US deal, coupon and product-review sites essentially no longer run on Blogger.** I collected 412 blog domains from 10 Feedspot 2026 lists (coupon, Amazon deals, product reviews, giveaways, mom, home decor, gadgets, gift ideas, freebies, money-saving) and machine-checked them. About 2% are Blogger, and WordPress was detected on at least 237 of the 377 not already checked by hand. I also hand-checked about 100 well-known US deal, coupon, DIY and food blogs. Hip2Save, Krazy Coupon Lady, Money Saving Mom (blocked by Cloudflare), Living Rich With Coupons, Southern Savers, Freebie Guy, Passionate Penny Pincher, Kroger Krazy and Totally Target are all off Blogger, mostly on WordPress with Mediavine or Raptive ads [P].
   - Hip2Save itself **started on Blogspot in 2008 and moved to WordPress in 2009 after "Blogspot took the blog offline"** [SR]. It now self-reports 10.8M+ sessions a month and 251K+ email subscribers (2026 media kit) [SR].
2. **The Blogger survivors that earn from US shopping are mid-size creator blogs, not "best X" review sites.** Examples:
   - Thrifty Decor Chick: home DIY plus shopping finds.
   - Dimples and Tangles: home and fashion with LTK and Amazon picks.
   - Product Review Mom: reviews, deals, gift guides and make-money posts.
   - I Should Be Mopping the Floor: free printables and fonts plus "finds" posts.
   - Mommy's Kitchen: recipes.
   - Smaller blogspot-subdomain giveaway and review blogs: New Age Mama, icefairy's Treasure Chest, Razzle Dazzle Styles.
3. **Premium ad networks do run on Blogger, but only on custom domains** [P]:
   - Raptive (AdThrive): Thrifty Decor Chick, Dimples and Tangles, I Should Be Mopping the Floor.
   - Mediavine: Product Review Mom, Amusing Planet.
   - Monumetric: Mommy's Kitchen.
   - Playwire: SpoilerTV.
   - Every blogspot-subdomain site in the sample runs only AdSense, sometimes with Skimlinks.
   - Raptive's minimum is now **25,000 pageviews a month** (since October 2025). Mediavine's Journey tier is **1,000 sessions a month** (since 2026-01-15) [2ry/SR].
4. **Their revenue stack is ads plus creator-commerce links plus a personal brand, not Amazon Associates alone:**
   - Thrifty Decor Chick: LTK (`on.ltk.com`) links to Walmart, plus Amazon and Target storefronts.
   - Dimples and Tangles: LTK "Shop my IG", 28 `amzn.to` links in one Prime Day post, Walmart hauls, a Flodesk newsletter.
   - Product Review Mom: Amazon Associates, `link.amazon` links, brand-direct links and sponsored reviews.
5. **Their content is short, personal and photo-led.** Feed median length is about 300–1,100 words, with the author's own photos (blogger.googleusercontent.com), seasonal and sale-event timing (Prime Big Deal Days, Walmart deals, holiday decor) and recurring series ("Five Friday Favorites", "Wednesday Whimsy", monthly menu plans).
   - Verdict Picks' public feed has a median of about 6,000 words per post. It uses press photos and has no named person or own photos [P].
6. **Returning-reader engines are email and Pinterest, with comments a distant third.**
   - Pinterest is the top social referrer Similarweb lists for Thrifty Decor Chick, I Should Be Mopping the Floor, Mommy's Kitchen and Dimples and Tangles [3P].
   - Email runs on FeedBlitz, Mailchimp, Flodesk or follow.it, because Blogger's own FollowByEmail widget was shut off in July 2021 [SR, Google].
   - **Verdict Picks has no working email form.** Only Contempo's FollowByEmail CSS is present [P].
7. **Even Google is leaving Blogger for its own blogs.** On 2026-10-29, `blog.chromium.org`, `security.googleblog.com` and `adsense.googleblog.com` all 301-redirect to `blog.google`. Their last Blogger posts are dated March and April 2026 [P].
   - Android Developers, Workspace Updates and Chrome Releases are still on Blogger [P].
   - I found no announcement of the move.

---

## 1. The 24 biggest live Blogger sites, verified 2026-10-29

Sorted roughly by third-party traffic. "Marker" is the Blogger blog id from the site's own feed. Monetization was detected from homepage HTML: ad-script names and affiliate domains.

| # | Site | Niche | Marker (feed blog id) | Third-party traffic | Top channel / social [3P] | Posting rate [P] | Monetization seen [P] |
|---|---|---|---|---|---|---|---|
| 1 | https://thehackernews.com | Cybersecurity news (India-run, US audience) | blog-4802841478634147276; 17,641 posts; behind Cloudflare | Similarweb 4M (3 mo, Sept 2026). Semrush: 2.3M Jul, 1.85M Aug, 1.87M Sept 2026 (updated 2026-10-13). Earlier self-report: more than 4M unique monthly readers (2015) | Direct 48.9% (SW); Direct 45.3%, Google 29.2% (Semrush); social: X, then LinkedIn and Facebook | ≥150 posts in Sept 2026 (feed cap; Blogger reports ~249) | Google Ad Manager (googletag), sponsored/webinar content, newsletter |
| 2 | https://www.irasutoya.com | Free clip-art illustrations (Japan) | blog-8749391503645026985; 25,424 posts | SW 2.8M (3 mo); 86.6% Japan | Organic search 74% | Few new posts (9 in Aug 2026) | AdSense (28 ad units on homepage) |
| 3 | https://www.gossiplankanews.com | Sri Lanka gossip/news | blog-4779058738889857399; 57,611 posts | SW 2.3M; 82.6% Sri Lanka | Direct 59.8%; Facebook, WhatsApp | ≥150 in Sept 2026 (Blogger reports ~550) | AdSense, Taboola, GAM |
| 4 | https://www.indgovtjobs.in | Indian government job alerts | blog-7242213784467625673; 16,111 posts | SW ~2M; 98% India | Direct 43.8% | ~128–157 in Sept 2026 | AdSense, vdo.ai |
| 5 | https://www.padasalai.net | Tamil Nadu education news | blog-4039164633152506177; 107,593 posts | SW 1.4M; 97% India | Organic 63.6% | ≥150 in Sept 2026 | AdSense |
| 6 | https://www.lankacnews.com | Sri Lanka news | blog-3005203787208851684 | SW 1.4M; 82.7% Sri Lanka | Organic 61.1% | ≥150 in Sept 2026 | AdSense, Infolinks, Ezoic tag |
| 7 | https://www.kalviseithi.net | Tamil Nadu education news | blog-4194027626261768144; 69,233 posts | SW 197.4K; 41% India | Organic 48.6% | ≥150 in Sept 2026 | AdSense (heavy: 211 `adsbygoogle` hits) |
| 8 | https://www.amusingplanet.com | Curiosities, travel, history | blog-8890523669575867377; 5,215 posts | SW 179.1K; 48.5% US | Organic 51.4%; Reddit, Quora, YouTube | 6–10 posts/month | Mediavine (`scripts.mediavine.com/tags/amusing-planet.js`), Taboola |
| 9 | https://www.spoilertv.com | TV news and spoilers | blog-29964715; 183,280 posts | SW 158.1K; 37% US | Direct 61.1%; Facebook, X, Reddit | ≥150 in Sept 2026 | Playwire, GAM, AdSense |
| 10 | https://www.nieniedialogues.com | US mom/family diary | blog-16611152; 3,468 posts | SW 108.2K; 32% US | Direct 84.7% | 13–25 posts/month | No ad script detected |
| 11 | https://www.thriftydecorchick.com | US home DIY and decor + shopping finds | blog-7781670590071996754; 1,586 posts | SW 70.3K (3 mo); 82% US. Kochava: "104k visitors" (no period) and "3.02K estimated visits" in the same profile, i.e. unreliable | Organic 62.8%; **Pinterest**, then Facebook | 5–9 posts/month | Raptive (AdThrive) + Raptive affiliate script, LTK, Amazon and Target storefronts |
| 12 | https://www.stelladimokokorkus.com | Nigerian celebrity gossip | blog-352385313518803988; 123,017 posts | SW 67.1K; country split looks implausible (75% "US") | Direct 81.8% | ≥150 in Sept 2026 | Infolinks, GAM |
| 13 | https://www.ishouldbemoppingthefloor.com | US free printables, fonts, crafts + "finds" | blog-6127662372199652126; 2,226 posts | SW 64.7K; 74.5% US | Organic 51.2%; **Pinterest** | 0–5 posts/month (slowing) | Raptive (AdThrive), Amazon (`amzn.to`), Etsy shop |
| 14 | https://www.mommyskitchen.net | US home cooking and canning | blog-8390396285139687239; 1,332 posts | SW 52.5K; 83.9% US | Organic 68.3%; **Pinterest**, then Facebook | 2–5 posts/month | Monumetric |
| 15 | https://www.digitalinformationworld.com | Tech and social media news | blog-5050352549609773373; 30,851 posts | SW 35.3K (looks low) | Direct 39.6% | ~85 in Sept 2026 | AdSense, MGID |
| 16 | https://www.productreviewmom.com | US product reviews, deals, gift guides, survey/side-income | blog-6150555444999938303; 896 posts | SW 18.2K; 90.5% US (desktop) | Direct 44.1%; Affiliate is 3rd channel | 7–10 posts/month | Mediavine, Amazon Associates, brand affiliates, sponsored |
| 17 | https://android-developers.googleblog.com | Google developer blog | blog-6755709643044947179 | googleblog.com overall: SW global rank #24,809 (no visits shown) | Direct 43.3% (googleblog.com) | 5–13 posts/month | None (Google) |
| 18 | https://workspaceupdates.googleblog.com | Google Workspace changelog | blog-5245696872621940063 | (as above) | n/a | 40–52 posts/month | None |
| 19 | https://chromereleases.googleblog.com | Chrome release notes | blog-8982037438137564684; 6,460 posts | (as above) | n/a | 39–61 posts/month | None |
| 20 | https://www.atlasofwonders.com | Travel curiosities (sister site of Amusing Planet) | blog-4627375674293405544 | Not checked | n/a | ~1 post/month | Mediavine tag present |
| 21 | https://www.sarkarinaukriblog.com | Indian job alerts | blog-30026366; 19,344 posts | Not checked | n/a | 8–10 posts/month | n/a |
| 22 | https://foodwishes.blogspot.com | Chef John recipe videos (YouTube-led) | blog-7173052990851751381; 3,022 posts | Subdomain; no SW data | n/a | 1–2 posts/month | AdSense; YouTube is the main business |
| 23 | https://newagemama.blogspot.com | US reviews, giveaways, free Kindle books, unboxings | blog-377194681452174571; **16,696 posts** | Subdomain; no SW data. Feedspot: X/Twitter 21.4K | n/a | ~30 posts/month (daily) | AdSense, Skimlinks, Amazon |
| 24 | https://icefairystreasurechest.blogspot.com | US family reviews and giveaways (book blog tours) | blog-8926522047608644233; 3,752 posts | Subdomain. Feedspot: Facebook 20.6K, X 16.6K | n/a | 2–10 posts/month | AdSense, Amazon, Walmart, Narrativ, Awin, ShareASale, Rafflecopter |

Also verified as Blogger but small or inactive:
- https://razzledazzlestyles.blogspot.com: giveaways and reviews, 2,258 posts, 3–15 posts/month, AdSense and Amazon.
- https://martinfamilymoments.blogspot.com: family diary, 2,573 posts.
- https://www.dimplesandtangles.com: deep dive below. No Similarweb visit number shown; 85% US; Pinterest is the top social referrer.
- Inactive or near-inactive Blogger sites: calculatedriskblog.com (last Blogger post 2026-01-12; readership moved to Substack), thelifeofjenniferdawn.com (last post 2018), multimillionaireroad.com (last post 2024-11), classicalhomemaking.com, hyperboleandahalf.blogspot.com, gregmankiw.blogspot.com, kenlevine.blogspot.com, cliffmass.blogspot.com, strobist.blogspot.com, googlemapsmania.blogspot.com, design-seeds.com, lunchboxdad.com (last post 2025-11).

Excluded on purpose:
- Several high-traffic Blogger sites in Wappalyzer's 2026 "top Blogger sites" list are piracy or anime-streaming sites, such as anichin.cafe, kusonime.com and ovagames.com (https://www.wappalyzer.com/technologies/blogs/blogger, fetched 2026-10-29). They are not useful models.

### Where the candidates came from
- The Blogspot 100 (2012 data, republished 2014): https://ypmb.blogspot.com/2014/02/the-blogspot-100-top-blogger-sites.html. I used it to find historic big Blogger sites and then checked which are still on Blogger.
- Wappalyzer, Hunter.io and WebTechSurvey "sites using Blogger" lists, all fetched 2026-10-29:
  - https://www.wappalyzer.com/technologies/blogs/blogger (claims 270,000 tracked sites)
  - https://hunter.io/technologies/blogger
  - https://webtechsurvey.com/technology/blogger
  - BuiltWith required verification and was not readable.
- Feedspot 2026 lists:
  - https://bloggers.feedspot.com/coupons_blogs/
  - https://bloggers.feedspot.com/amazon_deal_blogs/
  - https://bloggers.feedspot.com/giveaway_blogs/
  - https://bloggers.feedspot.com/product_review_blogs/
  - https://bloggers.feedspot.com/home_decor_blogs/
  - https://bloggers.feedspot.com/mom_blogs/
  - https://bloggers.feedspot.com/money_saving_blogs/
  - plus the gadget, gift_ideas and freebies lists
- I could not find a "Blogger featured blogs" showcase from Google in 2026.

---

## 2. Former Blogger sites that migrated (and what that teaches)

| Site | Then | Now (verified 2026-10-29 [P]) | When / why | Source |
|---|---|---|---|---|
| Hip2Save (hip2save.com) | Started on Blogspot, 2008 | WordPress (wp-content) | **2009: "Blogspot took the blog offline"; she "panicked" and rebuilt on WordPress within days** [SR] | https://hip2save.com/2018/06/26/hip2saves-sweetest-memories-over-the-past-decade/ (2018-06-26) |
| Hip2Save today, as a benchmark | n/a | 2026 media kit claims [SR]: 10.8M+ shopper sessions/month, 251K+ opt-in email, 58K+ opt-in SMS, 2.2M+ social followers, 2.1M+ monthly Pinterest reach, 100,000 pieces of content a year, 91% US, 79% mobile, app rated 4.9 from 17K reviews | n/a | https://hip2save.com/wp-content/uploads/2026/03/2026-Hip-Happenings-Media-Kit-Packet.pdf (March 2026) |
| Linda Ikeji's Blog (Nigeria) | Blogspot from 2007, then a custom domain still on Blogger (2015 and 2016 reports) | WordPress (wp-content) | Move date not found | https://techpoint.africa/2015/10/01/linda-ikejis-blog-new-domain-name (2015-10-01); https://en.wikipedia.org/wiki/Linda_Ikeji |
| PostSecret | #1 in the Blogspot 100 (2012 data) | WordPress | Not found | Blogspot 100 list above |
| Cup of Jo (joannagoddard.blogspot.com) | #4 in the 2012 list | WordPress with ad network | Not found | same |
| Skinnytaste, Budget Bytes (budgetbytes.blogspot.com), Closet Cooking, The Graphics Fairy, Mod Podge Rocks, IKEA Hackers, Carscoop(s), Dumb Little Man, BLDGBLOG, Joe.My.God, Mish (now mishtalk.com) | All in the 2012 Blogspot 100 | All WordPress | Budget Bytes' founder discusses "why she switched from Blogger to WordPress" in a Food Blogger Pro episode (undated) | https://www.foodbloggerpro.com/blog/article/making-the-leap-to-full-time-blogging-with-beth-moncel-from-budget-bytes-fb/ |
| Cake Wrecks | Blogger era | Squarespace | Not found | [P] |
| Writer Beware | Blogger | WordPress, 2022-03-22 | "much greater flexibility in terms of design, control, and ease of use" | https://victoriastrauss.com/2022/03/22/the-writer-beware-blog-has-moved/ |
| Calculated Risk | Blogger (still exists) | Main readership on Substack. Similarweb shows only 8.3K visits over 3 months for calculatedriskblog.com; last Blogger post 2026-01-12 [P] | Newsletter model | [P] + Similarweb |
| Free Technology for Teachers | Blogger | Homepage meta-refreshes to freetech4teach.teachermade.com (WordPress) | Blog owned by TeacherMade; Richard Byrne "moving on from daily blogging" (date not found) | https://freetech4teach.teachermade.com/?p=35748 |
| Google Chromium, Online Security and AdSense blogs | Blogger (googleblog.com) | 301 to blog.google/chromium/, /security/, /products/adsense | Last Blogger posts March and April 2026; no announcement found | [P] |
| The Coupon Challenge (coupon blog) | Blogger | WordPress | Wrote a series on the cost and adjustment of moving | https://www.thecouponchallenge.com/?p=4755 |

**Lessons from the migrations:**
- (a) Blogger is a fine place to *start*, but nearly every site that became a large US deal or review business left. Typical reasons: design and control, plugins, ad-network and SEO tooling, platform risk, and email.
- (b) Platform risk is real. Hip2Save was taken offline in 2009. In August 2026 a wave of Blogger blogs got removal notices citing malware/Community Guidelines with an 89-day deletion countdown, reported as false positives (https://ppc.land/blogger-owners-face-89-day-deletion-clock-as-google-malware-flags-misfire/; https://www.bleepingcomputer.com/news/google/google-blogger-locks-hundreds-of-blogs-in-malware-false-positive/amp/ [2ry]).
- (c) Sites that stayed on Blogger *and* earn well all use a **custom domain**. That makes a later platform move painless: same domain, 301s possible, and ad-network approval.

---

## 3. Deep dives: US shopping, product and home sites on Blogger (8 sites)

All [P] unless marked. "Feed words" is the median word count of the last 30 posts in the full-content feed. That is roughly the body text without the theme.

### 3.1 Thrifty Decor Chick: https://www.thriftydecorchick.com (best overall model)

- **Who / since:** Sarah (Saucedo), started spring 2008, full-time since mid-2009 [SR] (https://thriftydecorchick.com/p/about-me.html; Raptive creator page https://raptive.com/keepitreal/creators/sarah-saucedo/, about Sept 2024).
- **Platform:** Blogger on a custom domain, with a custom responsive template ("Design by Code&Blog"). Homepage is 96 KB HTML with 20 scripts, 4 of them external.
- **Above the fold:** Logo banner, then a mega-menu: Our Home / DIY AND HOME / Decorating / Lifestyle / **Shop** ("Shop Our Whole House", "My Amazon Storefront", "My Target Storefront", "My Best Home Finds"). Below that are the newest post card, social icons (Facebook, Subscribe, Instagram, Pinterest, YouTube), and a sidebar with a welcome photo and bio, Popular Posts and a big label cloud.
- **Homepage:** Six post cards (thumbnail, excerpt, "Read the full post"), then "Older posts".
- **Posting:** 1,586 posts in total. 5–9 posts a month over Dec 2025–Oct 2026. Median about 325 feed words. Median 2 comments per post, max 34.
- **10 recent titles:**
  - The Best New Walmart Christmas Holiday Decor Finds!
  - An EASY Fix to Keep Couch Cushions From Sliding Everywhere
  - A New DIY Coffee Table: From Store Bought to Family Heirloom!
  - Non-Traditional Decorating Ideas for a Cozy Fall Home
  - FREE Fall Artwork for Autumn Decorating {25 Options!}
  - My Home, Beauty and Fashion Favorites {Prime Day Deals!}
  - Our Full and Beautiful Fall Mantel {Free From the Yard!}
  - Beyond the Mum: Fall Container and Window Box Ideas
  - A Tour of The Biggest Organization Transformations in Our Home!
  - Welcoming Fall: Simple and Delicious Pumpkin Bread Recipe
- **Top labels (last 81 posts):** DIY 37, before and after 25, solutions 24, **shopping 14**, molding 13, decorating 12.
- **Product links:** In the Walmart Christmas post, 17 inline text links go to **`on.ltk.com`** (LTK links resolving to Walmart). There are no buttons, no price tables and only 2 `$` mentions. Products appear in her own in-store or in-home photos, all on blogger.googleusercontent.com. The Prime Day post is a curated "favorites" list.
- **Ads and affiliate tech:** Raptive/AdThrive (`adthrive-ads-...-manual`), the Raptive affiliate link script (`affiliate-cdn.raptive.com/affiliate.mvp.min.js`), and a CafeMedia video player.
- **Disclosure:**
  - In-post: "This post may contain affiliate links for your convenience… I may earn a small commission".
  - "Blog Policies and Disclosure" page (https://www.thriftydecorchick.com/p/blog-policies.html): "As an Amazon Associate I earn from qualifying purchases". It names CafeMedia as ad partner and says sponsored content "will be clearly identified".
- **Email:** A FeedBlitz form on a "Subscribe to TDC" page ("No spam, EVER") (https://www.thriftydecorchick.com/p/blog-page.html).
- **Followers [3P Feedspot]:** Facebook 128.3K, Instagram 114.4K, DA 53 (https://bloggers.feedspot.com/home_decor_blogs/).
- **Traffic [3P]:** Similarweb 70.3K visits over 3 months (Sept 2026), 82% US, organic search 62.8%, Pinterest the top social source. Being on Raptive implies at least 25K pageviews a month today (more when she joined); this is an inference.
- **Returning-reader drivers:** Home "series" (house tours, before-and-afters, seasonal mantels), free printable art, comments, and a long-running personal voice. She wrote about blog decline in 2015: bloggers leaving for Instagram, falling comments, Facebook reach pay-walled (https://www.thriftydecorchick.com/2015/01/where-have-all-blogs-gone.html).

### 3.2 Dimples and Tangles: https://www.dimplesandtangles.com (closest "deals + finds" model on Blogger)

- **Who:** Jennifer Griffin, Oklahoma (disclosure page https://www.dimplesandtangles.com/p/disclosures.html).
- **Platform:** Blogger on a custom domain, template by Balkeni Studio, behind Cloudflare. Homepage is 127 KB with 34 scripts.
- **Above the fold:** Menu (About, Home Tours, Seasonal Tours, DIY, Before And After, Tutorials, Tablescapes, Mantles, Crafts, Fashion, Recipes, Event Decor, Travel, Family, **Shop**, Contact). Below it is a row of four image tiles: Seasonal Tours, DIY, Tablescapes and **"Shop my Ig"**, which goes to an LTK storefront. Then a site-wide line "This Post May Contain Affiliate Links. Please Read Our Disclosure Policy", then post excerpts with "CONTINUE READING »". The sidebar has social icons, a Blog Archive with counts and an Atom feed link.
- **Posting:** 1,418 posts in total. Lumpy rate: 9 in Nov 2025, 1 in Sept 2026, 9 in Oct 2026. **Median about 1,100 feed words**, median 6 comments.
- **10 recent titles:**
  - THE BEST NEWS!!!
  - FIVE FRIDAY FAVORITES
  - IT'S SWEATER WEATHER! MY FALL HAUL OF COLORFUL AND NEUTRAL FAVORITES
  - 2026 FALL HOME TOUR || FRONT PORCH
  - WALMART HAUL TRY ON- BUDGET FRIENDLY FINDS YOU'LL LOVE!
  - MY TOP 25 PERSONAL FAVE AMAZON PRIME BIG DEALS- SALE ENDS TODAY!
  - MY WALMART DEALS SALE PICKS- HOME, FASHION, AND GIFT IDEAS
  - FIVE FRIDAY FAVORITES
  - NATIONAL PARKS ROAD TRIP 2026 PART 1- MOUNT RUSHMORE…
  - WHAT I WORE LATELY || CLOSET CHRONICLES {3}
- **Labels:** Fashion 35, **Shopping 20**, Seasonal Tour 20, **Five Friday Favorites 15**, **Sales 10**, Gift Ideas 6. Other categories include "Deal Alert!", "Shop My Home" and "Sponsored post".
- **Product links:**
  - The Prime Day post has **28 `amzn.to` links** plus a "Shop all of my Amazon" folder link. Each item gets a short personal paragraph ("I've had this shawl wrap for years…") and her own photo.
  - The Walmart try-on haul has **76 `on.ltk.com` links**, 19 own photos and 8 `$` price mentions.
  - No "price at time of posting" disclaimer was found. Urgency comes from the title ("SALE ENDS TODAY!").
- **Ads, affiliate and email:** Raptive/AdThrive with the Raptive affiliate script. A Flodesk newsletter (`view.flodesk.com`) is linked in posts. Snapwidget shows an Instagram feed.
- **Traffic [3P]:** Similarweb shows no visit total; 85% US, organic search 36.1%, Pinterest the top social source. Follower counts were not found from a reliable source.

### 3.3 Product Review Mom: https://www.productreviewmom.com (closest "reviews" model on Blogger)

- **Who:** "Lou" (Louida Martin), LM Marketing, LLC, Atlanta.
- **Platform:** Blogger on a custom domain. The custom landing-style homepage is 108 KB.
- **Above the fold:** A hero, "Hey! I'm Lou, Your Go-To for Honest Reviews", with the author photo and an "Explore My Reviews" button, then an **"AS SEEN IN" row (Dr. Oz, Woman's World, First For Women, CNBC)**. Below that: Featured Posts, "Explore By Category" tiles (Beauty, Travel, Fashion, Food, Cars, Money), About, Latest from the Blog, and an email box "✨ Stay in the Loop!" (follow.it detected in HTML).
- **Menu:** Categories (Travel, Cars, Money, Beauty, Gift Guide), About Lou, **Advertise**, Start A Blog, Get Paid to Test Products, Disclosure, Contact Lou. The footer links a sitemap page.
- **Posting:** 896 posts in total; a **steady 7–10 posts a month for 12 months**. Median about 574 feed words; comments near 0.
- **10 recent titles:**
  - Spooktacular Halloween Events Across the U.S. You Can't Miss!
  - STIR Medley: A Culinary Gem in Johns Creek!
  - YouGov Review: Make Money While Influencing the News
  - Vital Red Light Review: The Best Red Light Therapy Device at Home
  - How to Join LifePoints Consumer Panel
  - Get Anime Costume Ideas for Halloween & Cosplay
  - Skincare Deals for Amazon Prime Day: K-Beauty and French Favorites
  - Testing Apps and Services for Cash: How Gemsloot Works
  - Fall Skincare Guide: 5 Easy Steps for Hydrated, Glowing Skin
  - Dippity-Do Girls with Curls Review: Affordable, Soft, and Defined Curls
- **Labels:** Must-Have 60, Beauty 33, Beauty Product Reviews 31, Atlanta 28, Make Extra Money 28, Paid Surveys Review 24, Gift Guide 16.
- **Content refresh:** The feed shows "Get Anime Costume Ideas…" re-published 2026-10-12, but its URL is `/2017/10/…`. Old seasonal posts get re-dated each year.
- **Product links:**
  - The Prime Day skincare post lists 18 products, each with "**X% OFF Sale Price: $Y**", her own product photos (19) and 18 `link.amazon` links. No "prices may change" disclaimer was found.
  - The red-light review (797 words) links 5 times to the brand's own site, shows "Price: $299" and uses 7 own photos. It is likely a brand partnership; no in-post sponsorship line was found by my text scan.
- **Ads:** Mediavine (`scripts.mediavine.com/tags/product-review-mom.js`).
- **Disclosure:** A site-wide statement: "a participant in the Amazon Services LLC Associates Program…" and "an affiliate marketer for different brands and may earn an commission on sign ups and sales".
- **Followers [3P Feedspot]:** Facebook 2.2K, X 4.3K, Instagram 11.8K, DA 32 (https://bloggers.feedspot.com/product_review_blogs/).
- **Traffic [3P]:** Similarweb 18.2K visits over 3 months (Sept 2026), 90.5% US (desktop); top channels Direct 44%, Organic, then **Affiliate**. Mediavine membership suggests real traffic is higher than Similarweb shows; this is an inference.

### 3.4 I Should Be Mopping the Floor: https://www.ishouldbemoppingthefloor.com (freebies as traffic engine)

- **Platform:** Blogger on a custom domain, classic "Simple" template, 84 KB.
- **Navigation:** Image-button menu (Homepage, Projects and Crafts, **Free Fonts**, **Free Printables and SVG Files**, Printables → Etsy shop, Journals and Planners, Facebook Covers and Device Wallpapers, Get Organized).
- **Sidebar:** About, "Subscribe to the Newsletter" (Mailchimp: `…us6.list-manage.com`, on https://www.ishouldbemoppingthefloor.com/p/sign-up-for.html), social icons and font promos.
- **Posting:** 2,226 posts in total; now 0–5 posts a month. The feed is summary-only (about 65 words).
- **10 recent titles:**
  - Free October Leaf Wallpapers
  - Fall Artistic Wallpapers for All Devices
  - Free Summer Sunflower Wallpapers
  - Wednesday Whimsy: Floral Kitchen Finds
  - Wednesday Whimsy: Adorable Lemon Finds
  - Free Summer Watermelon Wallpapers
  - Wednesday Whimsy: Cute Summer Tops
  - Free Spring Bird Wallpapers
  - Wednesday Whimsy: Kitchen Towels
  - Free Printable Champagne Gift Tags
- **Product links:** The "Wednesday Whimsy" shopping posts (about 511 words) open with "This post for floral kitchen finds contains affiliate links. I make a small percentage when these links are used, at no additional cost to you." They contain 28 `amzn.to` links, with items grouped by category (small appliances, textiles) and a one-line personal take each.
- **Ads:** Raptive/AdThrive.
- **Traffic [3P]:** Similarweb 64.7K over 3 months, 74.5% US, organic 51.2%, Pinterest the top social source.
- **Lesson:** Years of free printables, fonts and wallpapers built evergreen Pinterest and search traffic and an email list. Shopping roundups are layered on top of that audience.

### 3.5 Mommy's Kitchen: https://www.mommyskitchen.net

- Blogger on a custom domain, 269 KB homepage.
- **Ads:** Monumetric ad slots (`<!--MONUMETRIC [BTF|Pos 2]…-->`).
- **Social:** Pinterest, Facebook, Instagram, YouTube and TikTok links; heavy newsletter prompts (78 "newsletter" mentions).
- **Posting:** 1,332 posts; 2–5 a month. Recurring **monthly menu plan with free printable** ("October Menu Plan", "September Menu – Free Printable Monthly Menu Plan").
- **Traffic [3P]:** Similarweb 52.5K over 3 months, 83.9% US, organic 68.3%; Pinterest then Facebook.
- **Lesson:** A recurring monthly utility post plus a printable brings readers back on schedule.

### 3.6 New Age Mama: https://newagemama.blogspot.com (blogspot subdomain, high volume)

- **Size and rate:** 16,696 posts; about 30 posts a month (daily).
- **10 recent titles:** "The Slasher Experience… is #FREE on Amazon for Halloween", "Jessica is FREE for Halloween", "Unclaimed Mail from Fun Delivered – Stone Bracelets & Phone Cases", "Triumvirate is FREE on Amazon for Halloween!", "Michael's Mystery Box – Flowers & Trays", "Falling Star is Now Available on Audio", "TikTok Mystery Box from Hot Mystery Box", "Unclaimed Mail… Pink Shirt & Bath Bombs", "Player eBook FREE – Read Along on Audible!", "Unclaimed Mail… Mic & Pore Clay Stick".
- **Format:** Short posts (about 193 feed words). Labels: mystery box 72, unboxing 50, Books 45.
- **Monetization:** AdSense (`ca-pub-…`), **Skimlinks** (`s.skimresources.com/js/71430X1520171.skimlinks.js`, which auto-affiliates outbound links), Amazon, and the author's own books.
- **Followers:** Blogger Followers gadget present (iframe; count not visible in HTML); Feedburner links. Feedspot: X 21.4K, DA 31.
- **Lesson:** "Free today" and unboxing posts are fast, timely and repeatable. On a subdomain, monetization stays at AdSense plus Skimlinks.

### 3.7 icefairy's Treasure Chest: https://icefairystreasurechest.blogspot.com

- **Size and rate:** 3,752 posts; 2–10 a month.
- **Format:** Nearly all "Virtual Tour: Review & Prize Pack Giveaway" posts (labels: Reviews 144, Giveaways 143, Blog Tour 104, Gift Card 63, Amazon 56). Summary feed.
- **Monetization:** AdSense plus Amazon, Walmart, Narrativ, Awin and ShareASale links, Rafflecopter giveaways, follow.it email and a Followers gadget.
- **Followers [3P]:** Facebook 20.6K, X 16.6K (Feedspot).
- **Lesson:** Giveaways create reader actions (entries, follows, emails) but low-value traffic. Not a model for a buying-guide brand.

### 3.8 Razzle Dazzle Styles: https://razzledazzlestyles.blogspot.com

- **Size and rate:** 2,258 posts; 3–15 a month.
- **Content:** Product-gifted reviews and giveaways ("Win a Lintzapper… #giveaway #holidaygiftguide"); posts about 270 words.
- **Monetization and email:** AdSense, Amazon, follow.it email ("check your e-mails for the newsletter").
- **Lesson:** This is what a blogspot review blog looks like when it never builds a brand. The site is 769 KB, with hashtag-stuffed labels and no premium ads.

### Cross-site patterns (8 deep dives plus the 24-site list)

| Pattern | Seen on | Verdict Picks now |
|---|---|---|
| Custom domain | Every site with premium ads (TDC, D&T, ISBMTF, PRM, Mommy's Kitchen, Amusing Planet, SpoilerTV) | `acts39.blogspot.com`; the subdomain does not match the brand |
| Named human + face + About above the fold | PRM hero, TDC welcome box, D&T About photo | Not observed |
| Own photos of products in use | TDC, D&T, PRM (19 own photos in a deals post), Mommy's Kitchen | Press/retailer photos |
| Post length (feed median) | 300–1,100 words | About 6,000 words |
| Seasonal and retail-event posts timed to Prime Days, Walmart deals, holidays | TDC, D&T, PRM | Has seasonal roundups (good) |
| Recurring series | "Five Friday Favorites", "Wednesday Whimsy", monthly menu plans | "Product of the Day" label exists |
| Shop hub (storefronts) | TDC Shop menu (Amazon + Target storefronts, best finds); D&T "Shop my IG" (LTK) | Price Check page + category hubs |
| Multiple retailers | TDC (Walmart via LTK, Amazon, Target), D&T (Amazon + Walmart), icefairy (Amazon, Walmart, Awin, ShareASale) | Amazon only |
| Email list via third-party tool | FeedBlitz, Mailchimp, Flodesk, follow.it | None (Contempo FollowByEmail CSS only) |
| Pinterest as main social referrer | TDC, ISBMTF, Mommy's Kitchen, D&T | Pins exist, very new |
| Price display | PRM "X% OFF Sale Price $Y"; D&T mentions in text; TDC none | Price Check page |
| "Price at time of posting" disclaimer | **Not found on any of the 8** | n/a |
| Disclosure style | Short line at top of post plus a policy page with the Amazon Associates sentence | Has a disclosure (4 "disclosure" hits on homepage) |
| Comments | TDC median 2, D&T median 6; others about 0 | 0 |

---

## 4. Lessons for Verdict Picks, ranked by likely impact for a new site in 2026

Evidence grade: **A** = seen directly on several successful Blogger sites and consistent with Google or ad-network primary docs. **B** = seen on one or two sites, or third-party data. **C** = inference.

1. **Move to a branded custom domain now (for example verdictpicks.com), still on Blogger.** (Impact: very high; Evidence: A)
   - Every Blogger site I found with Raptive, Mediavine, Monumetric or Playwire uses a custom domain. Every subdomain site in the sample is AdSense-only.
   - "acts39" does not match "Verdict Picks", which hurts brand searches, Pinterest trust and future ad-network applications.
   - A custom domain also makes any later move to WordPress a 301 move instead of a restart. That matters given the Hip2Save 2009 takedown and the August 2026 Blogger false-positive removal wave.
   - Blogger supports custom domains for free (the domain costs about $10–15 a year).
2. **Start an email list on a third-party tool this week.** (Impact: high for returning readers; Evidence: A)
   - Successful sites use FeedBlitz (TDC), Mailchimp (ISBMTF), Flodesk (D&T) or follow.it (PRM, icefairy, Razzle Dazzle). Blogger's FollowByEmail stopped in July 2021 and Google said it will not return (https://support.google.com/blogger/answer/10477563).
   - Hip2Save, the migrated benchmark, self-reports 251K email and 58K SMS subscribers. Email is the deal-site moat.
   - Offer a reason to subscribe: a weekly "Verdicts + price drops" email or a Black Friday watchlist.
3. **Put a real person and real photos on the page.** (Impact: high for trust and Google reviews quality; Evidence: A)
   - Every successful site leads with a named author and photo (PRM's hero plus "As seen in", TDC's welcome box, D&T's About photo). They use their own photos of products in their homes.
   - Google's own review guidance asks for "evidence such as visuals, audio, or other links of your own experience" and suggests "links to multiple sellers" (https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews, updated 2025-12-10).
   - Verdict Picks uses press photos and no visible human. Even a few own photos per guide (unboxing, in-use, size comparison) would differentiate.
4. **Add retailer diversity and creator-commerce links.** (Impact: medium-high revenue; Evidence: A for usage, B for payoff)
   - Successful Blogger shopping sites rarely rely on Amazon alone. They add Walmart and Target via LTK, Amazon and Target storefronts, Awin, ShareASale, Skimlinks, and Raptive's affiliate script.
   - Add a second retailer link (Walmart or Target) on top picks. Consider Skimlinks or Sovrn while on AdSense.
   - Build an "Amazon storefront"-style Shop menu, which TDC uses as a top-level nav item.
5. **Shorter, scannable, event-timed posts alongside the long guides.** (Impact: medium-high; Evidence: A for pattern, C for transfer to a guide site)
   - Winners publish 300–1,100-word posts tied to retail moments ("Top 25 Prime Big Deals – Sale Ends Today", "Walmart Deals Sale Picks", "Best New Walmart Christmas Decor Finds") and refresh old seasonal URLs each year (PRM re-dates /2017/ posts).
   - A 6,000-word median is far outside this range. Keep pillar guides, but add short "deal picks" and "what I'd buy" posts that link to them.
6. **Create a recurring series and a reason to come back on a schedule.** (Impact: medium; Evidence: A)
   - Examples: "Five Friday Favorites" (D&T), "Wednesday Whimsy" (ISBMTF), monthly menu plan plus printable (Mommy's Kitchen), daily "free today" posts (New Age Mama). Hip2Save says it publishes about 100,000 pieces a year.
   - For Verdict Picks this could be a weekly "Price Check: what dropped this week" post using the existing Price Check page, sent to email.
7. **Treat Pinterest as the primary social channel and make every post pinnable.** (Impact: medium; Evidence: B, from Similarweb social-referrer data)
   - Pinterest is the top social source for TDC, ISBMTF, Mommy's Kitchen and D&T. Hip2Save claims 2.1M+ monthly Pinterest reach.
   - Use vertical images with own photos and keep pins flowing to seasonal guides 45–60 days before the event.
8. **Plan the ad path to a realistic threshold.** (Impact: medium, later; Evidence: B)
   - Mediavine Journey needs 1,000 sessions a month (from 2026-01-15; https://www.productiveblogging.com/everything-you-need-to-know-about-journey-by-mediavine/, updated 2026-01-19). It needs the Grow script live for 30 days and a site at least 4 months old.
   - One unverified source says Journey requires a self-hosted site, not a free subdomain. That is another reason for lesson 1.
   - Raptive needs 25,000 pageviews a month (https://raptive.com/blog/opening-the-door-to-more-creators-who-meet-raptive-quality-standards/, updated 2025-10-16).
   - AdSense is fine as a placeholder.
9. **Use a short disclosure line at the top of posts plus a policy page.** (Impact: compliance, low traffic impact; Evidence: A)
   - All successful sites do this. TDC's "This post may contain affiliate links for your convenience…" and D&T's site-wide "This Post May Contain Affiliate Links. Please Read Our Disclosure Policy" are good templates.
   - Keep the exact Amazon sentence: "As an Amazon Associate I earn from qualifying purchases."
   - Verdict Picks already goes further on price disclaimers than any of the 8 sites. Its posts carry "Prices and availability are those seen at US retailers at the time of writing (October 2026), are subject to change…" [P, feed 2026-10-29]. Keep that.
10. **Show prices and discounts the way PRM does.** (Impact: low-medium; Evidence: B)
    - "X% OFF – Sale Price: $Y" per item, with the event in the title. Keep prices date-stamped, since none of the 8 sites date-stamp them.

### What does NOT transfer
- **The 2008–2015 growth path.** TDC (2008), Hip2Save (2008), ISBMTF and the giveaway blogs grew through blog rolls, link parties, comment communities, Facebook organic reach and early Pinterest. TDC herself described Facebook reach being pay-walled and comments drifting to Instagram by 2015. Their current traffic is mostly **legacy authority plus a returning audience**. A 7-week-old site cannot copy that; it can only copy the habits.
- **Giveaway and blog-tour formats** (icefairy, Razzle Dazzle, New Age Mama). They create activity, but they are low-value traffic and off-brand for an "expert verdict" site.
- **High-volume news or job-alert Blogger sites** (THN, Gossip Lanka, IndGovtJobs, Padasalai, SpoilerTV). Their model is 150+ posts a month of breaking news with direct and repeat traffic. It is a different business, though it does show Blogger can carry millions of visits.
- **Faceless long "best X" affiliate guides.** I did not find a single successful US "best X" review site on Blogger. The Google 2023–2024 updates hit independent review sites hard: HouseFresh reported losing 91% of Google traffic after the March 2024 core update (https://searchengineland.com/review-site-google-traffic-affiliate-seo-content-440143, 2024 [2ry/SR]). A reported recovery came in October 2025 (https://ppc.land/housefresh-achieves-notable-traffic-recovery-after-google-algorithm-impacts-2/ [2ry]). Verdict Picks' format competes in the hardest part of Google, so the human, photo and email signals above matter more for it than for a decor blog.
- **Brand storefront programs (LTK, Amazon Influencer).** These usually require an established social presence. LTK's own help page lists criteria (https://help.liketoknow.it/hc/en-us/articles/360000834554); third-party guides cite about 4 months of consistent content and an engaged audience, with no public follower minimum [2ry]. Treat this as a 6–12-month goal.

---

## 5. Verdict Picks snapshot used for comparison ([P], 2026-10-29)

- **Feed:** Blogger id blog-9072207571822466986. The public feed has 31 posts, 10 of them published in October 2026. Median about 6,093 feed words. 0 comments.
- **Top labels:** Amazon Finds 10, Buying Guide 7, Car 4, Under $100 3, Kitchen 3, Best Sellers 3, Product of the Day 3, Review 3.
- **Homepage:** Contempo template, 169 KB, 10 scripts, an AdSense tag present, 3 Walmart mentions. No email form: only theme CSS for FollowByEmail. Disclosure text present.
- **Latest titles:** Winter Car Emergency Kit 2026; Best Portable Tire Inflator 2026; ThermoPop 2 vs Thermapen ONE vs ThermoPro 2026; Instant Pot Duo vs Duo Plus vs Rio 2026; Furhaven Orthopedic Dog Bed Review 2026; Gifts Under $50 for 2026; Dreo Space Heater Review 2026; Black Friday Tech and Car Deals 2026; Rubbermaid Brilliance Review 2026; Gifts for Car Lovers 2026.

---

## 6. Evidence quality and limitations

- **Similarweb's free numbers are unreliable for small sites.**
  - TDC (a Raptive site) shows only about 23K visits a month. Kochava gives both "104k visitors" and "3.02K estimated visits" for the same site (https://d2msby6dr6c92m.cloudfront.net/ad_partners/thrifty-decor-chick, updated 2026-10-26).
  - Stella Dimoko Korkus showing 75% US traffic is implausible.
  - The Hacker News: Similarweb (about 1.3M a month) and Semrush (1.87M in Sept 2026) roughly agree.
  - Use these figures for ranking only.
- **Feed limits.** Post counts per month come from Blogger feeds, capped at 150 entries per request. For high-volume sites I give "≥150" and Blogger's own approximate totalResults.
- **Ad-network detection** relies on script names in homepage HTML (adthrive/raptive, scripts.mediavine.com, MONUMETRIC comments, playwire config). A false negative is possible if ads load lazily.
- **Followers.** Blogger Followers gadget counts load in an iframe and were not readable. Social follower numbers come from Feedspot [3P] and may be stale.
- **Not available.** PageSpeed Insights (API quota exhausted) and Semrush pages for small sites (404).
- **Unknown move dates.** For several migrated sites (Cup of Jo, Skinnytaste, Budget Bytes, PostSecret, Linda Ikeji) I verified the current platform but found no reliable move date.
- **Blocked domains.** About 30 domains could not be fetched (Cloudflare challenge or connection reset), for example moneysavingmom.com, iheartorganizing.com and webupd8.org. They are not counted either way.

## 7. Sources (all accessed 2026-10-29 unless dated)

**Primary site fetches:**
- HTML and `/feeds/posts/default?alt=json` for every site in the tables, e.g. https://www.thriftydecorchick.com/feeds/posts/default?alt=json
- Pages listed inline above, e.g. https://www.thriftydecorchick.com/2026/10/the-best-new-walmart-christmas-holiday.html, https://www.dimplesandtangles.com/2026/10/my-top-25-personal-fave-amazon-prime.html, https://www.productreviewmom.com/2026/10/vital-charge-by-vital-red-light-review.html, https://www.ishouldbemoppingthefloor.com/2026/06/wednesday-whimsy-floral-kitchen-finds.html

**Third-party traffic:**
- Similarweb (data month Sept 2026): https://www.similarweb.com/website/thehackernews.com/, …/irasutoya.com/, …/gossiplankanews.com/, …/indgovtjobs.in/, …/padasalai.net/, …/lankacnews.com/, …/kalviseithi.net/, …/amusingplanet.com/, …/spoilertv.com/, …/nieniedialogues.com/, …/thriftydecorchick.com/, …/stelladimokokorkus.com/, …/ishouldbemoppingthefloor.com/, …/mommyskitchen.net/, …/digitalinformationworld.com/, …/productreviewmom.com/, …/dimplesandtangles.com/, …/calculatedriskblog.com/, …/googleblog.com/
- Semrush (updated 2026-10-13): https://semrush.com/website/thehackernews.com/overview

**Lists:** Feedspot 2026 lists and the Blogspot 100 (2012 data), linked in section 1.

**Platform and ad-network documentation:**
- https://support.google.com/blogger/answer/10477563 (FollowByEmail shutdown, 2021)
- https://raptive.com/blog/opening-the-door-to-more-creators-who-meet-raptive-quality-standards/ (updated 2025-10-16)
- https://www.productiveblogging.com/everything-you-need-to-know-about-journey-by-mediavine/ (updated 2026-01-19)
- https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews (updated 2025-12-10)

**Migrations:** Hip2Save (2018 post and March 2026 media kit), Writer Beware (2022-03-22), TechPoint Africa (2015-10-01), Food Blogger Pro (Budget Bytes, undated), The Coupon Challenge, TeacherMade/FreeTech4Teachers; all linked in section 2.

**Risk:** ppc.land and BleepingComputer on the August 2026 Blogger removals, linked in section 2.
