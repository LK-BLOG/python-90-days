# Day 36 事务示例
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    balance = Column(Float, default=0)

Base.metadata.create_all(engine)
session = Session()

# 创建账户
session.add_all([Account(name='Alice', balance=1000), Account(name='Bob', balance=500)])
session.commit()

def transfer(session, from_id, to_id, amount):
    sender = session.query(Account).get(from_id)
    receiver = session.query(Account).get(to_id)
    if sender.balance < amount:
        raise ValueError('余额不足')
    sender.balance -= amount
    receiver.balance += amount
    session.commit()
    print(f'Transferred {amount}: {sender.name} -> {receiver.name}')

try:
    transfer(session, 1, 2, 300)
    print(f'Alice: {session.query(Account).get(1).balance}')
    print(f'Bob: {session.query(Account).get(2).balance}')
except Exception as e:
    session.rollback()
    print(f'Error: {e}')
session.close()
