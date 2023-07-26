from rest_framework import serializers

from merchant.models import Merchant


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = model.get_fields(
            excludes=[
                "account",
                "created_at",
                "updated_at",
                "status",
                "merchant_wallets",
                "merchant_transactions",
            ]
        )
