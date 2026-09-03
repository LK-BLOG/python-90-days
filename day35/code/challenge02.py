# Challenge 02: SQLAlchemy 模型定义
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# TODO: 定义 User 模型
# TODO: 定义 Post 模型（有外键到 User）
# TODO: 定义 Comment 模型（有外键到 Post 和 User）
# TODO: 创建表
