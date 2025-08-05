import sqlite3
from config.settings import DB_PATH
from datetime import date

class ProjectDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._create_schema()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10) # Add timeout to reduce locking issues
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _create_schema(self):
        # This method remains the same as it's only called once at init.
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS dim_languages (language_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)")
                cursor.execute("CREATE TABLE IF NOT EXISTS dim_tags (tag_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS dim_projects (
                        project_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, url TEXT,
                        description TEXT, language_id INTEGER,
                        FOREIGN KEY (language_id) REFERENCES dim_languages (language_id)
                    )""")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS dim_dates (
                        date_id INTEGER PRIMARY KEY, full_date DATE NOT NULL UNIQUE, year INTEGER,
                        month INTEGER, day INTEGER, weekday INTEGER, week_of_year INTEGER
                    )""")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS assoc_project_tags (
                        project_id INTEGER, tag_id INTEGER, PRIMARY KEY (project_id, tag_id),
                        FOREIGN KEY (project_id) REFERENCES dim_projects (project_id),
                        FOREIGN KEY (tag_id) REFERENCES dim_tags (tag_id)
                    )""")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fact_trending_snapshots (
                        snapshot_id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL, date_id INTEGER NOT NULL,
                        rank INTEGER NOT NULL, stars INTEGER, forks INTEGER,
                        UNIQUE(project_id, date_id),
                        FOREIGN KEY (project_id) REFERENCES dim_projects (project_id),
                        FOREIGN KEY (date_id) REFERENCES dim_dates (date_id)
                    )""")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS summarized_projects (
                        name TEXT PRIMARY KEY, url TEXT, description TEXT, language TEXT, stars INTEGER,
                        forks INTEGER, contributor_count INTEGER, created_at TEXT, updated_at TEXT,
                        open_issues INTEGER, watchers INTEGER, summary_date TEXT NOT NULL
                    )""")
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database error (_create_schema): {e}")

    # --- Refactored Dimension Helpers to use a passed cursor ---

    def _get_or_create_dimension_id(self, cursor, table, column, value):
        cursor.execute(f"SELECT {column}_id FROM {table} WHERE name = ?", (value,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (value,))
            return cursor.lastrowid

    def get_or_create_language_id(self, cursor, language_name):
        if not language_name or language_name == 'N/A':
            return None
        return self._get_or_create_dimension_id(cursor, 'dim_languages', 'language', language_name)

    def get_or_create_tag_id(self, cursor, tag_name):
        return self._get_or_create_dimension_id(cursor, 'dim_tags', 'tag', tag_name)

    def get_or_create_date_id(self, cursor, date_obj):
        date_id = int(date_obj.strftime('%Y%m%d'))
        cursor.execute("SELECT date_id FROM dim_dates WHERE date_id = ?", (date_id,))
        if cursor.fetchone():
            return date_id
        else:
            cursor.execute("INSERT INTO dim_dates (date_id, full_date, year, month, day, weekday, week_of_year) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (date_id, date_obj, date_obj.year, date_obj.month, date_obj.day, date_obj.weekday(), date_obj.isocalendar()[1]))
            return date_id

    def get_or_create_project_id(self, cursor, project_data):
        cursor.execute("SELECT project_id FROM dim_projects WHERE name = ?", (project_data['name'],))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            lang_id = self.get_or_create_language_id(cursor, project_data.get('language'))
            cursor.execute("INSERT INTO dim_projects (name, url, description, language_id) VALUES (?, ?, ?, ?)",
                           (project_data['name'], project_data.get('url'), project_data.get('description'), lang_id))
            project_id = cursor.lastrowid
            
            tag_names = project_data.get('tags', [])
            for tag_name in tag_names:
                tag_id = self.get_or_create_tag_id(cursor, tag_name)
                cursor.execute("INSERT OR IGNORE INTO assoc_project_tags (project_id, tag_id) VALUES (?, ?)", (project_id, tag_id))
            return project_id

    # --- Main method now manages the connection for the whole transaction ---

    def add_trending_snapshots(self, projects_data, snapshot_date):
        """
        Adds a batch of trending snapshots in a single transaction.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                date_id = self.get_or_create_date_id(cursor, snapshot_date)
                
                for project_data in projects_data:
                    project_id = self.get_or_create_project_id(cursor, project_data)
                    cursor.execute(
                        """INSERT OR IGNORE INTO fact_trending_snapshots 
                           (project_id, date_id, rank, stars, forks) 
                           VALUES (?, ?, ?, ?, ?)""",
                        (
                            project_id, date_id, project_data['rank'],
                            project_data.get('stars', 0), project_data.get('forks', 0)
                        )
                    )
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database error (add_trending_snapshots): {e}")


    # --- Methods for the old reporting feature (to keep it working) ---
    def get_all_summarized_project_names(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM summarized_projects")
                return {row[0] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            print(f"❌ Database error (get_all_summarized_project_names): {e}")
            return set()

    def add_summarized_project(self, project):
        if not project: return
        today_str = date.today().isoformat()
        project_data = (
            project.get('name'), project.get('url'), project.get('description', 'N/A'),
            project.get('language', 'N/A'), project.get('stars', 0), project.get('forks', 0),
            project.get('contributor_count', 0), project.get('created_at', 'N/A'),
            project.get('updated_at', 'N/A'), project.get('open_issues', 0),
            project.get('watchers', 0), today_str
        )
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT OR REPLACE INTO summarized_projects 
                       (name, url, description, language, stars, forks, contributor_count, 
                        created_at, updated_at, open_issues, watchers, summary_date) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    project_data
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database error (add_summarized_project): {e}")
