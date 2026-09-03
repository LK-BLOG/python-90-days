# Day 37 课程：Docker 基础

## 第一部分：Docker 概念

### 1.1 核心概念

- 镜像（Image）：只读模板，类似类
- 容器（Container）：镜像的运行实例，类似对象
- 仓库（Registry）：存储镜像的地方，如 Docker Hub
- Dockerfile：构建镜像的脚本

### 1.2 常用命令

# 镜像操作
docker images                    # 列出本地镜像
docker pull python:3.11           # 拉取镜像
docker build -t myapp:1.0 .       # 构建镜像
docker rmi myapp:1.0              # 删除镜像

# 容器操作
docker run -d -p 8000:8000 myapp  # 后台运行，映射端口
docker ps                         # 查看运行中的容器
docker ps -a                      # 查看所有容器
docker stop <container_id>        # 停止容器
docker logs <container_id>        # 查看日志
docker exec -it <id> /bin/bash    # 进入容器

# 清理
docker system prune -a            # 清理未使用的资源

---

## 第二部分：Dockerfile

### 2.1 Python 应用 Dockerfile

`dockerfile
# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 复制依赖文件（利用缓存层）
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
`

### 2.2 .dockerignore

`
__pycache__
*.py[cod]
.venv
.git
.env
.pytest_cache
*.md
.vscode
.idea
`

### 2.3 构建和运行

`ash
# 构建
docker build -t my-api:1.0 .

# 运行
docker run -d -p 8000:8000 --name api my-api:1.0

# 查看日志
docker logs -f api

# 停止并删除
docker stop api && docker rm api
`

---

## 第三部分：docker-compose

### 3.1 docker-compose.yml

`yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
`

### 3.2 Compose 命令

`ash
docker-compose up -d          # 后台启动所有服务
docker-compose down            # 停止并删除
docker-compose logs -f api     # 查看某个服务日志
docker-compose exec api bash   # 进入某个服务容器
docker-compose build           # 重新构建
docker-compose ps              # 查看服务状态
`

---

## 常见错误
1. 不用 .dockerignore -> 构建慢，镜像大
2. 先 COPY 代码再 pip install -> 缓存层失效
3. 用 root 用户运行 -> 安全风险
4. 镜像里放密钥 -> 泄露
5. 没有 HEALTHCHECK -> 不知道服务是否正常

## 动手练习
1. 为一个 FastAPI 应用编写 Dockerfile
2. 用 docker-compose 编排 API + 数据库 + Redis
3. 使用多阶段构建减小镜像体积
