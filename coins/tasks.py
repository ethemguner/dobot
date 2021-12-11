from celery import Celery
from celery import shared_task

from apis.binance_api import BinanceInterface
from coins.models import Coin

app = Celery('tasks', broker='pyamqp://guest@localhost//')
binance_interface = BinanceInterface()


@shared_task
def update_coins_prices_task():
    binance_interface.update_coins_prices()
    return "update_coins_prices_task finished"
