# 🚀 OpenClaw 설치 가이드 (Vultr VPS)

**대상:** 완전 초보자 (터미널 처음 써보는 분도 OK!)  
**소요 시간:** 약 30분  
**비용:** 첫 달 무료! (아래 링크 사용 시)

---

## 📋 목차

1. [Vultr 가입하기](#1-vultr-가입하기)
2. [서버 만들기](#2-서버-만들기)
3. [서버 접속하기](#3-서버-접속하기)
4. [OpenClaw 설치하기](#4-openclaw-설치하기)
5. [텔레그램 연결하기](#5-텔레그램-연결하기)
6. [테스트하기](#6-테스트하기)
7. [문제 해결](#7-문제-해결)

---

## 1. Vultr 가입하기

### 1-1. 회원가입 (무료 크레딧 받기!)

👉 **[이 링크로 가입하면 첫 달 무료!](https://www.vultr.com/?ref=9861802)**

1. 위 링크 클릭
2. **Create Account** 버튼 클릭
3. 이메일, 비밀번호 입력
4. 이메일 인증 (받은 메일에서 링크 클릭)

### 1-2. 결제 수단 등록

> ⚠️ 무료 크레딧 받으려면 결제 수단 등록 필수! (바로 청구 안 됨)

1. 로그인 후 **Billing** 메뉴 클릭
2. **Add Payment Method** 클릭
3. 신용카드 또는 PayPal 등록
4. 무료 크레딧 자동 적용됨 ✅

---

## 2. 서버 만들기

### 2-1. 새 서버 생성

1. 왼쪽 메뉴에서 **Products** 클릭
2. 오른쪽 상단 **Deploy +** 버튼 클릭 (파란색)
3. **Deploy New Server** 선택

### 2-2. 서버 종류 선택

| 항목 | 선택 |
|------|------|
| Choose Type | **Cloud Compute** (가장 왼쪽) |
| CPU & Storage | **Regular Performance** |

### 2-3. 서버 위치 선택

**추천:** 🇰🇷 Seoul (한국) 또는 🇯🇵 Tokyo (일본)

> 본인 위치와 가까울수록 빠름!

### 2-4. 운영체제 선택

| 항목 | 선택 |
|------|------|
| Image Type | **Operating System** |
| OS | **Ubuntu 24.04 LTS x64** ⭐ 추천 |

> 다른 버전도 되지만, 24.04 LTS가 가장 안정적

### 2-5. 서버 사양 선택

**최소 사양 (월 $6):**
| 항목 | 값 |
|------|-----|
| vCPU | 1 |
| RAM | 1 GB |
| Storage | 25 GB SSD |

**추천 사양 (월 $12):** ⭐
| 항목 | 값 |
|------|-----|
| vCPU | 1 |
| RAM | 2 GB |
| Storage | 55 GB SSD |

> 무료 크레딧 있으니 $12 사양 추천!

### 2-6. 추가 설정

| 항목 | 설정 |
|------|------|
| Auto Backups | OFF (비용 절약) |
| IPv6 | ON (무료) |
| Server Hostname | `openclaw` (원하는 이름) |

### 2-7. 배포!

1. 맨 아래 **Deploy Now** 클릭
2. 2-3분 기다리기 (Installing → Running)
3. Status가 **Running** 되면 완료! ✅

---

## 3. 서버 접속하기

### 3-1. 접속 정보 확인

1. 서버 목록에서 방금 만든 서버 클릭
2. 아래 정보 메모 (또는 복사):

```
IP Address: 123.456.789.000 (예시)
Username: root
Password: xxxxxx (눈 아이콘 클릭해서 보기)
```

### 3-2. 접속 방법 선택

#### 방법 A: 웹 콘솔 (가장 쉬움!) ⭐

1. 서버 상세 페이지에서 오른쪽 상단 **View Console** 클릭
2. 검은 화면 나오면 아무 키나 누르기
3. `login:` 나오면 `root` 입력 후 Enter
4. `Password:` 나오면 비밀번호 입력 후 Enter

> 💡 비밀번호 입력 시 화면에 안 보이는 게 정상!

#### 방법 B: Mac 터미널

1. Mac에서 **터미널** 앱 열기 (Spotlight에서 "터미널" 검색)
2. 아래 명령어 입력 (IP 주소 바꿔서):

```bash
ssh root@123.456.789.000
```

3. `yes` 입력 후 Enter
4. 비밀번호 입력 후 Enter

#### 방법 C: Windows (PowerShell)

1. Windows 검색에서 **PowerShell** 열기
2. 아래 명령어 입력:

```powershell
ssh root@123.456.789.000
```

3. `yes` 입력 후 Enter
4. 비밀번호 입력 후 Enter

### 3-3. 접속 성공 확인

아래처럼 보이면 성공! 🎉

```
Welcome to Ubuntu 24.04 LTS
...
root@openclaw:~#
```

---

## 4. OpenClaw 설치하기

> 이제부터 명령어를 하나씩 복사해서 붙여넣기 하세요!

### 4-1. 시스템 업데이트

```bash
apt update && apt upgrade -y
```

> 1-2분 걸림. 완료되면 다음 단계로!

### 4-2. Node.js 설치

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
```

설치 확인:
```bash
node --version
```
`v22.x.x` 나오면 성공!

### 4-3. OpenClaw 설치

```bash
npm install -g openclaw
```

설치 확인:
```bash
openclaw --version
```
버전 번호 나오면 성공!

### 4-4. OpenClaw 초기 설정

```bash
openclaw init
```

이 명령어 실행하면 질문들이 나와요:

| 질문 | 답변 |
|------|------|
| Where to store config? | Enter (기본값) |
| API Provider | `anthropic` 선택 |
| API Key | Anthropic API 키 입력 |

> 💡 Anthropic API 키가 없다면? → [console.anthropic.com](https://console.anthropic.com)에서 발급

---

## 5. 텔레그램 연결하기

### 5-1. 텔레그램 봇 만들기

1. 텔레그램에서 **@BotFather** 검색해서 채팅 시작
2. `/newbot` 입력
3. 봇 이름 입력 (예: `My OpenClaw Bot`)
4. 봇 유저네임 입력 (예: `my_openclaw_bot`) - 반드시 `_bot`으로 끝나야 함
5. **토큰** 복사해두기 (예: `1234567890:ABCdefGHI...`)

### 5-2. 내 텔레그램 ID 확인

1. 텔레그램에서 **@userinfobot** 검색해서 채팅 시작
2. `/start` 입력
3. **Id** 숫자 복사해두기 (예: `1234567890`)

### 5-3. OpenClaw 설정 파일 수정

```bash
nano ~/.openclaw/config.yaml
```

아래 내용 추가 (또는 수정):

```yaml
channels:
  telegram:
    token: "여기에_봇_토큰_붙여넣기"
    ownerIds:
      - "여기에_내_텔레그램_ID"
```

저장하고 나가기:
- `Ctrl + O` → Enter (저장)
- `Ctrl + X` (나가기)

### 5-4. OpenClaw 시작!

```bash
openclaw gateway start
```

---

## 6. 테스트하기

### 6-1. 텔레그램에서 테스트

1. 아까 만든 봇에게 메시지 보내기
2. "안녕!" 입력
3. 봇이 대답하면 성공! 🎉

### 6-2. 상태 확인

서버에서:
```bash
openclaw status
```

정상이면 이렇게 보여요:
```
Gateway: running
Uptime: ...
Sessions: 1
```

---

## 7. 문제 해결

### ❌ "command not found: openclaw"

Node.js가 제대로 설치 안 됨. 다시 설치:
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
npm install -g openclaw
```

### ❌ 텔레그램 봇이 응답 안 함

1. 토큰 확인:
```bash
cat ~/.openclaw/config.yaml
```

2. 로그 확인:
```bash
openclaw gateway logs
```

3. 재시작:
```bash
openclaw gateway restart
```

### ❌ API 키 오류

```bash
openclaw init
```
다시 실행해서 API 키 재입력

### ❌ 서버 재부팅 후 작동 안 함

OpenClaw 다시 시작:
```bash
openclaw gateway start
```

자동 시작 설정 (선택):
```bash
openclaw gateway enable
```

---

## 🎉 완료!

축하합니다! OpenClaw가 24시간 돌아가는 AI 비서가 생겼어요!

### 다음 단계

- 📖 [OpenClaw 문서](https://docs.openclaw.ai)
- 💬 [Discord 커뮤니티](https://discord.com/invite/clawd)
- 🛠️ 설정 커스터마이징

### 유용한 명령어

| 명령어 | 설명 |
|--------|------|
| `openclaw status` | 상태 확인 |
| `openclaw gateway logs` | 로그 보기 |
| `openclaw gateway restart` | 재시작 |
| `openclaw gateway stop` | 중지 |

---

## 💡 팁

### 비용 절약

- 사용 안 할 때: 서버 Snapshot 찍고 삭제 → 나중에 복원
- 무료 크레딧 다 쓰면: 최소 사양($6)으로 변경

### 보안 강화

비밀번호 대신 SSH 키 사용 (고급):
```bash
# 로컬 컴퓨터에서
ssh-keygen -t ed25519

# 서버에 키 복사
ssh-copy-id root@서버IP
```

---

**문의:** 문제 있으면 Discord 커뮤니티에서 질문하세요!

---

*이 가이드는 2026년 2월 기준입니다.*  
*작성: 소미 🐱*
