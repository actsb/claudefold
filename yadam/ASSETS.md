# Yadam assets map (no secrets in this file — the repository is public)

Updated 2026-11-21 after the cloud work folder was wiped by a container restart.

## Where things live
| What | Where | Notes |
|---|---|---|
| Published videos, playlists, schedules | YouTube (Korean Musical Folktales, 가성비리빙연구소) | Safe |
| Plan pages | claude.ai artifacts (strategy, Vrew guide, tools, weekly report) | Safe |
| OAuth branding pages | GitHub Pages: actsb.github.io/claudefold/oauth/ (branch claude/sharp-lovelace-n7vhzq) | Never delete |
| Film masters (clean_master2.mkv, full_v4.mp4, full_v4_*.srt) | User's PC: `I:\내 드라이브\영상` (Google Drive desktop mount) — to be confirmed | Keep a copy in Google Drive: the cloud session can only reach files through Drive |
| Credentials (Gemini key, OAuth client JSONs, refresh tokens) | Gemini key: environment network secret. OAuth files: private folder in the user's Google Drive | Never in git |
| Scripts | This branch, folder yadam/ (to be rebuilt) | No secrets |

## Rule learned
The cloud scratchpad is not durable. Anything needed again goes to git (code), Google Drive (media, private files) or environment secrets (keys).
