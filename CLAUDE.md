# Claude Code notes for this repository

## Working folder
This repository is meant to be checked out at `D:\Claude_Work\LongYoutube` on the owner's Windows PC and worked on there
(`cd D:\Claude_Work\LongYoutube` then `claude`). Everything produced for a video lives under `video/<slug>/`:
sources in git (`script/`, `assets/`, `youtube-meta.md`, `thumbnail.png`, `README.md`) and large outputs next to
them but git-ignored (`build/`, `*.mp4`, `parts/`). Never write project files anywhere else.
Tools and models are project-local and git-ignored: `tools/` (ffmpeg), `models/` (TTS models), `fonts/` (Nanum fonts).

## Long-form yadam video pipeline (`video/2026-09-yadam-manbok`)
- First time on a machine: `python scripts/yadam_build.py video/2026-09-yadam-manbok --setup`
  (downloads the Supertonic 3 Korean TTS model, ffmpeg on Windows, installs Python deps, then prints what it found).
  Also needed once: Node 22 + `npm i -g playwright && npx playwright install chromium` (only for regenerating art).
- Full build: `python scripts/yadam_build.py video/2026-09-yadam-manbok` ; redo from a step: `--from tts` / `--from render`.
- Steps and their scripts: `yadam_art.py` (SVG art) -> `yadam_music.py` (synth music/ambience) -> `yadam_script.py`
  (parse `script/*.md`) -> `yadam_tts.py` (Supertonic 3, per-character voice cast in `CAST`, emotion rules in `delivery()`)
  -> `yadam_render.py` (Pillow cut-out animation + ffmpeg, burned-in large subtitles, -14 LUFS mix)
  -> `yadam_thumbnail.py` -> `yadam_qa.py`. `yadam_env.py` resolves ffmpeg/models/fonts on any OS.
- Script format: see the docstring of `scripts/yadam_script.py`. Editing `script/*.md` and running `--from tts` re-synthesises
  only changed sentences (cache in `build/tts/`) and re-renders.
- YouTube: `set YOUTUBE_TOKEN=ya29...` (1-hour token from https://developers.google.com/oauthplayground with the
  YouTube Data API v3 `youtube` + `youtube.upload` scopes) then
  `python scripts/publish_youtube.py video/2026-09-yadam-manbok/yadam_manbok_1080p.mp4 --meta video/2026-09-yadam-manbok/youtube-meta.md --thumb video/2026-09-yadam-manbok/thumbnail.png --srt video/2026-09-yadam-manbok/subtitles.srt --privacy private`.
- Delivery: a cloud session cannot write to the PC; it delivers by pushing this branch (sources) and by sending
  `parts/` (30 MB chunks + `join_*.bat`) in chat. On the PC, prefer rebuilding locally with `yadam_build.py`.

## Conventions
- Commit messages in English, one line summary + short body; push to the working branch after each meaningful step.
- Korean user-facing text (scripts, meta, README for the video) stays in Korean.
- Do not commit anything under `build/`, `tools/`, `models/`, `fonts/`, or `.mp4`/`.wav` files.
