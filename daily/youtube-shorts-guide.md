# Verdict Picks Toon 쇼츠: 유튜브 업로드 안내 (profhlab@gmail.com 채널)

파일 위치: `shorts/` (GitHub Pages: https://actsb.github.io/claudefold/shorts/)
- `ep1.mp4`, `ep2.mp4`, `ep3.mp4`: 1080×1920, 60초 미만, 음악 포함
- `epN-thumb.jpg`: 미리보기 이미지
- `epN.<언어>.srt`: 11개 언어 자막 (en, es, pt, fr, de, ja, ko, zh-Hans, hi, id, vi)
- `epN-youtube.json`: 11개 언어 제목·설명과 업로드 설정

## 왜 손으로 올려야 하나
YouTube는 API 심사를 통과하지 않은 앱이 올린 영상을 **모두 비공개로 잠급니다**. 그래서 영상 업로드만 운영자님이 YouTube Studio에서 직접 합니다. 번역 제목·설명과 자막 11개는 아래 2단계를 한 번 해 두시면 Claude가 API로 자동으로 넣습니다.

## 1단계: 영상 업로드 (편당 3분)
1. https://studio.youtube.com (profhlab@gmail.com) → 만들기 → 동영상 업로드 → `ep1.mp4`
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
3. 왼쪽 범위 입력칸에 `https://www.googleapis.com/auth/youtube.force-ssl` 입력 → Authorize APIs → **profhlab@gmail.com**으로 로그인하고 유튜브 채널 선택 → Exchange authorization code for tokens
4. 나온 **Refresh token**을 Claude 환경 설정(Settings → 환경 cloudfold → 환경 변수)에 `YOUTUBE_REFRESH_TOKEN`이라는 이름으로 저장
   - **대화창에 붙여 넣지 마세요.**

그다음 Claude가 `python3 scripts/youtube_localize.py <영상ID> shorts/ep1-youtube.json`으로 10개 언어 제목·설명과 11개 자막을 넣습니다.

## 2단계를 하지 않는 경우 (손으로 하기)
YouTube Studio → 자막 → 영상 선택 → 언어 추가 (편당 10개 언어) → 언어마다 다음을 넣습니다.
- "제목 및 설명": json의 해당 언어 내용
- "자막" → 파일 업로드 → "타이밍 포함" → 해당 `.srt`

세 편 합쳐 약 1시간이 걸립니다.
