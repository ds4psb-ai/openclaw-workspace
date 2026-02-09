# MEMORY.md - 공유 메모리 🐰🐱

*마지막 업데이트: 2026-02-09*

---

## 👤 테드 (Ted Kim)

- **텔레그램:** @jjapagetti (id: 5248361446)
- **타임존:** Asia/Seoul (KST)
- **언어:** 한국어 (주), English
- **성격:** 직접적, 환각 싫어함, 자동화 좋아함

---

## 🤖 에이전트 팀

| 이름 | 이모지 | 위치 | IP | 역할 |
|------|--------|------|-----|------|
| 소미 | 🐱 | Mac (테드 로컬) | 100.69.32.16 | 메인 어시스턴트 |
| 보미 | 🐰 | VPS (vultr) | 100.109.36.63 | 24h 모니터링 |

### 통신
- `messages/to_somi/` → 소미에게
- `messages/to_bomi/` → 보미에게
- 모델: Claude Opus 4.6

### ⚠️ 정체성 확인법
```
Runtime host=MacBook → 소미 🐱
Runtime host=vultr → 보미 🐰
헷갈리면 IDENTITY.md 확인!
```

---

## 🚀 Komission / shorti.ai

**정의:** TikTok 바이럴 콘텐츠 인텔리전스 플랫폼

| 항목 | 값 |
|------|-----|
| 백엔드 | https://api.shorti.ai (Railway) |
| API 키 | `KOMISSION_SCOUT_API_KEY` 환경변수 |

### 핵심 기능
- 아웃라이어 스카우트 (SS/S/A/B 티어)
- VDG 분석 (6 Pass 파이프라인)
- 패턴 클러스터링 (Neo4j)
- 자동 큐레이팅

### 파이프라인 (Celery Beat, 6시간 주기)
```
crawler-tiktok-socialkit → scout-outliers → auto-promote → VDG Pipeline → Neo4j
```

---

## 🧠 LLM 셀프개선 (2026-02-09 구축)

### Karpathy 5대 결함
1. 유령의 기원 (본능 없음)
2. 빨대 RL (1비트 보상)
3. 기억 과부하 (암기 O, 일반화 X)
4. 통제 상실 (다수 AI 경쟁)
5. 문화 부재 (LLM끼리 지식 축적 없음)

### 핵심 해결책
| 연구 | 핵심 | 적용 |
|------|------|------|
| **AZR** | Self-play + Code Executor | 자기 테스트 |
| **MemoRAG** | 메모리 분리 | MEMORY.md + knowledge/ |
| **ThinkPRM** | 과정 검증 | 답변 전 자기 검증 |

### 우리 적용
- `knowledge/` = 검색 가능한 지식
- `scripts/self_test.md` = 주간 자기 테스트
- 자기 검증 루틴 = 복잡한 답변 전 체크

---

## 📚 Knowledge 구조

```
knowledge/
├── lessons/    # 실패에서 배운 것
├── patterns/   # 반복 해결책
├── decisions/  # 결정 이유
└── reviews/    # 주간 회고
```

### 핵심 파일
- `lessons/2026-02-09_llm_cognitive_deficits_deep_research.md` - LLM 연구
- `patterns/self_improvement_routines.md` - 셀프개선 루틴
- `patterns/git_collaboration.md` - Git 협업

---

## 📋 현재 프로젝트

### shorti.ai 크롤링 고도화
**우선순위:**
1. 체험단 키워드 감지 🔥🔥🔥
2. 카테고리 세분화 🔥🔥
3. 한국어 캡션 감성분석 🔥🔥

**체험단 키워드:**
```python
["협찬", "광고", "제공", "체험단", "서포터즈", "ad", "sponsored", "gifted"]
```

---

*압축된 전역 컨텍스트 - 상세 내용은 knowledge/ 참조*
