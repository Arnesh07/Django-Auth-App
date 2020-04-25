from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # Overriding the create method to hash passwords.
    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        user.save()
        return user
