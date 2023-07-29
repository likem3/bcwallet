from django.conf import settings as app_settings
from django.db import transaction as app_transaction
from rest_framework import serializers

from account.models import Account, Wallet, WalletAttribut, WalletBalance
from apis.addrbank.currency import Currency
from merchant.models import Merchant
from merchant.serializers import MerchantSerializer


class AccountSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(many=False, read_only=True)
    merchant_code = serializers.IntegerField(
        min_value=1000,
        write_only=True,
        help_text=app_settings.HELPER_TEXT["merchant_code"],
    )

    class Meta:
        model = Account
        fields = model.get_fields(
            excludes=["wallets", "account_transactions"], extras=["merchant_code"]
        )
        read_only_fields = model.get_fields(
            excludes=["user_id", "email", "username", "merchant_code"]
        )
        extra_kwargs = {
            "merchant_code": {
                "required": True
            }
        }

    def update(self, instance, validated_data):
        # Disable updating the user_id field
        validated_data.pop("user_id", None)
        return super().update(instance, validated_data)

    def validate(self, attrs):
        super().validate(attrs)
        merchant_code = attrs["merchant_code"]
        if not Merchant.objects.filter(status="active", code=merchant_code).exists():
            raise serializers.ValidationError(
                {"merchant_code": "Invalid merchant code"}
            )

        return attrs

    def create(self, validated_data):
        account = Account.get_or_create(**validated_data)

        if not account:
            raise serializers.ValidationError("Unable to create account")

        return account

    def validate_user_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("User ID must be a positive integer.")

        # Validate uniqueness of user_id
        if Account.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("user_id already saved")
        return value


class WalletAttributSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAttribut
        fields = [
            "address_qr",
            "symbol",
            "logo",
        ]


class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletBalance
        fields = [
            "amount",
            "unit",
            "created_at",
            "updated_at",
        ]


class WalletSerializer(serializers.ModelSerializer):
    attributs = WalletAttributSerializer(read_only=True)
    balance = WalletBalanceSerializer(many=False, read_only=True)
    merchant = MerchantSerializer(many=False, read_only=True)
    merchant_code = serializers.IntegerField(
        min_value=1000,
        write_only=True,
        help_text=app_settings.HELPER_TEXT["merchant_code"],
    )

    class Meta:
        model = Wallet
        fields = model.get_fields(
            excludes=["wallet_transactions", "wallet_tasks"],
            extras=["attributs", "balance", "merchant_code"],
        )
        read_only_fields = model.get_fields(
            excludes=["user_id", "currency_id", "merchant_code"]
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.balance.exists():
            latest_balance = instance.balance.latest("created_at")
            representation["balance"] = WalletBalanceSerializer(latest_balance).data
        else:
            representation["balance"] = None

        return representation

    def validate(self, data):
        merchant_code = data["merchant_code"]
        if not Merchant.objects.filter(code=merchant_code, status="active").exists():
            raise serializers.ValidationError(
                {"merchant_code": "Invalid merchant code"}
            )

        handdler = Currency()
        currenccy = handdler.get_currency_detail(data["currency_id"])

        if not currenccy:
            raise serializers.ValidationError({"currency_id": "Invalid currency_id"})

        return data

    @app_transaction.atomic
    def create(self, validated_data):
        merchant = Merchant.objects.get(code=validated_data.pop("merchant_code"))
        account = Account.get_or_create(
            merchant_code=merchant.code, user_id=validated_data["user_id"]
        )
        try:
            wallet = Wallet.create_user_wallet(
                account=account,
                merchant=merchant,
                **validated_data,
            )
            if not wallet:
                raise serializers.ValidationError({"creating": "Server error!"})
            return wallet

        except Exception as e:
            print(str(e))
            raise serializers.ValidationError({"creating address": "Server error!"})
