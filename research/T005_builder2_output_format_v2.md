# 빌더 2 출력 형식 개선안 (v2)

## 🎯 목표
- 수강생이 **작업 순서대로** 쉽게 따라할 수 있는 구조
- 씬별로 IMAGE + MOTION 프롬프트 묶기
- **앵커 이미지 생성 단계** 명시
- 복붙 피로도 최소화

---

## 📋 개선된 출력 구조

### 현재 (4개 파일)
```
오마쥬_IMAGE.md (씬 1-8)
오마쥬_MOTION.md (씬 1-8)
변주_IMAGE.md (씬 1-8)
변주_MOTION.md (씬 1-8)
```

### 개선안 (2개 파일 + 워크플로우 통합)
```
오마쥬_WORKFLOW.md (앵커 → 씬별 IMAGE+MOTION)
변주_WORKFLOW.md (앵커 → 씬별 IMAGE+MOTION)
```

---

## 📄 개선된 출력 예시

```markdown
# 🎬 오마쥬 버전 워크플로우

> 원본 영상을 재현하는 프롬프트입니다.
> 생성 순서: 앵커 이미지 → 씬별 이미지 → 모션 영상

---

## 🌟 STEP 0: 앵커 이미지 먼저 생성하세요!

캐릭터 일관성을 위해 **앵커 씬의 이미지를 먼저** 생성합니다.
생성된 이미지를 다른 씬에서 `--cref` 파라미터로 참조하세요.

| 앵커 | 씬 | 설명 |
|------|-----|------|
| 👨 MALE_ANCHOR | Scene 02 | 남자 주인공 얼굴 레퍼런스 |
| 👩 FEMALE_ANCHOR | Scene 05 | 여자 주인공 얼굴 레퍼런스 |

---

## 📍 Scene 01: 남자의 등장
**타임코드:** 00:00.00~00:01.67

### 🖼️ IMAGE 프롬프트

**NanoBanana Pro** (한국어)
```
90년대 빈티지 필름 스타일, 화창한 오후의 교외 주택가...
```
[📋 복사]

**Midjourney V7** (영어)
```
1990s vintage film aesthetic, sunny afternoon... --iw 2.0 --ar 9:16 --v 7 --style raw --cw 50 --stylize 250
```
[📋 복사]

### 🎥 MOTION 프롬프트

**Kling 3.0**
```
Beat 0-2s: Wide shot, static camera looking out from a porch...
Audio: [Ambient: Birds chirping, light wind]
```
[📋 복사]

**Veo 3.1**
```
Subject: Young blond man in denim jacket holding red roses
Action: Walking confidently along red brick path towards the camera
...
```
[📋 복사]

---

## 📍 Scene 02: 기다림 ⭐ MALE ANCHOR
**타임코드:** 00:01.67~00:04.56

> ⚠️ **앵커 씬입니다!** 이 씬의 이미지를 먼저 생성하고, 다른 씬에서 --cref로 참조하세요.

### 🖼️ IMAGE 프롬프트
...

### 🎥 MOTION 프롬프트
...

---

[씬 03-08 동일 구조]

---

## ✅ 작업 체크리스트

- [ ] Scene 02 이미지 생성 (MALE ANCHOR)
- [ ] Scene 05 이미지 생성 (FEMALE ANCHOR)
- [ ] Scene 01 이미지 생성 (--cref로 앵커 참조)
- [ ] Scene 03 이미지 생성
- [ ] Scene 04 이미지 생성
- [ ] Scene 06 이미지 생성
- [ ] Scene 07 이미지 생성
- [ ] Scene 08 이미지 생성
- [ ] 모든 씬 모션 영상 생성
- [ ] 타임라인에 맞게 편집
```

---

## 🔧 빌더 2 프롬프트 수정 사항

### 추가할 지시문

```
출력 형식 지침:
1. 오마쥬와 변주 각각 하나의 통합 워크플로우 파일로 출력
2. 각 씬마다 IMAGE와 MOTION 프롬프트를 함께 묶어서 출력
3. 앵커 씬(⭐ 표시)은 맨 앞에 별도 섹션으로 강조
4. 작업 체크리스트 포함
5. 각 프롬프트 블록 뒤에 [📋 복사] 표시
```

### 삭제할 것
- `<<<OHMAGE_IMAGE_START>>>` 등의 구분자 (웹 파서용이 아니면 불필요)
- "Builder 1의 IMAGE_PROMPTS 내용을 그대로 사용합니다. 생략합니다." → 실제 프롬프트 출력

---

## 💡 추가 개선 아이디어

### 1. QR 코드 / 딥링크
각 프롬프트에 QR 코드 생성 → 폰으로 스캔하면 바로 복사

### 2. Midjourney 봇 연동
`/imagine` 명령어 형태로 출력 → Discord에 바로 붙여넣기 가능

### 3. 진행 상황 트래커
체크리스트를 인터랙티브하게 → 완료한 씬 표시

---

## 🎯 권장 구현 순서

1. **[즉시]** 빌더 2 프롬프트 수정 → 통합 워크플로우 형식으로 출력
2. **[1주일]** Academy 웹에 MD 파서 도구 추가
3. **[선택]** 안티그래비티 어시스턴트 (LLM 기반 가이드)
