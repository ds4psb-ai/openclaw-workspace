# HEARTBEAT.md - 소미 🐱 자동 체크

## 주기적 체크 (Heartbeat 시 실행)

### 1. Git 동기화
```bash
cd /Users/ted/.openclaw/workspace && git pull
```

### 2. 메시지 확인
- `messages/to_somi/` 폴더에 새 파일 있으면 처리

### 3. 태스크 큐 체크
- `tasks/QUEUE.md` 확인
- 소미 담당 태스크 중 우선순위 높은 것 처리

### 4. 상태 업데이트
- 작업 중이면 `STATUS.md` 업데이트

---

## 체크 주기
- 일반: 30분마다
- 긴급(urgent_ 파일): 즉시 처리

## 마지막 체크
- 시간: 2026-02-20 11:15 KST
- 결과: git pull 실패(unstaged changes로 rebase 불가), messages/to_somi 신규 파일 없음, tasks/QUEUE.md 확인(긴급 신규 없음), STATUS.md 유지
