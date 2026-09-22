"""Synthesise the narration for the yadam video, one subtitle line at a time, with timing.

Voice: sherpa-onnx running the mimic3 `ko_KO/kss_low` VITS model (offline, Korean).
Model dir: $YADAM_TTS_MODEL or the first `vits-mimic3-ko_KO-kss_low` found under /tmp/claude-0/*/scratchpad/tts.
Get it with:  curl -L -o m.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-mimic3-ko_KO-kss_low.tar.bz2 && tar xjf m.tar.bz2

Usage: python3 scripts/yadam_tts.py video/2026-09-yadam-manbok [--speed 0.76] [--pause 0.6]
Reads build/script.json, writes build/tts/<hash>.wav (cache), build/narration.wav (22.05 kHz mono)
and build/timing.json: every line with start/end seconds, plus scene/chapter boundaries.
"""
import argparse, hashlib, json, os, pathlib, re, sys
import numpy as np, soundfile as sf

SR = 22050
PAUSE_SENT, PAUSE_PARA, PAUSE_SPEAKER, PAUSE_SCENE = 0.55, 0.85, 0.65, 1.4
CARD_CHAPTER, CARD_TITLE, LEAD_IN = 5.0, 7.0, 0.8   # seconds of silence for chapter/title cards, and before the first line of a scene


def find_model():
    if os.environ.get('YADAM_TTS_MODEL'):
        return pathlib.Path(os.environ['YADAM_TTS_MODEL'])
    for p in pathlib.Path('/tmp').glob('claude-0/*/*/scratchpad/tts/vits-mimic3-ko_KO-kss_low'):
        return p
    sys.exit('TTS model not found; set YADAM_TTS_MODEL')


def clean_for_tts(text):
    t = text.replace('“', '').replace('”', '').replace('"', '').replace("'", '')
    t = re.sub(r'[!?]', '.', t)
    t = t.replace('…', '.').replace('...', '.')
    t = re.sub(r'\s+', ' ', t).strip()
    if not t.endswith('.'):
        t += '.'
    return t


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--speed', type=float, default=0.76)
    ap.add_argument('--pause', type=float, default=PAUSE_SENT); a = ap.parse_args()
    root = pathlib.Path(a.root); build = root / 'build'; cache = build / 'tts'; cache.mkdir(parents=True, exist_ok=True)
    data = json.loads((build / 'script.json').read_text(encoding='utf-8'))
    import sherpa_onnx
    d = find_model()
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=str(d / 'ko_KO-kss_low.onnx'), tokens=str(d / 'tokens.txt'), data_dir=str(d / 'espeak-ng-data'),
                                                   noise_scale=0.667, noise_scale_w=0.8, length_scale=1.0), num_threads=4, provider='cpu'), max_num_sentences=1)
    tts = sherpa_onnx.OfflineTts(cfg)

    def synth(text):
        key = hashlib.sha1(f"{a.speed}|{text}".encode()).hexdigest()[:16]
        f = cache / f'{key}.wav'
        if f.exists():
            x, _ = sf.read(f, dtype='float32'); return x
        g = tts.generate(clean_for_tts(text), sid=0, speed=a.speed)
        x = np.asarray(g.samples, dtype=np.float32)
        # trim leading/trailing near-silence so pauses are ours, not the model's
        nz = np.where(np.abs(x) > 0.01)[0]
        if len(nz):
            x = x[max(0, nz[0] - int(0.05 * SR)): min(len(x), nz[-1] + int(0.12 * SR))]
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
            for i, ln in enumerate(sc['lines']):
                if i and ln['speaker'] != prev_speaker:
                    silence(PAUSE_SPEAKER)
                x = synth(ln['text']); s0 = t
                chunks.append(x); t += len(x) / SR
                # subtitle chunks share the sentence's time span proportionally to their length
                subs, total, cur = [], sum(len(c) for c in ln['subs']), s0
                for c in ln['subs']:
                    e = cur + (t - s0) * len(c) / total
                    subs.append({"text": c, "start": round(cur, 3), "end": round(e, 3)}); cur = e
                sj['lines'].append({"text": ln['text'], "speaker": ln['speaker'], "start": round(s0, 3), "end": round(t, 3), "subs": subs})
                silence(PAUSE_PARA if ln['para_end'] else a.pause)
                prev_speaker = ln['speaker']
            silence(PAUSE_SCENE)
            sj['end'] = t; cj['scenes'].append(sj)
            print(f"  ch{ch['n']} scene {len(cj['scenes'])}: {sj['end']-sj['start']:.1f}s", flush=True)
        cj['end'] = t; timing['chapters'].append(cj)
        print(f"chapter {ch['n']} {ch['title']}: ends at {t/60:.1f} min", flush=True)
    audio = np.concatenate(chunks)
    sf.write(build / 'narration.wav', audio, SR)
    timing['total'] = t
    (build / 'timing.json').write_text(json.dumps(timing, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"narration: {t/60:.2f} min, peak {np.abs(audio).max():.3f}")


if __name__ == '__main__':
    main()
