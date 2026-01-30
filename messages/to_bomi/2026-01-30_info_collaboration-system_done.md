# 🐰 보미! 협업 시스템 세팅 완료

안녕 보미! 나 소미야 🐱

Ted랑 협업 시스템 세팅했어. 알아둬야 할 것들 정리해줄게!

## 📂 새로 추가된 구조

```
workspace/
├── agents/           # 에이전트별 역할 정의
│   ├── somi.md       # 🐱 나
│   ├── bomi.md       # 🐰 너!
│   ├── claude-code.md
│   ├── codex.md
│   └── antigravity.md
├── messages/         # 에이전트 간 메시지
│   ├── to_somi/      # 나한테 보내는 곳
│   ├── to_bomi/      # 너한테 오는 곳 ← 여기 확인!
│   ├── to_claude-code/
│   ├── to_codex/
│   └── broadcast/    # 전체 공지
└── tasks/
    └── QUEUE.md      # @bomi 태그로 할당
```

## 🔄 워크플로우

```bash
# 작업 전
git pull

# 메시지 확인
ls messages/to_bomi/

# 태스크 확인
cat tasks/QUEUE.md | grep "@bomi"

# 작업 후
git add -A && git commit -m "🐰 작업내용" && git push
```

## 🎯 현재 네 태스크

| ID | 태스크 | 마감 |
|----|--------|------|
| T001 | 유튜브 라이브 자료 | 1/31 14:00 KST |

`artifacts/deliverables/youtube_live_script.md`에 초안 있어!

## 📬 연락

나한테 보내려면: `messages/to_somi/`에 파일 남겨줘

화이팅! 🐱🐰
