#!/usr/bin/env python3
"""Price Check: is today's price a good one? (daily/price-check-plan.md)

Like Danawa's model pages and Fallcent's buy-or-wait signal, within Amazon's Associates rules: no Amazon price, rating, rank
or price history is ever shown (Program Policies 2(b), 6(t), 6(y)). Each entry in brand/price-check.json is one exact model
with prices seen at other stores (source and date), our "good" and "great" lines and a verdict. The reader taps "See today's
price" and compares Amazon's checkout price with the lines.

  python3 scripts/price_check.py    # rebuild brand/pages/price-check.html (the "Price Check" page)

assemble_post.py calls post_block() to add the same cards to a post's "Price check" section (before the buy box) when
the post is rebuilt, so posts gain the section one at a time (improve days), never in one mass republish.
"""
import datetime, html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import link_cards as LC

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "brand" / "price-check.json"
PAGE = ROOT / "brand" / "pages" / "price-check.html"
PAGE_URL = "/p/price-check.html"
VERDICT = {"buy": ("Buy now", LC.PRODUCT), "ok": ("Fair price", LC.GUIDE), "wait": ("Wait for a sale", LC.WARN)}


def esc(s):
    return html.escape(s, quote=True)


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def day(iso):
    return datetime.date.fromisoformat(iso).strftime("%b %-d, %Y")


def guide_url(key):
    import site_index
    P = site_index.publisher_posts().get(key, {})
    return (P.get("url") or "").replace(LC.SITE, "")


def card(e, link_guide=True):
    d, cid = e["card"]
    cards = {c["id"]: c for c in json.loads((ROOT / d / "cards.json").read_text(encoding="utf-8"))["cards"]}
    c = cards[cid]
    svg = (ROOT / d / "images" / "cards" / f"{cid}.svg").read_text(encoding="utf-8")
    pill, palette = VERDICT[e["verdict"]]
    href = html.unescape(html.unescape(c["cta"]))
    return LC.card(esc(e["name"]), href, img=LC.art_thumb(svg), pill=pill, palette=palette,
                   highlight=f'Good price: {esc(e["good"])} · Great: {esc(e["great"])}',
                   detail=f'<strong>Model:</strong> {esc(e["model"])} {esc(e["why"])}',
                   meta=f'Seen at other stores: {esc(e["street"])} · checked {day(e["checked"])}',
                   cta="See today's price", paid="amazon." in href,
                   name_href=(guide_url(e["guide"]) or None) if link_guide else None,
                   attrs=f' id="pc-{esc(e["key"])}"')


HOW = ('<p style="margin:0 0 .5em;"><strong>How to use it:</strong> tap <em>See today\'s price</em>, then compare the price at '
       'checkout with our lines. At or under <strong>Good</strong> is a good buy; at or under <strong>Great</strong> is as low as we have '
       'seen it go at major US stores. The button opens the product on Amazon with today\'s price; the numbers here are prices seen at other '
       'stores and list prices, each with its source and date. We never quote prices from Amazon.</p>')


def post_block(post_key, data=None):
    """The "Price check" section for one post, or "" when no entry points at it."""
    data = data or load()
    items = [e for e in data["items"] if e["guide"] == post_key]
    if not items:
        return ""
    return ('<div class="vp-pricecheck" id="price-check" style="margin:1.6em 0;">'
            '<h2 style="color:#1B2A41;font-size:1.6em;line-height:1.25;margin:0 0 .4em;">Price check: is today\'s price a good one?</h2>'
            + HOW + LC.grid([card(e, link_guide=False) for e in items], margin=".6em 0 .6em")
            + f'<p style="font-size:15px;margin:.4em 0 0;"><a href="{PAGE_URL}" style="color:#1B2A41;font-weight:700;">Every price check, by category →</a></p></div>\n')


def page(data):
    items = data["items"]
    cats = data["categories"]
    latest = max(e["checked"] for e in items)
    rows = "".join(
        f'<tr><td style="padding:8px 10px;border-top:1px solid #e3e3e3;"><a href="#pc-{esc(e["key"])}" style="color:#1B2A41;font-weight:700;">{esc(e["name"])}</a></td>'
        f'<td style="padding:8px 10px;border-top:1px solid #e3e3e3;white-space:nowrap;color:{VERDICT[e["verdict"]][1]["hl"]};font-weight:700;">{VERDICT[e["verdict"]][0]}</td>'
        f'<td style="padding:8px 10px;border-top:1px solid #e3e3e3;">{esc(e["good"])}</td>'
        f'<td style="padding:8px 10px;border-top:1px solid #e3e3e3;">{esc(e["great"])}</td>'
        f'<td style="padding:8px 10px;border-top:1px solid #e3e3e3;white-space:nowrap;">{day(e["checked"])}</td></tr>'
        for k in cats for e in items if e["category"] == k)
    sections = ""
    for k, title in cats.items():
        group = [e for e in items if e["category"] == k]
        if group:
            sections += (f'<h2 id="cat-{k}" style="color:#1B2A41;font-size:1.35em;margin:1.4em 0 .3em;">{esc(title)}</h2>'
                         + LC.grid([card(e) for e in group], margin=".4em 0 1em") + "\n")
    jump = " · ".join(f'<a href="#cat-{k}" style="color:#1B2A41;">{esc(v)}</a>' for k, v in cats.items() if any(e["category"] == k for e in items))
    log = "".join(f"<li>{esc(x)}</li>" for x in data.get("changelog", [])[:12])
    return f'''<!-- Price Check page: generated by scripts/price_check.py from brand/price-check.json. Edit the JSON, not this file. -->
<style>
{LC.CSS}</style>
<div style="max-width:760px;margin:0 auto;font-size:18px;line-height:1.65;color:#222;">
<p class="vp-nav" style="font-size:15px;margin:0 0 .8em;color:#555;"><strong style="color:#1B2A41;">Guides:</strong> <a href="/p/robot-vacuums.html" style="color:#1B2A41;">Robot Vacuums</a> · <a href="/p/wireless-earbuds.html" style="color:#1B2A41;">Wireless Earbuds</a> · <a href="/p/smart-glasses.html" style="color:#1B2A41;">Smart Glasses</a> · <a href="/p/power-stations.html" style="color:#1B2A41;">Power Stations</a> · <a href="/p/best-sellers.html" style="color:#1B2A41;">Best Sellers</a> · <a href="{PAGE_URL}" style="color:#1E8E5A;font-weight:700;">Price Check</a></p>
<p style="font-size:21px;color:#1B2A41;"><strong>Is today's price a good one?</strong> For every product we recommend: the exact model to buy, the price that makes it a good buy, the price that is as low as it goes, and whether to buy now or wait for the next sale.</p>
<p style="font-size:15px;color:#555;"><em>As an Amazon Associate I earn from qualifying purchases. The <strong>See today's price</strong> buttons are paid links. Last checked: {day(latest)}.</em></p>
{HOW}
<p style="font-size:16px;"><strong>Jump to:</strong> {jump}</p>
<h2 style="color:#1B2A41;font-size:1.35em;margin:1.2em 0 .3em;">All price lines at a glance</h2>
<div style="overflow-x:auto;margin:.4em 0 1.2em;"><table style="border-collapse:collapse;width:100%;min-width:560px;font-size:15px;">
<thead><tr style="background:#1B2A41;color:#fff;"><th style="text-align:left;padding:8px 10px;">Product</th><th style="text-align:left;padding:8px 10px;">Verdict</th><th style="text-align:left;padding:8px 10px;">Good price</th><th style="text-align:left;padding:8px 10px;">Great price</th><th style="text-align:left;padding:8px 10px;">Checked</th></tr></thead>
<tbody>{rows}</tbody></table></div>
{sections}
<h2 style="color:#1B2A41;font-size:1.35em;margin:1.4em 0 .3em;">How we set the lines</h2>
<ul>
<li><strong>Exact model first.</strong> Look-alike names and older models are the commonest way to overpay, so every entry names the model to buy and the ones it is confused with.</li>
<li><strong>Good</strong> is a price we would pay ourselves today; <strong>Great</strong> is as low as we have seen it at a major US store or the maker's own store, with the date.</li>
<li><strong>Sources:</strong> list prices from the maker, and prices seen at Walmart, Target, Best Buy, Home Depot, Costco, Chewy, PetSmart and brand stores, each named with its date in the card. We never quote prices, ratings or price history from Amazon; the button opens the product page, which shows today's price and has its own price-history link.</li>
<li><strong>Verdicts:</strong> <em>Buy now</em> when the usual price is already near the low or you need it before a date (a holiday, winter); <em>Fair price</em> when sales move it only a little; <em>Wait for a sale</em> when a dated record shows a bigger cut is likely soon. We change a verdict only after re-checking, and the date on each card says when.</li>
<li>We earn a commission on Amazon purchases through the buttons; it never changes the lines. <a href="/p/how-we-rank-products.html">How we rank</a> · <a href="/p/affiliate-disclosure.html">Disclosure</a></li>
</ul>
<h3 style="color:#1B2A41;">What changed</h3>
<ul style="font-size:15px;color:#444;">{log}</ul>
</div>
'''


def policy_check(raw):
    """The Amazon data rules check_post.py applies to posts: an Amazon price, rating or rank in the page stops the build."""
    import check_post
    body = re.sub(r"<!--.*?-->", " ", re.sub(r"<svg.*?</svg>", " ", raw, flags=re.S), flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    hits = [f"{label}: …{text[max(0, m.start() - 50):m.end() + 20].strip()}…" for label, pat in check_post.AMAZON_FAIL for m in re.finditer(pat, text, re.I)]
    if hits or re.search(r"\bWRITE\b", text):
        sys.exit("price check not written; fix brand/price-check.json:\n" + "\n".join(hits or ["a WRITE marker"]))


def main():
    data = load()
    out = page(data)
    policy_check(out)
    PAGE.write_text(out, encoding="utf-8")
    print(f"{PAGE.relative_to(ROOT)}: {len(data['items'])} price checks in {len({e['category'] for e in data['items']})} categories")


if __name__ == "__main__":
    main()
