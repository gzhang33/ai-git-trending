from .database import ProjectDatabase
from datetime import date, timedelta

def analyze_trends(days=7):
    """
    Analyzes trending data using the new star schema.
    """
    db = ProjectDatabase()
    conn = db._get_connection()
    cursor = conn.cursor()

    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # --- Most Frequent Projects ---
    cursor.execute("""
        SELECT p.name, COUNT(f.snapshot_id) as count
        FROM fact_trending_snapshots f
        JOIN dim_projects p ON f.project_id = p.project_id
        JOIN dim_dates d ON f.date_id = d.date_id
        WHERE d.full_date BETWEEN ? AND ?
        GROUP BY p.name
        ORDER BY count DESC
        LIMIT 10
    """, (start_date.isoformat(), end_date.isoformat()))
    most_frequent_projects = cursor.fetchall()

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
                MIN(d.full_date) as first_day,
                MAX(d.full_date) as last_day,
                SUM(CASE WHEN d.full_date = (SELECT MIN(d2.full_date) FROM dim_dates d2 JOIN fact_trending_snapshots f2 ON d2.date_id = f2.date_id WHERE f2.project_id = f.project_id AND d2.full_date BETWEEN ? AND ?) THEN f.stars END) as start_stars,
                SUM(CASE WHEN d.full_date = (SELECT MAX(d2.full_date) FROM dim_dates d2 JOIN fact_trending_snapshots f2 ON d2.date_id = f2.date_id WHERE f2.project_id = f.project_id AND d2.full_date BETWEEN ? AND ?) THEN f.stars END) as end_stars
            FROM fact_trending_snapshots f
            JOIN dim_projects p ON f.project_id = p.project_id
            JOIN dim_dates d ON f.date_id = d.date_id
            WHERE d.full_date BETWEEN ? AND ?
            GROUP BY f.project_id, p.name
            HAVING COUNT(f.snapshot_id) > 1
        )
        SELECT 
            name,
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
        {"name": row[0], "star_increase": row[1], "start_stars": row[2], "end_stars": row[3]}
        for row in surging_projects_raw
    ]

    conn.close()

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
    return data
