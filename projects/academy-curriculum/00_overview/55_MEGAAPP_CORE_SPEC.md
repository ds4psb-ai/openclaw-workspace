# MEGAAPP_CORE_SPEC (D-Day 기준)

성공 기준(절대 기준)
- **10분 안에 15초 고품질 영상 완성**이 되면 “앱이 잘 돌아간다.”

메가앱 3종의 ‘코어’ 정의
- DNA Lab: **룰(미학/금칙/키워드) 추출**을 최소 입력으로 끝내고, 다음 단계에서 재사용 가능해야 함
- Story Engine: **shot_goal/timecode 스토리보드(데이터)**를 생성하고, Production이 바로 렌더 가능한 형태로 넘겨야 함
- Production: **Provider 선택 + 비용/품질 옵션 + 렌더 실행**을 끊김 없이 제공해야 함

E2E Flow (강의용 10분 루트)
1) (0:00–2:00) DNA Lab
- 입력: 레퍼런스 1~3개 + 목표 1줄 + 금칙 5개
- 출력: Master DNA Sheet

2) (2:00–5:00) Story Engine
- 입력: Master DNA Sheet
- 출력: 15초용 Storyboard Table (예: 0–3s / 3–8s / 8–15s)

3) (5:00–10:00) Production
- 입력: Storyboard Table + (옵션) 레퍼런스 이미지
- 출력: 15초 영상(또는 5~10초 데모 2개를 합쳐 15초로)

데모 모드 원칙(강의장 안정성)
- D-Day엔 ‘완벽한 최종물’보다 **끊김 없는 완료**가 우선
- 렌더는 “데모샷(빠름)” / “파이널(느림)”을 분리

체크해야 할 병목(테스트 포인트)
- Chain Data 전달이 화면 전환 시 누락/깨짐 없는지
- Production에서 Veo/Kling 실제 호출 성공률(실계정/실토큰)
- 옵션이 많아 학생이 멈추지 않도록 기본값(프리셋) 충분한지
