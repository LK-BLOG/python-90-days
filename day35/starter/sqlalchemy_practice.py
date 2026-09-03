# Day 35 SQLAlchemy 骨架 - TODO: 完善
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///myapp.db')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    # TODO: 添加 username, email, age 字段
    # TODO: 添加 created_at 字段
    # TODO: 添加与 Post 的关系

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    # TODO: 添加 title, content 字段
    # TODO: 添加 author_id 外键
    # TODO: 添加与 User 的关系

# TODO: 创建表
# TODO: 实现 CRUD 函数
# TODO: 实现查询函数（过滤、排序、分页）
