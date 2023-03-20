from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Wishlist
from users.serializers import TinyUserSerializer
from houses.serializers import TinyHouseSerializer


class WishlistSerializer(serializers.ModelSerializer):
    house = TinyHouseSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ("house",)
