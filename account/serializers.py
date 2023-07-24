import uuid

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from account.models import Account, Wallet, WalletAttribut, WalletBalance
from apis.addrbank.currency import Currency
from merchant.serializers import MerchantSerializer
from merchant.models import Merchant

from django.conf import settings as app_settings


class CreateAccountSerializer(serializers.ModelSerializer):
    merchant_code = serializers.IntegerField(
        min_value=1000,
        write_only=True,
        help_text=app_settings.HELPER_TEXT["merchant_code"]
    )

    class Meta:
        model = Account
        fields = Account.get_fields(excludes=["wallets", "account_transactions"], extras=["merchant_code"])
        read_only_fields = Account.get_fields(excludes=["user_id", "email", "username", "merchant_code"])

    def validate(self, attrs):
        super().validate(attrs)
        merchant_code = attrs["merchant_code"]
        if not Merchant.objects.filter(status='active', code=merchant_code).exists():
            raise serializers.ValidationError({"merchant_code": "Invalid merchant code"})

        return attrs

    def create(self, validated_data):
        account = Account.get_or_create(
            **validated_data
        )

        if not account:
            raise serializers.ValidationError("Unable to create account")

        return account

class AccountSerializer(serializers.ModelSerializer):
    merchant_code = serializers.IntegerField(source="merchant.code", allow_null=True)

    class Meta:
        model = Account
        fields = Account.get_fields(excludes=["wallets", "account_transactions", "merchant"], extras=["merchant_code"])
        read_only_fields = Account.get_fields(excludes=["user_id", "email", "username"])

    def update(self, instance, validated_data):
        # Disable updating the user_id field
        validated_data.pop("user_id", None)
        return super().update(instance, validated_data)

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

    class Meta:
        model = Wallet
        fields = model.get_fields(
            excludes=["wallet_transactions", "wallet_tasks"],
            extras=["attributs", "balance"],
        )
        read_only_fields = Wallet.get_fields(excludes=["user_id", "currency_id"])

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.balance.exists():
            latest_balance = instance.balance.latest("created_at")
            representation["balance"] = WalletBalanceSerializer(latest_balance).data
        else:
            representation["balance"] = None
        return representation

    def validate(self, data):
        # blockchain, network = handle_blockchain_network(data["blockchain"])
        if not Account.objects.filter(
            user_id=data["user_id"], status="active"
        ).exists():
            raise serializers.ValidationError({"user_id": "invalid user id"})

        handdler = Currency()
        currenccy = handdler.get_currency_detail(data["currency_id"])

        if not currenccy:
            raise serializers.ValidationError({"currency_id": "Invalid currency_id"})

        return data

    def create(self, validated_data):
        account = Account.objects.get(user_id=validated_data["user_id"])
        try:
            wallet = Wallet.create_user_wallet(
                account=account,
                **validated_data,
            )

            if not wallet:
                raise serializers.ValidationError({"creating": "Server error!"})

            return wallet

        except Exception as e:
            raise ParseError(f"error {e}")
