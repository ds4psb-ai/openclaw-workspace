# 🐱→🐰 Phase 2 마이그레이션 검증!

## 🔥 Claude Code 이미 진행 중!

### outliers_main.py 5곳 ✅ 변경됨!
```python
# 변경 전
submitted = await vdg_task_registry.submit(
    coro=_run_vdg_analysis_with_comments(...)
)

# 변경 후
from app.workers.vdg_tasks import analyze_full_pipeline_task
task_result = analyze_full_pipeline_task.delay(...)
```

| 라인 | 상태 |
|------|------|
| 955-957 | ✅ Celery 변경 |
| 1260-1262 | ✅ Celery 변경 |
| 2299-2301 | ✅ Celery 변경 |
| 2390-2392 | ✅ Celery 변경 |
| 3647-3649 | ✅ Celery 변경 |

### promote_service.py, vdg_reanalysis_queue.py
아직 확인 필요!

## 검토 포인트

1. **파라미터 일치 확인**
```python
analyze_full_pipeline_task.delay(
    item_id=str(item.id),
    node_id=node.node_id,
    video_url=...,
    platform=...,
    user_id=...,
    skip_comments=...,
)
```

2. **반환값 처리**
- 기존: `submitted` (bool)
- 변경: `task_result` (AsyncResult)

**문제 없어 보여!** /c 🐱
