from .database import ProjectDatabase
from datetime import date, timedelta
from config.logging_config import get_logger

# 创建日志记录器
logger = get_logger('analyzer', 'INFO')

def analyze_trends(days=7):
    """
    Analyzes trending data using the new star schema.
    """
    logger.info(f"开始分析最近{days}天的趋势数据")
    db = ProjectDatabase()
    conn = db._get_connection()
    cursor = conn.cursor()

    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # --- Most Frequent Projects ---
    cursor.execute("""
        SELECT p.name, p.url, p.description, l.name as language, COUNT(f.snapshot_id) as count,
               AVG(f.stars) as avg_stars
        FROM fact_trending_snapshots f
        JOIN dim_projects p ON f.project_id = p.project_id
        JOIN dim_dates d ON f.date_id = d.date_id
        LEFT JOIN dim_languages l ON p.language_id = l.language_id
        WHERE d.full_date BETWEEN ? AND ?
        GROUP BY p.name, p.url, p.description, l.name
        ORDER BY count DESC
        LIMIT 10
    """, (start_date.isoformat(), end_date.isoformat()))
    most_frequent_projects_raw = cursor.fetchall()
    most_frequent_projects = [
        {
            "name": row[0],
            "url": row[1], 
            "description": row[2][:100] + "..." if row[2] and len(row[2]) > 100 else row[2],
            "language": row[3] or "Unknown",
            "count": row[4],
            "avg_stars": int(row[5]) if row[5] else 0
        }
        for row in most_frequent_projects_raw
    ]

    # --- Most Frequent Languages ---
    cursor.execute("""
        SELECT l.name, COUNT(f.snapshot_id) as count
        FROM fact_trending_snapshots f
        JOIN dim_projects p ON f.project_id = p.project_id
        JOIN dim_languages l ON p.language_id = l.language_id
        JOIN dim_dates d ON f.date_id = d.date_id
        WHERE d.full_date BETWEEN ? AND ? AND l.name IS NOT NULL
        GROUP BY l.name
        ORDER BY count DESC
        LIMIT 10
    """, (start_date.isoformat(), end_date.isoformat()))
    most_frequent_languages = cursor.fetchall()

    # --- Surging Projects (Star Increase) ---
    cursor.execute("""
        WITH StarHistory AS (
            SELECT 
                f.project_id,
                p.name,
                p.url,
                p.description,
                l.name as language,
                MIN(d.full_date) as first_day,
                MAX(d.full_date) as last_day,
                SUM(CASE WHEN d.full_date = (SELECT MIN(d2.full_date) FROM dim_dates d2 JOIN fact_trending_snapshots f2 ON d2.date_id = f2.date_id WHERE f2.project_id = f.project_id AND d2.full_date BETWEEN ? AND ?) THEN f.stars END) as start_stars,
                SUM(CASE WHEN d.full_date = (SELECT MAX(d2.full_date) FROM dim_dates d2 JOIN fact_trending_snapshots f2 ON d2.date_id = f2.date_id WHERE f2.project_id = f.project_id AND d2.full_date BETWEEN ? AND ?) THEN f.stars END) as end_stars
            FROM fact_trending_snapshots f
            JOIN dim_projects p ON f.project_id = p.project_id
            LEFT JOIN dim_languages l ON p.language_id = l.language_id
            JOIN dim_dates d ON f.date_id = d.date_id
            WHERE d.full_date BETWEEN ? AND ?
            GROUP BY f.project_id, p.name, p.url, p.description, l.name
            HAVING COUNT(f.snapshot_id) > 1
        )
        SELECT 
            name,
            url,
            description,
            language,
            (end_stars - start_stars) as star_increase,
            start_stars,
            end_stars
        FROM StarHistory
        WHERE star_increase > 50 -- Threshold for surging
        ORDER BY star_increase DESC
        LIMIT 10
    """, (start_date.isoformat(), end_date.isoformat(), start_date.isoformat(), end_date.isoformat(), start_date.isoformat(), end_date.isoformat()))
    surging_projects_raw = cursor.fetchall()
    surging_projects = [
        {
            "name": row[0], 
            "url": row[1], 
            "description": row[2][:100] + "..." if row[2] and len(row[2]) > 100 else row[2],
            "language": row[3] or "Unknown",
            "star_increase": row[4], 
            "start_stars": row[5], 
            "end_stars": row[6]
        }
        for row in surging_projects_raw
    ]

    conn.close()
    
    logger.info(f"趋势分析完成，发现{len(most_frequent_projects)}个热门项目，{len(most_frequent_languages)}种热门语言，{len(surging_projects)}个快速增长项目")

    return {
        "time_window_days": days,
        "most_frequent_projects": most_frequent_projects,
        "most_frequent_languages": most_frequent_languages,
        "surging_projects": surging_projects,
    }

def get_trend_by_tag(tag_name, days=30):
    """
    Get the trend for a specific tag.
    """
    logger.info(f"开始分析标签'{tag_name}'最近{days}天的趋势")
    db = ProjectDatabase()
    conn = db._get_connection()
    cursor = conn.cursor()

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    cursor.execute("""
        SELECT d.full_date, COUNT(DISTINCT f.project_id)
        FROM fact_trending_snapshots f
        JOIN dim_dates d ON f.date_id = d.date_id
        JOIN assoc_project_tags apt ON f.project_id = apt.project_id
        JOIN dim_tags t ON apt.tag_id = t.tag_id
        WHERE t.name = ? AND d.full_date BETWEEN ? AND ?
        GROUP BY d.full_date
        ORDER BY d.full_date ASC
    """, (tag_name, start_date.isoformat(), end_date.isoformat()))
    
    data = cursor.fetchall()
    conn.close()
    
    logger.info(f"标签'{tag_name}'的趋势分析完成，共{len(data)}个数据点")
    return data