# Trending Sound + VDG 파이프라인 연구

*작성: 소미 🐱 | 2026-02-06*

---

## 1. 현재 상태

### SocialKit Adapter
```python
# SocialKitSearchVideo - 현재 필드
@dataclass
class SocialKitSearchVideo:
    id: str
    url: str
    desc: str
    views: int
    likes: int
    shares: int
    comments: int
    author_username: str
    cover_url: str
    # ❌ music/sound 정보 없음!
```

### VDG 스키마 (vdg_v4.py)
```python
# 이미 있는 audio 관련 필드
audio_context: str  # speech, music, mixed, silence, ambient
audio_stimulation: float  # 도파민 레이더 0-10
audio_style: str  # voiceover, direct_address
GeminiAudioAnalysis  # Gemini 음성 분석
```

---

## 2. TikTok API Music 데이터 구조

일반적으로 TikTok API는 다음을 반환 (SocialKit 확인 필요):

```json
{
  "music": {
    "id": "6848574019963972353",
    "title": "original sound",
    "authorName": "@creator",
    "playUrl": "https://...",
    "coverLarge": "https://...",
    "duration": 15
  }
}
```

---

## 3. 구현 제안

### Phase 1: SocialKit에서 Music 수집

**A. SocialKitSearchVideo 확장**
```python
@dataclass
class SocialKitSearchVideo:
    # 기존 필드...
    
    # 추가
    music_id: str = ""
    music_title: str = ""
    music_author: str = ""
```

**B. from_api_response 수정**
```python
# socialkit_adapter.py
music = v.get("music", {})
videos.append(
    SocialKitSearchVideo(
        # 기존...
        music_id=str(music.get("id", "")),
        music_title=music.get("title", ""),
        music_author=music.get("authorName", ""),
    )
)
```

**C. raw_payload에 저장**
```python
# tiktok_tasks.py
raw_payload = {
    "source": "socialkit_search",
    "music_id": item.get("music_id"),
    "music_title": item.get("music_title"),
    "hashtags": item.get("hashtags", []),
}
```

### Phase 2: Trending Sound 랭킹

**A. 새 Celery Task**
```python
@celery_app.task
def analyze_trending_sounds(hours: int = 24):
    """최근 크롤된 영상에서 인기 사운드 분석"""
    
    # 1. raw_payload에서 music_id 추출
    items = get_recent_outliers(hours=hours)
    
    # 2. music_id별 집계
    sound_stats = {}
    for item in items:
        music_id = item.raw_payload.get("music_id")
        if music_id:
            if music_id not in sound_stats:
                sound_stats[music_id] = {
                    "title": item.raw_payload.get("music_title"),
                    "count": 0,
                    "total_views": 0,
                    "avg_engagement": 0,
                }
            sound_stats[music_id]["count"] += 1
            sound_stats[music_id]["total_views"] += item.view_count
    
    # 3. 랭킹 정렬
    trending = sorted(
        sound_stats.items(),
        key=lambda x: (x[1]["count"], x[1]["total_views"]),
        reverse=True
    )[:20]
    
    return {"trending_sounds": trending}
```

**B. Beat Schedule**
```python
"analyze-trending-sounds": {
    "task": "...",
    "schedule": crontab(hour="2,8,14,20"),  # 6시간마다
}
```

### Phase 3: VDG 연동

**A. VDG 분석 시 music 정보 활용**
```python
# vdg_feature_extractor.py 또는 새 함수
def enrich_vdg_with_sound_trend(vdg_result, music_id):
    """VDG 결과에 사운드 트렌드 정보 추가"""
    
    sound_trend = get_sound_trend_info(music_id)
    
    if sound_trend:
        vdg_result["sound_trend"] = {
            "is_trending": sound_trend["rank"] <= 20,
            "rank": sound_trend["rank"],
            "usage_count": sound_trend["count"],
            "viral_potential": "high" if sound_trend["rank"] <= 5 else "medium",
        }
    
    return vdg_result
```

**B. 스카웃 알림에 표시**
```python
# notification_service.py
if sound_trend and sound_trend["is_trending"]:
    message += f"🎵 *트렌딩 사운드:* #{sound_trend['rank']} ({sound_trend['title'][:20]})\n"
```

---

## 4. 데이터 흐름

```
SocialKit API
    ↓ (music_id, music_title 수집)
CrawledVideoData
    ↓ (raw_payload에 저장)
OutlierItem (DB)
    ↓
analyze_trending_sounds (집계)
    ↓
TrendingSound 랭킹
    ↓
VDG 분석 시 연동 + 스카웃 알림
```

---

## 5. 확인 필요 사항

### SocialKit API 응답에 music 포함되는지?

```bash
# 테스트 방법 (Railway 환경에서)
curl "https://api.socialkit.io/v1/tiktok/search?query=kbeauty&limit=1" \
  -H "Authorization: Bearer $SOCIALKIT_ACCESS_KEY" | jq '.data.results[0].music'
```

만약 music 없으면:
1. SocialKit 다른 엔드포인트 확인
2. 또는 video detail API로 개별 조회
3. 또는 다른 API 대안 (TikTok-Api 등)

---

## 6. 우선순위

| 단계 | 작업 | 의존성 |
|------|------|--------|
| 0 | SocialKit music 응답 확인 | - |
| 1 | SocialKitSearchVideo에 music 필드 추가 | 단계 0 |
| 2 | raw_payload에 music 저장 | 단계 1 |
| 3 | Trending Sound 랭킹 Task | 단계 2 |
| 4 | VDG 연동 | 단계 3 |
| 5 | 스카웃 알림 표시 | 단계 4 |

---

## References

- VDG v4 스키마: `app/schemas/vdg_v4.py`
- SocialKit Adapter: `app/services/socialkit_adapter.py`
- TikTok API music 구조: 일반적 패턴 참고
