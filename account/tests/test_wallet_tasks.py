from django.utils import timezone
from faker import Faker
from model_bakery import baker

from account.models import Account, Wallet, WalletTask, WalletBalance
from account.tasks import create_wallet_task, get_update_wallet_balance_candidate
from account.tests.response_mock import Currency
from recharge.models import Transaction
from utils.tests import TestSetup
from datetime import timedelta


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

        self.assertIsNotNone(wallet_task, "wallet task is none")
        self.assertEqual(wallet_task[0].status, "open")
        self.assertEqual(wallet_task[0].transaction_code, transaction1.code)

    def test_update_wallet_balance_candidate_success_with_last_balance_odler_half_hour(self):
        half_hour_ago = timezone.now() - timedelta(minutes=30)
        wallet_balance = baker.make(
            WalletBalance,
            wallet=self.wallet,
            amount=1
        )
        wallet_balance.created_at = half_hour_ago
        wallet_balance.save()

        get_update_wallet_balance_candidate()

        wallet_task = WalletTask.objects.get(
            wallet=self.wallet
        )

        self.assertIsNotNone(wallet_task, "wallet task is none")
        self.assertEqual(wallet_task.status, "open")

    def test_update_wallet_balance_candidate_fail_with_last_balance_not_odler_half_hour(self):
        half_hour_ago = timezone.now() - timedelta(minutes=29)
        wallet_balance = baker.make(
            WalletBalance,
            wallet=self.wallet,
            amount=1
        )
        wallet_balance.created_at = half_hour_ago
        wallet_balance.save()

        get_update_wallet_balance_candidate()

        self.assertFalse(WalletTask.objects.filter(
            wallet=self.wallet
        ).exists())

    def test_update_wallet_balance_with_wallet_task_already_open(self):
        half_hour_ago = timezone.now() - timedelta(minutes=30)
        wallet_balance = baker.make(
            WalletBalance,
            wallet=self.wallet,
            amount=1
        )
        wallet_balance.created_at = half_hour_ago
        wallet_balance.save()

        get_update_wallet_balance_candidate()

        wallet_task = WalletTask.objects.get(
            wallet=self.wallet,
            status="open"
        )

        get_update_wallet_balance_candidate()

        wallet_task1 = WalletTask.objects.get(
            wallet=self.wallet,
            status="open"
        )

        self.assertEqual(wallet_task.created_at, wallet_task1.created_at)
        self.assertEqual(wallet_task.status, "open")
        self.assertEqual(wallet_task1.status, "open")

    def test_update_wallet_balance_with_task_already_success(self):
        half_hour_ago = timezone.now() - timedelta(minutes=30)
        wallet_balance = baker.make(
            WalletBalance,
            wallet=self.wallet,
            amount=1
        )
        wallet_balance.created_at = half_hour_ago
        wallet_balance.save()

        wallet_task = baker.make(
            WalletTask,
            wallet=self.wallet,
            status="open"
        )

        get_update_wallet_balance_candidate()

        wallet_task_after = WalletTask.objects.get(
            wallet=self.wallet,
            status="open"
        )

        self.assertEqual(wallet_task.created_at, wallet_task_after.created_at)
        self.assertEqual(wallet_task.status, wallet_task_after.status)