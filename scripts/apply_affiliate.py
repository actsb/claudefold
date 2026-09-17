"""Swap a post's software links to affiliate links once a program accepts the site, and rewrite the disclosure sentences to match.
Usage: python3 scripts/apply_affiliate.py posts/<slug> affiliate.json [--dry-run]
affiliate.json: {"higgsfield": "https://<tracking link>", "elevenlabs": "https://<tracking link>"}   (omit a key to leave that card as a plain link)
Then rebuild (assemble_post → seo_layer → assemble_post → build_post → check_post) and republish with publish_blogger.py.
The tracking links themselves are never committed anywhere else; keep affiliate.json outside the repo or in .gitignore.
"""
import json, pathlib, re, sys

NAMES = {"higgsfield": "Higgsfield", "elevenlabs": "ElevenLabs"}

def main(post_dir, cfg_path, dry=False):
    d = pathlib.Path(post_dir); links = json.loads(pathlib.Path(cfg_path).read_text(encoding="utf-8"))
    on = [k for k in ("higgsfield", "elevenlabs") if links.get(k)]
    if not on: raise SystemExit("no links given")
    names = " and ".join(NAMES[k] for k in on)
    # 1. cards: cta + paid flag (the assembler then adds rel=sponsored, the "(paid link)" tag and the buy-box "paid link" line)
    cj = d / "cards.json"; spec = json.loads(cj.read_text(encoding="utf-8"))
    for c in spec["cards"]:
        if c["id"] in on:
            c["cta"] = links[c["id"]]; c["paid"] = True; c["rel"] = "nofollow sponsored noopener"
    plain = [NAMES[k] for k in ("higgsfield", "elevenlabs") if k not in on] + ["Claude"]
    spec["buy_total"] = re.sub(r"The software buttons are ordinary links; we hold no affiliate relationship with Higgsfield, Anthropic or ElevenLabs at the time of writing\.",
                               f"The {names} buttons are paid links: if you subscribe through one, we earn a commission at no extra cost to you. The {' and '.join(plain)} button{'s are' if len(plain) > 1 else ' is an'} ordinary link{'s' if len(plain) > 1 else ''}.", spec["buy_total"])
    # 2. source: byline, Korean summary, setup step 3, referral paragraph, method note
    sp = d / "src" / "00-easy.html"; s = sp.read_text(encoding="utf-8"); before = s
    s = s.replace("The software links are ordinary links; we hold no affiliate relationship with Higgsfield, Anthropic or ElevenLabs at the time of writing.",
                  f"Software links marked (paid link) are affiliate links for {names}: if you subscribe through one, we earn a commission at no extra cost to you. The Claude links are ordinary links.")
    s = s.replace("소프트웨어 링크는 일반 링크입니다.", f"{' · '.join(NAMES[k] for k in on)} 링크는 제휴 링크이고(paid link 표시), 클로드 링크는 일반 링크입니다.")
    if "higgsfield" in on:
        s = s.replace('Create it on <a href="https://higgsfield.ai/" rel="nofollow noopener" target="_blank">Higgsfield\'s site</a> first (the same link as in the stack below), then connect;',
                      f'Create it on <a href="{links["higgsfield"]}" rel="nofollow sponsored noopener" target="_blank">Higgsfield\'s site</a> first (paid link; the same link as in the stack below), then connect;')
    s = s.replace('It is also the gate we are standing at: this page carries no software affiliate links yet, and it will say "paid link" next to any that arrive.',
                  f'This page carries affiliate links for {names}, each marked "paid link"' + ('; a new Higgsfield account that arrives through the link may see a time-limited discount at signup, which is the program\'s own offer, not a coupon.' if "higgsfield" in on else '.'))
    s = s.replace("The five-skill pack and the connector permission settings come from a Korean-language lesson we studied but do not embed; the English tutorials above cover the same method. The plan, the animatic,",
                  f"The five-skill pack and the connector permission settings come from a Korean-language lesson we studied but do not embed; the English tutorials above cover the same method. Verdict Picks is an affiliate of {names}; the links are marked and the commission never changes what you pay. The plan, the animatic,")
    changed = sum(1 for a, b in zip(before.split("\n"), s.split("\n")) if a != b)
    print(f"{d.name}: links for {names}; {changed} source lines changed; cards updated: {on}")
    if dry: print("dry run, nothing written"); return
    cj.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); sp.write_text(s, encoding="utf-8")
    print("now rebuild: assemble_post → seo_layer → assemble_post → build_post → check_post, then publish_blogger.py --posts-only --only <key>")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], dry="--dry-run" in sys.argv)
