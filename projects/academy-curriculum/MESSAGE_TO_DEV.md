# 📨 개발자에게 보낼 메시지 (복사용)

---

## 짧은 버전 (카톡/슬랙용)

```
안녕하세요! 성수동 AI 영상 아카데미 커리큘럼 기획이 거의 완료됐어요.

crebit.studio에 아카데미 섹션 구현하고 싶은데, 기획 문서 5개 전달드릴게요.
검토하시고 기술적으로 가능한 범위 + 대략 일정 알려주시면 감사하겠습니다!

📁 문서 위치: projects/academy-curriculum/
- 00_RESEARCH.md (시장조사)
- 01_TOOL_STACK.md (툴 스택)  
- 02_NOTEBOOKLM_DNA_TEMPLATE.md (DNA 템플릿)
- 03_VEO_KLING_JSON_SCHEMA.md (API 스키마)
- 04_8WEEK_CURRICULUM.md (8주 커리큘럼) ⭐ 핵심
- COLLAB_REQUEST_VIVID_DEV.md (협업 요청 상세) ⭐ 이것부터

핵심 요청:
1. 아카데미 랜딩 페이지 (crebit.studio/academy)
2. 수강생 대시보드 (진도/자료/과제)
3. 기존 Vivid 앱 연동 (Abyss Mirror, Prompt Alchemy 등)

2/3 1기 시작인데 일정 빠듯해서요 ㅠㅠ 최소 MVP라도 가능할지 봐주세요!
```

---

## 긴 버전 (이메일용)

```
제목: [협업요청] 성수동 아카데미 → crebit.studio 구현 건

안녕하세요,

성수동 AI 영상 아카데미 커리큘럼 기획이 마무리 단계입니다.
이걸 crebit.studio에 구현해서 수강생 관리 + Vivid 앱 연동하고 싶습니다.

■ 배경
- 8주 오프라인 아카데미 (24만원, 소수정예)
- Curious Refuge 대비 75% 저렴 + 한국어 + 거장 DNA 특화
- 2/3 (화) 1기 시작 예정

■ 구현 희망 사항
1. 아카데미 랜딩 페이지 (코스 소개, 등록 CTA)
2. 수강생 전용 대시보드 (로그인, 진도, 자료, 과제)
3. 기존 Vivid Dimension Apps 연동
4. (가능하면) Veo/Kling API 연동

■ 전달 문서 (GitHub repo 참조)
- projects/academy-curriculum/ 폴더 전체
- 특히 COLLAB_REQUEST_VIVID_DEV.md 먼저 봐주세요

■ 논의 필요 사항
- 기술적 가능 범위
- 대략적 공수 (몇 MD?)
- 현실적 일정 (2/3 전 MVP 가능?)
- 추가 리소스 필요 여부

일정이 빠듯한 건 알고 있습니다.
최소 MVP (랜딩 + 기본 대시보드)라도 가능한지 검토 부탁드려요.

시간 되실 때 짧게 통화하거나 미팅하면 좋겠습니다.
감사합니다!

Ted
```

---

## 첨부 파일 안내

개발자에게 공유할 때:
1. **GitHub repo 접근권한 주기** (가장 쉬움)
2. 또는 폴더 전체 zip으로 전달
3. 또는 Notion/Google Docs에 복사

```bash
# 폴더 전체 zip
cd /path/to/workspace
zip -r academy-curriculum.zip projects/academy-curriculum/
```
