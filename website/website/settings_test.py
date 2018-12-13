from website.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'website',
        'USER': 'website',
        'PASSWORD': 'website',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}