---
name: vivid
description: Crebit Studio (Vivid) - 크리에이티브 AI 콘텐츠 생성 플랫폼 개발. Use for Vivid project coding, testing, deployment, Dimension App creation, or any work in /Users/ted/vivid directory.
---

# Vivid (Crebit Studio) 개발 스킬

## Quick Reference

| 항목 | 값 |
|------|-----|
| 프로젝트 | `/Users/ted/vivid` |
| Frontend | Next.js 16, React 19 (port 3100) |
| Backend | FastAPI, Python 3.11 (port 8100) |
| AI | Google Gemini API |
| DB | PostgreSQL 5433, Redis 6380, Qdrant 6333 |

## 필수 검증 명령어

```bash
# Backend 테스트
cd /Users/ted/vivid/backend && source .venv/bin/activate && pytest --tb=short -q

# Frontend 빌드
cd /Users/ted/vivid/frontend && npm run build
```

## 개발 서버 실행

```bash
# Backend
cd /Users/ted/vivid/backend && source .venv/bin/activate && uvicorn app.main:app --port 8100 --reload

# Frontend
cd /Users/ted/vivid/frontend && npm run dev
```

## 핵심 원칙

1. **확인 후 코딩**: `Grep`/`Read`로 파일 존재 확인 → 코드 작성
2. **환각 금지**: 존재하지 않는 파일/함수 참조 금지
3. **테스트 동반**: 새 기능 추가 시 테스트도 함께
4. **타입 명시**: Python type hints, TypeScript strict

## Dimension Apps (13개)

| App | 기능 |
|-----|------|
| 1D~4D | 차원별 콘텐츠 생성 |
| Abyss Mirror | 창작 DNA 분석 |
| Reference Decoder | 레퍼런스 분석 |
| Scenario Generator | 시나리오 생성 |
| Sound Crafter | 사운드 생성 |
| Storyboard Sketcher | 스토리보드 |
| Prompt Alchemy | 프롬프트 최적화 |
| Visual Realizer (3D) | 이미지 생성 |
| Video Maker (VEO) | 비디오 생성 |
| Quality Director | 품질 검증 |
| Aesthetic Director | 미학 가이드 |

## 앱 개발 시 필수 참조

| 문서 | 경로 |
|------|------|
| 앱 개발 가이드 | `docs/DIMENSION_APP_DEVELOPER_GUIDE.md` |
| 앱 YAML 스키마 | `config/apps/content/dimensions/*.yaml` |
| Backend 가이드 | `backend/CLAUDE.md` |
| Frontend 가이드 | `frontend/CLAUDE.md` |

## 배포

### Railway (Backend)
```bash
# Dockerfile CMD (shell form 필수)
CMD sh -c "uvicorn app.main:app --port ${PORT:-8080}"
```
상세: `docs/RAILWAY_DEPLOYMENT_GUIDE.md`

### Vercel (Frontend)
```bash
# API 방식 배포 (CLI보다 안정적)
VERCEL_TOKEN=$(cat "/Users/ted/Library/Application Support/com.vercel.cli/auth.json" | jq -r '.token')
curl -s -X POST "https://api.vercel.com/v13/deployments?skipAutoDetectionConfirmation=1" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "crebit",
    "project": "crebit", 
    "gitSource": {"type": "github", "org": "ds4psb-ai", "repo": "vivid", "ref": "main"},
    "target": "production"
  }'
```
상세: `docs/VERCEL_DEPLOYMENT_GUIDE.md`

## Key Files

| 파일 | 역할 |
|------|------|
| `CLAUDE.md` | 메인 설정 (이 파일 먼저 읽기!) |
| `backend/app/generation_client.py` | Shot/Prompt Contract |
| `backend/app/routers/run_token.py` | Run Token |
| `frontend/src/lib/api.ts` | Typed API Client |

## 작업 전 체크리스트

1. [ ] `/Users/ted/vivid/CLAUDE.md` 읽기
2. [ ] 관련 하위 CLAUDE.md 확인 (backend/, frontend/)
3. [ ] 앱 작업 시 `docs/DIMENSION_APP_DEVELOPER_GUIDE.md` 참조
4. [ ] 테스트 실행 후 커밋
