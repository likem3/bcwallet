from rest_framework import serializers
from account.models import Account, Wallet as AccountWallet
from account.serializers import WalletAttributSerializer
from recharge.models import Transaction
from bcwallet.settings import HELPER_TEXT
from utils.handlers import handle_minimum_deposit_amount
from decimal import Decimal
from apis.addrbank.currency import Currency
from account.tasks import create_wallet_task
from django.db import transaction as model_transaction
from django.utils import timezone
from datetime import timedelta


class DepositTransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(min_value=1, write_only=True, help_text=HELPER_TEXT['user_id'])
    currency_id = serializers.IntegerField(min_value=1, write_only=True, help_text=HELPER_TEXT['currency_id'])
    amount = serializers.DecimalField(max_digits=25, decimal_places=10, help_text=HELPER_TEXT['trx_amount'])
    transaction_id = serializers.CharField(help_text=HELPER_TEXT['trx_transaction_id'])
    detail = serializers.SerializerMethodField()

    _account = None
    _wallet = None
    _currency = None
    _amount = None

    class Meta:
        model = Transaction
        fields = Transaction.get_fields(excludes=[
            "id"
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "approved_by",
            "cancelled_by",
            "deleted_by",
        ], extras=['detail'])
        read_only_fields = Transaction.get_fields(excludes=[
            "transaction_id",
            "currency_id",
            "user_id",
            "amount",
        ])

    def validate(self, attrs):
        # Call the parent's validate() method first
        attrs = super().validate(attrs)

        user_id = attrs["user_id"]
        currency_id = attrs["currency_id"]

        try:
            self._account = Account.objects.get(user_id=user_id)
        except Account.DoesNotExist:
            raise serializers.ValidationError({'user_id': 'Invalid user_id'})

        handdler = Currency()
        self._currency = handdler.get_currency_detail(currency_id)

        if not self._currency:
            raise serializers.ValidationError({'currency_id': 'Invalid currency_id'})

        try:
            self._wallet = self._account.wallets.get(
                currency_id=currency_id
            )
        except AccountWallet.DoesNotExist:
            pass

        if Transaction.objects.filter(
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
        query = {
            'account': self._account,
            'user_id': validated_data['user_id'],
            'currency_id': validated_data['currency_id'],
        }

        try:
            if not self._wallet:
                user_wallet = AccountWallet.create_user_wallet(
                    **query
                )
                if not user_wallet:
                    raise serializers.ValidationError({'wallet_id': 'unnable to create wallet'})

                self._wallet = user_wallet
        
        except Exception as e:
            print(str(e))
            raise serializers.ValidationError({'wallet_id': 'unnable to create wallet'})

        amount = Decimal(validated_data['amount'])
        minimum_amount = Decimal(handle_minimum_deposit_amount(self._wallet.currency_symbol))
        if amount < minimum_amount:
            raise serializers.ValidationError({'amount': f'Invalid minimum amount, must greater than {minimum_amount}'})

        query['wallet'] = self._wallet
        query['amount'] = amount
        query['currency_id'] = self._wallet.currency_id
        query['currency_name'] = self._wallet.currency_name
        query['currency_symbol'] = self._wallet.currency_symbol
        query['currency_blockchain'] = self._wallet.currency_blockchain
        query['currency_std'] = self._wallet.currency_std
        query['transaction_id'] = validated_data['transaction_id']

        try:
            transaction = Transaction.create_deposit_transaction(
                **query
            )

            exec_time = timezone.now() + timedelta(minutes=1)
            exp_time = timezone.now() + timedelta(minutes=3)
            create_wallet_task.apply_async(
                args=(transaction.code,),
                eta=exec_time,
                expires=exp_time
            )

            return transaction
        except Exception as e:
            print(str(e))
            raise serializers.ValidationError({'deposit': 'create deposit failed, server failed'})


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
