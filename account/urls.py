from django.urls import path
from account.views import (
    UserCreateView,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserSuspendView,
    WalletListView,
    WalletDetailView,
    WalletCreateView,
)

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("create/", UserCreateView.as_view(), name="user-create"),
    # path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # path("<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    # path("<int:pk>/suspend/", UserSuspendView.as_view(), name="user-update"),
    # path("wallets/", WalletListView.as_view(), name="wallets-list"),
    # path("wallets/create/", WalletCreateView.as_view(), name="wallets-create"),
    # path("wallets/<int:pk>/", WalletDetailView.as_view(), name="wallets-detail"),
    # path('wallets/<int:pk>/update/', WalletUpdateView.as_view(), name='wallets-update'),
    # path('wallets/<int:pk>/suspend/', UserSuspendView.as_view(), name='user-update'),
]
