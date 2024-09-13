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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        manager_department = request.user.manager.department
        queryset = queryset.filter(department=manager_department)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_birthdays_of_the_day(request):
    now = datetime.now()
    birthday_members = Member.objects.filter(
        birth_date__day=now.day, birth_date__month=now.month
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
