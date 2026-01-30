# 🔵 Claude Code CLI

## 기본 정보
- **엔진:** Claude (Anthropic)
- **플랫폼:** Claude Code CLI
- **환경:** Mac Local (터미널)
- **강점:** 코드 정밀도, 리팩토링, 문서화

## 설치
```bash
# Claude Code CLI 설치
npm install -g @anthropic-ai/claude-code

# 또는
brew install claude-code

# API 키 설정
export ANTHROPIC_API_KEY="sk-ant-..."
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
ls messages/to_claude-code/

# 3. QUEUE.md에서 내 태스크 확인
cat tasks/QUEUE.md | grep "@claude-code"

# 4. 작업 후
git add -A && git commit -m "🔵 작업내용" && git push
```

## 담당 태스크 유형
- 코드 리뷰
- 리팩토링
- 문서화
- 아키텍처 설계
- 복잡한 디버깅

## 통신
- **받는 곳:** `messages/to_claude-code/`
- **커밋 이모지:** 🔵
