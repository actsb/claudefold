# Pinterest 자동 핀 설정 가이드 (한 번만)

**어떻게 돌아가나:** 매일 블로그 글이 발행되면 Claude가 `pinterest/pins-*.md`에 핀 문구(제목·설명·대체 텍스트·글 링크)를 준비해 둡니다. **핀은 운영자가 고른 것만 올라갑니다**(아래 규정, 8단계). 운영자가 고르면 GitHub가 `.github/workflows/pinterest.yml`을 실행하고, `scripts/pinterest_pins.py`가 Pinterest API로 세로형 핀을 만듭니다. 같은 보드에 같은 글 링크의 핀이 이미 있으면 건너뛰고, 자동 실행은 한 번에 최대 2개까지만 올려 스팸처럼 보이지 않게 합니다.

**왜 GitHub에서 도나:** Claude 클라우드 환경은 네트워크 정책상 pinterest.com 접속이 막혀 있고, Pinterest는 리프레시 토큰을 **쓸 때마다 새것으로 바꾸고 옛것은 폐기**합니다. GitHub Actions는 Pinterest에 접속할 수 있고, 매 실행마다 새 토큰을 비밀값으로 다시 저장할 수 있습니다. 토큰은 GitHub 비밀값에만 있고 저장소 파일·채팅에는 절대 들어가지 않습니다.

## 먼저 알아둘 Pinterest 규정

* API로 만든 핀이 **다른 사람에게 보이려면** 앱이 **Standard access** 승인을 받아야 합니다. 처음엔 **Trial access**로 시작하며, Trial 동안 만든 핀과 보드는 **본인에게만 보이는 테스트(샌드박스) 핀**입니다.
* Standard 신청에는 **연결 과정을 녹화한 화면 영상**이 반드시 필요합니다(혼자 쓰는 앱이어도 동일). 심사는 보통 1~4주, 더 걸리기도 합니다.
* **핀은 사용자가 하나씩 골라야 합니다.** Pinterest 개발자 가이드라인은 핀을 예약·자동 게시하는 앱에 대해 “the end user must choose each Pin to be published”라고 정합니다. 그래서 이 자동화는 운영자가 고르지 않은 핀은 절대 올리지 않습니다. Claude도 승인 표시를 스스로 넣지 않습니다.
* 핀 **수정** API는 베타라 앱에 따라 막혀 있습니다. 그래서 `fix` 모드는 수정이 거부되면 **기존 핀을 지우고 완전한 새 핀으로 교체**합니다.
* 승인 전에도 자동 핀을 원하면 Pinterest 자체 기능 **RSS 자동 게시**(API·승인 불필요)를 쓸 수 있습니다 → 맨 아래 부록.

## 1단계 — 비즈니스 계정 (1분)
Pinterest → 오른쪽 위 프로필 옆 ∨ → **설정** → **계정 관리** → **비즈니스 계정으로 전환** (무료).

## 2단계 — 블로그 소유 확인 (5분)
1. Pinterest 설정 → **소유권 확인된 계정(Claimed accounts)** → 웹사이트 **확인(Claim)** → **HTML 태그 추가** → `<meta name="p:domain_verify" content="…"/>` 한 줄 복사.
2. Blogger → **테마** → 맞춤설정 옆 **▼** → **HTML 편집** → 맨 위 `<head>` 바로 다음 줄에 붙여넣기 → 저장(디스크 아이콘).
3. Pinterest로 돌아가 **확인(Verify)**. (이 태그는 공개 정보라 채팅으로 보내 주셔도 괜찮습니다. 넣을 위치를 봐 드릴 수 있습니다.)

## 3단계 — Pinterest 개발자 앱 만들기 (5분 + Trial 승인 대기)
1. https://developers.pinterest.com/apps/ → 비즈니스 계정으로 로그인 → **Connect app**(또는 Create app).
2. 입력값:
   * App name: `Verdict Picks Publisher`
   * Company / website: `https://acts39.blogspot.com`
   * Privacy policy URL: `https://acts39.blogspot.com/p/privacy-cookie-policy.html`
   * 용도 설명(영어로 그대로): `Publishes pins for new posts on my own blog (acts39.blogspot.com) to my own Pinterest account. Single user: the blog owner, who chooses each pin before it is published; nothing is pinned without that choice. No other users' data is accessed or stored.`
3. 제출 → **Trial access** 승인 메일을 기다립니다(보통 며칠).
4. 승인 후 My apps → 앱 → **Configure**:
   * **App ID**와 **App secret key**(Show 눌러 복사) → 4단계에서 GitHub 비밀값으로만 저장.
   * **Redirect URIs**에 `https://actsb.github.io/claudefold/tools/pinterest-connect.html` 추가 → Save.

## 4단계 — GitHub 비밀값 3개 (5분)
1. **비밀값 저장용 토큰(PAT)**: https://github.com/settings/personal-access-tokens/new
   * Token name `Verdict Picks Pinterest` · Expiration: 가장 긴 기간
   * Repository access: **Only select repositories** → `actsb/claudefold`
   * Permissions → Repository permissions → **Secrets: Read and write**
   * **Generate token** → 복사 (다시 볼 수 없으니 바로 다음 단계에 붙여넣기)
2. https://github.com/actsb/claudefold/settings/secrets/actions → **New repository secret** 세 번:
   * `PINTEREST_APP_ID` = 앱 ID
   * `PINTEREST_APP_SECRET` = 앱 비밀키
   * `GH_SECRETS_PAT` = 방금 만든 토큰
3. 처음이면 저장소의 **Actions** 탭에서 워크플로 사용을 허용(Enable)해 주세요.

## 5단계 — 연결 (2분, 코드는 바로 사용)
1. https://actsb.github.io/claudefold/tools/pinterest-connect.html 열기 → 앱 ID 입력 → **Pinterest에서 승인하기** → 허용.
2. 돌아온 페이지의 **코드 복사**.
3. https://github.com/actsb/claudefold/actions/workflows/pinterest.yml → **Run workflow** → mode **connect**, code 붙여넣기 → **Run workflow**.
4. 초록 체크 = 연결 완료. `PINTEREST_REFRESH_TOKEN` 비밀값이 자동으로 생기고, 이후 매 실행마다 새것으로 교체됩니다.

## 6단계 — 확인
Run workflow → mode **check** → 로그에 `connected as @계정이름`과 보드 목록이 보이면 정상.

## 7단계 — Standard access 신청 (영상)
1. 녹화 도구: Windows **Win + Alt + R**(Xbox Game Bar) 또는 캡처 도구(Win + Shift + S → 녹화).
2. 녹화 순서(3분 안팎). 핵심은 **핀이 사용자가 하나씩 고른 뒤에만 게시된다**는 것을 보여 주는 것입니다.
   ① 연결 페이지 → Pinterest 승인 화면 → 허용 → 코드 표시
   ② GitHub Actions에서 mode **connect** 실행 → 성공
   ③ mode **list** 실행 → 로그(또는 실행 요약)에서 `your OK` 목록, 즉 운영자의 선택을 기다리는 핀들을 보여 주기
   ④ mode **pin**, target에 그중 글 링크 하나를 붙여넣고 실행 → 로그의 `chosen by the owner: …`와 `pinned: … → https://www.pinterest.com/pin/…`
   ⑤ Pinterest에서 방금 만든 핀 열기
3. developers.pinterest.com → My apps → 앱 → **Upgrade / Request Standard access** → 영상 업로드, 설명은 3단계 용도 설명(영어 문장)을 그대로.

## 8단계 — 승인 후 자동화 켜기와 매일 핀 고르기
https://github.com/actsb/claudefold/settings/variables/actions → **New repository variable** → 이름 `PINTEREST_LIVE`, 값 `true`.

**매일 할 일(1~2분): 올릴 핀 고르기.** 편한 방법 하나를 고르세요.
* **A. 바로 올리기:** https://github.com/actsb/claudefold/actions/workflows/pinterest.yml → **Run workflow** → mode **pin**, target에 올릴 글 링크(여러 개면 띄어쓰기로 구분) → **Run workflow**. 무엇이 기다리는지는 mode **list**로 확인합니다(실행 요약에 링크가 나옵니다). Claude의 매일 보고에도 그날 핀 링크가 적혀 있습니다.
* **B. 미리 승인해 두기:** 해당 월의 `pinterest/pins-2026-10.md`에서 그 핀 항목의 **Alt text** 아래에 빈 줄을 두고 두 줄을 추가해 저장(커밋)합니다.
  ```
  **Approved**
  yes
  ```
  또는 Claude 대화에서 “○○ 글 핀 승인해 줘”라고 하면 Claude가 같은 두 줄을 넣어 줍니다. 저장되면 자동 실행이 그 핀을 올리고, 글이나 이미지가 아직 안 올라왔으면 매일 11:23 UTC(한국 20:23)에 다시 시도합니다.

자동 실행(저장소 변경 시, 매일 20:23)은 **승인된 핀만** 올립니다. 승인 표시가 없는 핀은 몇 달이 지나도 올라가지 않습니다.

## 9단계 — 기존 Levoit 핀 고치기
Run workflow → mode **fix**, target `https://acts39.blogspot.com/2026/09/levoit-core-300p-review-2026.html` → 수정이 거부되면 지우고 제목·설명·대체 텍스트가 모두 들어간 새 핀으로 교체합니다.

## 문제 해결
| 증상 | 해결 |
|---|---|
| 승인 화면 `redirect_uri` 오류 | 3단계 Redirect URI를 연결 페이지 하단 주소와 똑같이 등록 |
| connect 실패 "refused the token request" | 코드가 만료·재사용됨 → 5단계를 처음부터(코드는 받자마자 사용) |
| 매일 실행이 "Invalid refresh token" | 토큰 저장이 한 번 실패한 경우 → 5단계 connect 다시 |
| "GH_SECRETS_PAT is missing" | 4단계 토큰을 비밀값으로 추가 후 connect 다시 |
| 핀이 나만 보임 | 아직 Trial access → 7단계 승인 후 공개 |
| "not online yet" | 글이나 이미지가 아직 안 올라온 것 → 다음 실행에 자동 재시도 |
| 자동 실행이 핀을 하나도 안 올림 | 승인된 핀이 없는 것(정상) → 8단계 A 또는 B로 고르기 |

**보안:** 앱 비밀키·토큰은 GitHub 비밀값에만. 의심되면 Pinterest 개발자 앱에서 비밀키를 재발급하고 5단계를 다시 하면 이전 토큰은 모두 무효가 됩니다.

## 부록 — API 없이 지금 바로: RSS 자동 게시 (선택)
Pinterest 설정 → **핀 일괄 만들기(Bulk create Pins)** → **자동 게시(Auto-publish)** → RSS 주소 `https://acts39.blogspot.com/feeds/posts/default?alt=rss` → 보드 **Best of Amazon 2026** → 저장. (2단계 소유 확인이 먼저 필요, 데스크톱에서만.)
* 장점: 승인·토큰 없이 새 글마다 하루 안에 핀 생성.
* 한계: 이미지는 Pinterest가 글에서 고르고(가로 표지일 가능성), 제목·설명은 글 제목·요약이 그대로 들어갑니다.
* RSS 자동 게시는 운영자가 피드 연결을 직접 켜는 Pinterest 자체 기능이라 위 승인 단계와 무관합니다. 다만 새 글이 모두 자동으로 핀이 됩니다.
* API 자동화가 켜지면 RSS 연결은 해제하세요. 같은 보드라면 스크립트가 이미 있는 링크의 핀을 건너뛰므로 중복은 생기지 않습니다.
