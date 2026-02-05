# 🔬 빌더 시스템 심층 연구

> **시작**: 2026-02-05 01:23 KST
> **목표**: 빌더1 → 빌더2 → imge.md + motion.md 파이프라인 완전 이해
> **연구자**: 소미 🐱

---

## 📁 프로젝트 구조

```
/Users/ted/vivid/viral-video-automation/
├── builder1-temp/           # Builder 1 Canvas App (분석기)
├── builder2-temp/           # Builder 2 Canvas App (변주 엔진)
├── builder-parody-engine/   # Parody Engine (이전 버전?)
├── builder-analysis/        # 분석 관련
├── builder-v2-analysis/     # V2 분석
├── docs/                    # 문서
├── templates/               # 템플릿들
├── prompts/                 # 프롬프트들
└── *.zip                    # 배포용 ZIP 파일들
```

---

## 🔍 연구 진행 상황

### Phase 1: 파일 구조 파악 ✅
- [x] 프로젝트 디렉토리 탐색
- [x] Canvas App 구조 확인 (React + Vite)
- [ ] 핵심 파일 분석 시작

### Phase 2: 빌더1 분석 (진행중)
- [ ] constants.ts - 시스템 프롬프트
- [ ] App.tsx - 워크플로우 로직
- [ ] types.ts - 데이터 구조
- [ ] 입력/출력 형식 정의

### Phase 3: 빌더2 분석
- [ ] constants.ts - 시스템 프롬프트
- [ ] App.tsx - 워크플로우 로직
- [ ] 오마주/변주 로직
- [ ] 최종 출력 형식

### Phase 4: 파이프라인 연결
- [ ] 빌더1 OUTPUT → 빌더2 INPUT 인터페이스
- [ ] 빌더2 OUTPUT → imge.md 형식
- [ ] 빌더2 OUTPUT → motion.md 형식

### Phase 5: 테드 의도 파악
- [ ] 현재 시스템의 한계점
- [ ] 원하는 최종 산출물 형태
- [ ] 개선 방향

---

## 📝 연구 노트

### [01:23] 시작
- vivid/viral-video-automation 폴더 발견
- 여러 버전의 빌더가 존재함
  - builder1-hardened.zip (현재 배포)
  - builder1-v7.1-hardened.zip
  - builder1-v7.2-frame-verify.zip
  - builder2-hardened.zip

---

## 🔑 핵심 발견: 빌더1 시스템 프롬프트 V7.4

**파일**: `/Users/ted/vivid/viral-video-automation/builder1-temp/constants.ts`

### 빌더1 목적
- AI 이미지 프롬프트 생성기
- NanoBanana Pro (기본, 한글) + Midjourney V7 (선택, 영문)

### 4-STEP 워크플로우
1. **STEP 1**: 영상 분석 (통합)
   - 씬 테이블 (Phase, Timecode, ANCHOR)
   - 캐릭터 프로필
   - Visual Rhyme (과거 vs 현재)
   - 구도 분석 (소실점, 삼분할, 심도 레이어)

2. **STEP 2**: Phase 1-2 IMAGE 프롬프트 (과거/회상)
   - 듀얼 레퍼런스 라벨
   - Midjourney V7 파라미터
   - 씬별 --no 맞춤

3. **STEP 3**: Phase 3-4 IMAGE 프롬프트 (현재)
   - Visual Rhyme 대조 섹션

4. **STEP 4**: 최종 출력
   - `<<<ANALYSIS_START>>>` ... `<<<ANALYSIS_END>>>`
   - `<<<IMAGE_PROMPTS_START>>>` ... `<<<IMAGE_PROMPTS_END>>>`

### Builder 2로 전달
- 영상 파일
- 마크다운 전체 (ANALYSIS + IMAGE_PROMPTS)
- persona.json (선택)
- 베스트 댓글 (선택)

---

## 🔑 핵심 발견: 빌더2 시스템 프롬프트 V4.0

**파일**: `/Users/ted/vivid/viral-video-automation/builder2-temp/constants.ts`

### 빌더2 목적
- PARODY ENGINE - 복사-붙여넣기 가능한 프롬프트 생성
- IMAGE + MOTION 프롬프트 출력

### 4-STEP 워크플로우
1. **STEP 1**: 검증 + 바이럴 로직 분석
   - Builder 1 출력 파싱
   - 재현성 검증 (구도, 인물, 조명, 동작, 분위기)
   - 바이럴 로직 (Hook Genome, Dopamine Radar, Causal Chain)
   - 통제 변수 vs 변주 가능 정의

2. **STEP 2**: 캐릭터 + MOTION 프롬프트
   - 캐릭터 변환표
   - 모든 씬 MOTION (Kling 3.0 + Veo 3.1)
   - 출력: `<<<OHMAGE_IMAGE_START>>>` + `<<<OHMAGE_MOTION_START>>>`

3. **STEP 3**: 변주 옵션 생성
   - A: 안정형 (8%)
   - B: 밸런스형 (15%)
   - C: 과감형 (18%)

4. **STEP 4**: 최종 출력 (변주 버전)
   - `<<<VARIATION_IMAGE_START>>>` + `<<<VARIATION_MOTION_START>>>`

### 최종 산출물 (4개 파일!)
```
1. 오마쥬 IMAGE (NanoBanana + MJ)
2. 오마쥬 MOTION (Kling + Veo)
3. 변주 IMAGE
4. 변주 MOTION
```

---

## 🎯 테드 의도 파악 (초기 가설)

테드가 원하는 "imge.md, motion.md":

```
imge.md = 오마쥬/변주 IMAGE 프롬프트 파일
         (NanoBanana Pro + Midjourney V7)

motion.md = 오마쥬/변주 MOTION 프롬프트 파일
            (Kling 3.0 + Veo 3.1)
```

### 현재 시스템의 출력 형태
- 하나의 긴 마크다운에 구분자(<<<...>>>)로 섹션 분리
- 사용자가 수동으로 복사해서 분리해야 함

### 개선 가능성?
- 자동으로 imge.md, motion.md 분리 출력?
- Canvas App에서 다운로드 버튼 제공?

---

## 📝 연구 노트 (계속)

### [01:30] 빌더1, 빌더2 시스템 프롬프트 분석 완료
- 둘 다 매우 상세한 시스템 프롬프트
- 빌더1: 470줄+ (V7.4)
- 빌더2: 400줄+ (V4.0)
- 구조화된 출력 (구분자 패턴)

### 다음 연구 항목
- [x] templates/ 폴더 탐색
- [x] prompts/ 폴더 탐색
- [x] 실제 출력 예시 찾기
- [ ] App.tsx 워크플로우 로직 분석
- [ ] 빌더2 설계 검증

---

## 🎯 핵심 발견: 실제 프로젝트 산출물

**위치**: `/Users/ted/vivid/viral-video-automation/projects/kylenutt-parody/`

### 프로젝트 폴더 구조
```
kylenutt-parody/
├── prompts/
│   ├── IMAGE_PROMPTS.md  ← ⭐ imge.md 의 실체!
│   └── MOTION_PROMPTS.md ← ⭐ motion.md 의 실체!
├── generated/
│   ├── images/
│   └── videos/
├── docs/
│   ├── ANALYSIS.md
│   ├── CRITIQUE_LOG.md
│   └── PROFILES.md
├── reference/
├── brief.md
├── PROJECT_CONTEXT.md
└── STATE.md
```

---

## 📄 IMAGE_PROMPTS.md 형식 분석

**버전**: 10-CUT BALANCED PROMPT v3.0
**총 길이**: ~280줄

### 구조
```markdown
# 🎬 VIDEO PARODY: 10-CUT BALANCED PROMPT v3.0

## ⚙️ 필수 설정 (Midjourney)
## 📁 추출된 키프레임 (10-Cut 정밀)

# 🏗️ PHASE 1: ANCHOR FIRST
## 📼 Scene 2 ⭐ ANCHOR

# 🏗️ PHASE 2: THE 90s (Scene 1, 3~7)
## 📼 Scene 1: The Arrival
## 📼 Scene 3: Side View
[... 계속]

# 🏗️ PHASE 3: THE GLITCH (Scene 8)
## 🔄 Scene 8: The Glitch Transition

# 🏗️ PHASE 4: THE PRESENT (Scene 9~10)
## 📱 Scene 9: Digital Isolation
## 📱 Scene 10: The Selfie

## ✅ 10-Cut 체크리스트
```

### 핵심 패턴
1. **듀얼 레퍼런스**
   ```
   **[Image 1: COMPOSITION]** [scene URL]
   **[Image 2: CHARACTER FACE]** [ANCHOR URL]
   ```

2. **프롬프트 형식**
   - Midjourney V6/V7 파라미터 포함
   - `--iw 2.0 --ar 9:16 --v 6.0 --style raw --cw 50 --no [제외 항목]`

3. **PHASE 분리** (과거/글리치/현재)

---

## 📄 MOTION_PROMPTS.md 형식 분석

**버전**: K-PARADOX MOTION PROMPTS v9.0
**총 길이**: ~200줄

### 구조
```markdown
# 🎬 K-PARADOX MOTION PROMPTS v9.0 (10-CUT)

## ⚙️ GLOBAL SETTINGS
## 📊 10-CUT TIMEFRAME

## 📼 SCENE 1: The Arrival (1.27s)
### [📋 COPY] Positive
### [📋 COPY] Negative
| Camera | Motion Score |

[... 모든 씬 반복]

## ✅ FINAL CHECKLIST
```

### 핵심 패턴
1. **타이밍 규칙**
   - `IMMEDIATELY` - 첫 동작
   - `then holds` - 이후 유지
   - `within first second` - 시간 제약

2. **Motion Score** (1-7)
   - 동작 강도 수치화

3. **Negative 프롬프트**
   - `delayed *` 패턴 필수

4. **Camera 타입**
   - Static, Zoom In, Zoom Out, Roll

---

## 🔄 전체 파이프라인 정리

```
┌─────────────────────────────────────────────────────┐
│                    PIPELINE                          │
├─────────────────────────────────────────────────────┤
│                                                      │
│  [원본 영상] + [FFmpeg 타임스탬프]                   │
│       ↓                                              │
│  ┌─────────────────────────────────────────────┐    │
│  │ BUILDER 1 (영상 분석기)                      │    │
│  │ - 씬 테이블                                  │    │
│  │ - 캐릭터 프로필                              │    │
│  │ - Visual Rhyme                              │    │
│  │ - 구도 분석                                  │    │
│  │                                              │    │
│  │ OUTPUT: VIDEO_PROMPTS_RAW.md                │    │
│  │  ├─ <<<ANALYSIS>>>                          │    │
│  │  └─ <<<IMAGE_PROMPTS>>>                     │    │
│  └─────────────────────────────────────────────┘    │
│       ↓                                              │
│  ┌─────────────────────────────────────────────┐    │
│  │ BUILDER 2 (패러디 엔진)                      │    │
│  │ + persona.json (선택)                        │    │
│  │ + 베스트 댓글 (선택)                         │    │
│  │                                              │    │
│  │ STEP 1: 검증 + 바이럴 로직                   │    │
│  │ STEP 2: 캐릭터 + MOTION                     │    │
│  │ STEP 3: 변주 옵션                           │    │
│  │ STEP 4: 최종 출력                           │    │
│  │                                              │    │
│  │ OUTPUT (4개 파일):                          │    │
│  │  ├─ 오마쥬 IMAGE_PROMPTS.md                 │    │
│  │  ├─ 오마쥬 MOTION_PROMPTS.md                │    │
│  │  ├─ 변주 IMAGE_PROMPTS.md                   │    │
│  │  └─ 변주 MOTION_PROMPTS.md                  │    │
│  └─────────────────────────────────────────────┘    │
│       ↓                                              │
│  [이미지 생성] NanoBanana Pro / Midjourney          │
│       ↓                                              │
│  [영상 생성] Kling 2.0 / Veo 3.1                    │
│       ↓                                              │
│  [편집] CapCut / Premiere                           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🤔 현재 시스템의 잠재적 문제점

### 1. 빌더1 → 빌더2 인터페이스
- 빌더1의 <<<IMAGE_PROMPTS>>> 출력이 빌더2에서 그대로 재사용되는지?
- 아니면 빌더2가 완전히 새로 작성하는지?

### 2. 최종 파일 분리
- 현재: 하나의 마크다운에 구분자로 모든 내용
- 원하는 것: 별도 파일로 깔끔하게 분리 (imge.md, motion.md)
- Canvas App에서 다운로드 버튼 제공 필요?

### 3. MOTION_PROMPTS 중복 가이드
- 빌더2에 MOTION 생성 기능이 있음
- 별도 MOTION_BUILDER도 존재
- 어떤 것이 최신/권장인지?

---

## 📝 연구 노트 (계속)

### [01:35] 실제 프로젝트 산출물 분석 완료
- kylenutt-parody 프로젝트에서 IMAGE_PROMPTS.md, MOTION_PROMPTS.md 발견
- 테드가 원하는 imge.md, motion.md의 실체 확인
- 매우 상세하고 구조화된 형식

### [01:40] 현재 시스템 vs 원하는 시스템
- 빌더1: 영상 분석 → RAW.md (ANALYSIS + IMAGE_PROMPTS)
- 빌더2: RAW + 영상 → 오마쥬/변주 (IMAGE + MOTION) × 2

문제: 빌더2가 잘 설계되어 있는가?
- 입력 파싱이 명확한가?
- 출력 형식이 IMAGE_PROMPTS.md, MOTION_PROMPTS.md와 일치하는가?

---

## 🔧 빌더2 Canvas App 구현 분석

### 기술 스택
- React + TypeScript + Vite
- Gemini API (@google/genai)
- **Model**: `gemini-3-pro-preview`
- **Thinking**: `ThinkingLevel.HIGH`
- **Max Output**: 32000 tokens

### 워크플로우 (App.tsx)
```typescript
// 상태 관리
const [currentStep, setCurrentStep] = useState(1); // 1→4

// 입력
- file (영상) - 필수
- builder1Output (빌더1 마크다운) - 필수
- personaJson (선택)
- bestComments (선택, 최대 5개)

// STEP 진행
STEP 1: 검증 (영상 + 빌더1 출력)
STEP 2: 오마쥬 생성 (사용자 "다음" 입력)
STEP 3: 변주 옵션 (Persona + Comments 주입)
STEP 4: 최종 출력
```

### API 호출 (geminiService.ts)
```typescript
// 각 스텝마다 영상 re-attach
parts.unshift({ inlineData: currentFileBase64 });

// STEP 3에서 컨텍스트 주입
if (currentStep === 2 && (cachedPersonaJson || cachedBestComments.length > 0)) {
  // Persona + 베스트 댓글 추가
}
```

### 출력 형식 (시스템 프롬프트 기준)
```
STEP 2 출력:
  <<<OHMAGE_IMAGE_START>>> ... <<<OHMAGE_IMAGE_END>>>
  <<<OHMAGE_MOTION_START>>> ... <<<OHMAGE_MOTION_END>>>

STEP 4 출력:
  <<<VARIATION_IMAGE_START>>> ... <<<VARIATION_IMAGE_END>>>
  <<<VARIATION_MOTION_START>>> ... <<<VARIATION_MOTION_END>>>
```

---

## ❓ 핵심 검증 필요 사항

### 1. 출력 형식 GAP
**시스템 프롬프트**: 구분자(<<<>>>)로 섹션 분리된 하나의 긴 마크다운
**실제 프로젝트 산출물**: 별도 파일 (IMAGE_PROMPTS.md, MOTION_PROMPTS.md)

**질문**: 
- 빌더2 출력을 수동으로 파일 분리해야 하는가?
- 자동 분리 기능이 있는가?
- 아니면 실제 프로젝트의 파일들은 빌더2 이전에 수동 작성된 것인가?

### 2. 빌더1 → 빌더2 인터페이스
**빌더1 출력**:
```
<<<ANALYSIS_START>>>
[씬 테이블, 캐릭터, Visual Rhyme, 구도 분석]
<<<ANALYSIS_END>>>

<<<IMAGE_PROMPTS_START>>>
[모든 씬 IMAGE 프롬프트]
<<<IMAGE_PROMPTS_END>>>
```

**빌더2 입력**: 위 전체를 `builder1Output`으로 받음

**질문**:
- 빌더2가 빌더1의 IMAGE_PROMPTS를 파싱해서 재활용하는가?
- 아니면 완전히 새로 작성하는가?
- 시스템 프롬프트에 "Builder 1 IMAGE를 기반으로 오마쥬 IMAGE 작성"이라고 되어 있지만, 실제로 어떻게 동작하는지?

### 3. MOTION 프롬프트 생성 주체
**현재 상태**:
- 빌더2에 MOTION 생성 기능 있음 (<<<OHMAGE_MOTION_START>>>)
- 별도 MOTION_BUILDER 시스템 프롬프트도 존재 (templates/)

**질문**:
- 어떤 것이 권장되는가?
- 빌더2가 MOTION도 커버하는 것이 최신 설계인가?

### 4. 버전 혼란
**발견된 버전들**:
- Builder 1: V7.4 (builder1-temp/constants.ts)
- Builder 2: V4.0 (builder2-temp/constants.ts)
- Builder 2 (templates/): V1.0 (BUILDER_2_PARODY_ENGINE_SYSTEM_PROMPT.md)
- Motion Builder: V1.0 (templates/)

**질문**:
- 최신/권장 버전이 무엇인가?
- 모든 버전이 동기화되어 있는가?

---

## 🎯 테드 의도 파악 (업데이트된 가설)

### 테드가 원하는 것
1. **빌더1 → 빌더2** 파이프라인이 **원활하게** 동작
2. **최종 산출물**이 `imge.md`, `motion.md` 형태로 **깔끔하게** 분리
3. **빌더2 설계**가 이 목표에 **최적화**되어 있는지 검증

### 현재 시스템의 잠재적 문제
1. **파일 분리 없음**: 빌더2가 하나의 긴 마크다운 출력, 수동 분리 필요
2. **구분자 파싱**: 사용자가 <<<>>> 구분자를 찾아서 복사해야 함
3. **형식 불일치**: 빌더2 출력 형식과 실제 프로젝트 산출물 형식이 다름

### 개선 방향 제안
1. **Canvas App에 다운로드 버튼 추가**
   - "IMAGE 다운로드" → IMAGE_PROMPTS.md
   - "MOTION 다운로드" → MOTION_PROMPTS.md

2. **출력 형식 표준화**
   - 빌더2 출력을 실제 프로젝트 산출물 형식에 맞춤
   - kylenutt-parody의 IMAGE_PROMPTS.md, MOTION_PROMPTS.md를 템플릿으로

3. **파싱 자동화**
   - <<<>>> 구분자를 파싱해서 자동 분리

---

## 📝 연구 노트 (계속)

### [01:45] 빌더2 Canvas App 구현 분석 완료
- geminiService.ts: Gemini 3 Pro, ThinkingLevel.HIGH
- 4-STEP 챗 기반 워크플로우
- STEP 3에서 Persona/Comments 지연 주입

### [01:50] 핵심 GAP 발견
- 빌더2 출력 형식 vs 실제 프로젝트 산출물 형식 불일치
- 수동 파일 분리 필요할 수 있음
- 다운로드 기능 추가 필요성

### 다음 연구 항목
- [ ] 빌더2 실제 테스트 (실행해서 출력 확인)
- [ ] 빌더1 출력과 빌더2 입력 파싱 검증
- [ ] Canvas App에 파일 분리 다운로드 기능 구현 가능성

---

*연구 계속 중... (01:50 KST)*

---

## 📚 추가 발견: notebooklm-sources 분석

### 핵심 철학 문서들
- `10_CONTROLLED_VARIABLES.md` - 통제변인 vs 변수
- `00_BEGINNER_INTRO.md` - 초보자용 개념 설명
- `08_ACADEMY_GUIDE.md` - 전체 워크플로우 가이드

### 통제변인 vs 변수 (바이럴 공식)

```
바이럴 영상 = 통제변인(80-95%) + 변수(5-20%)
```

**통제변인 (절대 바꾸지 않음)**:
- Cut Sequence (컷 순서)
- Scene Timing (밀리초 타이밍)
- Composition (100% 구도 매칭)
- Lighting Contrast (3200K→5600K)
- IMMEDIATELY Pattern (첫 0.3초 동작)
- Camera Angles

**변수 (자유롭게 바꿈)**:
- Character Ethnicity (외국인→한국인)
- Cultural Details (미국 90년대→한국 90년대)
- Clothing Styles
- Food/Props
- Text/Banners

### Builder 1 vs Builder 2 차이 (공식 가이드)

| | Builder 1 | Builder 2 |
|---|-----------|-----------|
| **역할** | 원본 분석 | 패러디/오마주 생성 |
| **입력** | 원본 영상만 | 원본 + Builder 1 결과 + (프로필) |
| **출력** | 원본 그대로 프롬프트 | 한국인 버전 프롬프트 |
| **캐릭터** | 외국인 유지 | 한국인으로 변환 |

### Builder 2 결과물 (4개 파일)

```
1. 오마쥬 IMAGE (NanoBanana + Midjourney)
2. 오마쥬 MOTION (Kling + Veo)
3. 변주 IMAGE
4. 변주 MOTION
```

### RAW 다운로드 기능
> "다운로드가 안 될 때? → RAW 버튼 클릭하면 전체 원본 다운로드 가능!"

---

## 🔬 최종 분석: 빌더2 설계 검증

### ✅ 잘 된 부분

1. **시스템 프롬프트 (V4.0)**
   - 4-STEP 워크플로우 명확
   - 검증 + 바이럴 로직 + 오마쥬 + 변주
   - ANTI-LAZY GUARD로 생략 방지
   - Kling 3.0 + Veo 3.1 최신 패턴

2. **Canvas App 구현**
   - Gemini 3 Pro + ThinkingLevel.HIGH
   - 영상 re-attach로 각 스텝 정밀 분석
   - STEP 3에서 Persona/Comments 지연 주입

3. **통제변인 철학 준수**
   - 구도/타이밍/조명 100% 유지
   - 캐릭터/문화만 변경

### ⚠️ 검증 필요 부분

1. **출력 형식 GAP**
   - 시스템 프롬프트: <<<>>> 구분자 기반 하나의 마크다운
   - 실제 프로젝트: IMAGE_PROMPTS.md + MOTION_PROMPTS.md 별도 파일
   - **질문**: 자동 분리 기능이 있는가? RAW 버튼으로 해결되는가?

2. **빌더1 → 빌더2 파싱**
   - 빌더1 출력: <<<ANALYSIS>>> + <<<IMAGE_PROMPTS>>>
   - 빌더2 시스템 프롬프트에 파싱 지침 있음
   - **질문**: 실제로 정확히 파싱되는가?

3. **MOTION 프롬프트 형식**
   - 빌더2 MOTION: Beat System + Veo Full Slot
   - 실제 프로젝트 MOTION: 단순 Positive/Negative 형식
   - **질문**: 최신 형식이 실제 프로젝트와 다른가?

### 🎯 개선 제안

1. **다운로드 기능 명확화**
   - 4개 파일 각각 별도 다운로드 버튼
   - 또는 ZIP 묶음 다운로드

2. **출력 형식 표준화**
   - 실제 프로젝트 산출물 형식에 맞춤
   - kylenutt-parody를 템플릿으로 사용

3. **버전 동기화**
   - templates/ 폴더의 구버전 정리
   - 최신 버전만 유지

---

## 📝 최종 연구 노트

### [02:00] 심층 연구 완료

**탐색한 파일들**:
- builder1-temp/ (Canvas App)
- builder2-temp/ (Canvas App)
- templates/ (40+ 문서)
- prompts/ (프롬프트 템플릿)
- projects/kylenutt-parody/ (실제 산출물)
- notebooklm-sources/ (아카데미 자료)
- docs/ (아키텍처, 피벗 리포트)

**핵심 결론**:
1. 빌더2 시스템 프롬프트는 **잘 설계됨** (V4.0)
2. 통제변인 철학이 **명확히 반영**됨
3. 출력 형식 **GAP 존재** - 구분자 vs 별도 파일
4. 실제 테스트로 **검증 필요**

---

## 🚀 다음 단계 제안

1. **빌더2 실제 테스트**
   - kylenutt 영상으로 빌더2 실행
   - 출력 형식 확인
   - 파일 분리 기능 검증

2. **빌더1 → 빌더2 연동 테스트**
   - 빌더1 출력을 빌더2에 입력
   - 파싱 정확도 확인

3. **개선 구현** (필요시)
   - 다운로드 기능 개선
   - 출력 형식 표준화

---

*연구 완료: 2026-02-05 02:00 KST*
*총 연구 시간: ~40분*
*탐색 파일 수: 30+ 개*
