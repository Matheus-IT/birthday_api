from io import StringIO
from django.core.management.base import BaseCommand
from decouple import config
import firebase_admin
from firebase_admin import credentials, messaging
from api.models import Member
from datetime import datetime
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from api.services import notify_birthdays_service


cred = credentials.Certificate(config("FIREBASE_KEY_PATH"))
firebase_admin.initialize_app(cred)


class Command(BaseCommand):
    help = "Sends request to notify users on firebase"

    def handle(self, *args, **options):
        notify_birthdays_service()
