from flask import Flask, jsonify, render_template
from config.settings import MD_DIR
import os
import markdown as md
from datetime import datetime, timedelta
from app.database import ProjectDatabase

app = Flask(__name__, template_folder='templates', static_folder='images', static_url_path='/images')
db = ProjectDatabase()

def get_report_data_from_filename(filename):
    try:
        date_str = filename.split('_')[-1].replace('.md', '')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return {
            "isoDate": date_str,
            "displayDate": date_obj.strftime('%Y年%m月%d日'),
            "weekday": date_obj.strftime('%A'),
            "path": os.path.join(MD_DIR, filename)
        }
    except (IndexError, ValueError):
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/reports')
def get_reports():
    try:
        files = os.listdir(MD_DIR)
        md_files = sorted([f for f in files if f.endswith('.md')], reverse=True)
        
        reports_meta = []
        for filename in md_files:
            data = get_report_data_from_filename(filename)
            if data:
                with open(data['path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                    project_count = content.count('### ✨')
                data['projectCount'] = project_count if project_count > 0 else 4
                reports_meta.append(data)

        return jsonify(reports_meta)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/report/<date_str>')
def get_report_content(date_str):
    filename = f"github_trending_{date_str}.md"
    filepath = os.path.join(MD_DIR, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "Report not found"}), 404

    try:
        md_content = ""
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        return jsonify({"mdContent": md_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def get_stats():
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM summarized_projects")
            total_projects = cursor.fetchone()[0]

            cursor.execute("SELECT language, COUNT(*) as count FROM summarized_projects WHERE language != 'N/A' AND language IS NOT NULL GROUP BY language ORDER BY count DESC LIMIT 1")
            top_lang_row = cursor.fetchone()
            top_language = top_lang_row[0] if top_lang_row else "N/A"

            one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            cursor.execute("SELECT COUNT(*) FROM summarized_projects WHERE summary_date >= ?", (one_week_ago,))
            weekly_new = cursor.fetchone()[0]
            
            total_reports = len([f for f in os.listdir(MD_DIR) if f.endswith('.md')])

            # New Stats
            cursor.execute("SELECT SUM(forks) FROM summarized_projects")
            total_forks = cursor.fetchone()[0] or 0

            cursor.execute("SELECT AVG(contributor_count) FROM summarized_projects WHERE contributor_count != 'N/A'")
            avg_contributors = cursor.fetchone()[0] or 0
            
            stats = {
                "totalReports": total_reports,
                "totalProjects": total_projects,
                "topLanguage": top_language,
                "weeklyNew": weekly_new,
                "totalForks": f"{total_forks:,}", # Formatted with commas
                "avgContributors": round(avg_contributors, 1)
            }
            return jsonify(stats)
    except Exception as e:
        print(f"Error in /api/stats: {e}")
        return jsonify({"error": str(e)}), 500
