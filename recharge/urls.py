from django.urls import path
from recharge.views import (
    InitiateTransactionView,
    CreateDepositTransactionView,
    TransactionListByUserIDView,
    TransactionDetailByUserIDView,
    # UpdateReceiptIdDepositTransactionView
)

urlpatterns = [
    path(
        "recharge/wallet/",
        InitiateTransactionView.as_view(),
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
    # path(
    #     'transaction/<int:user_id>/<str:code>/receipt/',
    #     UpdateReceiptIdDepositTransactionView.as_view(),
    #     name="user-transaction-update-recipe_id"
    # ),
]
