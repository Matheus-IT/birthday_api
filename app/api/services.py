from firebase_admin import credentials, messaging
from api.models import Member
from datetime import datetime
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from decouple import config


def notify_birthdays_service():
    now = datetime.now()
    birthday_people = Member.objects.filter(
        birth_date__day=now.day, birth_date__month=now.month
    )

    if not birthday_people.exists():
        return

    birthday_people_truncated = birthday_people[:11]

    notification_body = build_notification_body(birthday_people_truncated)
    notification_title = build_notification_title(birthday_people_truncated)

    message = messaging.Message(
        notification=messaging.Notification(
            title=notification_title, body=notification_body
        ),
        topic="birthdays-of-the-day",
    )

    try:
        # Send the message
        response = messaging.send(message)
        # Check the response for any errors
        print("Successfully sent message:", response)

        recipient_list = config("EMAIL_RECIPIENT_LIST").split(",")

        email_body = render_to_string(
            "api/birthdays_of_the_day.html",
            {
                "birthday_people_names": [
                    p.name.upper() for p in birthday_people_truncated
                ]
            },
        )

        result = mail.send_mail(
            (
                "Aniversariantes do dia"
                if len(birthday_people_truncated) > 1
                else "Aniversariante do dia"
            ),
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            html_message=email_body,
            fail_silently=False,
        )
        print("result", result)
    except Exception as e:
        print("Error", e)


def get_recipient_list():
    # return config("EMAIL_RECIPIENT_LIST").split(",")
    pass


def build_notification_body(birthday_people):
    notification_body = ""
    n_of_people = len(birthday_people)

    if n_of_people == 1:
        return ""  # The name will be in the title, not in the body

    for i in range(n_of_people):
        # if there's more than the maximum and this is the last, show "..."
        if n_of_people > 10 and i == n_of_people - 1:
            notification_body += "..."
        else:
            notification_body += f"- {birthday_people[i].name.upper()}"

        if i < n_of_people - 1:
            notification_body += "\n"
    return notification_body


def build_notification_title(birthday_people):
    if len(birthday_people) == 1:
        birthday_member = birthday_people[0]
        return f"O aniversariante do dia é {birthday_member.name.upper()}!"
    return "Aniversariantes do dia!"
