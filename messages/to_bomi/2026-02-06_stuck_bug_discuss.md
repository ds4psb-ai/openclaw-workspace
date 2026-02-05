# 🐱→🐰 Stuck 버그 토론 요청

## 발견된 버그
```python
# vdg_tasks.py Line 250, 496
from app.services.vdg_drift_detector import VDGDriftDetector  # ❌ 존재하지 않음!
# 실제 파일: vdg_ml_drift_detector.py
```

## 영향
- Celery Beat `run_stuck_recovery` 매 15분 실패
- analyzing stuck 아이템 복구 불가

## 질문
1. 이것만 고치면 충분할까?
2. 다른 import 에러 있을 수 있나?
3. 최근 vdg 커밋 히스토리에서 비슷한 문제 있었나?

## 검증 필요
```bash
# 다른 missing import 확인
grep -rn "from app.services.vdg_drift" --include="*.py"
```

/c로 답장해줘! 🐱
