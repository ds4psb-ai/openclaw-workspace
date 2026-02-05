# 바이럴 아웃라이어 탐지 & 비용 효율 크롤링 전략

> 연구일: 2026-02-05  
> 목적: TikTok/YouTube 뷰티 콘텐츠에서 오가닉 바이럴 아웃라이어를 비용 효율적으로 탐지하는 시스템 구축

---

## 1. 바이럴 아웃라이어 탐지 알고리즘

### 1.1 아웃라이어 정의 기준

#### 핵심 메트릭: Viral Multiplier (VM)
```
VM = 조회수 / 팔로워수
```

| VM 범위 | 분류 | 설명 |
|---------|------|------|
| < 1x | Underperform | 팔로워 대비 저조 |
| 1x - 5x | Normal | 일반적 성과 |
| 5x - 20x | Good | 양호한 성과 |
| 20x - 50x | Excellent | 우수 성과 |
| **≥ 50x** | **Outlier** | 바이럴 아웃라이어 (Virlo.ai 기준) |

#### 보조 메트릭: Engagement Outlier Score (EOS)
```python
# Z-Score 기반 (평균에서 얼마나 벗어났는지)
z_score = (engagement_rate - creator_avg_engagement) / creator_std_engagement

# IQR 기반 (더 robust, 왜곡된 분포에 강함)
Q1, Q3 = np.percentile(creator_engagements, [25, 75])
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

is_outlier = engagement_rate > upper_bound or z_score > 2.5
```

**권장**: 소셜 미디어 데이터는 long-tail 분포이므로 **IQR 방식** 권장

### 1.2 플랫폼별 벤치마크 (2025-2026)

#### TikTok
| 팔로워 규모 | 평균 참여율 | 아웃라이어 기준 (상위 5%) |
|------------|------------|------------------------|
| < 5K | 4.2% - 5.0% | > 15% |
| 5K - 100K | 2.5% - 4.0% | > 12% |
| 100K - 1M | 1.5% - 2.5% | > 8% |
| > 1M | 0.8% - 1.5% | > 5% |

#### YouTube Shorts
| 팔로워 규모 | 평균 참여율 | 아웃라이어 기준 |
|------------|------------|----------------|
| < 10K | 3.0% - 4.5% | > 10% |
| 10K - 500K | 1.5% - 3.0% | > 7% |
| > 500K | 0.5% - 1.5% | > 4% |

### 1.3 시간 기반 급상승 탐지 (Velocity Detection)

#### Velocity Score 계산
```python
def calculate_velocity(views_history: list, timestamps: list) -> dict:
    """
    시간별 조회수 증가 속도 분석
    
    views_history: [1000, 5000, 25000, 100000]
    timestamps: [0h, 1h, 3h, 6h]
    """
    velocities = []
    for i in range(1, len(views_history)):
        delta_views = views_history[i] - views_history[i-1]
        delta_time = timestamps[i] - timestamps[i-1]  # hours
        velocity = delta_views / delta_time
        velocities.append(velocity)
    
    return {
        'max_velocity': max(velocities),
        'avg_velocity': sum(velocities) / len(velocities),
        'acceleration': velocities[-1] / velocities[0] if velocities[0] > 0 else float('inf')
    }
```

#### Early Viral Signals (첫 1-24시간)
| 시간대 | 바이럴 시그널 | 임계값 |
|--------|-------------|--------|
| 첫 1시간 | Watch time > 80% | Hook 성공 |
| 첫 3시간 | Views > 5x 평균 | 알고리즘 픽업 |
| 첫 6시간 | Shares > 평균의 10x | 확산 시작 |
| 24시간 | Profile views +200-300% | 크리에이터 발굴 |

#### 실시간 모니터링 파이프라인
```python
class VelocityMonitor:
    """
    게시 후 24시간 동안 velocity 추적
    """
    CHECKPOINTS = [1, 3, 6, 12, 24]  # hours
    
    def should_escalate(self, video_id: str) -> bool:
        """급상승 중인 콘텐츠인지 판단"""
        views_at_checkpoints = self.get_views_at_checkpoints(video_id)
        
        # 기준: 3시간 내 5x 증가 + 가속 중
        if len(views_at_checkpoints) >= 2:
            growth_rate = views_at_checkpoints[-1] / views_at_checkpoints[0]
            is_accelerating = self.is_accelerating(views_at_checkpoints)
            
            return growth_rate > 5 and is_accelerating
        return False
```

---

## 2. 오가닉 바이럴 vs 광고 판별

### 2.1 스폰서 콘텐츠 탐지 방법

#### 텍스트 기반 탐지 (NLP)
```python
SPONSOR_KEYWORDS = {
    'explicit': [
        '#ad', '#sponsored', '#partnership', '#gifted',
        '#광고', '#협찬', '#유료광고포함', 'Paid partnership',
        '제공받았', '협찬받았', '소정의 원고료'
    ],
    'implicit': [
        '링크는 프로필', '할인코드', '링크 타고', 
        '스와이프업', 'link in bio', 'code:', 'use code'
    ]
}

def detect_sponsored_text(caption: str, comments: list) -> dict:
    caption_lower = caption.lower()
    
    # Explicit 키워드 (확실한 광고)
    explicit_match = any(kw in caption_lower for kw in SPONSOR_KEYWORDS['explicit'])
    
    # Implicit 키워드 (광고 가능성)
    implicit_match = any(kw in caption_lower for kw in SPONSOR_KEYWORDS['implicit'])
    
    # 댓글 분석 (브랜드/회사 계정 댓글)
    brand_comment = any(is_brand_account(c.author) for c in comments[:20])
    
    return {
        'is_sponsored': explicit_match,
        'likely_sponsored': implicit_match or brand_comment,
        'confidence': 1.0 if explicit_match else (0.7 if implicit_match else 0.3)
    }
```

#### 메타데이터 기반 탐지
```python
def detect_sponsored_metadata(video_data: dict) -> dict:
    signals = {
        # 플랫폼 공식 라벨
        'has_paid_partnership_label': video_data.get('is_paid_partnership', False),
        
        # 태그에 브랜드명 포함
        'has_brand_tag': bool(extract_brand_mentions(video_data.get('hashtags', []))),
        
        # 비정상적으로 많은 제품 링크
        'has_product_links': len(video_data.get('product_links', [])) > 0,
        
        # 브랜드 계정 멘션
        'mentions_brand': bool(video_data.get('mentioned_users', [])),
    }
    
    score = sum(signals.values()) / len(signals)
    return {'signals': signals, 'sponsored_probability': score}
```

### 2.2 오가닉 바이럴의 특징

| 특성 | 오가닉 바이럴 | 광고/프로모션 |
|------|-------------|--------------|
| **참여 패턴** | 지수적 성장 (J-curve) | 초기 스파이크 후 급락 |
| **댓글 다양성** | 다양한 감정, 태그, 질문 | 유사한 칭찬, 구매 의향 |
| **공유율** | Shares > Likes 비율 높음 | Likes > Shares |
| **시청 시간** | 자연스러운 분포 | 초반 집중 (CTA) |
| **소스 트래픽** | FYP/추천 우세 (70%+) | 외부/검색 트래픽 높음 |

### 2.3 ML 기반 오가닉 판별 모델

```python
from sklearn.ensemble import RandomForestClassifier

ORGANIC_FEATURES = [
    # 참여 패턴
    'share_to_like_ratio',      # 오가닉: > 0.3
    'comment_diversity_score',   # 댓글 유니크 단어 비율
    'engagement_velocity_std',   # 참여 속도 변동성 (오가닉: 높음)
    
    # 소스 분석
    'fyp_traffic_ratio',         # FYP에서 온 비율
    'external_traffic_ratio',    # 외부 링크 유입
    
    # 크리에이터 패턴
    'creator_avg_sponsored_rate', # 크리에이터 평균 광고 비율
    'posting_frequency_anomaly',  # 급격한 포스팅 빈도 변화
    
    # 텍스트/메타
    'sponsor_keyword_score',
    'brand_mention_count',
    'product_link_present',
]

class OrganicClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
    
    def predict_organic_probability(self, video_features: dict) -> float:
        """0: 확실히 광고, 1: 확실히 오가닉"""
        features = self.extract_features(video_features)
        return self.model.predict_proba([features])[0][1]
```

---

## 3. 비용 효율적 크롤링 파이프라인

### 3.1 2단계 필터 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 1: 저비용 필터링                        │
│  목적: 후보 풀 축소 (10만 → 1만)                                 │
│  비용: 무료 ~ $0.001/video                                      │
├─────────────────────────────────────────────────────────────────┤
│  • Public API (TikTok Research API - 학술용 무료)               │
│  • 기본 메타데이터만 수집 (views, likes, hashtags)               │
│  • Viral Multiplier 기준 1차 필터                               │
│  • 해시태그 기반 카테고리 필터                                   │
└──────────────────────┬──────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 2: 상세 추출                            │
│  목적: 상세 분석용 데이터 (1만 → 500 아웃라이어)                  │
│  비용: $0.01-0.05/video                                         │
├─────────────────────────────────────────────────────────────────┤
│  • 유료 API (EnsembleData, Apify, Bright Data)                  │
│  • 댓글, engagement 히스토리, 크리에이터 프로필                  │
│  • 스폰서 탐지 상세 분석                                         │
│  • 비디오 다운로드 (선택적)                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 API 호출 최소화 전략

#### 가격 비교 (2025-2026 기준)
| 서비스 | 가격 | 포함 데이터 | 추천 용도 |
|--------|------|------------|----------|
| TikTok Research API | 무료 | 기본 메타데이터 | Stage 1 |
| Apify TikTok | $0.006/query + $0.0003/post | 상세 | Stage 2 |
| EnsembleData | Pay-per-use | 실시간 | Stage 2 |
| Bright Data | $0.001-0.01/req | 전체 | 대량 크롤링 |

#### 스마트 캐싱 전략
```python
import redis
from datetime import timedelta

class SmartCache:
    """
    데이터 신선도에 따른 캐싱 전략
    """
    
    TTL_CONFIG = {
        'video_metadata': timedelta(hours=6),    # 조회수는 자주 변함
        'creator_profile': timedelta(days=7),    # 프로필은 덜 변함
        'hashtag_trending': timedelta(hours=1),  # 트렌드는 빠르게 변함
        'video_comments': timedelta(days=1),     # 댓글은 하루 단위
    }
    
    def __init__(self):
        self.redis = redis.Redis()
    
    def get_or_fetch(self, key: str, data_type: str, fetch_fn: callable):
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        
        data = fetch_fn()
        ttl = self.TTL_CONFIG.get(data_type, timedelta(hours=1))
        self.redis.setex(key, ttl, json.dumps(data))
        return data
```

#### 배치 처리 최적화
```python
from concurrent.futures import ThreadPoolExecutor
import time

class BatchProcessor:
    """
    Rate limit 준수하며 배치 처리
    """
    
    def __init__(self, rate_limit: int = 30, per_seconds: int = 60):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.request_times = []
    
    def process_batch(self, items: list, processor_fn: callable) -> list:
        results = []
        
        for item in items:
            self._wait_if_rate_limited()
            
            try:
                result = processor_fn(item)
                results.append(result)
                self.request_times.append(time.time())
            except RateLimitError:
                time.sleep(self.per_seconds)  # Exponential backoff
                result = processor_fn(item)
                results.append(result)
        
        return results
    
    def _wait_if_rate_limited(self):
        now = time.time()
        # 시간 윈도우 내 요청 수 계산
        recent = [t for t in self.request_times if now - t < self.per_seconds]
        
        if len(recent) >= self.rate_limit:
            sleep_time = self.per_seconds - (now - recent[0])
            time.sleep(max(0, sleep_time))
```

### 3.3 전체 파이프라인 아키텍처

```python
class OutlierDetectionPipeline:
    """
    비용 효율적 아웃라이어 탐지 파이프라인
    
    예상 비용 (일일):
    - Stage 1: 100,000 videos × $0 = $0 (무료 API)
    - Stage 2: 10,000 videos × $0.01 = $100
    - 총: ~$100/day for 100K video scan
    """
    
    def __init__(self):
        self.stage1_api = TikTokResearchAPI()  # 무료
        self.stage2_api = EnsembleDataAPI()    # 유료
        self.cache = SmartCache()
        self.classifier = OrganicClassifier()
    
    def run_daily_scan(self, hashtags: list, region: str = 'KR'):
        # Stage 1: 해시태그 기반 수집 (무료)
        candidates = []
        for hashtag in hashtags:
            videos = self.stage1_api.search_hashtag(
                hashtag=hashtag,
                region=region,
                max_count=10000
            )
            candidates.extend(videos)
        
        # Stage 1 필터링
        outlier_candidates = self.filter_outliers(candidates)
        print(f"Stage 1: {len(candidates)} → {len(outlier_candidates)}")
        
        # Stage 2: 상세 데이터 수집 (유료)
        detailed_data = []
        for video in outlier_candidates:
            data = self.cache.get_or_fetch(
                key=f"video:{video.id}",
                data_type='video_metadata',
                fetch_fn=lambda: self.stage2_api.get_video_details(video.id)
            )
            detailed_data.append(data)
        
        # 오가닉 필터링
        organic_outliers = [
            v for v in detailed_data
            if self.classifier.predict_organic_probability(v) > 0.7
        ]
        
        print(f"Final: {len(organic_outliers)} organic outliers found")
        return organic_outliers
    
    def filter_outliers(self, videos: list) -> list:
        """Stage 1 아웃라이어 필터"""
        outliers = []
        for v in videos:
            vm = v.views / max(v.creator_followers, 1)
            if vm >= 50:  # Viral Multiplier ≥ 50x
                outliers.append(v)
        return outliers
```

---

## 4. 뷰티 카테고리 필터링

### 4.1 해시태그 기반 필터

```python
BEAUTY_HASHTAGS = {
    # 대분류
    'primary': [
        '#뷰티', '#beauty', '#makeup', '#skincare', '#메이크업',
        '#스킨케어', '#화장품', '#cosmetics', '#beautytok'
    ],
    
    # 세부 카테고리
    'skincare': [
        '#스킨케어', '#skincareroutine', '#glassskin', '#kbeauty',
        '#피부관리', '#moisturizer', '#serum', '#sunscreen',
        '#skincareproducts', '#antiaging', '#acne'
    ],
    
    'makeup': [
        '#메이크업', '#makeuptutorial', '#lipstick', '#eyeshadow',
        '#foundation', '#concealer', '#eyemakeup', '#lipmakeup',
        '#grwm', '#makeuplook', '#dailymakeup'
    ],
    
    'haircare': [
        '#헤어', '#hair', '#haircare', '#hairstyle', '#haircolor',
        '#헤어스타일', '#염색', '#펌', '#hairtutorial'
    ],
    
    'nailart': [
        '#네일', '#nailart', '#nails', '#gelnails', '#젤네일',
        '#네일아트', '#manicure'
    ],
    
    # 트렌드/바이럴
    'trending': [
        '#tiktokmademebuyit', '#viralbeauty', '#beautyfinds',
        '#drugstoremakeup', '#affordablebeauty', '#beautyhacks'
    ]
}

def filter_beauty_content(videos: list, min_hashtag_match: int = 2) -> list:
    """
    뷰티 관련 콘텐츠만 필터링
    """
    all_beauty_tags = set()
    for category_tags in BEAUTY_HASHTAGS.values():
        all_beauty_tags.update([t.lower() for t in category_tags])
    
    beauty_videos = []
    for video in videos:
        video_tags = set(t.lower() for t in video.hashtags)
        matches = video_tags.intersection(all_beauty_tags)
        
        if len(matches) >= min_hashtag_match:
            video.beauty_category = categorize_beauty_content(matches)
            beauty_videos.append(video)
    
    return beauty_videos

def categorize_beauty_content(matched_tags: set) -> str:
    """세부 카테고리 분류"""
    category_scores = {}
    
    for category, tags in BEAUTY_HASHTAGS.items():
        if category == 'primary':
            continue
        score = len(matched_tags.intersection(set(t.lower() for t in tags)))
        category_scores[category] = score
    
    if max(category_scores.values()) == 0:
        return 'general_beauty'
    
    return max(category_scores, key=category_scores.get)
```

### 4.2 크리에이터 카테고리 기반 필터

```python
class CreatorCategorizer:
    """
    크리에이터 프로필 기반 뷰티 카테고리 분류
    """
    
    BEAUTY_KEYWORDS_BIO = [
        'beauty', 'makeup', 'skincare', 'cosmetics', 'mua',
        '뷰티', '메이크업', '화장', '피부', 'beauty creator',
        'makeup artist', 'skin specialist', 'esthetician'
    ]
    
    def is_beauty_creator(self, creator: dict) -> tuple[bool, float]:
        """
        크리에이터가 뷰티 분야인지 판단
        
        Returns: (is_beauty, confidence)
        """
        signals = []
        
        # Bio 분석
        bio = creator.get('bio', '').lower()
        bio_match = any(kw in bio for kw in self.BEAUTY_KEYWORDS_BIO)
        signals.append(bio_match)
        
        # 최근 콘텐츠 분석 (최근 30개)
        recent_videos = creator.get('recent_videos', [])
        beauty_ratio = sum(
            1 for v in recent_videos 
            if self._is_beauty_content(v)
        ) / max(len(recent_videos), 1)
        signals.append(beauty_ratio > 0.5)
        
        # 팔로잉 분석 (뷰티 브랜드/크리에이터 팔로우)
        following = creator.get('following', [])
        beauty_following = sum(
            1 for f in following 
            if self._is_beauty_account(f)
        ) / max(len(following), 1)
        signals.append(beauty_following > 0.3)
        
        confidence = sum(signals) / len(signals)
        return confidence > 0.5, confidence
    
    def _is_beauty_content(self, video: dict) -> bool:
        tags = video.get('hashtags', [])
        return any(t.lower() in BEAUTY_HASHTAGS['primary'] for t in tags)
```

### 4.3 ML 기반 콘텐츠 분류

```python
from transformers import pipeline

class BeautyContentClassifier:
    """
    비디오 콘텐츠 자체를 분석하여 뷰티 카테고리 분류
    """
    
    def __init__(self):
        # 텍스트 분류
        self.text_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        # 이미지 분류 (썸네일 분석)
        self.image_classifier = pipeline(
            "image-classification",
            model="google/vit-base-patch16-224"
        )
    
    def classify(self, video: dict) -> dict:
        """
        멀티모달 분류
        """
        labels = [
            "skincare tutorial",
            "makeup tutorial",
            "hair styling",
            "nail art",
            "beauty review",
            "beauty haul",
            "not beauty related"
        ]
        
        # 텍스트 분류 (캡션 + 해시태그)
        text = f"{video.get('caption', '')} {' '.join(video.get('hashtags', []))}"
        text_result = self.text_classifier(text, labels)
        
        # 썸네일 분류
        thumbnail = video.get('thumbnail_url')
        if thumbnail:
            image_result = self.image_classifier(thumbnail)
        else:
            image_result = None
        
        # 결과 통합
        return {
            'primary_category': text_result['labels'][0],
            'confidence': text_result['scores'][0],
            'all_scores': dict(zip(text_result['labels'], text_result['scores'])),
            'image_analysis': image_result
        }
```

---

## 5. 통합 구현 예시

### 5.1 Daily Scan Workflow

```python
import asyncio
from datetime import datetime

class BeautyOutlierScanner:
    """
    뷰티 카테고리 바이럴 아웃라이어 일일 스캔
    """
    
    def __init__(self):
        self.pipeline = OutlierDetectionPipeline()
        self.beauty_filter = filter_beauty_content
        self.organic_classifier = OrganicClassifier()
    
    async def run_daily_scan(self):
        """
        일일 스캔 실행
        
        예상 결과:
        - Input: 100,000+ videos from beauty hashtags
        - Stage 1 Output: ~5,000 potential outliers
        - Stage 2 Output: ~500 detailed analysis
        - Final: ~50-100 organic beauty outliers
        """
        
        print(f"[{datetime.now()}] Starting daily beauty outlier scan...")
        
        # 1. 해시태그 기반 수집
        all_beauty_tags = []
        for tags in BEAUTY_HASHTAGS.values():
            all_beauty_tags.extend(tags)
        
        raw_videos = await self.pipeline.stage1_collect(
            hashtags=all_beauty_tags,
            region='KR',
            lookback_hours=24
        )
        print(f"Collected {len(raw_videos)} videos")
        
        # 2. 뷰티 필터
        beauty_videos = self.beauty_filter(raw_videos)
        print(f"Beauty filtered: {len(beauty_videos)}")
        
        # 3. Outlier 필터
        outliers = self.pipeline.filter_outliers(beauty_videos)
        print(f"Potential outliers: {len(outliers)}")
        
        # 4. Stage 2: 상세 데이터 (유료)
        detailed = await self.pipeline.stage2_enrich(outliers)
        
        # 5. 오가닉 필터
        organic_outliers = [
            v for v in detailed
            if self.organic_classifier.predict_organic_probability(v) > 0.7
            and not v.get('is_sponsored', False)
        ]
        
        print(f"Final organic outliers: {len(organic_outliers)}")
        
        # 6. 결과 저장
        self.save_results(organic_outliers)
        
        return organic_outliers
    
    def save_results(self, outliers: list):
        """결과를 DB/파일에 저장"""
        for video in outliers:
            # 필요한 형태로 저장
            result = {
                'video_id': video['id'],
                'platform': video['platform'],
                'viral_multiplier': video['views'] / video['creator_followers'],
                'engagement_rate': video['engagement_rate'],
                'beauty_category': video['beauty_category'],
                'organic_score': video['organic_probability'],
                'creator': video['creator_username'],
                'detected_at': datetime.now().isoformat(),
            }
            # DB insert or file append
```

### 5.2 비용 예측

```
일일 운영 비용 (예상):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stage 1 (무료 API):
  - 100,000 videos × $0.00 = $0.00

Stage 2 (유료 API - 상위 5%만):
  - 5,000 videos × $0.01 = $50.00

인프라:
  - Redis Cache: ~$10/month ÷ 30 = $0.33
  - Compute: ~$30/month ÷ 30 = $1.00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
일일 총 비용: ~$51.33
월간 총 비용: ~$1,540
```

---

## 6. 참고 자료

### 논문
1. "Characterizing and Predicting Viral-and-Popular Video Content" (CIKM 2015)
2. "Counting How the Seconds Count: Algorithm-User Interplay in TikTok" (arXiv 2503.20030)
3. "Slapping Cats, Bopping Heads: Understanding Virality" (arXiv 2111.02452)
4. "InstaSynth: Sponsored Content Detection with LLMs" (ICWSM 2024)

### 도구/서비스
- [Virlo.ai](https://virlo.ai) - 바이럴 아웃라이어 탐지 SaaS
- [TikTok Research API](https://developers.tiktok.com/doc/research-api-specs-query-videos/)
- [EnsembleData](https://ensembledata.com) - TikTok 스크래핑 API
- [Apify TikTok Scraper](https://apify.com/clockworks/tiktok-scraper)

### 벤치마크 데이터
- [Social Insider TikTok Benchmarks 2025](https://www.socialinsider.io/social-media-benchmarks/tiktok)
- [Sprout Social TikTok Stats 2025](https://sproutsocial.com/insights/tiktok-stats/)
