from django.shortcuts import render

from coins.models import Coin
from transactions.models import Transaction
from wallet.models import Wallet


def dashboard(request):
    return render(
        request, "coins/dashboard.html", context={
            "coins": Coin.objects.all(),
            "transactions": Transaction.objects.all().order_by("-id"),
            "wallets": Wallet.objects.all(),
        }
    )


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
