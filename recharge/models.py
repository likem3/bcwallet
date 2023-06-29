from django.db import models
from utils.models import ExtraBaseModel
from account.models import Account, Wallet
from utils.handlers import handle_transaction_code
from django.utils import timezone
from datetime import timedelta


class Transaction(ExtraBaseModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )

    code = models.CharField(max_length=255, unique=True)
    origin_code = models.CharField(max_length=255, blank=True, null=True)
    account = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name="account_transactions"
    )
    wallet = models.ForeignKey(
        to=Wallet, on_delete=models.CASCADE, related_name="wallet_transactions"
    )
    from_address = models.CharField(max_length=100, null=True, blank=True)
    to_address = models.CharField(max_length=100, null=True, blank=True)
    from_currency = models.CharField(max_length=50, null=True, blank=True)
    to_currency = models.CharField(max_length=50, null=True, blank=True)
    network = models.CharField(max_length=30, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=25, decimal_places=10, blank=True, null=True
    )
    rate = models.DecimalField(max_digits=25, decimal_places=10, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    cancel_reason = models.TextField(null=True, blank=True)
    proof_of_payment = models.TextField(blank=True, null=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    receipt_id = models.CharField(max_length=255, null=True, blank=True)

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
        )

        return trx

    @classmethod
    def create_withdrawal_transaction(
        cls, account, wallet, blockchain, network, amount
    ):
        pass
