"""
This module sets up the Celery task queue for the moviemate app.
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the environment variable DJANGO_SETTINGS_MODULE to your Django project's settings file.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviemate.settings')

# Create an instance of the Celery application and name it after your Django project.
app = Celery('scraper')

# Have Celery use Django's settings for its own configuration.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
