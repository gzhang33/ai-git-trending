#!/bin/bash

# GitHub Trending Reporter - 前后端分离版本启动脚本

echo "🚀 启动 GitHub Trending Reporter"
echo "================================"

# 检查是否安装了必要的依赖
echo "📦 检查依赖..."

# 检查Python依赖
if [ ! -d "backend/venv" ]; then
    echo "⚠️  未找到Python虚拟环境，正在创建..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# 检查Node.js依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  未找到Node.js依赖，正在安装..."
    cd frontend
    npm install
    cd ..
fi

echo "✅ 依赖检查完成"

# 启动后端服务
echo "🔧 启动后端服务 (端口: 5000)..."
cd backend
source venv/bin/activate
python run_web.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端开发服务器
echo "🎨 启动前端服务 (端口: 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 服务启动完成！"
echo "================================"
echo "📱 前端地址: http://localhost:5173"
echo "🔧 后端API: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 处理退出信号
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# 等待进程结束
wait