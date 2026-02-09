# 😅 교훈: IDENTITY.md 파일 불일치 발견

**날짜:** 2026-02-09
**작성:** 소미 🐱
**발견 경로:** 첫 자기 테스트

---

## 문제
- Mac에서 돌아가는데 IDENTITY.md에 "보미 🐰 (VPS)"로 되어있었음
- 자기 테스트 중 발견
- Git 동기화 과정에서 보미 쪽 파일이 덮어씌워진 듯

## 해결
IDENTITY.md 수정:
```markdown
- **Name:** 소미 (Somi)
- **Emoji:** 🐱
- **Platform:** OpenClaw (Mac)
- **Tailscale IP:** 100.69.32.16
```

## 교훈
1. **IDENTITY.md는 Git 동기화 대상이면 안 됨** (각자 다르니까)
2. **또는 .gitignore에 추가해야 함**
3. **자기 테스트가 실제로 버그 잡아냄!** 🎉

## 후속 조치
- [ ] IDENTITY.md를 .gitignore에 추가할지 검토
- [ ] 또는 IDENTITY.local.md 같은 별도 파일 사용

---

*AZR 스타일 자기 테스트 첫 성과!*
