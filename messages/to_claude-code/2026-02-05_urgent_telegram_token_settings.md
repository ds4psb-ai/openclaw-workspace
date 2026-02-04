# [URGENT] telegram_webhook.py settings 토큰/시크릿 처리 수정 요청

테드 코멘트: 개발 거의 끝난 듯. 아래 diff 방향으로 **토큰/시크릿 관련 hasattr fallback 제거**하고, settings 값이 없으면 그냥 빈 문자열로 처리하지 말고 **명시적으로 settings.*를 직접 참조 + falsy면 return** 패턴으로 통일해줘.

## 요청 변경사항 (예시 diff)

### 1) TELEGRAM_WEBHOOK_SECRET
```diff
- _TELEGRAM_WEBHOOK_SECRET = settings.TELEGRAM_WEBHOOK_SECRET if hasattr(settings, "TELEGRAM_WEBHOOK_SECRET") else ""
+ _TELEGRAM_WEBHOOK_SECRET = settings.TELEGRAM_WEBHOOK_SECRET
```

### 2) answerCallbackQuery
```diff
- token = settings.TELEGRAM_BOT_TOKEN if hasattr(settings, "TELEGRAM_BOT_TOKEN") else ""
- if not token:
+ if not settings.TELEGRAM_BOT_TOKEN:
    return
- url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
+ url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
```

### 3) editMessageText
```diff
- token = settings.TELEGRAM_BOT_TOKEN if hasattr(settings, "TELEGRAM_BOT_TOKEN") else ""
- if not token:
+ if not settings.TELEGRAM_BOT_TOKEN:
    return
- url = f"https://api.telegram.org/bot{token}/editMessageText"
+ url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/editMessageText"
```

## 범위
- `backend/app/routers/telegram_webhook.py` 내 **모든 Telegram 토큰/시크릿 참조**에 대해 동일하게 적용해줘. ("그리고 계속해" = 동일 패턴 반복)

## 의도
- settings에 값이 설정돼있지 않은 상태를 조용히 통과시키지 말고(빈 문자열), 빠르게 return/에러로 드러나게.

처리 후 커밋/푸시 부탁.
