from django.core.management.base import BaseCommand
from decouple import config
import firebase_admin
from firebase_admin import credentials, messaging


class Command(BaseCommand):
    help = "Sends request to notify users on firebase"

    def handle(self, *args, **options):

        cred = credentials.Certificate(config("FIREBASE_KEY_PATH"))
        firebase_admin.initialize_app(cred)

        message = messaging.Message(
            notification=messaging.Notification(
                title="Testando", body="Mensagem enviada do servidor"
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
