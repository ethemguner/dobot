from django.shortcuts import render

from transactions.models import Transaction
from wallet.models import Wallet


def wallet_details(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    context = {
        "coin_assets": wallet.coin_assets.all(),
        "total_balance": wallet.total_balance,
        "wallet": wallet,
        "decision_settings": wallet.decision_setting.all(),
        "transactions": Transaction.objects.filter(wallet=wallet)
    }
    return render(request, "wallet/details.html", context=context)
