import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_BASE_URL = os.getenv('LLM_BASE_URL')
LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4-turbo')

SCHEDULE_TIME = os.getenv('SCHEDULE_TIME', "09:00")
NUM_PROJECTS_TO_SUMMARIZE = int(os.getenv('NUM_PROJECTS_TO_SUMMARIZE', 8))
MAX_PROJECTS_TO_SCRAPE = int(os.getenv('MAX_PROJECTS_TO_SCRAPE', 25))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
MD_DIR = os.path.join(OUTPUT_DIR, 'md')
HTML_DIR = os.path.join(OUTPUT_DIR, 'html')
DB_PATH = os.path.join(OUTPUT_DIR, 'reporter.db')

# --- 抓取配置 ---
GITHUB_TRENDING_URL = "https://github.com/trending"

# --- Prompt 模板 ---
# 1. 用于生成单项目深度点评的模板
SINGLE_PROJECT_PROMPT_TEMPLATE = """
# 角色：资深技术分析师与博主

## 任务：对以下这个 GitHub 项目进行一次深刻且生动的单点分析

### 项目信息
- **项目名称**: `{name}`
- **编程语言**: `{language}`
- **项目描述**: `{description}`
- **项目链接**: `{url}`
- **今日星标数**: `{stars}`

### 写作要求
- **风格**: 专业、风趣、有洞见，多使用 Emoji ✨💡🚀📈🤔 增加可读性。
- **结构**: 必须包含以下几个部分，并使用 Markdown 加以组织：
    - `### ✨ {name}`
    - `**一句话点评**: [用一句话精彩地概括其核心价值]`
    - `**💡 技术亮点与创新**: [深入分析其技术栈、实现方式或设计思路的过人之处]`
    - `**📈 潜在影响与应用**: [探讨它可能对行业带来的改变，或在哪些具体场景下能大放异彩]`
    - `**🔗 项目链接**: [{name}]({url})`
- **纯净度**: **直接输出该项目的 Markdown 分析内容，不要任何额外的解释或客套话。**
"""

# 2. 用于生成日报开篇导语的模板
OVERVIEW_PROMPT_TEMPLATE = """
# 角色：顶尖技术观察员

## 任务：根据今天值得关注的几个项目名称，生成一句引人注目的开篇导语

### 今日焦点项目列表
{project_names}

### 要求
- **风格**: 高度概括、充满激情、一语中的。
- **格式**: 只输出一句话，用 `##` 作为 Markdown 标题。
- **示例**: `## 🚀 AI 浪潮持续席卷，今天 GitHub 被几个颠覆性的开源模型刷屏了！`
- **纯净度**: **只输出一句话的导语，不要任何其他文字。**
"""

# --- HTML 模板  ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans SC', sans-serif;
            line-height: 1.8;
            color: #34495e;
            background: linear-gradient(to right bottom, #fdfbfb, #ebedee);
            margin: 0;
            padding: 20px;
        }}
        .main-container {{
            max-width: 850px;
            margin: 40px auto;
            background-color: #ffffff;
            padding: 30px 50px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        }}
        h1, h2, h3, h4 {{
            color: #2c3e50;
            font-weight: 700;
        }}
        h1 {{
            font-size: 2.2em;
            text-align: center;
            margin-bottom: 20px;
            border-bottom: none;
        }}
        h2 {{
            font-size: 1.6em;
            margin-top: 50px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }}
        .card {{
            background: #f9f9f9;
            border-left: 5px solid #3498db;
            padding: 20px;
            margin: 25px 0;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }}
        code {{
            background-color: #e8f6ff;
            color: #2980b9;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #2c3e50;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        a {{
            color: #2980b9;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }}
        a:hover {{
            color: #1f618d;
            text-decoration: underline;
        }}
        ul, ol {{
            padding-left: 25px;
        }}
        li {{
            margin-bottom: 12px;
        }}
        .footer {{
            text-align: center;
            margin-top: 60px;
            font-size: 0.9em;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        {content}
        <div class="footer">
            <p>❤️ Generated by GitHub Trending Reporter</p>
        </div>
    </div>
</body>
</html>
"""
