# MEMORY.md - 보미의 장기 기억 🐰

*마지막 업데이트: 2026-02-02*

---

## 👤 테드 (Ted Kim)

- **텔레그램:** @jjapagetti
- **타임존:** Asia/Seoul (KST)
- **언어:** 한국어 (주), English

### 성격/선호
- 직접적인 커뮤니케이션 선호
- 환각/추측 싫어함 → 실제 출력 확인 요구
- 자동화 좋아함

---

## 🚀 프로젝트

### Prompty Academy
- **정의:** AI 영상 제작 오프라인 강의 (성수동)
- **웹사이트:** https://www.prompty.co.kr/academy
- **Discord:** https://discord.gg/8zKZRXmGUp
- **핵심 도구:** Google AI Pro, Antigravity, Kling AI
- **빌더 3개:** 이미지 프롬프트 생성기, 바이브 철학관, 패러디 오마주 엔진
- **상태:** 2회차 수업 2026-02-05

### Mac 원격 제어
- **Tailscale 연결:** VPS(100.109.36.63) ↔ Mac(100.69.32.16)
- **SSH:** ted@100.69.32.16
- **명령 서버:** http://100.109.36.63:9999 (Mac 터미널에서 폴링)
- **가능:** SSH, Chrome 조작, 스크린샷, 파일 전송

### Komission
- **정의:** TikTok 바이럴 콘텐츠 인텔리전스 플랫폼
- **백엔드:** https://api.shorti.ai (Railway)
- **기능:** 아웃라이어 스카우트, VDG 분석, 큐레이팅
- **스킬:** `~/.openclaw/skills/openclaw-komission-scout/`
- **API 키:** `KOMISSION_SCOUT_API_KEY` (환경변수)
- **상태:** Scout promote 테스트 성공 (2026-02-02)

### 에이전트 팀 (절대 헷갈리지 마!!)
| 이름 | 이모지 | 위치 | IP | 토큰 |
|------|--------|------|-----|------|
| **보미 (나!)** | 🐰 | VPS | 100.109.36.63 | e1e02af3ca6ab644d6beeee7d9a09993ae58e3f89edfcf56 |
| **소미** | 🐱 | Mac | 100.69.32.16 | 5946a9034f444d7e06d3ddf17663b68c958654d8947e2d07 |
| @ag-komission | ⚡ | - | - | - |

---

## 📋 진행 중인 태스크

### T003 - Komission 숏폼 큐레이팅 자동화
- **상태:** ✅ 스킬 설치 완료, promote 테스트 성공
- **남은 것:**
  - [ ] cron job 설정 (6시간마다)
  - [ ] VDG 상세 분석 연동
  - [ ] 패턴 DB 구축

---

## 🔧 시스템 설정

### OpenClaw 설정 (2026-02-02 적용)
- `compaction.memoryFlush.enabled: true`
- `memorySearch.sources: ["memory", "sessions"]`
- `memorySearch.experimental.sessionMemory: true`

---

## 📝 중요한 결정들

| 날짜 | 결정 | 이유 |
|------|------|------|
| 2026-02-02 | Vivid 메모리 삭제 | 테드 요청 |

---

## 💡 배운 것들

- 테드는 실제 터미널 출력 확인을 중요시함
- "환각 아님 ✅" 검증 습관화

---

*이 파일은 세션 간 지속되는 장기 기억입니다. 중요한 것만 기록.*
