# Editorial Workflow — from "which product next?" to published

## 1. Picking the next product (30 minutes, monthly)

Score candidates 1–5 on each and pick the highest total:

| Signal | Where to look | What scores high |
|---|---|---|
| Search demand | Google Trends (US, 12 months) for "best <product>"; Amazon search bar autocomplete | Rising or seasonally peaking soon |
| Basket size | Amazon Best Sellers price band | $150+ average (affiliate commission is a % of the sale) |
| Brand confusion | Count of distinct brands in Amazon's top 20 best sellers | 5+ brands = readers need a guide |
| Review conflict | Ratio of 1-star to 5-star reviews on the top 3 products | Contradictions = a real "what to know" story |
| Freshness | Product launch calendar (CES in January, IFA in September, Prime Day cycles) | New generation in the last 6 months |

Amazon pages that surface the candidates: **Best Sellers**, **Movers & Shakers** (24-hour rank gainers), **New Releases**, **Most Wished For** — all under the "Robotic Vacuums"-style category pages.

## 2. Research checklist (4–6 hours per category guide)

- [ ] Amazon Best Sellers top 20 in the category: brand, model, generation, rating, review count.
- [ ] Independent lab tests: RTINGS, Vacuum Wars / category-equivalent, Tom's Guide, TechGearLab, Consumer Reports, Reviewed, Wirecutter. Note *measured* numbers, not claims.
- [ ] Owner reviews on Amazon: sort by **Most recent** and read the 1-, 2- and 3-star reviews for the top 6 products; log recurring themes (tally, don't invent percentages).
- [ ] Reddit: r/<category> "regret", "should I buy", "6 months later" threads for the same products.
- [ ] Manufacturer pages: current lineup, MSRP, warranty, consumables prices.
- [ ] Deal history: Slickdeals / 9to5Toys / camelcamelcamel for the typical sale price of each pick.
- [ ] YouTube: one long review and one Short per pick from established channels; confirm each ID plays before publishing.
- [ ] Industry news that changes the advice (bankruptcies, recalls, firmware pulls, tariffs).

## 3. Writing rules

* Lead with the verdict box; readers who scroll no further must still get the right answer.
* Every spec claim gets a reality check ("claimed 36,000 Pa; measured 0.41 kPa at the intake").
* Every pick gets: spec box, 3–5 pros, 3–5 cons, the single most common owner complaint, "who should skip it", link.
* Show your sources in a numbered list at the end; link the labs and reviewers you leaned on.
* Prices: manufacturer list price + "typically on sale for" language. No live Amazon prices in text.
* Images: inline SVG charts we make ourselves (no hosting, no copyright risk) + product images only via Amazon SiteStripe.
* Video: long review embeds at 16:9; Shorts at 9:16, max 360px wide, in a "60-second look" callout.
* Length: category guide 5,000–9,000 words. Head-to-head 2,000–3,500. Deep dive 1,200–2,000.

## 4. Quality bar before Publish

- [ ] Verdict box, disclosure line, and table of contents are in the first screen.
- [ ] No spec appears without a source or a measured counterpart.
- [ ] Every recommended product has a "who should skip it".
- [ ] All `YOURTAG-20` placeholders replaced.
- [ ] `scripts/check_post.py` passes (word count, no unreplaced placeholders, balanced tags, all embeds listed).
- [ ] Preview on mobile: tables scroll horizontally, videos fit, SVGs visible.
- [ ] Labels: 1 category + 1 post type + ≤4 intent labels. Search description ≤155 chars. Custom permalink set.

## 5. Update cadence

* Category guides: refresh every 6 months or when a new generation launches (add "Updated <Month Year>" under the title, keep the URL).
* Deals posts: expire — add a dated note at the top after the event and remove them from the Featured Post slot.
