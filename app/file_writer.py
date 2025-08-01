import os
import markdown as md
from datetime import datetime
from config.settings import MD_DIR, HTML_DIR, HTML_TEMPLATE

def save_summary_files(summary_content):
    os.makedirs(MD_DIR, exist_ok=True)
    os.makedirs(HTML_DIR, exist_ok=True)
    today_str = datetime.now().strftime('%Y-%m-%d')
    file_basename = f"github_trending_{today_str}"
    md_filename = f"{file_basename}.md"
    html_filename = f"{file_basename}.html"
    md_path = os.path.join(MD_DIR, md_filename)
    html_path = os.path.join(HTML_DIR, html_filename)
    title = f"GitHub 热点日报 ({today_str})"
    tags = "GitHub, Trending, Tech, OpenSource"
    md_frontmatter = f"""---
title: "{title}"
date: {today_str}
tags: [{tags}]
---
"""
    full_md_content = f"{md_frontmatter}\n{summary_content}"
    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(full_md_content)
        print(f"✅ Markdown file saved to: {md_path}")
    except IOError as e:
        print(f"❌ Error writing Markdown file: {e}")
        return
    try:
        html_body = md.markdown(summary_content, extensions=['fenced_code', 'tables'])
        final_html = HTML_TEMPLATE.format(title=title, content=f"<h1>{title}</h1>\n{html_body}")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"✅ HTML file saved to: {html_path}")
    except Exception as e:
        print(f"❌ Error creating or writing HTML file: {e}")