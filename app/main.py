# 文件名: app/main.py
# 作用: 核心任务调度与编排，已按新逻辑完全重构。

from datetime import datetime
from config.settings import NUM_PROJECTS_TO_SUMMARIZE
from .scraper import scrape_github_trending
from .database import ProjectDatabase
from .summarizer import get_summary_for_single_project, get_overview_intro
from .file_writer import save_summary_files
import time

def job():
    print(f"\n--- 🚀 Starting new job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    db = ProjectDatabase()
    
    # 1. 抓取 GitHub Trending 数据 (已按 MAX_PROJECTS_TO_SCRAPE 限制)
    all_trending_repos = scrape_github_trending()
    if not all_trending_repos:
        print("⏹️ Job finished: No data scraped.")
        return

    # 2. 【核心逻辑】从上到下筛选出固定数量的、未被总结过的新项目
    repos_to_summarize = []
    existing_project_names = db.get_all_summarized_project_names()
    
    print(f"🕵️‍♀️ Filtering for {NUM_PROJECTS_TO_SUMMARIZE} new projects from the top {len(all_trending_repos)} trending repos...")
    for repo in all_trending_repos:
        if repo['name'] not in existing_project_names:
            repos_to_summarize.append(repo)
        if len(repos_to_summarize) == NUM_PROJECTS_TO_SUMMARIZE:
            print(f"👍 Found {NUM_PROJECTS_TO_SUMMARIZE} new projects to summarize.")
            break # 已找到足够数量的新项目，停止搜索

    # 3. 检查是否找到了足够的新项目
    if len(repos_to_summarize) < NUM_PROJECTS_TO_SUMMARIZE:
        print(f"⚠️ Found only {len(repos_to_summarize)} new projects. Not enough to meet the target of {NUM_PROJECTS_TO_SUMMARIZE}.")
        print("⏹️ Job finished.")
        return

    # 4. 逐一分析项目并收集结果
    individual_summaries = []
    for project in repos_to_summarize:
        summary = get_summary_for_single_project(project)
        if summary:
            individual_summaries.append(summary)
            time.sleep(1) 
        else:
            print(f"❌ Critical error: Failed to summarize '{project['name']}'. Aborting today's job to ensure data consistency.")
            return

    # 5. 生成开篇导语并组合成最终报告
    intro = get_overview_intro(repos_to_summarize)
    final_report = intro + "\n\n" + "\n\n---\n\n".join(individual_summaries)
    
    # 6. 保存文件并将所有成功总结的项目一次性存入数据库
    save_summary_files(final_report)
    for project in repos_to_summarize:
        db.add_summarized_project(project)
    print(f"💾 Successfully saved {len(repos_to_summarize)} projects to database.")

    print(f"--- ✅ Job finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")