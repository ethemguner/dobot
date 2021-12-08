from datetime import datetime
from decimal import Decimal

from binance.client import Client
from django.conf import settings
from django.utils import timezone

from coins.models import Coin, CoinPriceChange
from data_types.models import Kline
from decision_maker.models import DecisionSetting, Decision
from transactions.models import Transaction
from wallet.models import Wallet


class BinanceInterface:
    """
    Binance Client for bot operations.
    """
    def __init__(
            self,
            api_key=settings.BINANCE_KEY,
            api_secret=settings.BINANCE_SECRET
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(self.api_key, self.api_secret)

    def _selected_interval(self, interval):
        """Returns interval type from python-binance package client.
        Args:
            interval (str): 1minute, 3minute, 1hour...

        Returns:
            str
        """
        return getattr(self.client, "KLINE_INTERVAL_%s" % interval.upper())

    @staticmethod
    def convert_timestamp(timestamp):
        """Converts timestamp to datetime object.
        Args:
            timestamp (int): Timestamp came from Binance API service.
        Returns:
            datetime object
        """
        return datetime.fromtimestamp(timestamp / 1000)

    @staticmethod
    def _get_value(kline_data, index):
        """Returns value from kline_data or None.

        Args:
            kline_data (list): Data came from Binance API service.
            index (int): Index of element we want to get.

        Returns:
            None or a int/str value.
        """
        try:
            return kline_data[index]
        except IndexError:
            return None

    def _create_kline(self, kline_data, coin, interval):
        """Creates kline in our DB.

        Args:
            kline_data (list): Data came from Binance API service.
            coin (Coin): Coin instance that we will save its knile data to DB.
            interval (str): 1minute, 3minute, 1week, 1day...
        """
        open_timestamp = kline_data[0]
        try:
            Kline.objects.get(timestamp=open_timestamp)
        except Kline.DoesNotExist:
            model_args = {
                "interval": self._selected_interval(interval),
                "open_time": self.convert_timestamp(open_timestamp),
                "open_price": float(self._get_value(kline_data, 1)),
                "highest_price": float(self._get_value(kline_data, 2)),
                "lowest_price": float(self._get_value(kline_data, 3)),
                "close_price": float(self._get_value(kline_data, 4)),
                "volume": float(self._get_value(kline_data, 5)),
                "close_time": self.convert_timestamp(kline_data[6]),
                "quote_asset_volume": float(self._get_value(kline_data, 7)),
                "number_of_trades": int(self._get_value(kline_data, 8)),
                "taker_buy_base_asset_volume": float(self._get_value(kline_data, 9)),
                "taker_buy_quote_asset_volume": float(self._get_value(kline_data, 10)),
                "ignore": float(self._get_value(kline_data, 11)),
                "coin": coin,
                "timestamp": int(open_timestamp)
            }
            Kline.objects.create(**model_args)
        except Kline.MultipleObjectsReturned:
            pass

    def get_klines(self, interval, coin_id):
        """Gets klines data from Binance and creates Kline instances in DB.

        Args:
            interval (str): 1minute, 3minute, 1day...
            coin_id (int): ID of coin in our system.
        """
        coin = Coin.objects.get(id=coin_id)
        klines = self.client.get_klines(
            symbol=coin.symbol,
            interval=self._selected_interval(interval)
        )
        for kline in klines:
            self._create_kline(kline, coin, interval)

    @staticmethod
    def _get_value_as_decimal(value):
        return Decimal(value).quantize(Decimal("0.00"))

    def create_price_change(self, coin, previous_price, new_price):
        """Creates CoinPriceChange instance in our DB.

        Args:
            coin (Coin): Coin instance.
            previous_price (str): Previous price of coin.
            new_price (str): New price for coin that came from Binance API.
        """
        CoinPriceChange.objects.create(
            coin=coin,
            price=new_price,
            change=self._get_value_as_decimal(new_price) - previous_price,
            change_ratio=self._get_change_ratio(new_price, previous_price)
        )

    @staticmethod
    def _get_change_ratio(new_price, previous_price):
        change_value = float(new_price) - float(previous_price)
        return Decimal(float((change_value / float(new_price)) * 100)).quantize(Decimal("0.0000"))

    def update_coins_prices(self):
        """Updates price of coins that available for our system.
        """
        tickers = self.client.get_all_tickers()
        coins = Coin.objects.all()

        # We cannot get recent price of a specific symbol,
        # thus we had to do something that not cool. Although,
        # we did some tricks to reduce the time we will spend.
        updated_coins = list()
        for ticker in tickers:
            symbol = ticker.get("symbol")
            coin_count = coins.count()

            if len(updated_coins) == coin_count:
                break

            if symbol in list(coins.values_list("symbol", flat=True)):
                for coin in coins:
                    if ticker.get("symbol") == coin.symbol:
                        previous_price = coin.current_price
                        coin.current_price = float(ticker.get("price"))
                        if coin.symbol == coin.COIN_BTC:
                            self.decide(float(ticker.get("price")))
                        coin.last_update = timezone.now()
                        coin.save()
                        self.create_price_change(
                            coin,
                            previous_price,
                            ticker.get("price")
                        )
                        updated_coins.append(coin)

    def decide(self, current_price):
        decision_settings = DecisionSetting.objects.first()
        change_value = current_price - float(decision_settings.entry_price_level)

        ratio = float((change_value / current_price) * 100)

        # TODO: by desicion
        if ratio > 0 and ratio > decision_settings.ratio_to_sell and not decision_settings.dont_sell:
            self.sell(current_price, decision_settings)
        if 0 > ratio < decision_settings.ratio_to_buy and not decision_settings.dont_buy:
            self.buy(current_price, decision_settings)

    @staticmethod
    def sell(current_price, decision_settings):
        wallet = Wallet.objects.first()
        new_balance = (float(wallet.coin_balance) * current_price)
        fee = (new_balance / 100) * 0.05
        new_balance -= fee
        wallet.total_balance = new_balance
        wallet.coin_balance = 0
        wallet.save()

        coin = Coin.objects.get(symbol=Coin.COIN_BTC)

        decision = Decision.objects.create(
            type_of_decision=Decision.TYPE_SELL,
            coin=coin,
            price_level=float(current_price),
        )

        Transaction.objects.create(
            transaction_type=Transaction.TYPE_SELL,
            coin=coin,
            wallet=wallet,
            decision=decision,
        )

        decision_settings.entry_price_level = float(current_price)
        decision_settings.dont_sell = True
        decision_settings.dont_buy = False
        decision_settings.save()

    @staticmethod
    def buy(current_price, decision_settings):
        wallet = Wallet.objects.first()
        new_coin_balance = (float(wallet.total_balance) / current_price)
        wallet.total_balance = 0
        wallet.coin_balance = new_coin_balance
        wallet.save()

        coin = Coin.objects.get(symbol=Coin.COIN_BTC)

        decision = Decision.objects.create(
            type_of_decision=Decision.TYPE_BUY,
            coin=Coin.objects.get(symbol=Coin.COIN_BTC),
            price_level=float(current_price),
        )

        Transaction.objects.create(
            transaction_type=Transaction.TYPE_BUY,
            coin=coin,
            wallet=wallet,
            decision=decision,
        )

        decision_settings.entry_price_level = float(current_price)
        decision_settings.dont_sell = False
        decision_settings.dont_buy = True
        decision_settings.save()





