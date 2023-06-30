from rest_framework import generics
from account.serializers import AccountSerializer, WalletSerializer
from account.models import Account, Wallet
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from account.schemas import create_wallet_schema
from django_filters.rest_framework import DjangoFilterBackend

class UserListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'user_id', 'email', 'status']
    search_fields = ['user_id', 'email', 'username']
    ordering_fields = ['id', 'created_at', 'user_id']


class UserDetailSuspendView(generics.RetrieveDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "suspended"
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailSuspendUserView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer
    lookup_field = "user_id"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "suspended"
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WalletListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer

    @swagger_auto_schema(**create_wallet_schema)
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class WalletDetailView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer


class WalletListByUserIDView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer

    def get_queryset(self):
        return self.queryset.filter(account__user_id=self.kwargs.pop("user_id"))
