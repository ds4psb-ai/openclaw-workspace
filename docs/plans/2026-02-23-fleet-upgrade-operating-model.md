# Komission A0/OpenClaw Fleet Upgrade Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 현재 4대 VPS(a0 + OpenClaw) 운영을 “측정 가능/자동 복구/안전 업데이트/정확 스케줄링” 체계로 업그레이드한다.

**Architecture:** 기존 프로세스는 유지하고, 리서치 근거 기반으로 관측(Baseline) → 스케줄 분리(Cron/Heartbeat) → 복구 자동화(Runbook Code) → 점진 업데이트(Dry-run + Canary) 순서로 도입한다. 장애 복구 권한 범위 내 재시작은 자동 처리하고, 정책 변경/배포는 수동 승인으로 분리한다.

**Tech Stack:** OpenClaw Gateway cron, shell/ssh, docker 상태 점검, Markdown runbook, Telegram 알림

---

## External Research Snapshot (2026-02)

### R1. OpenClaw Releases (`openclaw/openclaw`)
- `openclaw update --dry-run` 지원: 업데이트 전 영향도 확인 가능
- Cron/Gateway/Auth/Exec 관련 안정화 다수
- 시사점: 운영 업데이트는 **dry-run → canary → rollout** 고정 필요

### R2. OpenClaw Docs - Cron Jobs
- cron은 Gateway 내부에서 persistent하게 동작 (`~/.openclaw/cron/`)
- 실행 모드 분리: `main(systemEvent)` vs `isolated(agentTurn)`
- 시사점: 무거운 작업은 isolated cron으로 분리해야 메인 세션 오염/지연 감소

### R3. OpenClaw Docs - Cron vs Heartbeat
- Heartbeat: 컨텍스트 기반 배치 점검
- Cron: 정시성/독립성/모델별 실행
- 시사점: “정확 시간”/“무거운 작업”은 cron, awareness는 heartbeat로 분리

### R4. OpenClaw Docs - Automation Troubleshooting
- 진단 ladder: `openclaw status → gateway status → logs → doctor → channels probe`
- cron/heartbeat 실패 시 공통 시그니처 및 원인 체계 제공
- 시사점: 운영 runbook에 **표준 진단 커맨드**를 내장해야 MTTR 감소

### R5. Agent Zero 공식 저장소
- SKILL.md 기반 확장, 멀티에이전트 협업, 터미널 중심 운영 패턴 강조
- 시사점: 현재 체계는 방향성 일치. 핵심 갭은 기능보다 **표준화/관측/복구 자동화**

---

### Task 0: 리서치 근거 문서 고정 (변경 이력 관리)

**Files:**
- Create: `docs/fleet/research-2026-02-openclaw-a0.md`

**Step 1: 리서치 원문 요약 저장**
- 릴리즈/cron/cron-vs-heartbeat/troubleshooting/a0 레퍼런스 요약

**Step 2: 운영 의사결정 매핑 표 작성**
- “근거 → 정책 변경 항목” 1:1 매핑

**Step 3: Commit**
```bash
git add docs/fleet/research-2026-02-openclaw-a0.md
git commit -m "ops: add 2026-02 openclaw/a0 research baseline"
```

### Task 1: Baseline 지표 수집 스크립트 고정

**Files:**
- Create: `scripts/ops/fleet_baseline.sh`
- Create: `artifacts/reports/fleet/baseline_YYYY-MM-DD.md`

**Step 1: 스크립트 작성 (4대 공통 지표 수집)**
- 수집 항목: uptime, load average, disk %, 핵심 프로세스 수, docker 컨테이너 상태
- 대상: VPS1~4

**Step 2: 수동 실행으로 출력 검증**
Run: `bash scripts/ops/fleet_baseline.sh`
Expected: 4대 모두 섹션 출력 + 실패 호스트 명시

**Step 3: 리포트 파일 생성**
Run: `bash scripts/ops/fleet_baseline.sh > artifacts/reports/fleet/baseline_$(date +%F).md`
Expected: 날짜별 baseline 파일 생성

**Step 4: Commit**
```bash
git add scripts/ops/fleet_baseline.sh artifacts/reports/fleet/.gitkeep
git commit -m "ops: add fleet baseline collection script"
```

### Task 2: Heartbeat vs Cron 책임 분리 (문서+운영 규칙)

**Files:**
- Modify: `HEARTBEAT.md`
- Create: `docs/fleet/cron-heartbeat-boundary.md`

**Step 1: HEARTBEAT.md 경량화**
- heartbeat는 상태 확인/큐 확인 중심으로 제한
- 무거운 분석/요약 작업은 cron isolated로 분리 명시

**Step 2: 경계 문서화**
- heartbeat/cron 분류표 작성
- 정시성 필요한 작업은 cron으로 강제

**Step 3: 검증**
- heartbeat 실행 시 1~2분 내 종료되는지 확인

**Step 4: Commit**
```bash
git add HEARTBEAT.md docs/fleet/cron-heartbeat-boundary.md
git commit -m "ops: split heartbeat and cron responsibilities"
```

### Task 3: 자동 복구 스크립트 + 2회 실패 에스컬레이션

**Files:**
- Create: `scripts/ops/recover_worker.sh`
- Create: `scripts/ops/recover_head.sh`
- Modify: `docs/fleet-runbook.md`

**Step 1: worker/head 복구 스크립트 작성**
- worker down: `/opt/a0-worker/start.sh`
- head down: `/opt/a0-head/restart.sh`
- 실행 로그 저장 (`artifacts/logs/recovery/`)

**Step 2: 2회 재시도 로직 추가**
- 1차 실패 시 재시도
- 2차 실패 시 즉시 실패 + 에스컬레이션 템플릿 출력

**Step 3: dry-run 옵션 추가**
Run: `bash scripts/ops/recover_worker.sh --host 158.247.230.78 --dry-run`
Expected: 실제 실행 없이 명령만 표시

**Step 4: 실검증**
- 정상 서버에서 no-op 점검 후 exit code 확인

**Step 5: Commit**
```bash
git add scripts/ops/recover_worker.sh scripts/ops/recover_head.sh docs/fleet-runbook.md
git commit -m "ops: add automated recovery scripts with escalation"
```

### Task 4: Troubleshooting ladder 런북 내장

**Files:**
- Modify: `docs/fleet-runbook.md`
- Create: `docs/fleet/automation-troubleshooting-cheatsheet.md`

**Step 1: 표준 진단 순서 반영**
- `openclaw status`
- `openclaw gateway status`
- `openclaw logs --follow`
- `openclaw doctor`
- `openclaw channels status --probe`

**Step 2: cron/heartbeat 실패 시그니처 표 추가**
- disabled/not-due/delivery none/quiet-hours/requests-in-flight 등

**Step 3: Commit**
```bash
git add docs/fleet-runbook.md docs/fleet/automation-troubleshooting-cheatsheet.md
git commit -m "ops: embed automation troubleshooting ladder in runbook"
```

### Task 5: 업데이트 안전 절차 (dry-run + canary + rollback)

**Files:**
- Create: `docs/fleet/update-playbook.md`

**Step 1: 업데이트 표준 절차 정의**
- `openclaw update --dry-run` 결과 저장
- Canary 대상 1대 적용
- 30~60분 모니터링
- 이상 없으면 잔여 노드 롤아웃

**Step 2: 롤백 기준 정의**
- gateway 비정상, cron 미실행, 메시지 송수신 실패 시 롤백

**Step 3: 검증 체크리스트 추가**
- `openclaw status`, cron list/run/runs, Telegram test send

**Step 4: Commit**
```bash
git add docs/fleet/update-playbook.md
git commit -m "ops: add openclaw safe update playbook"
```

### Task 6: VDG 파이프라인 관측 포인트 추가 (운영 관점)

**Files:**
- Create: `docs/fleet/vdg-observability-spec.md`
- Modify: `tasks/QUEUE.md`

**Step 1: 상태전이 KPI 정의**
- 전이 카운트: `pending→analyzing`, `failed_retryable`, `failed_permanent`, `post_processing_failed`
- SLA: 대기시간, 재시도율, 영구실패율

**Step 2: 알림 임계값 정의**
- 예: 30분 내 `failed_permanent` N건 이상 시 ALERT

**Step 3: 구현 백로그 등록**
- P0/P1 티켓으로 분해 후 QUEUE 반영

**Step 4: Commit**
```bash
git add docs/fleet/vdg-observability-spec.md tasks/QUEUE.md
git commit -m "ops: define VDG observability KPIs and alert thresholds"
```

### Task 7: 크론 잡 최소셋 구성 (정시성 중심)

**Files:**
- Create: `docs/fleet/cron-jobs-minset.md`

**Step 1: 잡 4개 정의**
1) 30분 health snapshot (isolated)
2) 6시간 VDG 요약 리포트 (isolated)
3) 1일 1회 업데이트 사전 점검 (main/systemEvent)
4) 1일 1회 cron self-check (`cron status + due job sanity`) (isolated)

**Step 2: cron 명령/툴콜 예시 작성**
- add/list/run/runs/wake 포함
- `main=systemEvent`, `isolated=agentTurn` 제약 명시

**Step 3: 운영 검증 절차 추가**
- run 결과 announce/none 동작 확인

**Step 4: Commit**
```bash
git add docs/fleet/cron-jobs-minset.md
git commit -m "ops: define minimum cron job set for fleet monitoring"
```

### Task 8: 완료 검증 (Evidence before assertions)

**Files:**
- Create: `artifacts/reports/fleet/upgrade_validation_YYYY-MM-DD.md`

**Step 1: 검증 명령 실행**
- baseline 스크립트
- cron list/run/runs
- recover 스크립트 dry-run
- VPS 상태 점검(프로세스+디스크)
- troubleshooting ladder 1회 리허설

**Step 2: 결과 캡처**
- 명령/출력/판정(PASS/FAIL) 기록

**Step 3: 최종 보고 작성**
- 변경점, 리스크, 다음 액션 3개

**Step 4: Commit**
```bash
git add artifacts/reports/fleet/upgrade_validation_*.md
git commit -m "ops: add fleet upgrade validation evidence"
```

---

## P0 / P1 / P2 우선순위
- **P0 (오늘):** Task 0, 1, 2, 3
- **P1 (이번 주):** Task 4, 5, 7
- **P2 (다음 주):** Task 6, 8

## Definition of Done
- 외부 리서치 근거 문서가 고정되고 운영 정책과 매핑됨
- 4대 baseline 자동 수집 가능
- heartbeat는 경량, 정시/무거운 작업은 cron isolated로 분리됨
- 자동복구 2회 재시도 + 에스컬레이션 동작
- 업데이트 절차가 dry-run/canary/rollback 기반으로 문서화
- VDG 관측 KPI + 임계값 정의 완료
- 검증 리포트로 PASS/FAIL 증빙 확보
