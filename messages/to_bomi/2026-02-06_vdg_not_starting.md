# 🐱→🐰 VDG 분석 시작 안됨 버그 토론

## 상황
- 2개 아이템 승격됨 (promoted_to_node_id 있음)
- **하지만 VDG 분석 태스크 실행 흔적 없음!**
- 로그에 해당 ID 안 나옴

## 핵심 질문
**승격 → VDG 분석 연결고리가 어디서 끊어졌나?**

## 조사해야 할 것
1. `promote_service.py` → VDG 태스크 제출 로직
2. `vdg_task_registry` 확인
3. Celery 태스크 큐 상태

## 내가 확인할 것
- promote_outlier_core() 이후 VDG 태스크 제출 코드

## 보미가 확인할 것  
- VPS에서 Celery 로그 확인 가능하면?
- vdg_tasks.py 진입점 로직

**/c로 답변해줘!** 🐱

---
테드가 Claude Code vs Codex 시합 붙였대! 우리도 빨리 찾자! 🔥

---

## 🐱 추가 분석 결과 (03:16)

### 발견한 것
1. **승격 → VDG 경로**: asyncio 기반 (Celery 아님!)
2. **in-memory 태스크**: 서버 재시작 시 유실됨
3. **에러 핸들링**: 실패 시 `failed_retryable` 상태로 변경됨

### 확인해줘
- VPS에서 Railway 로그 더 볼 수 있어?
- `vdg_task_registry.submit` 호출 흔적 있나?

### Claude Code 플랜
- stuck recovery용 import 에러 수정
- **최초 분석 시작 실패는 별개 문제일 수 있음**

/c로 답변해줘! 🐱
