from account.models import Account, Wallet
from rest_framework import serializers
import random
import string
import uuid
from bcwallet.settings import BLOCKCHAIN_OPTIONS, NETWORK_OPTIONS
from apis.cryptoapi.address import CreateAddressHandler
from rest_framework.exceptions import ParseError


class AccountSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField(required=False)
    status = serializers.CharField(default="nonactive")

    def generate_random_username(self):
        # Generate a random username using a combination of letters and digits
        length = 8
        letters_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_digits) for _ in range(length))

    def create(self, validated_data):
        if "username" not in validated_data:
            validated_data["username"] = self.generate_random_username()
        return Account.objects.create(uuid=uuid.uuid4(), **validated_data)

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

    class Meta:
        model = Account
        fields = (
            "id",
            "uuid",
            "user_id",
            'email',
            "username",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("uuid", "id", "created_at", "updated_at")


class WalletSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), source="account"
    )
    blockchain = serializers.ChoiceField(choices=BLOCKCHAIN_OPTIONS)
    network = serializers.ChoiceField(choices=NETWORK_OPTIONS)

    class Meta:
        model = Wallet
        fields = (
            "id",
            "account_id",
            "user_id",
            "blockchain",
            "network",
            "address",
            "label",
            "status",
        )
        read_only_fields = (
            "id",
            "user_id",
            "wallet_id",
            "label",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        account = validated_data.pop("account")
        validated_data["user_id"] = account.user_id

        try:
            handler = CreateAddressHandler()
            handler.create_address(
                blockchain=validated_data["blockchain"],
                network=validated_data["network"],
                label=account.user_id,
            )

            # handler.create_fake_adress(
            #     blockchain=validated_data["blockchain"],
            #     network=validated_data["network"],
            #     label=account.user_id,
            # )

            if handler._address and handler._label:
                return Wallet.objects.create(
                    account=account,
                    address=handler._address,
                    label=handler._label,
                    **validated_data,
                )
            else:
                raise ParseError("create address failed")
        except Exception as e:
            raise ParseError(f"error {e}")
