# TikTok 바이럴 URL 발굴 (Discovery) 방법 연구

**연구일:** 2026-02-05  
**연구자:** 소미 🐱

---

## 문제 정의

| 용도 | YouTube | TikTok |
|------|---------|--------|
| **발굴 (Discovery)** | ✅ YouTube API | ❌ 없음 |
| **추출 (Enrichment)** | ✅ YouTube API | ✅ SocialKit |

**필요한 것:** TikTok 바이럴/트렌딩 URL 자동 발굴

---

## 옵션 분석

### 1. 🌟 TikTok Creative Center (추천!)

**URL:** https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en

**제공 데이터:**
- 트렌딩 해시태그
- 인기 비디오 (국가별)
- 트렌딩 사운드
- 인기 크리에이터

**장점:**
- ✅ **무료**
- ✅ 공식 TikTok 제공
- ✅ 국가/카테고리 필터
- ✅ 실시간 트렌드

**단점:**
- ❌ 공식 API 없음 (웹 스크래핑 필요)
- ❌ 로그인 필요할 수 있음

**구현 방법:**
```python
# Playwright/Puppeteer로 Creative Center 스크래핑
# 또는 API 엔드포인트 리버스 엔지니어링
```

---

### 2. TikTok-Api (Python 비공식 라이브러리)

**GitHub:** https://github.com/davidteather/TikTok-Api

**기능:**
- 트렌딩 비디오 가져오기
- 해시태그별 비디오 검색
- 사운드별 비디오 검색
- 사용자 비디오 가져오기

**장점:**
- ✅ 무료 오픈소스
- ✅ Python 라이브러리
- ✅ 많이 사용됨 (검증됨)

**단점:**
- ❌ 비공식 (TikTok 정책 변경시 깨질 수 있음)
- ❌ 설정 복잡 (playwright 의존)
- ❌ Rate limiting

**구현:**
```python
from TikTokApi import TikTokApi

async with TikTokApi() as api:
    # 트렌딩 비디오
    trending = await api.trending.videos(count=30)
    
    # 해시태그 검색
    hashtag = api.hashtag(name="kbeauty")
    videos = await hashtag.videos(count=30)
```

---

### 3. 공식 TikTok API (Research API)

**URL:** https://developers.tiktok.com/

**장점:**
- ✅ 공식 지원
- ✅ 안정적

**단점:**
- ❌ 승인 필요 (Research API는 학술/비영리만)
- ❌ 상업용은 제한적
- ❌ Rate limit: 1000 calls/hour

**결론:** 상업용으로는 적합하지 않음

---

### 4. Apify TikTok Scrapers

**URL:** https://apify.com/novi/tiktok-trend-api

**기능:**
- 트렌딩 비디오 추출
- 워터마크 없는 다운로드
- 지역별 필터

**가격:**
- $49/월 (Starter) ~ $499/월 (Business)

**장점:**
- ✅ 안정적
- ✅ 유지보수 불필요

**단점:**
- ❌ 유료

---

### 5. 수동 + 반자동 하이브리드

**방법:**
1. TikTok Creative Center 매일 체크
2. 뷰티 관련 트렌딩 URL 수동 입력
3. SocialKit으로 메타데이터 자동 추출

**장점:**
- ✅ 비용 없음
- ✅ 큐레이션 품질 높음 (사람이 선별)

**단점:**
- ❌ 노동집약적
- ❌ 확장성 낮음

---

## 🎯 추천 전략

### Phase 1: 빠른 시작 (지금)
```
[TikTok Creative Center] 
    → 수동 URL 입력 (ops/outlier)
    → SocialKit enrichment
    → Scout Bot 알림
```

### Phase 2: 반자동화 (1-2주 내)
```
[TikTok-Api 라이브러리]
    → #kbeauty, #skincare 등 해시태그 크롤링
    → 자동 outlier 등록
    → SocialKit enrichment
```

### Phase 3: 풀 자동화 (향후)
```
[TikTok Creative Center 스크래핑]
    → 트렌딩 비디오 자동 수집
    → 뷰티 카테고리 필터
    → VDG 분석
    → Scout Bot
```

---

## 구현 우선순위

| 우선순위 | 작업 | 난이도 | 효과 |
|---------|------|--------|------|
| 1 | 수동 입력 + SocialKit | ⭐ | ⭐⭐⭐ |
| 2 | TikTok-Api 해시태그 크롤러 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 3 | Creative Center 스크래핑 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 결론

**지금 당장:** 수동 입력 + SocialKit (이미 가능)

**다음 단계:** TikTok-Api로 #kbeauty 등 해시태그 자동 크롤링

**장기:** Creative Center 스크래핑 자동화

---

*Claude Code한테: TikTok-Api 라이브러리로 해시태그 크롤러 만들어*
