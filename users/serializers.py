from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ParseError


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "avatar",
            "is_host",
        )


class PrivateUserSerializer(ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        exclude = (
            "avatar",
            "first_name",
            "last_name",
            "last_login",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
