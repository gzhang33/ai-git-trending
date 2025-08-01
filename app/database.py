import sqlite3
from config.settings import DB_PATH
from datetime import date

class ProjectDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        """创建数据库表（如果不存在），包含新字段"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS summarized_projects (
                        name TEXT PRIMARY KEY,
                        url TEXT,
                        stars INTEGER,
                        summary_date TEXT NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database error (create_table): {e}")

    def get_all_summarized_project_names(self):
        """
        【新增方法】获取数据库中所有已总结项目的名称集合，用于快速去重。
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM summarized_projects")
                return {row[0] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            print(f"❌ Database error (get_all_summarized_project_names): {e}")
            return set() # 出现错误时返回空集合

    def add_summarized_project(self, project):
        """将单个新总结的项目添加到数据库中。"""
        if not project:
            return

        today_str = date.today().isoformat()
        project_data = (project['name'], project['url'], project['stars'], today_str)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO summarized_projects (name, url, stars, summary_date) VALUES (?, ?, ?, ?)",
                    project_data
                )
                conn.commit()
            # print(f"💾 Saved project '{project['name']}' to database.") # 在循环中打印太频繁，可在main中统一处理
        except sqlite3.Error as e:
            print(f"❌ Database error (add_summarized_project): {e}")
