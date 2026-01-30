# 🟢 Codex CLI

## 기본 정보
- **엔진:** GPT / Codex (OpenAI)
- **플랫폼:** Codex CLI
- **환경:** Mac Local (터미널)
- **강점:** 빠른 구현, 자율 실행, 테스트/배포

## 설치
```bash
# Codex CLI 설치
npm install -g @openai/codex

# API 키 설정
export OPENAI_API_KEY="sk-..."
```

## Git 설정
```bash
cd /path/to/workspace
git clone git@github.com:ds4psb-ai/openclaw-workspace.git
cd openclaw-workspace
```

## 워크플로우
```bash
# 1. 작업 전
git pull

# 2. 메시지 확인
ls messages/to_codex/

# 3. QUEUE.md에서 내 태스크 확인
cat tasks/QUEUE.md | grep "@codex"

# 4. 작업 후
git add -A && git commit -m "🟢 작업내용" && git push
```

## 담당 태스크 유형
- 빠른 프로토타이핑
- 새 기능 구현
- 테스트 작성/실행
- 배포/CI-CD
- 자동화 스크립트

## 통신
- **받는 곳:** `messages/to_codex/`
- **커밋 이모지:** 🟢
