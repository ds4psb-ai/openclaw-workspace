# 🐱→🐰 Celery Worker 전체 구조

## 파일별 태스크 목록

### 1. vdg_tasks.py (VDG 분석)
| 태스크 | 설명 |
|--------|------|
| `analyze_video` | VDG만 분석 (기존) |
| `analyze_full_pipeline` | **전체 파이프라인 (NEW!)** |
| `batch_analyze` | 배치 분석 |
| `run_stuck_recovery` | stuck 복구 (15분마다) |
| `run_reanalysis_queue` | 재분석 큐 처리 |
| `send_drift_report` | 드리프트 리포트 |
| `run_ml_drift_report` | ML 드리프트 |
| `refresh_baseline` | 베이스라인 리프레시 |
| `health_check` | 헬스체크 |

### 2. tiktok_tasks.py (TikTok 크롤러)
| 태스크 | 설명 |
|--------|------|
| `crawl_tiktok_socialkit` | SocialKit 크롤링 |
| `crawl_tiktok_meme` | Meme 크롤링 |
| `enrich_outlier_scores` | 점수 보강 |
| `auto_promote_outliers` | 자동 승격 |

### 3. youtube_tasks.py (YouTube 크롤러)
| 태스크 | 설명 |
|--------|------|
| `crawl_youtube_trending` | 트렌딩 크롤링 |
| `crawl_youtube_strategy` | 전략 크롤링 |
| `health_check` | 헬스체크 |

### 4. beauty_scout_tasks.py
| 태스크 | 설명 |
|--------|------|
| `scout_beauty_outliers` | K-Beauty SS/S tier 알림 |

### 5. notebooklm_tasks.py
| 태스크 | 설명 |
|--------|------|
| `resync_cluster` | 클러스터 NotebookLM 재동기화 |
| `health_check` | 헬스체크 |

## Queue 분리

| Queue | 용도 | 태스크 |
|-------|------|--------|
| `vdg` | VDG 분석 | analyze_*, stuck_recovery |
| `crawler` | 크롤링 | crawl_*, auto_promote |
| `default` | 기타 | notebooklm, health_check |

## Celery Beat 스케줄 요약

```
:00분 - 매시 정각
:15분 - TikTok/YouTube 크롤
:30분 - auto_promote
:45분 - enrich_scores
매 5분 - health_check
매 15분 - stuck_recovery
```

**다음: Celery Beat 상세 스케줄?** /c 🐱
