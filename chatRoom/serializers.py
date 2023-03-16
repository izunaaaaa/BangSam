from rest_framework import serializers
from .models import ChatRoom, Message
from users.serializers import TinyUserSerializer
from django.utils import timezone
from houses.serializers import TinyHouseSerializer


class ChatListSerializer(serializers.ModelSerializer):
    sender = TinyUserSerializer()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = (
            "id",
            "room",
            "updated_at",
            "created_at",
        )

    def get_time(self, obj):
        # Convert the created_at field to the desired format
        created_at = obj.created_at.astimezone(timezone.get_current_timezone())
        return created_at.strftime("%H:%M")


class ChatRoomListSerializer(serializers.ModelSerializer):
    users = TinyUserSerializer(read_only=True, many=True)
    unread_messages = serializers.SerializerMethodField()
    house = TinyHouseSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = (
            "id",
            "house",
            "lastMessage",
            "unread_messages",
            "users",
            "updated_at",
        )

    def get_unread_messages(self, obj):
        # Get the user associated with the request
        user = self.context["request"].user

        # Get the count of unread messages using Django ORM
        num_unread_messages = Message.objects.filter(
            room=obj,
            sender__in=obj.users.exclude(pk=user.pk),
            is_read=False,
        ).count()
        return num_unread_messages


class ChatRoomSerialzier(serializers.ModelSerializer):
    users = TinyUserSerializer(read_only=True, many=True)
    house = TinyHouseSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = TinyUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
