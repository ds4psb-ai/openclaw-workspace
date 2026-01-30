#!/usr/bin/env bash
set -euo pipefail

cd /Users/ted/.openclaw/workspace

while true; do
  ts=$(date '+%F %T %Z')
  git pull origin main >/dev/null 2>&1 || true

  # Show any new message filenames (without spamming contents)
  new_bomi=$(ls -1 messages/to_bomi 2>/dev/null | grep -v '^\.gitkeep$' || true)
  new_somi=$(ls -1 messages/to_somi 2>/dev/null | grep -v '^\.gitkeep$' || true)

  echo "[$ts] sync ok | to_bomi: $(echo "$new_bomi" | wc -l | tr -d ' ') files | to_somi: $(echo "$new_somi" | wc -l | tr -d ' ') files"

  sleep 300
done
