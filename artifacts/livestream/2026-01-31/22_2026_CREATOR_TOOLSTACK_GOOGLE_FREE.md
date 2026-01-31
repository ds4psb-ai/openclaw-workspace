# 2026 AI 영상 제작 크리에이터 툴스택 + Google 무료 축(라이브용)

## 1) 2026 크리에이터들이 쓰는 ‘영상 생성’ 축(대표군)
- Runway (영화/크리에이티브 워크플로)
- Pika (숏폼/밈)
- Kling (모션/표현)
- Luma (시네마틱)
- Sora (내러티브)
- **Google Veo 3.1** (모바일/세로/레퍼런스 기반 일관성)

## 2) Google ‘무료/저비용’로 와 닿는 축
- **NotebookLM(무료 입구)**
  - 소스 기반 답변(출처/인용)
  - Audio Overview(Deep Dive/Brief/Critique/Debate)
- **Google Antigravity(무료 입구)**
  - ‘말로 만드는’ 에이전트 개발 플랫폼(코드 설명 최소, 자연어로 시연)
- **Veo 3.1(유료/크레딧 핵심 엔진)**
  - 4K/60fps, 네이티브 9:16, Ingredients(레퍼런스 이미지 최대 4장), 오디오까지(플랜/크레딧 기반)
  - 포지션: ‘완전 무료’가 아니라 **플러그인형 상위 엔진**

## 3) ‘뾰족한 수’(라이브에서 와… 나오는 설계)
1) **NotebookLM(거장 DNA 질문 5개) → shot_goal/timecode 스토리보드 표 자동 생성**
2) **Mixboard(무드보드/컨셉 보드)**로 색감/구도 후보 2~3안을 뽑고 ‘시각 언어’를 고정
3) Antigravity로 무드보드+스토리보드를 받아 **샷 리스트를 구조화**(Scene/Shot 분리)
4) Render는 플러그인: **Scene=Veo 3.1 / Shot=Kling 2.6**
5) 라이브 후: NotebookLM **Brief(2분)** 오디오를 바이럴 방에 공유(확산 자동화)

## 4) 인용/근거(라이브에서 말할 때)
- Veo 3.1 업데이트(세로 지원, 레퍼런스 기반 일관성, 1080p/4K 업스케일):
  - https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/
- NotebookLM Chat/Audio Overview 공식:
  - https://support.google.com/notebooklm/answer/16179559?hl=en
  - https://support.google.com/notebooklm/answer/16212820?hl=en
- Antigravity:
  - https://www.antigravity.google/
