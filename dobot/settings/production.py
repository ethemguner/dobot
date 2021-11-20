from .base import *

DEBUG = False

ALLOWED_HOSTS = ["production_host_here"]

SECRET_KEY = "secret_key from environ"

# Database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "db name from environ",
        "USER": "user name from environ",
        "PASSWORD": "password from environ",
        "HOST": "host from environ",
        "PORT": "5432",
    }
}

# Celery stuff. This can be unnecessary and we can put it in base.py
BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Istanbul'

