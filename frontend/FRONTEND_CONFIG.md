# 前端端口配置说明

## 📋 配置统一

前端项目现在已经统一配置后端API端口，所有调用都指向后端的默认端口。

### 🔧 配置文件

**环境变量配置**: `frontend/.env`
```env
VITE_API_BASE_URL=http://localhost:5002
```

### 📁 涉及的文件

1. **[vite.config.ts](./vite.config.ts)** - Vite开发服务器代理配置
   - 使用环境变量 `VITE_API_BASE_URL`
   - 默认值: `http://localhost:5002`

2. **[src/api/reports.ts](./src/api/reports.ts)** - API调用配置
   - 使用环境变量 `VITE_API_BASE_URL`
   - 默认值: `http://localhost:5002`

3. **[src/views/Home.vue](./src/views/Home.vue)** - 首页组件
   - API_BASE_URL: `http://localhost:5002` ✅

4. **[src/views/Home-simple.vue](./src/views/Home-simple.vue)** - 简化首页
   - API_BASE_URL: `http://localhost:5002` ✅ (已更新)

### 🔄 配置优先级

1. **环境变量** - `VITE_API_BASE_URL`
2. **默认值** - `http://localhost:5002`

### 🚀 使用方式

#### 开发环境
```bash
cd frontend
npm run dev
```
*自动使用 `.env` 文件中配置的端口*

#### 临时更改端口
```bash
# 方式1: 修改 .env 文件
echo "VITE_API_BASE_URL=http://localhost:8080" > .env

# 方式2: 使用环境变量
VITE_API_BASE_URL=http://localhost:8080 npm run dev
```

### 🔗 前后端端口匹配

| 组件 | 配置位置 | 端口 | 状态 |
|------|----------|------|------|
| 后端服务 | `backend/.env` | 5002 | ✅ |
| 前端API | `frontend/.env` | 5002 | ✅ |
| Vite代理 | `vite.config.ts` | 5002 | ✅ |

### 📝 注意事项

1. **开发环境**: Vite会自动代理API请求到后端
2. **生产环境**: 需要确保Nginx配置正确转发API请求
3. **Docker部署**: 容器间通信使用容器名而非localhost

### 🛠️ 故障排除

#### 前端无法连接后端
1. 检查后端服务是否在正确端口启动
   ```bash
   cd backend
   python app.py --mode web
   ```

2. 检查前端环境变量配置
   ```bash
   cd frontend
   cat .env
   ```

3. 检查浏览器网络面板是否有跨域错误

#### 端口配置不生效
1. 重启Vite开发服务器
   ```bash
   cd frontend
   npm run dev
   ```

2. 清除浏览器缓存
3. 检查环境变量是否正确读取

---

**配置文件位置**:
- 前端: `frontend/.env`
- 后端: `backend/.env`