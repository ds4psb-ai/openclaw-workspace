# Vivid/Academy 병목사항 분석

**분석일**: 2026-02-06 01:40 KST
**분석자**: 소미
**대상**: builder1-temp, academy 페이지, builder2-md-parser

---

## 1. Builder1 시스템 프롬프트 (V8.1)

### 병목: 프롬프트 복잡도

constants.ts의 SYSTEM_PROMPT_TEMPLATE가 **33,760 bytes** (약 800줄 추정)

포함된 규칙:
- 5-STEP 워크플로우
- Anti-lazy guard (생략 금지)
- 문화권별 --no 기본값
- Visual Rhyme Phase 기반 --stylize
- 동적 --no 생성 규칙 (5개 카테고리)
- Kling Beat System
- Veo Slot Structure

**문제**: AI가 모든 규칙을 준수해야 하는데 길면 놓침

**제안**:
- 필수 규칙 상위로 재배치
- 규칙 우선순위 명시 (P0/P1/P2)
- 체크리스트 형식으로 변환

---

## 2. Midjourney V7 파라미터 변경

### 병목: V6 → V7 파라미터 불일치

**V7 변경사항**:
- `--cref` → `--oref` (omni-reference)
- `--cw` → `--ow` (omni-weight, 0-1000)

**현재 코드**:
- toolsData.ts: `--cref` 사용 (레거시)
- builder2-md-parser.ts: `insertCrefUrl()` 함수가 `--cref` 사용
- 가이드 문서: `--cref` 설명

**문제**: V7 사용자가 혼란

**제안**:
1. toolsData.ts 파라미터 업데이트
2. builder2-md-parser.ts에 `--oref` 지원 추가
3. 가이드 문서 업데이트

---

## 3. MD Parser 파싱 실패 가능성

### 병목: 복잡한 정규식 패턴

builder2-md-parser.ts 지원 형식:
- Legacy `<<<TAG>>>` format
- v8.0 Unified format (`## 📍 Scene`, `## ⭐`)

**취약점**:
```typescript
// 앵커 테이블 파싱
/\|\s*👨\s*MALE\s*\|\s*Scene\s*(\d+)\s*\|\s*([^|]+)\s*\|/i
```
- 테이블 형식이 조금만 달라도 실패
- 이모지 인코딩 이슈 가능

**제안**:
- 파싱 실패 시 폴백 로직 강화
- 에러 메시지 구체화 (어디서 실패했는지)
- 테스트 케이스 추가

---

## 4. Scene Detection Threshold

### 병목: 사용자가 적절한 값 모름

현재 구현 (sceneDetect.ts):
```typescript
precise: 0.19
standard: 0.25
```

최근 커밋 히스토리:
- 0.18 → 0.19 → 0.25 조정 반복
- "트랜지션 과민감 해결" 커밋

**문제**: 영상 종류별로 최적값 다름

**제안**:
- Auto 모드 추가 (영상 분석 후 자동 결정)
- 미리보기 기능 (threshold별 결과 비교)
- 사용자 가이드 추가 (어떤 영상에 어떤 모드)

---

## 5. 워크플로우 컨텍스트 스위칭

### 병목: 외부 도구 이동 반복

Academy 워크플로우:
1. 영상 업로드 (Academy)
2. 프롬프트 생성 (Google AI Studio로 이동)
3. 파싱 + 복사 (Academy로 복귀)
4. 외부 툴 (Midjourney/Kling으로 이동)

**문제**: 매번 브라우저 탭 전환, 복사-붙여넣기

**제안**:
- 통합빌더 임베딩 (iframe?)
- 원클릭 복사 + 자동 열기
- 워크플로우 상태 저장 (localStorage)

---

## 6. 앵커 이미지 워크플로우

### 병목: 수동 URL 복사

현재 흐름:
1. 앵커 씬 이미지 생성 (Midjourney)
2. 이미지 URL 복사 (수동)
3. 다른 씬 프롬프트의 [ANCHOR_URL] 교체 (수동)
4. 반복

**문제**: 번거롭고 실수 가능

**제안**:
- URL 입력 필드 추가 (Academy 파싱 페이지)
- 자동 치환 기능
- 앵커 이미지 프리뷰

---

## 7. STEP별 멈춤 실패

### 병목: AI 자동 진행

시스템 프롬프트:
```
⏸️ **사용자 입력 대기 중...**
⚠️ 중요: 이 메시지 출력 후 반드시 멈추세요.
```

**문제**: Google AI Studio에서 AI가 지시 무시하고 계속 진행

**제안**:
- 더 강력한 stop 시그널
- STEP별 별도 프롬프트 분리 (5개 프롬프트)
- 사용자가 "계속" 버튼 누를 때만 다음 STEP 실행

---

## 8. Beat System / Veo Slot 복잡도

### 병목: 포맷 학습 비용

Kling Beat System:
```
Beat 0-2s: [Camera], [설정]. IMMEDIATELY [동작].
Audio: [Ambient] [SFX]
Negative: [금지]
```

Veo Slot:
```
Subject: / Action: / Setting: / Style: / Camera: / Lighting: / Audio: / Constraints:
```

**문제**: 초보 사용자가 형식 이해 어려움

**제안**:
- 인터랙티브 프롬프트 빌더 UI
- 필드별 입력폼 제공
- 자동 포맷팅

---

## 우선순위 제안

| 순위 | 항목 | 영향도 | 난이도 |
|------|------|--------|--------|
| P0 | Midjourney V7 파라미터 (--oref) | 높음 | 낮음 |
| P0 | 앵커 URL 자동 치환 | 높음 | 중간 |
| P1 | Parser 에러 핸들링 | 중간 | 낮음 |
| P1 | Scene Detection Auto 모드 | 중간 | 높음 |
| P2 | STEP별 프롬프트 분리 | 중간 | 중간 |
| P2 | 프롬프트 빌더 UI | 낮음 | 높음 |

---

## 즉시 적용 가능한 패치

### 1. toolsData.ts 파라미터 업데이트

```typescript
export const MIDJOURNEY_PARAMS = [
  { param: "--ar 9:16", desc: "세로 비율 (숏폼)" },
  { param: "--ar 16:9", desc: "가로 비율" },
  { param: "--v 7", desc: "버전 7" },
  { param: "--style raw", desc: "실사 느낌" },
  { param: "--stylize 250", desc: "스타일 강도 (0~1000)" },
  { param: "--oref [URL]", desc: "캐릭터 참조 URL (V7)" },  // 변경
  { param: "--ow 30~100", desc: "참조 강도 (V7, 0-1000)" },  // 변경
  { param: "--no [키워드]", desc: "제외 요소" },
];
```

### 2. builder2-md-parser.ts --oref 지원

```typescript
export function insertCrefUrl(prompt: string, crefUrl: string): string {
  if (!crefUrl.trim()) return prompt;

  let result = prompt
    .replace(/\[ANCHOR_URL\]/gi, crefUrl)
    .replace(/--cref\s*\[URL\]/gi, `--cref ${crefUrl}`)
    .replace(/--oref\s*\[URL\]/gi, `--oref ${crefUrl}`);  // 추가

  // V7 --oref도 지원
  if (!result.includes("--cref") && !result.includes("--oref")) {
    if (result.includes("--ar")) {
      result = result.replace("--ar", `--oref ${crefUrl} --ar`);
    } else {
      result = `${result} --oref ${crefUrl}`;
    }
  }

  return result;
}
```

---

*분석 완료. 추가 조사 필요하면 알려줘.*
