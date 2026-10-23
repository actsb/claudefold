#!/usr/bin/env python3
"""Apply the photo manifests in research/photo-manifests/*.json to the cards that show each product.

Each manifest entry with "status": "ok" gives one licensed press photo in brand/photos/ and the cards that use it; this
writes a "photo" dict (product_photos.py) into those cards' cards.json, after checking the file opens, is not from an
Amazon or retailer host, and carries a credit, a terms URL and a source. Entries marked "none" are listed so the owner can
ask the brand (daily/image-plan-2026-10-23.md has the email).

  python3 scripts/apply_photos.py            # dry run: what would change
  python3 scripts/apply_photos.py --write    # write cards.json
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANNED = re.compile(r"amazon\.|media-amazon|images-amazon|walmart\.|bestbuy\.|target\.com|homedepot\.|lowes\.|costco\.|chewy\.|petsmart\.|pinterest\.|reddit\.|google\.com/imgres", re.I)


def main():
    write = "--write" in sys.argv
    from PIL import Image
    changed, missing, rejected = {}, [], []
    for mf in sorted((ROOT / "research" / "photo-manifests").glob("*.json")):
        for e in json.loads(mf.read_text(encoding="utf-8")):
            if e.get("status") != "ok":
                missing.append((mf.stem, e["product"], e.get("notes", "")))
                continue
            f = ROOT / e.get("file", "")
            why = None
            if not e.get("file", "").startswith("brand/photos/") or not f.exists():
                why = "file missing"
            elif any(BANNED.search(e.get(k, "") or "") for k in ("image_url", "source")):
                why = "image from a banned host"
            elif not (e.get("credit") and e.get("terms") and e.get("source")):
                why = "credit, terms or source missing"
            else:
                try:
                    with Image.open(f) as im:
                        im.verify()
                except Exception as x:
                    why = f"not an image ({x})"
            if why:
                rejected.append((mf.stem, e["product"], why)); continue
            photo = {"file": e["file"], "kind": "brand", "credit": e["credit"], "source": e["source"], "terms": e["terms"],
                     "uses": [u for u in e.get("uses", ["web"]) if u in ("web", "social")] or ["web"], "checked": e.get("checked", "")}
            for d, cid in e["cards"]:
                changed.setdefault(d, {})[cid] = photo
    for d, by_id in changed.items():
        p = ROOT / d / "cards.json"
        spec = json.loads(p.read_text(encoding="utf-8"))
        n = 0
        for c in spec["cards"]:
            if c["id"] in by_id and c.get("photo", {}).get("kind") != "own":   # our own photo always wins
                if c.get("photo") != by_id[c["id"]]:
                    c["photo"] = by_id[c["id"]]; n += 1
        print(f"{d}: {n} card photo(s) {'written' if write else 'to write'}")
        if write and n:
            p.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for m, prod, why in rejected:
        print(f"REJECTED [{m}] {prod}: {why}")
    print(f"\nno licensed photo yet ({len(missing)}): ask the brand (daily/image-plan-2026-10-23.md, section 4)")
    for m, prod, note in missing:
        print(f"  [{m}] {prod}: {note[:100]}")


if __name__ == "__main__":
    main()
