import uuid

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from account.models import Account, Wallet, WalletAttribut, WalletBalance


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = Account.get_fields(excludes=["wallets", "account_transactions"])
        read_only_fields = Account.get_fields(excludes=["user_id", "email", "username"])

    def create(self, validated_data):
        try:
            return Account.objects.create(
                uuid=uuid.uuid4(), status="active", **validated_data
            )
        except Exception as e:
            raise serializers.ValidationError(f"Unable to create account, {str(e)}")

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
            raise serializers.ValidationError("invalid user id")

        # TODO add validation for currency_id inputed

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
