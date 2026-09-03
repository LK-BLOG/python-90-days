# Day 38 微服务示例 - 用户服务
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='User Service')
users_db = {1: {'id': 1, 'name': 'Alice', 'email': 'alice@test.com'}}

class UserCreate(BaseModel):
    name: str
    email: str

@app.get('/users/{user_id}')
async def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(404, 'User not found')
    return user

@app.post('/users/', status_code=201)
async def create_user(user: UserCreate):
    uid = max(users_db.keys()) + 1 if users_db else 1
    users_db[uid] = {'id': uid, **user.model_dump()}
    return users_db[uid]
