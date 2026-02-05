# 🔬 Builder 2 (패러디 오마주 엔진) 심층 분석 V2

> **분석자**: 소미 🐱
> **날짜**: 2026-02-05
> **버전**: V4.0 (builder2-hardened.zip)
> **연구 시간**: 약 2시간 (웹서칭 + 프롬프트 분석)

---

## 📋 Executive Summary

Builder 2는 **Builder 1 출력 + 원본 영상**을 입력받아:
1. **재현성 검증** (TEXT REPRODUCIBILITY CHECK)
2. **바이럴 로직 분석** (Hook Genome, Dopamine Radar)
3. **MOTION 프롬프트 생성** (Kling 3.0 / Veo 3.1)
4. **변주 옵션 제안** (8%/15%/18%)

---

## 🎯 Part 1: 플랫폼별 프롬프트 최신 스펙

### Kling 3.0 (2026년 2월 기준)

**공식 권장 구조 (fal.ai 가이드):**
```
Scene Setting: 환경 + 조명
Subject Description: 주체 상세
Motion Directives: 움직임 지시
Stylistic Guidance: 스타일
```

**고급 기법:**
- **가중치**: `++sleek red convertible++` (중요 요소 강조)
- **Negative prompts**: "No people, no text overlays, no distortion..."
- **기술 스펙**: "Shot on virtual anamorphic lens, 24mm, f/2.8" (스타일 큐)

**Beat System (Builder 2 방식):**
```
Beat 0-5s: Car speeds past camera left to right, engine roaring.
Beat 5-10s: Drift around corner, tires screeching.
Audio:
0-5s: Engine roar (high RPM), rain pattering on metal
5s: SFX: Tires screeching on wet pavement
```

**✅ Builder 2와 공식 스펙 비교:**
| 요소 | Builder 2 | 공식 권장 | 평가 |
|------|-----------|-----------|:----:|
| 시간 구조 | Beat 기반 (0-2s, 2-4s) | Action beats | ✅ 호환 |
| Audio | [SFX:] [Ambient:] | 별도 Audio 섹션 | ✅ 일치 |
| Negative | "Negative: ..." | "No X, no Y" | ✅ 일치 |
| 카메라 | 텍스트 설명 | 텍스트 설명 | ✅ 일치 |

**⚠️ 주의할 점:**
- 복합 움직임 (360도 회전 + 줌인) → 왜곡 발생 가능
- "maintains exact appearance throughout" 추가 권장
- 길이: Kling 3.0은 최대 15초 지원

---

### Veo 3.1 (Google Cloud 공식 가이드)

**5-Part Formula:**
```
[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]
```

**Audio 지시 문법:**
```
Dialogue (Character, Tone): "Line of dialogue"
SFX: Loud, sharp metallic thud
Ambience: Crowded market, distant synth music
```

**JSON Schema 지원 (고급):**
```json
{
  "camera": { "movement": "tracking_shot", "speed": "fast" },
  "subject": "red sports car drifting",
  "lighting": { "key": "street_lamps", "contrast": "high" },
  "audio": { "sfx": "engine_rev", "ambience": "heavy_rain" }
}
```

**✅ Builder 2와 공식 스펙 비교:**
| 요소 | Builder 2 | 공식 권장 | 평가 |
|------|-----------|-----------|:----:|
| Subject | ✅ | Subject | ✅ 일치 |
| Action | ✅ | Action | ✅ 일치 |
| Setting | ✅ | Context | ✅ 일치 |
| Style | ✅ | Style & Ambiance | ✅ 일치 |
| Camera | ✅ | Cinematography | ✅ 일치 |
| Lighting | 별도 분리 | Style에 포함 | 🟡 약간 다름 |
| Audio | 3카테고리 | 3카테고리 | ✅ 일치 |
| Constraints | ✅ | Negative prompts | ✅ 일치 |

**⚠️ 주의할 점:**
- 최적 길이: 150-300자 (400자 초과 시 truncate)
- 클립 길이: 4, 6, 또는 8초
- 해상도: 720p 또는 1080p

---

## 🧠 Part 2: 바이럴 심리학 분석

### Builder 2의 바이럴 분석 프레임워크

**1. Hook Genome (첫 0.5-3초):**
| 훅 유형 | 설명 | 심리학적 근거 |
|---------|------|---------------|
| visual_punch | 시각적 임팩트 | Surprise trigger |
| story_hook | 스토리 훅 | Curiosity gap |
| pattern_break | 패턴 깨기 | Novelty seeking |
| curiosity_gap | 호기심 유발 | Open loop / Zeigarnik Effect |

**2. Dopamine Radar (5축 0-10):**
| 축 | 설명 | 연구 근거 |
|----|------|-----------|
| visual_spectacle | 시각적 스펙터클 | Aesthetic satisfaction |
| audio_stimulation | 청각적 자극 | Sound = 88% essential (TikTok연구) |
| narrative_intrigue | 서사적 흥미 | Personal stories |
| emotional_resonance | 감정적 공명 | Emotion drives sharing |
| comedy_shock | 코미디/충격 | Humor outperforms other emotions |

**3. Causal Chain:**
- A → B → C → 감정 킥
- Zeigarnik Effect: 미완성 이야기가 기억에 남음
- Sora 2 "Causal Chain Technique"과 동일 원리

### 연구 기반 15가지 바이럴 트리거

| # | 트리거 | 왜 작동하나 | Builder 2 적용 |
|---|--------|-------------|----------------|
| 1 | Surprise | 충격이 주목을 끔 | Hook Genome |
| 2 | Humor | 웃음이 공유를 유발 | Dopamine Radar |
| 3 | Relatability | "나도 그래" 공감 | 변주 옵션 |
| 4 | Nostalgia | 과거 향수 | Visual Rhyme (과거/현재) |
| 5 | Challenges | 참여 욕구 | - |
| 6 | Open Loops | 궁금증 유지 | Hook Genome |
| 7 | Fear/Shock | 두려움이 행동 유발 | Dopamine Radar |
| 8 | Quick How-Tos | 빠른 보상 | - |
| 9 | Aesthetics | 미적 만족 | Dopamine Radar |
| 10 | Contrarian | 논쟁 유발 | - |
| 11 | Personal Stories | 감정적 연결 | Persona JSON |
| 12 | Authority | 신뢰 구축 | - |
| 13 | Countdowns | 리스트 형식 | - |
| 14 | Duets/Reactions | 트렌드 편승 | 변주 옵션 |
| 15 | FOMO | 긴급함 | - |

### 3초 법칙 (The 3-Second Rule)

**연구 결과:**
- 첫 3초 시청자의 65%가 10초 이상 시청
- 첫 3초 시청자의 ~50%가 1분 이상 시청
- 주목 스팬: 3초 미만 (TikTok 분석)

**Builder 2 적용:**
- STEP 1에서 Hook Genome 분석
- 첫 컷의 visual_punch 필수 확인
- "IMMEDIATELY" 패턴으로 즉각적 동작 강제

---

## 🔧 Part 3: Builder 2 세부 분석

### 입력 검증

**Builder 1 출력 형식:**
```
<<<ANALYSIS_START>>>
씬 테이블, 캐릭터 프로필, Visual Rhyme, 구도 분석
<<<ANALYSIS_END>>>

<<<IMAGE_PROMPTS_START>>>
모든 씬 IMAGE 프롬프트
<<<IMAGE_PROMPTS_END>>>
```

**⚠️ 잠재적 문제:**
| 문제 | 위험도 | 대응 |
|------|:------:|------|
| 구분자 누락 | 🔴 높음 | Builder 1 출력 먼저 확인 |
| 형식 불일치 | 🟡 중간 | 수동으로 구분자 추가 |
| 씬 누락 | 🔴 높음 | 완전성 체크 |

### STEP 1: 재현성 검증

**5개 카테고리:**
| 카테고리 | 검증 항목 |
|----------|----------|
| 구도 | Camera angle, framing, vanishing point |
| 인물 | Face features, clothing, positioning |
| 조명 | Color temp (3200K/5600K), shadows |
| 동작 | Start/end actions, timing |
| 분위기 | Film grain, color grading, era cues |

**바이럴 로직:**
- Hook Genome (훅 유형 4가지)
- Dopamine Radar (5축 점수)
- Causal Chain (인과 사슬)

### STEP 2: MOTION 프롬프트 생성

**Kling 3.0 Beat System:**
```
Beat 0-2s: [Camera] + [Scene]. IMMEDIATELY [action].
Beat 2-4s: [Continuation]
Audio: [SFX:] [Ambient:]
Negative: [unwanted]
```

**Beat 개수 규칙:**
- Scene < 2s: Single Beat
- Scene 2-4s: 2 Beats
- Scene > 4s: 3+ Beats

**Veo 3.1 Full Slot:**
```
Subject: [캐릭터 + 의상]
Action: [동작 + 타이밍]
Setting: [장소, 시간대, 시대]
Style: [필름 그레인, 색보정]
Camera: [샷 타입 + 무브먼트]
Lighting: [색온도, 방향]
Audio: "Dialogue: []. SFX: []. Ambient: []"
Constraints: [Negative]
```

**핵심 키워드:**
- `IMMEDIATELY`: 동작 즉시 시작
- `maintains exact appearance throughout`: 외형 일관성
- `stable camera movement`: 안정적 카메라

### STEP 3: 변주 옵션

| 옵션 | 변주율 | 변경 범위 |
|------|:------:|-----------|
| 🅰️ 안정형 | 8% | 소품 디테일만 |
| 🅱️ 밸런스형 | 15% | 의상 컬러, 시대적 소품 |
| 🆎 과감형 | 18% | 문화권/스타일 전환 |

**통제 변수 (80-95% 유지):**
- Timing: 컷 길이, 전환 타이밍
- Composition: 소실점, 삼분할, 인물 위치
- Camera: 앵글, 프레이밍
- Lighting: 색온도, 그림자 방향
- Motion: 동작 타이밍

**변주 가능 (5-20%):**
- Ethnicity: 인종, 얼굴 특징
- Clothing: 의상 스타일
- Props: 소품
- Cultural: 시대/문화권 디테일

### STEP 4: 최종 출력

**4개 파일:**
1. `<<<OHMAGE_IMAGE_START>>>` ... `<<<OHMAGE_IMAGE_END>>>`
2. `<<<OHMAGE_MOTION_START>>>` ... `<<<OHMAGE_MOTION_END>>>`
3. `<<<VARIATION_IMAGE_START>>>` ... `<<<VARIATION_IMAGE_END>>>`
4. `<<<VARIATION_MOTION_START>>>` ... `<<<VARIATION_MOTION_END>>>`

---

## ⚠️ Part 4: 잠재적 문제점 및 해결책

### 문제 #1: 입력 형식 불일치
**증상**: Builder 2가 Builder 1 출력을 파싱 못함
**원인**: 구분자 (`<<<ANALYSIS_START>>>` 등) 누락
**해결**: 
- Builder 1 테스트 후 구분자 확인
- 없으면 수동으로 추가

### 문제 #2: MOTION 프롬프트 품질
**증상**: Kling/Veo에서 예상과 다른 결과
**원인**: 
- 복합 움직임 요청 (회전+줌)
- 프롬프트 너무 길거나 모호
**해결**:
- 단일 움직임으로 분리
- 구체적 동작 명시 ("IMMEDIATELY")
- Veo 300자 이내 유지

### 문제 #3: 씬 누락/축약
**증상**: 일부 씬 프롬프트 빠짐, "위와 유사한" 사용
**원인**: LLM의 게으른 출력
**해결**:
- Quality Guard 규칙 존재 (금지 패턴)
- 출력 후 씬 개수 확인

### 문제 #4: Audio 동기화
**증상**: SFX와 동작 타이밍 불일치
**원인**: Beat 구간과 Audio 타임코드 불일치
**해결**:
- Audio 타임코드를 Beat와 정확히 매칭
- 예: `5s: SFX: Tires screeching` ↔ `Beat 5-10s: tires screeching`

### 문제 #5: 변주가 원본과 너무 다름
**증상**: 18% 변주인데 완전 다른 영상 느낌
**원인**: 통제 변수 침범
**해결**:
- A(8%) 옵션부터 시작
- do_not[] 리스트 확인

---

## 📊 Part 5: 품질 체크리스트

### Builder 1 출력 확인
- [ ] `<<<ANALYSIS_START>>>` 구분자 있음
- [ ] `<<<IMAGE_PROMPTS_START>>>` 구분자 있음
- [ ] 모든 씬 포함 (씬 개수 확인)
- [ ] 타임코드 정밀도 (밀리초)
- [ ] 캐릭터 프로필 완전성

### Builder 2 STEP 1 확인
- [ ] 재현성 검증 테이블 출력
- [ ] 5개 카테고리 모두 체크
- [ ] Hook Genome 분석 포함
- [ ] Dopamine Radar 5축 점수
- [ ] 통제/변주 변수 구분

### Builder 2 STEP 2 확인
- [ ] 모든 씬 MOTION 프롬프트 생성
- [ ] Kling Beat System 형식 준수
- [ ] Veo Full Slot 형식 준수
- [ ] Audio 3카테고리 분리 (Dialogue/SFX/Ambient)
- [ ] "위와 유사한" 패턴 없음

### Builder 2 STEP 3 확인
- [ ] 3가지 변주 옵션 제시
- [ ] 각 옵션의 변경점 명확

### Builder 2 STEP 4 확인
- [ ] 4개 파일 구분자 모두 있음
- [ ] 오마주 IMAGE/MOTION
- [ ] 변주 IMAGE/MOTION
- [ ] 씬 누락 없음

---

## 🎓 Part 6: 패러디/오마주 법적 고려

**Fair Use 4가지 요소:**
1. 목적 및 성격 (상업적 vs 교육적)
2. 원본 저작물의 성격
3. 사용된 양과 비중
4. 원본의 시장 가치에 미치는 영향

**패러디 vs 풍자:**
- **패러디**: 원본 자체를 비평/논평 → Fair Use 인정 가능성 높음
- **풍자**: 원본을 도구로 사회 비평 → Fair Use 인정 어려움

**Builder 2의 변주는:**
- "오마주" (원본 존중, 구도/분위기 유지)
- 캐릭터만 변경 → 교육적/창작적 목적으로 해석 가능
- 상업적 사용 시 주의 필요

---

## 📝 Part 7: 최종 권장사항

### 즉시 적용

1. **Builder 1 → Builder 2 연결 확인**
   - Builder 1 먼저 테스트
   - 구분자 출력 여부 확인
   - 없으면 Builder 1 프롬프트에 강제 지시 추가

2. **Veo 프롬프트 길이 관리**
   - 300자 이내 유지
   - 초과 시 핵심만 남기고 축약

3. **씬 완전성 체크**
   - 출력 후 씬 개수 확인
   - "위와 유사한" 패턴 검색

### 수업 시 팁

1. **먼저 A(8%) 옵션으로 시작**
   - 안정적 결과
   - 원본과 비교 용이

2. **Audio 동기화 확인**
   - SFX 타임코드와 Beat 매칭
   - 불일치 시 수동 조정

3. **복합 움직임 피하기**
   - "360도 회전하면서 줌인" → 왜곡
   - 단일 움직임으로 분리

---

## 📚 참고 자료

### 웹 리서치 출처
- fal.ai Kling 2.6 Pro Prompt Guide
- Google Cloud Veo 3.1 Ultimate Prompting Guide
- Medium: "How to Actually Control Next-Gen Video AI"
- Clipwise: "15 Psychology Triggers for Viral Videos"
- JoinBrands: "3 Hooks That Make Videos Go Viral"

### Builder 2 내부 문서
- `viral-video-automation/builder2-hardened.zip`
- `viral-video-automation/projects/umbrella-parody/`
- `viral-video-automation/projects/kylenutt-parody/`

---

## 🎬 Part 8: 실전 팁 (웹 리서치 기반)

### Kling AI 프롬프트 팁

**공식 프롬프트 구조:**
```
Subject + Subject Description + Subject Movement + Scene + Scene Description
+ [Camera Language] + [Lighting] + [Atmosphere]
```

**핵심 팁:**
1. **단순함 유지**: 5-10초에 적합한 시각적 콘텐츠
2. **숫자 피하기**: "5 trees"보다 "several trees" (AI가 숫자 일관성 어려움)
3. **복잡한 물리 주의**: 공 튀기기, 던지기 궤적 → 실패 가능성 높음
4. **다중 주체 주의**: 여러 캐릭터가 다른 행동 → AI가 같은 행동으로 통일시킴

**카메라 움직임 (Kling):**
| 타입 | 옵션 |
|------|------|
| Horizontal | Move left, Move right |
| Vertical | Move up, Move down |
| Zoom | In, Out |
| Pan | Up, Down (주의: 전통적 의미와 다름!) |
| Tilt | Left, Right |
| Roll | Left, Right |
| 특수 | 360 rotation (10초 필요) |

**Image-to-Video 프롬프트:**
- 구조: `Subject + Movement, Background + Movement`
- 씬 설명 불필요 (이미지가 제공)
- 주체와 움직임만 명시

### 캐릭터 일관성 Best Practices

**Anchor System 원리:**
1. 고해상도 레퍼런스 이미지 → AI가 "identity anchor" 구축
2. 모든 후속 생성에서 동일 아이덴티티 유지
3. 장소/의상 변경해도 얼굴 특징 유지

**Builder 2의 Anchor 워크플로우:**
```
1. ANCHOR_GIRL 먼저 생성 (MJ V7)
2. ANCHOR_BOY 먼저 생성 (MJ V7)
3. 이후 모든 씬에서 [ANCHOR_IMG URL] 포함
4. Elements Feature로 일관성 강화
```

**일관성 실패 시 해결:**
- 샷 길이 줄이기
- Anchor 프레임 추가
- 동일 identity embedding 재사용
- Adapter weight 약간 증가

### Veo 멀티샷 일관성

**성공적인 멀티샷 시퀀스 3가지 특징:**
1. 작고 규율 있는 레퍼런스 세트 + 프롬프트 간 반복 어휘
2. 의도적 브릿지 샷 (전환점에서 모델의 자유도 감소)
3. 단순 메트릭으로 측정된 반복 (샷 잠금 시점 결정)

**권장 워크플로우:**
- 레퍼런스로 아이덴티티와 팔레트 고정
- 카메라 문법과 프레임 컨디셔닝으로 브릿지 안정화
- 퍼포먼스와 미세 디테일은 내러티브 허용 범위 내에서 변형

---

## 🔄 Part 9: Builder 1 → Builder 2 연결 검증

### 구분자 체크
```bash
# Builder 1 출력에서 확인할 것
grep "<<<ANALYSIS_START>>>" builder1_output.md
grep "<<<IMAGE_PROMPTS_START>>>" builder1_output.md
```

### 누락 시 수동 추가 템플릿
```markdown
<<<ANALYSIS_START>>>
## 📊 영상 분석 요약
[씬 테이블, 캐릭터 프로필, Visual Rhyme, 구도 분석]
<<<ANALYSIS_END>>>

<<<IMAGE_PROMPTS_START>>>
## 🖼️ IMAGE PROMPTS
[모든 씬 프롬프트]
<<<IMAGE_PROMPTS_END>>>
```

### 씬 개수 확인
```bash
# 씬 개수 세기
grep -c "### Scene" builder1_output.md
grep -c "### 🎬 Scene" builder2_output.md
```

---

## ✅ 최종 체크리스트 (수업 전)

### 필수 (5분)
- [ ] Builder 1 테스트 → 구분자 출력 확인
- [ ] 구분자 없으면 수동 추가 방법 준비
- [ ] Builder 2 STEP 1 → 재현성 테이블 확인

### 권장 (추가 10분)
- [ ] Builder 2 STEP 2 → MOTION 형식 확인
- [ ] Veo 프롬프트 300자 이내 확인
- [ ] "위와 유사한" 패턴 없음 확인

### 수업 중 팁
- A(8%) 옵션부터 시작
- 복합 움직임 피하기 (회전+줌 동시 X)
- 캐릭터 2명 이상이면 같은 행동 권장

---

*분석 완료: 2026-02-05 02:45 UTC*
*최종 업데이트: 2026-02-05 03:00 UTC*
*분석자: 소미 🐱*
