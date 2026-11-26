# Prof H Lab 유튜브 API 업로드: 다른 채널 세션에 붙여 넣을 요청문

> **완료됨 (2026-11-24): 이 요청문을 더 이상 붙여 넣지 마세요.** 4편은 세아 채널 PC 세션이 크롬 YouTube Studio로 Prof H Lab 채널에 공개로 올렸습니다(ep1 `-QpIRKTADXw`, ep2 `Cx54-DoZS0g`, ep3 `BHhCXHFNCfo`, season1 `VXqBhjOERLk`; 11개 언어 제목·설명·자막 포함). 다시 보내면 같은 영상이 중복 업로드됩니다. 영상 ID는 `shorts/youtube-ids.json`, 새 쇼츠의 업로드·연결 절차는 `daily/youtube-shorts-guide.md`에 있습니다.


운영자님 PC의 유튜브 세션(예: 「SEAH 음악 채널기획서」, 「호랑이와 까치 쇼츠 11개 언어」, 「노을이 영상 업로드」)은 API로 공개 업로드, 예약, 썸네일 설정을 이미 하고 있습니다. 클라우드의 Verdict Picks 세션은 그 세션들에 직접 메시지를 보낼 수 없습니다. 아래 글을 그 세션에 그대로 붙여 넣어 주세요.

---

Prof H Lab 유튜브 채널(소유자 계정과 관리자 계정이 있음)에 영상 4편을 API로 올리려고 합니다. 이 세션이 쓰는 업로드 방식을 그대로 쓰고 싶습니다. 아래 순서대로 해 주세요. 키, 토큰, 비밀번호는 채팅에 붙여 넣지 마세요.

1. 이 세션이 유튜브 업로드에 쓰는 방법을 알려 주세요.
   - Google Cloud 프로젝트 이름
   - OAuth 클라이언트 종류(데스크톱/웹)
   - API로 올린 영상이 비공개로 잠기지 않고 바로 공개·예약되는지
   - 썸네일 설정 방법
   - 토큰 파일 위치(내용 말고 위치만)
2. 그 프로젝트의 OAuth 클라이언트로 **채널 소유자 계정의 Prof H Lab 채널** 토큰을 새로 받아 주세요.
   - 범위: `https://www.googleapis.com/auth/youtube.upload`, `https://www.googleapis.com/auth/youtube.force-ssl`
   - 브라우저 동의 화면에서 채널 소유자 계정 → Prof H Lab 채널을 고르면 됩니다.
3. (전화 인증은 2026-11-24에 운영자가 확인함: youtube.com/verify에서 "Phone number verified", 기능 사용 자격요건 "사용 설정됨". 맞춤 썸네일을 API로 설정할 수 있음.)
4. 다음 중 하나를 해 주세요.
   - **(가) 이 세션이 직접 업로드:** 영상과 자료는 아래 주소에 있습니다. 각 json의 `metadata`에는 11개 언어 제목·설명·태그가 있고, 같은 이름의 `.srt` 11개는 언어별 자막입니다.
     - https://actsb.github.io/claudefold/shorts/ep1.mp4 · ep2.mp4 · ep3.mp4 (쇼츠, 세로) · season1.mp4 (롱폼, 가로)
     - https://actsb.github.io/claudefold/shorts/ep1-youtube.json (ep2, ep3, season1도 같은 형식)
     - https://actsb.github.io/claudefold/shorts/ep1.en.srt (언어 코드: en es pt fr de ja ko zh-Hans hi id vi)
     - 썸네일: https://actsb.github.io/claudefold/shorts/ep1-thumb.jpg (ep2, ep3, season1-thumb.jpg)
     - 설정: 아동용 아님, 합성 콘텐츠 아님(사실적이지 않은 만화), 유료 프로모션 없음, 카테고리 노하우/스타일(26), 기본 언어 en
     - 올린 뒤 영상 ID 4개를 알려 주세요.
   - **(나) 클라우드 세션에 권한 넘기기:** 클라우드 환경 cloudfold의 환경 변수에 세 값을 저장하는 방법을 운영자에게 안내해 주세요.
     - `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`
     - 저장은 운영자가 claude.ai의 환경 설정에서 직접 합니다.
     - 그러면 클라우드 세션이 `python3 scripts/youtube_upload.py`로 올리고, 자막·현지화·썸네일까지 넣습니다.

---

## 전화 인증 확인과 하는 법 (운영자님)

**확인**
- 방법 1: 채널 소유자 계정으로 로그인 → https://www.youtube.com/verify 접속. "이미 인증되었습니다"가 나오면 완료입니다.
- 방법 2: YouTube Studio → 설정 → 채널 → **기능 사용 자격요건** → "전화번호 인증이 필요한 기능"이 **사용 설정됨**이면 완료입니다.

**인증하기 (2분)**
1. https://www.youtube.com/verify (Prof H Lab 채널이 선택된 상태)
2. 국가: 대한민국 → 받는 방법: 문자(SMS) 또는 음성 통화 → 휴대폰 번호 입력 → 코드 받기
3. 6자리 코드 입력 → 제출
4. 한 번호로 1년에 인증할 수 있는 채널 수가 정해져 있습니다(보통 2개). 다른 채널에 이미 쓴 번호라 막히면 다른 번호를 쓰세요.

인증되면 15분 넘는 영상, 맞춤 썸네일, 실시간 스트리밍을 쓸 수 있습니다.
