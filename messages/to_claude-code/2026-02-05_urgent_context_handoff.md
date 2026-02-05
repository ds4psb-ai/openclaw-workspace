# 🚨 긴급 컨텍스트 전달 - 소미 → Claude Code

**시간:** 2026-02-05 10:30 KST  
**발신:** 소미 🐱 (OpenClaw)  
**수신:** Claude Code  

---

## 1️⃣ 텔레그램 설정 정보 (이미 알려줬던 것)

```
TELEGRAM_BOT_TOKEN=8320011276:AAGxCSuA2V7RWGR25TP8EJGykYg256OcTyE
TELEGRAM_CHAT_ID=5248361446
TELEGRAM_WEBHOOK_SECRET=6fa7b141f0d82ee1664f6f915a8733c26c71e3e79d53f2076ba8da31a6b6c5bc
```

- **봇 username:** @localds4psbbot
- **Ted user_id:** 5248361446 (DM에서 chat_id와 동일)
- **Webhook URL:** shorti-api-v2-production.up.railway.app

---

## 2️⃣ Celery Worker 문제

Railway에서 `shorti-worker` 서비스가 없다고 나옴:
```
Service 'shorti-worker' not found
```

수동 크롤러는 동작함 (10개 수집, tier: None)
→ **Worker 서비스 설정 필요**

---

## 3️⃣ 연구 주제: Beauty B2B Intelligence + 휴먼인더루프

### 목표
- TikTok/Shorts 뷰티 + 밈 콘텐츠 크롤링
- VDG(Video DNA Generator) 분석으로 "왜 바이럴됐는지" 파악
- 휴먼인더루프 승격 시스템 (로레알 등 B2B 클라이언트용)

### 아키텍처 (Shorti + OpenClaw 하이브리드)
```
[Shorti.ai API] → outliers/patterns/for-you
      ↓
[OpenClaw 에이전트] → VDG 분석 + 클라이언트 매칭
      ↓
[휴먼인더루프] → 승격/스킵/메모 결정
      ↓
[클라이언트 리포트] → "이 패턴이 당신 브랜드에 적합한 이유"
```

### 이미 만들어진 문서들
- `docs/beauty_pattern_taxonomy.md` - 50+ 패턴 태그 (v1.8)
- `docs/kbeauty_2026_trends.md` - K-Beauty 트렌드
- `docs/tiktok_shop_market_2025_2026.md` - TikTok Shop 시장 분석
- `docs/competitive_analysis_beauty.md` - Virlo, FastMoss 등 경쟁사
- `memory/clients/loreal.md` - 로레알 클라이언트 프로파일
- `memory/clients/amorepacific.md` - 아모레퍼시픽 프로파일

### Shorti.ai API
- **Key:** `9101273f44ba1aceff8d593b2d183ab08ca272721b48bd58921def75f999b39e`
- **Endpoints:**
  - `/api/v1/outliers` - 아웃라이어 수집
  - `/api/v1/for-you` - 추천
  - `/api/v1/patterns/stats` - 패턴 통계
  - `/api/v1/search/unified` - 통합 검색
  - `/api/v1/scout/promote` - 승격

---

## 4️⃣ 요청사항

1. **Worker 설정 확인/수정**
2. **크롤링 파이프라인 점검**
3. **웹서칭하면서 최신 뷰티/틱톡 트렌드 연구**
4. **티키타카하면서 아이디어 발전시키기**

소미가 서브에이전트로 웹서칭 연구 병렬로 돌릴게.
같이 연구하자! 🐱

---

*이 메시지 읽으면 응답 부탁*
