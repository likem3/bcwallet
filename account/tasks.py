from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from account.models import Wallet, WalletBalance, WalletTask
from recharge.models import Transaction
from django.db.models import OuterRef, Subquery, F, Case, When, CharField, Value
from apis import Switcher
from decimal import Decimal
from django.db import transaction as app_transaction

@shared_task
def create_wallet_task(transaction_code):
    try:
        transaction = Transaction.objects.get(code=transaction_code)
        wallet = transaction.wallet
        WalletTask.create_task(
            wallet=wallet,
            transaction_code=transaction.code,
        )

    except Transaction.DoesNotExist:
        print(f'{transaction_code} is invalid')
        return {
            'status': 'failed',
            'msg': f'{transaction_code} is invalid'
        }

    except Exception as e:
        print(str(e))
        return {
            'status': 'failed',
            'msg': str(e)
        }

@shared_task
def get_update_wallet_balance_candidate():
    try:
        current_time = timezone.now()
        threshold_time = current_time - timedelta(minutes=30)

        last_balance_subquery = WalletBalance.objects.filter(
            wallet_id=OuterRef('id')
        ).order_by('-created_at').values('created_at')[:1]

        wallets = Wallet.objects.exclude(
            wallet_tasks__status='open'
        ).annotate(
            last_balance_update=Subquery(last_balance_subquery)
        ).filter(
            last_balance_update__lte=threshold_time
        ).distinct()

        if not wallets:
            return {
                'wallet_ids': []
            }

        wallet_tasks = []
        wallet_ids = []

        for wallet in wallets:
            wallet_ids.append(wallet.id)
            wallet_tasks.append(
                WalletTask(
                    wallet=wallet
                )
            )

        wallet_task_in = WalletTask.objects.filter(wallet_id__in=wallet_ids)
        if wallet_task_in:
            wallet_task_in.update(status='cencel')

        WalletTask.objects.bulk_create(
            wallet_tasks
        )

        return {
            'wallet_ids': wallet_ids,
        }

    except Exception as e:
        print(str(e))

@shared_task
@app_transaction.atomic
def update_wallet_balance():
    candidates = WalletTask.objects.filter(status='open').order_by('-created_at')[:10]

    task_update = []
    balance_update = []
    affected_wallet_id = []
    success_task_id = []
    transactions_candidate = {}
    balance_update_created_at = []

    for candidate in candidates:
        affected_wallet_id.append(candidate.wallet.id)

        wallet = candidate.wallet
        symbol = wallet.currency_symbol
        std = wallet.currency_std
        address = wallet.address
        network = wallet.network

        try:
            last_balances = wallet.balance
            last_balance = last_balances.latest('created_at')
            last_balance_amount = round(Decimal(last_balance.amount), 10)
        except WalletBalance.DoesNotExist:
            last_balance = None
            last_balance_amount = round(Decimal(0), 10)

        switcher = Switcher.handler(symbol=symbol, std=std)
        handler = switcher()

        try:
            if network == 'mainnet':
                balance = handler.get_balance(address)
            else:
                balance = handler.get_balance_test(address)

        except Exception as e:
            candidate.attemp += 1
            candidate.status = 'fail' if candidate.attemp >= 3 else 'open'
            task_update.append(candidate)
            print(str(e))
            continue

        balance = round(Decimal(balance), 10)

        print(f'lb: {last_balance_amount}\nbn:{balance}')
        if last_balance_amount == balance:
            if not candidate.transaction_code or candidate.attemp > 3:
                candidate.status = 'cancel'
                candidate.attemp = candidate.attemp

                if last_balance:
                    last_balance.created_at = timezone.now()
                    last_balance.updated_at = timezone.now()
                    balance_update_created_at.append(last_balance)

            else:
                candidate.status = candidate.status
                candidate.attemp += 1

            task_update.append(candidate)
            continue

        query = {
            'wallet': candidate.wallet,
            'amount': balance,
            'unit': symbol
        }

        if last_balance:
            query['amount_change'] = Decimal(balance - last_balance_amount)
            query['last_updated_at'] = last_balance.updated_at
        else:
            query['amount_change'] = balance
            query['last_updated_at'] = timezone.now()

        balance_update.append(WalletBalance(
            **query
        ))

        # Update transaction if wallet balance change same or bigger transaction amount
        if candidate.transaction_code:
            transactions_candidate[candidate.transaction_code] = query['amount_change']

        success_task_id.append(candidate.id)
    
    try:
        if task_update:
            WalletTask.objects.bulk_update(
                task_update,
                ['attemp', 'status', 'created_at']
            )

        if balance_update:
            WalletBalance.objects.bulk_create(
                balance_update
            )

        if success_task_id:
            WalletTask.objects.filter(id__in=success_task_id).update(status='success')

        # updating transaction success
        if transactions_candidate:
            update_transactions_status_success.delay(transactions_candidate)

        if balance_update_created_at:
            WalletBalance.objects.bulk_update(
                balance_update_created_at,
                ['created_at', 'updated_at']
            )

        return {
            'affected_wallet_id': affected_wallet_id,
            'success_task_id': success_task_id,
            'transactions_candidate': transactions_candidate,
        }
    except Exception as e:
        print(str(e))
        return {
            'status': 'task_failed'
        }


@shared_task
def update_transactions_status_success(transactions_data={}):
    transactions = Transaction.objects.filter(
        code__in=transactions_data.keys(),
        status='pending'
    )
    trx_update_data = []
    trx_ids_updated = []
    if transactions:
        for trx in transactions:
            balance_in = transactions_data.get(trx.code, 0)
            if balance_in and Decimal(balance_in) >= Decimal(trx.amount):
                trx.status = 'completed'
                trx_update_data.append(trx)
                trx_ids_updated.append({
                    trx.code: balance_in
                })

    if trx_update_data:
        Transaction.objects.bulk_update(
            trx_update_data,
            ['status']
        )
    
    return trx_ids_updated


@shared_task
def update_transaction_status_failed():
    # Calculate the time threshold (30 minutes ago)
    threshold = timezone.now() - timedelta(minutes=30)

    num_affected = Transaction.objects.filter(
        expired_at__lt=threshold, status='pending'
    ).update(
        status='failed'
    )

    return {
        'total_trx_updated_to_fail': num_affected
    }