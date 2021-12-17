from django.contrib import admin

from notifications.models import Subscription, Notification

admin.site.register(Subscription)
admin.site.register(Notification)