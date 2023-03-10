from rest_framework import serializers
from .models import Houselist


class HouseListSerializer(serializers.ModelSerializer):
    model = Houselist
    fields = "__all__"
