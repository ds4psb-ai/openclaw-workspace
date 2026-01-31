# Mixboard Stage Guide (수업/라이브에서 ‘미학’ 체감 만드는 15분 루틴)

근거(공식/언론)
- Google Blog: Mixboard는 텍스트로 보드를 시작하거나 프리셋 보드를 쓰고, 자연어로 수정/결합/재생성 가능(Nano Banana 기반). 공개 베타(미국): https://blog.google/innovation-and-ai/models-and-research/google-labs/mixboard/
- Labs: https://labs.google.com/mixboard/welcome
- TechCrunch 요약(피드 대신 텍스트로 시작, 자연어 편집/결합): https://techcrunch.com/2025/09/24/google-launches-an-ai-powered-mood-board-app-mixboard/

## 목표
- ‘거장 DNA(언어)’를 **시각 언어(보드)**로 바꾸고, 팀/학생이 **즉시 합의**하도록 만든다.

## 15분 루틴(수업/라이브)
1) (2분) 키워드 10개 확정
- NotebookLM DNA Sheet에서: 색/조명/질감/구도/리듬/금칙 키워드만 뽑기

2) (5분) Mixboard 보드 1개 생성
- 방법 A: 텍스트 프롬프트로 시작
- 방법 B: 프리셋 보드 선택 후 수정

3) (5분) 자연어 수정 3번(필수)
- “더 어둡게, 대비 높게, 필름 그레인 조금”
- “배경은 더 단순하게, 소품은 2개만”
- “카메라는 더 낮은 앵글, 더 시네마틱”

4) (3분) ‘샷 리스트 입력’으로 변환
- 보드에서 얻은: 색/구도/소품/조명 규칙을 `SHOT_SCHEMA.md`의 style_locks/negatives로 복사

## 수강생이 얻는 산출물
- Moodboard v1~v3 캡처 + style_locks/negatives 규칙 세트

## 라이브에서 말할 한 문장
- “미학은 감이 아니라 **보드로 고정**하는 겁니다. 한 번 고정되면, 이후엔 속도가 붙어요.”
