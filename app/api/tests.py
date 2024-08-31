import json
from freezegun import freeze_time
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from datetime import datetime
from api.models import User, Member


class GetBirthdaysOfTheDayTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="12345678")
        self.client.force_authenticate(self.user)
        self.today = datetime(day=5, month=5, year=2024)

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
        member = Member.objects.create(
            name="test",
            profile_picture="",
            phone_number="1345678910",
            birth_date=datetime(day=self.today.day, month=self.today.month, year=1990),
        )
        # when
        with freeze_time(lambda: self.today):
            res = self.client.get(reverse("api:get_birthdays_of_the_day"))
        # then
        res_data = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_data["birthday_members"]), 1)
        self.assertEqual(res_data["birthday_members"][0]["name"], member.name)

    def test_should_get_just_the_birthday_members(self):
        # given we have multiple members, but just one member is having birthday today
        member1 = Member.objects.create(
            name="test1",
            profile_picture="",
            phone_number="1345678910",
            birth_date=datetime(day=self.today.day, month=self.today.month, year=1990),
        )
        member2 = Member.objects.create(
            name="test2",
            profile_picture="",
            phone_number="1345678910",
            birth_date=datetime(day=10, month=10, year=1990),
        )

        # when
        with freeze_time(lambda: self.today):
            res = self.client.get(reverse("api:get_birthdays_of_the_day"))
        # then
        res_data = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_data["birthday_members"]), 1)
        self.assertEqual(res_data["birthday_members"][0]["name"], member1.name)
