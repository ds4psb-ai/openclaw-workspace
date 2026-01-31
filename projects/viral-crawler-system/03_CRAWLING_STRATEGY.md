# 03. 크롤링 전략

## 🎯 타겟 플랫폼

### 1순위: TikTok
- 가장 활발한 숏폼 플랫폼
- 트렌드 발생지
- API 제한 있음 → 스크래핑 병행 필요

### 2순위: YouTube Shorts
- API 상대적으로 안정
- 크리에이터 데이터 풍부
- 긴 영상과의 관계 분석 가능

### 3순위: Instagram Reels
- API 제한 심함
- TikTok 리포스트 많음
- 선택적 수집

---

## 📊 수집 데이터

### 필수
| 항목 | 설명 |
|------|------|
| video_id | 고유 식별자 |
| platform | tiktok / youtube / instagram |
| url | 원본 링크 |
| title | 제목 |
| description | 설명 |
| hashtags | 해시태그 목록 |
| creator_id | 크리에이터 ID |
| creator_name | 크리에이터 이름 |
| view_count | 조회수 |
| like_count | 좋아요 수 |
| comment_count | 댓글 수 |
| share_count | 공유 수 |
| created_at | 게시 시간 |
| crawled_at | 크롤링 시간 |

### 선택 (추후)
- 썸네일 이미지
- 영상 길이
- 음악/사운드 정보
- 자막/텍스트

---

## ⏰ 크롤링 스케줄

### OpenClaw cron 설정 (제안)

```
# 매 2시간: 트렌딩 크롤링
0 */2 * * * trending_crawl

# 매 6시간: 특정 해시태그 크롤링
0 */6 * * * hashtag_crawl

# 매일 02:00 UTC: 전일 통계 집계
0 2 * * * daily_stats

# 매일 04:00 UTC: 중복 제거 및 정리
0 4 * * * cleanup
```

---

## 🔍 발견 전략

### 1. 트렌딩 기반
- 각 플랫폼 트렌딩 페이지
- 빠르게 성장하는 영상 감지

### 2. 해시태그 기반
- 타겟 해시태그 목록 관리
- 새 해시태그 자동 발견

### 3. 크리에이터 기반
- 주목할 크리에이터 리스트
- 새 영상 모니터링

### 4. 연관 영상 기반
- 승격된 영상과 유사한 영상
- 알고리즘 추천 따라가기

---

## ⚠️ 제한 및 대응

### Rate Limiting
- 요청 간격 조절 (최소 1-2초)
- IP 로테이션 (필요시)
- 실패 시 exponential backoff

### 차단 대응
- User-Agent 로테이션
- 헤드리스 브라우저 사용
- 프록시 풀 관리

### 데이터 정책
- 메타데이터만 저장 (영상 파일 X)
- 개인정보 최소화
- 삭제된 영상 처리

---

## 📦 출력 형식

```json
{
  "video_id": "7234567890123456789",
  "platform": "tiktok",
  "url": "https://tiktok.com/@user/video/7234567890123456789",
  "title": "영상 제목",
  "hashtags": ["#trending", "#viral"],
  "creator": {
    "id": "user123",
    "name": "크리에이터명",
    "followers": 100000
  },
  "metrics": {
    "views": 1000000,
    "likes": 50000,
    "comments": 1000,
    "shares": 5000
  },
  "crawled_at": "2026-01-31T06:30:00Z"
}
```
