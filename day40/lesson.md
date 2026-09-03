# Day 40 课程：消息队列 & 异步任务

## 第一部分：消息队列概念

### 1.1 为什么需要消息队列

同步处理：
请求 -> 处理 -> 响应（用户等待）

异步处理：
请求 -> 发消息到队列 -> 立即响应
                ↓
          Worker 后台处理

场景：
- 发送邮件/短信
- 生成报告
- 图片处理
- 数据同步
- 定时任务

### 1.2 Redis 作为消息队列

`python
import redis
import json
import time
from threading import Thread

r = redis.Redis(decode_responses=True)

# 生产者
def produce(queue_name: str, task: dict):
    r.lpush(queue_name, json.dumps(task))

# 消费者
def consume(queue_name: str):
    while True:
        _, task_json = r.brpop(queue_name, timeout=5)
        if task_json:
            task = json.loads(task_json)
            process_task(task)

def process_task(task: dict):
    print(f"Processing: {task}")
    time.sleep(2)  # 模拟耗时操作
    print("Done")
`

---

## 第二部分：Celery 基础

### 2.1 安装和配置

`ash
pip install celery[redis]
`

`python
# celery_app.py
from celery import Celery

app = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
)
`

### 2.2 定义任务

`python
# tasks.py
from celery_app import app
import time

@app.task
def add(x, y):
    return x + y

@app.task(bind=True)
def send_email(self, to, subject, body):
    try:
        # 模拟发送邮件
        time.sleep(3)
        print(f"Email sent to {to}")
        return {"status": "sent", "to": to}
    except Exception as exc:
        self.retry(exc=exc, countdown=60, max_retries=3)

@app.task
def generate_report(report_type, params):
    time.sleep(10)
    return {"file": f"/reports/{report_type}.pdf"}
`

### 2.3 调用任务

`python
# 同步调用（阻塞）
result = add(4, 4)
print(result)  # 8

# 异步调用（非阻塞）
result = add.delay(4, 4)
print(result.id)  # 任务ID
print(result.get(timeout=10))  # 等待结果

# 带超时
result = add.apply_async(args=[4, 4], expires=300)

# 后台运行
send_email.delay("user@test.com", "Welcome!", "Hello!")
`

### 2.4 运行 Worker

`ash
# 启动 worker
celery -A celery_app worker --loglevel=info

# 启动多个 worker
celery -A celery_app worker --loglevel=info --concurrency=4
`

---

## 第三部分：Celery Beat 定时任务

`python
# celery_app.py
app.conf.beat_schedule = {
    'cleanup-every-hour': {
        'task': 'tasks.cleanup',
        'schedule': 3600.0,  # 每小时
    },
    'report-daily': {
        'task': 'tasks.generate_daily_report',
        'schedule': {
            'hour': 8,
            'minute': 0,
        },
    },
}

# 启动 beat
# celery -A celery_app beat --loglevel=info
`

---

## 第四部分：异步模式

### 4.1 任务链

`python
from celery import chain, group, chord

# 链式调用
workflow = chain(
    add.s(2, 2),
    add.s(4),  # 结果传给下一个
)
result = workflow.apply_async()  # (2+2)+4 = 10

# 并行执行
job = group(add.s(i, i) for i in range(10))
result = job.apply_async()

# chord: 并行执行 + 回调
callback = add_all.s()  # 汇总函数
header = [add.s(i, i) for i in range(10)]
result = chord(header)(callback)
`

### 4.2 错误处理

`python
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def unreliable_task(self):
    try:
        # 可能失败的操作
        raise ConnectionError("Database down")
    except ConnectionError as exc:
        self.retry(exc=exc)

# 任务失败回调
@app.task
def task_failure_handler(request, exc, traceback):
    print(f"Task {request.id} failed: {exc}")

# 信号
from celery.signals import task_success, task_failure

@task_success.connect
def on_success(sender, **kwargs):
    print(f"Task {sender.request.id} succeeded")
`

---

## 常见错误
1. 在任务中使用全局对象 -> 多 worker 下不安全
2. 忘记处理异常 -> 任务静默失败
3. 任务参数不可序列化 -> 无法传递
4. 没有设置超时 -> 任务永久挂起

## 动手练习
1. 用 Redis 实现简单的任务队列
2. 创建 Celery 异步任务
3. 实现任务链和并行执行
4. 配置定时任务
