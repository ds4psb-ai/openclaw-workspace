# Veo / Kling 공용 샷 JSON 스키마

**용도:** shorti.ai 백엔드 + 커리큘럼 데모

---

## 🎯 단일 POST /generate 인터페이스

```json
{
  "engine": "veo" | "kling",
  "mode": "scene" | "shot",
  "payload": { ... }
}
```

---

## 📐 공용 샷 스키마

```json
{
  "shot_id": "shot_001",
  "timecode": {
    "start": "00:00:00",
    "end": "00:00:05",
    "duration_sec": 5
  },
  "shot_goal": "훅 - 시청자 주목 끌기",
  
  "visual": {
    "description": "어두운 방에서 화면이 갑자기 밝아지며 주인공 얼굴 클로즈업",
    "style_reference": "wes_anderson",
    "color_palette": ["#F5E6D3", "#E8B4B8", "#A8D8EA"],
    "contrast": "high",
    "aspect_ratio": "9:16"
  },
  
  "camera": {
    "shot_type": "close_up",
    "movement": "push_in",
    "speed": "slow",
    "angle": "eye_level"
  },
  
  "subject": {
    "type": "person",
    "description": "30대 남성, 놀란 표정",
    "action": "눈을 크게 뜨며 카메라를 바라봄",
    "reference_images": ["ref_001.jpg", "ref_002.jpg"]
  },
  
  "audio": {
    "type": "sfx_music",
    "music_mood": "tension_buildup",
    "sfx": "dramatic_whoosh",
    "voice": null
  },
  
  "text_overlay": {
    "enabled": false,
    "content": null,
    "position": null
  }
}
```

---

## 🎬 Veo 3.1 전용 파라미터

```json
{
  "engine": "veo",
  "mode": "scene",
  "payload": {
    "model": "veo-3.1",
    "resolution": "4k",
    "fps": 60,
    "aspect_ratio": "9:16",
    
    "ingredients_to_video": {
      "enabled": true,
      "reference_images": [
        "character_front.jpg",
        "character_side.jpg",
        "style_reference.jpg",
        "mood_board.jpg"
      ]
    },
    
    "audio": {
      "generate": true,
      "type": "full",
      "dialogue": "오늘 제가 보여드릴 것은...",
      "sfx": "ambient_office",
      "music_mood": "inspiring"
    },
    
    "shots": [
      { /* 공용 샷 스키마 */ }
    ]
  }
}
```

### Veo 강점 활용 포인트
- `ingredients_to_video`: 레퍼런스 이미지 4장으로 캐릭터 일관성
- `resolution: "4k"` + `fps: 60`: 고퀄리티 시네마틱
- `aspect_ratio: "9:16"`: 네이티브 세로 영상

---

## 🎥 Kling 2.6 전용 파라미터

```json
{
  "engine": "kling",
  "mode": "shot",
  "payload": {
    "model": "kling-2.6-pro",
    "resolution": "1080p",
    "duration_sec": 5,
    "generation_mode": "turbo",
    
    "input_type": "text_to_video",
    
    "audio": {
      "generate": true,
      "lip_sync": true,
      "dialogue": "안녕하세요!",
      "voice_style": "energetic_male",
      "music_beat": 120
    },
    
    "camera_motion": {
      "type": "fpv",
      "speed": "fast",
      "path": "forward_dive"
    },
    
    "shot": { /* 공용 샷 스키마 */ }
  }
}
```

### Kling 강점 활용 포인트
- `lip_sync: true`: 자동 립싱크
- `camera_motion.type: "fpv"`: FPV 드론 샷
- `generation_mode: "turbo"`: 빠른 생성 (대량 생산)

---

## 📋 파이프라인 분기 로직

```
if (content_type === "cinematic" || need_character_consistency) {
  → Veo 3.1 파이프라인
  → Scene-level planner
  → ingredients_to_video 활성화
}

if (content_type === "shorts" || need_audio_sync || need_fpv) {
  → Kling 2.6 파이프라인
  → Shot-level punch
  → lip_sync / camera_motion 활성화
}
```

---

## 🔄 shorti.ai API 엔드포인트

### POST /generate
```json
// Request
{
  "engine": "veo",
  "mode": "scene",
  "payload": { ... }
}

// Response
{
  "job_id": "job_abc123",
  "status": "processing",
  "estimated_time_sec": 120,
  "preview_url": null
}
```

### GET /status/{job_id}
```json
{
  "job_id": "job_abc123",
  "status": "completed",
  "result": {
    "video_url": "https://...",
    "duration_sec": 15,
    "resolution": "4k"
  }
}
```

---

## 🎓 커리큘럼 데모용 예시

### "거장 DNA 스타일 쇼츠" 생성

**입력:**
```json
{
  "engine": "veo",
  "mode": "scene",
  "payload": {
    "model": "veo-3.1",
    "resolution": "1080p",
    "aspect_ratio": "9:16",
    "ingredients_to_video": {
      "enabled": true,
      "reference_images": [
        "wes_anderson_palette.jpg",
        "symmetric_composition.jpg"
      ]
    },
    "shots": [
      {
        "shot_id": "hook",
        "duration_sec": 3,
        "shot_goal": "대칭 구도로 시선 고정",
        "camera": {
          "shot_type": "wide",
          "movement": "static"
        },
        "visual": {
          "style_reference": "wes_anderson",
          "description": "파스텔톤 방, 정중앙에 인물"
        }
      }
    ]
  }
}
```

---

**작성:** 보미 🐰  
**용도:** shorti.ai 백엔드 + 커리큘럼 JSON 1:1 대응
