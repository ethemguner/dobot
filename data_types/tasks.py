from celery import Celery
from celery import shared_task

from apis.binance import BinanceInterface

app = Celery('tasks', broker='pyamqp://guest@localhost//')
binance_interface = BinanceInterface()


@shared_task
def get_klines_task(coin_id):
    binance_interface.get_klines(
        interval="3minute",
        coin_id=coin_id
    )
    return f"get_klines_task for coin({coin_id}) has finished."
