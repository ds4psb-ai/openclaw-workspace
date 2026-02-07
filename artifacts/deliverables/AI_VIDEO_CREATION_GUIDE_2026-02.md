AI 영상 제작 실전 가이드
Prompty Academy 워크플로우 실행 매뉴얼

Prompty Academy (Crebit AI Studio) | 2026년 2월 기준

────────────────────────────────────────

Prompty Academy 워크플로우

[Dashboard]
- 홈 대시보드
- 환경 설정
- $300 무료 크레딧 받기

[Workflow]
1. 영상 업로드 → 레퍼런스 영상 드래그앤드롭, 씬 감지
2. 프롬프트 생성 → 통합빌더 (Google AI Studio)
3. 파싱 + 복사 → 오마주/변주 씬별 프롬프트 정리
4. 외부 툴 → 이미지/영상 생성

이 가이드는 [4. 외부 툴] 실행 방법을 설명합니다.

────────────────────────────────────────

이미지 생성 도구

────────────────────────────────────────

[A] NanoBanana Pro (한글 OK)

접속: gemini.google.com

실행 방법:
1. Google 로그인
2. 모델: Gemini 2.0 Flash 또는 Thinking
3. NanoBanana Pro 프롬프트 복사 → 붙여넣기 → Enter
4. 이미지 다운로드

특징:
- 한국어 프롬프트 지원
- 무료 (일일 제한)
- 텍스트 렌더링 정확


[B] Midjourney V7 (--cref)

접속: midjourney.com

웹사이트 (추천):
1. 로그인 → Create
2. 프롬프트 붙여넣기 → Enter
3. 이미지 다운로드

파라미터:
--ar 9:16       세로 비율 (숏폼)
--ar 16:9       가로 비율
--v 7           버전 7
--style raw     실사 느낌
--stylize 250   스타일 강도 (0~1000)
--cref [URL]    캐릭터 참조 URL
--cw 30~100     참조 강도 (얼굴 30, 전체 100)
--no [키워드]   제외 요소


앵커 이미지 사용법:

앵커 이미지 = 첫 번째 씬에서 생성한 캐릭터 기준 이미지
이 이미지를 --cref로 참조하면 다른 씬에서도 같은 캐릭터 유지

1. 앵커 씬 먼저 생성 (--cref 없는 프롬프트)
2. 이미지 URL 복사
   웹: 이미지 우클릭 → 이미지 주소 복사
   Discord: 이미지 클릭 → 브라우저에서 열기 → URL 복사
3. 다른 씬 프롬프트의 [ANCHOR_URL]을 복사한 URL로 교체
4. 나머지 씬 생성

────────────────────────────────────────

영상 생성 도구

────────────────────────────────────────

[C] Kling 3.0 (4K)

접속: klingai.com

실행:
1. 로그인 → AI Videos → Image to Video
2. 이미지 업로드
3. Kling 프롬프트 붙여넣기
4. 설정:
   - Mode: Standard / Professional
   - Duration: 2~5초
5. Generate → 다운로드

카메라 옵션:
Static          고정 (클로즈업에 적합)
Dolly In/Out    줌인/줌아웃
Pan Left/Right  좌우 패닝
Tilt Up/Down    상하 틸트

Motion Score:
1-2   정적 (배경, 클로즈업)
3-4   약간 움직임 (대화, 표정)
5     활발한 움직임 (걷기, 액션)


[D] Veo 3.1 (오디오 포함)

접속: labs.google/fx/tools/flow

실행:
1. Google 로그인
2. Image to Video 선택
3. 이미지 업로드
4. Veo 프롬프트 붙여넣기
5. Generate → 다운로드

특징:
- 대사/효과음 자동 생성
- Google 크레딧 사용 가능

────────────────────────────────────────

Kling vs Veo 선택 가이드

Kling 추천:
- 캐릭터 일관성 중요할 때
- 4K 고화질 필요할 때
- 카메라 움직임 세밀 제어

Veo 추천:
- 대사나 효과음 필요한 씬
- 빠른 프로토타입
- Google 크레딧 있을 때

일반적인 방법:
Kling으로 영상 생성 → CapCut에서 오디오 추가

────────────────────────────────────────

오디오 추가 방법

Veo: 자동 생성됨

Kling (무음):
1. ElevenLabs - TTS (음성)
2. Suno - 배경음악
3. CapCut/Premiere에서 추가

────────────────────────────────────────

영상 합치기

추천 도구:
1. CapCut (무료, 추천) - 모바일/PC, 자동 자막
2. Premiere Pro - 전문가용
3. DaVinci Resolve - 무료, 컬러그레이딩 강력

방법:
씬별로 생성한 클립들을 타임라인에 순서대로 배치

────────────────────────────────────────

퀵 레퍼런스

도구              용도              접속                           특징
NanoBanana Pro    이미지            gemini.google.com              한글 OK
Midjourney V7     이미지            midjourney.com                 --cref
Kling 3.0         영상              klingai.com                    4K
Veo 3.1           영상              labs.google/fx/tools/flow      오디오 포함

────────────────────────────────────────

(c) 2026 Prompty Academy
