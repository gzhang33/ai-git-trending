# GitHub Trending Reporter 🚀

[English](./README-EN.md) | 简体中文

**一个自动化分析 GitHub Trending 的机器人，为您每日精选、总结并生成技术洞察报告。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![Docker Support](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

---

## 🌟 项目亮点

- **📈 每日追踪与分析**: 自动抓取 GitHub Trending 的最新热门项目，并利用大语言模型（LLM）进行深度分析，产出“一句话点评”、“技术亮点”和“潜在影响”等洞察。
- **🌐 交互式报告**: 提供美观、现代化的 Web 界面，支持报告浏览、搜索和筛选，提供远超静态 Markdown 的阅读体验。
- **🚀 智能数据看板**: 内置趋势分析功能，可查看“上榜最频繁项目”、“热门语言趋势”以及“星标蹿升最快项目”，助您洞察技术潮流。
- **⚙️ 灵活高度可配**: 从 LLM 模型、API 地址到抓取频率、报告数量，几乎所有核心参数均可通过环境变量轻松配置。
- **📦 开箱即用**: 提供 Docker 支持，一键启动，无需繁琐的环境配置。

## 📊 数据看板与报告示例

项目不仅生成每日的详细报告，还提供了多维度的数据分析看板。

| 功能 | 截图 |
| :--- | :--- |
| **Web 报告主页** | ![Web UI Example](images/web.png) |
| **项目交互式卡片** | ![Interaction Example](images/interaction.png) |
| **星标蹿升趋势分析** | ![Star Surge Example](images/star.png) |
| **Markdown 产出示例** | ![Markdown Example](images/image.png) |


## 🛠️ 技术栈

- **后端**: Python 3.x, Flask
- **数据抓取**: `requests`, `BeautifulSoup4`
- **AI 集成**: `openai`
- **任务调度**: `schedule`
- **数据库**: `SQLite`
- **部署**: `Docker`

## 🚀 快速开始

### 1. 环境准备

克隆仓库并进入项目目录：
```bash
git clone https://github.com/lgy1027/ai-git-trending.git
cd ai-git-trending
```

### 2. 配置环境变量

复制 `.env.example` 文件为 `.env`，并填入您的 LLM 服务凭证：
```bash
cp .env.example .env
```
编辑 `.env` 文件：
```env
# .env
LLM_API_KEY="sk-your_api_key_here"
LLM_BASE_URL="https://api.openai.com/v1" # 根据您的服务商修改
LLM_MODEL="gpt-4-turbo" # 可选，默认为 gpt-4-turbo
```

### 3. 运行项目

#### 方式一：使用 Docker (推荐)

确保您已安装 Docker，然后执行：
```bash
# 构建镜像
docker build -t trending-reporter .

# 运行容器
docker run --env-file .env -p 5000:5000 trending-reporter
```

#### 方式二：本地运行

安装依赖：
```bash
pip install -r requirements.txt
```

项目包含两个独立的脚本：
- **启动 Web 服务**: `python run_web.py` (访问 `http://127.0.0.1:5000`)
- **手动触发报告生成**: `python run_reporter.py`

## ⚙️ 详细配置

### 环境变量 (`.env`)

- `LLM_API_KEY`: **(必需)** 大语言模型服务的 API Key。
- `LLM_BASE_URL`: **(必需)** 大语言模型服务的基础 URL。
- `LLM_MODEL`: (可选) 指定使用的模型，默认为 `gpt-4-turbo`。
- `GITHUB_API_TOKEN`: (可选) 您的 GitHub API Token。配置后可获取更详细的项目信息，并避免因 API 请求频率限制导致的问题。
- `SCHEDULE_TIME`: (可选) 每日任务执行的时间 (HH:MM 格式)，默认为 `"09:00"`。
- `NUM_PROJECTS_TO_SUMMARIZE`: (可选) 每日需要分析的新项目数量，默认为 `8`。
- `MAX_PROJECTS_TO_SCRAPE`: (可选) 从 Trending 列表中筛选的项目总数，默认为 `25`。
- `TRENDING_DATE_RANGE`: (可选) 指定抓取的时间范围，可选值为 `daily`, `weekly`, `monthly`，默认为 `daily`。

### Prompt 模板 (`config/settings.py`)

- `SINGLE_PROJECT_PROMPT_TEMPLATE`: 单个项目分析的 Prompt。
- `OVERVIEW_PROMPT_TEMPLATE`: 报告开篇导语的 Prompt。

## 公众号

欢迎关注我的公众号，获取实时技术解析及前沿观察。

<img src="images/wechat.png" width="300" height="300">

## 🤝 贡献

欢迎任何形式的贡献！如果您有好的想法或发现了 Bug，请随时提出 Issue 或提交 Pull Request。

## � 许可证

本项目采用 [MIT 许可证](LICENSE)。
