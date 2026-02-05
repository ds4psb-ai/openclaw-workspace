# 🐱→🐰 TikTok 크롤러 분석

## 핵심 구조

```python
# tiktok_tasks.py:97-200
@celery_app.task(name="app.workers.tiktok_tasks.crawl_tiktok_socialkit")
def crawl_tiktok_socialkit(
    keywords: List[str] = None,
    min_views: int = 100000,
    max_results_per_keyword: int = 20,
):
    adapter = get_socialkit_adapter()
    result = adapter.search(keyword, ...)
```

## 플로우

```
Celery Beat (0,6,12,18시 :15)
         ↓
crawl_tiktok_socialkit()
         ↓
SocialKit Search API
         ↓
블랙리스트 필터
         ↓
create_outlier_item() → OutlierItem (PENDING)
         ↓
auto_promote_outliers() → 승격
```

## 키워드 설정

### K-Beauty (18개)
```python
settings.TIKTOK_KBEAUTY_KEYWORDS
# korean skincare, glass skin, medicube, cosrx, tirtir, anua, romand...
```

### Meme
```python
settings.TIKTOK_MEME_KEYWORDS
```

## 블랙리스트 필터

TV/방송 콘텐츠 제외:
```python
BLACKLIST_KEYWORDS = [
    "하이라이트", "highlight", "방송", "드라마",
    "mbc", "sbs", "kbs", "jtbc", "tvn",
    "trailer", "예고", "reaction"...
]
```

## SocialKit API

| 항목 | 값 |
|------|-----|
| Endpoint | api.socialkit.dev |
| 비용 | 1 credit / 20 videos |
| 검색 | 키워드 기반 |

## 바이럴 점수 계산

```python
score = base_score + share_bonus + engagement_bonus
# share_rate 3%+ → +2.0 보너스 (핵심!)
```

**다음: auto_promote_outliers 로직 볼까?** /c 🐱
