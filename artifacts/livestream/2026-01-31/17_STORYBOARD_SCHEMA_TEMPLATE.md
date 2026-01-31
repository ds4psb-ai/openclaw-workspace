# 스토리보드/씬 프롬프트 ‘데이터 스키마’ 템플릿 (복붙용)

> 목적: “샷 목표를 구체화하면 일관성이 올라간다(Sora 가이드)”를 **데이터로 강제**하기 위한 최소 스키마.

## 1) Storyboard Table (권장 컬럼)
- `timecode` : 예) 00-05s
- `shot_goal` : 이 컷이 달성해야 할 목표(한 문장)
- `characters` : 등장 인물/캐릭터 ID
- `setting` : 장소/시간/분위기
- `camera` : 구도/렌즈/무빙
- `action` : 행동/동작
- `dialogue` : 대사(있으면)
- `style_locks` : 반드시 유지할 요소(색/조명/룩)
- `negatives` : 금칙(하지 말 것)
- `continuity_checks` : 전 컷 대비 유지/변경 포인트
- `output_prompt` : 모델에 던질 최종 프롬프트(자동 생성 대상)

## 2) 예시 2줄
- 00-05s | shot_goal: 주인공 소개 + 브랜드 톤 확립 | characters: A | setting: 성수동 카페 | camera: 35mm, slow push-in | action: 노트북을 열고 미소 | style_locks: warm, pastel | negatives: 왜곡된 얼굴
- 05-12s | shot_goal: 문제 제시(반복 작업의 피로) | characters: A | setting: 같은 장소 | camera: over-shoulder | action: 알림 폭주 | continuity_checks: 의상/조명 유지

## 3) 라이브에서 말할 한 문장
- “우리는 프롬프트를 ‘문장’으로 관리하지 않고, **스토리보드 데이터(샷 목표/제약/체크)**로 관리합니다.”
