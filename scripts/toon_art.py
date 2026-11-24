#!/usr/bin/env python3
"""Generate a comic's panel art with Google Gemini (gemini-2.5-flash-image) from posts/<dir>/webtoon.json.

  python3 scripts/toon_art.py posts/<dir> [--only 3,5] [--force]

Each panel with an "art" dict {"prompt": "...", "size": "1536x1024" | "1024x1536" | "1024x1024", "cast": ["sam", "biscuit"]}
gets posts/<dir>/toon-art/<id>-pNN.jpg (1440 px wide JPEG). The prompt sent is: the series style + the cast sheet for every
character named in "cast" + the panel prompt + the no-text rule. Existing files are kept unless --force or --only names
the panel, so a rerun costs nothing. Lettering (balloons, captions, numbers) is never drawn by the model: webtoon.py adds it.

The API key is never read here: the session's network proxy injects it for generativelanguage.googleapis.com
(Google's OpenAI-compatible images endpoint). Characters are original; never ask the model for an existing series' style,
an artist's name, a real person, a brand logo or a specific real product.
"""
import base64, json, os, pathlib, subprocess, sys, time, urllib.request, urllib.error

URL = "https://generativelanguage.googleapis.com/v1beta/openai/images/generations"
MODEL = "gemini-2.5-flash-image"
STYLE = ("Professional Korean-style vertical webtoon panel, full-color digital illustration, crisp clean line art, soft cel shading, "
         "cinematic composition and lighting, expressive faces, consistent character design. ")
NO_TEXT = (" Absolutely no text, letters, numbers, captions, speech bubbles, signatures, watermarks, logos or brand names anywhere in the image (phones and laptops are plain, with no maker logo on the back or lid); "
           "screens and labels are blank or abstract. No panel border, no white margins or letterboxing: the art fills the whole frame edge to edge.")
CAST = {
    "sam": "Sam: a man in his late 20s, warm brown skin, short dark curly hair, clean-shaven, friendly round face, mustard-yellow hoodie with white drawstrings, light gray joggers.",
    "biscuit": "Biscuit: Sam's small tricolor beagle puppy (brown, black saddle, white chest and paws, long floppy brown ears), red collar.",
    "vera": "Vera: a confident woman in her early 30s, light skin, long straight dark-brown hair with side-swept bangs, small gold stud earrings, navy blazer over an emerald-green top; the guide's host.",
    "jo": "Jo: a woman in her early 30s, fair skin, auburn chin-length bob, round tortoiseshell glasses, teal cardigan over a white tee.",
    "june": "June: Jo's grandmother, about 80, gentle smile, short silver curly hair, rosy cheeks, lavender knit cardigan, reading glasses on a chain.",
}

NATIVE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
NATIVE_MODEL = os.environ.get("TOON_IMAGE_MODEL", "gemini-3-pro-image")
RATIO = {"1536x1024": "3:2", "1024x1536": "2:3", "1024x1024": "1:1"}

def gen_native(prompt, size, refs=()):
    """Gemini's own API (key in the x-goog-api-key header, injected by the proxy): better models and reference images."""
    parts = [{"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(pathlib.Path(r).read_bytes()).decode()}} for r in refs]
    parts.append({"text": prompt})
    body = json.dumps({"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": RATIO.get(size, "3:2")}}}).encode()
    req = urllib.request.Request(NATIVE.format(model=NATIVE_MODEL), data=body, headers={"x-goog-api-key": "proxy-injected", "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    for p in r["candidates"][0]["content"]["parts"]:
        if "inlineData" in p: return base64.b64decode(p["inlineData"]["data"])
    raise KeyError("no image in the response")

def gen(prompt, size, refs=()):
    """Native API first; if its key is not set up (HTTP 400/401/403), the OpenAI-compatible endpoint (Bearer key, no references)."""
    native = True
    for attempt in range(4):
        try:
            if native: return gen_native(prompt, size, refs)
            body = json.dumps({"model": MODEL, "prompt": prompt, "n": 1, "response_format": "b64_json", "size": size}).encode()
            req = urllib.request.Request(URL, data=body, headers={"Authorization": "Bearer proxy-injected", "Content-Type": "application/json"})
            return base64.b64decode(json.load(urllib.request.urlopen(req, timeout=240))["data"][0]["b64_json"])
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:200]
            if native and e.code in (400, 401, 403) and ("API key" in msg or "credential" in msg.lower() or e.code != 400):
                print(f"  native API refused ({e.code}); using the compatible endpoint"); native = False; continue
            print(f"  retry {attempt + 1}: HTTP {e.code} {msg}"); time.sleep(5 * (attempt + 1))
        except (urllib.error.URLError, KeyError, IndexError, TimeoutError) as e:
            print(f"  retry {attempt + 1}: {e}"); time.sleep(5 * (attempt + 1))
    raise SystemExit("image generation failed")

def trim(f):
    """The model sometimes adds a white or coloured margin and a frame line: trim flat edges until nothing changes, then shave the line."""
    size = lambda: subprocess.run(["identify", "-format", "%wx%h", str(f)], capture_output=True, text=True).stdout
    before = size()
    for _ in range(4):
        prev = size()
        subprocess.run(["mogrify", "-fuzz", "12%", "-trim", "+repage", str(f)], check=True)
        if size() == prev: break
    if size() != before: subprocess.run(["mogrify", "-shave", "5x5", "+repage", str(f)], check=True)

def main(d, only=None, force=False):
    d = pathlib.Path(d); spec = json.loads((d / "webtoon.json").read_text(encoding="utf-8")); sid = spec["id"]
    out = d / "toon-art"; out.mkdir(exist_ok=True)
    cast = {**CAST, **spec.get("cast", {})}
    for i, p in enumerate(spec["panels"], 1):
        if "art" not in p: continue
        f = out / f"{sid}-p{i:02d}.jpg"
        if f.exists() and not force and not (only and i in only): continue
        if only and i not in only: continue
        a = p["art"]
        who = " ".join(cast[c] for c in a.get("cast", []))
        prompt = STYLE + spec.get("style", "") + (" Characters: " + who + " " if who else " ") + "Scene: " + a["prompt"] + NO_TEXT
        refs = [pathlib.Path(__file__).resolve().parent.parent / r for r in a.get("refs", []) + [f"brand/toon-cast/{c}.jpg" for c in a.get("cast", []) if (pathlib.Path(__file__).resolve().parent.parent / f"brand/toon-cast/{c}.jpg").exists()]]
        if refs: prompt += " Match the character designs in the attached reference images exactly (face, hair, outfit), but not their pose or background."
        t = time.time(); png = gen(prompt, a.get("size", "1536x1024"), refs)
        tmp = out / f".{f.stem}.png"; tmp.write_bytes(png)
        trim(tmp)
        subprocess.run(["convert", str(tmp), "-resize", "1440x", "-strip", "-quality", "88", str(f)], check=True); tmp.unlink()
        print(f"panel {i:02d}: {f.name} ({f.stat().st_size // 1024} KB, {time.time() - t:.0f} s)")

if __name__ == "__main__":
    a = sys.argv[1:]
    only = {int(x) for x in a[a.index("--only") + 1].split(",")} if "--only" in a else None
    main(a[0], only, "--force" in a)
