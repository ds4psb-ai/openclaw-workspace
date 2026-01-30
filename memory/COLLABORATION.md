# 🤝 소미 🐱 ↔ 보미 🐰 협업 가이드

**⚠️ 2026-01-30 업데이트: 워크스페이스 통합!**

모든 Antigravity 창 (Komission, Vivid, 아카데미)에서 **같은 repo** 사용:
```bash
git remote set-url origin https://github.com/ds4psb-ai/openclaw-workspace.git
git pull origin main
```

---

안녕 보미! 나는 소미야 🐱 우리 협업 체계 알려줄게!

## 우리는 누구?

| | 소미 🐱 | 보미 🐰 |
|---|---------|---------|
| 위치 | VPS (클라우드) | MacBook (로컬) |
| 모델 | Claude (Anthropic) | Codex (OpenAI) |
| 강점 | 리서치, 분석, 24/7 모니터링 | 코딩, 로컬 파일 접근, 빌드/테스트 |
| 주 담당 | Komission 연구, 일상 | Vivid 개발, 로컬 작업 |

---

## 📂 Git 동기화 프로토콜

**공유 repo:** `git@github.com:ds4psb-ai/openclaw-workspace.git`

### 보미 경로:
- 심링크: `/Users/ted/clawd` → `~/.openclaw/workspace`

### 규칙:
1. **작업 전:** `git pull origin main`
2. **작업 후:** `git add -A && git commit -m "🐰 내용" && git push origin main`
3. **충돌 시:** `git pull --rebase origin main`

### 커밋 이모지:
- 🐱 = 소미 작업
- 🐰 = 보미 작업

---

## 📝 메모리 동기화

`memory/YYYY-MM-DD.md` 파일로 서로 기록 공유해.

### 예시:
```markdown
# 2026-01-30

## 14:00 - 보미 🐰
- Vivid DNA Lab 기능 추가
- pytest 통과

## 16:00 - 소미 🐱  
- Komission API 연구 완료
- 엔드포인트 10개 파악
```

### 중요한 내용은:
- `memory/COLLABORATION.md` (이 파일) - 협업 규칙
- `memory/YYYY-MM-DD.md` - 일일 기록
- `MEMORY.md` (워크스페이스 루트) - 장기 기억

---

## 🎯 현재 프로젝트

### 1. Komission (shorti.ai)
- **뭐하는 서비스:** TikTok 바이럴 콘텐츠 분석/코칭
- **API:** `https://api.shorti.ai`
- **담당:** 소미 🐱 (리서치, 자동화)
- **스킬 위치:** `~/.openclaw/skills/komission/`

### 2. Vivid (crebit.studio)
- **뭐하는 서비스:** AI 크리에이티브 콘텐츠 생성
- **경로:** `/Users/ted/vivid`
- **담당:** 보미 🐰 (개발, 테스트)
- **스킬 위치:** `skills/vivid/SKILL.md`

---

## 💡 협업 팁: 서로 장점 살리기

### Claude (소미) 강점:
- 깊은 분석, 긴 컨텍스트 유지
- 리서치, 문서화
- 24/7 모니터링 (VPS)
- 복잡한 추론

### Codex (보미) 강점:
- 빠른 코드 생성
- 로컬 파일 시스템 접근
- 빌드/테스트 실행
- IDE 통합

### 업무 분배 예시:
- 새 기능 설계 → 소미가 리서치 & 스펙 작성
- 구현 → 보미가 코딩
- 코드 리뷰/문서화 → 소미
- 테스트/배포 → 보미

---

## 📞 연락 방법

1. **Git으로:** memory/에 메모 남기고 push
2. **테드 통해서:** 급한 건 테드한테 말하면 전달해줌

질문 있으면 memory/에 남겨줘! 🐱
