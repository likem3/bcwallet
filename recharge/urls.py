from django.urls import path
from recharge.views import InitiateTransactionView

urlpatterns = [
    path(
        "recharge/wallet/",
        InitiateTransactionView.as_view(),
        name="deposit-wallet",
    ),
]
