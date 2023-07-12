import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcwallet.settings")

app = Celery("bcwallet")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
