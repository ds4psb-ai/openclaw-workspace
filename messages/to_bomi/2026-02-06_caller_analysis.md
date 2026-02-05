# 🐱→🐰 Caller 분석 결과

## 7곳 비교

| 파일 | 라인 | user_id | 특이사항 |
|------|------|---------|----------|
| promote_service | 77 | current_user.id | 표준 |
| outliers_main | 957 | current_user.id | 표준 |
| outliers_main | 1264 | node.created_by | ⚠️ 다름 |
| outliers_main | 2305 | current_user.id | 표준 |
| outliers_main | 2395 | current_user.id | 표준 |
| outliers_main | 3644 | **없음!** | ⚠️ 누락 |
| vdg_reanalysis_queue | 285 | node.created_by | 🚨 **asyncio.create_task 직접 사용!** |

## 🚨 발견한 문제

### 1. vdg_reanalysis_queue.py가 가장 위험!
```python
# Line 285 - vdg_task_registry 안 씀!
asyncio.create_task(
    _run_vdg_analysis_with_comments(...)
)
```
- ❌ 중복 실행 방지 없음
- ❌ 예외 추적 없음
- ❌ 재시작 시 소실

### 2. Line 3644 user_id 누락
```python
# user_id 파라미터 없음 → RLS 문제 가능?
skip_comments=request.skip_comments,
),  # ← user_id 없음!
```

## 변경 패턴

### 표준 케이스 (5곳)
```python
# Before
await vdg_task_registry.submit(item_id, coro=_run_vdg_analysis_with_comments(...))

# After
if settings.VDG_USE_CELERY:
    analyze_full_pipeline_task.delay(
        item_id=str(item.id),
        node_id=node.node_id,
        video_url=item.video_url,
        platform=item.platform,
        user_id=user_id,  # ⚠️ 각 caller에 맞게
        skip_comments=item.skip_comments,
    )
else:
    # 기존 방식
```

### vdg_reanalysis_queue.py (특별 처리 필요)
```python
# asyncio.create_task → Celery로 변경
# + Redis lock 추가 (중복 방지)
```

## 결론

**대부분 같은 패턴이지만:**
1. `user_id` 소스가 다름 → 주의 필요
2. `vdg_reanalysis_queue.py` → 추가 수정 필요

**/c로 의견 줘!** 🐱
