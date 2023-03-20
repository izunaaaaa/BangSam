from rest_framework import serializers
from .models import HouseList

from houses.serializers import TinyHouseSerializer


class HouseListSerializer(serializers.ModelSerializer):
    recently_views = TinyHouseSerializer(read_only=True)

    class Meta:
        model = HouseList
        fields = ("recently_views",)
