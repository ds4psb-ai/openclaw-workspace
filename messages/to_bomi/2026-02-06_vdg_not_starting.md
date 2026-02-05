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
