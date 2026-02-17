# 2026 AI 영상 제작 크리에이터 툴스택 + Google 무료/저비용 축(라이브용)

## 1) 2026 크리에이터들이 쓰는 ‘영상 생성’ 축(대표군)
- Runway (영화/크리에이티브 워크플로)
- Pika (숏폼/밈)
- Kling (모션/표현)
- Luma (시네마틱)
- Sora (내러티브)
- **Google Veo 3.1** (레퍼런스 기반 일관성 + 숏폼 친화)

## 2) Google 무료·저비용으로 바로 시작하는 축
- **NotebookLM (무료 입구)**
  - 소스 기반 답변(출처/인용)
  - Audio Overview(Deep Dive/Brief/Critique/Debate)
- **Google Labs의 Antigravity (무료 입구)**
  - ‘말로 만드는’ 에이전트 개발 플랫폼(코드 설명을 최소화하고, 자연어로 시연)
- **Veo 3.1 (유료/크레딧 핵심 엔진)**
  - 포지션: ‘완전 무료’가 아니라 **플러그인형 상위 엔진**
  - 운영 멘트: “무료 구간으로 기획을 끝내고, 렌더 단계에서만 유료 엔진을 선택적으로 사용”

## 3) ‘뾰족한 수’(라이브에서 ‘와…’가 나오는 설계)
1) **NotebookLM(거장 DNA 질문 5개) → shot_goal/timecode 스토리보드 표 자동 생성**
2) **Mixboard(무드보드/컨셉 보드)**로 색감/구도 후보 2–3안을 뽑아 ‘시각 언어’를 고정
3) Antigravity로 무드보드+스토리보드를 받아 **샷 리스트를 구조화**(Scene/Shot 분리)
4) Render는 플러그인: **Scene=Veo 3.1 / Shot=Kling 2.6**
5) 라이브 후: NotebookLM **Brief(2분)** 오디오를 바이럴 채널에 공유(확산 자동화)

## 4) 인용/근거(라이브에서 말할 때: “세 줄”)
- **Veo 3.1 ‘Ingredients to Video’는 레퍼런스 이미지 기반 생성에서 캐릭터/배경/오브젝트 일관성을 강화**(같은 주인공으로 여러 씬 구성에 유리)
  - https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/ (핵심: identity/background/object consistency를 공식적으로 강조)
- **Ingredients to Video는 네이티브 세로(9:16) 출력을 지원** → Shorts/릴스용 데모가 “바로” 됨(크롭 얘기 안 해도 됨)
  - https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/ (핵심: 9:16 portrait mode 지원을 명시)
- **1080p/4K는 ‘네이티브 생성’이 아니라 업스케일 옵션(경로/제품에 따라 지원 범위가 다를 수 있음)** → 라이브에서는 “어디에서 업스케일 되는지”를 같이 말하면 신뢰가 올라감
  - https://arstechnica.com/google/2026/01/googles-updated-veo-model-can-make-vertical-videos-from-reference-images-with-4k-upscaling/ (핵심: 4K/1080p 업스케일과 제공 경로(Flow/API/Vertex AI 등) 언급, 라이브에서는 Google 공식 공지와 함께 교차 확인 권장)

### 라이브 데모 체크리스트(측정 가능)
- [ ] 레퍼런스 이미지 2장으로 **같은 인물/같은 의상** 9:16 클립 2개 생성 → “일관성 차이”를 화면 비교
- [ ] 같은 프롬프트로 **배경만 바꾼 버전 2개** 생성 → “주인공 유지” 확인
- [ ] 최종 1개를 **업스케일 옵션(가능한 경로에서)**로 저장 → “편집용 결과물” 느낌 확인

## 참고 링크(원문)
- Veo 3.1 업데이트(레퍼런스 기반 일관성, 9:16, 1080p/4K 업스케일):
  - https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/
- NotebookLM Chat/Audio Overview 공식:
  - https://support.google.com/notebooklm/answer/16179559?hl=en
  - https://support.google.com/notebooklm/answer/16212820?hl=en
- Antigravity:
  - https://www.antigravity.google/
