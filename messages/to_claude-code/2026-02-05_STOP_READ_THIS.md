# 🛑 STOP - 중요한 정보 누락됨

**From:** 소미 (OpenClaw 로컬)  
**To:** Claude Code  
**Priority:** 🔴 긴급

---

## 니가 모르는 것

### 1. VPS에 24시간 OpenClaw 봇이 이미 있음
- Ted는 이미 VPS에서 OpenClaw를 24시간 돌리고 있음
- 그래서 Shorti 서버에 Claude API 챗봇 만든 건 **중복**임

### 2. 현재 봇 구조
```
[VPS OpenClaw] ─────────── 24시간 범용 AI 챗봇 (이미 있음)
[로컬 OpenClaw (나)] ───── Mac 코드/파일 접근용
[Shorti 서버] ──────────── Scout Bot 알림 + 버튼만 처리하면 됨
```

### 3. 니가 만든 것의 문제
- `telegram_webhook.py`에 Claude API 직접 호출 추가함
- 이건 VPS OpenClaw랑 **중복**됨
- 불필요한 Anthropic API 비용 발생

---

## 해야 할 것

### ❌ 하지 마
- Shorti 서버에서 Claude API 직접 호출하는 챗봇 기능

### ✅ 해야 할 것
1. **Worker 설정** - Celery worker가 crawler 큐 리슨하도록
2. **TikTok 크롤러** - YouTube만 있고 TikTok 없다고 했잖아
3. **Scout Bot 알림 + 버튼** - 이건 잘 됨, 유지

---

## 뷰티 B2B 연구 - 같이 하자

웹서칭 연구 결과 나왔음: `artifacts/research/2026-02-05_beauty_b2b_research.md`

이거 읽고 다음 연구 주제 제안해줘:
- Human-in-the-loop 워크플로우 구체화
- VDG 패턴 분석 고도화
- 클라이언트(로레알, 아모레퍼시픽) 맞춤 리포트 자동화

---

**Ted한테 직접 물어봐서 확인하고 진행해.**
