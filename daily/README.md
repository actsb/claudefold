# Daily product of the day — runbook

One guide a day, inside the blog's clusters: either one popular product with the best value in its category ("product of the day"), or a roundup that compares several (section 11). Researched to the end, written for a US shopper who wants to buy today. This file is the complete procedure; a fresh session with no memory of earlier work can follow it top to bottom. The plan behind the queue (clusters, seasonal deadlines, commission rates) is in `daily/strategy-2026-10.md`.

## 0. Ground rules (never skip)

* **Truth first.** Every number is attributed and dated ("reported by X in month 2026", "at the time of writing"). No live Amazon price is ever stated as fact; the buttons show today's price. No invented reviews, quotes, ratings or people.
* **Experts are real, cited and linked.** The "What the experts say" section paraphrases or briefly quotes published sources a search snippet supports (Consumer Reports, Wirecutter, America's Test Kitchen, a university extension office, a professional association, a named engineer/dermatologist/vet writing under their own name). Never fabricate a name, a title or a quote. Vera is an illustration and is labelled as one.
* **Amazon data rules (Associates Program Policies; the account is still in its 180-day review).** Never show Amazon star ratings or averages, Amazon rating or review counts, five-star shares, Amazon customer-review or Q&A quotes or close paraphrases, or digests built from them (TheReviewIndex, ReviewMeta, Fakespot). Never state an Amazon price as a number, including dated Amazon prices from deal posts or trackers (camelcamelcamel, Keepa). Allowed: ratings, counts and owner reviews from other retailers (Walmart, Best Buy, Home Depot, Lowe's, Target, Costco, the brand's own store) with source and date; forum and expert reviews; our own analysis; price bands ("under $50") or a non-Amazon price with its source and date; buttons that say "See today's price". Avoid Amazon rank or badge claims ("#1 on Amazon", "Amazon's Choice"): say "our top pick". Titles, covers, pins and search descriptions follow the same rules. `check_post.py` fails a post that breaks them.
* **Depth over cadence (AdSense and Google's scaled-content policy).** A day's post must add something a reader cannot get from one listing: a comparison with sourced numbers, a who-should-skip-it verdict, the cost of ownership, what changed from the last model. If the research cannot support that, publish nothing that day and say why in the report. Stay inside the blog's clusters (home cleaning; sleep and home comfort; kitchen; car; pets; bathroom) unless daily/strategy-2026-10.md says otherwise. Every post links to 2–3 of our related guides in its body (descriptive anchors), and the "More guides" block (`scripts/site_index.py --inject`) links the rest.
* **Links are cards, two or three to a row, never a stack of text links.** Wherever a page offers several things to click through to (products to buy, our own guides to read), they are cards in a grid: two to a row in the post column (three where the column is wider), one to a row for product cards and two for guide cards on a phone. Each card has a coloured bar on the left, a small pill, the picture on the left, the name in bold, one highlight sentence in colour, a grey detail line, a small line with the price band, where and when ("About $50 · US retailers, Oct 2026"; on guide cards "Updated <date>") and the call to action with a round arrow button at the bottom. Never a vertical stack of full-width boxes that each end in a text link. `scripts/link_cards.py` builds every one of them: the buy box, picks whose `<!--CARD:id-->` markers sit next to each other (they share a grid), any list written as `<ul class="vp-linkcards">` (section 4), the More guides block and the Best Sellers hub. A single product stays one full-width card, and a link inside a sentence stays in the sentence. The price line never sits next to the word Amazon (`check_post.py` fails it): the band is what US retailers charged, and the button says "See today's price".
* **Disclosure before the first paid link**: the byline sentence, "(paid link)" next to every Amazon link and button (the assembler adds it wherever it is missing), the Korean summary opens with "[제휴 링크 포함]".
* **Videos**: only English-language YouTube embeds whose titles were confirmed in search results; official iframe with `?rel=0`; a "Watch on YouTube" link; no downloaded thumbnails. Our own clips: no people, no Korean text.
* **Images**: our own renders/infographics/photos only. No Amazon product images, no hotlinking, no vendor logos.
* **Tone**: plain, specific, a little dry humour, no hype words ("game-changer", "must-have"). Short sentences. Cons get the same space as pros.

## 1. Setup (fresh session)

```bash
bash scripts/bootstrap.sh            # ffmpeg-static + sharp into the scratchpad; prints FFMPEG and NODE_PATH
export FFMPEG=<printed path>
```

## 2. Pick today's product

`daily/queue.json` holds the queue, in the order to write it. **First finish unfinished work:** if an entry is at `"status": "writing"` and its folder has no checked `post.html` or still holds WRITE markers (a roundup can take two runs), today's job is to finish that entry. Otherwise take the first entry with `"status": "queued"`; the `"date"` field is only the plan, and `daily_post.py new` replaces it with the day the post is written. Entries at `"parked"` are skipped. If no queued entry is left, run the refill research (prompt in section 8) and append 14 new entries first. An entry with `"format": "roundup"` follows section 11.

## 3. Research (three agents, in parallel, ~50 searches each)

1. **Owners**: what owners say after weeks/months (praise, complaints, failure modes, sizes/variants that matter, questions people actually ask, counterfeit or fulfilment issues). Sources: Reddit threads, forum posts, and owner reviews at other retailers (Walmart, Best Buy, Home Depot, Lowe's, Target, Costco, the brand's own store), each with its date. Not Amazon customer reviews, ratings or Q&A: section 0 keeps them off the page, so they must not shape it either.
2. **Video and experts**: English YouTube reviews/how-tos with exact titles and IDs from result URLs (never guess an ID); published expert sources (CR, Wirecutter, ATK, RTINGS, universities, professional bodies) with what each actually says; the product's official manual/instructions for the how-to section.
3. **Price and channels**: dated prices at Walmart, Target, Costco, Home Depot, the brand's own store and Temu/AliExpress look-alikes, plus the brand's list price; Subscribe & Save, bundles, warranty/registration, return windows; how deep past sales went in percent (Prime Day, Big Deal Days, Black Friday); the honest "when Amazon is not the cheapest". Amazon's own prices are never published (section 0), so the post speaks in bands and percent-off rules.

Save the three briefs to `research/daily-<date>-<slug>.md`.

## 4. Scaffold and write

```bash
python3 scripts/daily_post.py new <key>          # creates posts/<date>-<slug>/ from the queue entry
```

Then edit `posts/<dir>/cards.json` (product card, optional accessory cards, `buy` dicts, `video` fields), the new guide's card on `brand/pages/hub-best-sellers.html` (its one line, section 7), `cover.json` (bright style; title lines, subtitle, pin bullets, url) and `strips.json` (one four-panel "in real life" strip). Write `src/00-easy.html` following `daily/template-00-easy.html` section by section; the template's `<!-- WRITE: ... -->` comments say what each part must contain. Target 1,800–2,600 words of body text. Question-form H2s. Ten Quick answers (they become the FAQ schema).

**Several links in one place are written as a link-card list** (section 0): alternatives, "also consider", "more of our guides". Write `<ul class="vp-linkcards">` with one `<li>` per product or guide, in one of these patterns, and the assembler turns the list into cards (a product that has a card in `cards.json` gets its render and price band; a guide gets its picture, title and date from the site index):

```html
<ul class="vp-linkcards">
<li><strong>Cheaper:</strong> the <a href="https://www.amazon.com/s?k=...&amp;tag=verdictpicks-20">Product name</a> (price band, source) — one sentence on who it suits.</li>
<li><span style="…border-radius:999px…">Best overall</span> <strong>Product name</strong> — the verdict in a clause: the detail. <a href="https://www.amazon.com/s?k=...">See on Amazon</a></li>
<li>Why this reader needs it next: our <a href="/2026/10/....html">guide name</a>.</li>
<li><span style="…border-radius:999px…">Skip</span> <strong>Product</strong> — why. (no link: a note card)</li>
</ul>
```

Picks that belong together get their `<!--CARD:id-->` markers on consecutive lines: they share one grid, two to a row. A marker on its own stays a full-width card.

Product art: `cards.json` `"category"` must be a renderer in `scripts/product_cards.py` (`generic` with an `"art": {"shape": "box|bottle|cylinder|flat|sphere|bag", ...}` works for anything). Dedicated renderers exist for `purifier` (a Core 300-style tower), `robot`, `earbuds`, `glasses`, `power`, `tracker`, `bottle`, `cleaner`, `groomvac`, `roller`, `litterbot`, `harness`, `kong`, `bags`, `chat`, `film`, `voice`, `lightbox`, `tripod` and `ssd`; add one to `DRAW` when a product deserves its own silhouette. A second card for the consumable (filter, refill, bag) with its own `buy` dict puts the repeat purchase in the buy box.

## 5. Build, check, preview

```bash
python3 scripts/daily_post.py build posts/<dir>   # cards, strips, cover, pin, infographic, assemble, SEO layer, build, check, PNGs
node scripts/preview_post.mjs posts/<dir>/post.html <scratch>/prev/day 760 4000
node scripts/preview_post.mjs posts/<dir>/post.html <scratch>/prev/dayphone 390 3000
```
Look at the first and last slices at both widths. Fix overlaps before publishing. Link cards (buy box, grids of picks, More guides) sit two to a row at 760 px; at 390 px product cards are one to a row and guide cards two.

## 6. Publish

**Image hosting.** Blogger's API has no image upload. The cover stays a real URL (`images/cover.jpg` on GitHub Pages) so Google can crawl it, index it and use it as the share image; `publish_blogger.py` embeds only the small Pinterest thumbnail (`pin.png`) as a compressed JPEG `data:` URI at publish time (ImageMagick `convert`; the `post.html` in the repo is unchanged), so most of the post renders even if Pages is down. Everything else in the post (cards, strips, infographics, host art) is inline SVG. Pinterest (the Save button's `media=` and the Pinterest workflow) needs the public Pages URL too. If `convert` is missing or the post would exceed 700,000 characters, the Pages URL is kept and a message says so.

Images are served by GitHub Pages from this branch (`https://actsb.github.io/claudefold/<path>`; the repo root holds `.nojekyll`). Never hotlink `raw.githubusercontent.com`: browsers and Pinterest fail on it. So **push before you publish** — the post must not go live before its images are online:

```bash
git add -A && git commit -m "Daily pick: <product> (built)" && git push -u origin claude/sharp-lovelace-n7vhzq
python3 scripts/publish_blogger.py --check
python3 scripts/publish_blogger.py --posts-only --only <key>
python3 scripts/publish_blogger.py --hubs-only        # the Best Sellers hub carries the new line
```
Unattended auth uses BLOGGER_CLIENT_ID / BLOGGER_CLIENT_SECRET / BLOGGER_REFRESH_TOKEN from the environment. If they are absent, do everything else, commit, push, and end the run by telling the owner the post is built and needs a Blogger token (attended path in the publisher's docstring). Never ask for a token to be pasted into a repository file.

Backlog rule: when credentials work, first publish every earlier queue entry whose `status` is still `writing` and whose folder holds a checked `post.html` with no WRITE markers (`--posts-only --only <key>` for each, then mark it `published` with its URL), then publish today's. A run without credentials leaves entries at `writing`; they are not lost.

## 7. After publishing

* `daily/queue.json`: set the entry's `"status": "published"` and `"url"`.
* `scripts/publish_blogger.py`: add `"url": "<the live URL>",` under the post's `"dir"` line in `POSTS`. The publisher finds a live post by its URL first, so a later title change updates the post instead of creating a duplicate. When you change a live title, also keep the old title in the entry's `"aliases"` list and change the `## <title>` heading in `daily/search-descriptions.md` to match (the site index matches posts by title).
* `brand/pages/hub-best-sellers.html`: `daily_post.py new` puts a draft card first in the entry's cluster grid (the queue entry's `"cluster"`; a new cluster opens its own section with a WRITE intro). The card is one line; replace the WRITE text in its highlight (`<div class="vp-lc-hl" …>WRITE: …</div>`) with one line on who it is for and the verdict, no Amazon ratings, counts or prices, and the WRITE intro of a new section. Do it while writing the post (section 4), not after publishing: the publisher refuses to publish a page or post that still holds a WRITE marker, so `--hubs-only` would skip the hub. `python3 scripts/site_index.py --hub` re-renders every card (after a design change; it keeps each card's title and line).
* `pinterest/pins-2026-*.md` and `promo/<date>-<slug>.md`: the scaffolder writes drafts; complete them.
* The Pinterest pin is created from that pin entry by `.github/workflows/pinterest.yml` (GitHub Actions, `scripts/pinterest_pins.py`) once the queue entry is `published`, the entry has no WRITE markers **and the owner has chosen it**. Pinterest's Developer Guidelines require the user to choose each pin an app publishes, so the automatic runs only pin entries carrying `**Approved**` / `yes`, and the owner can also pin a link directly (workflow mode `pin`). Never add the Approved field yourself, not even for a pin you think is obviously fine; add it only when the owner names that pin in the conversation. Put the day's pin link in the Korean report so the owner can choose it. Never call Pinterest from the Routine (the environment's network policy blocks it). Limits: title ≤100, description ≤500, alt text ≤500 characters; `python3 scripts/pinterest_pins.py list` shows which entries are ready. Owner setup: `daily/pinterest-setup.md`.
* `posts/<dir>/post-meta.md`: title, slug, labels, search description (≤150 chars), status, timestamp.
* `daily/search-descriptions.md`: add the same search description at the top of the list (`## <post title>`, the URL, the text in a ```text block). Blogger has no API for this field (no v3 field; the GData write API was shut down 2024-09-30; see research/blogger-search-description-2026-10-05.md), so the owner enters it in the editor, or a Claude session running in the owner's own signed-in browser does it from this list. The publisher updates posts with PATCH, which leaves a description entered by hand untouched.
* Home-page teasers and feed summaries come from the first text in the post body, so `assemble_post.py` puts the cover and the lead first and the style block, guide links and byline after the jump break (`teaser_first`). Write the lead as a self-contained summary.
* To see what Blogger serves for a page (head tags, teaser text, feed entry) from outside this environment's network policy, run the manual workflow **Actions → Live page check** with the URL.
* Commit and push: `git add -A && git commit -m "Daily pick: <product>" && git push -u origin claude/sharp-lovelace-n7vhzq`.
* Final report to the owner: URL, what was verified, what could not be (UNVERIFIED items), the search description to paste, and any embed to double-check.

## 8. Refilling the queue (every two weeks)

Read `daily/strategy-2026-10.md` first (clusters, the seasonal calendar, commission rates). Research prompt: "For a US shopper in the next 4–8 weeks, rank 20 candidates inside these clusters only: kitchen, car, home cleaning, sleep and home comfort, pets, bathroom (Kitchen and Automotive pay 4.5% on Amazon's standard table, home, pet and tools 3%, health and personal care 1%, so favour the first two and skip personal care). Mix single products in the $40–$150 sweet spot with roundups and 'X vs Y' comparisons for queries a new site can win ('best X for [narrow need]', 'X vs Y', 'is X worth it'), and the seasonal guides due in that window. For each: the variant people buy, a price band with a non-Amazon source, owner opinion at a non-Amazon retailer or forum, the alternative it beats, the seasonal hook, English YouTube titles and IDs from result URLs, honest cons." Give each new entry a `"cluster"` (cleaning, comfort, kitchen, car, pets, bathroom, tech, home, gifts, deals) and, for a roundup, `"format": "roundup"`, `"model"` and `"picks"`. Exclude every product already published or parked (see `daily/queue.json` and `posts/`). Titles follow section 0: no Amazon ratings, counts, ranks or prices.

## 9. Why this shape

* One product, one verdict, one buy box: the conversion path is short and the disclosure sits above the only paid links.
* Owner-reported problems, real expert citations and a retailer comparison are what Google's reviews system rewards and what the FTC's endorsement rules require.
* The daily cadence is sustainable because the research is delegated, the art is generated, and the checklist is fixed.

## 10. The Routine that runs this

* Routine sessions start **without the repository attached** (Routines cannot carry a source repo), so the prompt's step 0 attaches it with the `add_repo` tool before any work; without that, a run can build a post but never push it.
* Routine "Verdict Picks — product of the day (daily post)", id `trig_0199fgHgdp4CqDTQ4s7NnF8Q`, cron `53 9 * * *` (09:53 UTC = 5:53 a.m. Eastern = 6:53 p.m. Korea), a fresh cloud session per run, push + email notification when a run finishes. Its prompt is the text in `daily/routine-prompt.md`.
* Pause or resume: the owner's Routines list on claude.ai, or `update_trigger` with `enabled` from a session that holds the claude-code-remote tools.
* Unattended publishing needs three environment secrets on the cloud environment (Edit environment → secrets): `BLOGGER_CLIENT_ID`, `BLOGGER_CLIENT_SECRET`, `BLOGGER_REFRESH_TOKEN` (how to obtain them: the docstring of `scripts/publish_blogger.py`; the owner's step-by-step guide in Korean is `daily/blogger-credentials.md`). Without them each run builds and commits the post and asks the owner for a one-hour access token.

## 11. Roundup format (queue entries with `"format": "roundup"`)

A roundup compares several products for one need ("Best bidet of 2026", "Thanksgiving hosting essentials", "Gifts for car lovers"). It is the deeper format Google's reviews guidance rewards (comparisons, quantitative tables, who should skip what), so roundups take priority over a single-product post when a seasonal deadline is near. The model is the entry's `"model"` folder (default `posts/2026-10-best-bidet-2026`; deal hubs use `posts/2026-09-prime-big-deal-days-2026`): read its `src/00-easy.html` and `cards.json` in full before writing.

1. **Research** (the three agents of section 3, scoped to the entry's `"picks"`): owners and experts per candidate, then price bands. Keep 5–10 picks the research can support; drop a candidate with no sourced owner or expert opinion.
2. **Scaffold** with `python3 scripts/daily_post.py new <key>` as usual, then replace the one-product structure with the model's: a lead that names the top pick and why; key takeaways; the Korean summary; the top pick as `<!--TOPPICK-->`; why owners recommend it and what unhappy owners say; a comparison table with sourced numbers (our own scores, never Amazon stars); one card per pick (`<!--CARD:id-->`, in ranking order; markers on consecutive lines share a grid, two to a row) with who should buy it and who should skip it; costs of ownership; experts; videos; Quick answers; "The bottom line" that returns to the top pick; `<!--BUYBOX-->`; the method note ("How this guide was made"). The top pick is both the first and the last product the reader meets.
3. **Link our own reviews.** Every pick we have already reviewed links to that review with a descriptive anchor; gift guides and deal hubs lean on them. Two or more of our guides in one place are a `<ul class="vp-linkcards">` list (section 4), which becomes guide cards. Deal hubs give bands and percent-off rules, never Amazon prices.
4. **Length:** 3,000–7,000 words of body text; `check_post.py` runs with `--min-words 1500` inside `daily_post.py build`, so the floor is the same as a daily post.
5. **Two runs are fine.** If the research or writing is not finished, commit and push with the entry at `"status": "writing"` (never publish a half-written guide); the next run finishes it before anything new (section 2).
