from datetime import timedelta
from decimal import Decimal

import requests
from celery import shared_task
from django.utils import timezone
from requests.exceptions import HTTPError

from account.models import Wallet, WalletTask
from recharge.models import Transaction
from utils.handlers import get_transaction_notif_url


@shared_task
def create_transaction_task(transaction_id, wallet_id):
    try:
        transaction = Transaction.objects.get(transaction_id)
        wallet = Wallet.objects.get(wallet_id)
        WalletTask.create_task(transaction=transaction, wallet=wallet)

    except Transaction.DoesNotExist:
        print(f"{transaction_id} is invalid")

    except Wallet.DoesNotExist:
        print(f"{wallet_id} is invalid")

    except Exception as e:
        print(str(e))


@shared_task
def update_transactions_status_success(transactions_data={}):
    transactions = Transaction.objects.filter(
        code__in=transactions_data.keys(), status="pending"
    )
    trx_update_data = []
    trx_ids_updated = []
    if transactions:
        for trx in transactions:
            balance_in = transactions_data.get(trx.code, 0)
            if balance_in and Decimal(balance_in) >= Decimal(trx.amount):
                trx.status = "completed"
                url = get_transaction_notif_url(trx=trx, status="completed")
                if url:
                    execute_callback_url_transaction.delay(args=(url,))

                trx_update_data.append(trx)
                trx_ids_updated.append({trx.code: balance_in})

    if trx_update_data:
        Transaction.objects.bulk_update(trx_update_data, ["status"])

    return trx_ids_updated


@shared_task
def update_transaction_status_failed():
    # Calculate the time threshold (30 minutes ago)
    threshold = timezone.now() - timedelta(minutes=30)

    trxs = Transaction.objects.filter(expired_at__lt=threshold, status="pending")
    if trxs:
        for trx in trxs:
            url = get_transaction_notif_url(trx=trx, status="failed")
            if url:
                execute_callback_url_transaction.delay(url=url)

        trxs.update(status="failed")

    return {"total_trx_updated_to_fail": trxs if trxs else 0}


@shared_task
def execute_callback_url_transaction(url=None):
    result = {"url": url}
    if url:
        try:
            response = requests.get(url, timeout=1)

            if response.status_code in [200, 201]:
                result["status"] = "success"

            else:
                result["status"] = "failed"
                result["status_code"] = response.status_code

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            result["status"] = "failed"
            result["message"] = str(http_err)

        except Exception as err:
            result["status"] = "failed"
            result["message"] = str(err)

    return result
