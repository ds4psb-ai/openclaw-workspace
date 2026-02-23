# Coding Conventions - Komission

Rules extracted from project CLAUDE.md. Follow these when implementing code changes.

---

## VDG Schema SSoT (CRITICAL)

```python
# NEVER access VDG data directly. Always use the normalizer.
from app.services.vdg_schema_normalizer import normalize_vdg_schema
normalized = normalize_vdg_schema(vdg_data)
```

- 23 canonical fields mapped in normalizer
- `vdg_data_access.py` provides dual-read (vdg_analyses → gemini_analysis fallback)
- `flash_prescan` JSONB consolidates 5 old columns

---

## Testing Rules

- **Minimum 5 tests** per new service/function
- Run after every change: `pytest --testmon`
- Parallel: `pytest --testmon -n auto`
- Frontend build check: `cd frontend && bun run build`
- Never mark a task complete without proving it works
- Test fixtures use `db_session` with transaction rollback
- OutlierItem tests need `test_source` fixture (FK to OutlierSource)

---

## Code Style

- Clean, readable code with minimal comments
- Comment only non-obvious logic
- Simple solutions over clever ones
- Follow existing project conventions
- No hallucination: verify files/functions with Glob/Read before use

---

## Git Rules

- Concise commit messages explaining "why" not "what"
- Stage specific files (not `git add .`)
- Atomic commits: one logical change per commit
- Code comments and commit messages in English

---

## Deployment Rules

- **NEVER push without Ted's explicit approval**
- Backend: `git push origin main` → Railway auto-deploy
- Frontend: git push → Vercel auto-deploy
- VPS: rsync (see fleet-runbook.md)
- Urgent: `railway up` or `vercel redeploy`

---

## DB Rules (Neon)

- Production DB via Neon MCP only (projectId: `divine-firefly-43994087`)
- DDL changes: run via Neon MCP, then stamp alembic_version
- Never run Alembic DDL on Railway (will fail due to role ownership)
- MV refresh: use SECURITY DEFINER functions

---

## State Machine

- ALL status transitions via `analysis_state_machine.py:transition()`
- Include `reason="..."` parameter for every transition
- Use `force=True` only for admin/recovery operations
- Side effects (stuck_at, retry_count, last_error) are auto-managed

---

## Error Handling

- Use `KomissionError` hierarchy from `app/exceptions.py`
- No bare `except:` — always specify exception type
- Sub-session pattern for Neon 5min timeout
- 39+ intentional error handling markers in codebase
