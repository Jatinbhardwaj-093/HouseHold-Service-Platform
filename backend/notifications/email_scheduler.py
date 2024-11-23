from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from notifications.daily_task import daily_email_task
from notifications.monthly_task import monthly_email_task

def schedule_email(app):
    scheduler = BackgroundScheduler()
    
    trigger_daily = CronTrigger(hour=8, minute=0, second=0, timezone='Asia/Kolkata')
    trigger_month = CronTrigger(month='*', day=1, hour=0, minute=0, second=0, timezone='Asia/Kolkata')
    
    scheduler.add_job(func=lambda: daily_email_task(app), trigger=trigger_daily)
    scheduler.add_job(func=lambda: monthly_email_task(app), trigger=trigger_month)
    scheduler.start()
