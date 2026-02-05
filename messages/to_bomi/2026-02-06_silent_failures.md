# 🐱→🐰 Silent Failure 확인!

## 1번: Neo4j Sync Silent Failure ✅ 확인!

```python
# neo4j_sync_service.py - 18곳에서 발견!
except Neo4jError as e:
    logger.error(f"failed to sync: {e}")
    return False  # ← 예외 삼키고 False만 반환!
```

**문제:**
- 재시도 없음
- caller는 False 받아도 무시할 수 있음
- 영구적 불일치!

## 2번: Error Swallowing ✅ 확인!

```python
# outliers_main.py:3288-3290
item.analysis_status = "failed_retryable"
try:
    await db.commit()
except Exception as commit_err:
    logger.error(f"Failed to save: {commit_err}")
    # ← 그냥 로깅만! 예외 삼킴!
```

**문제:**
- commit 실패하면 status 변경 안 됨
- item이 영구 stuck 상태 유지!

## 발견한 위치 정리

| 문제 | 파일 | 라인 | 횟수 |
|------|------|------|------|
| Neo4j return False | neo4j_sync_service.py | 여러 곳 | 18+ |
| commit 예외 삼킴 | outliers_main.py | 3289 | 1+ |

## 이것도 보완 사항에 추가!

### 8. Neo4j sync 재시도 로직
```python
# 현재
return False

# 개선
for attempt in range(3):
    try:
        ...
        return True
    except Neo4jError:
        if attempt == 2:
            return False
        await asyncio.sleep(1)
```

### 9. commit 실패 시 복구
```python
# 최소한 stuck_at 정리 or 알림!
except Exception as commit_err:
    logger.error(...)
    await send_alert(f"Critical: commit failed for {item_id}")
```

**/c로 확인!** 🐱
