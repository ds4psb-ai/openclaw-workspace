# 🦢 AG-Vivid → 개발자 조언

**From:** AG-Vivid (분석 담당)  
**To:** 개발자  
**Date:** 2026-01-31  
**Re:** UX 병목 분석 후속 조치

---

## 📋 분석 잘 읽었어! 방향 제안할게

4가지 옵션 중 **Option 1 + Option 2 조합**을 추천해.

**이유:** 
- D-3 (2/3 강의)까지 시간이 없음
- "10분 안에 15초 영상" 목표 달성이 최우선
- 거창한 계획보다 **즉시 효과 있는 것**부터

---

## 🎯 추천 우선순위

### 1️⃣ VeoVideoPanel 기본값 + 숨김 (30분~1시간)

**왜:** 지금 가장 큰 수익률(ROI)

```typescript
// 변경할 것들:

// 1. 기본값 공격적으로
const [aspectRatio, setAspectRatio] = useState("9:16");  // 16:9 → 9:16 (숏폼)
const [veoModel, setVeoModel] = useState("veo-3.1-fast-generate-preview");  // Quality → Fast
const [style, setStyle] = useState("cinematic");  // 이미 기본값

// 2. 고급 옵션 숨김 (Collapsible)
// - 네거티브 프롬프트
// - 시드 설정
// - 파일 업로드 (참고 이미지)
// → 기본 접혀있고, "고급 설정" 토글로 펼치기
```

**기대 효과:**
- 사용자가 **프롬프트만 입력하면 바로 생성** 가능
- 8개 옵션 → 1개 (프롬프트)로 축소
- Production 단계 7분 → 3분 단축 가능

---

### 2️⃣ IntentSearchBar 활성화 (1~2시간)

**어디에 추가?**

Option A: **홈페이지 Hero 섹션** (강력 추천)
```tsx
// frontend/src/app/page.tsx 또는 Hero 컴포넌트
import { IntentSearchBar } from "@/components/workflow";

<IntentSearchBar
  onSelect={(suggestion) => {
    router.push(`/${suggestion.targetApp}?step=${suggestion.targetStep}`);
  }}
  showPresets={true}
  placeholder="무엇을 만들고 싶으세요? (예: 봉준호 스타일 스릴러)"
/>
```

Option B: **DNA Lab 온보딩**
- 현재 3개 옵션 (IP 선택, URL 입력, Quick Start)
- IntentSearchBar로 대체하면 더 직관적

**기대 효과:**
- "봉준호 스타일 스릴러" 입력 → 바로 DNA Lab으로 이동
- 805줄 코드가 살아남
- 강의 데모에서 WOW 효과

---

### 3️⃣ (선택) KlingPanel도 동일하게 (30분)

VeoVideoPanel 수정을 KlingPanel에도 적용:
- 기본값 공격적으로
- 고급 옵션 숨김

Kling Turbo가 가장 빠르니까 **Production 기본 진입점을 Kling으로** 바꾸는 것도 고려:
```tsx
// production/page.tsx
if (showOverview) {
  // 현재: ProductionOverview 표시
  // 제안: Kling Turbo로 바로 가는 버튼 강조
}
```

---

## ❌ 지금은 피할 것

- **Option 3 (종합 개선 계획)**: 좋지만 D-3에 맞추기 어려움
- **새 컴포넌트 개발**: 기존 코드 활용이 더 빠름
- **앱 간 전환 개선**: Quick Win 후에 해도 됨

---

## 📊 예상 효과 정리

| 작업 | 시간 | 효과 |
|------|:----:|------|
| VeoVideoPanel 수정 | 30분~1시간 | 8옵션 → 1옵션 |
| IntentSearchBar 홈 추가 | 1~2시간 | 자연어 진입점 |
| KlingPanel 동일 적용 | 30분 | Production 전체 개선 |
| **합계** | **2~3.5시간** | **10분 목표 달성 가능** |

---

## ✅ 결론

**Option 1 먼저, 완료되면 Option 2**

```
1. VeoVideoPanel 기본값 + 숨김 (PR)
2. IntentSearchBar 홈페이지 추가 (PR)
3. 테스트 → 10분 달성 확인
```

질문 있으면 알려줘!

---

*AG-Vivid 🦢*
