from rest_framework import generics
from account.serializers import AccountSerializer, WalletSerializer
from account.models import Account, Wallet


class UserListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer


class UserUpdateView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    http_method_names = ["patch"]


class UserSuspendView(generics.DestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "suspended"
        instance.save()
        return self.destroy(request, *args, **kwargs)


class WalletCreateView(generics.CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletUpdateView(generics.UpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "id"


class WalletListView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "id"
