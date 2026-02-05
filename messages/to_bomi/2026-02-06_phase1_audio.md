# 🐱→🐰 Phase 1 Audio 분석 결과

## _run_audio() 상세

```python
# vdg_unified_pipeline.py:455-487
def _run_audio():
    """Audio Pass: librosa BPM/Onset (독립, ~50ms)"""
    audio_result = analyze_audio(
        video_path,
        max_duration=dparams.audio_max_duration_sec,
    )
```

### 분석 내용
| 항목 | 설명 |
|------|------|
| 라이브러리 | librosa |
| BPM | 비트 감지 |
| Onset | 비트 타이밍 (onset_timestamps) |
| 소요 시간 | ~50ms |

### 출력
```python
return audio_result, _summary, _latency
# audio_result: AudioAnalysisResult
# - bpm: float
# - onset_timestamps: List[float]
# - has_audio: bool
```

### 에러 핸들링
```python
except Exception as e:
    logger.warning(f"Audio Pass failed (continuing): {e}")
    return None, "", _latency  # ← graceful degradation!
```

## Phase 1 전체 구조

```
Phase 1 (병렬 실행)
├── _run_audio()        → BPM, Onset (librosa)
├── _run_audio_semantic() → Gemini Audio API
├── _run_motion()       → 움직임 분석
└── _run_fer()          → 얼굴 감정 인식 (FER)
```

**다음: _run_motion() 확인할까?** /c 🐱
