# Day 52 课程：文档、性能、安全和部署

## 第一部分：API文档

### 1.1 FastAPI自动生成文档
`python
app = FastAPI(
    title="Blog API",
    description="A RESTful blog API",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
)

# 详细响应模型
@router.get("/articles/{id}", response_model=ArticleResponse, summary="Get article")
async def get_article(id: int):
    \"\"\"获取文章详情。

    - **id**: 文章ID
    - 返回文章的完整内容、作者信息和标签
    \"\"\"
    ...
`

### 1.2 OpenAPI配置
`python
openapi_tags = [
    {"name": "auth", "description": "用户认证"},
    {"name": "articles", "description": "文章CRUD"},
    {"name": "comments", "description": "评论CRUD"},
]

app = FastAPI(openapi_tags=openapi_tags)
`

---

## 第二部分：性能优化

### 2.1 查询优化
`python
# N+1问题
# 坏：每次访问author都发一次查询
articles = await db.scalars(select(Article))
for article in articles:
    author = await db.get(User, article.author_id)  # N+1!

# 好：joinedload一次查出
from sqlalchemy.orm import selectinload
query = select(Article).options(selectinload(Article.author))
articles = await db.scalars(query)
`

### 2.2 数据库索引
`python
class Article(Base):
    title = Column(String(200), index=True)  # 搜索优化
    created_at = Column(DateTime, index=True)  # 排序优化
    author_id = Column(Integer, ForeignKey("users.id"), index=True)  # 关联查询
`

### 2.3 异步和并发
`python
import asyncio
import httpx

async def get_article_with_related(article_id: int):
    """并行获取相关数据"""
    async with httpx.AsyncClient() as client:
        # 并行请求
        article_task, comments_task, related_task = await asyncio.gather(
            db.get(Article, article_id),
            db.scalars(select(Comment).where(Comment.article_id == article_id)),
            get_related_articles(article_id),
        )
    return article_task, comments_task, related_task
`

---

## 第三部分：安全加固

### 3.1 安全头
`python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
`

### 3.2 CORS配置
`python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],  # 不要用 * in prod
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=600,
)
`

### 3.3 输入验证
`python
from pydantic import Field, field_validator

class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, pattern=r"^[a-zA-Z0-9\s\-_]+$")
    content: str = Field(..., min_length=1, max_length=50000)

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        # 基本XSS防护
        return v.replace("<script>", "").replace("</script>", "")
`

### 3.4 速率限制
`python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@router.get("/articles/")
@limiter.limit("30/minute")
async def list_articles(request: Request):
    ...
`

---

## 第四部分：Docker + CI/CD

### 4.1 Dockerfile
`dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
`

### 4.2 docker-compose.yml
`yaml
version: "3.8"
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://postgres:password@db/blog
      - REDIS_URL=redis://redis:6379
    depends_on: [db, redis]

  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=blog
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine

  celery:
    build: .
    command: celery -A app.celery_app worker
    depends_on: [db, redis]

volumes:
  pgdata:
`

### 4.3 GitHub Actions
`yaml
name: CI/CD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v4

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: echo "Deploy your app here"
`

---

## 本课总结

| 模块 | 关键点 |
|------|--------|
| 文档 | OpenAPI/Swagger/ReDoc |
| 性能 | 避免N+1/索引/异步并发 |
| 安全 | 安全头/CORS/输入验证/速率限制 |
| 部署 | Docker/CI-CD/GitHub Actions |
