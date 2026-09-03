# Day 40 消息队列骨架 - TODO: 实现
from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

# TODO: 实现异步邮件发送
def send_email(to: str, subject: str, body: str):
    time.sleep(2)
    print(f'Email sent to {to}')

@app.post('/subscribe/')
async def subscribe(email: str, background_tasks: BackgroundTasks):
    # TODO: 用 BackgroundTasks 异步发送邮件
    pass

# TODO: 实现 Celery 任务
# from celery_app import celery_app
# @celery_app.task
# def send_notification(user_id, message): ...
