# T003 – Komission 숏폼 큐레이팅 자동화 연구

**담당:** @somi @ag-komission  
**목표:** shorti.ai API로 고퀄리티 숏폼 자동 큐레이팅  
**상태:** 🔬 리서치 중

---

## 1. API 분석 결과

### 사용 가능한 엔드포인트 (API Key)

| 엔드포인트 | 용도 | 큐레이팅 활용 |
|------------|------|---------------|
| `GET /api/v1/outliers` | 아웃라이어 목록 | ⭐ 핵심. SS/S 티어 필터링 |
| `GET /api/v1/for-you` | 추천 피드 | 개인화 큐레이팅 |
| `GET /api/v1/patterns/library` | 패턴 라이브러리 | 패턴 기반 필터링 |
| `POST /api/v1/search/unified` | 통합 검색 | 키워드 기반 큐레이팅 |

### 제한사항

| 기능 | 상태 | 비고 |
|------|------|------|
| VDG 분석 | ❌ JWT 전용 | API Key로 직접 분석 불가 |
| 후보 목록 | ❌ JWT 전용 | candidates 접근 불가 |
| Analytics | ❌ JWT 전용 | 대시보드 데이터 불가 |

---

## 2. 큐레이팅 자동화 설계

### 방식 A: Outlier 기반 (권장)

```
[Cron/Heartbeat]
    ↓
[GET /api/v1/outliers?tier=SS,S&limit=10]
    ↓
[필터링: engagement_rate > 0.1, view_count > 100K]
    ↓
[중복 체크: 이미 큐레이션한 영상 제외]
    ↓
[저장: curated_videos.json]
    ↓
[알림: 새 고퀄 영상 N개 발견]
```

### 방식 B: For-You 기반

```
[Cron/Heartbeat]
    ↓
[GET /api/v1/for-you]
    ↓
[recommendations 필터: outlier_score > 1000]
    ↓
[저장 + 알림]
```

### 방식 C: Search 기반 (키워드)

```
[설정된 키워드 리스트]
    ↓
[POST /api/v1/search/unified {"query": "hook"}]
    ↓
[결과 정렬: relevance_score]
    ↓
[저장 + 알림]
```

---

## 3. 구현 계획

### Phase 1: 기본 파이프라인 (API Key만)

1. **Outlier Fetcher** - SS/S 티어 영상 주기적 수집
2. **Deduplicator** - 이미 본 영상 필터링
3. **Storage** - `artifacts/curation/` 에 JSON 저장
4. **Notifier** - 새 영상 발견 시 알림

### Phase 2: 패턴 매칭

1. **Pattern Matcher** - 패턴 라이브러리와 영상 매칭
2. **Category Filter** - 카테고리별 큐레이팅

### Phase 3: VDG 통합 (JWT 필요)

1. **VDG Analyzer** - 새 영상 자동 분석
2. **DNA Extractor** - 분석 결과에서 DNA 추출
3. **Similar Finder** - 유사 패턴 영상 추천

---

## 4. 필요 리소스

### 🔴 필수: API Key 설정

```bash
# 환경변수 설정 필요
export OPENCLAW_API_KEY="ock_live_xxxxx"
```

**테드에게 요청:**
- `OPENCLAW_API_KEY` 환경변수 설정 필요
- 또는 `.env` 파일에 추가

### 🟡 선택: JWT 토큰 (VDG 분석용)

- VDG 분석 기능 사용하려면 JWT 인증 필요
- 현재는 API Key만으로 Phase 1~2 진행 가능

---

## 5. 샘플 코드 (Phase 1)

```python
# komission_curator.py
import os
import json
import requests
from datetime import datetime

API_URL = "https://api.shorti.ai"
API_KEY = os.getenv("OPENCLAW_API_KEY")

def fetch_outliers(tier="SS,S", limit=10):
    """SS/S 티어 아웃라이어 가져오기"""
    resp = requests.get(
        f"{API_URL}/api/v1/outliers",
        headers={"X-API-Key": API_KEY},
        params={"tier": tier, "limit": limit}
    )
    return resp.json()

def filter_high_engagement(outliers, min_rate=0.1):
    """engagement_rate 기준 필터링"""
    return [o for o in outliers if o.get("engagement_rate", 0) > min_rate]

def save_curation(videos, path="artifacts/curation/"):
    """큐레이션 결과 저장"""
    filename = f"{path}{datetime.now().strftime('%Y-%m-%d')}_curation.json"
    with open(filename, "w") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    return filename

def run_curation():
    outliers = fetch_outliers()
    filtered = filter_high_engagement(outliers)
    # TODO: 중복 체크
    saved = save_curation(filtered)
    return f"Curated {len(filtered)} videos → {saved}"
```

---

## 6. 다음 단계

| 순서 | 작업 | 담당 | 상태 |
|------|------|------|------|
| 1 | API Key 설정 | 테드 | ⏳ 대기 |
| 2 | API 연결 테스트 | 소미 | ⏳ 대기 |
| 3 | Phase 1 구현 | 소미 | ⏳ 대기 |
| 4 | Cron 자동화 | 소미 | ⏳ 대기 |

---

**최종 업데이트:** 2026-01-31 07:00 KST
