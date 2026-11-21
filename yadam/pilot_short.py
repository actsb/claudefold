#!/usr/bin/env python3
"""pilot 쇼츠 제작: cut a 9:16 Short (1080x1920) from a subtitle-free master.
House style: big subtitles at the bottom, 0.5 s dissolves between segments, no audition step.
Subtitles come from an SRT written by Claude (translations by Claude, never auto-translate);
only cues overlapping each segment are kept and re-timed.

Usage:
  python3 yadam/pilot_short.py MASTER.mkv OUT.mp4 --seg 00:12:03.5-00:12:21 --seg 00:31:10-00:31:30 \
      --srt short_en.srt [--fit blur|crop] [--font-size 76]
--srt timing is relative to the FINAL short (write it after a dry run with --no-subs), or use
--master-srt to slice cues from the master's own SRT.
"""
import argparse, os, re, subprocess, sys, tempfile

def ts(s):
    p = [float(x) for x in s.replace(",", ".").split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))

def fmt(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

def read_srt(p):
    out = []
    for b in re.split(r"\n\s*\n", open(p, encoding="utf-8-sig").read().strip()):
        L = b.strip().splitlines()
        i = next((k for k, l in enumerate(L) if "-->" in l), None)
        if i is None: continue
        a, b2 = [ts(x.strip()) for x in L[i].split("-->")]
        out.append((a, b2, "\n".join(L[i + 1:])))
    return out

XF = 0.5  # dissolve length (house rule)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("master"); ap.add_argument("out")
    ap.add_argument("--seg", action="append", required=True); ap.add_argument("--srt", default=""); ap.add_argument("--master-srt", default="")
    ap.add_argument("--fit", default="blur", choices=["blur", "crop"]); ap.add_argument("--font-size", type=int, default=76)
    ap.add_argument("--no-subs", action="store_true")
    a = ap.parse_args()
    segs = [tuple(ts(x) for x in s.split("-")) for s in a.seg]
    durs = [e - s for s, e in segs]
    total = sum(durs) - XF * (len(segs) - 1)
    if total > 60: print(f"warning: {total:.1f}s is over 60 s", file=sys.stderr)
    # offsets of each segment in the final timeline
    offs, t = [], 0.0
    for d in durs: offs.append(t); t += d - XF
    cues = []
    if a.master_srt:
        for (s, e), o in zip(segs, offs):
            for c0, c1, txt in read_srt(a.master_srt):
                if c1 > s and c0 < e: cues.append((max(c0, s) - s + o, min(c1, e) - s + o, txt))
    elif a.srt:
        cues = read_srt(a.srt)
    tmp = tempfile.mkdtemp(); srt_out = os.path.join(tmp, "s.srt")
    with open(srt_out, "w", encoding="utf-8") as f:
        for i, (c0, c1, txt) in enumerate(cues, 1): f.write(f"{i}\n{fmt(c0)} --> {fmt(c1)}\n{txt}\n\n")
    if a.fit == "blur":
        vf1 = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2[bg];"
               "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-120")
    else:
        vf1 = "scale=-2:1920,crop=1080:1920"
    inputs, fc = [], []
    for i, (s, e) in enumerate(segs):
        inputs += ["-ss", f"{s}", "-t", f"{e - s}", "-i", a.master]
        fc.append(f"[{i}:v]{vf1},setsar=1,fps=30,format=yuv420p[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}]")
    v, au = "[v0]", "[a0]"
    for i in range(1, len(segs)):
        fc.append(f"{v}[v{i}]xfade=transition=fade:duration={XF}:offset={offs[i]:.3f}[vx{i}];{au}[a{i}]acrossfade=d={XF}[ax{i}]")
        v, au = f"[vx{i}]", f"[ax{i}]"
    if cues and not a.no_subs:
        style = (f"FontName=Noto Sans CJK KR,FontSize={a.font_size},Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
                 f"BorderStyle=1,Outline=5,Shadow=1,Alignment=2,MarginV=260,WrapStyle=0")
        fc.append(f"{v}subtitles='{srt_out}':original_size=1080x1920:force_style='{style}'[vs]"); v = "[vs]"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", v, "-map", au,
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
    print(f"wrote {a.out} ({total:.1f}s, {len(cues)} subtitle cues)")

if __name__ == "__main__":
    main()
