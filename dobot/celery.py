import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dobot.settings')

app = Celery(
    "dobot",
    include=[
        "notifications.tasks",
        "coins.tasks"
    ]
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

UPDATE_COINS_FREQUENCY = 60


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(180.0, get_klines.s(), name='get_klines')
    sender.add_periodic_task(UPDATE_COINS_FREQUENCY, update_coins_prices.s(), name='update_coins_prices')


@app.task
def get_klines():
    from data_types.tasks import get_klines_task
    from coins.models import Coin
    coins = Coin.objects.all()
    for coin in coins:
        get_klines_task.apply_async(
            [coin.id],
            countdown=1,
            queue="get_klines"
        )
    return "get_klines app.task has finished"


@app.task
def update_coins_prices():
    from coins.tasks import update_coins_prices_task
    update_coins_prices_task.apply_async(countdown=1, queue="price_update")
