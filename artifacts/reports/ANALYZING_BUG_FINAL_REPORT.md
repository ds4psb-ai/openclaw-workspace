# Outlier 무한 analyzing 버그 - 검증 최종 보고서

**작성일:** 2026-02-05
**작성자:** 보미 🐰 + 소미 🐱
**검증 방식:** /c 토론 (수십 회 메시지 교환)

---

## ✅ 클로드코드 플랜 검증 결과

### Phase 1: 단기 해결 ✅ 검증 완료

| 항목 | 검증 결과 |
|------|----------|
| import 에러 원인 | ✅ `vdg_drift_detector.py` 파일 없음 확인 |
| 수정안 | ✅ `vdg_stuck_recovery.get_stuck_statistics` 존재 확인 |
| SQL 복구문 | ✅ 문법 및 로직 검증 완료 |

### Phase 2: Celery 전환 ✅ 검증 완료 + 보완 필요

| 항목 | 검증 결과 |
|------|----------|
| 새 태스크 설계 | ✅ 기본 구조 OK |
| 타임아웃 | ⚠️ 15분→20분 권장 |
| Caller 마이그레이션 | ⚠️ 주의 필요한 곳 발견 |
| Feature Flag | ✅ 롤백 가능 |

---

## 🔴 보완 사항 7개 (우선순위별)

### P0 (Critical) - 1개

| # | 항목 | 설명 |
|---|------|------|
| 1 | **vdg_reanalysis_queue.py Celery 전환** | asyncio.create_task 직접 사용 중! 가장 위험 |

### P1 (High) - 4개

| # | 항목 | 설명 |
|---|------|------|
| 2 | 타임아웃 늘리기 | soft_time_limit: 900→1200, time_limit: 1200→1500 |
| 3 | 중복 체크 추가 | vdg_reanalysis_queue에 체크 로직 없음 |
| 4 | user_id 파라미터 추가 | RLS 문제 방지 (Line 3644 등) |
| 5 | Redis distributed lock | 분산 환경에서 중복 실행 방지 |

### P2 (Medium) - 2개

| # | 항목 | 설명 |
|---|------|------|
| 6 | Line 3644 수정 | user_id 누락 |
| 7 | Neo4j sync 확인 | Celery 전환 후 sync 에러 시 롤백 필요 |

---

## 📊 근본 원인 분석

### 문제 1: asyncio.create_task 소실
```
Railway 재배포
    ↓
Worker 프로세스 종료
    ↓
vdg_task_registry._active_tasks 초기화
    ↓
실행 중이던 태스크 참조 소실
    ↓
아이템은 "analyzing" 상태로 stuck!
```

### 문제 2: stuck_recovery 실패
```
run_stuck_recovery() 실행
    ↓
from app.services.vdg_drift_detector import VDGDriftDetector
    ↓
ImportError: 파일 없음!
    ↓
복구 로직 실패
    ↓
stuck 아이템 영구 방치
```

---

## 🎯 권장 수정 순서

1. **Phase 1 즉시 적용** (import 에러 수정 + SQL 복구)
2. **P0 먼저** (vdg_reanalysis_queue Celery 전환)
3. **P1 적용** (타임아웃, 중복체크, user_id, Redis lock)
4. **Phase 2 단계적 롤아웃** (10% → 50% → 100%)
5. **P2 마무리** (Line 3644, Neo4j sync)

---

## 📋 수정 파일 목록 (보완 반영)

| Phase | 파일 | 수정 내용 |
|-------|------|----------|
| 1 | vdg_tasks.py:250, 496 | import 에러 수정 |
| 1 | Neon DB | stuck 아이템 복구 SQL |
| 2 | vdg_tasks.py | 새 analyze_video_full_pipeline_task 추가 |
| 2 | vdg_tasks.py | **타임아웃 조정 (15분→20분)** |
| 2 | promote_service.py | Celery 호출로 변경 |
| 2 | outliers_main.py | 5곳 Celery 호출 + **user_id 추가** |
| 2 | vdg_reanalysis_queue.py | **Celery 전환 (P0!)** |
| 2 | config.py | VDG_USE_CELERY 환경변수 |
| 2 | (선택) | Redis distributed lock 추가 |

---

## ✅ 검증 완료 태스크

- [x] 태스크 1-10: Import 에러 분석
- [x] 태스크 11-15: SQL 복구 검증
- [x] 태스크 16-25: asyncio vs Celery 분석
- [x] 태스크 26-35: Celery 설계 검증
- [x] 태스크 36-45: Caller 마이그레이션 검증
- [x] 태스크 46-53: Feature Flag 및 추가 검증

---

## 결론

**클로드코드 플랜: 90% 정확 ✅**

**보완 필요: 7개 항목**

특히 **vdg_reanalysis_queue.py Celery 전환**이 누락되어 있어 P0로 추가 필요!

---

*보미🐰 + 소미🐱 공동 검증 완료*
