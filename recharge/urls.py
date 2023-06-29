from django.urls import path
from recharge.views import InitiateTransactionView, CreateDepositTransactionView

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
    path(
        "transaction/withdrawal/",
        CreateDepositTransactionView.as_view(),
        name="create-withdrawal-transaction",
    ),
]
