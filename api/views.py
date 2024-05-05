from django.contrib.auth import authenticate
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_birthdays_of_the_day(request):
    now = datetime.now()
    birthday_members = Member.objects.filter(
        birth_date__day=now.day, birth_date__month=now.month
    )

    if not birthday_members.exists():
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    member_serializer = MemberSerializer(birthday_members, many=True)

    return Response({"birthday_members": member_serializer.data})
