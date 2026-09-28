# Daily product of the day — runbook

One post a day: one Amazon best-seller with the best value in its category, researched to the end, written for a US shopper who wants to buy today. This file is the complete procedure; a fresh session with no memory of earlier work can follow it top to bottom.

## 0. Ground rules (never skip)

* **Truth first.** Every number is attributed and dated ("reported by X in month 2026", "at the time of writing"). No live Amazon price is ever stated as fact; the buttons show today's price. No invented reviews, quotes, ratings or people.
* **Experts are real, cited and linked.** The "What the experts say" section paraphrases or briefly quotes published sources a search snippet supports (Consumer Reports, Wirecutter, America's Test Kitchen, a university extension office, a professional association, a named engineer/dermatologist/vet writing under their own name). Never fabricate a name, a title or a quote. Vera is an illustration and is labelled as one.
* **Disclosure before the first paid link**: the byline sentence, "(paid link)" on every Amazon button (the assembler adds it), the Korean summary opens with "[제휴 링크 포함]".
* **Videos**: only English-language YouTube embeds whose titles were confirmed in search results; official iframe with `?rel=0`; a "Watch on YouTube" link; no downloaded thumbnails. Our own clips: no people, no Korean text.
* **Images**: our own renders/infographics/photos only. No Amazon product images, no hotlinking, no vendor logos.
* **Tone**: plain, specific, a little dry humour, no hype words ("game-changer", "must-have"). Short sentences. Cons get the same space as pros.

## 1. Setup (fresh session)

```bash
bash scripts/bootstrap.sh            # ffmpeg-static + sharp into the scratchpad; prints FFMPEG and NODE_PATH
export FFMPEG=<printed path>
```

## 2. Pick today's product

`daily/queue.json` holds the queue. Take the first entry with `"status": "queued"` (or the one whose `"date"` is today). If the queue is empty, run the candidate-shortlist research (prompt in section 8) and append 14 new entries first.

## 3. Research (three agents, in parallel, ~50 searches each)

1. **Owners**: what owners say after weeks/months (praise, complaints, failure modes, sizes/variants that matter, Q&A questions people actually ask, counterfeit or fulfilment issues). Sources: search snippets of Amazon reviews and Q&A, Reddit threads, forum posts, retailer reviews.
2. **Video and experts**: English YouTube reviews/how-tos with exact titles and IDs from result URLs (never guess an ID); published expert sources (CR, Wirecutter, ATK, RTINGS, universities, professional bodies) with what each actually says; the product's official manual/instructions for the how-to section.
3. **Price and channels**: reported prices at Amazon, Walmart, Target, Costco, Home Depot, the brand's own store and Temu/AliExpress look-alikes; Subscribe & Save, bundles, warranty/registration, return windows; sale history (Prime Day, Big Deal Days, Black Friday); the honest "when Amazon is not the cheapest".

Save the three briefs to `research/daily-<date>-<slug>.md`.

## 4. Scaffold and write

```bash
python3 scripts/daily_post.py new <key>          # creates posts/<date>-<slug>/ from the queue entry
```

Then edit `posts/<dir>/cards.json` (product card, optional accessory cards, `buy` dicts, `video` fields), `cover.json` (bright style; title lines, subtitle, pin bullets, url) and `strips.json` (one four-panel "in real life" strip). Write `src/00-easy.html` following `daily/template-00-easy.html` section by section; the template's `<!-- WRITE: ... -->` comments say what each part must contain. Target 1,800–2,600 words of body text. Question-form H2s. Ten Quick answers (they become the FAQ schema).

Product art: `cards.json` `"category"` must be a renderer in `scripts/product_cards.py` (`generic` with an `"art": {"shape": "box|bottle|cylinder|flat|sphere|bag", ...}` works for anything). Dedicated renderers exist for `purifier` (a Core 300-style tower), `robot`, `earbuds`, `glasses`, `power`, `tracker`, `bottle`, `cleaner`, `groomvac`, `roller`, `litterbot`, `harness`, `kong`, `bags`, `chat`, `film`, `voice`, `lightbox`, `tripod` and `ssd`; add one to `DRAW` when a product deserves its own silhouette. A second card for the consumable (filter, refill, bag) with its own `buy` dict puts the repeat purchase in the buy box.

## 5. Build, check, preview

```bash
python3 scripts/daily_post.py build posts/<dir>   # cards, strips, cover, pin, infographic, assemble, SEO layer, build, check, PNGs
node scripts/preview_post.mjs posts/<dir>/post.html <scratch>/prev/day 760 4000
node scripts/preview_post.mjs posts/<dir>/post.html <scratch>/prev/dayphone 390 3000
```
Look at the first and last slices at both widths. Fix overlaps before publishing.

## 6. Publish

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
* `brand/pages/hub-best-sellers.html`: add the one-line entry (done by `daily_post.py new` as a draft line; check it).
* `pinterest/pins-2026-*.md` and `promo/<date>-<slug>.md`: the scaffolder writes drafts; complete them.
* The Pinterest pin is created from that pin entry by `.github/workflows/pinterest.yml` (GitHub Actions, `scripts/pinterest_pins.py`) once the queue entry is `published` and the entry has no WRITE markers; the final push triggers it. Never call Pinterest from the Routine (the environment's network policy blocks it). Limits: title ≤100, description ≤500, alt text ≤500 characters; `python3 scripts/pinterest_pins.py list` shows which entries are ready. Owner setup: `daily/pinterest-setup.md`.
* `posts/<dir>/post-meta.md`: title, slug, labels, search description (≤150 chars), status, timestamp.
* Commit and push: `git add -A && git commit -m "Daily pick: <product>" && git push -u origin claude/sharp-lovelace-n7vhzq`.
* Final report to the owner: URL, what was verified, what could not be (UNVERIFIED items), the search description to paste, and any embed to double-check.

## 8. Refilling the queue (every two weeks)

Research prompt: "Rank 20 single Amazon best-sellers with the best value for a US shopper next month, spread across kitchen, cleaning, home comfort, personal care, tools, car, sleep, fitness, tech accessories, storage, pet, outdoor, kids, office; $20–$150 sweet spot; for each: variant people buy, reported price range, review count/rating, the alternative it beats, seasonal hook, English YouTube titles and IDs from result URLs, honest cons, Amazon-specific advantage." Exclude every product already published (see `daily/queue.json` and `posts/`).

## 9. Why this shape

* One product, one verdict, one buy box: the conversion path is short and the disclosure sits above the only paid links.
* Owner-reported problems, real expert citations and a retailer comparison are what Google's reviews system rewards and what the FTC's endorsement rules require.
* The daily cadence is sustainable because the research is delegated, the art is generated, and the checklist is fixed.

## 10. The Routine that runs this

* Routine "Verdict Picks — product of the day (daily post)", id `trig_0199fgHgdp4CqDTQ4s7NnF8Q`, cron `53 9 * * *` (09:53 UTC = 5:53 a.m. Eastern = 6:53 p.m. Korea), a fresh cloud session per run, push + email notification when a run finishes. Its prompt is the text in `daily/routine-prompt.md`.
* Pause or resume: the owner's Routines list on claude.ai, or `update_trigger` with `enabled` from a session that holds the claude-code-remote tools.
* Unattended publishing needs three environment secrets on the cloud environment (Edit environment → secrets): `BLOGGER_CLIENT_ID`, `BLOGGER_CLIENT_SECRET`, `BLOGGER_REFRESH_TOKEN` (how to obtain them: the docstring of `scripts/publish_blogger.py`; the owner's step-by-step guide in Korean is `daily/blogger-credentials.md`). Without them each run builds and commits the post and asks the owner for a one-hour access token.
