from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError
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
            "pk",
            "name",
        )


class TinyHouseSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = ("id", "title")


class HouseSerializer(ModelSerializer):

    Image = ImageSerializer(many=True, read_only=True)
    dong = DonglistSerializer()
    host = TinyUserSerializer(read_only=True)

    class Meta:
        model = House
        fields = (
            "visited",
            "id",
            "host",
            "is_sale",
            "title",
            "gu",
            "dong",
            "room_kind",
            "sell_kind",
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
            "thumnail",
            "Image",
        )

    # def validate_room(self,room):
    def validate(self, data):

        dong_name = data.get("dong", {}).get("name")
        if dong_name:
            try:
                dong_list = Dong_list.objects.get(name=dong_name)
            except Dong_list.DoesNotExist:
                raise serializers.ValidationError("Invalid dong name")

            data["dong"] = dong_list

        if not data.get("room"):
            raise ParseError("room not specified")

        if not data.get("pyeongsu"):
            raise ParseError("pyeongsu not specified")

        if data.get("toilet") == None:
            raise ParseError("toilet not specified")

        sell_kind = data.get("sell_kind")
        if sell_kind == "SALE":
            if not data.get("sale") or data.get("deposit") or data.get("monthly_rent"):
                raise ParseError("sale error")

        if sell_kind == "CHARTER":
            if not data.get("deposit") or data.get("sale") or data.get("monthly_rent"):
                raise ParseError("deposit error")

        if sell_kind == "MONTHLY_RENT":
            if (
                not data.get("monthly_rent")
                or not data.get("deposit")
                or data.get("sale")
            ):
                raise ParseError("monthly_rent error")
        return data
