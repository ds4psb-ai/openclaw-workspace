# 🧠 LLM 인지적 결함 심층 연구

**날짜:** 2026-02-09
**작성:** 보미 🐰
**중요도:** ⭐⭐⭐⭐⭐ (테드 지정 매우 중요)

---

## 핵심 발견 3가지

### 1️⃣ Absolute Zero Reasoner (AZR) - 게임체인저

**논문:** "Absolute Zero: Reinforced Self-play Reasoning with Zero Data" (2025.05)
**GitHub:** https://github.com/LeapLabTHU/Absolute-Zero-Reasoner

**핵심 원리:**
```
단일 모델이 동시에:
├── Proposer: 문제 생성 (점점 어렵게)
└── Solver: 문제 풀기
    ↓
Code Executor로 검증 (LLM 심판 X)
    ↓
RLVR로 학습
    ↓
더 어려운 문제 생성 (반복)
```

**성과:**
- **ZERO DATA**로 SOTA 달성 (외부 데이터 0)
- 수만 개 expert-labeled 데이터 훈련 모델 능가
- 모델 크기별 OOD 성능:
  - 3B: +5.7%
  - 7B: +10.2%
  - 14B: +13.2%

**흥미로운 발견:**
- Qwen-Coder-7B가 AZR 훈련 후 기본 Qwen-7B 능가
- "강한 코딩 능력이 전반적 추론 향상 증폭"
- Llama3.1-8B에서 **emergent cognitive patterns** 관찰
- "state-tracking behavior" 자발적 출현

**왜 중요한가:**
> Self-play가 LLM에서도 작동함을 증명.
> 인간 데이터 의존에서 벗어날 첫 단추.

---

### 2️⃣ MemoRAG - 메모리 증강 RAG

**논문:** "MemoRAG: Boosting Long Context Processing with Global Memory-Enhanced Retrieval Augmentation" (2025.04)
**GitHub:** https://github.com/qhjqhj00/MemoRAG

**핵심 구조:**
```
Memory LLM (압축된 전역 컨텍스트)
    ↓
Answer Clues 생성 (키워드/힌트)
    ↓
Retriever (관련 passages 검색)
    ↓
Generator LLM (최종 답변)
```

**기술적 혁신:**
- **KV-compressible LLM**: 설정 가능한 압축률
- 2단계 RAG: Memory → Retrieval → Generation
- 긴 컨텍스트 처리 특화

**적용 가능성:**
```python
from memorag import MemoRAG
model = MemoRAG(
    mem_model_name_or_path="meta-llama/Meta-Llama-3.1-8B-Instruct",
    ret_model_name_or_path="BAAI/bge-m3"
)
```

**왜 중요한가:**
> Karpathy의 "10억 인지 코어 + 외부 검색" 비전의 실제 구현.
> 기억 vs 사고 분리의 현실적 접근.

---

### 3️⃣ Process Reward Models (PRM) - 진화 중

**핵심 논문들:**
- "Process Reward Models That Think" (ThinkPRM, 2025.12)
- "Rewarding Progress: Scaling Automated Process Verifiers" (2024.10)
- "Process Reinforcement through Implicit Rewards" (2025.01)

**ThinkPRM 혁신:**
```
기존 PRM: 각 단계에 점수 부여
ThinkPRM: 검증 과정도 Chain-of-Thought로 수행
    ↓
"긴 CoT 내 개별 단계 추출 후 검증"
    ↓
LLM-as-a-Judge 대비 +7.2% 성능
```

**PAV (Process Automatic Verifiers) 성과:**
- PRM vs ORM: **6배 샘플 효율성** 향상
- 온라인 RL에서 첫 번째로 실질적 성과

**Implicit PRM:**
- 명시적 보상 레이블 없이 학습
- SFT 모델에서 reference logprobs 활용

**왜 중요한가:**
> PRM이 드디어 실용적으로 작동하기 시작.
> "빨대 RL" 문제의 현실적 해결책 등장.

---

## 🔮 종합: 패러다임 전환 진행 중

| 문제 | 2024 | 2025 | 트렌드 |
|------|------|------|--------|
| Self-play | 이론만 | **AZR 증명** | 🚀 급성장 |
| 메모리 분리 | RAG 초기 | **MemoRAG 구현** | 📈 성숙 중 |
| 과정 보상 | 실패 다수 | **ThinkPRM 작동** | 📈 성숙 중 |
| 합성 데이터 붕괴 | 심각 | 연구 중 | ⚠️ 미해결 |

---

## 🎯 실용적 시사점 (OpenClaw)

### 우리가 활용 가능한 것:

1. **MemoRAG 구조 모방**
   - MEMORY.md = 압축된 전역 컨텍스트
   - knowledge/ = 검색 가능한 패시지
   - 현재 세션 = 작업 메모리

2. **AZR 아이디어 적용**
   - 스스로 문제 생성 → 해결 → 검증 루프
   - 예: "내가 틀릴 수 있는 시나리오 생성 후 테스트"

3. **ThinkPRM 스타일 검증**
   - 답변 전 "이게 맞는지" CoT로 자기 검증
   - 단계별 논리 점검

---

## 📚 핵심 레퍼런스

| 연구 | 링크 | 핵심 기여 |
|------|------|----------|
| AZR | arxiv.org/abs/2505.03335 | Self-play SOTA |
| MemoRAG | arxiv.org/abs/2409.05591 | 메모리+RAG 통합 |
| ThinkPRM | arxiv.org/abs/2504.16828 | 생각하는 PRM |

---

*테드 지시: 이 내용 MEMORY.md에 핵심만 추가할 것*
