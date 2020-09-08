from celery import shared_task

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_api.settings')
app = Celery('movie_scrapper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()