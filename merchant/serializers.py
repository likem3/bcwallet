from rest_framework import serializers
from merchant.models import Merchant

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = Merchant.get_fields(excludes=["created_at", "updated_at", "status"])