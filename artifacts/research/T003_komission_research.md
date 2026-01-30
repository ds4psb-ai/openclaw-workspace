# T003 - Komission 숏폼 큐레이팅 자동화 연구

**담당:** @somi 🐱  
**시작:** 2026-01-30 21:33 UTC  
**상태:** 🟡 진행 중

---

## 🎯 목표
shorti.ai API를 활용한 고퀄리티 숏폼 자동 큐레이팅 시스템 설계

---

## 📚 API 조사 결과

### Base URL
- `https://api.shorti.ai`
- 인증: `X-API-Key: <OPENCLAW_API_KEY>`

### 핵심 엔드포인트

| 기능 | 엔드포인트 | 용도 |
|------|-----------|------|
| VDG 분석 | `/api/v1/vdg/async/analyze` | 영상 URL → AI 분석 |
| 아웃라이어 | `/api/v1/outliers` | 급상승 영상 목록 |
| 패턴 검색 | `/api/v1/patterns/*` | 바이럴 패턴 DB |
| 추천 피드 | `/api/v1/for-you` | 맞춤 추천 |
| 통합 검색 | `/api/v1/search/unified` | 키워드 검색 |

### VDG (Viral Depth Genealogy)
- Gemini 2.5 Pro 멀티모달 분석
- OpenCV 영상 처리
- 오디오 분석
- 바이럴 패턴 자동 추출

---

## 🔧 자동화 파이프라인 설계

### Phase 1: 아웃라이어 수집
```
1. /api/v1/outliers 호출 (주기적)
2. 급상승 영상 목록 수집
3. 필터링 (조회수, 좋아요, 카테고리)
```

### Phase 2: VDG 분석
```
1. 선별된 영상 URL → /api/v1/vdg/async/analyze
2. AI 분석 결과 수신
3. 패턴 추출 및 저장
```

### Phase 3: 큐레이팅
```
1. 패턴 DB에서 유사 패턴 검색
2. 트렌드 클러스터링
3. 인사이트 리포트 생성
```

### Phase 4: 자동 리포트
```
1. 일간/주간 트렌드 요약
2. 추천 콘텐츠 아이디어
3. 테드에게 알림
```

---

## 🛠️ 구현 계획

### 스크립트 구조
```
scripts/
├── komission/
│   ├── fetch_outliers.py     # 아웃라이어 수집
│   ├── analyze_vdg.py        # VDG 분석 트리거
│   ├── curate_patterns.py    # 패턴 큐레이팅
│   └── generate_report.py    # 리포트 생성
```

### cron 스케줄
- 아웃라이어 수집: 매 6시간
- VDG 분석: 새 영상 발견 시
- 리포트 생성: 매일 09:00 KST

---

## ⚠️ 필요 사항

### 1. API 키 필요
- `OPENCLAW_API_KEY` 환경변수 미설정
- 테드에게 API 키 요청 필요

### 2. 구현 필요
- [ ] 아웃라이어 수집 스크립트
- [ ] VDG 분석 자동화
- [ ] 패턴 저장/검색 로직
- [ ] 리포트 생성기
- [ ] cron job 설정

---

## 📅 다음 단계

1. ⏸️ API 키 확보 대기
2. 🔜 아웃라이어 수집 스크립트 작성 (mock 데이터로 테스트)
3. 🔜 VDG 분석 파이프라인 구현
4. 🔜 자동 리포트 시스템

---

**업데이트:** 2026-01-30 21:45 UTC  
**작성:** 소미 🐱
