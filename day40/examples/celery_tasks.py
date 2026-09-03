# Day 40 Celery 任务示例
from celery import Celery
import time

app = Celery('demo', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

@app.task(bind=True, max_retries=3)
def send_email(self, to, subject, body):
    try:
        print(f'Sending email to {to}: {subject}')
        time.sleep(2)
        return {'status': 'sent', 'to': to}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

@app.task
def process_data(data):
    time.sleep(1)
    return {'processed': len(data), 'result': [x * 2 for x in data]}

@app.task
def generate_report(report_type):
    time.sleep(3)
    return {'file': f'/tmp/{report_type}_report.pdf', 'status': 'ready'}
