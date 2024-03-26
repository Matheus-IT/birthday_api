from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


def hello_view(request):
    return JsonResponse({'msg': 'Salut!'})


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        print('email', email)
        password = request.data.get('password')
        print('password', password)
        user = authenticate(email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
