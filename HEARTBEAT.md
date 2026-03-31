# HEARTBEAT.md - Periodic Check Protocol

## On Every Heartbeat (30min)

### 1. Git Sync
```bash
cd /Users/ted/.openclaw/workspace && git pull
```

### 2. Message Check
- Check `messages/to_somi/` for new files → process them

### 3. Task Queue
- Check `tasks/QUEUE.md` for assigned tasks
- Prioritize by urgency

### 4. Fleet Health (cron-assisted)
- Fleet health cron runs every 30min independently
- On heartbeat: check cron output for any alerts
- If cron reports issues: execute recovery per `docs/fleet-runbook.md`
- Do NOT duplicate the health check if cron already ran recently

### 5. Status Update
- Update `STATUS.md` if working on something

---

## Coding Request Handling

When Ted asks for code changes:
1. Use coding-agent skill with workdir `/Users/ted/komission`
2. Read relevant files before making changes
3. Run `pytest --testmon` after implementation
4. Run `bun run build` for frontend changes
5. Report results with pass/fail counts
6. Never push — wait for Ted's approval

---

## Auto-Recovery Protocol

When fleet issues are detected (by cron or observation):
1. Execute recovery immediately (no approval needed for restarts)
2. Log incident in `memory/YYYY-MM-DD.md`:
   ```
   [HH:MM] [ALERT] description → action taken → result
   ```
3. Report to Ted via Telegram with concise summary
4. If recovery fails after 2 attempts: escalate to Ted

---

## Check Cadence
- Normal: every 30 minutes
- Urgent files (`urgent_*`): process immediately
- Fleet alerts: act immediately

## Last Check
- Time: 2026-03-31 03:39 KST
- Result: Git synced. VPS3/VPS4 still unreachable (Vultr - already escalated #918). VPS1/VPS2 OK per memory log. SSH from Mac failing (key issue, not fleet).
