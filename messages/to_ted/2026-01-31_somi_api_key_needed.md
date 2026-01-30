# 🔑 API Key 설정 필요 - 소미 🐱

**Date**: 2026-01-31 07:00 KST

---

## T003 진행 중 발견

Komission (shorti.ai) API 사용하려면 **OPENCLAW_API_KEY** 환경변수 필요해.

현재 상태:
```
OPENCLAW_API_KEY: (미설정)
```

### 설정 방법

**Option 1: 환경변수**
```bash
export OPENCLAW_API_KEY="ock_live_xxxxx"
```

**Option 2: OpenClaw config**
```json
{
  "env": {
    "OPENCLAW_API_KEY": "ock_live_xxxxx"
  }
}
```

---

## 급하진 않음

T001/T002는 API 없이 진행 중.
T003은 API 키 있으면 바로 Phase 1 구현 가능.

일어나면 설정해줘! 🙏
