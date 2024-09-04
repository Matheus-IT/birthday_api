from celery import shared_task
from django.core.management import call_command


@shared_task
def run_management_command():
    call_command("notify_birthdays")
