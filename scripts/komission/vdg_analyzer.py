#!/usr/bin/env python3
"""
T003 - Komission VDG 분석 스크립트
소미 🐱

VDG = Viral Depth Genealogy
- 영상 URL → AI 분석 → 패턴 추출
"""

import os
import json
import requests
import time
from datetime import datetime, timezone

API_KEY = os.getenv("OPENCLAW_API_KEY", "ock_live_9REMohW7Bp4Ryqih36Hloj5zvQnHuJjckpHwze9XDks")
BASE_URL = "https://api.shorti.ai"

def submit_vdg_analysis(video_url: str):
    """VDG 분석 요청 (비동기)"""
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"video_url": video_url}
    resp = requests.post(f"{BASE_URL}/api/v1/vdg/async/analyze", headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()

def get_analysis_status(task_id: str):
    """분석 상태 조회"""
    headers = {"X-API-Key": API_KEY}
    resp = requests.get(f"{BASE_URL}/api/v1/vdg/async/status/{task_id}", headers=headers)
    resp.raise_for_status()
    return resp.json()

def search_patterns(query: str, limit: int = 10):
    """패턴 검색"""
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"query": query, "limit": limit}
    resp = requests.post(f"{BASE_URL}/api/v1/search/unified", headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()

def get_pattern_stats():
    """패턴 통계"""
    headers = {"X-API-Key": API_KEY}
    resp = requests.get(f"{BASE_URL}/api/v1/patterns/stats", headers=headers)
    resp.raise_for_status()
    return resp.json()

def analyze_outlier_patterns(outliers: list):
    """아웃라이어 영상들의 공통 패턴 분석"""
    patterns = []
    for outlier in outliers:
        if outlier.get('vdg_analysis'):
            patterns.append(outlier['vdg_analysis'])
    
    # 패턴 요약
    summary = {
        "total_analyzed": len(patterns),
        "common_elements": [],
        "trending_hooks": [],
        "engagement_insights": []
    }
    
    return summary

def generate_vdg_report(analysis_results: list):
    """VDG 분석 리포트 생성"""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    report = f"""# 🧬 VDG 분석 리포트
**생성:** {now}

## 📊 분석 요약
- 분석 완료: {len(analysis_results)}개 영상

## 🔍 패턴 인사이트
"""
    for result in analysis_results:
        report += f"""
### {result.get('title', 'Untitled')}
- **상태:** {result.get('status', 'unknown')}
- **URL:** {result.get('video_url', '')}
"""
    return report

def main():
    print("🧬 VDG 분석기 시작...")
    
    # 패턴 통계 조회
    try:
        stats = get_pattern_stats()
        print(f"📊 패턴 DB 통계: {json.dumps(stats, indent=2)}")
    except Exception as e:
        print(f"⚠️ 패턴 통계 조회 실패: {e}")
    
    # 패턴 검색 테스트
    try:
        results = search_patterns("hook", limit=5)
        print(f"🔍 'hook' 검색 결과: {json.dumps(results, indent=2)[:500]}...")
    except Exception as e:
        print(f"⚠️ 패턴 검색 실패: {e}")
    
    print("✅ VDG 분석기 준비 완료!")

if __name__ == "__main__":
    main()
