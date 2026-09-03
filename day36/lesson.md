# Day 36 课程：数据库进阶

## 第一部分：关系类型

### 1.1 一对一

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    profile = relationship('Profile', uselist=False, back_populates='user')

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    bio = Column(String(500))
    user = relationship('User', back_populates='profile')

### 1.2 一对多

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    books = relationship('Book', back_populates='author', cascade='all, delete-orphan')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books')

### 1.3 多对多

from sqlalchemy import Table

# 关联表
student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id')),
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    courses = relationship('Course', secondary=student_course, back_populates='students')

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    students = relationship('Student', secondary=student_course, back_populates='courses')

---

## 第二部分：事务和连接池

### 2.1 事务

from sqlalchemy.orm import Session

def transfer_money(session: Session, from_id: int, to_id: int, amount: float):
    try:
        from_user = session.query(User).get(from_id)
        to_user = session.query(User).get(to_id)
        from_user.balance -= amount
        to_user.balance += amount
        session.commit()
    except Exception:
        session.rollback()
        raise

### 2.2 连接池配置

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=20,           # 最大连接数
    max_overflow=10,        # 超出池大小的最大连接
    pool_timeout=30,        # 获取连接超时
    pool_recycle=3600,      # 连接回收时间
    pool_pre_ping=True,     # 使用前检查连接
)

---

## 第三部分：Redis 基础

### 3.1 安装

pip install redis

### 3.2 基本操作

import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# String
r.set('name', 'Alice')
r.get('name')  # 'Alice'
r.setex('token', 3600, 'abc123')  # 1小时过期

# Hash
r.hset('user:1', mapping={'name': 'Alice', 'age': '30'})
r.hget('user:1', 'name')  # 'Alice'
r.hgetall('user:1')

# List
r.lpush('queue', 'task1', 'task2', 'task3')
r.rpop('queue')  # 'task1'
r.llen('queue')

# Set
r.sadd('tags', 'python', 'fastapi', 'redis')
r.smembers('tags')
r.sismember('tags', 'python')  # True

# Sorted Set
r.zadd('scores', {'alice': 100, 'bob': 85})
r.zrevrange('scores', 0, -1)  # 按分数倒序

### 3.3 缓存模式

def get_user(user_id: int) -> dict:
    cache_key = f"user:{user_id}"
    
    # 1. 尝试从缓存读取
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # 2. 缓存未命中，查数据库
    user = session.query(User).get(user_id)
    if not user:
        return None
    
    data = {"id": user.id, "name": user.username}
    
    # 3. 写入缓存
    r.setex(cache_key, 300, json.dumps(data))  # 5分钟过期
    
    return data

---

## 常见错误
1. 忘记 cascade -> 删除父记录报 IntegrityError
2. 多对多关系忘记 secondary -> 查询失败
3. 事务中抛异常没 rollback -> 后续操作失败
4. 连接池耗尽 -> 应用卡死
5. Redis 没设过期 -> 内存无限增长

## 动手练习
1. 实现多对多关系（学生-课程）
2. 用事务实现转账
3. 用 Redis 实现缓存层
4. 用 Redis 实现简单消息队列
