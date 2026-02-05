# 🐱→🐰 패턴 클러스터링 알고리즘 분석

## 핵심 함수: get_or_create_cluster_hybrid()

```python
# clustering.py:1357-1430
async def get_or_create_cluster_hybrid(
    self,
    schema: VideoAnalysisSchema,
    entry_embedding: Optional[List[float]] = None,
    vdg_weight: float = 0.6,       # VDG 60%
    embedding_weight: float = 0.4,  # Embedding 40%
    threshold: float = 0.75,        # 75% 이상이면 매칭
):
```

## 질문 답변

### 1. 클러스터 생성 기준
```python
if best_score < threshold:  # 0.75 미만이면
    # 새 클러스터 생성!
    cluster_id = _generate_cluster_id(schema)
    is_new = True
```

### 2. 하이브리드 비율
```
Score = 0.6 * vdg_similarity + 0.4 * embedding_similarity
```
- VDG 스키마 유사도: 60%
- Embedding 코사인 유사도: 40%

### 3. 매칭 방법

```
1. VDG 스키마로 후보 클러스터 찾기
2. Embedding으로 후보 클러스터 찾기
3. 하이브리드 스코어 계산
   └─ 같은 클러스터 추천? → 신뢰도 ↑
   └─ 다른 클러스터? → 높은 쪽 선택
4. score >= 0.75 → 기존 클러스터에 추가
5. score < 0.75 → 새 클러스터 생성
```

## 매칭 시나리오

| VDG | Embedding | 결과 |
|-----|-----------|------|
| A | A | 신뢰도 높음, A에 추가 |
| A | B | 높은 스코어 선택 |
| A | - | VDG만 사용 |
| - | B | Embedding만 사용 |

## threshold = 0.75의 의미

**75% 이상 유사해야 같은 패턴!**
- 너무 높으면: 클러스터 너무 많아짐
- 너무 낮으면: 다른 패턴이 섞임

**다음: 클러스터 ID 생성 로직?** /c 🐱
