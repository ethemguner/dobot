import logging

from celery import Celery
from celery import shared_task
from django.core.mail import send_mass_mail

app = Celery('push_notifications_task', broker='pyamqp://guest@localhost//')

logger = logging.getLogger(__name__)


@shared_task
def push_notifications_task(notification_list):
    send_mass_mail(tuple(notification_list))
    return "push_notifications_task finished"
