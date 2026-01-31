# 📚 Learning Data

재귀 학습을 위한 데이터 저장소

## 파일 구조

- `rules.json` - 자동 승격/탈락 규칙
- `decisions.jsonl` - 테드 결정 기록 (승격/탈락)
- `stats_weekly.json` - 주간 통계 (자동 생성)
- `patterns.md` - 발견된 패턴 문서화

## 데이터 형식

### decisions.jsonl
```json
{
  "id": 123,
  "video_id": "abc123",
  "action": "promote",
  "tags": ["cafe", "ugc"],
  "reason": "카페 리뷰 적합",
  "score": 450,
  "decided_by": "ted",
  "decided_at": "2026-01-31T10:00:00Z"
}
```

## 학습 주기

- **일일:** decisions.jsonl 기록
- **주간:** 패턴 분석 → rules.json 업데이트 제안
- **월간:** 자동화율 리뷰
