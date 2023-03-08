from django.urls import path
from . import views

urlpatterns = [
    # path("", views.Users.as_view()),
    path("me/", views.UserMe.as_view()),
    # path("change-password", views.ChangePassword.as_view()),
    path("login/", views.LogIn.as_view()),
    # path("log-out", views.LogOut.as_view()),
    path("@<str:username>/", views.UserDetail.as_view()),
]
