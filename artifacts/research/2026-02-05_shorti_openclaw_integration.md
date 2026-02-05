# Shorti + OpenClaw 통합 전략

**연구일:** 2026-02-05  
**연구자:** 소미 🐱

---

## 현재 Shorti 시스템 분석

### 아웃라이어 선별 기준 (OutlierSelector)

```python
# Primary platforms (TikTok, Instagram)
primary_view_threshold = 500,000      # 50만 뷰
primary_growth_threshold = 1.2        # 1.2x 성장률

# Secondary platforms (YouTube 등)
secondary_view_threshold = 1,000,000  # 100만 뷰
secondary_growth_threshold = 1.8      # 1.8x 성장률
```

**조건:** (뷰 >= threshold) OR (성장률 >= threshold)

### 파이프라인 흐름

```
[크롤링] 
    → OutlierSource (소스 등록)
    → OutlierItem (후보 저장)
    
[분석]
    → NotebookLibrary (VDG 분석)
    → OutlierSelector (기준 충족 체크)
    
[승격]
    → RemixNode (최종 승격)
    → Scout Bot 알림
    → Human-in-the-loop (promote/skip/tag)
```

---

## 비용 효율적 크롤링 전략

### 문제: SocialKit API 비용
- 마구잡이 크롤링 = 비용 폭발
- 엄선된 후보만 상세 추출 필요

### 해결: 3단계 퍼널

```
┌─────────────────────────────────────────────────────────────┐
│ Stage 1: 무료 Discovery (TikTok-Api / Creative Center)     │
│ - 해시태그별 최신 비디오 목록 (URL만)                       │
│ - 기본 메타데이터 (조회수, 좋아요)                          │
│ - 비용: $0                                                  │
│ - 볼륨: 1000+ 영상/일                                       │
└─────────────────────────────────────────────────────────────┘
                    ↓ 1차 필터 (조회수/성장률)
┌─────────────────────────────────────────────────────────────┐
│ Stage 2: 경량 검증                                          │
│ - TikTok oEmbed API (무료, rate limit 있음)                │
│ - 영상 존재 여부, 기본 정보 확인                            │
│ - 비용: $0                                                  │
│ - 볼륨: ~100 영상/일                                        │
└─────────────────────────────────────────────────────────────┘
                    ↓ 2차 필터 (아웃라이어 조건)
┌─────────────────────────────────────────────────────────────┐
│ Stage 3: SocialKit 상세 추출                                │
│ - 트랜스크립트, 댓글, 상세 메타데이터                       │
│ - VDG 분석용 데이터                                         │
│ - 비용: ~$0.01/영상 (SocialKit 크레딧)                      │
│ - 볼륨: ~20 영상/일                                         │
└─────────────────────────────────────────────────────────────┘
                    ↓ VDG 분석 & Scout Bot
┌─────────────────────────────────────────────────────────────┐
│ Stage 4: Human-in-the-loop                                  │
│ - Scout Bot 알림                                            │
│ - promote/skip/client-tag 결정                              │
│ - 볼륨: ~5-10 영상/일                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 뷰티 필터링 전략

### 해시태그 기반 (1차)

```python
BEAUTY_HASHTAGS = [
    # K-Beauty
    "kbeauty", "koreanbeauty", "koreanskincare",
    "glassskin", "koreanmakeup",
    
    # Skincare
    "skincare", "skincareRoutine", "skincaretips",
    "moisturizer", "serum", "sunscreen",
    
    # Makeup
    "makeup", "makeuptutorial", "grwm",
    "foundation", "lipstick", "eyeshadow",
    
    # Trends
    "beautytok", "beautyhacks", "viralbeauty",
    "tiktokmademebuyit",
]
```

### 키워드 기반 (2차)

```python
BEAUTY_KEYWORDS = [
    # 제품 타입
    "moisturizer", "serum", "toner", "cleanser",
    "foundation", "concealer", "mascara",
    
    # 브랜드 (타겟 클라이언트)
    "cerave", "laneige", "cosrx", "innisfree",
    "maybelline", "loreal", "nyx",
    
    # 액션
    "skincare routine", "makeup tutorial",
    "get ready with me", "review",
]
```

### 오가닉 vs 광고 판별

```python
AD_INDICATORS = [
    "#ad", "#sponsored", "#gifted", "#pr",
    "partnership", "collab with",
    "link in bio", "use code",
]

def is_organic(caption: str, comments: list) -> bool:
    caption_lower = caption.lower()
    
    # 광고 표시 체크
    for indicator in AD_INDICATORS:
        if indicator in caption_lower:
            return False
    
    # 댓글 패턴 분석 (진짜 engagement vs 봇)
    # ... sentiment analysis
    
    return True
```

---

## OpenClaw 역할

### 자동화 가능한 것
1. **웹서칭 연구** - 트렌드 분석, 경쟁사 모니터링
2. **문서 생성** - 클라이언트 리포트, 패턴 분석
3. **코드 리뷰** - 크롤러/분석기 개선 제안

### Human-in-the-loop 지원
1. **Scout Bot 알림 보강** - 컨텍스트 추가
2. **클라이언트 매칭** - "이 패턴은 로레알에 적합" 판단
3. **인사이트 생성** - "이 영상이 바이럴된 이유"

### 활용 예시

```
[Scout Bot 알림]
🎯 새 아웃라이어: "Glass Skin Tutorial"
- 조회수: 2.3M (평균 대비 15x)
- 해시태그: #glassskin #kbeauty
- 오가닉: ✅

[소미 분석 추가]
💡 인사이트:
- 패턴: #before-after + #tutorial
- 클라이언트 적합: 라네즈, 설화수 (glass skin = K-뷰티 핵심)
- 추천 액션: 로레알 Active 디비전에도 공유 (La Roche-Posay)
```

---

## 구현 로드맵

### Phase 1: 수동 + SocialKit (지금)
- Creative Center에서 수동 URL 입력
- SocialKit으로 enrichment
- Scout Bot 알림

### Phase 2: TikTok-Api 자동화 (1주)
- 해시태그 크롤러 구현
- 1차 필터 자동화
- Celery task 스케줄링

### Phase 3: 풀 파이프라인 (2주)
- 3단계 퍼널 완성
- 오가닉 판별 로직
- OpenClaw 인사이트 통합

### Phase 4: AI 자동 매칭 (향후)
- 패턴 → 클라이언트 자동 매칭
- 예측 모델 (어떤 패턴이 뜰지)
- 자동 리포트 생성

---

## 예상 비용

| 단계 | 볼륨/일 | 비용/일 |
|------|---------|---------|
| Discovery | 1000+ | $0 |
| 검증 | 100 | $0 |
| SocialKit | 20 | ~$0.20 |
| VDG 분석 | 20 | (자체) |
| **합계** | - | **~$6/월** |

---

*Claude Code한테: 이 전략대로 TikTok-Api 크롤러 구현해*
