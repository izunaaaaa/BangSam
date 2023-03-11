from rest_framework import serializers
from .models import HouseList


class HouseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseList
        fields = "__all__"
