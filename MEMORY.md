# MEMORY.md - Somi Domain Knowledge

*Operational knowledge for Komission DevOps. Updated incrementally.*

---

## Fleet Topology

| Host | IP | Tailscale | Role | Processes |
|------|----|-----------|------|-----------|
| VPS1 (brain-cell1) | 178.128.103.162 | brain-cell1 | Head | producer_loop, primary_observer |
| VPS2 (discovery-cell2) | 165.232.165.189 | discovery-cell2 | Worker+Shadow | worker_loop, shadow_analyzer |
| VPS3 (quality-cell3) | 158.247.230.78 | quality-cell3 | Worker | worker_loop |
| VPS4 (ops-cell4) | 158.247.241.31 | ops-cell4 | Worker | worker_loop |

- System Python 3.12 (no venv), pip requires `--break-system-packages`
- Code paths: VPS1 `/opt/a0-head/`, VPS2-4 `/opt/a0-worker/`
- Shared module: `/opt/a0-{head,worker}/shared/`
- Not a git repo — deploy via rsync

---

## VDG Pipeline (State Machine)

```
pending → analyzing → vdg_saved → completed
                   ↘ comments_pending_review → comments_ready → analyzing
                   ↘ comments_failed → analyzing
                   ↘ failed_retryable → analyzing
                   ↘ failed_permanent (terminal)
vdg_saved → post_processing_failed → completed | analyzing
```

- 9 states, all transitions in `app/services/analysis_state_machine.py`
- Use `await transition(item, AnalysisStatus.XXX, reason="...")` for ALL changes
- `force=True` for admin/recovery from any state
- 2-stage pipeline: Stage1 (Flash+librosa parallel) → Stage2 (Pro Deep)
- Flash Pre-scan replaces 5 passes: Audio, Motion, FER, VP, Lighting

---

## VDG Schema SSoT

- 23 canonical fields in `vdg_schema_normalizer.py`
- `flash_prescan` JSONB: audio/emotion/motion/composition/vp/lighting/key_moments/meta
- Always use `normalize_vdg_schema()` — never access raw JSON
- `vdg_data_access.py`: dual-read (vdg_analyses → gemini_analysis fallback)

---

## Cascade Delete Order (26 steps)

FK dependency chain for OutlierItem re-analysis cleanup.
Full order in `backend/app/routers/outliers/delete.py` → `_cascade_cleanup_promoted_item()`.
Key rule: all DELETEs first, pending reset LAST (avoids race condition).

---

## Deployment Paths

| Target | Method | Command |
|--------|--------|---------|
| Backend (Railway) | git push | `git push origin main` (auto-deploy) |
| Frontend (Vercel) | git push | Auto-deploy on main push |
| VPS Fleet | rsync | See `docs/fleet-runbook.md` |

- Vercel: `frontend` project, Root Directory = `frontend`
- CLI upload (`vercel --prod`) fails — use git-based deploy or `vercel redeploy`

---

## DB Constraints (Neon)

- Production DB: Neon MCP, projectId = `divine-firefly-43994087`
- Tables owned by `neondb_owner`, app connects as `app_rls_XXX`
- `app_rls_XXX` CANNOT `SET ROLE neondb_owner` → Alembic DDL always fails on Railway
- Solution: Run DDL via Neon MCP, then stamp `alembic_version`
- MV refresh: SECURITY DEFINER functions (neondb_owner privileges)
  - `refresh_pattern_cluster_stats_fn()`, `refresh_hook_type_stats_fn()`
  - New MVs: create function + GRANT + add to `_REFRESH_FUNCTIONS` dict

---

## API Keys

### Shorti.ai
- Key: `9101273f44ba1aceff8d593b2d183ab08ca272721b48bd58921def75f999b39e`
- Endpoints: outliers, for-you, patterns/stats, search/unified, scout/promote

---

## Ted's Projects

| Project | Status | Description |
|---------|--------|-------------|
| Komission | Active | Short-form viral intelligence platform (VDG) |
| Vivid (Crebit Studio) | Active | AI content generation platform |

---

## Recent Incidents

*(Auto-updated on recovery. Format: date, issue, action, result)*

---

*Last updated: 2026-02-23 by Somi*
