# Day 51 课程：中间件、后台任务、缓存和测试

## 第一部分：中间件

### 1.1 FastAPI中间件
`python
import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logging.info(f"{request.method} {request.url.path} {response.status_code} {duration:.3f}s")
    return response

# 请求ID中间件
import uuid

@app.middleware("http")
async def request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# 错误处理中间件
@app.middleware("http")
async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.exception(f"Unhandled error: {e}")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
`

---

## 第二部分：Celery后台任务

### 2.1 基本使用
`python
from celery import Celery

celery_app = Celery("worker", broker="redis://localhost:6379/1")

@celery_app.task
def send_email(to: str, subject: str, body: str) -> bool:
    # 模拟发送邮件
    print(f"Sending email to {to}: {subject}")
    return True

@celery_app.task
def generate_report(report_type: str, params: dict) -> str:
    # 模拟生成报告
    print(f"Generating {report_type} report...")
    return f"/reports/{report_type}_latest.pdf"

# 在API中调用
@app.post("/articles/")
async def create_article(article_in: ArticleCreate, ...):
    article = ...
    # 异步通知订阅者
    send_email.delay("subscriber@example.com", "New Article", article.title)
    return article
`

### 2.2 任务链
`python
from celery import chain, group

# 链式调用
workflow = chain(
    extract_data.s(url),
    transform_data.s(),
    load_to_db.s(),
)
result = workflow.apply_async()

# 并行执行
parallel = group(
    generate_report.s("sales", {"month": "2024-01"}),
    generate_report.s("users", {"month": "2024-01"}),
    generate_report.s("inventory", {"month": "2024-01"}),
)
results = parallel.apply_async()
`

---

## 第三部分：缓存层

### 3.1 FastAPI + Redis缓存
`python
import json
import redis

redis_client = redis.from_url("redis://localhost:6379/0")

def cache_response(ttl: int = 300):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

@router.get("/articles/")
@cache_response(ttl=60)
async def list_articles(...):
    ...
`

---

## 第四部分：测试

### 4.1 FastAPI测试
`python
from httpx import AsyncClient
import pytest

@pytest.fixture
async def client():
    from app.main import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_article(client):
    # 注册用户
    resp = await client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123"
    })
    assert resp.status_code == 201

    # 登录
    resp = await client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "test123"
    })
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 创建文章
    resp = await client.post("/api/v1/articles/", json={
        "title": "Test Article",
        "content": "Hello World"
    }, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["title"] == "Test Article"
`

### 4.2 集成测试
`python
@pytest.mark.asyncio
async def test_full_article_lifecycle(client, auth_headers):
    # 创建
    resp = await client.post("/api/v1/articles/", json={
        "title": "Lifecycle Test", "content": "Content"
    }, headers=auth_headers)
    article_id = resp.json()["id"]

    # 读取
    resp = await client.get(f"/api/v1/articles/{article_id}")
    assert resp.status_code == 200

    # 更新
    resp = await client.put(f"/api/v1/articles/{article_id}", json={
        "title": "Updated"
    }, headers=auth_headers)
    assert resp.json()["title"] == "Updated"

    # 删除
    resp = await client.delete(f"/api/v1/articles/{article_id}", headers=auth_headers)
    assert resp.status_code == 204
`

---

## 本课总结

| 模块 | 关键点 |
|------|--------|
| 中间件 | 日志/计时/错误处理/请求ID |
| Celery | 异步任务/任务链/定时任务 |
| 缓存 | Redis缓存/缓存装饰器 |
| 测试 | httpx.AsyncClient/pytest |
