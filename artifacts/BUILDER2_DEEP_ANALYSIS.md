# 🔬 Builder 2 (패러디 오마주 엔진) 심층 분석

> **분석자**: 소미 🐱
> **날짜**: 2026-02-05
> **버전**: V4.0 (builder2-hardened.zip)

---

## 📋 Executive Summary

Builder 2는 **Builder 1 출력 + 원본 영상**을 입력받아 **MOTION 프롬프트 (Kling 3.0 / Veo 3.1)**를 생성하고, **변주 옵션**을 제안하는 도구.

### 핵심 워크플로우
```
Builder 1 출력 (IMAGE) + 영상
    ↓ STEP 1: 재현성 검증 + 바이럴 로직 분석
    ↓ STEP 2: MOTION 프롬프트 생성 (오마주)
    ↓ STEP 3: 변주 옵션 제안 (A/B/C)
    ↓ STEP 4: 변주 프롬프트 출력
4개 파일: 오마주 IMAGE/MOTION + 변주 IMAGE/MOTION
```

---

## 🔍 상세 분석

### 1️⃣ 입력 형식 검증

**Builder 2가 기대하는 Builder 1 출력:**
```
<<<ANALYSIS_START>>>
[씬 테이블, 캐릭터 프로필, Visual Rhyme, 구도 분석]
<<<ANALYSIS_END>>>

<<<IMAGE_PROMPTS_START>>>
[모든 씬 IMAGE 프롬프트]
<<<IMAGE_PROMPTS_END>>>
```

**⚠️ 잠재적 문제 #1: 입력 형식 불일치**

| 문제 | 설명 | 위험도 |
|------|------|:------:|
| Builder 1이 구분자 안 넣음 | `<<<ANALYSIS_START>>>` 등 누락 가능 | 🔴 높음 |
| 수동 작성 프롬프트 | 기존 프로젝트들은 다른 형식 사용 | 🟡 중간 |
| 구분자 오타 | `<<<` vs `<<` 등 | 🟡 중간 |

**검증 방법:**
1. Builder 1을 먼저 돌려서 실제 출력 형식 확인
2. 구분자가 정확히 포함되는지 체크
3. 없으면 Builder 1 프롬프트에 구분자 출력 강제 추가

---

### 2️⃣ STEP 1: 재현성 검증 + 바이럴 로직

**재현성 체크리스트 (5개 카테고리):**

| 카테고리 | 검증 항목 | 중요도 |
|----------|----------|:------:|
| 구도 | 카메라 앵글, 프레이밍, 소실점 | ⭐⭐⭐ |
| 인물 | 얼굴 특징, 의상, 위치 | ⭐⭐⭐ |
| 조명 | 색온도 (3200K/5600K), 그림자 | ⭐⭐ |
| 동작 | 시작/끝 동작, 타이밍 | ⭐⭐ |
| 분위기 | 필름 그레인, 색보정, 시대감 | ⭐ |

**바이럴 로직 분석:**

1. **Hook Genome (첫 0.5-3초)**
   - visual_punch: 시각적 임팩트
   - story_hook: 스토리 훅
   - pattern_break: 패턴 깨기
   - curiosity_gap: 호기심 유발

2. **Dopamine Radar (5축)**
   - visual_spectacle (시각적 스펙터클)
   - audio_stimulation (청각적 자극)
   - narrative_intrigue (서사적 흥미)
   - emotional_resonance (감정적 공명)
   - comedy_shock (코미디/충격)

3. **Causal Chain**: A → B → C → 감정 킥

**⚠️ 잠재적 문제 #2: 검증 정확도**

| 문제 | 설명 | 위험도 |
|------|------|:------:|
| 영상 분석 한계 | Gemini가 모든 프레임 정확히 볼 수 없음 | 🟡 중간 |
| 주관적 스코어링 | 1-10점이 일관성 없을 수 있음 | 🟢 낮음 |
| 바이럴 분석 과신 | Hook Genome 등이 실제로 유용한지? | 🟡 중간 |

---

### 3️⃣ STEP 2: MOTION 프롬프트 생성

**Kling 3.0 Beat System:**

```
Beat Count Rules:
- Scene < 2s: Single Beat only
- Scene 2-4s: 2 Beats
- Scene > 4s: 3+ Beats

Pattern:
Beat 0-2s: [Camera] + [Scene]. IMMEDIATELY [action].
Beat 2-4s: [Continuation action]
Audio: [Character: "대사"] [SFX: 소리] [Ambient: 배경]
Negative: [unwanted elements]
```

**핵심 키워드: `IMMEDIATELY`**
- 동작이 즉시 시작되도록 강제
- 지연, 페이드인 방지

**Veo 3.1 Full Slot Structure:**

```
Subject: [캐릭터 + 의상]
Action: [동작 + 타이밍]
Setting: [장소, 시간대, 시대]
Style: [필름 그레인, 색보정, 분위기]
Camera: [샷 타입 + 무브먼트]
Lighting: [색온도, 방향, 강도]
Audio: "Dialogue: []. SFX: []. Ambient: []"
Constraints: [Negative prompt]
```

**⚠️ 잠재적 문제 #3: MOTION 프롬프트 품질**

| 문제 | 설명 | 위험도 |
|------|------|:------:|
| Veo 길이 제한 | 150-300자 권장, 400자 초과 시 truncate | 🔴 높음 |
| Beat 타이밍 불일치 | 실제 영상과 Beat 구간 안 맞을 수 있음 | 🟡 중간 |
| IMMEDIATELY 미작동 | Kling이 이 키워드 무시할 가능성 | 🟡 중간 |
| Audio 카테고리 | Kling/Veo가 Audio 제대로 처리하나? | 🟡 중간 |
| 씬별 복붙 | "위와 유사한" 패턴 사용 가능성 | 🟡 중간 |

**Quality Guard 확인:**
프롬프트에 게으른 출력 방지 규칙 포함:
- "similar to Scene X" 금지
- "as above" 금지
- "위와 유사한" 금지

→ 하지만 Gemini가 실제로 지키는지 확인 필요

---

### 4️⃣ STEP 3: 변주 옵션

**3가지 변주:**

| 옵션 | 변주율 | 내용 |
|------|:------:|------|
| 🅰️ 안정형 | 8% | 인종/배경만 변경, 소품 디테일 조정 |
| 🅱️ 밸런스형 | 15% | 의상 컬러 변경, 시대적 소품 추가 |
| 🆎 과감형 | 18% | 문화권/스타일 전환 (일본/동남아) |

**⚠️ 잠재적 문제 #4: 변주 품질**

| 문제 | 설명 | 위험도 |
|------|------|:------:|
| 변주율 측정 불가 | 8%/15%/18%가 실제로 그 정도인지? | 🟢 낮음 |
| 변주가 너무 급진적 | 18%라도 원본과 너무 달라질 수 있음 | 🟡 중간 |
| 통제 변수 침범 | 타이밍/구도가 의도치 않게 바뀔 수 있음 | 🟡 중간 |

---

### 5️⃣ STEP 4: 최종 출력

**4개 파일:**
1. `<<<OHMAGE_IMAGE_START>>>` ~ `<<<OHMAGE_IMAGE_END>>>`
2. `<<<OHMAGE_MOTION_START>>>` ~ `<<<OHMAGE_MOTION_END>>>`
3. `<<<VARIATION_IMAGE_START>>>` ~ `<<<VARIATION_IMAGE_END>>>`
4. `<<<VARIATION_MOTION_START>>>` ~ `<<<VARIATION_MOTION_END>>>`

**⚠️ 잠재적 문제 #5: 출력 완전성**

| 문제 | 설명 | 위험도 |
|------|------|:------:|
| 씬 누락 | 일부 씬 프롬프트 빠질 수 있음 | 🔴 높음 |
| 토큰 한계 | 64K 토큰이지만 긴 영상은 부족할 수 있음 | 🟡 중간 |
| 구분자 누락 | `<<<>>>` 태그 안 넣을 수 있음 | 🟡 중간 |

---

## 🎯 테스트 체크리스트

### Phase 1: Builder 1 출력 확인
- [ ] Builder 1에 짧은 영상 (10-15초) 입력
- [ ] STEP 1~4 완료
- [ ] `<<<ANALYSIS_START>>>` 구분자 포함 여부 확인
- [ ] `<<<IMAGE_PROMPTS_START>>>` 구분자 포함 여부 확인
- [ ] 모든 씬 프롬프트 포함 여부 확인

### Phase 2: Builder 2 기본 테스트
- [ ] Builder 1 출력 + 영상 입력
- [ ] STEP 1 재현성 검증 테이블 출력 확인
- [ ] STEP 2 MOTION 프롬프트 형식 확인
  - [ ] Kling Beat System 형식
  - [ ] Veo Slot Structure 형식
  - [ ] 모든 씬 포함
- [ ] STEP 3 변주 옵션 3개 제시 확인
- [ ] STEP 4 4개 파일 구분자 포함 확인

### Phase 3: 실제 생성 테스트
- [ ] Kling 3.0에 MOTION 프롬프트 복붙
- [ ] 영상 생성 결과 원본과 비교
- [ ] 타이밍 일치 여부
- [ ] 동작 일치 여부
- [ ] Veo 3.1 동일 테스트

---

## 🔧 권장 개선사항

### 즉시 적용 가능 (Low-hanging fruit)

1. **Builder 1 구분자 강제**
   ```
   STEP 4 출력 시 반드시 다음 구분자를 사용할 것:
   <<<ANALYSIS_START>>> ... <<<ANALYSIS_END>>>
   <<<IMAGE_PROMPTS_START>>> ... <<<IMAGE_PROMPTS_END>>>
   ```

2. **Veo 길이 체크**
   - 각 Veo 프롬프트 생성 후 길이 확인 지시 추가
   - 300자 초과 시 축약 버전 제공

3. **씬 완전성 체크**
   - "모든 씬을 출력했는지 확인하고, 누락된 씬이 있으면 추가"

### 중기 개선

1. **Beat 타이밍 자동 매핑**
   - Builder 1 타임코드 → Beat 구간 자동 변환

2. **변주 미리보기**
   - 변주 옵션 선택 전 각 옵션의 핵심 변경점 상세 설명

3. **Quality Score 자동화**
   - 재현성 검증 결과를 수치화해서 "7/10 이하면 경고"

---

## 📊 위험도 요약

| 위험 | 설명 | 위험도 | 대응 |
|------|------|:------:|------|
| 입력 형식 불일치 | Builder 1이 구분자 안 넣음 | 🔴 | Builder 1 출력 먼저 확인 |
| Veo 길이 초과 | 400자 넘으면 truncate | 🔴 | 길이 체크 추가 |
| 씬 누락 | 일부 씬 빠짐 | 🔴 | 완전성 체크 추가 |
| Beat 타이밍 | 실제 영상과 불일치 | 🟡 | 수동 조정 필요 |
| 변주 품질 | 원본과 너무 다름 | 🟡 | A(8%) 옵션 권장 |
| IMMEDIATELY 미작동 | Kling이 무시 | 🟡 | 테스트 필요 |

---

## ✅ 오늘 수업 전 필수 테스트

1. **Builder 1** 먼저 테스트
   - umbrella-encounter 영상으로 STEP 1~4 돌리기
   - 구분자 포함 여부 확인

2. **Builder 2** 테스트
   - Builder 1 출력 복붙
   - STEP 1~4 돌리기
   - MOTION 프롬프트 형식 확인

3. **Kling 테스트** (시간 되면)
   - Scene 1개만 MOTION 프롬프트로 생성
   - 원본과 비교

---

## 📚 최신 플랫폼 스펙 확인

### Kling 3.0 (2026.02 기준)

**공식 프롬프트 템플릿:**
```
Subject: (who/what)
Setting: (where)
Action beats: (1–3 short beats)
Camera: (lens + movement + framing)
Lighting: (soft, golden hour, studio, neon, etc.)
Style: (cinematic realism / ad-style / documentary)
Constraints: (no text, no warping, stable face, consistent outfit)
```

**Builder 2 Beat System과 비교:**
- Builder 2: Beat 기반 (0-2s, 2-4s, 4-Ns)
- 공식: Action beats로 1-3개 간략 기술
- **차이점**: Builder 2가 더 시간 구체적, 공식은 더 간결

**Kling 3.0 새 기능:**
- 최대 15초 연속 생성
- 다국어 지원 (한국어 포함)
- 향상된 모션 품질

### Veo 3.1 (Google Cloud 공식 가이드)

**5-Part Formula:**
```
[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]
```

**오디오 지시:**
- 대사: `A woman says, "We have to leave now."`
- SFX: `SFX: thunder cracks in the distance`
- Ambient: `Ambient noise: the quiet hum of a starship bridge`

**해상도/길이:**
- 720p 또는 1080p
- 4, 6, 또는 8초 클립

**Builder 2 Veo 형식과 비교:**
| Builder 2 | 공식 가이드 | 일치 |
|-----------|-------------|:----:|
| Subject | Subject | ✅ |
| Action | Action | ✅ |
| Setting | Context | ✅ |
| Style | Style & Ambiance | ✅ |
| Camera | Cinematography | ✅ |
| Lighting | (Style에 포함) | 🟡 |
| Audio | (대사/SFX/Ambient) | ✅ |
| Constraints | Negative prompts | ✅ |

**결론**: Builder 2 Veo 형식이 공식 가이드와 **잘 맞음**! Lighting만 별도 분리된 것이 차이.

---

## 🎯 최종 권장사항

### 수업 전 필수
1. Builder 1 테스트 → 구분자 확인
2. Builder 2 테스트 → MOTION 형식 확인
3. Kling 1개 씬 테스트 (시간 되면)

### 프롬프트 품질 개선
1. Veo 프롬프트 300자 이내 유지
2. Kling Beat 대신 공식 "Action beats" 형식 고려
3. 씬별 독립 작성 (복붙 금지)

### 장기 개선
1. Builder 1/2 구분자 강제 로직 강화
2. 실제 생성 결과 피드백 반영
3. 플랫폼 업데이트 추적

---

*분석 완료: 2026-02-05 02:30 UTC*
*업데이트: 2026-02-05 02:45 UTC (Kling 3.0, Veo 3.1 스펙 추가)*
*분석자: 소미 🐱*
