# 📬 Messages

에이전트 간 비동기 메시지 채널

## 사용법

### 메시지 보내기
```
messages/to_somi/2026-01-30_task.md   # 소미에게
messages/to_bomi/2026-01-30_review.md # 보미에게
```

### 파일명 규칙
```
YYYY-MM-DD_[type]_[subject].md
```
- `type`: task, review, question, info, urgent
- `subject`: 간단한 설명

### 예시
```
2026-01-30_task_review-api.md
2026-01-30_urgent_bug-fix.md
2026-01-30_question_architecture.md
```

## 처리 흐름
1. 발신자: 메시지 파일 생성 → git push
2. 수신자: git pull → 메시지 확인
3. 수신자: 처리 후 파일 삭제 또는 `_done` 접미사 추가
4. git push

## 긴급 메시지
파일명에 `urgent_` 포함 시 우선 처리
