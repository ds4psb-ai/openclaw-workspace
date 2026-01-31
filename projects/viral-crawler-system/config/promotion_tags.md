# 🏷️ 승격 태그 체계

**작성:** 소미 🐱
**목적:** 테드 승격/탈락 결정 시 사용할 표준 태그

---

## ✅ 승격 태그 (Promote Tags)

### 콘텐츠 유형
| 태그 | 설명 | 예시 |
|------|------|------|
| `ugc` | 일반인 크리에이터 콘텐츠 | 핸드폰 촬영, 리믹스 가능 |
| `vlog` | 일상/브이로그 | 데일리, 루틴 |
| `review` | 제품/장소 리뷰 | 언박싱, 솔직후기 |
| `tutorial` | 튜토리얼/하우투 | 레시피, DIY |
| `meme` | 밈/유머 | 리액션, 챌린지 |

### 카테고리
| 태그 | 설명 |
|------|------|
| `food` | 맛집, 카페, 요리 |
| `beauty` | 뷰티, 스킨케어, GRWM |
| `fitness` | 운동, 홈트, 루틴 |
| `lifestyle` | 라이프스타일, 인테리어 |
| `tech` | 테크, 가젯, 앱 |
| `travel` | 여행, 핫플 |

### 품질 지표
| 태그 | 설명 |
|------|------|
| `high_engagement` | 참여율 10%+ |
| `trending` | 현재 트렌드 적합 |
| `filmable` | 촬영 재현 가능 |
| `original` | 독창적 아이디어 |

---

## ❌ 탈락 태그 (Reject Tags)

| 태그 | 설명 |
|------|------|
| `ad` | 광고/협찬/PPL |
| `repost` | 리포스트/도용 의심 |
| `celebrity` | 연예인/아이돌 |
| `tv_content` | TV 방송 클립 |
| `news` | 뉴스/시사 |
| `low_quality` | 저화질/저품질 |
| `not_filmable` | 재현 불가 (장비, 예산) |

---

## 📝 사용 예시

### 승격 시
```json
{
  "action": "promote",
  "tags": ["ugc", "food", "high_engagement", "filmable"],
  "reason": "카페 리뷰, 핸드폰 재현 가능"
}
```

### 탈락 시
```json
{
  "action": "reject",
  "tags": ["ad", "celebrity"],
  "reason": "PPL 광고, 연예인 출연"
}
```

---

## 🔄 태그 조합 가이드

### 자동 승격 후보 (향후)
```
high_engagement + ugc + filmable → 자동 승격 검토
```

### 자동 탈락 후보 (향후)
```
ad OR celebrity OR tv_content → 자동 탈락
```

---

**테드 피드백 후 업데이트 예정**
