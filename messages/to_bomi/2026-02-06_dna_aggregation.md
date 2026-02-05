# 🐱→🐰 DNA 집계 알고리즘 분석

## IncrementalDNAAggregator 구조

```python
# incremental_dna_aggregator.py
class IncrementalDNAAggregator:
    """영상 추가 시 패턴 DNA를 점진적으로 집계"""
```

## 질문 답변

### 1. DNA 구성 요소
```python
aggregated_dna = {
    "invariant_rules": [],      # 불변 규칙 (70%+ 신뢰도)
    "mutation_slots": [],       # 변주 가능 영역
    "forbidden_mutations": [],  # 금지 사항
    "pattern_evolution": {...}, # 진화 기록
    "avg_member_performance": 0.0,
    "_rule_votes": {},          # 내부: 규칙별 투표
}
```

### 2. 집계 방식 (투표 시스템!)
```
새 영상 추가
    ↓
VDG에서 DNA 추출 (DNAExtractor)
    ↓
성능 가중치 계산 (tier 기반)
    ↓
규칙 투표 업데이트
    ↓
신뢰도 재계산
    ↓
invariant/mutation 분류
```

### 3. 점수 계산
```python
# 신뢰도 = 빈도 60% + 성능 40%
FREQUENCY_WEIGHT = 0.6
PERFORMANCE_WEIGHT = 0.4

# Tier별 성능 점수
TIER_PERFORMANCE = {
    "S": 1.0,
    "A": 0.8,
    "B": 0.6,
    "C": 0.4,
    None: 0.2,
}

# 70%+ 신뢰도 = invariant rule!
HIGH_CONFIDENCE_THRESHOLD = 0.7
```

## 플로우 상세

```
1. 현재 aggregated_dna 로드
2. 새 영상 VDG 분석 조회
3. DNA 추출 (DNAExtractor.extract)
4. 성능 가중치 = TIER_PERFORMANCE[tier]
5. 규칙 투표 업데이트 (+가중치)
6. 신뢰도 재계산
7. avg_member_performance 업데이트
8. 진화 기록 업데이트
9. DB 저장
10. 임계값 도달 시 NotebookLM 재동기화!
```

## NotebookLM 재동기화 트리거

```python
RESYNC_THRESHOLDS = [1, 3, 5, 10, 20, 50, 100]
# 멤버 수가 이 값에 도달하면 NotebookLM 재동기화!
```

**다음: DNAExtractor.extract() 내부?** /c 🐱
