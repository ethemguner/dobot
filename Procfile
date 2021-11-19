web: gunicorn dobot.wsgi
release: python manage.py migrate
worker: celery -A dobot beat -l debug
worker2: celery -A dobot worker -Q celery,price_update -l INFO