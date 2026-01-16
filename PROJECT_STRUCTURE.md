# 灵魂伴侣 - 项目结构说明

## 📁 项目目录结构

```
soul-mate-full/
├── backend/                    # 后端 Flask 应用
│   ├── app.py                 # Flask 应用主文件
│   ├── run.sh                 # 后端启动脚本
│   └── .env.example           # 环境变量示例
│
├── frontend/                   # 前端 React 应用
│   ├── src/
│   │   ├── pages/             # 页面组件
│   │   │   └── Home.tsx       # 主页面（聊天界面）
│   │   ├── components/        # UI 组件
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── RecommendationCard.tsx
│   │   │   └── UserProfileSidebar.tsx
│   │   ├── lib/
│   │   │   └── api.ts         # API 客户端
│   │   ├── App.tsx            # 应用主组件
│   │   ├── main.tsx           # 入口文件
│   │   └── index.css          # 全局样式
│   ├── public/                # 静态资源
│   ├── index.html             # HTML 模板
│   ├── package.json           # 前端依赖
│   └── vite.config.ts         # Vite 配置
│
├── soul_mate/                  # Python Agent 核心模块
│   ├── agent.py               # Agent 主类
│   ├── llm_client.py          # LLM 客户端（支持自定义 API）
│   ├── user_profile.py        # 用户画像管理
│   ├── content_fetcher.py     # 内容获取
│   └── __init__.py
│
├── data/                       # 数据存储目录
│   └── user_profiles/         # 用户画像数据
│
├── examples/                   # 示例代码
│   └── demo.py
│
├── tests/                      # 测试文件
│
├── start.sh                    # 统一启动脚本（推荐使用）
├── main.py                     # Python 应用入口
├── requirements.txt            # Python 依赖
├── package.json               # 前端依赖（在 frontend 目录）
├── README.md                  # 项目说明
├── LICENSE                    # 许可证
└── .env                       # 环境配置（需自己创建）
```

## 🚀 快速启动

### 方式 1：启动前后端（推荐）

```bash
./start.sh all
```

**功能**：
- ✅ 自动检查系统依赖（Python、Node.js、npm）
- ✅ 自动安装后端依赖（Python 包）
- ✅ 自动安装前端依赖（npm 包）
- ✅ 自动检测端口冲突并使用可用端口
- ✅ 同时启动后端和前端服务
- ✅ 自动配置前后端通信

### 方式 2：仅启动后端

```bash
./start.sh backend
```

**功能**：
- ✅ 安装后端依赖
- ✅ 启动 Flask 服务器（默认 8010 端口）

### 方式 3：仅启动前端

```bash
./start.sh frontend
```

**功能**：
- ✅ 安装前端依赖
- ✅ 启动 Vite 开发服务器（默认 3008 端口）

## 📋 启动脚本选项

### 基本用法

```bash
./start.sh [模式] [选项]
```

### 模式

- `all` - 启动前后端（默认）
- `backend` - 仅启动后端
- `frontend` - 仅启动前端

### 选项

- `--backend-port PORT` - 指定后端端口（默认 8010）
- `--frontend-port PORT` - 指定前端端口（默认 3008）
- `--help` - 显示帮助信息

### 示例

```bash
# 启动前后端，使用默认端口
./start.sh all

# 启动前后端，指定后端端口为 8011
./start.sh all --backend-port 8011

# 启动前后端，指定前端端口为 3009
./start.sh all --frontend-port 3009

# 启动前后端，同时指定两个端口
./start.sh all --backend-port 8011 --frontend-port 3009

# 仅启动后端
./start.sh backend

# 仅启动前端，指定端口
./start.sh frontend --frontend-port 3009

# 显示帮助
./start.sh --help
```

## ⚙️ 环境配置

### 创建 .env 文件

在项目根目录创建 `.env` 文件（或复制 `backend/.env.example`）：

```bash
cp backend/.env.example .env
```

### 配置内容

```env
# OpenAI API 配置（支持 HaiHub 等兼容 API）
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.haihub.cn/v1/
OPENAI_MODEL=Kimi-K2-Instruct

# Flask 配置
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_PORT=8010

# CORS 配置
CORS_ORIGINS=http://localhost:3008,http://localhost:3000,http://127.0.0.1:3008

# 日志配置
LOG_LEVEL=INFO

# 数据存储路径
DATA_DIR=data/user_profiles
```

## 🔍 验证安装

### 1. 检查后端

```bash
curl http://localhost:8010/health
```

**预期响应**：
```json
{"status": "healthy", "service": "soul-mate-agent"}
```

### 2. 检查前端

访问浏览器：
```
http://localhost:3008
```

**预期结果**：看到灵魂伴侣聊天界面

## 🧪 测试功能

### 测试推荐功能

在聊天框输入：
```
推荐一些关于Python编程的书籍
```

**预期结果**：
- ✅ Agent 理解需求
- ✅ 调用 Kimi 模型生成推荐
- ✅ 返回推荐内容（包含理由、亮点、评分等）

### 测试无关问题过滤

在聊天框输入：
```
今天天气怎么样？
```

**预期结果**：
- ✅ Agent 识别无关问题
- ✅ 礼貌拒绝并引导回到阅读话题

## 📊 API 端点

### 健康检查
```
GET /health
```

### 发送消息
```
POST /api/chat
Content-Type: application/json

{
  "user_id": "user123",
  "message": "推荐一些书籍",
  "session_id": "session123"
}
```

### 获取用户画像
```
GET /api/user/{user_id}
```

### 提交反馈
```
POST /api/feedback
Content-Type: application/json

{
  "user_id": "user123",
  "item_id": "book123",
  "liked": true,
  "item_info": {...}
}
```

## 🔧 故障排查

### 问题 1：端口已被占用

**症状**：
```
Address already in use
```

**解决**：
```bash
# 使用不同的端口
./start.sh all --backend-port 8011 --frontend-port 3009

# 或查找占用端口的进程
lsof -i :8010
kill -9 <PID>
```

### 问题 2：Python 依赖安装失败

**症状**：
```
pip install failed
```

**解决**：
```bash
# 手动安装
cd soul-mate-full
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 问题 3：npm 依赖安装失败

**症状**：
```
npm ERR!
```

**解决**：
```bash
# 清除缓存并重新安装
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 问题 4：前端无法连接后端

**症状**：
```
发送消息失败
```

**解决**：
```bash
# 检查后端是否运行
curl http://localhost:8010/health

# 检查 API URL 配置
# 在 frontend/src/lib/api.ts 中验证 API_BASE_URL
```

## 📝 开发工作流

### 1. 启动服务

```bash
./start.sh all
```

### 2. 修改代码

- 后端代码：修改 `backend/app.py` 或 `soul_mate/` 目录下的文件
- 前端代码：修改 `frontend/src/` 下的文件

### 3. 热重载

- **后端**：Flask 开发服务器自动重载（FLASK_DEBUG=1）
- **前端**：Vite 开发服务器自动热更新

### 4. 测试

```bash
# 后端测试
cd soul-mate-full
python -m pytest tests/

# 前端测试
cd frontend
npm run test
```

## 🚢 部署

### 生产构建

```bash
# 前端构建
cd frontend
npm run build

# 后端部署
# 使用 gunicorn 或其他 WSGI 服务器
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8010 backend.app:app
```

## 📚 相关文档

- [README.md](./README.md) - 项目说明
- [FINAL_STARTUP_GUIDE.md](../FINAL_STARTUP_GUIDE.md) - 完整启动指南
- [API_INTEGRATION.md](./frontend/API_INTEGRATION.md) - API 集成文档

## 🎯 下一步

1. 配置 `.env` 文件（添加 API Key）
2. 运行 `./start.sh all` 启动服务
3. 访问 `http://localhost:3008` 使用应用
4. 测试推荐功能

---

**灵魂伴侣已准备就绪！** 🎉
