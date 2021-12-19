from django.contrib import admin

from wallet.models import Wallet, CoinAsset

admin.site.register(Wallet)
admin.site.register(CoinAsset)
