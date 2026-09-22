"""Synthesise the narration for the yadam video, one subtitle line at a time, with timing.

Voices: sherpa-onnx. Default engine `supertonic` = Supertonic 3 (int8, 31 languages incl. Korean, 10 built-in voices:
sid 0-4 female, 5 young male, 6-9 male), cast per character below. Fallback engine `mimic3` = the single-voice
`ko_KO/kss_low` VITS model bent into a cast by pitch shifting.
Supertonic model: $YADAM_ST3_MODEL or sherpa-onnx-supertonic-3-tts-int8-2026-05-11 under /tmp/claude-0/*/scratchpad/tts, from
  https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2
Model dir: $YADAM_TTS_MODEL or the first `vits-mimic3-ko_KO-kss_low` found under /tmp/claude-0/*/scratchpad/tts.
Get it with:  curl -L -o m.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-mimic3-ko_KO-kss_low.tar.bz2 && tar xjf m.tar.bz2

Usage: python3 scripts/yadam_tts.py video/2026-09-yadam-manbok [--speed 0.76] [--pause 0.6]
Reads build/script.json, writes build/tts/<hash>.wav (cache), build/narration.wav (22.05 kHz mono)
and build/timing.json: every line with start/end seconds, plus scene/chapter boundaries.
"""
import argparse, hashlib, json, os, pathlib, re, sys
import numpy as np, soundfile as sf

SR = 22050
PAUSE_SENT, PAUSE_PARA, PAUSE_SPEAKER, PAUSE_SCENE = 0.38, 0.68, 0.55, 1.2
FADE = 0.025   # raised-cosine fade at both ends of every clip (no clicks, no abrupt onsets)
CARD_CHAPTER, CARD_TITLE, LEAD_IN = 5.0, 7.0, 0.8   # seconds of silence for chapter/title cards, and before the first line of a scene


# ---- expressive delivery -------------------------------------------------------------------------------
# One VITS voice is bent into a cast: pitch (resampling factor, <1 = lower and darker), base speed and gain.
# The synth runs faster by 1/pitch so the resampled clip lands on the intended duration.
PROFILES = {
    None:            dict(pitch=1.00, speed=0.90, gain=0.0, expr=False),   # narrator: calm, unhurried
    "manbok":        dict(pitch=0.90, speed=0.95, gain=0.5, expr=True),
    "sunok":         dict(pitch=1.00, speed=0.90, gain=-0.5, expr=True),
    "dolsoe":        dict(pitch=1.14, speed=1.00, gain=0.0, expr=True),
    "mother":        dict(pitch=0.95, speed=0.82, gain=-1.0, expr=True),
    "kim_jinsa":     dict(pitch=0.84, speed=0.88, gain=0.5, expr=True),
    "yongchil":      dict(pitch=0.88, speed=1.00, gain=1.0, expr=True),
    "eosa_ragged":   dict(pitch=0.83, speed=0.88, gain=0.0, expr=True),
    "eosa_official": dict(pitch=0.82, speed=0.86, gain=1.5, expr=True),
    "satto":         dict(pitch=0.86, speed=0.92, gain=1.0, expr=True),
    "villager_m":    dict(pitch=0.90, speed=0.95, gain=0.0, expr=True),
    "villager_f":    dict(pitch=1.02, speed=0.95, gain=0.0, expr=True),
    "merchant":      dict(pitch=0.90, speed=0.95, gain=0.0, expr=True),
    "grandpa_modern": dict(pitch=0.85, speed=0.85, gain=0.0, expr=True),
    "girl_modern":   dict(pitch=1.16, speed=1.00, gain=0.0, expr=True),
}
# Supertonic 3 cast: sid, pitch (resample factor), base speed, gain dB
CAST = {
    None:             dict(sid=8, pitch=1.00, speed=0.92, gain=0.0),   # narrator: mid-low male, calm
    "manbok":         dict(sid=5, pitch=1.00, speed=0.97, gain=0.5),   # young, warm
    "sunok":          dict(sid=0, pitch=1.00, speed=0.93, gain=0.0),
    "dolsoe":         dict(sid=1, pitch=1.08, speed=1.02, gain=0.0),   # child: brightest female voice, raised
    "mother":         dict(sid=4, pitch=0.97, speed=0.85, gain=-0.5),  # elderly: lowest female, slow
    "kim_jinsa":      dict(sid=9, pitch=0.98, speed=0.88, gain=0.5),   # deep, stately
    "yongchil":       dict(sid=7, pitch=1.03, speed=1.02, gain=1.0),   # sly, quick
    "eosa_ragged":    dict(sid=6, pitch=1.00, speed=0.90, gain=0.0),
    "eosa_official":  dict(sid=6, pitch=0.98, speed=0.88, gain=1.5),   # authority
    "satto":          dict(sid=9, pitch=1.04, speed=0.96, gain=1.0),
    "villager_m":     dict(sid=8, pitch=1.06, speed=1.00, gain=0.0),
    "villager_f":     dict(sid=2, pitch=1.00, speed=1.00, gain=0.0),
    "merchant":       dict(sid=7, pitch=0.97, speed=0.98, gain=0.0),
    "grandpa_modern": dict(sid=6, pitch=1.00, speed=0.86, gain=0.0),
    "girl_modern":    dict(sid=3, pitch=1.08, speed=1.02, gain=0.0),
}
SAD = ("울", "눈물", "떠났", "죽", "무릎", "죄송", "슬", "한숨", "차가", "얼음")
HOOK_START = ("여러분", "과연", "그런데", "하지만")


def delivery(text, speaker, is_chapter_end, engine="supertonic"):
    """-> (speed, pitch, gain_db, expressive, pause_after_extra, sid)"""
    table = CAST if engine == "supertonic" else PROFILES
    pr = table.get(speaker, table[None])
    speed, pitch, gain, expr, extra = pr["speed"], pr["pitch"], pr["gain"], pr.get("expr", True), 0.0
    if "!" in text:                       # shouts and exclamations: louder, livelier, a touch quicker
        gain += 2.0; speed *= 1.04; expr = True
    if "출두야" in text:                   # the big reveal
        gain += 1.5; speed *= 0.9; extra += 0.8
    if any(w in text for w in SAD):       # sorrow: slower, softer
        speed *= 0.93; gain -= 1.0
    if text.startswith(HOOK_START) or text.rstrip("?.!").endswith("까요") or "그때였습니다" in text:
        speed *= 0.92; extra += 0.9      # hooks and cliffhangers: slow down, then hold the silence
    if text.endswith("?"):
        speed *= 0.96
    if is_chapter_end:
        speed *= 0.94; extra += 0.6
    return speed, pitch, gain, expr, extra, pr.get("sid", 0)


def pitch_shift(x, p):
    """Resample by factor p (p<1 -> lower, longer). Linear interpolation is fine for +-16 %."""
    if abs(p - 1.0) < 1e-3:
        return x
    pos = np.arange(0, len(x) - 1, p, dtype=np.float64)
    return np.interp(pos, np.arange(len(x)), x).astype(np.float32)


def find_st3():
    if os.environ.get('YADAM_ST3_MODEL'):
        return pathlib.Path(os.environ['YADAM_ST3_MODEL'])
    for p in pathlib.Path('/tmp').glob('claude-0/*/*/scratchpad/tts/sherpa-onnx-supertonic-3-tts-int8-2026-05-11'):
        return p
    sys.exit('Supertonic 3 model not found; set YADAM_ST3_MODEL')


def find_model():
    if os.environ.get('YADAM_TTS_MODEL'):
        return pathlib.Path(os.environ['YADAM_TTS_MODEL'])
    for p in pathlib.Path('/tmp').glob('claude-0/*/*/scratchpad/tts/vits-mimic3-ko_KO-kss_low'):
        return p
    sys.exit('TTS model not found; set YADAM_TTS_MODEL')


def clean_for_tts(text, engine="supertonic"):
    t = text.replace('“', '').replace('”', '').replace('"', '').replace("'", '')
    if engine != "supertonic":
        t = re.sub(r'[!?]', '.', t)
    t = t.replace('…', '.').replace('...', '.')
    t = re.sub(r'\s+', ' ', t).strip()
    if not t.endswith('.'):
        t += '.'
    return t


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--speed', type=float, default=0.9)
    ap.add_argument('--noise', type=float, default=0.55); ap.add_argument('--noise-w', type=float, default=0.65)
    ap.add_argument('--engine', default='supertonic', choices=['supertonic', 'mimic3'])
    ap.add_argument('--pause', type=float, default=PAUSE_SENT); a = ap.parse_args()
    root = pathlib.Path(a.root); build = root / 'build'; cache = build / 'tts'; cache.mkdir(parents=True, exist_ok=True)
    data = json.loads((build / 'script.json').read_text(encoding='utf-8'))
    import sherpa_onnx
    if a.engine == "supertonic":
        d = find_st3()
        cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(supertonic=sherpa_onnx.OfflineTtsSupertonicModelConfig(
            duration_predictor=str(d / 'duration_predictor.int8.onnx'), text_encoder=str(d / 'text_encoder.int8.onnx'),
            vector_estimator=str(d / 'vector_estimator.int8.onnx'), vocoder=str(d / 'vocoder.int8.onnx'), tts_json=str(d / 'tts.json'),
            unicode_indexer=str(d / 'unicode_indexer.bin'), voice_style=str(d / 'voice.bin')), num_threads=4, provider='cpu'), max_num_sentences=1)
        tts_calm = tts_expr = sherpa_onnx.OfflineTts(cfg)
    else:
        d = find_model()
        def make(noise, noise_w):
            cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=str(d / 'ko_KO-kss_low.onnx'), tokens=str(d / 'tokens.txt'), data_dir=str(d / 'espeak-ng-data'),
                                                           noise_scale=noise, noise_scale_w=noise_w, length_scale=1.0), num_threads=4, provider='cpu'), max_num_sentences=1)
            return sherpa_onnx.OfflineTts(cfg)
        tts_calm, tts_expr = make(a.noise, a.noise_w), make(0.78, 0.72)
    global SR
    SR = tts_calm.sample_rate

    def synth(text, speed=None, pitch=1.0, gain=0.0, expr=False, sid=0):
        speed = (speed or a.speed) * a.speed / 0.9   # --speed scales every profile (0.9 = profiles as written)
        key = hashlib.sha1(f"{a.engine}|{sid}|{speed:.3f}|{pitch:.3f}|{gain:.2f}|{int(expr)}|{a.noise}|{a.noise_w}|v4|{text}".encode()).hexdigest()[:16]
        f = cache / f'{key}.wav'
        if f.exists():
            x, _ = sf.read(f, dtype='float32'); return x
        g = (tts_expr if expr else tts_calm).generate(clean_for_tts(text, a.engine), sid=sid, speed=speed / pitch)
        x = pitch_shift(np.asarray(g.samples, dtype=np.float32), pitch) * (10 ** (gain / 20))
        # trim only real silence (low threshold, generous padding) so soft onsets and tails survive,
        # then fade both ends so clips join the pauses without clicks
        nz = np.where(np.abs(x) > 0.003)[0]
        if len(nz):
            x = x[max(0, nz[0] - int(0.06 * SR)): min(len(x), nz[-1] + int(0.16 * SR))]
        n = min(int(FADE * SR), len(x) // 4)
        if n > 0:
            w = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, n, dtype=np.float32))
            x[:n] *= w; x[-n:] *= w[::-1]
        sf.write(f, x, SR); return x

    chunks, t, timing = [], 0.0, {"sr": SR, "chapters": []}
    def silence(sec):
        nonlocal t
        chunks.append(np.zeros(int(sec * SR), np.float32)); t += sec

    for ch in data['chapters']:
        cj = {"n": ch['n'], "title": ch['title'], "start": t, "scenes": []}
        if ch['n'] > 0:
            cj['card'] = [t, t + CARD_CHAPTER]; silence(CARD_CHAPTER)
        for sc in ch['scenes']:
            sj = {k: v for k, v in sc.items() if k != 'lines'}; sj['start'] = t; sj['lines'] = []
            if sc['kind'] == 'title':
                sj['card'] = [t, t + CARD_TITLE]; silence(CARD_TITLE)
            silence(LEAD_IN)
            prev_speaker = None
            last_scene = sc is ch['scenes'][-1]
            for i, ln in enumerate(sc['lines']):
                if i and ln['speaker'] != prev_speaker:
                    silence(PAUSE_SPEAKER)
                chapter_end = last_scene and i >= len(sc['lines']) - 2
                speed, pitch, gain, expr, extra, sid = delivery(ln['text'], ln['speaker'], chapter_end, a.engine)
                x = synth(ln['text'], speed, pitch, gain, expr, sid); s0 = t
                chunks.append(x); t += len(x) / SR
                # subtitle chunks share the sentence's time span proportionally to their length
                subs, total, cur = [], sum(len(c) for c in ln['subs']), s0
                for c in ln['subs']:
                    e = cur + (t - s0) * len(c) / total
                    subs.append({"text": c, "start": round(cur, 3), "end": round(e, 3)}); cur = e
                sj['lines'].append({"text": ln['text'], "speaker": ln['speaker'], "start": round(s0, 3), "end": round(t, 3), "subs": subs})
                silence((PAUSE_PARA if ln['para_end'] else a.pause) + extra)
                prev_speaker = ln['speaker']
            silence(PAUSE_SCENE)
            sj['end'] = t; cj['scenes'].append(sj)
            print(f"  ch{ch['n']} scene {len(cj['scenes'])}: {sj['end']-sj['start']:.1f}s", flush=True)
        cj['end'] = t; timing['chapters'].append(cj)
        print(f"chapter {ch['n']} {ch['title']}: ends at {t/60:.1f} min", flush=True)
    audio = np.concatenate(chunks)
    rms = float(np.sqrt((audio[np.abs(audio) > 0.002] ** 2).mean()))   # speech-only RMS
    audio = np.clip(audio * (10 ** (-18 / 20) / rms), -0.98, 0.98).astype(np.float32)
    sf.write(build / 'narration.wav', audio, SR)
    timing['total'] = t
    (build / 'timing.json').write_text(json.dumps(timing, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"narration: {t/60:.2f} min, peak {np.abs(audio).max():.3f}")


if __name__ == '__main__':
    main()
