#!/usr/bin/env python3
"""
T003 - Komission 숏폼 큐레이터
소미 🐱

아웃라이어 영상을 분석하고 인사이트를 추출하여
크리에이터에게 유용한 트렌드 리포트 생성
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

API_KEY = os.getenv("OPENCLAW_API_KEY", "9101273f44ba1aceff8d593b2d183ab08ca272721b48bd58921def75f999b39e")
BASE_URL = "https://api.shorti.ai"
WORKSPACE = Path("/root/.openclaw/workspace")

class KomissionCurator:
    def __init__(self):
        self.headers = {"X-API-Key": API_KEY}
    
    def fetch_outliers(self, limit=20):
        """아웃라이어 수집"""
        resp = requests.get(
            f"{BASE_URL}/api/v1/outliers?limit={limit}",
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()
    
    def fetch_for_you(self, limit=20):
        """추천 피드 수집"""
        resp = requests.get(
            f"{BASE_URL}/api/v1/for-you?limit={limit}",
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()
    
    def analyze_trends(self, outliers):
        """트렌드 분석"""
        trends = {
            "tier_distribution": {},
            "top_categories": {},
            "avg_engagement": 0,
            "top_creators": [],
            "insights": []
        }
        
        items = outliers.get('items', [])
        if not items:
            return trends
        
        total_engagement = 0
        for item in items:
            # 티어 분포
            tier = item.get('outlier_tier', 'unknown')
            trends["tier_distribution"][tier] = trends["tier_distribution"].get(tier, 0) + 1
            
            # 카테고리
            cat = item.get('category', 'unknown')
            trends["top_categories"][cat] = trends["top_categories"].get(cat, 0) + 1
            
            # 참여율
            total_engagement += item.get('engagement_rate', 0)
            
            # 탑 크리에이터
            creator = item.get('creator_username')
            if creator:
                trends["top_creators"].append({
                    "username": creator,
                    "views": item.get('view_count', 0),
                    "score": item.get('outlier_score', 0)
                })
        
        trends["avg_engagement"] = total_engagement / len(items) if items else 0
        trends["top_creators"] = sorted(
            trends["top_creators"], 
            key=lambda x: x['score'], 
            reverse=True
        )[:5]
        
        # 인사이트 생성
        if trends["tier_distribution"].get('SS', 0) > 0:
            trends["insights"].append("🔥 SS티어 바이럴 영상 발견! 즉시 분석 권장")
        
        if trends["avg_engagement"] > 0.1:
            trends["insights"].append("📈 평균 참여율 10% 이상 - 활성 트렌드")
        
        return trends
    
    def generate_daily_report(self):
        """일간 큐레이션 리포트 생성"""
        now = datetime.now(timezone.utc)
        date_str = now.strftime('%Y-%m-%d')
        
        # 데이터 수집
        outliers = self.fetch_outliers(limit=20)
        trends = self.analyze_trends(outliers)
        
        # 리포트 생성
        report = f"""# 📊 Komission 일간 큐레이션 리포트
**날짜:** {date_str}  
**생성:** {now.strftime('%H:%M UTC')}  
**생성자:** 소미 🐱

---

## 🎯 요약
- **총 아웃라이어:** {outliers.get('total', 0)}개
- **평균 참여율:** {trends['avg_engagement']*100:.2f}%

## 🏆 티어 분포
"""
        for tier, count in sorted(trends['tier_distribution'].items()):
            report += f"- **{tier}:** {count}개\n"
        
        report += "\n## 🌟 Top 크리에이터\n"
        for i, creator in enumerate(trends['top_creators'], 1):
            report += f"{i}. **@{creator['username']}** - 조회수 {creator['views']:,} / 점수 {creator['score']:.2f}\n"
        
        report += "\n## 💡 인사이트\n"
        for insight in trends['insights']:
            report += f"- {insight}\n"
        
        if not trends['insights']:
            report += "- 특별한 인사이트 없음\n"
        
        report += f"""
## 📈 상세 아웃라이어

| 크리에이터 | 티어 | 조회수 | 좋아요 | 점수 |
|-----------|------|--------|--------|------|
"""
        for item in outliers.get('items', [])[:10]:
            report += f"| @{item.get('creator_username', 'unknown')} | {item.get('outlier_tier', '-')} | {item.get('view_count', 0):,} | {item.get('like_count', 0):,} | {item.get('outlier_score', 0):.2f} |\n"
        
        report += f"""
---

## 🔗 액션 아이템
1. SS/S 티어 영상 VDG 분석 실행
2. 트렌드 패턴 저장
3. 크리에이터 인사이트 도출

---
*자동 생성 by 소미 🐱 - Komission Curator*
"""
        
        # 저장
        report_dir = WORKSPACE / "artifacts" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_path = report_dir / f"curation_{date_str}.md"
        report_path.write_text(report)
        
        # 최신 리포트 링크
        latest_path = report_dir / "curation_latest.md"
        latest_path.write_text(report)
        
        return report, str(report_path)

def main():
    print("🐱 Komission 큐레이터 시작...")
    
    curator = KomissionCurator()
    
    try:
        report, path = curator.generate_daily_report()
        print(f"✅ 리포트 생성 완료: {path}")
        print("\n" + "="*50 + "\n")
        print(report)
    except Exception as e:
        print(f"❌ 에러: {e}")
        raise

if __name__ == "__main__":
    main()
