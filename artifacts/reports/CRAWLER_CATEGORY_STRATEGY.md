# 🎯 TikTok Crawler 카테고리 전략 연구

*2026-02-05 by 소미 🐱*

---

## 1. 카테고리 분리: 뷰티 vs 밈

### 현재 문제점
- 모든 키워드가 뷰티에 집중됨
- 밈/코미디 콘텐츠 놓치고 있음
- 카테고리별 필터링 기준 없음

### 제안: 2트랙 크롤링

```
┌─────────────────────────────────────────────────────────┐
│                    TikTok Crawler                        │
├────────────────────────┬────────────────────────────────┤
│      🧴 BEAUTY         │         😂 MEME/COMEDY         │
├────────────────────────┼────────────────────────────────┤
│ 목적: 제품/브랜드 발굴  │ 목적: 바이럴 포맷 발굴         │
│ 활용: 클라이언트 리포트 │ 활용: 크리에이티브 레퍼런스    │
│ KPI: 브랜드 언급, 구매↑ │ KPI: 공유율, 리텐션            │
└────────────────────────┴────────────────────────────────┘
```

---

## 2. 키워드 세분화

### 🧴 BEAUTY 키워드 (현재 8개 → 15개)

#### Tier 1: K-Beauty 핵심 (매 크롤링)
```python
BEAUTY_TIER1 = [
    "kbeauty",
    "koreanskincare", 
    "koreanmakeup",
    "glassskin",
    "skincareroutine",
    "grwm",
]
```

#### Tier 2: 확장 (로테이션)
```python
BEAUTY_TIER2 = [
    "skintok",
    "makeuptutorial",
    "skincaretips",
    "beautyhacks",
    "cleanbeauty",
    "dewyskin",
    "douyin skincare",  # 중국 트렌드
    "올리브영",         # 한국어 검색
    "한국화장품",
]
```

### 😂 MEME/COMEDY 키워드 (신규)

#### Tier 1: 코미디 핵심
```python
MEME_TIER1 = [
    "funny",
    "comedy",
    "meme",
    "relatable",
    "humor",
    "skit",
]
```

#### Tier 2: 트렌드 기반
```python
MEME_TIER2 = [
    "trending",
    "viral",
    "funnyvideos",
    "comedygold",
    "relatablehumor",
    "tiktokcomedy",
    "POV",           # POV 스킷
    "storytime",     # 스토리텔링
]
```

---

## 3. 필터링 기준 차별화

### 🧴 BEAUTY 필터
| 기준 | 값 | 이유 |
|------|-----|------|
| 최소 조회수 | 500K | 브랜드 관심 기준 |
| Engagement Rate | 3%+ | Beauty 평균 3.9% |
| 우선순위 | 브랜드 언급 | 클라이언트 리포트용 |

```python
def filter_beauty(item):
    return (
        item["view_count"] >= 500_000 and
        item["engagement_rate"] >= 0.03 and
        # 보너스: K-Beauty 브랜드 언급 시 우선
        has_brand_mention(item["title"], KBEAUTY_BRANDS)
    )
```

### 😂 MEME 필터
| 기준 | 값 | 이유 |
|------|-----|------|
| 최소 조회수 | 1M | 밈은 조회수 높음 |
| 공유율 | 5%+ | 바이럴 지표 |
| 리텐션 | 완주율 높은 것 | 포맷 퀄리티 |

```python
def filter_meme(item):
    share_rate = item["share_count"] / item["view_count"]
    return (
        item["view_count"] >= 1_000_000 and
        share_rate >= 0.05
    )
```

---

## 4. 티어 기준 재정의

### BEAUTY 티어 (현재)
| 티어 | 조회수 | 비고 |
|------|--------|------|
| SS | 5M+ | 메가 바이럴 |
| S | 1M+ | 아웃라이어 |
| A | 500K+ | 잠재력 |
| B | 100K+ | 모니터링 |

### MEME 티어 (제안)
| 티어 | 조회수 | 공유율 | 비고 |
|------|--------|--------|------|
| SS | 20M+ | 10%+ | 밈 레전드 |
| S | 5M+ | 7%+ | 바이럴 |
| A | 1M+ | 5%+ | 확산 중 |
| B | 500K+ | 3%+ | 모니터링 |

**이유:** 밈은 뷰티보다 조회수 베이스가 높음 (엔터테인먼트 특성)

---

## 5. 데이터 스키마 확장

### OutlierItem 확장 필드 (제안)
```python
class OutlierItem:
    # 기존 필드...
    
    # 신규 필드
    content_category: str  # "beauty" | "meme" | "lifestyle" | "tech"
    share_rate: float      # share_count / view_count
    brand_mentions: list   # ["SKIN1004", "ANUA", ...]
    meme_format: str       # "POV" | "storytime" | "skit" | "challenge"
    is_trending: bool      # 트렌딩 여부
```

### OutlierSource 분리
```
- tiktok_socialkit_beauty   # 뷰티 전용
- tiktok_socialkit_meme     # 밈 전용
- tiktok_socialkit_general  # 일반
```

---

## 6. 크롤링 스케줄 분리

```python
beat_schedule = {
    # 뷰티: 6시간마다
    "crawler-socialkit-beauty": {
        "task": "crawl_socialkit",
        "schedule": crontab(minute=0, hour="*/6"),
        "kwargs": {
            "category": "beauty",
            "keywords": BEAUTY_TIER1 + rotate(BEAUTY_TIER2),
            "min_views": 500_000,
        },
    },
    
    # 밈: 4시간마다 (트렌드 변화 빠름)
    "crawler-socialkit-meme": {
        "task": "crawl_socialkit",
        "schedule": crontab(minute=30, hour="*/4"),
        "kwargs": {
            "category": "meme",
            "keywords": MEME_TIER1 + rotate(MEME_TIER2),
            "min_views": 1_000_000,
        },
    },
}
```

---

## 7. Scout Bot 알림 분리

### BEAUTY 알림
```
🧴 K-Beauty 아웃라이어!

@{username} | {views} 뷰 | {tier}
브랜드 언급: {brands}
카테고리: {category}

{video_url}
```

### MEME 알림
```
😂 Meme 바이럴!

@{username} | {views} 뷰 | {tier}
포맷: {meme_format}
공유율: {share_rate}%

{video_url}
```

---

## 8. 액션 아이템

### 즉시 (Phase 1)
- [ ] OutlierSource 분리: `tiktok_socialkit_beauty`, `tiktok_socialkit_meme`
- [ ] 키워드 세트 분리
- [ ] 필터링 기준 분기 처리

### 다음 (Phase 2)
- [ ] `content_category` 필드 추가
- [ ] `share_rate` 계산 로직
- [ ] Scout Bot 알림 분기

### 나중 (Phase 3)
- [ ] 브랜드 언급 자동 감지
- [ ] 밈 포맷 분류 (AI)
- [ ] 트렌드 감지 알림

---

## 9. 예상 결과

| 지표 | 현재 | 개선 후 |
|------|------|---------|
| 수집 카테고리 | 1개 (뷰티) | 2개 (뷰티+밈) |
| 키워드 수 | 8개 | 24개 |
| 아웃라이어 발견율 | - | +50% (예상) |
| 클라이언트 활용도 | 낮음 | 높음 |

---

## 10. K-Beauty 브랜드 리스트 (참고)

```python
KBEAUTY_BRANDS = [
    # 스킨케어
    "SKIN1004", "ANUA", "Beauty of Joseon", "COSRX",
    "Innisfree", "Laneige", "Sulwhasoo", "Dr.Jart+",
    
    # 메이크업
    "rom&nd", "Peripera", "CLIO", "3CE", "TIRTIR",
    
    # 디바이스
    "Medicube", "Foreo",
    
    # 편집샵
    "올리브영", "Olive Young",
]
```

---

*다음 단계: 테드 피드백 후 구현 시작*
