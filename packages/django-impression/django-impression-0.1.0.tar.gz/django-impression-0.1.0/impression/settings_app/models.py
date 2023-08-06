from settings_model.models import SettingsModel

from django.core.validators import MaxValueValidator
from django.db import models


class ImpressionSettings(SettingsModel):
    """
    Custom Django settings, customized for Impression Standalone.
    """

    default_service = models.CharField(max_length=255, blank=True, default="default")
    email_host = models.CharField(max_length=255, blank=True, default="localhost")
    email_port = models.PositiveIntegerField(
        default=25, validators=[MaxValueValidator(65535)]
    )
    email_username = models.CharField(max_length=255, blank=True)
    email_password = models.CharField(max_length=255, blank=True)

    __settings_filename__ = "impression_settings.py"
    __settings_map__ = [
        ("default_service", "IMPRESSION_DEFAULT_SERVICE", True, True),
        ("email_host", "EMAIL_HOST", True, True),
        ("email_port", "EMAIL_PORT", True, True),
        ("email_username", "EMAIL_HOST_USER", True, True),
        ("email_password", "EMAIL_HOST_PASSWORD", True, True),
    ]

    class Meta:
        verbose_name = verbose_name_plural = "Impression Settings"

    def encode_setting(self, field):
        return field.__repr__()
