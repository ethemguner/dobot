from django.db import models


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

    def __str__(self):
        return "{} from {}".format(self.type_of_decision, self.price_level)


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
        decimal_places=2,
    )
    ratio_to_buy = models.DecimalField(
        verbose_name="Ratio to Buy",
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True
    )
    dont_buy = models.BooleanField(
        default=True
    )
    dont_sell = models.BooleanField(
        default=True
    )

    def __str__(self):
        return "Price Level: {} - Sell Ratio: {} - Buy Ratio {}".format(
            self.entry_price_level,
            self.ratio_to_sell,
            self.ratio_to_buy,
        )

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
