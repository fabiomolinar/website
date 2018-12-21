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

DATABASE_ROUTERS = [
    'ali.routers.AliRouter',
]