from django.db import models
from utils.models import BaseModel

from django.conf import settings as app_settings
from django.core.validators import MinValueValidator


class Merchant(BaseModel):
    code=models.PositiveIntegerField(
        unique=True,
        help_text=app_settings.HELPER_TEXT["merchant_code"],
        validators=[MinValueValidator(1000)]
    )
    name=models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text=app_settings.HELPER_TEXT['merchant_name'],
    )
    status = models.CharField(
        max_length=20,
        choices=app_settings.STATUS_CHOICES_MODEL,
        default="active",
        help_text=app_settings.HELPER_TEXT['merchant_status'],
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        db_table = "merchant_merchants"
        ordering = ["-created_at"]

    @classmethod
    def create_merchant(cls, code, name=None, status='active'):
        merchant = cls.objects.create(
            code=code,
            name=name,
            status=status
        )

        return merchant
