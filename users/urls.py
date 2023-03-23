from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.UserMe.as_view()),
    path("login/", views.LogIn.as_view()),
    path("naver/", views.NaverLogin.as_view()),
    path("kakao/", views.KakaoLogin.as_view()),
    path("checkID/", views.CheckID.as_view()),
    path("signup/", views.SignUp.as_view()),
    path("check-validate/", views.CheckValidate.as_view()),
    path("logout/", views.LogOut.as_view()),
    path("changepassword/", views.ChangePassword.as_view()),
    path("@<str:username>/", views.UserDetail.as_view()),
    path("selllist/all", views.AllSellList.as_view()),
    path("selllist/sell", views.SellList.as_view()),
    path("selllist/notsell", views.NotSellList.as_view()),
    path("find/id", views.FindId.as_view()),
    path("find/password", views.FindPassword.as_view()),
    path("new-password", views.NewPassword.as_view()),
]
