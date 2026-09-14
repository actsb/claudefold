"""Apply the site's search/AI-search structure to a post's easy layer (src/00-easy.html):
byline with Published/Updated and the editors link, a Key-takeaways box plus a collapsed Korean summary
before the first H2, question-form H2s with a one-sentence verdict, no manual jump break, and minified
JSON-LD (ItemList of the cards + FAQPage from the Quick answers) before the pin block.
Usage: python3 scripts/seo_layer.py posts/<slug> brand/seo-configs.json
"""
import html as H, json, pathlib, re, sys

H2 = '<h2 style="color:#1B2A41;font-size:1.6em;line-height:1.25;margin:1.4em 0 .5em;">'
def esc(s): return H.escape(s, quote=False)

def main(post_dir, cfg_path):
    d = pathlib.Path(post_dir); cfg = json.loads(pathlib.Path(cfg_path).read_text(encoding="utf-8"))[d.name]
    p = d / "src" / "00-easy.html"; t = p.read_text(encoding="utf-8")
    # 1. byline
    m = re.search(r'<p style="font-size:15px;color:#555;"><em>(Published|Updated) ([A-Z][a-z]+ \d{1,2}, \d{4}) · By Verdict Picks staff ·', t)
    if m:
        t = t.replace(m.group(0), f'<p style="font-size:15px;color:#555;"><em>Published {m.group(2)} · Updated {cfg["updated"]} · By the <a href="/p/about-verdict-picks.html">Verdict Picks editors</a> (Vera, our host, is an illustrated persona) ·', 1)
    else:
        t = re.sub(r'· Updated [A-Z][a-z]+ \d{1,2}, \d{4} ·', f'· Updated {cfg["updated"]} ·', t, count=1)
    # 2. no manual jump break (the assembler adds one after the lead)
    t = t.replace("<!--more-->\n", "").replace("<!--more-->", "")
    # 3. key takeaways + Korean summary before the first H2
    if "Key takeaways" not in t:
        box = ('<div class="vp-key" style="border:2px solid #1E8E5A;border-radius:14px;padding:16px 18px;background:#fff;margin:1em 0 1.4em;">'
               '<p style="margin:0 0 .4em;font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#1E8E5A;">Key takeaways</p>'
               '<ul style="margin:0;padding-left:20px;font-size:17px;">' + "".join(f'<li style="margin-bottom:.3em;"><strong>{esc(k)}</strong> {esc(v)}</li>' for k, v in cfg["takeaways"]) + '</ul></div>\n'
               '<details style="margin:0 0 1.4em;font-size:16px;color:#333;"><summary style="cursor:pointer;color:#1B2A41;font-weight:700;">한국어 요약 (Korean summary)</summary>'
               f'<p style="margin:.6em 0 0;">{cfg["korean"]}</p></details>\n')
        i = t.index("<h2 "); t = t[:i] + box + t[i:]
    # 4. question-form H2s with a verdict sentence
    for old, new, verdict in cfg.get("h2", []):
        if re.search(r"<h2[^>]*>" + re.escape(new) + r"</h2>", t): continue   # already rewritten (re-runs are safe)
        # match the H2 by its text; keep whatever attributes it carries (some have id="picker" for jump links)
        m = re.search(r"<h2([^>]*)>" + re.escape(old) + r"</h2>", t)
        if not m: raise SystemExit(f"H2 not found in {d.name}: {old}")
        t = t.replace(m.group(0), f"<h2{m.group(1)}>" + new + "</h2>" + (f'\n<p style="font-size:1.1em;"><strong>{esc(verdict)}</strong></p>' if verdict else ""), 1)
    # 4b. stories: one real comparison table (th headers) built from the cards, under the alternatives H2
    if cfg.get("table") and "<table" not in t:
        cards_ = json.loads((d / "cards.json").read_text(encoding="utf-8"))["cards"]
        th = 'style="text-align:left;padding:10px 12px;"'; td = 'style="padding:10px 12px;border:1px solid #ddd;vertical-align:top;"'
        rows = "".join(f'<tr><td {td}><a href="#card-{c["id"]}" style="color:#1B2A41;font-weight:700;">{esc(c["name"])}</a><br><span style="font-size:14px;color:#1E8E5A;">{esc(c.get("badge", ""))}</span></td>'
                       f'<td {td}>{esc(c["price"])}</td><td {td}>{esc(c["buy_if"][0].upper() + c["buy_if"][1:])}</td><td {td}>{esc(c["skip_if"][0].upper() + c["skip_if"][1:])}</td></tr>' for c in cards_)
        table = ('<div style="overflow-x:auto;margin:.6em 0 1.2em;"><table style="border-collapse:collapse;width:100%;font-size:16px;min-width:640px;">'
                 f'<thead><tr style="background:#1B2A41;color:#fff;"><th {th}>Product</th><th {th}>Price at the time of writing</th><th {th}>Buy it if</th><th {th}>Skip it if</th></tr></thead>'
                 f'<tbody>{rows}</tbody></table></div>\n')
        m = re.search(r"<h2[^>]*>" + re.escape(cfg["table"]) + r"</h2>\n", t)
        if not m: raise SystemExit(f"table anchor H2 not found in {d.name}: {cfg['table']}")
        t = t[:m.end()] + table + t[m.end():]
    # 5. JSON-LD
    t = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", t, flags=re.S)
    cards = json.loads((d / "cards.json").read_text(encoding="utf-8"))["cards"]
    url = cfg["url"]
    def clean(s): return H.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    qa = t[t.index("Quick answers"):] if "Quick answers" in t else ""
    faq = re.findall(r"<h3[^>]*>(.*?)</h3>\s*<p>(.*?)</p>", qa, flags=re.S)
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": cfg["list_name"], "url": url,
           "itemListOrder": "https://schema.org/ItemListOrderAscending", "numberOfItems": len(cards),
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f'{c["name"]} — {c.get("badge", "")}'.strip(" —"), "url": f'{url}#card-{c["id"]}'} for i, c in enumerate(cards)]}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in faq]})
    script = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + "</script>\n"
    if "<!--PIN-->" not in t: raise SystemExit(f"no pin block in {d.name}")
    t = t.replace("<!--PIN-->", script + "<!--PIN-->", 1)
    p.write_text(t, encoding="utf-8")
    print(f"{d.name}: byline ok, takeaways {t.count('Key takeaways')}, h2 rewrites {len(cfg.get('h2', []))}, faq entries {len(faq)}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
