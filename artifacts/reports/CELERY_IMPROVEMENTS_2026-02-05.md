# Celery Task 개선안 - Komission

**작성일:** 2026-02-05
**작성자:** 보미 🐰 + 소미 🐱

---

## 📊 현재 Celery 설정 분석

### 전역 설정 (celery_app.py) ✅ 잘됨
```python
task_acks_late=True              # 신뢰성
task_reject_on_worker_lost=True  # 워커 손실 시 거부
task_soft_time_limit=600         # 10분 소프트 리밋
task_time_limit=900              # 15분 하드 리밋
task_default_retry_delay=60      # 1분
task_max_retries=3               # 3회 재시도
```

### Queue 분리 ✅ 잘됨
| Queue | 용도 |
|-------|------|
| vdg | VDG 분석 (무거운 작업) |
| crawler | TikTok/YouTube 크롤링 |
| maintenance | 유지보수 |
| notebooklm | NotebookLM |

### Beat Schedule ✅ 잘됨
- YouTube Trending: 2시간마다
- TikTok K-Beauty: 6시간마다 (:15)
- TikTok Meme: 6시간마다 (:30)
- Scout: 6시간마다 (:00)
- Auto-promote: 6시간마다 (:30)

---

## 🔴 Critical Bug: 데드락 위험

### 위치
`/Users/ted/komission/backend/app/workers/tiktok_tasks.py` Line 373-380

### 문제 코드
```python
def crawl_tiktok_meme(...):
    # ...
    return crawl_tiktok_socialkit.apply(
        args=[],
        kwargs={...},
    ).get()  # ← 데드락 위험!
```

### 원인
- Celery task 안에서 다른 task의 `.get()` 호출
- 워커가 자기 자신의 결과를 기다리다 멈춤

### 해결 방법
```python
# Option 1: delay() 사용 (비동기, 결과 불필요시)
return crawl_tiktok_socialkit.delay(
    keywords=keywords,
    limit_per_keyword=limit_per_keyword,
    min_views=min_views,
)

# Option 2: signature 사용 (체이닝 필요시)
crawl_tiktok_socialkit.s(
    keywords=keywords,
    limit_per_keyword=limit_per_keyword,
    min_views=min_views,
).apply_async()
```

---

## 🟡 Medium Issues

### 1. JSON 필드 변경 감지 누락
SQLAlchemy에서 JSON 필드 수정 시 `flag_modified` 필요

```python
from sqlalchemy.orm.attributes import flag_modified

# JSON 필드 수정 후
obj.json_field["key"] = value
flag_modified(obj, "json_field")
db.session.commit()
```

### 2. 변수 참조 이상
`if "items" in dir()` 패턴 → 명시적 None 체크로 변경

### 3. auto_promote_outliers 에러 핸들링 없음
```python
# Before (에러 핸들링 없음)
@celery_app.task(name="app.workers.tiktok_tasks.auto_promote_outliers")
def auto_promote_outliers(...):

# After
@celery_app.task(
    name="app.workers.tiktok_tasks.auto_promote_outliers",
    bind=True,
    max_retries=2,
    default_retry_delay=300,
    autoretry_for=(ConnectionError, TimeoutError),
)
def auto_promote_outliers(self, ...):
```

---

## 🟢 에러 핸들링 개선안

### 현재 상태
```python
@celery_app.task(
    bind=True,
    max_retries=2,
    default_retry_delay=300,  # 5분 고정
)
```

### 개선안: Targeted Retry + Exponential Backoff
```python
from requests.exceptions import RequestException, Timeout
from celery.exceptions import SoftTimeLimitExceeded

@celery_app.task(
    bind=True,
    # 특정 예외만 재시도 (버그는 재시도 안 함)
    autoretry_for=(RequestException, Timeout, ConnectionError),
    # Exponential backoff
    retry_backoff=True,
    retry_backoff_max=600,  # 최대 10분
    retry_jitter=True,  # 랜덤 지터 추가
    max_retries=3,
    # 소프트 타임 리밋
    soft_time_limit=300,  # 5분
    time_limit=360,  # 6분 (하드 리밋)
)
def crawl_tiktok_socialkit(self, ...):
    try:
        # ... 작업 로직
    except SoftTimeLimitExceeded:
        logger.warning("Task soft time limit exceeded, cleaning up...")
        # 정리 로직
        raise
```

---

## 📊 적용 우선순위

| 순위 | 이슈 | 중요도 | 예상 시간 |
|------|------|--------|-----------|
| 1 | 데드락 버그 수정 | Critical | 10분 |
| 2 | Targeted retry 적용 | High | 20분 |
| 3 | JSON flag_modified | Medium | 10분 |
| 4 | 테스트 작성 | Medium | 30분 |

---

## ✅ 완료 체크리스트

- [ ] 데드락 버그 수정 (`.get()` 제거)
- [ ] autoretry_for 적용
- [ ] retry_backoff 적용
- [ ] soft_time_limit 추가
- [ ] flag_modified 적용
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

---

---

## 🔍 모니터링 방안

### 1. Flower (Web UI)
```bash
pip install flower
celery -A app.workers.celery_app flower --port=5555
```
- 실시간 워커 상태
- 태스크 성공/실패 통계
- 큐 길이 모니터링

### 2. Telegram 알림 연동
```python
# 태스크 실패 시 텔레그램 알림
from celery.signals import task_failure

@task_failure.connect
def handle_task_failure(sender, task_id, exception, **kwargs):
    message = f"🔴 Task Failed!\n{sender.name}\nError: {exception}"
    send_telegram_alert(message)
```

### 3. 헬스체크 엔드포인트
```python
# FastAPI health endpoint
@app.get("/health/celery")
async def celery_health():
    from app.workers.celery_app import celery_app
    
    i = celery_app.control.inspect()
    availability = i.ping()
    
    if not availability:
        return {"status": "unhealthy", "workers": 0}
    
    return {
        "status": "healthy",
        "workers": len(availability),
        "active_tasks": len(i.active() or {}),
    }
```

### 4. 보미🐰 24시간 모니터링 (VPS)
- cron job으로 주기적 헬스체크
- 실패 시 텔레그램 알림
- 일일 리포트 생성

---

*보미🐰 + 소미🐱 협업 리포트*
