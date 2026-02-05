# 해시태그 조합 분석 & Meme 카테고리 연구

*작성: 소미 🐱 | 2026-02-06*

---

## 1. 해시태그 조합 전략

### 최적 개수
- **3-5개** 권장 (CapCut/ByteDance 공식)
- 너무 많으면 알고리즘 혼란

### 3-3-3 전략 (9개 최대)

| 유형 | 예시 | 목적 |
|------|------|------|
| **Broad (3개)** | #fyp, #viral, #trending | 넓은 도달 |
| **Niche (3개)** | #kbeauty, #skincareroutine | 타겟 커뮤니티 |
| **Content-specific (3개)** | #glassskintutorial, #pdrn | 검색 SEO |

### TikTok SEO 시대

> **41% Gen Z가 소셜앱을 검색엔진으로 사용** (Sprout Social 2025)

해시태그 = **검색 키워드**로 취급해야 함
- ❌ #fyp 30개 도배
- ✅ 정확한 키워드 3-5개

### 해시태그 조합별 성과 (일반적 패턴)

| 조합 | 도달 | 참여율 | 적합 |
|------|------|--------|------|
| Broad only | 높음 | 낮음 | 인지도 목적 |
| Niche only | 낮음 | 높음 | 커뮤니티 빌딩 |
| **Mixed (3-3-3)** | 중간 | 중상 | **최적** |

---

## 2. K-Beauty 해시태그 추천

### Broad (도달용)
```
#fyp #foryou #viral #trending #beauty #skincare
```

### Niche (K-Beauty 커뮤니티)
```
#kbeauty #koreanbeauty #glassskin #koreanskincare
#beautytok #skincaretok #grwm
```

### Content-specific (검색 SEO)
```
#pdrnskincare #peptideserum #glassskintutorial
#morningshed #medicubereview #cosrxreview
#skincareroutine2025 #beforeafter
```

### 브랜드 해시태그
```
#medicube #cosrx #tirtir #anua #romand #missha
```

---

## 3. Meme 카테고리 분리 전략

### 현재 문제
- K-Beauty와 Meme이 같은 파이프라인
- Meme은 조회수 높지만 비즈니스 가치 다름
- 참여 패턴이 다름 (공유율 특히 높음)

### Meme 특성

| 지표 | Beauty | Meme |
|------|--------|------|
| 평균 조회수 | 낮음 | 높음 |
| 참여율 | 5-8% | 10-15% |
| 공유율 | 1-2% | **5-10%** |
| 비즈니스 가치 | 높음 (제품) | 낮음 (엔터) |
| 바이럴 속도 | 느림 | 빠름 |

### 분리 기준 제안

```python
MEME_KEYWORDS = [
    "funny", "comedy", "meme", "relatable", "humor",
    "skit", "pov", "viral", "trend", "challenge",
]

MEME_THRESHOLDS = {
    "min_views": 1_000_000,  # Beauty 500K vs Meme 1M
    "min_share_rate": 0.03,  # 3% 이상
}
```

### 구현 방안

**A. 별도 OutlierSource**
```python
# 현재
source_name = "tiktok_socialkit"

# 변경
source_name = "tiktok_socialkit_beauty"  # K-Beauty
source_name = "tiktok_socialkit_meme"    # Meme/Comedy
```

**B. category 필드 활용**
```python
# 현재: keyword 그대로
category = "kbeauty"

# 변경: 메타 카테고리 추가
category = "kbeauty"
content_category = "beauty"  # or "meme"
```

**C. 별도 Celery Task**
```python
@celery_app.task
def crawl_tiktok_meme():
    """Meme/Comedy 크롤러 (높은 threshold)"""
    return crawl_tiktok_socialkit(
        keywords=MEME_KEYWORDS,
        min_views=1_000_000,  # 1M+
    )
```

### Beat Schedule 제안

```python
# Beauty: 6시간마다
"tiktok-beauty-crawl": {
    "schedule": crontab(minute=15, hour="0,6,12,18"),
    "kwargs": {"keywords": KBEAUTY_KEYWORDS, "min_views": 500000},
}

# Meme: 12시간마다 (덜 자주)
"tiktok-meme-crawl": {
    "schedule": crontab(minute=15, hour="3,15"),
    "kwargs": {"keywords": MEME_KEYWORDS, "min_views": 1000000},
}
```

---

## 4. raw_payload 해시태그 활용

### 현재 수집 중
```python
raw_payload = {
    "hashtags": ["kbeauty", "skincare", "glassskin"],
}
```

### 분석 아이디어

**A. 해시태그 조합별 성과**
```sql
-- 해시태그 조합별 평균 참여율
SELECT 
    raw_payload->'hashtags' as tags,
    AVG(view_count) as avg_views,
    AVG((like_count + comment_count + share_count)::float / view_count * 100) as avg_engagement
FROM outlier_items
WHERE raw_payload->'hashtags' IS NOT NULL
GROUP BY raw_payload->'hashtags'
ORDER BY avg_engagement DESC
LIMIT 20;
```

**B. 공통 해시태그 빈도**
```python
def analyze_hashtag_frequency():
    """SS/S tier 영상의 공통 해시태그"""
    items = get_outliers(tier=["SS", "S"])
    
    tag_counts = Counter()
    for item in items:
        tags = item.raw_payload.get("hashtags", [])
        tag_counts.update(tags)
    
    return tag_counts.most_common(30)
```

**C. 해시태그 → 참여율 상관관계**
```python
# #grwm 포함 영상 vs 미포함 영상 참여율 비교
with_grwm = get_outliers(hashtag_contains="grwm")
without_grwm = get_outliers(hashtag_not_contains="grwm")

print(f"#grwm 평균 참여율: {avg_engagement(with_grwm):.2f}%")
print(f"#grwm 미포함: {avg_engagement(without_grwm):.2f}%")
```

---

## 5. 구현 우선순위

| 순위 | 항목 | 난이도 | 가치 |
|------|------|--------|------|
| 1 | 해시태그 빈도 분석 스크립트 | 쉬움 | 높음 |
| 2 | Meme 카테고리 분리 (별도 source) | 중간 | 중간 |
| 3 | 해시태그 → 성과 상관관계 분석 | 중간 | 높음 |
| 4 | 자동 해시태그 추천 | 높음 | 높음 |

---

## 6. 다음 단계

1. **데이터 수집** - 일주일 정도 raw_payload에 hashtags 쌓이면
2. **분석 스크립트** - SS/S tier 공통 해시태그 추출
3. **인사이트 리포트** - "이 해시태그 조합이 가장 효과적"
4. **Meme 분리** - 필요 시 별도 파이프라인

---

## References

- [Sprout Social - TikTok Hashtags 2025](https://sproutsocial.com/insights/tiktok-hashtags/)
- [Admetrics - TikTok Hashtags Guide](https://www.admetrics.io/en/post/tiktok-hashtags)
- TikTok Creative Center - Trend Discovery
