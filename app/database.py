import sqlite3
from config.settings import DB_PATH
from datetime import date, timedelta

class ProjectDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS summarized_projects (
                        name TEXT PRIMARY KEY,
                        url TEXT,
                        stars INTEGER,
                        language TEXT,
                        summary_date TEXT NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database error (create_table): {e}")

    def get_all_summarized_project_names(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM summarized_projects")
                return {row[0] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            print(f"❌ Database error (get_all_summarized_project_names): {e}")
            return set()

    def get_recent_project_names(self, days=7):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                seven_days_ago = (date.today() - timedelta(days=days)).isoformat()
                cursor.execute("SELECT name FROM summarized_projects WHERE summary_date >= ?", (seven_days_ago,))
                return {row[0] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            print(f"❌ Database error (get_recent_project_names): {e}")
            return set()

    def add_summarized_project(self, project):
        if not project:
            return

        today_str = date.today().isoformat()
        project_data = (project['name'], project['url'], project['stars'], project.get('language', 'N/A'), today_str)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO summarized_projects (name, url, stars, language, summary_date) VALUES (?, ?, ?, ?, ?)",
                    project_data
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database error (add_summarized_project): {e}")
