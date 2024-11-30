from flask_mail import Mail
from celery import Celery,Task
from flask import Flask

# Celery Configuration
class CeleryConfig():
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'

# Initialize the Mail extension
mail = Mail()

def create_celery(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.name,task_cls=FlaskTask)
    celery.config_from_object(CeleryConfig)
    celery.set_default()
    return celery



