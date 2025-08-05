import sqlite3
from config.settings import DB_PATH
from datetime import date, timedelta

class ProjectDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._create_table()
        self._migrate_schema()

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
                        description TEXT,
                        language TEXT,
                        stars INTEGER,
                        forks INTEGER,
                        contributor_count INTEGER,
                        created_at TEXT,
                        updated_at TEXT,
                        open_issues INTEGER,
                        watchers INTEGER,
                        summary_date TEXT NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database error (create_table): {e}")

    def _migrate_schema(self):
        """
        Ensures the database schema is up-to-date by adding missing columns.
        """
        print("🔍 Checking database schema...")
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Get existing columns
                cursor.execute("PRAGMA table_info(summarized_projects)")
                columns = [row[1] for row in cursor.fetchall()]
                
                # Define all expected columns
                expected_columns = {
                    "description": "TEXT",
                    "forks": "INTEGER",
                    "contributor_count": "INTEGER",
                    "created_at": "TEXT",
                    "updated_at": "TEXT",
                    "open_issues": "INTEGER",
                    "watchers": "INTEGER"
                }
                
                migrated = False
                for col, col_type in expected_columns.items():
                    if col not in columns:
                        print(f"  -> Adding missing column: '{col}'")
                        cursor.execute(f"ALTER TABLE summarized_projects ADD COLUMN {col} {col_type}")
                        migrated = True
                
                if migrated:
                    conn.commit()
                    print("✅ Database schema migration completed.")
                else:
                    print("✅ Database schema is up-to-date.")

        except sqlite3.Error as e:
            print(f"❌ Database error (migrate_schema): {e}")

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
        
        # Ensure all fields have a default value
        project_data = (
            project.get('name'), 
            project.get('url'),
            project.get('description', 'N/A'),
            project.get('language', 'N/A'),
            project.get('stars', 0),
            project.get('forks', 0),
            project.get('contributor_count', 0),
            project.get('created_at', 'N/A'),
            project.get('updated_at', 'N/A'),
            project.get('open_issues', 0),
            project.get('watchers', 0),
            today_str
        )

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT OR REPLACE INTO summarized_projects (
                        name, url, description, language, stars, forks, contributor_count, 
                        created_at, updated_at, open_issues, watchers, summary_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    project_data
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database error (add_summarized_project): {e}")
