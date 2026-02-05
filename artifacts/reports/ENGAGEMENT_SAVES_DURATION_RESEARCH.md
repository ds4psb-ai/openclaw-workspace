# Engagement, Saves, Duration 심화 연구

*작성: 소미 🐱 | 2026-02-06*

---

## 1. Engagement Rate 벤치마크 (2025)

### 플랫폼별 비교

| 플랫폼 | 평균 참여율 |
|--------|-------------|
| **TikTok** | 2.5-4.6% |
| Instagram | 0.5-0.7% |
| Facebook | 0.1-0.2% |
| YouTube | <1% |

> TikTok이 5배 이상 높음!

### 참여율 기준

| 수준 | 참여율 |
|------|--------|
| 평균 | 2.5-4.6% |
| 좋음 | **5%+** |
| 우수 | **8-10%+** |

### 팔로워 규모별 참여율

| 팔로워 | 참여율 | 인사이트 |
|--------|--------|----------|
| <100K | **7.5%** | 소규모 = 높은 참여 |
| 100K-500K | 5.1% | |
| 500K-1M | 4.48% | |
| 1M-5M | 3.76% | |
| 5M-10M | 4.22% | 반등 |
| 10M+ | 2.88% | 메가 = 낮은 참여 |

> 📌 **소규모 크리에이터 주목!** 팔로워 적어도 바이럴 가능

### 업종별 참여율

| 업종 | 참여율 |
|------|--------|
| 고등교육 | 7.36% |
| 비영리 | 3.04% |
| 여행 | 2.73% |
| 스포츠 | 2.68% |
| Food & Beverage | 2.04% |
| Fashion | 0.95% |
| **Health & Beauty** | **0.85%** |
| Agencies | 0.7% |

> ⚠️ **Health & Beauty가 가장 낮음!** K-Beauty 평가 시 참고

---

## 2. Saves (저장) - 가장 강력한 바이럴 지표

### 왜 중요한가?

> "Saves = content users want to revisit = high utility or entertainment value"
> — TikTok Algorithm 2025

- 저장 = "나중에 다시 볼 것" = **높은 가치 신호**
- 알고리즘이 **shares + saves를 가장 강력한 relevance 신호**로 처리
- 2025년 알고리즘 업데이트: saves/shares 가중치 증가

### Save Rate 계산

```python
save_rate = saves / view_count * 100
```

### Save Rate 벤치마크 (추정)

| 수준 | Save Rate |
|------|-----------|
| 평균 | 0.1-0.3% |
| 좋음 | 0.5-1% |
| 바이럴 | **1%+** |

> 📌 **Save Rate 1%+ = 바이럴 후보**

### 활용 제안

```python
# outlier_factory.py에 save_rate 보너스 추가
def calculate_score(...):
    # 기존 share_rate 보너스에 더해
    save_rate = (saves or 0) / view_count
    if save_rate >= 0.01:  # 1%+
        viral_score += 1.5  # 보너스
```

---

## 3. Duration (영상 길이) - 최적 길이 분석

### 목적별 최적 길이

| 목적 | 길이 | 특징 |
|------|------|------|
| **바이럴** | 11-18초 | 높은 완시청률, 리플레이 |
| 스토리텔링 | 21-34초 | 훅 + 페이오프 |
| 교육/정보 | 30-60초 | edutainment |
| 딥다이브 | 1-3분 | 전문 콘텐츠 |

> ⚠️ **35초 이후 이탈률 급증!**

### K-Beauty 콘텐츠 최적 길이

| 콘텐츠 유형 | 추천 길이 |
|-------------|-----------|
| Before/After | 11-18초 |
| GRWM (짧은) | 21-34초 |
| 튜토리얼 | 30-60초 |
| 루틴 풀버전 | 60-120초 |

### Meme/Comedy 최적 길이

| 콘텐츠 유형 | 추천 길이 |
|-------------|-----------|
| 펀치라인 | 7-15초 |
| 스킷 | 15-30초 |
| POV | 21-34초 |

### Duration 기반 분석 쿼리

```sql
-- 길이별 성과 분석
SELECT 
    CASE 
        WHEN (raw_payload->>'duration')::int <= 15 THEN '0-15s (viral)'
        WHEN (raw_payload->>'duration')::int <= 34 THEN '15-34s (story)'
        WHEN (raw_payload->>'duration')::int <= 60 THEN '34-60s (edu)'
        ELSE '60s+ (deep)'
    END as duration_bucket,
    COUNT(*) as count,
    AVG(view_count) as avg_views,
    AVG((like_count + comment_count + share_count)::float / NULLIF(view_count,0) * 100) as avg_engagement
FROM outlier_items
WHERE raw_payload->>'duration' IS NOT NULL
GROUP BY duration_bucket
ORDER BY avg_engagement DESC;
```

---

## 4. 통합 바이럴 점수 제안

### 현재 vs 개선

```python
# 현재
score = base_score + share_bonus + engagement_bonus

# 개선 (saves + duration 반영)
def calculate_viral_score_v2(view_count, likes, comments, shares, saves, duration):
    base_score = view_count / 100_000
    
    engagement = (likes + comments + shares) / view_count
    share_rate = shares / view_count
    save_rate = saves / view_count if saves else 0
    
    # 공유율 보너스
    share_bonus = 2.0 if share_rate >= 0.03 else (share_rate * 50)
    
    # 저장률 보너스 (신규)
    save_bonus = 1.5 if save_rate >= 0.01 else (save_rate * 100)
    
    # 참여율 보너스
    engagement_bonus = engagement * 10
    
    # Duration 보너스 (11-34초 최적)
    duration_bonus = 0
    if 11 <= duration <= 34:
        duration_bonus = 0.5  # 최적 길이
    elif duration < 11 or duration > 60:
        duration_bonus = -0.5  # 너무 짧거나 길면 감점
    
    return base_score + share_bonus + save_bonus + engagement_bonus + duration_bonus
```

---

## 5. 핵심 인사이트

### 바이럴 필수 조건
1. **Share Rate 3%+** - 알고리즘 부스트
2. **Save Rate 1%+** - 높은 가치 신호
3. **Duration 11-34초** - 최적 완시청률
4. **Engagement 5%+** - 평균 이상

### K-Beauty 특화 주의사항
- Health & Beauty 업종 평균 참여율 **0.85%** (가장 낮음)
- 5% 이상이면 **우수**, 2% 이상이면 **양호**
- 업종 평균 대비로 평가해야 함

### 데이터 수집 후 할 것
1. duration 구간별 성과 분석
2. save_rate와 바이럴 상관관계
3. K-Beauty vs Meme 업종 벤치마크 비교

---

## References

- [Emplicit - TikTok Engagement Rate Benchmarks 2025](https://emplicit.co/tiktok-engagement-rate-benchmarks-2025/)
- [Shortimize - Good Engagement Rate on TikTok](https://www.shortimize.com/blog/what-is-a-good-engagement-rate-on-tiktok)
- [TriVision - Best Length for TikTok Video 2026](https://trivisionstudios.com/best-length-for-tiktok-video-in-2026/)
- [Fanpage Karma - TikTok Algorithm 2025](https://www.fanpagekarma.com/insights/the-2025-tiktok-algorithm-what-you-need-to-know/)
