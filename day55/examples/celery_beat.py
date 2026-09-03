\"\"\"Celery Beat定时配置\"\"\"

from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    \"scheduler\",
    broker=\"redis://localhost:6379/1\",
    backend=\"redis://localhost:6379/2\",
)


@celery_app.task(bind=True, max_retries=3, time_limit=300)
def cleanup_expired_data(self):
    \"\"\"每小时清理过期数据\"\"\"
    print(\"Cleaning up expired data...\")
    return {\"cleaned\": 42}


@celery_app.task(bind=True, max_retries=3)
def generate_daily_report(self, report_type: str = \"daily\"):
    \"\"\"每天生成报告\"\"\"
    print(f\"Generating {report_type} report...\")
    return {\"type\": report_type, \"status\": \"completed\"}


@celery_app.task
def health_check():
    \"\"\"每5分钟健康检查\"\"\"
    return {\"status\": \"healthy\", \"timestamp\": str(__import__(\"datetime\").datetime.now())}


# Beat调度配置
celery_app.conf.beat_schedule = {
    \"cleanup-hourly\": {
        \"task\": \"celery_beat.cleanup_expired_data\",
        \"schedule\": crontab(minute=0, hour=\"*/1\"),
    },
    \"daily-report\": {
        \"task\": \"celery_beat.generate_daily_report\",
        \"schedule\": crontab(hour=8, minute=0),
        \"args\": (\"daily\",),
    },
    \"weekly-report\": {
        \"task\": \"celery_beat.generate_daily_report\",
        \"schedule\": crontab(hour=9, minute=0, day_of_week=\"monday\"),
        \"args\": (\"weekly\",),
    },
    \"health-check\": {
        \"task\": \"celery_beat.health_check\",
        \"schedule\": 300.0,
    },
}

celery_app.conf.timezone = \"Asia/Shanghai\"
