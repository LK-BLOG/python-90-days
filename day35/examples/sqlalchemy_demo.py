# Day 35 SQLAlchemy 基础示例
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    age = Column(Integer, default=0)
    posts = relationship('Post', back_populates='author', cascade='all, delete-orphan')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000))
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')

Base.metadata.create_all(engine)

def demo():
    session = SessionLocal()
    # 创建
    user = User(username='alice', email='alice@test.com', age=30)
    session.add(user)
    session.commit()

    post = Post(title='Hello World', content='First post', author_id=user.id)
    session.add(post)
    session.commit()

    # 查询
    u = session.query(User).filter_by(username='alice').first()
    print(f"User: {u.username}, Posts: {len(u.posts)}")
    
    # 关联查询（避免 N+1）
    from sqlalchemy.orm import joinedload
    posts = session.query(Post).options(joinedload(Post.author)).all()
    for p in posts:
        print(f"Post: {p.title} by {p.author.username}")

    session.close()

if __name__ == '__main__':
    demo()
