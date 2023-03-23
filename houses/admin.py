from django.contrib import admin
from .models import House, Gu_list, Dong_list, Option, Safetyoption


@admin.action(description="Delete None Image House")
def delete_house(model_admin, request, houses):
    for room in houses:
        if room.Image.all().count() == 0:
            print(room)
            room.delete()


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    actions = (delete_house,)

    list_filter = (
        "room_kind",
        "sell_kind",
    )
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
        (
            "Option",
            {
                "fields": (
                    "option",
                    "Safetyoption",
                ),
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
class DongAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = (
        "pk",
        "gu",
        "name",
    )
    list_filter = ("gu",)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = (
        "pk",
        "name",
    )
    list_filter = ("name",)


@admin.register(Safetyoption)
class Safetyoption(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = (
        "pk",
        "name",
    )
    list_filter = ("name",)
