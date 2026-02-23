---
name: coding-agent
description: Run Codex CLI, Claude Code, OpenCode, or Pi Coding Agent via background process for programmatic control.
metadata: {"clawdbot":{"emoji":"🧩","requires":{"anyBins":["claude","codex","opencode","pi"]}}}
---

# Coding Agent Skill

Launch and manage coding agents (Claude Code, Codex CLI, OpenCode, Pi) as background processes with session tracking.

## Supported Agents

| Agent | Launch Command | Best For |
|-------|---------------|----------|
| Claude Code | `claude "task"` | Complex multi-file changes |
| Codex CLI | `codex exec --full-auto "task"` | Autonomous coding |
| OpenCode | `opencode run "task"` | Quick edits |
| Pi | `pi "task"` | Lightweight tasks |

## Usage Pattern

### 1. Start Session

```bash
# Claude Code (recommended for komission)
cd <workdir> && claude --print "Your task description here" &
SESSION_PID=$!

# Codex CLI
cd <workdir> && codex exec --full-auto "task" &
SESSION_PID=$!
```

### 2. Monitor Session

```bash
# Check if running
ps -p $SESSION_PID

# Tail output
tail -f /tmp/coding-session-$SESSION_PID.log
```

### 3. Kill Session

```bash
kill $SESSION_PID
```

## Parallel Workflow (Git Worktrees)

For multiple independent tasks:

```bash
# Create worktrees
git worktree add /tmp/task-1 -b fix/task-1
git worktree add /tmp/task-2 -b fix/task-2

# Launch agents in parallel
cd /tmp/task-1 && claude --print "Fix bug X" &
cd /tmp/task-2 && claude --print "Add feature Y" &

# After completion, merge back
git checkout main
git merge fix/task-1
git merge fix/task-2

# Cleanup
git worktree remove /tmp/task-1
git worktree remove /tmp/task-2
```

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `workdir` | Working directory for the agent |
| `task` | Natural language task description |
| `agent` | Which agent to use (claude, codex, opencode, pi) |
| `timeout` | Max execution time in seconds |

## Tips

- Use `claude --print` for non-interactive single-shot tasks
- Use `codex exec --full-auto` for fully autonomous mode
- Always specify absolute paths for `workdir`
- Check agent output before committing changes
