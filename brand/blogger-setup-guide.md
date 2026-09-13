# Blogger Setup Guide — Verdict Picks

Blog dashboard: https://www.blogger.com/blog/posts/9072207571822466986

Work through this top to bottom once. Every step is a Blogger UI setting; nothing needs code except the HTML pages provided in `brand/pages/`.

> **Status:** blog address is `acts39.blogspot.com`, reader access is already **Public**, the five pages and the launch post were imported on 2026-09-12. Blogger auto-shows the EU cookie notice; step 8 covers what it does not.  

---

## 1. Basic identity — `Settings → Basic`

| Setting | Value |
|---|---|
| **Title** | `Verdict Picks` |
| **Description** | `Deep-dive buying guides for the products Americans search for most on Amazon — every brand compared, thousands of owner reviews distilled, one clear verdict.` (this text is what many themes show under the title and what Google uses when no search description exists) |
| **Blog language** | English (United States) |
| **Adult content** | Off |
| **Google Analytics Measurement ID** | Optional now; add a GA4 `G-XXXXXXX` ID later. If you add it, the Privacy page already discloses Analytics. |
| **Favicon** | Upload a square PNG (≤100 KB) — navy square with white "VP". |

## 2. Privacy — `Settings → Privacy`

* **Visible to search engines** → **ON**. (Off means Google is asked not to index the blog. A review blog with no search traffic has no readers.)

## 3. Publishing — `Settings → Publishing`

* **Blog address**: try `verdictpicks.blogspot.com`; fallbacks in `brand-kit.md`.
* **Custom domain**: skip until the blog has 20+ posts; when you add one, keep **Redirect domain** on so `verdictpicks.com` and `www.verdictpicks.com` both work.

## 4. Permissions — `Settings → Permissions` ← this is why the blog is "private"

* **Reader access** → **Public**. (Currently "Private to authors" — nobody but you can open it.)
* Blog admins and authors: only you for now.

## 5. HTTPS — `Settings → HTTPS`

* **HTTPS redirect** → ON.

## 6. Posts — `Settings → Posts`

* **Max posts shown on main page**: 10.
* **Image lightbox**: ON (lets readers zoom the comparison charts).

## 7. Comments — `Settings → Comments`

* Comment location: Embedded. Who can comment: Users with Google accounts. Comment moderation: **Always** (affiliate blogs attract spam). Reader comment captcha: ON.

## 8. EU cookie notice + privacy — what the dashboard message means

Blogger already injects a notice for EU visitors that covers **Google's** cookies (Blogger, Analytics, AdSense). It does **not** cover:
* **Amazon Associates links** (Amazon sets a 24-hour attribution cookie when a reader clicks through), and
* **YouTube embeds** (Google/YouTube cookies from the video player).

So:
1. Publish the **Privacy & Cookies** page from `brand/pages/privacy-policy.html` (it names all three parties) and link it in the footer (step 12).
2. Leave Blogger's automatic notice **on** (it is on by default). Do not add a second cookie banner.
3. To confirm the notice really displays, view the blog from an EU location (a VPN exit in Germany/France works) — Blogger only shows it to EU visitors.
4. If you later add a third-party widget (e.g., a price-tracking script), extend the Privacy page.

## 9. Meta tags — `Settings → Meta tags`

* **Enable search description** → ON. This unlocks the per-post **Search Description** field (the meta description Google shows). Every post in this repo ships with one in its `post-meta.md`.
* **Search description** (blog-level): `Verdict Picks compares every brand, distills thousands of Amazon reviews, and tells you exactly which product to buy for your home, budget, and needs.`

## 10. Crawlers and indexing — `Settings → Crawlers and indexing`

* **Enable custom robots.txt** → ON, paste:
  ```
  User-agent: *
  Disallow: /search
  Allow: /
  Sitemap: https://acts39.blogspot.com/sitemap.xml
  ```
  (Replace `YOURADDRESS`. Blocking `/search` prevents thin label/search pages from being indexed as duplicates.)
* **Enable custom robots header tags** → ON. Home page: `all`, `noodp`. Archive and search pages: `noindex`, `noodp`. Post and page: `all`, `noodp`.
* Google Search Console: verify the blog (Blogger blogs are auto-verified when you open Search Console with the same Google account) and submit `sitemap.xml`.

## 11. Formatting — `Settings → Formatting`

* Time zone: your US time zone (e.g., `(GMT-05:00) Eastern Time`). Date header format: `Monday, January 1, 2026`. Timestamp: `9:00 AM`.

## 12. Theme and layout — `Theme` and `Layout`

1. **Theme** → choose **Emporio** (grid) or **Contempo**. Click **Customize** → set the accent color to `#1E8E5A` and headings to `#1B2A41` (Advanced → colors).
2. **Layout** → add/arrange gadgets:
   * **Pages** gadget (top, "Show as: Top tabs") — add the five pages from step 13 plus one **link per category** pointing to its label URL, e.g. `https://acts39.blogspot.com/search/label/Robot%20Vacuums`. This is how Blogger's flat labels become a category menu.
   * **Featured Post** (sidebar/top) — pin the current flagship guide.
   * **Labels** gadget — Display: *Selected labels* → tick only the category labels (not the post-type labels), Sort: alphabetically, Show number of posts: on.
   * **Popular Posts** — last 30 days, 5 posts, thumbnails on.
   * **Search box**.
   * **HTML/JavaScript** gadget in the footer: paste the affiliate disclosure sentence and links to Privacy, Disclosure, Contact (see `brand/pages/README` notes inside each page).
3. **Theme → Customize → Advanced → Add CSS** — paste the contents of `brand/templates/theme-additions.css` (verdict box, spec tables, badge pills, responsive video). Blogger keeps `<style>` inside posts too, but theme-level CSS survives theme edits and keeps posts lighter.

## 13. Pages — `Pages → New page` (switch to HTML view before pasting)

| Page title | File | Path suggestion (Blogger picks it from the title) |
|---|---|---|
| About Verdict Picks | `brand/pages/about.html` | `/p/about-verdict-picks.html` |
| How We Rank Products | `brand/pages/how-we-rank.html` | `/p/how-we-rank-products.html` |
| Affiliate Disclosure | `brand/pages/affiliate-disclosure.html` | `/p/affiliate-disclosure.html` |
| Privacy & Cookie Policy | `brand/pages/privacy-policy.html` | `/p/privacy-cookie-policy.html` |
| Contact Us | `brand/pages/contact.html` | `/p/contact-us.html` |

Each page: Options → Reader comments: **Don't allow**.

## 14. Amazon Associates (monetization) — do this the same day you go public

1. Apply at https://affiliate-program.amazon.com with the live blog URL. You get a tracking ID that looks like `verdictpicks-20`.
2. The ID is `verdictpicks-20`, and every Amazon link in the posts already carries it (all links in this repo are Amazon search links, e.g. `https://www.amazon.com/s?k=Roborock+Saros+10R&tag=verdictpicks-20`, so they work before you have product ASINs).
3. Amazon gives you **180 days to make 3 qualifying sales** or the account is closed; publish 5–8 guides before applying so there is traffic.
4. Product photos: use **SiteStripe → Image** on the Amazon product page (paste the generated `<a><img></a>` code into the post's image slots). Amazon's operating agreement does not allow hot-linking product images any other way; the image slots in the launch post are clearly marked.
5. Prices: do not paste live Amazon prices into text. Use manufacturer list price and "typically on sale for…" phrasing (this is how the launch post is written), or Amazon's own PA-API/SiteStripe widgets.
6. Disclosure: the sentence "As an Amazon Associate I earn from qualifying purchases." must be visible near the top of every post (already in the template) and on the Disclosure page.

## 15. Publishing a post (repeat for every article)

1. **Posts → New post → HTML view** (`<>` icon) → paste `post.html`.
2. Right sidebar → **Labels**: paste the comma-separated list from `post-meta.md`.
3. **Search Description**: paste from `post-meta.md` (≤155 characters).
4. **Permalink → Custom permalink**: paste the slug from `post-meta.md`.
5. **Options**: Reader comments: Allow. Compose mode: leave as is. Line breaks: *Use <br> tag* is off (keep off so pasted HTML keeps its paragraphs).
6. Upload the PNG copies of the graphics (`images/*.png`) with the image toolbar **only if** the inline SVGs do not display in Preview (they normally do).
7. **Preview** → confirm: verdict box renders, tables scroll on mobile, every YouTube embed plays (if one shows "Video unavailable", swap the ID — a list of alternates is in `post-meta.md`).
8. **Publish**. Then share the URL in Search Console → URL inspection → Request indexing.

## 16. Blogger "beta features" from the dashboard message

* **Google Search links** (auto-inserted keyword links): leave **off** for now. They add outbound links Google chooses, not you, and they can pull readers away from the affiliate links.
* **Google Search previews**: harmless, but unnecessary for product content. Skip.
