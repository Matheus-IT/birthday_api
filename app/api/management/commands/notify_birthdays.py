from django.core.management.base import BaseCommand
from api.services import notify_birthdays_service


class Command(BaseCommand):
    help = "Sends request to notify users on firebase"

    def handle(self, *args, **options):
        notify_birthdays_service()
