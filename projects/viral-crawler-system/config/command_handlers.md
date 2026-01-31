# 🎮 Telegram 명령어 처리 로직

**작성:** 소미 🐱
**목적:** 테드 명령어 파싱 및 API 호출 로직 정의

---

## 📋 지원 명령어 목록

| 명령어 | 별칭 | 기능 | API 호출 |
|--------|------|------|----------|
| `/s` | "크롤러 상태", "상태" | 상태 확인 | `GET /crawlers/s` |
| `/p` | "크롤러 정지", "정지", "멈춰" | 일시정지 | `POST /crawlers/p` |
| `/r` | "크롤러 시작", "재개", "시작" | 재개 | `POST /crawlers/r` |
| `/run` | "크롤링 해", "수집 시작" | 수동 실행 | `POST /crawlers/run` |
| `/pending` | "대기 목록", "뭐 있어?" | 승격 대기 조회 | `GET /outliers/promotion/pending` |

---

## 🔧 명령어 파싱 로직

### 1. 크롤러 상태 (/s)

**인식 패턴:**
```
/s
크롤러 상태
상태 확인
크롤러 어때?
```

**처리 로직:**
```python
if message in ["/s", "크롤러 상태", "상태", "상태 확인"]:
    response = GET /api/v1/crawlers/s
    
    # 응답 포맷
    """
    📊 *크롤러 상태*
    
    상태: ▶️ 실행 중
    Quiet Hours: 23:00-08:00 KST
    현재 시간: 18:00 KST
    
    [정지 /p] [수동 실행 /run]
    """
```

---

### 2. 크롤러 정지 (/p)

**인식 패턴:**
```
/p
크롤러 정지
정지
멈춰
잠깐 멈춰
```

**처리 로직:**
```python
if message in ["/p", "크롤러 정지", "정지", "멈춰"]:
    response = POST /api/v1/crawlers/p
    
    # 응답 포맷
    """
    🛑 *크롤러 정지됨*
    
    재개하려면: /r
    """
```

---

### 3. 크롤러 재개 (/r)

**인식 패턴:**
```
/r
크롤러 시작
재개
시작
다시 시작
```

**처리 로직:**
```python
if message in ["/r", "크롤러 시작", "재개", "시작"]:
    response = POST /api/v1/crawlers/r
    
    # 응답 포맷
    """
    ▶️ *크롤러 재개됨*
    
    다음 크롤링: 2시간 후
    상태 확인: /s
    """
```

---

### 4. 수동 크롤링 (/run)

**인식 패턴:**
```
/run
크롤링 해
수집 시작
크롤링 시작
YouTube 크롤링
TikTok 크롤링
```

**처리 로직:**
```python
if "/run" in message or "크롤링" in message:
    # 플랫폼 파싱
    platforms = []
    if "youtube" in message.lower() or "쇼츠" in message:
        platforms.append("youtube")
    if "tiktok" in message.lower() or "틱톡" in message:
        platforms.append("tiktok")
    if not platforms:
        platforms = ["youtube", "tiktok"]  # 기본값
    
    response = POST /api/v1/crawlers/run
    Body: {"platforms": platforms, "limit": 20}
    
    # 응답 포맷
    """
    🚀 *크롤링 시작!*
    
    플랫폼: YouTube, TikTok
    Job ID: crawl_20260131_094500
    
    완료되면 알려드릴게요!
    """
```

---

### 5. 승격 대기 조회 (/pending)

**인식 패턴:**
```
/pending
대기 목록
뭐 있어?
아웃라이어 보여줘
```

**처리 로직:**
```python
if message in ["/pending", "대기 목록", "뭐 있어?"]:
    response = GET /api/v1/outliers/promotion/pending?page_size=5
    
    if response.total == 0:
        """
        📭 *승격 대기 목록 비어있음*
        
        크롤링 실행: /run
        """
    else:
        # 첫 번째 아웃라이어 상세 표시
        """
        🔍 *승격 대기* (총 {total}건)
        
        #1 - S-tier 🏆
        📌 초간단 5분 레시피
        📊 523x | 👁️ 1.2M
        🔗 [링크]
        
        [승격] [탈락] [다음]
        """
```

---

## ✅ 승격/탈락 명령어

### 승격 처리

**인식 패턴:**
```
승격
올려
좋아
ㅇㅋ
1번 승격
```

**처리 로직:**
```python
if "승격" in message or message in ["올려", "좋아", "ㅇㅋ"]:
    # 현재 보여주고 있는 아웃라이어 ID 사용
    response = POST /api/v1/outliers/promotion/{current_id}/promote
    Body: {
        "reason": "테드_수동_승격",
        "tags": [],  # 태그 파싱 가능 시 추가
        "promoted_by": "ted"
    }
    
    # 응답 포맷
    """
    ✅ *승격 완료!*
    
    📌 초간단 5분 레시피
    
    [다음 보기] [통계]
    """
    
    # decisions.jsonl 기록
    log_decision(id, "promote", "ted")
```

---

### 탈락 처리

**인식 패턴:**
```
탈락
버려
패스
안돼
ㄴㄴ
```

**처리 로직:**
```python
if "탈락" in message or message in ["버려", "패스", "ㄴㄴ"]:
    response = POST /api/v1/outliers/promotion/{current_id}/reject
    Body: {
        "reason": "테드_수동_탈락"
    }
    
    # 응답 포맷
    """
    ❌ *탈락 처리됨*
    
    [다음 보기] [통계]
    """
    
    # decisions.jsonl 기록
    log_decision(id, "reject", "ted")
```

---

### 나중에 처리

**인식 패턴:**
```
나중에
스킵
패스
다음
```

**처리 로직:**
```python
if message in ["나중에", "스킵", "다음"]:
    # API 호출 없음 - 다음 아웃라이어 표시
    show_next_outlier()
```

---

## 📊 상태 관리

### 현재 컨텍스트 유지

```python
# 세션별 상태
session_state = {
    "current_outlier_id": 123,      # 현재 보여주고 있는 ID
    "pending_queue": [123, 456],    # 대기 목록 ID
    "last_command": "/pending",      # 마지막 명령
    "last_response_time": datetime   # 마지막 응답 시간
}
```

---

## 🔐 API 호출 헬퍼

```python
API_BASE = "https://shorti-api-v2-production.up.railway.app"
API_KEY = "ock_live_9REMohW7Bp4Ryqih36Hloj5zvQnHuJjckpHwze9XDks"

async def call_api(method: str, endpoint: str, body: dict = None):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    if method == "GET":
        response = requests.get(f"{API_BASE}{endpoint}", headers=headers)
    else:
        response = requests.post(f"{API_BASE}{endpoint}", headers=headers, json=body)
    
    return response.json()
```

---

## 📝 결정 기록

```python
def log_decision(outlier_id: int, action: str, decided_by: str):
    """learning/decisions.jsonl에 기록"""
    entry = {
        "id": outlier_id,
        "action": action,  # "promote" | "reject"
        "decided_by": decided_by,  # "ted" | "somi_auto"
        "decided_at": datetime.utcnow().isoformat()
    }
    
    with open("learning/decisions.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
```

---

**테드 피드백 후 업데이트 예정**
