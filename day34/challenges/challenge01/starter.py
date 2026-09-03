# Challenge 01: 中间件和异常处理
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

app = FastAPI()

# TODO: 实现计时中间件
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    pass

# TODO: 实现自定义异常
class AppError(Exception):
    pass

# TODO: 注册异常处理器
