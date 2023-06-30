from django.db import models
from utils.models import BaseModel
from apis.cryptoapi.address import CreateAddressHandler
from utils.handlers import generate_qrcode_with_logo
from bcwallet.settings import (
    LOGO_SETTINGS,
    BLOCKCHAIN_CODE,
    STATUS_CHOICES_MODEL,
    HELPER_TEXT,
)
from django.db import transaction


class Account(BaseModel):
    uuid = models.UUIDField(
        unique=True, editable=False, help_text=HELPER_TEXT["account_uuid"]
    )
    user_id = models.PositiveIntegerField(
        unique=True, help_text=HELPER_TEXT["account_user_id"]
    )
    email = models.EmailField(
        unique=True, max_length=100, help_text=HELPER_TEXT["account_email"]
    )
    username = models.CharField(
        max_length=255, unique=True, help_text=HELPER_TEXT["account_username"]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES_MODEL,
        default="nonactive",
        help_text="status of the account",
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = "account_accounts"


class Wallet(BaseModel):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="wallets",
        help_text=HELPER_TEXT["account"],
    )
    user_id = models.PositiveIntegerField(help_text=HELPER_TEXT["user_id"])
    blockchain = models.CharField(max_length=50, help_text=HELPER_TEXT["blockchain"])
    network = models.CharField(max_length=20, help_text=HELPER_TEXT["network"])
    address = models.CharField(
        unique=True, max_length=255, help_text=HELPER_TEXT["address"]
    )
    label = models.CharField(
        unique=True, max_length=255, help_text=HELPER_TEXT["wallet_label"]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES_MODEL,
        default="nonactive",
        help_text="status of the wallet",
    )

    def __str__(self):
        return self.address

    class Meta:
        db_table = "account_wallets"

    @classmethod
    @transaction.atomic
    def create_user_wallet(cls, account, user_id, blockchain, network, status="active"):
        if cls.objects.filter(
            account=account, user_id=user_id, blockchain=blockchain, network=network
        ).exists():
            return

        handler = CreateAddressHandler()

        handler.create_address(
            blockchain=blockchain, network=network, label=account.user_id
        )

        if handler._address and handler._label:
            wallet = cls.objects.create(
                account=account,
                user_id=user_id,
                blockchain=blockchain,
                network=network,
                address=handler._address,
                label=handler._label,
                status=status,
            )

            wallet_logo = LOGO_SETTINGS[wallet.blockchain]
            wallet_image_b64 = generate_qrcode_with_logo(
                text=wallet.address, logo_path=wallet_logo
            )
            wallet_symbol = BLOCKCHAIN_CODE[wallet.blockchain]

            WalletAttribut.objects.create(
                wallet=wallet,
                address_qr=wallet_image_b64,
                symbol=wallet_symbol,
                logo=wallet_logo,
            )

            return wallet
        else:
            return

    @classmethod
    def get_account_blockchain_wallet(cls, account, blockchain, network):
        return cls.objects.filter(
            account=account, blockchain=blockchain, network=network
        )


class WalletAttribut(BaseModel):
    wallet = models.OneToOneField(
        Wallet,
        on_delete=models.CASCADE,
        related_name="attributs",
        help_text=HELPER_TEXT["wallet"],
    )
    address_qr = models.TextField(
        null=True, blank=True, help_text=HELPER_TEXT["address_qr"]
    )
    symbol = models.CharField(
        max_length=5, null=True, blank=True, help_text=HELPER_TEXT["wallet_symbol"]
    )
    logo = models.TextField(null=True, blank=True, help_text=HELPER_TEXT["wallet_logo"])

    def __str__(self):
        return str(self.wallet.address)

    class Meta:
        db_table = "account_wallet_attributs"


class WalletBalance(BaseModel):
    wallet = models.OneToOneField(
        Wallet,
        on_delete=models.CASCADE,
        related_name="balance",
        null=True,
        blank=True,
        help_text=HELPER_TEXT["wallet"],
    )
    amount = models.DecimalField(
        max_digits=25,
        decimal_places=10,
        null=True,
        blank=True,
        help_text=HELPER_TEXT["wallet_balance_amount"],
    )
    unit = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text=HELPER_TEXT["wallet_balance_unit"],
    )
    created_timestamp = models.DateTimeField(
        null=True, blank=True, help_text=HELPER_TEXT["created_timestamp"]
    )

    def __str__(self):
        return str(self.wallet.address)

    class Meta:
        db_table = "account_wallet_balance"
