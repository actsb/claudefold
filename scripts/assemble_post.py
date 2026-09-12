#!/usr/bin/env python3
"""Assemble a post: the easy shopping-guide layer + the long deep-dive folded into <details>.

Usage: python3 scripts/assemble_post.py posts/<slug>
Reads  src/00-easy.html (placeholders: <!--TOPPICK-->, <!--CARDS-->, <!--CARD:id-->),
       cards.json, images/cards/<id>.svg, src/01..06 (the deep-dive parts)
Writes post.src.html (then run build_post.py to inline the remaining <!--SVG:...--> figures).
"""
import json, re, sys, pathlib, html

BADGE = ('display:inline-block;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.02em;'
         'padding:4px 11px;border-radius:999px;background:{bg};color:#fff;')
BTN = ('display:inline-block;background:#1E8E5A;color:#fff;text-decoration:none;font-weight:700;'
       'font-size:18px;padding:12px 20px;border-radius:8px;')
VIDEO = ('<div class="vp-video" style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;background:#000;margin:14px 0 4px;">'
         '<iframe style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" src="https://www.youtube.com/embed/{vid}" title="{title}" loading="lazy" '
         'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')

def esc(s): return html.escape(s, quote=True)

STYLE = """<style>
.vp-post img{max-width:100%;height:auto}
.vp-post .vp-grid a{color:#1B2A41;font-weight:700}
@media (max-width:640px){
  .vp-post .vp-gridwrap{overflow:visible}
  .vp-post .vp-grid{min-width:0!important;display:block;border:0}
  .vp-post .vp-grid thead{display:none}
  .vp-post .vp-grid tbody,.vp-post .vp-grid tr{display:block}
  .vp-post .vp-grid tr{border:1px solid #ddd;border-radius:10px;margin:0 0 14px;overflow:hidden}
  .vp-post .vp-grid td{display:block;border:0!important;border-top:1px solid #eee!important;padding:9px 12px!important}
  .vp-post .vp-grid td:first-child{border-top:0!important;background:#1B2A41!important;color:#fff;font-size:1.05em}
  .vp-post .vp-grid td[data-col]:not(:first-child)::before{content:attr(data-col);display:block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:#1E8E5A;margin-bottom:2px}
}
</style>
"""

def responsive_grid(html_text):
    """Add class vp-grid + data-col labels to the picker table so the CSS can stack it on phones."""
    def fix_table(m):
        t = m.group(0)
        heads = re.findall(r"<th[^>]*>(.*?)</th>", t, flags=re.S)
        def fix_row(rm):
            row = rm.group(0); i = [0]
            def fix_td(tm):
                label = re.sub(r"<[^>]+>", "", heads[i[0]]) if i[0] < len(heads) else ""
                i[0] += 1
                return tm.group(1) + f' data-col="{esc(label)}"' + tm.group(2)
            return re.sub(r"(<td)([^>]*>)", fix_td, row)
        t = re.sub(r"<tr>.*?</tr>", fix_row, t, flags=re.S)
        t = t.replace("<table ", '<table class="vp-grid" ', 1)
        return t
    html_text = re.sub(r'<table style="border-collapse:collapse;width:100%;font-size:17px;min-width:\d+px;">.*?</table>', fix_table, html_text, count=1, flags=re.S)
    return html_text.replace('<div style="overflow-x:auto;margin:1em 0 1.4em;">', '<div class="vp-gridwrap" style="overflow-x:auto;margin:1em 0 1.4em;">', 1)


def card_svg(d, cid):
    f = d / "images" / "cards" / f"{cid}.svg"
    svg = f.read_text(encoding="utf-8").strip()
    return re.sub(r"^<\?xml[^>]*\?>\s*", "", svg)

def cta(c, label):
    return f'<a style="{BTN}" href="{esc(c["cta"]).replace("&amp;amp;","&amp;")}" rel="nofollow sponsored noopener" target="_blank">{esc(label)} →</a>'

def top_pick(d, c):
    return f'''<div class="vp-top" id="top-pick" style="display:flex;flex-wrap:wrap;gap:22px;align-items:center;border:3px solid #1E8E5A;border-radius:16px;padding:20px;background:#fff;margin:1.2em 0 1.6em;">
<div style="flex:1 1 280px;min-width:0;">{card_svg(d, c["id"])}</div>
<div style="flex:1.2 1 300px;min-width:0;">
<span style="{BADGE.format(bg='#1E8E5A')}">{esc(c["badge"])}</span>
<h3 style="font-size:1.7em;line-height:1.2;margin:.35em 0 .2em;color:#1B2A41;">{esc(c["name"])}</h3>
<p style="font-size:1.25em;font-weight:700;color:#1E8E5A;margin:0 0 .6em;">{esc(c["price"])}</p>
<ul style="margin:0 0 1em;padding-left:20px;">
<li style="margin-bottom:.4em;"><strong>Buy it if</strong> {esc(c["buy_if"])}</li>
<li style="margin-bottom:.4em;"><strong>Skip it if</strong> {esc(c["skip_if"])}</li>
<li><strong>From the reviews:</strong> {esc(c["owners"])}</li>
</ul>
{cta(c, "See today's price on Amazon")}
</div>
</div>'''

def pick_card(d, c, n, with_video=True):
    vid = VIDEO.format(vid=c["video"], title=esc(c.get("video_title", c["name"] + " review"))) if (c.get("video") and with_video) else ""
    return f'''<div class="vp-card" id="card-{c["id"]}" style="border:1px solid #ddd;border-radius:14px;padding:18px;background:#fff;margin:1.2em 0;">
<div style="display:flex;flex-wrap:wrap;gap:20px;align-items:center;">
<div style="flex:1 1 240px;min-width:0;max-width:420px;">{card_svg(d, c["id"])}</div>
<div style="flex:1.4 1 280px;min-width:0;">
<span style="{BADGE.format(bg='#1B2A41')}">{n}. {esc(c["badge"])}</span>
<h3 style="font-size:1.45em;line-height:1.2;margin:.35em 0 .2em;color:#1B2A41;">{esc(c["name"])}</h3>
<p style="font-size:1.15em;font-weight:700;color:#1E8E5A;margin:0 0 .5em;">{esc(c["price"])}</p>
<ul style="margin:0 0 .9em;padding-left:20px;">
<li style="margin-bottom:.35em;"><strong>Buy it if</strong> {esc(c["buy_if"])}</li>
<li style="margin-bottom:.35em;"><strong>Skip it if</strong> {esc(c["skip_if"])}</li>
<li><strong>From the reviews:</strong> {esc(c["owners"])}</li>
</ul>
{cta(c, "Check the price on Amazon")}
</div>
</div>
{vid}
</div>'''

def main(post_dir):
    d = pathlib.Path(post_dir)
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    cards = spec["cards"]; by_id = {c["id"]: c for c in cards}
    easy = (d / "src" / "00-easy.html").read_text(encoding="utf-8")
    easy = responsive_grid(easy)
    easy = easy.replace('<div class="vp-post"', STYLE + '<div class="vp-post"', 1)
    notice = ('<p class="vp-notice" style="font-size:16px;background:#F7F5F0;border-left:5px solid #1B2A41;padding:10px 14px;margin:0 0 1.2em;">'
              '<strong>Two ways to read this.</strong> In a hurry: the quick guide starts right here — one pick, a 10-second picker, every product in 30 seconds. '
              'Have twenty minutes: the <a href="#deep" style="color:#1B2A41;font-weight:700;">complete deep-dive</a> follows on this same page — how we tested, every brand, every pick in detail, thousands of owner reviews, and when to buy.</p>\n')
    easy = easy.replace("<h2 style=", notice + "<h2 style=", 1)
    easy = easy.replace("<!--TOPPICK-->", top_pick(d, cards[0]))
    easy = easy.replace("<!--CARDS-->", "\n".join(pick_card(d, c, i + 1, with_video=(i > 0)) for i, c in enumerate(cards)))
    easy = re.sub(r"<!--CARD:([a-z0-9\-]+)-->", lambda m: pick_card(d, by_id[m.group(1)], cards.index(by_id[m.group(1)]) + 1), easy)
    parts = sorted(p for p in (d / "src").glob("0[1-9]-*.html"))
    deep = "\n".join(p.read_text(encoding="utf-8") for p in parts)
    # strip the wrapper, byline and cover the deep-dive parts open with, and the wrapper close at the end
    deep = re.sub(r'^\s*<div class="vp-post"[^>]*>\s*<p[^>]*><em>.*?</em></p>\s*<p[^>]*><img[^>]*></p>', "", deep, count=1, flags=re.S)
    deep = re.sub(r"</div>\s*$", "", deep.rstrip(), count=1)
    # reading guide for the deep-dive: one line per section with a minutes estimate
    secs = [(m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip(), m.start()) for m in re.finditer(r'<h2 id="([a-z0-9\-]+)"[^>]*>(.*?)</h2>', deep, flags=re.S)]
    items = []
    for i, (sid, title, pos) in enumerate(secs):
        nxt = secs[i + 1][2] if i + 1 < len(secs) else len(deep)
        words = len(re.findall(r"[A-Za-z0-9$][A-Za-z0-9$'’.,%/-]*", re.sub(r"<[^>]+>", " ", deep[pos:nxt])))
        mins = max(1, round(words / 230))
        items.append(f'<li style="margin-bottom:.3em;"><a href="#{sid}" style="color:#1B2A41;font-weight:700;">{esc(title)}</a> <span style="color:#777;font-size:.9em;">· about {mins} min</span></li>')
    out = (easy
           + '\n<h2 id="deep" style="color:#1B2A41;font-size:1.6em;line-height:1.25;margin:1.6em 0 .5em;">Have more time? The full deep-dive, section by section</h2>\n'
           + '<p>The quick guide above is enough to buy well. If you want to know <em>why</em> — how we tested, what every brand does well and badly, every pick in detail, what thousands of owners said, and when to buy — the complete analysis follows. Read it in one go, or one section at a time when you have a few minutes. Each section stands on its own.</p>\n'
           + '<div class="vp-roadmap" style="border:2px solid #1B2A41;border-radius:12px;padding:14px 20px;background:#F7F5F0;margin:1em 0 1.6em;">\n<strong style="color:#1B2A41;">Reading plan</strong>\n<ol style="margin:8px 0 0;padding-left:22px;">\n' + "\n".join(items) + '\n</ol>\n</div>\n'
           + '<div class="vp-deep" style="border-top:3px solid #1B2A41;margin-top:1.4em;padding-top:1.2em;font-size:0.94em;">\n' + deep + '\n</div>\n'
           + '<p style="margin:1.6em 0 1em;"><a href="#top-pick" style="display:inline-block;background:#1B2A41;color:#fff;text-decoration:none;font-weight:700;padding:10px 16px;border-radius:8px;">↑ Back to the quick guide and the top pick</a></p>\n'
           + '<p style="font-size:15px;color:#555;"><em>As an Amazon Associate I earn from qualifying purchases. Prices are US list and sale prices seen in 2026 at the time of writing; check the retailer for today\'s price. We do not accept products or payment from manufacturers. <a href="/p/how-we-rank-products.html">How we rank</a> · <a href="/p/affiliate-disclosure.html">Disclosure</a></em></p>\n'
           + '</div>\n')
    (d / "post.src.html").write_text(out, encoding="utf-8")
    print(f"assembled {d/'post.src.html'} ({len(out):,} bytes, {len(cards)} cards)")

if __name__ == "__main__":
    main(sys.argv[1])
