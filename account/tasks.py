from celery import shared_task
from bcwallet.settings import (
    BLOCKCHAIN_NETWORK_MAP,
    ENVIRONMENT_SETTING,
    CRYPTOAPI_BASE_URL,
    CRYPTOAPI_API_KEY,
    CRYPTOAPI_MASTER_WALLET,
)
import requests
import time
from django.utils import timezone
from account.models import Wallet, WalletBalance


@shared_task
def generate_random_number():
    print("task run!!")


@shared_task
def update_wallets_tasks(wallet_balances={}):
    wallets = Wallet.objects.filter(
        status="active", account__status="active", address__in=wallet_balances.keys()
    )

    for wallet in wallets:
        address = wallet.address

        balance, _ = WalletBalance.objects.get_or_create(wallet=wallet)
        balance_data = wallet_balances.get(address, {})

        if not balance_data or not balance_data.get("confirmedBalance"):
            continue

        confirmed_balance = balance_data.get("confirmedBalance", {})
        balance.amount = confirmed_balance.get("amount")
        balance.unit = confirmed_balance.get("unit")
        balance.created_timestamp = timezone.make_aware(
            timezone.datetime.utcfromtimestamp(balance_data.get("createdTimestamp"))
        )

        balance.save()


@shared_task
def get_wallets_balances():
    result_wallets = {}
    blockchain_networks = {
        blockchain: network_map["production"]
        if ENVIRONMENT_SETTING == "production"
        else network_map["development"]
        for blockchain, network_map in BLOCKCHAIN_NETWORK_MAP.items()
    }

    for blockchain, network in blockchain_networks.items():
        if not Wallet.objects.filter(
            status="active",
            account__status="active",
            blockchain=blockchain,
            network=network,
        ).exists():
            continue

        url = "{}/wallet-as-a-service/wallets/{}/{}/{}/addresses".format(
            CRYPTOAPI_BASE_URL,
            CRYPTOAPI_MASTER_WALLET,
            blockchain,
            network
        )
        limit = 50
        offset = 0

        while True:
            params = {"limit": limit, "offset": offset}
            headers = {
                "X-API-Key": CRYPTOAPI_API_KEY,
                "Content-Type": "application/json",
            }

            api_response = requests.get(url=url, headers=headers, params=params)
            response_data = api_response.json().get("data")
            response_items = response_data.get("items", [])

            if response_data and response_items:
                for wallet in response_items:
                    result_wallets[wallet["address"]] = wallet

            if len(response_items) < limit:
                break

            offset += limit
            time.sleep(0.3)

    update_wallets_tasks.delay(wallet_balances=result_wallets)
