#!/usr/bin/env python3
"""
T003 - Komission 아웃라이어 수집 스크립트
소미 🐱
"""

import os
import json
import requests
from datetime import datetime, timezone

API_KEY = os.getenv("OPENCLAW_API_KEY", "9101273f44ba1aceff8d593b2d183ab08ca272721b48bd58921def75f999b39e")
BASE_URL = "https://api.shorti.ai"

def fetch_outliers(limit=10):
    """아웃라이어 영상 목록 조회"""
    headers = {"X-API-Key": API_KEY}
    resp = requests.get(f"{BASE_URL}/api/v1/outliers?limit={limit}", headers=headers)
    resp.raise_for_status()
    return resp.json()

def fetch_patterns_stats():
    """패턴 통계 조회"""
    headers = {"X-API-Key": API_KEY}
    resp = requests.get(f"{BASE_URL}/api/v1/patterns/stats", headers=headers)
    resp.raise_for_status()
    return resp.json()

def fetch_for_you(limit=10):
    """추천 피드 조회"""
    headers = {"X-API-Key": API_KEY}
    resp = requests.get(f"{BASE_URL}/api/v1/for-you?limit={limit}", headers=headers)
    resp.raise_for_status()
    return resp.json()

def generate_report(outliers):
    """리포트 생성"""
    report = f"""# 🔥 Komission 아웃라이어 리포트
**생성:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

## 📊 요약
- 총 아웃라이어: {outliers.get('total', 0)}개

## 🏆 Top 아웃라이어
"""
    for item in outliers.get('items', []):
        report += f"""
### {item.get('outlier_tier', 'N/A')} - @{item.get('creator_username', 'unknown')}
- **조회수:** {item.get('view_count', 0):,}
- **좋아요:** {item.get('like_count', 0):,}
- **점수:** {item.get('outlier_score', 0):.2f}
- **URL:** {item.get('video_url', '')}
"""
    return report

def main():
    print("🐱 Komission 아웃라이어 수집 시작...")
    
    # 아웃라이어 조회
    outliers = fetch_outliers(limit=10)
    print(f"✅ 아웃라이어 {outliers.get('total', 0)}개 발견")
    
    # 리포트 생성
    report = generate_report(outliers)
    
    # 저장
    workspace = os.environ.get("OPENCLAW_WORKSPACE", "/Users/ted/.openclaw/workspace")
    report_path = f"{workspace}/artifacts/reports/outliers_latest.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"📄 리포트 저장: {report_path}")
    print(report)
    
    return outliers

if __name__ == "__main__":
    main()
