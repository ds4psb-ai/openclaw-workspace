# Vivid + 아카데미 자동화 리서치

> **작성자**: 보미 🐰
> **작성일**: 2026-01-31 01:45 KST

---

## 📊 현재 Vivid 자동화 인프라

### 이미 구현된 것들 ✅

| 기능 | 설명 | 파일 |
|------|------|------|
| **ARQ (Redis Queue)** | 비동기 백그라운드 작업 | `main.py` |
| **Drift Cron** | 매일 02:00 UTC 자동 실행 | `services/drift_cron.py` |
| **Batch Processing** | 50% 비용 절감, 24시간 내 완료 | `routers/batch.py` |
| **Stripe Webhook** | 결제 이벤트 자동 처리 | `routers/stripe_webhook.py` |
| **Crebit 코스 시스템** | 수강 신청/결제 관리 | `routers/crebit.py` |
| **Monitor + Alerts** | 시스템 모니터링/알림 | `routers/monitor.py` |

---

## 🎓 아카데미 자동화 방안

### 1. 수강생 모집 자동화

#### OpenClaw Cron으로 정기 홍보
```bash
# 매일 오전 10시 카톡 채널 홍보 메시지
openclaw cron add \
  --name "Academy Daily Promo" \
  --cron "0 10 * * *" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "성수동 아카데미 D-N 홍보 메시지 생성해서 카톡 채널에 전송" \
  --deliver --channel telegram
```

#### 신청 알림 웹훅
```python
# Vivid에 웹훅 엔드포인트 추가
@router.post("/webhook/application")
async def application_webhook(data: ApplicationCreate):
    # 신청 시 즉시 OpenClaw에 알림
    requests.post("http://localhost:18789/hooks/agent", json={
        "message": f"🎓 새 수강 신청! {data.name} ({data.phone})",
        "deliver": True
    })
```

### 2. 수강생 관리 자동화

| 자동화 | 트리거 | 액션 |
|--------|--------|------|
| 신청 확인 | 신청 완료 | 확인 이메일/카톡 발송 |
| 결제 리마인더 | 신청 후 24시간 | 결제 독려 메시지 |
| 수업 리마인더 | 수업 2시간 전 | 알림 메시지 |
| 후기 요청 | 수업 완료 후 | 후기 작성 요청 |

### 3. 콘텐츠 자동화

#### Vivid로 홍보 콘텐츠 자동 생성
```bash
# 매주 월요일 홍보 이미지 생성
openclaw cron add \
  --name "Weekly Promo Content" \
  --cron "0 9 * * 1" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "Vivid 3D 앱으로 이번 주 아카데미 홍보 이미지 생성" \
  --deliver --channel telegram
```

---

## 🔗 OpenClaw ↔ Vivid 연동

### 방법 1: Webhook (추천)
```
Vivid Event → OpenClaw Webhook → 소미/보미 처리 → 응답
```

**장점**: 실시간, 이벤트 드리븐
**설정**:
```yaml
# Vivid에 webhook 추가
OPENCLAW_WEBHOOK_URL=http://localhost:18789/hooks/agent
```

### 방법 2: API 폴링
```
OpenClaw Cron → Vivid API 조회 → 변경 감지 → 알림
```

**장점**: 간단, 추가 설정 최소화
**설정**: OpenClaw cron job으로 주기적 체크

### 방법 3: 공유 Redis
```
Vivid → Redis Pub/Sub → OpenClaw 구독
```

**장점**: 가장 빠름, 실시간
**단점**: 인프라 복잡도 증가

---

## 📋 구현 우선순위

| 순위 | 자동화 | 난이도 | 효과 |
|:----:|--------|:------:|:----:|
| 1️⃣ | 신청 알림 웹훅 | ⭐ | ⭐⭐⭐ |
| 2️⃣ | 수업 리마인더 Cron | ⭐ | ⭐⭐⭐ |
| 3️⃣ | 정기 홍보 Cron | ⭐⭐ | ⭐⭐ |
| 4️⃣ | 홍보 콘텐츠 자동 생성 | ⭐⭐⭐ | ⭐⭐ |
| 5️⃣ | 결제 리마인더 | ⭐⭐ | ⭐⭐⭐ |

---

## 🚀 즉시 실행 가능한 것

### 1. 수업 리마인더 (OpenClaw Cron)
```bash
# 2/3(화) 수업 2시간 전 리마인더
openclaw cron add \
  --name "Class Reminder 2/3" \
  --at "2026-02-03T17:00:00+09:00" \
  --session main \
  --text "🎓 오늘 19:00 성수동 아카데미 첫 수업! 준비됐어?"
```

### 2. 라이브 전 리마인더
```bash
# 내일(일) 라이브 1시간 전 리마인더  
openclaw cron add \
  --name "Live Reminder" \
  --at "2026-02-01T13:00:00+09:00" \
  --session main \
  --text "📺 1시간 후 유튜브 라이브! 준비 체크해!"
```

---

## 📝 TODO (테드 결정 필요)

1. [ ] Vivid에 OpenClaw 웹훅 엔드포인트 추가할까?
2. [ ] 카톡 채널 API 연동 가능? (자동 메시지 발송용)
3. [ ] 이메일 발송 서비스 있어? (수강생 알림용)
4. [ ] Crebit 시스템에 수업 일정 데이터 있어?

---

## 참고: Vivid 기존 코드

- Crebit 코스 시스템: `backend/app/routers/crebit.py`
- 결제 시스템: `backend/app/routers/payment.py`
- Stripe 웹훅: `backend/app/routers/stripe_webhook.py`
- Batch 처리: `backend/app/routers/batch.py`
- Drift Cron: `backend/app/services/drift_cron.py`
