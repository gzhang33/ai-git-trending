from datetime import datetime
from config.settings import NUM_PROJECTS_TO_SUMMARIZE, DAYS_TO_SKIP
from .scraper import scrape_github_trending
from .database import ProjectDatabase
from .summarizer import get_summary_for_single_project, get_overview_intro
from .file_writer import save_summary_files
import time

def job():
    print(f"\n--- 🚀 Starting new job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    db = ProjectDatabase()
    
    all_trending_repos = scrape_github_trending()
    if not all_trending_repos:
        print("⏹️ Job finished: No data scraped.")
        return

    snapshot_date = datetime.now().date()
    print(f"💾 Ingesting {len(all_trending_repos)} projects for date: {snapshot_date.isoformat()}")
    
    # Add rank to each project
    for i, repo_data in enumerate(all_trending_repos):
        repo_data['rank'] = i + 1
        
    # Use the new batch insertion method
    db.add_trending_snapshots(all_trending_repos, snapshot_date)
    
    print(f"✅ Successfully ingested {len(all_trending_repos)} snapshots into the database.")

    # --- The summarization logic remains, but uses the new DB methods ---
    
    # Get project names that have been summarized recently
    existing_project_names = db.get_all_summarized_project_names()
    
    repos_to_summarize = []
    print(f"🕵️‍♀️ Filtering for {NUM_PROJECTS_TO_SUMMARIZE} new projects to summarize...")
    for repo in all_trending_repos:
        if repo['name'] not in existing_project_names:
            repos_to_summarize.append(repo)
        if len(repos_to_summarize) >= NUM_PROJECTS_TO_SUMMARIZE:
            print(f"👍 Found {len(repos_to_summarize)} new projects to summarize.")
            break

    if not repos_to_summarize:
        print("✅ No new projects to summarize today.")
    else:
        print(f"📝 Summarizing {len(repos_to_summarize)} new projects...")
        individual_summaries = []
        for project in repos_to_summarize:
            summary = get_summary_for_single_project(project)
            if summary:
                individual_summaries.append(summary)
                # Also add it to the legacy summarized_projects table
                db.add_summarized_project(project)
                time.sleep(1) 
            else:
                print(f"❌ Warning: Failed to summarize '{project['name']}'. Skipping this project.")

        if individual_summaries:
            intro = get_overview_intro(repos_to_summarize)
            final_report = intro + "\n\n" + "\n\n---\n\n".join(individual_summaries)
            
            save_summary_files(final_report)
            print(f"💾 Successfully saved report for {len(repos_to_summarize)} projects.")

    print(f"--- ✅ Job finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
