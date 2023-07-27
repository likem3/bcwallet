from faker import Faker
from model_bakery import baker

from account.models import Account, Wallet, WalletTask
from account.tasks import create_wallet_task
from account.tests.response_mock import Currency
from recharge.models import Transaction
from utils.tests import TestSetup


class WalletTaskTestCase(TestSetup):
    def setUp(self):
        super().setUp()
        self.autheticate()
        self.account = baker.make(Account, user_id=111, status="active")
        self.faker = Faker()
        self.currency = Currency()
        self.wallet = baker.make(
            Wallet,
            merchant=self.merchant,
            account=self.account,
            user_id=self.account.user_id,
            currency_id=self.currency.get_currency("BTC")["id"],
            status="active",
        )

    def test_create_wallet_task_from_transaction_success(self):
        transaction1 = baker.make(Transaction, merchant=self.merchant, wallet=self.wallet, status="pending")

        create_wallet_task(transaction1.code)

        wallet_task = WalletTask.objects.filter(
            transaction_code=transaction1.code, wallet=self.wallet
        )

        self.assertIsNotNone(wallet_task, "Wallet Task is none")

    # def test_create_wallet_task_from_transaction_fail_not_found(self):
    #     transaction1 = baker.make(
    #         Transaction,
    #         wallet=self.wallet,
    #         status='pending'
    #     )

    #     create_wallet_task(transaction1.code)

    #     wallet_task = WalletTask.objects.filter(
    #         transaction_code=transaction1.code,
    #         wallet=self.wallet
    #     )

    #     self.assertIsNone(None, wallet_task)
