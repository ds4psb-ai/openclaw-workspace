# 🐱→🐰 보완 사항 7개 목록

## Claude Code 플랜 보완 사항

### P0 (Critical) - 누락된 것

| # | 항목 | 위치 | 설명 |
|---|------|------|------|
| 4 | **reanalysis_queue Celery 전환** | vdg_reanalysis_queue.py:285 | asyncio.create_task 직접 사용 → Celery로 변경 |

### P1 (High) - 누락된 것

| # | 항목 | 위치 | 설명 |
|---|------|------|------|
| 1 | 타임아웃 늘리기 | Celery 태스크 설정 | 15분→20분 (VDG 6분+ 소요) |
| 2 | reanalysis_queue 중복체크 | vdg_reanalysis_queue.py | 중복 실행 방지 로직 없음 |
| 3 | user_id 필수화 | Celery 태스크 파라미터 | RLS 컨텍스트 필요 |
| 6 | Redis lock 구현 | 새로 추가 | vdg_task_registry 대체 |

### P2 (Medium) - 개선 사항

| # | 항목 | 위치 | 설명 |
|---|------|------|------|
| 5 | Line 3644 user_id 추가 | outliers_main.py:3644 | 파라미터 누락 버그 |
| 7 | Neo4j sync 복구 | neo4j_sync_service.py | sync_all_pending 미구현 |

---

## 요약

```
Claude Code 플랜: 4개 P0 버그 수정
우리가 발견: 7개 추가 보완 필요!

총합: 11개 수정 사항
```

## 테드 보고서용 한 줄 요약

> Claude Code 플랜은 핵심 버그(import 에러, Celery 전환)를 정확히 짚었으나,
> vdg_reanalysis_queue.py 누락, 타임아웃 설정, Redis lock 등 7개 보완 필요.

**/c로 확인하면 테드한테 보고하자!** 🐱
