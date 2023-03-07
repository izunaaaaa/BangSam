from django.urls import path
from .views import ChattingList, ChattingRoomList

urlpatterns = [
    path("roomlist", ChattingRoomList.as_view()),
    path("<int:pk>/chatlist", ChattingList.as_view()),
]
