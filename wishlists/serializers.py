from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Wishlist
from users.serializers import TinyUserSerializer


class WishlistSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = "__all__"
