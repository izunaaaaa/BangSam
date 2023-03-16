# import app.routing
from django.urls import path
from chatRoom.consumers import TextRoomConsumer, NotificationConsumer

websocket_urlpatterns = [
    path("ws/<str:room_name>", TextRoomConsumer.as_asgi()),
    path("notifications", NotificationConsumer.as_asgi()),
]
