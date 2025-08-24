import os
from dotenv import load_dotenv

# 获取项目根目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载项目根目录下的.env文件
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)

GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_BASE_URL = os.getenv('LLM_BASE_URL')
LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4-turbo')

SCHEDULE_TIME = os.getenv('SCHEDULE_TIME', "09:00")
NUM_PROJECTS_TO_SUMMARIZE = int(os.getenv('NUM_PROJECTS_TO_SUMMARIZE', 8))
MAX_PROJECTS_TO_SCRAPE = int(os.getenv('MAX_PROJECTS_TO_SCRAPE', 25))
DAYS_TO_SKIP = int(os.getenv('DAYS_TO_SKIP', 7))

# 设置输出目录路径 - 指向项目根目录下的output目录
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
MD_DIR = os.path.join(OUTPUT_DIR, 'md')
HTML_DIR = os.path.join(OUTPUT_DIR, 'html')
DB_PATH = os.path.join(OUTPUT_DIR, 'reporter.db')

TRENDING_DATE_RANGE = os.getenv('TRENDING_DATE_RANGE', 'daily').lower()

GITHUB_TRENDING_URL = f"https://github.com/trending?since={TRENDING_DATE_RANGE}"

SINGLE_PROJECT_PROMPT_TEMPLATE = """
# 角色：资深技术分析师与博主

## 任务：对以下这个 GitHub 项目进行一次深刻且生动的单点分析

### 项目信息
- **项目名称**: `{name}`
- **编程语言**: `{language}`
- **项目描述**: `{description}`
- **项目链接**: `{url}`
- **总星标数**: `{stars}`
- **Forks**: `{forks}`
- **贡献者数量**: `{contributor_count}`
- **创建日期**: `{created_at}`
- **最近更新**: `{updated_at}`
- **开放Issue数**: `{open_issues}`
- **Watchers**: `{watchers}`

### 写作要求
- **风格**: 专业、风趣、有洞见，多使用 Emoji ✨💡🚀📈🤔 增加可读性。
- **结构**: 必须包含以下几个部分，并使用 Markdown 加以组织：
    - `### ✨ {name} ({stars}星)）`
    - `**一句话点评**: [用一句话精彩地概括其核心价值]`
    - `**💡 技术亮点与创新**: [深入分析其技术栈、实现方式或设计思路的过人之处]`
    - `**📈 潜在影响与应用**: [探讨它可能对行业带来的改变，或在哪些具体场景下能大放异彩]`
    - `**🔗 项目链接**: [{name}]({url})`
- **纯净度**: **直接输出该项目的 Markdown 分析内容，不要任何额外的解释或客套话。**
"""

OVERVIEW_PROMPT_TEMPLATE = """
# 角色：顶尖技术分析师

## 任务：根据今日的热点项目列表，生成一段简明扼要的摘要。

### 今日焦点项目列表
{project_details}

### 要求
- **风格**: 专业、精炼、信息导向。
- **内容**:
    1.  **主题概括**: 用一句话点出今天上榜项目的主要技术领域或趋势（例如：AI Infra、开发工具、多模态应用等）。
    2.  **范围说明**: 概括项目范围，提及一些具体的例子，格式为“从...到...”。
    3.  **结尾**: 固定以“具体项目摘要如下：”结尾，确保与后续内容无缝衔接。
- **格式**: 输出一个简洁的段落，使用 Markdown `##` 作为主标题。
- **示例**:
    `## 今日热点：AI Infra 与多模态应用持续升温`
    `今天的 GitHub 热榜涵盖了从底层的 AI 基础设施到上层的多模态应用等多个领域。具体项目摘要如下：`
- **纯净度**: **只输出摘要部分，不要任何其他无关文字。**
"""

ENTITY_PROMPT_TEMPLATE = """
# 角色：顶尖技术战略分析师

## 任务：基于以下开发者/组织信息，生成一段精辟的“速览”点评。

### 实体信息
- **名称**: `{name}` ({type})
- **简介**: {bio}
- **创建于**: {created_at}
- **关注者**: {followers}
- **公开仓库数**: {public_repos}

### 旗下知名仓库
{top_repos}

### 技术栈偏好分析
- **主要语言**: {main_languages}

### 写作要求
- **风格**: 专业、有洞察力、数据驱动。
- **结构**:
    - `**技术影响力**: [一句话总结其在技术社区的地位和影响力]`
    - `**技术栈偏好**: [分析其主要使用的编程语言和技术领域]`
    - `**核心领域**: [判断其专注的核心方向，例如：AI Infra、前端工具、数据科学等]`
- **纯净度**: **直接输出 Markdown 格式的点评，不要任何额外解释。**
"""

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
