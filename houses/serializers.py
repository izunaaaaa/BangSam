from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from .models import House, Gu_list, Dong_list
from images.serializers import ImageSerializer
from users.serializers import TinyUserSerializer
from wishlists.models import Wishlist
from drf_yasg import openapi


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
        )


class HouseSerializer(ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = (
            "id",
            "title",
            "thumnail",
            "room_kind",
            "deposit",
            "sell_kind",
            "address",
            "sell_kind",
            "sale",
            "monthly_rent",
            "thumnail",
            "is_liked",
        )

    def get_is_liked(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    house__pk=data.pk,
                ).exists()
        return False


class HouseDetailSerializer(ModelSerializer):

    Image = ImageSerializer(many=True, read_only=True)
    dong = DonglistSerializer(read_only=True)
    host = TinyUserSerializer(read_only=True)
    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

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
            "is_host",
            "is_liked",
        )

    def get_is_host(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return data.host == request.user
        return False

    def get_is_liked(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    house__pk=data.pk,
                ).exists()
        return False

    def validate(self, data):
        sell_kind = data.get("sell_kind")
        if sell_kind == "SALE":
            if not data.get("sale") or data.get("deposit") or data.get("monthly_rent"):
                if data.get("sale") < 0:
                    raise ValidationError("sale error")

        if sell_kind == "CHARTER":
            if not data.get("deposit") or data.get("sale") or data.get("monthly_rent"):
                if data.get("deposit") < 0:
                    raise ValidationError("deposit error")

        if sell_kind == "MONTHLY_RENT":
            if (
                not data.get("monthly_rent")
                or not data.get("deposit")
                or data.get("sale")
            ):
                if data.get("monthly_rent") < 0 or data.get("deposit"):
                    raise ValidationError("monthly_rent error")
        return data

    def validate_dong(self, data):
        dong_name = data
        if dong_name:
            try:
                dong_list = Dong_list.objects.get(name=dong_name)
            except Dong_list.DoesNotExist:
                raise ValidationError("Invalid dong name")

        return dong_list

    def validate_room(self, data):
        if data == None or data < 0:
            raise ValidationError("room not specified")
        return data

    def validate_pyeongsu(self, data):
        if data == None or data < 0:
            raise ValidationError("pyeongsu not specified")
        return data

    def validate_toilet(self, data):
        if data == None or data < 0:
            raise ValidationError("toilet not specified")
        return data

    def validate_maintenance_cost(self, data):
        if data == None or data < 0:
            raise ValidationError("Maintenance cost not specified")
        return data

    def validate_distance_to_station(self, data):
        if data == None or data < 0:
            raise ValidationError("Maintenance cost not specified")
        return data
