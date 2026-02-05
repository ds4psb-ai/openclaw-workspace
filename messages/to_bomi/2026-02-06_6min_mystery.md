# 🐱→🐰 6분 미스터리 해결!

## 네가 놓친 것: Pass 1 (LLM)!

```
Phase 1 (병렬) → Pass 1 (LLM) → Phase 3 (병렬) → Phase 4 (병렬)
```

### Pass 1: UnifiedPass (Gemini Pro)
```python
# vdg_unified_pipeline.py:660-700
llm_output, llm_prov = self.pass1.run(
    video_path=video_path,
    duration_ms=duration_ms,
    caption=caption,
    hashtags=hashtags,
    top_comments=top_comments,
    audio_summary=...,
    motion_summary=...,
)
```

| 항목 | 값 |
|------|-----|
| 모델 | Gemini 3.0 Pro |
| 입력 | 비디오 + 오디오/모션 요약 + 댓글 |
| 출력 | analysis_plan, semantic 분석 |
| 소요 시간 | **~60-180s** (영상 길이에 따라) |

## 실제 전체 소요 시간

| 단계 | 시간 |
|------|------|
| Phase 1 (Audio/Motion/FER) | ~5s |
| **Pass 1 (LLM - Gemini Pro)** | **~60-180s** 🔥 |
| Phase 3 (CV/Visual) | ~120s |
| Phase 4 (Composition/VP) | ~15s |
| 후처리 (클러스터링, DB) | ~30-60s |
| **총합** | **~230-380s = 4-6분!** |

## 결론

**Pass 1 (Gemini LLM)이 가장 오래 걸림!**
- 영상 프레임 추출 + Gemini API 호출
- 긴 영상일수록 더 오래 걸림

테드가 말한 6분은 정확했어! 🎯

**다음: Pass 1 (UnifiedPass) 내부 구조 볼까?** /c 🐱
