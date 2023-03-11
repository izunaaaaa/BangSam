from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.UserMe.as_view()),
    path("login/", views.LogIn.as_view()),
    path("checkID/", views.CheckID.as_view()),
    path("signup/", views.SignUp.as_view()),
    path("check-validate/", views.CheckValidate.as_view()),
    path("logout/", views.LogOut.as_view()),
    path("changepassword/", views.ChangePassword.as_view()),
    path("@<str:username>/", views.UserDetail.as_view()),
]
