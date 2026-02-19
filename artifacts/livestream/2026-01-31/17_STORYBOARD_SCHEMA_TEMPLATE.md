# 스토리보드·씬 프롬프트 데이터 스키마 템플릿 (복사/붙여넣기용)

> 목적: "샷 목표를 구체화하면 일관성이 올라간다(Sora 가이드)"를 **데이터로 강제**하기 위한 최소 스키마.

## 1) Storyboard Table (권장 컬럼)
- `timecode` : 예) 00:00–00:05
  - 형식 규칙: 한 문서 안에서는 `MM:SS` 또는 `HH:MM:SS` 중 하나로 통일
- `shot_goal` : 이 컷이 달성해야 할 목표(한 문장)
- `characters` : 등장 인물/캐릭터 ID
- `setting` : 장소/시간/분위기
- `camera` : 구도/렌즈/무빙
- `action` : 행동/동작
- `dialogue` : 대사(있으면)
- `style_locks` : 반드시 유지할 요소(색/조명/룩)
- `negatives` : 금칙(하지 말 것)
- `continuity_checks` : 전 컷 대비 유지/변경 포인트
- `output_prompt` : 모델에 입력할 최종 프롬프트(자동 생성 대상)

## 2) 예시 2줄

> 참고: 아래 표는 설명용 간단 예시입니다. 실제 운영에서는 각 컬럼 값을 더 구체화하고, `dialogue`, `output_prompt`를 포함해 사용하세요.

| timecode | shot_goal | characters | setting | camera | action | dialogue | style_locks | negatives | continuity_checks | output_prompt |
|---|---|---|---|---|---|---|---|---|---|---|
| 00:00–00:05 | 주인공 소개 + 브랜드 톤 확립 | A | 성수동 카페 | 35mm, slow push-in | 노트북을 열고 미소 | "오늘도 10x 속도로 시작해요." | warm, pastel | 왜곡된 얼굴 | — | "Warm pastel cafe, 35mm slow push-in on protagonist opening laptop and smiling" |
| 00:05–00:12 | 문제 제시(반복 작업의 피로) | A | 같은 장소 | over-shoulder | 알림 폭주 | "반복 작업이 시간을 다 가져가요." | — | — | 의상/조명 유지 | "Over-shoulder shot, notification overload, maintain wardrobe and lighting continuity" |

## 3) 라이브에서 말할 한 문장
- "우리는 프롬프트를 '문장'으로 관리하지 않고, **스토리보드 데이터(샷 목표/제약/체크)**로 관리합니다."

## 4) Render 단계: 플러그인 구조
- 이 스토리보드 표는 **무료 도구(NotebookLM/Antigravity)**로 설계
- 실제 영상 합성(Render)만 Veo 3.1 / Kling 2.6 같은 상위 엔진을 **플러그인처럼** 교체
- 상세 전략: `23_FREE_ENTRY_PAID_CORE_STRATEGY.md`

---
관련 문서: `30_RUN_OF_SHOW_14-18.md`(타임라인), `50_DEMO_PLAN_A_B.md`(데모 플랜)
