# 灵魂伴侣 - 部署指南

## 📦 项目打包和部署

### 方式 1：使用压缩包部署

#### 1. 下载压缩包

```bash
# 从 GitHub 或其他源下载 soul-mate-full.tar.gz
wget https://your-server/soul-mate-full.tar.gz
```

#### 2. 解压项目

```bash
tar -xzf soul-mate-full.tar.gz
cd soul-mate-full
```

#### 3. 配置环境

```bash
# 复制环境配置示例
cp backend/.env.example .env

# 编辑 .env，添加您的 API Key
nano .env
```

**需要配置的内容**：
```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.haihub.cn/v1/
OPENAI_MODEL=Kimi-K2-Instruct
FLASK_PORT=8010
```

#### 4. 启动服务

```bash
# 给启动脚本添加执行权限
chmod +x start.sh

# 启动前后端
./start.sh all
```

---

## 🐳 Docker 部署

### 创建 Dockerfile

在项目根目录创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim as backend-builder

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 多阶段构建 - 前端
FROM node:22-slim as frontend-builder

WORKDIR /app/frontend

# 复制前端代码
COPY frontend/package*.json ./
RUN npm ci

COPY frontend .
RUN npm run build

# 最终镜像
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制 Python 依赖
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# 复制后端代码
COPY backend ./backend
COPY soul_mate ./soul_mate
COPY main.py .
COPY requirements.txt .

# 复制前端构建结果
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# 暴露端口
EXPOSE 8010 3008

# 环境变量
ENV FLASK_ENV=production
ENV FLASK_PORT=8010

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8010/health || exit 1

# 启动脚本
CMD ["python", "backend/app.py"]
```

### 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  soul-mate:
    build: .
    ports:
      - "8010:8010"
      - "3008:3008"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_API_BASE=${OPENAI_API_BASE}
      - OPENAI_MODEL=${OPENAI_MODEL}
      - FLASK_ENV=production
      - FLASK_PORT=8010
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### 构建和运行 Docker 镜像

```bash
# 构建镜像
docker build -t soul-mate:latest .

# 运行容器
docker run -d \
  -p 8010:8010 \
  -p 3008:3008 \
  -e OPENAI_API_KEY=sk-your-key \
  -e OPENAI_API_BASE=https://api.haihub.cn/v1/ \
  -e OPENAI_MODEL=Kimi-K2-Instruct \
  -v $(pwd)/data:/app/data \
  --name soul-mate \
  soul-mate:latest

# 或使用 docker-compose
docker-compose up -d
```

---

## 🚀 云服务器部署

### 腾讯云 / 阿里云 / 华为云

#### 1. 购买云服务器

- 推荐配置：2核 4GB 内存，50GB 存储
- 操作系统：Ubuntu 20.04 LTS 或 CentOS 8

#### 2. 连接到服务器

```bash
ssh -i your-key.pem ubuntu@your-server-ip
```

#### 3. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# 安装其他工具
sudo apt install -y git curl wget
```

#### 4. 部署项目

```bash
# 克隆或下载项目
git clone https://github.com/SnowCharon/soul-mate-agent.git
cd soul-mate-agent

# 或解压压缩包
tar -xzf soul-mate-full.tar.gz
cd soul-mate-full

# 配置环境
cp backend/.env.example .env
nano .env  # 编辑添加 API Key

# 启动服务
chmod +x start.sh
./start.sh all
```

#### 5. 配置防火墙

```bash
# 开放端口
sudo ufw allow 8010/tcp
sudo ufw allow 3008/tcp
sudo ufw enable
```

#### 6. 配置反向代理（可选）

使用 Nginx 作为反向代理：

```bash
sudo apt install -y nginx
```

创建 `/etc/nginx/sites-available/soul-mate`：

```nginx
upstream backend {
    server localhost:8010;
}

upstream frontend {
    server localhost:3008;
}

server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/soul-mate /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 使用 Systemd 管理服务

### 创建 Systemd 服务文件

创建 `/etc/systemd/system/soul-mate.service`：

```ini
[Unit]
Description=Soul Mate Agent Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/soul-mate-full
ExecStart=/home/ubuntu/soul-mate-full/start.sh all
Restart=on-failure
RestartSec=10
Environment="OPENAI_API_KEY=sk-your-key"
Environment="OPENAI_API_BASE=https://api.haihub.cn/v1/"
Environment="OPENAI_MODEL=Kimi-K2-Instruct"

[Install]
WantedBy=multi-user.target
```

### 管理服务

```bash
# 启用服务
sudo systemctl enable soul-mate

# 启动服务
sudo systemctl start soul-mate

# 查看状态
sudo systemctl status soul-mate

# 查看日志
sudo journalctl -u soul-mate -f

# 停止服务
sudo systemctl stop soul-mate

# 重启服务
sudo systemctl restart soul-mate
```

---

## 📊 监控和日志

### 查看服务日志

```bash
# 查看实时日志
tail -f /var/log/soul-mate.log

# 或使用 journalctl
sudo journalctl -u soul-mate -f
```

### 性能监控

```bash
# 监控进程
top -p $(pgrep -f "python backend/app.py")

# 监控端口
netstat -tulpn | grep 8010
netstat -tulpn | grep 3008
```

---

## 🔒 安全建议

### 1. 环境变量管理

- 不要在代码中硬编码 API Key
- 使用 `.env` 文件管理敏感信息
- 在生产环境中使用密钥管理服务（如 AWS Secrets Manager）

### 2. HTTPS 配置

```bash
# 使用 Let's Encrypt 获取免费 SSL 证书
sudo apt install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

### 3. 速率限制

在 Nginx 中配置速率限制：

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
    proxy_pass http://backend;
}
```

### 4. 定期备份

```bash
# 备份数据目录
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# 定期备份（使用 cron）
0 2 * * * cd /home/ubuntu/soul-mate-full && tar -czf backup-$(date +\%Y\%m\%d).tar.gz data/
```

---

## 🚨 故障恢复

### 服务崩溃

```bash
# 检查进程
ps aux | grep python

# 重启服务
./start.sh all

# 或使用 systemd
sudo systemctl restart soul-mate
```

### 数据恢复

```bash
# 从备份恢复
tar -xzf backup-20240116.tar.gz
```

---

## 📈 性能优化

### 1. 使用生产级 WSGI 服务器

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动
gunicorn -w 4 -b 0.0.0.0:8010 backend.app:app
```

### 2. 前端静态文件优化

- 启用 Gzip 压缩
- 使用 CDN 分发静态资源
- 配置缓存策略

### 3. 数据库优化

- 添加数据库索引
- 定期清理日志
- 优化查询

---

## 📞 获取帮助

如遇到部署问题：

1. 查看日志：`journalctl -u soul-mate -f`
2. 检查端口：`netstat -tulpn | grep 8010`
3. 测试 API：`curl http://localhost:8010/health`
4. 查看项目文档：[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

---

**祝部署顺利！** 🚀
