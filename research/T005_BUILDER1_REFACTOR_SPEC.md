# 🔧 빌더1 리팩토링 명세서

> **목적:** 빌더1을 단일 통합 빌더로 리팩토링
> **결과:** 1개 MD 파일 출력 (오마쥬 워크플로우 완성본)
> **담당:** 클로드코드 개발자

---

## 📋 현재 vs 목표

### 현재 빌더1 (4단계)
```
STEP 1: 영상 분석 (씬 테이블, 캐릭터, Visual Rhyme, 구도)
STEP 2: Phase 1-2 IMAGE 프롬프트 (Scene 01-04)
STEP 3: Phase 3-4 IMAGE 프롬프트 (Scene 05-08)
STEP 4: 최종 출력 (<<<ANALYSIS>>> + <<<IMAGE_PROMPTS>>>)
```

### 목표 빌더1 (5단계)
```
STEP 1: 영상 분석 (기존 유지)
STEP 2: Phase 1-2 IMAGE 프롬프트 (기존 유지)
STEP 3: Phase 3-4 IMAGE 프롬프트 (기존 유지)
STEP 4: MOTION 프롬프트 생성 ← 신규!
STEP 5: 통합 워크플로우 출력 ← 변경!
```

---

## 🆕 STEP 4: MOTION 프롬프트 생성

### 프롬프트에 추가할 지시문

```markdown
## STEP 4: MOTION 프롬프트 생성

각 씬의 IMAGE 프롬프트를 기반으로 **간단한 MOTION 프롬프트**를 생성합니다.

### 규칙
1. IMAGE가 구체적이므로 MOTION은 **핵심 동작만** 설명
2. 형식: `Beat [시작]-[끝]s: [주요 동작]. [카메라]. Audio: [선택적]`
3. Negative 프롬프트 포함

### 출력 형식 (각 씬마다)

#### [📋 COPY] Kling 3.0:
```
Beat 0-Xs: [주요 동작 1문장]. [카메라 움직임].
Audio: [Ambient: 환경음] [SFX: 효과음]
Negative: [원하지 않는 것들]
```

#### [📋 COPY] Veo 3.1:
```
Subject: [피사체]
Action: [동작]
Camera: [카메라]
Audio: "[오디오 설명]"
Constraints: [제약사항]
```

### 씬별 MOTION 생성 가이드

| Scene | 주요 동작 | 카메라 | Motion Score |
|-------|----------|--------|--------------|
| 01 | 남자가 걸어온다 | Static | 3 |
| 02 | 남자가 위를 올려다본다 | Handheld | 4 |
| 03 | 문이 열리고 여자 등장 | Static (OTS) | 5 |
| 04 | 남자가 미소 짓는다 | Static | 2 |
| 05 | 여자가 머리카락을 넘긴다 | Static | 3 |
| 06 | 차 문을 열어준다 | Pan Left | 6 |
| 07 | 차가 출발한다 | Static | 5 |
| 08 | 정적인 장면 + UI 알림 | Static | 1 |

**중요:** 이미지가 구체적이므로 모션은 간단하게! 복잡한 설명 불필요.
```

---

## 🔄 STEP 5: 통합 워크플로우 출력

### 프롬프트에 추가할 지시문

```markdown
## STEP 5: 통합 워크플로우 출력

모든 정보를 **하나의 워크플로우 MD 파일**로 통합 출력합니다.

### 출력 형식

# 🎬 오마쥬 워크플로우

> Generated: [날짜]
> Builder Version: v8.0 (통합)
> Source: [영상 제목/설명]

---

## 🌟 STEP 0: 앵커 이미지 먼저 생성하세요!

캐릭터 일관성을 위해 **앵커 씬의 이미지를 먼저** 생성합니다.
생성 후 이미지 URL을 복사해두세요!

| 앵커 | 씬 | 용도 |
|------|-----|------|
| 👨 MALE_ANCHOR | Scene [번호] | 남자 주인공 레퍼런스 |
| 👩 FEMALE_ANCHOR | Scene [번호] | 여자 주인공 레퍼런스 |

### 👨 MALE ANCHOR (Scene XX)

**[📋 COPY] Midjourney V7:**
```
[앵커 씬의 Midjourney 프롬프트 - --cref 없이]
```

### 👩 FEMALE ANCHOR (Scene XX)

**[📋 COPY] Midjourney V7:**
```
[앵커 씬의 Midjourney 프롬프트 - --cref 없이]
```

⚠️ **생성 후 이미지 URL을 복사해두세요!**
다른 씬의 `[ANCHOR_URL]` 부분에 붙여넣습니다.

---

## 📍 Scene 01: [제목]
**타임코드:** [시작]~[끝]

### 🖼️ IMAGE 프롬프트

**[📋 COPY] NanoBanana Pro:**
```
[한국어 프롬프트]
```

**[📋 COPY] Midjourney V7:**
```
[영어 프롬프트 --cref [MALE_ANCHOR_URL] 또는 [FEMALE_ANCHOR_URL] 포함]
```

### 🎥 MOTION 프롬프트

**[📋 COPY] Kling 3.0:**
```
Beat 0-Xs: [동작]. [카메라].
Audio: [오디오]
Negative: [제외할 것]
```

**[📋 COPY] Veo 3.1:**
```
Subject: [피사체]
Action: [동작]
Camera: [카메라]
Audio: "[오디오]"
Constraints: [제약]
```

---

## 📍 Scene 02: [제목] ⭐ MALE ANCHOR
**타임코드:** [시작]~[끝]

> ℹ️ 이 씬의 이미지는 STEP 0에서 생성합니다.

### 🖼️ IMAGE 프롬프트
[위와 동일 형식]

### 🎥 MOTION 프롬프트
[위와 동일 형식]

---

[Scene 03-08 동일 구조로 반복]

---

## ✅ 작업 체크리스트

### 이미지 생성
- [ ] MALE ANCHOR 이미지 생성 (Scene XX)
- [ ] FEMALE ANCHOR 이미지 생성 (Scene XX)
- [ ] Scene 01 이미지 (--cref로 앵커 참조)
- [ ] Scene 02 이미지 ← 앵커에서 완료
- [ ] Scene 03 이미지
- [ ] Scene 04 이미지
- [ ] Scene 05 이미지 ← 앵커에서 완료
- [ ] Scene 06 이미지
- [ ] Scene 07 이미지
- [ ] Scene 08 이미지 (앵커 참조 불필요)

### 모션 생성
- [ ] Scene 01 모션
- [ ] Scene 02 모션
- [ ] Scene 03 모션
- [ ] Scene 04 모션
- [ ] Scene 05 모션
- [ ] Scene 06 모션
- [ ] Scene 07 모션
- [ ] Scene 08 모션

---

## 📊 요약 정보

| 항목 | 값 |
|------|-----|
| 총 씬 수 | X |
| 총 영상 길이 | XX.XX초 |
| MALE ANCHOR | Scene XX |
| FEMALE ANCHOR | Scene XX |
| 인물 없는 씬 | Scene XX |

### --cref 사용 가이드

| 씬 | 등장 캐릭터 | --cref 사용 |
|----|------------|-------------|
| 01 | 남자 | `--cref [MALE_ANCHOR_URL] --cw 30` |
| 02 | 남자 (앵커) | 앵커 씬 - URL 생성용 |
| 03 | 남자+여자 | `--cref [MALE_URL] [FEMALE_URL] --cw 50` |
| ... | ... | ... |
```

---

## 📝 구현 체크리스트

### 1. 빌더1 프롬프트 복제
- [ ] 기존 빌더1 프롬프트 백업
- [ ] 새 버전 생성 (v8.0 통합)

### 2. STEP 4 추가
- [ ] MOTION 프롬프트 생성 지시문 추가
- [ ] 씬별 Motion Score 가이드 포함
- [ ] Kling/Veo 형식 템플릿 추가

### 3. STEP 5 수정
- [ ] 기존 분리 출력 → 통합 워크플로우 형식으로 변경
- [ ] STEP 0 앵커 섹션 추가
- [ ] 씬별 IMAGE + MOTION 묶음
- [ ] 체크리스트 추가
- [ ] --cref 가이드 추가

### 4. 테스트
- [ ] 샘플 영상으로 실행
- [ ] 출력물 검증
- [ ] Academy 웹 도우미와 호환 확인

---

## ⚠️ 주의사항

1. **기존 태그 제거**
   - `<<<ANALYSIS_START>>>` 등 분리 태그 제거
   - 통합 형식으로 변경

2. **앵커 씬 식별**
   - 씬 테이블에서 ⭐ ANCHOR 표시된 씬 찾기
   - STEP 0에 해당 씬 프롬프트 배치

3. **--cref 플레이스홀더**
   - 앵커 씬 제외한 모든 씬에 `[MALE_ANCHOR_URL]` 또는 `[FEMALE_ANCHOR_URL]` 삽입
   - --cw 값은 씬 특성에 따라 조절 (클로즈업: 80-100, 와이드: 30-50)

4. **MOTION 간소화**
   - 이미지가 구체적이므로 모션은 핵심만
   - 복잡한 설명 피하기

---

## 📁 파일 경로 (참고)

| 파일 | 용도 |
|------|------|
| 빌더1 프롬프트 | Google AI Studio에서 수정 |
| `/viral-video-automation/builder2-temp/constants.ts` | 빌더2 참고용 |

---

**이 문서를 빌더1 프롬프트에 반영하면 완료!**
