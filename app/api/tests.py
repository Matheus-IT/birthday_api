import json
from freezegun import freeze_time
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from datetime import datetime
from api.models import User, Member, Manager, Department, Organization


TODAY = datetime(day=5, month=5, year=2024)


def create_member1(birthday_today):
    return Member.objects.create(
        name="test1",
        profile_picture="",
        phone_number="1345678910",
        birth_date=datetime(
            day=TODAY.day if birthday_today else 10,
            month=TODAY.month if birthday_today else 10,
            year=1990,
        ),
    )


def create_member2(birthday_today):
    return Member.objects.create(
        name="test2",
        profile_picture="",
        phone_number="1345678911",
        birth_date=datetime(
            day=TODAY.day if birthday_today else 11,
            month=TODAY.month if birthday_today else 11,
            year=1995,
        ),
    )


class GetBirthdaysOfTheDayTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="12345678")
        Manager.objects.create(
            auth=self.user,
            department=Department.objects.create(
                name="test department",
                organization=Organization.objects.create(
                    name="test organization",
                ),
            ),
        )
        self.client.force_authenticate(self.user)

    def test_should_not_get_birthdays_when_theres_none(self):
        # given that we don't have birthdays today
        # when
        res = self.client.get(reverse("api:get_birthdays_of_the_day"))
        # then
        res_data = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_data["birthday_members"]), 0)

    def test_should_get_one_birthday_member(self):
        # given one member is having birthday today
        member = create_member1(birthday_today=True)
        # when
        with freeze_time(lambda: TODAY):
            res = self.client.get(reverse("api:get_birthdays_of_the_day"))
        # then
        res_data = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_data["birthday_members"]), 1)
        self.assertEqual(res_data["birthday_members"][0]["name"], member.name)

    def test_should_get_just_the_birthday_members(self):
        # given we have multiple members, but just one member is having birthday today
        member1 = create_member1(birthday_today=True)
        member2 = create_member2(birthday_today=False)

        # when
        with freeze_time(lambda: TODAY):
            res = self.client.get(reverse("api:get_birthdays_of_the_day"))
        # then
        res_data = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_data["birthday_members"]), 1)
        self.assertEqual(res_data["birthday_members"][0]["name"], member1.name)
