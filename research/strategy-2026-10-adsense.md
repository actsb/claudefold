# AdSense approval for a Blogger affiliate blog: strategy for Verdict Picks (researched 2026-10-05)

Scope: https://acts39.blogspot.com. One month old, blogspot subdomain, 17 posts of 1,800–4,000 words. The posts are AI-assisted, editor-checked Amazon buying guides with illustrations only. The owner is resident in Korea. The repo's own state was read from `daily/adsense-readiness.md` and `brand/pages/*.html`.

**How this was researched.** Three research passes ran about 145 web searches in total.
- Direct page fetches of support.google.com, developers.google.com and affiliate-program.amazon.com were blocked by this environment's network policy. So every Google or Amazon quote below comes from the search-engine extract of that exact official URL, not from reading the live page.
- "Undated" means the page's own last-updated stamp could not be seen. All pages were accessed on 2026-10-05.
- Reddit could not be searched.
- **Before quoting anything below as Google's exact wording, open the URL in a browser.**

Labels:
- **[G]** Google official (AdSense Help, Publisher Policies, Blogger Help, Search Central, web.dev)
- **[G-community]** a volunteer Product Expert on support.google.com. Not policy.
- **[A]** Amazon official
- **[IRS]** US government
- **[S]** blog, forum, video or vendor. Anecdote, not evidence.

---

## Verdict

1. **No Google rule blocks this blog today.**
   - Google states no minimum post count, word count, traffic or (for Korea/US) site age.
   - A `*.blogspot.com` subdomain is a fully valid AdSense site through Blogger's Earnings tab.
   - A custom domain is **not** required and Google never says it improves the odds. The earlier note in `daily/adsense-readiness.md` that says so repeats folklore.
2. **Rejection, if it comes, will almost certainly be "Low value content."** For this site, that judgement rests on three Google texts:
   - AdSense's ban on ads on "automatically generated content without manual review or curation".
   - Search's "scaled content abuse" and "thin affiliation" spam policies.
   - The reviews guidance asking for "evidence … of your own experience".

   A daily, templated, illustration-only, research-not-testing roundup site sits close to all three. Volume is not the problem; distinctiveness and visible human accountability are.
3. **Two honesty problems should be fixed before applying.** They are cheap to fix and costly if a reviewer spots them:
   - **(a) The About page says "an independent publication based in the United States"** (`brand/pages/about.html`), but the owner lives in Korea. AdSense and Search both treat misleading site-ownership claims as a trust problem. Change it to something true.
   - **(b) The About page says "the Verdict Picks editors review them"**, but no person is named anywhere. Google "strongly encourages" bylines that lead to real information about the author, and warns against invented personas.
4. **Recommended timing:**
   - Spend about 2–3 weeks on the fixes in the "what to do when" list.
   - Request review around **2026-10-26 to 2026-11-02**, at about 6–8 weeks of age and 35–45 posts.
   - Expect a decision within days to about 4 weeks.
   - If rejected, fix and re-request from the same Sites entry. Do not delete and re-add the site.

---

## 1. Eligibility, site review, and every common rejection reason

### Eligibility and the review process

| Requirement | Google's wording (search extract) | Source |
|---|---|---|
| Age 18+, own content | "If you have your own content that meets our policies and you're 18 or over, you can sign up" | https://support.google.com/adsense/answer/9724 (undated) [G] |
| Content quality | content should be "high-quality, original, and attract an audience" | same [G] |
| Site access | must be able to place code in `<head>`; "won't be able to verify that you're the site owner" otherwise | answer/9724, https://support.google.com/adsense/answer/91205 (undated) [G] |
| Readiness checklist | "unique content that's relevant to your visitors and provides a great user experience"; "clear, easy-to-use navigation" (alignment, readability, functionality); a comment section is suggested | https://support.google.com/adsense/answer/7299563 (undated) [G] |
| Whole-site review | Google checks payment details and "reviews your entire site". This "usually takes a few days, but in some cases can take 2–4 weeks" | https://support.google.com/adsense/answer/10162, https://support.google.com/adsense/answer/12170222 (undated) [G] |
| Site status states | **Requires review** (not checked yet; finish tasks, click Request review). **Getting ready** (checks running; stays here if setup tasks are unfinished). **Ready**. **Needs attention** (fix issues) | answer/12170222 (undated) [G] |
| Connecting a non-Blogger site | AdSense code snippet, ads.txt line, or meta tag | https://support.google.com/adsense/answer/7584263 (undated) [G]. Blogger blogs skip this (see §2) |
| One account per person | duplicate accounts are rejected | https://support.google.com/adsense/answer/81904 (undated) [G] |
| Account setup deadline | about 6 months to finish setup or the account is deactivated | account-setup help extract (undated) [G]; unverified detail |
| Korea | not a restricted country | https://support.google.com/adsense/answer/13402307 (undated) [G] |

### Rejection reasons and fixes

Main sources:
- "What to do when your site isn't ready to show ads": https://support.google.com/adsense/answer/12176698 (undated) [G]
- "Your AdSense account wasn't approved": https://support.google.com/adsense/answer/81904 (undated) [G]

| Reason | What Google says | Concrete fix for Verdict Picks |
|---|---|---|
| **Low value content** | The site must "provide enough valuable content to users and have a good user experience and navigational elements"; "continuing to apply without understanding these policies may result in rejection" (answer/12176698). The underlying policy bans ads "on screens without publisher-content or with low-value content, that are under construction, or that are used for alerts, navigation or other behavioral purposes" and says "Don't place ads on automatically generated content without manual review or curation" (https://support.google.com/publisherpolicies/answer/11112688, undated) [G]. A Google Community Guide says reviewers weigh E-E-A-T and apply a stricter YMYL bar (https://support.google.com/adsense/community-guide/241032356, undated) [G-community] | Make human review visible: a named editor, a per-post "how this guide was made" box, a dated corrections line. Add original synthesis per post (own comparison table, a "who should skip it" verdict, numbers with sources). Remove or fix the off-topic post (`2026-09-claude-higgsfield-mcp-ai-video` is an AI-video-tools piece on a home-products site). Strengthen the thinnest pages first rather than adding more posts. Several 2026 Korean sources report "rewrite, don't add" as what worked after repeated low-value rejections (https://tali.kr/adsense-approval-2026, 2026 [S]) |
| **Site down or unavailable / site isn't ready** | "Make sure that your site is published and live on the web"; remove logins; don't block the crawler in robots.txt; valid SSL and HTTP→HTTPS redirect; correct any mistyped URL (answer/12176698, answer/81904) [G] | Check that the blog is public (Settings → Permissions → Reader access = Public), "Visible to search engines" is on, HTTPS redirect is on, and there is no custom robots.txt that blocks `Mediapartners-Google` |
| **Valuable inventory: No content / Under construction / Insufficient content** (older labels for the same policy) | The site "may not have enough text, and/or the site was deemed to be 'under construction'"; "sites that contain mostly images, videos … may not be approved"; pages need "enough text … for our specialists to review" (https://blog.google/products/adsense/how-to-address-insufficient-content/, undated) [G]. Use "complete sentences and paragraphs, not only headlines" (answer/81904) [G] | Hide empty or near-empty labels and pages. Make sure hub pages (`hub-*.html`) have real paragraphs, not just link lists. No "coming soon" pages. The `follow.html` page should carry some text |
| **Replicated / copied / scraped content** | Not allowed: "embedded or copied content from others without additional commentary, curation, or otherwise adding value", "automatically generated content without manual review or curation", slight rewording "with synonyms or automated techniques", and pages that mostly embed media (https://support.google.com/publisherpolicies/answer/11190248, undated) [G]. Program policies: "contribute your own original content … specialist knowledge, improvement ideas, reviews, or your personal thoughts" (https://support.google.com/adsense/answer/48182) [G] | Paraphrased owner-review themes and lab numbers count only with added judgement. Keep the verdicts, skip lists and cost-of-ownership math prominent. Do not let YouTube embeds dominate any screen |
| **Site navigation** | "navigational elements" (answer/12176698); alignment, readability, functioning menus (answer/7299563) [G] | Top menu linking the hubs plus About / How we rank / Contact / Privacy / Disclosure. Check on a phone. No broken links. Secondary guides say the same (several 2026 guides [S]) |
| **Policy violations** | "There are policy violations on your site which need resolving"; check the Policy center (answer/12176698) [G]. From April 2025 the Policy center separates policy issue, regulatory issue and advertiser preference (https://support.google.com/adsense/answer/11066888) [G] | Read the Program policies once. The usual traps for this site are misrepresentation (fix the "based in the US" line) and unclear ad/affiliate separation |
| **Spam / webmaster guidelines** | Violations can mean "Google-served ads disabled"; examples include doorway pages and "'cookie cutter' approaches such as affiliate programs with little or no original content" (https://support.google.com/adsense/answer/1348737, undated) [G] | See §4: vary the template and add original value per page |
| **Unsupported language** | content must be mainly in a supported language (answer/81904) [G] | English, so fine. The Korean summary in each post should stay a short add-on, not the main content |

**AI content.**
- No AdSense rule bans AI-assisted content. The rule is "automatically generated content without manual review or curation" (answer/11112688, answer/11190248) [G].
- Search: "Appropriate use of AI or automation is not against our guidelines" unless its primary purpose is ranking manipulation (https://developers.google.com/search/blog/2023/02/google-search-and-ai-content, 2023-02-08) [G].
- The Search Central guide "Using generative AI content" (https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) [G] was reportedly revised on 2026-10-01. The revision says "it is critical to manually factcheck and review all AI-generated content for accuracy and trustworthiness before publishing", and extends that review to titles, meta descriptions, structured data and alt text. The revision date and wording come from secondary reports: https://www.seroundtable.com/google-updates-ai-content-guidelines-factcheck-review-42217.html and https://www.searchenginejournal.com/google-fact-check-ai-content-before-publishing/591782/ (2026-10-01/02) [S]. Verify on the live page.
- AdSense's "AI labeling regulations" page (https://support.google.com/adsense/answer/17258538) is about ad creatives, not publisher content [G].

**Policies vs restrictions.**
- A violated **policy** must be fixed, or ads are disabled.
- A **restriction** only means less demand.
- Sources: https://support.google.com/publisherpolicies/answer/10400453 and https://support.google.com/adsense/answer/10437795 (undated) [G].

---

## 2. Blogger specifics

- **Earnings tab vs adsense.google.com.**
  - Blogger Help "Advertise on your blog": in Blogger choose the blog, then **Earnings → Create AdSense account (or Sign up for AdSense)**. Then add payment details and verify the phone. It also says "If your blog isn't currently eligible, learn how to qualify" (https://support.google.com/blogger/answer/1269077, undated) [G]. No 2025–26 notice of the tab's removal was found.
  - AdSense's URL rules list `example.blogspot.com` as valid: "Subdomains are only allowed on host partner sites like Blogger", and these "follow a different account creation process" (https://support.google.com/adsense/answer/2784438, undated) [G].
  - "Add a new site": for host-partner sites "you'll need to go to your host partner to add your site" (https://support.google.com/adsense/answer/12169212, undated) [G].
  - A Product Expert goes further: blogspot blogs "added in any other way will be rejected" (Blogger community thread 255336953, undated) [G-community].
  - **Use the Earnings tab.**
  - Folklore: the Earnings tab is missing until the blog is "eligible" (old blogs; stramaxon.com 2012 [S]).
- **Blogspot vs custom domain.**
  - Since the site-management change of **2023-03-20**, AdSense accepts "Sites that are managed by AdSense platform partners (e.g., site.blogspot.com)" (https://support.google.com/adsense/answer/12170421) [G].
  - No Google page says a custom domain raises the odds. The claim appears only on blogs [S].
  - What a custom domain changes is the process: it can also be added directly in AdSense like any domain (answer/12170421, answer/2784438) [G]. It also changes branding and portability.
  - Recommendation: not needed for approval. If you want one for the long term, connect it **before** applying, or wait until well after approval. Changing the URL during a review adds a variable.
- **ads.txt on Blogger.**
  - If the blog is "only configured to use AdSense using the Blogger-AdSense integration, then you don't need to manually set up ads.txt. Blogger will do this for you" (Blogger Help answer/1269077) [G].
  - Turn on **Settings → Monetization → Enable custom ads.txt** only for third-party networks or hand-placed AdSense code. If it is on, you must include `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0` yourself (line format from https://support.google.com/adsense/answer/12171612) [G].
  - After a change, the status may take a few days, and up to a month on low-traffic sites (https://support.google.com/adsense/answer/9785052) [G].
  - Correction to `daily/adsense-readiness.md` item 4: it says to set up ads.txt after approval. With the Earnings-tab integration, leave custom ads.txt **off**.
- **Review time.**
  - Google: "usually takes a few days, but in some cases it can take two to four weeks" (answer/12170222) [G].
  - Product Expert: "up to 6 weeks" [G-community].
  - 2026 blogs report anywhere from 48 hours to 2–3 months (adsenseaudit.net, techidea.online, 2026) [S].
- **Re-applying.**
  - No official waiting period. Fix, then **Request review** again on the Sites page (answer/12176698, answer/12170222) [G].
  - "Make sure you don't remove your site and resubmit it because this can delay the process" (answer/12170222) [G].
  - "Wait 2–4 weeks" is blog advice (techmessy.com 2026-07, adstimate.com 2026) [S]. It is still sensible, because the fixes need time to be recrawled.
- **PIN and identity** (details in §6).
  - Ads can start after approval, but payment needs the address PIN (mailed at about $10) and possibly identity verification (https://support.google.com/adsense/answer/157667) [G].

---

## 3. Posts, length, site age, traffic: evidence vs folklore

**What Google says.**
- No minimum number of posts, length, traffic or site age appears in eligibility (answer/9724) or readiness (answer/7299563) [G].
- Reviews guidance: "Focus on the quality and originality of your reviews, not the length" (https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews) [G].
- Publishing more, or more often, is not rewarded in itself. John Mueller said this, as reported by https://www.seroundtable.com/google-content-frequency-25367.html (about 2018) [S reporting G].
- **Site age rule.** A historical 6-month rule for applicants in China and India is repeated by old and new blogs (webnots.com; amitbhawani.com) [S]. It does not appear in current search extracts of answer/9724 or answer/13402307 [G]. It never applied to Korea or the US.
- **Volunteer opinion.** A Blogger Product Expert says a new blog with few posts is "not eligible" and should publish "for a long time (at least several months)" with "a decent amount of organic traffic" (thread 255336953, undated) [G-community]. This is opinion, not policy, but it reflects what volunteers see.

**2025–2026 case data** (all [S], all anecdotal):

| Case | Source / date |
|---|---|
| Approved with 7, 8 and 14 in-depth posts | https://inuidea.com/google-adsense-approval/ (2025–26) |
| 28-day-old blog, ~30 visits a day, approved in 6 days | https://blogerhub.com/adsense-approval-checklist-for-2026-step-by-step-for-new-blogs/ (2026) |
| 25 AI-assisted, human-edited posts, approved in 48 h (site 1.5 years old) | https://alex-hustler.medium.com/adsense-approval-in-2026-what-changed-and-what-still-works-c1cbbb66b32a (2026) |
| Blogspot blog with 296 posts still not approved; "some approved with 10 posts, some fail with 50" | https://m.dcinside.com/board/blogspot/306, https://worpsense.com/adsense-approval-probability-guide/ (2025) |
| 2026: low-value rejections common even at 30+ posts; cause cited is posts that rewrite search results | https://tali.kr/adsense-approval-2026, https://sta.tion.co.kr/content.php?slug=adsense-approval-2026 (2026) |
| AI-heavy sites approved after the AI-flagged pages were edited or unpublished | https://originality.ai/blog/adsense-rejects-site-ai-content (about 2023–24; vendor of an AI detector, biased) |
| AI affiliate rejections linked to fast publishing, the same template everywhere, no named author, thin archive/tag pages | https://adsenseaudit.net/guides/adsense-ai-content-policy-2026 (2026) |

**Folklore, with no Google basis:**
- "15–20" or "20–30" posts; "1,000–1,500+ words"; "3–6 months old"
- "X visitors a day"
- "remove affiliate links before applying" (okeyravi.com, undated)
- "Terms page required"

**Reading.**
- The anecdotes run from 7 posts approved to 296 rejected, so post count does not predict the result.
- 17 posts of 1,800–4,000 words already clears every folklore threshold.
- The remaining levers are distinctiveness, visible human accountability and some organic traffic.
- A few weeks of age plus search impressions in Search Console is a reasonable, if unproven, comfort margin.

---

## 4. Policies that put this kind of site at risk

| Policy | Google's wording (search extract) | Why it touches Verdict Picks |
|---|---|---|
| **Scaled content abuse** (Search spam policy, March 2024) | "many pages are generated for the primary purpose of manipulating search rankings and not helping users… no matter how it's created". Example: "Using generative AI tools or other similar tools to generate many pages without adding value for users"; "stitching or combining content from different web pages without adding value" (https://developers.google.com/search/docs/essentials/spam-policies [G]; announcement https://developers.google.com/search/blog/2024/03/core-update-spam-policies, 2024-03-05 [G]) | A scheduled routine publishes one AI-assisted roundup a day from the same template. The "stitching" example matches "summarise lab tests + owner reviews" unless the synthesis adds a real judgement |
| **Thin affiliation** | "product affiliate links where the product descriptions and reviews are copied directly from the original merchant without any original content or added value". "Not every site that participates in an affiliate program is a thin affiliate." Value-adds: "additional information about price, original product reviews, rigorous testing and ratings, navigation of products or categories, and product comparisons" (spam-policies page) [G] | Spec-sheet restatement is the danger. Comparisons, navigation hubs and price context are explicitly the cure |
| **Site reputation abuse** | "publishing third-party pages on a site in an attempt to abuse search rankings by taking advantage of the host site's ranking signals"; this applies "regardless of whether there is first-party involvement" (https://developers.google.com/search/blog/2024/11/site-reputation-abuse, 2024-11-19) [G]. A 2026-08 post reportedly changed EEA enforcement (https://developers.google.com/search/blog/2026/08/update-site-reputation-policy) [G, not opened] | **Not applicable.** It targets third-party sections on a strong host. A first-party blogspot blog has no reputation to borrow. Only relevant if guest or sponsored posts are ever accepted |
| **Reviews guidance / reviews system** | "Provide evidence such as visuals, audio, or other links of your own experience"; "Share quantitative measurements"; "Explain what sets something apart from its competitors"; "Discuss the benefits and drawbacks … based on your own original research"; "Describe how a product has evolved from previous models"; for a "best" pick, "include why you consider it the best, with first-hand supporting evidence"; "Consider including links to multiple sellers"; for ranked lists, "including original images from tests performed with the product" (write-high-quality-reviews) [G]. The reviews system rewards "insightful analysis and original research… written by experts or enthusiasts", and for review-heavy sites "any content within a site might be evaluated" (https://developers.google.com/search/docs/appearance/reviews-system) [G] | The biggest structural gap: no first-hand evidence, illustrations only, Amazon-only links. Being site-wide, the system judges the whole blog |
| **AdSense: ads on screens without publisher content / low value** | Ads not allowed on such screens; content must be "of value to the user and be the focal point"; Google "may limit or disable ad serving on pages with low value content" (publisherpolicies/answer/11112688) [G]. Companion: "automatically generated content without manual review or curation" (answer/11190248) [G]. "More ads or paid promotional material than publisher-content" is not allowed (https://support.google.com/publisherpolicies/answer/11169917) [G] | Buy boxes and "Check price" buttons arguably count as paid promotional material (inference). On a phone screen, buttons plus ads must not outweigh text |
| **Quality Rater Guidelines** | Jan 2025 update (2025-01-23): Lowest rating if "all or almost all of the MC … is auto or AI generated, or reposted from other sources with little to no effort, little to no originality, and little to no added value"; "the use of Generative AI tools alone does not determine the level of effort" (reported by https://www.searchenginejournal.com/google-updates-search-quality-rater-guidelines-what-to-know/538259/ and https://searchengineland.com/google-quality-raters-content-ai-generated-454161, 2025-01 [S quoting G]; PDF https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf [G], not opened). Sept 2025 update (2025-09-11) was "minor" (AI Overview examples, YMYL civic info) (https://www.seroundtable.com/google-search-quality-raters-guidelines-update-40092.html [S]). A claimed "June 2026" update appears only on marketing blogs and is **unverified; do not rely on it** | Raters look for effort, originality, who is responsible for the site, and first-hand experience compared with other pages on the same topic |
| **Helpful content (Who/How/Why)** | Warning questions: "Are you using extensive automation to produce content on many topics?"; "Are you producing lots of content on many different topics in hopes that some of it might perform well?"; bylines "where one might be expected"; disclose how content was produced, including "AI-assisted" content (https://developers.google.com/search/docs/fundamentals/creating-helpful-content) [G]. Helpful-content signals have been part of core ranking since March 2024 (https://developers.google.com/search/docs/appearance/ranking-systems-guide) [G] | Topic sprawl (pillows, jump starters, bidets, AI video tools, smart glasses) plus daily automation fits the first two warning questions. Narrower clusters help |
| **FTC fake-review rule** (outside Google) | Final rule announced 2024-08-14, in force 2024-10-21; bans fake or AI-generated reviews and testimonials (https://www.sidley.com/en/insights/newsupdates/2024/08/us-ftcs-new-rule-on-fake-and-ai-generated-reviews-and-social-media-bots, 2024-08) [S, law firm] | Never invent "we tested" claims or owner quotes. The current About page already says "we research; we do not lab-test", which is good |

**Recent updates.** All dates are via the Search Status Dashboard (https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history) [G], as reported by [S]:

| Update | Dates | Reported effect |
|---|---|---|
| Core | 2025-03-13 to 03-27 | — |
| Core | 2025-06-30 to 07-17 | Affiliate roundups reported hit (opinion) |
| Spam | 2025-08-26 to 09-22 | — |
| Core | 2025-12-11 to 12-29 | — |
| Spam | 2026-03-24 to 03-25 | — |
| Core | 2026-03-27 to 04-08 | One tracker claims 71% of monitored affiliate sites fell: https://www.affiversemedia.com/googles-march-2026-core-update-hit-affiliate-sites-harder-than-any-other-category/ [S, single dataset] |
| Core | 2026-05-21 to 06-02 | — |
| Spam | 2026-06-24 to 06-26 | — |
| Spam | 2026-08-18 to 08-21 | — |
| Spam | from 2026-09-24 | Possibly still rolling out today: https://www.searchenginejournal.com/google-september-2026-spam-update/590828/ |

Google never names "affiliate" as a target. Every affiliate-impact claim above is third-party analysis.

**What a reviewer or algorithm would likely look for.** These are inferred from the policies above.
- **Red flags:**
  - many near-identical AI roundups on a fixed daily drip
  - the same template on every page
  - unverifiable testing claims
  - spec-sheet restatement
  - Amazon-only links
  - no accountable person
  - thin label and archive pages
  - illustrations that could pass for product photos
- **What lowers the risk:**
  1. An exact "how this guide was made" box on every post. It says what was read, what was compared, that AI drafted parts, who checked it and when, and what was not verified. (Who/How/Why [G]; gen-AI guide [G])
  2. Original synthesis that is not available elsewhere:
     - own comparison table with sourced numbers
     - 3-year cost of ownership
     - "who should skip it"
     - what changed from the last model
     (Reviews guidance [G])
  3. A real, named, accountable editor with an author page. A real person can use initials and a short bio. Never a fictional expert. (Helpful content [G])
  4. Hand fact-checking of titles, meta descriptions, structured data and alt text as well as body text. (Gen-AI guide 2026-10-01 per [S])
  5. Where possible, links to a second seller (Walmart/Target/brand) alongside Amazon. (Reviews guidance [G]) These can be plain links; no second affiliate program is needed.
  6. Some first-hand evidence over time. Even buying 2–3 cheap featured products and photographing them is the single strongest upgrade. (Reviews guidance [G])
  7. Fewer, deeper posts, or a cadence that does not look machine-driven. Daily publishing is not penalised as such, but it is not rewarded either (Mueller [S]). Uniformity at scale is what the scaled-content policy describes.
  8. Topic focus: keep the home, cleaning, sleep and gadget clusters, and drop or move off-topic pieces.

---

## 5. Article composition: checklists from Google's guidance

**Per post** (sources: write-high-quality-reviews, creating-helpful-content, spam-policies, qualify-outbound-links, google-images [G]; Amazon policies [A])
1. **Byline** linking to an author/editor page. Bylines are "strongly encouraged … where readers might expect it", not required [G].
2. **"How this guide was made" box.** Sources read (lab outlets, number of owner reviews scanned, manuals), AI assistance disclosed, editor name and check date, what was not verified.
3. **Verdict up top:** who it is for and who should skip it.
4. **Quantitative comparison table** against 2–4 rivals, with every number attributed and dated. "Share quantitative measurements" [G].
5. **Pros and cons of equal weight**, "what sets it apart", and changes from the previous model [G].
6. **For ranked lists:** each item can stand on its own, and ideally links to a single-product review on the site. "Write a high quality ranked list … in combination with in-depth single-product reviews" [G].
7. **Citations as plain links** to the primary sources (lab test pages, manuals, recall databases).
8. **Images:**
   - Label illustrations as illustrations, in the caption.
   - Descriptive alt text and file names; images near the relevant text.
   - A real-URL cover image for `og:image` and image search (https://developers.google.com/search/docs/appearance/google-images) [G].
   - If any image is AI-generated, add IPTC `DigitalSourceType=TrainedAlgorithmicMedia`. This is recommended for web pages and required in Merchant Center (https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata) [G].
   - Illustrations can never serve as "evidence of your own experience".
9. **Amazon links:**
   - `rel="sponsored"` (or `sponsored nofollow`) on every affiliate link (https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links; https://developers.google.com/search/blog/2021/07/link-tagging-and-link-spam-update, 2021-07) [G].
   - "(paid link)" near the link, plus the sitewide sentence "As an Amazon Associate I earn from qualifying purchases" (https://affiliate-program.amazon.com/help/operating/agreement) [A].
   - Google sets no numeric affiliate-link limit. The practical limit is that content, not buttons, must dominate each screen (publisherpolicies/answer/11169917) [G].
10. **No Amazon star ratings, customer-review quotes or hard-coded prices.**
    - Amazon's policies page (reported effective 2026-04-14) allows prices or availability only when served by Amazon in the link or via Creators API / PA API. Customer reviews and star ratings are allowed only via the API (https://affiliate-program.amazon.com/help/operating/policies) [A].
    - **Check the daily template here.** The About page says "We report prices with their source and date". A dated price reported by a third party is safest phrased as "around $X at [outlet] in [month]". Avoid any statement of Amazon's own current price or star rating.
11. **Internal links with descriptive anchors.** No "click here"; `<a href>` only (https://developers.google.com/search/docs/crawling-indexing/links-crawlable) [G]. Link to the category hub and 2–3 related guides.
12. **Visible published and updated dates.** Keep structured data truthful: no invented ratings, author as a real person or an organization.

**Site level, before applying**
- About, Contact, Privacy (cookies and ads), Affiliate disclosure and How we rank pages. All exist; fix the wording noted in the Verdict.
- A menu linking the hubs, with labels as category hubs (inference) and breadcrumbs where possible (https://developers.google.com/search/docs/appearance/structured-data/breadcrumb) [G].
- No empty labels or archive pages, no broken links, no off-topic posts.
- Search Console verified with the sitemap submitted, so Google has crawled everything.

**Ad-friendly layout** (for after approval)
- Ads must not be "mistaken for other site content, such as a menu, navigation, or download links", and need care near buttons (https://support.google.com/adsense/answer/1346295) [G]. **Keep ads well away from the Amazon buttons.**
- "Enough content above the fold" (https://support.google.com/adsense/answer/132618) [G].
- Better Ads Standards: for example, no mobile ad density above 30% (https://support.google.com/publisherpolicies/answer/11127848) [G].
- Avoid "an excessive amount of ads that distract from or interfere with the main content" (https://developers.google.com/search/docs/appearance/page-experience) [G].

---

## 6. After approval

**ads.txt.** Leave Blogger's custom ads.txt **off** while you use only the Earnings-tab integration, because Blogger handles it (Blogger Help answer/1269077) [G]. If AdSense later shows an "ads.txt missing" warning, check https://acts39.blogspot.com/ads.txt first. Only then turn on custom ads.txt and paste the Google line (answer/12171612, https://support.google.com/adsense/answer/12171244) [G].

**Auto ads vs manual on Blogger.**
- Auto ads: Blogger → Earnings → "Control how ads are shown on your blog" → Auto ads → Save. Ads appear in about 10–20 minutes. A responsive theme is advised (https://support.google.com/adsense/answer/9155509) [G].
- Manual: Layout → Blog Posts gadget → "Show Ads Between Posts", or Add a Gadget → AdSense; in-article units (https://support.google.com/blogger/answer/1269077, https://support.google.com/adsense/answer/9189562) [G].
- The Auto ads **ad-load slider was removed** (announced 2026-03-11, launched 2026-04-16). It was replaced by "Maximum number of ads" and "Minimum distance between ads" for banners (https://support.google.com/adsense/answer/16683740) [G].
- Excluded areas use CSS selectors and apply to in-page ads only, not anchors (https://support.google.com/adsense/answer/12626543) [G].
- Page exclusions can be "This page only" or "All pages under this section" (https://support.google.com/adsense/answer/9262311) [G].
- Formats: in-page banner and multiplex; overlay anchor, vignette and side rail; intent-driven ad intents (https://support.google.com/adsense/answer/9261805, https://support.google.com/adsense/answer/9305577, vignette frequency https://support.google.com/adsense/answer/13956167) [G].
- **Ad intents** can turn words in the text into ad links. Each type can be turned off, or areas excluded with the `google-anno-skip` class (https://support.google.com/adsense/answer/13844047, https://support.google.com/adsense/answer/13829157) [G].
- **Recommendation (inference):**
  - Start with Auto ads plus anchor ads.
  - Ad intents **off**, so they do not compete with Amazon links in the text.
  - Vignettes on low frequency, or off at first.
  - Add `google-anno-skip` and an excluded area around the buy box.

**Ad density vs Amazon conversions.**
- No Google or Amazon data exists. Secondary sources only:
  - Time on page fell about 19.5% after adding display ads (https://diggitymarketing.com/display-ads-case-study/, undated [S]).
  - A claim of affiliate RPM $25–45 vs display $6–20 per 1,000 views (https://dev.to/danie_rozin/why-we-chose-affiliate-links-over-display-ads-and-the-revenue-math-behind-it-4em5 [S]).
- **Test on this site:**
  - Exclude the 3 best-converting guides from ads for 4 weeks.
  - Compare Amazon clicks per 1,000 views (Associates "Link type"/tracking IDs) against ad RPM on similar posts.
  - Keep whichever earns more per page.

**Core Web Vitals.**
- "Good" is LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1, at the 75th percentile (https://web.dev/articles/vitals) [G]. INP became a Core Web Vital on 2024-03-12 (https://web.dev/blog/inp-cwv-march-12) [G].
- Core Web Vitals are used by ranking systems (https://developers.google.com/search/docs/appearance/core-web-vitals) [G].
- Ads cause layout shift when they load late. Reserve space with `min-height` and avoid collapsing empty slots (https://web.dev/articles/optimize-cls, https://developers.google.com/publisher-tag/guides/minimize-layout-shift) [G].
- On Blogger, manual in-article units in a fixed-height wrapper control CLS better than Auto ads (inference).
- The posts' inline SVGs and large data-URI images already weigh on LCP. Check PageSpeed Insights on 2–3 posts before and after enabling ads.

**Amazon + AdSense together.**
- No Amazon rule forbids AdSense on the same site.
- Amazon forbids Special Links in pop-ups "in conjunction with the display of any site that is not your site", incentivised clicks, and offline or email use (https://affiliate-program.amazon.com/help/operating/agreement) [A].
- The site must hold original content; third-party material needs "significant commentary, analysis, or transformation" (https://affiliate-program.amazon.com/help/operating/participation/) [A].
- New accounts need **3 qualifying sales within 180 days** of applying, or the account is closed (https://affiliate-program.amazon.com/help/node/topic/G7MJTPEP9NC3YKMG) [A]. Check Associates Central for the deadline date.

**Account setup for a Korea-resident publisher.**

| Step | Rule | Timing | Source |
|---|---|---|---|
| Phone verification | At signup through Blogger | Day 0 | Blogger answer/1269077 [G] |
| Identity verification | Government photo ID, possibly a video selfie | Up to 45 days to complete; checks take up to 2 days; payments held until done | https://support.google.com/adsense/answer/4354737 [G] |
| Address PIN | Mailed when earnings reach the verification threshold (about $10, "can vary depending on your location"); 6 digits, standard international mail, "usually takes 3 weeks", no tracking | Request a replacement after 3 weeks (https://support.google.com/adsense/answer/1348257). Enter it within 4 months of generation or ads stop. 3 wrong entries also stop ads | https://support.google.com/adsense/answer/157667, https://support.google.com/adsense/answer/9668823 [G] |
| US tax info | Individuals outside the US file **W-8BEN** (Payments → Settings → Manage tax info). Once validly documented, "only the portion of your revenue earned from US users" is subject to US withholding. Without the form: up to 30% of US earnings, or up to 24% of worldwide earnings (backup withholding) for some account types | Do it right after approval, before the first payment | https://support.google.com/adsense/answer/10735961, https://support.google.com/paymentscenter/answer/10349995 [G] |
| Treaty rate | The US–Korea convention, Article 8 (industrial or commercial profits), taxes such profits in the US only through a US permanent establishment, which implies 0%. Korean bloggers commonly claim Article 8(1) at 0% (https://it.nogcha.kr/777, https://uknew.co/w-8ben/ [S]). If the income were treated as royalties, the treaty table gives 10–15% | **Confirm with a Korean tax adviser.** AdSense income is also taxable in Korea | https://www.irs.gov/pub/irs-trty/korea.pdf, https://www.irs.gov/individuals/international-taxpayers/tax-treaty-tables [IRS] |
| Payment method | **Wire transfer** to a Korean bank account in the payee's name (account number, SWIFT, bank name). Up to 15 business days; paid in USD | After the PIN and the threshold | https://support.google.com/adsense/answer/3372975, https://support.google.com/adsense/answer/6025222 [G] |
| Threshold and schedule | $100 for USD accounts. Last month's earnings are finalized around the 3rd. Holds must be cleared and the balance at or above the threshold by the 20th. Paid between the 21st and the 26th | Monthly | https://support.google.com/adsense/answer/1709871, https://support.google.com/adsense/answer/7164703 [G] |
| Amazon payouts (non-US) | Gift card ($10 minimum, no fee), check to a non-US address ($100 minimum, $15 fee waived), or International Direct Deposit where available. A tax interview (W-8BEN) must be validated before any payment; otherwise up to 30% withholding; 1042-S issued by March 15 | — | https://affiliate-program.amazon.com/help/node/topic/GGD9H76RMDDNEWAE, https://affiliate-program.amazon.com/help/node/topic/GPFZ6W6CF4E5BD9V [A] |

---

## What to do when

These dates assume today is 2026-10-05 and the blog launched in early September 2026. Each step points to the section that sources it.

### Before applying (2026-10-05 → about 2026-10-25)
1. **This week** (§1 Verdict, §4 Helpful content, §5 site level):
   - Change the About page's "based in the United States" to a true statement, for example "edited from Seoul for US shoppers".
   - Replace "the Verdict Picks editors" with a real, named editor, initials allowed, plus a short author page. Never a fictional expert.
   - Keep the Vera illustration clearly labelled as fictional, as it already is.
2. **This week** (§1 low value, §4 helpful content): move, rewrite or unpublish the off-topic `claude-higgsfield-mcp-ai-video` post. Decide the 4–6 category clusters the blog covers.
3. **This week** (§1 site down, §5 site level):
   - Blogger settings: reader access Public, visible to search engines, HTTPS redirect on.
   - No crawler-blocking robots.txt.
   - Verify Search Console and submit the sitemap.
4. **By 10-15** (§5 per post, §4 risk list):
   - Add the "How this guide was made" box (sources, AI disclosure, editor and date, unverified items) to the daily template and to all existing posts.
   - Make sure every Amazon link carries `rel="sponsored"`.
   - Check that no post states an Amazon current price, Amazon star rating or quoted Amazon customer review (§5 item 10).
5. **By 10-20** (§4, §5 items 4–6):
   - Upgrade the 5 strongest posts first: own comparison table vs rivals, previous-model changes, "who should skip it".
   - Add a second-seller link where one exists.
   - If at all possible, buy 1–3 cheap featured items and add real photos labelled as your own (the single strongest first-hand signal).
6. **By 10-20** (§1 insufficient content, §5 site level):
   - Every hub and label page has paragraphs of text.
   - No empty labels; a menu reaches every hub and policy page; mobile layout checked.
   - Remove buttons-only screens.
7. **Throughout** (§3, §4 scaled content):
   - Keep publishing, but favour depth over cadence.
   - If the routine can't add original synthesis on a given day, skip that day rather than publish a thin roundup.
   - Hand-check titles, meta descriptions, alt text and structured data for each post (gen-AI guide, reportedly revised 2026-10-01).

### Applying (about 2026-10-26 → 11-02)
8. In Blogger: **Earnings → Sign up for AdSense** (§2). Use the owner's legal name and Korean address exactly as on ID, because the PIN letter goes there. Verify the phone.
9. Do **not** also add the site at adsense.google.com, enable custom ads.txt, or change the domain during review (§2).
10. Wait. Status "Getting ready" can take days to about 4 weeks (§2). Do not remove and re-add the site.

### After approval
11. **Day 0–1** (§6):
    - Turn on Auto ads with ad intents off, vignettes off or low, and anchor on.
    - Exclude the buy-box area; add `google-anno-skip`.
    - Check there are no ads next to the Amazon buttons.
12. **Day 0–7** (§6 table): submit W-8BEN (take treaty advice first); complete identity verification if asked (45-day limit); add wire-transfer bank details.
13. **Week 1–2** (§6 CWV): run PageSpeed Insights on 3 posts and fix CLS by reserving ad space or using manual units.
14. **When earnings pass about $10** (§6 table): watch for the PIN letter, which takes about 3 weeks. Request a new one after 3 weeks. Enter it within 4 months.
15. **Weeks 2–6** (§6 density test): exclude the 3 best Amazon-converting posts from ads and compare revenue per 1,000 views.
16. **Ongoing:**
    - Leave custom ads.txt off unless AdSense flags it (§6).
    - Check the Policy center monthly (§1).
    - First payout comes on the 21st–26th of the month after the balance reaches $100 (§6).
    - Separately, make sure Amazon's 3-sales-in-180-days deadline is met (§6).

### If rejected
17. Read the exact reason in AdSense → Sites. Map it to the table in §1.
18. For **Low value content**:
    - Strengthen what exists (steps 4–6) rather than adding posts.
    - Unpublish the weakest 20–30% of posts or merge them into hubs.
    - Add first-hand photos to the top guides.
    - The Korean 2026 reports say "rewrite, don't add" ([S], §3).
19. Allow 2–4 weeks for recrawl (blog advice, no Google rule; §2). Then click **Request review** on the same site entry.
20. After a second low-value rejection: reduce the publishing cadence, run a deliberate sweep that adds original evidence, and wait a further month of organic traffic before the third request.
