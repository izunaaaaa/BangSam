from django.urls import path
from . import views

urlpatterns = [
    path("", views.HouseLists.as_view()),
]
