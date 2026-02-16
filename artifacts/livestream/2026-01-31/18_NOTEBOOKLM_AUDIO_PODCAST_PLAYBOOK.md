# NotebookLM ‘Audio Overview’로 라이브를 ‘와!’ 수준으로 업그레이드하는 플레이북

## 왜 이게 ‘와!’ 포인트인가
- NotebookLM의 **Audio Overviews**는 업로드한 소스를 기반으로 AI 호스트들이 ‘대화형 팟캐스트’처럼 **딥다이브 요약**을 만들어줌.
- 핵심: 라이브 중에 만든 산출물/문서/공지/레퍼런스를 즉시 소스로 넣고 → **에피소드로 변환** → 방송 후 확산(바이럴방/클립/요약)까지 끊김 없이 연결.

## 기능 근거(공식 3줄)
- **Audio Overviews는 “업로드한 소스”를 요약하는 AI 호스트 대화(Deep Dive)이며, 소스 내용의 ‘객관적 반영’을 지향**(의견 제조가 아니라 정리/요약)
  - https://support.google.com/notebooklm/answer/16212820?hl=en (Takeaway: 소스 기반 요약 + 객관적 반영 원칙 명시)
- **Audio Overview는 Deep Dive/Brief/Critique/Debate 포맷 + 언어 선택 + 길이/커스텀 프롬프트로 조정 가능** → 라이브 후 “2분 요약(Brief)” 같은 공유용 출력이 바로 나옴
  - https://support.google.com/notebooklm/answer/16212820?hl=en (Takeaway: 동일 공식 문서 내 포맷/언어/길이/프롬프트 커스터마이즈 옵션)
- **Audio Overviews는 50+ 언어로 확장(베타)됐고, Interactive mode는 영어만(베타)** → 한국어로도 ‘확산용’ 출력이 가능하다는 말의 근거가 됨
  - https://workspaceupdates.googleblog.com/2025/04/language-expansion-audio-overviews-notebooklm.html (Takeaway: 50+ languages, interactive English-only)

---

## A) 라이브 전(13:00–13:50) 세팅
1) NotebookLM 노트북 1개 생성: `LIVE_YYYYMMDD`
2) 소스 업로드(최소 5개)
   - 오늘 공지 텍스트(카톡 멘션/유튜브 설명)
   - 라이브 운영 핵심 문서 3–5개
   - 레퍼런스 링크 모음(15_OVERSEAS_REFERENCES.md)
   - Polar 문서 링크/요약(결제 파트 대비)
   - 스토리보드 스키마 템플릿(17_STORYBOARD_SCHEMA_TEMPLATE.md)

3) Chat 설정
   - 스타일: Default 또는 Learning Guide
   - 길이: Shorter(라이브 중 빠르게)
4) 라이브 직전 30초 점검
   - 오늘 라이브 공지/스크립트 최신본이 소스에 포함됐는지 확인(구버전 답변 방지)

---

## B) 라이브 중(‘팟캐스트 제작’이 아니라 ‘진행 보조’로 사용)

### 1) 실시간 Q&A 큐레이션
**Chat 프롬프트 예시(복붙):**
- “오늘 채팅 질문을 3개의 카테고리(성능/일관성/결제)로 묶고, 각 카테고리에서 TOP3 질문과 1문장 답변 방향을 써줘. 출처는 오늘 라이브 문서에서만.”

### 2) ‘다음 30분 진행’ 자동 리캡
- “지금까지 한 일 5줄, 다음에 할 일 5줄로 타임라인을 만들어줘. 라이브에서 읽을 수 있게 말투는 짧게.”

### 3) ‘스토리보드/샷 목표’ 자동 생성
- “방금 만든 기능을 소개하는 30초 데모 영상을 만들 거야. timecode 기반(0–5s/5–12s/…)으로 storyboard 테이블을 작성해줘.”

---

## C) 라이브 후(바이럴/재사용 파이프라인: 진짜 ‘와’)

### 1) Audio Overview를 ‘에피소드’로 뽑는다
- 포맷 추천:
  - Deep Dive: “이번 주말 라이브에서 뭘 만들었는지 + 왜 중요한지”
  - Brief: “2분 요약(사람들이 공유하기 좋음)”
  - Debate: “노코드 에이전트 vs 전통 개발 — 언제 뭐가 이득인가”(바이럴)

### 2) 커스텀 프롬프트(복붙용 추천)
- “대상은 AI 영상 제작/크리에이터. 판매 티 나지 않게. 오늘 만든 시스템의 ‘핵심 통찰 3개’와 ‘다음 행동 3개’를 강조해.”

### 3) 산출물 3종으로 분해
- (1) 2분 오디오(Brief) → 텔레그램/카톡 공유
- (2) 10–15분 오디오(Deep Dive) → 유튜브 커뮤니티/재업로드
- (3) 요약 텍스트(NotebookLM Chat) → 바이럴 방 고정글

---

## D) OpenClaw (구 Moltbot) + NotebookLM 결합 아이디어(자동화)
- OpenClaw는 ‘메신저=리모컨’ 패턴(오늘 우리가 쓰는 방식)이라,
  - 라이브 끝나면: “오늘 라이브 요약/타임스탬프/오디오 생성 체크리스트” 초안을 자동 생성해 바이럴 방에 올리는 루프를 만들 수 있음.

> 안전: 키/토큰/대시보드 노출 금지, 자동화는 **dry-run → 승인(QA) → 실반영 1회** 순서로 시작.
