from django.urls import path

from recharge.views import (CreateDepositTransactionView, CurrencyListClass,
                            DetailUpdateDepostiTransactionOriginCodeView,
                            DetailUpdateDepostiTransactionView)

urlpatterns = [
    path(
        "transactions/deposit/",
        CreateDepositTransactionView.as_view(),
        name="create-deposit-transaction",
    ),
    path(
        "transactions/deposit/<str:code>",
        DetailUpdateDepostiTransactionView.as_view(),
        name="detail-deposit-transaction",
    ),
    path(
        "transactions/deposit/origin/<str:origin_code>/",
        DetailUpdateDepostiTransactionOriginCodeView.as_view(),
        name="detail-deposit-transaction-origin",
    ),
    path("currencies/", CurrencyListClass.as_view(), name="currency-list"),
]
