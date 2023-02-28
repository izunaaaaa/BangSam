from django.urls import path
from . import views

urlpatterns = [
    path("", views.Review.as_view()),
]
