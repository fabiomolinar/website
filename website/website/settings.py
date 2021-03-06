"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('WEBSITE_DJANGO_SECRET_KEY', '!luz5ul72p8z%e+9ffm8cv!zhb1+qkznbx5pqu@a)j(by9)_dt')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('WEBSITE_DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['fabiomolinar.com', 'www.fabiomolinar.com', '.fabiomolinar.com', 'localhost', 'www.localhost', '.localhost']


# Application definition

INSTALLED_APPS = [
    'base.apps.BaseConfig',
    'ali.apps.AliConfig',
    'django_celery_results',
    'django_celery_beat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_comments',
    'mptt',
    'tagging',
    'zinnia',
    'compressor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'zinnia.context_processors.version',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'website',
        'USER': 'website',
        'PASSWORD': os.environ.get('WEBSITE_POSTGRES_WEBSITE_PASSWORD', 'website'),
        'HOST': os.environ.get('WEBSITE_DJANGO_DB_HOST', 'website_db'),
        'PORT': '5432',
    },
    'ali': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ali',
        'USER': 'ali',
        'PASSWORD': os.environ.get('WEBSITE_POSTGRES_ALI_PASSWORD', 'ali'),
        'HOST': os.environ.get('WEBSITE_DJANGO_DB_HOST', 'website_db'),
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = [
    'ali.routers.AliRouter',
]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('pt', _('Portuguese'))
]

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

SITE_ID = 1

# ----- My settings -----

ADMINS = [('Fabio Molinar', 'fabiomolinar+website@gmail.com')]
MANAGERS = [('Fabio Molinar', 'fabiomolinar+website@gmail.com')]

# Zinnia
ZINNIA_MARKUP_LANGUAGE = 'markdown'
ZINNIA_PROTOCOL = 'https'

# Serving static files
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static')
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'media')

# Scrapyd host
SCRAPYD_HOST = os.environ.get('WEBSITE_DJANGO_SCRAPYD_HOST', 'collector')
# How many days we will cache the results from a query
ALI_SEARCH_CACHE = 3
# How many seconds to wait while listening for an event from the DB (in seconds)
ALI_SEARCH_TIMEOUT = 15
# Default tracker
ALI_DEFAULT_TRACKER = 'mp3'

# Celery
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = os.environ.get('WEBSITE_DJANGO_CELERY_BROKER_URL', 'pyamqp://guest:guest@rabbitmq:5672/')
CELERY_TIMEZONE = 'Europe/Warsaw'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_MAX_LOOP_INTERVAL = 300

# Security
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Email

EMAIL_BACKEND = os.environ.get('WEBSITE_DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('WEBSITE_DJANGO_EMAIL_HOST', 'smtp.zoho.com')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('WEBSITE_DJANGO_EMAIL_HOST_USER', 'default@domain.com')
EMAIL_HOST_PASSWORD = os.environ.get('WEBSITE_DJANGO_EMAIL_HOST_PASSWORD', 'password')
EMAIL_USE_TLS = os.environ.get('WEBSITE_DJANGO_EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('WEBSITE_DJANGO_EMAIL_USE_SSL', 'True') == 'True'

# Twitter

TWITTER_AUTH = os.environ.get('TWITTER_BEARER_TOKEN', 'asdqweasd')