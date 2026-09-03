\"\"\"Celery后台任务\"\"\"

from celery import Celery

celery_app = Celery(
    \"blog_worker\",
    broker=\"redis://localhost:6379/1\",
    backend=\"redis://localhost:6379/2\",
)

celery_app.conf.update(
    task_serializer=\"json\",
    accept_content=[\"json\"],
    result_serializer=\"json\",
    timezone=\"UTC\",
    enable_utc=True,
)


@celery_app.task(bind=True, max_retries=3)
def send_notification_email(self, to: str, subject: str, body: str) -> bool:
    \"\"\"发送通知邮件\"\"\"
    try:
        # 模拟发送
        print(f\"[Email] To: {to}, Subject: {subject}\")
        return True
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@celery_app.task
def generate_report_task(report_type: str, params: dict) -> str:
    \"\"\"生成报告\"\"\"
    import time
    time.sleep(2)  # 模拟耗时
    return f\"/reports/{report_type}_{params.get('date', 'latest')}.pdf\"


@celery_app.task
def cleanup_expired_tokens() -> int:
    \"\"\"清理过期token\"\"\"
    print(\"Cleaning up expired tokens...\")
    return 42  # 返回清理数量


# 定时任务配置
celery_app.conf.beat_schedule = {
    \"cleanup-tokens\": {
        \"task\": \"celery_tasks.cleanup_expired_tokens\",
        \"schedule\": 3600.0,  # 每小时
    },
}
