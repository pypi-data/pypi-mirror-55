from django.contrib import admin

from .models import ImpressionSettings


@admin.register(ImpressionSettings)
class ImpressionSettingsAdmin(admin.ModelAdmin):
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_display = (
        "name",
        "is_active",
        "default_service",
        "email_host",
        "email_port",
        "email_username",
        "email_password",
    )
    fieldsets = (
        (None, {"fields": ("name", "is_active")}),
        ("Impression Settings", {"fields": ("default_service",)}),
        (
            "Email Settings",
            {
                "fields": (
                    "email_host",
                    "email_port",
                    "email_username",
                    "email_password",
                )
            },
        ),
    )
