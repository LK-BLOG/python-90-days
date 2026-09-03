# Day 38 微服务骨架
# TODO: 实现用户服务和订单服务
from fastapi import FastAPI
app = FastAPI()

@app.get('/users/{user_id}')
async def get_user(user_id: int):
    # TODO: 实现
    pass
