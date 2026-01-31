# 04. Polar 결제 연동 가이드 (16:30-17:30) - 공식 문서 기반 v3

**출처:** polar.sh/docs, Medium 튜토리얼 (paudelronish)

---

## 💳 Polar 소개 (5분)

### 왜 Polar인가?
```
"결제 연동하면 보통 뭐가 필요하죠?

❌ PG사 심사 (최소 며칠~몇 주)
❌ 사업자등록증
❌ 세금 처리 직접
❌ 복잡한 Stripe 설정

Polar는 이게 다 필요 없어요."
```

### Polar = Merchant of Record
```
"Polar가 뭐냐면요,

Stripe 위에서 돌아가는데,
'Merchant of Record' 역할을 해요.

쉽게 말하면:
- 세금? Polar가 처리
- 환불? Polar가 처리  
- 법적 문제? Polar가 책임

여러분은 링크만 붙이면 됩니다."
```

### 수수료 비교
| 서비스 | 수수료 | 셋업 시간 |
|--------|--------|----------|
| Stripe 직접 | ~3% | 며칠~주 |
| Paddle | ~5% | 며칠 |
| **Polar** | **~2.4%** | **몇 분** |

---

## 🛠️ Step 1: Polar 계정 + 상품 생성 (10분)

### 대시보드 접속
```
1. polar.sh 접속
2. GitHub 로그인 (가장 빠름)
3. Organization 생성 or 선택
```

### 상품(Product) 생성
```
Products → Create Product

이름: "Vivid Pro"
설명: "AI 스토리보드 Pro 기능"
가격: $9.99/월 (또는 일회성)

→ Create!
```

### 화면에 보여줄 것
- Product ID 복사
- Price ID 복사
- "이 두 개가 핵심이에요"

---

## 🔗 Step 2: Checkout 버튼 추가 (15분)

### 가장 간단한 방법 (링크)
```
"가장 쉬운 방법:
Polar에서 Checkout Link 복사해서
버튼에 붙이면 끝!"
```

```html
<a href="https://polar.sh/checkout/...">
  Pro 업그레이드
</a>
```

### 고급 방법 (코딩 아는 분용)
> 코드로 더 세밀하게 조절 가능하지만,
> 오늘은 쉬운 방법(링크)으로 할게요!

### 멘트
```
"코딩 아시는 분들은 더 고급 방법도 있어요.
근데 오늘은 제일 쉬운 방법으로 갑니다!

결과는 똑같아요!"
```

---

## 🔔 Step 3: 결제 완료 알림 연동 (15분)

### 이게 뭔지
```
"결제가 완료되면 Polar가 우리한테 알려줘요.
'이 사람 결제했어!' 하고요.

그러면 우리 앱이 '아, 이 분 Pro 회원이구나!' 
하고 자동으로 기능을 열어주는 거예요."
```

### Polar 대시보드 설정
```
Settings → Webhooks → Add Endpoint

URL: https://myapp.com/api/webhook/polar
Events: 
  ✅ checkout.updated
  ✅ subscription.created
  ✅ subscription.canceled

→ Save
```

### Webhook 핸들러 (Next.js)
```typescript
// app/api/webhook/polar/route.ts
import { Webhooks } from "@polar-sh/nextjs";

export const POST = Webhooks({
  webhookSecret: process.env.POLAR_WEBHOOK_SECRET,
  onPayload: async (payload) => {
    
    if (payload.type === "checkout.updated") {
      // 결제 완료!
      const checkout = payload.data;
      if (checkout.status === "confirmed") {
        // DB에 Pro 권한 부여
        await db.user.update({
          where: { email: checkout.customerEmail },
          data: { plan: "pro" }
        });
      }
    }
    
    if (payload.type === "subscription.created") {
      // 구독 시작!
      console.log("New subscriber:", payload.data);
    }
  }
});
```

---

## ✅ Step 4: 테스트 결제 (10분)

### Sandbox 모드 확인
```
"중요! 테스트할 때는 Sandbox 모드로!
진짜 카드 긁으면 안 돼요 😅"
```

### 테스트 순서
```
1. 앱에서 "Pro 업그레이드" 버튼 클릭
2. Polar 결제창 열림
3. 테스트 카드로 결제
   - 카드번호: 4242 4242 4242 4242
   - 만료: 아무 미래 날짜
   - CVC: 아무 숫자
4. 결제 완료!
5. Webhook 수신 확인
6. DB에서 Pro 권한 확인
```

### 성공 멘트 (하이라이트!)
```
"봤죠?! 진짜 됩니다!

5분 전에는 버튼만 있었는데,
지금은 진짜 결제가 돼요.

이게 Polar의 힘이에요.
PG심사? 필요 없어요."
```

---

## 🚨 트러블슈팅

### 결제창 안 열림
```
원인: Checkout URL 오류
해결: Polar 대시보드에서 새 링크 복사
```

### Webhook 안 옴
```
원인: URL 오타 or 서버 다운
해결: 
1. URL 확인
2. 서버 로그 확인
3. Polar 대시보드 → Webhooks → Logs
```

### API 에러 코드
| 코드 | 의미 | 해결 |
|------|------|------|
| 400 | 잘못된 요청 | 파라미터 확인 |
| 401 | 인증 실패 | API 키 확인 |
| 404 | 상품 없음 | Product ID 확인 |
| 500 | 서버 에러 | 잠시 후 재시도 |

---

## 📋 필수 환경변수

```env
# .env.local
POLAR_ACCESS_TOKEN=polar_at_xxx
POLAR_WEBHOOK_SECRET=polar_wh_xxx
POLAR_PRODUCT_ID=prod_xxx
POLAR_ORG_ID=org_xxx
```

---

## 🎯 라이브 데모 시간 배분

| 시간 | 내용 | 목표 |
|------|------|------|
| 16:30 | Polar 소개 | 왜 좋은지 이해 |
| 16:35 | 상품 생성 | Product ID 획득 |
| 16:45 | Checkout 버튼 | 버튼 클릭 → 결제창 |
| 17:00 | Webhook 연동 | 결제 완료 → DB 반영 |
| 17:15 | 테스트 결제 | **성공 순간 = 하이라이트!** |
| 17:25 | Q&A | 결제 관련 질문 |

---

## 💡 핵심 메시지

```
"결제 기능은 어렵지 않아요.
Polar 덕분에 5분이면 됩니다.

어려운 건 '결제 붙일 가치가 있는 앱을 만드는 것'이에요.
그건 오늘 우리가 3시간 동안 한 거죠!"
```

---

**담당:** 보미 🐰 (기술) + 소미 🐱 (멘트)  
**버전:** v3 (공식 문서 기반)
