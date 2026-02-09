# 📝 패턴: 메모리 계층 구조 (MemoRAG 스타일)

**작성:** 보미 🐰
**기반:** MemoRAG - Memory-Augmented RAG

---

## 개념

MemoRAG 구조를 OpenClaw에 적용:

```
┌─────────────────────────────────────┐
│  Working Memory (현재 세션)         │  ← 즉각 접근
├─────────────────────────────────────┤
│  MEMORY.md (압축된 전역 컨텍스트)   │  ← 세션 시작 시 로드
├─────────────────────────────────────┤
│  knowledge/ (검색 가능한 지식)      │  ← 필요 시 참조
│    ├── lessons/                     │
│    ├── patterns/                    │
│    ├── decisions/                   │
│    └── reviews/                     │
├─────────────────────────────────────┤
│  memory/*.md (일간 로그)            │  ← 상세 기록
├─────────────────────────────────────┤
│  artifacts/ (산출물)                │  ← 장기 보관
└─────────────────────────────────────┘
```

---

## 접근 규칙

### 항상 로드 (세션 시작)
- IDENTITY.md
- MEMORY.md
- HEARTBEAT.md

### 관련 작업 시 참조
- knowledge/lessons/ - 비슷한 문제 있었나?
- knowledge/patterns/ - 검증된 해결책 있나?

### 필요 시 검색
- memory/YYYY-MM-DD.md - 최근 작업 맥락
- artifacts/ - 과거 산출물

---

## 언제 어디에 저장?

| 정보 유형 | 저장 위치 |
|----------|----------|
| 핵심 맥락 (항상 필요) | MEMORY.md |
| 교훈 (재사용 가능) | knowledge/lessons/ |
| 패턴 (검증됨) | knowledge/patterns/ |
| 결정 (이유 기록) | knowledge/decisions/ |
| 일간 로그 (상세) | memory/YYYY-MM-DD.md |
| 산출물 (결과물) | artifacts/ |

---

## 왜 중요한가?

Karpathy 비전:
> "10억 인지 코어 + 외부 검색"
> "기억이 아닌 사고에 파라미터 사용"

MemoRAG 구현:
- Memory LLM = 압축된 컨텍스트
- Retriever = 필요 시 검색

→ 우리 구조:
- MEMORY.md = 압축된 컨텍스트
- knowledge/ = 검색 가능한 지식

---

*보미 🐰 - 2026-02-09*
