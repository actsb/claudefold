# Tasks for Claude in Chrome (the owner's own signed-in Chrome)

Blogger's API cannot change settings, layout or a post's search description, and this repository's cloud sessions cannot reach blogger.com at all. These tasks therefore run in the owner's own Chrome, where Blogger, Search Console and Pinterest are already signed in, through the **Claude in Chrome** extension.

**How to start (owner, once):**
1. Install the extension: Chrome Web Store → search "Claude" (publisher: Anthropic) → **Add to Chrome** → pin it → sign in with the same Claude account.
2. Open a Claude conversation that has Claude in Chrome turned on: the Claude desktop app, claude.ai, or the Chrome side panel. In a Claude Code conversation, use the **+** menu in the message box: if it offers your computer or browser, pick it before sending.
3. Send: *"Open https://github.com/actsb/claudefold/blob/claude/sharp-lovelace-n7vhzq/daily/chrome-tasks.md and do the tasks marked 'now', one by one. Ask me before anything marked 'ask first'. Report what you changed."*
4. Allow the sites it asks for (blogger.com, search.google.com, bing.com, pinterest.com).

**Rules for the Claude session doing this:** work in new tabs; never change the blog's theme HTML, delete anything, or touch payment, tax or account-security pages; stop and ask when a page looks different from these steps; after each task, tick it here only by telling the owner (this file is updated from the repository side).

---

## 1. Search descriptions (now)
For every post in https://github.com/actsb/claudefold/blob/claude/sharp-lovelace-n7vhzq/daily/search-descriptions.md:
blogger.com → **Posts** → open the post (match the title) → right-hand panel **Post settings → Search description** → paste the text from the list exactly → **Update** (top right). Do not change anything else in the post. Skip a post whose field already holds the same text.

## 1b. Blog-wide description texts (now)
The blog's own description texts still say the guides distill "thousands of Amazon reviews", which the guides no longer use (Amazon's affiliate rules). The blog-wide search description is also what Blogger shows as the share text for pages without their own.
1. blogger.com → **Settings** → **Meta tags** → **Search description** (the blog-wide one) → replace with: `Verdict Picks compares every brand, distills lab tests and owner reports, and tells you which product to buy for your home, budget and needs.` → **Save**.
2. **Settings** → **Basic** → **Description** → replace with: `Deep-dive buying guides for the products Americans shop for most: every brand compared, lab tests and owner reports distilled, one clear verdict.` → **Save**.

## 2. Navigation shows every trust page (now)
blogger.com → **Layout** → the **Pages** gadget (top navigation) → **Edit** → tick: About Verdict Picks, How We Rank Products, Affiliate Disclosure, Privacy & Cookie Policy, Contact Us, and the category hubs (Robot Vacuums, Wireless Earbuds, Smart Glasses, Power Stations, Best Sellers) → **Save**.

## 3. Search Console and sitemaps (now; the Korean step-by-step with the request-indexing order is daily/search-console-bing.md)
1. https://search.google.com/search-console → property **https://acts39.blogspot.com/** (add it as a URL-prefix property if it is missing; Blogger blogs owned by the same Google account usually verify automatically).
2. **Sitemaps** → submit `sitemap.xml` and `sitemap-pages.xml`.
3. **URL inspection** → request indexing for the five newest posts in the description list (the daily quota is small; do not repeat for the same URL).

## 4. Bing Webmaster Tools (now)
https://www.bing.com/webmasters → sign in → **Import from Google Search Console** → choose acts39.blogspot.com → import (this brings the sitemaps too).

## 5. Pinterest without the API (ask first)
Only if the owner has a Pinterest business account: Pinterest **Settings → Bulk create Pins → Auto-publish** → RSS `https://acts39.blogspot.com/feeds/posts/default?alt=rss` → board **Best of Amazon 2026** → save. (Turn it off once the API automation in daily/pinterest-setup.md is live.)

## 6. Crawl settings check (check now; change only with the owner's OK)
1. robots.txt answered 404 in the October 5 crawl check (daily/search-console-bing.md). In **Settings → Crawlers and indexing**, report whether **Enable custom robots.txt** is on. With the owner's OK: if it is on, turn it off (Blogger's default robots.txt comes back); if it is off and robots.txt still answers 404, turn it on and paste exactly the text in daily/search-console-bing.md section 3. Never type `Disallow: /`.
2. blogger.com → **Settings**: **Privacy → Visible to search engines** is on; **Permissions → Reader access** is Public; **HTTPS → HTTPS redirect** is on; **Crawlers and indexing → Enable custom robots.txt** is off.
3. Same section → **Enable custom robots header tags**. The recommended values: home page `all`; archive and search pages `noindex`; posts and pages `all`; never `nosnippet`. Report what is set now; change it only after the owner says yes.
4. Open any post, View page source (Ctrl+U), search for `max-image-preview`. If it is missing, tell the owner; the line `<meta content='max-image-preview:large' name='robots'/>` goes right after `<head>` in Theme → Edit HTML, which the owner does (theme HTML is off-limits for this session).

## 7. Amazon disclosure in the footer (now)
blogger.com → **Layout** → in the footer (or the sidebar) **Add a Gadget** → **Text** → leave the title empty → content: `As an Amazon Associate I earn from qualifying purchases.` → **Save** → **Save arrangement** if shown. Skip if a gadget with this sentence already exists.

## 8. Google AdSense application (ask first; apply between October 26 and November 2, 2026, see daily/strategy-2026-10.md section 3)
blogger.com → **Earnings** → **Sign up for AdSense** → follow the Google screens with the owner present (name, address and payment details are the owner's to enter, exactly as on their ID, because the PIN letter goes to that address). Do not add the site at adsense.google.com, and do not turn on custom ads.txt.

## 9. Amazon Associates account check (view only; ask before any change)
https://affiliate-program.amazon.com → **Account Settings** → **Edit Your Website and Mobile App List**: report whether `https://acts39.blogspot.com` and the full Pinterest profile URL are listed. Adding a missing one is a change: ask first. Also report the account's sign-up date (for the 180-day, three-sale deadline) if the home page shows it. Do not open the tax or payment pages; the owner does those.
