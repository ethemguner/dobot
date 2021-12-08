from decimal import Decimal

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CoinPriceChange, Coin


@receiver(post_save, sender=CoinPriceChange, dispatch_uid="send-current-coin-price-to-websocket")
def send_current_coin_price_to_websocket(sender, instance, created, *args, **kwargs):
    if not isinstance(instance, CoinPriceChange):
        return

    if not created:
        return

    # We don't need to send full datetime, hour, minute and seconds is enough
    # for now.
    change_time_format = "%H:%M:%S"
    change_total_time_format = "%m/%d/%Y, %H:%M:%S"
    total_change = CoinPriceChange.objects.filter(
        coin__symbol=Coin.COIN_BTC
    ).aggregate(
        total=Sum('change_ratio')
    ).get("total")
    message_dict = {
        "current_price": float(instance.price),
        "symbol": instance.coin.symbol,
        "change_value": float(instance.change),
        "created": instance.created.strftime(change_time_format),
        "change_ratio": float(Decimal(instance.change_ratio).quantize(Decimal('0.00000'))),
        "total_change": float(Decimal(total_change).quantize(Decimal('0.00000'))),
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"coin_stream", {
            "type": "send_message_to_ws",
            "message": message_dict
        }
    )


post_save.connect(send_current_coin_price_to_websocket)
