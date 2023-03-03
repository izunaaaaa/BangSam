from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import House


class HouseSerializer(ModelSerializer):
    class Meta:
        model = House
        # fields = "__all__"
        exclude = ("updated_at",)


class HouseDetailSerializer(ModelSerializer):
    class Meta:
        model = House
        exclude = ("updated_at",)
