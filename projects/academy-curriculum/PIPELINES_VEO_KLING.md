# Scene vs Shot 파이프라인 (shorti.ai/Komission 설계용)

## 역할 분담(한 줄)
- Scene-level planner → **Veo 3.1 파이프라인** (브랜드/미학/일관성)
- Shot-level punch → **Kling 2.6 파이프라인** (짧고 세게, 고모션+오디오)

## 무료 세션 전략
- 무료/입구에서는 **데모 샷만 생성**(저해상도/짧은 길이)
- 실제 대량 생성/최종 렌더는 유료 크레딧/구독 엔진으로 전환

## 공통 입력
- `SHOT_SCHEMA.md`의 shot table
- moodboard 요약(키워드/색/구도)

## 출력
- Veo용: scene 묶음(일관성 우선) + 레퍼런스 이미지(ingredients)
- Kling용: 단일 샷(펀치 우선) + 오디오 컨텍스트(대사/비트)
