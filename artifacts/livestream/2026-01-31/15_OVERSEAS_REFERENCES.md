# 해외 사례/라이브 노하우 레퍼런스 (인용용)

> 목표: 오늘 라이브(14:00–18:00 KST)에서 “우리가 왜 이 구조로 간다”를 뒷받침할 **해외 사례/운영 패턴**을 *인용 가능한 링크 + 한 줄 요약*으로 정리.

---

## A) ‘노코드/대화형 빌드’ 라이브/롱폼 사례 (YouTube)

### 1) You B Tech — *No Coding Required! AI Builds Complete Full Stack Web App from PRD (Live Demo)*
- 링크: https://www.youtube.com/watch?v=GryK032UWVE
- 한 줄: **PRD 한 장 → 앱을 끝까지 완주**를 먼저 보여주며 신뢰를 확보하는 전형적인 패턴.
- 오늘 가져올 운영 포인트
  - 초반 3분에 “오늘 뭘 완주할지” 스코프 선언
  - ‘툴 소개’가 아니라 **입력→검수→산출** 프로세스를 반복 리마인드
  - 텐션 유지를 위해 **Plan B(캡처/녹화/대체 멘트)** 필수

### 2) Building a Full-Stack Website with AI - No Coding Experience
- 링크: https://www.youtube.com/watch?v=MvvrxdePk5Y
- 한 줄: “코딩 경험 없음”을 전면에 두고 **완주**로 설득.
- 오늘 가져올 포인트
  - ‘코드 0줄’은 반복하되, 마지막에 **재현성(로그/버전)**으로 신뢰 마무리

### 3) How To Build & Sell Web Apps With AI In Minutes! (No Code)
- 링크: https://www.youtube.com/watch?v=4SrAzs8wbH8
- 한 줄: 빌드에서 끝내지 않고 **판매/운영(수익화)**로 이어지는 메시지 구조.
- 오늘 가져올 포인트
  - Part 3는 ‘판매’가 아니라 **운영 가능성(결제→제공→로그)**으로 프레이밍

### 4) How to Build A $25,000/Mo Web App in 20 Minutes (Using AI)
- 링크: https://www.youtube.com/watch?v=BSR1rq1CaKc
- 한 줄: “결과 먼저 → 디테일”로 전개해 시청자 이탈을 줄임.
- 오늘 가져올 포인트
  - Part 1 시작에 **Before/After를 먼저 보여주고** 이유를 설명(해외 패턴)

---

## B) 프롬프트 일관성/스토리보드(Sora/Veo) 레퍼런스

### 1) OpenAI Cookbook — *Sora 2 Prompting Guide*
- 링크: https://cookbook.openai.com/examples/sora/sora2_prompting_guide
- 한 줄: **샷(shot)이 달성해야 할 목표를 구체화**하면 일관성과 제어력이 올라간다.
- 오늘 라이브에 적용
  - “스토리보드는 ‘컷 목표의 연쇄’”
  - 우리는 그 목표/제약을 **데이터/룰로 고정**해서 흔들림을 줄인다

### 2) Skywork — *Multi-prompt / multi-shot consistency (Veo 3.1 best practices)*
- 링크: https://skywork.ai/blog/multi-prompt-multi-shot-consistency-veo-3-1-best-practices/
- 한 줄: **0–5s/5–12s 타임코드 기반으로 분할 생성**이 멀티샷 일관성에 유리.
- 오늘 라이브에 적용
  - “스토리보드 기능 대응”을 **타임코드 분할/전환 규칙**으로 설계

---

## C) 결제/수익화(Polar) 레퍼런스 + ‘Stripe/결제 운영’ 라이브 패턴

### Polar 공식 문서/SDK
- 홈: https://polar.sh/
- Sandbox: https://polar.sh/docs/integrate/sandbox
- Adapters: https://github.com/polarsource/polar-adapters
- 한 줄: 샌드박스로 결제 플로우 전체를 검증하고 빠르게 붙일 수 있다.
- 오늘 라이브에 적용
  - Part 3는 ‘수익화’가 아니라 **운영 가능성(결제→즉시 제공→로그)**
  - 실패 대비: 샌드박스/대체 화면/Plan B 멘트

### 결제 라이브 운영 패턴(Stripe 예시)
- Marco Behler Live Coding — Stripe payment integration
  - 인덱스: https://www.marcobehler.com/guides/live-coding
  - Ep1: https://www.youtube.com/watch?v=BIDNKRluql4
  - Ep2: https://www.youtube.com/watch?v=gUqMdwgEAIQ
- 한 줄: **문제→원인→복구**를 라이브에서 숨기지 않고 보여주면 신뢰가 올라간다(=PlanB가 곧 콘텐츠)

---

## D) Claude Code / ‘vibe coding’ 운영 루프 레퍼런스

### InfoWorld — *Vibe coding with Claude Code*
- 링크: https://www.infoworld.com/article/3853805/vibe-coding-with-claude-code.html
- 한 줄: 프로젝트 디렉토리에서 CLI로 **Plan→Build→Iterate** 루프를 빠르게 돌리는 게 핵심.

### Medium — *How I “Vibe Coded” a Live App for $0 Using Claude + GitHub*
- 링크: https://medium.com/@xx.u/how-i-vibe-coded-a-live-app-for-0-using-claude-github-79dbc04d1da2
- 한 줄: GitHub/배포까지 ‘대화로’ 밀어붙이며 **버전/로그**가 신뢰를 만든다.

---

## E) OpenClaw 사용 사례(맥락)

### MiniMax Docs — *Build Your AI Assistant on Telegram with OpenClaw (moltbot)*
- 링크: https://platform.minimax.io/docs/solutions/moltbot

### OpenClaw 공식 문서(텔레그램)
- 링크: https://docs.openclaw.ai/channels/telegram

---

## F) 오늘 라이브에 바로 가져올 ‘레퍼런스 인용 문장’ 3개
1) “해외에서도 PRD 한 장으로 앱을 끝까지 완주하는 라이브가 요즘 표준처럼 굳어지고 있어요. 오늘도 **완주**로 보여드릴게요.”
2) “Sora 쪽 가이드도 결국 ‘샷 목표를 구체화하면 일관성이 올라간다’예요. 우리는 그걸 **데이터/룰로 강제**합니다.”
3) “결제는 판매가 아니라 **운영 가능성**입니다. 결제→즉시 제공→로그가 끊김 없이 돌아가야 서비스예요.”
