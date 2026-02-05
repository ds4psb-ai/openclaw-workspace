# MEMORY.md - 소미 🐱 장기 기억

*일간 노트(memory/YYYY-MM-DD.md)에서 중요한 것만 여기에 정리*

---

## 📌 중요 결정들

### 2026-01-31
- **협업 시스템 구축**: Git 기반 멀티 에이전트 협업 (소미, 보미, AG-Vivid, AG-Komission)
- **태스크 관리**: tasks/QUEUE.md 중앙 집중식 관리
- **메시지 시스템**: messages/to_{agent}/ 폴더 구조

### 2026-02-04
- **Beauty B2B Intelligence**: Shorti + OpenClaw 하이브리드 아키텍처 결정
- **클라이언트 관리**: clients.json 설정 파일 + memory/clients/*.md 컨텍스트 파일

---

## 🔑 API 키 & 설정

### Shorti.ai
- Key: `9101273f44ba1aceff8d593b2d183ab08ca272721b48bd58921def75f999b39e`
- Endpoints: outliers, for-you, patterns/stats, search/unified, scout/promote

---

## 👥 테드 프로젝트들

### 진행 중
1. **Vivid (Crebit Studio)** - AI 콘텐츠 생성 플랫폼
2. **Komission** - 숏폼 큐레이팅/자동화
3. **성수동 아카데미** - 휴머나이저 AI 영상 제작 아카데미 1기

### 완료
- T001 유튜브 라이브 자료 (2026-01-31 14:00)
- T002 Vivid UX 티켓 쪼개기
- T003 Komission 스크립트 기본 구현

---

## 💡 인사이트 & 교훈

### 스크립트 경로 문제
- 하드코딩된 `/root/...` 경로 → 환경변수 `OPENCLAW_WORKSPACE` 사용으로 수정
- macOS에서는 `/Users/ted/.openclaw/workspace`

---

## 🔧 Komission 크롤러 시스템 (2026-02-06 완성)

### 아키텍처

```
SocialKit API → tiktok_tasks.py → CrawledVideoData DTO
                                        ↓
                              outlier_factory.py (calculate_score)
                                        ↓
                              OutlierItem (DB)
                                        ↓
                         enrich_outlier_scores (creator_multiplier)
                                        ↓
                         beauty_scout_tasks.py → Telegram 알림
```

### 핵심 파일

| 파일 | 역할 |
|------|------|
| `tiktok_tasks.py` | TikTok 크롤러 (SocialKit) |
| `youtube_tasks.py` | YouTube 크롤러 |
| `outlier_factory.py` | DTO→OutlierItem, calculate_score |
| `beauty_scout_tasks.py` | SS/S tier Telegram 알림 |
| `config.py` | K-Beauty 키워드 18개 |

### 바이럴 점수 공식

```python
score = base_score + share_bonus + engagement_bonus
# share_rate 3%+ → +2.0 보너스 (핵심!)
```

### Tier 기준

| Tier | Score | 조회수 |
|------|-------|--------|
| SS | 50+ | 5M+ |
| S | 20+ | 2M+ |
| A | 10+ | 1M+ |
| B | 5+ | 500K+ |

### Celery Beat 스케줄

- 크롤: 0,6,12,18시 **:15**
- Enrichment: 0,6,12,18시 **:45**
- Scout: 1,7,13,19시

### 활용 쿼리

```sql
-- SS/S tier 참여율 분석
SELECT outlier_tier, category, 
  AVG((like_count + COALESCE(comment_count,0) + COALESCE(share_count,0))::float 
      / NULLIF(view_count,0) * 100) as avg_engagement
FROM outlier_items 
WHERE crawled_at > NOW() - INTERVAL '1 day'
GROUP BY outlier_tier, category;
```

### 리서치 문서

- `artifacts/reports/TIKTOK_VIRAL_BENCHMARKS_2025.md`
- `artifacts/reports/KBEAUTY_TIKTOK_RESEARCH.md`
- `artifacts/reports/CRAWLER_ENHANCEMENT_SPEC.md`

---

## 📊 다음 연구 주제

1. **creator_multiplier 활용** - 평소 10배 = 바이럴 신호
2. **해시태그 조합 분석** - raw_payload hashtags
3. **트렌딩 사운드 연동** - sound_id 활용
4. **Meme 카테고리 분리** - 1M+ threshold
5. **경쟁사 비교** - Virlo, Analisa.io

---

## 📅 정기 업무

- Heartbeat 시 git sync 필수
- 5분마다 cron job들이 돌고 있음
- 중요한 발견 시 테드에게 즉시 보고

---

*마지막 업데이트: 2026-02-06 01:11 KST by 소미 🐱*
