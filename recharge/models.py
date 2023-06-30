from django.db import models
from utils.models import ExtraBaseModel
from account.models import Account, Wallet
from utils.handlers import handle_transaction_code
from django.utils import timezone
from datetime import timedelta
from bcwallet.settings import TRANSACTION_STATUS


class Transaction(ExtraBaseModel):
    STATUS_CHOICES = TRANSACTION_STATUS

    code = models.CharField(
        max_length=255,
        unique=True,
        help_text="Code of the transaction, also serves as the transaction identifier",
    )
    origin_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Origin transaction if the transaction \
            is derived from another transaction",
    )
    account = models.ForeignKey(
        to=Account,
        on_delete=models.CASCADE,
        related_name="account_transactions",
        help_text="Related data of the account performing the transaction",
    )
    wallet = models.ForeignKey(
        to=Wallet,
        on_delete=models.CASCADE,
        related_name="wallet_transactions",
        help_text="Related data of the wallet performing the transaction",
    )
    from_address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Currency address that sends in the transaction",
    )
    to_address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Currency address that receives in the transaction",
    )
    from_currency = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Symbol of the source currency such as BTC, ETH, etc",
    )
    to_currency = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Symbol of the target currency such as BTC, ETH, etc",
    )
    blockchain = models.CharField(
        max_length=30, null=True, blank=True, help_text="Main blockchain name used"
    )
    network = models.CharField(
        max_length=30, null=True, blank=True, help_text="Transaction network name used"
    )
    amount = models.DecimalField(
        max_digits=25,
        decimal_places=10,
        blank=True,
        null=True,
        help_text="Separated by a dot, the amount to be received (e.g., 0.001)",
    )
    rate = models.DecimalField(
        max_digits=25,
        decimal_places=10,
        blank=True,
        null=True,
        help_text="Separated by a dot, exchange rate if different currencies",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Transaction status",
    )
    cancel_reason = models.TextField(
        null=True, blank=True, help_text="Reason why the transaction becomes canceled"
    )
    proof_of_payment = models.TextField(
        blank=True,
        null=True,
        help_text="Image in base64 format of the transaction receipt",
    )
    expired_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The expiration of the transaction before it gets ignored",
    )
    receipt_id = models.CharField(
        max_length=255, null=True, blank=True, help_text="The transaction hash (txid)"
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        db_table = "recharge_transactions"

    @classmethod
    def create_deposit_transaction(cls, account, wallet, blockchain, network, amount):
        trx = Transaction.objects.create(
            code=handle_transaction_code(blockchain, network, account.user_id, "DP"),
            account=account,
            wallet=wallet,
            to_address=wallet.address,
            from_currency=wallet.attributs.symbol,
            to_currency=wallet.attributs.symbol,
            network=network,
            amount=amount,
            expired_at=(timezone.now() + timedelta(minutes=30)),
            blockchain=blockchain,
        )

        return trx

    @classmethod
    def create_withdrawal_transaction(
        cls, account, wallet, blockchain, network, amount
    ):
        pass
