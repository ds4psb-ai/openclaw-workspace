#!/usr/bin/env python3
"""
SocialKit 크롤러 결과 모니터링 스크립트
소미 🐱 2026-02-05

Usage:
    # Railway 환경에서 실행
    cd /Users/ted/komission/backend && source venv/bin/activate
    railway run -- python3 /path/to/check_outliers.py
"""

import os
from datetime import datetime, timezone, timedelta

def main():
    from sqlalchemy import create_engine, text
    
    DATABASE_URL = os.getenv("DATABASE_URL", "").replace("+asyncpg", "")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not set")
        return
    
    engine = create_engine(DATABASE_URL)
    KST = timezone(timedelta(hours=9))
    
    with engine.connect() as conn:
        print("=" * 60)
        print(f"📊 Komission Outlier 현황 ({datetime.now(KST).strftime('%Y-%m-%d %H:%M KST')})")
        print("=" * 60)
        
        # 1. Source별 통계
        print("\n📁 Source별 통계:")
        stats = conn.execute(text("""
            SELECT os.name, COUNT(oi.id), 
                   COALESCE(AVG(oi.view_count), 0)::bigint,
                   MAX(oi.crawled_at)
            FROM outlier_sources os
            LEFT JOIN outlier_items oi ON oi.source_id = os.id
            GROUP BY os.name
            ORDER BY COUNT(oi.id) DESC
        """)).fetchall()
        
        for s in stats:
            name, count, avg_views, last_crawl = s
            avg_str = f"{avg_views/1_000_000:.1f}M" if avg_views >= 1_000_000 else f"{avg_views:,}"
            last_str = str(last_crawl)[:16] if last_crawl else "Never"
            print(f"  {name}: {count}개 | 평균 {avg_str} 뷰 | 최근: {last_str}")
        
        # 2. TikTok SocialKit 상세
        print("\n🎯 TikTok SocialKit 최근 20개:")
        items = conn.execute(text("""
            SELECT oi.title, oi.view_count, oi.outlier_tier, 
                   oi.creator_username, oi.thumbnail_url, oi.crawled_at
            FROM outlier_items oi 
            JOIN outlier_sources os ON oi.source_id = os.id 
            WHERE os.name = 'tiktok_socialkit'
            ORDER BY oi.crawled_at DESC NULLS LAST
            LIMIT 20
        """)).fetchall()
        
        if not items:
            print("  (데이터 없음 - 크롤링 대기 중)")
        else:
            for i, item in enumerate(items, 1):
                title, views, tier, username, thumb, crawled = item
                title_short = (title or '')[:30]
                views_str = f"{views/1_000_000:.1f}M" if views and views >= 1_000_000 else f"{views:,}" if views else "0"
                thumb_status = "✅" if thumb else "❌"
                print(f"  {i:2}. [{tier or '?'}] {views_str:>8} | @{username or 'unknown':<15} | {thumb_status} | {title_short}")
        
        # 3. 티어별 통계
        print("\n📈 티어별 통계:")
        tier_stats = conn.execute(text("""
            SELECT oi.outlier_tier, COUNT(*), AVG(oi.view_count)::bigint
            FROM outlier_items oi 
            JOIN outlier_sources os ON oi.source_id = os.id 
            WHERE os.name = 'tiktok_socialkit'
            GROUP BY oi.outlier_tier
            ORDER BY oi.outlier_tier
        """)).fetchall()
        
        if not tier_stats:
            print("  (데이터 없음)")
        else:
            for t in tier_stats:
                tier, count, avg = t
                avg_str = f"{avg/1_000_000:.1f}M" if avg and avg >= 1_000_000 else f"{avg:,}" if avg else "0"
                print(f"  {tier or '?'}: {count}개 (평균 {avg_str} 뷰)")
        
        # 4. 썸네일 상태
        print("\n🖼️ 썸네일 상태:")
        thumb_stats = conn.execute(text("""
            SELECT 
                COUNT(*) FILTER (WHERE oi.thumbnail_url IS NOT NULL AND oi.thumbnail_url != '') as with_thumb,
                COUNT(*) FILTER (WHERE oi.thumbnail_url IS NULL OR oi.thumbnail_url = '') as without_thumb
            FROM outlier_items oi 
            JOIN outlier_sources os ON oi.source_id = os.id 
            WHERE os.name = 'tiktok_socialkit'
        """)).fetchone()
        
        if thumb_stats:
            with_t, without_t = thumb_stats
            total = with_t + without_t
            if total > 0:
                pct = (with_t / total) * 100
                print(f"  썸네일 있음: {with_t}개 ({pct:.0f}%)")
                print(f"  썸네일 없음: {without_t}개")
            else:
                print("  (데이터 없음)")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
