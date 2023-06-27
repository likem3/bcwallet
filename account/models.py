from django.db import models
from utils.models import BaseModel
from apis.cryptoapi.address import CreateAddressHandler
from utils.handlers import generate_qrcode_with_logo
from bcwallet.settings import LOGO_SETTINGS, BLOCKCHAIN_CODE
from django.db import transaction


class Account(BaseModel):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("nonactive", "Non-active"),
        ("suspended", "Suspended"),
    )

    uuid = models.UUIDField(unique=True, editable=False)
    user_id = models.IntegerField(unique=True)
    email = models.EmailField(unique=True, max_length=100)
    username = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="nonactive"
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = "account_accounts"


class Wallet(BaseModel):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("nonactive", "Non-Active"),
    )

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="wallets"
    )
    user_id = models.IntegerField()
    blockchain = models.CharField(max_length=50)
    network = models.CharField(max_length=20)
    address = models.CharField(unique=True, max_length=255)
    label = models.CharField(unique=True, max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="nonactive"
    )

    def __str__(self):
        return self.address

    class Meta:
        db_table = "account_wallets"

    @classmethod
    @transaction.atomic
    def create_user_wallet(cls, account, user_id, blockchain, network, status='active'):
        handler = CreateAddressHandler()

        # handler.create_address(
        #     blockchain=blockchain, network=network, label=account.user_id
        # )

        handler.create_fake_adress(
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
        Wallet, on_delete=models.CASCADE, related_name="attributs"
    )
    address_qr = models.TextField(null=True, blank=True)
    symbol = models.CharField(max_length=5, null=True, blank=True)
    logo = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.wallet_id)

    class Meta:
        db_table = "account_wallet_attributs"
