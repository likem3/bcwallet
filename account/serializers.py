from account.models import Account, Wallet
from rest_framework import serializers
import random
import string
import uuid
from bcwallet.settings import BLOCKCHAIN_OPTIONS, NETWORK_OPTIONS, STATUS_OPTIONS
from rest_framework.exceptions import ParseError


class AccountSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    status = serializers.ChoiceField(choices=STATUS_OPTIONS, default="active")

    def generate_random_username(self):
        # Generate a random username using a combination of letters and digits
        length = 8
        letters_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_digits) for _ in range(length))

    def create(self, validated_data):
        try:
            if "username" not in validated_data:
                validated_data["username"] = self.generate_random_username()
            return Account.objects.create(uuid=uuid.uuid4(), **validated_data)
        except Exception as e:
            raise serializers.ValidationError(f"Unable to create account, {str(e)}")

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
            "email",
            "username",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("uuid", "id", "created_at", "updated_at")


class WalletSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.filter(status="active"), source="account"
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
            "address",
            "label",
            "created_at",
            "updated_at",
        )

    def validate(self, data):
        if Wallet.objects.filter(
            account=data["account"],
            blockchain=data["blockchain"],
            network=data["network"],
        ).exists():
            raise serializers.ValidationError(
                "wallet with specific blockhain and network already created"
            )
        return data

    def create(self, validated_data):
        account = validated_data.pop("account")
        validated_data["user_id"] = account.user_id

        try:
            return Wallet.create_user_wallet(
                account=account,
                **validated_data,
            )

        except Exception as e:
            raise ParseError(f"error {e}")
