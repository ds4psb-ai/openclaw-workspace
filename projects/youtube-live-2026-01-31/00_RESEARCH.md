# 00. 리서치 문서 (2025 최신 데이터 기반)

**작성:** 소미 🐱 + 보미 🐰  
**업데이트:** 2026-01-31 03:05 UTC  
**소스:** Brave Search API + 공식 문서

---

## 📊 YouTube 라이브 핵심 데이터 (2025)

### 시청자 이탈 원인 (onewrk.com 리서치)
| 원인 | 비율 | 대응 |
|------|------|------|
| **오디오 품질 불량** | 64% | 외장 마이크 필수 |
| 첫 10초 품질 판단 | - | 오프닝 리허설 필수 |
| 화질 불안정 | 23% | 10Mbps+ 인터넷 |

> **핵심:** 시청자는 **첫 10초**에 퀄리티를 판단한다. 오디오가 가장 중요!

### 최적 라이브 길이 (1of10.com)
| 길이 | 효과 |
|------|------|
| 30-45분 | 최소 유효 시간 |
| **1-3시간** | Watch time 최대화 (추천) |
| 4시간+ | 시청자 피로감 주의 |

> **우리 계획:** 4시간이므로 **중간 리캡 필수** + 채팅 인터랙션으로 피로감 분산

### Watch Time = 성장 공식
- 라이브는 평균 **30분+ 시청** (일반 영상의 3배)
- 채팅 활성화 → 알고리즘에 "engaging content" 신호
- 리플레이도 검색 트래픽 유입

---

## 🎯 해외 라이브 운영 패턴 (검증된 사례)

### 1. 오프닝 10초 법칙
**출처:** YouTube Creator Academy, onewrk.com

> "시청자는 첫 10초에 남을지 떠날지 결정한다"

**실행:**
```
❌ "안녕하세요, 오늘은..."
✅ "4시간 후, 여러분도 결제 받는 앱 만들 수 있어요."
```

### 2. 이름 불러주기 효과
**출처:** 1of10.com - "Viewers love hearing their name read aloud"

**실행:**
- 첫 10분 동안 채팅 닉네임 적극 호명
- "OO님 질문 감사해요!"
- Super Chat은 무조건 읽기

### 3. 30분마다 Before/After
**출처:** 해외 라이브 운영 패턴 분석

**실행:**
```
14:30 → "지금까지: 스토리보드 UI 생성"
15:00 → "지금까지: 드래그앤드롭 기능"
15:30 → "지금까지: 스토리보드 완성!"
```

### 4. 질문 포맷 강제
**출처:** 해외 Q&A 라이브 베스트 프랙티스

**실행:**
```
❌ 자유 질문
✅ "질문은 [직업/상황/원하는 결과] 형식으로!"
예: "개발자/사이드프로젝트/결제 붙이고 싶어요"
```

---

## 💳 Polar 결제 통합 가이드 (공식 문서 기반)

### Polar란?
**출처:** polar.sh/docs/introduction

> "개발자를 위한 오픈소스 결제 인프라"
> - Stripe 기반이지만 **MoR(Merchant of Record)** 역할
> - 글로벌 세금(VAT, GST) 자동 처리
> - 기존 결제 시스템보다 **20% 낮은 수수료**

### 왜 Polar인가? (vs Stripe 직접 연동)
| 항목 | Stripe 직접 | Polar |
|------|------------|-------|
| PG 심사 | 필요 | **불필요** |
| 세금 처리 | 직접 | 자동 |
| 셋업 시간 | 수일~수주 | **몇 분** |
| 수수료 | ~3% | ~2.4% |

### 통합 순서 (Medium 튜토리얼 기반)
**출처:** medium.com/@paudelronish

```
1. Polar 계정 생성 (sandbox 환경)
2. Product/Price 생성
3. Checkout 세션 생성
4. Webhook 핸들러 설정
5. 테스트 결제
```

### 핵심 코드 (Next.js 예시)
```typescript
// 1. Polar SDK 초기화
import { Polar } from "@polar-sh/sdk";
const polarApi = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN,
  server: "sandbox" // 또는 "production"
});

// 2. Checkout 생성
const checkout = await polarApi.checkouts.create({
  productId: process.env.POLAR_PRODUCT_ID,
  customerEmail: email,
  successUrl: "https://myapp.com/success",
});

// 3. Webhook 핸들러
if (payload.type === "subscription.created") {
  // 구독 생성됨 → DB 업데이트
}
```

### 라이브 데모 순서
1. **Product 생성** (2분) - Polar 대시보드
2. **Checkout 버튼** (3분) - 앱에 추가
3. **Webhook 연동** (5분) - 결제 완료 처리
4. **테스트 결제** (2분) - 실제 결제 성공!

---

## 📺 레퍼런스 영상/문서 목록

### YouTube 라이브 운영
| 제목 | URL | 핵심 |
|------|-----|------|
| YouTube Live Guide 2025 | 1of10.com | 1-3시간 최적, 이름 호명 |
| Streaming Setup Guide | onewrk.com | 첫 10초, 오디오 64% |
| Complete 2025 Guide | YouTube | OBS 설정 |

### Polar 결제
| 제목 | URL | 핵심 |
|------|-----|------|
| Polar 공식 문서 | polar.sh/docs | Quick Start |
| Next.js 통합 | Medium | Webhook 핸들러 |
| Polar GitHub | github.com/polarsource | 오픈소스 |

### AI 앱 빌딩 라이브
| 제목 | URL | 핵심 |
|------|-----|------|
| Bolt.new Tutorials | support.bolt.new | Stripe 연동 |
| Bolt v2 Blog | bolt.new/blog | 자동 디버깅 |
| You B Tech | YouTube | PRD→앱 완주 |

---

## 🎬 오늘 라이브 적용 포인트

### 오프닝 (첫 10초)
```
"4시간 후, 여러분도 진짜 돈 받는 앱 만들 수 있어요.
코드 한 줄 없이. 에러? AI가 알아서 고쳐줍니다."
```

### 오디오 체크
- [ ] 외장 마이크 연결
- [ ] OBS 음량 -12dB ~ -6dB
- [ ] 테스트 녹음 확인

### 채팅 인터랙션
- 이름 불러주기 (첫 10분 집중)
- 30분마다 투표형 질문
- Super Chat 즉시 반응

### 리캡 타이밍
- 14:30, 15:00, 15:30, 16:00, 16:30, 17:00
- "지금까지 한 것 / 다음에 할 것"

### 결제 데모 핵심
> "Polar는 PG심사 없이 바로 결제 연동 가능해요.
> 5분 만에 진짜 결제 버튼 붙이는 거 보여드릴게요!"

---

## ✅ 검증된 데이터 요약

| 항목 | 수치/사실 | 출처 |
|------|----------|------|
| 오디오 이탈률 | 64% | onewrk.com |
| 첫 판단 시간 | 10초 | onewrk.com |
| 최적 라이브 길이 | 1-3시간 | 1of10.com |
| 평균 시청 시간 | 30분+ | 1of10.com |
| Polar 수수료 | ~2.4% | polar.sh |
| Polar 셋업 | 몇 분 | polar.sh |

---

**이 문서는 Brave Search API로 수집한 2025년 최신 데이터 기반입니다.**
