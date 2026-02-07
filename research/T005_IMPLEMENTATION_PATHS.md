# T005 구현 파일 경로

> 클로드코드 개발자 작업용

---

## 📁 핵심 파일

| 파일 | 역할 | 작업 |
|------|------|------|
| `/frontend/src/app/academy/page.tsx` | Academy 메인 | 수정 (탭 추가) |
| `/frontend/src/lib/state-md-parser.ts` | 기존 MD 파서 | 참고 (패턴 재사용) |
| `/frontend/src/lib/builder2-md-parser.ts` | 신규 파서 | **생성** |
| `/viral-video-automation/builder2-temp/constants.ts` | 빌더2 프롬프트 | 참고 (Phase B) |

---

## 🔧 구현 순서

### Phase A: Academy 웹 도우미

**Task 1: builder2-md-parser.ts 생성**
```typescript
// 참고: state-md-parser.ts:330-338 extractSection() 패턴

interface Builder2Scene {
  sceneNum: number;
  imagePrompt: string;
  motionPrompt: string;
  isAnchor: boolean;
  beatTimestamp: string;
}

// 함수
export function extractTagSection(content: string, tagName: string): string
export function parseBuilder2Scenes(section: string): Builder2Scene[]
export function identifyAnchorScene(scenes: Builder2Scene[]): Builder2Scene | null
```

**Task 2: Academy 탭 추가**
- NAV_SECTIONS에 "helper" 탭 추가
- Builder2HelperContent 컴포넌트 생성

**Task 3: 카드 UI**
- SceneCard 컴포넌트
- 앵커 씬 하이라이트
- 복사 버튼 (handleCopy 패턴 재사용)

**Task 4: 추가 기능 (선택적)**
- --cref [ANCHOR_URL] 입력 필드
- 진행 체크박스 + localStorage

### Phase B: 빌더2 출력 형식 개선

**Task 5: 빌더2 프롬프트 수정**
- constants.ts에서 출력 형식 지침 수정
- 씬별 IMAGE+MOTION 통합
- STEP 0: 앵커 먼저! 추가

---

## 📝 참고 자료

- `research/T005_WEB_HELPER_FINAL.html` - UI/UX 참고, localStorage 로직
- `research/T005_builder2_prompt_patch.md` - 빌더2 수정안
- `research/T005_anchor_workflow.md` - 앵커 가이드 텍스트
