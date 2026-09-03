# Challenge 02: JWT 认证
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class UserRegister(BaseModel):
    username: str
    password: str

# TODO: 实现注册
# TODO: 实现登录（返回 JWT）
# TODO: 实现 token 验证依赖
# TODO: 保护端点 /me
