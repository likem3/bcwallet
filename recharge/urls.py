from django.urls import path
from recharge.views import (
    DepositRechargeView,
    CreateDepositTransactionView,
    TransactionListByUserIDView,
    TransactionDetailByUserIDView,
    CurrencyListClass,
)

urlpatterns = [
    path(
        "recharge/wallet/",
        DepositRechargeView.as_view(),
        name="get-deposit-wallet",
    ),
    path(
        "transaction/deposit/",
        CreateDepositTransactionView.as_view(),
        name="create-deposit-transaction",
    ),
    # path(
    #     "transaction/withdrawal/",
    #     CreateDepositTransactionView.as_view(),
    #     name="create-withdrawal-transaction",
    # ),
    path(
        "transaction/<int:user_id>/",
        TransactionListByUserIDView.as_view(),
        name="user-transaction-list",
    ),
    path(
        "transaction/<int:user_id>/<str:code>/",
        TransactionDetailByUserIDView.as_view(),
        name="user-transaction-detail",
    ),
    path(
        'currencies/',
        CurrencyListClass.as_view(),
        name="currency-list"
    ),
]
