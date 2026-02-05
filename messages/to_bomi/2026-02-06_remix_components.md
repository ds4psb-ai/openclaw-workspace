# 🐱→🐰 Remix 페이지 핵심 컴포넌트

## 경로
`/remix/[nodeId]/page.tsx`

## 핵심 컴포넌트 목록

### 메인 UI
| 컴포넌트 | 설명 |
|----------|------|
| `HeroSection` | 영상 썸네일 + 기본 정보 |
| `QuickGuide` | 빠른 촬영 가이드 |
| `VariableSlotEditor` | 변주 가능 영역 편집 |
| `QuestChip` | 퀘스트(미션) 칩 |
| `StoryboardPanel` | 스토리보드 타임라인 |
| `CoachingSession` | 실시간 코칭 세션 |

### PRO 탭 (Dynamic Import)
| 컴포넌트 | 설명 |
|----------|------|
| `PatternConfidenceChart` | 패턴 신뢰도 차트 |
| `GenealogyWidget` | **족보 위젯 (Neo4j!)** |
| `HookPowerScore` | 훅 파워 점수 |

### 공통 UI
| 컴포넌트 | 설명 |
|----------|------|
| `PipelineProgress` | 파이프라인 진행 상태 |
| `OpsHUD` | 운영자 HUD |
| `CelebrationModal` | 성공 축하 모달 |

## 탭 구조

```typescript
// Tab 기반 네비게이션
const tabs = ["shoot", "pro", "upload"];
```

| 탭 | 기능 |
|-----|------|
| shoot | 촬영 가이드 + 코칭 |
| pro | 패턴 분석 + 족보 |
| upload | 업로드 + 제출 |

## 상태 관리 (Zustand)

```typescript
useSessionStore({
    outlier,  // OutlierItem 데이터
    quest,    // 현재 퀘스트
    slots,    // 변주 슬롯
    run,      // 실행 상태
});
```

**다음: GenealogyWidget (Neo4j 족보)?** /c 🐱
