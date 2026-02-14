# OpenClaw 멀티 인스턴스 백엔드화 설계 (Vivid 제외)

작성일: 2026-02-15 (KST)
대상: Komission / Beauty Brand + Creator Account Intelligence

## 0) 문제 재정의

우선순위는 인프라 분리가 아니라 **브랜드/크리에이터 계정 중심 운영체계 내재화**다.
OpenClaw는 다음 두 레이어로 사용한다.

- **Control Plane (Main OpenClaw)**: 의사결정, 우선순위, 승인, 보고
- **Data Plane (Komission OpenClaw Instance)**: 크롤링, 엄선/승격 분석, 점수 계산, 배치 실행

핵심 산출물은 `outlier report`가 아니라 `account intelligence`다.

---

## 1) 타깃 아키텍처

### 1.1 컴포넌트

1. **Account Registry Service (브랜드/크리에이터 관리 코어)**
- 역할: 브랜드/크리에이터 마스터 데이터 + 상태 + 담당/우선순위/룰 관리
- 저장: `data/accounts/accounts.db` (SQLite 시작, 추후 Postgres)
- 테이블:
  - `accounts` (brand/creator)
  - `account_groups` (client/sector/watchlist)
  - `account_memberships`
  - `account_relations` (brand<->creator)
  - `account_policies` (금지 패턴/선호 패턴/리스크 임계치)
  - `account_health_snapshots` (활성도/증감률/리스크 상태)

2. **Ingestion Workers (Komission instance)**
- 역할: 계정 단위 크롤링
- 입력: active/watch 상태 계정 목록
- 출력: raw events + normalized media features

3. **Pattern Clustering Engine (패턴 클러스터링)**
- 역할: 영상/카피/후킹/CTA/비주얼 요소를 벡터화해 클러스터 생성
- 산출:
  - `pattern_clusters`
  - `cluster_members`
  - `cluster_drift` (시간 경과에 따른 패턴 변화)
- 목적: 단일 영상이 아니라 "반복 가능한 포맷"을 추출

4. **Personalized Recommendation Engine (맞춤형 추천)**
- 역할: 브랜드별/크리에이터별 추천 생성
- 입력: 계정 정책 + 패턴 클러스터 + 최근 성과
- 산출:
  - `recommendation_items`
  - `why_this` (설명가능성)
  - `do/dont checklist`

5. **Promotion Intelligence Engine**
- 역할: 엄선/승격 판단
- 산출:
  - `promotion_candidates`
  - `promotion_decisions`
  - `decision_reasons`

6. **Delivery & Orchestration**
- OpenClaw cron: 주기 실행
- OpenClaw sessions_send/message: 알림/보고
- Main에서 승인 시 Data Plane에 작업 위임

### 1.2 논리 토폴로지

- Main OpenClaw
  - 사용자 대화, 전략 변경, 승인
  - Komission 세션으로 명령 전달 (`sessions_send`)
- Komission OpenClaw
  - 계정 크롤, score 계산, 승격 후보 선별
  - 결과를 artifacts + summary로 반환

---

## 2) 코드베이스 매핑 (현재 → 목표)

현재 파일:
- `scripts/komission/fetch_outliers.py`
- `scripts/komission/vdg_analyzer.py`
- `scripts/komission/curator.py`
- `scripts/komission/check_outliers.py`
- `memory/clients/amorepacific.md`, `memory/clients/loreal.md`

### 2.1 신규 디렉토리

- `scripts/komission/account_core/`
  - `models.py` (SQLite schema)
  - `registry_sync.py` (clients memory -> registry)
  - `selectors.py` (crawl 대상 계정 선택)
- `scripts/komission/pipeline/`
  - `crawl_accounts.py`
  - `compute_account_signals.py`
  - `promotion_ranker.py`
  - `publish_digest.py`
- `data/accounts/`
  - `accounts.db`
  - `seed_accounts.yaml`
- `artifacts/reports/accounts/`
  - `account_digest_latest.md`
  - `promotion_candidates_latest.md`

### 2.2 기존 스크립트 리팩터링

- `fetch_outliers.py` → `crawl_accounts.py`로 분리 (글로벌 limit 기반 제거)
- `curator.py` → 계정 단위 KPI(브랜드 적합도, 협업 가능성) 중심으로 전환
- `vdg_analyzer.py` → 후보 영상만 비동기 분석하도록 큐 기반으로 변경

---

## 3) 데이터 모델 (MVP)

### accounts
- `id` (pk)
- `platform` (tiktok/youtube/...)
- `handle`
- `account_type` (brand|creator)
- `client_key` (amorepacific/loreal/...)
- `priority_tier` (p0/p1/p2)
- `status` (active/watch/paused)
- `owner` (담당자/에이전트)
- `tags` (json)
- `created_at`, `updated_at`

### account_policies
- `id`
- `account_id`
- `preferred_patterns` (json)
- `blocked_patterns` (json)
- `tone_constraints` (json)
- `risk_threshold`
- `updated_at`

### account_health_snapshots
- `id`
- `account_id`
- `captured_at`
- `posting_freq_7d`
- `engagement_rate_7d`
- `velocity_delta`
- `risk_flags` (json)

### account_relations
- `id`
- `src_account_id`
- `dst_account_id`
- `relation_type` (mentioned/collab/competitor_overlap/...)
- `strength` (0~1)
- `evidence_ref`

### pattern_clusters
- `id`
- `cluster_key`
- `cluster_label`
- `embedding_version`
- `top_features` (json)
- `window_start`, `window_end`
- `confidence`

### cluster_members
- `id`
- `cluster_id`
- `content_id`
- `account_id`
- `distance_score`

### recommendation_items
- `id`
- `target_account_id`
- `content_id` (reference)
- `cluster_id`
- `rec_type` (creative_idea/collab_target/timing/format)
- `priority_score`
- `why_this` (text/json)
- `status` (new/sent/accepted/rejected)

### promotion_candidates
- `id`
- `account_id`
- `content_id`
- `promotion_score`
- `brand_fit_score`
- `risk_score`
- `decision_state` (proposed/approved/rejected)
- `reason_json`

---

## 4) 승격 분석(엄선) 로직 내재화

최종 점수 예시:

`promotion_score = 0.35*virality + 0.30*brand_fit + 0.20*conversion_proxy + 0.15*novelty - risk_penalty`

- **virality**: view velocity, engagement, share rate
- **brand_fit**: 클라이언트별 선호 패턴/금지 패턴 매칭
- **conversion_proxy**: CTA/상품 연계/라이브커머스 적합성
- **novelty**: 최근 14일 내 패턴 중복도 역수
- **risk_penalty**: controversy, policy, tone mismatch

승격 상태 머신:
- `proposed -> triaged -> approved -> published`
- `rejected`는 사유 mandatory

---

## 5) OpenClaw 멀티 인스턴스 운영안

### 단계 A (즉시)
- Main 세션에서 Komission 세션으로 위임
- cron은 Main에 두고 실행은 Komission으로 라우팅

### 단계 B (분리)
- Komission 전용 Gateway/세션에서 cron 직접 실행
- Main은 결과 수신 + 승인만 수행

### 세션 계약(Contract)
- 요청 템플릿:
  - `RUN_CRAWL_SCOPE {client_key, account_tier, lookback}`
  - `RUN_PROMOTION_RANK {client_key, threshold}`
- 응답 템플릿:
  - `SUMMARY + artifacts path + errors + next_actions`

---

## 6) 4주 실행 로드맵

### Week 1 — Account Registry 구축
- [ ] `accounts.db` 스키마 생성
- [ ] `memory/clients/*.md` 기반 seed 작성
- [ ] registry sync 스크립트
- [ ] 기존 보고서에 account_id 컬럼 추가

### Week 2 — Account-scoped Crawl 전환
- [ ] `crawl_accounts.py` 작성
- [ ] active/watch 대상만 크롤
- [ ] 실패 재시도/백오프/중복제거
- [ ] 품질 대시보드(`coverage`, `freshness`)

### Week 3 — Promotion Intelligence
- [ ] 점수 계산기 구현
- [ ] 승격 상태 머신 구현
- [ ] approval workflow(메인 세션에서 승인)
- [ ] 후보 리포트 자동 생성

### Week 4 — 멀티 인스턴스 고도화
- [ ] Komission 전용 인스턴스로 cron 이전
- [ ] Main↔Komission 세션 계약 고정
- [ ] 장애 대응(runbook, retry, dead-letter)
- [ ] 비용/성능 튜닝

---

## 7) 운영 지표 (필수)

- 계정 커버리지: `active accounts with fresh crawl / total active`
- 승격 정밀도: `approved 후 성과 기준 충족 비율`
- 처리지연: crawl->proposal->approval->publish lead time
- 노이즈율: rejected ratio & top rejection reasons

---

## 8) 보안/품질 체크포인트

- API Key 하드코딩 제거 (`OPENCLAW_API_KEY` 필수)
- PII/비공개 데이터 로그 마스킹
- 멱등성 키(`platform+content_id`) 도입
- 장애 시 degrade: 전역 리포트 대신 마지막 정상 스냅샷 전송

---

## 9) 리스크와 롤백

리스크:
- 계정 스키마 설계 미흡 -> 분석 일관성 저하
- 분리 시 세션 계약 불안정 -> 운영 복잡성 증가

롤백:
- Week 4 이전에는 기존 `curator.py` 결과를 병행 유지
- 신규 점수계는 shadow mode(의사결정 미반영)로 1주 검증

---

## 10) 외부 사례에서 가져온 원칙

- 멀티테넌시에서 control plane/data plane 분리 (AWS/Azure 가이드 공통)
- tenant/account 단위 isolation + shared model 혼합 전략
- 추론/배치는 공유, 민감 데이터/정책은 테넌트 경계 내 유지

(참고)
- Azure Multitenant AI/ML approaches
- AWS Prescriptive Guidance: agentic AI multi-tenant architecture
