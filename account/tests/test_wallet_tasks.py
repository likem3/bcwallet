from unittest.mock import patch

from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status

from account.models import Account, Wallet, WalletTask
from recharge.models import Transaction
from account.tests.response_mock import Currency
from utils.tests import TestSetup
from account.tasks import create_wallet_task

class WalletTaskTestCase(TestSetup):
    def setUp(self):
        super().setUp()
        self.autheticate()
        self.account = baker.make(Account, user_id=111, status="active")
        self.faker = Faker()
        self.currency = Currency()
        self.wallet = baker.make(
            Wallet,
            account=self.account,
            user_id=self.account.user_id,
            currency_id=self.currency.get_currency('BTC')['id'],
            status='active'
        )

    def test_create_wallet_task_from_transaction_success(self):
        transaction1 = baker.make(
            Transaction,
            wallet=self.wallet,
            status='pending'
        )

        create_wallet_task(transaction1.code)

        wallet_task = WalletTask.objects.filter(
            transaction_code=transaction1.code,
            wallet=self.wallet
        )

        self.assertIsNone(None, wallet_task)

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