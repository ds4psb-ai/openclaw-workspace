# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

### Komission

- Repo: /Users/ted/komission
- Backend test: `cd /Users/ted/komission/backend && source venv/bin/activate && pytest --testmon`
- Frontend build: `cd /Users/ted/komission/frontend && bun run build`
- Claude Code: `claude --print "task"` (non-interactive mode)
- Codex: `codex exec --full-auto "task"`
- Deploy backend: `cd /Users/ted/komission && git push origin main`
- Deploy VPS (shared):
  ```bash
  rsync -avz --exclude='.env' --exclude='__pycache__' openclaw/shared/ root@178.128.103.162:/opt/a0-head/shared/
  ssh root@178.128.103.162 "cd /opt/a0-head && bash restart.sh"
  ```

### SSH Hosts

| Host | IP | Tailscale | Role |
|------|----|-----------|------|
| VPS1 (brain-cell1) | root@178.128.103.162 | brain-cell1 | producer + observer |
| VPS2 (discovery-cell2) | root@165.232.165.189 | discovery-cell2 | worker + shadow |
| VPS3 (quality-cell3) | root@158.247.230.78 | quality-cell3 | worker |
| VPS4 (ops-cell4) | root@158.247.241.31 | ops-cell4 | worker |

### Fleet Recovery

- Worker down: `ssh root@<IP> "cd /opt/a0-worker && bash start.sh"`
- VPS1 full restart: `ssh root@178.128.103.162 "cd /opt/a0-head && bash restart.sh"`
- Agent Zero unresponsive: `docker restart a0-main`
- Recovery failed: Report to Telegram, await manual intervention
