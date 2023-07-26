from django.apps import AppConfig


class RechargeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recharge"

    def ready(self):
        import recharge.signals  # noqa: F401
