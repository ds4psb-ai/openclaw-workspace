# OpenClaw 기능 극대화 & 자동화 리서치

## 🎯 현재 목적
1. **Komission** — TikTok 바이럴 콘텐츠 분석
2. **Vivid** — 비디오 생성
3. **Ted 일상 지원** — 알림, 리마인더, 정보 조회

---

## 1. 자동화 도구

### 🔄 Heartbeat (주기적 체크)
매 30분마다 자동 실행 → HEARTBEAT.md 체크리스트 수행

**설정:**
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m",
        "target": "telegram",
        "activeHours": { "start": "08:00", "end": "23:00" }
      }
    }
  }
}
```

**HEARTBEAT.md 예시:**
```markdown
# 체크리스트
- [ ] Komission 새 아웃라이어 확인
- [ ] 중요 알림 있는지 체크
- [ ] 캘린더 오늘/내일 일정
```

### ⏰ Cron Jobs (정확한 스케줄)
특정 시간에 정확히 실행

**예시: 매일 아침 9시 Komission 리포트**
```bash
openclaw cron add \
  --name "Komission Daily Report" \
  --cron "0 9 * * *" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "Komission API에서 어제 새로운 아웃라이어 조회하고 요약해줘" \
  --deliver \
  --channel telegram
```

**예시: 20분 후 리마인더**
```bash
openclaw cron add \
  --name "Reminder" \
  --at "20m" \
  --session main \
  --system-event "리마인더: 회의 시작 10분 전!" \
  --wake now \
  --delete-after-run
```

### 🔗 Webhooks (외부 트리거)
Komission/Vivid에서 OpenClaw로 알림 보내기

**설정:**
```json
{
  "hooks": {
    "enabled": true,
    "token": "your-webhook-secret",
    "path": "/hooks"
  }
}
```

**Komission에서 호출:**
```bash
curl -X POST http://VPS-IP:18789/hooks/agent \
  -H 'Authorization: Bearer your-webhook-secret' \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "새 바이럴 영상 발견: @creator의 영상이 100만뷰 돌파!",
    "name": "Komission",
    "deliver": true,
    "channel": "telegram"
  }'
```

---

## 2. 스킬 확장

### 현재 활성 가능 스킬
| 스킬 | 용도 | 상태 |
|------|------|------|
| komission | TikTok 분석 | ✅ 생성됨 |
| skill-creator | 커스텀 스킬 생성 | ✅ eligible |
| github | GitHub 연동 | ✅ eligible |
| coding-agent | 코딩 에이전트 | ✅ eligible |
| weather | 날씨 조회 | ✅ eligible |
| video-frames | 비디오 프레임 추출 | ✅ eligible |

### 추천 추가 스킬
1. **웹 검색** — Brave API 키 설정 필요
2. **캘린더** — Google Calendar 연동
3. **노션** — Notion API 연동
4. **TTS** — 음성 알림 (ElevenLabs)

---

## 3. 추천 자동화 워크플로우

### A. Komission 모니터링 자동화

```
[Komission 서버] 
    ↓ (새 아웃라이어 발견)
[Webhook → OpenClaw]
    ↓
[소미가 분석 & 요약]
    ↓
[Telegram으로 알림]
```

**구현:**
1. Komission에 webhook 트리거 추가
2. OpenClaw hooks 설정
3. 자동 알림 수신

### B. 일일 리포트 자동화

```
[매일 아침 9시 - Cron]
    ↓
[Komission API 조회]
    ↓
[어제 성과 요약]
    ↓
[Telegram 전송]
```

### C. 콘텐츠 아이디어 자동 생성

```
[바이럴 패턴 감지]
    ↓
[AI 분석 & 아이디어 제안]
    ↓
[Vivid로 영상 생성 요청]
    ↓
[결과 Telegram 전송]
```

---

## 4. 즉시 적용 가능한 설정

### 웹 검색 활성화
```bash
openclaw configure --section web
# Brave API 키 입력 (https://brave.com/search/api/)
```

### Heartbeat 최적화
HEARTBEAT.md 업데이트:
```markdown
# 소미 체크리스트

## 우선순위 높음
- Komission 새 알림 확인
- 중요 메시지 응답

## 주기적 (2-4시간마다)
- 캘린더 다음 일정
- 날씨 (외출 전)

## 야간 제외
- 23:00-08:00 사이는 HEARTBEAT_OK만
```

### Cron 예약 작업 추가
```bash
# 주간 리포트 (월요일 아침)
openclaw cron add \
  --name "Weekly Komission Report" \
  --cron "0 9 * * 1" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "지난 주 Komission 성과 요약해줘: 새 아웃라이어, 패턴 트렌드, 추천 액션" \
  --deliver --channel telegram
```

---

## 5. 보안 고려사항

- ✅ Gateway loopback 유지 (외부 노출 X)
- ✅ Webhook token 별도 설정
- ✅ API 키는 환경변수로 관리
- ⚠️ Tailscale 사용 시 인증 필수

---

## 다음 단계

1. [ ] Brave API 키 설정 (웹 검색)
2. [ ] HEARTBEAT.md 최적화
3. [ ] Komission webhook 연동
4. [ ] Vivid 스킬 생성
5. [ ] 일일/주간 Cron 설정
