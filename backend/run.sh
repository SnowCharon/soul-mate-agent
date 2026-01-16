#!/bin/bash

# 灵魂伴侣后端启动脚本

# 设置环境变量
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_PORT=8010

# 检查 OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  警告: 未设置 OPENAI_API_KEY 环境变量"
    echo "请先运行: export OPENAI_API_KEY='your-api-key'"
    echo ""
fi

# 安装依赖（如果需要）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install -r requirements.txt

# 启动服务器
echo "🚀 启动灵魂伴侣后端服务器..."
echo "📍 地址: http://localhost:8010"
echo "📍 API 文档: http://localhost:8010/api/docs (如果启用 Swagger)"
echo ""

python backend/app.py
