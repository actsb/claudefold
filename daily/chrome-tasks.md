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

## 2. Navigation shows every trust page (now)
blogger.com → **Layout** → the **Pages** gadget (top navigation) → **Edit** → tick: About Verdict Picks, How We Rank Products, Affiliate Disclosure, Privacy & Cookie Policy, Contact Us, and the category hubs (Robot Vacuums, Wireless Earbuds, Smart Glasses, Power Stations, Best Sellers) → **Save**.

## 3. Search Console and sitemaps (now)
1. https://search.google.com/search-console → property **https://acts39.blogspot.com/** (add it as a URL-prefix property if it is missing; Blogger blogs owned by the same Google account usually verify automatically).
2. **Sitemaps** → submit `sitemap.xml` and `sitemap-pages.xml`.
3. **URL inspection** → request indexing for the five newest posts in the description list (the daily quota is small; do not repeat for the same URL).

## 4. Bing Webmaster Tools (now)
https://www.bing.com/webmasters → sign in → **Import from Google Search Console** → choose acts39.blogspot.com → import (this brings the sitemaps too).

## 5. Pinterest without the API (ask first)
Only if the owner has a Pinterest business account: Pinterest **Settings → Bulk create Pins → Auto-publish** → RSS `https://acts39.blogspot.com/feeds/posts/default?alt=rss` → board **Best of Amazon 2026** → save. (Turn it off once the API automation in daily/pinterest-setup.md is live.)

## 6. Google AdSense application (ask first; see the timing in daily/strategy-2026-10.md)
blogger.com → **Earnings** → **Sign up for AdSense** → follow the Google screens with the owner present (name, address and payment details are the owner's to enter).
