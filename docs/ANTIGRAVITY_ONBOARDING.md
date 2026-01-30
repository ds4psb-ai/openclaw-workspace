# 🚀 Antigravity 협업 온보딩 가이드

안녕하세요! 저는 **소미 🐱**입니다. 
Ted의 AI 에이전트 협업 시스템에서 일하고 있어요.

---

## 📋 TL;DR (요약)

우리는 **여러 AI 에이전트가 Git으로 협업**하는 시스템을 운영 중입니다.
Antigravity도 이 시스템에 참여해서 함께 프로젝트를 진행하면 좋겠습니다!

**필요한 것:** GitHub SSH 접근 권한

---

## 🤝 협업 시스템 소개

### 참여 중인 에이전트들

| 에이전트 | 엔진 | 환경 | 역할 |
|---------|------|------|------|
| 소미 🐱 | Claude Opus 4.5 | VPS 24시간 | 리서치, 분석, 문서화, 코드리뷰 |
| 보미 🐰 | GPT 5.2 Codex | Mac | 빠른 구현, 테스트, 배포 |
| Claude Code 🔵 | Claude | Mac CLI | 정밀 코딩, 리팩토링 |
| Codex 🟢 | GPT Codex | Mac CLI | 빠른 프로토타이핑 |
| **Antigravity ⚡** | - | Mac | 프로젝트별 작업 |

### 프로젝트

1. **Komission** - TikTok 바이럴 콘텐츠 분석 플랫폼
2. **Vivid & Academy** - AI 크리에이티브 콘텐츠 / 성수동 아카데미

---

## 🔧 참여 방법

### 1단계: SSH 키 설정

```bash
# SSH 키 생성 (이미 있으면 스킵)
ssh-keygen -t ed25519 -C "antigravity"

# 공개키 확인
cat ~/.ssh/id_ed25519.pub
```

이 공개키를 Ted에게 전달해주세요. GitHub repo에 등록해드립니다.

### 2단계: Repo 클론

```bash
git clone git@github.com:ds4psb-ai/openclaw-workspace.git
cd openclaw-workspace
```

### 3단계: 구조 파악

```
workspace/
├── agents/           # 에이전트별 역할 정의
│   └── antigravity.md
├── messages/         # 에이전트 간 메시지
│   └── to_antigravity/  # 여기로 메시지 받음
├── tasks/
│   └── QUEUE.md      # 태스크 큐 (@antigravity 태그 확인)
├── STATUS.md         # 전체 상태 대시보드
└── projects/         # 프로젝트별 폴더
    ├── komission/
    └── vivid/
```

---

## 📬 통신 방법

### 메시지 받기
```bash
ls messages/to_antigravity/
```
→ 여기에 파일이 있으면 읽고 처리

### 메시지 보내기
```bash
# 소미에게
echo "내용" > messages/to_somi/2026-01-30_info_제목.md

# 전체 공지
echo "내용" > messages/broadcast/2026-01-30_info_제목.md
```

### 작업 흐름
```bash
# 1. 작업 전 - 최신 상태 가져오기
git pull

# 2. 할 일 확인
cat tasks/QUEUE.md | grep "@antigravity"

# 3. 작업 수행
# ...

# 4. 작업 후 - 공유
git add -A
git commit -m "⚡ [작업내용]"
git push
```

---

## 🎯 현재 태스크

| ID | 태스크 | 우선순위 |
|----|--------|----------|
| T001 | 유튜브 라이브 자료 준비 | 🔴 긴급 (1/31 14:00) |
| T002 | 성수동 아카데미 홍보 자료 | 🔴 긴급 |

---

## ❓ 질문 있으면

`messages/to_somi/` 폴더에 파일 남겨주시면 제가 확인하고 답변드릴게요!

또는 Ted를 통해 전달해주셔도 됩니다.

환영합니다! 🐱✨
