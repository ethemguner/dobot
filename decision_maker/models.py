from django.db import models

from wallet.models import Wallet


class Decision(models.Model):
    class Meta:
        verbose_name = "Decision"
        verbose_name_plural = "Decisions"

    TYPE_SELL = "SELL"
    TYPE_BUY = "BUY"

    DECIDE_TYPES = (
        (TYPE_BUY, "Buy"),
        (TYPE_SELL, "Sell"),
    )

    coin = models.ForeignKey(
        to="coins.Coin",
        verbose_name="Coin to Decide",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    price_level = models.DecimalField(
        verbose_name="Decided Price Level",
        max_digits=19,
        decimal_places=2
    )
    type_of_decision = models.CharField(
        verbose_name="Type of Decision",
        max_length=255,
        null=True,
        blank=True,
        choices=DECIDE_TYPES
    )
    income_ratio = models.DecimalField(
        verbose_name="Income by Decision",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    wallet = models.ForeignKey(
        to="wallet.Wallet",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Wallet Decided"
    )
    created = models.DateTimeField

    def __str__(self):
        if self.wallet:
            return f"[{self.coin.symbol}] " \
                   f"({self.wallet.name}) " \
                   f"{self.type_of_decision} from {self.price_level} " \
                   f"| {self.wallet.name}"
        else:
            return f"[{self.coin.symbol}] " \
                   f"({self.wallet.name}) " \
                   f"{self.type_of_decision} from {self.price_level} " \
                   f"| no wallet defined"


class DecisionSetting(models.Model):
    class Meta:
        verbose_name = "Decision Setting"
        verbose_name_plural = "Decision Settings"

    entry_price_level = models.DecimalField(
        verbose_name="Entry Price Level",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=False
    )
    coin = models.ForeignKey(
        to="coins.Coin",
        verbose_name="Coin to Decide",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    ratio_to_sell = models.DecimalField(
        verbose_name="Ratio to Sell",
        max_digits=19,
        decimal_places=11,
    )
    ratio_to_buy = models.DecimalField(
        verbose_name="Ratio to Buy",
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )
    allocated_money_amount = models.DecimalField(
        verbose_name="Allocated Money",
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )
    dont_buy = models.BooleanField(
        default=False
    )
    dont_sell = models.BooleanField(
        default=False
    )

    def __str__(self):
        wallets = Wallet.objects.filter(decision_setting=self).values_list("name", flat=True)
        wallet_names = ",".join(wallets)
        message = "[{}] Price Level: {} | Allocated Money: {} ".format(
            self.coin.symbol,
            self.entry_price_level,
            self.allocated_money_amount
        )
        if not self.dont_buy and self.dont_sell:
            message += "| Buy if coin decreases %{} ".format(self.ratio_to_buy)
        elif self.dont_buy and not self.dont_sell:
            message += "| Sell if coin increases %{} ".format(self.ratio_to_sell)
        else:
            message += "| Passive state, do nothing. "

        if wallet_names:
            message += "({})".format(wallet_names)

        return message

    def get_action(self):
        if not self.dont_buy:
            action_value = (self.entry_price_level / 100) * self.ratio_to_buy
            action_value = self.entry_price_level + action_value
            return f"System will buy If {self.coin.symbol} will be {action_value}"
        if not self.dont_sell:
            action_value = (self.entry_price_level / 100) * self.ratio_to_sell
            action_value = self.entry_price_level + action_value
            return f"System will sell If {self.coin.symbol} will be {action_value}"
        return "System will do not take an action right now."
