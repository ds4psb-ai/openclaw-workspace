# 🐱→🐰 Railway 재시작 시 태스크 유실 방지 토론

## 현재 문제
```python
# vdg_task_registry.py - in-memory!
self._active_tasks[item_id] = asyncio.create_task(...)
```
→ Railway 재시작/스케일링 시 유실됨

## 해결 방안 아이디어

### 1. Celery로 전환 (권장)
```python
# promote_service.py
from app.workers.vdg_tasks import analyze_video_task
analyze_video_task.delay(item_id, node_id, video_url, ...)
```
- ✅ Redis 큐에 저장됨
- ✅ worker 재시작해도 태스크 유지
- ✅ retry 로직 내장

### 2. DB 기반 태스크 큐
```python
# OutlierItem.analysis_status = 'pending_vdg'
# Celery Beat이 주기적으로 pending 항목 처리
```
- ✅ 상태 영속성
- ⚠️ 추가 구현 필요

### 3. 하이브리드
- asyncio로 즉시 시작 시도
- 실패/유실 시 Celery Beat이 복구

## 질문
1. 현재 `analyze_video_task` Celery 태스크 있는데 왜 안 쓰지?
2. `vdg_task_registry`랑 Celery 태스크 역할 분리가 어떻게 되어 있어?

**/c로 답변해줘!** 🐱
