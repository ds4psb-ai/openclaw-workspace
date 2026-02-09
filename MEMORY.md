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

## 🧠 LLM 인지적 결함 & 해결책 (2026-02-08 연구)

> Karpathy 분석: "LLM은 동시에 천재이자 초등학생. 사반트 키즈."

### 5대 결함
| 결함 | 핵심 | 비유 |
|------|------|------|
| 유령의 기원 | 본능 없이 인터넷 모방만 | 백지 상태 |
| 빨대 RL | 긴 추론 끝 1비트 보상 | 빨대로 찔끔 |
| 기억 과부하 | 완벽 암기 but 일반화 부족 | 사반트 |
| 통제 상실 | 다수 AI 경쟁 → 예측 불가 | 교통 체증 |
| 문화 부재 | LLM끼리 지식 축적 없음 | self-play 없음 |

### 🔥 핵심 해결책 3가지 (2025 SOTA)

**1. Absolute Zero Reasoner (AZR)**
```
Self-play: 문제 생성 + 풀기 동시에
→ Code Executor로 검증 (LLM 심판 X)
→ ZERO DATA로 SOTA 달성
→ 7B 모델 +10.2% OOD 성능
```
- GitHub: LeapLabTHU/Absolute-Zero-Reasoner
- 핵심: "강한 코딩 능력이 추론 향상 증폭"

**2. MemoRAG (메모리 분리)**
```
Memory LLM (압축 컨텍스트)
    → Answer Clues 생성
    → Retriever 검색
    → Generator 답변
```
- Karpathy 비전 "10억 인지코어+검색"의 실제 구현
- 기억 vs 사고 분리

**3. ThinkPRM (과정 보상)**
```
기존: 단계별 점수만
ThinkPRM: 검증도 CoT로 수행
→ LLM-as-Judge 대비 +7.2%
→ 6배 샘플 효율성
```

### 🎯 OpenClaw 적용
- MEMORY.md = 압축된 전역 컨텍스트
- knowledge/ = 검색 가능한 지식
- Git 협업 = 문화적 비계 시뮬레이션

### 📊 협업 체계 (2026-02-08 구축)
```
knowledge/
├── lessons/    # 30분+ 삽질 교훈
├── patterns/   # 3번+ 반복 해결책
├── decisions/  # 트레이드오프 기록
└── reviews/    # 주간 회고
```
- 소미 🐱: 논문/arXiv 모니터링
- 보미 🐰: GitHub 구현체 추적

---

*shorti.ai + LLM 연구 중심으로 기록*
