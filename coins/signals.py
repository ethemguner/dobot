from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CoinPriceChange


@receiver(post_save, sender=CoinPriceChange, dispatch_uid="send-current-coin-price-to-websocket")
def send_current_coin_price_to_websocket(sender, instance, created, *args, **kwargs):
    if not isinstance(instance, CoinPriceChange):
        return

    if not created:
        return

    # We don't need to send full datetime, hour, minute and seconds is enough
    # for now.
    time_format = "%H:%M:%S"
    message_dict = {
        "current_price": float(instance.price),
        "symbol": instance.coin.symbol,
        "change_value": float(instance.change),
        "created": instance.created.strftime(time_format)
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"coin_stream", {
            "type": "send_message_to_ws",
            "message": message_dict
        }
    )


post_save.connect(send_current_coin_price_to_websocket)
