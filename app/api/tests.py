import json
from freezegun import freeze_time
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from datetime import datetime
from api.models import User, Member, Manager, Department, Organization


class GetBirthdaysOfTheDayTests(APITestCase):
    def setUp(self):
        self.TODAY = datetime(day=5, month=5, year=2024)

        self.user = User.objects.create(email="test@test.com", password="12345678")
        self.test_department = Department.objects.create(
            name="test department",
            organization=Organization.objects.create(
                name="test organization",
            ),
        )
        Manager.objects.create(
            auth=self.user,
            department=self.test_department,
        )
        self.client.force_authenticate(self.user)

    def create_member1(self, birthday_today):
        return Member.objects.create(
            name="test1",
            profile_picture="",
            phone_number="1345678910",
            birth_date=datetime(
                day=self.TODAY.day if birthday_today else 10,
                month=self.TODAY.month if birthday_today else 10,
                year=1990,
            ),
            department=self.test_department,
        )

    def create_member2(self, birthday_today):
        return Member.objects.create(
            name="test2",
            profile_picture="",
            phone_number="1345678911",
            birth_date=datetime(
                day=self.TODAY.day if birthday_today else 11,
                month=self.TODAY.month if birthday_today else 11,
                year=1995,
            ),
            department=self.test_department,
        )

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
        member = self.create_member1(birthday_today=True)
        # when
        with freeze_time(lambda: self.TODAY):
            res = self.client.get(reverse("api:get_birthdays_of_the_day"))
        # then
        res_data = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_data["birthday_members"]), 1)
        self.assertEqual(res_data["birthday_members"][0]["name"], member.name)

    def test_should_get_just_the_birthday_members(self):
        # given we have multiple members, but just one member is having birthday today
        member1 = self.create_member1(birthday_today=True)
        member2 = self.create_member2(birthday_today=False)

        # when
        with freeze_time(lambda: self.TODAY):
            res = self.client.get(reverse("api:get_birthdays_of_the_day"))
        # then
        res_data = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_data["birthday_members"]), 1)
        self.assertEqual(res_data["birthday_members"][0]["name"], member1.name)

    def test_should_get_members_from_department_of_manager(self):
        """
        Should get members having birthday today only that are from the department of the manager
        """
        # given we have multiple members, but just one member is having birthday today
        member1 = self.create_member1(birthday_today=True)
        member2 = self.create_member2(birthday_today=False)

        # when
        with freeze_time(lambda: self.TODAY):
            res = self.client.get(reverse("api:get_birthdays_of_the_day"))
        # then
        res_data = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_data["birthday_members"]), 1)
        self.assertEqual(res_data["birthday_members"][0]["name"], member1.name)


class MemberViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="12345678")
        self.manager_department = Department.objects.create(
            name="test department",
            organization=Organization.objects.create(
                name="test organization",
            ),
        )
        Manager.objects.create(
            auth=self.user,
            department=self.manager_department,
        )
        self.client.force_authenticate(self.user)

    def test_should_create_member_with_department_of_manager(self):
        # given
        payload = {
            "name": "test member",
            "profile_picture": "",
            "phone_number": "12345678910",
            "birth_date": "2024-05-05",
        }
        # when
        res = self.client.post(reverse("api:member-list"), data=payload)
        # then
        res_data = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_data["department"], self.manager_department.pk)

    def test_should_succeed_when_manager_delete_member_of_his_department(self):
        # given
        m = Member.objects.create(
            name="test1",
            profile_picture="",
            phone_number="1345678910",
            birth_date=datetime(
                day=10,
                month=10,
                year=1990,
            ),
            department=self.manager_department,
        )
        # when
        res = self.client.delete(reverse("api:member-detail", kwargs={"pk": m.id}))
        # then
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Member.objects.filter(id=m.id).exists())
