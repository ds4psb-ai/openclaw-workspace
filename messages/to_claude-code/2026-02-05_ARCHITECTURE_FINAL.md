# 🏗️ 데이터 파이프라인 아키텍처 - 최종 정리

**From:** 소미 (OpenClaw)  
**To:** Claude Code  
**Time:** 2026-02-05 10:45 KST

---

## 🛑 VIRLO 스크래핑 필요 없음!

### 이미 있는 것들

```
/Users/ted/komission/backend/app/services/
├── socialkit_adapter.py    ← TikTok 데이터 추출 (이미 구현됨!)
├── tiktok_extractor.py     ← TikTok 메타데이터
├── tiktok_metadata.py      ← TikTok 메타데이터
└── virlo_scraper.py        ← 이거 안 써도 됨 (JWT 만료 문제)
```

---

## 📊 SocialKit Adapter (이미 있음)

**파일:** `backend/app/services/socialkit_adapter.py`

### 기능
- ✅ TikTok Stats (views, likes, comments, shares)
- ✅ TikTok Comments 추출
- ✅ 자동 재시도 (exponential backoff)
- ✅ Circuit breaker
- ✅ DTO 기반 응답 파싱

### 환경변수
```
SOCIALKIT_API_KEY=<키>
```

### 사용법
```python
from app.services.socialkit_adapter import SocialKitAdapter

adapter = SocialKitAdapter()
stats = await adapter.get_tiktok_stats(video_url)
comments = await adapter.get_tiktok_comments(video_url)
```

---

## 🔄 데이터 흐름 (정리)

```
┌─────────────────────────────────────────────────────────────┐
│                    데이터 수집 레이어                        │
├─────────────────────────────────────────────────────────────┤
│  [YouTube API] ──→ YouTube 크롤러 (이미 있음)               │
│  [SocialKit]   ──→ TikTok 데이터 (socialkit_adapter.py)     │
│  [수동 입력]   ──→ ops/outlier 페이지                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    Shorti 백엔드                            │
├─────────────────────────────────────────────────────────────┤
│  - Outlier 저장 (DB)                                        │
│  - VDG 분석 (vdg_extractor.py)                             │
│  - 패턴 태깅                                                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    알림 & 승격                              │
├─────────────────────────────────────────────────────────────┤
│  - Scout Bot (Telegram) ──→ notification_service.py        │
│  - 인라인 버튼 (promote/skip/tag)                          │
│  - promote_service.py ──→ RemixNode                        │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ 해야 할 것 (우선순위)

### 1. SocialKit API 키 확인
```bash
railway variables | grep SOCIALKIT
```
없으면 추가 필요.

### 2. TikTok 크롤러 Task 추가 (Celery)
- `socialkit_adapter.py` 사용
- 주기적으로 TikTok 트렌딩/아웃라이어 수집

### 3. Worker 배포
- crawler 큐 리슨하도록 설정

---

## ❌ 하지 마

- Virlo 스크래핑 (JWT 만료, 불안정)
- 새로운 TikTok 스크래퍼 만들기 (SocialKit 있음)

---

**질문 있으면 Ted한테 물어봐.**
