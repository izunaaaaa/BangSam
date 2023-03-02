from django.urls import path
from . import views

urlpatterns = [
    path("", views.Reviews.as_view()),
]
