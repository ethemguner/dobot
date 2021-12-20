from django.db import models


class Transaction(models.Model):
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    TYPE_SELL = "SELL"
    TYPE_BUY = "BUY"

    TRANSACTION_TYPES = (
        (TYPE_SELL, "Sell"),
        (TYPE_BUY, "Buy")
    )

    transaction_type = models.CharField(
        max_length=255,
        verbose_name="Transaction Type",
        choices=TRANSACTION_TYPES,
        null=True,
        blank=True
    )
    money_amount = models.DecimalField(
        verbose_name="Money Amount Transacted",
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )
    coin_amount = models.DecimalField(
        verbose_name="Coin Amount Transacted",
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )
    commission_amount = models.DecimalField(
        verbose_name="Commission Amount",
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )
    coin = models.ForeignKey(
        to="coins.Coin",
        verbose_name="Coin Transacted",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        to="wallet.Wallet",
        verbose_name="Wallet Transacted",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    decision = models.ForeignKey(
        to="decision_maker.Decision",
        verbose_name="Decision Info",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        null=True
    )

    def __str__(self):
        message = "{} action for {} while price is {} in {} | ".format(
            self.transaction_type,
            self.coin.symbol,
            self.decision.price_level,
            self.wallet.name
        )
        if self.transaction_type == self.TYPE_BUY:
            message += "Bought coin amount: %s" % str(self.coin_amount)
        else:
            message += "Sold coin amount: %s" % str(self.coin_amount)
        return message
