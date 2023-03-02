from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "username",
                    "password",
                    "name",
                    "email",
                    "address",
                    "gender",
                ),
            },
        ),
        (
            "User Kind",
            {
                "fields": (
                    "is_host",
                    "is_custom",
                    "is_realtor",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )
    list_display = (
        "pk",
        "username",
        "name",
<<<<<<< HEAD
        "is_host",
        "is_custom",
        "is_realtor",
=======
        "username",
>>>>>>> d53453c2991c6da1dc5dc7dc201f1aef23dfa85b
    )
