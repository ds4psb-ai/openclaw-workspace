# Komission 파이프라인 조사 보고서 - 소미 🐱

**작성일**: 2026-02-06
**담당**: Neo4j 스키마, 패턴 클러스터링, 승격→분석→가이드 플로우

---

## 1. Neo4j 스키마 분석

### 아키텍처
```
PostgreSQL (SSoT) ──→ Neo4j (읽기 전용 캐시)
     │                      │
     ├── remix_nodes       ├── :RemixNode
     ├── outlier_items     ├── :OutlierItem
     ├── pattern_clusters  ├── :PatternCluster
     └── vdg_edges         └── :EVOLVED_TO / :FORKED_FROM
```

- **원칙**: PostgreSQL이 SSoT, Neo4j는 eventual consistency
- **실패 격리**: Neo4j 실패해도 서비스 중단 없음

### 노드 레이블 (8개)

| 레이블 | 용도 | 주요 속성 |
|--------|------|-----------|
| `RemixNode` | VDG 분석 결과 | node_id, title, layer, view_count |
| `OutlierItem` | 크롤링된 아웃라이어 | item_id, external_id, outlier_tier, platform |
| `PatternCluster` | 패턴 클러스터 | cluster_id, cluster_name, pattern_type |
| `HookCluster` | 훅 클러스터 | cluster_id, display_name, hook_type |
| `ViralKick` | 바이럴 킥 | kick_id, kick_type |
| `CompositionAnalysis` | 구도 분석 | composition_id, rot_score, gr_score |
| `MusicCluster` | 바이럴 음악 추적 | music_id, title, author, usage_count |

### 관계 (7개)

| 관계 | 설명 | 방향 |
|------|------|------|
| `EVOLVED_TO` | 진화 (Fork) | parent → child |
| `FORKED_FROM` | 포크 원본 | child → parent |
| `BELONGS_TO_CLUSTER` | 클러스터 소속 | item → cluster |
| `HAS_COMPOSITION` | 구도 분석 보유 | node → composition |
| `HAS_HOOK` | 훅 보유 | node → hook |
| `HAS_KICK` | 킥 보유 | node → kick |
| `USES_MUSIC` | 음악 사용 | OutlierItem → MusicCluster |

### Embedding 차원
- VDG: 3072 (gemini-embedding-001)
- Composition: 3072 (gemini-embedding-001)

---

## 2. 패턴 클러스터링 로직

### GraphRAGPatternMiner

**파일**: `app/services/graphrag_pattern_mining.py`

```python
class GraphRAGPatternMiner:
    # 기능:
    # 1. 벡터 유사도 검색 (Neo4j HNSW)
    # 2. 패턴 클러스터링
    # 3. 구도 개선 추천 생성
```

### 클러스터링 규칙 (Rule-based)

| 클러스터 | 조건 |
|----------|------|
| Rule of Thirds Focused | rot_score > 0.7 |
| Golden Ratio Focused | gr_score > 0.7 |
| Perspective (Vanishing Point) | vp_type != "none" |

### 추천 생성 로직

현재 분석 vs 유사 바이럴 패턴 평균 비교:
- 삼분할 점수 낮으면 → 삼분할 구도 활용 추천
- 황금비 점수 낮으면 → 황금비 활용 추천

---

## 3. 승격 → 분석 → 가이드 플로우

### 승격 (promote_outlier_core)

**파일**: `app/services/promote_service.py`

```
OutlierItem (크롤링)
    │
    ▼ promote_outlier_core()
    │
    ├── 1. RemixNode 생성
    │       - node_id 생성
    │       - layer = MASTER
    │       - permission = READ_ONLY
    │
    ├── 2. OutlierItem 상태 업데이트
    │       - status = PROMOTED
    │       - promoted_to_node_id = node.id
    │
    └── 3. VDG 분석 트리거 (auto_analyze=True)
            - analysis_status = "analyzing"
            - vdg_task_registry.submit()
```

### VDG 파이프라인

**파일**: `app/services/vdg_2pass/vdg_unified_pipeline.py`

```
┌─────────────────────────────────────────┐
│  Pass 1: UnifiedPass (Gemini 3.0 Pro)  │
│  - Hook clip: 10fps (정밀 microbeat)    │
│  - Full video: 1fps (전체 인과)         │
│  - 출력: 의미/인과/Plan Seed            │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Pass 2: CVMeasurementPass             │
│  - ffmpeg + OpenCV                      │
│  - 3개 MVP 메트릭:                      │
│    center_offset, brightness, blur      │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Merger: VDG Result                     │
│  - Semantic + CV 측정값 통합            │
│  - Deterministic IDs 생성               │
│  - Evidence 링크                        │
└─────────────────────────────────────────┘
```

### VDG Task 설정

```python
@celery_app.task(
    queue="vdg",              # crawler와 분리!
    max_retries=2,
    soft_time_limit=600,      # 10분
    time_limit=900,           # 15분 hard limit
    acks_late=True,
    reject_on_worker_lost=True,
)
```

### PipelineConfig 주요 설정

| 설정 | 기본값 | 설명 |
|------|--------|------|
| hook_clip_seconds | 4.0 | 훅 클립 길이 |
| hook_clip_fps | 10.0 | 훅 클립 FPS |
| full_video_fps | 1.0 | 전체 영상 FPS |
| enable_audio_mode | True | 오디오 분석 활성화 |
| enable_face_emotion | True | 얼굴 감정 인식 |

---

## 4. 발견된 주요 패턴

### 좋은 점 ✅
1. **SSoT 아키텍처**: PostgreSQL 중심, Neo4j는 캐시
2. **Queue 분리**: VDG와 crawler 완전 분리
3. **acks_late**: 안전한 태스크 완료 확인
4. **2-Pass 아키텍처**: AI(의미) + CV(측정) 분리

### 개선 가능 영역 ⚠️
1. **패턴 클러스터링**: 현재 규칙 기반 → ML 기반 가능
2. **추천 다양성**: 현재 구도 위주 → 오디오/훅 패턴 추천 확장 가능

---

## 6. Stuck Recovery 메커니즘

**파일**: `app/services/vdg_stuck_recovery.py`

### 설정
- `STUCK_THRESHOLD_MINUTES = 30` (30분 이상 analyzing → stuck 판정)
- Max retries: 3

### 상태 전이
```
analyzing (30분+ stuck)
    │
    ├── retry_count < 3 → failed_retryable → 자동 재시도
    └── retry_count >= 3 → failed_permanent → 영구 실패
```

### 주요 함수
| 함수 | 역할 |
|------|------|
| `get_stuck_items()` | 30분+ stuck 아이템 조회 |
| `recover_stuck_items()` | 상태 전이 + retry_count 증가 |
| `get_stuck_statistics()` | 통계 조회 (수정 없음) |

---

## 5. 다이어그램: 전체 플로우

```
[크롤러] TikTok/YouTube
    │
    ▼ crawl_tiktok_socialkit()
    │
[OutlierItem] ─→ SS/S tier 필터
    │
    ▼ auto_promote_outliers()
    │
[RemixNode] ─→ promote_outlier_core()
    │
    ▼ vdg_task_registry.submit()
    │
[VDG 분석] ─→ Pass 1 (Gemini) + Pass 2 (CV)
    │
    ▼ neo4j_sync.sync_remix_node()
    │
[Neo4j] ─→ 그래프 관계 생성
    │
    ▼ graphrag_pattern_mining
    │
[가이드 추천] ─→ 프론트엔드
```

---

*작성: 소미 🐱 | 2026-02-06 02:55 KST*
