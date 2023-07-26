from django.urls import path

from account.views import (
    UserDetailMerchantView,
    UserDetailSuspendView,
    UserListCreateView,
    WalletDetailView,
    WalletListByUserIDView,
    WalletListCreateView,
)

urlpatterns = [
    path("accounts/", UserListCreateView.as_view(), name="user-list-create"),
    path(
        "accounts/<int:pk>/",
        UserDetailSuspendView.as_view(),
        name="user-detail-suspend-by-id",
    ),
    path(
        "accounts/<int:merchant_code>/<int:user_id>/",
        UserDetailMerchantView.as_view(),
        name="user-detail-suspend-by-merchant_code-user_id",
    ),
    path("wallets/", WalletListCreateView.as_view(), name="wallets-list-create"),
    path("wallets/<int:pk>/", WalletDetailView.as_view(), name="wallets-detail"),
    path(
        "wallets/user/<int:user_id>/",
        WalletListByUserIDView.as_view(),
        name="wallets-user-list",
    ),
]
