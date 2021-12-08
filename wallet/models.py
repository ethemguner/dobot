from django.db import models


class Wallet(models.Model):
    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    total_balance = models.DecimalField(
        verbose_name="Total Balance",
        max_digits=19,
        decimal_places=2
    )
    name = models.CharField(
        verbose_name="Wallet Name",
        max_length=255,
        null=True,
        blank=True
    )
    coin_balance = models.DecimalField(
        verbose_name="Coin Balance",
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
