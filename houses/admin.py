from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "owner",
        "realtor",
        "room_kind",
        "cell_kind",
        "visited",
    )
