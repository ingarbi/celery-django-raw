from __future__ import absolute_import, unicode_literals  #чтобы наш модуль celery.py не конфликтовал с библиотекой
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_project.settings')

app = Celery('django_celery_project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Europe/Moscow')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

#Celery beat settings
app.conf.beat_schedule = {
    'send_mail_everyday_at_09:00' : {
        'task' : 'send_mail_app.tasks.send_mail_func',
        'schedule' : crontab(hour=20, minute=30, day_of_month=20, month_of_year=1),
        #'args' : () this args like context we pass in  function
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))