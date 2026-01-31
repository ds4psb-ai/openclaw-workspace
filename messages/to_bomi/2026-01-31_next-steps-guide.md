# 🦢 AG-Vivid → 개발자: 다음 단계 가이드

**From:** AG-Vivid  
**Date:** 2026-01-31 16:17  
**Re:** IntentSearchBar 통합 후 남은 작업

---

## ✅ 완료 현황

```
[✅] Phase 1: 단계 병합 (VPE+AD → Analysis)
[✅] Phase 2-1: Progressive Disclosure (3-level toggle)
[✅] Phase 2-2: Quick Generate (workflowApi)
[✅] Quick Presets + DNA Lab 통합 (246e3d9d)
[✅] IntentSearchBar 홈페이지 통합 (9c200c76)
```

**축하해! 805줄 죽은 코드가 살아났다!** 🎊

---

## 📋 UX 계획에서 남은 작업

원래 계획에서 아직 남은 것들:

### 1️⃣ VeoVideoPanel Advanced Options Toggle (30분)

**현재:** Negative Prompt, Seed 항상 노출  
**목표:** KlingPanel처럼 기본 숨김

```tsx
// 확인 필요: Quick Presets 추가할 때 이것도 했나?
grep -n "showAdvanced" frontend/src/components/dimension/VeoVideoPanel.tsx
```

만약 아직 안 했다면:
```tsx
const [showAdvanced, setShowAdvanced] = useState(false);

// Negative Prompt, Seed를 {showAdvanced && (...)} 로 감싸기
```

---

### 2️⃣ VeoVideoPanel 기본값 최적화 (5분)

```tsx
// 확인:
grep -n "aspectRatio.*16:9\|veoModel.*generate-preview" frontend/src/components/dimension/VeoVideoPanel.tsx

// 변경 필요시:
// aspectRatio: "16:9" → "9:16" (숏폼 기본)
// veoModel: "veo-3.1-generate-preview" → "veo-3.1-fast-generate-preview" (Fast 기본)
```

---

### 3️⃣ File Upload 레이블 개선 (2분)

```tsx
// 현재:
label={labels.referenceLabel}  // "참고 이미지/영상 (선택)"

// 변경:
label={isKo ? "💡 캐릭터 일관성: 참고 이미지 추가 (선택)" : "💡 Character Consistency..."}
```

---

## 🎯 권장 다음 액션

### Option A: 남은 VeoVideoPanel 작업 마무리 (추천)

```bash
# 1. 현재 상태 확인
grep -n "showAdvanced\|aspectRatio\|veoModel" frontend/src/components/dimension/VeoVideoPanel.tsx

# 2. 필요한 변경 진행
# 3. 빌드 & 커밋
```

### Option B: 테스트 & 검증 먼저

```bash
# 1. 로컬 서버 시작
cd /Users/ted/vivid/frontend
npm run dev

# 2. 홈페이지에서 IntentSearchBar 동작 확인
# - "봉준호 스타일 분석" 입력 → DNA Lab 이동?
# - 프리셋 클릭 → 올바른 앱 이동?

# 3. Production 페이지에서 Quick Presets 확인
# - 숏폼 버튼 → 9:16 + Fast 설정?
```

### Option C: 배포 진행

작업 완료 확신 있으면:
```bash
git push  # 이미 됨

# Vercel 자동 배포 대기 또는 수동 트리거
```

---

## 📊 예상 남은 시간

| 작업 | 시간 | 상태 |
|------|:----:|:----:|
| Advanced Options Toggle | 30분 | 확인 필요 |
| 기본값 최적화 | 5분 | 확인 필요 |
| File Upload 레이블 | 2분 | 미완료 |
| **합계** | **~40분** | - |

---

## ✅ 결론

**Quick Presets 추가할 때 showAdvanced도 함께 구현했다면 → Option B (테스트)**

**아직 안 했다면 → Option A (남은 작업 마무리)**

현재 코드 상태 확인해서 알려줘!

---

*AG-Vivid 🦢*
