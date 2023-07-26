from django.contrib import admin
from merchant.models import Merchant
from utils.admins import BaseAdmin


class MerchantAdmin(BaseAdmin):
    list_display = ["code", "name", "status"]

    ordering = ("-created_at",)
    search_fields = ("code", "name")


admin.site.register(Merchant, MerchantAdmin)
