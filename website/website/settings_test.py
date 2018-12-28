# pylint: disable=W0614
from website.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'website',
        'USER': 'website',
        'PASSWORD': 'website',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'ali': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ali',
        'USER': 'ali',
        'PASSWORD': 'ali',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Scrapyd 
SCRAPYD_HOST = 'localhost'

# Celery
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'pyamqp://'
CELERY_TIMEZONE = 'Europe/Warsaw'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
