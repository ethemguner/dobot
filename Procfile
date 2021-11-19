web: gunicorn dobot.wsgi
web: daphne -b 0.0.0.0 -p $PORT mysite.asgi:application
release: python3 manage.py migrate
worker: celery -A dobot worker -Q celery,price_update -l info -B