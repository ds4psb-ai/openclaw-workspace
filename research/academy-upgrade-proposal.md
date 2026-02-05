# 🚀 Academy 페이지 업그레이드 제안서

> **작성일**: 2026-02-05
> **작성자**: 소미 🐱
> **대상**: prompty.co.kr/academy

---

## 📊 현재 상태 분석

### 강점
- ✅ Stitch 7 디자인 - 깔끔하고 모던한 UI
- ✅ 전체 워크플로우 시각화 (Home 탭)
- ✅ 단계별 명확한 가이드
- ✅ 외부 도구 링크 통합

### 개선 기회
- ❌ 진행 상태 추적 없음
- ❌ 결과물 관리 기능 없음
- ❌ 오프라인 지원 없음
- ❌ 커뮤니티 연동 없음

---

## 🎯 업그레이드 우선순위

### P0: 즉시 구현 (1-2시간)

#### 1. 진행 상태 트래킹

```typescript
// hooks/useProgress.ts
import { useState, useEffect } from 'react';

interface Progress {
  setup: boolean;
  credit: boolean;
  anchor: boolean;
  builder1: boolean;
  vibe: boolean;
  builder2: boolean;
  image: boolean;
  video: boolean;
}

const STORAGE_KEY = 'academy-progress';

export function useProgress() {
  const [progress, setProgress] = useState<Progress>({
    setup: false,
    credit: false,
    anchor: false,
    builder1: false,
    vibe: false,
    builder2: false,
    image: false,
    video: false,
  });

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) setProgress(JSON.parse(saved));
  }, []);

  const updateProgress = (key: keyof Progress, value: boolean) => {
    const updated = { ...progress, [key]: value };
    setProgress(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  };

  const completedCount = Object.values(progress).filter(Boolean).length;
  const totalCount = Object.keys(progress).length;
  const percentage = Math.round((completedCount / totalCount) * 100);

  return { progress, updateProgress, completedCount, totalCount, percentage };
}
```

#### 2. 프로그레스 바 컴포넌트

```typescript
// components/ProgressBar.tsx
function ProgressBar({ percentage }: { percentage: number }) {
  return (
    <div className="fixed top-0 left-0 right-0 z-50 h-1 bg-gray-800">
      <div 
        className="h-full bg-gradient-to-r from-purple-500 to-emerald-500 transition-all duration-500"
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
}
```

#### 3. 완료 체크박스 추가

```typescript
// 각 ContentCard에 추가
function CompletionCheck({ 
  checked, 
  onToggle,
  label 
}: { 
  checked: boolean; 
  onToggle: () => void;
  label: string;
}) {
  return (
    <button
      onClick={onToggle}
      className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-all ${
        checked 
          ? 'bg-emerald-500/20 text-emerald-400' 
          : 'bg-white/5 text-gray-400 hover:bg-white/10'
      }`}
    >
      <span className="material-symbols-outlined">
        {checked ? 'check_circle' : 'radio_button_unchecked'}
      </span>
      <span className="text-sm">{label}</span>
    </button>
  );
}
```

---

### P1: 주간 내 구현 (4-8시간)

#### 4. 사이드바 진행 상태 표시

```typescript
// NAV_SECTIONS 수정
{section.items.map((item) => {
  const isCompleted = progress[item.key];
  return (
    <li key={item.key} className="relative">
      {isCompleted && (
        <div className="absolute -left-1 top-1/2 -translate-y-1/2 w-2 h-2 bg-emerald-500 rounded-full" />
      )}
      {/* 기존 버튼 */}
    </li>
  );
})}
```

#### 5. "다음 단계" 네비게이션

```typescript
function NextStepButton({ 
  currentTab, 
  progress,
  setActiveTab 
}: { ... }) {
  const TAB_ORDER: TabKey[] = [
    'setup', 'credit', 'anchor', 'builder1', 
    'vibe', 'builder2', 'image', 'video', 'homework'
  ];
  
  const currentIndex = TAB_ORDER.indexOf(currentTab);
  const nextTab = TAB_ORDER[currentIndex + 1];
  
  if (!nextTab || currentTab === 'homework') return null;
  
  return (
    <button
      onClick={() => setActiveTab(nextTab)}
      className="fixed bottom-8 right-8 px-6 py-3 bg-purple-500 text-white rounded-full shadow-lg hover:bg-purple-600 transition-all flex items-center gap-2"
    >
      다음 단계
      <span className="material-symbols-outlined">arrow_forward</span>
    </button>
  );
}
```

#### 6. 복사 성공 토스트

```typescript
function Toast({ message, visible }: { message: string; visible: boolean }) {
  return (
    <div className={`fixed bottom-24 left-1/2 -translate-x-1/2 px-4 py-2 bg-emerald-500 text-white rounded-lg shadow-lg transition-all duration-300 ${
      visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
    }`}>
      {message}
    </div>
  );
}
```

---

### P2: 2주 내 구현

#### 7. 오프라인 지원 (PWA)

```typescript
// next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
});

module.exports = withPWA({
  // existing config
});
```

#### 8. FAQ 아코디언

```typescript
function FAQ({ items }: { items: { q: string; a: string }[] }) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  
  return (
    <div className="space-y-2">
      {items.map((item, i) => (
        <div key={i} className="border border-white/10 rounded-lg overflow-hidden">
          <button
            onClick={() => setOpenIndex(openIndex === i ? null : i)}
            className="w-full p-4 text-left flex justify-between items-center"
          >
            <span className="text-white font-medium">{item.q}</span>
            <span className="material-symbols-outlined text-gray-400">
              {openIndex === i ? 'expand_less' : 'expand_more'}
            </span>
          </button>
          {openIndex === i && (
            <div className="px-4 pb-4 text-gray-400 text-sm">
              {item.a}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
```

---

### P3: 월간 내 구현

#### 9. Discord 피드 연동

```typescript
// API Route: /api/discord-feed
export async function GET() {
  const WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;
  // Discord API로 최근 메시지 가져오기
  // 또는 별도 웹훅 서버 구축
}
```

#### 10. 수강생 갤러리

```typescript
// 관리자 승인된 작품만 표시
interface GalleryItem {
  id: string;
  author: string;
  thumbnail: string;
  videoUrl?: string;
  createdAt: Date;
  likes: number;
}
```

---

## 🎭 Builder 2 업그레이드 제안

### V2.0 변경사항

#### 1. 패러디 모드 확장

```markdown
## 🔓 VARIABLE ELEMENTS (Parody Options)

### Select Parody Mode:
- **[A] Korean Mode** (Default) - 1990s 한국 가정
- **[B] Japanese Mode** - 1990s 일본 가정
- **[C] Chinese Mode** - 1990s 중국 가정
- **[D] Western Retro** - 1980s 미국 가정
- **[E] Anime Mode** - 2D 애니메이션 스타일
- **[F] Fantasy Mode** - 판타지 세계관
- **[G] Custom Mode** - persona.json 사용
```

#### 2. 자동 품질 제안

```markdown
## 📊 AI Quality Analysis

### Auto-Detected Issues:
| Scene | Issue | Suggested Fix |
|-------|-------|---------------|
| 3 | Low character detail | Add "detailed face, clear features" |
| 7 | Lighting mismatch | Change "warm" to "cool fluorescent" |

### One-Click Fix
[Apply All Suggestions] → AI가 자동으로 프롬프트 수정
```

#### 3. 바이럴 훅 상세 분석

```markdown
## 🔥 Viral Hook Analysis

### Emotional Timeline
```
0s ━━━━━━ 5s ━━━━━━ 10s ━━━━━━ 15s ━━━━━━ 17s
   ↑           ↑              ↑           ↑
  Hook     Build-up      Peak(!)     Resolution
 (warm)   (tension)     (glitch)     (lonely)
```

### Recommended Enhancements
- Scene 8 Glitch: 더 강한 시각적 전환 (0.5s → 0.3s)
- Scene 10 Selfie: 4초 → 5초 (감정 여운)
```

#### 4. Kling 3.0 / Veo 3.1 최적화

```markdown
## 🎬 Motion Prompts (V2.0)

### Kling 3.0 Optimized
- Character Lock: 자동 활성화
- 4K Cinematic: 기본값
- Multi-Shot: 스토리보드 지원

### Veo 3.1 Audio Integration
- Auto SFX: "family chatter", "cake candles"
- Dialogue Sync: 대사 타이밍 자동 감지
- BGM Suggestion: 90s nostalgic instrumental
```

---

## 📅 구현 일정 제안

| 주차 | 작업 | 예상 시간 |
|------|------|----------|
| Week 1 | P0 구현 (진행 상태 트래킹) | 4h |
| Week 1 | P1 구현 (다음 단계, 토스트) | 4h |
| Week 2 | Builder 2 V2.0 시스템 프롬프트 | 8h |
| Week 2 | P2 구현 (PWA, FAQ) | 6h |
| Week 3 | 테스트 및 버그 수정 | 4h |
| Week 4 | P3 구현 (커뮤니티) | 8h |

**총 예상 시간: 34시간**

---

## 📝 즉시 적용 가능한 변경

### 1. Home 탭에 진행률 추가

현재 Hero 섹션 아래에 추가:

```tsx
{/* Progress Section */}
<div className="mt-8 max-w-md mx-auto">
  <div className="flex justify-between text-sm mb-2">
    <span className="text-gray-400">진행률</span>
    <span className="text-purple-400">{percentage}%</span>
  </div>
  <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
    <div 
      className="h-full bg-gradient-to-r from-purple-500 to-emerald-500"
      style={{ width: `${percentage}%` }}
    />
  </div>
</div>
```

### 2. 각 탭에 완료 버튼 추가

ContentCard 하단에:

```tsx
<div className="mt-6 pt-4 border-t border-white/10 flex justify-end">
  <CompletionCheck
    checked={progress[activeTab]}
    onToggle={() => updateProgress(activeTab, !progress[activeTab])}
    label="이 단계 완료"
  />
</div>
```

---

*이 제안서는 테드의 피드백 후 수정될 수 있습니다.*
