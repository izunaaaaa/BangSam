from django.urls import path
from . import views

urlpatterns = [
    path("", views.Houses.as_view()),
    path("<int:pk>", views.HouseDetail.as_view()),
    path("gulist", views.GuList.as_view()),
    path("<int:pk>/donglist", views.DongList.as_view()),
    path("deleteroom", views.DeleteRoom.as_view()),
    path("<int:pk>/changesell", views.ChangeSell.as_view()),
]
