from django.urls import path
from .views import GetUploadURL

urlpatterns = [
    path("geturl", GetUploadURL.as_view()),
]
