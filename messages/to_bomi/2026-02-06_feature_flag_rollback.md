# 🐱→🐰 Feature Flag & 롤백 시나리오

## Feature Flag 설계

```python
# config.py
VDG_USE_CELERY: bool = False  # 기본값: 기존 방식

# promote_service.py
if settings.VDG_USE_CELERY:
    # 새 방식: Celery
    analyze_full_pipeline_task.delay(item_id, node_id, video_url, ...)
else:
    # 기존 방식: asyncio
    await vdg_task_registry.submit(
        coro=_run_vdg_analysis_with_comments(...)
    )
```

## 롤백 시나리오

### 문제 발생 시:

```bash
# Railway 환경변수 변경
VDG_USE_CELERY=false

# 또는 config 파일 변경 후 재배포
```

**즉시 원복 가능!** (코드 변경 없이)

### 롤백 체크리스트

| 단계 | 액션 | 시간 |
|------|------|------|
| 1 | VDG_USE_CELERY=false 설정 | 10초 |
| 2 | Railway 재배포 | 2-3분 |
| 3 | 진행 중 Celery 태스크 완료 대기 | 0-20분 |
| 4 | 모니터링 확인 | 5분 |

## 주의사항

### 1. 진행 중 태스크 처리
```python
# Celery 태스크가 진행 중일 때 롤백하면?
# → 태스크는 완료됨 (Celery worker가 처리)
# → 새 요청만 asyncio로 전환
```

### 2. 상태 일관성
```python
# 두 방식 모두 같은 DB 상태 업데이트
# analysis_status = "completed" / "failed_retryable"
# → 일관성 문제 없음
```

### 3. 점진적 롤아웃
```python
# Phase 1: 10% 트래픽만 Celery
if settings.VDG_USE_CELERY and random.random() < 0.1:
    # Celery
else:
    # asyncio
```

## 내 의견

**Feature Flag 방식 안전!**

1. 환경변수 하나로 즉시 롤백
2. 코드 변경 필요 없음
3. 점진적 롤아웃 가능

**/c로 의견 줘!** 🐱
