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
    failed_wallet_ids = []
    balance_update = []
    affected_wallet_id = []
    success_wallet_id = []
    transactions_candidate = {}
    for candidate in candidates:
        affected_wallet_id.append(candidate.wallet.id)
        symbol = candidate.wallet.currency_symbol
        std = candidate.wallet.currency_std
        address = candidate.wallet.address
        network = candidate.wallet.network

        switcher = Switcher.handler(symbol=symbol, std=std)
        handler = switcher()

        try:
            if network == 'mainnet':
                balance = handler.get_balance(address)
            else:
                balance = handler.get_balance_test(address)
        except Exception as e:
            print(str(e))
            failed_wallet_ids.append(candidate.wallet.id)
            continue

        query = {
            'wallet': candidate.wallet,
            'amount': Decimal(balance),
            'unit': symbol
        }

        balance_obj_list = candidate.wallet.balance.order_by('-created_at')
        if balance_obj_list:
            balance_obj = balance_obj_list[0]
            last_balance = balance_obj.amount if balance_obj.amount else 0
            query['amount_change'] = Decimal(Decimal(balance) - Decimal(last_balance))
            query['last_updated_at'] = balance_obj.updated_at
        else:
            query['amount_change'] = Decimal(balance)
            query['last_updated_at'] = timezone.now()


        balance_update.append(WalletBalance(
            **query
        ))

        # Update transaction if wallet balance change same or bigger transaction amount
        if candidate.transaction_code:
            transactions_candidate[candidate.transaction_code] = query['amount_change']

        success_wallet_id.append(candidate.wallet.id)
    
    try:
        WalletTask.objects.filter(wallet__id__in=failed_wallet_ids).update(
            attemp=F('attemp') + 1,
            status=Case(
                When(attemp__gte=3, then=Value('fail')),
                default=F('status'),
                output_field=CharField()
            )
        )
        WalletBalance.objects.bulk_create(
            balance_update
        )
        WalletTask.objects.filter(wallet__id__in=success_wallet_id).update(status='success')

        # updating transaction success
        update_transactions_status_success.delay(transactions_candidate)

        return {
            'affected_wallet_id': affected_wallet_id,
            'failed_wallet_id': failed_wallet_ids,
            'success_wallet_id': success_wallet_id,
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
                trx_update_data.append({
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