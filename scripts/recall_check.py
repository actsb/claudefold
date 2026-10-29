#!/usr/bin/env python3
"""Recall Check: US product recalls in our categories, from the CPSC's own data (daily/strategy-2026-10-29.md, section 4).

Pulls this year's and last year's recalls from the CPSC SaferProducts API (public, no key), keeps the ones in our clusters
(heating and sleep, kitchen, cleaning, power and batteries, car, pets, bathroom; never toys or children's products), and
writes brand/pages/recall-check.html: a search box and one card per recall with the hazard, the models, the units, the
remedy and a link to the CPSC notice. Where a recall names a product we cover, the card says so and links our guide.
CPSC "sold at" lines often quote the price a store charged; every price is cut, so no Amazon price ever reaches the page.

  python3 scripts/recall_check.py            # fetch and rebuild the page (weekly, on the Saturday improve day)
  python3 scripts/publish_blogger.py --page "Recall Check"
"""
import datetime, html, json, pathlib, re, sys, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import link_cards as LC   # SITE only

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "brand" / "pages" / "recall-check.html"
API = "https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallDateStart={start}"
PAGE_URL = "/p/recall-check.html"

# first match wins; the order puts specific words before general ones
CLUSTERS = [
    ("heat", "Heating and sleep", r"heated (blanket|throw|mattress)|electric blanket|heating pad|hand warmer|space heater|\bheaters?\b|mattress|pillow|humidifier|air purifier|air cleaner|\bfans?\b|weighted blanket|bed rail|sauna"),
    ("power", "Power banks and batteries", r"power bank|power station|portable charger|\bchargers?\b|batter(y|ies)|generator|extension cord|power strip|surge protector|e-?bike"),
    ("car", "Car", r"jump starter|tire inflator|dash ?cam|\bcar\b|vehicle|automotive"),
    ("kitchen", "Kitchen", r"kettle|pressure cooker|slow cooker|rice cooker|air fryer|fryer|blender|mixer|toaster|\boven|grill|coffee|espresso|kitchen|knife|knives|cookware|\bpans?\b|food processor|range|dishwasher|refrigerator|freezer|mug|tumbler|water bottle|food container|thermometer"),
    ("cleaning", "Cleaning", r"vacuum|\bmops?\b|steam cleaner|pressure washer|carpet cleaner|cleaning|broom|wipes|detergent|laundry|washing machine|clothes dryer"),
    ("pets", "Pets", r"\bpets?\b|\bdogs?\b|\bcats?\b|litter|leash|collar|aquarium|chew toy"),
    ("bath", "Bathroom", r"bidet|toilet|shower|bathroom|hair dryer|curling|flat iron"),
]
SKIP = re.compile(r"\btoys?\b|child|children|baby|babies|infant|crib|bassinet|stroller|high chair|teeth|pacifier|youth|\bkids?\b|"
                  r"toddler|play ?yard|playpen|bicycle|helmet|dresser|chest of drawers|nightwear|pajama|sleepwear|costume|swing set", re.I)
PRICE = re.compile(r"\s*(for|at|priced at|retailing for|selling for)?\s*(about|approximately|between|from)?\s*\$[\d,.]+(\s*(to|and|-|–)\s*\$[\d,.]+)?", re.I)


def esc(s):
    return html.escape(str(s or ""), quote=True)


def fetch(start):
    with urllib.request.urlopen(urllib.request.Request(API.format(start=start), headers={"User-Agent": "VerdictPicks recall check"}), timeout=120) as r:
        return json.loads(r.read())


def cluster(r):
    text = " ".join([r.get("Title") or ""] + [p.get("Name") or "" for p in r.get("Products", [])])
    if SKIP.search(text):
        return None
    for key, _, pat in CLUSTERS:
        if re.search(pat, text, re.I):
            return key
    return None


def first_sentence(s, n=220):
    s = re.sub(r"\s+", " ", s or "").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    s = m.group(1) if m else s
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def no_amounts(s):
    """ "a full refund of the $65 purchase price … or an $80 store credit" -> "a full refund of the purchase price … or a store credit" """
    s = re.sub(r"\ban \$[\d,.]+\s*(?=[^aeiouAEIOU])", "a ", s)
    return re.sub(r"\$[\d,.]+\s*", "", s)


def sold_at(r):
    """Where it was sold, with every price cut ("Amazon.com from March 2025 through August 2026")."""
    out = []
    for x in r.get("Retailers", []):
        s = re.sub(r"^Sold (At|exclusively at|online at)?:?\s*", "", (x.get("Name") or "").strip(), flags=re.I)
        if not s or re.search(r"\b(co|ltd|inc|llc|dba)\b\.?|, of [A-Z]", s, re.I) and not re.search(r"^[\w.&' -]*\.com|stores?\b|online", s, re.I):
            continue
        s = PRICE.sub("", s).strip(" .,;")
        out.append(re.sub(r"\s+", " ", s))
    return "; ".join(out)


def our_guides():
    """(brand, our guide's URL, its title) for every brand on a product card of a live guide (site-index.json)."""
    idx = ROOT / "brand" / "site-index.json"
    out, seen = [], set()
    for p in json.loads(idx.read_text(encoding="utf-8")) if idx.exists() else []:
        cards = ROOT / p.get("dir", "") / "cards.json"
        if not p.get("url") or not cards.exists():
            continue
        for c in json.loads(cards.read_text(encoding="utf-8")).get("cards", []):
            brand = re.sub(r"[^A-Za-z0-9-]", "", c["name"].split()[0]).lower()
            if len(brand) > 3 and brand not in GENERIC and (brand, p["key"]) not in seen:
                seen.add((brand, p["key"]))
                out.append((brand, p["url"].replace(LC.SITE, ""), p["title"]))
    return out


GENERIC = {"best", "original", "classic", "heated", "portable", "cordless", "electric", "smart", "mini", "pack", "extra", "large", "small", "wireless", "digital", "instant-read", "budget", "premium", "amazon", "earth", "foldable", "yeti", "black", "white", "home", "kitchen"}


def card(r, label, covered):
    """One recall as a compact card (classes styled once in the page's <style>, so 200+ cards stay light)."""
    products = r.get("Products", [])
    models = "; ".join(p["Model"].strip() for p in products if (p.get("Model") or "").strip())
    units = "; ".join(p["NumberOfUnits"].strip() for p in products if (p.get("NumberOfUnits") or "").strip())
    hazard = first_sentence(no_amounts(" ".join(h.get("Name", "") for h in r.get("Hazards", []))), 170)
    remedy = first_sentence(no_amounts(" ".join(x.get("Name", "") for x in r.get("Remedies", []))), 200)
    date = datetime.date.fromisoformat(r["RecallDate"][:10])
    where = sold_at(r)
    name = products[0]["Name"] if products and products[0].get("Name") else r["Title"]
    search = esc(no_amounts(" ".join([r.get("Title", ""), name, models, where])).lower())
    rows = ((f"<p><b>Models:</b> {esc(first_sentence(models, 160))}</p>" if models else "")
            + (f"<p><b>Units:</b> {esc(units)}</p>" if units else "")
            + (f"<p><b>What to do:</b> {esc(remedy)}</p>" if remedy else ""))
    meta = f"Recalled {date.strftime('%b %-d, %Y')}" + (f" · Sold at {esc(where)}" if where else "")
    guide = (f'<p class="g">We cover {esc(covered[0].title())} in <a href="{esc(covered[1])}">{esc(covered[2])}</a></p>' if covered else "")
    return (f'<div class="rc" data-q="{search}"><span class="pl">{esc(label)}</span><b class="n">{esc(name)}</b>'
            + (f'<p class="h">{esc(hazard)}</p>' if hazard and hazard != "None reported." else "")
            + rows + f'<p class="m">{meta}</p>' + guide
            + f'<a class="go" href="{esc(r["URL"])}" rel="nofollow noopener" target="_blank">Read the CPSC notice →</a></div>')


CSS = """.rc-g{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:12px;margin:.4em 0 1em}
.rc{display:flex;flex-direction:column;gap:5px;background:#fff;border:1px solid #DDE3EA;border-left:5px solid #E07B1A;border-radius:14px;padding:12px 14px;box-shadow:0 1px 3px rgba(16,24,40,.05);font-size:14px;line-height:1.5;color:#444}
.rc p{margin:0}.rc .pl{align-self:flex-start;font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;background:#FBEFE2;color:#8A4B0C}
.rc .n{font-size:16px;line-height:1.35;color:#1B2A41}.rc .h{font-weight:700;color:#8A4B0C}.rc .m{font-size:13px;color:#8A8F98}
.rc .g{font-size:13px}.rc .g a{color:#1B2A41;font-weight:700}
.rc .go{margin-top:auto;padding-top:4px;color:#1B2A41;font-weight:700;font-size:15px;text-decoration:none}
.vp-rc-hide{display:none !important}
"""


def page(recalls, today):
    covered = our_guides()
    groups = {k: [] for k, _, _ in CLUSTERS}
    for r in recalls:
        k = cluster(r)
        if k:
            groups[k].append(r)
    total = sum(len(v) for v in groups.values())
    labels = {k: lab for k, lab, _ in CLUSTERS}
    sections, jump = "", []
    for k, rs in groups.items():
        if not rs:
            continue
        rs.sort(key=lambda r: r["RecallDate"], reverse=True)
        jump.append(f'<a href="#rc-{k}" style="color:#1B2A41;">{esc(labels[k])} ({len(rs)})</a>')
        cards = []
        for r in rs:
            text = (r.get("Title", "") + " " + " ".join(p.get("Name", "") for p in r.get("Products", []))).lower()
            hit = next((c for c in covered if re.search(rf"\b{re.escape(c[0])}\b", text)), None)
            cards.append(card(r, labels[k], hit))
        sections += (f'<h2 id="rc-{k}" class="vp-rc-h" style="color:#1B2A41;font-size:1.35em;margin:1.4em 0 .3em;">{esc(labels[k])}</h2>'
                     + '<div class="rc-g">' + "".join(cards) + "</div>\n")
    first = min(r["RecallDate"][:10] for r in recalls)
    present = [labels[k].lower() for k, rs in groups.items() if rs]
    kinds = ", ".join(present[:-1]) + " and " + present[-1] if len(present) > 1 else "".join(present)
    return f'''<!-- Recall Check page: generated by scripts/recall_check.py from the CPSC SaferProducts API. Do not edit by hand. -->
<style>
{CSS}</style>
<div style="max-width:760px;margin:0 auto;font-size:18px;line-height:1.65;color:#222;">
<p class="vp-nav" style="font-size:15px;margin:0 0 .8em;color:#555;"><strong style="color:#1B2A41;">Guides:</strong> <a href="/p/robot-vacuums.html" style="color:#1B2A41;">Robot Vacuums</a> · <a href="/p/power-stations.html" style="color:#1B2A41;">Power Stations</a> · <a href="/p/best-sellers.html" style="color:#1B2A41;">Best Sellers</a> · <a href="/p/price-check.html" style="color:#1B2A41;">Price Check</a> · <a href="{PAGE_URL}" style="color:#C2410C;font-weight:700;">Recall Check</a></p>
<p style="font-size:21px;color:#1B2A41;"><strong>Is the one you own recalled?</strong> Every US recall since {datetime.date.fromisoformat(first).strftime("%B %Y")} for the kinds of things we cover ({kinds}). {total} recalls, newest first, from the U.S. Consumer Product Safety Commission.</p>
<p style="font-size:16px;color:#444;"><strong>How to check:</strong> type the brand or the model number from the label (often on the plug, the controller or under the base). If it matches, stop using it and follow the remedy on the CPSC notice: most recalls offer a refund or a free repair. Then report any incident at <a href="https://www.saferproducts.gov/" rel="nofollow noopener" target="_blank">SaferProducts.gov</a>.</p>
<div style="position:sticky;top:0;z-index:2;background:#fff;padding:8px 0;">
<input id="vp-rc-q" type="search" placeholder="Brand or model number, e.g. JKMAX or power bank" aria-label="Search recalls" style="width:100%;box-sizing:border-box;font-size:17px;padding:12px 14px;border:2px solid #1B2A41;border-radius:12px;">
<p id="vp-rc-n" style="font-size:14px;color:#666;margin:.3em 0 0;"></p></div>
<p style="font-size:16px;"><strong>Jump to:</strong> {" · ".join(jump)}</p>
{sections}
<h2 style="color:#1B2A41;font-size:1.35em;margin:1.4em 0 .3em;">About this page</h2>
<ul style="font-size:16px;">
<li><strong>Source:</strong> the CPSC's recall database (SaferProducts.gov API), the official US record. We sort recalls into our categories by their titles and leave out toys and children's products, which the CPSC lists at <a href="https://www.cpsc.gov/Recalls" rel="nofollow noopener" target="_blank">cpsc.gov/Recalls</a>.</li>
<li><strong>Updated:</strong> {today.strftime("%B %-d, %Y")}. We refresh it every week; a recall can be announced any day, so the CPSC notice is the final word.</li>
<li>"Sold at" names the stores the CPSC lists; we leave out the prices. Where a recall names a brand we cover, the card links our guide.</li>
<li>No affiliate links on this page. <a href="/p/how-we-rank-products.html">How we rank</a> · <a href="/p/affiliate-disclosure.html">Disclosure</a></li>
</ul>
</div>
<script>
(function(){{var q=document.getElementById("vp-rc-q"),n=document.getElementById("vp-rc-n");if(!q)return;
var cards=[].slice.call(document.querySelectorAll(".rc[data-q]")),heads=[].slice.call(document.querySelectorAll(".vp-rc-h"));
function run(){{var t=q.value.trim().toLowerCase(),shown=0;cards.forEach(function(c){{var ok=!t||c.getAttribute("data-q").indexOf(t)>-1;c.classList.toggle("vp-rc-hide",!ok);if(ok)shown++;}});
heads.forEach(function(h){{var g=h.nextElementSibling,any=g&&g.querySelector(".rc[data-q]:not(.vp-rc-hide)");h.classList.toggle("vp-rc-hide",!any);if(g)g.classList.toggle("vp-rc-hide",!any);}});
n.textContent=t?(shown+" recall"+(shown==1?"":"s")+" match \\u201c"+q.value.trim()+"\\u201d"):"";}}
q.addEventListener("input",run);}})();
</script>
'''


def main():
    today = datetime.date.today()
    start = f"{today.year - 1}-01-01"
    recalls = fetch(start)
    if len(recalls) < 50:
        sys.exit(f"only {len(recalls)} recalls from the CPSC API since {start}; page not rewritten")
    out = page(recalls, today)
    if "$" in re.sub(r"<(script|style)\b.*?</\1>", "", out, flags=re.S):
        sys.exit("a price slipped into the recall page; page not rewritten")
    PAGE.write_text(out, encoding="utf-8")
    print(f"{PAGE.relative_to(ROOT)}: {out.count('data-q=')} recalls in our categories (of {len(recalls)} since {start})")


if __name__ == "__main__":
    main()
