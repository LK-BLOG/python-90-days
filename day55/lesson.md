# Day 55 课程：任务调度 & 定时系统

## 第一部分：APScheduler

### 1.1 基本概念
`python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

scheduler = AsyncIOScheduler()

# 间隔执行
@scheduler.scheduled_job(IntervalTrigger(minutes=30))
async def cleanup():
    print("Cleaning up...")

# Cron表达式
@scheduler.scheduled_job(CronTrigger(hour=3, minute=0))
async def daily_report():
    print("Generating daily report...")

# 启动
scheduler.start()
`

### 1.2 存储和持久化
`python
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

scheduler = AsyncIOScheduler(jobstores=jobstores)
`

---

## 第二部分：Celery Beat

### 2.1 配置定时任务
`python
celery_app.conf.beat_schedule = {
    'cleanup-every-hour': {
        'task': 'tasks.cleanup',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'daily-report': {
        'task': 'tasks.generate_report',
        'schedule': crontab(hour=8, minute=0),
        'args': ('daily',),
    },
    'monitor-every-5min': {
        'task': 'tasks.health_check',
        'schedule': 300.0,
    },
}
`

### 2.2 动态定时任务
`python
from celery import current_app

def add_scheduled_task(task_name: str, schedule, args=()):
    current_app.conf.beat_schedule[task_name] = {
        'task': task_name,
        'schedule': schedule,
        'args': args,
    }
`

---

## 第三部分：任务链和工作流

### 3.1 chain（顺序执行）
`python
from celery import chain

# 数据处理管道
result = chain(
    extract.s(source_url),
    transform.s(),
    validate.s(),
    load.s(destination),
)()
`

### 3.2 group（并行执行）
`python
from celery import group

# 并行处理
result = group(
    process_item.s(item) for item in items
)()
`

### 3.3 chord（并行+回调）
`python
from celery import chord

# 并行计算，最后汇总
result = chord(
    [calculate.s(i) for i in range(10)],
    aggregate.s()
)()
`

---

## 第四部分：分布式任务调度

### 4.1 多Worker部署
`ash
# 启动多个worker
celery -A app worker --concurrency=4 --hostname=worker1@%h
celery -A app worker --concurrency=4 --hostname=worker2@%h
celery -A app beat --scheduler=redbeat.RedBeatScheduler
`

### 4.2 任务路由
`python
celery_app.conf.task_routes = {
    'tasks.email': {'queue': 'email'},
    'tasks.report': {'queue': 'reports'},
    'tasks.process': {'queue': 'processing'},
}
`

### 4.3 任务优先级
`python
@celery_app.task(queue='high_priority')
def urgent_task():
    pass

@celery_app.task(queue='low_priority')
def background_task():
    pass
`

---

## 本课总结

| 工具 | 用途 |
|------|------|
| APScheduler | 进程内调度，简单灵活 |
| Celery Beat | 分布式定时，生产级 |
| chain/group/chord | 任务编排 |
| 任务路由 | 分流到不同worker |
| Redis/RabbitMQ | 消息代理 |
