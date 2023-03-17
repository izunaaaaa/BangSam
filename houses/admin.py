from django.contrib import admin
from .models import House, Gu_list, Dong_list


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    list_display = (
        "pk",
        "gu",
        "dong",
        "title",
        "host",
        "room_kind",
        "sell_kind",
        "visited",
    )

    fieldsets = (
        (
            "User Info",
            {
                "fields": ("host",),
            },
        ),
        (
            "Room Info",
            {
                "fields": (
                    "title",
                    "pyeongsu",
                    "dong",
                    "address",
                    "room_kind",
                    "room",
                    "toilet",
                    "distance_to_station",
                    "description",
                )
            },
        ),
        (
            "Cost Info",
            {
                "fields": (
                    "sell_kind",
                    "sale",
                    "deposit",
                    "monthly_rent",
                    "maintenance_cost",
                ),
            },
        ),
        (
            "Check Box",
            {
                "fields": ("is_sale",),
            },
        ),
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
