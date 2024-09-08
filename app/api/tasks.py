from celery import shared_task
from django.core.management import call_command


@shared_task
def call_notify_birthdays():
    call_command("notify_birthdays")
