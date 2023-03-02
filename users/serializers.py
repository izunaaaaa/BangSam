from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "first_name",
            "last_name",
            "date_joined",
            "avatar",
            "groups",
            "user_permissions",
        )
