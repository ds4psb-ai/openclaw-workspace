# 🔬 메가앱 UX 병목 분석 리포트

**From:** AG-Vivid 🦢  
**Date:** 2026-01-31  
**목적:** 10분 안에 15초 영상 완성 목표 달성을 위한 UX 병목 지점 식별

---

## 📊 Executive Summary

### 🔴 핵심 문제

**"버튼이 너무 많고 뭘 눌러야 하는지 혼란스럽다"**

코드 분석 결과, 가장 큰 병목은 **Production 앱의 VeoVideoPanel**(1010줄)에 있음:
- 입력 필드: 6개+ (프롬프트, 네거티브 프롬프트, 파일 업로드, 비율, 길이, 스타일, 모델, 시드)
- 버튼: 6개+ (스타일 4개, 모델 2개, 시드 토글, 생성, 다운로드, 복사)
- 사용자가 모든 옵션을 이해하고 선택해야 함

---

## 📁 메가앱별 복잡도 분석

### 1. DNA Lab (분석)

| 지표 | 값 | 평가 |
|------|:---:|:----:|
| 페이지 코드 | 431줄 | 🟡 |
| 워크플로우 단계 | 3개 (analysis, mirror, qc) | ✅ |
| 온보딩 옵션 | 3개 (IP 선택, URL 입력, Quick Start) | 🟡 |
| UnifiedAnalysisPanel | 618줄 | 🔴 |

**병목 지점:**
1. `UnifiedAnalysisPanel` 618줄 - VPE+AD 통합했지만 여전히 복잡
2. 온보딩 3가지 옵션 → 사용자가 뭘 선택해야 할지 고민
3. `MissingDataBanner` 경고 → 사용자 이탈 유발

**개선 제안:**
- 온보딩 → **"URL 하나만 입력하세요"** 단일 옵션으로 단순화
- 분석 결과 → **한 줄 요약** + 상세 접기

---

### 2. Story Engine (구성)

| 지표 | 값 | 평가 |
|------|:---:|:----:|
| 페이지 코드 | 175줄 | ✅ |
| 워크플로우 단계 | 2개 (story, prompt) | ✅ |
| Overview 뷰 | 있음 | ✅ |

**평가:** 가장 단순함! 모범 사례.

**개선 포인트:**
- StoryArchitectPanel, UnifiedPromptPanel 내부 복잡도 확인 필요
- Story → Prompt 자동 전환 여부

---

### 3. Production (제작) ← 🔴 가장 큰 병목

| 지표 | 값 | 평가 |
|------|:---:|:----:|
| 페이지 코드 | 239줄 | ✅ |
| Provider 선택 | 3개 (Veo, Kling, Suno) | 🟡 |
| VeoVideoPanel | **1010줄** | 🔴🔴🔴 |
| KlingPanel | **692줄** | 🔴🔴 |

**VeoVideoPanel 입력 필드 (11줄 391~801):**

```
1. 프롬프트 (textarea, 6줄)
2. 참고 이미지/영상 (file upload)
3. 네거티브 프롬프트 (textarea, 3줄)
4. 비율 (select, 4옵션: 16:9, 9:16, 1:1, 4:3)
5. 길이 (select, 3옵션: 4초, 6초, 8초)
6. 스타일 (button grid, 4옵션: Cinematic, Realistic, Artistic, Anime)
7. 모델 (button grid, 2옵션: Quality, Fast)
8. 시드 (toggle + input)
9. 크레딧 표시
10. 생성 버튼
```

**문제:**
- 사용자가 **8개 설정**을 결정해야 비디오 생성 가능
- "Cinematic vs Realistic vs Artistic vs Anime" → 차이를 모름
- "Quality vs Fast" → 가격 차이만 표시, 품질 차이 불명확

---

## 🎯 핵심 병목 3가지

### 1. VeoVideoPanel 과도한 옵션 (🔴 Critical)

**현재:** 8개 설정을 사용자가 직접 선택
**목표:** 프롬프트만 입력하면 나머지 자동 설정

**제안:**
```
[기본 모드] 프롬프트만 입력 → AI가 최적 설정 자동 선택
[고급 모드] 현재 UI 유지 (접어두기)
```

### 2. Provider 선택 혼란 (🟡 Medium)

**현재:** Veo vs Kling vs Suno 중 선택해야 함
**문제:** 사용자는 차이를 모름

**제안:**
```
"15초 영상 만들기" 버튼 하나 → 자동으로 Kling Turbo 선택
(SmartProviderSelector 이미 구현됨 - 활성화 필요)
```

### 3. 앱 간 전환 마찰 (🟡 Medium)

**현재:** DNA Lab → Story Engine → Production 각각 수동 이동
**목표:** Chain Data 자동 전달 + 원클릭 다음 단계

**제안:**
```
분석 완료 후: "이 스타일로 스토리 만들기" 버튼
스토리 완료 후: "이 스토리로 영상 만들기" 버튼
```

---

## ✅ Phase 9-12 기능 활성화 상태 (심층 분석)

코드 분석 결과:

| Phase | 기능 | 구현 상태 | 활성화 상태 | 위치 |
|:-----:|------|:--------:|:----------:|------|
| 9 | SmartProviderSelector | ✅ 547줄 | ✅ **활성화** | `ProductionOverview.tsx:216` |
| 9 | CostEstimator | ✅ 코드 있음 | ✅ **활성화** | `ProductionOverview.tsx:226` |
| 11 | IntentSearchBar | ✅ 805줄 | 🔴 **미사용** | app 폴더에서 import 없음! |
| 12 | ProductionOverview | ✅ 461줄 | ✅ **활성화** | `production/page.tsx:91` |

### 🔴 핵심 발견: IntentSearchBar 805줄이 죽은 코드!

`IntentSearchBar.tsx` 분석:
- **기능:** "무엇을 만들고 싶으세요?" 자연어 검색
- **인텐트 분류:** `analyze`, `story`, `generate`, `style-transfer` 등
- **프리셋 지원:** 거장 스타일(봉준호, 웡카와이), 장르, 플랫폼별
- **자동 앱/단계 추천:** 입력에 따라 DNA Lab/Story Engine/Production으로 라우팅

**왜 죽은 코드인가?**
```bash
grep -r "IntentSearchBar" frontend/src/app/  # 결과 없음!
```

→ **아무 페이지에서도 IntentSearchBar를 import하지 않음**

### ✅ ProductionOverview는 잘 작동 중

`/production` 접속 시:
1. `ProductionOverview` 컴포넌트 렌더링
2. `SmartProviderSelector`로 Veo/Kling/Suno 선택
3. `CostEstimator`로 비용 표시
4. "빠른 시작" 버튼 제공

**하지만 문제:**
- SmartProviderSelector 선택 후 → 여전히 VeoVideoPanel의 8개 옵션 입력해야 함
- "빠른 시작" = 실제로는 빠르지 않음

---

## 📋 즉시 실행 가능한 개선안 (코드 수정 없이)

1. **VeoVideoPanel 기본값 더 공격적으로 설정**
   - 비율: 9:16 (숏폼 기본)
   - 길이: 8초 (최대)
   - 스타일: Cinematic
   - 모델: Fast (저비용)

2. **고급 옵션 접어두기**
   - 네거티브 프롬프트, 시드 → 기본 숨김

3. **Production 기본 진입점 변경**
   - `/production` → `/production?step=kling` (가장 빠른 Provider)

---

## 🎬 "10분 안에 15초 영상" 달성을 위한 최적 경로

```
[현재 예상 시간]
DNA Lab: 5분 (URL 입력 + 분석 대기 + 결과 확인)
Story Engine: 3분 (시나리오 생성 + 프롬프트 변환)
Production: 7분 (설정 선택 + 렌더링 대기)
= 총 15분 ❌

[목표]
DNA Lab: 2분 (URL 입력 → 원클릭 분석)
Story Engine: 2분 (자동 시나리오 → 원클릭 프롬프트)
Production: 6분 (자동 설정 → Kling Turbo 렌더링)
= 총 10분 ✅
```

---

## 🔜 다음 단계

1. **즉시:** VeoVideoPanel 기본값 수정 (PR 가능)
2. **오늘:** IntentSearchBar, SmartProviderSelector 활성화 확인
3. **내일:** E2E 테스트로 10분 달성 검증

---

*AG-Vivid 🦢*
