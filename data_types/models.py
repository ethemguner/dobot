from django.db import models

from coins.models import Coin


class Kline(models.Model):
    """
    Kline
    """
    class Meta:
        verbose_name = "Kline"
        verbose_name_plural = "Klines"

    KI_1MINUTE = '1m'
    KI_3MINUTE = '3m'
    KI_5MINUTE = '5m'
    KI_15MINUTE = '15m'
    KI_30MINUTE = '30m'
    KI_1HOUR = '1h'
    KI_2HOUR = '2h'
    KI_4HOUR = '4h'
    KI_6HOUR = '6h'
    KI_8HOUR = '8h'
    KI_12HOUR = '12h'
    KI_1DAY = '1d'
    KI_3DAY = '3d'
    KI_1WEEK = '1w'
    KI_1MONTH = '1M'

    KLINE_INTERVAL_TYPES = (
        (KI_1MINUTE, "1 minute (interval)"),
        (KI_3MINUTE, "3 minutes (interval)"),
        (KI_5MINUTE, "5 minutes (interval)"),
        (KI_15MINUTE, "15 minutes (interval)"),
        (KI_30MINUTE, "30 minutes (interval)"),
        (KI_1HOUR, "1 hour (interval)"),
        (KI_2HOUR, "2 hours (interval)"),
        (KI_4HOUR, "4 hours (interval)"),
        (KI_6HOUR, "6 hours (interval)"),
        (KI_8HOUR, "8 hours (interval)"),
        (KI_12HOUR, "12 hours (interval)"),
        (KI_1DAY, "1 day (interval)"),
        (KI_1WEEK, "1 week (interval)"),
        (KI_1MONTH, "1 month (interval)"),
    )
    coin = models.ForeignKey(
        to="coins.Coin",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    interval = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=KLINE_INTERVAL_TYPES
    )
    open_time = models.DateTimeField(
        verbose_name="Open Time",
        null=True,
        blank=True
    )
    open_price = models.DecimalField(
        verbose_name="Open Price",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    highest_price = models.DecimalField(
        verbose_name="Highest Price",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    lowest_price = models.DecimalField(
        verbose_name="Lowest Price",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    close_price = models.DecimalField(
        verbose_name="Close Price",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    volume = models.DecimalField(
        verbose_name="Volume",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    close_time = models.DateTimeField(
        verbose_name="Close Time",
        null=True,
        blank=True
    )
    quote_asset_volume = models.DecimalField(
        verbose_name="Quote Asset Volume",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    number_of_trades = models.PositiveBigIntegerField(
        verbose_name="Number of Trades",
        null=True,
        blank=True
    )
    taker_buy_base_asset_volume = models.DecimalField(
        verbose_name="Taker Buy Base Asset Volume",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    taker_buy_quote_asset_volume = models.DecimalField(
        verbose_name="Taker Buy Base Asset Volume",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    ignore = models.DecimalField(
        verbose_name="Ignore",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    timestamp = models.PositiveBigIntegerField(
        verbose_name="Timestamp",
        null=True,
        default=True
    )
    created = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True
    )

