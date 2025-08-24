# GitHub Trending Reporter - 后端使用说明

## 概述

后端已整合为统一的启动入口，支持三种运行模式：
- **完整模式 (full)**: 同时运行Web API服务和定时报告生成任务
- **Web模式 (web)**: 仅运行Web API服务
- **报告模式 (reporter)**: 仅运行定时报告生成任务

## 快速开始

### 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 基本运行

```bash
# 运行完整服务 (推荐)
python app.py

# 仅运行Web API服务
python app.py --mode web

# 仅运行定时报告生成器
python app.py --mode reporter
```

## 详细用法

### 命令行参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--mode` | 运行模式 (full/web/reporter) | full | `--mode web` |
| `--host` | Web服务监听地址 | 127.0.0.1 | `--host 0.0.0.0` |
| `--port` | Web服务端口 | 5001 | `--port 8080` |
| `--debug` | 启用调试模式 | False | `--debug` |

### 运行模式详解

#### 1. 完整模式 (full) - 推荐

```bash
python app.py
# 或
python app.py --mode full --port 5001 --debug
```

- 同时启动Web API服务和定时任务
- Web服务在主线程运行，定时任务在后台线程运行
- 适合生产环境和开发环境

#### 2. Web模式 (web)

```bash
python app.py --mode web --port 8080 --debug
```

- 仅启动Web API服务
- 适合前端开发时只需要API服务
- 支持热重载（debug模式）

#### 3. 报告模式 (reporter)

```bash
python app.py --mode reporter
```

- 仅运行定时报告生成任务
- 启动时立即执行一次报告生成
- 之后根据配置的时间定期执行
- 适合在服务器上独立运行数据采集任务

### 高级用法示例

```bash
# 生产环境 - 监听所有地址，端口80
python app.py --host 0.0.0.0 --port 80

# 开发环境 - 启用调试模式
python app.py --debug

# 仅运行API服务，用于前端开发
python app.py --mode web --debug --port 3001

# 服务器环境 - 仅运行数据采集
python app.py --mode reporter
```

## API 端点

Web服务提供以下API端点：

### API端点
- `GET /api/reports` - 获取所有报告列表
- `GET /api/report/<date>` - 获取指定日期的报告内容
- `GET /api/projects/<date>` - 获取指定日期的项目列表
- `GET /api/project/<project_name>` - 获取指定项目的详细信息
- `GET /api/stats` - 获取统计数据
- `GET /api/trends` - 获取趋势分析数据

### 静态资源
- `/images/*` - 静态图片资源访问

### 示例请求

```bash
# 获取统计信息
curl http://localhost:5001/api/stats

# 获取报告列表
curl http://localhost:5001/api/reports

# 获取特定日期的项目
curl http://localhost:5001/api/projects/2025-08-21
```

## 配置

项目配置通过 `config/settings.py` 文件管理，主要配置项：

- `SCHEDULE_TIME`: 定时任务执行时间 (格式: "HH:MM")
- `MD_DIR`: Markdown报告存储目录
- `DB_PATH`: 数据库文件路径
- `LLM_API_KEY`: LLM API密钥
- `GITHUB_API_TOKEN`: GitHub API令牌

## 注意事项

1. **端口冲突**: 默认使用5001端口，如果被占用请使用 `--port` 参数指定其他端口
2. **调试模式**: 生产环境请勿使用 `--debug` 参数
3. **权限问题**: 如果使用80端口，可能需要管理员权限
4. **数据库**: 确保output目录存在且有写入权限
5. **环境变量**: 确保.env文件配置正确

## 旧文件说明

以下旧的启动文件已被新的统一启动入口替代并已删除：

- `run_web.py` → 已删除，请使用 `python app.py --mode web`
- `run_reporter.py` → 已删除，请使用 `python app.py --mode reporter`

项目现在使用统一的启动入口 `app.py`，提供更好的可维护性和用户体验。

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 解决方案：使用其他端口
   python app.py --port 5002
   ```

2. **数据库权限错误**
   ```bash
   # 检查output目录权限
   ls -la output/
   # 如果需要，修改权限
   chmod 755 output/
   ```

3. **API返回错误**
   ```bash
   # 检查日志输出
   python app.py --debug
   ```

### 日志输出

启动时会显示详细的配置信息：
```
🚀 GitHub Trending Reporter
============================================================
📅 Current time: 2025-08-23 10:30:00
🎯 Mode: full
🌐 Web service: http://127.0.0.1:5001
🐛 Debug mode: OFF
⏰ Scheduled time: 09:00
============================================================
```

## 开发贡献

如需修改启动逻辑，请编辑 `app.py` 文件。该文件包含了完整的参数解析、服务启动和错误处理逻辑。