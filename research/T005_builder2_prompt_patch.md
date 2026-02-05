# 빌더 2 프롬프트 수정안

## 🎯 목표
빌더 2의 출력 형식을 "작업 순서 중심"으로 변경

---

## 📋 현재 빌더 2 출력 구조 (문제)

```
1. 재현성 검증
2. Hook Genome / Dopamine Radar
3. <<<OHMAGE_IMAGE_START>>> (생략됨)
4. <<<OHMAGE_MOTION_START>>>
   - 씬별 Kling/Veo 프롬프트
5. 변주 옵션 선택
6. <<<VARIATION_IMAGE_START>>>
7. <<<VARIATION_MOTION_START>>>
```

**문제점:**
- IMAGE와 MOTION이 분리되어 있음
- 앵커 단계가 명시되지 않음
- 오마쥬 IMAGE가 "생략"됨

---

## 🔧 수정할 빌더 2 프롬프트 섹션

### 추가할 지시문 (출력 형식)

```markdown
## 출력 형식 지침

1. **통합 워크플로우 형식**으로 출력합니다:
   - 오마쥬: `오마쥬_WORKFLOW.md`
   - 변주: `변주_WORKFLOW.md`

2. 각 워크플로우 파일은 다음 구조를 따릅니다:

### 구조 템플릿

```markdown
# 🎬 [오마쥬/변주] 워크플로우

## 🌟 STEP 0: 앵커 이미지 먼저 생성하세요!

캐릭터 일관성을 위해 **앵커 씬의 이미지를 먼저** 생성합니다.

| 앵커 | 씬 | 용도 |
|------|-----|------|
| 👨 MALE_ANCHOR | Scene [번호] | 남자 주인공 레퍼런스 |
| 👩 FEMALE_ANCHOR | Scene [번호] | 여자 주인공 레퍼런스 |

### 👨 MALE ANCHOR 프롬프트

**Midjourney V7:**
```
[프롬프트]
```

### 👩 FEMALE ANCHOR 프롬프트

**Midjourney V7:**
```
[프롬프트]
```

⚠️ **생성 후 이미지 URL을 복사해두세요!**

---

## 📍 Scene 01: [제목]
**타임코드:** [시작~끝]

### 🖼️ IMAGE 프롬프트

**NanoBanana Pro:**
```
[프롬프트]
```

**Midjourney V7:**
```
[프롬프트 --cref [MALE_ANCHOR_URL] ...]
```

### 🎥 MOTION 프롬프트

**Kling 3.0:**
```
[프롬프트]
```

**Veo 3.1:**
```
[프롬프트]
```

---

[씬 02-08 동일 구조]

---

## ✅ 작업 체크리스트

- [ ] MALE ANCHOR 이미지 생성 (Scene XX)
- [ ] FEMALE ANCHOR 이미지 생성 (Scene XX)
- [ ] Scene 01 이미지 생성
- [ ] Scene 01 모션 생성
- [ ] Scene 02 모션 생성 (이미지는 앵커에서 완료)
[...]
```

3. **중요 규칙:**
   - IMAGE와 MOTION을 각 씬 아래에 함께 배치
   - 앵커 씬(⭐ 표시)은 STEP 0에 별도 섹션으로
   - `<<<OHMAGE_IMAGE_START>>>` 같은 구분자 사용하지 않음
   - 오마쥬 IMAGE 프롬프트를 "생략"하지 말고 전체 출력
   - 각 프롬프트에 `--cref [MALE_ANCHOR_URL]` 또는 `[FEMALE_ANCHOR_URL]` 플레이스홀더 포함

4. **체크리스트 규칙:**
   - 앵커 씬은 이미지만 체크 (모션은 나중에)
   - 나머지 씬은 이미지 + 모션 각각 체크
   - Scene 08 등 인물 없는 씬은 앵커 참조 불필요 표시
```

---

## 📝 실제 수정 예시

### Before (현재)

```markdown
<<<OHMAGE_IMAGE_START>>>
# 🖼️ 오마쥬 IMAGE PROMPTS
(Builder 1의 IMAGE_PROMPTS 내용을 그대로 사용합니다. 사용자가 이미 보유 중이므로 생략합니다.)
<<<OHMAGE_IMAGE_END>>>

<<<OHMAGE_MOTION_START>>>
### 🎬 Scene 01: 남자의 등장
#### [📋 COPY] Kling 3.0
Beat 0-2s: ...

#### [📋 COPY] Veo 3.1
Subject: ...
<<<OHMAGE_MOTION_END>>>
```

### After (개선)

```markdown
# 🎬 오마쥬 워크플로우

## 🌟 STEP 0: 앵커 이미지 먼저 생성하세요!

### 👨 MALE ANCHOR (Scene 02에서 추출)

**Midjourney V7:**
```
1990s romance movie still, medium shot of a man standing on a front porch. 20-year-old Caucasian male, short neat blond hair, sharp features. Wearing a denim jacket over a white t-shirt. Holding a bouquet of red roses, looking up expectantly as if waiting for someone. --ar 9:16 --v 7 --style raw --stylize 250
```

### 👩 FEMALE ANCHOR (Scene 05에서 추출)

**Midjourney V7:**
```
1990s rom-com close-up shot. Front view of a 20s blond woman's face. She is smiling brightly with genuine happiness. Large yellow ribbon in her hair, yellow dress shoulder line visible. --ar 9:16 --v 7 --style raw --stylize 250
```

⚠️ 생성 후 이미지 URL을 복사해두세요!

---

## 📍 Scene 01: 남자의 등장
**타임코드:** 00:00.00~00:01.67

### 🖼️ IMAGE 프롬프트

**NanoBanana Pro:**
```
90년대 빈티지 필름 스타일, 화창한 오후의 교외 주택가...
```

**Midjourney V7:**
```
1990s vintage film aesthetic, sunny afternoon... --cref [MALE_ANCHOR_URL] --ar 9:16 --v 7 --style raw --cw 30 --stylize 250
```

### 🎥 MOTION 프롬프트

**Kling 3.0:**
```
Beat 0-2s: Wide shot, static camera looking out from a porch...
```

**Veo 3.1:**
```
Subject: Young blond man in denim jacket holding red roses...
```

---

## 📍 Scene 02: 기다림 ⭐ MALE ANCHOR
**타임코드:** 00:01.67~00:04.56

> ℹ️ 이 씬의 이미지는 STEP 0에서 이미 생성했습니다. 모션만 생성하세요.

### 🎥 MOTION 프롬프트

**Kling 3.0:**
```
Beat 0-3s: Medium shot, slight handheld movement...
```

---

[계속...]

---

## ✅ 작업 체크리스트

- [ ] MALE ANCHOR 이미지 생성
- [ ] FEMALE ANCHOR 이미지 생성
- [ ] Scene 01 이미지 (--cref로 앵커 참조)
- [ ] Scene 01 모션
- [ ] Scene 02 모션 (이미지는 앵커에서 완료)
- [ ] Scene 03 이미지
- [ ] Scene 03 모션
- [ ] Scene 04 이미지
- [ ] Scene 04 모션
- [ ] Scene 05 모션 (이미지는 앵커에서 완료)
- [ ] Scene 06 이미지
- [ ] Scene 06 모션
- [ ] Scene 07 이미지
- [ ] Scene 07 모션
- [ ] Scene 08 이미지 (앵커 참조 불필요)
- [ ] Scene 08 모션
```

---

## 🔑 핵심 변경 요약

| 항목 | 현재 | 개선 후 |
|------|------|---------|
| 파일 개수 | 4개 | 2개 |
| IMAGE 생략 | "사용자 보유 중" | 전체 출력 |
| 앵커 안내 | 없음 | STEP 0 섹션 |
| --cref 플레이스홀더 | 없음 | `[MALE_ANCHOR_URL]` |
| 씬 구조 | IMAGE만 or MOTION만 | IMAGE + MOTION 묶음 |
| 체크리스트 | 없음 | 포함 |
