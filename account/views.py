from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Account, Wallet
from account.schemas import create_wallet_schema, get_account_list_schema
from account.serializers import AccountSerializer, CreateAccountSerializer, WalletSerializer
from utils.paginations import SizePagePagination
from utils.mixins import DetailMultipleFieldLookupMixin


class UserListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Account.objects.filter(status="active")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["merchant__code", "user_id", "email", "username"]
    ordering_fields = ["id", "-id", "created_at", "-created_at", "user_id"]
    pagination_class = SizePagePagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateAccountSerializer
        return AccountSerializer

    @swagger_auto_schema(**get_account_list_schema)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDetailSuspendView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "suspended"
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailMerchantView(DetailMultipleFieldLookupMixin, generics.RetrieveDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer
    lookup_query_fields = {
        'merchant_code': 'merchant__code',
        'user_id': 'user_id',
    }
    lookup_fields = ['merchant_code', 'user_id']

    @swagger_auto_schema(operation_id="merchant_user_read")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="merchant_user_delete")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "suspended"
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailSuspendUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.filter(status="active")
    serializer_class = AccountSerializer
    lookup_field = "user_id"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "suspended"
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WalletListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["user_id", "address", "label"]
    search_fields = ["user_id", "address", "label"]
    ordering_fields = ["id", "-id", "created_at", "-created_at", "user_id", "label"]
    pagination_class = SizePagePagination

    @swagger_auto_schema(**create_wallet_schema)
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class WalletDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer


class WalletListByUserIDView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.filter(status="active", account__status="active")
    serializer_class = WalletSerializer

    def get_queryset(self):
        return self.queryset.filter(account__user_id=self.kwargs.pop("user_id"))
