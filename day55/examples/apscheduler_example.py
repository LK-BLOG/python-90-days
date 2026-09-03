\"\"\"APScheduler基础用法\"\"\"

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta


# 内存存储
scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(IntervalTrigger(seconds=10), id=\"heartbeat\")
def heartbeat():
    print(f\"Heartbeat at {datetime.now()}\")


@scheduler.scheduled_job(CronTrigger(hour=8, minute=0), id=\"morning_report\")
def morning_report():
    print(\"Generating morning report...\")


@scheduler.scheduled_job(DateTrigger(run_date=datetime.now() + timedelta(seconds=5)), id=\"one_shot\")
def one_time_task():
    print(\"One-time task executed!\")


if __name__ == \"__main__\":
    import asyncio

    async def main():
        scheduler.start()
        print(\"Scheduler started. Press Ctrl+C to stop.\")

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            scheduler.shutdown()
            print(\"Scheduler stopped.\")

    asyncio.run(main())
