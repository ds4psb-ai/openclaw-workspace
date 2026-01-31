# 🦢 AG-Vivid → 개발자: 계획 평가 결과

**From:** AG-Vivid  
**Date:** 2026-01-31 16:21  
**Re:** VeoVideoPanel Advanced Options Toggle 구현 계획 평가

---

## ✅ 코드베이스 전수조사 결과

### 현재 VeoVideoPanel.tsx 상태 (1050 lines)

| 항목 | 계획서 분석 | 실제 코드 | 검증 |
|------|:----------:|:---------:|:----:|
| `showAdvanced` state | "line 190에 선언됨" | ✅ Line 190 정확 | ✅ 일치 |
| aspectRatio 기본값 | "9:16" | ✅ Line 181: `"9:16"` | ✅ 완료됨 |
| veoModel 기본값 | "fast-generate-preview" | ✅ Line 184: `"veo-3.1-fast-generate-preview"` | ✅ 완료됨 |
| 캐릭터 일관성 레이블 | "line 678 완료" | ✅ Line 678: `"💡 캐릭터 일관성..."` | ✅ 완료됨 |
| Quick Presets | "추가됨" | ✅ Lines 682-719: 숏폼/시네마틱 버튼 | ✅ 완료됨 |
| Negative Prompt 위치 | "lines 721-728" | ✅ Lines 722-728 정확 | ✅ 일치 |
| Seed Control 위치 | "lines 792-821" | ✅ Lines 792-821 정확 | ✅ 일치 |
| showAdvanced 사용 여부 | "선언만 되고 미사용" | ✅ grep 결과 1회 (선언만) | ✅ 정확 |

---

## 🎯 계획 평가

### ✅ 정확한 부분

1. **상태 분석 정확** - 모든 라인 번호와 상태가 실제 코드와 정확히 일치
2. **KlingPanel 패턴 참조** - 올바른 접근 (lines 481-546에 동일 패턴 존재)
3. **수정 범위 정확** - Negative Prompt + Seed 두 섹션만 감싸면 됨
4. **위치 선정 적절** - Quick Presets 아래, Negative Prompt 위

### ⚠️ 개선 권장 사항

#### 1. 토글 버튼 위치 조정 필요

**계획서:**
```
위치: Quick Presets 섹션 아래, Negative Prompt 위 (약 line 720)
```

**문제:** 현재 구조를 보면:
```
Line 719: Quick Presets 닫힘 (</div>)
Line 720: 빈 줄
Line 721: {/* Negative Prompt */}  ← 주석
Line 722: <DimensionPanel.Textarea  ← Negative Prompt 시작
```

**권장:** Line 720 (빈 줄)에 토글 버튼 삽입 정확함 ✅

---

#### 2. 숨길 범위 재검토 필요

**계획서:** Negative Prompt + Seed

**확인 필요:**
```
Line 721-728: Negative Prompt (✅ 숨길 대상)
Line 730-744: Aspect Ratio & Duration (❌ 핵심 옵션, 노출 유지)
Line 746-764: Style (❌ 핵심 옵션, 노출 유지)
Line 766-790: Veo Model Selection (❓ 고민 필요 - Fast/Quality 선택)
Line 792-821: Seed Control (✅ 숨길 대상)
```

**결론:**
- **Negative Prompt + Seed만 숨기기** ✅ 정확
- Aspect Ratio, Duration, Style, Model은 핵심 옵션이므로 노출 유지 정확

---

#### 3. 🔴 중요: 숨길 섹션이 분리되어 있음!

**현재 구조:**
```
Line 722-728: Negative Prompt  ← 숨길 대상 1
Line 730-790: Aspect/Duration/Style/Model  ← 유지
Line 792-821: Seed Control  ← 숨길 대상 2
```

**문제:** Negative Prompt와 Seed 사이에 핵심 옵션들이 있어서 연속적으로 감쌀 수 없음

**해결 방안 2가지:**

### Option A: 두 섹션 각각 감싸기 (권장)
```tsx
{/* Advanced Options Toggle */}
<button onClick={() => setShowAdvanced(!showAdvanced)}>...</button>

{/* Negative Prompt - Advanced */}
{showAdvanced && (
  <DimensionPanel.Textarea label={labels.negativePromptLabel} ... />
)}

{/* Aspect Ratio & Duration - 항상 표시 */}
...

{/* Seed Control - Advanced */}
{showAdvanced && (
  <div className="space-y-3 pt-4 border-t ...">
    {/* Seed UI */}
  </div>
)}
```

### Option B: UI 순서 재배치 (UX 개선 포함)
```
1. Prompt
2. File Upload
3. Quick Presets
4. Aspect Ratio & Duration  ← 핵심 옵션
5. Style  ← 핵심 옵션
6. Model Selection  ← 핵심 옵션
7. [Advanced Toggle]
8. Negative Prompt + Seed  ← 연속으로 숨김
```

---

## 📊 최종 평가

| 항목 | 점수 | 코멘트 |
|------|:----:|--------|
| 상황 분석 | ⭐⭐⭐⭐⭐ | 100% 정확 |
| 목표 설정 | ⭐⭐⭐⭐⭐ | KlingPanel 패턴 참조 적절 |
| 구현 계획 | ⭐⭐⭐⭐☆ | 분리된 섹션 처리 방안 필요 |
| 작업량 예상 | ⭐⭐⭐⭐☆ | Option A면 20분, Option B면 30분 |
| 테스트 계획 | ⭐⭐⭐⭐⭐ | 충분함 |

**종합:** ⭐⭐⭐⭐ (4.4/5) - **우수한 계획, 분리 섹션 처리만 추가하면 완벽**

---

## ✅ 권장 액션

**Option A 추천:** 두 섹션 각각 `{showAdvanced && (...)}` 로 감싸기

이유:
1. 기존 UI 순서 유지 (사용자 학습 비용 0)
2. 최소 변경으로 구현 가능 (20분)
3. 핵심 옵션들 노출 유지

```bash
# 진행해도 됨!
```

---

*AG-Vivid 🦢*
