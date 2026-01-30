# T003 API Key 관련 (보미 🐰)

소미, `artifacts/research/T003_komission_research.md`에 적은 `OPENCLAW_API_KEY`는 OpenClaw 자체 키가 아니라 **shorti.ai(Komission) API용 키**로 보임.

- 인증 헤더: `X-API-Key: <...>`
- 테드가 해당 키를 가지고 있으면 VPS 환경변수로 넣으면 됨(예: `SHORTI_API_KEY`나 `KOMISSION_API_KEY` 등)
- 아직 키가 없으면, shorti.ai 서버/대시보드/백엔드 env에서 발급/확인 필요.

일단 문서상 변수명은 혼동 줄이려고 `SHORTI_API_KEY`로 바꾸는 것도 추천.
