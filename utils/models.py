from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, help_text="creation datetime")
    updated_at = models.DateTimeField(auto_now=True, help_text="updated datetime")

    class Meta:
        abstract = True

    @classmethod
    def get_fields(cls, excludes=[], extras=[]):
        fields = [
            field.name for field in cls._meta.get_fields() if field.name not in excludes
        ]

        if extras:
            fields.extend(extras)

        return list(dict.fromkeys(fields))


class ExtraBaseModel(BaseModel):
    deleted_at = models.DateTimeField(
        null=True, blank=True, help_text="deleted datetime"
    )
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
        help_text="user performing create action",
    )
    approved_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_approved_by",
        help_text="user performing approve action",
    )
    cancelled_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_cancelled_by",
        help_text="user performing cancell action",
    )
    deleted_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_deleted_by",
        help_text="user performing delete action",
    )

    class Meta:
        abstract = True
