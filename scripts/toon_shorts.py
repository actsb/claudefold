#!/usr/bin/env python3
"""Turn a post's comic (webtoon.json + toon-art/) into a YouTube Short: 1080x1920, 30 fps, under 60 s, music, English
subtitles, plus subtitle files and titles/descriptions in 11 languages (translated by Gemini through the proxy-held key).

  python3 scripts/toon_shorts.py posts/<dir> OUT_DIR [--no-translate]

Writes OUT_DIR/<id>.mp4, <id>.<lang>.srt for every language and <id>-youtube.json (title and description per language,
plus the upload settings). Every panel is the lettered comic panel (the same facts as the guide), centred over a blurred
copy of its art with a slow push-in, crossfaded to the next. Music is synthesised by scripts/make_music.py (no samples).
Needs FFMPEG (scripts/bootstrap.sh) and Playwright (scripts/render_png.mjs).
"""
import json, os, pathlib, re, subprocess, sys, urllib.request, urllib.error, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import webtoon

ROOT = pathlib.Path(__file__).resolve().parent.parent
FF = os.environ.get("FFMPEG") or str(next(pathlib.Path("/tmp").glob("claude-0/*/*/scratchpad/ffm/node_modules/ffmpeg-static/ffmpeg"), "ffmpeg"))
VW, VH, FPS, XF = 1080, 1920, 30, 0.35
LANGS = {"en": "English", "es": "Spanish", "pt": "Portuguese (Brazil)", "fr": "French", "de": "German", "ja": "Japanese",
         "ko": "Korean", "zh-Hans": "Chinese (Simplified)", "hi": "Hindi", "id": "Indonesian", "vi": "Vietnamese"}
BLOG = "https://acts39.blogspot.com"

def run(*a): subprocess.run([str(x) for x in a], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def panel_lines(p):
    out = []
    for it in p.get("items", []) + p.get("over", []):
        if it["t"] in ("say", "narr"): out.append(it["text"])
        elif it["t"] == "card": out.append(it["title"] + ": " + "; ".join(" ".join(r[:2]) if isinstance(r, list) else r for r in it["rows"]))
        elif it["t"] == "text": out.append(it["text"])
    return out

def band_svg(top, bottom):
    def t(x, y, s, size, weight, fill, anchor="middle", ls=0):
        return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter,Helvetica,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" letter-spacing="{ls}">{html.escape(s)}</text>'
    lines = webtoon.wrap(top[1], 960, 46, True)[:2]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}">'
            f'<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1424" stop-opacity="0.92"/><stop offset="1" stop-color="#0B1424" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="g2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0B1424" stop-opacity="0.92"/><stop offset="1" stop-color="#0B1424" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="{VW}" height="300" fill="url(#g1)"/><rect y="{VH-260}" width="{VW}" height="260" fill="url(#g2)"/>'
            + t(VW / 2, 92, top[0], 30, 800, "#7FD1A8", ls=6)
            + "".join(t(VW / 2, 158 + i * 56, l, 46, 800, "#FFFFFF") for i, l in enumerate(lines))
            + t(VW / 2, VH - 120, bottom, 34, 700, "#FFFFFF")
            + t(VW / 2, VH - 72, "Characters are fictional · art made with Google Gemini (AI)", 24, 500, "#C9D4E5")
            + '</svg>')

def gemini_json(prompt, model="gemini-3.1-pro-preview"):
    """Native Gemini API (x-goog-api-key) first, the OpenAI-compatible endpoint (Bearer) if that key is not set up."""
    try:
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}).encode()
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", data=body,
                                     headers={"x-goog-api-key": "proxy-injected", "Content-Type": "application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=600))
        txt = "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"] if not p.get("thought"))
    except urllib.error.HTTPError as e:
        if e.code not in (400, 401, 403): raise
        body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}}).encode()
        req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", data=body,
                                     headers={"Authorization": "Bearer proxy-injected", "Content-Type": "application/json"})
        txt = json.load(urllib.request.urlopen(req, timeout=600))["choices"][0]["message"]["content"]
    return json.loads(re.sub(r"^```(json)?|```$", "", txt.strip(), flags=re.M))

def srt_time(t):
    ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"

def panel_speakers(p):
    sp = {"narrator"}
    for it in p.get("items", []) + p.get("over", []):
        if it["t"] == "say": sp.add(it.get("who", "narrator"))
    return sorted(sp)

def still(png, D, out, W=None, H=None, zoom=0.05):
    W, H = W or VW, H or VH
    run(FF, "-y", "-framerate", "30", "-loop", "1", "-t", f"{D:.3f}", "-i", png, "-filter_complex",
        f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},zoompan=z='1+{zoom}*on/({D*30:.0f})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30,format=yuv420p[v]",
        "-map", "[v]", "-t", f"{D:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out)

def panel_clip(png, art, D, band, out):
    w, h = [int(v) for v in subprocess.run(["identify", "-format", "%w %h", str(png)], capture_output=True, text=True).stdout.split()]
    fw = 1000; fh = round(fw * h / w)
    if fh > 1340: fh = 1340; fw = round(fh * w / h)
    src = art if art is not None and art.exists() else png
    flt = (f"[0:v]scale={VW}:{VH}:force_original_aspect_ratio=increase,crop={VW}:{VH},gblur=sigma=28,eq=brightness=-0.18:saturation=1.1[bg];"
           f"[1:v]scale={fw}:{fh},format=rgba,scale=w='trunc({fw}*(1+0.05*t/{D:.3f})/2)*2':h=-2:eval=frame[fg];"
           f"[bg][fg]overlay=x='(W-w)/2':y='(H-h)/2+30':eval=frame[v1];[2:v]format=rgba,scale={VW}:{VH}[band];[v1][band]overlay=0:0,fps={FPS},format=yuv420p[v]")
    run(FF, "-y", "-loop", "1", "-t", f"{D:.3f}", "-i", src, "-loop", "1", "-t", f"{D:.3f}", "-i", png, "-loop", "1", "-t", f"{D:.3f}", "-i", band,
        "-filter_complex", flt, "-map", "[v]", "-r", FPS, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out)

def localize(sid, out, title, description, tags, lines, kind):
    """Title, description, tags and the spoken subtitle lines in the 11 languages (cached per input)."""
    import hashlib
    cache_f = out / f"{sid}-i18n-cache.json"; key = hashlib.sha1(json.dumps([title, description, tags, lines]).encode()).hexdigest()
    cache = json.loads(cache_f.read_text(encoding="utf-8")) if cache_f.exists() else {}
    if cache.get("key") != key: cache = {"key": key, "meta": {}, "subs": {}}
    cache["meta"]["en"] = {"title": title, "description": description, "tags": tags}; cache["subs"]["en"] = lines
    for lang, name in LANGS.items():
        if lang in cache["meta"]: continue
        r = gemini_json(f"Translate this YouTube {kind}'s title, description, tags and spoken subtitle lines from English into {name}, natural and lively as a native "
                        f"speaker would write them, keeping the jokes. Keep product names, model numbers, prices, URLs, hashtags, chapter timestamps and source names "
                        f"exactly; translate dates naturally; 'space heater' is an electric room heater. Tags: 10 to 15 short search terms people in that language "
                        f"really type (keep brand names). Return JSON {{\"title\": str (max 100 characters), \"description\": str, \"tags\": [str], "
                        f"\"subtitles\": [str] (same count and order)}}.\n\n" + json.dumps({"title": title, "description": description, "tags": tags, "subtitles": lines}, ensure_ascii=False))
        if len(r.get("subtitles", [])) != len(lines): raise SystemExit(f"{lang}: subtitle count mismatch")
        cache["meta"][lang] = {"title": r["title"][:100], "description": r["description"], "tags": r["tags"]}; cache["subs"][lang] = r["subtitles"]
        cache_f.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8"); print("translated", lang)
    return cache["meta"], cache["subs"]

def main(d, out, translate=True):
    import toon_voice as V
    d = pathlib.Path(d); out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    spec, blocks = webtoon.build(d, return_blocks=True); sid = spec["id"]
    yt = json.loads((d / "youtube.json").read_text(encoding="utf-8"))
    work = out / f"{sid}-work"; png = work / "png"; png.mkdir(parents=True, exist_ok=True)
    for f in list(png.glob("*")) + list(work.glob("c*.mp4")): f.unlink()
    for i, (gap, h, svg, tr) in enumerate(blocks):
        (png / f"b{i:02d}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {h}"><rect width="800" height="{h}" fill="#fff"/>{svg}</svg>', encoding="utf-8")
    (png / "band.svg").write_text(band_svg((f'VERDICT PICKS TOON · EP {sid[2:]}', spec["title"]), yt.get("band", "Full review & today's price: acts39.blogspot.com")), encoding="utf-8")
    subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(png)], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(png), "band.svg"], check=True, stdout=subprocess.DEVNULL, env={**os.environ, "ALPHA": "1"})
    cover = ROOT / "shorts" / "thumbs" / f"{sid}-cover.jpg"
    # shots: the cover (or the title card), every panel, the end card
    shots = [("still", cover if cover.exists() else png / "b00.png", None)]
    shots += [("panel", png / f"b{i:02d}.png", d / "toon-art" / f"{sid}-p{i:02d}.jpg") for i in range(1, len(blocks) - 1)]
    shots.append(("panel", png / f"b{len(blocks)-1:02d}.png", None))
    plan = ([{"kind": "hook over the cover", "text": [spec["title"], spec.get("subtitle", "")] + yt["thumb"]["lines"], "speakers": ["narrator"]}]
            + [{"kind": "panel", "text": panel_lines(p), "speakers": panel_speakers(p)} for p in spec["panels"]]
            + [{"kind": "end card", "text": [spec.get("end", ""), "Full guide and sources: link in the description."], "speakers": ["narrator", "vera"]}])
    script = V.write_script(plan, f"YouTube Short (about 60 to 75 seconds) of the comic '{spec['title']}'", d / "narration-short.json", yt.get("words", 160))
    # time every shot to its voice lines
    voiced, dur = [], []
    for k, lines in enumerate(script):
        vs = [(l, *V.synth(l["text"], l["who"])) for l in lines]
        speech = sum(x[2] for x in vs) + 0.12 * max(0, len(vs) - 1)
        board = 0 < k < len(script) - 1 and "art" not in spec["panels"][k - 1]
        dur.append(max(3.6 if board else 1.8, speech + 0.75)); voiced.append(vs)
    starts, x = [], 0.0
    for D in dur: starts.append(x); x += D - XF
    total = x + XF
    clips = []
    for k, ((kind, p, art), D) in enumerate(zip(shots, dur)):
        c = work / f"c{k:02d}.mp4"
        still(p, D, c) if kind == "still" else panel_clip(p, art, D, png / "band.png", c); clips.append(c)
    placed, cues = [], []
    for k, vs in enumerate(voiced):
        t = starts[k] + (0.25 if k else 0.15)
        for l, f, sec in vs: placed.append((t, f)); cues.append((t, t + sec, l["text"])); t += sec + 0.12
    music = work / "music.wav"; mixed = work / "mix.wav"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_music.py"), str(music), str(int(total) + 2), str(yt.get("music_seed", 7))], check=True, stdout=subprocess.DEVNULL)
    V.mix(placed, total, music, mixed)
    ins = []; [ins.extend(["-i", str(c)]) for c in clips]
    chain, last, off = [], "[0:v]", 0.0
    for i in range(1, len(clips)):
        off += dur[i - 1] - XF; chain.append(f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]"); last = f"[x{i}]"
    mp4 = out / f"{sid}.mp4"
    run(FF, "-y", *ins, "-i", mixed, "-filter_complex", ";".join(chain), "-map", last, "-map", f"{len(clips)}:a", "-t", f"{total:.2f}",
        "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "8M", "-bufsize", "12M", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", mp4)
    meta, subs = localize(sid, out, yt["title"], yt["description"], yt.get("tags", []), [c[2] for c in cues], "Short") if translate else ({"en": {"title": yt["title"], "description": yt["description"], "tags": yt.get("tags", [])}}, {"en": [c[2] for c in cues]})
    for lang, lines in subs.items():
        (out / f"{sid}.{lang}.srt").write_text("".join(f"{k+1}\n{srt_time(a)} --> {srt_time(b)}\n{line}\n\n" for k, ((a, b, _), line) in enumerate(zip(cues, lines))), encoding="utf-8")
    if cover.exists(): subprocess.run(["convert", str(cover), "-quality", "90", str(out / f"{sid}-thumb.jpg")], check=True)
    (out / f"{sid}-youtube.json").write_text(json.dumps({"video": mp4.name, "thumbnail": f"{sid}-thumb.jpg", "orientation": "1080x1920", "seconds": round(total, 1),
        "default_language": "en", "made_for_kids": False, "category": "Howto & Style", "altered_content": "No (stylised cartoon, not realistic)",
        "paid_promotion": False, "voices": "Google Gemini TTS (AI voices)", "languages": LANGS, "metadata": meta}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    import shutil; shutil.rmtree(work, ignore_errors=True)
    print(f"{mp4} ({mp4.stat().st_size // 1024} KB, {total:.1f} s, {len(clips)} shots, {len(cues)} voice lines); subtitles: {', '.join(subs)}")

if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], "--no-translate" not in a)
