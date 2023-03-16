from django.urls import path
from .views import ChattingList, ChattingRoomList, ChattingRoom

urlpatterns = [
    path("", ChattingRoomList.as_view()),
    path("<int:pk>", ChattingRoom.as_view()),
    path("<int:pk>/chatlist", ChattingList.as_view()),
]
