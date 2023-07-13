from recharge.models import Transaction
from account.models import Wallet, WalletTask
from celery import shared_task


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
def sum(a, b):
    print(f"{a + b}")
    return {"result": a + b}
