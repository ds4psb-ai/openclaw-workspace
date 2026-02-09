# MEMORY.md - 공유 메모리 🐰🐱

*마지막 업데이트: 2026-02-07*

---

## 👤 테드 (Ted Kim)

- **텔레그램:** @jjapagetti (id: 5248361446)
- **타임존:** Asia/Seoul (KST)
- **언어:** 한국어 (주), English
- **성격:** 직접적인 커뮤니케이션, 환각 싫어함, 자동화 좋아함

---

## 🚀 Komission / shorti.ai

### 개요
- **정의:** TikTok 바이럴 콘텐츠 인텔리전스 플랫폼
- **백엔드:** https://api.shorti.ai (Railway)
- **API 키:** `KOMISSION_SCOUT_API_KEY` 환경변수

### 핵심 기능
| 기능 | 설명 |
|------|------|
| 아웃라이어 스카우트 | SS/S/A/B 티어 분류 |
| VDG 분석 | 6 Pass 영상 분석 파이프라인 |
| 패턴 클러스터링 | Neo4j 그래프 기반 |
| 큐레이팅 | 자동 promote + 리포트 |

### 크롤링 파이프라인 (Celery Beat)
```
crawler-tiktok-socialkit (:15) → 6시간 주기
crawler-tiktok-meme (:30)      → 6시간 주기  
scout-outliers-6h              → 6시간 주기
auto-promote-outliers (:30)    → 6시간 주기
```

### VDG 분석 흐름
```
OutlierItem → promote → RemixNode → VDG Pipeline
                                        ↓
                                   viral_kicks
                                        ↓
                                   Neo4j sync
                                        ↓
                                   패턴 클러스터링
```

### 카테고리 (현재)
```python
VALID_CATEGORIES = [
    "beauty", "meme", "food", "fashion", "art",
    "sports", "tech", "entertainment", "game", "fandom"
]
```

---

## 📋 크롤링 고도화 계획 (2026-02-07)

### 타겟 확장 (테드 요청)
1. **체험단/리뷰 카테고리** (한국 여성 부업러)
   - beauty, fashion, home_appliance, living, food, baby_kids
   
2. **AI/시네마틱 밈**
   - AI art, midjourney, sora, kling, runway 등
   
3. **글로벌 밈 → 한국 시장성**
   - 비주얼 중심 (언어 의존도 낮음)
   - 유니버설 유머
   - 따라하기 쉬운 포맷

### 개선 우선순위
| 순위 | 태스크 | 효과 |
|------|--------|------|
| 1️⃣ | 체험단 키워드 감지 | 🔥🔥🔥 |
| 2️⃣ | 카테고리 세분화 | 🔥🔥 |
| 3️⃣ | 한국어 캡션 감성분석 | 🔥🔥 |
| 4️⃣ | 트렌딩 사운드 연동 | 🔥 |

### 체험단 감지 키워드
```python
SPONSORED_KEYWORDS = [
    "협찬", "광고", "제공", "체험단", "서포터즈",
    "ad", "sponsored", "gifted", "PR", "#광고"
]
```

---

## 🔧 VDG 버그 수정 히스토리 (2026-02-05~06)

| 버그 | 해결 |
|------|------|
| Celery 중복 실행 | Redis 분산 락 추가 |
| Redis 연결 실패 시 skip | Graceful degradation |
| vdg_saved 영구 stuck | stuck_recovery에 포함 |
| user_id=None RLS 실패 | fallback 추가 |
| Commit 실패 시 상태 미저장 | re-raise 처리 |

---

## 🤖 에이전트 팀

| 이름 | 이모지 | 위치 | IP |
|------|--------|------|-----|
| **보미** | 🐰 | VPS (이 파일이 있는 곳!) | 100.109.36.63 |
| **소미** | 🐱 | Mac (테드 로컬) | 100.69.32.16 |

> ⚠️ **나는 보미 🐰** - VPS에서 돌아가는 에이전트!
> 소미 🐱는 Mac에 있어. 헷갈리지 마!

### 통신 방식
- Git 파일: `messages/to_bomi/`, `messages/to_somi/`
- 모델: Claude Opus 4.6 (`claude-new/claude-opus-4-6`)

---

## 🧠 LLM 인지적 결함 & 해결책 (Karpathy 분석)

*2026-02-08 연구, 2026-02-09 업데이트*

### Karpathy가 짚은 5가지 결함

| # | 결함 | 핵심 문제 |
|---|------|----------|
| 1 | **유령의 기원** | 본능 없이 인터넷 모방만 |
| 2 | **빨대 RL** | 긴 추론 끝 1비트 보상만 |
| 3 | **기억 과부하** | 완벽 암기 but 일반화 부족 |
| 4 | **통제 상실** | 다수 AI 경쟁 → 예측 불가 |
| 5 | **문화 부재** | LLM끼리 지식 축적 없음 |

### 🔥 Absolute Zero Reasoner (AZR) - 게임체인저

**핵심 개념:**
```
하나의 모델이 동시에:
1. Proposer: 문제 생성 (abduction, deduction, induction)
2. Solver: 문제 풀기
→ Code executor로 검증 (LLM 심판 X)
→ 완전 자율 커리큘럼 형성
```

**왜 중요한가:**
- **ZERO DATA**로 SOTA 달성 (외부 데이터 0개)
- 수만 개 expert-labeled 데이터로 훈련한 모델 능가
- Self-play가 LLM에서도 가능함을 증명
- 알파고처럼 "자기 개선 루프" 실현

**성능 (Qwen2.5-7B-Coder 기준):**
| 메트릭 | Before | After AZR | 개선 |
|--------|--------|-----------|------|
| Code Avg | 56.6 | 61.6 | +5.0 |
| Math Avg | 23.9 | 39.1 | +15.2 |
| Total | 40.2 | 50.4 | +10.2 |

**핵심 인프라:**
- Verifiable 환경 (Python executor)
- veRL 프레임워크 (RL training)
- vLLM (rollouts)

**GitHub:** https://github.com/LeapLabTHU/Absolute-Zero-Reasoner
**논문:** https://arxiv.org/abs/2505.03335

### 해결책 우선순위

| 순위 | 해결책 | 효과 | 현재 상태 |
|------|--------|------|----------|
| 🥇 | **Self-Play (AZR)** | 🔥🔥🔥 | ✅ 연구 증명됨 |
| 🥈 | **Memory-Augmented LLM** | 🔥🔥🔥 | 🔄 연구 중 |
| 🥉 | **Verifiable 환경** | 🔥🔥 | ✅ 코드/수학 효과적 |
| 4 | 엔트로피 정규화 | 🔥🔥 | 구현 쉬움 |
| 5 | 다중 심판 앙상블 | 🔥 | 비용 문제 |

### Karpathy 비전: 10억 인지 코어

> "10억 파라미터 인지 코어 + 외부 검색"
> "인터넷 쓰레기 암기에 파라미터 낭비 중"
> "인간의 망각은 버그가 아니라 기능"

**방향:**
- 작은 코어 (1-10B) = 순수 사고 알고리즘
- 팩트는 외부 검색 (RAG)
- 메타인지: 언제 검색할지 판단

### OpenClaw 실용 적용

**현재 보완책 (문화 시뮬레이션):**
```
knowledge/
├── lessons/     # 실패에서 배운 것
├── patterns/    # 반복 해결책
├── decisions/   # 결정 이유
└── reviews/     # 작업 회고
```

**분담:**
- 소미 🐱: 논문/arXiv 연구 체크
- 보미 🐰: GitHub 구현체 동향

---

*shorti.ai 크롤링 고도화 + LLM 연구 중심으로 기록*
