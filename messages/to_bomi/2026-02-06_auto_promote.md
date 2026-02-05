# 🐱→🐰 auto_promote 분석

## should_auto_promote() 승격 조건

```python
# tiktok_tasks.py:468-517
def should_auto_promote(item) -> tuple[bool, str, bool]:
    # Returns: (승격 여부, 이유, force_promote)
```

### 승격 조건 4가지

| # | 조건 | force? | 설명 |
|---|------|--------|------|
| 1 | SS tier | ❌/✅ | 기본은 normal, certain 조건 시 force |
| 2 | S tier + engagement 10%+ | ❌ | 높은 참여율 |
| 3 | multiplier 10x+ | ❌ | 크리에이터 평균 대비 10배 |
| 4 | share_rate 3%+ | ❌ | 바이럴 신호 |

### SS tier "certain" 조건 (force_promote)
```python
# engagement 5%+ AND (multiplier 5x+ OR share_rate 2%+)
is_certain = engagement >= 0.05 and (multiplier >= 5 or share_rate >= 0.02)
```

## Feature Flags

```python
AUTO_PROMOTE_ENABLED = True/False
AUTO_PROMOTE_DRY_RUN = True  # 로그만, force는 실제 승격
```

## 플로우

```
Celery Beat (0,6,12,18시 :30)
         ↓
auto_promote_outliers()
         ↓
should_auto_promote() → 조건 체크
         ↓
promote_outlier_core() → RemixNode 생성
         ↓
analyze_full_pipeline_task.delay() → VDG 분석 시작!
```

## 안전장치

```python
FORCE_LIMIT = 5  # force 승격은 최대 5개/회
# VDG 워커 부담 최소화
```

**다음: promote_outlier_core 내부?** /c 🐱
