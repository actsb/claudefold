# Verdict Picks — Amazon deep-dive buying guides (Blogger)

Working repository for the English-language Google Blogger site
**Verdict Picks** (blog ID `9072207571822466986`).

The site's editorial promise: pick the products US Amazon shoppers search
for most, cross-reference independent lab tests with the recurring themes
in thousands of owner reviews, compare every relevant brand, and end with
one clear verdict per household type — so a reader can choose and buy in
minutes.

## What is in this repo

| Path | What it is |
|---|---|
| `brand/brand-kit.md` | Blog name, tagline, positioning, voice, visual identity, naming alternatives |
| `brand/blogger-setup-guide.md` | Click-by-click Blogger configuration (make the blog public, SEO, EU cookie notice, labels, pages, layout, monetization compliance) |
| `brand/categories-and-labels.md` | The category system (implemented as Blogger labels + a top nav), post-type labels, and the exact label strings to use |
| `brand/editorial-workflow.md` | How to pick the next product, the research checklist, article structure, and the quality bar every post must clear |
| `brand/pages/*.html` | Static pages ready to paste into Blogger → Pages → New page → HTML view (About, How We Rank, Affiliate Disclosure, Privacy & Cookies, Contact) |
| `brand/templates/post-template.html` | Reusable post skeleton (quick-picks table, spec boxes, pros/cons, video embeds, FAQ, sources) |
| `posts/2026-09-best-robot-vacuums/post.html` | **Launch article** — Blogger-ready HTML, 7,000+ words, inline SVG graphics, YouTube video + Shorts embeds |
| `posts/2026-09-best-robot-vacuums/post-meta.md` | Title, labels, search description, permalink, and the publishing checklist for that post |
| `posts/2026-09-best-robot-vacuums/research-notes.md` | Data and sources the article is built from |
| `posts/2026-09-best-robot-vacuums/images/` | The article graphics as `.svg` (inline in the post) and `.png` (for upload via the Blogger image tool) |
| `scripts/` | `build_post.py` (inlines the SVGs into the post), `check_post.py` (word count / HTML / link / embed audit), `render_png.mjs` (SVG → PNG via Chromium) |

## Publishing a post (short version)

1. Blogger → Posts → **New post** → switch the editor to **HTML view** (the `<>` icon).
2. Paste the contents of `posts/<slug>/post.html`.
3. In the right-hand post settings: add the **Labels**, the **Search Description**, and the custom **Permalink** listed in `post-meta.md`.
4. Replace every `YOURTAG-20` with your Amazon Associates tracking ID.
5. Preview, check the video embeds play, then **Publish**.

Full detail: `brand/blogger-setup-guide.md`.

## Rebuilding the launch article

```bash
python3 scripts/build_post.py posts/2026-09-best-robot-vacuums   # inline SVGs -> post.html
python3 scripts/check_post.py posts/2026-09-best-robot-vacuums/post.html
node scripts/render_png.mjs posts/2026-09-best-robot-vacuums/images  # optional PNG copies
```

## Two ways to publish without copy-pasting

1. **One-file import (no credentials):** Blogger → Settings → Manage blog → **Import content** → choose
   `posts/2026-09-best-robot-vacuums/blogger-import.xml` → tick *Automatically publish all imported posts and pages*.
   Imports the launch post (with its 6 labels) and the 5 static pages. Regenerate with `python3 scripts/make_blogger_import.py [--draft]`.
2. **API publish (from this repo):** mint a 1-hour token at https://developers.google.com/oauthplayground
   (scope *Blogger API v3 → https://www.googleapis.com/auth/blogger*), then
   `BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py [--draft|--check]`.
   Creates/updates the 5 pages and publishes the post; idempotent by title.

Blog *settings* (public visibility, title, description, search-description toggle) are not exposed by the API — those are five clicks in Settings, listed in `brand/blogger-setup-guide.md`.
