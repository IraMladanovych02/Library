from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_config.settings")

app = Celery("library_config")

app.config_from_object(settings, namespace="CELERY")

app.conf.enable_utc = False

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
