# 구글 서치콘솔 · 빙 웹마스터 등록 가이드 (2026-10-05 점검 결과 포함)

서치콘솔과 빙의 실제 등록 상태(속성, 색인된 글 수)는 블로그 주인 계정으로 로그인해야만 보입니다. 아래 점검은 검색엔진이 블로그를 읽어 갈 수 있는지를 밖에서 확인한 결과입니다. 다시 점검하려면 GitHub → Actions → **Crawl check** → Run workflow를 누르면 됩니다.

## 점검 결과 (2026-10-05, GitHub 서버에서 접속)

| 항목 | 결과 | 뜻 |
|---|---|---|
| `sitemap.xml` | 정상(200), 글 17개 모두 포함 | 그대로 제출하면 됩니다 |
| `sitemap-pages.xml` | 정상(200), 페이지 11개 | 그대로 제출하면 됩니다 |
| 홈·글의 noindex | 없음 | 색인 가능 |
| 라벨·검색 페이지의 noindex | 없음 | 내용이 얇은 목록 페이지까지 색인될 수 있습니다 → 3단계 |
| `robots.txt` | **404(없음)**, 두 번 확인 | 검색이 막히지는 않습니다(404면 "제한 없음"으로 처리). 다만 블로거 기본 robots.txt에 있는 사이트맵 안내와 `/search` 제외가 빠져 있습니다. "맞춤 robots.txt"가 켜진 채 비어 있을 가능성이 큽니다 → 3단계 |
| 구글 소유 확인 태그 | 없음 | 정상입니다. 블로거 블로그는 같은 구글 계정이면 자동으로 확인됩니다 |
| 빙 소유 확인 태그 | 없음 | 빙은 "서치콘솔에서 가져오기"로 등록하면 태그가 필요 없습니다 |
| 서치콘솔 (운영자 확인, 10월 5일) | `sitemap.xml` 성공: 9/13 제출, 10/5 마지막으로 읽음, 발견 13개. `sitemap-pages.xml` 성공: 9/15 제출, 10/2 마지막으로 읽음, 발견 11개 | 서치콘솔 등록과 사이트맵 제출은 끝났습니다. 13개는 구글이 읽은 시점의 수이고, 10월 4일 글 4개(O-Cedar, NOCO, 베개, 비데)는 다음 번 읽을 때 잡힙니다. 남은 것은 빙 등록과 3장 설정입니다 |

## 1. 구글 서치콘솔 (10분)
1. https://search.google.com/search-console 에 **블로그를 만든 구글 계정**으로 접속합니다.
2. 왼쪽 위 속성 목록에서 `https://acts39.blogspot.com/`을 고릅니다.
   - 목록에 없으면: **속성 추가** → **URL 접두어** → `https://acts39.blogspot.com/` → **계속**. 블로거 블로그는 보통 바로 확인됩니다.
   - 확인 방법을 묻는다면 **HTML 태그**를 고르고, 그 한 줄을 블로거 **테마 → HTML 편집**의 `<head>` 바로 아래에 붙여 넣은 뒤 **확인**을 누릅니다.
3. 왼쪽 메뉴 **Sitemaps** → "새 사이트맵 추가"에 `sitemap.xml`을 넣고 **제출**합니다. 같은 방법으로 `sitemap-pages.xml`도 **제출**합니다. (이 블로그는 둘 다 이미 제출되어 "성공"입니다. 다시 제출할 필요 없습니다.)
   - 둘 다 상태가 **성공**이고, 발견된 URL이 각각 17개와 11개로 나오면 정상입니다(며칠 걸릴 수 있음).
4. **페이지**(색인 생성) 보고서에서 "색인이 생성됨" 수와 "색인이 생성되지 않음"의 사유를 봅니다. "크롤링됨 - 현재 색인이 생성되지 않음"이 많으면 글 품질 신호이니 알려 주세요.
5. **URL 검사**: 맨 위 검색창에 글 주소를 붙여 넣고 → **색인 생성 요청**을 누릅니다.
   - 하루 한도가 작습니다(약 10개). 아래 4장 순서대로 하루 5개씩 하고, 같은 주소를 반복하지 않습니다.
6. 앞으로는 새 글이 올라온 날 그 주소 하나만 색인 요청합니다.

## 2. 빙 웹마스터 도구 (5분)
1. https://www.bing.com/webmasters 에 로그인합니다(Microsoft 계정 또는 구글 계정으로 가능).
2. **Import your sites from GSC**(서치콘솔에서 가져오기) → 구글 계정 허용 → `acts39.blogspot.com` 선택 → **Import**. 소유 확인과 사이트맵이 함께 넘어옵니다.
   - 서치콘솔 등록(1장)이 먼저 되어 있어야 가져오기가 됩니다.
   - 가져오기가 안 되면 **Add site manually** → 주소 입력 → 확인 방법 **HTML Meta Tag** → `msvalidate.01` 한 줄을 블로거 테마 `<head>` 아래에 붙여 넣은 뒤 **Verify**.
3. **Sitemaps** 메뉴에 두 사이트맵이 있는지 봅니다. 없으면 **Submit sitemap**에 전체 주소를 넣습니다: `https://acts39.blogspot.com/sitemap.xml`, `https://acts39.blogspot.com/sitemap-pages.xml`.
4. **URL Submission**에 글 주소를 넣어 제출합니다. 하루 한도는 화면에 나옵니다. 처음 한 번은 17개를 모두 넣어도 됩니다.
5. 빙은 ChatGPT 검색과 Copilot이 쓰는 색인이라, 구글과 함께 등록할 가치가 있습니다.

## 3. 블로거 설정 두 가지 (5분): 설정 → 크롤러 및 색인 생성
1. **맞춤 robots.txt 사용**
   - 켜져 있다면 **끄고 저장**합니다. 블로거 기본 robots.txt(사이트맵 안내, `/search` 제외 포함)가 돌아옵니다. 가장 안전한 방법입니다.
   - 꺼져 있는데도 404라면, 켜고 아래 내용을 **한 글자도 바꾸지 말고** 붙여 넣은 뒤 저장합니다. `Disallow: /` 한 줄만 잘못 들어가도 블로그 전체가 검색에서 사라집니다.
     ```
     User-agent: Mediapartners-Google
     Disallow:

     User-agent: *
     Disallow: /search
     Allow: /

     Sitemap: https://acts39.blogspot.com/sitemap.xml
     Sitemap: https://acts39.blogspot.com/sitemap-pages.xml
     ```
2. **맞춤 robots 헤더 태그 사용**을 켭니다.
   - 홈페이지 태그: `all`
   - 보관함 및 검색 페이지 태그: `noindex`
   - 게시물 및 페이지 태그: `all`
   - `nosnippet`은 고르지 않습니다(AI 답변에서도 빠집니다).
3. 저장한 뒤 Claude에게 "크롤 점검 다시 해 줘"라고 하면 Crawl check로 결과를 확인합니다.

## 4. 색인 요청 순서 (서치콘솔 URL 검사, 하루 5개)
- **1일차** (구글이 아직 발견하지 못한 10월 4일 글 + 세일 글):
  - https://acts39.blogspot.com/2026/09/prime-big-deal-days-2026.html (세일이 10월 6~7일)
  - https://acts39.blogspot.com/2026/10/best-bidet-2026.html
  - https://acts39.blogspot.com/2026/10/noco-gb40-jump-starter-review-2026.html
  - https://acts39.blogspot.com/2026/10/o-cedar-easywring-spin-mop-review-2026.html
  - https://acts39.blogspot.com/2026/10/beckham-hotel-pillows-review-2026.html
- **2일차:**
  - https://acts39.blogspot.com/2026/09/best-robot-vacuums-2026_0205504732.html
  - https://acts39.blogspot.com/2026/09/best-wireless-earbuds-2026.html
  - https://acts39.blogspot.com/2026/09/best-portable-power-stations-2026.html
  - https://acts39.blogspot.com/2026/09/best-smart-glasses-2026.html
  - https://acts39.blogspot.com/2026/09/levoit-core-300p-review-2026.html
- **3일차:**
  - https://acts39.blogspot.com/2026/10/bedsure-heated-throw-review-2026.html
  - https://acts39.blogspot.com/2026/09/best-pet-products-on-amazon-2026.html
  - https://acts39.blogspot.com/2026/09/best-value-dog-essentials-on-amazon-2026.html
  - https://acts39.blogspot.com/2026/09/bissell-little-green-review-2026.html
  - https://acts39.blogspot.com/2026/09/owala-freesip-review-2026.html
- **4일차:**
  - https://acts39.blogspot.com/2026/09/apple-airtag-2-review-2026.html
  - 허브 https://acts39.blogspot.com/p/best-sellers.html
  - 그날의 새 글
- AI 영상 도구 글은 처리 방법을 정할 때까지 요청하지 않습니다(전략 문서 8장).

## 5. (선택) 확인을 자동으로: Search Console API 권한 추가
지금 토큰은 블로거 권한만 있어서, 서치콘솔 데이터는 Claude가 읽을 수 없습니다. 토큰을 한 번 더 발급하면서 서치콘솔 권한을 더하면 매일 루틴이 다음을 자동으로 할 수 있습니다.
- 사이트맵 제출
- 글마다 색인 여부와 마지막 크롤링 날짜 확인(하루 2,000건까지)
- 노출수·클릭수·클릭률·평균 순위를 매일 보고서에 한 줄로

**방법:**
1. Google Cloud Console(블로거 API를 켠 같은 프로젝트) → **API 및 서비스 → 라이브러리** → "Google Search Console API" → **사용**.
2. **OAuth 동의 화면 → 데이터 액세스(범위)** → **범위 추가** → `https://www.googleapis.com/auth/webmasters` → **저장**.
3. `daily/blogger-credentials.md` 4단계를 그대로 하되, Step 1 입력칸에 두 범위를 띄어 써서 넣습니다: `https://www.googleapis.com/auth/blogger https://www.googleapis.com/auth/webmasters` → 두 권한 모두 허용 → Exchange → 나온 **Refresh token**(Access token 아님)을 `BLOGGER_REFRESH_TOKEN`에 다시 저장합니다.

**제한:** 서치콘솔의 "색인 생성 요청" 버튼은 API로 제공되지 않습니다. 구글 Indexing API는 채용 공고·라이브 영상 전용입니다. 그래서 새 글의 색인 요청은 계속 직접 하거나 Claude in Chrome으로 합니다.
