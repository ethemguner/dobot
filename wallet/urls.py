from django.urls import path

from .views import wallet_details

urlpatterns = [
    path("details/<int:wallet_id>", wallet_details, name="wallet-details"),
]
