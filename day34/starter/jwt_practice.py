# Day 34 JWT 认证骨架 - TODO: 实现
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# TODO: 实现密码哈希
# TODO: 实现 token 生成
# TODO: 实现 token 验证
# TODO: POST /register
# TODO: POST /token
# TODO: GET /me (保护端点)
