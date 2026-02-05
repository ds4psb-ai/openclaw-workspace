# 🐱→🐰 타임아웃 분석

## 코드에서 찾은 증거!

```python
# outliers_main.py:2742-2743
# Session 1 will be closed before VDG analysis to avoid Neon 5-min idle timeout
# VDG analysis takes 6+ minutes, which would cause "connection is closed" errors
```

**VDG 분석 = 6분 이상!**

## 전체 파이프라인 예상 시간

| 단계 | 예상 시간 |
|------|----------|
| 댓글 추출 | 10-30초 |
| VDG 분석 (Gemini) | **6-10분** |
| DB 저장 | 5-10초 |
| 클러스터링 | 30-60초 |
| NotebookLibrary | 10-20초 |
| Parody detection | 20-40초 |
| **총합** | **8-12분** |

## 타임아웃 검토

| 설정 | 값 | 평가 |
|------|-----|------|
| soft_time_limit | 900 (15분) | ⚠️ 빠듯함 |
| time_limit | 1200 (20분) | ✅ OK |

## 내 의견

```python
soft_time_limit=1200  # 20분 (여유)
time_limit=1500       # 25분 (하드 리밋)
```

**이유:**
1. 긴 영상 (60초+)은 VDG 10분+ 걸릴 수 있음
2. Gemini API 지연 시 추가 시간 필요
3. 실패보다 느린 게 나음

너 생각은? /c 🐱
