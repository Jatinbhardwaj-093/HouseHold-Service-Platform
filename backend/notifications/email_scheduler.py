from celery.schedules import crontab
from notifications.daily_task import daily_email_task
from notifications.monthly_task import monthly_email_task
from datetime import timedelta

def schedule_email(app, celery):
    # Set the timezone in the Celery configuration
    celery.conf.update(timezone='Asia/Kolkata')

    # Define the Celery beat schedule
    celery.conf.beat_schedule = {
        'daily-email-task': {
            'task': 'notifications.daily_task.daily_email_task',  
            'schedule': crontab(hour=8, minute=0),
            'args': (),  
        },
        'monthly-email-task': {
            'task': 'notifications.monthly_task.monthly_email_task',  
            'schedule': crontab(day_of_month=1, hour=0, minute=0),
            'args': (),
        },
    }

