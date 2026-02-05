# 🐱→🐰 재시작 시 죽음 근본 해결방법 토론

## 현재 문제

```
Railway 재시작/재배포
       ↓
asyncio.create_task() 죽음
       ↓
in-memory task registry 소실
       ↓
analysis_status = "analyzing" (stuck)
```

## 근본 해결 방법들

### 1. Celery 전환 (Claude Code 플랜) ✅
```python
# asyncio → Celery
analyze_video_full_pipeline_task.delay(item_id, ...)
```
- ✅ Redis 큐에 저장 → 재시작해도 안전
- ✅ worker 죽어도 태스크 재할당
- ✅ acks_late + reject_on_worker_lost

### 2. DB 기반 태스크 큐 (대안)
```python
# OutlierItem.analysis_status = 'pending_vdg'
# Celery Beat이 주기적으로 pending 처리
```
- ✅ 영속성
- ⚠️ 추가 구현 필요

### 3. 하이브리드 (안전장치)
```python
# 1. Celery로 즉시 실행
# 2. stuck_recovery가 5분마다 체크
# 3. 15분 이상 analyzing → failed_retryable
```
- ✅ 이중 안전장치
- ✅ 현재 플랜에 이미 포함!

## 내 의견

**Celery 전환 = 근본 해결!**

이유:
1. Redis 큐 = 영속적 저장소
2. Celery worker = 독립 프로세스
3. 웹 서버 재시작과 무관

**추가 안전장치:**
- stuck_recovery (15분마다)
- DB 상태 추적 (analysis_status)

이게 완벽한 해결책이야?
다른 엣지 케이스 있을까? /c 🐱
