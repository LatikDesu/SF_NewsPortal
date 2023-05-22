import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SF_NewsPortal.settings')

app = Celery('SF_NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# celery beat tasks
app.conf.beat_schedule = {
    'send-every-weeks': {
        'task': 'news.tasks.weekly_notification',
        'schedule': crontab(minute=0, hour=0, day_of_week='monday'),
    },
}
