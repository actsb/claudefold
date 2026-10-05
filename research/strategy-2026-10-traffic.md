# Traffic and promotion plan — Verdict Picks (acts39.blogspot.com), October 2026

Compiled 2026-10-05 from four parallel web-research sweeps (about 160 search and fetch calls in total). Read with `research/seo-ai-search-2026-09.md`, which this file extends rather than repeats.

**How to read the sources.** This environment's proxy blocked direct page fetches of developers.google.com, support.google.com, bing.com, indexnow.org, help/policy.pinterest.com, affiliate-program.amazon.com, support.reddithelp.com and transparency.meta.com. Claims marked as official therefore rest on search-engine extracts of those official URLs, not on full-page reads, and most of those pages show no visible date ("undated"). Wording may be paraphrased. **[3rd]** = only blogs, forums, vendors, news or videos. **[vendor]** = a vendor's own study. Before building anything compliance-critical on a claim, open the official page in a browser. In the plans, **[Owner]** = the owner must do it by hand (signed-in dashboards, accounts, judgement). **[Session]** = a scheduled Claude session can do it inside this repository (writing, building, publishing with the Blogger token, drafting copy).

---

## Verdict

1. **The big lever is not promotion but what Google and Bing think of the content.** Google's reviews guidance asks for first-hand evidence, measurements, pros and cons, and links to more than one seller. Its spam policies name thin affiliation and scaled AI content. Since March 2024, helpful-content signals are part of core ranking and act site-wide. Third-party trackers called affiliate sites the worst-hit category of the March 2026 core update. A daily post that only summarises other people's reviews is the main risk to everything below.
2. **Narrow the topics.** The current queue jumps from pressure cookers to water flossers to heaters to dog beds. Pick 3–5 categories and build each into a hub with comparisons and "is X worth it" posts. Those are the query types a new site can actually win, and AI answer engines cite pages that answer narrow sub-questions even when they don't rank in the top 10.
3. **Search plumbing takes two hours, once, by hand.**
   * Google Search Console: sitemaps, and request indexing once per new post.
   * Bing Webmaster Tools: import from Search Console, add the sitemap, submit each new URL. Bing feeds Copilot and, partly, ChatGPT.
   * Check robots.txt and the robots header tags.
   * Add `max-image-preview:large` to the theme.
   * IndexNow is not realistically available on a blogspot subdomain.
4. **Pinterest is the only social channel likely to send meaningful traffic in year one, and it is slow.** Creator reports put it at 2–3 weeks for a trickle and 6–12 months for compounding traffic.
   * The current automation publishes nothing public until the app gets Standard access.
   * Pinterest's Developer Guidelines require the user to choose each Pin, so the pipeline needs a per-Pin approval step before the Standard-access video.
5. **Every other channel should link to the blog post, never straight to Amazon.** That covers Reddit, Quora, Facebook groups, X/Threads, Flipboard, Medium, Shorts and email.
   * Quora bans affiliate links outright.
   * Reddit's filters treat Amazon links as spam.
   * Amazon's email permission is worded ambiguously.
   * Amazon does not list Pinterest as an accepted social site.
6. **AdSense has no published traffic minimum. Paid, exchanged or bot traffic is the only promotion that can hurt it.**
   * Organic social referrals are fine.
   * Never buy cheap traffic, never join click or engagement exchanges, never ask for clicks.
   * The more urgent clock is Amazon's: an Associates account must make three qualifying sales within 180 days of sign-up.

---

## 1. Getting indexed and ranking on Blogger

**Search Console.**
* New Blogger blogs are "added and verified automatically" for the Google account that owns the blog. Either a URL-prefix or a Domain property works for Google-hosted sites. Sources: https://support.google.com/webmasters/answer/9008080 (undated) and https://support.google.com/webmasters/answer/34592 (undated).
* Use the URL-prefix property `https://acts39.blogspot.com/`. The owner doesn't control DNS for blogspot.com, so a Domain property only works through Google's auto-verification. (Inference.)

**Sitemaps Blogger generates.**
* `/sitemap.xml` covers posts, as a paginated index.
* `/sitemap-pages.xml` covers static pages. The default robots.txt reportedly does not list it, so submit it separately.
* The older `/atom.xml?redirect=false&start-index=1&max-results=500` still works but adds nothing for a blog under 500 posts.
* Sources [3rd]: https://etlx.blogspot.com/2025/09/robots.html (Sep 2025) and https://blog.bloggertheme9.com/2026/09/blogger-sitemap-google-search-console.html (Sep 2026).
* `sitemap.xml` has already been submitted (per the September brief).

**Default robots.txt.** The commonly quoted blogspot default [3rd, not seen live from here]:
* `User-agent: Mediapartners-Google` / `Disallow:` (the AdSense crawler may fetch everything);
* `User-agent: *` / `Disallow: /search` / `Allow: /` (`/search` covers label and search pages);
* `Sitemap: …/sitemap.xml`.
* Source: https://www.danpros.com/post/setting-up-robotstxt-on-blogger (undated).
* The owner should open https://acts39.blogspot.com/robots.txt once and confirm there is no `Disallow: /`.

**Request indexing quota.**
* Google's wording: "There's a quota for submitting individual URLs and requesting a recrawl multiple times for the same URL won't get it crawled any faster". Crawling "can take anywhere from a few days to a few weeks". Source: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl (undated).
* Google publishes no number. The often-quoted "about 10–12 per day per property" comes from practitioner tests [3rd]: https://nickleroy.com/blog/how-many-urls-can-you-request-indexing-for-in-gsc-case-study/ (undated).
* Rule: request indexing once per new post, on publish day, using the clean URL (never `?m=1`).

**Bing Webmaster Tools.**
* **Import from Search Console:** sites already verified in Google are imported and verified automatically. Source: https://blogs.bing.com/webmaster/september-2019/Import-sites-from-Search-Console-to-Bing-Webmaster-Tools (Sep 2019).
* **Discovery:** Bing finds pages through IndexNow, sitemaps and links. It "needs to see at least one link pointing to your website" and applies a quality threshold. Sources: https://www.bing.com/webmasters/help/why-is-my-site-not-in-the-index-2141dfab (undated); https://blogs.bing.com/webmaster/2025/7/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search/ (Jul 2025).
* **URL Submission:** the quota is shown in the tool. Snippets of https://www.bing.com/webmasters/help/URL-Submission-62f2860b (undated) mention up to 10,000 a day; new sites historically get less. Check the number on screen.

**IndexNow on Blogger.**
* The spec allows a key file outside the root through `keyLocation`, but the file must be on the same host, and its folder limits which URLs can be submitted. Source: https://www.indexnow.org/documentation (undated).
* Blogger cannot serve an arbitrary `.txt` key file, and nothing shows that Blogger pings IndexNow itself [3rd]: https://aldambi2.blogspot.com/2025/07/indexnow-not-working-on-blogger.html (Jul 2025).
* The "host the key on GitHub Pages" trick breaks the same-host rule. Don't use it.
* **Conclusion:** use the Bing sitemap plus manual URL Submission. IndexNow becomes possible only with a custom domain and a host that serves files.

**Custom robots.txt and robots header tags.**
* Blogger's custom robots.txt replaces the default entirely. One typo (`Disallow: /`) de-indexes the blog. Source: https://support.google.com/blogger/answer/9691230 (undated). Leave it off.
* Custom robots header tags, commonly recommended values [3rd]:
  * Home: `all`
  * Archive and search pages: `noindex`
  * Posts and pages: `all`
  * Never `nosnippet` or `max-snippet`, which also remove pages from AI answers.
  * Source: https://www.innateblogger.com/2021/06/crawlers-and-indexing-settings-blogger.html (2021).
  * These match the values already in `research/seo-ai-search-2026-09.md`.
* `?m=1` mobile URLs carry a canonical tag pointing to the clean URL. Seeing them in GSC as "Alternate page with proper canonical tag" is normal [3rd]: https://blog.bloggertheme9.com/2026/09/remove-m1-from-blogger-url.html (Sep 2026).

**max-image-preview:large and Discover.**
* Large Discover cards need an image at least 1200 px wide, plus `max-image-preview:large` (or AMP). Source: https://developers.google.com/search/docs/appearance/google-discover (undated).
* Default Blogger themes reportedly lack the tag [3rd]: https://www.learnerlagoon.com/2025/08/bloggers-default-theme-why-you-should.html (Aug 2025).
  * Check: View Source → search for `max-image-preview`.
  * If missing, add `<meta content='max-image-preview:large' name='robots'/>` in the theme head.
* **Blogger caveat (from `daily/README.md`):** our cover is a `data:` URI, which cannot be an `og:image` or an image-search result. The blog is therefore probably not Discover-eligible until a hosted cover image is used.
* The February 2026 Discover core update favours in-depth, original content from sites with topic expertise. Source: https://developers.google.com/search/blog/2026/02/discover-core-update (Feb 2026).
* Treat Discover as a bonus, not a channel.

**How long a new site takes.**
* Google says changes can take "a few hours" to "several months", and to wait a few weeks before judging. Source: https://developers.google.com/search/docs/fundamentals/seo-starter-guide (revamped Feb 2024).
* John Mueller has said there is no sandbox, but a site months to about a year old is "still very fresh" and can fluctuate [3rd, reported speech]: https://www.searchenginejournal.com/google-rankings-for-new-sites-could-fluctuate-for-up-to-a-year/372109/ (2020).
* Mueller has also said widespread "Crawled – currently not indexed" can signal site-wide quality doubts, citing undifferentiated AI content [3rd report of a July 2026 podcast, not checked against the audio]: https://www.seroundtable.com/google-crawled-not-indexed-quality-ai-content-41701.html (2026).

**Query types a new site can win.**
* Practitioner consensus only; Google says nothing official [3rd: https://www.gelato.com/blog/affiliate-marketing-keyword-research-guide (2026)]. Winnable:
  * long-tail "best X for [narrow use or constraint]";
  * "X vs Y";
  * "is X worth it";
  * single-model reviews, especially of new or renamed variants (as with the PureWash M100 naming in the bidet guide).
* Broad "best X" head terms are dominated by established publishers.

**Quality rules that apply directly.**
* Reviews guidance: first-hand evidence (your own photos, video, measurements), quantitative measurements, what sets a product apart, pros and cons, changes from earlier models, and links to more than one seller. Source: https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews (undated).
* Spam policies (thin affiliation; scaled content abuse): https://developers.google.com/search/docs/essentials/spam-policies (undated).
* Helpful content folded into core ranking: https://developers.google.com/search/blog/2024/03/core-update-spam-policies (Mar 2024).
* Core updates: 2025-03-13, 2025-06-30, 2025-12-11; 2026-03-27 to 04-08; 2026-05-21 to 06-02. Source: https://status.search.google.com/summary.
* "Affiliate sites worst hit in March 2026" comes from a third party with unverified methodology [3rd]: https://www.wsiworld.com/blog/google-march-2026-core-update-why-credibility-now-drives-search-visibility (2026).

## 2. AI Overviews, AI Mode and other AI answer engines

**Google.**
* **Eligibility:** a page only needs to be indexed and snippet-eligible. "There are no additional technical requirements." Source: https://developers.google.com/search/docs/appearance/ai-features (undated).
* **Query fan-out:** both features issue many related searches, so the set of cited pages is "wider and more diverse" than classic results. Same source.
* **"Still SEO":** Google's guide "Optimizing your website for generative AI features" (https://developers.google.com/search/docs/fundamentals/ai-optimization-guide, about 2026-05-15 per coverage) says you don't need:
  * llms.txt;
  * special schema;
  * Markdown copies of pages;
  * AI-only rewrites;
  * chunking content into small pieces.
  * Coverage: https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/ (May 2026).
* **May 2025 Google post:** https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search (May 2025). Its advice: unique "non-commodity" content, clear main content, structured data that matches visible text, and images and video.
* **Preview controls:** `nosnippet` removes a page from AI Overviews and AI Mode.
* **Google-Extended** does not affect AI Overviews, AI Mode or Search ranking. Source: https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers (undated).
* **Measurement:** Search Console's "Generative AI performance" report (impressions only) launched 2026-06-03. Source: https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports (Jun 2026).
* **Shopping inside Google:** I/O 2026 merged AI Overviews and AI Mode into one experience and announced a cross-surface "Universal Cart". Source: https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/ (May 2026).
  * Agentic checkout (UCP) lets people buy inside AI Mode: https://www.searchenginejournal.com/google-announces-ai-mode-checkout-protocol-business-agent/564764/ (Jan 2026).
  * Implication (inference): an affiliate page's role becomes being *the cited evaluation*, not the place where people click to buy.
  * Claims that AI Mode is now the default for everyone are unconfirmed.

**ChatGPT.**
* **Crawlers:**
  * OAI-SearchBot puts sites into ChatGPT search; OpenAI recommends allowing it.
  * GPTBot is training only.
  * ChatGPT-User is for fetches a user triggers.
  * Source: https://developers.openai.com/api/docs/bots (undated).
* **Bing:** ChatGPT search launched on Bing's index and now also uses its own and other providers [3rd]: https://www.thekeyword.co/news/openai-s-chatgpt-search-relies-on-bing-s-index (2024). Bing indexing is still the safest route.
* **Shopping research** (2025-11-24) builds buyer's guides and "cites reliable sources". Source: https://openai.com/index/chatgpt-shopping-research/ (Nov 2025). There is no evidence either way on whether small affiliate blogs get cited.

**Perplexity.** PerplexityBot indexes pages for citation and obeys robots.txt. Source: https://docs.perplexity.ai/guides/bots (undated).

**Bing and Copilot.**
* Bing Webmaster Tools has an "AI Performance" report (preview from 2026-02-10) showing citations in Copilot and Bing AI summaries, plus grounding queries. Source: https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview (Feb 2026).
* Microsoft's own advice: clear headings, tables, FAQ sections and freshness help AI answers reference content. Source: https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers (Oct 2025).

**What gets cited [vendor].**
* **Ahrefs, March 2026:** only 38% of AI Overview citations rank in the top 10, down from 76% in July 2025, which points to fan-out. Source: https://ahrefs.com/blog/ai-overview-citations-top-10 (Mar 2026).
* **Ahrefs, July 2025:** cited pages were 25.7% fresher than organic results. Source: https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content (Jul 2025).
* **Semrush:** Reddit, YouTube, Wikipedia and LinkedIn dominate citations. Source: https://searchengineland.com/ai-search-engines-cite-reddit-youtube-and-linkedin-most-study-473138 (2026).
* **What this means for us:** an unknown blog competes with forums and video. Answering narrow sub-questions with first-hand evidence is the only thing that sets it apart.

**Structure that helps.** Already in our template:
* question H2s with a one-sentence verdict first;
* a key-takeaways box;
* a real `<table>`;
* FAQ;
* JSON-LD that matches the visible text.

Add:
* a visible "How we chose" / methodology box saying what was hands-on and what was researched;
* original photos or measurements where possible;
* a second retailer link where it is honest (the price research already finds Walmart, Target and Costco);
* monthly refreshes of the top posts, changing the "Updated" date and `dateModified` only when the content really changed.

Don't add llms.txt.

## 3. Pinterest

**Affiliate links.**
* Pinterest's Commercial and Branded Content Guidelines allow affiliate links. Conditions: one authentic account, original content that adds value, transparency, and no "creating affiliate Pins repetitively or in large volumes." Source: https://policy.pinterest.com/en/commercial-and-branded-content-guidelines (undated).
* Deceptive redirects and abused shorteners can be blocked; link directly to the source. Sources: https://policy.pinterest.com/en/community-guidelines (undated); https://help.pinterest.com/en/article/fix-a-broken-link (undated).
* Amazon's list of accepted social sites names Facebook, Instagram, Twitter, YouTube, TikTok and Twitch, not Pinterest. Source: https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM (undated).
* **Our pattern of Pin → blog post is the safe one.** Never pin amzn.to links.

**Disclosure.**
* The FTC names Pinterest: a Pin that endorses a product needs a clear disclosure, placed with the endorsement. Source: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers (Nov 2019, current).
* A Pin to our own review page arguably doesn't need "#ad" (interpretation). Adding "Affiliate links in the guide" to each description is cheap insurance.

**Spam and fresh Pins.**
* Rate-limit blocks are triggered by saving "a lot of Pins from the same website quickly". They usually lift within 24 h, and retrying makes them worse. Source: https://help.pinterest.com/en/article/rate-limit-blocks (undated).
* Pinterest asks developers to cap Pins at "a reasonable but small daily or weekly number" and to check for duplicate titles, descriptions and URLs. Source: https://developers.pinterest.com/docs/getting-started/best-practices/ (undated).
* Pinterest favours fresh content: Pins sharing the same image and URL are counted together. Source: https://help.pinterest.com/en/business/article/pin-performance-and-distribution (undated).
* Likely-generative images are labelled "AI modified", and since October 2025 users can see fewer GenAI Pins in home decor, beauty and fashion [news]: https://techcrunch.com/2025/10/16/pinterest-adds-controls-to-let-you-limit-the-amount-of-ai-slop-in-your-feed/ (2025-10-16). Our pins are programmatic renders; real photos are safer.

**Cadence.**
* Official: create "frequently and consistently… aim to create original content weekly", with no daily number. Source: https://create.pinterest.com/fundamentals/ (undated).
* Tailwind [vendor]: 1–5 fresh Pins a day; new accounts 3–5 a week. Source: https://www.tailwindapp.com/blog/pinterest-posting-frequency (2025).

**Formats.**
* 2:3, 1000×1500 px, short legible text overlay (≤ about 10 words). Source: https://business.pinterest.com/creative-best-practices/ (undated).
* One unified Pin format since August 2023 (Idea Pins merged in). Source: https://create.pinterest.com/blog/new-pin-format-update/ (Aug 2023).
* Article Rich Pins are still documented and now attach automatically from Open Graph or Schema metadata, with no validator. Source: https://help.pinterest.com/en/business/article/rich-pins (undated).

**Boards and Pinterest SEO.**
* Keywords go in Pin titles and descriptions and in board names and descriptions. Source: https://create.pinterest.com/blog/seo-best-practices/ (undated).
* Pinterest Trends gives up to two years of search data by region. Source: https://help.pinterest.com/en/business/article/pinterest-trends (undated).
* Claim the website first (HTML tag). Source: https://help.pinterest.com/en-gb/business/article/claim-your-website (undated).
* Group boards matter less now [3rd, anecdotal].

**Timeline to traffic [3rd, anecdotal].**
* 2–3 weeks for a trickle: https://www.straycurls.com/what-does-pinterest-traffic-look-like-for-a-new-blog/ (undated).
* 60–90 days for meaningful traffic and 6–12 months for compounding growth: https://improvado.io/blog/pinterest-traffic (2026).

**API rules (this matters for our pipeline).**
* "All Pins and Boards created with Trial access are only visible to their creator as Sandbox entities." Source: https://developers.pinterest.com/docs/key-concepts/access-tiers/ (undated).
* Developer Guidelines: apps must not let users "automatically initiate actions without specifically considering each action… if an app allows Pin scheduling, the end user must choose each Pin to be published." Source: https://policy.pinterest.com/en/developer-guidelines (undated).
* Our pipeline currently pins automatically when a queue entry turns `published`. **Before recording the Standard-access video, add an explicit per-Pin approval step.** For example, an `approved: true` field the owner sets per pin entry, or a manual `workflow_dispatch` run that lists the pins and asks for confirmation. The video should show that step.
* Rate limits (about 1,000 calls a day on Trial; about 100 a minute for writes on Standard; snippet numbers) are irrelevant at our volume. Source: https://developers.pinterest.com/docs/reference/rate-limits/ (undated).
* **RSS auto-publish:** needs a claimed site, makes Pins within 24 h, up to 200 a day, one board per feed. It can make one Pin per image in the feed. Source: https://help.pinterest.com/en/business/article/auto-publish-pins-from-your-rss-feed (undated).
  * Our data-URI covers may not give it a usable image. Expect landscape or odd Pins.
  * Never run RSS and the API on the same posts.

## 4. Other channels

**Amazon rules on every channel.**
* **No cloaking:** no link shortener "in a manner that makes it unclear that you are linking to an Amazon Site." Source: https://affiliate-program.amazon.com/help/operating/agreement (undated).
* **Disclosures:** "As an Amazon Associate I earn from qualifying purchases" on the site and on social accounts, plus "#ad" or "(paid link)" next to links. Source: https://affiliate-program.amazon.com/help/operating/policies (undated).
* **Offline:** printed material, ebooks and mailings are banned. Same source.
* **Email:** links are allowed only in solicited (opted-in) "emails, SMS and direct messaging from your social media Sites". The wording is ambiguous, and it reportedly changed around March 2024 [3rd]: https://geniuslink.com/blog/can-you-include-affiliate-links-in-emails/ (undated).
* **180-day clock:** three qualifying sales within 180 days or the account closes [3rd; check in Associates Central]: https://getaawp.com/blog/amazon-affiliate-program-requirements/ (2026).

| Channel | Rules (source) | What brings clicks | What gets accounts banned | Low-risk routine |
|---|---|---|---|---|
| **Reddit** | Spam = "repeated or unsolicited actions… that negatively affect redditors"; promotion "not inherently spam", but many communities are strict (https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam, undated). The 10% rule is Reddiquette and now enforced per subreddit (https://support.reddithelp.com/hc/en-us/articles/205926439-Reddiquette, undated). | Detailed answers in buying-question threads; a link to a guide only when someone asks [3rd] | Same link across subreddits, Amazon-tagged links, multiple accounts, vote help; new-account karma and age filters remove posts silently [3rd: https://redditgrow.ai/blog/reddit-karma-requirements, 2026] | Comment only for 30 days, about 10 helpful comments a week, then at most 1 blog link a week where the subreddit allows it; say it's your blog |
| **Quora** | "Affiliate links are not allowed"; disclose your affiliation; the answer must make sense without leaving Quora (https://help.quora.com/hc/en-us/articles/9456583756180-Question-and-Answer-Policies, undated) | Complete answers to "best X under $Y" questions with one blog link | Affiliate or shortened links, link-only or copy-pasted answers | 3 answers a week; credential "Writes buying guides at acts39.blogspot.com" |
| **Facebook groups** | Meta bans posting "at very high frequencies", repetitive content and cloaked links (https://transparency.meta.com/policies/community-standards/spam/, undated). Meta tested a cap of 2 links a month for professional profiles and Pages (https://techcrunch.com/2025/12/17/facebook-is-testing-a-link-posting-limit-for-professional-accounts-and-pages, 2025-12-17; current status unknown) | Graphics people want to save (cost tables), link in the first comment [3rd] | Same text pasted into many groups, bursts of posts | 3–5 groups that allow links; at most 1 share per group per week, rewritten each time |
| **X / Threads** | X bans "bulk, duplicative" posting, copypasta and misleading shorteners (https://help.x.com/en/rules-and-policies/platform-manipulation, undated). X says "links are not deboosted" (https://x.com/nikitabier/status/1977422602328232415, Oct 2025). Threads says link posts work better after a ranking fix (https://www.socialmediatoday.com/news/meta-says-link-posts-ranked-properly-threads-reach/750126/, 2025) | A useful fact in the post, link in a reply [3rd] | Identical repeated posts, mass mentions, automation | 1 post a day each, from the promo kit; "(paid links)" where relevant; Amazon disclosure in the bio |
| **Flipboard** | Public magazines; self-serve RSS feed submission (https://about.flipboard.com/inside-flipboard/new-feed-your-rss-feed-into-a-flipboard-magazine/, undated) | Unknown; no current traffic data | Low risk | Submit the feed once; also flip other good sources |
| **Medium** | "Import a story" sets a canonical link and backdates the story (https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium, undated); affiliate links allowed with disclosure (https://help.medium.com/hc/en-us/articles/213477928-Medium-Rules, undated) | Summaries linking to the full guide | Posts made mainly to sell lose Boost and may be treated as spam [3rd] | 1–2 imports or rewritten summaries a week |
| **YouTube Shorts** | Links in Shorts descriptions and comments are not clickable since 2023-08-31 (https://9to5google.com/2023/08/10/youtube-shorts-links-spam/, 2023-08-10). The spam policy covers external links, including telling viewers to visit a site (https://support.google.com/youtube/answer/2801973, undated) | Brand awareness; the channel profile link | Mass affiliate-only Shorts | Optional, months 2–3: 2–3 Shorts a week from the existing clips |
| **Email** | CAN-SPAM: honest headers and subject lines, a postal address, unsubscribe honoured within 10 business days (https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business, undated). Free tiers: Kit up to 10,000, Beehiiv up to 2,500 [3rd: https://www.emailtooltester.com/en/blog/free-newsletter-platforms/, 2026] | A weekly "best of" email to people who opted in | Bought lists; Amazon links in PDFs or ebooks | Weekly digest linking to blog posts only |

## 5. Internal linking and topical authority

**Google's guidance.**
* Links must be `<a href>` elements.
* "Every page you care about should have a link from at least one other page on your site."
* Anchors should be "descriptive, reasonably concise, and relevant."
* Source: https://developers.google.com/search/docs/crawling-indexing/links-crawlable (undated).

**"Topical authority".**
* Google's 2023 "topic authority" system is for news only. Source: https://searchengineland.com/google-launches-new-topic-authority-system-to-better-surface-news-content-427485 (2023-05).
* Mueller called topical authority essentially relevance and said "don't worry about it". Source: https://www.searchenginejournal.com/google-on-topical-authority-dont-worry-about-it/501209/ (2023-11-14).
* He also said "it's really hard to call a site authoritative after 30 articles", then clarified there is no magic number. Source: https://www.seroundtable.com/myth-30-articles-makes-your-site-authoritative-in-google-search-32432.html (2021).
* **Nobody has credible evidence for "N posts per cluster"**; "10–30" is SEO-blog opinion.
* What is official: site-wide quality signals, so thin posts drag the rest down.

**Blogger specifics.**
* Label pages (`/search/label/X`) are noindexed by our recommended header-tag setting, and default robots.txt blocks `/search` from crawling.
  * So label pages neither rank nor pass discovery.
  * Hubs must be static Pages (we already have `/p/…` hubs) with hand-written intros and plain links.
* Related-post gadgets usually load with JavaScript from feeds. Plain in-body links in the post HTML are the dependable option (inference from Google's link guidance).

**Recommended structure.**
* Pick 3–5 categories that the queue keeps returning to, and give each a hub Page:
  * **Home cleaning:** O-Cedar mop, Bissell Little Green, robot vacuums.
  * **Sleep and home comfort:** Beckham pillows, Bedsure throw, Dreo heater, Levoit purifier.
  * **Bathroom and personal care:** bidet, Waterpik, Revlon.
  * **Car:** NOCO GB40, tire inflator.
  * **Pets:** existing pet guides, Furhaven bed.
* Aim for about 6–10 posts per hub before adding a new category: one "best of" guide, 2–3 "X vs Y" posts, and single-product "is it worth it" reviews. This is a working target, not a sourced threshold.
* In every post, add 3–6 descriptive in-body links, including one to its hub.
* On publish, add a link to the new post from 2–3 older posts in the same cluster, so no post is orphaned.
* Make the first label the main category, since themes build breadcrumbs from it (unverified).

## 6. Promotion and AdSense review

**Eligibility.**
* Original content that meets policy, age 18+, access to the site's HTML. Content must be "high-quality, original, and attract an audience". Blogger blogs apply through the Earnings tab. Source: https://support.google.com/adsense/answer/9724 (undated).
* **No published traffic minimum.** Rejections cite "low value content" or "site not ready". Source: https://support.google.com/adsense/answer/81904 (undated).
* A site whose posts restate Amazon listings is the classic low-value case. Indexing state is a useful proxy: many "Crawled – currently not indexed" posts means improve or merge before applying (inference).

**Invalid traffic** (any clicks or impressions that artificially inflate costs or earnings). Source: https://support.google.com/adsense/answer/16737 (undated). It includes:
* clicking your own ads;
* asking for clicks, or placements that cause accidental clicks;
* bots and automated tools.

**Banned traffic sources.** Source: https://support.google.com/adsense/answer/48182 (undated).
* paid-to-click, paid-to-surf, autosurf and click-exchange programs;
* unsolicited mass email;
* pop-up or redirect software.

**Paid traffic.**
* Allowed if it complies with policy, but "publishers are ultimately responsible for the traffic to their ads" and Google urges caution. Source: https://support.google.com/adsense/answer/1348722 (undated).
* Bot traffic that arrives through bought traffic is a top reason for account closure. Source: https://support.google.com/adsense/answer/2660562 (undated).
* **Recommendation:** no paid traffic at all before approval or in the first months after.

**Social traffic.** Organic referrals are ordinary traffic. Avoid engagement pods and "visit my site" swap groups.

**After approval.**
* Never click your own ads; never use "click" language.
* Keep ads away from the Amazon buttons, to avoid accidental clicks.
* Watch for sudden spikes from one unknown referrer.

**Korea notes.**
* A PIN is mailed at $10 of earnings; verify it within about 4 months [3rd].
* Submit a W-8BEN in AdSense, or Google may withhold up to 30%. Source: https://support.google.com/adsense/answer/10735961 (undated). Check the treaty rate the tax tool shows.

---

## Weekly routine (from week 2)

| Day (KST evening) | Task | Who |
|---|---|---|
| Daily | Write, build and publish the day's post; draft its pin entry and promo kit; add 2–3 links to it from older same-cluster posts and update its hub | [Session] (the existing Routine, extended) |
| Daily, 5 min | Search Console URL Inspection → Request indexing (new URL, once); Bing → URL Submission; paste the search description | [Owner] |
| Daily, 2 min | Approve the day's pin entry (once the approval gate exists); post the X/Threads lines from the promo kit | [Owner] |
| Mon | Weekly report: GSC and Bing impressions per post, pages "not indexed", top queries → choose next week's "vs" and "worth it" topics | [Owner] exports or screenshots; [Session] analyses files the owner commits |
| Tue / Thu | Reddit: about 5 helpful comments each day, links only when asked; Quora: 1–2 answers | [Owner] |
| Wed | One new Pin design for one older post (≥7 days since that URL's last Pin) | [Session] drafts the image and copy; [Owner] approves |
| Fri | Refresh one older post (price notes, new model, owner complaints), real "Updated" date only | [Session] |
| Sat | Medium import or summary of the week's best guide; one Facebook group share | [Owner] |
| Sun | Optional newsletter digest (blog links only) | [Session] drafts; [Owner] sends |

## Dated plan

### Week 1 (Oct 6–12, 2026)
* [Owner] Open `/robots.txt` and confirm there's no `Disallow: /`. Confirm the custom robots header tags: home `all`, archive/search `noindex`, posts and pages `all`, no nosnippet.
* [Owner] Search Console: submit `sitemap-pages.xml`; check the Pages report for "Crawled – currently not indexed". Request indexing for any published post not yet indexed, within the daily quota.
* [Owner] Bing Webmaster Tools: import from Search Console, submit both sitemaps, submit all published post URLs.
* [Owner] Theme head: add `max-image-preview:large` if missing (5-minute edit; a session can supply the exact line).
* [Owner] Pinterest steps 1–3 of `daily/pinterest-setup.md`: business account, claim the site, create the developer app.
* [Session] Add the per-Pin approval gate to `scripts/pinterest_pins.py` / `pinterest.yml` before the Standard-access video, and update `daily/pinterest-setup.md` step 7 to show it.
* [Session] Draft the 5 cluster hub pages (or extend the existing hubs) and a "How we choose" methodology page. Add the in-body cross-links between existing posts in the same cluster.
* [Owner] Note the Amazon Associates sign-up date and work out the 180-day deadline.
* [Owner] Create Reddit and Quora accounts if needed; comments only, no links.

### Weeks 2–4 (Oct 13 – Nov 2)
* [Owner] Record the Pinterest Standard-access video (connect → approve → pin) and submit it. Expect 1–4 weeks.
* [Owner] Meanwhile, optionally switch on RSS auto-publish to one board. Turn it off the day `PINTEREST_LIVE` is set.
* [Session] Re-order `daily/queue.json` so each of the 5 clusters gets 1–2 new posts a week, with "X vs Y" and "is X worth it" titles drawn from the queries GSC and Bing start showing. Holiday angle for Pinterest, 45–60 days ahead: gift guides by cluster before Thanksgiving (Nov 26) and Black Friday (Nov 27).
* [Session] Add a methodology box and a second-retailer line to the post template.
* [Owner] Flipboard: submit the RSS feed. Start the weekly routine above.
* [Owner] Apply for AdSense once about 25–30 solid posts exist and the trust pages and navigation have no empty links. No paid traffic.

### Months 2–3 (Nov 3, 2026 – Jan 4, 2027)
* [Owner] When Standard access lands, set `PINTEREST_LIVE=true`: 1 fresh Pin a day (the new post), plus up to 2 new-design Pins for older posts, ≤5 a day, ≥7 days between Pins to the same URL. Raise volume only after 8 clean weeks.
* [Session] From Big Deal Days through Cyber Monday (Nov 30), publish deal notes inside existing cluster posts, not separate thin deal posts.
* [Session] Monthly refresh of the top 10 posts by impressions.
* [Owner] Check the AI reports monthly: Search Console's Generative AI report and Bing's AI Performance report.
* [Owner] Reddit: after 30 days of comments, at most 1 relevant blog link a week where allowed. Medium: 1–2 imports a week.
* [Owner] Optional: Shorts from the existing clips (channel link to the blog); a Kit or Beehiiv newsletter.
* [Owner] Decide on a custom domain before the blog grows. It enables a Domain property, hosted images for `og:image`/Discover, and IndexNow. Moving later means a migration.
* Expected by early January (anecdotal ranges): a few hundred Search impressions a day on long-tail queries if the posts are indexed; Pinterest still early. Judge by impressions and indexed-page count, not clicks.

### Hard limits for scheduled sessions
* No signed-in dashboards: Search Console, Bing, Pinterest, Reddit, Quora, Facebook, X, Medium, AdSense.
* Pinterest only through the GitHub workflow, never from a Routine.
* Never read or use BLOGGER_* or PINTEREST_* outside the publisher scripts.
* Never post to social accounts.
* Never buy or exchange traffic.
