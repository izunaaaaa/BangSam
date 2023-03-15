from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import House, Gu_list, Dong_list
from houselists.serializers import HouseListSerializer
from images.serializers import ImageSerializer
from users.serializers import TinyUserSerializer


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
            # "gu",
            "pk",
            "name",
        )


class TinyHouseSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = ("id", "title")


class HouseSerializer(ModelSerializer):
    dong = DonglistSerializer(read_only=True)

    class Meta:
        model = House
        fields = (
            "id",
            "is_owner",
            "owner",
            "title",
            "gu",
            "dong",
            "room_kind",
            "cell_kind",
            "sale",
            "deposit",
            "monthly_rent",
            "maintenance_cost",
            "room",
            "toilet",
            "pyeongsu",
            "distance_to_station",
            "address",
            "description",
            "visited",
        )


class HouseDetailSerializer(ModelSerializer):
    Image = ImageSerializer(many=True, read_only=True)
    dong = DonglistSerializer(read_only=True)
    owner = TinyUserSerializer(read_only=True)

    class Meta:
        model = House
        fields = (
            "id",
            "is_owner",
            "owner",
            "title",
            "gu",
            "dong",
            "room_kind",
            "cell_kind",
            "sale",
            "deposit",
            "monthly_rent",
            "maintenance_cost",
            "room",
            "toilet",
            "pyeongsu",
            "distance_to_station",
            "address",
            "description",
            "visited",
            "Image",
        )
