# Day 38 课程：Docker 进阶 + 微服务

## 第一部分：Docker 进阶

### 1.1 网络

`ash
# 创建自定义网络
docker network create mynet

# 容器加入网络
docker run -d --name api --network mynet myapi
docker run -d --name db --network mynet postgres

# 容器间通过服务名通信
# api 容器中可以访问 db:5432
`

### 1.2 卷挂载

`ash
# 匿名卷
docker run -v /app/data myapp

# 命名卷
docker volume create mydata
docker run -v mydata:/app/data myapp

# 绑定挂载（开发用）
docker run -v C:\Users\lk\Documents\Codex\2026-09-03\zai/src:/app/src myapp

# docker-compose 中
volumes:
  - ./src:/app/src          # 绑定挂载
  - pgdata:/var/lib/postgresql/data  # 命名卷
`

### 1.3 资源限制

`ash
# 限制内存和 CPU
docker run -m 512m --cpus 1.5 myapp

# docker-compose 中
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
`

---

## 第二部分：微服务架构

### 2.1 核心概念

``
单体应用（Monolith）：
┌──────────────────────┐
│  用户 + 订单 + 支付   │
│  + 库存 + 通知 + ... │
│    全在一个进程里      │
└──────────────────────┘

微服务（Microservices）：
┌──────┐  ┌──────┐  ┌──────┐
│ 用户  │  │ 订单  │  │ 支付  │
│ 服务  │  │ 服务  │  │ 服务  │
└──┬───┘  └──┬───┘  └──┬───┘
   │         │         │
   └──── API Gateway ──┘
``

### 2.2 服务间通信

# 同步：HTTP REST / gRPC
# 异步：消息队列（RabbitMQ / Redis Stream / Kafka）

# HTTP 调用示例
import httpx

async def get_user(user_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://user-service:8001/users/{user_id}")
        resp.raise_for_status()
        return resp.json()

---

## 第三部分：微服务 Docker Compose

`yaml
version: "3.8"

services:
  gateway:
    build: ./gateway
    ports:
      - "8000:8000"
    depends_on:
      - user-service
      - order-service

  user-service:
    build: ./user-service
    environment:
      - DB_URL=postgresql://user:pass@user-db:5432/users
    depends_on:
      - user-db

  order-service:
    build: ./order-service
    environment:
      - DB_URL=postgresql://user:pass@order-db:5432/orders
      - USER_SERVICE_URL=http://user-service:8001
    depends_on:
      - order-db

  user-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: users
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - user-db-data:/var/lib/postgresql/data

  order-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: orders
    volumes:
      - order-db-data:/var/lib/postgresql/data

volumes:
  user-db-data:
  order-db-data:
`

---

## 常见错误
1. 服务间直接用 localhost -> Docker 中 localhost 是容器自己
2. 没有 depends_on -> 服务启动顺序不确定
3. 数据库密码硬编码 -> 安全风险
4. 没有健康检查 -> 服务没准备好就开始通信

## 动手练习
1. 用 docker-compose 创建多网络
2. 拆分一个单体应用为 2 个微服务
3. 实现服务间 HTTP 通信
4. 配置健康检查和依赖顺序
