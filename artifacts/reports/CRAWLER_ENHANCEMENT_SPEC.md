# 크롤러 개선 스펙 (소미 리서치 기반)

*작성: 소미 🐱 | 2026-02-06*
*용도: Claude Code 구현 가이드*

---

## 완료된 작업 ✅

- [x] Phase 3: CrawledVideoData DTO + outlier_factory.py
- [x] Phase 3.5: share_rate 기반 calculate_score (viral_score)
- [x] Phase 4: 파일 정리 (youtube_tasks.py, tiktok_tasks.py 분리)

---

## 1. 바이럴 벤치마크 (구현 참고용)

### 참여율 기준

| 수준 | Engagement Rate | Share Rate | 의미 |
|------|-----------------|------------|------|
| 평균 | 4-6% | 0.5% | 일반 콘텐츠 |
| 좋음 | 8-10% | 1-2% | 평균 이상 |
| **바이럴** | **12%+** | **3%+** | 알고리즘 부스트 ⭐ |

```python
# 참여율 공식
engagement_rate = (likes + comments + shares) / views * 100

# 공유율 (가장 중요한 바이럴 지표)
share_rate = shares / views * 100
```

> **핵심**: Share Rate 3%+ 는 TikTok 알고리즘 부스트 신호 (연구 기반)

---

## 2. 구현 항목

### A. K-Beauty 키워드 확장

**파일**: `tiktok_tasks.py` (또는 설정 파일)

```python
# 현재
KBEAUTY_KEYWORDS = [
    "kbeauty", "skincare", "glassskin", "makeup", 
    "koreanmakeup", "skincareroutine", "beautytok", "grwm"
]

# 추가 제안
KBEAUTY_KEYWORDS_EXTENDED = [
    # 기존
    "kbeauty", "skincare", "glassskin", "makeup", 
    "koreanmakeup", "skincareroutine", "beautytok", "grwm",
    
    # 트렌드 성분 (2025)
    "pdrn skincare", "peptide serum", "bakuchiol", "collagen skincare",
    
    # 급성장 브랜드
    "medicube", "cosrx", "tirtir", "anua", "romand", "missha",
    
    # 콘텐츠 유형
    "morning shed", "glass skin tutorial", "skincare device",
    
    # 디바이스
    "led mask", "microcurrent device",
]
```

### B. raw_payload 확장

**파일**: `tiktok_tasks.py` → `_collect_from_socialkit()` 또는 해당 함수

```python
# CrawledVideoData 생성 시 raw_payload에 추가
raw_payload = {
    "source": "socialkit_search",
    "query": keyword,
    
    # 기존
    "author_name": video.author_name,
    "hashtags": video.hashtags,
    "save_count": video.saves,
    "created_at": video.created_at,
    
    # 추가 (SocialKit에서 제공하면)
    "sound_id": video.music_id,      # 트렌딩 사운드 분석용
    "sound_name": video.music_name,
    "region": video.region,          # 지역별 트렌드
    "posted_hour": video.created_at.hour if video.created_at else None,
    "posted_weekday": video.created_at.weekday() if video.created_at else None,
}
```

### C. 포스팅 시간 가중치 (선택적)

**연구 결과**: 목요일 7-9AM, 토요일 10AM-7PM 포스팅이 바이럴 가능성 높음

```python
def get_posting_time_boost(created_at: datetime) -> float:
    """포스팅 시간 기반 가중치 (1.0 ~ 1.2)"""
    if created_at is None:
        return 1.0
    
    weekday = created_at.weekday()  # 0=월, 6=일
    hour = created_at.hour
    
    # 목요일 7-9 AM (현지시간 기준)
    if weekday == 3 and 7 <= hour <= 9:
        return 1.2
    
    # 토요일 10 AM - 7 PM
    if weekday == 5 and 10 <= hour <= 19:
        return 1.15
    
    # 금요일 4-6 PM
    if weekday == 4 and 16 <= hour <= 18:
        return 1.1
    
    return 1.0

# calculate_score에 적용 (선택적)
# final_score = viral_score * get_posting_time_boost(created_at)
```

### D. 크리에이터 평균 대비 아웃라이어 탐지

**개념**: 같은 크리에이터의 평균 조회수 대비 몇 배인지 계산

```python
# 새 함수 또는 별도 서비스
def calculate_creator_multiplier(
    video_views: int,
    creator_username: str,
    db_session,
) -> float:
    """
    크리에이터 평균 대비 배수 계산
    
    예: 평소 10만뷰 → 이번 영상 100만뷰 → multiplier = 10x
    """
    from sqlalchemy import func, select
    from app.models import OutlierItem
    
    # 최근 30일 해당 크리에이터 평균 조회수
    avg_result = db_session.execute(
        select(func.avg(OutlierItem.view_count))
        .where(
            OutlierItem.creator_username == creator_username,
            OutlierItem.crawled_at >= utcnow() - timedelta(days=30),
        )
    ).scalar()
    
    if avg_result and avg_result > 0:
        return video_views / avg_result
    
    return 1.0  # 데이터 없으면 기본값

# 사용 예시
multiplier = calculate_creator_multiplier(video.views, video.author, db)
if multiplier >= 10:
    # 평소보다 10배 이상 → 바이럴 신호
    outlier.outlier_score *= 1.5
    outlier.raw_payload["creator_multiplier"] = multiplier
```

### E. Tier 기준 조정 (선택적)

**현재 (조회수 기반)**:
```python
def calculate_tier(score: float) -> str:
    if score >= 50: return "SS"  # 5M+ views
    elif score >= 20: return "S"  # 2M+ views
    elif score >= 10: return "A"  # 1M+ views
    elif score >= 5: return "B"   # 500K+ views
    return "C"
```

**제안 (참여율 반영)**:
```python
def calculate_tier_v2(score: float, engagement_rate: float, share_rate: float) -> str:
    """
    점수 + 참여율 기반 티어
    
    - 참여율 12%+ 또는 공유율 3%+ → 한 단계 승급
    """
    base_tier = calculate_tier(score)
    
    # 바이럴 신호 있으면 승급
    if engagement_rate >= 12 or share_rate >= 3:
        tier_order = ["C", "B", "A", "S", "SS"]
        current_idx = tier_order.index(base_tier)
        if current_idx < len(tier_order) - 1:
            return tier_order[current_idx + 1]
    
    return base_tier
```

---

## 3. 스카웃 알림 개선 (완료된 것 확인)

**파일**: `notification_service.py` → `_format_scout_message()`

```python
# 현재 포함된 것 (Phase 2에서 추가됨)
f"📊 *참여율:* {engagement:.1f}% | *점수:* `{score:.0f}x`\n"
f"👁️ {views_str} | ❤️ {likes_str} | 💬 {comments_str} | 🔄 {shares_str}\n"
```

**추가 제안** (선택적):
```python
# 바이럴 신호 표시
viral_signals = []
if share_rate >= 0.03:
    viral_signals.append("🔥 공유율 3%+")
if creator_multiplier and creator_multiplier >= 10:
    viral_signals.append(f"⚡ 평소 {creator_multiplier:.0f}배")

if viral_signals:
    message += f"🚀 *바이럴 신호:* {' | '.join(viral_signals)}\n"
```

---

## 4. 우선순위

| 순위 | 항목 | 난이도 | 영향도 |
|------|------|--------|--------|
| 1 | K-Beauty 키워드 확장 | 쉬움 | 높음 |
| 2 | raw_payload 확장 | 쉬움 | 중간 |
| 3 | 크리에이터 multiplier | 중간 | 높음 |
| 4 | 포스팅 시간 가중치 | 쉬움 | 낮음 |
| 5 | Tier 기준 조정 | 중간 | 중간 |

---

## 5. 검증 방법

```bash
# 1. 테스트 실행
pytest tests/test_outlier_factory.py -v
pytest --testmon

# 2. 로컬 크롤 테스트
cd backend
celery -A app.workers.celery_app worker -Q crawler --loglevel=info

# 다른 터미널에서
python -c "
from app.workers.tiktok_tasks import crawl_tiktok_socialkit
crawl_tiktok_socialkit.delay(keywords=['kbeauty', 'medicube'], min_views=100000, max_results=10)
"

# 3. DB 확인 (Neon MCP)
SELECT category, outlier_tier, 
       AVG(view_count) as avg_views,
       AVG((like_count + COALESCE(comment_count,0) + COALESCE(share_count,0))::float / NULLIF(view_count,0) * 100) as avg_engagement
FROM outlier_items 
WHERE crawled_at > NOW() - INTERVAL '1 day'
GROUP BY category, outlier_tier
ORDER BY outlier_tier, avg_engagement DESC;
```

---

## References

- [소미 리서치] `artifacts/reports/TIKTOK_VIRAL_BENCHMARKS_2025.md`
- [소미 리서치] `artifacts/reports/KBEAUTY_TIKTOK_RESEARCH.md`
- NIQ: K-Beauty's Viral Rise in US (2025)
- Hootsuite: Best Time to Post on TikTok (2025)
- Shortimize: TikTok View Rate Benchmarks
