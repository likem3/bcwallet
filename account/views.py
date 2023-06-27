from rest_framework import generics
from account.serializers import AccountSerializer, WalletSerializer
from account.models import Account, Wallet
from rest_framework.response import Response
from rest_framework import status


class UserListView(generics.ListAPIView):
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer


class UserDetailByIDView(generics.RetrieveAPIView):
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer
    lookup_field = "user_id"


class UserCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer


class UserSuspendView(generics.DestroyAPIView):
    queryset = Account.objects.filter(status__in=["active", "nonactive"])
    serializer_class = AccountSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "suspended"
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSuspendByUserIDView(generics.DestroyAPIView):
    queryset = Account.objects.filter(status__in=["active", "nonactive"])
    lookup_field = "user_id"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "suspended"
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WalletCreateView(generics.CreateAPIView):
    serializer_class = WalletSerializer


class WalletListView(generics.ListAPIView):
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer


class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer


class WalletListByUserIDView(generics.ListAPIView):
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer
    lookup_field = "account__user_id"
