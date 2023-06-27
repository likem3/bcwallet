from rest_framework import serializers
from account.models import Account, Wallet as AccountWallet, WalletAttribut
from bcwallet.settings import BLOCKCHAIN_OPTIONS, NETWORK_OPTIONS
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404


class WalletAttributSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAttribut
        fields = "__all__"


class DepositWalletSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(min_value=1)
    blockchain = serializers.ChoiceField(choices=BLOCKCHAIN_OPTIONS)
    network = serializers.ChoiceField(choices=NETWORK_OPTIONS)
    attributs = serializers.SerializerMethodField()
    

    class Meta:
        model = AccountWallet
        fields = [
            "id",
            "account",
            "user_id",
            "blockchain",
            "network",
            "address",
            "label",
            "status",
            "attributs"
        ]
        read_only_fields = ["id", "user_id", "account", "address", "label", "status", "attributs"]

    def get_attributs(self, obj):
        attributs_data = WalletAttributSerializer(obj.attributs).data
        return attributs_data

    def create(self, validated_data):
        try:
            account = Account.objects.get(user_id=validated_data['user_id'])

            blockchain = validated_data["blockchain"]
            network = validated_data["network"]

            account_wallet = AccountWallet.objects.get(
                account=account, blockchain=blockchain, network=network
            )

        except Account.DoesNotExist:
            raise serializers.ValidationError("Invalid user_id")

        except AccountWallet.DoesNotExist:
            account_wallet = AccountWallet.create_user_wallet(
                account=account,
                user_id=account.user_id,
                blockchain=blockchain,
                network=network,
            )

        if not account_wallet:
            raise APIException("Failed to create account wallet.", code="server_error")

        return account_wallet
