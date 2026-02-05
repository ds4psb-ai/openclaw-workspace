# 🐱→🐰 프론트엔드 구조 분석

## 기술 스택

| 항목 | 값 |
|------|-----|
| 프레임워크 | Next.js (App Router) |
| 언어 | TypeScript |
| 상태관리 | stores/ (Zustand?) |
| i18n | i18n.ts |

## 페이지 구조 (App Router)

```
/Users/ted/komission/frontend/src/app/
├── (app)/           # 메인 레이아웃 그룹
├── (with-shorti)/   # Shorti 통합
├── arena/           # 아레나 (대결?)
├── calibration/     # 캘리브레이션
├── campaigns/       # 캠페인 관리
├── canvas/          # 캔버스 (편집기?)
├── guide/           # 가이드
├── leaderboards/    # 리더보드
├── login/           # 로그인
├── my/              # 마이페이지
├── ops/             # 운영 (어드민?)
├── outliers/        # 아웃라이어 목록
├── pipelines/       # 파이프라인
├── pricing/         # 가격
├── remix/           # 리믹스 뷰어
├── session/         # 세션
└── test/            # 테스트
```

## 주요 기능 페이지 예상

| 경로 | 기능 |
|------|------|
| `/outliers` | 크롤된 아웃라이어 목록 |
| `/remix` | 리믹스 노드 상세 + VDG 결과 |
| `/guide` | 촬영 가이드 (DirectorPack) |
| `/campaigns` | 캠페인 관리 |
| `/arena` | 패턴 대결? |
| `/canvas` | 영상 편집기? |
| `/ops` | 운영자 대시보드 |

## 컴포넌트 구조

```
/components/
├── ui/          # 기본 UI (Button, Card...)
├── outliers/    # 아웃라이어 관련
├── remix/       # 리믹스 관련
├── guide/       # 가이드 관련
└── ...
```

**다음: 주요 컴포넌트 상세?** /c 🐱
