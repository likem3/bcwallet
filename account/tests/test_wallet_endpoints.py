from unittest.mock import patch

from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status

from account.models import Account, Wallet
from account.tests.response_mock import Currency
from apis.addrbank.address import Address as AddressHandler
from apis.addrbank.currency import Currency as CurrencyHandler
from utils.tests import TestSetup


class WalletTestCase(TestSetup):
    def setUp(self):
        super().setUp()
        self.autheticate()
        self.account = baker.make(Account, merchant=self.merchant, user_id=111, status="active")
        self.faker = Faker()
        self.currency = Currency()

    @patch.object(CurrencyHandler, "get_currency_detail")
    @patch.object(AddressHandler, "get_assign_address")
    def wallet_create_address_success(
        self, symbol, mock_create_address, mock_currency_details
    ):
        url = reverse("wallets-list-create")
        btc_currency = self.currency.get_currency(symbol)
        data = {
            "merchant_code": self.merchant.code,
            "user_id": self.account.user_id,
            "currency_id": btc_currency["id"]
        }

        mock_currency_details.return_value = btc_currency
        mock_create_address.return_value = self.currency.get_address(
            symbol=symbol,
            merchant_code=self.merchant.code,
            user_id=self.account.user_id
        )

        response = self.client.post(url, data=data)
        response_json = response.json()
        response_data = response_json["data"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            f"{self.merchant.code} - {btc_currency['symbol']} - {data['user_id']}", response_data["label"]
        )
        self.assertEqual(btc_currency["symbol"], response_data["currency_symbol"])

    @patch.object(CurrencyHandler, "get_currency_detail")
    @patch.object(AddressHandler, "get_assign_address")
    def wallet_create_address_fail_assign_address(
        self, symbol, mock_create_address, mock_currency_details
    ):
        url = reverse("wallets-list-create")
        btc_currency = self.currency.get_currency(symbol)
        data = {
            "merchant_code": self.merchant.code,
            "user_id": self.account.user_id,
            "currency_id": btc_currency["id"]
        }

        mock_currency_details.return_value = btc_currency
        mock_create_address.return_value = None

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_create_btc_address_success(self):
        self.wallet_create_address_success("BTC")

    def test_wallet_create_doge_address_success(self):
        self.wallet_create_address_success("DOGE")

    def test_wallet_create_ltc_address_success(self):
        self.wallet_create_address_success("LTC")

    def test_wallet_create_eth_address_success(self):
        self.wallet_create_address_success("ETH")

    def test_wallet_create_trx_address_success(self):
        self.wallet_create_address_success("TRX")

    def test_wallet_create_usdt_address_success(self):
        self.wallet_create_address_success("USDTTRC20")

    def test_wallet_create_btc_address_fail_assign_addreess(self):
        self.wallet_create_address_fail_assign_address("BTC")

    def test_wallet_create_doge_address_fail_assign_addreess(self):
        self.wallet_create_address_fail_assign_address("DOGE")

    def test_wallet_create_ltc_address_fail_assign_addreess(self):
        self.wallet_create_address_fail_assign_address("LTC")

    def test_wallet_create_eth_address_fail_assign_addreess(self):
        self.wallet_create_address_fail_assign_address("ETH")

    def test_wallet_create_trx_address_fail_assign_addreess(self):
        self.wallet_create_address_fail_assign_address("TRX")

    def test_wallet_create_usdt_address_fail_assign_addreess(self):
        self.wallet_create_address_fail_assign_address("USDTTRC20")

    def test_create_wallet_fail_invalid_merchant_code(self):
        url = reverse("wallets-list-create")
        btc_currency = self.currency.get_currency("BTC")
        data = {
            "merchant_code": self.merchant.code + 1,
            "user_id": self.account.user_id,
            "currency_id": btc_currency["id"]
        }

        response = self.client.post(url, data=data)
        response_json = response.json()
        error_message = response_json["error"]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("merchant_code", error_message)

    @patch.object(CurrencyHandler, "get_currency_detail")
    @patch.object(AddressHandler, "get_assign_address")
    def test_create_wallet_success_auto_create_account_with_user_id(
        self, mock_create_address, mock_currency_details
    ):
        url = reverse("wallets-list-create")
        btc_currency = self.currency.get_currency("BTC")
        data = {
            "merchant_code": self.merchant.code,
            "user_id": self.account.user_id + 1,
            "currency_id": btc_currency["id"]
        }
        
        mock_currency_details.return_value = btc_currency
        mock_create_address.return_value = self.currency.get_address(
            symbol="BTC",
            merchant_code=self.merchant.code,
            user_id=self.account.user_id + 1
        )

        response = self.client.post(url, data=data)
        response_json = response.json()
        response_data = response_json["data"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            f"{self.merchant.code} - {btc_currency['symbol']} - {data['user_id']}", response_data["label"]
        )

    @patch.object(CurrencyHandler, "get_currency_detail")
    def test_create_wallet_fail_invalid_currency_id(self, get_currency_detail):
        url = reverse("wallets-list-create")
        data = {
            "merchant_code": self.merchant.code,
            "user_id": self.account.user_id + 1,
            "currency_id": 30000
        }

        get_currency_detail.return_value = None

        response = self.client.post(url, data=data)
        response_json = response.json()
        error_message = response_json["error"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("currency_id", error_message)

    def test_get_wallet_list_success(self):
        currencies = self.currency.get_currencies()

        url = reverse("wallets-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["data"]["results"] == [])

        for key in currencies.keys():
            address_resp = self.currency.get_address(key, self.merchant.code, self.account.user_id)
            baker.make(
                Wallet,
                account=self.account,
                user_id=self.account.user_id,
                currency_id=address_resp["currency_id"],
                currency_name=address_resp["currency"]["name"],
                currency_symbol=address_resp["currency"]["symbol"],
                currency_blockchain=address_resp["currency"]["blockchain"],
                currency_std=address_resp["currency"]["std"],
                network=address_resp["currency"]["network"]["type"],
                address=address_resp["address"],
                label=address_resp["label"],
                status="active",
            )

        url = reverse("wallets-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.json()["data"]["results"]) > 0)

    def test_get_wallet_list_by_user_success(self):
        currencies = self.currency.get_currencies()

        url = reverse("wallets-merchant-user-list", args=(self.merchant.code, self.account.user_id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["data"]["results"] == [])

        for key in currencies.keys():
            address_resp = self.currency.get_address(key, self.merchant.code, self.account.user_id)
            baker.make(
                Wallet,
                merchant=self.merchant,
                account=self.account,
                user_id=self.account.user_id,
                currency_id=address_resp["currency_id"],
                currency_name=address_resp["currency"]["name"],
                currency_symbol=address_resp["currency"]["symbol"],
                currency_blockchain=address_resp["currency"]["blockchain"],
                currency_std=address_resp["currency"]["std"],
                network=address_resp["currency"]["network"]["type"],
                address=address_resp["address"],
                label=address_resp["label"],
                status="active",
            )

        url = reverse("wallets-merchant-user-list", args=(self.merchant.code, self.account.user_id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.json()["data"]["results"]) > 0)

    def test_get_wallet_detail_by_id_success(self):
        currencies = self.currency.get_currencies()

        for key in currencies.keys():
            address_resp = self.currency.get_address(key, self.merchant.code, self.account.user_id)
            wallet = baker.make(
                Wallet,
                merchant=self.merchant,
                account=self.account,
                user_id=self.account.user_id,
                currency_id=address_resp["currency_id"],
                currency_name=address_resp["currency"]["name"],
                currency_symbol=address_resp["currency"]["symbol"],
                currency_blockchain=address_resp["currency"]["blockchain"],
                currency_std=address_resp["currency"]["std"],
                network=address_resp["currency"]["network"]["type"],
                address=address_resp["address"],
                label=address_resp["label"],
                status="active",
            )

            url = reverse("wallets-detail", args=(wallet.id,))
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.json()["data"] != {})

    def test_get_wallet_detail_by_id_fail(self):
        url = reverse("wallets-detail", args=(1,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
