# Day 36 数据库进阶骨架
# TODO: 多对多关系 + 事务 + Redis
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# TODO: 定义 Student, Course, 多对多关联表
# TODO: 实现事务转账函数
# TODO: 实现 Redis 缓存层
