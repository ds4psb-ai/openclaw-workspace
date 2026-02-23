---
name: agent-zero-bridge
description: Bridge between OpenClaw and Agent Zero on VPS1 (brain-cell1). Delegate tasks to A0 fleet and retrieve results.
metadata: {"clawdbot":{"emoji":"🔗"}}
---

# Agent Zero Bridge

Delegate tasks to the Agent Zero fleet running on VPS1 (brain-cell1) and retrieve results.

## Architecture

```
Telegram → OpenClaw (Mac) → SSH → VPS1 (brain-cell1) → Agent Zero (Docker)
                                                      → VPS2-4 Workers
```

## Connection Details

| Component | Address |
|-----------|---------|
| A0 Web UI | http://brain-cell1:50080 (Tailscale) |
| A0 Docker | a0-main container on VPS1 |
| VPS1 SSH | root@brain-cell1 (Tailscale) or root@178.128.103.162 |

## Usage

### Delegate a task to Agent Zero

When the user says "delegate to a0: <task>", execute via SSH:

```bash
ssh root@brain-cell1 "curl -sf -X POST http://localhost:50080/api/message \
  -H 'Content-Type: application/json' \
  -d '{\"message\": \"<task>\"}'"
```

### Check fleet status

```bash
# All workers
for vps in brain-cell1 discovery-cell2 quality-cell3 ops-cell4; do
  echo "=== $vps ==="
  ssh root@$vps "ps aux | grep -E '(worker_loop|producer_loop|primary_observer|shadow_analyzer)' | grep -v grep"
done
```

### Restart a worker

```bash
# Worker (VPS2-4)
ssh root@<hostname> "cd /opt/a0-worker && bash start.sh"

# Head (VPS1)
ssh root@brain-cell1 "cd /opt/a0-head && bash restart.sh"

# Agent Zero container
ssh root@brain-cell1 "docker restart a0-main"
```

## Fleet Topology

| VPS | Hostname | Role | Lanes |
|-----|----------|------|-------|
| VPS1 | brain-cell1 | Producer + Observer + A0 | - |
| VPS2 | discovery-cell2 | Worker + Shadow | discovery |
| VPS3 | quality-cell3 | Worker | quality |
| VPS4 | ops-cell4 | Worker | ops |
