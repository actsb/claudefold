"""Parse the yadam screenplay (video/<slug>/script/*.md) into a JSON shot list.

Format of a script file:
  # CHAPTER n | 장 제목                      -> chapter card (n=0: no card, prologue)
  ## TITLE 제목 | 부제                        -> main title card scene
  ## SCENE bg=<bg> cam=<zoomin|zoomout|panleft|panright|static> amb=<amb> music=<calm|tense|warm|none>
           chars=name:pose:x[:flip] ... props=name:x:y:scale ... fx=rain|snow|none
  plain line                                  -> narration (split into subtitle-sized sentences)
  @name line                                  -> dialogue spoken by character `name` (mouth animates)

Usage: python3 scripts/yadam_script.py video/2026-09-yadam-manbok  -> writes build/script.json
"""
import json, pathlib, re, sys

SENT_END = re.compile(r'(?<=[.!?])\s+')
MAX_SUB = 42  # max characters per subtitle line before we split on a comma


def split_sentences(text):
    """Sentences as TTS units. A very short sentence ("예.", "네?") is merged with its neighbour, because the
    VITS model produces almost nothing for a lone syllable; the subtitle still shows it as its own chunk."""
    parts = [p.strip() for p in SENT_END.split(text.strip()) if p.strip()]
    merged = []
    for p in parts:
        if merged and len(merged[-1].split()[-1]) <= 4 and len(merged[-1]) <= 6:
            merged[-1] = merged[-1] + ' ' + p          # previous was tiny: glue this one onto it
        else:
            merged.append(p)
    if len(merged) > 1 and len(merged[-1]) <= 6:       # tiny last sentence: glue onto the previous
        merged[-2:] = [merged[-2] + ' ' + merged[-1]]
    return merged


def subtitle_chunks(sentence):
    """A TTS unit may be shown as several subtitle chunks: first at sentence ends, then long sentences at the comma nearest the middle."""
    out = []
    for s in [p.strip() for p in SENT_END.split(sentence) if p.strip()]:
        if len(s) <= MAX_SUB or ',' not in s:
            out.append(s); continue
        idx = [m.start() for m in re.finditer(',', s)]
        mid = min(idx, key=lambda i: abs(i - len(s) / 2))
        a, b = s[:mid + 1].strip(), s[mid + 1:].strip()
        out += [a, b] if b else [a]
    return out


def parse_scene_header(line):
    spec = {"bg": "village_spring_day", "cam": "static", "amb": "none", "music": "calm", "chars": [], "props": [], "fx": "none"}
    mode = None
    for tok in line.split():
        if '=' in tok:
            k, v = tok.split('=', 1)
            if k in ('chars', 'props'):
                mode = k; spec[k] = []; tok = v
            else:
                spec[k] = v; mode = None; continue
        p = tok.split(':')
        if mode == 'chars':
            spec['chars'].append({"name": p[0], "pose": p[1] if len(p) > 1 else 'stand', "x": float(p[2]) if len(p) > 2 else 0.5, "flip": len(p) > 3 and p[3] == 'flip'})
        elif mode == 'props':
            spec['props'].append({"name": p[0], "x": float(p[1]) if len(p) > 1 else 0.5, "y": float(p[2]) if len(p) > 2 else 0.85, "scale": float(p[3]) if len(p) > 3 else 1.0})
    return spec


def parse(root):
    root = pathlib.Path(root)
    chapters = []
    for f in sorted((root / 'script').glob('*.md')):
        chap = None; scene = None
        for raw in f.read_text(encoding='utf-8').splitlines():
            line = raw.rstrip()
            if not line.strip():
                continue
            if line.startswith('# CHAPTER'):
                m = re.match(r'# CHAPTER\s+(\d+)\s*\|\s*(.+)', line)
                chap = {"n": int(m.group(1)), "title": m.group(2).strip(), "scenes": []}
                chapters.append(chap); scene = None
            elif line.startswith('## TITLE'):
                t = line[len('## TITLE'):].strip()
                title, _, sub = t.partition('|')
                scene = {"kind": "title", "title": title.strip(), "sub": sub.strip(), "lines": [], "bg": "title_card", "cam": "static", "amb": "none", "music": "calm", "chars": [], "props": [], "fx": "none"}
                chap['scenes'].append(scene)
            elif line.startswith('## SCENE'):
                scene = {"kind": "scene", "lines": [], **parse_scene_header(line[len('## SCENE'):])}
                chap['scenes'].append(scene)
            else:
                speaker = None; text = line
                m = re.match(r'@(\w+)\s+(.*)', line)
                if m:
                    speaker, text = m.group(1), m.group(2)
                for s in split_sentences(text):
                    scene['lines'].append({"speaker": speaker, "text": s, "subs": subtitle_chunks(s), "para_end": False})
                if scene['lines']:
                    scene['lines'][-1]['para_end'] = True
    return {"chapters": chapters}


if __name__ == '__main__':
    root = pathlib.Path(sys.argv[1])
    data = parse(root)
    out = root / 'build' / 'script.json'; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    n_scenes = sum(len(c['scenes']) for c in data['chapters'])
    n_lines = sum(len(s['lines']) for c in data['chapters'] for s in c['scenes'])
    n_chars = sum(len(l['text']) for c in data['chapters'] for s in c['scenes'] for l in s['lines'])
    print(f"{len(data['chapters'])} chapters, {n_scenes} scenes, {n_lines} subtitle lines, {n_chars} chars -> {out}")
