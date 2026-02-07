# Komission 파이프라인 전체 분석 보고서

**작성일:** 2026-02-05
**작성자:** 보미 🐰 (+ 소미 🐱 합류 예정)
**목적:** 코드 수정 없이 전체 파이프라인 조사

---

## 📁 분석 범위

| 영역 | 파일 수 | 총 라인 |
|------|---------|---------|
| VDG Services | 22개 | ~8,000줄 |
| Neo4j Services | 4개 | ~3,000줄 |
| Pattern Services | 6개 | ~2,500줄 |
| Celery Workers | 6개 | ~4,000줄 |

---

## 🔥 1. VDG 파이프라인

### 1.1 메인 파일: vdg_unified_pipeline.py (1574줄)

**실행 흐름:**
```
VDGUnifiedPipeline.run()
├── Phase 1 (병렬, 4 threads)
│   ├── _run_audio → AudioAnalysisResult
│   ├── _run_audio_semantic → AudioSemanticResult
│   ├── _run_motion → MotionAnalysisResult
│   └── _run_fer → FaceEmotionResult
├── Phase 3 (병렬, 2 threads)
│   ├── _run_cv_pass → CVPassResult
│   └── _run_visual_pass → VisualPassResult
├── Phase 4 (병렬, 2 threads)
│   ├── _run_composition → CompositionResult
│   └── _run_vanishing_point → VanishingPointResult
└── _merge_results() → VDGUnifiedResult
```

### 1.2 DB 저장: vdg_db_saver.py

**저장 테이블:**
- `viral_kicks` - 개별 킥 (timestamp, analysis)
- `keyframe_evidences` - CV 검증 키프레임
- `comment_evidences` - 댓글 증거

**카테고리 정규화:**
10개 유효 카테고리: beauty, meme, food, fashion, art, sports, tech, entertainment, game, fandom

### 1.3 Recovery 시스템

| 파일 | 역할 |
|------|------|
| vdg_stuck_recovery.py | 15분+ stuck 상태 복구 |
| vdg_self_healing.py | 자동 복구 |
| vdg_reanalysis_queue.py | visual_empty/failed 재분석 |
| vdg_post_processing_recovery.py | 후처리 복구 |

---

## 🗃️ 2. Neo4j 연동

### 2.1 Neo4jSyncService (1572줄)

**Sync 메서드:**
- `sync_remix_node()` - 리믹스 노드
- `sync_outlier_item()` - 아웃라이어 아이템
- `sync_pattern_cluster()` - 패턴 클러스터
- `sync_hook_cluster()` - 훅 클러스터
- `sync_viral_kick()` - 바이럴 킥
- `sync_composition_analysis()` - 구성 분석
- `sync_vdg_analysis()` - VDG 분석

**검색 메서드:**
- `search_similar_compositions()` - 유사 구도 검색
- `search_similar_vdg()` - 유사 VDG 검색
- `get_similar_lighting_recommendations()` - 조명 추천
- `get_similar_hook_recommendations()` - 훅 추천

**벡터 인덱스:**
- `create_composition_vector_index()` - 구도 벡터 인덱스
- `create_vdg_embedding_index()` - VDG 임베딩 인덱스

---

## 🔄 3. 승격 플로우

### 3.1 promote_service.py

```python
async def promote_outlier_core(db, item, created_by, auto_analyze=True):
    # 1. RemixNode 생성
    node = RemixNode(
        node_id=await generate_remix_node_id(db),
        title=item.title,
        source_video_url=item.video_url,
        platform=item.platform,
        layer=NodeLayer.MASTER,
    )
    
    # 2. 상태 변경
    item.status = OutlierItemStatus.PROMOTED
    item.promoted_to_node_id = node.id
    
    # 3. VDG 분석 시작
    if auto_analyze:
        item.analysis_status = "analyzing"
        await vdg_task_registry.submit(...)
```

### 3.2 전체 승격 → 분석 흐름

```
1. OutlierItem (PENDING)
   ↓ promote_outlier_core()
2. RemixNode 생성
   ↓
3. VDG 분석 시작 (vdg_task_registry.submit)
   ↓
4. VDGUnifiedPipeline.run()
   ↓
5. vdg_db_saver.save_vdg_to_db()
   ↓
6. Neo4j sync (neo4j_sync_service)
   ↓
7. 패턴 클러스터링 (graphrag_pattern_mining)
   ↓
8. 가이드 생성 (?)
```

---

## 🎯 4. 패턴 클러스터링

### GraphRAGPatternMiner

```python
class GraphRAGPatternMiner:
    async def find_similar_compositions(kick_analysis):
        # 1. 킥 분석 → 임베딩
        # 2. Neo4j 벡터 유사도 검색
        # 3. 패턴 클러스터링
        # 4. 구도 개선 추천 생성
```

**결과 타입:**
- `SimilarPattern` - 유사 패턴
- `PatternCluster` - 패턴 클러스터
- `PatternMiningResult` - 마이닝 결과

---

## ⚙️ 5. Celery Beat Schedule

| Task | 주기 | Queue |
|------|------|-------|
| vdg-stuck-recovery | 15분마다 | maintenance |
| vdg-reanalysis-queue | 30분마다 | vdg |
| vdg-drift-daily-report | 매일 09:00 KST | maintenance |
| crawler-tiktok-socialkit | 6시간마다 (:15) | crawler |
| crawler-tiktok-meme | 6시간마다 (:30) | crawler |
| scout-outliers-6h | 6시간마다 | crawler |
| auto-promote-outliers | 6시간마다 (:30) | crawler |

---

## ❓ 6. 추가 조사 필요

### 6.1 "가이드" 기능 연동 ✅ 분석 완료

**생성 플로우:**
```
VDG Pipeline
    ↓ VDGv4 데이터
DirectorCompiler.compile() [vdg_2pass/director_compiler.py]
    ↓ DirectorPack
    ├── dna_invariants (불변 규칙)
    ├── mutation_slots (가변 영역)
    └── forbidden_mutations (금지)
    ↓
director_pack_cache [director_pack_cache.py]
    ↓ node.director_pack_cache에 저장
extract_shooting_guide_from_director_pack() [vdg_extractor.py:1731]
    ↓ 가이드 UI 데이터 반환
        {
            "invariant": [...],   # 필수 요소
            "variable": [...],    # 변주 가능
            "do_not": [...],      # 금지 사항
            "checkpoints": [...]  # 체크포인트
        }
```

**코치 메시지 도메인:**
- 🎣 hook, ⏱️ timing, 📷 composition, 🎵 pacing, 🎤 audio

### 6.2 에러 핸들링 검토 ✅

**VDG 파이프라인 에러 핸들링:**

| 항목 | 현재 상태 | 평가 |
|------|----------|------|
| CV timeout | graceful degradation | ✅ |
| Visual fatal | re-raise | ✅ |
| Phase별 timeout | 설정됨 | ✅ |
| 메트릭 기록 | increment_failure() | ✅ |

**보안 검토:**
| 항목 | 현재 상태 | 평가 |
|------|----------|------|
| 입력 검증 | validate_* 함수들 | ✅ |
| SQL Injection | SQLAlchemy ORM | ✅ |
| Quality Gate | 결과 검증 레이어 | ✅ |

**잠재적 이슈:**
1. CV timeout vs Visual fatal 처리 방식 불일치
2. Phase 1 전체 실패 시 진행 여부 불명확

**2026 베스트 프랙티스:**
- Python 3.11+ `ExceptionGroup` 사용 권장
- 병렬 실행 시 여러 예외 동시 처리

### 6.3 Neo4j 스키마
- 노드 타입: RemixNode, OutlierItem, PatternCluster, HookCluster, ViralKick
- 엣지 타입: FORK, SIMILAR_LIGHTING, SIMILAR_HOOK, BELONGS_TO_CLUSTER

---

## 📋 7. 다음 단계

1. [ ] Neo4j 스키마 상세 분석
2. [ ] 가이드 API 엔드포인트 찾기
3. [ ] 에러 로그 분석
4. [ ] 프론트엔드 연동 확인

---

## 🐱 8. 소미 분석 결과 (Neo4j)

### 8.1 아키텍처
- **PostgreSQL** = SSoT (Single Source of Truth)
- **Neo4j** = 읽기 전용 캐시 (eventual consistency)

### 8.2 노드 레이블 (8개)
| 레이블 | 설명 |
|--------|------|
| RemixNode | VDG 분석 결과 |
| OutlierItem | 크롤링된 아웃라이어 |
| PatternCluster | 패턴 클러스터 |
| HookCluster | 훅 클러스터 |
| ViralKick | 바이럴 킥 |
| CompositionAnalysis | 구성 분석 |
| MusicCluster | 바이럴 음악 추적 |

### 8.3 관계 (7개)
- `EVOLVED_TO` - 진화 관계
- `FORKED_FROM` - 포크 관계
- `BELONGS_TO_CLUSTER` - 클러스터 소속
- `HAS_COMPOSITION` - 구성 보유
- `HAS_HOOK` - 훅 보유
- `HAS_KICK` - 킥 보유
- `USES_MUSIC` - 음악 사용

---

## 📊 통합 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────┐
│                  DATA FLOW                       │
├─────────────────────────────────────────────────┤
│  Crawler (TikTok/YouTube)                       │
│       ↓                                          │
│  OutlierItem (PostgreSQL)                       │
│       ↓ promote_outlier_core()                  │
│  RemixNode (PostgreSQL)                         │
│       ↓ VDG Pipeline                            │
│  ┌──────────────────────────────────┐           │
│  │ Phase 1: Audio/Motion/FER        │           │
│  │ Phase 3: CV/Visual               │           │
│  │ Phase 4: Composition/VP          │           │
│  └──────────────────────────────────┘           │
│       ↓                                          │
│  viral_kicks, keyframe_evidences (PostgreSQL)   │
│       ↓ neo4j_sync_service                      │
│  ┌──────────────────────────────────┐           │
│  │ Neo4j (읽기 캐시)                 │           │
│  │ - RemixNode, ViralKick           │           │
│  │ - PatternCluster, HookCluster    │           │
│  │ - MusicCluster                   │           │
│  └──────────────────────────────────┘           │
│       ↓ graphrag_pattern_mining                 │
│  패턴 추천 / 가이드                             │
└─────────────────────────────────────────────────┘
```

---

*보미🐰 + 소미🐱 공동 분석 진행 중*
