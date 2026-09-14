"""Royalty-free background music, synthesised from scratch (no samples): a gentle plucked-string
loop with a soft pad, written as a 16-bit WAV. Pure Python, no numpy.
Usage: python3 scripts/make_music.py out.wav [seconds=12] [seed=7]
"""
import math, random, struct, sys, wave

SR = 22050

def pluck(freq, seconds, decay=0.996, brightness=0.5, seed=0):
    """Karplus–Strong plucked string."""
    n = int(SR * seconds); p = max(2, int(SR / freq)); rnd = random.Random(seed)
    buf = [rnd.uniform(-1, 1) for _ in range(p)]
    out = []; i = 0
    while len(out) < n:
        nxt = decay * (brightness * buf[i] + (1 - brightness) * buf[(i + 1) % p])
        out.append(buf[i]); buf[i] = nxt; i = (i + 1) % p
    return out

def pad(freq, seconds, amp=0.12):
    n = int(SR * seconds); out = []
    for t in range(n):
        x = t / SR
        env = min(1.0, x / 0.4) * min(1.0, (seconds - x) / 0.6)
        v = (math.sin(2 * math.pi * freq * x) + 0.5 * math.sin(2 * math.pi * freq * 2 * x + 0.3) + 0.25 * math.sin(2 * math.pi * freq * 3 * x)) / 1.75
        out.append(amp * env * v)
    return out

NOTE = {n: 440.0 * 2 ** ((i - 9) / 12) for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}
def f(name, octave): return NOTE[name] * 2 ** (octave - 4)

def main(out, seconds=12.0, seed=7):
    rnd = random.Random(seed)
    bpm = 96; beat = 60 / bpm
    # C major pentatonic melody over a I–V–vi–IV pad, ukulele-ish register
    scale = [("C", 5), ("D", 5), ("E", 5), ("G", 5), ("A", 5), ("C", 6)]
    chords = [[("C", 4), ("E", 4), ("G", 4)], [("G", 3), ("B", 3), ("D", 4)], [("A", 3), ("C", 4), ("E", 4)], [("F", 3), ("A", 3), ("C", 4)]]
    total = int(SR * seconds); mix = [0.0] * total
    def add(sig, start, gain):
        s = int(start * SR)
        for k, v in enumerate(sig):
            j = s + k
            if j >= total: break
            mix[j] += gain * v
    # pad: one chord per bar (4 beats)
    bar = 4 * beat; t = 0.0; ci = 0
    while t < seconds:
        for (n, o) in chords[ci % 4]: add(pad(f(n, o), bar + 0.2), t, 0.9)
        ci += 1; t += bar
    # melody: eighth notes with rests, mostly stepwise
    t = 0.0; idx = 2; seed_i = seed
    while t < seconds - 0.5:
        if rnd.random() < 0.78:
            idx = max(0, min(len(scale) - 1, idx + rnd.choice([-1, -1, 0, 1, 1, 2])))
            n, o = scale[idx]; dur = beat / 2 * rnd.choice([1, 1, 2])
            add(pluck(f(n, o), min(1.6, dur + 0.9), seed=seed_i), t, 0.55); seed_i += 1
            t += dur
        else:
            t += beat / 2
    # bass pluck on beats 1 and 3
    t = 0.0; ci = 0
    while t < seconds:
        root = chords[ci % 4][0]; add(pluck(f(root[0], root[1] - 1), 1.2, decay=0.998, seed=99 + ci), t, 0.35)
        add(pluck(f(root[0], root[1] - 1), 1.0, decay=0.998, seed=199 + ci), t + 2 * beat, 0.25)
        ci += 1; t += bar
    # fade in/out and normalise
    peak = max(1e-6, max(abs(v) for v in mix)); fade = int(SR * 0.8)
    data = bytearray()
    for i, v in enumerate(mix):
        g = min(1.0, i / fade, (total - i) / fade)
        data += struct.pack("<h", int(max(-1, min(1, v / peak * 0.8 * g)) * 32767))
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(bytes(data))
    print(f"wrote {out}: {seconds}s at {SR} Hz, seed {seed}")

if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 12.0, int(sys.argv[3]) if len(sys.argv) > 3 else 7)
