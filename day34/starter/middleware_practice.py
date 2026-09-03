# Day 34 中间件骨架 - TODO: 实现
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    # TODO: 记录开始时间
    # TODO: 调用下一个中间件
    # TODO: 设置 X-Process-Time 头
    pass

# TODO: 实现自定义异常类 AppError
# TODO: 注册异常处理器
