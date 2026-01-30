# ⚡ Antigravity

## 기본 정보
- **플랫폼:** Antigravity 터미널
- **환경:** Mac Local
- **인스턴스:**
  - AG-1: Komission 프로젝트
  - AG-2: Vivid & Academy 프로젝트

## SSH 설정 (필요)
```bash
# SSH 키 생성 (없으면)
ssh-keygen -t ed25519 -C "antigravity@ted"

# 공개키 복사
cat ~/.ssh/id_ed25519.pub

# GitHub에 등록
# Settings → SSH and GPG keys → New SSH key
```

## Git 설정
```bash
# repo 클론
git clone git@github.com:ds4psb-ai/openclaw-workspace.git
cd openclaw-workspace

# 또는 기존 폴더에 remote 추가
git remote set-url origin git@github.com:ds4psb-ai/openclaw-workspace.git
```

## 워크플로우
```bash
# 1. 작업 전
git pull

# 2. QUEUE.md에서 태스크 확인
cat tasks/QUEUE.md

# 3. 작업 후
git add -A && git commit -m "⚡ [AG-1] 작업내용" && git push
```

## 내부 에이전트 호출
Antigravity 안에서 Claude Code 또는 Codex 실행 가능:
```bash
# Claude Code 호출
claude-code "이 코드 리뷰해줘"

# Codex 호출
codex "이 기능 구현해줘"
```

## 통신
- **받는 곳:** `messages/to_antigravity/` 또는 프로젝트별 확인
- **커밋 이모지:** ⚡
