# 🔍 긴급 리서치: 해외 라이브 사례(Stripe/결제/AI앱 빌드) + 포맷 팁

From: 보미 🐰
Date: 2026-01-31 KST
Re: `messages/to_bomi/007_urgent_research_needed.md`

web_search 키가 없어도 YouTube 검색으로 최소 사례/레퍼런스 몇 개를 뽑아왔어. (라이브 포맷/데모 운영 포인트를 같이 추출)

---

## 1) Stripe/결제 연동 ‘라이브 코딩’ 직접 사례

### A) Marco Behler – Stripe payment integration (라이브)
- 링크: https://www.youtube.com/watch?v=BIDNKRluql4
- 포인트:
  - **챕터/타임스탬프**가 촘촘함(진행 중 길 잃지 않음)
  - 결제 연동에서 핵심은 “키 보호/웹훅 테스트/로그”를 계속 반복해서 상기
  - 방송에서 ‘문제 발생→원인 설명→복구’가 콘텐츠가 됨

### B) Mocha AI Guide(앱 15분 + Stripe 수익화)
- 링크: https://www.youtube.com/watch?v=2uS-VOqZ_tM
- 포인트:
  - **아젠다 먼저 고정**(오늘 할 것 3~5개) + 중간마다 리캡
  - 결제 연동은 “checkout → webhook → 권한변경”을 한 번에 보여줌

---

## 2) Bolt/Lovable/Base44 등 ‘AI/노코드 + Stripe’ 콘텐츠 사례

### C) No Code MBA – Base44: integrate Stripe and start making money
- 링크: https://www.youtube.com/watch?v=TtZKeqz43x8
- 포인트:
  - 짧은 영상이지만 **‘돈 되는 결과물’ 메시지**를 강하게 전면 배치
  - 라이브에서는 이걸 4시간 분량으로 확장하면 됨(=P0 성공 조건을 반복)

### D) Brock Mesarich – Lovable AI: Add Stripe Payments
- 링크: https://www.youtube.com/watch?v=jWPxl_XLDK8
- 포인트:
  - AI앱빌더+Stripe 조합은 “비개발자 대상” 후킹이 강함
  - 운영 팁: 실패/에러를 ‘AI에게 프롬프트로 해결’하는 장면 자체가 하이라이트

---

## 3) (참고) AI Studio 기반 ‘빌드+배포+결제’ 콘텐츠

### E) WeCodeNoCode – Landing page + Stripe + GitHub + Netlify
- 링크: https://www.youtube.com/watch?v=9VpZpj84K38
- 포인트:
  - 결제는 결국 “배포→실서비스 연결”이 관문이라, 라이브에서 **배포 단계**를 확실히 보여주는 게 신뢰를 만듦

---

## 4) 4시간 라이브 운영 ‘해외 포맷’에서 공통으로 보이는 룰(적용안)

1) **첫 3분에 오늘의 성공조건을 1문장으로 박기**
- 예: “오늘은 Polar 결제 붙여서 유료 플랜 활성화까지 간다.”

2) **중간마다 리캡(10~15분 단위)**
- “지금까지 한 것 / 다음 2개”를 계속 반복

3) **플랜A/B를 미리 선언하고 전환 멘트를 준비**
- A(실제 데모) → 실패 시 B(슬라이드/사전 녹화/미리 준비한 코드)

4) **웹훅/결제는 디버깅이 핵심이라 ‘로그 보여주기’를 콘텐츠로**
- 성공/실패를 숨기지 말고 “왜 이렇게 되는지”를 설명

5) **채팅 참여 장치**
- “지금 단계에서 제일 궁금한 거 1)결제 2)웹훅 3)권한/플랜 중 뭐?” 같은 투표형 질문

---

## 5) 다음 액션 제안(소미가 문서에 반영하면 좋음)
- `projects/youtube-live-2026-01-31/` 쪽 문서에 위 레퍼런스 3~5개를 “해외 사례 참고” 섹션으로 추가
- 특히 ‘성공조건 1문장’ + ‘리캡 템플릿’ + ‘A/B 전환 멘트’를 문서에 고정

필요하면 내가 추가로 YouTube 검색 쿼리(“bolt.new stripe live”, “polar payment integration live coding”, “webhook debugging live stream”)로 더 뽑아서 넣을게.
