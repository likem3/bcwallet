from datetime import timedelta
from decimal import Decimal

from django.conf import settings as app_settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import transaction as model_transaction
from django.utils import timezone
from rest_framework import serializers

from account.models import Account
from account.models import Wallet as AccountWallet
from account.serializers import WalletAttributSerializer
from account.tasks import create_wallet_task
from apis.addrbank.currency import Currency
from merchant.models import Merchant
from merchant.serializers import MerchantSerializer
from recharge.models import Transaction
from utils.handlers import handle_minimum_deposit_amount


class DepositTransactionSerializer(serializers.ModelSerializer):
    merchant_code = serializers.IntegerField(
        min_value=1000,
        write_only=True,
        help_text=app_settings.HELPER_TEXT["merchant_code"],
    )
    user_id = serializers.IntegerField(
        min_value=1, write_only=True, help_text=app_settings.HELPER_TEXT["user_id"]
    )
    currency_id = serializers.IntegerField(
        min_value=1, write_only=True, help_text=app_settings.HELPER_TEXT["currency_id"]
    )
    amount = serializers.DecimalField(
        max_digits=25,
        decimal_places=10,
        help_text=app_settings.HELPER_TEXT["trx_amount"],
    )
    callback_url = serializers.CharField(
        help_text=app_settings.HELPER_TEXT["trx_callback_url"]
    )
    merchant = MerchantSerializer(many=False, read_only=True)
    detail = serializers.SerializerMethodField()

    _account = None
    _wallet = None
    _currency = None
    _amount = None
    _merchant = None

    class Meta:
        model = Transaction
        fields = Transaction.get_fields(
            excludes=[
                "id" "created_at",
                "updated_at",
                "deleted_at",
                "created_by",
                "approved_by",
                "cancelled_by",
                "deleted_by",
            ],
            extras=["detail", "merchant_code"],
        )
        read_only_fields = Transaction.get_fields(
            excludes=[
                "currency_id",
                "amount",
                "user_id",
                "callback_url",
                "origin_code",
            ]
        )

    def validate(self, attrs):
        # Call the parent's validate() method first
        attrs = super().validate(attrs)

        user_id = attrs["user_id"]
        currency_id = attrs["currency_id"]
        callback_url = attrs["callback_url"]
        merchant_code = attrs["merchant_code"]

        if callback_url:
            validator = URLValidator()
            try:
                validator(callback_url)
            except ValidationError:
                raise serializers.ValidationError(
                    {"callback_url": "Invalid callback url"}
                )

        try:
            self._merchant = Merchant.objects.get(code=merchant_code, status="active")
        except Merchant.DoesNotExist:
            raise serializers.ValidationError(
                {"merchant_code": "Invalid merchant code"}
            )

        handdler = Currency()
        self._currency = handdler.get_currency_detail(currency_id)

        if not self._currency:
            raise serializers.ValidationError({"currency_id": "Invalid currency_id"})

        if Transaction.objects.filter(
            merchant=self._merchant,
            account__user_id=user_id,
            currency_id=currency_id,
            status="pending",
        ).exists():
            raise serializers.ValidationError("User still has pending transaction")

        return attrs

    def get_detail(self, obj):
        attributs_data = WalletAttributSerializer(obj.wallet.attributs).data
        return attributs_data

    @model_transaction.atomic
    def create(self, validated_data):
        self._account = Account.get_or_create(
            merchant_code=validated_data.pop("merchant_code"),
            user_id=validated_data.get("user_id"),
        )

        query = {
            "merchant": self._merchant,
            "account": self._account,
            "user_id": validated_data["user_id"],
            "currency_id": validated_data["currency_id"],
        }

        try:
            self._wallet = self._account.wallets.get(
                currency_id=self._currency.get("id")
            )

        except AccountWallet.DoesNotExist:
            user_wallet = AccountWallet.create_user_wallet(**query)
            if not user_wallet:
                raise serializers.ValidationError(
                    {"wallet_id": "unnable to create wallet"}
                )
            self._wallet = user_wallet

        except Exception as e:
            print(str(e))
            raise serializers.ValidationError({"wallet_id": "unnable to create wallet"})

        amount = Decimal(validated_data["amount"])
        minimum_amount = Decimal(
            handle_minimum_deposit_amount(self._wallet.currency_symbol)
        )
        if amount < minimum_amount:
            raise serializers.ValidationError(
                {
                    "amount": "Invalid minimum amount, must greater than {}".format(
                        minimum_amount
                    )
                }
            )

        query["wallet"] = self._wallet
        query["amount"] = amount
        query["currency_id"] = self._wallet.currency_id
        query["currency_name"] = self._wallet.currency_name
        query["currency_symbol"] = self._wallet.currency_symbol
        query["currency_blockchain"] = self._wallet.currency_blockchain
        query["currency_std"] = self._wallet.currency_std
        query["callback_url"] = validated_data["callback_url"]
        if validated_data.get("origin_code"):
            query["origin_code"] = validated_data["origin_code"]

        try:
            transaction = Transaction.create_deposit_transaction(**query)

            exec_time = timezone.now() + timedelta(minutes=1)
            exp_time = timezone.now() + timedelta(minutes=3)
            create_wallet_task.apply_async(
                args=(transaction.code,), eta=exec_time, expires=exp_time
            )

            return transaction
        except Exception as e:
            print(str(e))
            raise serializers.ValidationError(
                {"deposit": "create deposit failed, server failed"}
            )


class UpdateDepositTransactionSerializer(serializers.ModelSerializer):
    merchant = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = model.get_fields(
            excludes=[
                "id" "created_at",
                "updated_at",
                "deleted_at",
                "created_by",
                "approved_by",
                "cancelled_by",
                "deleted_by",
            ],
            extras=["detail"],
        )
        read_only_fields = model.get_fields(
            excludes=[
                "transaction_id",
            ]
        )

    def get_detail(self, obj):
        attributs_data = WalletAttributSerializer(obj.wallet.attributs).data
        return attributs_data

    def get_merchant(self, obj):
        merchant_data = MerchantSerializer(obj.merchant).data
        return merchant_data


class NetworkSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    type = serializers.CharField()


class CurrencySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    symbol = serializers.CharField()
    blockchain = serializers.CharField()
    std = serializers.CharField()
    network = NetworkSerializer()
