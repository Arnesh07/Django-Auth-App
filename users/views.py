from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView 
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

import requests

from .constants import OAUTH2_DEV_TOKEN_URL
from .models import User
from .private_constants import CLIENT_ID, CLIENT_SECRET
from .serializers import UserSerializer

class SignupView(generics.CreateAPIView):
    # Signup is available to every user.
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()

class LoginView(APIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        response = requests.post(OAUTH2_DEV_TOKEN_URL,
            data = {
                'grant_type': 'password',
                'username': email,
                'password': password,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            }
        )
        return Response(response.json())

class HomePageView(APIView):
    # Restricted to authenticated users only.
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        return HttpResponse('Home Page')
