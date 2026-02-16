---
name: komission
description: Komission Ops Core - OpenClaw 4-agent 모니터링/운영 도구. 태스크 조회, 핸드오프 추적, 정책 위반 감시, 일일 스탠드업 생성, 품질 메트릭 대시보드. Use when asked about Komission status, agent tasks, policy events, standups, or rework metrics.
---

# Komission OpenClaw Ops Core

## Quick Reference

| Item | Value |
|------|-------|
| Project | `/Users/ted/komission` |
| Backend | FastAPI (port 8000) |
| Frontend | Next.js 16 (port 3000) |
| Production API | `https://shorti.ai` |
| Local API | `http://localhost:8000` |
| Admin Dashboard | `/ops/openclaw` |
| API Key | `$KOMISSION_SCOUT_API_KEY` (env) |

## API Endpoints (Admin OpenClaw)

All require `Authorization: Bearer <token>` with admin role.

### Overview Metrics
```bash
curl -H "Authorization: Bearer $TOKEN" https://shorti.ai/api/v1/admin/openclaw/overview?days=7
```
Returns: `rework_rate`, `total_tasks`, `handoff_success_rate`, `avg_handoff_latency_ms`, `total_handoffs`, `policy_violations_count`

### Tasks
```bash
curl -H "Authorization: Bearer $TOKEN" https://shorti.ai/api/v1/admin/openclaw/tasks?limit=20&status=rework
```

### Handoffs
```bash
curl -H "Authorization: Bearer $TOKEN" https://shorti.ai/api/v1/admin/openclaw/handoffs?limit=20
```

### Policy Events
```bash
curl -H "Authorization: Bearer $TOKEN" https://shorti.ai/api/v1/admin/openclaw/policy-events?limit=20
```

### Standups
```bash
# List recent standups
curl -H "Authorization: Bearer $TOKEN" https://shorti.ai/api/v1/admin/openclaw/standups?limit=10

# Trigger standup generation
curl -X POST -H "Authorization: Bearer $TOKEN" https://shorti.ai/api/v1/admin/openclaw/standups/run
```

### Sessions
```bash
curl -H "Authorization: Bearer $TOKEN" https://shorti.ai/api/v1/admin/openclaw/sessions?limit=50
```

## 4-Agent Architecture

| Agent | Role | Allowed Actions |
|-------|------|-----------------|
| **Director** | Orchestrator | delegate, synthesize, final_decision ONLY |
| **Scout** | Trend/Code scanning | scan_trends, fetch_trends, cluster_analysis |
| **Analytics** | Metrics/Reports | compute_kpis, cohort_analysis, generate_alert |
| **Memory** | Knowledge management | update_memory, read_user_context, memory_search |

### Director Hardguard Rules
- Director CANNOT directly execute domain actions
- Blocked actions auto-redirect to correct agent (PolicyService routing map)
- All violations logged as `policy_blocked` events

### Memory Isolation
- Key schema: `{agent}:{scope}:{key}`
- Agents can only RW own raw memory
- Director can READ other agents' `summary` scope only
- Cross-agent raw access = `memory_violation` event

## Useful Queries (Production via Neon)

```sql
-- Today's task summary
SELECT owner_agent, status, COUNT(*)
FROM openclaw_tasks
WHERE created_at > CURRENT_DATE
GROUP BY owner_agent, status;

-- Recent policy violations
SELECT event_type, actor_agent, details, created_at
FROM openclaw_policy_events
ORDER BY created_at DESC LIMIT 10;

-- Rework rate (7 days)
SELECT
  COUNT(*) FILTER (WHERE status = 'rework')::float / NULLIF(COUNT(*), 0) as rework_rate
FROM openclaw_tasks
WHERE created_at > NOW() - INTERVAL '7 days';
```

## Development Commands

```bash
# Backend test
cd /Users/ted/komission/backend && source venv/bin/activate && pytest --testmon -q

# Frontend build
cd /Users/ted/komission/frontend && bun run build

# Run server
cd /Users/ted/komission/backend && source venv/bin/activate && uvicorn app.main:app --reload
```

## When to Use This Skill

- "Komission 상태 어때?" -> Overview metrics API
- "오늘 태스크 뭐 있어?" -> Tasks API
- "정책 위반 있었어?" -> Policy events API
- "스탠드업 만들어" -> POST standups/run
- "재작업률 어때?" -> Overview metrics (rework_rate)
- "핸드오프 성공률?" -> Overview metrics (handoff_success_rate)
