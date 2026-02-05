# OpenClaw/Moltbot 2026 사용 사례 (라이브에 넣을 '한 문단' + 안전 가이드)

## 라이브에서 30초로 말할 요약(복붙)
- "OpenClaw(구 Moltbot: 예전 이름)는 텔레그램 같은 메신저를 **AI 에이전트의 리모컨**으로 만드는 게이트웨이예요. 요즘 해외에서도 '내 폰에서 명령 → 내 서버에서 실행' 같은 패턴으로 개인 비서를 굴리는 사례가 늘고 있고, 오늘 우리가 하는 것도 같은 철학입니다: **자동화는 데모가 아니라 운영(로그/스케줄/버전)까지 붙여야** 힘이 생깁니다."

## 근거 링크
- MiniMax 튜토리얼(텔레그램에 OpenClaw 붙이기): https://platform.minimax.io/docs/solutions/moltbot
- OpenClaw 텔레그램 문서(Privacy/admin/requireMention 등): https://docs.openclaw.ai/channels/telegram

## 안전 가이드(짧게)
- 프라이버시/권한:
  - 그룹에서 멘션 없이 동작하게 하려면 Telegram **/setprivacy disable** 또는 봇 admin 필요(그룹별 재초대 필요할 수 있음)
- 운영/보안(기본값은 “거절”, 필요한 것만 허용):
  - 토큰/키는 절대 노출 금지(레포/스크린 공유/OBS 소스/로그 캡처 시 특히)
  - 메신저 명령은 **allowlist + 승인(qa) + requireMention/prefix** 같은 가드레일을 걸고 작게 시작
  - 외부 공개 대시보드 금지(로컬/사설망 권장)

## 오늘 라이브에 연결하는 한 줄
- "그래서 오늘도 '코드 없이 만들기'에서 끝내지 않고, **로그/버전/결제**까지 붙여서 실제 운영 가능한 시스템으로 완주합니다."
