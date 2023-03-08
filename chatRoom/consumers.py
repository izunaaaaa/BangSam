# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from users.models import User
from .models import ChatRoom, Message
from .serializers import MessageSerializer
from users.serializers import TinyUserSerializer
from django.utils import timezone


class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json.get("text")
        sender = text_data_json.get("sender")
        type = text_data_json.get("type")
        try:
            user = User.objects.get(username=sender)
            self.user = user
        except User.DoesNotExist:
            return
        room = Chatting_Room.objects.get(pk=self.room_name)
        if not type:
            msg = Message.objects.create(text=text, sender=user, room=room)
            user = TinyUserSerializer(user).data

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": text,
                    "sender": user,
                    "time": msg.created_at.astimezone(
                        timezone.get_current_timezone()
                    ).strftime("%H:%M"),
                },
            )
            # Update chat list with new last message
            last_message = text
            for user in room.users.all():
                chat_room = user.username + "_notifications"
                unread_message = Message.objects.filter(
                    room=room,
                    is_read=False,
                ).exclude(sender=user)
                unread_count = unread_message.count()
                async_to_sync(self.channel_layer.group_send)(
                    chat_room,
                    {
                        "type": "new_data",
                        "text": last_message,
                        "room_id": room.id,
                        "unread_count": unread_count,
                        "updated_at": room.updated_at.strftime("%Y-%m-%d"),
                    },
                )

        elif type == "read_msg":
            dict_data = text_data_json
            room = Chatting_Room.objects.get(pk=dict_data.get("room"))
            for user in room.users.all():
                if user.username != dict_data.get("sender"):
                    async_to_sync(self.channel_layer.group_send)(
                        user.username + "_notifications",
                        {
                            "type": "update_read",
                            "sender": dict_data.get("sender"),
                        },
                    )
                # else:
                #     async_to_sync(self.channel_layer.group_send)(
                #         user.username + "_notifications",
                #         {
                #             "type": "update_count",
                #         },
                #     )
        #     unread_message = Message.objects.filter(room=room, is_read=False).exclude(
        #         sender=self.user
        #     )
        #     unread_message.update(is_read=True)
        #     unread_count = unread_message.count()
        #     async_to_sync(self.channel_layer.group_send)(
        #         self.user.username + "_notifications",
        #         {
        #             "type": "unread_data",
        #             "unread_count": unread_count,
        #             "room_id": room.id,
        #         },
        #     )

    def chat_message(self, event):
        text = event["message"]
        sender = event["sender"]
        time = str(event["time"])
        print(time)
        self.send(text_data=json.dumps({"text": text, "sender": sender, "time": time}))


from .models import Message, Chatting_Room


class NotificationConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.notification_group_name = None

    def connect(self):

        user_pk = self.scope["query_string"]
        result = user_pk.decode("utf-8")
        result = result[5:]
        try:
            self.user = User.objects.get(pk=result)
        except User.DoesNotExist:
            return

        # set notification group name
        self.notification_group_name = self.user.username + "_notifications"
        self.accept()

        # add channel to notification group
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

    def receive(self, text_data):
        dict_data = eval(text_data)
        if dict_data.get("room"):
            room = Chatting_Room.objects.get(pk=dict_data.get("room"))
        else:
            return
        for user in room.users.all():
            if user.username != dict_data.get("sender"):
                async_to_sync(self.channel_layer.group_send)(
                    user.username + "_notifications",
                    {
                        "type": "update_read",
                        "sender": dict_data.get("sender"),
                    },
                )
            # else:
            #     async_to_sync(self.channel_layer.group_send)(
            #         user.username + "_notifications",
            #         {
            #             "type": "update_count",
            #         },
            #     )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(code)

    def new_data(self, event):
        self.send_json(event)

    def unread_data(self, event):
        self.send_json(event)

    def update_read(self, event):
        self.send_json(event)

    def update_count(self, event):
        self.send_json(event)
