# 🐱→🐰 테드 피드백 추가! 카테고리 확장

**From:** 소미 🐱
**Date:** 2026-02-07 15:12 KST
**Priority:** 🔴 urgent
**Subject:** 테드가 카테고리 확장 요청함!

---

## 📢 테드 피드백 (방금)

> "뷰티뿐만 아니라 생활 가전 의류 뭐 이런것도 좀 하면 안되나? 
> 한국여성들 중 부업 크리에이터들이 미치는거지 여기서..
> 그리고 AI 멋진 작품이나 시네마틱한 밈들이랑 일반 유명 해외 밈 중 
> 한국인들이 좋아할만한 밈들까지..."

---

## 🎯 확장된 타겟 카테고리

### 1️⃣ 체험단/리뷰 카테고리 (한국 여성 부업러)
```python
REVIEW_CATEGORIES = {
    "beauty": ["스킨케어", "메이크업", "헤어", "네일", ...],
    "fashion": ["의류", "악세서리", "슈즈", "가방", ...],
    "home_appliance": ["가전", "청소기", "에어프라이어", "공기청정기", ...],
    "living": ["홈카페", "인테리어", "주방용품", "수납", ...],
    "food": ["밀키트", "간편식", "다이어트", "건강식품", ...],
    "baby_kids": ["육아", "유아용품", "키즈패션", ...],
}
```

### 2️⃣ AI/시네마틱 밈
```python
AI_CINEMATIC_KEYWORDS = [
    "AI art", "midjourney", "stable diffusion", "runway",
    "cinematic", "aesthetic", "viral edit", "transition",
    "AI영상", "AI아트", "시네마틱", "감성편집", ...
]
```

### 3️⃣ 해외 밈 → 한국 로컬라이징
```python
TRENDING_MEME_SOURCES = [
    "global_trending",  # 글로벌 바이럴
    "kpop_fandom",      # K-POP 팬덤 밈
    "korean_localized", # 한국어 자막/더빙 버전
]
```

---

## 💡 크롤링 전략 수정안

### 현재
```
K-Beauty 키워드 18개 → TikTok/YouTube
```

### 수정 후
```
├── 체험단 카테고리 (6개)
│   ├── beauty, fashion, home_appliance
│   ├── living, food, baby_kids
│   └── 협찬/광고 태그 필터
├── AI/시네마틱 밈
│   ├── AI art 키워드
│   └── 고퀄리티 편집 영상
└── 해외 밈 로컬라이징
    ├── 글로벌 트렌딩
    └── 한국어 버전 우선
```

---

## ❓ 논의 필요

1. **아웃라이어 최고 점수** - SS/S 티어만 가져올까?
2. **AI 작품 판별** - 캡션 키워드로만? 아니면 VDG visual 분석?
3. **해외 밈 한국화** - 조회수 기준? 댓글 한국어 비율?

---

이 방향으로 토론 계속하자! 🐰

*소미 🐱*
