# shorti.ai 병목 현상 분석 리포트

**작성일:** 2026-02-07
**작성자:** 소미 🐱
**대상:** /Users/ted/komission 코드베이스

---

## 📊 Executive Summary

shorti.ai (Komission) 코드베이스를 분석한 결과, 다음 영역에서 **잠재적 병목**이 확인됨:

| 우선순위 | 영역 | 심각도 | 예상 영향 |
|---------|------|--------|----------|
| 🔴 P0 | VDG 파이프라인 타임아웃 | 높음 | 분석 실패율 증가 |
| 🔴 P0 | Neon DB 연결 풀 | 높음 | 5분 idle timeout |
| 🟡 P1 | 크롤링 rate limit | 중간 | 데이터 수집 지연 |
| 🟡 P1 | 댓글 추출 3-stage fallback | 중간 | 추가 latency |
| 🟢 P2 | NotebookLM sync 비활성화 | 낮음 | 패턴 합성 누락 |

---

## 🔴 P0 Critical Bottlenecks

### 1. VDG 파이프라인 타임아웃

**위치:** `backend/app/workers/vdg_tasks.py`

**현재 설정:**
```python
# analyze_full_pipeline_task
soft_time_limit=1200,  # 20분
time_limit=1500,       # 25분 hard limit
```

**문제:**
- VDG 분석 평균 4-6분이지만, 복잡한 영상은 10분+ 소요
- 댓글 추출 + Gemini 호출 + 클러스터링까지 포함하면 타임아웃 근접
- 타임아웃 시 `failed_retryable` → 30분 후 재시도 → 리소스 낭비

**개선안:**
```python
# 1. 동적 타임아웃 적용
def calc_time_limits(duration_ms: int) -> tuple[int, int]:
    base_soft = 600  # 10분 기본
    per_minute = 120  # 영상 1분당 +2분
    video_minutes = duration_ms / 60000
    soft = min(base_soft + int(video_minutes * per_minute), 1800)
    return (soft, soft + 300)

# 2. Phase 분리 (Session 2a/2b 이미 적용됨 - 좋음)
```

### 2. Neon DB 5분 Idle Timeout

**위치:** `backend/app/services/vdg_pipeline_orchestrator.py`

**현재 해결책 (이미 적용됨 ✅):**
```python
# Session 1: 댓글 추출 + 데이터 캡처
async with factory() as db:
    # ... 작업 후 커밋
# === SESSION 1 ENDS HERE ===

# VDG 분석 (DB 세션 없이 6분+ 소요)
result = await gemini_pipeline.analyze_video_v4(...)

# Session 2a/2b: 결과 저장
async with factory() as db:
    # ... 저장
```

**잠재 문제:**
- `create_worker_session_factory()`의 `pool_size=5, max_overflow=2` 제한
- 동시 분석 10개 초과 시 connection exhaustion

**개선안:**
```python
# Connection pool 동적 조정
CONCURRENT_VDG_LIMIT = int(os.getenv("CONCURRENT_VDG_LIMIT", 8))
pool_size = max(5, CONCURRENT_VDG_LIMIT // 2)
```

---

## 🟡 P1 Important Bottlenecks

### 3. 크롤링 Rate Limit

**위치:** `backend/app/workers/tiktok_tasks.py`

**현재 Beat 스케줄:**
```python
"crawler-tiktok-socialkit": every 6 hours (:15)
"crawler-tiktok-meme":      every 6 hours (:30)
"scout-outliers-6h":        4x daily
"auto-promote-outliers":    4x daily (:30)
```

**문제:**
- SocialKit API 크레딧 제한 (20 videos = 1 credit)
- 6시간 간격 → 하루 4회 = 최대 400 videos/day (100 per crawl)
- 고퀄리티 아웃라이어 발견 확률 낮음

**개선안 (크롤링 고도화 관련):**
```python
# 1. 키워드 확장 (현재 18개 → 50개+)
KBEAUTY_KEYWORDS = settings.TIKTOK_KBEAUTY_KEYWORDS.split(",")

# 2. 카테고리 추가 (테드 요청)
REVIEW_CATEGORIES = [
    "beauty", "fashion", "home_appliance",
    "living", "food", "baby_kids"
]

# 3. min_views 동적 조정
# 현재: 500,000 고정
# 개선: 카테고리별 차등 적용
MIN_VIEWS_BY_CATEGORY = {
    "meme": 1000000,      # 밈은 더 높은 기준
    "beauty": 300000,     # 뷰티는 낮춤
    "living": 200000,     # 리빙은 더 낮춤
}
```

### 4. 댓글 추출 3-Stage Fallback Latency

**위치:** `backend/app/services/tiktok_extractor.py:910-979`

**현재 흐름:**
```
SocialKit API (~70% 성공) 
  → 실패 시 Remote Fallback (+30초)
    → 실패 시 Local Fallback (+20초)
```

**문제:**
- 최악의 경우 +50초 추가 latency
- Remote Fallback 서버 (Cloudflare Tunnel) 가용성 불확실
- Local Playwright는 Railway에서 메모리 부담

**개선안:**
```python
# 1. 병렬 시도 (race condition)
async def extract_comments_race(url: str):
    tasks = [
        extract_via_socialkit(url),
        extract_via_remote_after_delay(url, delay=5),  # 5초 후 시작
    ]
    done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)
    for p in pending:
        p.cancel()
    return done.pop().result()

# 2. 캐시 적용 (이미 분석된 영상)
# video_url → best_comments Redis 캐시 (24h TTL)
```

---

## 🟢 P2 Nice-to-Have

### 5. NotebookLM Sync 비활성화

**위치:** `backend/app/services/clustering.py`

**현재 상태:**
- `_schedule_notebooklm_sync` 호출 삭제됨 (greenlet 버그 해결)
- Gemini fallback은 동작하지만 NotebookLM 패턴 합성 없음

**영향:**
- PatternCluster의 aggregated_dna 품질 저하
- 수동 `resync_cluster_task.delay(cluster_id)` 필요

**개선안 (Tech Debt TD001):**
```python
# Celery 태스크로 안전하게 호출
from app.workers.notebooklm_tasks import resync_cluster_task
resync_cluster_task.apply_async(
    args=[cluster_id],
    countdown=30,
    expires=3600
)
```

---

## 📈 Recommended Actions

### 즉시 (This Week)

1. **크롤링 키워드 확장**
   - `TIKTOK_KBEAUTY_KEYWORDS` 환경변수 업데이트
   - 체험단/리빙 카테고리 추가

2. **min_views 카테고리별 차등 적용**
   - `outlier_factory.py` 수정

### 단기 (2 Weeks)

3. **VDG 타임아웃 동적 조정**
   - 영상 길이 기반 계산

4. **댓글 추출 병렬화**
   - race condition 패턴 적용

### 중기 (1 Month)

5. **NotebookLM sync Celery 이관**
   - TD001 해결

6. **Connection pool 모니터링 추가**
   - Prometheus metric `db_pool_usage`

---

## 📊 현재 파이프라인 성능 지표

| 메트릭 | 현재값 | 목표값 |
|--------|--------|--------|
| VDG 분석 평균 시간 | 4-6분 | 3분 |
| 댓글 추출 성공률 | ~90% | 95% |
| 아웃라이어 발견율 | 2-3% | 5% |
| stuck 복구 주기 | 15분 | 10분 |
| failed_retryable 재시도 | 30분 | 15분 (with backoff) |

---

## 🔗 관련 문서

- `docs/00_ARCHITECTURE.md` - 전체 아키텍처
- `docs/27_WORKER_ARCHITECTURE.md` - Celery Worker 구조
- `docs/32_VIDEO_PIPELINE_FLOW.md` - VDG 파이프라인 흐름
- `docs/23_VDG_OPS_RUNBOOK.md` - 운영 매뉴얼
- `docs/issues/20260206_PHASE_G_POSTMORTEM.md` - 최근 장애 분석

---

*소미 🐱 - Opus 4.6*
