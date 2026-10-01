# AdSense 심사 대비 점검표 (2026-10-01 조사·수정)

출처(검색으로 확인): Google 검색 센터 [리뷰 작성 가이드](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews), [이미지 SEO](https://developers.google.com/search/docs/appearance/google-images), [AdSense 게시자 정책](https://support.google.com/adsense/answer/10502938), 여러 승인·거절 사례 글(내용은 2차 자료라 참고용).

## 심사에서 보는 것 → 현재 상태
| 항목 | 상태 |
|---|---|
| 필수 페이지(소개·연락처·개인정보처리방침·제휴 고지) | 있음. 개인정보처리방침 주소는 **/p/privacy-cookie-policy.html** |
| 원본·유용한 콘텐츠(얇은 글, 제휴 링크만 있는 글 금지) | 일일 글은 1,800~4,000단어. 링크만 있는 글 없음 |
| 허위·과장 표시(Misrepresentation) | **수정함**: "tested picks"·"how we tested" 표현 삭제, 소개 페이지에 "직접 실험하지 않고 조사한다 / 일러스트는 우리 것 / AI 보조 + 편집자 검토" 명시 |
| 제휴 고지 | 글 첫 줄, 버튼, 별도 페이지에 있음 |
| 이미지가 크롤러에 보이는가 | 표지는 실제 URL의 JPEG(68KB, alt·크기 지정). 나머지 그림은 글 안 SVG(aria-label 있음) |
| 구조화 데이터 | Article(작성자 = 조직, 날짜, 표지 이미지) + ItemList + FAQPage. 허위 별점 없음 |

## 이미지에 대해 (중요)
* 글 안에 base64로 넣은 이미지는 구글 이미지 검색 색인·og:image에 쓰이지 않고 페이지가 무거워집니다(구글 문서: 소량만). 그래서 **표지는 다시 실제 URL(cover.jpg)** 로 되돌렸고, 장식용 핀 썸네일만 글에 포함합니다.
* 구글은 리뷰 글에서 **직접 찍은 사진·사용 증거**를 높게 봅니다. 우리는 일러스트만 있어서 이 부분이 약점입니다. 대표 글 몇 개는 제품을 직접 구입해 사진을 찍어 넣는 것이 가장 효과적입니다(없는 사진을 만들어 넣지 말 것).

## 직접 해야 할 일 (자동화 불가)
1. Google Cloud OAuth 동의 화면의 **개인정보처리방침 링크를 `https://acts39.blogspot.com/p/privacy-cookie-policy.html` 로 수정**(처음 넣은 /p/privacy-policy.html 은 존재하지 않는 주소).
2. 가능하면 **사용자 지정 도메인** 연결(blogspot 하위 도메인도 가능하지만 승인 확률이 낮다는 경험담이 많음).
3. 글이 충분히 쌓인 뒤 신청: 경험담상 20~25개 이상, 사이트 운영 기간 몇 달. 현재 글 약 13개(일일 글 2개).
4. 승인 후 Blogger 설정 → 수익 창출에서 ads.txt 설정.
5. 글 하단의 "editors" 표현이 실제 운영과 맞는지 확인(맞지 않으면 알려 주세요).
