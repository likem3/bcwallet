from celery import shared_task

from account.models import Wallet, WalletTask
from recharge.models import Transaction
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import requests
from requests.exceptions import HTTPError

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
                trx_update_data.append(trx)
                trx_ids_updated.append({trx.code: balance_in})

    if trx_update_data:
        Transaction.objects.bulk_update(trx_update_data, ["status"])

    return trx_ids_updated


@shared_task
def update_transaction_status_failed():
    # Calculate the time threshold (30 minutes ago)
    threshold = timezone.now() - timedelta(minutes=30)

    trxs = Transaction.objects.filter(
        expired_at__lt=threshold, status="pending"
    )
    for trx in trxs:
        # callback_url = trx.get_notif_parameters_url(merchant_code=trx.merchant.code, status="failed")
        # execute_callback_url_transaction(callback_url)
        # breakpoint()
        # # execute_callback_url_transaction.delay(args=(callback_url,))
        # print("url callback : ", callback_url)
        pass

    trxs.update(status="failed")

    return {"total_trx_updated_to_fail": trxs}


@shared_task
def execute_callback_url_transaction(url=None):
    if url:
        try:
            response = requests.get(url, timeout=1)

            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "url": url,
                }
            
            else:
                return {
                    "status": "failed",
                    "url": url,
                    "status_code": response.status_code
                }

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')

        except Exception as err:
            print(f'Other error occurred: {err}')

