#!/usr/bin/env python3
"""
Komission 숏폼 큐레이팅 자동화 - Phase 1
담당: @somi
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# 설정
API_URL = os.getenv("KOMISSION_API_URL", "https://api.shorti.ai")
API_KEY = os.getenv("OPENCLAW_API_KEY", "")
CURATION_DIR = Path("artifacts/curation")
SEEN_FILE = CURATION_DIR / "seen_videos.json"


def get_headers():
    """API 헤더 생성"""
    if not API_KEY:
        raise ValueError("OPENCLAW_API_KEY 환경변수가 설정되지 않았습니다.")
    return {"X-API-Key": API_KEY}


def fetch_outliers(tier: str = "SS,S", limit: int = 10) -> list:
    """
    SS/S 티어 아웃라이어 가져오기
    
    Args:
        tier: 티어 필터 (SS, S, A, B, C)
        limit: 결과 수 제한
    
    Returns:
        아웃라이어 리스트
    """
    resp = requests.get(
        f"{API_URL}/api/v1/outliers",
        headers=get_headers(),
        params={"tier": tier, "limit": limit}
    )
    resp.raise_for_status()
    return resp.json()


def fetch_for_you(limit: int = 10) -> list:
    """
    개인화 추천 피드 가져오기
    
    Returns:
        추천 리스트
    """
    resp = requests.get(
        f"{API_URL}/api/v1/for-you",
        headers=get_headers(),
        params={"limit": limit}
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("recommendations", [])


def filter_high_engagement(outliers: list, min_rate: float = 0.1) -> list:
    """
    engagement_rate 기준 필터링
    
    Args:
        outliers: 아웃라이어 리스트
        min_rate: 최소 engagement_rate
    
    Returns:
        필터링된 리스트
    """
    return [o for o in outliers if o.get("engagement_rate", 0) > min_rate]


def load_seen_videos() -> set:
    """이미 본 영상 ID 로드"""
    if SEEN_FILE.exists():
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen_videos(seen: set):
    """본 영상 ID 저장"""
    CURATION_DIR.mkdir(parents=True, exist_ok=True)
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def deduplicate(videos: list, seen: set) -> list:
    """
    중복 제거 (이미 본 영상 필터링)
    
    Args:
        videos: 영상 리스트
        seen: 이미 본 영상 ID set
    
    Returns:
        새로운 영상만
    """
    return [v for v in videos if v.get("id") not in seen]


def save_curation(videos: list, prefix: str = "curation") -> str:
    """
    큐레이션 결과 저장
    
    Args:
        videos: 영상 리스트
        prefix: 파일명 prefix
    
    Returns:
        저장된 파일 경로
    """
    CURATION_DIR.mkdir(parents=True, exist_ok=True)
    filename = CURATION_DIR / f"{datetime.now().strftime('%Y-%m-%d_%H%M')}_{prefix}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    
    return str(filename)


def format_summary(videos: list) -> str:
    """
    큐레이션 요약 포맷
    
    Args:
        videos: 영상 리스트
    
    Returns:
        요약 텍스트
    """
    if not videos:
        return "새로운 고퀄 영상 없음"
    
    lines = [f"🎬 새로운 고퀄 영상 {len(videos)}개 발견!\n"]
    
    for i, v in enumerate(videos[:5], 1):  # 상위 5개만
        tier = v.get("outlier_tier", "?")
        score = v.get("outlier_score", 0)
        views = v.get("view_count", 0)
        creator = v.get("creator_username", "unknown")
        url = v.get("video_url", "")
        
        lines.append(
            f"{i}. [{tier}] {creator}\n"
            f"   조회수: {views:,} | Score: {score:.0f}\n"
            f"   {url}\n"
        )
    
    if len(videos) > 5:
        lines.append(f"\n... 외 {len(videos) - 5}개")
    
    return "\n".join(lines)


def run_curation(
    method: str = "outliers",
    tier: str = "SS,S",
    limit: int = 10,
    min_engagement: float = 0.1
) -> dict:
    """
    메인 큐레이션 실행
    
    Args:
        method: "outliers" | "for-you"
        tier: 티어 필터 (outliers 방식)
        limit: 결과 수 제한
        min_engagement: 최소 engagement_rate
    
    Returns:
        {
            "new_videos": list,
            "file": str,
            "summary": str
        }
    """
    # 1. 영상 가져오기
    if method == "outliers":
        videos = fetch_outliers(tier=tier, limit=limit)
    elif method == "for-you":
        videos = fetch_for_you(limit=limit)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # 2. 필터링
    videos = filter_high_engagement(videos, min_engagement)
    
    # 3. 중복 제거
    seen = load_seen_videos()
    new_videos = deduplicate(videos, seen)
    
    # 4. 저장
    if new_videos:
        file = save_curation(new_videos, prefix=method)
        
        # seen 업데이트
        for v in new_videos:
            seen.add(v.get("id"))
        save_seen_videos(seen)
    else:
        file = None
    
    # 5. 요약
    summary = format_summary(new_videos)
    
    return {
        "new_videos": new_videos,
        "file": file,
        "summary": summary
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Komission 숏폼 큐레이터")
    parser.add_argument("--method", default="outliers", choices=["outliers", "for-you"])
    parser.add_argument("--tier", default="SS,S")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--min-engagement", type=float, default=0.1)
    parser.add_argument("--dry-run", action="store_true", help="API 키 없이 테스트")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("🔍 Dry run mode (API 키 없음)")
        print(f"  Method: {args.method}")
        print(f"  Tier: {args.tier}")
        print(f"  Limit: {args.limit}")
        print(f"  Min Engagement: {args.min_engagement}")
        print("\n✅ 코드 구조 확인 완료. API 키 설정 후 실행하세요.")
    else:
        try:
            result = run_curation(
                method=args.method,
                tier=args.tier,
                limit=args.limit,
                min_engagement=args.min_engagement
            )
            print(result["summary"])
            if result["file"]:
                print(f"\n📁 저장됨: {result['file']}")
        except ValueError as e:
            print(f"❌ Error: {e}")
        except requests.exceptions.HTTPError as e:
            print(f"❌ API Error: {e}")
