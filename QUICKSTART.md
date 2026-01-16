# 灵魂伴侣 - 快速开始指南

## 🚀 30 秒快速启动

### 第 1 步：配置 API Key

编辑 `.env` 文件（或创建一个新的）：

```bash
# 如果没有 .env 文件，复制示例
cp backend/.env.example .env

# 编辑 .env，添加您的 API Key
nano .env
```

**需要配置的内容**：
```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.haihub.cn/v1/
OPENAI_MODEL=Kimi-K2-Instruct
```

### 第 2 步：启动服务

```bash
# 一行命令启动前后端
./start.sh all
```

### 第 3 步：访问应用

打开浏览器访问：
```
http://localhost:3008
```

**完成！** 🎉

---

## 📋 常见命令

### 启动前后端（推荐）
```bash
./start.sh all
```

### 仅启动后端
```bash
./start.sh backend
```

### 仅启动前端
```bash
./start.sh frontend
```

### 自定义端口
```bash
# 后端使用 8011，前端使用 3009
./start.sh all --backend-port 8011 --frontend-port 3009
```

### 查看帮助
```bash
./start.sh --help
```

---

## ✅ 验证安装

### 检查后端
```bash
curl http://localhost:8010/health
```

应该返回：
```json
{"status": "healthy", "service": "soul-mate-agent"}
```

### 检查前端
访问 `http://localhost:3008`，应该看到聊天界面。

---

## 🧪 测试推荐功能

在聊天框输入：
```
推荐一些关于机器学习的书籍
```

应该看到：
- ✅ Agent 的回复
- ✅ 推荐的书籍列表
- ✅ 每本书的推荐理由、内容亮点、适合场景、评分

---

## 🆘 常见问题

### Q: 启动时出现"端口已被占用"错误

**A**: 脚本会自动查找可用端口。如果您想指定特定端口：
```bash
./start.sh all --backend-port 8011 --frontend-port 3009
```

### Q: 前端无法连接后端

**A**: 确保：
1. 后端服务正在运行（检查 8010 端口）
2. `.env` 文件已正确配置
3. 网络连接正常

### Q: npm 依赖安装失败

**A**: 清除缓存并重新安装：
```bash
cd frontend
npm cache clean --force
rm -rf node_modules
npm install
```

### Q: Python 依赖安装失败

**A**: 手动安装：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📁 项目结构简览

```
soul-mate-full/
├── backend/          # Flask 后端
├── frontend/         # React 前端
├── soul_mate/        # Python Agent 核心
├── start.sh          # 启动脚本
├── requirements.txt  # Python 依赖
└── .env             # 环境配置（需自己创建）
```

---

## 📚 更多信息

- **详细项目结构**：查看 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)
- **完整启动指南**：查看 [FINAL_STARTUP_GUIDE.md](../FINAL_STARTUP_GUIDE.md)
- **API 文档**：查看 `frontend/API_INTEGRATION.md`

---

## 🎯 下一步

1. ✅ 配置 `.env` 文件
2. ✅ 运行 `./start.sh all`
3. ✅ 访问 `http://localhost:3008`
4. ✅ 开始使用灵魂伴侣！

---

**需要帮助？** 查看 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) 的故障排查部分。
