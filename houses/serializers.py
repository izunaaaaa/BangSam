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
    class Meta:
        model = House
        fields = (
            "thumnail",
            "id",
            "is_host",
            # "host",
            "is_sale",
            "title",
            # "gu",
            # "dong",
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
            "visited",
        )


class HouseDetailSerializer(ModelSerializer):
    Image = ImageSerializer(many=True, read_only=True)
    dong = DonglistSerializer()
    host = TinyUserSerializer(read_only=True)

    class Meta:
        model = House
        fields = (
            "id",
            "is_host",
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
            "visited",
            "Image",
        )

    def update(self, instance, validated_data):
        # 중첩된 필드의 값을 가져옵니다.
        dong_data = validated_data.pop("dong", None)

        # instance의 값을 업데이트합니다.
        instance = super().update(instance, validated_data)

        # dong_data가 존재하면 Dong 객체를 업데이트합니다.
        if dong_data is not None:
            # dong_serializer = DonglistSerializer(instance.dong, data=dong_data)
            # dong_serializer.is_valid(raise_exception=True)
            # dong_serializer.save()
            dong_instance, _ = Dong_list.objects.get_or_create(pk=dong_data.get("pk"))
            dong_instance.name = dong_data.get("name")
            dong_instance.save()
            instance.dong = dong_instance

        return instance
