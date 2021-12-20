import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dobot.settings")
django.setup()

import logging
from decimal import Decimal

from asgiref.sync import async_to_sync
from binance import ThreadedWebsocketManager
from channels.layers import get_channel_layer
from django.utils import timezone

from apis.binance_api import BinanceInterface
from coins.models import Coin

logger = logging.getLogger(__name__)

binance_interface = BinanceInterface()
print("BinanceInterface initialized and connected to Binance.")
all_coins = Coin.objects.all()

price_data = {}
for coin in all_coins:
    price_data[coin.symbol] = {"symbol": coin.symbol, "price": None, "error": None}

print("price_data is ready to handle income data.")


def update_current_price_of_coin(message):
    for coin in all_coins:
        coin_symbol_from_ws = message["s"]
        coin_price_from_ws = float(message["c"])
        if coin_symbol_from_ws == coin.symbol:
            if message["e"] != "error":
                price_data[coin.symbol].update({"price": coin_price_from_ws})
            else:
                price_data[coin.symbol].update({"error": True})


print("ThreadedWebsocketManager initializing for per coin.")
listening_coins = list()
websocket_managers = dict()
for coin in Coin.objects.all():
    websocket_manager = ThreadedWebsocketManager()
    websocket_manager.start()
    ticker = websocket_manager.start_symbol_ticker_socket(
        symbol=coin.symbol,
        callback=update_current_price_of_coin
    )
    listening_coins.append(ticker)
    websocket_managers[coin.symbol] = websocket_manager
    print("Websocket thread started for %s" % coin.symbol)


def send_to_system_websocket(coin, current_price, previous_price):
    change_time_format = "%H:%M:%S"
    change_value = float(current_price) - float(previous_price)
    change_ratio = float((change_value / float(data["price"])) * 100)
    message_dict = {
        "created": timezone.now().strftime(change_time_format),
        "current_price": float(current_price),
        "symbol": coin,
        "change_value": float(Decimal(change_value).quantize(Decimal("0.000"))),
        "change_ratio": float(Decimal(change_ratio).quantize(Decimal('0.00000'))),
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"coin_stream", {
            "type": "send_message_to_ws",
            "message": message_dict
        }
    )


print("All initialized! Starting to listen binance websocket.")
previous_prices = dict()
while True:
    for coin_symbol, data in price_data.items():
        if data["error"]:
            ws_manager = websocket_managers[coin_symbol]
            ws_manager.stop()
            ws_manager.start()
        else:
            if previous_prices.get(coin_symbol) != data["price"]:
                previous_price = previous_prices.get(coin_symbol)
                previous_prices[coin_symbol] = data["price"]
                coin = Coin.objects.get(symbol=coin_symbol)
                binance_interface.decide(coin)

                if previous_price:
                    send_to_system_websocket(
                        coin=coin_symbol,
                        current_price=data["price"],
                        previous_price=previous_price
                    )
