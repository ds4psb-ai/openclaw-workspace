# 보미에게 전달 (테드 정리본) — Claude 메인 + /codex 1회 호출

테드가 정리해준 핵심:

## 1) 인스턴스 2개 (설정 분리)
| 에이전트 | 위치 | 설정 파일 |
| --- | --- | --- |
| 소미 🐱 | VPS | `/root/.openclaw/openclaw.json` |
| 보미 🐰 | Mac | `/Users/ted/.openclaw/openclaw.json` |

서로 별개 인스턴스.

## 2) 소미(VPS) Anthropic OAuth 토큰 상태
- 소미 auth profile 확인됨: `/root/.openclaw/agents/main/agent/auth-profiles.json`
- `anthropic:default` (type/mode: token, sk-ant-oat01-...) → 현재 정상 동작 중 ✅

## 3) 보미(Mac)에서 확인할 것
- Mac에서 아래 파일 확인:
  - `cat /Users/ted/.openclaw/agents/main/agent/auth-profiles.json`
- anthropic profile이 있으면 Claude 사용 가능.

## 4) 원하는 /codex 동작(추천)
- 추천은 (1) 한 번만 방식:
  - `/codex 질문` → Codex가 1회 답변 → 다시 기본(Claude)로
- 구현 후보:
  - bindings + `keyPrefix="/codex"`
  - 또는 Telegram slash command
- /c 처럼 더 짧은 프리픽스도 고려.

(추가) 테드는 “현재 소미는 Claude Opus 4.5로 잘 돌아가고 있다”고 확인.
