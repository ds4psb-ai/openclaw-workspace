# TikTok 바이럴 벤치마크 & API 대안 연구

*작성: 소미 🐱 | 2026-02-06*

---

## 1. 바이럴 벤치마크 (2025 기준)

### 참여율 (Engagement Rate)

| 수준 | Engagement Rate | Like Ratio | 의미 |
|------|-----------------|------------|------|
| 평균 | 4-6% | 4% | 일반적인 콘텐츠 |
| 좋음 | 8-10% | 5-10% | 평균 이상 성과 |
| **바이럴** | **12%+** | **10%+** | 알고리즘 부스트 |

> 📌 **참여율 공식**: `(likes + comments + shares) / views × 100`

### 세부 지표

| 지표 | 평균 | 좋음 | 바이럴 |
|------|------|------|--------|
| Like Ratio | 4% | 5-10% | 10%+ |
| Comment Rate | 0.2% | 0.5-2% | 2%+ |
| Share Rate | 0.5% | 1-2% | **3%+** ⭐ |

> ⚡ **Share Rate가 가장 중요!** TikTok 알고리즘이 공유 많은 영상에 부스트 줌

### View-to-Follower Ratio

| 팔로워 규모 | 평균 조회수 | 목표 비율 |
|-------------|-------------|-----------|
| 1K-5K | 860/post | 17-86% |
| 50K-100K | 8,700/post | 9-17% |
| 100K-1M | 25,200/post | 3-25% |
| 1M+ | 가변적 | 1-5% |

### Watch Time (시청 지속률)

| 지표 | 목표 | 의미 |
|------|------|------|
| 3초 유지율 | **70-80%+** | Hook 성공 여부 |
| 평균 시청시간 | 15-20초 | 30초 영상 기준 50-70% |
| 완시청률 | 50%+ | 짧은 영상일수록 높아야 함 |

---

## 2. 아웃라이어 탐지 기준 제안

현재 시스템 vs 벤치마크 기반 개선안:

### 현재 (조회수 기반)
```
SS: 5M+ views
S:  1M+ views
A:  500K+ views
B:  100K+ views
```

### 개선안 (참여율 기반)
```python
def calculate_tier(views, likes, comments, shares):
    engagement = (likes + comments + shares) / views * 100
    share_rate = shares / views * 100
    
    # 바이럴 잠재력 = 참여율 + 공유율 가중치
    viral_score = engagement + (share_rate * 2)  # 공유율 2배 가중
    
    if views >= 5_000_000 and viral_score >= 12:
        return "SS"  # 대규모 + 높은 참여
    elif views >= 1_000_000 and viral_score >= 10:
        return "S"
    elif views >= 500_000 and viral_score >= 8:
        return "A"
    elif viral_score >= 6:
        return "B+"  # 조회수 낮아도 참여율 좋음
    else:
        return "B"
```

### 핵심 인사이트
1. **Share Rate 3%+** → 알고리즘 부스트 신호
2. **소규모 계정 (1-5K)도 바이럴 가능** → 팔로워 무관하게 수집
3. **3초 Hook** → 썸네일/제목 중요성

---

## 3. TikTok API 대안 분석

### 현재 사용 중
- **SocialKit**: 1 credit / 20 videos (비용 효율적)

### 무료 대안

| 이름 | 유형 | 장점 | 단점 |
|------|------|------|------|
| **TikTok-Api** (davidteather) | Python 오픈소스 | 무료, 활발한 유지보수 | 봇 감지 취약, 프록시 필요 |
| **tiktok-scraper** | Node.js | 무료, 빠름 | 업데이트 느림 |

### 유료 대안

| 이름 | 가격대 | 특징 |
|------|--------|------|
| **TikAPI** | $49+/월 | 풀 API, 500+ 회사 사용 |
| **EnsembleData** | 문의 | 인플루언서 마케팅 특화 |
| **TikHub API** | $29+/월 | 700+ endpoints, 14개 플랫폼 |
| **Apify** | $49+/월 | 노코드, 크레딧 기반 |
| **Phyllo** | 문의 | Creator 데이터 특화 |

### 추천

**현재 유지**: SocialKit (비용 효율 최고)

**백업 옵션**:
1. **TikTok-Api (무료)** - 직접 운영 시 비용 0, 단 프록시 비용 발생
2. **TikHub** - SocialKit 대비 엔드포인트 다양

---

## 4. 크롤러 개선 제안

### A. Engagement 기반 필터링 추가

```python
# 현재: 조회수만 체크
if video.views >= 500_000:
    collect(video)

# 개선: 참여율도 체크
engagement = (video.likes + video.comments + video.shares) / video.views
if video.views >= 100_000 and engagement >= 0.08:  # 10만뷰 + 8% 참여율
    collect(video)  # 조회수 낮아도 바이럴 잠재력 있음
```

### B. Share Rate 우선순위

```python
# 공유율 3% 이상이면 자동 SS 후보
share_rate = video.shares / video.views
if share_rate >= 0.03:
    video.priority = "HIGH"
    video.viral_signal = "share_rate_3pct"
```

### C. 크리에이터 평균 대비 성과

```python
# 크리에이터 평균 조회수 대비 몇 배?
creator_avg = get_creator_avg_views(video.author)
multiplier = video.views / creator_avg
if multiplier >= 10:  # 평소보다 10배 이상
    video.outlier_score *= 2  # 점수 부스트
```

---

## 5. 다음 연구 주제

1. **K-Beauty 특화 벤치마크** - 뷰티 카테고리 평균 참여율
2. **시간대별 바이럴 패턴** - 언제 올린 영상이 터지나
3. **해시태그 효과 분석** - #kbeauty vs #skincare 성과 비교
4. **Trending Sound 연동** - 음원 트렌드 API 연동 가능성

---

## References

- [Shortimize - TikTok View Rate Benchmarks 2025](https://www.shortimize.com/blog/what-is-a-good-view-rate-for-tiktok)
- [Proxidize - TikTok Statistics 2025](https://proxidize.com/research/tiktok-statistics/)
- [Fanpage Karma - TikTok Algorithm 2025](https://www.fanpagekarma.com/insights/the-2025-tiktok-algorithm-what-you-need-to-know/)
- [GitHub - davidteather/TikTok-Api](https://github.com/davidteather/TikTok-Api)
