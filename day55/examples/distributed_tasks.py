\"\"\"分布式任务系统\"\"\"

from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    \"distributed\",
    broker=\"redis://localhost:6379/1\",
    backend=\"redis://localhost:6379/2\",
)

# 任务路由
celery_app.conf.task_routes = {
    \"tasks.email\": {\"queue\": \"email\"},
    \"tasks.report\": {\"queue\": \"reports\"},
    \"tasks.process\": {\"queue\": \"processing\"},
    \"tasks.monitor\": {\"queue\": \"monitoring\"},
}

# Worker并发配置
celery_app.conf.worker_concurrency = 4
celery_app.conf.worker_prefetch_multiplier = 1


@celery_app.task(queue=\"email\", bind=True, max_retries=3)
def send_email_task(self, to: str, subject: str, body: str):
    try:
        print(f\"Sending email to {to}: {subject}\")
        return {\"status\": \"sent\", \"to\": to}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@celery_app.task(queue=\"reports\", time_limit=600)
def generate_report_task(report_type: str, params: dict):
    import time
    time.sleep(2)
    print(f\"Generated {report_type} report\")
    return {\"type\": report_type, \"file\": f\"/reports/{report_type}.pdf\"}


@celery_app.task(queue=\"processing\", rate_limit=\"10/m\")
def process_item_task(item_id: int):
    print(f\"Processing item {item_id}\")
    return {\"item\": item_id, \"processed\": True}


@celery_app.task(queue=\"monitoring\")
def health_check_task():
    import platform
    return {
        \"hostname\": platform.node(),
        \"status\": \"healthy\",
    }


# Beat调度（分布式感知）
celery_app.conf.beat_schedule = {
    \"email-cleanup\": {
        \"task\": \"distributed.cleanup_email_queue\",
        \"schedule\": crontab(minute=0, hour=\"*/2\"),
        \"options\": {\"queue\": \"email\"},
    },
    \"health-monitor\": {
        \"task\": \"distributed.health_check_task\",
        \"schedule\": 60.0,
        \"options\": {\"queue\": \"monitoring\"},
    },
}
