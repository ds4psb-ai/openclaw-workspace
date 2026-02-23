# Fleet Runbook - VPS Operations Manual

## Fleet Topology

| Host | IP | Tailscale | Role | Processes |
|------|----|-----------|------|-----------|
| VPS1 (brain-cell1) | 178.128.103.162 | brain-cell1 | Head | producer_loop, primary_observer |
| VPS2 (discovery-cell2) | 165.232.165.189 | discovery-cell2 | Worker+Shadow | worker_loop, shadow_analyzer |
| VPS3 (quality-cell3) | 158.247.230.78 | quality-cell3 | Worker | worker_loop |
| VPS4 (ops-cell4) | 158.247.241.31 | ops-cell4 | Worker | worker_loop |

- All VPS: System Python 3.12 (no venv)
- pip install requires `--break-system-packages`
- Code paths: VPS1 `/opt/a0-head/`, VPS2-4 `/opt/a0-worker/`
- Shared module nested: `/opt/a0-{head,worker}/shared/`
- Not a git repo — files deployed via rsync

---

## Health Check Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Disk usage | > 80% | [ALERT] Report + identify large files |
| Memory usage | > 90% | [ALERT] Report + check for leaks |
| worker_loop missing | Any VPS | [ALERT] Auto-restart immediately |
| producer_loop missing | VPS1 | [ALERT] Auto-restart via restart.sh |
| primary_observer missing | VPS1 | [ALERT] Auto-restart via restart.sh |

Expected healthy state: `worker_loop 4/4 running`.

---

## Recovery Procedures

### Worker Down (VPS2/3/4)

```bash
# Check which worker is down
ssh root@<IP> "pgrep -f worker_loop || echo 'DOWN'"

# Restart
ssh root@<IP> "cd /opt/a0-worker && bash start.sh"

# Verify
ssh root@<IP> "pgrep -f worker_loop && echo 'OK'"
```

### VPS2 Full Restart (worker + shadow)

```bash
ssh root@165.232.165.189 "cd /opt/a0-worker && bash restart.sh"
# restart.sh kills worker_loop + shadow_analyzer, restarts both
```

### VPS1 Head Restart (producer + observer)

```bash
ssh root@178.128.103.162 "cd /opt/a0-head && bash restart.sh"
# restart.sh kills producer_loop + primary_observer, restarts both
```

### Docker Container Unresponsive

```bash
ssh root@<IP> "docker restart a0-main"
```

### Recovery Failed

Report to Ted via Telegram. Do not retry more than 2 times.

---

## Deployment (rsync)

### VPS1 (brain-cell1) — Head

```bash
rsync -avz --exclude='.env' --exclude='start.sh' --exclude='restart.sh' --exclude='start-vps*.sh' --exclude='__pycache__' --exclude='*.pyc' --exclude='start.sh.env' openclaw/a0-head/ root@178.128.103.162:/opt/a0-head/

rsync -avz --exclude='__pycache__' --exclude='*.pyc' openclaw/shared/ root@178.128.103.162:/opt/a0-head/shared/

ssh root@178.128.103.162 "cd /opt/a0-head && bash restart.sh"
```

### VPS2 (discovery-cell2) — Worker+Shadow

```bash
rsync -avz --exclude='.env' --exclude='start.sh' --exclude='restart.sh' --exclude='start-vps*.sh' --exclude='__pycache__' --exclude='*.pyc' --exclude='start.sh.env' openclaw/a0-worker/ root@165.232.165.189:/opt/a0-worker/

rsync -avz --exclude='__pycache__' --exclude='*.pyc' openclaw/shared/ root@165.232.165.189:/opt/a0-worker/shared/

ssh root@165.232.165.189 "cd /opt/a0-worker && bash restart.sh"
```

### VPS3 (quality-cell3) — Worker

```bash
rsync -avz --exclude='.env' --exclude='start.sh' --exclude='restart.sh' --exclude='start-vps*.sh' --exclude='__pycache__' --exclude='*.pyc' --exclude='start.sh.env' openclaw/a0-worker/ root@158.247.230.78:/opt/a0-worker/

rsync -avz --exclude='__pycache__' --exclude='*.pyc' openclaw/shared/ root@158.247.230.78:/opt/a0-worker/shared/

ssh root@158.247.230.78 "cd /opt/a0-worker && bash start.sh"
```

### VPS4 (ops-cell4) — Worker

```bash
rsync -avz --exclude='.env' --exclude='start.sh' --exclude='restart.sh' --exclude='start-vps*.sh' --exclude='__pycache__' --exclude='*.pyc' --exclude='start.sh.env' openclaw/a0-worker/ root@158.247.241.31:/opt/a0-worker/

rsync -avz --exclude='__pycache__' --exclude='*.pyc' openclaw/shared/ root@158.247.241.31:/opt/a0-worker/shared/

ssh root@158.247.241.31 "cd /opt/a0-worker && bash start.sh"
```

**Note**: VPS3/4 use `start.sh` (no `restart.sh` available).

---

## Incident Log Format

When auto-recovering, log to `memory/YYYY-MM-DD.md`:

```
[HH:MM] [ALERT] VPS3 worker_loop not found → restarted via start.sh → OK (pid 12345)
```
