from django.contrib import admin
from .models import House, Gu_list, Dong_list


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "owner",
        "realtor",
        "room_kind",
        "cell_kind",
        "visited",
    )


@admin.register(Gu_list)
class GuAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )


@admin.register(Dong_list)
class GuAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "gu",
        "name",
    )
    list_filter = ("gu",)
