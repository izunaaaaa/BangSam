from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from .models import House, Gu_list, Dong_list, Option, Safetyoption
from images.serializers import ImageSerializer
from users.serializers import TinyUserSerializer
from wishlists.models import Wishlist
from drf_yasg import openapi


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = ("name",)


class SafetyOptionSerializer(ModelSerializer):
    class Meta:
        model = Safetyoption
        fields = ("name",)


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
            "is_sale",
        )


class HouseSerializer(ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    dong = DonglistSerializer(read_only=True)

    class Meta:
        model = House
        fields = (
            "id",
            "title",
            "thumnail",
            "room_kind",
            "deposit",
            "sell_kind",
            "gu",
            "dong",
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
    option = OptionSerializer(many=True, read_only=True)
    Safetyoption = SafetyOptionSerializer(many=True, read_only=True)

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
            "address",
            "description",
            "Image",
            "is_host",
            "option",
            "Safetyoption",
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
                raise ValidationError("no sale or deposit / monthly_rent is exist")

        if sell_kind == "CHARTER":
            if not data.get("deposit") or data.get("sale") or data.get("monthly_rent"):
                raise ValidationError("no deposit or no sale or monthly_rent is exist")

        if sell_kind == "MONTHLY_RENT":
            if (
                not data.get("monthly_rent")
                or not data.get("deposit")
                or data.get("sale")
            ):
                raise ValidationError("no monthly_rent or no deposit or sale is exist")
        return data

    def validate_room(self, data):
        if data == None or data < 0:
            raise ValidationError("room data must be required")
        return data

    def validate_pyeongsu(self, data):
        if data == None or data < 0:
            raise ValidationError("pyeongsu data must be required")
        return data

    def validate_toilet(self, data):
        if data == None or data < 0:
            raise ValidationError("toilet data must be required")
        return data

    def validate_maintenance_cost(self, data):
        if data == None or data < 0:
            raise ValidationError("Maintenance cost data must be required")
        return data

    def validate_sale(self, data):
        if data <= 0:
            raise ValidationError("sale data must be greater than 0")
        return data

    def validate_deposit(self, data):
        if data <= 0:
            raise ValidationError("deposit data must be greater than 0")
        return data

    def validate_monthly_rent(self, data):
        if data <= 0:
            raise ValidationError("monthly_rent data must be greater than 0")
        return data
