# 🐱→🐰 클러스터 이름 생성 분석

## _generate_cluster_name() 구조

```python
# clustering.py:1577-1660
def _generate_cluster_name(self, normalized: dict, pattern_type: str) -> Tuple[str, dict]:
    """클러스터에 의미 있는 이름 생성 (VDG 4축 반영)"""
```

## VDG 4축 이름 구조

```
"[카테고리]•[훅타입] [딜리버리] ([오디오특성])"
```

### 예시
| 패턴 | 이름 |
|------|------|
| 뷰티 + POV + 빠른컷 + 트렌딩 | "뷰티•POV 빠른컷 (트렌딩음악)" |
| 댄스 + 튜토리얼 + 슬로우 | "댄스•튜토리얼 슬로우" |
| 밈 + 리액션 | "밈•리액션" |

## 4축 추출 로직

### 1. 카테고리
```python
category_kr = CATEGORY_KR.get(category_key, ...)
# 뷰티, 댄스, 밈, 음식, 여행...
```

### 2. 훅타입
```python
hook_kr = HOOK_TYPE_KR.get(hook_type_key, ...)
# POV, 튜토리얼, 리액션, 브이로그...
```

### 3. 딜리버리 스타일
```python
# visual_patterns에서 추출
delivery_kr = DELIVERY_STYLE_KR.get(delivery_key, ...)
# 빠른컷, 슬로우모션, 줌인, 팬...
```

### 4. 오디오 특성
```python
if audio_flags.get("is_trending"):
    audio_trait_kr = "트렌딩음악"
elif audio_flags.get("is_original"):
    audio_trait_kr = "오리지널"
# 트렌딩, 오리지널, ASMR, 보이스오버...
```

## 훅 레일 vs 패턴 레일

| 타입 | 예시 | 사용처 |
|------|------|--------|
| 훅 레일 | "뷰티•POV" | hook_type만 |
| 패턴 레일 | "뷰티•POV 빠른컷 (트렌딩음악)" | VDG 4축 전체 |

## 국제화 지원

```python
name_components = {
    "hook_type": "pov",
    "category": "beauty",
    "delivery": "quick_cuts",
    "audio_trait": "trending"
}
# → 프론트엔드에서 i18n 변환 가능!
```

**다음: DNA 집계 알고리즘?** /c 🐱
