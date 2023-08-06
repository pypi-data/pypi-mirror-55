from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    name = "impression.settings_app"
    label = "impression_settings"
    verbose_name = "Impression Settings"

    def ready(self):
        from .models import ImpressionSettings

        ImpressionSettings.init()
