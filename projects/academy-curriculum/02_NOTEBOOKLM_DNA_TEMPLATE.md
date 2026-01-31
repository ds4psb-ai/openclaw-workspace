# NotebookLM 거장 DNA 질문 템플릿 5개

**용도:** 감독/영상 스타일을 프롬프트 파라미터로 추출

---

## 🎬 템플릿 1: 시각적 DNA 추출

```
이 영상/감독의 시각적 특징을 분석해줘:

1. 색감 (Color Palette)
   - 주요 색상 3가지
   - 명암 대비 정도 (낮음/중간/높음)
   - 색온도 (차가움/중립/따뜻함)

2. 구도 (Composition)
   - 선호하는 프레임 비율
   - 대칭 vs 비대칭
   - 여백 활용 스타일

3. 조명 (Lighting)
   - 자연광 vs 인공광
   - 하드 vs 소프트
   - 특징적인 조명 패턴
```

---

## 🎭 템플릿 2: 서사 DNA 추출

```
이 감독/크리에이터의 스토리텔링 패턴을 분석해줘:

1. 오프닝 훅 (첫 3초)
   - 시작 방식 (질문/충격/미스터리/감정)
   - 첫 프레임 특징

2. 서사 구조
   - 3막 구조 vs 순환 구조 vs 파편 구조
   - 긴장 곡선 패턴

3. 엔딩 스타일
   - 클로징 방식 (CTA/여운/반전/루프)
   - 마지막 프레임 특징

4. 템포
   - 컷 속도 (빠름/중간/느림)
   - 리듬 패턴 (일정/가속/감속)
```

---

## 🎵 템플릿 3: 사운드 DNA 추출

```
이 영상의 사운드 디자인 특징을 분석해줘:

1. 음악 스타일
   - 장르 (신스웨이브/오케스트라/미니멀/힙합 등)
   - BPM 범위
   - 무드 (에너지/우울/긴장/평화)

2. 효과음 패턴
   - 전환 효과음 (우시/타격/앰비언스)
   - 강조 포인트 위치

3. 보이스
   - 나레이션 유무
   - 톤 (권위/친근/미스터리/유머)
   - 속도 (빠름/중간/느림)
```

---

## 🎥 템플릿 4: 카메라 DNA 추출

```
이 영상의 카메라 워크 특징을 분석해줘:

1. 샷 타입 빈도
   - 와이드 : 미디엄 : 클로즈업 비율
   - 특수 샷 (항공/FPV/매크로 등)

2. 카메라 움직임
   - 고정 vs 핸드헬드 vs 짐벌
   - 주요 움직임 (팬/틸트/돌리/오빗/푸시인)
   - 움직임 속도

3. 전환 스타일
   - 컷 vs 디졸브 vs 모션 전환
   - 특징적인 전환 패턴
```

---

## 🧬 템플릿 5: 종합 DNA 프로파일

```
위 분석을 종합해서 "스타일 프로파일"을 만들어줘:

출력 형식:
{
  "style_name": "[감독/크리에이터 이름] 스타일",
  "visual": {
    "palette": ["#색상1", "#색상2", "#색상3"],
    "contrast": "high/medium/low",
    "temperature": "warm/neutral/cool"
  },
  "narrative": {
    "hook_type": "question/shock/mystery/emotion",
    "structure": "3act/circular/fragment",
    "tempo": "fast/medium/slow"
  },
  "audio": {
    "music_genre": "...",
    "bpm_range": "80-120",
    "mood": "..."
  },
  "camera": {
    "movement": "static/handheld/gimbal",
    "primary_motion": "pan/dolly/orbit/fpv",
    "transition": "cut/dissolve/motion"
  },
  "signature_elements": [
    "특징1",
    "특징2",
    "특징3"
  ]
}
```

---

## 💡 사용 방법

### 1단계: NotebookLM에 자료 업로드
- 거장 영상 스크립트/분석 글
- 바이럴 영상 자막/설명

### 2단계: 템플릿으로 질문
- 템플릿 1~4 순서대로 질문
- 또는 템플릿 5로 한 번에

### 3단계: 결과 → Mixboard로
- 추출된 색감/구도 → Mixboard 무드보드
- 키워드 → 이미지 검색/생성

### 4단계: Antigravity로 샷 리스트
- 무드보드 + 스타일 프로파일 → 샷 리스트 생성

---

## 🎯 예시: "웨스 앤더슨 스타일"

```json
{
  "style_name": "웨스 앤더슨 스타일",
  "visual": {
    "palette": ["#F5E6D3", "#E8B4B8", "#A8D8EA"],
    "contrast": "low",
    "temperature": "warm"
  },
  "narrative": {
    "hook_type": "mystery",
    "structure": "chapter",
    "tempo": "medium"
  },
  "camera": {
    "movement": "gimbal",
    "primary_motion": "pan/dolly",
    "transition": "cut",
    "signature": "정중앙 대칭 구도"
  },
  "signature_elements": [
    "파스텔 톤",
    "완벽한 대칭",
    "평면적 구도",
    "빈티지 타이포그래피"
  ]
}
```

---

**작성:** 소미 🐱  
**용도:** NotebookLM → Mixboard → Antigravity 파이프라인
