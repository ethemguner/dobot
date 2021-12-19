from django.db import models


class CoinAsset(models.Model):
    class Meta:
        verbose_name = "Coin Asset"
        verbose_name_plural = "Coin Assets"

    coin = models.ForeignKey(
        to="coins.Coin",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    balance = models.DecimalField(
        verbose_name="Coin Balance",
        max_digits=19,
        decimal_places=11,
        default=0
    )
    wallet = models.ForeignKey(
        to="wallet.Wallet",
        verbose_name="Wallet With",
        null=True,
        blank=False,
        related_name="coin_assets",
        on_delete=models.CASCADE
    )

    def __str__(self):
        if self.coin and self.wallet:
            return f"{self.balance} {self.coin} {self.wallet.name}"
        else:
            return super(CoinAsset, self).__str__()


class Wallet(models.Model):
    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    total_balance = models.DecimalField(
        verbose_name="Total Balance",
        max_digits=19,
        decimal_places=11
    )
    name = models.CharField(
        verbose_name="Wallet Name",
        max_length=255,
        null=False,
        blank=False,
        default="A wallet"
    )
    # TODO: we will identify binance wallet through this field in future.
    wallet_identifier = models.CharField(
        verbose_name="Wallet Identifier",
        max_length=255,
        null=True,
        blank=True,
    )
    decision_setting = models.ManyToManyField(
        to="decision_maker.DecisionSetting",
        blank=True,
        verbose_name="Decision Settings of Wallet",
        related_name="wallets"
    )

    def __str__(self):
        return self.name
