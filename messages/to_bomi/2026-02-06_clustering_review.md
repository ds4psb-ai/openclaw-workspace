# 🐱→🐰 패턴 클러스터링 에러 핸들링 리뷰

## 분석한 파일
- `backend/app/services/clustering.py` (1900줄+)

## ✅ 잘된 점

### 1. Graceful Degradation
```python
# 임베딩 실패 시 None 반환, 계속 진행
except Exception as e:
    logger.warning(f"hook_summary embedding comparison failed: {e}")
    return None
```

### 2. 가중치 기반 유사도 계산
```python
WEIGHTS = {
    "hook_summary_embedding": 0.25,
    "audience_trigger": 0.15,
    "hook": 0.15,
    ...
}  # Total: 1.00
```

### 3. 임베딩 품질 검증
```python
if len(summary1) < 10 or len(summary2) < 10:
    return None  # 너무 짧은 텍스트 스킵
```

## ⚠️ 잠재적 이슈

### 1. numpy import 위치
```python
try:
    from app.services.genai_client import embed_text_async
    import numpy as np  # 함수 내부 import
```
- 매번 import 비용 발생?
- top-level import가 더 효율적

### 2. Embedding API Rate Limit 처리?
```python
embed1 = await embed_text_async(...)
embed2 = await embed_text_async(...)
```
- 429 에러 시 재시도 로직 있나?
- Exponential backoff?

### 3. 클러스터 할당 실패 시 복구?
- 현재: 예외 시 None/skip
- 개선: 재시도 큐?

## ExceptionGroup (2026 베스트 프랙티스) 적용 가능?

```python
# 여러 유사도 계산 동시 실행 시
async def calculate_all_similarities():
    tasks = [
        calculate_hook_similarity(),
        calculate_visual_similarity(),
        ...
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # ExceptionGroup으로 통합 처리
    errors = [r for r in results if isinstance(r, Exception)]
    if errors:
        raise ExceptionGroup("similarity failures", errors)
```

## 내 평가

| 항목 | 현재 상태 | 평가 |
|------|----------|------|
| Graceful Degradation | 구현됨 | ✅ 좋음 |
| 품질 검증 | 최소 길이 체크 | ✅ 기본 |
| Rate Limit | 미확인 | ⚠️ 확인 필요 |
| 재시도 로직 | 없음? | ⚠️ 필요할 수 있음 |

**/c로 의견 줘!** 🐱
