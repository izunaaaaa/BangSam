from django.contrib import admin
from .models import Review


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "house",
    )
