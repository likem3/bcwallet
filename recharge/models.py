from django.db import models
from utils.models import ExtraBaseModel
from account.models import Account, Wallet
from utils.handlers import handle_transaction_code
from django.utils import timezone
from datetime import timedelta
from bcwallet.settings import TRANSACTION_STATUS, HELPER_TEXT, TRANSACTION_TYPE_OPTION


class Transaction(ExtraBaseModel):
    STATUS_CHOICES = TRANSACTION_STATUS

    code = models.CharField(
        max_length=255,
        unique=True,
        help_text=HELPER_TEXT["trx_code"],
    )
    origin_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=HELPER_TEXT["trx_origin_code"],
    )
    account = models.ForeignKey(
        to=Account,
        on_delete=models.CASCADE,
        related_name="account_transactions",
        help_text=HELPER_TEXT["account"],
    )
    wallet = models.ForeignKey(
        to=Wallet,
        on_delete=models.CASCADE,
        related_name="wallet_transactions",
        help_text=HELPER_TEXT["wallet"],
    )
    from_address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=HELPER_TEXT["trx_from_address"],
    )
    to_address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=HELPER_TEXT["trx_to_address"],
    )
    from_currency = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=HELPER_TEXT["trx_from_currency"],
    )
    to_currency = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=HELPER_TEXT["trx_to_currency"],
    )
    user_id = models.PositiveIntegerField(help_text=HELPER_TEXT["user_id"])
    currency_id = models.PositiveIntegerField(help_text=HELPER_TEXT["currency_id"])
    currency_name = models.CharField(
        max_length=50, null=True, blank=True, help_text=HELPER_TEXT["currency_name"]
    )
    currency_symbol = models.CharField(
        max_length=10, null=True, blank=True, help_text=HELPER_TEXT["currency_symbol"]
    )
    currency_blockchain = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=HELPER_TEXT["currency_blockchain"],
    )
    currency_std = models.CharField(
        max_length=20, null=True, blank=True, help_text=HELPER_TEXT["currency_std"]
    )
    amount = models.DecimalField(
        max_digits=25,
        decimal_places=10,
        blank=True,
        null=True,
        help_text=HELPER_TEXT["trx_amount"],
    )
    rate = models.DecimalField(
        max_digits=25,
        decimal_places=10,
        blank=True,
        null=True,
        help_text=HELPER_TEXT["trx_rate"],
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text=HELPER_TEXT["trx_status"],
    )
    cancel_reason = models.TextField(
        null=True, blank=True, help_text=HELPER_TEXT["trx_cancel_reason"]
    )
    proof_of_payment = models.TextField(
        blank=True,
        null=True,
        help_text=HELPER_TEXT["trx_proof_of_payment"],
    )
    expired_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=HELPER_TEXT["trx_expired_at"],
    )
    transaction_id = models.CharField(
        max_length=255, help_text=HELPER_TEXT["trx_transaction_id"]
    )
    type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text=HELPER_TEXT["trx_type"],
        choices=TRANSACTION_TYPE_OPTION,
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        db_table = "recharge_transactions"

    @classmethod
    def create_deposit_transaction(
        cls,
        account,
        wallet,
        user_id,
        amount,
        currency_id,
        currency_name,
        currency_symbol,
        currency_blockchain,
        currency_std,
        transaction_id,
    ):
        query = {
            "code": handle_transaction_code(
                wallet.currency_symbol, account.user_id, "DP"
            ),
            "account": account,
            "wallet": wallet,
            "to_address": wallet.address,
            "from_currency": wallet.attributs.symbol,
            "to_currency": wallet.attributs.symbol,
            "user_id": user_id,
            "currency_id": currency_id,
            "currency_name": currency_name,
            "currency_symbol": currency_symbol,
            "currency_blockchain": currency_blockchain,
            "currency_std": currency_std,
            "amount": amount,
            "transaction_id": transaction_id,
            "type": "deposit",
            "expired_at": (timezone.now() + timedelta(minutes=30)),
        }
        trx = Transaction.objects.create(**query)

        return trx

    @classmethod
    def create_withdrawal_transaction(
        cls, account, wallet, blockchain, network, amount
    ):
        pass
