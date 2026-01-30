# 🚦 Agent Status Dashboard

**Last Updated:** 2026-01-31 06:35 KST (21:35 UTC)

---

## 🤖 자동화 상태
- **Cron:** 5분마다 git sync ✅
- **협업 시스템:** 작동 중 ✅
- **Telegram 그룹:** 설정 중 (멘션 감지 이슈)

---

## 👥 Agents

### 소미 🐱 (VPS/Claude)
- **Status:** 🟢 Working
- **Current Task:** T003 Komission 큐레이팅 워크플로우 문서화
- **Location:** VPS (24/7)
- **Blocker:** API 키 필요

### local 🐰 (Mac/GPT)  
- **Status:** 🟢 Active
- **Current Task:** T001/T002/Komission 플랜 진행 중
- **Location:** MacBook

### AG-Komission ⚡
- **Status:** 🟡 Assigned
- **Current Task:** T003 대기
- **SSH:** ✅ 등록됨

### AG-Vivid ⚡
- **Status:** 🟢 Working
- **Current Task:** T001/T002 초안 완료
- **SSH:** ✅ 등록됨

---

## 📊 태스크 현황

| ID | 태스크 | 담당 | 상태 |
|----|--------|------|------|
| T001 | 유튜브 라이브 (1/31 14:00) | local, AG-Vivid | 🟢 초안 완료 |
| T002 | Vivid UX 최적화 | local, AG-Vivid | 🟢 플랜 완료 |
| T003 | Komission 큐레이팅 | 소미, AG-Komission | 🟡 워크플로우 문서화 |
| T004 | 성수동 아카데미 | - | 📋 신규 |

---

## 📝 진행 상황 (2026-01-31)

### local 🐰 완료
- ✅ Vivid UX 가설 기반 감사 플랜
- ✅ Komission 큐레이팅 워크플로우 뼈대
- ✅ T001 초안 (런오브쇼, 멘트, Q&A, OBS 체크리스트)

### 소미 🐱 완료
- ✅ 협업 시스템 구축 (agents/, messages/)
- ✅ Git 5분 동기화 Cron
- ✅ Komission 워크플로우 문서 (`projects/komission/CURATION_WORKFLOW.md`)

### 진행 중
- 🔄 Telegram 그룹 멘션 이슈 해결
- 🔄 API 키 대기 (Komission)

---

## 🔔 Recent Activity

| 시간 (KST) | Agent | Action |
|------------|-------|--------|
| 06:35 | 소미 🐱 | Komission 워크플로우 문서 작성 |
| 06:32 | local 🐰 | T001/T002/Komission 플랜 공유 |
| 06:25 | 소미 🐱 | Telegram 그룹 설정 시도 |
| 05:48 | 소미 🐱 | 태스크 배정 완료 |

---

## ⚠️ Blockers

1. **Komission API 키** - 테드에게 요청 필요
2. **Telegram 그룹 멘션** - 설정 조정 중

---

## 💡 테드 확인 필요

1. **T001 주제/타깃/CTA** - local이 최종본 리라이트 대기 중
2. **Komission 타입** - 뉴스레터? 커미션 마켓? 기회 트래커?
3. **API 키** - `OPENCLAW_API_KEY` 환경변수 설정
