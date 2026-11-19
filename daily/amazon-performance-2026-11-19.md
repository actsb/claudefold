# 아마존 클릭·실적 분석과 다음 계획 (2026-11-19)

## 1. 확인할 수 있는 숫자
아마존 클릭·주문·수익은 운영자님 Associates Central에서만 볼 수 있습니다. 아마존은 제휴 실적용 공개 API를 제공하지 않고, 구글 드라이브에도 Associates 리포트가 없었습니다. 아래는 블로그 쪽에서 확인한 숫자입니다.

| 항목 | 값 | 비고 |
|---|---|---|
| 블로그 조회수 (블로거 통계) | 최근 7일 13, 최근 30일 53, 전체 262 | 11/1에는 30일 92. 운영자 본인 방문과 봇이 섞여 있음 |
| 실제 사이트 글 / 페이지 | 40 / 13 | 11월에 새 글 9개 (TV, 스피커, 도어벨, 킨들, 폰 AI 번들 등) |
| 아마존 링크 | 511개 | 모두 verdictpicks-20 태그 있음 |
| 그중 **검색 결과 페이지** 링크 | **491개 (96%)** | 상품 페이지 링크는 18개 |
| 구매 상자(정확한 모델) 카드 | 87장 (31개 글) | 상품 페이지 링크는 3장뿐 |

**추정 (가정이 들어간 계산):** 월 53회 조회에 아마존으로 넘어가는 비율을 5~20%로 잡으면(업계 자료, 공급자 수치) 월 3~10회 클릭입니다. 클릭의 5~10%가 구매로 이어진다고 보면 월 0.2~1건입니다. 실제 숫자는 Associates Central에서 확인해야 합니다.

## 2. 진단
1. **방문자가 너무 적습니다 (가장 큰 원인).**
   - 링크를 아무리 고쳐도 방문자가 월 50명이면 주문은 거의 0건입니다.
   - 첫 판매 3건(첫 180일 심사, 2027년 2월 중순 마감 추정)을 채우려면 블랙프라이데이·사이버먼데이(11/27~11/30)와 12월 선물 시즌에 방문자를 모아야 합니다.
2. **링크가 구매로 이어지기 어렵습니다.**
   - 96%가 아마존 검색 결과로 갑니다. 검색 결과에는 경쟁 상품과 광고가 섞여 있어, 독자가 우리가 추천한 그 모델을 찾다가 이탈하거나 다른 상품을 삽니다.
   - 다른 상품을 사도 24시간 안이면 수수료는 붙습니다. 하지만 정확한 상품 페이지로 보낼 때보다 구매 확률이 낮다고 봅니다.
3. **측정이 없습니다.**
   - 어느 글에서 아마존 클릭이 나오는지 모릅니다. 블로거 통계는 글별 조회수를 API로 주지 않고, 사이트에 GA4가 없습니다.
4. **운영자님 설정이 아직입니다.**
   - 보관 페이지 noindex, 검색 설명 31개, 블로그 소개문("thousands of Amazon reviews" 문구), 핀터레스트 게시 0개.

## 3. 계획
### A. 측정 (이번 주, 운영자님 15분)
1. **Associates Central 확인:** 보고서 → 기간 "가입 이후" → 클릭, 주문 수량, 수익과 "Link Type"·"Tracking ID"별 표를 캡처해 보내 주세요. 이 숫자가 모든 판단의 출발점입니다.
2. **GA4 연결:**
   - profhlab이 쓰는 같은 구글 애널리틱스 계정에 Verdict Picks용 웹 데이터 스트림을 추가하고(측정 ID G-…), 블로거 → 설정 → Google 애널리틱스 측정 ID에 넣습니다.
   - "향상된 측정"의 외부 링크 클릭이 켜져 있으면 글별 아마존 클릭이 자동으로 기록됩니다.
   - profhlab 주간 측정 루틴에 이 스트림을 함께 보도록 부탁합니다.

### B. 구매 전환 (Claude, 진행 중)
1. **구매 상자 87장을 상품 페이지 링크로 교체합니다** (`amazon.com/dp/ASIN?tag=verdictpicks-20`).
   - 상품 번호(ASIN)는 아마존을 긁지 않고 확인합니다. 제조사 사이트의 "아마존에서 구매" 링크, 또는 검색 결과의 아마존 주소를 두 곳 이상에서 맞춰 봅니다.
   - 확신이 높은 것만 바꾸고, 나머지는 검색 링크로 둡니다.
2. **순서:** 블랙프라이데이 기기 가이드(TV, 스피커, 도어벨, 킨들, 폰 번들)와 방문이 많을 만한 가이드(로봇청소기, 이어폰, 파워스테이션, 비데)부터 바꾸고, 바뀐 글만 다시 발행합니다.
3. **이후 새 글도 구매 상자는 상품 페이지 링크로 쓰도록 매일 작업 규칙에 넣습니다.**

### C. 블랙프라이데이 기간 방문자 (11/19~12/1)
1. **핀터레스트 (운영자님, 하루 10분):** 빠른 핀 페이지에서 블랙프라이데이·기기 가이드 핀부터 하루 5~10개 올립니다. 지금 즉시 방문자를 만들 수 있는 거의 유일한 채널입니다.
2. **profhlab 연결 (profhlab 세션):**
   - 삼성 TV 글 → TV 가이드는 연결됐습니다.
   - Alexa+ 끄기 → 스피커 가이드, Kindle → 킨들 가이드, Ring → 도어벨 가이드 연결을 요청합니다. 지난 28일 노출: Alexa+ 531, Ring 317, Kindle 117.
3. **서치콘솔 (운영자님 10분):** 11월 새 가이드 5개(TV, 스피커, 도어벨, 킨들, 블랙프라이데이 vs 사이버먼데이)에 색인 요청을 합니다.
4. **블로거 설정 3가지 (운영자님, Claude in Chrome 한 문장):** `daily/chrome-tasks.md` 0, 0b, 1, 1b, 2번.

### D. 180일 마감 대비
- 마감까지 3건이 안 되면 계정이 닫힙니다. 나중에 다시 신청할 수 있고, 그동안 쌓은 글과 링크는 그대로 씁니다.
- 지인 구매 부탁, 본인 구매, 쿠폰·유료 광고로 아마존에 직접 보내기는 규정 위반이라 하지 않습니다.
- 제안(승인 필요): 한국어 요약의 "한국에서 직구할 때" 세 줄(`daily/video-analysis-2026-11-05.md` 제안 1). 한국 독자의 amazon.com 구매가 수수료로 인정되는지 Associates 도움말에서 먼저 확인합니다.

## 4. 진행 기록
- **2026-11-19:** 구매 상자 35장(19개 글)을 상품 페이지 링크로 바꾸고 발행했습니다. 상품 번호가 두 출처로 확인된 것만 바꿨습니다(`research/asin-map-2026-11-19.json`). Price Check에도 27개가 반영됐습니다. 매일 작업 규칙(README 0장)에 같은 방식을 넣었습니다.
- **2026-11-19:** 운영자님 아마존 계정이 비밀번호 재설정 뒤 "비정상 활동"으로 임시 잠금됐습니다. 고객센터 문의가 필요합니다.

## 5. 운영자님 확인용: 아직 검색 링크인 구매 상자 (52장)
계정 잠금이 풀린 뒤 아마존 상품 페이지에서 링크 생성 도구(SiteStripe → Text)로 정확한 링크를 만들어 보내 주시면 바꾸겠습니다. low는 아마존 검색 결과 한 곳에서만 확인된 상품 번호, none은 아마존 상품이 아니거나 찾지 못한 경우입니다.

| 상품 | 글 | 확신 | 후보 상품 번호 | 메모 |
|---|---|---|---|---|
| Rabbitgoo No-Pull Dog Harness | dogs | low | B01M8JT6FT | Amazon result title: 'rabbitgoo Dog Harness, No Pull for Large Dogs with 2 Leash Clips'; A |
| KONG Classic (natural rubber, made in the USA) | dogs | low | B0002AR0I8 | Amazon title: 'KONG Classic Stuffable Dog Toy, Natural Rubber Chew, for Large Dogs' (model |
| Earth Rated Dog Poop Bags (270, unscented, refill rolls) | dogs | low | B00LAI9OM6 | Amazon title: 'Earth Rated Dog Poop Bags on Refill Rolls, 270 Bags, Unscented'. Lavender 2 |
| Higgsfield (the rendering half: images, video, the MCP conne | aivideo | none | - | Not an Amazon product (software/subscription sold by the maker); keep the current maker li |
| Claude (the planning half: shot list, prompts, review) | aivideo | none | - | Not an Amazon product (software/subscription sold by the maker); keep the current maker li |
| ElevenLabs (the voice that turns a silent clip into an ad) | aivideo | none | - | Not an Amazon product (software/subscription sold by the maker); keep the current maker li |
| Foldable photo light box, 12–16 inch (with LED strips) | aivideo | none | - | The pick is a generic spec, not one product, so there is no single ASIN to verify; keep th |
| Phone tripod with a ball head and remote | aivideo | none | - | The pick is a generic spec, not one product, so there is no single ASIN to verify; keep th |
| Portable SSD, 1–2 TB (USB-C) | aivideo | none | - | The pick is a generic spec, not one product, so there is no single ASIN to verify; keep th |
| Levoit Core 300-P Air Purifier | levoit300 | low | B07VVK39F7 | Amazon titles for this ASIN read '...Core300-P, White'. Matches the ASIN already on the ca |
| Levoit Core 300-RF Replacement Filter (genuine Original 3-in | levoit300 | low | B07RSZSYNC | Amazon title: 'LEVOIT Core 300 Air Purifier Replacement Filter, 3-In-1 Filter... Core300-R |
| Bedsure Heated Blanket Electric Throw (50 x 60 in) | bedsure-throw | low | B0BZYVG8NW | Amazon title names '...Preheat Function, 6 Heat & 6 Timer (Up to 10H), 8H Auto Off, ETL Ce |
| LUXE Bidet NEO 185 (dual nozzle, non-electric) | bidets2026 | low | B00P2XZIP2 | Amazon title 'LUXE Bidet NEO 185 - Bidet Attachment for Toilet Seat, White'. Matches the c |
| Instant Pot Duo 6-Quart 7-in-1 | instant-pot-duo | low | B00FLYWNYQ | B00FLYWNYQ is the main 'Instant Pot Duo 6 Qt 7-in-1 Electric Pressure Cooker, Stainless St |
| ThermoWorks ThermoPop 2 (instant-read thermometer) | thanksgiving-hosting | low | B0DG6M1TMY | Amazon title names 'ThermoWorks ThermoPop 2 ... Cayenne Pepper Red'. Tom's Guide links a d |
| Cuisinart MultiClad Pro Triple Ply 16-inch Roasting Pan with | thanksgiving-hosting | low | B0041Q409G | Amazon title 'Cuisinart MultiClad Pro 16" Stainless Roasting Pan & Rack'. Do not confuse w |
| Black+Decker ComfortGrip 9-inch Electric Knife | thanksgiving-hosting | low | B01K1JJ80M | Amazon title 'BLACK+DECKER 9 inch Electric Carving Knife, Comfort Grip Handle & Safety Loc |
| OXO Good Grips Good Gravy Fat Separator (4-cup) | thanksgiving-hosting | low | B071F2ZM15 | URL slug 'OXO-Grips-Gravy-Separator-4-Cup'; ASIN lookup describes a clear 4-cup bottom-rel |
| Hamilton Beach Temp Tracker 6-quart Slow Cooker | thanksgiving-hosting | low | B07BB9ZQDY | Amazon slug and review titles name model 33866 (6-quart Set & Forget with probe, black sta |
| Rubbermaid Brilliance Food Storage Containers (10-piece plas | thanksgiving-hosting | low | B01JCNEIC6 | Amazon title 'Rubbermaid Brilliance Food Storage Containers, Set of 5 (10 Pieces), BPA-Fre |
| REDTIGER F7NP 4K Front and Rear Dash Cam | redtiger-f7np | low | B098WVKF19 | Amazon title 'REDTIGER F7NP 4K Dash Cam Front Rear, STARVIS 2 Sensor, Free Card Included'. |
| REDTIGER F7NP 4K dash cam (front and rear) | gifts-car-lovers | low | B098WVKF19 | Same product as card 'redtiger-f7np'. Amazon title 'REDTIGER F7NP 4K Dash Cam Front Rear,  |
| Black+Decker Dustbuster AdvancedClean cordless hand vacuum ( | gifts-car-lovers | low | B006LXOJC0 | Amazon title names '(CHV1410L)'. It is also linked by third-party publishers' affiliate UR |
| Braun 500-lumen rechargeable magnetic work light | gifts-car-lovers | none | - | The pick is the Harbor Freight Braun 500-lumen bar (item 59536), a Harbor Freight store pr |
| Drop Stop car seat gap filler | gifts-car-lovers | low | B00BYH6C1E | Amazon result title 'Drop Stop - The Original Patented Car Seat Gap Filler (AS SEEN ON Sha |
| Hopkins SubZero snow brush and ice scraper (metal-joint tele | gifts-car-lovers | low | B0016GVKAG | Closest match: 'SUBZERO Twist-lock Snowbrush 42"' with a telescoping steel handle. No list |
| Rubbermaid Brilliance Leak-Proof Food Storage Set (10-piece) | rubbermaid-brilliance | low | B01JCNEIC6 | Container mix in the Amazon listing (two 1.3-cup, two 3.2-cup, one 9.6-cup) matches the pi |
| Dreo 1500W PTC Ceramic Space Heater (oscillating, with therm | dreo-heater | low | B0B3MXGBVT | Amazon title 'DREO Atom One Space Heater with Remote, 70°Oscillating... 1500W PTC Ceramic  |
| ThermoWorks ThermoPop 2 instant-read thermometer | gifts-under-50 | low | B0DG6M1TMY | Same product as card 'thermopop'. Amazon title names 'ThermoWorks ThermoPop 2 ... Cayenne  |
| Apple AirTag (2nd generation), single | gifts-under-50 | low | B0GJTFXNRX | Amazon title 'Apple AirTag (2nd Generation): Tracker...' (model MFE94LL/A, single unit). T |
| KONG Classic dog toy (medium) | gifts-under-50 | low | B000AYN7LU | Amazon title 'KONG Classic Stuffable Dog Toy, Natural Rubber Chew, for Medium Dogs'. A 2-p |
| Rubbermaid Brilliance leak-proof food storage set | gifts-under-50 | low | B01JCNEIC6 | 10-piece set from Amazon results only. Tom's Guide links a 44-piece Brilliance set as B07X |
| ChomChom Roller pet hair remover | gifts-under-50 | low | B00BAGTNAQ | Amazon result titled 'ChomChom Roller Pet Hair Remover' (also indexed under /gp/product/). |
| Furhaven Orthopedic Sofa Dog Bed (Large) | furhaven-bed | low | B01JAY07IQ | Amazon title '...Orthopedic Dog Bed for Large/Medium Dogs... For Dogs Up to 55 lbs - Plush |
| Instant Pot Duo 6-Quart 7-in-1 (model 112-0170-01) | instant-pot-models | low | B00FLYWNYQ | Same finding as the instant-pot-duo card: B097TSGT9G's slug carries 112-0170-01 but its pa |
| ThermoWorks ThermoPop 2 | meat-thermometer | low | B0DG6M1TMY | Same product as card 'thermopop'. Amazon title names 'ThermoWorks ThermoPop 2 ... Cayenne  |
| Roku Select Series 55-inch (2026) | smart-tv-privacy | low | B0FXZ21F3X | Amazon title 'Roku 55-Inch Select Series Smart TV 2026-4K (2160p) QLED TV' (model likely 5 |
| LG C6 OLED 55-inch (OLED55C6PUA) | smart-tv-privacy | low | B0GRKGQ8HH | Amazon titles for this ASIN name 'OLED55C6PUA, 2026' (shown as currently unavailable in on |
| Sony Bravia 7 II 55-inch (K55XR70M2) | smart-tv-privacy | low | B0H3DZGCNN | Amazon title 'Sony BRAVIA 7 II 55-Inch True RGB 4K HDR Google TV with Gemini'; ASIN lookup |
| Samsung S90H OLED 55-inch (QN55S90HAEXZA) | smart-tv-privacy | low | B0GPYDMBYX | Amazon title 'Samsung 55-Inch Class S90H Series, OLED, 4K, Smart TV, 2026 Model'; ASIN loo |
| Sunbeam Royal Luxe Microplush Heated Throw (50 x 60 in) | heated-blanket-recalls | low | B008BF2OAK | Amazon title '...Royal Luxe Microplush Heated Blanket, 4 Heat Settings, 4-Hour Auto Shut-O |
| Beautyrest Marselle Oversized Faux Fur Heated Throw (50 x 70 | heated-blanket-recalls | none | - | No listing named 'Marselle' was found. The closest 50x70 Beautyrest faux-fur throws are B0 |
| Apple HomePod mini (2nd generation) | smart-speakers-alexa-plus | low | B0HQF7CCJW | Amazon title 'Apple HomePod mini 2 - White'; ASIN lookup ties it to model MGHK4AM/A. Midni |
| Google Home Speaker | smart-speakers-alexa-plus | none | - | No Amazon listing titled 'Google Home Speaker' was found. A 'Google - Premium Audio Speake |
| Sunbeam Restful Quilted Heated Mattress Pad, Queen (dual con | heating-cost-per-night | low | B0D2DQTHLD | Amazon title 'Sunbeam Restful Quilted Heated Mattress Pad, Queen 80 x 60'; listing summary |
| Reolink Video Doorbell PoE | doorbell-no-subscription | low | B0B7S1HMPC | Amazon title 'REOLINK Video Doorbell PoE 2K Wired Outdoor Security Camera with Chime V2'.  |
| Aqara Doorbell Camera Hub G410 | doorbell-no-subscription | low | B0F6CJ93GS | Amazon title 'Aqara Smart Doorbell Camera G410 with Chime, HomeKit Secure Video, Black'. G |
| TP-Link Tapo D225 | doorbell-no-subscription | low | B0D8MKQ5RC | Amazon title 'Tapo 2K+ Wired or Battery Powered Smart Video Doorbell with Chime, D225'. To |
| Google Pixel 11 Pro (256 GB, unlocked) | phone-ai-bundle-deals | low | B0H832JH4Z | Amazon title 'Google Pixel 11 Pro - Unlocked Smartphone, Gemini - 256 GB - Obsidian' (base |
| Samsung Galaxy S26 Ultra (256 GB, unlocked) | phone-ai-bundle-deals | low | B0G4SWDH8P | Amazon title 'Samsung Galaxy S26 Ultra, Unlocked Android Smartphone, 256GB, Black'. Tom's  |
| Google Pixel 11 (256 GB, unlocked) | phone-ai-bundle-deals | low | B0H8363LHL | Amazon title 'Google Pixel 11 - Unlocked Smartphone, Gemini - 256 GB - Pistachio'. No plai |
| Samsung Galaxy S26 FE (128 GB, unlocked) | phone-ai-bundle-deals | low | B0H7SLXZPB | Amazon title 'Samsung Galaxy S26 FE, Unlocked Phone, Graphite, 128GB' (base colour), Amazo |
