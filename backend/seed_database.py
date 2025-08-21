import sqlite3
from datetime import date, timedelta
import random
from app.database import ProjectDatabase

# --- Configuration ---
NUM_DAYS_TO_SEED = 14  # Generate data for the last 14 days
PROJECTS_PER_DAY = 20 # Number of trending projects per day

# --- Mock Data Pool ---
PROJECT_POOL = [
    {"name": "llm-compiler", "language": "Python", "tags": ["ai", "compiler", "llm"]},
    {"name": "react-three-fiber", "language": "TypeScript", "tags": ["web", "react", "graphics", "threejs"]},
    {"name": "polars", "language": "Rust", "tags": ["data-science", "dataframe", "rust"]},
    {"name": "fastapi", "language": "Python", "tags": ["web", "api", "python"]},
    {"name": "htmx", "language": "JavaScript", "tags": ["web", "frontend", "javascript"]},
    {"name": "bun", "language": "Zig", "tags": ["javascript", "runtime", "performance"]},
    {"name": "lobe-chat", "language": "TypeScript", "tags": ["ai", "llm", "chat", "agent"]},
    {"name": "neovim", "language": "C", "tags": ["editor", "vim", "lua"]},
    {"name": "tauri", "language": "Rust", "tags": ["desktop", "rust", "gui"]},
    {"name": "supabase", "language": "TypeScript", "tags": ["backend", "database", "postgres"]},
    {"name": "langchain", "language": "Python", "tags": ["ai", "llm", "agent"]},
    {"name": "docker", "language": "Go", "tags": ["devops", "container", "docker"]},
    {"name": "kubernetes", "language": "Go", "tags": ["devops", "orchestration", "container"]},
    {"name": "vscode", "language": "TypeScript", "tags": ["editor", "microsoft"]},
    {"name": "tensorflow", "language": "C++", "tags": ["ai", "machine-learning"]},
    {"name": "pytorch", "language": "Python", "tags": ["ai", "machine-learning"]},
    {"name": "ansible", "language": "Python", "tags": ["devops", "automation"]},
    {"name": "huggingface-transformers", "language": "Python", "tags": ["ai", "nlp", "machine-learning"]},
    {"name": "deno", "language": "Rust", "tags": ["javascript", "runtime"]},
    {"name": "svelte", "language": "TypeScript", "tags": ["web", "frontend", "javascript"]},
]

def clear_database(db):
    """Clears all relevant tables before seeding."""
    print("🗑️ Clearing old data from tables...")
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            # Clear in reverse order of dependency
            cursor.execute("DELETE FROM fact_trending_snapshots;")
            cursor.execute("DELETE FROM assoc_project_tags;")
            cursor.execute("DELETE FROM dim_projects;")
            cursor.execute("DELETE FROM dim_tags;")
            cursor.execute("DELETE FROM dim_languages;")
            cursor.execute("DELETE FROM dim_dates;")
            # Also clear the old table if it exists
            cursor.execute("DELETE FROM trending_history;")
            conn.commit()
        print("✅ Old data cleared.")
    except sqlite3.Error as e:
        print(f"⚠️  Could not clear tables (they might not exist yet): {e}")


def seed_data():
    """
    Populates the database with mock trend data using the star schema.
    """
    print("🌱 Starting to seed mock data for the new Star Schema...")
    db = ProjectDatabase()
    
    # Clear existing data to prevent duplicates
    clear_database(db)

    today = date.today()
    
    print(f"📅 Generating data for the last {NUM_DAYS_TO_SEED} days...")
    for i in range(NUM_DAYS_TO_SEED):
        current_date = today - timedelta(days=i)
        
        # Select a random subset of projects for the day
        projects_for_the_day = random.sample(PROJECT_POOL, k=min(len(PROJECT_POOL), PROJECTS_PER_DAY))
        
        # Prepare the list of project data for batch insertion
        batch_data = []
        for rank, project_info in enumerate(projects_for_the_day, 1):
            # Simulate star growth over time
            base_stars = (NUM_DAYS_TO_SEED - i) * 200
            stars = base_stars + random.randint(50, 300)
            
            project_data = {
                "name": project_info["name"],
                "url": f"https://github.com/mock/{project_info['name']}",
                "description": f"A mock description for {project_info['name']}.",
                "language": project_info["language"],
                "tags": project_info["tags"],
                "stars": stars,
                "forks": stars // 4 + random.randint(10, 50),
                "rank": rank,
            }
            batch_data.append(project_data)
            
        # Use the correct batch method once per day
        db.add_trending_snapshots(batch_data, current_date)

    print(f"✅ Successfully seeded data for {NUM_DAYS_TO_SEED} days.")


if __name__ == "__main__":
    seed_data()
