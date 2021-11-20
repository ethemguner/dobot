from .base import *
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "django-insecure-%tyxpn+x)=60+e@ruguew#x5kt=xi@9#4!$1o)b$q9z3dr-12o"

# Database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "dobotdb",
        "USER": "dobot",
        "PASSWORD": "safa0606",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Binance components.
BINANCE_KEY = ""
BINANCE_SECRET = ""

# Celery stuff.
BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Istanbul'
