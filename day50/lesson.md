# Day 50 课程：REST API 架构设计

## 第一部分：API架构设计

### 1.1 项目概览：博客/论坛API
`
功能：
- 用户注册/登录
- 文章CRUD
- 评论CRUD
- 标签系统
- 分页、过滤、搜索
- 权限控制（作者只能编辑自己的文章）
`

### 1.2 RESTful API设计
`
GET    /api/v1/articles          # 获取文章列表
POST   /api/v1/articles          # 创建文章
GET    /api/v1/articles/{id}     # 获取文章详情
PUT    /api/v1/articles/{id}     # 更新文章
DELETE /api/v1/articles/{id}     # 删除文章
GET    /api/v1/articles/{id}/comments  # 获取评论
POST   /api/v1/articles/{id}/comments  # 添加评论
POST   /api/v1/auth/register     # 注册
POST   /api/v1/auth/login        # 登录
`

### 1.3 项目结构
`
blog_api/
├── pyproject.toml
├── alembic/              # 数据库迁移
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── config.py         # 配置
│   ├── database.py       # 数据库连接
│   ├── models/           # SQLAlchemy模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── article.py
│   │   └── comment.py
│   ├── schemas/          # Pydantic schema
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── article.py
│   │   └── comment.py
│   ├── api/              # 路由
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── articles.py
│   │   │   ├── comments.py
│   │   │   └── auth.py
│   ├── services/         # 业务逻辑
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── article_service.py
│   ├── repositories/     # 数据访问
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   └── article_repo.py
│   ├── middleware/       # 中间件
│   │   └── __init__.py
│   └── utils/            # 工具
│       ├── __init__.py
│       ├── auth.py       # JWT认证
│       └── pagination.py
├── tests/
└── docker-compose.yml
`

---

## 第二部分：数据模型

### 2.1 SQLAlchemy模型
`python
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

# 文章-标签多对多
article_tags = Table(
    "article_tags", Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    articles = relationship("Article", back_populates="author")

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article")
    tags = relationship("Tag", secondary=article_tags)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    article = relationship("Article", back_populates="comments")
`

---

## 第三部分：CRUD路由

### 3.1 文章路由
`python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/v1/articles", tags=["articles"])

@router.get("/")
async def list_articles(
    page: int = 1,
    page_size: int = 20,
    tag: str | None = None,
    author: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Article)
    if tag:
        query = query.filter(Article.tags.any(Tag.name == tag))
    if author:
        query = query.filter(Article.author.has(username=author))
    
    # 分页
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    query = query.offset((page - 1) * page_size).limit(page_size)
    articles = await db.scalars(query)
    
    return {
        "items": articles,
        "total": total,
        "page": page,
        "page_size": page_size,
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article(
    article_in: ArticleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    article = Article(**article_in.model_dump(), author_id=current_user.id)
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article
`

### 3.2 权限控制
`python
from fastapi import Depends, HTTPException, status

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (jwt.JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def require_author(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Article:
    article = await db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not the author")
    return article
`

---

## 第四部分：分页

### 4.1 游标分页
`python
@router.get("/")
async def list_articles_cursor(
    cursor: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    query = select(Article).order_by(Article.id.desc())
    if cursor:
        cursor_id = decode_cursor(cursor)
        query = query.where(Article.id < cursor_id)
    
    query = query.limit(limit + 1)  # 多查一个判断是否有下一页
    articles = await db.scalars(query)
    
    has_next = len(articles) > limit
    if has_next:
        articles = articles[:limit]
    
    next_cursor = encode_cursor(articles[-1].id) if has_next and articles else None
    
    return {
        "items": articles,
        "next_cursor": next_cursor,
    }
`

---

## 本课总结

| 模块 | 关键点 |
|------|--------|
| 数据模型 | SQLAlchemy ORM + 多对多关系 |
| 路由 | FastAPI Router + 资源式URL |
| 认证 | JWT + Depends注入 |
| 权限 | 作者只能编辑自己的内容 |
| 分页 | offset分页 / 游标分页 |
