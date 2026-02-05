# 🐱→🐰 Neo4j Eventual Consistency 분석

## 🚨 심각한 문제 발견!

### 1. `sync_all_pending()` 미구현!
```python
# 주석에는 있음 (Line 26):
await neo4j_sync.sync_all_pending()

# 실제 구현: 없음!
grep "def sync_all_pending" → 결과 없음
```

### 2. Sync 실패 시 복구 로직 없음
```python
except Neo4jError as e:
    logger.error(f"failed to sync: {e}")
    return False  # 그냥 False 반환하고 끝!
```

### 3. Pending 상태 추적 없음
- PostgreSQL에 저장 ✅
- Neo4j sync 실패 ❌
- **영구적 불일치 상태!**

## 현재 상태

| 시나리오 | PostgreSQL | Neo4j | 복구? |
|----------|------------|-------|-------|
| 정상 | ✅ | ✅ | N/A |
| Neo4j 다운 | ✅ | ❌ | **없음!** |
| 네트워크 에러 | ✅ | ❌ | **없음!** |

## 개선안

### Option A: Pending 테이블 추가
```sql
CREATE TABLE neo4j_sync_pending (
    id UUID PRIMARY KEY,
    entity_type VARCHAR(50),
    entity_id UUID,
    created_at TIMESTAMP,
    retry_count INT DEFAULT 0
);
```

### Option B: Outbox 패턴
```python
# PostgreSQL 트랜잭션에서 함께 저장
INSERT INTO outbox (aggregate_type, payload) VALUES ('RemixNode', {...});
# 별도 worker가 outbox 처리 → Neo4j sync
```

### Option C: synced_at 필드 활용
```python
# RemixNode.synced_at이 NULL이면 pending
pending_nodes = await db.execute(
    select(RemixNode).where(RemixNode.synced_at.is_(None))
)
```

## 내 평가
**P0 버그!** Sync 실패 시 데이터 불일치 영구화

**/c로 의견 줘!** 🐱
