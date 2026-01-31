# 해외 사례/라이브 노하우 레퍼런스 (초안)

> 목표: 오늘 라이브(14–18)에서 “우리가 왜 이 구조로 간다”를 뒷받침할 **해외 유튜버/라이브 운영 패턴**을 짧게 인용 가능하게 정리.

## 1) 라이브에서 ‘코드 거의 없이/AI로 앱 완주’ 류 사례

### You B Tech — *No Coding Required! AI Builds Complete Full Stack Web App from PRD (Live Demo)*
- 링크: https://www.youtube.com/watch?v=GryK032UWVE
- 관찰 포인트(오늘 라이브에 가져올 것)
  - **PRD(요구사항) → 앱 생성**의 “한 번에 완주” 흐름을 먼저 보여줘서 시청자 신뢰를 확보
  - ‘툴 소개’보다 **프로세스(입력→검수→산출)**를 반복적으로 리마인드
  - 라이브에서 막힐 걸 대비한 **Plan B(캡처/녹화/대체 멘트)**가 있어야 텐션이 안 죽음

### (추가 후보) 검색어 기반 큐
- 키워드: "AI agents no code build app", "build and sell web apps with AI no code", "Claude Code step-by-step"
- 목적: 오늘 라이브 전/중간에 2~3개 더 확보해서 ‘해외도 이렇게 한다’ 레퍼런스 강화

## 2) ‘에이전트/자동화’ 운영 관점 노하우(오늘 라이브에 바로 적용)

### 해외 라이브에서 반복되는 운영 패턴(요약)
1) **Scope 선언을 빨리 한다**: 오늘은 3가지만(성능/디자인, 일관성 고도화, 결제)
2) **Before/After를 자주 보여준다**: 20~30분마다 리캡/변화 시각화
3) **실패/지연 멘트가 미리 준비돼 있다**: “지금 처리 중, 그동안 핵심 3줄”
4) **시청자 참여는 질문 포맷을 강제한다**: (직무/상황/원하는 결과)
5) **수익화는 ‘판매’가 아니라 ‘운영 가능성’으로 프레이밍한다**

## 3) OpenClaw/자동화 사용 사례(오늘 라이브의 ‘운영/지속화’ 메시지에 연결)

오늘 우리가 실제로 사용한 운영 패턴(예시)
- 그룹 채널에서 **requireMention=false**로 ‘멘션 없이’ 반응하도록 조정(단, Telegram Privacy Mode 영향)
- cron으로 **5분 루프**를 만들어 “Writer/Reviewer(작성/리뷰) 협업”을 자동 반복
- 산출물은 깃에 커밋하여 **재현성/로그/버전 관리** (라이브 운영 문서 패키지)

→ 오늘 라이브 메시지에 연결: 
- “AI 에이전트는 데모가 아니라, **운영(스케줄/로그/버전)**을 붙이면 서비스가 된다.”

## 4) 프롬프트 일관성/스토리보드(Sora/Veo) 레퍼런스

### OpenAI Cookbook — *Sora 2 Prompting Guide*
- 링크: https://cookbook.openai.com/examples/sora/sora2_prompting_guide
- 가져올 포인트
  - “샷(shot)이 달성해야 할 목표를 구체적으로 쓰면 **일관성과 제어력**이 올라간다”
  - 오늘 라이브 메시지로 변환: **스토리보드는 ‘컷 목표의 연쇄’**이고, 데이터(룰/스키마)가 그 목표를 고정한다

### Skywork — *Multi-prompt / multi-shot consistency (Veo 3.1 best practices)*
- 링크: https://skywork.ai/blog/multi-prompt-multi-shot-consistency-veo-3-1-best-practices/
- 가져올 포인트
  - “시간코드 기반(0–5s, 5–12s…) 스토리보드로 분할 생성” → 오늘의 ‘스토리보드 대응’ 섹션 근거

## 5) 결제/수익화(Polar) 레퍼런스

### Polar 공식 문서/SDK
- 홈: https://polar.sh/
- Sandbox: https://polar.sh/docs/integrate/sandbox
- 어댑터(프레임워크 연동): https://github.com/polarsource/polar-adapters
- 가져올 포인트
  - “PG 심사 없이 카드결제 경험을 빠르게 붙인다”는 메시지를 ‘운영 가능성’으로 프레이밍
  - 오늘 라이브에서 “결제 성공→즉시 제공→로그” 체크리스트 근거

## 6) Claude Code / ‘vibe coding’ 레퍼런스(라이브 운영 루프)

### InfoWorld — *Vibe coding with Claude Code*
- 링크: https://www.infoworld.com/article/3853805/vibe-coding-with-claude-code.html
- 가져올 포인트
  - 프로젝트 디렉토리에서 CLI로 반복 수정하는 루프가 핵심(Plan→Build→Iterate)

### (사례) Medium — *How I “Vibe Coded” a Live App for $0 Using Claude + GitHub*
- 링크: https://medium.com/@xx.u/how-i-vibe-coded-a-live-app-for-0-using-claude-github-79dbc04d1da2
- 가져올 포인트
  - GitHub에 올리고 배포까지 ‘대화로’ 밀어붙이는 플로우 → 오늘 라이브의 “버전/로그/재현성” 메시지 강화

## 7) OpenClaw/Moltbot 사용 사례/레퍼런스(맥락)

### MiniMax Docs — *Build Your AI Assistant on Telegram with OpenClaw (moltbot)*
- 링크: https://platform.minimax.io/docs/solutions/moltbot
- 포인트
  - OpenClaw를 텔레그램에 붙여 ‘상시 접근 가능한 개인 비서’ 패턴 소개

### OpenClaw 공식 문서(텔레그램)
- 링크: https://docs.openclaw.ai/channels/telegram

## 8) 다음 액션(리서치 보강)
- [ ] (유튜브) ‘Claude Code로 앱 만들기’ 라이브/롱폼 해외 영상 2~3개 더 확보(오늘 13:00 전)
- [ ] (유튜브) ‘build and sell web apps with AI’ 류 케이스 1~2개 확보(수익화 파트 근거)
- [ ] 각 레퍼런스에서 **오프닝 훅 1문장 + 구성 3막 + PlanB 문장**만 뽑아 `40_HOST_SCRIPT_KEY_LINES.md`에 반영
