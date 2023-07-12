from django.urls import path
from recharge.views import (
    CreateDepositTransactionView,
    TransactionListByUserIDView,
    CurrencyListClass,
)

urlpatterns = [
    path(
        "transactions/deposit/",
        CreateDepositTransactionView.as_view(),
        name="create-deposit-transaction",
    ),
    path(
        "transactions/user/<int:user_id>/",
        TransactionListByUserIDView.as_view(),
        name="user-transaction-list",
    ),
    path(
        'currencies/',
        CurrencyListClass.as_view(),
        name="currency-list"
    ),
]
