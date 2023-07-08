from django.db import models
from utils.models import BaseModel
from apis.addrbank.address import Address as AddressHandler
from utils.handlers import generate_qrcode_with_logo
from bcwallet.settings import (
    LOGO_SETTINGS,
    STATUS_CHOICES_MODEL,
    HELPER_TEXT,
    WALLET_TASK_STATUS
)
from django.db import transaction as app_transaction


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
    currency_id = models.PositiveIntegerField(help_text=HELPER_TEXT["currency_id"])
    currency_name = models.CharField(max_length=50, null=True, blank=True, help_text=HELPER_TEXT["currency_name"])
    currency_symbol = models.CharField(max_length=10, null=True, blank=True, help_text=HELPER_TEXT["currency_symbol"])
    currency_blockchain = models.CharField(max_length=50, null=True, blank=True, help_text=HELPER_TEXT["currency_blockchain"])
    currency_std = models.CharField(max_length=20, null=True, blank=True, help_text=HELPER_TEXT["currency_std"])
    address = models.CharField(
        unique=True, max_length=255, help_text=HELPER_TEXT["address"]
    )
    label = models.CharField(
        unique=True, max_length=255, help_text=HELPER_TEXT["wallet_label"]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES_MODEL,
        default="active",
        help_text="status of the wallet",
    )

    def __str__(self):
        return f"{self.address} - {self.currency_symbol}"

    class Meta:
        db_table = "account_wallets"

    @classmethod
    @app_transaction.atomic
    def create_user_wallet(cls, account, user_id, currency_id, status="active"):
        query = {
            'account': account,
            'user_id': user_id,
            'currency_id': currency_id,
        }

        try:
            return cls.objects.get(**query)

        except Wallet.DoesNotExist:
            handler = AddressHandler()

            handler.create_address(
                currency_id=currency_id, user_id=user_id
            )

            query['address'] = handler._address
            query['label'] = handler._label
            query['currency_id'] = handler._currency['id']
            query['currency_name'] = handler._currency['name']
            query['currency_symbol'] = handler._currency['symbol']
            query['currency_blockchain'] = handler._currency['blockchain']
            query['currency_std'] = handler._currency['std']
            query['status'] = status

            wallet_logo = LOGO_SETTINGS[query['currency_symbol']]

            if handler._address and handler._label and handler._currency:
                wallet = cls.objects.create(**query)


                wallet_image_b64 = generate_qrcode_with_logo(
                    text=wallet.address, logo_path=wallet_logo
                )

                wallet_symbol = query['currency_symbol']

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
    def get_account_blockchain_wallet(cls, account, user_id, currency_id):
        return cls.objects.filter(
            account=account, user_id=user_id, currency_id=currency_id
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
    wallet = models.ForeignKey(
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
    amount_change = models.DecimalField(
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
    last_updated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="last updated datetime"
    )

    def __str__(self):
        return str(self.wallet.address)

    class Meta:
        db_table = "account_wallet_balance"


class WalletTask(BaseModel):
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='wallet_tasks',
        help_text=HELPER_TEXT['wtt_wallet_id']
    )
    transaction_code = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=HELPER_TEXT['wtt_transaction_code']
    )
    status = models.CharField(
        max_length=20,
        choices=WALLET_TASK_STATUS,
        default="open",
        null=True,
        blank=True,
        help_text=HELPER_TEXT['wtt_attemp']
    )
    attemp = models.PositiveIntegerField(default=0, help_text=HELPER_TEXT['wtt_status'])

    def __str__(self):
        return str(self.wallet.address)

    class Meta:
        db_table = "account_wallet_tasks"

    @classmethod
    def create_task(cls, transaction, wallet):
        cls.objects.create(
            transaction=transaction,
            wallet=wallet,
        )
