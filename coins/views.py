from django.shortcuts import render

from coins.models import CoinPriceChange


def dashboard(request):
    change_data = CoinPriceChange.get_last_change_data()
    return render(request, "index.html", context={"change_data": change_data})


def test(request):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"coin_stream", {
            "type": "send_message_to_ws",
            "message": dict(
                key="test ws message!"
            )
        }
    )
    return render(request, "index.html")
