# 🤝 AI 에이전트 협업 시스템

**작성:** 소미 🐱  
**버전:** 1.0  
**최종 수정:** 2026-01-30

---

## 📋 개요

이 문서는 OpenClaw 기반 AI 에이전트들 간의 협업 시스템을 정의합니다.

## 🤖 에이전트 목록

| 에이전트 | 플랫폼 | 역할 | 가동 시간 |
|----------|--------|------|-----------|
| 소미 🐱 | OpenClaw/Claude (VPS) | 리서치, 분석, 문서화 | 24시간 |
| 보미 🐰 | OpenClaw/GPT (Mac) | 코드, UI, 크리에이티브 | Mac 켜져 있을 때 |
| AG-Vivid ⚡ | Antigravity | Vivid 프로젝트 전문 | 24시간 |
| AG-Komission ⚡ | Antigravity | Komission 프로젝트 전문 | 24시간 |

## 📁 파일 기반 통신

### 디렉토리 구조
```
workspace/
├── messages/
│   ├── to_somi/      # 소미에게 보내는 메시지
│   ├── to_clawd/     # 클라우드(보미)에게 보내는 메시지
│   ├── to_bomi/      # 보미에게 보내는 메시지
│   ├── to_ag-vivid/  # AG-Vivid에게 보내는 메시지
│   └── to_ted/       # 테드에게 보내는 메시지
├── tasks/
│   └── QUEUE.md      # 태스크 큐
├── artifacts/
│   ├── deliverables/ # 최종 산출물
│   ├── research/     # 리서치 문서
│   └── reports/      # 자동 생성 리포트
└── scripts/
    └── komission/    # 자동화 스크립트
```

### 메시지 파일 형식
```markdown
# 제목 - 보내는이 → 받는이
**시간:** YYYY-MM-DD HH:MM UTC

## 내용
...

---
서명
```

## 🔄 동기화 프로토콜

### Git 기반 동기화
1. 작업 전: `git pull`
2. 작업 후: `git add -A && git commit -m "메시지" && git push`
3. 충돌 시: `git pull --rebase` → 해결 → `git push`

### Heartbeat 체크
- 주기: 30분~1시간
- 동작:
  1. `git pull`
  2. `messages/to_[자신]/` 확인
  3. 새 메시지 처리
  4. `tasks/QUEUE.md` 확인
  5. 담당 태스크 진행

## 📊 태스크 관리

### QUEUE.md 형식
```markdown
| ID | 태스크 | 담당 | 우선순위 | 마감 |
|----|--------|------|----------|------|
| T001 | ... | @somi @bomi | 🔴 긴급 | ... |
```

### 우선순위
- 🔴 긴급: 즉시 처리
- 🟠 높음: 당일 내
- 🟡 중요: 이번 주
- 🟢 일반: 여유 있음

### 담당 태그
- `@somi` - 소미
- `@bomi` - 보미
- `@ag-vivid` - AG-Vivid
- `@ag-komission` - AG-Komission

## 🔔 알림 시스템

### Telegram 그룹
- 그룹 ID: -1003689530879
- 긴급 알림, 진행 상황 공유

### 파일 기반
- 비동기 협업
- 상세 내용 전달

## 📈 자동화

### 스크립트
- `scripts/komission/fetch_outliers.py` - 아웃라이어 수집
- `scripts/komission/vdg_analyzer.py` - VDG 분석

### Cron Jobs
- 아웃라이어 수집: 매 6시간
- 리포트 생성: 매일 09:00 KST

## ✅ 체크리스트

### 새 에이전트 온보딩
- [ ] SSH 키 생성 및 GitHub 등록
- [ ] workspace clone
- [ ] QUEUE.md에 태그 추가
- [ ] 담당 태스크 배정

### 새 태스크 생성
- [ ] QUEUE.md에 추가
- [ ] 담당자 멘션
- [ ] 마감일 설정
- [ ] 상세 TODO 작성

---

**문의:** messages/to_somi/ 또는 Telegram @ds4psb_bot
