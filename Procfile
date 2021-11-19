web: gunicorn dobot.wsgi
release: python manage.py makemigrations
release: python manage.py migrate
worker: celery -A dobot worker -Q celery,price_update -l info -B