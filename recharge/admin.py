from django.utils.safestring import mark_safe

from recharge.models import Transaction
from utils.admins import BaseAdmin, admin


class TransactionAdmin(BaseAdmin):
    list_display = [
        "code",
        "type",
        "user_id",
        "to_address",
        "get_qr",
        "amount",
        "currency_symbol",
        "currency_std",
        "expired_at",
        "status",
    ]
    list_per_page = 15
    ordering = ("-created_at",)
    search_fields = ("user_id", "code", "to_address", "currency_symbol")

    _readonly_fields = [
        "code",
        "origin_code",
        "account",
        "wallet",
        "from_address",
        "to_address",
        "from_currency",
        "to_currency",
        "user_id",
        "currency_id",
        "currency_name",
        "currency_symbol",
        "currency_blockchain",
        "currency_std",
        "amount",
        "rate",
        "expired_at",
        "type",
        "deleted_at",
        "deleted_by",
        "approved_by",
        "cancelled_by",
        "created_by",
    ]

    list_filter = ("created_at", "status", "currency_symbol", "merchant__code", "type")

    @admin.display(ordering="wallet__attributs__address_qr", description="QR")
    def get_qr(self, obj):
        addrs = obj.wallet.address
        qr = obj.wallet.attributs.address_qr
        symbol = obj.wallet.currency_symbol
        std = obj.wallet.currency_std
        currency = symbol if not std else f"{symbol} - {std}"
        amount = obj.amount
        if qr:
            html_image = f"""
                <img
                    class="qr-image"
                    src="{qr}"
                    data-address="{addrs}"
                    data-amount="{amount}"
                    alt="{currency}"
                    height="10"
                    width="10"
                />
            """
            return mark_safe(html_image.strip())
        return ""

    class Media:
        css = {"all": ("css/qrimage.css",)}
        js = ("js/qrimage.js",)


admin.site.register(Transaction, TransactionAdmin)
