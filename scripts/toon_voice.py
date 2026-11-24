#!/usr/bin/env python3
"""Voices for the comic videos: a comic, dynamic narration script per shot (written by Gemini from the comic's own text,
checked so it adds no number that is not already on screen) and Gemini TTS with one voice per character.

write_script(shots, context, path, words)  -> [[{"who": ..., "text": ...}, ...] per shot]  (cached in path; edit by hand if needed)
synth(text, who)                          -> (wav path, seconds)   (cached in shorts/voice/)
mix(lines_at, total, music, out_wav)      -> narration placed at its times over the music, music ducked to 0.16
"""
import array, base64, hashlib, json, pathlib, re, subprocess, sys, urllib.request, wave
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import toon_shorts as TS

ROOT = TS.ROOT; FF = TS.FF
TTS_MODEL = "gemini-3.1-flash-tts-preview"   # follows delivery notes without reading them aloud (3.8-flash-tts read them)
VOICES = {   # prebuilt Gemini voices and the delivery each character gets
    "narrator": ("Puck", "a fast-talking, playful sitcom narrator with punchy comic timing"),
    "vera": ("Kore", "a confident, witty TV host, crisp, upbeat and quick"),
    "sam": ("Fenrir", "an excitable young man, quick and expressive, panics comically"),
    "jo": ("Leda", "a warm, determined young woman, lively and natural"),
    "june": ("Sulafat", "a sweet, playful grandmother with a gentle laugh in her voice"),
}
CACHE = ROOT / "shorts" / "voice"
SR = 24000

def _post(model, body):
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", data=json.dumps(body).encode(),
                                 headers={"x-goog-api-key": "proxy-injected", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))

def nums(s): return set(re.findall(r"\d[\d,.]*\d|\d", s.replace(",", "")))

def write_script(shots, context, path, words, extra=""):
    """shots: [{"kind": ..., "text": [...], "speakers": [...]}]. Returns one list of lines per shot."""
    path = pathlib.Path(path)
    if path.exists():
        s = json.loads(path.read_text(encoding="utf-8"))
        if len(s) == len(shots): return s
    allowed = set().union(*[nums(" ".join(x["text"])) for x in shots])
    prompt = (f"You write the voice-over for a {context}. Make it comic, dynamic and warm, like a great animated sitcom: punchy, playful, quick beats, "
              f"jokes from the situation, never mean. Total under {words} words. For each shot write 0 to 3 lines; each line has a speaker "
              f"(narrator, vera, sam, jo, june; use a character only if that character is in the shot's speakers) and the words to say. "
              f"Characters may say their balloon lines, tightened or punched up, but keep their meaning. The narrator links the scenes. "
              f"HARD RULES: add no new facts; every number, price, date, model name and source must be one that appears in the shot texts, "
              f"written the same way; keep source names when a number is said (say 'says CNET'); no Amazon ratings or prices; do not say the characters "
              f"used or tested a product. The last shot ends by sending viewers to the full guide in the description. "
              f"Return JSON: {{\"shots\": [[{{\"who\": str, \"text\": str}}, ...], ...]}} with exactly {len(shots)} entries in order.\n\n"
              + json.dumps([{"shot": i, "kind": x["kind"], "speakers": x["speakers"], "texts": x["text"]} for i, x in enumerate(shots)], ensure_ascii=False))
    for attempt in range(3):
        r = _post("gemini-3.1-pro-preview", {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}})
        txt = "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"] if not p.get("thought"))
        s = json.loads(re.sub(r"^```(json)?|```$", "", txt.strip(), flags=re.M))["shots"]
        extra = [n for sh in s for l in sh for n in nums(l["text"]) if n not in allowed]
        bad_who = [l["who"] for sh in s for l in sh if l["who"] not in VOICES]
        if len(s) == len(shots) and not extra and not bad_who:
            path.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"); return s
        print(f"  script retry {attempt + 1}: shots {len(s)}/{len(shots)}, new numbers {extra[:5]}, speakers {bad_who[:3]}")
    raise SystemExit("could not write a narration script that keeps to the facts")

def synth(text, who):
    voice, style = VOICES.get(who, VOICES["narrator"])
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"v3|{TTS_MODEL}|{voice}|{style}|{text}".encode()).hexdigest()[:16]
    f = CACHE / f"{key}.wav"
    if not f.exists():
        r = _post(TTS_MODEL, {"contents": [{"parts": [{"text": f"Say this as {style}, fast and punchy: {text}"}]}],
                              "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}})
        part = r["candidates"][0]["content"]["parts"][0]["inlineData"]; raw = base64.b64decode(part["data"])
        tmp = f.with_suffix(".in.wav")
        if raw[:4] == b"RIFF": tmp.write_bytes(raw)
        else:
            with wave.open(str(tmp), "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(raw)
        # trim leading/trailing silence, a touch faster, 24 kHz mono
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(tmp), "-af",
                        "silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.2:stop_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,atempo=1.1",
                        "-ar", str(SR), "-ac", "1", str(f)], check=True)
        tmp.unlink()
        with wave.open(str(f)) as w: sec = w.getnframes() / w.getframerate()
        if sec > 1.5 + 0.55 * len(text.split()):     # far too long for the words: the delivery note was probably read aloud
            print(f"  voice line too long ({sec:.1f} s for {len(text.split())} words), retrying without the delivery note")
            f.unlink(); r = _post(TTS_MODEL, {"contents": [{"parts": [{"text": text}]}], "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}})
            raw = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            with wave.open(str(tmp), "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(raw)
            subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(tmp), "-af", "silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.2:stop_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,atempo=1.1", "-ar", str(SR), "-ac", "1", str(f)], check=True)
            tmp.unlink()
    with wave.open(str(f)) as w: return f, w.getnframes() / w.getframerate()

def mix(placed, total, music, out_wav):
    """placed: [(start seconds, wav path)]. Writes a stereo-ready mono WAV: narration over the music at 0.16."""
    buf = array.array("h", [0]) * int((total + 1) * SR)
    for t0, f in placed:
        with wave.open(str(f)) as w: a = array.array("h", w.readframes(w.getnframes()))
        o = int(t0 * SR)
        for i, v in enumerate(a[: len(buf) - o]): buf[o + i] = max(-32768, min(32767, buf[o + i] + v))
    voice = pathlib.Path(out_wav).with_suffix(".voice.wav")
    with wave.open(str(voice), "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(buf.tobytes())
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(voice), "-i", str(music), "-filter_complex",
                    f"[1:a]aresample={SR},volume=0.16,afade=t=out:st={max(0, total-2):.2f}:d=2[m];[0:a]volume=1.35[v];[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
                    "-map", "[a]", "-t", f"{total:.2f}", str(out_wav)], check=True)
    voice.unlink()
