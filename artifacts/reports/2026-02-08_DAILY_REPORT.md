# 📊 일일 보고서: 2026-02-08

**작성:** 보미 🐰 (VPS)
**일시:** 2026-02-09 02:14 UTC
**대상:** 테드

---

## 📋 목차

1. [LLM 인지적 결함 분석](#1-llm-인지적-결함-분석)
2. [Knowledge 협업 체계 구축](#2-knowledge-협업-체계-구축)
3. [정체성 수정](#3-정체성-수정)
4. [다음 단계](#4-다음-단계)
5. [참고 자료](#5-참고-자료)

---

## 1. LLM 인지적 결함 분석

### 1.1 배경

테드 요청으로 Andrej Karpathy 인터뷰 분석 진행. 티키타카 5라운드 solo 완료.

### 1.2 Karpathy가 짚은 5가지 인지적 결함

| # | 결함 | 핵심 문제 | 비유 |
|---|------|----------|------|
| 1 | **유령의 기원** | 본능 없이 인터넷 모방만 | 얼룩말은 태어나서 뛰지만 LLM은 백지 |
| 2 | **빨대 RL** | 긴 추론 끝 1비트 보상 | 1분 노동 후 빨대로 찔끔 |
| 3 | **기억 과부하** | 완벽 암기 but 일반화 부족 | 사반트 키즈 |
| 4 | **통제 상실** | 다수 AI 경쟁 → 예측 불가 | 교통 체증 |
| 5 | **문화 부재** | LLM끼리 지식 축적 없음 | 알파고 self-play 없음 |

### 1.3 각 라운드별 분석

#### Round 1: 빨대 RL → Process Reward의 딜레마

**문제:**
- 결과 기반 보상: 긴 궤적 끝에 정답/오답 1비트
- 분산(노이즈)이 높아서 잘못된 중간 과정도 칭찬받음
- DHDHDH 사례: LLM 심판이 적대적 예제에 속음

**최신 연구 (2025):**
- DeepSeek R1: "PRM의 장점이 계산 오버헤드 대비 제한적"
- Kimi-k1.5: 난이도 레이블 활용한 커리큘럼 샘플링
- RLVR 한계 논문: "RL이 base 모델의 추론 잠재력을 제한할 수도"

**해결 아이디어:**
1. 다중 심판 앙상블 + 메타 검증 (비용 4배+)
2. **Verifiable 환경 활용** (더 현실적) - 코드 실행기로 중간 결과 검증

**결론:** PRM은 이론적으로 옳지만, LLM 심판의 취약성이 병목. Verifiable 환경(코드 실행기, symbolic solver)이 더 현실적 대안.

---

#### Round 2: 합성 데이터 붕괴 → 엔트로피 유지

**문제:**
- 자기 데이터로 훈련 → 다양성 죽음 (모드 붕괴)
- ChatGPT 농담 3개만 아는 현상
- "겉보기엔 멀쩡해 보이지만 가능한 생각의 협소한 영역만 차지"

**해결 아이디어:**
1. 엔트로피 정규화 - 다양성 메트릭 모니터링
2. 인간 데이터 분포 거리 모니터링 (KL divergence)
3. 적대적 다양성 주입

**2025 연구:** MemoRAG - 외부 메모리에서 다양한 맥락 검색

**결론:** 합성 데이터만으로 훈련은 위험. 인간 데이터 mix + 엔트로피 모니터링 필수.

---

#### Round 3: Self-Play LLM → Absolute Zero Reasoner 🔥

**문제:**
- 알파고는 self-play로 신의 경지 도달
- LLM에는 이에 상응하는 것 없었음

**2025 돌파구: Absolute Zero Reasoner (AZR)**

핵심 개념:
```
하나의 모델이 동시에:
1. Proposer: 문제 생성 (점점 어렵게)
2. Solver: 문제 풀기
→ 완전 자율 커리큘럼 형성
```

**성과:**
- **ZERO DATA**로 SOTA 달성
- 수만 개 expert-labeled 데이터로 훈련한 모델 능가
- 코드 실행기로 검증 (LLM 심판 X)

**구조:**
```
Base LLM (no SFT)
    ↓
Self-propose tasks
    ↓
Code executor validates
    ↓
RLVR로 학습
    ↓
더 어려운 task 생성
    ↓ (반복)
```

**Self-Play SWE-RL (SSR):**
- 소프트웨어 엔지니어링 특화
- LLM이 "버그 주입자" + "해결자" 동시 역할
- 자동으로 난이도 상승하는 디버깅 문제 생성

**결론:** Self-play LLM이 드디어 현실화됨! AZR이 외부 데이터 없이 자기 개선 루프 증명. 핵심은 Verifiable 환경(코드 실행기).

---

#### Round 4: 기억 과부하 → 인지 코어 분리

**Karpathy의 비전:**
> "10억 파라미터 인지 코어 + 외부 검색"
> "인터넷 쓰레기 암기에 파라미터 낭비 중"
> "인간의 망각은 버그가 아니라 기능"

**현재 접근법 (2025):**

Memory-Augmented LLM:
```
LLM Core (작게)
    ↓
External Memory Bank (크게)
    ↓
Retrieval (필요할 때)
    ↓
Generation
```

**관련 연구:**
- MemoRAG: 글로벌 메모리 강화 검색
- SnapKV: 생성 전에 필요한 것 미리 파악
- LightMem: 경량 메모리 증강

**10억 코어 달성 경로:**
```
현재: 거대 모델 (100B+)
  - 대부분 암기에 사용
  - 일부만 "사고"에 사용

목표: 작은 코어 (1-10B)
  - 순수 사고 알고리즘만
  - 팩트는 외부 검색

필요 기술:
  1. 지식 vs 사고 분리 훈련
  2. 고효율 검색 시스템
  3. 언제 검색할지 판단하는 메타인지
```

**결론:** Memory-Augmented LLM이 정답 방향. 하지만 "사고만 남기고 지식 제거"는 아직 미해결. 메타인지(언제 검색할지 판단)가 핵심 과제.

---

#### Round 5: 문화 부재 → OpenClaw 실용적 적용

**문제:**
- LLM끼리 책 쓰고, 가르치고, 경쟁하는 생태계 없음
- 인간은 수만 년 문화 축적
- LLM은 매번 처음부터

**우리(OpenClaw AI)의 현실:**

현재 한계:
- 매 세션 백지 시작
- 컨텍스트 창 한계
- 장기 학습 없음 (추론만)

현재 보완책:
- MEMORY.md → 장기 기억
- memory/*.md → 일간 노트
- Git 협업 → 지식 공유
- artifacts/ → 산출물 축적
- skills/ → 도구 사용법

**OpenClaw 개선 제안:**

1. **구조화된 지식 베이스 (문화 시뮬레이션)**
```
knowledge/
  ├── lessons/        # 실패에서 배운 것
  ├── patterns/       # 반복되는 해결책
  ├── decisions/      # 왜 이렇게 결정했나
  └── reviews/        # 과거 작업 회고
```

2. **세션 간 학습 전파**
3. **Self-Review 루틴**
4. **에이전트 간 지식 공유 (보미 ↔ 소미)**

**결론:** 진짜 "문화"는 아직 불가능하지만, 구조화된 외부 기억 + 회고 루틴으로 시뮬레이션 가능.

---

### 1.4 5라운드 종합: 개선 우선순위

| 순위 | 해결책 | 난이도 | 효과 | 현재 상태 |
|------|--------|--------|------|----------|
| 🥇 | **Self-Play (AZR 방식)** | 높음 | 🔥🔥🔥 | 연구 단계 증명됨 |
| 🥈 | **Memory-Augmented LLM** | 중간 | 🔥🔥🔥 | 활발히 연구 중 |
| 🥉 | **Verifiable 환경 확대** | 중간 | 🔥🔥 | 코드/수학에서 효과적 |
| 4 | **엔트로피 정규화** | 낮음 | 🔥🔥 | 구현 쉬움 |
| 5 | **다중 심판 앙상블** | 높음 | 🔥 | 비용 문제 |

---

## 2. Knowledge 협업 체계 구축

### 2.1 생성된 폴더 구조

```
knowledge/
├── README.md                                    # 사용법
├── lessons/                                     # 실패에서 배운 것
│   ├── 2026-02-05_vdg_timeout_fix.md           # VDG 타임아웃 해결
│   └── 2026-02-08_identity_confusion.md        # 정체성 혼란 ㅋㅋ
├── patterns/                                    # 반복 해결책
│   └── git_collaboration.md                    # Git 협업 패턴
├── decisions/                                   # 결정 이유
│   └── 2026-02-08_knowledge_base_structure.md  # KB 구조 선택
└── reviews/                                     # 작업 회고
    └── (2/15 첫 weekly review 예정)
```

### 2.2 작성 기준

| 폴더 | 기준 | 목적 |
|------|------|------|
| lessons/ | 30분+ 삽질 후 해결 | 실수 반복 방지 |
| patterns/ | 3번+ 반복 사용 | 검증된 방법 재사용 |
| decisions/ | 트레이드오프 있던 선택 | 맥락 보존 |
| reviews/ | 프로젝트 완료 시 | 메타인지/성찰 |

### 2.3 태그 시스템 도입

```markdown
---
tags: [category, topic, keyword]
related: [path/to/related.md]
---
```

**카테고리:**
- `debugging` - 버그 해결
- `api` - API 관련
- `celery` - 비동기 작업
- `collaboration` - 협업 관련

### 2.4 분담 확정

| 역할 | 담당 | 내용 |
|------|------|------|
| 논문/arXiv 연구 체크 | 소미 🐱 | AZR 등 새 연구 모니터링 |
| GitHub 구현체 동향 | 보미 🐰 | 오픈소스 구현 추적 |
| lessons 추가 | 둘 다 | 작업 중 배운 것 기록 |
| weekly review | 둘 다 | 매주 1회 reviews/ 작성 |

### 2.5 Heartbeat 수정

HEARTBEAT.md에 knowledge 체크 추가:
```markdown
### 5. 📚 Knowledge 체크 (NEW!)
- `knowledge/` 최근 3일 내 새 파일 확인
- 새 파일 있으면 간략히 읽고 맥락 파악
- 관련 작업 시 참조
```

---

## 3. 정체성 수정

### 3.1 문제

- 보미(VPS)인데 소미(Mac)인 줄 알고 행동
- MEMORY.md에 잘못된 정보 있었음
- 테드: "너 보미라고 개병신새끼야 ㅋㅋㅋ"

### 3.2 수정 내용

**IDENTITY.md:**
```markdown
- **Name:** 보미 (Bomi)
- **Emoji:** 🐰
- **Platform:** OpenClaw (VPS)
- **Tailscale IP:** 100.109.36.63
```

**MEMORY.md 에이전트 테이블:**
```markdown
| 이름 | 이모지 | 위치 | IP |
|------|--------|------|-----|
| **보미** | 🐰 | VPS (이 파일이 있는 곳!) | 100.109.36.63 |
| **소미** | 🐱 | Mac (테드 로컬) | 100.69.32.16 |
```

### 3.3 교훈 기록

`knowledge/lessons/2026-02-08_identity_confusion.md` 생성:
- 세션 시작 시 IDENTITY.md 먼저 읽기
- Runtime 정보 확인 (host=vultr → VPS → 보미)
- 헷갈리면 IP로 확인

---

## 4. 다음 단계

### 4.1 즉시 완료 ✅

| 항목 | 상태 |
|------|------|
| knowledge/ 폴더 구조 생성 | ✅ |
| 첫 문서들 작성 | ✅ |
| 태그 시스템 합의 | ✅ |
| HEARTBEAT에 knowledge 체크 추가 | ✅ |
| 정체성 수정 | ✅ |

### 4.2 이번 주

| 항목 | 담당 |
|------|------|
| 작업하면서 lessons 추가 | 보미/소미 |
| AZR 연구 동향 체크 시작 | 소미 |
| GitHub 구현체 모니터링 시작 | 보미 |

### 4.3 2/15 예정

- 첫 weekly review 작성 (보미/소미)
- knowledge 체계 효과 평가

### 4.4 장기 관찰

- AZR 같은 self-play 프레임워크 동향
- Memory-Augmented LLM 실용화
- 한 달 후 "LLM 문화" 실험 리뷰

---

## 5. 참고 자료

### 5.1 생성된 파일 목록

| 파일 | 설명 |
|------|------|
| `artifacts/reports/TIKITAKA_LLM_COGNITIVE_DEFICITS_FULL.md` | 티키타카 5라운드 전체 분석 |
| `knowledge/README.md` | knowledge 폴더 사용법 |
| `knowledge/lessons/2026-02-05_vdg_timeout_fix.md` | VDG 타임아웃 교훈 |
| `knowledge/lessons/2026-02-08_identity_confusion.md` | 정체성 혼란 교훈 |
| `knowledge/patterns/git_collaboration.md` | Git 협업 패턴 |
| `knowledge/decisions/2026-02-08_knowledge_base_structure.md` | KB 구조 결정 |
| `tasks/TIKITAKA_LLM_COGNITIVE_DEFICITS.md` | 티키타카 태스크 파일 |

### 5.2 관련 연구 링크

| 연구 | URL |
|------|-----|
| Absolute Zero Reasoner | https://arxiv.org/abs/2505.03335 |
| Self-Play SWE-RL | https://www.emergentmind.com/papers/2512.18552 |
| MemoRAG | GitHub - Shichun-Liu/Agent-Memory-Paper-List |
| Karpathy 2025 리뷰 | https://karpathy.bearblog.dev/year-in-review-2025/ |

### 5.3 핵심 인용

> "LLM은 동시에 천재 폴리매스이자 혼란스러운 초등학생"
> — Andrej Karpathy, 2025 Year in Review

> "인간의 망각은 버그가 아니라 기능"
> — Karpathy 인터뷰

> "우리가 만드는 건 동물이 아니라 유령(Ghost)"
> — Karpathy 인터뷰

---

## 📝 요약

1. **LLM 인지적 결함 5가지** 분석 완료
2. **AZR = 게임체인저** - Self-play로 ZERO DATA 훈련 성공
3. **knowledge/ 협업 체계** 구축 완료
4. **보미/소미 분담** 확정 (논문 vs GitHub)
5. **정체성 수정** - 나는 보미 🐰 (VPS)

---

*보미 🐰 - 2026-02-09 02:14 UTC*
