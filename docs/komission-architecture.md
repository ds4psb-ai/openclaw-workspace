# Komission Architecture Reference

## Stack

- **Backend**: FastAPI + PostgreSQL + Neo4j + Redis + Gemini
- **Frontend**: Next.js 16 + React 19 + Bun
- **Mobile**: Expo Router 4 + React Native
- **DB**: Neon PostgreSQL (production), Neo4j (graph), Redis (cache)

---

## VDG Pipeline Flow

```
OutlierItem (pending)
    ↓
[Stage 1: Flash Pre-scan]
  - Gemini Flash (1 call replaces 5 passes)
  - librosa audio analysis (parallel)
  - Output: flash_prescan JSONB (audio/emotion/motion/composition/vp/lighting/key_moments/meta)
    ↓
[Stage 2: Pro Deep Analysis]
  - Pass A: Gemini Pro thinking=high (structural analysis)
  - Pass B: Gemini Pro thinking=low (creative synthesis)
  - CV Pass: deterministic measurements (blur, brightness, motion_proxy)
    ↓
vdg_saved → post_processing → completed
```

### State Machine (9 states)

```
pending → analyzing → vdg_saved → completed
                   ↘ comments_pending_review → comments_ready → analyzing
                   ↘ comments_failed → analyzing
                   ↘ failed_retryable → analyzing
                   ↘ failed_permanent (terminal)
vdg_saved → post_processing_failed → completed | analyzing
```

All transitions via `analysis_state_machine.py:transition()`.

---

## Core Services

| File | Purpose | Lines |
|------|---------|-------|
| `app/routers/outliers/outliers_main.py` | Outlier endpoints | ~3200 |
| `app/services/vdg_pipeline_orchestrator.py` | VDG pipeline orchestration | ~840 |
| `app/services/viral_kick_service.py` | Viral kick extraction | ~100 |
| `app/services/vdg_2pass/vdg_unified_pipeline.py` | 2-Pass A/B orchestrator | — |
| `app/services/vdg_2pass/flash_prescan.py` | Flash Pre-scan (Stage 1) | — |
| `app/services/vdg_schema_normalizer.py` | 23 canonical fields SSoT | — |
| `app/services/vdg_data_access.py` | Dual-read layer | — |
| `app/services/analysis_state_machine.py` | State transitions | — |
| `app/services/hybrid_search.py` | L1/L2 Vector+BM25+Reranker | — |
| `app/services/audio_coach.py` | Gemini Live coaching | — |
| `app/exceptions.py` | KomissionError hierarchy | — |

---

## Key DB Tables

| Table | Purpose |
|-------|---------|
| `outlier_items` | Source videos with viral scores |
| `remix_nodes` | VDG analysis graph nodes |
| `vdg_analyses` | Full VDG analysis results |
| `viral_kicks` | Extracted viral kick moments |
| `pattern_clusters` | Grouped pattern analysis |
| `notebook_library` | Pattern library entries |
| `keyframe_evidences` | Visual evidence frames |
| `composition_analyses` | Composition breakdown |
| `comment_evidences` | Comment-based evidence |

---

## VDG Schema SSoT

23 canonical fields mapped in `vdg_schema_normalizer.py`.

```python
# ALWAYS use the normalizer — never access raw JSON
from app.services.vdg_schema_normalizer import normalize_vdg_schema
normalized = normalize_vdg_schema(vdg_data)
```

`flash_prescan` consolidated JSONB contains:
- `audio` — semantic audio analysis
- `emotion` — face emotion recognition
- `motion` — motion intensity/patterns
- `composition` — visual composition
- `vp` — vanishing point analysis
- `lighting` — lighting conditions
- `key_moments` — timestamp-based highlights
- `meta` — processing metadata

---

## Caching Strategy

| Endpoint | TTL | Notes |
|----------|-----|-------|
| `/home/for-you` (anon) | 60s | Trending |
| `/home/for-you` (user) | 300s | Personalized |
| `/home/campaigns` | 120s | Brand campaigns |
| `/home/hooks` | 180s | MV-based |
| `/home/patterns` | 180s | MV-based |
| `/outliers/items/{id}` | 300s | Item detail |

Warmup: 50s interval, `app/main.py:periodic_warmup()`.
DirectorPack: pre-computed at VDG save time, stored in `remix_nodes.director_pack_cache`.

---

## Key Terminology

| Term | Definition |
|------|------------|
| Outlier | Video outperforming creator's average |
| VDG 2-Pass | Pass A (structural) → Pass B (creative) → CV (deterministic) |
| Flash Pre-scan | Single Gemini Flash call replacing 5 separate passes |
| Director Pack | Compiled coaching rules from VDG analysis |
| Signal → Invariant | Data-driven rule promotion (70% → DNA) |
| Pattern DNA | VDG summary as primary source |
