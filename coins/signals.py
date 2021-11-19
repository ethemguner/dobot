from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Coin, CoinPriceChange


@receiver(post_save, sender=CoinPriceChange, dispatch_uid="send-current-coin-price-to-websocket")
def send_current_coin_price_to_websocket(sender, instance, created, *args, **kwargs):
    if not isinstance(instance, CoinPriceChange):
        return

    if not created:
        return

    message_dict = {
        "current_price": float(instance.price),
        "symbol": instance.coin.symbol,
        "change_value": float(instance.change)
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"coin_stream", {
            "type": "send_message_to_ws",
            "message": message_dict
        }
    )


post_save.connect(send_current_coin_price_to_websocket)
