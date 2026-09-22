#!/usr/bin/env python3
"""Royalty-free, fully synthesised music beds, stings and ambiences for the 1-hour
야담 (Korean folk-tale) animated video for senior viewers.

Everything is generated from scratch with numpy - no samples.  Instruments:
  * gayageum/geomungo-like plucked strings: Karplus-Strong (vectorised per period,
    extending scripts/make_music.py) resampled through a time-varying pitch curve so
    notes can carry 농현 vibrato, 추성 (bend-in) and 퇴성 (bend-down) ornaments.
  * soft sine drones whose partials complete an integer number of cycles per loop.
  * 장구-like thump (sine pitch-drop + filtered noise) and a light rim tick.
  * 징-like gong: inharmonic beating partials with a slow swell.
  * ambiences from FFT-filtered noise with slow random modulation, FM bird chirps,
    amplitude-modulated cricket pulses, drips, clinks, etc.

Output: 44.1 kHz, 16-bit, mono WAV.  Deterministic (fixed seeds).
Music loops are rendered cyclically (note tails wrap around the loop point, drones are
loop-periodic); ambience loops are rendered 3 s long and the ends equal-power crossfaded.

Usage:
    python3 scripts/yadam_music.py <out_dir> [--only name1,name2]

Regenerate the whole set (takes well under 2 minutes):
    python3 scripts/yadam_music.py video/2026-09-yadam-manbok/build/audio
"""
import math
import os
import sys
import time

import numpy as np
import soundfile as sf

SR = 44100
TAU = 2.0 * math.pi

# ----------------------------------------------------------------------------- basics
_NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def note(name):
    """'Eb4' -> Hz (A4 = 440)."""
    n = _NAMES[name[0]]
    i = 1
    while name[i] in "#b":
        n += 1 if name[i] == "#" else -1
        i += 1
    return 440.0 * 2 ** ((12 * (int(name[i:]) + 1) + n - 69) / 12)


def rng(seed):
    return np.random.default_rng(seed)


def tvec(n):
    return np.arange(n) / SR


def white(n, seed):
    return rng(seed).uniform(-1.0, 1.0, n)


def fftfilt(x, lo=None, hi=None, order=2, tilt=0.0):
    """Zero-phase Butterworth-magnitude filter via FFT (circular, so loop-safe).
    lo/hi = high-pass / low-pass corner in Hz; tilt in dB/octave around 1 kHz.
    Always removes DC."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1.0 / SR)
    fs = np.maximum(f, 1e-3)
    g = np.ones_like(f)
    if lo:
        g *= 1.0 / np.sqrt(1.0 + (lo / fs) ** (2 * order))
    if hi:
        g *= 1.0 / np.sqrt(1.0 + (fs / hi) ** (2 * order))
    if tilt:
        g *= (np.maximum(fs, 20.0) / 1000.0) ** (tilt / 6.0206)
    g[0] = 0.0
    return np.fft.irfft(X * g, n)


def lp_noise(n, fc, seed):
    """Smooth Gaussian random modulation curve (white noise low-passed at fc Hz), unit std."""
    y = fftfilt(rng(seed).standard_normal(n), hi=fc, order=4)
    return y / (y.std() + 1e-12)


def cyc_random(n, seconds, kmax, seed):
    """Smooth random curve in [-1, 1] that is exactly periodic over `seconds` (loop-safe LFO)."""
    r = rng(seed)
    t = tvec(n)
    y = np.zeros(n)
    for k in range(1, kmax + 1):
        y += np.sin(TAU * k * t / seconds + r.uniform(0, TAU)) / k
    return y / (np.max(np.abs(y)) + 1e-12)


def smooth01(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-12)


# ------------------------------------------------------------------ plucked strings
def ks_raw(p, n, decay, bright, seed, exc_lp=2, pick=0.22):
    """Karplus-Strong string with integer period p, computed one period per numpy step.
    decay: gain per period; bright: 2-tap loop filter weight (1 = no damping)."""
    buf = rng(seed).uniform(-1.0, 1.0, p)
    for _ in range(exc_lp):                      # warmer (silk-string) excitation
        buf = 0.5 * (buf + np.roll(buf, 1))
    d = max(1, int(round(p * pick)))             # pick-position comb
    buf = buf - np.roll(buf, d)
    buf /= np.max(np.abs(buf)) + 1e-12
    nper = n // p + 2
    out = np.empty(nper * p)
    nxt = np.empty(p)
    b, c = bright, 1.0 - bright
    for k in range(nper):
        out[k * p:(k + 1) * p] = buf
        nxt[:-1] = b * buf[:-1] + c * buf[1:]
        nxt[-1] = b * buf[-1] + c * nxt[0]
        nxt *= decay
        buf, nxt = nxt, buf
    return out[:n]


def pluck(freq, dur, t60=4.0, bright=0.55, seed=0, exc_lp=2, pick=0.22,
          cents=None, trem=None, amp=1.0):
    """Plucked string at exact `freq`, with optional pitch curve (cents(t)) and tremolo."""
    n = int(dur * SR)
    p = max(2, int(round(SR / freq)))
    f0 = SR / (p - (1.0 - bright))               # measured effective pitch of the block KS loop
    t = tvec(n)
    c = cents(t) if cents is not None else np.zeros(n)
    rate = (freq / f0) * 2.0 ** (c / 1200.0)
    pos = np.cumsum(rate) - rate[0]
    n_src = int(pos[-1]) + 3
    decay = 10.0 ** (-3.0 / (t60 * f0))
    src = ks_raw(p, n_src, decay, bright, seed, exc_lp, pick)
    y = np.interp(pos, np.arange(n_src), src)
    if trem is not None:
        y *= trem(t)
    nf = min(n, int(0.05 * SR))
    y[-nf:] *= np.linspace(1.0, 0.0, nf)
    return amp * y


# pitch-curve / tremolo factories (all take a time vector, return an array)
def vib(depth=40.0, rate=4.0, delay=0.35, ramp=0.6, phase=0.0):
    return lambda t: depth * smooth01((t - delay) / ramp) * np.sin(TAU * rate * t + phase)


def bend_in(cents=-90.0, dur=0.15):
    return lambda t: cents * (1.0 - smooth01(t / dur))


def bend_down(cents=-70.0, start=0.5, dur=0.6):
    return lambda t: cents * smooth01((t - start) / dur)


def combine(*fns):
    return lambda t: sum(f(t) for f in fns)


def tremolo(rate=4.5, depth=0.4, delay=0.4, ramp=0.5):
    return lambda t: 1.0 - depth * smooth01((t - delay) / ramp) * 0.5 * (1.0 - np.cos(TAU * rate * t))


# ------------------------------------------------------------ percussion / gong / pad
def thump(seed, heavy=False):
    """장구 궁편-like low thump: sine pitch-drop plus a short low-passed noise burst."""
    n = int((0.55 if heavy else 0.4) * SR)
    t = tvec(n)
    f = (44.0 if heavy else 52.0) + (70.0 if heavy else 60.0) * np.exp(-t / 0.035)
    body = np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t / (0.17 if heavy else 0.11))
    nz = white(n, seed) * np.exp(-t / 0.012)
    nz = np.convolve(nz, np.ones(10) / 10.0, mode="same")
    return norm(body + 0.3 * nz)


def tick(seed):
    """Light 채편-like rim tick."""
    n = int(0.08 * SR)
    t = tvec(n)
    nz = white(n, seed)
    nz = nz - np.roll(nz, 1)
    y = nz * np.exp(-t / 0.006) + 0.6 * np.sin(TAU * 720.0 * t) * np.exp(-t / 0.02)
    return norm(y)


def gong(f0, dur, swell=1.5, t60=7.0, seed=0, small=False):
    """징-like gong: inharmonic beating partials, slow swell, soft saturation."""
    n = int(dur * SR)
    t = tvec(n)
    r = rng(seed)
    if small:
        ratios, amps = [1.0, 1.42, 2.1, 2.9, 3.7], [1.0, 0.45, 0.3, 0.18, 0.1]
    else:
        ratios, amps = [1.0, 1.51, 2.04, 2.66, 3.35, 4.12, 5.3], [1.0, 0.55, 0.38, 0.25, 0.16, 0.1, 0.06]
    y = np.zeros(n)
    for i, (rt, a) in enumerate(zip(ratios, amps)):
        f = f0 * rt * (1.0 + r.uniform(-0.004, 0.004))
        beat = r.uniform(0.15, 1.2)
        dec = np.exp(-t * 6.91 / (t60 / (1.0 + 0.6 * i)))
        y += 0.5 * a * dec * (np.sin(TAU * (f + beat / 2) * t + r.uniform(0, TAU))
                              + np.sin(TAU * (f - beat / 2) * t + r.uniform(0, TAU)))
    att = np.sin(0.5 * np.pi * np.clip(t / swell, 0.0, 1.0)) ** 2
    y *= att * (1.0 + 0.12 * np.sin(TAU * 0.8 * t + 1.0))
    y = np.tanh(1.3 * norm(y)) / math.tanh(1.3)
    nf = min(n, int(0.1 * SR))
    y[-nf:] *= np.linspace(1.0, 0.0, nf)
    return norm(y)


def drone(parts, seconds, seed, mod=0.25):
    """Loop-exact warm drone: every partial completes an integer number of cycles in `seconds`."""
    n = int(seconds * SR)
    t = tvec(n)
    r = rng(seed)
    y = np.zeros(n)

    def q(f):
        return round(f * seconds) / seconds

    for f, a in parts:
        for det in (-0.13, 0.13):                 # gentle beating pair
            for h, ha in ((1, 1.0), (2, 0.3), (3, 0.1)):
                y += a * ha * np.sin(TAU * q((f + det) * h) * t + r.uniform(0, TAU))
    y *= 1.0 + mod * cyc_random(n, seconds, 3, seed + 1)
    return norm(y)


def pad_swell(freqs, dur, attack=1.0, tau=3.0):
    """Non-looping soft pad for stings: slow attack, exponential decay."""
    n = int(dur * SR)
    t = tvec(n)
    y = np.zeros(n)
    for i, f in enumerate(freqs):
        for det in (-0.4, 0.4):
            y += np.sin(TAU * (f + det) * t + 0.7 * i) + 0.3 * np.sin(TAU * 2 * (f + det) * t + i)
    env = np.sin(0.5 * np.pi * np.clip(t / attack, 0, 1)) ** 2 * np.exp(-np.maximum(t - attack, 0) / tau)
    return norm(y * env)


# ------------------------------------------------------------------------- mixer
class Mix:
    """Float mix buffer. With loop=True, events wrap around modulo the loop length."""

    def __init__(self, seconds, loop, guard=0.3):
        self.seconds = seconds
        self.L = int(round(seconds * SR))
        self.buf = np.zeros(self.L)
        self.loop = loop
        self.guard = guard

    def place(self, sig, t, gain=1.0):
        L = self.L
        s = int(round(t * SR))
        sig = sig[:L]
        n = len(sig)
        if self.loop:
            s %= L
            if s + n <= L:
                self.buf[s:s + n] += gain * sig
            else:
                k = L - s
                self.buf[s:] += gain * sig[:k]
                self.buf[:n - k] += gain * sig[k:]
        else:
            if s >= L or s + n <= 0:
                return
            if s < 0:
                sig = sig[-s:]
                s = 0
                n = len(sig)
            e = min(L, s + n)
            self.buf[s:e] += gain * sig[:e - s]

    def near_seam(self, t):
        """True if an onset at t would sit within `guard` seconds of the loop point."""
        if not self.loop:
            return False
        u = t % self.seconds
        return min(u, self.seconds - u) < self.guard


def loopify(x, L, X):
    """Take a buffer of length L+X, equal-power crossfade the extra tail into the head."""
    out = x[:L].copy()
    w = np.linspace(0.0, 1.0, X)
    out[:X] = out[:X] * np.sin(0.5 * np.pi * w) + x[L:L + X] * np.cos(0.5 * np.pi * w)
    return out


def walk(r, idx, lo, hi, stable):
    """Random-walk melody step over scale indices, gravitating to stable tones."""
    if idx not in stable and r.random() < 0.35:
        return min(stable, key=lambda s: (abs(s - idx), s))
    step = int(r.choice([-2, -1, -1, 0, 1, 1, 2, 3]))
    if idx >= hi - 1 and step > 0:
        step = -step
    if idx <= lo + 1 and step < 0:
        step = -step
    return int(np.clip(idx + step, lo, hi))


# ======================================================================= MUSIC BEDS
def bed_calm():
    """180 s, 58 BPM, 3/4 (58 bars), 평조 on Eb: Eb F Ab Bb C. Gayageum-like plucks,
    soft Eb drone, occasional 장구 thump, sparse long-decaying notes."""
    Ls, bpm = 180.0, 58.0
    beat = 60.0 / bpm
    bar = 3 * beat
    nbars = int(round(Ls / bar))                 # 58 bars exactly
    t0 = 0.5 * beat                              # keep the loop point mid-bar (sustain only)
    m = Mix(Ls, loop=True)
    r = rng(101)
    names = ["Eb3", "F3", "Ab3", "Bb3", "C4", "Eb4", "F4", "Ab4", "Bb4", "C5"]
    scale = [note(x) for x in names]
    stable = {0, 3, 5, 8}
    m.buf += 0.15 * drone([(note("Eb2"), 1.0), (note("Bb2"), 0.5), (note("Eb3"), 0.22)], Ls, seed=5)
    idx, seed = 5, 1000
    for b in range(nbars):
        bt = t0 + b * bar
        if r.random() < 0.45 and not m.near_seam(bt):
            m.place(thump(seed), bt, 0.2)
            seed += 1
        if (b % 3 == 0 or r.random() < 0.15) and not m.near_seam(bt):
            low = r.choice(["Eb2", "Eb2", "Bb2", "Ab2"])
            m.place(pluck(note(low), 8.0, t60=r.uniform(5, 7), bright=0.5, exc_lp=3, seed=seed), bt, 0.5)
            seed += 1
        if b % 4 == 3 and r.random() < 0.5:
            continue                             # breathing bar
        for pos, prob in ((0, 0.5), (1, 0.3), (1.5, 0.12), (2, 0.3), (2.5, 0.1)):
            if r.random() >= prob:
                continue
            t = bt + pos * beat
            if m.near_seam(t):
                continue
            idx = walk(r, idx, 0, len(scale) - 1, stable)
            f = scale[idx]
            u = r.random()
            cents = None
            if u < 0.3:
                cents = vib(depth=r.uniform(20, 50), rate=r.uniform(3.2, 4.8), delay=r.uniform(0.3, 0.7))
            elif u < 0.45:
                cents = bend_in(cents=-r.uniform(60, 120), dur=r.uniform(0.1, 0.2))
            elif u < 0.55:
                cents = bend_down(cents=-r.uniform(40, 80), start=r.uniform(0.4, 0.8), dur=r.uniform(0.4, 0.8))
            amp = r.uniform(0.5, 0.9)
            m.place(pluck(f, 6.0, t60=r.uniform(3.5, 5.5), bright=0.55, seed=seed, cents=cents), t, amp)
            seed += 1
            if r.random() < 0.12 and idx >= 3:   # occasional soft dyad a fifth below
                m.place(pluck(scale[idx - 3], 6.0, t60=4.0, bright=0.5, seed=seed), t + 0.02, amp * 0.5)
                seed += 1
    return fftfilt(m.buf, hi=7000, order=1)


def bed_tense():
    """120 s, 58 BPM, 4/4 (29 bars), 계면조 on C: C Eb F G Bb. Low register, slow tremolo,
    deep slow vibrato, 퇴성 bends, low drone, occasional 징 swell."""
    Ls, bpm = 120.0, 58.0
    beat = 60.0 / bpm
    bar = 4 * beat
    nbars = int(round(Ls / bar))                 # 29 bars exactly
    t0 = 0.5 * beat
    m = Mix(Ls, loop=True)
    r = rng(202)
    names = ["C2", "Eb2", "F2", "G2", "Bb2", "C3", "Eb3", "F3", "G3", "Bb3", "C4"]
    scale = [note(x) for x in names]
    stable = {0, 3, 5, 8, 10}
    m.buf += 0.2 * drone([(note("C2"), 1.0), (note("G2"), 0.45), (note("C3"), 0.2), (note("Eb3"), 0.08)],
                         Ls, seed=6, mod=0.3)
    gong_bars = [3, 11, 19, 26]
    idx, seed = 5, 2000
    for b in range(nbars):
        bt = t0 + b * bar
        if r.random() < 0.35 and not m.near_seam(bt):
            m.place(thump(seed, heavy=True), bt, 0.24)
            seed += 1
        if b in gong_bars:
            t = bt + r.uniform(0, 2) * beat
            m.place(gong(r.choice([98.0, 87.3, 110.0]), 10.0, swell=r.uniform(2.0, 3.0), t60=8.0, seed=seed), t, 0.3)
            seed += 1
        if b % 4 == 0 and not m.near_seam(bt):
            m.place(pluck(note(r.choice(["C2", "C2", "Bb1"])), 9.0, t60=r.uniform(6, 8), bright=0.45, exc_lp=3, seed=seed), bt, 0.5)
            seed += 1
        for pos, prob in ((0, 0.45), (1.5, 0.15), (2, 0.35), (3, 0.2), (3.5, 0.1)):
            if r.random() >= prob:
                continue
            t = bt + pos * beat
            if m.near_seam(t):
                continue
            idx = walk(r, idx, 2, len(scale) - 1, stable)
            f = scale[idx]
            u = r.random()
            cents = None
            if u < 0.3:
                cents = vib(depth=r.uniform(60, 90), rate=r.uniform(2.5, 3.5), delay=r.uniform(0.4, 0.9), ramp=0.8)
            elif u < 0.55:
                cents = bend_down(cents=-r.uniform(60, 110), start=r.uniform(0.5, 1.2), dur=r.uniform(0.6, 1.2))
            elif u < 0.65:
                cents = bend_in(cents=r.uniform(50, 100), dur=r.uniform(0.15, 0.3))
            trem = tremolo(rate=r.uniform(4.0, 5.5), depth=r.uniform(0.3, 0.45), delay=r.uniform(0.3, 0.6)) if r.random() < 0.4 else None
            amp = r.uniform(0.45, 0.85)
            m.place(pluck(f, 8.0, t60=r.uniform(5, 7), bright=0.45, exc_lp=3, seed=seed, cents=cents, trem=trem), t, amp)
            seed += 1
    return fftfilt(m.buf, hi=6000, order=1)


MEL_A = [[("F4", 2), ("G4", 1), ("Bb4", 1)], [("C5", 3), ("Bb4", 1)],
         [("D5", 1.5), ("C5", 0.5), ("Bb4", 2)], [("G4", 4)],
         [("F4", 1), ("G4", 1), ("Bb4", 2)], [("C5", 2), ("D5", 1), ("C5", 1)],
         [("Bb4", 2), ("G4", 2)], [("F4", 4)]]
MEL_B = [[("F5", 2), ("D5", 1), ("C5", 1)], [("D5", 3), ("C5", 1)],
         [("Bb4", 1.5), ("C5", 0.5), ("D5", 2)], [("C5", 4)],
         [("Bb4", 1), ("C5", 1), ("D5", 2)], [("C5", 2), ("Bb4", 1), ("G4", 1)],
         [("Bb4", 2), ("G4", 2)], [("F4", 4)]]
BASS_A = ["F2", "F2", "Bb2", "C3", "F2", "Bb2", "C3", "F2"]
BASS_B = ["F2", "Bb2", "Bb2", "C3", "Bb2", "C3", "C3", "F2"]


def bed_warm():
    """120 s, 66 BPM, 4/4 (33 bars), 평조 on F: F G Bb C D. A singable 8-bar tune (A B A B)
    on a brighter pluck, light bass plucks and dyads, gentle 장구 pattern, F drone."""
    Ls, bpm = 120.0, 66.0
    beat = 60.0 / bpm
    bar = 4 * beat
    nbars = int(round(Ls / bar))                 # 33 bars: 4 x 8-bar phrases + 1 breathing bar
    t0 = 0.5 * beat
    m = Mix(Ls, loop=True)
    r = rng(303)
    m.buf += 0.13 * drone([(note("F2"), 1.0), (note("C3"), 0.45), (note("F3"), 0.2)], Ls, seed=7, mod=0.2)
    fill = [note(x) for x in ["F4", "G4", "Bb4", "C5", "D5"]]
    seed = 3000
    for b in range(nbars):
        bt = t0 + b * bar
        if not m.near_seam(bt):
            m.place(thump(seed), bt, 0.18)
            seed += 1
        if b < 32:
            m.place(tick(seed), bt + 2 * beat, 0.07)
            seed += 1
            if r.random() < 0.5:
                m.place(tick(seed), bt + 3.5 * beat, 0.045)
                seed += 1
        phrase = b // 8
        if phrase >= 4:
            continue
        mel = (MEL_A, MEL_B)[phrase % 2][b % 8]
        bass = (BASS_A, BASS_B)[phrase % 2][b % 8]
        if not m.near_seam(bt):
            m.place(pluck(note(bass), 5.0, t60=4.5, bright=0.5, exc_lp=3, seed=seed), bt, 0.45)
            seed += 1
        if r.random() < 0.7:                     # soft root+fifth dyad on beat 3
            root = note(bass) * 2
            m.place(pluck(root, 4.0, t60=3.0, bright=0.5, seed=seed), bt + 2 * beat, 0.2)
            m.place(pluck(root * 1.5, 4.0, t60=3.0, bright=0.5, seed=seed + 1), bt + 2 * beat + 0.03, 0.16)
            seed += 2
        pos = 0.0
        for name, dur in mel:
            t = bt + pos * beat
            if not m.near_seam(t):
                cents = None
                if dur >= 2 and r.random() < 0.6:
                    cents = vib(depth=r.uniform(15, 35), rate=r.uniform(4.0, 5.2), delay=r.uniform(0.35, 0.6))
                elif r.random() < 0.2:
                    cents = bend_in(cents=-r.uniform(40, 90), dur=0.1)
                amp = r.uniform(0.75, 0.95) * (1.05 if pos == 0 else 1.0)
                m.place(pluck(note(name), 4.5, t60=3.5, bright=0.6, seed=seed, cents=cents), t, amp)
                seed += 1
            pos += dur
        if mel[-1][1] >= 2 and r.random() < 0.35:   # light pick-up fill on the "and" of 4
            t = bt + 3.5 * beat
            if not m.near_seam(t):
                m.place(pluck(r.choice(fill), 3.0, t60=2.5, bright=0.6, seed=seed), t, 0.3)
                seed += 1
    return fftfilt(m.buf, hi=8000, order=1)


# =========================================================================== STINGS
def sting_intro():
    """8 s: gong swell + rising pluck arpeggio (Eb 평조), clean ending."""
    m = Mix(8.0, loop=False)
    m.place(gong(note("Bb2"), 8.0, swell=1.2, t60=6.0, seed=11), 0.0, 0.55)
    m.place(pad_swell([note("Eb2"), note("Bb2")], 8.0, attack=1.5, tau=2.5), 0.0, 0.18)
    t = 1.0
    arp = ["Eb3", "Bb3", "Eb4", "F4", "Ab4", "Bb4", "C5", "Eb5"]
    for i, name in enumerate(arp):
        m.place(pluck(note(name), 6.0, t60=4.0, bright=0.58, seed=100 + i), t, 0.45 + 0.05 * i)
        t += 0.2 - 0.012 * i
    m.place(pluck(note("Bb4"), 5.0, t60=4.5, seed=120, cents=vib(30, 4.2, 0.3)), t + 0.25, 0.55)
    m.place(pluck(note("Eb5"), 5.0, t60=4.5, seed=121, cents=vib(30, 4.2, 0.35, phase=1)), t + 0.28, 0.6)
    return m.buf


def sting_chapter():
    """4 s: two soft gong-like tones and one pluck dyad."""
    m = Mix(4.0, loop=False)
    m.place(gong(note("Eb4"), 3.5, swell=0.12, t60=3.0, seed=21, small=True), 0.0, 0.5)
    m.place(gong(note("Bb3"), 3.4, swell=0.12, t60=3.0, seed=22, small=True), 0.6, 0.45)
    m.place(pluck(note("Eb4"), 2.6, t60=2.5, seed=23), 1.3, 0.5)
    m.place(pluck(note("Bb4"), 2.6, t60=2.5, seed=24, cents=vib(25, 4.5, 0.25)), 1.33, 0.55)
    return m.buf


def sting_end():
    """10 s: warm Eb strum over a soft pad, decaying to silence."""
    m = Mix(10.0, loop=False)
    m.place(pad_swell([note("Eb2"), note("Bb2"), note("Eb3"), note("Bb3")], 10.0, attack=0.8, tau=3.0), 0.0, 0.3)
    for i, name in enumerate(["Eb3", "Bb3", "Eb4", "F4", "Bb4"]):
        m.place(pluck(note(name), 9.0, t60=6.0, bright=0.55, seed=200 + i,
                      cents=vib(18, 3.8, 1.0, ramp=1.2, phase=i) if i >= 2 else None), 0.05 * i, 0.55)
    m.place(pluck(note("Eb5"), 8.0, t60=5.0, seed=210, cents=vib(22, 4.0, 0.8, ramp=1.0)), 0.3, 0.35)
    t = tvec(m.L)
    return m.buf * np.exp(-np.maximum(t - 2.0, 0.0) / 3.0)


# ======================================================================= AMBIENCES
AMB_L, AMB_X = 60.0, 3.0


def amb_frame():
    return Mix(AMB_L + AMB_X, loop=False)


def amb_finish(m):
    return loopify(m.buf, int(AMB_L * SR), int(AMB_X * SR))


def chirp(f_start, f_end, dur, trill_hz=0.0, trill_depth=0.0):
    n = int(dur * SR)
    t = tvec(n)
    u = t / dur
    f = f_start + (f_end - f_start) * u + trill_depth * np.sin(TAU * trill_hz * t)
    ph = TAU * np.cumsum(f) / SR
    env = np.sin(np.pi * u) ** 1.6
    return env * (np.sin(ph) + 0.2 * np.sin(2 * ph))


def birds(m, r, count, t_lo, t_hi, gain):
    for _ in range(count):
        t = r.uniform(t_lo, t_hi)
        fs = r.uniform(2200, 4200)
        g = r.uniform(*gain)
        for _ in range(int(r.integers(2, 6))):
            fe = fs + r.choice([-1, 1]) * r.uniform(300, 1500)
            dur = r.uniform(0.06, 0.18)
            tr = (r.uniform(25, 60), r.uniform(80, 350)) if r.random() < 0.5 else (0.0, 0.0)
            m.place(chirp(fs, fe, dur, *tr), t, g * r.uniform(0.7, 1.0))
            t += dur + r.uniform(0.06, 0.25)
            fs = float(np.clip(fs + r.uniform(-400, 400), 2000, 4500))


def cricket(n, fc, pulse_hz, npulse, chirp_rate, seed, gate_fc=0.12, seam_t=None):
    """Field-cricket voice: sine carrier gated by pulse trains grouped into chirps.
    seam_t: a time (the loop point) that is placed in the middle of a silent chirp gap."""
    t = tvec(n)
    pp = 1.0 / pulse_hz
    if npulse is None:                           # continuous trill
        tp = t % pp
        inside = 1.0
    else:
        cp = 1.0 / chirp_rate
        off = ((cp + npulse * pp) / 2.0 - seam_t) % cp if seam_t is not None else 0.0
        tc = (t + off) % cp
        inside = (tc < npulse * pp).astype(float)
        tp = tc % pp
    env = np.sin(np.pi * tp / pp) ** 2 * inside
    car = np.sin(TAU * fc * t + 0.3 * np.sin(TAU * 7.0 * t)) + 0.25 * np.sin(TAU * 2 * fc * t)
    gate = smooth01((lp_noise(n, gate_fc, seed + 1) + 0.9) / 0.8)
    slow = 0.65 + 0.35 * np.clip(lp_noise(n, 0.3, seed + 2), -1, 1)
    return env * car * gate * slow


def amb_day():
    m = amb_frame()
    n = m.L
    wind = fftfilt(white(n, 1), hi=450, order=2, tilt=-3)
    wind *= np.exp(0.7 * lp_noise(n, 0.12, 2))
    m.buf += 0.55 * norm(wind)
    hiss = fftfilt(white(n, 3), lo=1500, hi=6000, order=2) * np.exp(0.9 * lp_noise(n, 0.3, 4))
    m.buf += 0.05 * norm(hiss)
    birds(m, rng(5), 13, 0.6, AMB_L - 0.6, (0.12, 0.4))
    return amb_finish(m)


def amb_night():
    m = amb_frame()
    n = m.L
    wind = fftfilt(white(n, 11), hi=150, order=2) * np.exp(0.6 * lp_noise(n, 0.1, 12))
    m.buf += 0.4 * norm(wind)
    cr = cricket(n, 4200.0, 32.0, 3, 2.4, 13, seam_t=AMB_L)
    cr += 0.8 * cricket(n, 4550.0, 28.0, 4, 1.9, 14, seam_t=AMB_L)
    cr += 0.35 * cricket(n, 3900.0, 45.0, None, 1.0, 15, gate_fc=0.06)
    m.buf += 0.7 * norm(cr)
    return amb_finish(m)


def drip(seed):
    n = int(0.12 * SR)
    t = tvec(n)
    r = rng(seed)
    f = r.uniform(600, 1100) * np.exp(-t / 0.04) + r.uniform(400, 600)
    y = np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t / 0.045) * smooth01(t / 0.002)
    return norm(y)


def amb_rain():
    m = amb_frame()
    n = m.L
    r = rng(21)
    body = fftfilt(white(n, 22), lo=350, hi=9000, order=1, tilt=-2.5) * (1.0 + 0.22 * lp_noise(n, 0.35, 23))
    m.buf += 0.7 * norm(body)
    rumble = fftfilt(white(n, 24), hi=180, order=2) * (1.0 + 0.3 * lp_noise(n, 0.1, 25))
    m.buf += 0.25 * norm(rumble)
    for i in range(50):
        m.place(drip(300 + i), r.uniform(0.5, AMB_L - 0.5), r.uniform(0.08, 0.3))
    for i in range(36):                          # big drops on leaves
        k = int(0.006 * SR)
        m.place(norm(np.diff(white(k + 1, 400 + i)) * np.exp(-tvec(k) / 0.002)), r.uniform(0.5, AMB_L - 0.5), r.uniform(0.1, 0.25))
    return amb_finish(m)


def clink(seed):
    n = int(0.25 * SR)
    t = tvec(n)
    r = rng(seed)
    y = np.zeros(n)
    for f, a in ((2350, 1.0), (3720, 0.6), (5120, 0.4), (6900, 0.25)):
        y += a * np.sin(TAU * f * r.uniform(0.97, 1.03) * t) * np.exp(-t / r.uniform(0.04, 0.12))
    return norm(y * smooth01(t / 0.001))


def knock(seed):
    n = int(0.12 * SR)
    t = tvec(n)
    nz = fftfilt(white(n, seed), hi=500, order=2) * np.exp(-t / 0.02)
    return norm(nz + 0.7 * np.sin(TAU * 180.0 * t) * np.exp(-t / 0.03))


def amb_market():
    m = amb_frame()
    n = m.L
    r = rng(31)
    l1 = fftfilt(white(n, 32), lo=180, hi=800, order=2) * np.exp(0.8 * lp_noise(n, 0.25, 33)) * (0.7 + 0.3 * lp_noise(n, 3.5, 34))
    l2 = fftfilt(white(n, 35), lo=500, hi=2200, order=2) * np.exp(0.9 * lp_noise(n, 0.4, 36)) * (0.6 + 0.4 * lp_noise(n, 5.0, 37))
    l3 = fftfilt(white(n, 38), lo=900, hi=3500, order=2) * np.exp(1.0 * lp_noise(n, 0.5, 39)) * (0.6 + 0.4 * lp_noise(n, 6.0, 40))
    m.buf += 0.75 * norm(0.6 * norm(l1) + 0.35 * norm(l2) + 0.15 * norm(l3))
    for i in range(12):
        m.place(clink(500 + i), r.uniform(0.5, AMB_L - 0.5), r.uniform(0.08, 0.3))
    for i in range(7):
        m.place(knock(600 + i), r.uniform(0.5, AMB_L - 0.5), r.uniform(0.15, 0.35))
    return amb_finish(m)


def amb_river():
    m = amb_frame()
    n = m.L
    flow = fftfilt(white(n, 41), hi=2200, order=1, tilt=-3) * (1.0 + 0.15 * lp_noise(n, 0.15, 42))
    bubble = fftfilt(white(n, 43), lo=700, hi=3800, order=2) * np.exp(0.9 * lp_noise(n, 9.0, 44)) * (0.6 + 0.4 * lp_noise(n, 0.2, 45))
    deep = fftfilt(white(n, 46), hi=220, order=2) * (1.0 + 0.3 * lp_noise(n, 0.08, 47))
    m.buf += 0.6 * norm(flow) + 0.3 * norm(bubble) + 0.35 * norm(deep)
    return amb_finish(m)


def amb_winter():
    m = amb_frame()
    n = m.L
    t = tvec(n)
    g = np.exp(1.3 * lp_noise(n, 0.07, 51))
    g /= g.max()
    broad = fftfilt(white(n, 52), hi=350, order=2, tilt=-3) * g
    hollow = fftfilt(white(n, 53), lo=220, hi=650, order=3) * g ** 2
    f = 260.0 + 140.0 * np.clip(lp_noise(n, 0.04, 54), -1.5, 1.5) / 1.5
    ph = TAU * np.cumsum(f) / SR
    whistle = np.sin(ph) * lp_noise(n, 7.0, 55) * g ** 1.5
    whistle += 0.4 * np.sin(1.5 * ph) * lp_noise(n, 5.0, 56) * g ** 2
    m.buf += 0.6 * norm(broad) + 0.35 * norm(hollow) + 0.28 * norm(whistle)
    return amb_finish(m)


def amb_room():
    m = amb_frame()
    n = m.L
    r = rng(61)
    floor = fftfilt(white(n, 62), hi=250, order=2) * (1.0 + 0.1 * lp_noise(n, 0.1, 63))
    m.buf += 0.25 * norm(floor)
    m.buf += 0.03 * norm(fftfilt(white(n, 64), lo=2000, hi=8000, order=2))
    t = 0.5
    i = 0
    while t < AMB_L - 0.5:                       # candle crackle clusters
        for _ in range(int(r.integers(1, 6))):
            k = int(r.uniform(0.001, 0.005) * SR)
            burst = np.diff(white(k + 1, 700 + i)) * np.exp(-tvec(k) / 0.0015)
            m.place(norm(burst), t, r.uniform(0.3, 1.0))
            t += r.uniform(0.01, 0.12)
            i += 1
        t += r.uniform(0.4, 3.0)
    return amb_finish(m)


def amb_park_modern():
    m = amb_frame()
    n = m.L
    t = tvec(n)
    r = rng(71)
    breeze = fftfilt(white(n, 72), hi=700, order=2, tilt=-3) * np.exp(0.6 * lp_noise(n, 0.15, 73))
    m.buf += 0.5 * norm(breeze)
    bed = fftfilt(white(n, 74), hi=140, order=2) * (1.0 + 0.2 * lp_noise(n, 0.1, 75))
    m.buf += 0.45 * norm(bed)
    env = np.zeros(n)
    for _ in range(9):                           # passing cars in the distance
        c, w, a = r.uniform(2, AMB_L - 2), r.uniform(1.5, 3.0), r.uniform(0.3, 1.0)
        env += a * np.exp(-0.5 * ((t - c) / w) ** 2)
    env /= env.max() + 1e-12
    m.buf += 0.35 * norm(fftfilt(white(n, 76), lo=70, hi=320, order=2)) * env
    m.buf += 0.12 * norm(fftfilt(white(n, 77), lo=900, hi=3000, order=2)) * env ** 2
    birds(m, rng(78), 4, 0.6, AMB_L - 0.6, (0.1, 0.3))
    return amb_finish(m)


# ============================================================== finalise / verify
def finalize(x, peak_db, fade_in=0.0, fade_out=0.0):
    x = fftfilt(x, lo=20, order=2)               # DC / sub-rumble removal
    if fade_in:
        k = int(fade_in * SR)
        x[:k] *= np.linspace(0.0, 1.0, k)
    if fade_out:
        k = int(fade_out * SR)
        x[-k:] *= np.linspace(1.0, 0.0, k) ** 2
    x -= x.mean()
    x *= 10.0 ** (peak_db / 20.0) / (np.max(np.abs(x)) + 1e-12)
    return x


def db(v):
    return 20.0 * math.log10(max(v, 1e-12))


def check(path, loop):
    d, sr = sf.read(path, dtype="float64")
    assert sr == SR
    k = int(0.1 * SR)
    peak = float(np.max(np.abs(d)))
    rms = float(np.sqrt(np.mean(d ** 2)))
    head = float(np.sqrt(np.mean(d[:k] ** 2)))
    tail = float(np.sqrt(np.mean(d[-k:] ** 2)))
    seam = abs(d[0] - d[-1]) / (np.percentile(np.abs(np.diff(d)), 99) + 1e-12)
    ok = peak <= 0.95 and abs(float(d.mean())) < 1e-3
    if loop:
        ok = ok and abs(db(head) - db(tail)) <= 3.0 and seam < 3.0
    return dict(file=os.path.basename(path), dur=len(d) / SR, peak_db=db(peak), rms_db=db(rms),
                loop=loop, head_db=db(head), tail_db=db(tail), seam=float(seam), peak=peak, ok=ok)


# (name, builder, peak dBFS, loop, fade_in s, fade_out s)
JOBS = [
    ("bed_calm.wav", bed_calm, -12.0, True, 0, 0),
    ("bed_tense.wav", bed_tense, -12.0, True, 0, 0),
    ("bed_warm.wav", bed_warm, -12.0, True, 0, 0),
    ("sting_intro.wav", sting_intro, -8.0, False, 0.01, 1.5),
    ("sting_chapter.wav", sting_chapter, -8.0, False, 0.005, 0.8),
    ("sting_end.wav", sting_end, -8.0, False, 0.01, 1.2),
    ("amb_day.wav", amb_day, -20.0, True, 0, 0),
    ("amb_night.wav", amb_night, -20.0, True, 0, 0),
    ("amb_rain.wav", amb_rain, -20.0, True, 0, 0),
    ("amb_market.wav", amb_market, -20.0, True, 0, 0),
    ("amb_river.wav", amb_river, -20.0, True, 0, 0),
    ("amb_winter.wav", amb_winter, -20.0, True, 0, 0),
    ("amb_room.wav", amb_room, -26.0, True, 0, 0),
    ("amb_park_modern.wav", amb_park_modern, -20.0, True, 0, 0),
]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    out_dir = argv[1]
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    t_start = time.time()
    for name, fn, peak_db, loop, fi, fo in JOBS:
        if only and name.replace(".wav", "") not in only and name not in only:
            continue
        t1 = time.time()
        x = finalize(fn(), peak_db, fi, fo)
        path = os.path.join(out_dir, name)
        sf.write(path, x, SR, subtype="PCM_16")
        row = check(path, loop)
        row["secs"] = time.time() - t1
        rows.append(row)
        print(f"  wrote {name:22s} ({row['secs']:.1f}s)", flush=True)
    print()
    print(f"{'file':22s} {'dur s':>7s} {'peak dBFS':>10s} {'RMS dBFS':>9s} {'loop':>5s} {'head/tail dB':>16s} {'seam':>5s} {'max':>6s} ok")
    bad = 0
    for r in rows:
        ht = f"{r['head_db']:6.1f}/{r['tail_db']:6.1f}" if r["loop"] else "-"
        print(f"{r['file']:22s} {r['dur']:7.1f} {r['peak_db']:10.1f} {r['rms_db']:9.1f} {'yes' if r['loop'] else 'no':>5s} "
              f"{ht:>16s} {r['seam']:5.2f} {r['peak']:6.3f} {'OK' if r['ok'] else 'FAIL'}")
        bad += not r["ok"]
    print(f"\n{len(rows)} files in {time.time() - t_start:.1f}s -> {out_dir}"
          + ("" if not bad else f"  ({bad} FAILED checks)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
