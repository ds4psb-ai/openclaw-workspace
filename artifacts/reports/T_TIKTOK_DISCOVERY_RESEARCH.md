# TikTok Discovery 대안 리서치 리포트

**작성일:** 2026-02-05 11:15 KST  
**작성자:** 소미 🐱  
**목적:** Virlo 구독 종료 후 TikTok 바이럴 콘텐츠 Discovery 대안 탐색

---

## 📊 현재 상황

### 기존 인프라 (Vivid)
- `virlo_scraper.py` → Discovery (Virlo API 의존) ❌ 구독 종료
- `tiktok_extractor.py` → Enrichment (URL → 메타데이터) ✅ 동작
- `OutlierItem` → DB 모델 ✅

### 문제점
- Virlo 유료 구독 종료 → Discovery 불가
- TikTok-Api 세션 문제 (ms_token 필요)
- 수동 입력은 비효율적

---

## 🔍 발견한 대안들

### 1. TikTok Creative Center 직접 스크래핑 ⭐ 추천
- **URL:** https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en
- **데이터:** 트렌딩 해시태그, 음악, 크리에이터, 비디오
- **비용:** 무료 (공개 페이지)
- **방법:** Playwright/Puppeteer로 스크래핑 또는 내부 API 호출
- **장점:** 
  - 로그인 불필요
  - 국가/산업별 필터 가능
  - 실시간 트렌딩 데이터
- **단점:** TikTok 측 차단 가능성, 구현 필요

### 2. Apify TikTok Trends Scraper
- **URL:** https://apify.com/clockworks/tiktok-trends-scraper
- **비용:** $5/월 → ~800 결과
- **데이터:** Creative Center 스크래핑 (해시태그, 음악, 크리에이터, 비디오)
- **API:** REST API 제공, Python/Node SDK
- **장점:** 바로 사용 가능, API 안정적
- **단점:** 유료

### 3. ScrapeCreators TikTok API
- **URL:** https://scrapecreators.com/tiktok-api
- **비용:** 100 콜 무료, 이후 유료
- **엔드포인트:**
  - `GET /v1/tiktok/popular/hashtags` - 트렌딩 해시태그
  - `GET /v1/tiktok/popular/videos` - 인기 비디오
  - `GET /v1/tiktok/trending` - 트렌딩 피드
- **장점:** 간단한 REST API, Creative Center 데이터
- **단점:** 유료 (대량 사용 시)

### 4. bellingcat/tiktok-hashtag-analysis (오픈소스)
- **URL:** https://github.com/bellingcat/tiktok-hashtag-analysis
- **비용:** 무료
- **설치:** `pip install tiktok-hashtag-analysis`
- **명령:** `tiktok-hashtag-analysis kbeauty skincare --download`
- **장점:** 무료, 해시태그 분석 기능
- **단점:** TikTokApi 의존 (세션 문제 가능)

### 5. drawrowfly/tiktok-scraper (NPM)
- **URL:** https://github.com/drawrowfly/tiktok-scraper
- **비용:** 무료
- **설치:** `npm i -g tiktok-scraper`
- **명령:** `tiktok-scraper trend -n 100 --session sid_tt=...`
- **장점:** 트렌드, 해시태그, 유저 스크래핑
- **단점:** 세션 쿠키 필요할 수 있음

### 6. ScrapFly TikTok Scraper (오픈소스 + 유료 API)
- **URL:** https://github.com/scrapfly/scrapfly-scrapers/tree/main/tiktok-scraper
- **비용:** 무료 (오픈소스) / 유료 (API)
- **기술:** 숨겨진 JSON 데이터 추출 (`__UNIVERSAL_DATA` script 태그)
- **장점:** 잘 문서화됨, 프로덕션 레디
- **단점:** 풀 기능은 ScrapFly API 필요

---

## 💡 추천 구현 방안

### Phase 1: 즉시 적용 (무료)
**TikTok Creative Center 직접 스크래핑**

```python
# /vivid/backend/app/services/creative_center_scraper.py

import httpx
from playwright.async_api import async_playwright

async def fetch_trending_hashtags(country: str = "US", industry: str = None):
    """TikTok Creative Center에서 트렌딩 해시태그 가져오기"""
    url = f"https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        # 해시태그 데이터 추출
        hashtags = await page.evaluate('''
            () => {
                const items = document.querySelectorAll('[class*="hashtag"]');
                return Array.from(items).map(item => ({
                    name: item.textContent,
                    rank: item.dataset.rank
                }));
            }
        ''')
        
        await browser.close()
        return hashtags
```

### Phase 2: 안정화 (저비용)
**Apify 또는 ScrapeCreators API 연동**

```python
# Apify 연동 예시
import requests

def fetch_trending_via_apify(api_token: str):
    """Apify TikTok Trends Scraper 실행"""
    run_input = {
        "hashtags": True,
        "videos": True,
        "maxResults": 100,
        "countryCode": "US"
    }
    
    response = requests.post(
        "https://api.apify.com/v2/acts/clockworks~tiktok-trends-scraper/runs",
        headers={"Authorization": f"Bearer {api_token}"},
        json={"runInput": run_input}
    )
    return response.json()
```

### Phase 3: 파이프라인 통합
**기존 OutlierItem 파이프라인 연결**

```
Creative Center Scraper
    ↓
500K+ Views 필터
    ↓
OutlierItem 생성
    ↓
VDG Extractor (메타데이터 보강)
    ↓
Scout Bot → Telegram 알림
```

---

## 🎯 권장 액션

### 당장 (오늘)
1. ✅ Creative Center 스크래핑 스크립트 작성
2. ✅ 기존 OutlierItem 파이프라인에 연결
3. ✅ Celery Beat 스케줄 등록 (6시간마다)

### 이번 주
1. ScrapeCreators 무료 100콜로 테스트
2. 안정성 비교 후 최적 솔루션 선택
3. 모니터링 및 알림 설정

### 장기
1. 여러 소스 결합 (Creative Center + 해시태그 검색)
2. 자체 ML 모델로 아웃라이어 예측
3. 실시간 트렌드 감지

---

## 📈 비용 비교

| 솔루션 | 월 비용 | 데이터량 | 안정성 |
|--------|---------|----------|--------|
| Creative Center 직접 | $0 | 무제한 | ⚠️ 중간 |
| Apify | $5~ | ~800/월 | ✅ 높음 |
| ScrapeCreators | $0~$29 | 100 무료 | ✅ 높음 |
| bellingcat | $0 | 무제한 | ⚠️ 중간 |
| ScrapFly | $0~$49 | 가변 | ✅ 높음 |

---

## 🔗 참고 링크

- [TikTok Creative Center](https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en)
- [Apify TikTok Trends Scraper](https://apify.com/clockworks/tiktok-trends-scraper)
- [ScrapeCreators TikTok API](https://scrapecreators.com/tiktok-api)
- [bellingcat/tiktok-hashtag-analysis](https://github.com/bellingcat/tiktok-hashtag-analysis)
- [drawrowfly/tiktok-scraper](https://github.com/drawrowfly/tiktok-scraper)
- [ScrapFly TikTok Scraper](https://github.com/scrapfly/scrapfly-scrapers/tree/main/tiktok-scraper)

---

## ✅ 구현 완료 (2026-02-05)

### 생성된 파일

1. **`/vivid/backend/app/services/creative_center_scraper.py`**
   - `CreativeCenterScraper` 클래스
   - `fetch_trending_hashtags()` - 트렌딩 해시태그 가져오기
   - `fetch_trending_videos()` - 트렌딩 비디오 가져오기
   - `fetch_hashtag_details()` - 해시태그 상세 정보 (오디언스, 관련 해시태그 등)
   - `discover_beauty_hashtags()` - K-Beauty 해시태그 BFS 발굴

2. **`/vivid/backend/app/jobs/crawl_tiktok_trends.py`**
   - `crawl_tiktok_trends()` - Arq 크론 잡
   - K-Beauty 시드 해시태그 → 관련 해시태그 확장
   - OutlierItem 자동 생성
   - Telegram 알림 (TODO: 실제 연동)

### 테스트 결과

```
#kbeauty
  7일 조회수: 76,800,882
  전체 조회수: 69,587,934,144
  카테고리: Beauty & Personal Care
  관련 해시태그:
    - #koreanskincare
    - #yesstyle
    - #kbeautyskincare
    - #koreanmakeup
    - #yesstyleinfluencers
```

### 남은 작업

1. [ ] `worker.py`에 `crawl_tiktok_trends` 등록
2. [ ] Telegram Scout Bot 실제 연동
3. [ ] Railway 배포 테스트
4. [ ] 모니터링 대시보드 연결

---

*구현: 소미 🐱 | 2026-02-05 11:25 KST*
