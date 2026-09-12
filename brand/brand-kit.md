# Verdict Picks — Brand Kit

> Every brand. Thousands of reviews. One clear verdict.

## 1. Name, tagline, positioning

| Element | Value |
|---|---|
| **Blog name** | **Verdict Picks** |
| **Tagline** (Blogger "Description") | Deep-dive buying guides for the products Americans search for most on Amazon — every brand compared, thousands of owner reviews distilled, one clear verdict. |
| **One-line pitch** | We do the 20 hours of research so you can buy the right thing in 20 minutes. |
| **Audience** | US Amazon shoppers (25–55) about to spend $50–$2,000 on a considered purchase, who are drowning in specs, sponsored listings, and 5-star reviews that contradict the 1-star reviews. |
| **Category focus** | High-consideration, high-search-volume Amazon categories: home appliances, tech, personal care, pet & baby gear, outdoor/auto. |
| **Promise** | Independent, data-first, brand-agnostic. We say which product to buy for *your* situation — and which ones to skip. |
| **Revenue model** | Amazon Associates affiliate links (disclosed on every post), later display ads. Never sponsored rankings. |

### Why "Verdict Picks"
* **Verdict** signals that every article ends with a decision, not a list of 20 links.
* **Picks** is the language shoppers already use ("editor's picks", "top picks") and pairs naturally with category names: *Verdict Picks: Robot Vacuums*.
* Short, spellable, works as a favicon monogram (**VP**) and a social handle.

### Naming alternatives (if the blogspot address or handle is taken)
1. **Clear Verdict Reviews** — same idea, slightly more editorial.
2. **The Buy Ledger** — "we keep the receipts" tone; good for data-heavy posts.
3. **Cart Certain** — friendlier, consumer-facing.
4. **PickProof** — punchy, but harder to say what it means at a glance.

Recommended blogspot address to try, in order: `verdictpicks.blogspot.com`, `verdict-picks.blogspot.com`, `theverdictpicks.blogspot.com`. A custom domain (`verdictpicks.com` or `.co`) can be attached later under **Settings → Publishing → Custom domain** without breaking existing links (Blogger redirects the blogspot address automatically).

## 2. Editorial voice

* **Plain-spoken, second person.** "If you have a long-haired dog, skip this one." Not "Consumers with pets may wish to consider…".
* **Skeptical of marketing numbers.** Always pair a claimed spec with what independent testers measured or what owners actually experience (e.g., "36,000 Pa" vs. measured intake suction).
* **Decisive.** Every section that compares two things ends by saying which one wins and for whom.
* **Honest about downsides.** Each recommended product carries a "Who should skip it" line and the most common owner complaint.
* **No fake authority.** We cite the labs and reviewers we lean on (Vacuum Wars, RTINGS, Tom's Guide, TechGearLab, Consumer Reports, Reviewed, Wirecutter) and never claim tests we did not run.
* **US-specific.** Prices in USD, dimensions in inches (with metric in parentheses when it matters), US retailers, US warranty terms, US sale calendar (Prime Day, Prime Big Deal Days, Black Friday/Cyber Monday).

### Words we use / avoid
| Use | Avoid |
|---|---|
| "measured", "owners report", "in lab tests" | "best ever", "game-changing", "revolutionary" |
| "list price", "typically sells for", "we've seen it under $X on sale" | exact live Amazon prices (they change hourly and Amazon's affiliate rules restrict displaying them unless pulled via their API) |
| "skip it if…" | "may not be suitable for all users" |

## 3. Article formula (every post)

1. **Verdict box at the top** — 3–6 picks by use case, one sentence each, with the link.
2. **How we evaluated** — sources, what we weighted, what we ignored.
3. **The market right now** — who makes what, what changed this year.
4. **What actually matters** — the 6–10 buying factors, each with "what the spec sheet says vs. what matters".
5. **Brand-by-brand** — positioning, lineup, strengths, weaknesses, recurring owner complaints, who should buy.
6. **The picks, one by one** — spec box, pros, cons, owner-review consensus, "who should skip it", video.
7. **What owners complain about** — the review deep-dive by theme.
8. **Decision guide by household** — a flowchart and a table.
9. **Cost of ownership** and **when to buy**.
10. **FAQ** (8–12 questions people actually type into Google).
11. **Final verdict**, sources, and the affiliate disclosure.

Target length: 5,000–9,000 words for a category guide; 2,000–3,500 for a head-to-head; 1,200–2,000 for a single-product deep dive.

## 4. Visual identity

| Token | Value |
|---|---|
| Primary (ink) | `#1B2A41` — navy, used for headings and the verdict box border |
| Accent (verdict green) | `#1E8E5A` — "buy" signals, winner badges |
| Warning (skip amber) | `#C9781B` — "who should skip it", caveats |
| Neutral paper | `#F7F5F0` — table headers, callout backgrounds |
| Body text | `#222222` on white |
| Type | System sans-serif (Blogger themes ship their own); headings bold, 1.25 scale; body 17–18px |
| Graphics style | Flat, two-color charts with the accent for the winner; every chart has a source line beneath it |
| Badges | `BEST OVERALL`, `BEST VALUE`, `BUDGET PICK`, `PET PICK`, `MOP PICK`, `SKIP` — rounded pill, uppercase, 12px |

Favicon: navy square, white "VP" monogram (Blogger → Settings → Basic → Favicon; 100 KB max, square).

## 5. Recommended Blogger theme

**Emporio** (grid of cards, image-forward, mobile-first) or **Contempo** (classic magazine). Both are responsive and support the Featured Post + Labels + Pages gadgets the category navigation relies on. Avoid the legacy "Simple/Awesome Inc." themes — they are not mobile-optimized and hurt Core Web Vitals.

## 6. Legal must-haves (all provided in `brand/pages/`)

* Affiliate disclosure at the top of every post **and** a standalone page — Amazon's required wording is *"As an Amazon Associate I earn from qualifying purchases."*
* Privacy & Cookies page that names Google (Blogger/Analytics/AdSense), Amazon Associates, and YouTube embeds as third parties that may set cookies. Blogger auto-shows an EU cookie notice, but that notice only covers Google's own cookies — the page fills the gap.
* "How We Rank" page — the FTC expects endorsements to reflect honest opinions; documenting the method also builds trust and helps Google's reviews-system guidelines (first-hand evidence, quantitative measurements, comparisons).
