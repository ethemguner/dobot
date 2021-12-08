from decimal import Decimal

from django.db import models


class Coin(models.Model):
    class Meta:
        verbose_name = "Coin"
        verbose_name_plural = "Coins"

    COIN_BTC = "BTCUSDT"
    COIN_ETH = "ETHUSDT"
    COIN_BNB = "BNBUSDT"

    COIN_SYMBOLS = (
        (COIN_BTC, "Bitcoin/USD"),
        (COIN_ETH, "Etherium/USD"),
        (COIN_BNB, "Binance Coin/USD")
    )

    symbol = models.CharField(
        verbose_name="Symbol",
        max_length=50,
        choices=COIN_SYMBOLS
    )
    current_price = models.DecimalField(
        verbose_name="Current Price",
        max_digits=19,
        decimal_places=2
    )
    last_update = models.DateTimeField(
        verbose_name="Last Update",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.symbol


class CoinPriceChange(models.Model):
    class Meta:
        verbose_name = "Coin Price Change"
        verbose_name_plural = "Coin Price Changes"

    created = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True
    )
    price = models.DecimalField(
        verbose_name="Price",
        max_digits=19,
        decimal_places=2
    )
    change = models.DecimalField(
        verbose_name="Change",
        max_digits=19,
        decimal_places=2
    )
    coin = models.ForeignKey(
        to="coins.Coin",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    change_ratio = models.DecimalField(
        verbose_name="Change",
        max_digits=19,
        decimal_places=4,
        null=True,
        blank=True
    )

    def __str__(self):
        if self.change > 0:
            change = "+" + str(self.change)
        else:
            change = self.change
        return f"{self.coin.symbol} | {change}% | {self.price}"

    @classmethod
    def get_last_change_data(cls):
        change_data = dict()
        coins = Coin.objects.all()
        for coin in coins:
            coin_price_change = cls.objects.filter(
                coin=coin
            ).order_by("id").last()
            humanized_symbol = cls.get_humanized_symbol(coin.symbol)
            change_data[humanized_symbol] = {
                "symbol": coin.symbol,
                "price": coin_price_change.price,
                "change": coin_price_change.change,
                "change_ratio": Decimal(coin_price_change.change_ratio).quantize(Decimal('0.00000'))
            }
        return change_data

    @staticmethod
    def get_humanized_symbol(symbol):
        splitted_coin = symbol.split("USDT")
        splitted_coin[-1] = "$"
        return '/'.join(splitted_coin)
