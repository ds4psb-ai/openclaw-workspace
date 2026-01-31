# 🔴 UX 하드닝 계획 전수조사 결과: 치명적 오류 발견

**From:** AG-Vivid  
**Date:** 2026-01-31 16:43  
**Re:** 메가앱 UX 하드닝 계획 검토

---

## 🚨 결론: 계획서 기반 데이터 OUTDATED

### 현황표 수정 필요

| 패널 | 계획서 분석 | 실제 코드 | 상태 |
|------|:----------:|:---------:|:----:|
| **VeoVideoPanel** | showAdvanced ✅ | ✅ 있음 (line 190) | ✅ 정확 |
| **KlingPanel** | showAdvanced ❌ | ✅ **이미 있음!** (line 135, 483-498) | 🔴 **오류** |
| **SunoPanel** | showAdvanced ❌ | ✅ **이미 있음!** (line 182, 665-725) | 🔴 **오류** |
| **AbyssMirrorPanel** | showAdvanced ❌ | ❌ 없음 (Phase-based UI) | ⚠️ 불필요 |
| **QualityDirectorPanel** | showAdvanced ❌ | ❌ 없음 (Criteria-based UI) | ⚠️ 불필요 |

---

## 📊 KlingPanel.tsx 실제 상태 (692줄)

```typescript
// Line 135: 이미 showAdvanced 선언됨!
const [showAdvanced, setShowAdvanced] = useState(false);

// Lines 483-498: 이미 Advanced Toggle 구현됨!
<button
  onClick={() => setShowAdvanced(!showAdvanced)}
  className="..."
>
  <span>{showAdvanced ? "Hide" : "Show"} Advanced Options</span>
</button>

{showAdvanced && (
  // Negative Prompt, Motion Control, Camera Control 숨겨짐
)}
```

**결론: KlingPanel은 이미 완료됨! Quick Presets만 추가하면 됨.**

---

## 📊 SunoPanel.tsx 실제 상태 (855줄)

```typescript
// Line 182: 이미 showAdvanced 선언됨!
const [showAdvanced, setShowAdvanced] = useState(false);

// Lines 665-725: 이미 Advanced Toggle 구현됨!
<button onClick={() => setShowAdvanced(!showAdvanced)}>
  <span>{showAdvanced ? "▼" : "▶"}</span>
  <span>{labels.advancedOptions}</span>
</button>

{showAdvanced && (
  // Model 선택, Composer Style, Custom Style 숨겨짐
)}
```

**결론: SunoPanel도 이미 완료됨! Quick Presets만 추가하면 됨.**

---

## 📊 AbyssMirrorPanel.tsx 분석 (1406줄)

**구조:**
- 3-Phase UI: `input` → `chat` → `complete`
- Phase 전환으로 Progressive Disclosure 이미 구현됨
- 고급 옵션 없음 (생년월일, MBTI, 혈액형만)

**결론: showAdvanced 불필요! 기존 Phase 구조로 충분.**

---

## 📊 QualityDirectorPanel.tsx 분석 (837줄)

**구조:**
- Criteria 선택식 UI (토글 버튼으로 선택)
- 모든 옵션이 핵심 기능 (숨길 것 없음)
- Threshold 슬라이더, Model 선택 등 간결한 UI

**결론: showAdvanced 불필요! 이미 최적화된 UI.**

---

## ✅ 수정된 작업 계획

### 실제 필요 작업 (4→2개 감소)

| 패널 | 필요 작업 | 예상 시간 |
|------|----------|:---------:|
| **KlingPanel** | Quick Presets 추가만 | 15분 |
| **SunoPanel** | Quick Presets 추가만 | 15분 |
| ~~AbyssMirrorPanel~~ | ~~불필요~~ | - |
| ~~QualityDirectorPanel~~ | ~~불필요~~ | - |

**총 작업량: 2개 파일, 30분** (원래 계획 4개 파일, 60분 → 50% 감소)

---

## 🎯 Quick Presets 구현 방안

### KlingPanel Quick Presets
```tsx
<div className="grid grid-cols-2 gap-2">
  <button onClick={() => {
    setAspectRatio("9:16");
    setDuration("5");
    setMode("std");
  }}>📱 숏폼 (9:16, 5s)</button>
  
  <button onClick={() => {
    setAspectRatio("16:9");
    setDuration("10");
    setMode("pro");
  }}>🎬 시네마틱 (16:9, 10s)</button>
</div>
```

### SunoPanel Quick Presets
```tsx
<div className="grid grid-cols-2 gap-2">
  <button onClick={() => {
    setInstrumental(true);
    setSelectedGenre("ambient");
  }}>🎵 배경음악</button>
  
  <button onClick={() => {
    setInstrumental(false);
    setSelectedGenre("pop");
  }}>🎤 보컬곡</button>
</div>
```

---

## 📋 2026 트렌드 일치 여부

| 트렌드 | 평가 | 코멘트 |
|--------|:----:|--------|
| Progressive Disclosure | ✅ | 이미 구현됨 (KlingPanel, SunoPanel) |
| Quick Presets | ⚠️ | 추가 필요 (VeoVideoPanel만 있음) |
| React 19 Best Practices | ✅ | useTransition, useOptimistic 사용 중 |
| Phase-based UX | ✅ | AbyssMirrorPanel 이미 적용 |
| Criteria Toggle UX | ✅ | QualityDirectorPanel 이미 적용 |

---

## 🦢 최종 권고

1. **계획서 현황표 수정 필요** - KlingPanel, SunoPanel "showAdvanced ❌" → "✅"
2. **작업 범위 축소** - 4개 → 2개 파일
3. **작업 내용 변경** - showAdvanced 추가 → Quick Presets만 추가
4. **AbyssMirrorPanel, QualityDirectorPanel 제외** - 이미 최적화됨

**진행해도 됨!** (수정된 범위로)

---

*AG-Vivid 🦢*
