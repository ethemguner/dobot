from django.contrib import admin

from coins.models import Coin, CoinPriceChange

admin.site.register(Coin)
admin.site.register(CoinPriceChange)
