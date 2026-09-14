# Search and AI-search visibility brief — September 2026 (Verdict Picks)

Compiled September 14, 2026 from a researcher's web-search sweep (Google's AI-features and generative-AI optimisation guidance via secondary coverage, Ahrefs/CXL/5WPR citation studies, Blogger help threads, Naver Search Advisor guides, Bing Webmaster and OpenAI/Perplexity crawler docs). Items marked *unverified* rest on vendor data or community threads.

## What gets cited by Google AI Overviews / AI Mode

* No special markup or file is needed; a page must simply be indexed and snippet-eligible. Preview controls (`nosnippet`, `max-snippet`) remove a page from AI answers, so never enable them.
* Only about 38% of cited pages rank in the top 10 (Ahrefs, March 2026); cited pages are fresher than organic results.
* Most cited passages sit in the top 30% of a page; question-form headings are cited about twice as often; definitive sentences beat hedged ones; comparison tables and ranked "Best X for Y" lists earn the most citations (*vendor data*).
* FAQ rich results ended on May 7, 2026; FAQPage schema is harmless (Bing still parses it). Product/AggregateRating schema is for single-product pages only.
* JSON-LD survives in a Blogger post body when inserted minified on one line via HTML view or the API (the Compose editor strips line breaks). Blogger v3 themes already emit BlogPosting JSON-LD with `dateModified`.
* E-E-A-T: pair the illustrated host with an accountable byline that leads to an About page with a real name and contact.

## Applied to every post from now on (in the post HTML)

1. "Key takeaways" box of 40–80 words directly under the lead paragraph.
2. Question-form H2s for each product and for the buying/when-to-buy sections, each followed by one definitive verdict sentence.
3. One real `<table>` with `<th>` headers.
4. "Published … · Updated …" byline linking to the About page; note that Vera is a persona.
5. Minified JSON-LD: ItemList of the picks plus FAQPage mirroring the visible Quick answers.
6. `rel="nofollow sponsored noopener"` on every Amazon link; the Associates disclosure sentence above the fold (already in the byline).
7. A short Korean summary in a collapsed `<details>` block for Naver (effect inferred, not measured).
8. Original raster images where possible (inline SVG is markup, not an image asset): the cover PNG, and owner photos when available.
9. Titles of roughly 60–75 characters without exact prices (Amazon's pricing rule; Google rewrites long titles).

## Blogger settings and external registrations (owner's clicks)

* **Settings → Meta tags → Search description** enabled and filled per post (≤150 chars). Done for the first seven posts; do it for each new post.
* **Settings → Crawlers and indexing → Custom robots header tags**: Home = all; Archive and search = noindex; Posts and pages = all. Never set nosnippet or max-snippet.
* **Theme → Edit HTML**: add `<meta name="twitter:card" content="summary_large_image"/>` in the head if the theme lacks it; Blogger already emits basic Open Graph tags when a Search description exists.
* **Google Search Console**: sitemap.xml submitted (done); also submit `https://acts39.blogspot.com/sitemap-pages.xml`; request indexing for each new post.
* **Bing Webmaster Tools**: import the site from Search Console, submit both sitemaps, use URL Submission for new posts; ChatGPT search draws mostly on Bing's index.
* **Naver Search Advisor** (searchadvisor.naver.com): register `https://acts39.blogspot.com` with the HTML-tag method (paste the meta tag into the theme head), then submit RSS `https://acts39.blogspot.com/feeds/posts/default?alt=rss` and `sitemap.xml`; use 웹페이지 수집 요청 for new posts (50 a day). English pages surface in Naver's 웹문서 collection, rarely in the 블로그 tab; roughly 70–82% of AI Briefing citations come from Naver's own services, so a Korean companion post on a Naver Blog linking to the English original is the realistic route to AI Briefing.
* **Custom domain** (biggest structural upgrade): free blogspot subdomains are described by Google's John Mueller as spam magnets that make SEO harder; Blogger redirects the old address automatically, and a custom domain on Cloudflare enables IndexNow-style crawler hints for Bing and Naver.
* Labels: at most 20 per post and 200 characters combined; label pages are blocked by Blogger's own robots.txt (`Disallow: /search`), so labels are navigation, not ranking; keep hub pages as the crawlable equivalent. Use 10–13 labels per post, Title Case, each on three or more posts.
* Skip llms.txt (unused by AI services and impossible to host on blogspot). Custom robots.txt is unnecessary; if ever enabled, keep OAI-SearchBot, ChatGPT-User, PerplexityBot, Perplexity-User, ClaudeBot and Bingbot allowed.

## Affiliate compliance notes

* Google's reviews system demotes thin roundups; keep first-hand evidence, pros and cons, comparisons and links to more than one seller where sensible.
* Amazon's Operating Agreement restricts displaying prices that are not API-fed and refreshed; the posts state prices as "at the time of writing" with a disclaimer, and titles no longer carry exact prices. Consider tier words ("under $30", "splurge") in headings going forward.
* Disclosure must be hard to miss and near the links: the byline sentence covers the top of the page; the footer repeats it.

## Label set used on the pet guide (13 labels, 162 characters)

Pets, Pet Products, Buying Guide, Best Sellers, For Pet Owners, Cat Litter, Robot Litter Box, Pet Grooming, Pet Hair Removal, Cats, Dogs, Under $100, Amazon Finds

## Candidate label sets for the other posts (to apply at their next republish)

* Robot vacuums: Robot Vacuums, Buying Guide, Home Cleaning, For Pet Owners, Carpet, Hardwood Floors, Under $1000, Roborock, Dreame, Roomba, Smart Home, Amazon Finds
* Wireless earbuds: Wireless Earbuds, Buying Guide, AirPods, Sony, Bose, Noise Cancelling, Under $300, Under $100, Tech Gifts, Amazon Finds
* Smart glasses: Smart Glasses, AI Glasses, Buying Guide, Ray-Ban Meta, XR Glasses, Wearable Tech, Premium, Under $500, Privacy, Amazon Finds
* Power stations: Power Stations, Buying Guide, Home Backup, Camping, Emergency Prep, Anker SOLIX, EcoFlow, Jackery, Under $500, Solar, Amazon Finds
* AirTag 2 / Owala / Bissell stories: Best Sellers, Review, Under $100, Amazon Finds, plus the product's category (Trackers / Water Bottles / Carpet Cleaners) and audience (Travel / Hydration / For Pet Owners)
* Prime Big Deal Days: Deals, Prime Day, Buying Guide, Best Sellers, Robot Vacuums, Wireless Earbuds, Power Stations, Amazon Finds, Price Tracking
