# Blogger 자동 발행 자격 증명 발급 가이드 (한 번만 하면 됨)

목표: 매일 도는 Routine이 사람 없이 Blogger에 글을 올리려면 클라우드 환경에 세 값이 있어야 합니다.
`BLOGGER_CLIENT_ID`, `BLOGGER_CLIENT_SECRET`, `BLOGGER_REFRESH_TOKEN`. 이 값들은 **환경 설정에만** 저장하고, 저장소 파일이나 채팅에는 절대 넣지 않습니다.

준비: 블로그 소유 계정(profhlab@gmail.com)으로만 로그인한 **크롬 시크릿 창**을 씁니다(다른 계정으로 승인하면 "블로그 없음"으로 실패). 전체 소요 시간 약 15분.

## 1단계 — Google Cloud 프로젝트 만들고 Blogger API 켜기
1. https://console.cloud.google.com 접속 → 처음이면 약관 동의.
2. 화면 위 프로젝트 선택 상자 → **새 프로젝트** → 이름 `Verdict Picks Publisher` → **만들기** → 알림창에서 그 프로젝트 **선택**.
3. 왼쪽 메뉴 ≡ → **API 및 서비스** → **라이브러리** → 검색창에 `Blogger` → **Blogger API v3** → **사용**.

## 2단계 — OAuth 동의 화면(앱 등록)과 "프로덕션" 게시
1. ≡ → **API 및 서비스** → **OAuth 동의 화면** (새 콘솔은 **Google Auth Platform → 개요 → 시작하기**).
2. 앱 정보: 앱 이름 `Verdict Picks Publisher`, 사용자 지원 이메일 `profhlab@gmail.com`.
3. 대상(Audience): **외부(External)**.
4. 연락처 정보: `profhlab@gmail.com` → 정책 동의 → **만들기**.
5. (구 화면에 "범위" 단계가 있으면) **범위 추가 또는 삭제** → 필터에 `blogger` → `https://www.googleapis.com/auth/blogger` 체크 → 업데이트 → 저장 후 계속. 테스트 사용자 단계는 건너뜁니다.
6. **앱 게시(프로덕션)** — 가장 중요: **대상(Audience)** 페이지(또는 동의 화면 요약)에서 게시 상태 "테스트" 옆 **앱 게시** → 확인. 테스트 상태로 두면 리프레시 토큰이 7일 뒤 죽습니다. "확인이 필요할 수 있음" 안내가 떠도 게시는 됩니다. 우리만 쓰는 앱이라 Google 검증은 받지 않아도 되고, 승인할 때 "확인되지 않은 앱" 경고만 한 번 뜹니다.

## 3단계 — OAuth 클라이언트 ID와 보안 비밀 발급
1. ≡ → **API 및 서비스** → **사용자 인증 정보** → 위쪽 **+ 사용자 인증 정보 만들기** → **OAuth 클라이언트 ID**.
2. 애플리케이션 유형: **웹 애플리케이션** (데스크톱 앱을 고르면 다음 단계에서 `redirect_uri_mismatch`로 실패). 이름 `OAuth Playground`.
3. **승인된 리디렉션 URI** → **+ URI 추가** → `https://developers.google.com/oauthplayground` (끝에 슬래시 없음) → **만들기**.
4. 팝업의 **클라이언트 ID**(`…apps.googleusercontent.com`)와 **클라이언트 보안 비밀번호**(`GOCSPX-…`)를 복사해 둡니다. 나중에도 사용자 인증 정보 목록에서 그 클라이언트를 열면 다시 볼 수 있습니다.

## 4단계 — OAuth Playground에서 리프레시 토큰 받기
1. 같은 시크릿 창에서 https://developers.google.com/oauthplayground 접속.
2. 오른쪽 위 **⚙(톱니바퀴)** → **Use your own OAuth credentials** 체크 → **OAuth Client ID**, **OAuth Client secret**에 3단계 값 붙여넣기 → 창 닫기. (OAuth flow: Server-side, Access type: Offline 기본값 그대로.)
3. 왼쪽 **Step 1** 아래 입력칸(Input your own scopes)에 `https://www.googleapis.com/auth/blogger` 입력 → **Authorize APIs**.
4. 계정 선택에서 **profhlab@gmail.com**. "Google에서 확인하지 않은 앱" 화면이 나오면 **고급** → **Verdict Picks Publisher(으)로 이동(안전하지 않음)** → 권한 **허용/계속**.
5. 돌아오면 **Step 2**의 **Exchange authorization code for tokens** 클릭 → 오른쪽에 **Refresh token**(`1//0…`)과 Access token이 표시됩니다. **Refresh token**만 복사합니다(Access token은 1시간짜리라 필요 없음).
   * Refresh token 칸이 비어 있으면 예전에 이미 승인한 앱이라 그렇습니다. https://myaccount.google.com/permissions 에서 `Verdict Picks Publisher` 액세스를 삭제한 뒤 3~5번을 다시 합니다.

## 5단계 — Claude 클라우드 환경에 저장
1. 세션 화면 위 제목줄의 **환경 이름(클라우드 환경)** 클릭 → **Edit(환경 수정)**. 또는 claude.ai/code → **Environments** → 해당 환경 → **Edit**.
2. **API credentials** 섹션이 있으면 거기에, 없으면 **Environment variables**에 세 줄 추가(따옴표·공백 없이):
   * `BLOGGER_CLIENT_ID` = 3단계 클라이언트 ID
   * `BLOGGER_CLIENT_SECRET` = 3단계 보안 비밀
   * `BLOGGER_REFRESH_TOKEN` = 4단계 Refresh token
3. **저장**. 새로 시작하는 세션부터 적용됩니다(이미 열려 있는 세션은 못 읽음). 다음 Routine 실행(매일 09:53 UTC)이 `python3 scripts/publish_blogger.py --check`로 확인한 뒤 밀린 글부터 발행합니다.

## 잘 안 될 때
| 증상 | 원인 → 해결 |
|---|---|
| `redirect_uri_mismatch` | 3단계 URI 오타이거나 데스크톱 유형으로 만듦 → 웹 애플리케이션으로 다시 만들고 URI 정확히 입력 |
| `access_denied`, "테스트 사용자만 접근 가능" | 2단계 앱 게시가 안 됨 → 앱 게시 후 4단계 반복 |
| 며칠 뒤 `invalid_grant` | 테스트 상태에서 발급한 토큰(7일 만료) → 앱 게시 후 4단계 반복 |
| 403 "Blogger API has not been used in project…" | 1단계 API 사용 설정 누락 → 켜고 몇 분 뒤 재시도 |
| `--check`에 "no blogs" | 다른 구글 계정으로 승인 → 시크릿 창에서 profhlab@gmail.com으로 4단계 반복 |
| Refresh token이 안 보임 | 위 4-5의 권한 삭제 후 재승인 |

리프레시 토큰은 유출되면 누구나 블로그에 글을 올릴 수 있으니, 의심되면 https://myaccount.google.com/permissions 에서 앱 액세스를 삭제하면 즉시 무효가 됩니다(그 뒤 4단계만 다시 하면 됨).
