# 实战04：打包发布

阅读时间：35分钟
难度等级：⭐⭐ 进阶
你将收获：Docker 化、CI/CD、PyPI 发布

<br/>

***

<br/>

## 从开发到生产

**上篇回顾：**

```
✅ 实战03：引入 MCP
   - GitHub API 集成
   - GitLab API 集成
   - 自动同步仓库信息
   - 定时任务
```

**当前状态：**

```
开发环境
  └─ 本地运行（uvicorn）
  └─ SQLite 数据库
  └─ 手动启动
  └─ 无 MCP 配置
```

**生产环境需求：**

```
生产环境
  └─ Docker 容器化
  └─ PostgreSQL 数据库
  └─ 自动化部署
  └─ 环境变量管理
  └─ CI/CD 流水线
  └─ 监控和日志
```

**本篇目标：**

```
把 codestats-api 部署到生产环境

步骤：
✅ Docker 化（容器部署）
✅ 环境变量配置（MCP Token）
✅ CI/CD 自动化（GitHub Actions）
✅ 发布 CLI 到 PyPI
✅ 部署文档
```

**学习要点：**

- ✅ Docker 和 Docker Compose
- ✅ 环境变量管理
- ✅ CI/CD 流水线
- ✅ PyPI 发布流程
- ✅ 生产环境最佳实践

<br/>

***

<br/>

## 一、Docker 化

### 1.1 创建 Dockerfile

**创建 `Dockerfile`：**

```dockerfile
# 使用 Python 3.11 官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

<br/>

### 1.2 创建 Docker Compose

**创建 `docker-compose.yml`：**

```yaml
version: '3.8'

services:
  # API 服务
  api:
    build: .
    container_name: codestats-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://codestats:password@db:5432/codestats
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - GITLAB_TOKEN=${GITLAB_TOKEN}
      - GITLAB_URL=${GITLAB_URL:-https://gitlab.com/api/v4}
    depends_on:
      - db
      - redis
    volumes:
      - ./repos:/app/repos  # 挂载仓库目录
    networks:
      - codestats-network

  # PostgreSQL 数据库
  db:
    image: postgres:15-alpine
    container_name: codestats-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=codestats
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=codestats
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - codestats-network

  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: codestats-redis
    restart: unless-stopped
    networks:
      - codestats-network

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    container_name: codestats-nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
    networks:
      - codestats-network

volumes:
  postgres_data:

networks:
  codestats-network:
    driver: bridge
```

<br/>

### 1.3 创建环境变量文件

**创建 `.env.example`：**

```bash
# 应用配置
APP_NAME=CodeStats API
APP_VERSION=0.1.0
DEBUG=false

# 数据库配置
DATABASE_URL=postgresql://codestats:password@db:5432/codestats

# MCP 配置（必需）
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
GITLAB_URL=https://gitlab.com/api/v4

# Redis 配置
REDIS_URL=redis://redis:6379/0

# 安全配置
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://your-domain.com
```

**创建 `.env`（本地开发）：**

```bash
# 复制示例文件
cp .env.example .env

# 编辑并填入真实 token
vim .env
```

<br/>

***

<br/>

## 二、环境配置

### 2.1 更新配置文件

**更新 `app/config.py`：**

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "CodeStats API"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # 数据库配置
    database_url: str = "sqlite:///./codestats.db"
    
    # MCP 配置
    github_token: str = ""
    gitlab_token: str = ""
    gitlab_url: str = "https://gitlab.com/api/v4"
    
    # Redis 配置
    redis_url: str = "redis://localhost:6379/0"
    
    # API 配置
    api_prefix: str = "/api"
    
    # 安全配置
    secret_key: str = "dev-secret-key"
    allowed_origins: str = "*"
    
    @property
    def cors_origins(self) -> List[str]:
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

<br/>

### 2.2 更新数据库配置

**更新 `app/database.py`：**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 创建引擎（支持 PostgreSQL 和 SQLite）
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # 检查连接是否有效
    pool_size=10,
    max_overflow=20,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

<br/>

***

<br/>

## 三、CI/CD 自动化

### 3.1 创建 GitHub Actions

**创建 `.github/workflows/ci.yml`：**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # 测试
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  # 构建 Docker 镜像
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          yourusername/codestats-api:latest
          yourusername/codestats-api:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  # 部署
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_SSH_KEY }}
        script: |
          cd /opt/codestats
          docker-compose pull
          docker-compose up -d
          docker image prune -f
```

<br/>

***

<br/>

## 四、PyPI 发布（CLI 工具）

### 4.1 准备发布

**更新 `pyproject.toml`：**

```toml
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "codestats"
version = "0.1.0"
description = "Code statistics CLI tool with MCP integration"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
homepage = "https://github.com/yourusername/codestats"
repository = "https://github.com/yourusername/codestats"
keywords = ["code", "statistics", "cli", "mcp", "github"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

[tool.poetry.dependencies]
python = "^3.9"
click = "^8.1.0"
rich = "^13.0.0"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"

[tool.poetry.scripts]
codestats = "codestats.cli:main"
```

<br/>

### 4.2 发布到 PyPI

**使用 poetry 发布：**

```bash
# 1. 构建
poetry build

# 2. 发布到 TestPyPI（测试）
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi

# 3. 测试安装
pip install --index-url https://test.pypi.org/simple/ codestats

# 4. 发布到 PyPI（正式）
poetry publish

# 5. 验证发布
pip install codestats
codestats --help
```

<br/>

***

<br/>

## 五、部署文档

### 5.1 创建部署文档

**创建 `DEPLOYMENT.md` 文件，内容包括：**

<br/>

**前置要求：**

```
- Docker 和 Docker Compose
- GitHub Personal Access Token
- GitLab Personal Access Token（可选）
```

<br/>

**快速部署步骤：**

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/codestats.git
cd codestats

# 2. 配置环境变量
cp .env.example .env
vim .env

# 必填项：
# - GITHUB_TOKEN: GitHub Token
# - SECRET_KEY: 随机密钥

# 3. 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 检查状态
curl http://localhost/health
```

<br/>

**访问服务：**

```
- API 文档: http://localhost/docs
- ReDoc: http://localhost/redoc
- 健康检查: http://localhost/health
```

<br/>

**生产环境配置 - 使用 HTTPS：**

```bash
# 1. 获取 SSL 证书（Let's Encrypt）
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

```nginx
# 2. 更新 nginx.conf
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://api:8000;
    }
}
```

<br/>

**数据库备份：**

```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec codestats-db pg_dump -U codestats codestats > backup_$DATE.sql
EOF

chmod +x backup.sh

# 添加到 crontab（每天凌晨 2 点备份）
crontab -e
# 添加：0 2 * * * /opt/codestats/backup.sh
```

<br/>

**监控 - 使用 Prometheus + Grafana：**

```yaml
# 添加到 docker-compose.yml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

访问 Grafana: http://localhost:3000

<br/>

**故障排查：**

```bash
# 查看日志
docker-compose logs api          # API 日志
docker-compose logs db           # 数据库日志
docker-compose logs              # 所有服务日志

# 重启服务
docker-compose restart api       # 重启单个服务
docker-compose restart           # 重启所有服务

# 更新服务
docker-compose pull              # 拉取最新镜像
docker-compose up -d             # 重新创建容器
```

<br/>

***

<br/>

## 六、测试部署

### 6.1 本地测试

```bash
# 1. 构建镜像
docker-compose build

# 2. 启动服务
docker-compose up -d

# 3. 检查状态
docker-compose ps

# 输出：
# NAME                COMMAND                  SERVICE             STATUS
# codestats-api       "uvicorn app.main:ap…"   api                 running
# codestats-db        "docker-entrypoint.s…"   db                  running
# codestats-redis     "docker-entrypoint.s…"   redis               running
# codestats-nginx     "/docker-entrypoint.…"   nginx               running

# 4. 测试 API
curl http://localhost:8000/
curl http://localhost:8000/health

# 5. 测试 GitHub 集成
curl http://localhost:8000/api/github/repos

# 6. 停止服务
docker-compose down
```

<br/>

### 6.2 生产环境测试

```bash
# 1. SSH 到服务器
ssh user@your-server.com

# 2. 进入项目目录
cd /opt/codestats

# 3. 拉取最新代码
git pull

# 4. 更新环境变量
vim .env

# 5. 重启服务
docker-compose pull
docker-compose up -d

# 6. 检查健康状态
curl http://localhost:8000/health
```

<br/>

***

<br/>

## 七、总结

### 7.1 完成的工作

**容器化：**

```
✅ Dockerfile（API 服务）
✅ Docker Compose（完整栈）
✅ 环境变量配置
✅ 数据持久化
```

**CI/CD：**

```
✅ 自动测试
✅ 自动构建镜像
✅ 自动部署
✅ 代码覆盖率
```

**发布：**

```
✅ CLI 发布到 PyPI
✅ API 发布到 Docker Hub
✅ 完整的部署文档
```

<br/>

### 7.2 部署架构

```
┌─────────────────────────────────────┐
│         Nginx (反向代理)             │
│         Let's Encrypt (HTTPS)       │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐    ┌──────▼─────┐
│  API 服务  │    │   Redis    │
│  (Uvicorn) │    │  (缓存)    │
└───┬────────┘    └────────────┘
    │
┌───▼────────┐
│ PostgreSQL │
│  (数据库)  │
└────────────┘

外部服务（MCP）：
  - GitHub API
  - GitLab API
```

<br/>

### 7.3 下一步

**监控和日志：**

```
📋 Prometheus + Grafana
📋 ELK Stack（日志）
📋 告警系统
```

**性能优化：**

```
📋 负载均衡
📋 数据库连接池
📋 CDN 加速
```

**为下一篇做准备：**

```
🔄 实战05：设计全栈应用架构
   - 前后端分离架构
   - 用户认证系统
   - 权限管理
   - API 设计
```

<br/>

***

<br/>

## 八、常见问题

### Q1: 如何更新 GitHub Token？

```bash
# 1. 编辑 .env 文件
vim .env

# 2. 重启 API 服务
docker-compose restart api
```

### Q2: 数据库迁移失败怎么办？

```bash
# 1. 进入容器
docker-compose exec api bash

# 2. 运行迁移
alembic upgrade head

# 3. 检查日志
alembic current
```

### Q3: 如何查看容器日志？

```bash
# 实时日志
docker-compose logs -f api

# 最近 100 行
docker-compose logs --tail=100 api
```

### Q4: 如何备份数据？

```bash
# 备份 PostgreSQL
docker exec codestats-db pg_dump -U codestats codestats > backup.sql

# 恢复
cat backup.sql | docker exec -i codestats-db psql -U codestats codestats
```

<br/>

***

<br/>

**系列导航**

• 上一篇：实战03：引入 MCP
• 下一篇：实战05：设计全栈应用架构

<br/>

***

本文是《AI Coding 从入门到精通》系列第19篇  
作者：生活助理 | 发布时间：2026-04-06

**从开发到生产，自动化部署！** 🚀
