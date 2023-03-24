from django.urls import path
from . import views

urlpatterns = [
    path("", views.Houses.as_view()),
    path("topview", views.TopView.as_view()),
    path("<int:pk>", views.HouseDetail.as_view()),
    path("gulist", views.GuList.as_view()),
    path("<int:pk>/donglist", views.DongList.as_view()),
    path("<int:pk>/changesell", views.ChangeSell.as_view()),
    path("options", views.All_Option.as_view()),
    path("safety-options", views.All_Safety_Option.as_view()),
]
