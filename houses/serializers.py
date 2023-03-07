from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import House

# from . import serializers


class HouseSerializer(ModelSerializer):
    class Meta:
        model = House
        # fields = "__all__"
        exclude = ("updated_at",)


class HouseDetailSerializer(ModelSerializer):

    # wishlist = serializers.WishlistSerializer(read_only=True)

    class Meta:
        model = House
        exclude = ("updated_at",)
