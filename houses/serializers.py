from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import House, Gu_list, Dong_list
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
        fields = (
            "id",
            "title",
            "thumnail",
            "room_kind",
            "deposit",
            "sell_kind",
            "sale",
            "monthly_rent",
            "thumnail",
        )


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
            "gu",
            "is_host",
            "is_sale",
            "title",
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

    def validate(self, data):

        room = data["room"]
        if room == None:
            raise ParseError("room not specified")

        toilet = data["toilet"]
        if toilet == None:
            raise ParseError("toilet not specified")

        pyeongsu = data["pyeongsu"]
        if pyeongsu == None:
            raise ParseError("pyeongsu not specified")

        sell_kind = data["sell_kind"]
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
