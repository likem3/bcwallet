from django.urls import path
from account.views import (
    UserCreateView,
    UserListView,
    UserDetailView,
    UserDetailByIDView,
    UserSuspendView,
    UserSuspendByUserIDView,
    WalletListView,
    WalletDetailView,
    WalletCreateView,
    WalletListByUserIDView
)

urlpatterns = [
    path("account/", UserListView.as_view(), name="user-list"),
    path("account/create/", UserCreateView.as_view(), name="user-create"),
    path("account/<int:pk>/", UserDetailByIDView.as_view(), name="user-detail-by-id"),
    path("account/user/<int:user_id>/", UserDetailView.as_view(), name="user-detail-by-user_id"),
    path("account/<int:pk>/suspend/", UserSuspendView.as_view(), name="user-update"),
    path("account/user/<int:user_id>/suspend/", UserSuspendByUserIDView.as_view(), name="user-update"),

    path("wallets/", WalletListView.as_view(), name="wallets-list"),
    path("wallets/create/", WalletCreateView.as_view(), name="wallets-create"),
    path("wallets/<int:pk>/", WalletDetailView.as_view(), name="wallets-detail"),
    path("wallets/user/<int:user_id>/", WalletListByUserIDView.as_view(), name="wallets-user-list"),
]
