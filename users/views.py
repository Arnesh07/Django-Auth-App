from django.shortcuts import render
from rest_framework import generics, permissions

from .serializers import UserSerializer
from .models import User

class SignupView(generics.CreateAPIView):
    # Signup is available to every user.
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()
