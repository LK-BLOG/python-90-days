\"\"\"SQLAlchemy数据模型 — 博客API\"\"\"

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Table, Boolean, create_engine
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


# 文章-标签 多对多
article_tags = Table(
    \"article_tags\", Base.metadata,
    Column(\"article_id\", Integer, ForeignKey(\"articles.id\", ondelete=\"CASCADE\")),
    Column(\"tag_id\", Integer, ForeignKey(\"tags.id\", ondelete=\"CASCADE\")),
)


class User(Base):
    __tablename__ = \"users\"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship(\"Article\", back_populates=\"author\", cascade=\"all, delete\")
    comments = relationship(\"Comment\", back_populates=\"author\")


class Article(Base):
    __tablename__ = \"articles\"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500), default=\"\")
    author_id = Column(Integer, ForeignKey(\"users.id\"))
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship(\"User\", back_populates=\"articles\")
    comments = relationship(\"Comment\", back_populates=\"article\", cascade=\"all, delete\")
    tags = relationship(\"Tag\", secondary=article_tags, back_populates=\"articles\")


class Comment(Base):
    __tablename__ = \"comments\"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey(\"articles.id\"))
    author_id = Column(Integer, ForeignKey(\"users.id\"))
    created_at = Column(DateTime, default=datetime.utcnow)

    article = relationship(\"Article\", back_populates=\"comments\")
    author = relationship(\"User\", back_populates=\"comments\")


class Tag(Base):
    __tablename__ = \"tags\"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    articles = relationship(\"Article\", secondary=article_tags, back_populates=\"tags\")


if __name__ == \"__main__\":
    engine = create_engine(\"sqlite:///blog_example.db\")
    Base.metadata.create_all(engine)
    print(\"Tables created!\")
