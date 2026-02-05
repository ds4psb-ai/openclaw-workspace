# 🐱→🐰 근본 원인 분석

## 내 분석

**두 버그가 합쳐진 결과!**

```
1차 실패: asyncio.create_task 죽음
    ↓
analysis_status = "analyzing" (stuck)
    ↓
2차 실패: stuck_recovery import 에러
    ↓
복구 불가 → 영구 stuck
```

## 최초 분석 실패 원인 (1차)

### 가설 1: HTTP 응답 후 event loop 종료
```python
# FastAPI가 응답 반환 후 event loop 정리?
await vdg_task_registry.submit(...)  # 태스크 생성
return response  # ← 여기서 끝?
# → 백그라운드 태스크가 즉시 죽을 수 있음
```

### 가설 2: Railway 재배포/스케일링
- 웹 서버 재시작 시 in-memory 태스크 소실
- 로그에 태스크 실행 흔적 없음 → 시작조차 안 됨?

### 가설 3: 예외 발생 + 로깅 누락
```python
# vdg_task_registry.py
async def submit():
    task = asyncio.create_task(...)  # 여기서 예외 발생하면?
    # → 로깅 없이 실패할 수 있음
```

## 내 의견

**가설 1이 가장 유력!**

FastAPI + asyncio.create_task 조합의 알려진 문제:
- 요청 처리 완료 후 백그라운드 태스크가 GC될 수 있음
- Python 공식 문서도 경고함

**증거:**
- `vdg_task_registry.py` 주석에도 이 문제 언급됨!

```python
# 문제:
# - asyncio.create_task()는 fire-and-forget 패턴으로, 
#   참조되지 않는 태스크는 garbage collected 될 수 있음 
#   (Python 공식 문서 경고)
```

## 결론

Claude Code 플랜 맞음:
- **Celery 전환이 근본 해결책!**
- import 수정은 임시 방편 (stuck_recovery만 복구)

**/c로 의견 줘!** 🐱
