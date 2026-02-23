---
name: komission
description: Komission 프로젝트 개발. Use for any coding, testing, deployment, or debugging work in /Users/ted/komission/.
---

# Komission Dev Skill

## Quick Reference

| 항목 | 값 |
|------|-----|
| 프로젝트 | `/Users/ted/komission` |
| Backend | FastAPI (port 8000), venv at backend/venv |
| Frontend | Next.js 16, React 19 (port 3000), bun |
| DB | PostgreSQL :5434, Neo4j :7687, Redis :6379 |

## 필수 검증 명령어

```bash
# Backend 테스트
cd /Users/ted/komission/backend && source venv/bin/activate && pytest --testmon

# Frontend 빌드
cd /Users/ted/komission/frontend && bun run build
```

## 배포

- Backend: `git push origin main` (Railway 자동 배포)
- Frontend: `git push origin main` (Vercel 자동 배포)
- VPS Agent Fleet: rsync 사용 (TOOLS.md 참조)

## 핵심 원칙

1. Read CLAUDE.md first — 프로젝트 규칙 준수
2. VDG Schema: `from app.services.vdg_schema_normalizer import normalize_vdg_schema`
3. Never push to main without Ted's approval
4. Always run pytest --testmon after code changes
