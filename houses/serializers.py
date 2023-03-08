from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import House, Gu_list, Dong_list


class TinyHouseSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = ("id", "title")


class HouseSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = (
            "id",
            "gu",
            "title",
            "price",
            "room",
            "toilet",
            "pyeongsu",
            "distance_to_station",
            "room_kind",
            "cell_kind",
            "address",
            "photo",
            "description",
            "visited",
            "owner",
            "realtor",
            "dong",
        )


class HouseDetailSerializer(ModelSerializer):
    class Meta:
        model = House
        exclude = ("updated_at",)


class GulistSerializer(ModelSerializer):
    class Meta:
        model = Gu_list
        fields = (
            "pk",
            "name",
        )


class DonglistSerializer(ModelSerializer):
    class Meta:
        model = Dong_list
        fields = (
            "gu",
            "pk",
            "name",
        )
