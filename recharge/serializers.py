from rest_framework import serializers
from account.models import Account, Wallet as AccountWallet, WalletAttribut
from bcwallet.settings import BLOCKCHAIN_OPTIONS, NETWORK_OPTIONS
from rest_framework.exceptions import APIException
from recharge.models import Transaction
from utils.handlers import handle_blockchain_network, handle_minimum_deposit_amount
from decimal import Decimal


class WalletAttributDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAttribut
        fields = "__all__"


class DepositTransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(min_value=1, write_only=True)
    blockchain = serializers.ChoiceField(choices=BLOCKCHAIN_OPTIONS, write_only=True)
    amount = serializers.DecimalField(max_digits=25, decimal_places=10)
    detail = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "deleted_at",
            "code",
            "origin_code",
            "account",
            "wallet",
            "from_address",
            "to_address",
            "from_currency",
            "to_currency",
            "network",
            "rate",
            "status",
            "cancel_reason",
            "proof_of_payment",
            "expired_at",
            "receipt_id",
            "created_by",
            "approved_by",
            "cancelled_by",
            "deleted_by",
            "amount",
            "blockchain",
            "user_id",
            "detail",
        ]
        read_only_fields = [
            "id",
            "deleted_at",
            "code",
            "origin_code",
            "account",
            "wallet",
            "from_address",
            "to_address",
            "from_currency",
            "to_currency",
            "network",
            "rate",
            "status",
            "cancel_reason",
            "proof_of_payment",
            "expired_at",
            "receipt_id",
            "created_by",
            "approved_by",
            "cancelled_by",
            "deleted_by",
        ]

    def validate(self, attrs):
        # Call the parent's validate() method first
        attrs = super().validate(attrs)

        user_id = attrs["user_id"]
        amount = attrs["amount"]
        blockchain, network = handle_blockchain_network(attrs["blockchain"])

        if not Account.objects.filter(status="active", user_id=user_id).exists():
            raise serializers.ValidationError("Invalid user id")

        minimum_amount = Decimal(handle_minimum_deposit_amount(blockchain))
        if Decimal(amount) <= minimum_amount:
            raise serializers.ValidationError(
                f"deposit amount too small, minimum amount is {minimum_amount}"
            )

        if Transaction.objects.filter(
            account__user_id=user_id,
            blockchain=blockchain,
            network=network,
            status="pending",
        ).exists():
            raise serializers.ValidationError("User still has pending transaction")

        return attrs

    def get_detail(self, obj):
        attributs_data = WalletAttributDetailSerializer(obj.wallet.attributs).data
        return attributs_data

    def create(self, validated_data):
        try:
            account = Account.objects.get(user_id=validated_data["user_id"])

            blockchain, network = handle_blockchain_network(
                validated_data["blockchain"]
            )

            account_wallet = AccountWallet.objects.get(
                account=account, blockchain=blockchain, network=network
            )

        except Account.DoesNotExist:
            raise serializers.ValidationError("Invalid user_id")

        except AccountWallet.DoesNotExist:
            account_wallet = AccountWallet.create_user_wallet(
                account=account,
                user_id=account.user_id,
                blockchain=blockchain,
                network=network,
            )

        if not account_wallet:
            raise APIException("Failed to create account wallet.", code="server_error")

        transaction = Transaction.create_deposit_transaction(
            account, account_wallet, blockchain, network, validated_data["amount"]
        )

        return transaction


class UpdateReceiptTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = Transaction.get_fields()
        read_only_fields = Transaction.get_fields(excludes=["receipt_id"])
