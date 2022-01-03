from django.db import models
from django.utils.translation import ugettext_lazy as _

from wallet.models import Wallet


class Decision(models.Model):
    class Meta:
        verbose_name = _("Decision")
        verbose_name_plural = _("Decisions")

    TYPE_SELL = "SELL"
    TYPE_BUY = "BUY"

    DECIDE_TYPES = (
        (TYPE_BUY, _("Buy")),
        (TYPE_SELL, _("Sell")),
    )

    coin = models.ForeignKey(
        to="coins.Coin",
        verbose_name=_("Coin to Decide"),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    price_level = models.DecimalField(
        verbose_name=_("Decided Price Level"),
        max_digits=19,
        decimal_places=2
    )
    type_of_decision = models.CharField(
        verbose_name=_("Type of Decision"),
        max_length=255,
        null=True,
        blank=True,
        choices=DECIDE_TYPES
    )
    income_ratio = models.DecimalField(
        verbose_name=_("Income by Decision"),
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    wallet = models.ForeignKey(
        to="wallet.Wallet",
        verbose_name=_("Wallet Decided"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name=_("Created at"),
        null=True,
        blank=False,
        auto_now_add=True
    )

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
        verbose_name = _("Decision Setting")
        verbose_name_plural = _("Decision Settings")

    entry_price_level = models.DecimalField(
        verbose_name=_("Entry Price Level"),
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=False
    )
    coin = models.ForeignKey(
        to="coins.Coin",
        verbose_name=_("Coin to Decide"),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    ratio_to_sell = models.DecimalField(
        verbose_name=_("Ratio to Sell"),
        max_digits=19,
        decimal_places=11,
    )
    ratio_to_buy = models.DecimalField(
        verbose_name=_("Ratio to Buy"),
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )
    allocated_money_amount = models.DecimalField(
        verbose_name=_("Allocated Money"),
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )
    dont_buy = models.BooleanField(
        verbose_name=_("Don't buy"),
        default=False
    )
    dont_sell = models.BooleanField(
        verbose_name=_("Don't sell"),
        default=False
    )
    active = models.BooleanField(
        verbose_name=_("Active"),
        default=True
    )

    @property
    def is_active(self):
        return self.active

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def __str__(self):
        wallets = Wallet.objects.filter(decision_setting=self).values_list("name", flat=True)
        wallet_names = ",".join(wallets)
        message = f"[{self.coin.symbol}]"
        message += f"Price Level: {self.entry_price_level} | "
        message += f"Allocated Money: {self.allocated_money_amount} "

        if self.is_active:
            if not self.dont_buy and self.dont_sell:
                message += f"| Buy if coin decreases %{self.ratio_to_buy} "
            elif self.dont_buy and not self.dont_sell:
                message += f"| Sell if coin increases %{self.ratio_to_sell} "
            else:
                message += "| Passive state, do nothing. "
        else:
            message += "| Disabled, do nothing. "

        if wallet_names:
            message += f"({wallet_names})"

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
        return _("System will do not take an action right now.")
