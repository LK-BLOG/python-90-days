# Day 35 课程：SQL & SQLAlchemy

## 第一部分：SQL 基础

### 1.1 DDL - 数据定义

-- 创建表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 修改表
ALTER TABLE users ADD COLUMN bio TEXT;
DROP TABLE users;

### 1.2 DML - 数据操作

-- 插入
INSERT INTO users (username, email, age) VALUES ('alice', 'alice@test.com', 30);

-- 查询
SELECT * FROM users WHERE age > 25 ORDER BY username LIMIT 10;

-- 更新
UPDATE users SET age = 31 WHERE username = 'alice';

-- 删除
DELETE FROM users WHERE id = 1;

-- JOIN
SELECT u.username, p.title
FROM users u
JOIN posts p ON u.id = p.author_id
WHERE u.age > 25;

### 1.3 聚合

SELECT COUNT(*) as total, AVG(age) as avg_age
FROM users
GROUP BY department
HAVING COUNT(*) > 5;

---

## 第二部分：SQLAlchemy ORM

### 2.1 安装

pip install sqlalchemy

### 2.2 模型定义

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///app.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000))
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")

# 创建表
Base.metadata.create_all(engine)

### 2.3 CRUD 操作

session = SessionLocal()

# 创建
new_user = User(username="alice", email="alice@test.com", age=30)
session.add(new_user)
session.commit()
session.refresh(new_user)  # 刷新获取 id

# 查询
user = session.query(User).filter_by(username="alice").first()
users = session.query(User).filter(User.age > 25).all()

# 更新
user.age = 31
session.commit()

# 删除
session.delete(user)
session.commit()

# 关闭
session.close()

### 2.4 常用查询

# 排序
session.query(User).order_by(User.age.desc()).all()

# 分页
session.query(User).offset(0).limit(10).all()

# 计数
session.query(User).filter(User.age > 25).count()

# exists
session.query(session.query(User).filter_by(username="alice").exists()).scalar()

# 关联查询
user = session.query(User).options(
    joinedload(User.posts)
).first()

### 2.5 避免 N+1 问题

# 错误：每个 post 会额外查询 author
posts = session.query(Post).all()
for post in posts:
    print(post.author.username)  # N+1!

# 正确：使用 joinedload 一次查询
from sqlalchemy.orm import joinedload
posts = session.query(Post).options(joinedload(Post.author)).all()
for post in posts:
    print(post.author.username)  # 不会额外查询

---

## 第三部分：Alembic 数据库迁移

### 3.1 初始化

pip install alembic
alembic init alembic

### 3.2 配置 (alembic.ini)

sqlalchemy.url = sqlite:///app.db

### 3.3 生成迁移

alembic revision --autogenerate -m "create users table"

### 3.4 执行迁移

alembic upgrade head      # 升级到最新
alembic downgrade -1      # 回退一步
alembic history           # 查看迁移历史

---

## 常见错误
1. 忘记 session.close() -> 连接泄漏
2. N+1 查询 -> 性能灾难
3. 没有 cascade -> 删除父记录报错
4. session 在函数间传递 -> 线程安全问题
5. 忘记 Base.metadata.create_all -> 表不存在

## 动手练习
1. 用 SQLAlchemy 创建 User 和 Post 模型
2. 实现基本 CRUD 操作
3. 使用 joinedload 解决 N+1
4. 初始化 Alembic 并生成迁移
