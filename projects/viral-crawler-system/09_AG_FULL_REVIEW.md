# 🔍 AG 전체 리뷰 (2026-01-31)

**리뷰어:** AG (Antigravity)  
**원본:** 테드 전달 (Telegram)

---

## 📊 전체 평가

| 구분 | 점수 | 평가 |
|------|------|------|
| 구조화 | ⭐⭐⭐⭐⭐ | Phase 1-4 발전 단계 논리적 |
| 역할 분배 | ⭐⭐⭐⭐ | OpenClaw/AG 역할 구분 명확 |
| 기술 현실성 | ⭐⭐⭐ | 일부 착각 존재 |
| 2026 최신성 | ⭐⭐ | API/법적 상황 업데이트 필요 |
| 기존 시스템 연계 | ⭐ | ⚠️ Komission 기존 크롤러 미인지 |

---

## 🚨 핵심 발견: 기존 크롤러 이미 존재!

### 실제 기술 스택 (Apify 아님!)

```
실제 운영 스택:
┌─────────────────────────────────────────────────────────┐
│  TikTok 데이터 추출                                      │
│  ├── SocialKitAdapter (api.socialkit.dev)               │
│  │   ├── /tiktok/stats  → 조회수, 좋아요, 댓글수        │
│  │   └── /tiktok/comments → 댓글 목록                   │
│  └── Circuit Breaker + Exponential Backoff               │
├─────────────────────────────────────────────────────────┤
│  비디오 다운로드 (video_downloader.py)                   │
│  ├── TikTok: Playwright → yt-dlp + Residential Proxy    │
│  ├── YouTube: JSON Parsing → yt-dlp + Residential Proxy │
│  └── Instagram: yt-dlp + Residential Proxy              │
├─────────────────────────────────────────────────────────┤
│  Residential Proxy (DataImpulse)                         │
│  ├── TIKTOK_PROXY / YOUTUBE_PROXY 환경변수              │
│  └── 데이터센터 IP 봇 감지 우회                          │
└─────────────────────────────────────────────────────────┘
```

### 기존 구현 현황

| 파일 | 기능 | 상태 |
|------|------|------|
| socialkit_adapter.py | TikTok 데이터 추출 (SocialKit API) | ✅ 운영 중 |
| video_downloader.py | 비디오 다운로드 + Residential Proxy | ✅ 운영 중 |
| youtube.py | YouTube Shorts 크롤러 (Data API v3) | ✅ 운영 중 |
| tiktok.py | TikTok 크롤러 (Apify API) | ⚠️ **미사용 (레거시)** |
| content_filter.py | 콘텐츠 필터링 | ✅ 운영 중 |

---

## 🔴 소미 문서 오류 목록

1. **TikTok API 착각** → SocialKit API 사용 중 (Apify 아님)
2. **Instagram 과소평가** → 2024.12부터 개인 계정 API 완전 차단
3. **Week 1-2 불필요** → 기반 시스템 이미 존재
4. **법적 리스크 누락** → CFAA/ToS 섹션 필요

---

## ⚖️ 법적 고려사항 (2026년)

### 안전한 크롤링 원칙
- ✅ 공개 데이터만 수집
- ✅ robots.txt 존중
- ✅ Rate limit 준수
- ✅ 메타데이터만 저장
- ❌ CAPTCHA 우회 금지
- ⚠️ Residential Proxy = 회색 영역

---

## 🔧 AG 즉시 실행 가능 항목

| 우선순위 | 작업 | 예상 시간 |
|---------|------|----------|
| P0 | 24/7 크롤링 스케줄러 | 1일 |
| P0 | 승격 상태 필드 추가 | 2시간 |
| P1 | 승격 관리 API | 1일 |
| P1 | 테드용 승격 UI | 2일 |
| P2 | 경향성 통계 집계 | 1일 |

---

## 📝 수정된 로드맵

| 주차 | 작업 | 담당 |
|------|------|------|
| Week 1 | 24/7 크롤링 스케줄링 | AG |
| Week 2 | 승격 UI/API 구축 | AG |
| Week 3-4 | 승격 데이터 100건+ 축적 | 소미+테드 |
| Week 5-6 | 패턴 분석 & 규칙 학습 | 소미 |
| Week 7-8 | A/B 테스트 & 자동 승격 | 공동 |
