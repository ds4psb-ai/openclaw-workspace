# 07. OpenClaw 24시간 역량 & 기존 시스템 연동

**AG 리뷰 반영 + 2026 최신 리서치 기반**

---

## 🚨 핵심 수정: 기존 크롤러 활용!

AG 개발자 피드백 반영:
- ~~새 크롤러 구축~~ → **기존 Komission 크롤러 고도화**
- 이미 구현됨: youtube.py, tiktok.py, instagram.py, content_filter.py

---

## 🐱 OpenClaw 24시간 활용 가치

### 1. 자동 스케줄링 & 트리거
```
# 내가 할 수 있는 것
- cron으로 정기적 크롤링 API 호출
- 기존 /api/v1/crawlers 엔드포인트 활용
- 실패 시 자동 재시도 + 알림
```

### 2. 실시간 모니터링
```
# 24시간 감시
- 크롤러 상태 체크 (정상/에러)
- YouTube Quota 사용량 추적
- Apify 크레딧 모니터링
- 이상 탐지 시 테드에게 즉시 알림
```

### 3. 아웃라이어 자동 감지 & 알림
```
# 기존 Outlier Score 활용
- 크롤링 결과에서 고점수 영상 추출
- 승격 후보 자동 선별
- 테드에게 Telegram으로 즉시 알림
```

### 4. 피드백 루프 운영
```
# 학습 자동화
- 테드 승격/탈락 결정 기록
- 패턴 분석 및 메모리화
- 예측 정확도 추적
- 개선점 자동 제안
```

### 5. A/B 테스트 자동 운영
```
# 매일 자동 실행
- 중간 신뢰도 영상 2개씩 페어링
- 테드에게 선택지 전송
- 응답 수집 및 학습 반영
```

---

## ⚡ 기존 API 연동 방안

### 크롤링 트리거
```bash
# OpenClaw가 호출할 수 있는 기존 API
POST /api/v1/crawlers/youtube/search
POST /api/v1/crawlers/tiktok/search
POST /api/v1/crawlers/instagram/search

# 전략 기반 검색
{
  "strategy": "viral_global",
  "max_results": 50
}
```

### 아웃라이어 조회
```bash
# 기존 Outlier 조회 API 활용
GET /api/v1/outliers?min_score=1000&limit=10
```

### 승격 처리
```bash
# 승격 상태 업데이트
PATCH /api/v1/outliers/{id}
{
  "promoted": true,
  "promoted_by": "ted",
  "promoted_at": "2026-01-31T06:50:00Z"
}
```

---

## 🔄 재정의된 역할 분배

| 역할 | OpenClaw (소미) | AG 개발자 |
|------|-----------------|-----------|
| 크롤링 | API 호출 스케줄링 | 크롤러 로직 유지보수 |
| 모니터링 | 24/7 상태 감시 | 알림 시스템 구축 |
| 아웃라이어 | 후보 선별 & 알림 | 점수 계산 로직 |
| 승격 | A/B 테스트 운영 | 승격 파이프라인 |
| 학습 | 패턴 분석 & 메모리 | ML 모델 (선택) |

---

## 📅 즉시 시작 가능한 것

### OpenClaw (오늘부터)
1. **cron job 설정**: 매 6시간 크롤링 트리거
2. **모니터링 스크립트**: 크롤러 상태 체크
3. **알림 연동**: 고점수 아웃라이어 Telegram 전송
4. **승격 기록**: 테드 결정 → memory에 저장

### 필요한 것 (AG 개발자)
1. **API 접근 정보**: 엔드포인트 URL, 인증 키
2. **Webhook 또는 알림 채널**: 결과 수신 방법
3. **승격 API**: 상태 업데이트 엔드포인트

---

## 🎯 구체적 cron 스케줄 (제안)

```bash
# OpenClaw cron jobs

# 매 6시간: YouTube 트렌딩 크롤링 트리거
0 */6 * * * curl -X POST https://komission-api/crawlers/youtube/search

# 매 4시간: 아웃라이어 체크 & 알림
0 */4 * * * python check_outliers.py

# 매일 09:00 KST: A/B 테스트 전송
0 0 * * * python send_ab_test.py

# 매일 18:00 KST: 일일 리포트
0 9 * * * python daily_report.py

# 매주 월요일: 주간 분석
0 0 * * 1 python weekly_analysis.py
```

---

## 🧠 피드백 루프 상세

### 데이터 수집
```markdown
# memory/promotions/2026-01-31.md

## 승격된 영상
- video_id: abc123
- platform: tiktok
- outlier_score: 2500
- 테드 코멘트: "참여율 높음, 트렌드 적합"

## 탈락된 영상  
- video_id: xyz789
- platform: youtube
- outlier_score: 1800
- 탈락 이유: "광고성"
```

### 패턴 분석 (주간)
```markdown
# memory/patterns/week_05.md

## 승격 경향
- 평균 outlier_score: 2100
- 상위 해시태그: #trend, #viral
- 선호 플랫폼: TikTok 60%, YouTube 40%

## 탈락 패턴
- 광고성 콘텐츠 35%
- 저품질 썸네일 20%
- 참여율 낮음 45%
```

---

## ✅ AG 리뷰 반영 체크리스트

- [x] 기존 크롤러 존재 인지
- [x] "새 구축" → "고도화"로 재정의
- [x] TikTok Apify 활용 인지
- [x] YouTube Quota 관리 인지
- [x] Instagram 제한 인지
- [x] 구체적 API 연동 방안
- [x] 즉시 시작 가능한 액션

---

**Status:** 📋 AG 리뷰 반영 완료, API 정보 대기 중
