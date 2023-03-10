from django.contrib import admin
from .models import HouseList


@admin.register(HouseList)
class HouseListAdmin(admin.ModelAdmin):
    list_display = ("pk",)
