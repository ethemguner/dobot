from django.db import models


class Subscription(models.Model):
    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    email = models.EmailField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name="Email subscribed"
    )
    target_coins = models.ManyToManyField(
        to="coins.Coin",
        blank=True,
        verbose_name="Coins targeted"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Is active?"
    )
    lowest_ratio_point = models.DecimalField(
        verbose_name="Lowest Ratio Point",
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )
    highest_ratio_point = models.DecimalField(
        verbose_name="Highest Ratio Point",
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True
    )

    def __str__(self):
        info = f"{self.email} "
        for coin in self.target_coins.all():
            info = f"{info} {coin}->{coin.current_price}"

        return info

class Notification(models.Model):
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    subject = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        default="Notification from Dobot."
    )
    content = models.CharField(
        max_length=1500,
        null=True,
        blank=False
    )
    subscription = models.ForeignKey(
        to="notifications.Subscription",
        null=False,
        blank=False,
        verbose_name="Subscription",
        on_delete=models.CASCADE
    )
