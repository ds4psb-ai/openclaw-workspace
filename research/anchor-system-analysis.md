# 🎯 ANCHOR 시스템 전수조사

> **목적**: 레퍼런스(ANCHOR) 이미지 기반 오마쥬 파이프라인 완벽 검증
> **관점**: ANCHOR가 전체 파이프라인에서 어떻게 활용되는가?
> **시작**: 2026-02-05 02:40 KST

---

## 📋 전수조사 체크리스트

### Phase 1: ANCHOR 정의 및 선정
- [ ] ANCHOR란 무엇인가?
- [ ] ANCHOR 씬 선정 기준
- [ ] ANCHOR 씬의 특징

### Phase 2: ANCHOR 이미지 생성 (빌더1)
- [ ] ANCHOR 프레임 추출 방법
- [ ] ANCHOR 이미지 프롬프트 형식
- [ ] ANCHOR 생성 순서 (다른 씬보다 먼저?)

### Phase 3: ANCHOR 참조 시스템 (빌더1)
- [ ] 듀얼 레퍼런스 형식
- [ ] [Image 1: COMPOSITION] vs [Image 2: CHARACTER FACE]
- [ ] 다른 씬에서 ANCHOR 얼굴 참조 방법

### Phase 4: 빌더1 → 빌더2 전달
- [ ] ANCHOR 정보가 어떻게 전달되는가?
- [ ] 빌더2에서 ANCHOR 파싱
- [ ] ANCHOR 활용 방식

### Phase 5: 오마쥬 IMAGE 생성 (빌더2)
- [ ] ANCHOR 기반 캐릭터 변환
- [ ] 한국인 ANCHOR 생성
- [ ] 다른 씬에서 한국인 ANCHOR 참조

### Phase 6: 오마쥬 MOTION 생성 (빌더2)
- [ ] MOTION 프롬프트에서 ANCHOR 활용
- [ ] 캐릭터 일관성 유지 방법
- [ ] Kling Character Lock 기능

### Phase 7: 이미지 생성 도구
- [ ] NanoBanana Pro ANCHOR 참조
- [ ] Midjourney --cref 파라미터
- [ ] ANCHOR 이미지 URL 활용

### Phase 8: 영상 생성 도구
- [ ] Kling Canvas 멀티 이미지 참조
- [ ] Veo 3.1 참조 방식
- [ ] 캐릭터 일관성 유지

---

## 🔍 Phase 1: ANCHOR 정의 및 선정

### ANCHOR란?
- **주인공의 단독 정면 클로즈업** 씬
- 얼굴이 명확하게 보이는 기준 프레임
- 다른 모든 씬에서 **얼굴 참조**로 사용됨

### ANCHOR 선정 기준
```
✅ 주인공 단독 프레임
✅ 정면 또는 3/4 앵글
✅ 얼굴이 크게 보임 (클로즈업)
✅ 조명이 얼굴을 잘 비춤
✅ 감정이 명확 (shy smile 등)
```

### 예시 (kylenutt-parody)
```
Scene 2 ⭐ ANCHOR (00:01.27~00:02.28)
- 파일: ANCHOR_IMG.png
- 길이: 1.01s
- 설명: "아이 단독 정면"
- 목표: "한국 아이 얼굴 확정 → 모든 과거 씬에 재사용"
```

### ANCHOR 생성 순서
```
1. ANCHOR 프레임 추출 (FFmpeg)
2. ANCHOR 이미지 먼저 생성 (다른 씬보다 선행!)
3. GENERATED_ANCHOR.png 저장
4. 다른 씬에서 이 이미지 참조
```

---

## 🔍 Phase 2: ANCHOR 이미지 생성

### ANCHOR 프롬프트 구조

```markdown
[ANCHOR_IMG.png URL]

Exact same composition, lighting, and camera angle.

**Main subject**: Replace the child with a 7-year-old Korean boy:
  - black bowl cut (1990s Korean style)
  - single eyelids
  - shy gentle smile (lips closed)
  - looking at cake
  - Korean skin tone

**Note**: This is a close-up solo shot of the boy.

Keep warm candlelight under-lighting, 1990s home video aesthetic, Kodak Portra grain.

--iw 2.0 --ar 9:16 --v 6.0 --style raw --no western features, caucasian skin, blonde, blue eyes
```

### 핵심 패턴
1. 레퍼런스 이미지 URL 제공
2. "Exact same composition" - 구도 100% 유지
3. "**Main subject**" - 캐릭터 상세 설명
4. "Keep..." - 분위기/미학 유지
5. `--no` - 서양인 특징 명시적 제외

### 출력
→ `GENERATED_ANCHOR.png` 저장 (다른 씬에서 참조용)

---

## 🔍 Phase 3: 듀얼 레퍼런스 시스템 ⭐ (핵심!)

### 듀얼 레퍼런스 형식

```markdown
**[Image 1: COMPOSITION]** [scene01_arrival.png URL]
**[Image 2: CHARACTER FACE]** [GENERATED_ANCHOR.png URL]

**From Image 1**: Copy exact composition, character positions, clothing colors, lighting.
**From Image 2**: Copy the Korean boy's face.
```

### 작동 원리

```
┌─────────────────────────────────────────────────────────┐
│                   듀얼 레퍼런스                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Image 1: COMPOSITION]      [Image 2: CHARACTER FACE]  │
│  ┌─────────────────┐         ┌─────────────────┐        │
│  │ 원본 씬 프레임   │         │ GENERATED_ANCHOR│        │
│  │                 │         │                 │        │
│  │ - 구도          │         │ - 한국인 얼굴    │        │
│  │ - 인물 위치     │    +    │ - 표정          │        │
│  │ - 의상 색상     │         │ - 피부톤        │        │
│  │ - 조명          │         │                 │        │
│  └─────────────────┘         └─────────────────┘        │
│           ↓                           ↓                  │
│           └───────────┬───────────────┘                  │
│                       ↓                                  │
│              ┌─────────────────┐                         │
│              │   새로운 이미지   │                         │
│              │ (구도 + 한국인)  │                         │
│              └─────────────────┘                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Midjourney 파라미터
- `--iw 2.0`: Image Weight (높을수록 레퍼런스 충실)
- `--cw 50`: Character Weight (캐릭터 참조 강도)
- `--cref [URL]`: Character Reference (V7)
- `--no western features`: 서양인 특징 제외

---

## 🔍 Phase 4: 빌더1 → 빌더2 ANCHOR 전달

### 빌더2 파싱 동작
```
1. <<<ANALYSIS>>> 블록에서 씬 구조, ANCHOR 확인
2. 캐릭터 변환표 생성:
   | 원본 | 변환 |
   | Caucasian 6yo | 한국인 7세 남아 |
```

### 캐릭터 변환표
- 빌더1의 캐릭터 프로필 → 한국인으로 매핑
- 주인공, 엄마, 아빠 등 개별 변환 정의

---

## 🚨 Phase 5: 중요 GAP 발견!

### 문제: 빌더2 오마쥬 IMAGE 예시에 듀얼 레퍼런스 누락

**실제 프로젝트 산출물 (IMAGE_PROMPTS.md)**:
```markdown
**[Image 1: COMPOSITION]** [scene01_arrival.png URL]
**[Image 2: CHARACTER FACE]** [GENERATED_ANCHOR.png URL]

**From Image 1**: Copy exact composition...
**From Image 2**: Copy the Korean boy's face.
```

**빌더2 시스템 프롬프트 예시**:
```markdown
**[Image 1: COMPOSITION]** [스크린샷 URL 또는 설명]
                          ↑
              Image 2 (CHARACTER FACE) 누락!
```

### 영향
- 빌더2가 듀얼 레퍼런스 형식을 생성하지 않을 수 있음
- ANCHOR 얼굴 참조가 누락될 수 있음
- 캐릭터 일관성 저하 위험

### 권장 수정
빌더2 시스템 프롬프트의 "올바른 오마쥬 IMAGE 출력 예시"에 추가:
```markdown
**[Image 1: COMPOSITION]** [씬 프레임 URL]
**[Image 2: CHARACTER FACE]** [GENERATED_ANCHOR.png URL]

**From Image 1**: Copy exact composition, character positions, lighting.
**From Image 2**: Copy the Korean boy/girl's face.
```

---

## 🔍 Phase 6: MOTION에서 ANCHOR 활용

### Kling Canvas Elements 시스템 (VIDEO_KLING.md)

```markdown
**Elements 활용법:**
Element 1: 주인공 얼굴 (ANCHOR.png)
Element 2: 씬 구도 (scene.png)
Element 3: (선택) 배경/의상
Element 4: (선택) 소품
```

### 씬별 프롬프트 예시
```markdown
**Elements:**
1. ANCHOR.png (한국 아이 얼굴)
2. scene03_clapping.png (구도)

**Prompt:**
Korean family clapping for birthday boy...
```

### 🚨 GAP 발견: 빌더2에 Elements 미반영

**VIDEO_KLING.md (템플릿)**:
- Elements 섹션으로 ANCHOR + 씬 이미지 참조
- 캐릭터 일관성 유지 방법 명시

**빌더2 시스템 프롬프트**:
- Kling 3.0 Beat System만 정의
- Elements 참조 방법 없음
- MOTION 프롬프트에 ANCHOR 참조 없음

### 영향
- MOTION 프롬프트가 Elements 활용 지침 없이 생성됨
- 사용자가 수동으로 Elements 설정해야 함
- 캐릭터 일관성 저하 가능

### 권장 수정
빌더2 MOTION 프롬프트 형식에 추가:
```markdown
### Scene 01: [제목]

#### Kling 3.0 Elements
\`\`\`
Element 1: GENERATED_ANCHOR.png (캐릭터 얼굴)
Element 2: scene01_generated.png (씬 구도)
\`\`\`

#### [📋 COPY] Prompt
...
```

---

## 🔍 Phase 7: 이미지 생성 도구 (Midjourney)

### PROMPTS_MIDJOURNEY.md (템플릿) - V7 기능

**V7 신규 기능:**
```
--oref [URL]: Omni Reference (얼굴/형태 유지) ← NEW!
--cref [URL]: Character Reference (기존)
--cw 0~100: Character Weight
```

**복수 레퍼런스 형식 (템플릿)**:
```markdown
[scene.png URL] [ANCHOR.png URL]

**[Image 1: COMPOSITION]** - copy exact layout
**[Image 2: CHARACTER]** - copy Korean boy face

--iw 2.0 --oref [ANCHOR.png URL] --cw 50 --ar 9:16 --v 7
```

### 🚨 GAP 발견: 빌더2에 --oref 미반영

**빌더2 시스템 프롬프트**:
```
--iw 2.0 --ar 9:16 --v 7 --style raw --cw 50 --stylize 250 --no western features
                                      ↑
                             --cw만 있고 --oref/--cref 없음!
```

**문제:**
- `--cw` (Character Weight)는 `--cref` 또는 `--oref`와 함께 사용해야 의미 있음
- ANCHOR URL 참조 방법 없음
- 캐릭터 얼굴 일관성 유지 어려움

### 권장 수정
```markdown
--iw 2.0 --ar 9:16 --v 7 --style raw --oref [ANCHOR URL] --cw 50 --stylize 250 --no western features
                                      ↑
                           ANCHOR 참조 추가
```

---

## 🔍 Phase 8: 영상 생성 도구 (Veo 3.1)

### VIDEO_VEO.md (템플릿) - Reference 섹션

```markdown
**Reference:** [ANCHOR.png for boy's face]
**Reference:** [scene04_blowout.png for composition]

**Scene Description:**
Korean family singing happy birthday...
```

### 🚨 GAP 발견: 빌더2 Veo 형식에 Reference 누락

**빌더2 시스템 프롬프트 Veo 형식**:
```
Subject: [Character with clothing/appearance]
Action: [Specific motion with timing cue]
Setting: [Location, time of day, era]
Style: [Film grain, color grading, mood, era aesthetic]
Camera: [Shot type + movement]
Lighting: [Color temperature, direction]
Audio: "Dialogue: ... SFX: ... Ambient: ..."
Constraints: [Negative prompt]
                    ↑
          Reference 섹션 없음!
```

### 권장 수정
빌더2 Veo 형식에 Reference 추가:
```
Reference: [ANCHOR.png for character face], [scene.png for composition]
Subject: ...
Action: ...
...
```

---

## 📊 전수조사 결과 요약

### 발견된 GAP (4개)

| # | 위치 | 문제 | 영향 |
|---|------|------|------|
| 1 | 빌더2 IMAGE 예시 | 듀얼 레퍼런스 누락 (Image 2 없음) | 캐릭터 일관성 저하 |
| 2 | 빌더2 Kling 형식 | Elements 섹션 없음 | ANCHOR 참조 불가 |
| 3 | 빌더2 Midjourney 파라미터 | --oref 없음 | ANCHOR 참조 불가 |
| 4 | 빌더2 Veo 형식 | Reference 섹션 없음 | ANCHOR 참조 불가 |

### 핵심 원인

```
템플릿 문서들 (VIDEO_KLING.md, VIDEO_VEO.md, PROMPTS_MIDJOURNEY.md)
→ ANCHOR 참조 방법 잘 정의됨

빌더2 시스템 프롬프트 (constants.ts)
→ 템플릿 내용이 완전히 반영되지 않음
→ ANCHOR 참조 시스템 불완전
```

### 권장 조치

1. **빌더2 IMAGE 예시** - 듀얼 레퍼런스 추가
2. **빌더2 Kling 형식** - Elements 섹션 추가
3. **빌더2 Midjourney 파라미터** - `--oref [ANCHOR URL]` 추가
4. **빌더2 Veo 형식** - Reference 섹션 추가

---

*전수조사 완료: 2026-02-05 03:00 KST*

