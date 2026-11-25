# Verdict Picks Toon 쇼츠: 유튜브 업로드 안내

파일 위치: `shorts/` (GitHub Pages: https://actsb.github.io/claudefold/shorts/)
- `ep1.mp4`, `ep2.mp4`, `ep3.mp4`: 1080×1920, 60초 미만, 음악 포함
- `epN-thumb.jpg`: 미리보기 이미지
- `epN.<언어>.srt`: 11개 언어 자막 (en, es, pt, fr, de, ja, ko, zh-Hans, hi, id, vi)
- `epN-youtube.json`: 11개 언어 제목·설명과 업로드 설정
- `season1.mp4`: 시즌 1 롱폼, 가로 1920×1080, 5분 58초. 쇼츠를 이어 붙인 것이 아니라 별도 기획입니다(화별 새 오프닝 그림, 웹툰 스토리, Vera의 칠판 해설 4장씩, 챕터 6개). 자막·메타는 `season1.<언어>.srt`, `season1-youtube.json`. 설명란의 챕터로 YouTube가 챕터를 자동으로 만듭니다.

## 블로그 ↔ 유튜브 상호 연결 (운영자 지시, 2026-11-25)
쇼츠 설명란·댓글의 링크는 YouTube가 클릭되지 않게 막습니다([YouTube 고객센터](https://support.google.com/youtube/answer/13748639), 2023-08-31부터). 그래서 아래처럼 연결합니다.

**유튜브 → 블로그 (업로드할 때마다 Studio에서)**
1. **설명 첫 줄:** 블로그 글 전체 주소 (`epN-youtube.json`의 설명에 이미 들어 있음). 10개 번역 설명에도 주소가 그대로 들어 있습니다.
2. **관련 동영상:** 쇼츠 세부정보 → "관련 동영상"에 그 시즌 롱폼(시즌 1은 `VXqBhjOERLk`)을 지정합니다. 롱폼 설명의 블로그 링크는 클릭됩니다.
3. **고정 댓글:** Prof H Lab 계정으로 "Full review, today's price and the safety check: <글 주소>"를 달고 고정합니다.
4. **재생목록:** "Verdict Picks Toon" 재생목록에 쇼츠와 롱폼을 모두 넣습니다.
5. **채널 링크:** Studio → 맞춤설정 → 기본 정보 → 링크에 "Verdict Picks reviews" → `https://acts39.blogspot.com` (한 번만).
6. **화면:** 쇼츠 하단 띠에 "Full review & today's price: acts39.blogspot.com"이 나오고, 마지막 컷이 Verdict Picks와 주제를 말합니다(`toon_shorts.py`).

**블로그 → 유튜브 (자동)**
- 업로드하면 영상 ID를 `shorts/youtube-ids.json`에 기록합니다(`id`, `title`, `caption`, `uploaded`, `seconds`, `post`).
- 그 글만 다시 게시하면 `publish_blogger.py`가 글 맨 앞에 쇼츠, VideoObject 구조화 데이터, "Watch on YouTube"·Prof H Lab 구독·전체 에피소드 링크를 넣습니다.
- `python3 scripts/toon_page.py` 후 `--page "Verdict Picks Toon"`으로 에피소드 페이지를 갱신합니다.

## 왜 손으로 올려야 하나
YouTube는 API 심사를 통과하지 않은 앱이 올린 영상을 **모두 비공개로 잠급니다**. 그래서 영상 업로드만 운영자님이 YouTube Studio에서 직접 합니다. 번역 제목·설명과 자막 11개는 아래 2단계를 한 번 해 두시면 Claude가 API로 자동으로 넣습니다.

## 1단계: 영상 업로드 (편당 3분)
1. https://studio.youtube.com (채널 소유자 계정) → 만들기 → 동영상 업로드 → `ep1.mp4`
2. 제목·설명: `ep1-youtube.json`의 `metadata.en`을 그대로 붙여 넣기
3. 미리보기 이미지: `ep1-thumb.jpg` (쇼츠는 앱에서 영상 프레임을 고를 수도 있음)
4. 시청자층: **아니요, 아동용이 아닙니다**
5. 자세히 보기:
   - 변경된 콘텐츠(합성 콘텐츠): **아니요** (사실적으로 보이지 않는 만화 그림)
   - 유료 프로모션: 체크하지 않음 (협찬 없음)
   - 동영상 언어: 영어
   - 카테고리: 노하우/스타일
6. 공개 범위: **공개**
7. 업로드가 끝나면 영상 주소(`youtube.com/shorts/XXXXXXXXXXX`)를 Claude에게 알려 주세요. 영상 ID 11자만 있으면 됩니다.

## 2단계: 번역 자동 입력 권한 (한 번만, 10분)
Blogger 자동 발행에 쓰는 같은 Google Cloud 프로젝트를 씁니다.
1. Google Cloud Console → 그 프로젝트 → API 및 서비스 → 라이브러리 → **YouTube Data API v3** 사용 설정
2. https://developers.google.com/oauthplayground → 톱니바퀴 → "Use your own OAuth credentials"에 Blogger와 같은 Client ID와 Secret 입력
3. 왼쪽 범위 입력칸에 `https://www.googleapis.com/auth/youtube.force-ssl` 입력 → Authorize APIs → **채널 소유자 계정**으로 로그인하고 유튜브 채널 선택 → Exchange authorization code for tokens
4. 나온 **Refresh token**을 Claude 환경 설정(Settings → 환경 cloudfold → 환경 변수)에 `YOUTUBE_REFRESH_TOKEN`이라는 이름으로 저장
   - **대화창에 붙여 넣지 마세요.**

그다음 Claude가 `python3 scripts/youtube_localize.py <영상ID> shorts/ep1-youtube.json`으로 10개 언어 제목·설명과 11개 자막을 넣습니다.

## 2단계를 하지 않는 경우 (손으로 하기)
YouTube Studio → 자막 → 영상 선택 → 언어 추가 (편당 10개 언어) → 언어마다 다음을 넣습니다.
- "제목 및 설명": json의 해당 언어 내용
- "자막" → 파일 업로드 → "타이밍 포함" → 해당 `.srt`

세 편 합쳐 약 1시간이 걸립니다.

## Gemini 키를 헤더 방식으로 추가하기 (그림 품질 업그레이드용, 운영자님)
Claude는 키 값을 볼 수 없어 직접 넣을 수 없습니다.
1. claude.ai/code 세션 제목줄의 환경 메뉴(cloudfold) → 편집(Edit)
2. Network secrets(또는 API credentials) → 추가
   - 호스트: `generativelanguage.googleapis.com`
   - 헤더 이름: `x-goog-api-key`
   - 값: Google AI Studio 키
3. 저장. 새 세션부터 적용됩니다.

## 규칙 (운영자 지시, 2026-11-24)
- 쇼츠는 세로(1080×1920), 롱폼은 가로(1920×1080)로 따로 만든다.
- **쇼츠를 롱폼에 그대로 쓰는 것은 금지.** 쇼츠를 이어 붙이거나, 늘리거나, 가로로 옮기기만 한 롱폼은 만들지 않는다. 롱폼은 자체 기획과 대본, 새 16:9 그림, 챕터, 쇼츠에 없는 설명 구간(비교표, 비용, 체크리스트, 살 사람·기다릴 사람·건너뛸 사람과 출처)을 가진다.
