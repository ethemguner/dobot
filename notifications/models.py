from django.core.validators import MinLengthValidator, EmailValidator, DecimalValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subscription(models.Model):
    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    email = models.EmailField(
        verbose_name=_("Email subscribed"),
        null=False,
        blank=False,
        max_length=255,
        validators=[MinLengthValidator(5), EmailValidator()]
    )
    target_coins = models.ManyToManyField(
        to="coins.Coin",
        verbose_name=_("Coins targeted"),
        blank=True
    )
    active = models.BooleanField(
        verbose_name=_("Is active?"),
        default=True,
    )
    lowest_ratio_point = models.DecimalField(
        verbose_name=_("Lowest Ratio Point"),
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True,
        validators=[DecimalValidator(19, 11)]
    )
    highest_ratio_point = models.DecimalField(
        verbose_name=_("Highest Ratio Point"),
        max_digits=19,
        decimal_places=11,
        null=True,
        blank=True,
        validators=[DecimalValidator(19, 11)]
    )

    def __str__(self):
        info = f"{self.email} "
        for coin in self.target_coins.all():
            info = f"{info} {coin}->{coin.current_price}"

        return info


class Notification(models.Model):
    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    subject = models.CharField(
        verbose_name=_("Subject"),
        max_length=255,
        null=True,
        blank=False,
        default=_("Notification from Dobot."),
        validators=[MinLengthValidator(3), ]
    )
    content = models.TextField(
        verbose_name=_("Content"),
        null=True,
        blank=False
    )
    subscription = models.ForeignKey(
        verbose_name=_("Subscription"),
        to="notifications.Subscription",
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        verbose_name=_("Created at"),
        null=True,
        blank=False,
        auto_now_add=True
    )
    read = models.BooleanField(
        verbose_name=_("Has been read"),
        default=False
    )

    def __str__(self):
        return f"{self.subject}"
