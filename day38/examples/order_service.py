# Day 38 微服务示例 - 订单服务（调用用户服务）
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title='Order Service')
USER_SERVICE_URL = 'http://user-service:8001'

@app.get('/orders/{order_id}')
async def get_order(order_id: int):
    # 调用用户服务
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f'{USER_SERVICE_URL}/users/1')
            user = resp.json()
        except httpx.HTTPError:
            user = {'name': 'Unknown'}
    return {'order_id': order_id, 'user': user['name']}
