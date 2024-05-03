from django.core.management.base import BaseCommand
from decouple import config
import firebase_admin
from firebase_admin import credentials, messaging
from api.models import Member
from datetime import datetime


class Command(BaseCommand):
    help = "Sends request to notify users on firebase"

    def handle(self, *args, **options):
        cred = credentials.Certificate(config("FIREBASE_KEY_PATH"))
        firebase_admin.initialize_app(cred)

        now = datetime.now()
        birthday_people = Member.objects.filter(
            birth_date__day=now.day, birth_date__month=now.month
        )

        print("exists", birthday_people.exists())
        print("birthday_people", birthday_people)

        if not birthday_people.exists():
            return

        notification_body = ""

        for p in birthday_people:
            notification_body += f"{p.name} \n"

        message = messaging.Message(
            notification=messaging.Notification(
                title="Aniversariantes do dia", body=notification_body
            ),
            topic="birthdays-of-the-day",
        )

        try:
            # Send the message
            response = messaging.send(message)

            # Check the response for any errors
            print("Successfully sent message:", response)
        except Exception as e:
            print("Error", e)
