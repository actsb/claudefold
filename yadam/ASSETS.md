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

## Handoff for a new session (2026-11-21)
Start a new cloud session on this branch and read this file first. Reply to the user in Korean.

### State
- Container restart wiped the scratchpad on ~11-20. Lost: scripts, OAuth client files, refresh tokens, Gemini key file, film masters, release_log.
- Scheduled tasks DISABLED until recovery: daily check trig_011EL2mZjsdmUTaJohVc7GKn, weekly report trig_01Dh7rpzLXKiQbPBFHYjPfdE. Re-enable after recovery and update their prompts to the new file locations.
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
Vrew jobs kdh01 (tiger & magpie) and kdh02 (jeoseung saja) via the PC desktop app; Vrew update to 4.x; reply to the "중국식 음악" comment on KY5q4LSJcpY (drafted, not posted); next Arirang Decoded Short topic (regional Arirangs or Arirang Pass).
