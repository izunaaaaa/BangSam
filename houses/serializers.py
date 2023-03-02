from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import House


class HouseSerializer(ModelSerializer):
    class Meta:
        model = House
        # fields = "__all__"
        exclude = (
            "created_at",
            "updated_at",
        )


class HouseDetailSerializer(ModelSerializer):
    class Meta:
        model = House
        exclude = (
            "created_at",
            "updated_at",
        )
