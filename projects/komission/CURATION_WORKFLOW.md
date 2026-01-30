# 📊 Komission 숏폼 큐레이팅 자동화 워크플로우

**작성:** 소미 🐱
**날짜:** 2026-01-31

---

## 🎯 목표
shorti.ai API를 활용해 고퀄리티 숏폼 콘텐츠를 자동으로 큐레이팅

---

## 🔄 워크플로우 (5단계)

### 1️⃣ 수집 (Collection)
```
API: /api/v1/outliers
     /api/v1/for-you
```
- 아웃라이어 영상 자동 수집
- 추천 피드에서 트렌딩 콘텐츠 가져오기
- **주기:** 매일 1회

### 2️⃣ 트리아지 (Triage)
```
API: /api/v1/vdg/async/analyze
```
- VDG 분석으로 바이럴 패턴 추출
- 0~100 스코어링
- **기준:**
  - 바이럴 지수 > 70
  - 패턴 일치도 > 60%
  - 참신도 (기존 라이브러리 대비)

### 3️⃣ 심층 검토 (Deep Review)
```
API: /api/v1/patterns/search
     /api/v1/clusters
```
- 유사 패턴 클러스터 확인
- DNA 매칭으로 중복 제거
- 태깅: `#hook` `#transition` `#cta` 등

### 4️⃣ 주간 숏리스트 (Weekly Shortlist)
- Top 10~20 선정
- 카테고리별 분류:
  - 🔥 트렌딩 훅
  - 🎬 트랜지션
  - 💡 새로운 패턴
  - 📈 검증된 포맷

### 5️⃣ 발행 & 피드백
- 뉴스레터/채널 발행
- 성과 추적
- 피드백 반영 → 다음 주기에 적용

---

## 🏷️ 태깅 택소노미

| 카테고리 | 태그 예시 |
|---------|----------|
| 훅 유형 | `#question-hook` `#shock-hook` `#curiosity-hook` |
| 포맷 | `#tutorial` `#storytime` `#pov` `#duet` |
| 감정 | `#funny` `#emotional` `#satisfying` |
| 산업 | `#beauty` `#food` `#tech` `#fitness` |

---

## 📊 스코어링 기준

```
Total Score = 
  (Viral Index × 0.4) +
  (Pattern Match × 0.3) +
  (Novelty × 0.2) +
  (Engagement Rate × 0.1)
```

| 등급 | 점수 | 액션 |
|------|------|------|
| S | 90+ | 즉시 숏리스트 |
| A | 70-89 | 심층 검토 |
| B | 50-69 | 대기열 |
| C | <50 | 제외 |

---

## ⚙️ 자동화 구현

### Cron 스케줄
```
# 매일 09:00 - 아웃라이어 수집
0 9 * * * /scripts/collect_outliers.sh

# 매일 12:00 - VDG 분석
0 12 * * * /scripts/run_vdg_analysis.sh

# 금요일 15:00 - 주간 숏리스트 생성
0 15 * * 5 /scripts/generate_shortlist.sh
```

### 필요한 것
- [ ] **OPENCLAW_API_KEY** (테드에게 요청)
- [ ] 수집 스크립트 작성
- [ ] 분석 파이프라인 구현
- [ ] 숏리스트 템플릿

---

## 📝 숏리스트 템플릿

```markdown
# 🔥 주간 숏폼 큐레이션 (W05/2026)

## Top Picks

### 1. [영상 제목]
- **URL:** tiktok.com/...
- **Score:** 95/100
- **패턴:** #shock-hook #tutorial
- **왜 좋은가:** ...
- **적용 아이디어:** ...
```

---

## 🚀 다음 단계

1. API 키 받기
2. 수집 스크립트 테스트
3. VDG 분석 파이프라인 구축
4. 첫 주간 숏리스트 생성
