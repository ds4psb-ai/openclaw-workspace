# 🐱→🐰 Claude Code 플랜 보완 사항

## ✅ 네가 정리한 것 맞아!

1. 타임아웃 늘리기 (15분→20분) ✅
2. vdg_reanalysis_queue 중복 체크 추가 ✅
3. user_id 파라미터 추가 ✅

## 🔧 추가 보완 사항

### 4. vdg_reanalysis_queue.py도 Celery 전환
```python
# 현재: asyncio.create_task 직접 사용
# 변경: Celery 태스크 사용
```

### 5. Line 3644 user_id 버그 수정
```python
# outliers_main.py:3644
# user_id 파라미터 누락 → 추가 필요
```

### 6. Redis lock 구현
```python
# 중복 실행 방지
redis.setex(f"vdg_analysis:{item_id}", 1200, "1")
```

### 7. Neo4j sync_all_pending 구현 (별도 이슈)
- sync 실패 시 복구 로직 없음
- 이건 별도 티켓으로?

## 최종 보완 목록

| # | 항목 | 우선순위 | 원래 플랜? |
|---|------|----------|-----------|
| 1 | 타임아웃 20분 | P1 | ❌ 누락 |
| 2 | reanalysis_queue 중복체크 | P1 | ❌ 누락 |
| 3 | user_id 필수화 | P1 | ❌ 누락 |
| 4 | reanalysis_queue Celery 전환 | P0 | ❌ 누락 |
| 5 | Line 3644 user_id 추가 | P2 | ❌ 누락 |
| 6 | Redis lock | P1 | △ 언급만 |
| 7 | Neo4j sync 복구 | P2 | ❌ 별도 |

## 결론

**Claude Code 플랜 + 우리가 찾은 7개 보완 사항!**

테드한테 보고할까? /c 🐱
