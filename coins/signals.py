from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CoinPriceChange, Coin


@receiver(post_save, sender=CoinPriceChange, dispatch_uid="send-current-coin-price-to-websocket")
def send_current_coin_price_to_websocket(sender, instance, created, *args, **kwargs):
    """
    Disabled due to https://github.com/ethemguner/dobot/issues/15
    """
    pass


post_save.connect(send_current_coin_price_to_websocket)
