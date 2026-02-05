# TikTok Crawler 병렬 리서치 🔍

*2026-02-05 by 소미 🐱*

---

## 1. 키워드 확장 제안 (8개 → 15개)

### 현재 설정된 키워드
```python
BEAUTY_KEYWORDS = [
    "kbeauty", "skincare", "glassskin", "makeup", 
    "koreanmakeup", "skincareroutine", "beautytok", "grwm"
]
```

### 추가 추천 키워드
| 키워드 | 근거 |
|--------|------|
| `#KoreanSkincare` | Q3 97% 성장, 740K+ 신규 영상 (BeautyMatter) |
| `#CleanBeauty` | 지속적인 클린뷰티 트렌드 |
| `#MakeupTransformation` | 바이럴 Before/After 포맷 핵심 |
| `#SoftGlam` | 2025-2026 메이크업 대세 |
| `#CleanGirlMakeup` | 미니멀 뷰티 트렌드 |
| `#MakeupHack` | 팁/핵 콘텐츠 고engagement |
| `#BeautyRoutine` | 루틴 콘텐츠 검색량 높음 |

### 제안: 2티어 키워드 시스템
```python
# 1티어: 매 크롤링마다 (핵심)
TIER1_KEYWORDS = [
    "kbeauty", "koreanmakeup", "glassskin", "grwm",
    "skincareroutine", "koreanskincare"
]

# 2티어: 로테이션 (하루 2개씩)
TIER2_KEYWORDS = [
    "cleanbeauty", "makeuptransformation", "softglam",
    "cleangirl", "makeuphack", "beautyroutine",
    "skintok", "dewyskin"
]
```

---

## 2. TikTok 알고리즘 인사이트 2026

### 바이럴 핵심 요소
| 요소 | 설명 | 적용 |
|------|------|------|
| **Engagement Velocity** | 첫 30-60분 engagement가 바이럴 결정 | 초기 engagement 높은 영상 우선 수집 |
| **Watch Time** | 완주율 높을수록 추천 | 영상 길이 대비 조회수 비율 체크 |
| **Positive Sentiment** | 긍정/재미있는 콘텐츠 선호 (Semrush) | 댓글 sentiment 분석 고려 |
| **Niche Focus** | 단일 니치 집중 크리에이터 성장 빠름 | 뷰티 전문 크리에이터 우선 |

### 바이럴 콘텐츠 포맷 (뷰티 특화)
1. **GRWM (Get Ready With Me)** - 가장 인기
2. **Before/After Transformation** - 고engagement
3. **5-minute Quick Routine** - 접근성
4. **Product Demo/Review** - 구매 전환
5. **Skincare Routine Reveal** - 루틴 공개

### Traackr 2026 리포트 핵심
> "Smaller creators, routine-led demos, TikTok-native organic content가 paid scale보다 강한 engagement"

**시사점:** 대형 인플루언서보다 마이크로 크리에이터의 organic 콘텐츠가 더 효과적

---

## 3. 경쟁 도구 분석

| 서비스 | 특징 | 가격 | 우리 대안 |
|--------|------|------|----------|
| **Virlo** | AI 기반 바이럴 분석, 21.3K+ 크리에이터 | 유료 구독 | ❌ 만료됨 |
| **TikTok Creative Center** | 공식 트렌드 데이터 | 무료 | ✅ 해시태그 참고 |
| **Syncly** | Trend Discovery, Breakout Creators | 유료 | - |
| **Upfluence** | 멀티플랫폼 크리에이터 발굴 | $1.5-3K/월 | - |
| **Grin** | 버티컬별 발굴 (뷰티 특화) | 유료 | - |
| **SocialKit** | 검색 기반 영상 수집 | 크레딧 기반 | ✅ 현재 구현 |

### 우리 솔루션의 강점
- SocialKit: 저비용 (1크레딧/20영상)
- 자체 필터링: 50만+ 조회수 기준
- OutlierItem 저장: 개별 영상 URL 확보
- Scout Bot 연동: 텔레그램 알림

---

## 4. Scout Bot 알림 포맷 제안

### 현재 (추정)
```
새로운 아웃라이어 발견!
영상 URL: ...
조회수: ...
```

### 개선안
```
🔥 K-Beauty 아웃라이어 발견!

📊 @{username}
├ 조회수: {views:,} ({tier} 티어)
├ 좋아요: {likes:,} ({engagement_rate}%)
├ 키워드: #{keyword}
└ 발견: {discovered_at}

🔗 {video_url}

━━━━━━━━━━━━━━━
💡 왜 주목?
• {engagement_rate}% engagement (평균 대비 +{delta}%)
• {keyword} 카테고리 {rank}위
━━━━━━━━━━━━━━━
```

### 티어별 이모지
- SS (100M+): 🏆
- S (50M+): 🔥
- A (10M+): ⭐
- B (1M+): 📈

---

## 5. 추가 기능 제안

### 5.1 Engagement Rate 계산
```python
engagement_rate = (likes + comments + shares) / views * 100
```
- 뷰티 평균: 3-5%
- 바이럴급: 10%+

### 5.2 크리에이터 프로필 저장
```python
class CreatorProfile:
    username: str
    follower_count: int
    avg_views: int
    engagement_rate: float
    top_hashtags: list[str]
    discovered_videos: list[str]
```

### 5.3 트렌드 감지
- 동일 키워드에서 갑자기 조회수 급등 감지
- 새로운 바이럴 해시태그 자동 발견

---

## 6. 다음 액션 아이템

- [ ] 키워드 15개로 확장 (Claude Code에 전달)
- [ ] Engagement rate 필터 추가 (5%+ 기준)
- [ ] Scout Bot 알림 포맷 업그레이드
- [ ] 크리에이터 프로필 DB 스키마 설계
- [ ] 2티어 키워드 로테이션 로직

---

*Source: Brave Search, BeautyMatter, TikTok Creative Center, Traackr 2026 Report*
