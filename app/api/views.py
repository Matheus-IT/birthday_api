from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from api.models import Member
from api.serializers import MemberSerializer
from rest_framework.viewsets import ModelViewSet
from datetime import datetime


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=400)


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Member will have the same department as the manager's
        data = request.data.copy()
        data["department"] = request.user.manager.department.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        manager_department = request.user.manager.department
        queryset = queryset.filter(department=manager_department)
        queryset = self._sort_by_birth_date(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def _sort_by_birth_date(self, queryset):
        """
        Sort members by birth date (month and day), so the ones with upcoming birthdays appear first.
        And if the birthday already happened this year, it should appear at the end of the list.
        """
        now = datetime.now().date()

        for m in queryset:
            days_for_birthday = (m.birth_date.replace(year=now.year) - now).days
            if days_for_birthday < 0:
                days_for_birthday += 365  # Consider next year if birthday already happened
            m.days_for_birthday = days_for_birthday

        return sorted(queryset, key=lambda m: m.days_for_birthday)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_birthdays_of_the_day(request):
    now = datetime.now()
    birthday_members = Member.objects.filter(
        birth_date__day=now.day,
        birth_date__month=now.month,
        department=request.user.manager.department,
    )

    member_serializer = MemberSerializer(birthday_members, many=True)

    return Response({"birthday_members": member_serializer.data})


def birthdays_of_the_day_test(request):
    from collections import namedtuple

    p = namedtuple("Person", ["name"])
    birthday_people = [p("maria"), p("joão"), p("carlos")]
    # birthday_people = [p("mario")]
    return render(
        request,
        "api/birthdays_of_the_day.html",
        {"birthday_people_names": [p.name.upper() for p in birthday_people]},
    )
