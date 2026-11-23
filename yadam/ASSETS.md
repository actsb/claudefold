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
| Scripts | This branch, folder yadam/ (rebuilt 2026-11-21, see below) | No secrets |

## Production queue (user-approved 11-23, in this order)
1. Arirang Decoded Short: regional Arirangs (auto, film scenes) — DONE 69cR6SZJuzI, scheduled public 2026-11-24 07:00 KST
2. Tiger kindness folktale Short (Vrew) — instruction sheet yadam/vrew/tk01_지시문.md (11-23)
3. Secret royal inspector Park Mun-su 2-part Shorts (Vrew) — instruction sheet yadam/vrew/pm01_02_지시문.md (11-23)
4. Over Arirang Pass best-scene Shorts (auto, pilot_short.py)
No jeoseung saja / afterlife-judge topics on our channel.
Vrew output folder on the user's PC (D540win11): D:\Vrew반입\<job>\out (not Google Drive). Vrew jobs run in a session on the PC bridge environment "D540win11:D:\Claude_Work".

## Rule learned
The cloud scratchpad is not durable. Anything needed again goes to git (code), Google Drive (media, private files) or environment secrets (keys).

## Handoff for a new session (2026-11-21)
Start a new cloud session on this branch and read this file first. Reply to the user in Korean.

### State
- Container restart wiped the scratchpad on ~11-20. Lost: scripts, OAuth client files, refresh tokens, Gemini key file, film masters, release_log.
- Scheduled tasks (old ids deleted 11-21), now ENABLED: daily check trig_01EqjtueTtfFZ74A1YX2m47y and weekly report trig_01TFKbHCm214kBpTP1qkX3jp, both firing into the recovery session session_0178FLamKtGXWcroNq1UABjN, prompts use the yadam/ scripts.
- Credentials: the user adds them as environment Network secrets (this session was too long for the secure form):
  - generativelanguage.googleapis.com, header x-goog-api-key = Gemini API key
  - oauth2.googleapis.com, Authorization Basic = OAuth client ID : client secret of "koreanmusical uploader" (Cloud project "My First Project", number 825670073835; Google Auth Platform already PUBLISHED with branding links to actsb.github.io/claudefold/oauth/)
  - Then re-consent via OAuth Playground (redirect https://developers.google.com/oauthplayground, access_type=offline, prompt=consent select_account): YouTube for Korean Musical Folktales (scopes youtube, youtube.force-ssl, youtube.upload, yt-analytics.readonly), Drive (drive.readonly + drive.file, so the film files in the user's Drive can be downloaded), and 가성비리빙연구소 (youtube.force-ssl, youtube.upload; the gaseongbi-uploader project 1067598475600 has its own client — or reuse the KM client and share quota).
  - Keep refresh tokens only in the scratchpad, plus a private backup file in the user's Google Drive (never git — public repo).
- Film files in the user's Google Drive (PC path I:\내 드라이브\영상): folder 「아리랑 고개를 넘어 (완성본)」: Over_Arirang_Pass_full_v3_2026-10-22.mp4 + .srt, Over_Arirang_Pass_full_2026-10-19.mp4 + .srt, thumbnail A/B/C folder. Folder 「아카이브」: arirang.tar (3.3 GB), longyoutube.tar (6.9 GB), asr.tar, deliver.tar, hangul.tar, panel_frames.tar, video_project_move…tar, src_backup_202609…tgz (scripts as of 10-19), arimusical chapter/ep masters and shorts. Folder 「롱폼」: other yadam long-form MP4s. The user will NOT move or copy them; download through the Drive API.
- The public full film is v4 (YouTube 5jTXBPLF9f4); Drive holds v3. Shorts need a subtitle-free master (was clean_master2.mkv) — look inside arirang.tar / longyoutube.tar.

### Channels and ids
- Korean Musical Folktales UCNDIUDE7FVc29dLcxl_ueEQ (English, AI Korean folk musical). Episodes: Ep.3 23WGkmfZa-E, Ep.4 W7hGbORoQ7M, Ep.5 bE39pxgQvOM, Ep.6 DFdVH5dWUco, Ep.7 o2jdjydbIq0, Ep.8 DTio1YSDPwo, Ep.9 KOfef1xs2NA, full film 5jTXBPLF9f4.
- Playlists: Arirang Decoded PLJ9A_y_nDXqU, Over Arirang Pass series PLPTUKvzZ0QXM, Hangul PLDwR-TKEvm1g.
- Arirang Decoded Shorts: BTjxVoe47UI, pDx2xXgi_pE, 5ZQkNmIu5yI (1,097 views), KY5q4LSJcpY, B5XRAthaTr8 (11-18, emotional "Why Would BTS Name an Album ARIRANG?"). BTS pilot Xaolt2rJnfI.
- 가성비리빙연구소 UCd6mIDo7MFVfzoJs3Tg6VUA.

### Standing rules from the user
Subtitles at the bottom, big; smooth 0.5 s dissolves; the user does not audition songs; cheap production, report spend daily, monthly cap KRW 100,000; all translations written by Claude (not Gemini, not Vrew auto-translate); never delete or privatize the old public Ep.1 videos (XnQ-0UgXGQw, mzvCz6DSfbk, atITdRhiigY); never publish "[OLD" videos; delete local files only after a verified Drive copy; no model names in repository files; never echo credentials; user emails are private (never in this public repo); keep YouTube quota in check (10,000/day per project).

### Plan pages (claude.ai artifacts)
Strategy EkiyssFUtiUnYengAY1d8E · Vrew guide 9MacfRc92oxgPmDtj2QKzu · Tools KEQRR3VBcmyCUCCLrzzwmG · Weekly report 3fUcpEyLa1MFywhwGG6Gy9 · Series plan P2D3RdiaNXkRMvyPffAkE1 (URLs: https://claude.ai/artifact/<id>)

### Pending with the user
Vrew job kdh01 (tiger & magpie) via the PC desktop app (kdh02 jeoseung saja: CANCELLED 11-23, user decided not to make jeoseung/saja content on our channel); Vrew update to 4.x; reply to the "중국식 음악" comment on KY5q4LSJcpY (drafted, not posted); next Arirang Decoded Short topic (regional Arirangs or Arirang Pass).

## Scripts (yadam/, rebuilt 2026-11-21)
Set `YADAM_TOKDIR` to a private folder holding km.json, gsb.json, drive.json (each with a "refresh_token").
Refresh tokens: private backup file in the user's Google Drive (yadam_oauth_tokens_backup_2026-11-21.json, owner-only).
The OAuth client ID/secret come from the environment network secret for oauth2.googleapis.com (HTTP Basic).
| Script | Job |
|---|---|
| ytlib.py | token refresh + API helpers (shared) |
| tok_check.py | 토큰 점검: which channel/account each token reaches |
| views.py | 공개 조회수 for recent uploads (or --ids) |
| comments.py | 댓글 점검: recent threads, 미답변 marked; never posts |
| ctr48.py | first-48h Analytics per recent upload (impressions CTR only in Studio) |
| pilot_short.py | pilot 쇼츠 제작: 9:16 cut from a clean master, big bottom subs, 0.5 s dissolves |
| yt_up.py | upload (default private, --publish-at), thumbnail, captions, playlist; refuses "[OLD" titles |
| bench.py | 명당 조사: views/day by channel, format, weekday, KST hour block |
