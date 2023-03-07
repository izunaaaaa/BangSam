from django.urls import path
from . import views

urlpatterns = [
    path("", views.Houses.as_view()),
    path("<int:pk>", views.HouseDetail.as_view()),
    path("delete", views.Delete.as_view()),
]
