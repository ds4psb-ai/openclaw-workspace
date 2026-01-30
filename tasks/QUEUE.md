# 📋 Task Queue

## 에이전트 태그
- `@somi` - 소미 🐱 (OpenClaw/Claude, VPS 24h)
- `@bomi` - 보미 🐰 (OpenClaw/GPT, Mac)
- `@claude-code` - Claude Code CLI 🔵
- `@codex` - Codex CLI 🟢
- `@ag-komission` - Antigravity Komission ⚡
- `@ag-vivid` - Antigravity Vivid ⚡

---

## 🔴 In Progress (진행 중)

| ID | 태스크 | 담당 | 우선순위 | 마감 | 상태 |
|----|--------|------|----------|------|------|
| T001 | 유튜브 라이브 자료 | @bomi @somi | 🔴 긴급 | 1/31 14:00 KST | ✅ 최종본 완료 |
| T002 | Vivid 메가앱 UX | @ag-vivid @bomi @somi | 🔴 긴급 | - | ✅ 티켓 완료 |
| T003 | Komission 큐레이팅 | @somi @ag-komission | 🟡 중요 | - | ✅ 자동화 완료 |
| T004 | 성수동 아카데미 홍보 | @ag-vivid | 🟢 일반 | - | 🔄 진행 중 |

---

## 📝 태스크 상세

### T001 - 유튜브 라이브 자료
- **담당:** @bomi @ag-vivid @somi
- **마감:** 2026-01-31 14:00 KST
- **상태:** ✅ **최종본 완료** → 테드 검토 대기
- **파일:** 
  - `artifacts/deliverables/T001_YOUTUBE_LIVE_FINAL.md` ⭐ (소미 최종 통합본)
  - `artifacts/deliverables/T001_RUN_OF_SHOW.md` (보미)
  - `artifacts/deliverables/youtube_live_script.md` (보미)
- **완료 항목:**
  - [x] 스크립트 디테일 보완
  - [x] Q&A 추가 질문 보완
  - [x] 미확정 파트 → "카톡 상담에서 안내" 통일
  - [x] 타임라인 + 방송사고 대응 + OBS 체크리스트
- **테드 확인 필요:**
  - [ ] 화면 자료/슬라이드 최종 확인
  - [ ] 데모 서버 테스트

### T002 - Vivid 메가앱 UX 최적화
- **담당:** @ag-vivid @bomi @somi
- **목표:** Activation 완료율 ↑, 첫 성공까지 시간 ↓
- **상태:** ✅ **티켓 쪼개기 완료** → AG-Vivid 코드베이스 매핑 대기
- **파일:** 
  - `artifacts/reports/T002_VIVID_UX_P0_BACKLOG.md` (보미 P0 백로그)
  - `artifacts/reports/T002_VIVID_UX_TICKETS.md` ⭐ (소미 티켓 10개)
- **완료 항목:**
  - [x] Activation 정의: DNA Lab 업로드→분석완료→결과확인
  - [x] P0 백로그 작성
  - [x] 화면 컴포넌트 단위 티켓 (VIV-001~010)
  - [x] 권장 구현 순서
- **다음 단계:**
  - [ ] AG-Vivid 코드베이스 매핑
  - [ ] PR 단위로 구현 시작

### T003 - Komission 숏폼 큐레이팅 자동화
- **담당:** @somi @ag-komission
- **목표:** shorti.ai API로 고퀄리티 숏폼 자동 큐레이팅
- **상태:** ✅ **자동화 스크립트 완료!**
- **파일:** 
  - `artifacts/research/T003_komission_research.md` - 리서치
  - `scripts/komission/fetch_outliers.py` - 아웃라이어 수집
  - `scripts/komission/vdg_analyzer.py` - VDG 분석
  - `scripts/komission/curator.py` ⭐ - 큐레이션 리포트 생성
  - `artifacts/reports/curation_latest.md` - 최신 리포트
- **완료 항목:**
  - [x] API 키 찾음 (memory 파일에서)
  - [x] API 연결 테스트 완료
  - [x] 아웃라이어 수집 스크립트
  - [x] VDG 분석 스크립트
  - [x] 일간 큐레이션 리포트 자동 생성
- **결과:**
  - SS티어 아웃라이어 1개 발견 (@henrywestyt, 530만 조회)
  - 참여율 13.75% (매우 높음)
- **다음 단계:**
  - [ ] cron job 설정 (매 6시간)
  - [ ] VDG 상세 분석 연동
  - [ ] 패턴 DB 구축

---

## ✅ Done (완료)

| ID | 태스크 | 담당 | 완료일 |
|----|--------|------|--------|
| - | 협업 시스템 구축 | @somi | 2026-01-30 |
| - | Git 동기화 자동화 | @somi | 2026-01-30 |
