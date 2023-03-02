from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.UserMe.as_view()),
    path("@<str:username>/", views.UserDetail.as_view()),
]
